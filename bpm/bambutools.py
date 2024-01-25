from enum import Enum

def parseStage(stage):
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

def parseFan(fan):
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

class PrinterState(Enum):
    CONNECTED = 1,
    DISCONNECTED = 2,
    PAUSED = 3,
    QUIT = 4

