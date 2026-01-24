from enum import Enum, IntEnum
from typing import Any

from typing_extensions import deprecated

from bpm.bambucommands import HMS_STATUS

"""
`bambutools' hosts various classes and methods used internally and externally
by `bambu-printer-manager`.
"""


@staticmethod
def parseStage(stage_int: int) -> str:
    """
    Maps stg_cur numeric codes to human-readable print stages.
    Definitive mapping reconciled against Bambu Studio's internal string tables.
    """
    stage_map = {
        -1: "",
        0: "",  # BBL_STG_IDLE
        1: "Auto bed leveling",  # BBL_STG_ABL
        2: "Heatbed preheating",  # BBL_STG_BED_PREHEAT
        3: "Sweeping XY mech mode",  # BBL_STG_XY_SWEEP
        4: "Changing filament",  # BBL_STG_FILAMENT_CHANGE
        5: "M400 pause",  # BBL_STG_M400_PAUSE
        6: "Paused due to filament runout",  # BBL_STG_RUNOUT_PAUSE
        7: "Heating hotend",  # BBL_STG_HOTEND_HEATING
        8: "Calibrating extrusion",  # BBL_STG_EXTRUSION_CALI
        9: "Scanning bed surface",  # BBL_STG_BED_SCAN
        10: "Inspecting first layer",  # BBL_STG_FIRST_LAYER_INSPECT
        11: "Identifying build plate type",  # BBL_STG_PLATE_IDENTIFY
        12: "Calibrating Micro Lidar",  # BBL_STG_LIDAR_CALI
        13: "Homing toolhead",  # BBL_STG_HOMING
        14: "Cleaning nozzle tip",  # BBL_STG_NOZZLE_CLEAN
        15: "Checking extruder temperature",  # BBL_STG_EXTRUDER_TEMP_CHECK
        16: "Printing was paused by the user",  # BBL_STG_USER_PAUSE
        17: "Pause of front cover falling",  # BBL_STG_COVER_PAUSE
        18: "Calibrating the micro lidar",  # BBL_STG_LIDAR_CALI_2
        19: "Calibrating extrusion flow",  # BBL_STG_FLOW_CALI
        20: "Paused due to nozzle temperature malfunction",  # BBL_STG_NOZZLE_TEMP_PAUSE
        21: "Paused due to heat bed temperature malfunction",  # BBL_STG_BED_TEMP_PAUSE
        22: "Filament unloading",  # BBL_STG_FILAMENT_UNLOAD
        23: "Skip step pause",  # BBL_STG_SKIP_STEP_PAUSE
        24: "Filament loading",  # BBL_STG_FILAMENT_LOAD
        25: "Motor noise calibration",  # BBL_STG_MOTOR_CALI
        26: "Paused due to AMS lost",  # BBL_STG_AMS_LOST_PAUSE
        27: "Paused due to low speed of the heat break fan",  # BBL_STG_FAN_PAUSE
        28: "Paused due to chamber temperature control error",  # BBL_STG_CHAMBER_PAUSE
        29: "Cooling chamber",  # BBL_STG_CHAMBER_COOLING
        30: "Paused by the Gcode inserted by user",  # BBL_STG_GCODE_PAUSE
        31: "Motor noise showoff",  # BBL_STG_MOTOR_SHOWOFF
        32: "Nozzle filament covered detected pause",  # BBL_STG_NOZZLE_COVER_PAUSE
        33: "Cutter error pause",  # BBL_STG_CUTTER_PAUSE
        34: "First layer error pause",  # BBL_STG_FIRST_LAYER_PAUSE
        35: "Nozzle clog pause",  # BBL_STG_NOZZLE_CLOG_PAUSE
        255: "",
    }
    return stage_map.get(stage_int, f"Stage [{stage_int}]")


@staticmethod
@deprecated("This property is deprecated (v1.0.0). Use `scaleFanSpeed`.")
def parseFan(fan: int) -> int:
    """
    Mainly an internal method used for parsing Fan data
    !!! danger "Deprecated"
    This property is deprecated (v1.0.0). Use `scaleFanSpeed`.
    """
    fan = int(fan)
    if fan == 1:
        return 10
    elif fan == 2:
        return 20
    elif fan in (3, 4):
        return 30
    elif fan in (5, 6):
        return 40
    elif fan in (7, 8):
        return 50
    elif fan == 9:
        return 60
    elif fan in (10, 11):
        return 70
    elif fan == 12:
        return 80
    elif fan in (13, 14):
        return 90
    elif fan == 15:
        return 100
    return 0


@staticmethod
def parseAMSInfo(info_int: int) -> dict:
    """
    Parses decimal bit-packed AMS info for status and feature reconciliation.
    Reconciled against Bambu Studio source logic for H2D/X1/P1 hardware.
    """
    return {
        "is_powered": bool(info_int & 1),
        "is_online": bool(info_int & 2),
        "rfid_ready": bool(info_int & 4),
        "hub_sensor_triggered": bool(info_int & 8),
        "circ_fan_on": bool(info_int & 16),
        "h2d_toolhead_index": (info_int >> 5) & 0x1,
        "exhaust_fan_on": bool(info_int & 64),
        "humidity_sensor_ok": bool((info_int & 128) or (info_int & 131072)),
        "heater_on": bool(info_int & 256),
        "motor_running": bool(info_int & 512),
        "is_rotating": bool(info_int & 1024),  # Specific to AMS Drying Rotation
        "venting_active": bool(info_int & 2048),
        "high_power_mode": bool(info_int & 8192),
        "hardware_fault": bool((info_int & 4096) or (info_int & 16384)),
    }


@staticmethod
def parseAMSStatus(status_int: int) -> str:
    """
    Maps the ams_status code to human-readable descriptions.
    Definitive mapping reconciled against Bambu Studio source code.
    """
    # The high byte represents the primary operational state
    main_status = (status_int >> 8) & 0xFF

    status_map = {
        0x00: "Idle",  # BBL_AMS_STATUS_IDLE
        0x01: "Filament Changing",  # BBL_AMS_STATUS_FILAMENT_CHANGE
        0x02: "RFID Identifying",  # BBL_AMS_STATUS_RFID_READING
        0x03: "Assist/Engaged",  # BBL_AMS_STATUS_ASSIST (Feed Assist)
        0x04: "Calibration",  # BBL_AMS_STATUS_CALIBRATION
        0x10: "Self Check",  # BBL_AMS_STATUS_SELF_CHECK
        0x20: "Debug",  # BBL_AMS_STATUS_DEBUG
        0xFF: "Unknown",  # BBL_AMS_STATUS_UNKNOWN
    }

    # Audit Note: In H2D telemetry (e.g., 768 / 0x0300),
    # the 0x03 high byte correctly resolves to "Assist/Engaged".
    return status_map.get(main_status, "Idle")


@staticmethod
def parseRFIDStatus(status):
    """
    Can be used to parse `ams_rfid_status`
    """
    if status == 0:
        return "RFID Idle"
    elif status == 1:
        return "RFID Reading"
    elif status == 2:
        return "GCode Translating"
    elif status == 3:
        return "GCode Running"
    elif status == 4:
        return "RFID Assistant"
    elif status == 5:
        return "Switch Filament"
    elif status == 6:
        return "Has Filament"
    else:
        return "Unknown"


class ExtruderInfoState(IntEnum):
    """
    Consolidated logical states for extruder sensor status.
    Values represent unique state IDs to prevent bitmask collisions.
    """

    NO_NOZZLE = 0
    EMPTY = 1
    BUFFER_LOADED = 2
    LOADED = 3


@staticmethod
def parseExtruderInfo(info_int: int) -> ExtruderInfoState:
    """
    Decodes the extruder 'info' bit-packed status using unique ExtruderInfoState names.
    Bitmask logic (0x02, 0x04, 0x08) is reconciled against Bambu Studio source.
    """
    # 1. Hardware Interlock: Bit 3 (0x08) presence is mandatory for nozzle detection.
    if not (info_int & 0x08):
        return ExtruderInfoState.NO_NOZZLE

    # 2. Downstream Precedence: Bit 1 (0x02) indicates filament at the toolhead gears.
    if info_int & 0x02:
        return ExtruderInfoState.LOADED

    # 3. Upstream State: Bit 2 (0x04) indicates filament is only at the buffer/hub.
    if info_int & 0x04:
        return ExtruderInfoState.BUFFER_LOADED

    # 4. Default: Nozzle detected (Bit 3 is high), but no filament in the path.
    return ExtruderInfoState.EMPTY


class ExtruderStatus(IntEnum):
    """
    Operational states for physical extruders.
    Values are mapped directly from the Bambu Studio source code (BBL_EXTRUDER_STATE).
    """

    IDLE = 0
    HEATING = 1
    ACTIVE = 2
    SUCCESS = 3


@staticmethod
def parseExtruderStatus(stat_int: int) -> ExtruderStatus:
    """
    Decodes the operational extruder state using the exhaustive Enum map.
    Definitive mapping reconciled against Bambu Studio source.
    """
    # 1. Operational Precedence:
    # The 'working bits' at 8-9 (0x0300) are the primary indicators of
    # the extruder's mechanical state machine.
    working_bits = (stat_int >> 8) & 0x03

    # Check for the rare SUCCESS state (3)
    if working_bits == 0x03:
        return ExtruderStatus.ACTIVE
    elif working_bits == 0x02:
        # In the source, 0x02 is sometimes used for specific transitions,
        # but 0x03 is the official 'Working' flag.
        return ExtruderStatus.ACTIVE

    # 2. Thermal State:
    # Bit 0 (0x01) is the official 'Heater Active' flag in the stat register.
    if stat_int & 0x01:
        return ExtruderStatus.HEATING

    # 3. Default: The toolhead is in a standby or idle state.
    return ExtruderStatus.IDLE


class ServiceState(Enum):
    """
    This enum is used by `bambu-printer-manager` to track the underlying state
    of the `mqtt` connection to the printer.

    States
    ------
    * `NO_STATE` - Startup / initial state indicates no active session.
    * `CONNECTED` - Primary state expected when polling `BambuPrinter`.
    * `PAUSED` - `bambu-printer`'s session state is paused.
    * `QUIT` - When this state is triggered, all session based resources and threads are released.
    """

    NO_STATE = 0
    CONNECTED = 1
    DISCONNECTED = 2
    PAUSED = 3
    QUIT = 4


class PlateType(Enum):
    """
    Used by `BambuPrinter.print_3mf_file` to specify which plate should be used when
    starting a print job.
    """

    AUTO = 0
    COOL_PLATE = 1
    ENG_PLATE = 2
    HOT_PLATE = 3
    TEXTURED_PLATE = 4
    NONE = 999


class ActiveTool(IntEnum):
    """
    The currently active extruder index.

    * `SINGLE_EXTRUDER (-1)`: Standard single-toolhead architecture (X1/P1/A1).
    * `RIGHT_EXTRUDER (0)`: The primary/right toolhead in H2D (Dual Extruder) systems.
    * `LEFT_EXTRUDER (1)`: The secondary/left toolhead in H2D (Dual Extruder) systems.
    """

    SINGLE_EXTRUDER = -1
    RIGHT_EXTRUDER = 0
    LEFT_EXTRUDER = 1


class TrayState(IntEnum):
    """
    Operational status of the filament tray.

    * `UNLOADED (0)`: No filament detected in the toolhead path.
    * `LOADED (1)`: Filament is fully loaded into the toolhead.
    * `LOADING (2)`: Filament is currently being fed to the toolhead.
    * `UNLOADING (3)`: Filament is currently being retracted from the toolhead.
    """

    UNLOADED = 0
    LOADED = 1
    LOADING = 2
    UNLOADING = 3


class PrintOption(Enum):
    """
    Print Option enum
    """

    AUTO_RECOVERY = 0
    FILAMENT_TANGLE_DETECT = 1
    SOUND_ENABLE = 2
    AUTO_SWITCH_FILAMENT = 3


class AMSUserSetting(Enum):
    """
    AMS User Settings enum
    """

    CALIBRATE_REMAIN_FLAG = 0
    STARTUP_READ_OPTION = 1
    TRAY_READ_OPTION = 2


class AMSControlCommand(Enum):
    """
    AMS Control Commands enum
    """

    PAUSE = 0
    RESUME = 1
    RESET = 2


class NozzleDiameter(Enum):
    """
    Nozzle Diameter enum
    """

    POINT_TWO_MM = 0.2
    POINT_FOUR_MM = 0.4
    POINT_SIX_MM = 0.6
    POINT_EIGHT_MM = 0.8
    UNKNOWN = 0.0


class NozzleType(Enum):
    """
    Nozzle Type enum
    """

    STAINLESS_STEEL = 1
    HARDENED_STEEL = 2
    HS01 = 3
    HH01 = 4
    UNKNOWN = 0


class PrinterSeries(Enum):
    """
    Printer Series enum
    """

    UNKNOWN = 0
    X1 = 1
    P1 = 2
    A1 = 3
    P2 = 4
    H2 = 5


class PrinterModel(Enum):
    """
    Printer model enum
    """

    UNKNOWN = 0
    X1C = 1
    X1 = 2
    X1E = 3
    P1P = 4
    P1S = 5
    A1_MINI = 6
    A1 = 7
    P2S = 8
    H2S = 9
    H2D = 10


@staticmethod
def getSeriesByModel(model: PrinterModel) -> PrinterSeries:
    """
    Returns the Printer series enum based on the provided model.
    """
    try:
        return PrinterSeries[model.name[:2]]
    except (KeyError, AttributeError):
        return PrinterSeries.UNKNOWN


def getModelBySerial(serial: str) -> PrinterModel:
    """
    Returns the Printer model enum based on the provided serial #.
    """
    if serial.startswith("00M"):
        return PrinterModel.X1C
    elif serial.startswith("00W"):
        return PrinterModel.X1
    elif serial.startswith("03W"):
        return PrinterModel.X1E
    elif serial.startswith("01S"):
        return PrinterModel.P1P
    elif serial.startswith("01P"):
        return PrinterModel.P1S
    elif serial.startswith("030"):
        return PrinterModel.A1_MINI
    elif serial.startswith("039"):
        return PrinterModel.A1
    elif serial.startswith("22E"):
        return PrinterModel.P2S
    elif serial.startswith("093"):
        return PrinterModel.H2S
    elif serial.startswith("094"):
        return PrinterModel.H2D
    else:
        return PrinterModel.UNKNOWN


def decodeHMS(hex_val: Any) -> dict[str, Any]:
    """
    Decodes a raw integer or hex string into a rich diagnostic object
    using the HMS_STATUS lookup tables.
    """
    # 1. Normalization
    if isinstance(hex_val, int):
        clean_hex = hex(hex_val).replace("0x", "").upper()
    else:
        clean_hex = str(hex_val).replace("0x", "").upper()

    # 2. Proper Padding (8 for errors, 16 for HMS)
    if len(clean_hex) <= 8:
        clean_hex = clean_hex.zfill(8)
    else:
        clean_hex = clean_hex.zfill(16)

    # 3. Correct Dual-Bucket Lookup (Fixes the TypeError)
    data = HMS_STATUS.get("data", {})
    # Access the "en" list within each hardware dictionary bucket
    error_list = data.get("device_error", {}).get("en", [])
    hms_list = data.get("device_hms", {}).get("en", [])

    combined_list = error_list + hms_list
    entry = next((item for item in combined_list if item.get("ecode") == clean_hex), None)

    # 4. Metadata Extraction (Bitmasking)
    module_code = clean_hex[:4]
    severity_code = clean_hex[4:6] if len(clean_hex) == 8 else "00"

    severity_map = {"40": "Fatal", "80": "Warning", "10": "Info"}
    module_map = {
        "0300": "Toolhead/Heatbed",
        "0700": "AMS",
        "0B00": "MC (Motion Controller)",
        "0C00": "OTA/System",
        "1800": "Interface/Expansion",
    }

    return {
        "code": clean_hex,
        "module": module_map.get(module_code, f"Module {module_code}"),
        "severity": severity_map.get(severity_code, "Unknown"),
        "is_critical": severity_code in ["40", "80"],
        "intro": entry["intro"] if entry else "No description available for this code.",
    }


def scaleFanSpeed(raw_val: Any) -> int:
    """
    Scales proprietary 0-15 fan speed values to a 0-100 percentage.
    """
    try:
        val = int(raw_val)
        return min(max(round((val / 15.0) * 100), 0), 100)
    except Exception:
        return 0


def unpackTemperature(raw_temp: int) -> tuple[float, float]:
    """
    Unpacks a 32-bit packed temperature integer into a tuple of (Actual, Target).
    """
    return float(raw_temp & 0xFFFF), float((raw_temp >> 16) & 0xFFFF)


def sortFileTreeAlphabetically(source) -> dict:
    """
    Sorts a dict of file/directory nodes hierarchically in case-insensitive
    alphabetical order (ascending).

    Args:
        source (dict): A dict of lists representing files and/or directories.

    Returns:
        dict: The sorted dict of lists.
    """

    def sort_node_list(node_list):
        for item in node_list:
            if item.get("id", "").endswith("/") and "children" in item:
                item["children"] = sort_node_list(item["children"])

        def sort_key(item):
            return (not item.get("id", "").endswith("/"), item.get("name", "").lower())

        return sorted(node_list, key=sort_key)

    source["children"] = sort_node_list(source["children"])
    return source
