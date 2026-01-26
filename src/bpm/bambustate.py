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
    """
    Discovery features based on dev_feature_bits and hardware block presence.
    """

    has_ams: bool = False
    """True if an AMS unit is supported or detected. Population: `ams` block presence in `ams_root` or `p`."""
    has_lidar: bool = False
    """True if the printer has a LiDAR sensor. Population: Presence of `xcam` in `p` or `info`."""
    has_camera: bool = False
    """True if the printer has an internal camera. Population: Hardcoded to `True` for H2D series."""
    has_dual_extruder: bool = False
    """True if the printer is an H2D architecture. Population: `len(extruder_root.info) > 1`."""
    has_air_filtration: bool = False
    """True if the printer supports filtration. Population: `airduct` block presence in `device`."""
    has_chamber_temp: bool = False
    """True if the printer has a chamber sensor. Population: `ctc_root` block presence in `device`."""


@dataclass
class ExtruderState:
    """
    Detailed state for an individual physical extruder toolhead.
    """

    id: int = 0
    """Physical ID of the extruder. Population: `int(r.get("id"))`."""
    temp: float = 0.0
    """Current nozzle temperature. Population: `unpackTemperature(r.temp)`."""
    temp_target: float = 0.0
    """Target nozzle temperature. Population: `unpackTemperature(r.temp)`."""
    info_bits: int = 0
    """Raw bitmask for detection. Population: `int(r.get("info"))`."""
    state: ExtruderInfoState = ExtruderInfoState.NO_NOZZLE
    """Filament status. Population: `parseExtruderInfo(r.info)`."""
    status: ExtruderStatus = ExtruderStatus.IDLE
    """Operational state. Population: `parseExtruderStatus(r.stat)`."""
    active_tray: int = 255
    """Physical Source ID feeding toolhead. Population: `(r.snow >> 8) & 0xFF`."""
    slot_id: int = 255
    """Physical AMS slot feeding toolhead. Population: `r.snow & 0xFF`."""


@dataclass
class AMSUnitState:
    """
    Detailed state information about an individual AMS unit.
    """

    ams_id: str
    """Unique identifier. Population: `str(ams_idx)` from list enumeration."""
    chip_id: str = ""
    """Hardware serial. Population: `m.get("sn")` from `info.module`."""
    is_ams_lite: bool = False
    """True if AMS Lite. Population: `product_name` check in `info.module`."""
    temp_actual: float = 0.0
    """Current internal temp. Population: `float(r.get("temp"))`."""
    temp_target: int = 0
    """Target drying temp. Population: `trays[0].get("drying_temp")`."""
    humidity_index: int = 0
    """Humidity level (1-5). Population: `int(float(r.get("humidity")))`."""
    humidity_raw: int = 0
    """Raw sensor value. Population: `int(float(r.get("humidity_raw")))`."""
    is_online: bool = False
    """True if communicating. Population: `p_ams["is_online"]`."""
    is_powered: bool = False
    """True if powered. Population: `p_ams["is_powered"]`."""
    rfid_ready: bool = False
    """True if RFID functional. Population: `p_ams["rfid_ready"]`."""
    hub_sensor_triggered: bool = False
    """True if filament at hub. Population: `p_ams["hub_sensor_triggered"]`."""
    humidity_sensor_ok: bool = False
    """True if sensor functional. Population: `p_ams["humidity_sensor_ok"]`."""
    heater_on: bool = False
    """True if heater active. Population: `p_ams["heater_on"]`."""
    circ_fan_on: bool = False
    """True if circulation fan on. Population: `p_ams["circ_fan_on"]`."""
    exhaust_fan_on: bool = False
    """True if exhaust fan on. Population: `p_ams["exhaust_fan_on"]`."""
    dry_time: int = 0
    """Remaining minutes. Population: `int(float(r.get("dry_time")))`."""
    is_rotating: bool = False
    """True if rollers turning. Population: `p_ams["is_rotating"]`."""
    venting_active: bool = False
    """True if venting. Population: `p_ams.get("venting_active")`."""
    high_power_mode: bool = False
    """True if performance mode. Population: `p_ams.get("high_power_mode")`."""
    hardware_fault: bool = False
    """True if fault bit set. Population: `p_ams["hardware_fault"]`."""
    tray_exists: list[bool] = field(default_factory=lambda: [False] * 4)
    """Presence indicators. Population: Shifting `tray_exist_bits`."""
    assigned_to_extruder: ActiveTool = ActiveTool.SINGLE_EXTRUDER
    """Mapped toolhead. Population: `ActiveTool(p_ams.h2d_toolhead_index)`."""
    drying_stage: AMSDryingStage = AMSDryingStage.IDLE
    """Current cycle stage. Population: `_resolve_drying_stage`."""


@dataclass
class BambuState:
    """
    Full representation of the Bambu printer state, synchronized via MQTT telemetry.
    """

    gcode_state: str = "IDLE"
    """Current execution state. Population: `p.get("gcode_state")`."""
    current_stage_id: int = 0
    """Numeric stage ID. Population: `int(p.get("stg_cur"))`."""
    current_stage_name: str = ""
    """Human stage name. Population: `parseStage(current_stage_id)`."""
    print_percentage: int = 0
    """Job completion %. Population: `int(p.get("mc_percent"))`."""
    remaining_minutes: int = 0
    """Remaining time. Population: `int(p.get("mc_remaining_time"))`."""
    current_layer: int = 0
    """Current layer. Population: `int(p.get("layer_num"))`."""
    total_layers: int = 0
    """Total layers. Population: `int(p.get("total_layer_num"))`."""
    active_tray_id: int = 255
    """Current filament ID. Population: Computed in Tool Handoff."""
    active_tray_state: TrayState = TrayState.UNLOADED
    """Loading enum. Population: `ExtruderInfoState` check."""
    active_tray_state_name: str = TrayState.UNLOADED.name
    """Loading string. Population: `active_tray_state.name`."""
    target_tray_id: int = -1
    """Target filament ID. Population: Stage-specific targeting logic."""
    active_tool: ActiveTool = ActiveTool.SINGLE_EXTRUDER
    """Active toolhead index. Population: `extruder_root.state` shift."""
    is_external_spool_active: bool = False
    """True if external used. Population: `active_tray_id in [254, 255]`."""
    active_nozzle_temp: float = 0.0
    """Active nozzle temp. Population: Handoff from `a_ext` or `p`."""
    active_nozzle_temp_target: float = 0.0
    """Target nozzle temp. Population: Handoff from `a_ext` or `p`."""
    bed_temp: float = 0.0
    """Current bed temp. Population: `float(p.get("bed_temper"))`."""
    bed_temp_target: float = 0.0
    """Target bed temp. Population: `float(p.get("bed_target_temper"))`."""
    chamber_temp: float = 0.0
    """Current chamber temp. Population: `ctc_root.info.temp` (H2D Path)."""
    chamber_temp_target: float = 0.0
    """Target chamber temp. Population: Base persistence."""
    part_cooling_fan_speed_percent: int = 0
    """Part cooling speed. Population: `scaleFanSpeed(p.cooling_fan_speed)`."""
    part_cooling_fan_speed_target_percent: int = 0
    """Target cooling speed. Population: `scaleFanSpeed(p.cooling_fan_target)`."""
    chamber_fan_speed_percent: int = 0
    """Chamber fan speed. Population: `scaleFanSpeed(p.big_fan1_speed)`."""
    exhaust_fan_speed_percent: int = 0
    """Exhaust fan speed. Population: `scaleFanSpeed(p.big_fan2_speed)`."""
    heatbreak_fan_speed_percent: int = 0
    """Heatbreak fan speed. Population: `scaleFanSpeed(p.heatbreak_fan_speed)`."""
    has_active_filtration: bool = False
    """True if filtering. Population: Capabilities + `airduct` block presence."""
    zone_internal_percent: int = 0
    """Internal air distribution %. Population: `device.airduct.parts` (ID 16)."""
    zone_intake_percent: int = 0
    """Intake air distribution %. Population: `device.airduct.parts` (ID 32)."""
    zone_exhaust_percent: int = 0
    """Exhaust air distribution %. Population: `device.airduct.parts` (ID 48)."""
    top_vent_open: bool = False
    """Physical state of top vent. Population: Bitwise evaluation `state & 0x01`."""
    ams_status_raw: int = 0
    """Raw AMS status. Population: `int(p.get("ams_status"))`."""
    ams_status_text: str = ""
    """Human AMS status. Population: `parseAMSStatus(ams_status_raw)`."""
    ams_exist_bits: int = 0
    """Connected units mask. Population: `int(ams_root.ams_exist_bits, 16)`."""
    ams_connected_count: int = 0
    """Count of units. Population: `bin(ams_exist_bits).count("1")`."""
    ams_units: list[AMSUnitState] = field(default_factory=list)
    """Detailed AMS list. Population: Result of unit iteration."""
    extruders: list[ExtruderState] = field(default_factory=list)
    """Detailed tool list. Population: Result of extruder iteration."""
    ams_handle_map: dict[int, int] = field(default_factory=dict)
    """Logic index map. Population: `info.module` product parsing."""
    print_error: int = 0
    """Primary error code. Population: `int(p.get("print_error"))`."""
    hms_errors: list[dict] = field(default_factory=list)
    """HMS error list. Population: `decodeHMS` + `decodeError` synthesis."""
    capabilities: PrinterCapabilities = field(default_factory=PrinterCapabilities)
    """Hardware flags. Population: `PrinterCapabilities` instantiation."""

    @staticmethod
    def _resolve_drying_stage(parsed: dict, dry_time: int) -> AMSDryingStage:
        if dry_time < 1:
            return AMSDryingStage.IDLE
        if parsed.get("hardware_fault", False):
            return AMSDryingStage.FAULT
        if parsed.get("venting_active", False):
            return (
                AMSDryingStage.PURGING
                if parsed.get("heater_on", False)
                else AMSDryingStage.CONDITIONING
            )
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
        info, p = data.get("info", {}), data.get("print", {})
        ams_root, device = p.get("ams", {}), p.get("device", {})
        extruder_root = device.get("extruder", {})
        ctc_root = device.get("ctc", {})
        airduct_root = device.get("airduct", {})
        modules = info.get("module", [])
        updates = {}

        # 1. CAPABILITIES
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

        # 2. STATUS & PROGRESS
        updates["gcode_state"] = p.get("gcode_state", base.gcode_state)
        updates["current_stage_id"] = int(p.get("stg_cur", base.current_stage_id))
        updates["current_stage_name"] = parseStage(updates["current_stage_id"])
        updates["print_percentage"] = int(p.get("mc_percent", base.print_percentage))
        updates["remaining_minutes"] = int(
            p.get("mc_remaining_time", base.remaining_minutes)
        )
        updates["current_layer"] = int(p.get("layer_num", base.current_layer))
        updates["total_layers"] = int(p.get("total_layer_num", base.total_layers))

        # 3. THERMALS & AIRDUCT (H2D Path Reconciliation)
        updates["bed_temp"] = float(p.get("bed_temper", base.bed_temp))
        updates["bed_temp_target"] = float(
            p.get("bed_target_temper", base.bed_temp_target)
        )
        if ctc_root:
            updates["chamber_temp"] = float(
                ctc_root.get("info", {}).get("temp", base.chamber_temp)
            )
        else:
            updates["chamber_temp"] = float(p.get("chamber_temper", base.chamber_temp))

        updates["chamber_temp_target"] = base.chamber_temp_target

        if airduct_root:
            updates["has_active_filtration"] = True
            updates["top_vent_open"] = bool(int(airduct_root.get("state", 0)) & 0x01)
            parts = {part["id"]: part["state"] for part in airduct_root.get("parts", [])}
            updates["zone_internal_percent"] = parts.get(16, base.zone_internal_percent)
            updates["zone_intake_percent"] = parts.get(32, base.zone_intake_percent)
            updates["zone_exhaust_percent"] = parts.get(48, base.zone_exhaust_percent)

        # 4. EXTRUDERS & TOOLHEAD
        new_extruders = []
        if "info" in extruder_root:
            for r in extruder_root["info"]:
                act, tar = unpackTemperature(int(r.get("temp", 0)))
                new_extruders.append(
                    ExtruderState(
                        id=int(r.get("id", 0)),
                        temp=act,
                        temp_target=tar,
                        info_bits=int(r.get("info", 0)),
                        active_tray=(int(r.get("snow", 0)) >> 8) & 0xFF,
                        slot_id=int(r.get("snow", 0)) & 0xFF,
                        state=parseExtruderInfo(int(r.get("info", 0))),
                        status=parseExtruderStatus(int(r.get("stat", 0))),
                    )
                )
        updates["extruders"] = new_extruders if new_extruders else base.extruders
        if "state" in extruder_root:
            raw_tool_idx = (int(extruder_root["state"]) >> 4) & 0xF
            updates["active_tool"] = (
                ActiveTool(raw_tool_idx)
                if updates["capabilities"].has_dual_extruder
                else ActiveTool.SINGLE_EXTRUDER
            )
        else:
            updates["active_tool"] = base.active_tool

        # 5. AMS RECONCILIATION & HANDLE MAPPING
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
                u.chip_id, u.is_ams_lite = (
                    m.get("sn", u.chip_id),
                    "lite" in m.get("product_name", "").lower(),
                )
                cur_ams[ams_id_str] = u
        updates["ams_handle_map"] = new_handle_map

        for r in ams_root.get("ams", []):
            ams_idx = int(r.get("id", "0"))
            id_s = str(ams_idx)
            u = cur_ams.get(id_s, AMSUnitState(ams_id=id_s))
            u.temp_actual, u.humidity_index = (
                float(r.get("temp", u.temp_actual)),
                int(float(r.get("humidity", u.humidity_index))),
            )
            u.humidity_raw, u.dry_time = (
                int(float(r.get("humidity_raw", u.humidity_raw))),
                int(float(r.get("dry_time", u.dry_time))),
            )
            trays = r.get("tray", [])
            if trays:
                u.temp_target = int(float(trays[0].get("drying_temp", u.temp_target)))

            if "info" in r:
                p_ams = parseAMSInfo(int(r["info"]))
                u.is_online, u.is_powered, u.rfid_ready = (
                    p_ams["is_online"],
                    p_ams["is_powered"],
                    p_ams["rfid_ready"],
                )
                u.hub_sensor_triggered, u.humidity_sensor_ok = (
                    p_ams["hub_sensor_triggered"],
                    p_ams["humidity_sensor_ok"],
                )
                u.heater_on, u.circ_fan_on, u.exhaust_fan_on = (
                    p_ams["heater_on"],
                    p_ams["circ_fan_on"],
                    p_ams["exhaust_fan_on"],
                )
                u.is_rotating, u.venting_active, u.high_power_mode = (
                    p_ams["is_rotating"],
                    p_ams.get("venting_active", False),
                    p_ams.get("high_power_mode", False),
                )
                u.hardware_fault, u.drying_stage = (
                    p_ams["hardware_fault"],
                    cls._resolve_drying_stage(p_ams, u.dry_time),
                )
                if updates["capabilities"].has_dual_extruder:
                    u.assigned_to_extruder = ActiveTool(
                        p_ams.get("h2d_toolhead_index", 15)
                    )

            rb = r.get("tray_exist_bits", ams_root.get("tray_exist_bits"))
            if rb is not None:
                eb = int(rb, 16) if isinstance(rb, str) else int(rb)
                u.tray_exists = [bool((eb >> (4 * ams_idx)) & (1 << j)) for j in range(4)]
            cur_ams[id_s] = u
        updates["ams_units"] = list(cur_ams.values())

        # 6. TRAY & TOOL HANDOFF
        raw_tar_val = int(ams_root.get("tray_tar", p.get("tray_tar", 255)))
        if updates["current_stage_id"] != 24 or raw_tar_val == 255:
            updates["target_tray_id"] = -1
        elif raw_tar_val == 254 and updates["capabilities"].has_dual_extruder:
            updates["target_tray_id"] = 254 + (
                1 if updates["active_tool"].value == 0 else 0
            )
        else:
            updates["target_tray_id"] = raw_tar_val

        a_ext = next(
            (e for e in updates["extruders"] if e.id == updates["active_tool"].value),
            None,
        )
        if a_ext and updates["active_tool"] != ActiveTool.NOT_ACTIVE:
            updates["active_nozzle_temp"], updates["active_nozzle_temp_target"] = (
                a_ext.temp,
                a_ext.temp_target,
            )
            if a_ext.active_tray != 0:
                updates["active_tray_id"] = (
                    a_ext.active_tray
                    if a_ext.active_tray >= 254
                    else ((a_ext.active_tray - 1) << 2) | a_ext.slot_id
                )
                updates["active_tray_state"] = (
                    TrayState.LOADED
                    if a_ext.state == ExtruderInfoState.LOADED
                    else TrayState.UNLOADED
                )
        else:
            updates["active_nozzle_temp"] = float(
                p.get("nozzle_temper", base.active_nozzle_temp)
            )
            updates["active_nozzle_temp_target"] = float(
                p.get("nozzle_target_temper", base.active_nozzle_temp_target)
            )
            updates["active_tray_id"] = int(ams_root.get("tray_now", base.active_tray_id))
            if updates["active_tray_id"] == 255:
                updates["active_tray_id"] = -1
            updates["active_tray_state"] = (
                TrayState.UNLOADED
                if updates["active_tray_id"] == -1
                else TrayState.LOADED
            )

        updates["active_tray_state_name"] = updates["active_tray_state"].name
        updates["is_external_spool_active"] = updates["active_tray_id"] in [254, 255]

        # 7. GLOBAL METADATA & FANS
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

        # 8. ERROR HANDLING (Restored Baseline)
        updates["print_error"] = int(p.get("print_error", base.print_error))
        decoded_error = (
            decodeError(updates["print_error"]) if updates["print_error"] != 0 else {}
        )
        updates["hms_errors"] = decodeHMS(
            p.get("hms", base.hms_errors if "hms" not in p else [])
        )
        if decoded_error and decoded_error not in updates["hms_errors"]:
            updates["hms_errors"].insert(0, decoded_error)

        return replace(base, **updates)
