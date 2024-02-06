"""
`bambutools' hosts various classes and methods used internally and externally
by `bambu-printer-manager`.
"""
from enum import Enum

def parseStage(stage: int) -> str:
    """
    Mainly an internal method used for parsing stage data from the printer.
    """
    if type(stage) is int or stage.isnumeric():
        stage = int(stage)
        if stage == 0: return ""
        elif stage == 1: return "Auto bed leveling"
        elif stage == 2: return "Heatbed preheating"
        elif stage == 3: return "Sweeping XY mech mode"
        elif stage == 4: return "Changing filament"
        elif stage == 5: return "M400 pause"
        elif stage == 6: return "Paused due to filament runout"
        elif stage == 7: return "Heating hotend"
        elif stage == 8: return "Calibrating extrusion"
        elif stage == 9: return "Scanning bed surface"
        elif stage == 10: return "Inspecting first layer"
        elif stage == 11: return "Identifying build plate type"
        elif stage == 12: return "Calibrating Micro Lidar"
        elif stage == 13: return "Homing toolhead"
        elif stage == 14: return "Cleaning nozzle tip"
        elif stage == 15: return "Checking extruder temperature"
        elif stage == 16: return "Printing was paused by the user"
        elif stage == 17: return "Pause of front cover falling"
        elif stage == 18: return "Calibrating the micro lida"
        elif stage == 19: return "Calibrating extrusion flow"
        elif stage == 20: return "Paused due to nozzle temperature malfunction"
        elif stage == 21: return "Paused due to heat bed temperature malfunction"
        elif stage == 22: return "Filament unloading"
        elif stage == 23: return "Skip step pause"
        elif stage == 24: return "Filament loading"
        elif stage == 25: return "Motor noise calibration"
        elif stage == 26: return "Paused due to AMS lost"
        elif stage == 27: return "Paused due to low speed of the heat break fan"
        elif stage == 28: return "Paused due to chamber temperature control error"
        elif stage == 29: return "Cooling chamber"
        elif stage == 30: return "Paused by the Gcode inserted by user"
        elif stage == 31: return "Motor noise showoff"
        elif stage == 32: return "Nozzle filament covered detected pause"
        elif stage == 33: return "Cutter error pause"
        elif stage == 34: return "First layer error pause"
        elif stage == 35: return "Nozzle clog pause"
        return ""

def parseFan(fan: int) -> str:
    """
    Mainly an internal method used for parsing Fan data
    """
    if type(fan) is int or fan.isnumeric():
        fan = int(fan)
        if fan == 1: return 10
        elif fan == 2: return 20
        elif fan in (3, 4): return 30
        elif fan  in (5, 6): return 40
        elif fan in (7, 8): return 50
        elif fan == 9: return 60
        elif fan in (10, 11): return 70
        elif fan == 12: return 80
        elif fan in (13, 14): return 90
        elif fan == 15: return 100
    return 0

def parseAMSStatus(status: int) -> str:
    """
    Can be used to parse `ams_status`
    """
    main_status = (status & 0xFF00) >> 8
    # sub_status = status & 0xFF
    if main_status == 0x00:
        return "AMS Idle"
    elif main_status == 0x01:
        return "AMS Filament Change"
    elif main_status == 0x02:
        return "AMS RFID Identifying"
    elif main_status == 0x03:
        return "AMS Assist"
    elif main_status == 0x04:
        return "AMS Calibration"
    elif main_status == 0x10:
        return "AMS Self-Check"
    elif main_status == 0x20:
        return "AMS Debug"
    else:
      return "Unknown"

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
    NO_STATE = 0,
    CONNECTED = 1,
    DISCONNECTED = 2,
    PAUSED = 3,
    QUIT = 4

class PlateType(Enum):
    """
    Used by `BambuPrinter.print_3mf_file` to specify which plate should be used when 
    starting a print job.
    """
    AUTO = 0,
    COOL_PLATE = 1,
    HOT_PLATE = 2,
    TEXTURED_PLATE = 3