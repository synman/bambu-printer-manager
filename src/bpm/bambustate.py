import logging
from dataclasses import asdict, dataclass, field, replace
from typing import Any, Optional

# Core bpm imports
from bpm.bambuconfig import LoggerName
from bpm.bambutools import (
    ActiveTool,
    parseAMSStatus,
    parseExtruderInfo,
    parseExtruderState,
    parseStage,
)

logger = logging.getLogger(LoggerName)


@dataclass
class ExtruderState:
    """Detailed state for an individual physical extruder tool."""

    id: int = 0
    """The physical ID of the extruder (0 or 1)."""

    temp: float = 0.0
    """The current nozzle temperature in Celsius."""

    target: float = 0.0
    """The target nozzle temperature in Celsius."""

    state: int = 0
    """The raw state bitmask for this specific tool."""

    info_bits: int = 0
    """Additional status bits regarding the tool's health/status."""

    info_text: str = "Unknown"
    """Human-readable description of the tool's status (e.g., 'Loaded, Heating')."""

    state_text: str = "Idle"
    """Human-readable operational state (e.g., 'Active', 'Idle')."""


@dataclass
class AMSUnitState:
    """Detailed state information about each AMS unit."""

    ams_id: str
    """The unique identifier for this AMS unit (e.g., "0", "1")."""

    chip_id: str = ""
    """The hardware serial/chip ID of the AMS."""

    is_ams_lite: bool = False
    """True if this is an AMS Lite (A1 series), False for standard AMS."""

    temp_actual: float = 0.0
    """Current temperature inside the AMS (Celsius)."""

    temp_target: int = 0
    """Target drying temperature (0 if inactive). Always int."""

    humidity_index: int = 0
    """The humidity level index (1-5) reported by the sensor."""

    humidity_raw: int = 0
    """The raw sensor value for humidity. "0" often indicates AMS Lite."""

    is_online: bool = False
    """Whether the AMS is communicating with the printer."""

    is_powered: bool = False
    """Whether the AMS has power."""

    rfid_ready: bool = False
    """True if the RFID readers are idle/ready to read."""

    hub_sensor_triggered: bool = False
    """True if the filament hub sensor detects filament."""

    humidity_sensor_ok: bool = False
    """True if the humidity sensor is functioning."""

    heater_on: bool = False
    """True if the AMS dryer/heater is active."""

    circ_fan_on: bool = False
    """True if the circulation fan is running."""

    exhaust_fan_on: bool = False
    """True if the exhaust fan is running."""

    dry_time: int = 0
    """Remaining drying time in minutes."""

    is_rotating: bool = False
    """True if the spool rollers are currently rotating."""

    venting_active: bool = False
    """True if the venting mechanism is engaged."""

    high_power_mode: bool = False
    """True if AMS is in high power/performance mode."""

    hardware_fault: bool = False
    """True if a hardware fault bit is set."""

    tray_exists: list[bool] = field(default_factory=lambda: [False] * 4)
    """A list of 4 booleans indicating if a tray is present in slots 0-3."""

    assigned_to_extruder: int = 0
    """The extruder ID (0=Right, 1=Left) this AMS is physically mapped to."""


@dataclass(frozen=True)
class BambuState:
    """Full representation of the Bambu printer state."""

    gcode_state: str = "IDLE"
    """Current G-code execution state (e.g., "RUNNING", "IDLE", "PAUSE")."""

    current_stage_id: int = 0
    """Numeric ID of the current print stage."""

    current_stage_name: str = ""
    """Human-readable name of the print stage."""

    print_percentage: int = 0
    """Completion percentage (0-100)."""

    remaining_minutes: int = 0
    """Estimated time remaining in minutes."""

    current_layer: int = 0
    """The current layer number being printed."""

    total_layers: int = 0
    """The total number of layers in the print job."""

    active_tray_id: int = 255
    """The ID of the tray currently in use (0-15 AMS, 254/255 External, 255 Idle)."""

    target_tray_id: int = 255
    """The ID of the tray requested for the next operation."""

    active_tool: ActiveTool = ActiveTool.RIGHT_EXTRUDER
    """The currently active toolhead. Defaults to RIGHT_EXTRUDER (0)."""

    is_external_spool_active: bool = False
    """True if printing from an external spool (virtual tray 254/255)."""

    nozzle_temp: float = 0.0
    """Current temperature of the active nozzle."""

    nozzle_temp_target: float = 0.0
    """Target temperature of the active nozzle."""

    bed_temp: float = 0.0
    """Current bed temperature."""

    bed_temp_target: float = 0.0
    """Target bed temperature."""

    chamber_temp: float = 0.0
    """Current chamber temperature."""

    chamber_temp_target: float = 0.0
    """Target chamber temperature."""

    part_cooling_actual_percent: int = 0
    """Part cooling fan speed (0-100%)."""

    part_cooling_target_percent: int = 0
    """Target part cooling fan speed (0-100%)."""

    chamber_fan_speed_percent: int = 0
    """Chamber/Circulation fan speed (0-100%)."""

    exhaust_fan_speed_percent: int = 0
    """Exhaust/Filter fan speed (0-100%)."""

    heatbreak_fan_speed_percent: int = 0
    """Hotend heatbreak fan speed (0-100%)."""

    has_active_filtration: bool = False
    """True if the printer supports and reports air filtration data."""

    zone_internal_percent: int = 0
    """Internal circulation fan speed (H2D specific)."""

    zone_intake_percent: int = 0
    """Fresh air intake fan speed (H2D specific)."""

    zone_exhaust_percent: int = 0
    """Exhaust fan speed (H2D specific)."""

    ams_status_raw: int = 0
    """Raw status code from the AMS system."""

    ams_status_text: str = ""
    """Human-readable AMS status description."""

    ams_exist_bits: int = 0
    """Bitmask of detected AMS units."""

    ams_connected_count: int = 0
    """Count of connected AMS units."""

    clog_risk_detected: bool = False
    """True if clog detection algorithms have triggered."""

    ams_units: list[AMSUnitState] = field(default_factory=list)
    """Detailed state for every connected AMS unit."""

    extruders: list[ExtruderState] = field(default_factory=list)
    """Detailed state for every toolhead/extruder."""

    virtual_trays: set[int] = field(default_factory=set)
    """Set of valid external spool IDs (e.g. {254, 255})."""

    extruder_assignment: dict[int, int] = field(default_factory=lambda: {0: 0, 1: 0})
    """Map of Extruder ID to Filament Source Index."""

    @classmethod
    def fromJson(
        cls, data: dict[str, Any], current_state: Optional["BambuState"] = None
    ) -> "BambuState":
        """
        Parses a raw JSON message from the Bambu printer and returns an updated BambuState.
        """
        base = current_state if current_state else cls()
        p = data.get("print", {})
        ams_root = p.get("ams", {})
        device = p.get("device", {})
        extruder_root = device.get("extruder", {})
        upgrade_state = p.get("upgrade_state", {})

        def to_pct(val):
            return round((int(val) / 15) * 100)

        updates = {}

        # 0. Capture Configuration Mapping (Manual Bind)
        if p.get("command") == "manual_ams_bind":
            bind_list = p.get("bind_list", [])
            new_map = base.extruder_assignment.copy()
            for b in bind_list:
                if "extruder" in b and "ams_f_bind" in b:
                    new_map[int(b["extruder"])] = int(b["ams_f_bind"])
            updates["extruder_assignment"] = new_map
        else:
            updates["extruder_assignment"] = base.extruder_assignment

        # 1. AMS Units
        if "ams" in ams_root:
            root_tray_exist_bits = 0
            if "tray_exist_bits" in ams_root:
                val = ams_root["tray_exist_bits"]
                root_tray_exist_bits = int(val, 16) if isinstance(val, str) else int(val)

            new_ams_units = [AMSUnitState(**asdict(u)) for u in base.ams_units]
            ams_on_left_exists = False
            ams_on_right_exists = False

            for ams_raw in ams_root.get("ams", []):
                ams_id = ams_raw.get("id")
                if ams_id is None:
                    continue
                idx = next(
                    (i for i, u in enumerate(new_ams_units) if u.ams_id == ams_id), None
                )
                u = new_ams_units[idx] if idx is not None else AMSUnitState(ams_id=ams_id)
                if idx is None:
                    new_ams_units.append(u)

                raw_fw_id = upgrade_state.get("mc_for_ams_firmware", {}).get(
                    "current_run_firmware_id"
                )
                u.is_ams_lite = (
                    (int(raw_fw_id) == 0)
                    if raw_fw_id is not None
                    else (ams_raw.get("humidity_raw") == "0")
                )

                if "temp" in ams_raw:
                    u.temp_actual = float(ams_raw["temp"])
                if "temp_target" in ams_raw:
                    u.temp_target = int(float(ams_raw["temp_target"]))
                if "humidity" in ams_raw:
                    u.humidity_index = int(ams_raw["humidity"])
                if "humidity_raw" in ams_raw:
                    u.humidity_raw = int(ams_raw["humidity_raw"])
                if "chip_id" in ams_raw:
                    u.chip_id = ams_raw["chip_id"]
                if "dry_time" in ams_raw:
                    u.dry_time = int(ams_raw["dry_time"])

                if "info" in ams_raw:
                    info = (
                        int(ams_raw["info"], 16)
                        if isinstance(ams_raw["info"], str)
                        else int(ams_raw["info"])
                    )
                    u.is_powered, u.is_online = bool(info & 1), bool(info & 2)
                    u.rfid_ready, u.hub_sensor_triggered = bool(info & 4), bool(info & 8)
                    u.humidity_sensor_ok = bool(info & 64)

                    u.assigned_to_extruder = 1 if (info & 0x100) else 0

                    if u.assigned_to_extruder == 1:
                        ams_on_left_exists = True
                    else:
                        ams_on_right_exists = True

                    if not u.is_ams_lite:
                        u.circ_fan_on, u.exhaust_fan_on = bool(info & 16), bool(info & 32)
                        u.heater_on = bool(info & 128)

                        if u.assigned_to_extruder == 1:
                            u.is_rotating = False
                        else:
                            u.is_rotating = bool(info & 256)

                        u.venting_active = bool(info & 512)
                        u.high_power_mode = bool(info & 1024)
                        u.hardware_fault = bool(info & 2048)

                if "tray_exist_bits" in ams_raw:
                    eb = (
                        int(ams_raw["tray_exist_bits"], 16)
                        if isinstance(ams_raw["tray_exist_bits"], str)
                        else int(ams_raw["tray_exist_bits"])
                    )
                    u.tray_exists = [bool(eb & (1 << i)) for i in range(4)]
                elif ams_id.isdigit():
                    aid = int(ams_id)
                    eb = (root_tray_exist_bits >> (aid * 4)) & 0xF
                    u.tray_exists = [bool(eb & (1 << i)) for i in range(4)]

            updates["ams_units"] = new_ams_units
        else:
            ams_on_left_exists = any(u.assigned_to_extruder == 1 for u in base.ams_units)
            ams_on_right_exists = any(u.assigned_to_extruder == 0 for u in base.ams_units)

        # 2. Virtual Trays
        if "vir_slot" in p or "vir_slot" in ams_root:
            raw_vir_slots = p.get("vir_slot", ams_root.get("vir_slot", []))
            new_vir_set = set()
            for vt in raw_vir_slots:
                if "id" in vt:
                    try:
                        new_vir_set.add(int(vt["id"]))
                    except ValueError:
                        pass
            updates["virtual_trays"] = new_vir_set
        else:
            updates["virtual_trays"] = base.virtual_trays

        # 3. Extruders
        new_extruders = base.extruders
        if "info" in extruder_root:
            new_extruders = []
            for ext_raw in extruder_root.get("info", []):
                e_id = int(ext_raw.get("id", 0))
                raw_v = int(ext_raw.get("temp", 0))
                act_t, tar_t = float(raw_v & 0xFFFF), float((raw_v >> 16) & 0xFFFF)
                stat = int(ext_raw.get("stat", 0))
                info = int(ext_raw.get("info", 0))

                new_extruders.append(
                    ExtruderState(
                        id=e_id,
                        temp=act_t,
                        target=tar_t,
                        state=stat,
                        info_bits=info,
                        info_text=parseExtruderInfo(info),
                        state_text=parseExtruderState(stat),
                    )
                )
            updates["extruders"] = new_extruders

        # 4. Active Tool Logic
        tool_val = base.active_tool.value

        active_from_stat = -1
        for ext in new_extruders:
            if (ext.state & 0x300) == 0x300:
                active_from_stat = ext.id
                break

        if active_from_stat != -1:
            tool_val = active_from_stat
        elif p.get("command") == "select_extruder":
            tool_val = int(p.get("extruder_index", 0))
        elif "state" in extruder_root:
            raw_ext_bits = int(extruder_root.get("state", 0))
            if raw_ext_bits > 0:
                fallback_val = (raw_ext_bits & -raw_ext_bits).bit_length() - 1
                current_gcode = p.get("gcode_state", base.gcode_state)
                is_idle = current_gcode in ["IDLE", "FINISH", "READY"]
                if not is_idle:
                    tool_val = fallback_val

        try:
            updates["active_tool"] = ActiveTool(tool_val)
        except ValueError:
            logger.warning(
                f"Unknown tool ID {tool_val} detected. Defaulting to RIGHT_EXTRUDER."
            )
            updates["active_tool"] = ActiveTool.RIGHT_EXTRUDER

        # 5. Active Tray Logic
        raw_tray_now = p.get("tray_now", ams_root.get("tray_now"))

        if raw_tray_now is not None:
            tray_now = int(raw_tray_now)
            active_tool_id = updates["active_tool"].value
            tool_0_ext_id = 255 if 255 in updates["virtual_trays"] else 254

            if active_tool_id == 1:
                if not ams_on_left_exists and tray_now == 0:
                    updates["active_tray_id"] = 254
                else:
                    updates["active_tray_id"] = tray_now
            else:
                if not ams_on_right_exists and tray_now == 0:
                    updates["active_tray_id"] = tool_0_ext_id
                else:
                    updates["active_tray_id"] = tray_now

            updates["is_external_spool_active"] = updates["active_tray_id"] in [
                254,
                255,
                253,
            ]

        else:
            updates["active_tray_id"] = base.active_tray_id
            updates["is_external_spool_active"] = base.is_external_spool_active

        # 6. Global Nozzle Sync
        active_ext = next(
            (e for e in new_extruders if e.id == updates["active_tool"].value), None
        )
        if active_ext:
            updates["nozzle_temp"], updates["nozzle_temp_target"] = (
                active_ext.temp,
                active_ext.target,
            )
        elif "nozzle_temper" in p:
            updates["nozzle_temp"] = float(p["nozzle_temper"])
            updates["nozzle_temp_target"] = float(p.get("nozzle_target_temper", 0))

        # 7. General State
        field_map = {
            "gcode_state": "gcode_state",
            "mc_percent": "print_percentage",
            "mc_remaining_time": "remaining_minutes",
            "bed_temper": "bed_temp",
            "bed_target_temper": "bed_temp_target",
            "clog_risk": "clog_risk_detected",
        }
        for jk, attr in field_map.items():
            if jk in p:
                updates[attr] = p[jk]

        if "stg_cur" in p:
            updates["current_stage_id"] = int(p["stg_cur"])
            updates["current_stage_name"] = parseStage(updates["current_stage_id"])

        if "ams_status" in p:
            updates["ams_status_raw"] = int(p["ams_status"])
            updates["ams_status_text"] = parseAMSStatus(updates["ams_status_raw"])

        if "tray_tar" in ams_root:
            updates["target_tray_id"] = int(ams_root["tray_tar"])

        if "ams_exist_bits" in ams_root:
            updates["ams_exist_bits"] = int(ams_root["ams_exist_bits"])
            updates["ams_connected_count"] = bin(updates["ams_exist_bits"]).count("1")

        # 8. Layer Logic
        three_d = p.get("3D", {})
        updates["current_layer"] = three_d.get(
            "layer_num", p.get("layer_num", base.current_layer)
        )
        updates["total_layers"] = three_d.get(
            "total_layer_num", p.get("total_layer_num", base.total_layers)
        )

        # 9. Zones (H2D Fix: Use raw 0-100 values and Correct IDs)
        if "airduct" in device:
            updates["has_active_filtration"] = True
            # IDs: 16=Internal(Func0), 32=Intake(Func1), 48=Exhaust(Func2)
            parts = {
                part["id"]: part["state"] for part in device["airduct"].get("parts", [])
            }

            # Use raw values (no to_pct scaling)
            updates["zone_internal_percent"] = parts.get(16, 0)
            updates["zone_intake_percent"] = parts.get(32, 0)
            updates["zone_exhaust_percent"] = parts.get(48, 0)

        if "ctc" in device:
            updates["chamber_temp"] = float(
                device["ctc"].get("info", {}).get("temp", base.chamber_temp)
            )

        # 10. Fans
        fan_map = {
            "cooling_fan_speed": "part_cooling_actual_percent",
            "big_fan2_speed": "exhaust_fan_speed_percent",
        }
        for jk, attr in fan_map.items():
            if jk in p:
                updates[attr] = to_pct(p[jk])

        return replace(base, **updates)
