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
    ExtruderInfoState,
    ExtruderStatus,
    TrayState,
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
    Discovery features based on dev_feature_bits and logical presence of JSON data blocks.
    """

    has_ams: bool = False
    """True if an AMS unit is supported or detected."""
    has_lidar: bool = False
    """True if the printer has a LiDAR sensor."""
    has_camera: bool = False
    """True if the printer has an internal camera."""
    has_dual_extruder: bool = False
    """True if the printer is an H2D (Dual Extruder) architecture."""
    has_air_filtration: bool = False
    """True if the printer supports active air filtration."""
    has_chamber_temp: bool = False
    """True if the printer has a dedicated chamber temperature sensor."""


@dataclass
class ExtruderState:
    """
    Detailed state for an individual physical extruder toolhead.
    """

    id: int = 0
    """Physical ID of the extruder (0 or 1)."""
    temp: float = 0.0
    """Current nozzle temperature in Celsius."""
    temp_target: float = 0.0
    """Target nozzle temperature in Celsius."""
    info_bits: int = 0
    """Raw bitmask for filament and nozzle detection."""
    state: ExtruderInfoState = ExtruderInfoState.NO_NOZZLE
    """Human-readable filament/nozzle status."""
    status: ExtruderStatus = ExtruderStatus.IDLE
    """Human-readable operational state."""
    active_tray: int = 255
    """Physical Source ID currently feeding this extruder (0-3: AMS, 254: Virtual, 255: External)."""
    slot_id: int = 255
    """Physical AMS slot (0-3) currently feeding this extruder."""


@dataclass
class AMSUnitState:
    """
    Detailed state information about an individual AMS unit.
    """

    ams_id: str
    """Unique physical identifier for the AMS unit."""
    chip_id: str = ""
    """Hardware serial or chip ID."""
    is_ams_lite: bool = False
    """True if this hardware is identified as an AMS Lite."""
    temp_actual: float = 0.0
    """Current internal temperature of the AMS."""
    temp_target: int = 0
    """Target drying temperature."""
    humidity_index: int = 0
    """Humidity level index (1-5)."""
    humidity_raw: int = 0
    """Raw humidity sensor value."""
    is_online: bool = False
    """True if the unit is communicating with the printer."""
    is_powered: bool = False
    """True if the unit has power."""
    rfid_ready: bool = False
    """True if the RFID reader is operational."""
    hub_sensor_triggered: bool = False
    """True if filament is detected at the AMS hub."""
    humidity_sensor_ok: bool = False
    """True if the humidity sensor is functional."""
    heater_on: bool = False
    """True if the drying heater is active."""
    circ_fan_on: bool = False
    """True if the internal circulation fan is running."""
    exhaust_fan_on: bool = False
    """True if the exhaust fan is running."""
    dry_time: int = 0
    """Remaining drying time in minutes."""
    is_rotating: bool = False
    """True if the rollers are currently turning (specifically for drying rotation)."""
    venting_active: bool = False
    """True if the venting mechanism is active."""
    high_power_mode: bool = False
    """True if the unit is in performance power mode."""
    hardware_fault: bool = False
    """True if a hardware fault bit is set."""
    tray_exists: list[bool] = field(default_factory=lambda: [False] * 4)
    """Presence indicators for the four filament slots."""
    assigned_to_extruder: ActiveTool = ActiveTool.SINGLE_EXTRUDER
    """The toolhead currently mapped to this AMS unit."""


@dataclass
class BambuState:
    """
    Full representation of the Bambu printer state, synchronized via MQTT telemetry.
    """

    gcode_state: str = "IDLE"
    """Current G-code execution state (e.g., IDLE, RUNNING)."""
    current_stage_id: int = 0
    """Numeric ID of the current print stage."""
    current_stage_name: str = ""
    """Human-readable name of the current print stage."""
    print_percentage: int = 0
    """Completion percentage of the current print job."""
    remaining_minutes: int = 0
    """Estimated remaining time in minutes."""
    current_layer: int = 0
    """The layer currently being printed."""
    total_layers: int = 0
    """The total number of layers in the print job."""
    active_tray_id: int = 255
    """ID of the filament tray currently in use."""
    active_tray_state: TrayState = TrayState.UNLOADED
    """Loading status of the active tray."""
    target_tray_id: int = -1
    """Target tray ID for filament changes."""
    active_tool: ActiveTool = ActiveTool.SINGLE_EXTRUDER
    """The index of the currently active toolhead."""
    is_external_spool_active: bool = False
    """True if the external spool is being used."""
    active_nozzle_temp: float = 0.0
    """Current temperature of the active nozzle."""
    active_nozzle_temp_target: float = 0.0
    """Target temperature of the active nozzle."""
    bed_temp: float = 0.0
    """Current temperature of the heatbed."""
    bed_temp_target: float = 0.0
    """Target temperature of the heatbed."""
    chamber_temp: float = 0.0
    """Current temperature of the build chamber."""
    chamber_temp_target: float = 0.0
    """Target temperature of the build chamber."""
    part_cooling_fan_speed_percent: int = 0
    """Current speed of the part cooling fan."""
    part_cooling_fan_speed_target_percent: int = 0
    """Target speed of the part cooling fan."""
    chamber_fan_speed_percent: int = 0
    """Speed of the chamber circulation fan."""
    exhaust_fan_speed_percent: int = 0
    """Speed of the exhaust fan."""
    heatbreak_fan_speed_percent: int = 0
    """Speed of the heatbreak cooling fan."""
    has_active_filtration: bool = False
    """True if air filtration is active."""
    ams_status_raw: int = 0
    """Raw bit-packed status of the AMS system."""
    ams_status_text: str = ""
    """Human-readable status of the AMS system."""
    ams_exist_bits: int = 0
    """Bitmask indicating which AMS units are connected."""
    ams_connected_count: int = 0
    """Total number of detected AMS units."""
    ams_units: list[AMSUnitState] = field(default_factory=list)
    """Detailed states for each connected AMS unit."""
    extruders: list[ExtruderState] = field(default_factory=list)
    """Detailed states for each physical extruder."""
    ams_handle_map: dict[int, int] = field(default_factory=dict)
    """Mapping of physical AMS indices to logical handles."""
    hms_errors: list[dict] = field(default_factory=list)
    """Decoded Health Management System error messages."""
    capabilities: PrinterCapabilities = field(default_factory=PrinterCapabilities)
    """Hardware features discovered for the current printer."""

    @classmethod
    def fromJson(
        cls, data: dict[str, Any], current_state: Optional["BambuState"] = None
    ) -> "BambuState":
        """
        Parses root MQTT payloads into a unified BambuState with strict hardware gating.

        Args:
            data (Dict[str, Any]): The raw MQTT JSON payload from the printer.
            current_state (Optional[BambuState]): The existing state to update. If None, a new state is initialized.

        Returns:
            BambuState: A new BambuState instance reflecting the merged telemetry updates.
        """
        base = current_state if current_state else cls()
        info, p = data.get("info", {}), data.get("print", {})
        ams_root, device = p.get("ams", {}), p.get("device", {})
        extruder_root = device.get("extruder", {})
        modules = info.get("module", [])
        updates = {}

        # 1. CAPABILITIES & HARDWARE CROSS-VALIDATION
        feat_bits = info.get(
            "dev_feature_bits", device.get("dev_feature_bits", p.get("dev_feature_bits"))
        )
        caps = asdict(base.capabilities)
        if feat_bits is not None:
            b = int(feat_bits)
            caps.update(
                {
                    "has_air_filtration": bool(b & 0x01),
                    "has_dual_extruder": bool(b & 0x10),
                    # Zero-Inference Rule: LiDAR is physically impossible on H2D despite feature bit
                    "has_lidar": bool(b & 0x20) and ("xcam" in p or "xcam" in info),
                    "has_chamber_temp": bool(b & 0x40),
                }
            )

        # Feature Persistence Fix
        if "ctc" in device:
            caps["has_chamber_temp"] = True
        if "airduct" in device:
            caps["has_air_filtration"] = True
        if "ams" in ams_root or "ams" in p:
            caps["has_ams"] = True
        if len(extruder_root.get("info", [])) > 1:
            caps["has_dual_extruder"] = True
        caps["has_camera"] = True
        updates["capabilities"] = PrinterCapabilities(**caps)

        # 2. AMS HANDLE MAPPING
        new_handle_map = base.ams_handle_map.copy()
        for m in modules:
            if m.get("name", "").startswith("n3f/"):
                try:
                    idx = int(m["name"].split("/")[-1])
                    if match := re.search(r"\((\d+)\)", m.get("product_name", "")):
                        new_handle_map[idx] = int(match.group(1))
                except (ValueError, IndexError):
                    pass
        updates["ams_handle_map"] = new_handle_map

        # 3. EXTRUDER TELEMETRY
        new_extruders = []
        if "info" in extruder_root:
            for r in extruder_root["info"]:
                act, tar = unpackTemperature(int(r.get("temp", 0)))
                new_extruders.append(
                    ExtruderState(
                        id=int(r.get("id", 0)),
                        temp=act,
                        temp_target=tar,
                        active_tray=(int(r.get("snow", 0)) >> 8) & 0xFF,
                        slot_id=int(r.get("snow", 0)) & 0xFF,
                        state=parseExtruderInfo(int(r.get("info", 0))),
                        status=parseExtruderStatus(int(r.get("stat", 0))),
                    )
                )
        updates["extruders"] = new_extruders if new_extruders else base.extruders

        # 4. ACTIVE TOOLHEAD RECONCILIATION
        if "state" in extruder_root:
            updates["active_tool"] = (
                ActiveTool((int(extruder_root["state"]) >> 4) & 0xF)
                if updates["capabilities"].has_dual_extruder
                else ActiveTool.SINGLE_EXTRUDER
            )
        else:
            updates["active_tool"] = base.active_tool

        # 5. AMS UNIT RECONCILIATION
        cur_ams = {u.ams_id: u for u in base.ams_units}
        for m in modules:
            if "ams" in m.get("name", "") or "n3f" in m.get("name", ""):
                ams_id_str = m.get("name", "").split("/")[-1]
                unit = cur_ams.get(ams_id_str, AMSUnitState(ams_id=ams_id_str))
                unit.chip_id = m.get("sn", unit.chip_id)
                unit.is_ams_lite = "lite" in m.get("product_name", "").lower()
                cur_ams[ams_id_str] = unit

        for r in ams_root.get("ams", []):
            ams_idx = int(r.get("id", "0"))
            id_s = str(ams_idx)
            u = cur_ams.get(id_s, AMSUnitState(ams_id=id_s))

            if "info" in r:
                p_ams = parseAMSInfo(int(r["info"]))
                u.is_online, u.is_powered = p_ams["is_online"], p_ams["is_powered"]
                u.rfid_ready = p_ams["rfid_ready"]
                u.humidity_sensor_ok = p_ams["humidity_sensor_ok"]
                u.heater_on, u.is_rotating = p_ams["heater_on"], p_ams["is_rotating"]
                # H2D Architecture Assignment
                if updates["capabilities"].has_dual_extruder:
                    u.assigned_to_extruder = ActiveTool(
                        p_ams.get("h2d_toolhead_index", 0)
                    )

            # Robust Humidity/Timer Parsing (Fix for string "0")
            try:
                if "humidity_raw" in r:
                    u.humidity_raw = int(float(r["humidity_raw"]))
                if "dry_time" in r:
                    u.dry_time = int(float(r["dry_time"]))
                if "humidity" in r:
                    u.humidity_index = int(float(r["humidity"]))
            except (ValueError, TypeError):
                pass

            u.temp_actual = float(r.get("temp", u.temp_actual))

            # Bitmask-Based Tray Reconciliation (Nybble Shifting)
            rb = r.get("tray_exist_bits", ams_root.get("tray_exist_bits"))
            if rb is not None:
                eb = int(rb, 16) if isinstance(rb, str) else int(rb)
                u.tray_exists = [bool((eb >> (4 * ams_idx)) & (1 << j)) for j in range(4)]
            cur_ams[id_s] = u

        updates["ams_units"] = list(cur_ams.values())

        # 6. THERMAL & TRAY HANDOFF
        #
        a_ext = next(
            (e for e in updates["extruders"] if e.id == updates["active_tool"].value),
            None,
        )
        if a_ext:
            updates["active_nozzle_temp"], updates["active_nozzle_temp_target"] = (
                a_ext.temp,
                a_ext.temp_target,
            )
            if a_ext.active_tray != 0:
                updates["active_tray_id"] = (
                    a_ext.active_tray
                    if a_ext.active_tray >= 254
                    else (a_ext.active_tray << 2) | a_ext.slot_id
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
            updates["active_tray_id"] = int(
                ams_root.get("tray_now", p.get("tray_now", base.active_tray_id))
            )

        # 32-bit Packed Bed Thermal Unpacking (0x130013 -> 19.0)
        bed_raw = device.get("bed", {}).get("info", {}).get("temp")
        if bed_raw is not None:
            act, tar = unpackTemperature(int(bed_raw))
            updates["bed_temp"], updates["bed_temp_target"] = act, tar
        else:
            updates["bed_temp"] = float(p.get("bed_temper", base.bed_temp))
            updates["bed_temp_target"] = float(
                p.get("bed_target_temper", base.bed_temp_target)
            )

        # 7. GLOBAL METADATA & FANS
        raw_exist = ams_root.get("ams_exist_bits", base.ams_exist_bits)
        updates["ams_exist_bits"] = (
            int(raw_exist, 16) if isinstance(raw_exist, str) else int(raw_exist)
        )
        updates["ams_connected_count"] = bin(updates["ams_exist_bits"]).count("1")
        updates["ams_status_text"] = parseAMSStatus(
            int(p.get("ams_status", base.ams_status_raw))
        )
        updates["gcode_state"] = p.get("gcode_state", base.gcode_state)
        updates["current_stage_name"] = parseStage(
            int(p.get("stg_cur", base.current_stage_id))
        )
        updates["hms_errors"] = [decodeHMS(hex(c)) for c in p.get("hms", [])]
        updates["part_cooling_fan_speed_percent"] = scaleFanSpeed(
            p.get("cooling_fan_speed", 0)
        )
        updates["exhaust_fan_speed_percent"] = scaleFanSpeed(p.get("big_fan2_speed", 0))
        updates["has_active_filtration"] = (
            updates["capabilities"].has_air_filtration
            and updates["exhaust_fan_speed_percent"] > 0
        )

        return replace(base, **updates)
