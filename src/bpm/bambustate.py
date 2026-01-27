"""
`bambustate` provides a unified, thread-safe representation of a Bambu Lab printer's
operational state, synchronized via MQTT telemetry.
"""

import logging
import re
from dataclasses import asdict, dataclass, field, replace
from typing import Any, Optional

from bpm.bambutools import (
    ActiveTool,
    AMSDryingStage,
    ExtruderInfoState,
    ExtruderStatus,
    TrayState,
    decodeError,
    decodeHMS,
    parseAMSInfo,
    parseAMSStatus,
    parseExtruderInfo,
    parseExtruderStatus,
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
    active_tray: int = 255
    """Source ID. Population: `(r.snow >> 8) & 0xFF`."""
    slot_id: int = 255
    """AMS Slot. Population: `r.snow & 0xFF`."""


@dataclass
class AMSUnitState:
    """State information about an individual AMS unit."""

    ams_id: str
    """Unique ID. Population: `str(ams_idx)`."""
    chip_id: str = ""
    """Hardware serial. Population: `m.get("sn")`."""
    is_ams_lite: bool = False
    """True if AMS Lite. Population: `product_name` check."""
    temp_actual: float = 0.0
    """Actual temp. Population: `float(r.get("temp"))`."""
    temp_target: int = 0
    """Target drying temp. Population: `trays[0].drying_temp`."""
    humidity_index: int = 0
    """Humidity index. Population: `int(float(r.get("humidity")))`."""
    humidity_raw: int = 0
    """Raw humidity. Population: `int(float(r.get("humidity_raw")))`."""
    is_online: bool = False
    """Connectivity. Population: `p_ams["is_online"]`."""
    is_powered: bool = False
    """Power status. Population: `p_ams["is_powered"]`."""
    rfid_ready: bool = False
    """RFID status. Population: `p_ams["rfid_ready"]`."""
    hub_sensor_triggered: bool = False
    """Filament at hub. Population: `p_ams["hub_sensor_triggered"]`."""
    humidity_sensor_ok: bool = False
    """Sensor health. Population: `p_ams["humidity_sensor_ok"]`."""
    heater_on: bool = False
    """Heater state. Population: `p_ams["heater_on"]`."""
    circ_fan_on: bool = False
    """Circ fan state. Population: `p_ams["circ_fan_on"]`."""
    exhaust_fan_on: bool = False
    """Exhaust fan state. Population: `p_ams["exhaust_fan_on"]`."""
    dry_time: int = 0
    """Minutes left. Population: `int(float(r.get("dry_time")))`."""
    is_rotating: bool = False
    """Rollers turning. Population: `p_ams["is_rotating"]`."""
    venting_active: bool = False
    """Venting state. Population: `p_ams.get("venting_active")`."""
    high_power_mode: bool = False
    """Power mode. Population: `p_ams.get("high_power_mode")`."""
    hardware_fault: bool = False
    """Fault status. Population: `p_ams["hardware_fault"]`."""
    tray_exists: list[bool] = field(default_factory=lambda: [False] * 4)
    """Slot presence. Population: Shifting `tray_exist_bits`."""
    assigned_to_extruder: ActiveTool = ActiveTool.SINGLE_EXTRUDER
    """Target tool. Population: `ActiveTool(h2d_toolhead_index)`."""
    drying_stage: AMSDryingStage = AMSDryingStage.IDLE
    """Cycle stage. Population: `_resolve_drying_stage`."""


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
    remaining_minutes: int = 0
    """Time left. Population: `int(p.get("mc_remaining_time"))`."""
    current_layer: int = 0
    """Layer index. Population: `int(p.get("layer_num"))`."""
    total_layers: int = 0
    """Layer total. Population: `int(p.get("total_layer_num"))`."""
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
    bed_temp: float = 0.0
    """Bed temp. Population: `float(p.get("bed_temper"))`."""
    bed_temp_target: int = 0
    """Bed target. Population: `float(p.get("bed_target_temper"))`."""
    airduct_mode: int = 0
    """Raw current mode. Population: airduct.modeCur."""
    airduct_sub_mode: int = 0
    """Raw sub mode. Population: airduct.subMode."""
    chamber_temp: float = 0.0
    """Chamber temp. Population: `unpackTemperature(ctc_root.info.temp)`."""
    chamber_temp_target: int = 0
    """Chamber target. Population: `unpackTemperature(ctc_root.info.temp)`."""
    is_chamber_heating: bool = False
    """True if active heating. Population: Bitwise `airduct.state & 0x10`."""
    is_chamber_cooling: bool = False
    """True if active cooling. Population: Bitwise `airduct.state & 0x20`."""
    is_dryer_engaged: bool = False
    """True if subMode Bit 0. Population: airduct.subMode & 0x01."""
    ac_unit_power_percent: int = 0
    """AC/Compressor power. Population: airduct.parts ID 96."""
    part_cooling_fan_speed_percent: int = 0
    """Part fan %. Population: `scaleFanSpeed(p.cooling_fan_speed)`."""
    part_cooling_fan_speed_target_percent: int = 0
    """Part target %. Population: `scaleFanSpeed(p.cooling_fan_target_speed)`."""
    chamber_fan_speed_percent: int = 0
    """Chamber fan %. Population: `scaleFanSpeed(p.big_fan1_speed)`."""
    exhaust_fan_speed_percent: int = 0
    """Exhaust fan %. Population: `scaleFanSpeed(p.big_fan2_speed)`."""
    heatbreak_fan_speed_percent: int = 0
    """Heatbreak fan %. Population: `scaleFanSpeed(p.heatbreak_fan_speed)`."""
    has_active_filtration: bool = False
    """Filter status. Population: Bitwise `airduct.state & 0x08`."""
    airduct_state_raw: int = 0
    """Raw airduct status mask. Population: `device.airduct.state`."""
    zone_internal_percent: int = 0
    """Internal %. Population: `airduct.parts` ID 16."""
    zone_intake_percent: int = 0
    """Intake %. Population: `airduct.parts` ID 32."""
    zone_exhaust_percent: int = 0
    """Exhaust %. Population: `airduct.parts` ID 48."""
    top_vent_open: bool = False
    """Vent status. Population: Bitwise `airduct.state & 0x01`."""
    filter_obstruction_detected: bool = False
    """Filter pressure warning. Population: Bitwise `airduct.state & 0x02`."""
    zone_sync_error: bool = False
    """Alignment error. Population: Bitwise `airduct.state & 0x04`."""
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
    ams_handle_map: dict[int, int] = field(default_factory=dict)
    """Logical handles. Population: `info.module` parsing."""
    print_error: int = 0
    """Main error. Population: `int(p.get("print_error"))`."""
    hms_errors: list[dict] = field(default_factory=list)
    """HMS list. Population: `decodeHMS` + `decodeError` synthesis."""
    capabilities: PrinterCapabilities = field(default_factory=PrinterCapabilities)
    """Machine flags. Population: `PrinterCapabilities` instantiation."""

    @staticmethod
    def _resolve_drying_stage(parsed: dict, dry_time: int) -> AMSDryingStage:
        if dry_time < 1:
            return AMSDryingStage.IDLE
        if parsed.get("hardware_fault", False):
            return AMSDryingStage.FAULT
        if parsed.get("venting_active", False):
            if parsed.get("heater_on", False):
                return AMSDryingStage.PURGING
            return AMSDryingStage.CONDITIONING
        if parsed.get("heater_on", False):
            return AMSDryingStage.HEATING
        if parsed.get("exhaust_fan_on", False) or parsed.get("circ_fan_on", False):
            return AMSDryingStage.MAINTENANCE
        return AMSDryingStage.IDLE

    @classmethod
    def fromJson(
        cls, data: dict[str, Any], current_state: Optional["BambuState"] = None
    ) -> "BambuState":
        """Parses root MQTT payloads into a unified BambuState with 100% attribute traceability."""
        base = current_state if current_state else cls()
        info = data.get("info", {})
        p = data.get("print", {})

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

        # STATUS & PROGRESS
        updates["gcode_state"] = p.get("gcode_state", base.gcode_state)
        updates["current_stage_id"] = int(p.get("stg_cur", base.current_stage_id))
        updates["current_stage_name"] = parseStage(updates["current_stage_id"])
        updates["print_percentage"] = int(p.get("mc_percent", base.print_percentage))
        updates["remaining_minutes"] = int(
            p.get("mc_remaining_time", base.remaining_minutes)
        )
        updates["current_layer"] = int(p.get("layer_num", base.current_layer))
        updates["total_layers"] = int(p.get("total_layer_num", base.total_layers))

        # THERMALS & CTC DECODING
        updates["bed_temp"] = float(p.get("bed_temper", base.bed_temp))
        updates["bed_temp_target"] = int(p.get("bed_target_temper", base.bed_temp_target))

        if ctc_root:
            ctc_temp_raw = unpackTemperature(ctc_root.get("info", {}).get("temp", 0.0))
            ctc_temp = ctc_temp_raw[0]
            ctc_temp_target = ctc_temp_raw[1]
            updates["chamber_temp"] = ctc_temp
            updates["chamber_temp_target"] = int(ctc_temp_target)
        else:
            updates["chamber_temp"] = base.chamber_temp
            updates["chamber_temp_target"] = base.chamber_temp_target

        # AIRDUCT
        if airduct_root:
            updates["airduct_mode"] = int(airduct_root.get("modeCur", base.airduct_mode))
            updates["airduct_sub_mode"] = int(
                airduct_root.get("subMode", base.airduct_sub_mode)
            )

            updates["is_chamber_heating"] = updates["airduct_mode"] == 1
            updates["is_chamber_cooling"] = updates["airduct_mode"] == 2
            updates["has_active_filtration"] = updates["airduct_mode"] in [0, 2]

            updates["is_dryer_engaged"] = bool(updates["airduct_sub_mode"] & 0x01)
            updates["top_vent_open"] = bool(updates["airduct_sub_mode"] & 0x01)

            parts = {part["id"]: part["state"] for part in airduct_root.get("parts", [])}
            updates["zone_internal_percent"] = parts.get(16, base.zone_internal_percent)
            updates["zone_intake_percent"] = parts.get(32, base.zone_intake_percent)
            updates["zone_exhaust_percent"] = parts.get(48, base.zone_exhaust_percent)
            updates["ac_unit_power_percent"] = parts.get(96, base.ac_unit_power_percent)

        # EXTRUDERS
        new_extruders = []
        if "info" in extruder_root:
            for ams_ex in extruder_root["info"]:
                raw_t = int(ams_ex.get("temp", 0))
                act_t, tar_t = unpackTemperature(raw_t)
                raw_sn = int(ams_ex.get("snow", 0))

                ext = ExtruderState()
                ext.id = int(ams_ex.get("id", 0))
                ext.temp = act_t
                ext.temp_target = int(tar_t)
                ext.info_bits = int(ams_ex.get("info", 0))
                ext.state = parseExtruderInfo(ext.info_bits)
                ext.status = parseExtruderStatus(int(ams_ex.get("stat", 0)))
                ext.active_tray = (raw_sn >> 8) & 0xFF
                ext.slot_id = raw_sn & 0xFF
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

        # AMS UNITS & HANDLE MAPPING
        new_handle_map = base.ams_handle_map.copy()
        cur_ams = {u.ams_id: u for u in base.ams_units}

        for m in modules:
            if m.get("name", "").startswith("n3f/"):
                try:
                    idx = int(m["name"].split("/")[-1])
                    if match := re.search(r"\((\d+)\)", m.get("product_name", "")):
                        new_handle_map[idx] = int(match.group(1))
                except (ValueError, IndexError):
                    pass

                ams_id_str = str(idx)
                u = cur_ams.get(ams_id_str, AMSUnitState(ams_id=ams_id_str))
                u.chip_id = m.get("sn", u.chip_id)
                u.is_ams_lite = "lite" in m.get("product_name", "").lower()
                cur_ams[ams_id_str] = u

        updates["ams_handle_map"] = new_handle_map

        for ams_u in ams_root.get("ams", []):
            id_s = str(ams_u.get("id", "0"))
            u = cur_ams.get(id_s, AMSUnitState(ams_id=id_s))
            u.temp_actual = float(ams_u.get("temp", u.temp_actual))
            u.humidity_index = int(float(ams_u.get("humidity", u.humidity_index)))
            u.humidity_raw = int(float(ams_u.get("humidity_raw", u.humidity_raw)))
            u.dry_time = int(float(ams_u.get("dry_time", u.dry_time)))

            if "info" in ams_u:
                p_ams = parseAMSInfo(int(ams_u["info"]))
                u.is_online = p_ams["is_online"]
                u.is_powered = p_ams["is_powered"]
                u.rfid_ready = p_ams["rfid_ready"]
                u.hub_sensor_triggered = p_ams["hub_sensor_triggered"]
                u.humidity_sensor_ok = p_ams["humidity_sensor_ok"]
                u.heater_on = p_ams["heater_on"]
                u.circ_fan_on = p_ams["circ_fan_on"]
                u.exhaust_fan_on = p_ams["exhaust_fan_on"]
                u.is_rotating = p_ams["is_rotating"]
                u.venting_active = p_ams.get("venting_active", False)
                u.high_power_mode = p_ams.get("high_power_mode", False)
                u.hardware_fault = p_ams["hardware_fault"]
                u.drying_stage = cls._resolve_drying_stage(p_ams, u.dry_time)

                if updates["capabilities"].has_dual_extruder:
                    u.assigned_to_extruder = ActiveTool(
                        p_ams.get("h2d_toolhead_index", 15)
                    )

            rb = ams_u.get("tray_exist_bits", ams_root.get("tray_exist_bits"))
            if rb is not None:
                eb = int(rb, 16) if isinstance(rb, str) else int(rb)
                u.tray_exists = [
                    bool((eb >> (4 * int(id_s))) & (1 << j)) for j in range(4)
                ]

            cur_ams[id_s] = u

        updates["ams_units"] = list(cur_ams.values())

        # ACTIVE AND TARGET TRAY
        raw_tar_val = int(ams_root.get("tray_tar", p.get("tray_tar", 255)))
        if updates["current_stage_id"] != 24 or raw_tar_val == 255:
            updates["target_tray_id"] = -1
        elif raw_tar_val == 254 and updates["capabilities"].has_dual_extruder:
            updates["target_tray_id"] = 255 - updates["active_tool"].value
        else:
            updates["target_tray_id"] = raw_tar_val

        # if multi-extruder return the active one
        a_ext = next(
            (e for e in updates["extruders"] if e.id == updates["active_tool"].value),
            None,
        )
        if a_ext:
            if a_ext.status == ExtruderStatus.ACTIVE:
                updates["active_tray_id"] = a_ext.active_tray
                updates["active_nozzle_temp"] = a_ext.temp
                updates["active_nozzle_temp_target"] = a_ext.temp_target

                if a_ext.state == ExtruderInfoState.LOADED:
                    updates["active_tray_state"] = TrayState.LOADED
                elif updates["current_stage_id"] == 24:
                    updates["active_tray_state"] = TrayState.LOADING
                elif updates["current_stage_id"] == 22:
                    updates["active_tray_state"] = TrayState.UNLOADING
                else:
                    updates["active_tray_state"] = TrayState.UNLOADED

            if a_ext.active_tray == 254:
                updates["target_tray_id"] = 255 - a_ext.id
            else:
                updates["target_tray_id"] = a_ext.active_tray
        else:
            # otherwise process a single exruder printer update
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

        updates["part_cooling_fan_speed_percent"] = scaleFanSpeed(
            p.get("cooling_fan_speed", 0)
        )
        updates["part_cooling_fan_speed_target_percent"] = scaleFanSpeed(
            p.get("cooling_fan_target_speed", base.part_cooling_fan_speed_target_percent)
        )
        updates["heatbreak_fan_speed_percent"] = scaleFanSpeed(
            p.get("heatbreak_fan_speed", base.heatbreak_fan_speed_percent)
        )
        updates["exhaust_fan_speed_percent"] = scaleFanSpeed(p.get("big_fan2_speed", 0))
        updates["chamber_fan_speed_percent"] = scaleFanSpeed(
            p.get("big_fan1_speed", base.chamber_fan_speed_percent)
        )

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
