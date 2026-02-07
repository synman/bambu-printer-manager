"""
`bambustate` provides a unified, thread-safe representation of a Bambu Lab printer's
operational state, synchronized via MQTT telemetry.
"""

import logging
import time
from dataclasses import asdict, dataclass, field, replace
from typing import Any

from bpm.bambuconfig import BambuConfig
from bpm.bambutools import (
    ActiveTool,
    AirConditioningMode,
    AMSHeatingState,
    AMSModel,
    ExtruderInfoState,
    ExtruderStatus,
    TrayState,
    decodeError,
    decodeHMS,
    getAMSModelBySerial,
    parseAMSInfo,
    parseAMSStatus,
    parseExtruderInfo,
    parseExtruderStatus,
    parseExtruderTrayState,
    parseStage,
    scaleFanSpeed,
    unpackTemperature,
)

logger = logging.getLogger("bpm")


@dataclass
class PrinterCapabilities:
    """Discovery features based on hardware block presence in telemetry."""

    has_ams: bool = False
    """True if an AMS unit is detected. Population: `ams` block presence."""
    has_lidar: bool = False
    """True if printer has LiDAR. Population: `xcam` block presence."""
    has_camera: bool = False
    """True if printer has camera. Population: Hardcoded True for H2D."""
    has_dual_extruder: bool = False
    """True if H2D architecture. Population: `len(extruder_root.info) > 1`."""
    has_air_filtration: bool = False
    """True if airduct exists. Population: `airduct` block presence."""
    has_chamber_temp: bool = False
    """True if CTC exists. Population: `ctc_root` block presence."""


@dataclass
class ExtruderState:
    """State for an individual physical extruder toolhead."""

    id: int = 0
    """Physical ID. Population: `int(r.get("id"))`."""
    temp: float = 0.0
    """Current Temp. Population: `unpackTemperature(r.temp)`."""
    temp_target: int = 0
    """Target Temp. Population: `unpackTemperature(r.temp)`."""
    info_bits: int = 0
    """Raw bitmask. Population: `int(r.get("info"))`."""
    state: ExtruderInfoState = ExtruderInfoState.NO_NOZZLE
    """Filament status. Population: `parseExtruderInfo`."""
    status: ExtruderStatus = ExtruderStatus.IDLE
    """Op state. Population: `parseExtruderStatus`."""
    active_tray_id: int = -1
    """The active tray for this extruder. Population: `int(r.hnow)`"""
    target_tray_id: int = -1
    """The target tray for this extruder. Population: `int(r.htar >> 8)`."""
    tray_state: TrayState = TrayState.LOADED
    """The tray state of this extruder"""
    assigned_to_ams_id: int = -1
    """The id of the ams associated with this extruder"""


@dataclass
class AMSUnitState:
    """State information about an individual AMS unit."""

    ams_id: int
    """Unique ID. Population: `str(ams_idx)`."""
    chip_id: str = ""
    """Hardware serial. Population: `m.get("sn")`."""
    model: AMSModel = AMSModel.UNKNOWN
    """`AMSModel` for this unit"""
    temp_actual: float = 0.0
    """Actual temp. Population: `float(r.get("temp"))`."""
    temp_target: int = 0
    """Target drying temp. Population: `trays[0].drying_temp`."""
    humidity_index: int = 0
    """Humidity index. Population: `int(float(r.get("humidity")))`."""
    humidity_raw: int = 0
    """Raw humidity. Population: `int(float(r.get("humidity_raw")))`."""
    ams_info: int = 0
    """Underlying ams info value"""
    heater_state: AMSHeatingState = AMSHeatingState.NO_POWER
    """The computed state of the AMS's heater"""
    raw_extruder_id: int = -1
    """Raw extruder ID extracted from ams_info"""
    dry_time: int = 0
    """Minutes left. Population: `int(float(r.get("dry_time")))`."""
    tray_exists: list[bool] = field(default_factory=lambda: [False] * 4)
    """Slot presence. Population: Shifting `tray_exist_bits`."""
    assigned_to_extruder: ActiveTool = ActiveTool.SINGLE_EXTRUDER
    """Target tool computed from raw_extruder_id"""


@dataclass
class BambuClimate:
    """Contains all climate related attributes"""

    bed_temp: float = 0.0
    """Bed temp. Population: `float(p.get("bed_temper"))`."""
    bed_temp_target: int = 0
    """Bed target. Population: `float(p.get("bed_target_temper"))`."""
    airduct_mode: int = -1
    """Raw current mode. Population: airduct.modeCur."""
    airduct_sub_mode: int = -1
    """Raw sub mode. Population: airduct.subMode."""
    chamber_temp: float = 0.0
    """Chamber temp. Population: `unpackTemperature(ctc_root.info.temp)`."""
    chamber_temp_target: int = 0
    """Chamber target. Population: `unpackTemperature(ctc_root.info.temp)`."""
    air_conditioning_mode: AirConditioningMode = AirConditioningMode.NOT_SUPPORTED
    """The mode the printer's AC is in if equipped with one."""
    part_cooling_fan_speed_percent: int = 0
    """Part fan %. Population: `scaleFanSpeed(p.cooling_fan_speed)`."""
    part_cooling_fan_speed_target_percent: int = 0
    """Part target %. Population: `scaleFanSpeed(p.cooling_fan_target_speed)`."""
    aux_fan_speed_percent: int = 0
    """aux fan %. Population: `scaleFanSpeed(p.big_fan1_speed)`."""
    exhaust_fan_speed_percent: int = 0
    """Exhaust (chamber) fan %. Population: `scaleFanSpeed(p.big_fan2_speed)`."""
    heatbreak_fan_speed_percent: int = 0
    """Heatbreak fan %. Population: `scaleFanSpeed(p.heatbreak_fan_speed)`."""
    zone_intake_open: bool = False
    """Heater power. Population: airduct.parts ID 96."""
    zone_part_fan_percent: int = 0
    """Internal %. Population: `airduct.parts` ID 16."""
    zone_aux_percent: int = 0
    """aux %. Population: `airduct.parts` ID 32."""
    zone_exhaust_percent: int = 0
    """Exhaust %. Population: `airduct.parts` ID 48."""
    zone_top_vent_open: bool = False
    """Top vent status - derived from exhaust fan on and cooling ac mode."""
    is_chamber_door_open: bool = False
    """ For printers that support it (see `BambuConfig.has_chamber_door_sensor`), reports whether the chamber door is open """


@dataclass
class BambuState:
    """Representation of the Bambu printer state synchronized via MQTT."""

    gcode_state: str = "IDLE"
    """Execution state. Population: `p.get("gcode_state")`."""
    current_stage_id: int = 0
    """Stage numeric ID. Population: `int(p.get("stg_cur"))`."""
    current_stage_name: str = ""
    """Stage human name. Population: `parseStage`."""
    print_percentage: int = 0
    """Completion %. Population: `int(p.get("mc_percent"))`."""
    monotonic_start_time: int = -1
    """The monotonic time stamp of when this job started"""
    elapsed_minutes: int = 0
    """The elapsed time in minutes for this (or the last) job"""
    remaining_minutes: float = 0.0
    """Time remaining in minutes for the current job. Population: `int(p.get("mc_remaining_time"))`."""
    current_layer: int = 0
    """Layer index. Population: `int(p.get("layer_num"))`."""
    total_layers: int = 0
    """Layer total. Population: `int(p.get("total_layer_num"))`."""
    active_ams_id: int = -1
    """Current active AMS unit id"""
    active_tray_id: int = 255
    """Current tray. Population: Computed in Tool Handoff."""
    active_tray_state: TrayState = TrayState.UNLOADED
    """Loading enum. Population: `ExtruderInfoState` check."""
    active_tray_state_name: str = TrayState.UNLOADED.name
    """Loading string. Population: `active_tray_state.name`."""
    target_tray_id: int = -1
    """Next tray. Population: Stage-specific targeting logic."""
    active_tool: ActiveTool = ActiveTool.SINGLE_EXTRUDER
    """Active toolhead. Population: `extruder_root.state` shift."""
    is_external_spool_active: bool = False
    """Ext spool flag. Population: `active_tray_id in [254, 255]`."""
    active_nozzle_temp: float = 0.0
    """Nozzle temp. Population: Handoff from `a_ext` or `p`."""
    active_nozzle_temp_target: int = 0
    """Nozzle target. Population: Handoff from `a_ext` or `p`."""
    ams_status_raw: int = 0
    """Raw AMS status. Population: `int(p.get("ams_status"))`."""
    ams_status_text: str = ""
    """Human AMS status. Population: `parseAMSStatus`."""
    ams_exist_bits: int = 0
    """AMS mask. Population: `int(ams_root.ams_exist_bits, 16)`."""
    ams_connected_count: int = 0
    """AMS count. Population: `bin(ams_exist_bits).count("1")`."""
    ams_units: list[AMSUnitState] = field(default_factory=list)
    """Unit details. Population: Result of unit iteration."""
    extruders: list[ExtruderState] = field(default_factory=list)
    """Extruder details. Population: Result of extruder iteration."""
    print_error: int = 0
    """Main error. Population: `int(p.get("print_error"))`."""
    hms_errors: list[dict] = field(default_factory=list)
    """HMS list. Population: `decodeHMS` + `decodeError` synthesis."""
    capabilities: PrinterCapabilities = field(default_factory=PrinterCapabilities)
    """Machine flags. Population: `PrinterCapabilities` instantiation."""
    climate: BambuClimate = field(default_factory=BambuClimate)
    """Contains all climate related attributes"""
    stat: str = "0"
    fun: str = "0"

    @classmethod
    def fromJson(
        cls, data: dict[str, Any], current_state: "BambuState", config: BambuConfig
    ) -> "BambuState":
        """Parses root MQTT payloads into a unified BambuState with 100% attribute traceability."""

        base = current_state if current_state else cls()
        info = data.get("info", {})
        p = data.get("print", {})

        if (
            p
            and p.get("command", "") == "ams_filament_drying"
            and p.get("result", "") == "success"
        ):
            ams_id = p.get("ams_id", -1)
            ams = next((u for u in base.ams_units if u.ams_id == ams_id), None)
            if ams:
                ams.temp_target = int(p.get("temp", 0))

        ams_root = p.get("ams", {})
        device = p.get("device", {})

        extruder_root = device.get("extruder", {})
        ctc_root = device.get("ctc", {})
        airduct_root = device.get("airduct", {})

        modules = info.get("module", [])
        updates = {}

        # CAPABILITIES
        caps = asdict(base.capabilities)
        if ctc_root:
            caps["has_chamber_temp"] = True
        if "ams" in ams_root or "ams" in p:
            caps["has_ams"] = True
        if airduct_root:
            caps["has_air_filtration"] = True
        if len(extruder_root.get("info", [])) > 1:
            caps["has_dual_extruder"] = True

        caps["has_lidar"] = "xcam" in p or "xcam" in info
        caps["has_camera"] = True
        updates["capabilities"] = PrinterCapabilities(**caps)

        climate = asdict(base.climate)
        updates["climate"] = BambuClimate(**climate)

        # STATUS & PROGRESS
        updates["gcode_state"] = p.get("gcode_state", base.gcode_state)
        updates["current_stage_id"] = int(p.get("stg_cur", base.current_stage_id))
        updates["current_stage_name"] = parseStage(updates["current_stage_id"])

        updates["fun"] = p.get("fun", base.fun)
        fun = int(updates["fun"], 16)
        config.has_chamber_door_sensor = bool((fun >> 12) & 0x01)

        if config.has_chamber_door_sensor:
            updates["stat"] = p.get("stat", base.stat)
            stat = int(updates["stat"], 16)
            updates["climate"].is_chamber_door_open = bool((stat >> 23) & 0x01)

        if (
            updates["gcode_state"] in ("FAILED", "FINISH")
            and updates["gcode_state"] != base.gcode_state
        ):
            updates["monotonic_start_time"] = -1
        elif (
            updates["gcode_state"] in ("PREPARE", "RUNNING")
            and base.monotonic_start_time == -1
        ):
            updates["monotonic_start_time"] = time.monotonic()
        else:
            if updates["gcode_state"] in ("PREPARE", "RUNNING"):
                updates["elapsed_minutes"] = (
                    time.monotonic()
                    - updates.get("monotonic_start_time", base.monotonic_start_time)
                ) / 60.0

                updates["current_layer"] = int(p.get("layer_num", base.current_layer))
                updates["print_percentage"] = int(
                    p.get("mc_percent", base.print_percentage)
                )
                updates["total_layers"] = int(p.get("total_layer_num", base.total_layers))
                updates["remaining_minutes"] = float(
                    p.get("mc_remaining_time", base.remaining_minutes)
                )

        # AIRDUCT
        if airduct_root:
            updates["climate"].airduct_mode = int(
                airduct_root.get("modeCur", base.climate.airduct_mode)
            )
            updates["climate"].airduct_sub_mode = int(
                airduct_root.get("subMode", base.climate.airduct_sub_mode)
            )

            if updates["climate"].airduct_mode == 1:
                updates["climate"].air_conditioning_mode = AirConditioningMode.HEAT_MODE
            elif updates["climate"].airduct_mode == 0:
                updates["climate"].air_conditioning_mode = AirConditioningMode.COOL_MODE
                base.climate.chamber_temp_target = 0
            else:
                updates[
                    "climate"
                ].air_conditioning_mode = AirConditioningMode.NOT_SUPPORTED

            parts = {part["id"]: part["state"] for part in airduct_root.get("parts", [])}

            updates["climate"].zone_part_fan_percent = parts.get(
                16, base.climate.zone_part_fan_percent
            )
            updates["climate"].zone_aux_percent = parts.get(
                32, base.climate.zone_aux_percent
            )
            updates["climate"].zone_exhaust_percent = parts.get(
                48, base.climate.zone_exhaust_percent
            )

            zone_intake_open = parts.get(96, -1)
            updates["climate"].zone_intake_open = zone_intake_open not in (-1, 0)

            updates["climate"].zone_top_vent_open = bool(
                updates["climate"].zone_exhaust_percent > 0
                and not updates["climate"].zone_intake_open
            )

        # THERMALS & CTC DECODING
        updates["climate"].bed_temp = float(p.get("bed_temper", base.climate.bed_temp))
        updates["climate"].bed_temp_target = int(
            p.get("bed_target_temper", base.climate.bed_temp_target)
        )

        ctc_temp_target = 0.0
        if ctc_root:
            ctc_temp_raw = unpackTemperature(ctc_root.get("info", {}).get("temp", 0.0))
            ctc_temp = ctc_temp_raw[0]
            ctc_temp_target = ctc_temp_raw[1]
            updates["climate"].chamber_temp = ctc_temp
            updates["climate"].chamber_temp_target = int(ctc_temp_target)
        else:
            updates["climate"].chamber_temp = base.climate.chamber_temp

        if (
            ctc_temp_target == 0
            and updates["climate"].air_conditioning_mode != AirConditioningMode.HEAT_MODE
        ):
            updates["climate"].chamber_temp_target = base.climate.chamber_temp_target

        # EXTRUDERS
        new_extruders = []
        if "info" in extruder_root:
            for new_ext in extruder_root["info"]:
                raw_t = int(new_ext.get("temp", 0))
                act_t, tar_t = unpackTemperature(raw_t)

                sn = int(new_ext.get("snow", -1))
                hn = int(new_ext.get("hnow", -1))

                st = int(new_ext.get("star", -1))
                ht = int(new_ext.get("htar", -1))

                ext = ExtruderState()
                ext.id = int(new_ext.get("id", 0))

                ext.temp = act_t
                ext.temp_target = int(tar_t)

                ext.info_bits = int(new_ext.get("info", 0))
                ext.state = parseExtruderInfo(ext.info_bits)
                ext.status = parseExtruderStatus(int(new_ext.get("stat", 0)))

                ext.active_tray_id = parseExtruderTrayState(ext.id, hn, sn)
                ext.target_tray_id = parseExtruderTrayState(ext.id, ht, st)

                if base.extruders and len(base.extruders) > ext.id:
                    base_tray_state = base.extruders[ext.id].tray_state
                else:
                    base_tray_state = (
                        TrayState.LOADED
                        if ext.state != ExtruderInfoState.EMPTY
                        else TrayState.UNLOADED
                    )

                if (
                    ext.state == ExtruderInfoState.LOADED
                    and ext.status == ExtruderStatus.ACTIVE
                ):
                    ext.tray_state = TrayState.LOADED
                elif (
                    ext.state == ExtruderInfoState.EMPTY
                    and ext.status == ExtruderStatus.IDLE
                ):
                    ext.tray_state = TrayState.UNLOADED
                elif (
                    ext.state == ExtruderInfoState.LOADED
                    and ext.status == ExtruderStatus.HEATING
                    and base_tray_state not in (TrayState.LOADING, TrayState.UNLOADED)
                ):
                    ext.tray_state = TrayState.UNLOADING
                elif ext.status is not ExtruderStatus.IDLE:
                    ext.tray_state = TrayState.LOADING
                else:
                    ext.tray_state = base.active_tray_state

                new_extruders.append(ext)
        updates["extruders"] = new_extruders if new_extruders else base.extruders

        # TOOL SELECTION
        if "state" in extruder_root:
            raw_t_idx = (int(extruder_root["state"]) >> 4) & 0xF
            if updates["capabilities"].has_dual_extruder:
                updates["active_tool"] = ActiveTool(raw_t_idx)
            else:
                updates["active_tool"] = ActiveTool.SINGLE_EXTRUDER
        else:
            updates["active_tool"] = base.active_tool

        # AMS UNITS
        cur_ams = {u.ams_id: u for u in base.ams_units}

        for m in modules:
            if (
                m.get("name", "").startswith("n3f/")
                or m.get("name", "").startswith("n3s/")
                or m.get("name", "").startswith("ams")
            ):
                ams_id = int(m["name"].split("/")[-1])
                u = cur_ams.get(ams_id, AMSUnitState(ams_id=ams_id))
                u.chip_id = m.get("sn", u.chip_id)
                u.model = getAMSModelBySerial(u.chip_id)
                cur_ams[ams_id] = u

        for ams_u in ams_root.get("ams", []):
            id = int(ams_u.get("id", 0))
            u = cur_ams.get(id, AMSUnitState(ams_id=id))
            u.temp_actual = float(ams_u.get("temp", u.temp_actual))
            u.humidity_index = int(float(ams_u.get("humidity", u.humidity_index)))
            u.humidity_raw = int(float(ams_u.get("humidity_raw", u.humidity_raw)))
            u.dry_time = int(float(ams_u.get("dry_time", u.dry_time)))

            # ugly hack for capturing target temp
            if u.dry_time > 0 and u.temp_target < int(u.temp_actual) - 1:
                u.temp_target = int(u.temp_actual)
            elif u.dry_time == 0:
                u.temp_target = 0

            if "info" in ams_u:
                u.ams_info = int(ams_u["info"])
                p_ams = parseAMSInfo(u.ams_info)

                u.heater_state = p_ams["heater_state"]
                u.raw_extruder_id = p_ams["extruder_id"]

                if updates["capabilities"].has_dual_extruder:
                    u.assigned_to_extruder = ActiveTool(
                        p_ams.get("h2d_toolhead_index", 15)
                    )
                    updates["extruders"][
                        u.assigned_to_extruder.value
                    ].assigned_to_ams_id = u.ams_id

                rb = ams_root.get("tray_exist_bits")
                if rb is not None:
                    eb = int(rb, 16) if isinstance(rb, str) else int(rb)

                    # Calculate the bit shift based on the unit ID
                    # Standard AMS: 0, 1, 2, 3 -> shift 0, 4, 8, 12
                    # AMS-HT: 128, 129, 130, 131 -> shift 16, 20, 24, 28
                    if id >= 128:
                        shift = 16 + (4 * (id - 128))
                        # AMS-HT is a 1-slot unit, so we check only range(1)
                        u.tray_exists = [bool((eb >> shift) & (1 << j)) for j in range(1)]
                    else:
                        shift = 4 * id
                        # Standard AMS is a 4-slot unit, so we check range(4)
                        u.tray_exists = [bool((eb >> shift) & (1 << j)) for j in range(4)]

            cur_ams[id] = u

        updates["ams_units"] = list(cur_ams.values())

        # ACTIVE / TARGET TRAYS AND TOOL TEMP
        # if multi-extruder return the active one
        a_ext = next(
            (e for e in updates["extruders"] if e.id == updates["active_tool"].value),
            None,
        )
        if a_ext:
            updates["active_ams_id"] = (
                a_ext.assigned_to_ams_id if a_ext.active_tray_id not in (254, 255) else -1
            )
            updates["active_tray_id"] = a_ext.active_tray_id
            updates["target_tray_id"] = a_ext.target_tray_id

            updates["active_tray_state"] = a_ext.tray_state

            updates["active_nozzle_temp"] = a_ext.temp
            updates["active_nozzle_temp_target"] = a_ext.temp_target
        else:
            # otherwise process a single extruder printer update
            updates["active_nozzle_temp"] = float(
                p.get("nozzle_temper", base.active_nozzle_temp)
            )
            updates["active_nozzle_temp_target"] = int(
                p.get("nozzle_target_temper", base.active_nozzle_temp_target)
            )
            updates["active_tray_id"] = int(ams_root.get("tray_now", base.active_tray_id))
            if updates["active_tray_id"] == 255:
                updates["active_tray_id"] = -1
                updates["active_tray_state"] = TrayState.UNLOADED
            elif updates["current_stage_id"] == 24:
                updates["active_tray_state"] = TrayState.LOADING
            elif updates["current_stage_id"] == 22:
                updates["active_tray_state"] = TrayState.UNLOADING
            else:
                updates["active_tray_state"] = TrayState.LOADED

        if "active_tray_id" in updates:
            updates["is_external_spool_active"] = updates["active_tray_id"] in [254, 255]
        else:
            updates["is_external_spool_active"] = False

        if "active_tray_state" in updates:
            updates["active_tray_state_name"] = updates["active_tray_state"].name

        # GLOBAL METADATA & FANS
        raw_exist = ams_root.get("ams_exist_bits", base.ams_exist_bits)
        updates["ams_exist_bits"] = (
            int(raw_exist, 16) if isinstance(raw_exist, str) else int(raw_exist)
        )
        updates["ams_connected_count"] = bin(updates["ams_exist_bits"]).count("1")
        updates["ams_status_raw"] = int(p.get("ams_status", base.ams_status_raw))
        updates["ams_status_text"] = parseAMSStatus(updates["ams_status_raw"])

        part_cooling_fan_speed_percent = -1

        if not base.capabilities.has_chamber_temp:
            part_cooling_fan_speed_percent = (
                scaleFanSpeed(p.get("cooling_fan_speed"))
                if p.get("cooling_fan_speed", -1) != -1
                else -1
            )
        else:
            part_cooling_fan_speed_percent = updates["climate"].zone_part_fan_percent

        if part_cooling_fan_speed_percent == -1:
            part_cooling_fan_speed_percent = base.climate.part_cooling_fan_speed_percent

        updates["climate"].part_cooling_fan_speed_percent = part_cooling_fan_speed_percent
        updates["climate"].part_cooling_fan_speed_target_percent = updates[
            "climate"
        ].part_cooling_fan_speed_percent

        heatbreak_fan_speed_percent = scaleFanSpeed(p.get("heatbreak_fan_speed", -1))
        if heatbreak_fan_speed_percent == -1:
            heatbreak_fan_speed_percent = base.climate.heatbreak_fan_speed_percent
        updates["climate"].heatbreak_fan_speed_percent = heatbreak_fan_speed_percent

        exhaust_fan_speed_percent = -1
        if not base.capabilities.has_chamber_temp:
            exhaust_fan_speed_percent = scaleFanSpeed(p.get("big_fan2_speed", -1))
        else:
            exhaust_fan_speed_percent = updates["climate"].zone_exhaust_percent

        if exhaust_fan_speed_percent == -1:
            exhaust_fan_speed_percent = base.climate.exhaust_fan_speed_percent
        updates["climate"].exhaust_fan_speed_percent = exhaust_fan_speed_percent

        aux_fan_speed_percent = -1
        if not base.capabilities.has_chamber_temp:
            aux_fan_speed_percent = scaleFanSpeed(p.get("big_fan1_speed", -1))
        else:
            aux_fan_speed_percent = updates["climate"].zone_aux_percent

        if aux_fan_speed_percent == -1:
            aux_fan_speed_percent = base.climate.aux_fan_speed_percent
        updates["climate"].aux_fan_speed_percent = aux_fan_speed_percent

        # ERROR HANDLING
        updates["print_error"] = int(p.get("print_error", base.print_error))

        if updates["print_error"] != 0:
            decoded_error = decodeError(updates["print_error"])
        else:
            decoded_error = {}
            base.hms_errors = []

        updates["hms_errors"] = decodeHMS(p.get("hms", base.hms_errors))
        if decoded_error and decoded_error not in updates["hms_errors"]:
            updates["hms_errors"].insert(0, decoded_error)

        return replace(base, **updates)
