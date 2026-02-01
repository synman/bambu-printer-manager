from enum import Enum, IntEnum
from typing import Any

from typing_extensions import deprecated

from bpm.bambucommands import HMS_STATUS

"""
`bambutools' hosts various classes and methods used internally and externally
by `bambu-printer-manager`.
"""


class ActiveTool(IntEnum):
    """
    The currently active extruder index.

    * `SINGLE_EXTRUDER (-1)`: Standard single-toolhead architecture (X1/P1/A1).
    * `RIGHT_EXTRUDER (0)`: The primary/right toolhead in H2D (Dual Extruder) systems.
    * `LEFT_EXTRUDER (1)`: The secondary/left toolhead in H2D (Dual Extruder) systems.
    * `NOT_ACTIVE (15)`: The multi-extruder system is in a transitional state.
    """

    SINGLE_EXTRUDER = -1
    RIGHT_EXTRUDER = 0
    LEFT_EXTRUDER = 1
    NOT_ACTIVE = 15


class AirConditioningMode(IntEnum):
    """
    The mode the printer's air conditioning sub system is in.

    * `NOT_SUPPORTED (-1)`: This printer is not equipped with this feature.
    * `COOL_MODE (0)`: The printer is currently not heating. The top vent may be open if the exhaust fan is running.
    * `HEAT_MODE (1)`: The printer is actively heating the chamber with the recirculation fan active.
    """

    NOT_SUPPORTED = -1
    COOL_MODE = 0
    HEAT_MODE = 1


class AMSControlCommand(Enum):
    """
    AMS Control Commands enum
    """

    PAUSE = 0
    RESUME = 1
    RESET = 2


class AMSDryingStage(IntEnum):
    """
    Represents the operational stages of the AMS2 drying cycle.
    Resolved from heater, vent, and fan bitmasks.
    """

    IDLE = 0
    HEATING = 1  # Heater active, Vent closed
    PURGING = 2  # Vent open, Heater likely active
    CONDITIONING = 3  # Heater off, Vent open, Fan running
    MAINTENANCE = 4  # Post-cycle humidity monitoring
    FAULT = 5  # Error detected during cycle


class AMSModel(Enum):
    """
    AMS model enum
    """

    UNKNOWN = 0
    AMS_1 = 1
    AMS_LITE = 2
    AMS_HT = 3
    AMS_2_PRO = 4


class AMSSeries(Enum):
    """
    AMS Series enum
    """

    UNKNOWN = 0
    GEN_1 = 1
    GEN_2 = 2


class AMSUserSetting(Enum):
    """
    AMS User Settings enum
    """

    CALIBRATE_REMAIN_FLAG = 0
    STARTUP_READ_OPTION = 1
    TRAY_READ_OPTION = 2


class ExtruderInfoState(IntEnum):
    """
    Consolidated logical states for extruder sensor status.
    Values represent unique state IDs to prevent bitmask collisions.
    """

    NO_NOZZLE = 0
    EMPTY = 1
    BUFFER_LOADED = 2
    LOADED = 3


class ExtruderStatus(IntEnum):
    """
    Operational states for physical extruders.
    Values are mapped directly from the Bambu Studio source code (BBL_EXTRUDER_STATE).
    """

    IDLE = 0
    HEATING = 1
    ACTIVE = 2
    SUCCESS = 3


class NozzleDiameter(Enum):
    """
    Nozzle Diameter enum
    """

    UNKNOWN = 0.0
    POINT_TWO_MM = 0.2
    POINT_FOUR_MM = 0.4
    POINT_SIX_MM = 0.6
    POINT_EIGHT_MM = 0.8


class NozzleType(Enum):
    """
    Nozzle Type enum
    """

    UNKNOWN = 0
    STAINLESS_STEEL = 1
    HARDENED_STEEL = 2
    HS01 = 3
    HH01 = 4


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


class PrintOption(Enum):
    """
    Print Option enum
    """

    AUTO_RECOVERY = 0
    FILAMENT_TANGLE_DETECT = 1
    SOUND_ENABLE = 2
    AUTO_SWITCH_FILAMENT = 3


class ServiceState(Enum):
    """
    This enum is used by `bambu-printer-manager` to track the underlying state
    of the `mqtt` connection to the printer.
    """

    NO_STATE = 0
    CONNECTED = 1
    DISCONNECTED = 2
    PAUSED = 3
    QUIT = 4


class TrayState(IntEnum):
    """
    Operational status of the filament tray.
    """

    UNLOADED = 0
    LOADED = 1
    LOADING = 2
    UNLOADING = 3


@staticmethod
def decodeError(error: int) -> dict:
    """
    Decodes a raw print_error integer into a full HMS dictionary.
    """
    if error == 0:
        return {}

    raw_hex = f"{error:08X}".upper()
    wiki_slug = "-".join(raw_hex[i : i + 4] for i in range(0, 8, 4))
    res = {
        "code": f"HMS_{wiki_slug}",
        "msg": "Unknown HMS Error",
        "module": "System",
        "severity": "Error",
        "is_critical": False,
        "type": "device_error",
        "url": f"https://e.bambulab.com/?e={raw_hex}",
    }

    real_module = (error >> 24) & 0xFF
    module_map = {
        0x03: "Mainboard",
        0x05: "AMS",
        0x12: "AMS",
        0x07: "Toolhead",
        0x0B: "Webcam",
        0x10: "HMS",
    }
    res["module"] = module_map.get(real_module, "System")

    msg_list = HMS_STATUS.get("data", {}).get("device_error", {}).get("en", [])
    modules = ["03", "05", "07", "0B", "0C", "10", "12"]
    if raw_hex[:2] in modules:
        modules.remove(raw_hex[:2])
    modules.insert(0, raw_hex[:2])

    for module in modules:
        current_hex = f"{module}{raw_hex[2:]}"
        for entry in msg_list:
            if entry.get("ecode", "").upper() == current_hex.upper():
                res["msg"] = entry.get("intro", res["msg"])
                break
        if res["msg"] != "Unknown HMS Error":
            break

    mask = (error >> 16) & 0xFF
    if mask in (0x00, 0x01):
        res["severity"] = "Fatal" if mask == 0x00 else "Error"
        res["is_critical"] = True
    elif mask == 0x02:
        res["severity"] = "Warning"
        res["is_critical"] = False
    else:
        res["severity"] = "Info"
        res["is_critical"] = False

    return res


@staticmethod
def decodeHMS(hms_list: list) -> list[dict]:
    """
    Decodes the raw HMS list from telemetry into a structured list of dictionaries.
    """
    decoded_errors = []
    for item in hms_list:
        if isinstance(item, dict) and isinstance(item.get("code"), str):
            decoded_errors.append(item)
            continue
        try:
            attr = int(item.get("attr", 0))
            code = int(item.get("code", 0))
        except (AttributeError, ValueError, TypeError):
            continue
        if attr == 0:
            continue

        ecode = f"{attr:08X}{code:08X}"
        wiki_slug = "-".join(ecode[i : i + 4] for i in range(0, 16, 4))
        res = {
            "code": f"HMS_{wiki_slug}",
            "msg": "Unknown HMS Error",
            "module": "System",
            "severity": "Error",
            "is_critical": False,
            "type": "device_hms",
            "url": f"https://e.bambulab.com/?e={ecode}",
        }

        mid = (attr >> 24) & 0xFF
        mask = (attr >> 16) & 0xFF
        module_map = {
            0x03: "Mainboard",
            0x05: "AMS",
            0x12: "AMS",
            0x07: "Toolhead",
            0x0B: "Webcam",
            0x10: "HMS",
        }
        res["module"] = module_map.get(mid, "System")

        msg_list = HMS_STATUS.get("data", {}).get("device_hms", {}).get("en", [])
        for entry in msg_list:
            if entry.get("ecode", "").upper() == ecode:
                res["msg"] = entry.get("intro", res["msg"])
                break

        if mask in (0x00, 0x01):
            res["severity"], res["is_critical"] = (
                ("Fatal" if mask == 0x00 else "Error"),
                True,
            )
        elif mask == 0x02:
            res["severity"] = "Warning"
        else:
            res["severity"] = "Info"
        decoded_errors.append(res)
    return decoded_errors


@staticmethod
def getAMSModelBySerial(serial: str) -> AMSModel:
    """
    Returns the hardware model based on the serial number prefix.
    """
    prefix = serial[:3].upper()
    if prefix == "19C":
        return AMSModel.AMS_2_PRO
    if prefix == "19F":
        return AMSModel.AMS_HT
    if prefix == "006":
        return AMSModel.AMS_1
    if prefix == "03C":
        return AMSModel.AMS_LITE
    return AMSModel.UNKNOWN


@staticmethod
def getAMSSeriesByModel(model: AMSModel) -> AMSSeries:
    """
    Returns the AMS series enum based on the provided model.
    """
    if model in (AMSModel.AMS_1, AMSModel.AMS_LITE):
        return AMSSeries.GEN_1
    if model in (AMSModel.AMS_HT, AMSModel.AMS_2_PRO):
        return AMSSeries.GEN_2
    return AMSSeries.UNKNOWN


@staticmethod
@deprecated("This method is deprecated (v1.0.0). Use `getPrinterModelBySerial`.")
def getModelBySerial(serial: str) -> PrinterModel:
    return getPrinterModelBySerial(serial)


@staticmethod
def getPrinterModelBySerial(serial: str) -> PrinterModel:
    """
    Returns the Printer model enum based on the provided serial #.
    """
    mapping = {
        "00M": PrinterModel.X1C,
        "00W": PrinterModel.X1,
        "03W": PrinterModel.X1E,
        "01S": PrinterModel.P1P,
        "01P": PrinterModel.P1S,
        "030": PrinterModel.A1_MINI,
        "039": PrinterModel.A1,
        "22E": PrinterModel.P2S,
        "093": PrinterModel.H2S,
        "094": PrinterModel.H2D,
    }
    prefix = serial[:3]
    return mapping.get(prefix, PrinterModel.UNKNOWN)


@staticmethod
def getPrinterSeriesByModel(model: PrinterModel) -> PrinterSeries:
    """
    Returns the Printer series enum based on the provided model.
    """
    try:
        return PrinterSeries[model.name[:2]]
    except (KeyError, AttributeError):
        return PrinterSeries.UNKNOWN


@staticmethod
@deprecated("This method is deprecated (v1.0.0). Use `getPrinterSeriesByModel`.")
def getSeriesByModel(model: PrinterModel) -> PrinterSeries:
    return getPrinterSeriesByModel(model)


@staticmethod
def parseAMSInfo(info_int: int) -> dict:
    """
    Parses decimal bit-packed AMS info for status and feature reconciliation.
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
        "is_rotating": bool(info_int & 1024),
        "venting_active": bool(info_int & 2048),
        "high_power_mode": bool(info_int & 8192),
        "hardware_fault": bool((info_int & 4096) or (info_int & 16384)),
    }


@staticmethod
def parseAMSStatus(status_int: int) -> str:
    """
    Maps the ams_status code to human-readable descriptions.
    """
    main_status = (status_int >> 8) & 0xFF
    status_map = {
        0x00: "Idle",
        0x01: "Filament Changing",
        0x02: "RFID Identifying",
        0x03: "Assist/Engaged",
        0x04: "Calibration",
        0x10: "Self Check",
        0x20: "Debug",
        0xFF: "Unknown",
    }
    return status_map.get(main_status, "Idle")


@staticmethod
def parseExtruderInfo(info_int: int) -> ExtruderInfoState:
    """
    Decodes the extruder 'info' bit-packed status using unique ExtruderInfoState names.
    """
    if not (info_int & 0x08):
        return ExtruderInfoState.NO_NOZZLE
    if info_int & 0x02:
        return ExtruderInfoState.LOADED
    if info_int & 0x04:
        return ExtruderInfoState.BUFFER_LOADED
    return ExtruderInfoState.EMPTY


@staticmethod
def parseExtruderStatus(stat_int: int) -> ExtruderStatus:
    """
    Decodes the operational extruder state using the exhaustive Enum map.
    """
    working_bits = (stat_int >> 8) & 0x03
    if working_bits in (0x02, 0x03):
        return ExtruderStatus.ACTIVE
    if stat_int & 0x01:
        return ExtruderStatus.HEATING
    return ExtruderStatus.IDLE


@staticmethod
def parseExtruderTrayState(extruder: int, idx, status) -> int:
    if (
        idx == 254
        or (extruder == 0 and status == 65280)
        or (extruder == 1 and status == 65024)
    ):
        return 255 - extruder
    if (extruder == 0 and status & 0xFF == 255) or (
        extruder == 1 and status & 0xFE == 255
    ):
        return -1
    else:
        return status & 0xFF


@staticmethod
@deprecated("This property is deprecated (v1.0.0). Use `scaleFanSpeed`.")
def parseFan(fan: int) -> int:
    """
    !!! danger "Deprecated"
    This property is deprecated (v1.0.0). Use `scaleFanSpeed`.
    """
    fan_map = {
        1: 10,
        2: 20,
        3: 30,
        4: 30,
        5: 40,
        6: 40,
        7: 50,
        8: 50,
        9: 60,
        10: 70,
        11: 70,
        12: 80,
        13: 90,
        14: 90,
        15: 100,
    }
    return fan_map.get(int(fan), 0)


@staticmethod
def parseRFIDStatus(status):
    """
    Can be used to parse `ams_rfid_status`
    """
    rfid_map = {
        0: "RFID Idle",
        1: "RFID Reading",
        2: "GCode Translating",
        3: "GCode Running",
        4: "RFID Assistant",
        5: "Switch Filament",
        6: "Has Filament",
    }
    return rfid_map.get(status, "Unknown")


@staticmethod
def parseStage(stage_int: int) -> str:
    """
    Maps stg_cur numeric codes to human-readable print stages.
    """
    stage_map = {
        -1: "",
        0: "",
        1: "Auto bed leveling",
        2: "Heatbed preheating",
        3: "Sweeping XY mech mode",
        4: "Changing filament",
        5: "M400 pause",
        6: "Filament runout pause",
        7: "Heating hotend",
        8: "Calibrating extrusion",
        9: "Scanning bed surface",
        10: "Inspecting first layer",
        11: "Identifying build plate",
        12: "Calibrating Micro Lidar",
        13: "Homing toolhead",
        14: "Cleaning nozzle tip",
        15: "Temp check",
        16: "Paused by user",
        17: "Front cover falling",
        18: "Lidar calibration (alt)",
        19: "Calibrating flow",
        20: "Nozzle temp malfunction",
        21: "Bed temp malfunction",
        22: "Filament unloading",
        23: "Skip step pause",
        24: "Filament loading",
        25: "Motor noise calibration",
        26: "AMS lost pause",
        27: "Fan speed pause",
        28: "Chamber control error",
        29: "Cooling chamber",
        30: "Custom Gcode pause",
        31: "Motor noise showoff",
        32: "Nozzle cover pause",
        33: "Cutter error pause",
        34: "First layer error pause",
        35: "Nozzle clog pause",
        37: "Chamber control",
        38: "Chamber pre-heat (Legacy)",
        39: "Nozzle Offset Calibration",
        49: "Heating chamber",
        70: "Leading filament",
        71: "Reached toolhead",
        72: "Grabbing filament",
        73: "Purging",
        74: "Unloading",
        75: "Returning to AMS",
        76: "Cutting",
        77: "Tool switching",
        100: "Printing",
        255: "Completed",
    }
    return stage_map.get(stage_int, f"Stage [{stage_int}]")


@staticmethod
def resolveAMSDryingStage(parsed: dict, dry_time: int) -> AMSDryingStage:
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


@staticmethod
def scaleFanSpeed(raw_val: Any) -> int:
    """
    Scales proprietary 0-15 fan speed values to a 0-100 percentage.
    """
    try:
        val = int(raw_val)
        return min(max(round((val / 15.0) * 100), 0), 100)
    except Exception:
        return 0


@staticmethod
def sortFileTreeAlphabetically(source) -> dict:
    """
    Sorts a dict of file/directory nodes hierarchically.
    """

    def sort_node_list(node_list):
        for item in node_list:
            if item.get("id", "").endswith("/") and "children" in item:
                item["children"] = sort_node_list(item["children"])
        return sorted(
            node_list,
            key=lambda i: (not i.get("id", "").endswith("/"), i.get("name", "").lower()),
        )

    source["children"] = sort_node_list(source["children"])
    return source


@staticmethod
def unpackTemperature(raw_temp: int) -> tuple[float, float]:
    """
    Unpacks a 32-bit packed temperature integer into a tuple of (Actual, Target).
    """
    return float(raw_temp & 0xFFFF), float((raw_temp >> 16) & 0xFFFF)
