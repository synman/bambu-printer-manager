"""
`bambutools' hosts various classes and methods used internally and externally
by `bambu-printer-manager`.
"""

from enum import Enum, IntEnum


@staticmethod
def parseStage(stage: int) -> str:
    """
    Mainly an internal method used for parsing stage data from the printer.
    """
    if stage == 0:
        return ""
    elif stage == 1:
        return "Auto bed leveling"
    elif stage == 2:
        return "Heatbed preheating"
    elif stage == 3:
        return "Sweeping XY mech mode"
    elif stage == 4:
        return "Changing filament"
    elif stage == 5:
        return "M400 pause"
    elif stage == 6:
        return "Paused due to filament runout"
    elif stage == 7:
        return "Heating hotend"
    elif stage == 8:
        return "Calibrating extrusion"
    elif stage == 9:
        return "Scanning bed surface"
    elif stage == 10:
        return "Inspecting first layer"
    elif stage == 11:
        return "Identifying build plate type"
    elif stage == 12:
        return "Calibrating Micro Lidar"
    elif stage == 13:
        return "Homing toolhead"
    elif stage == 14:
        return "Cleaning nozzle tip"
    elif stage == 15:
        return "Checking extruder temperature"
    elif stage == 16:
        return "Printing was paused by the user"
    elif stage == 17:
        return "Pause of front cover falling"
    elif stage == 18:
        return "Calibrating the micro lida"
    elif stage == 19:
        return "Calibrating extrusion flow"
    elif stage == 20:
        return "Paused due to nozzle temperature malfunction"
    elif stage == 21:
        return "Paused due to heat bed temperature malfunction"
    elif stage == 22:
        return "Filament unloading"
    elif stage == 23:
        return "Skip step pause"
    elif stage == 24:
        return "Filament loading"
    elif stage == 25:
        return "Motor noise calibration"
    elif stage == 26:
        return "Paused due to AMS lost"
    elif stage == 27:
        return "Paused due to low speed of the heat break fan"
    elif stage == 28:
        return "Paused due to chamber temperature control error"
    elif stage == 29:
        return "Cooling chamber"
    elif stage == 30:
        return "Paused by the Gcode inserted by user"
    elif stage == 31:
        return "Motor noise showoff"
    elif stage == 32:
        return "Nozzle filament covered detected pause"
    elif stage == 33:
        return "Cutter error pause"
    elif stage == 34:
        return "First layer error pause"
    elif stage == 35:
        return "Nozzle clog pause"
    return ""


@staticmethod
def parseFan(fan: int) -> int:
    """
    Mainly an internal method used for parsing Fan data
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
def parseAMSInfo(info: int, has_temp: bool = False):
    """
    Mainly an internal method used for parsing AMS Info data
    """
    # BASE BITS: Shared across all AMS generations
    status = {
        "is_powered": bool(info & (1 << 0)),  # Bit 0
        "is_connected": bool(info & (1 << 1)),  # Bit 1
        "rfid_ready": bool(info & (1 << 2)),  # Bit 2
        "hub_sensor_triggered": bool(info & (1 << 3)),  # Bit 3
        "circ_fan_on": bool(info & (1 << 4)),  # Bit 4
        "exhaust_fan_on": bool(info & (1 << 5)),  # Bit 5
        "humidity_sensor_ok": bool(info & (1 << 6)),  # Bit 6
        "heater_on": bool(info & (1 << 7)),  # Bit 7
    }

    # ADVANCED BITS: H2D / AMS 2 Pro specific
    if has_temp:
        status.update(
            {
                "is_rotating": bool(info & (1 << 14)),  # Bit 13
                "venting_active": bool(info & (1 << 13)),  # Bit 14
                "high_power_mode": bool(info & (1 << 17)),  # Bit 17
                "hardware_fault": bool(info & (1 << 30)),  # Bit 30
            }
        )
    else:
        # Defaults for legacy AMS (X1/P1/A1)
        status.update(
            {
                "is_rotating": False,
                "venting_active": False,
                "high_power_mode": False,
                "hardware_fault": False,
            }
        )

    return status


@staticmethod
def parseAMSStatus(status):
    """
    Can be used to parse `ams_status`
    """
    if status == 0:
        return "Offline"
    elif status == 768:
        return "Idle"
    elif status == 1024:
        return "Pre-loading"
    elif status == 1280:
        return "Loading"
    elif status == 1536:
        return "Unloading"
    elif status == 1792:
        return "Cutting"
    elif status == 2048:
        return "Switching"
    elif status == 2304:
        return "Stall/Error"
    else:
        return "Unknown"


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


@staticmethod
def parseExtruderInfo(bits: int) -> str:
    """Parses the info_bits bitmask into a comma-separated string."""
    flags = []
    if bits & 1:
        flags.append("Detected")
    if bits & 2:
        flags.append("Loaded")
    if bits & 4:
        flags.append("Motor")
    if bits & 8:
        flags.append("Fan")
    if bits & 16:
        flags.append("Heating")
    if bits & 32:
        flags.append("Clog/Res")  # Bit 5 often reserved or clog
    if bits & 64:
        flags.append("Error")
    return ", ".join(flags) if flags else "Idle"


@staticmethod
def parseExtruderState(state_val: int) -> str:
    """Parses the state bitmask to determine operational status."""
    # Check bits 8 and 9 (0x300 = 768) which indicate the active driving tool
    if (state_val & 0x300) == 0x300:
        return "Active"
    return "Idle"


class PrinterState(Enum):
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
    Enum representing the currently active toolhead/extruder.

    Attributes:
        INACTIVE (-1): No tool is currently active or filament is unloaded.
        RIGHT_EXTRUDER (0): The primary or right-side extruder (Tool 0).
        LEFT_EXTRUDER (1): The secondary or left-side extruder (Tool 1).
    """

    INACTIVE = -1
    RIGHT_EXTRUDER = 0
    LEFT_EXTRUDER = 1


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
        # 1. Recursively sort the contents of any sub-directories first
        for item in node_list:
            if item.get("id", "").endswith("/") and "children" in item:
                item["children"] = sort_node_list(item["children"])

        # 2. Define the custom sorting key
        def sort_key(item):
            # The sort key tuple:
            # 1. Directory Precedence: True (directory) maps to 0, False (file) maps to 1.
            # 2. Alphabetical Order: The cleaned name is used for the case-insensitive sort.
            return (not item.get("id", "").endswith("/"), item.get("name", "").lower())

        # Apply the custom sort logic
        return sorted(node_list, key=sort_key)

    source["children"] = sort_node_list(source["children"])
    return source
