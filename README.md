[![PyPI version](https://badge.fury.io/py/bambu-printer-manager.svg)](https://badge.fury.io/py/bambu-printer-manager)

## bambu-printer-manager is an all in one pure python wrapper for interacting with and managing Bambu Labs printers.

### Dependencies
```
Python 3.12.1+

* webcolors and paho-mqtt install automatically 
```
### Installation
```
pip install bambu-printer-manager
```
### Imports
```py
from bpm.bambuconfig import BambuConfig
from bpm.bambuprinter import BambuPrinter
from bpm.bambutools import PrinterState
from bpm.bambutools import parseStage
from bpm.bambutools import parseFan
```

### Constructor(s)
```py
config = BambuConfig(hostname="{host name}", access_code="{access code}", serial_number="{serial #}")
printer = BambuPrinter(config=config)
```
or variations such as:
```py
config = BambuConfig()
printer = BambuPrinter()

config.hostname = "{host name}"
config.access_code = "{access code}"
config.serial_number = "{serial #}"

printer.config = config
```
or
```py
config = BambuConfig()

config.hostname = "{host name}"
config.access_code = "{access code}"
config.serial_number = "{serial #}"

printer = BambuPrinter(config=config)
```
or even
```py
printer = BambuPrinter(config=BambuConfig(hostname="{host name}", access_code="{access code}", serial_number="{serial #}"))
```
## BambuPrinter 
### Methods
`start_session()`
Starts the main processing loop (non-blocking) for connecting to the printer, sending commands, and receiving data updates via a callback.

`pause_session()`
Pauses the session (if it is active) preventing data updates from being received.  You can still send commands to the printer when `BambuPrinter` is in this state.

`resume_session()`
Resumes the session (if it is paused) and reactivates the receiption of data updates from the printer.

`quit()`
Disconnects from the printer, ends the session (if one is active), and tears down all background processes / threads.

`refresh()`
Requests a full data refresh from the printer asynchronously.  This is typically not necessary as all printer properties are typically populated within the first two or three data update cycles.  

`unload_filament()`
Unloads whatever filament/spool is currently loaded into the extruder.

`load_filament(slot)`
Loads the External feeder (spool id `254`), or one of the AMS / AMS-Lite spools (base 0) into the extruder.

Example:
```py
printer.load_filament(3)   # loads AMS spool #4 into the extruder
```

`send_gcode(gcode)`
Allows you to send GCode commands to the printer and supports multiple GCode commands `\n` delimited.

Example:
```py
printer.send_gcode("G28 XY")        # homes the X and Y axes
printer.send_gcode("G28 XY\nG28 Z") # homes XY and then homes Z
```

`print_3mf_file(name, bed, ams)`
Instructs the printer to print a `.3mf` previously uploaded to the printer's SDCard.  

* `name` is the path and filename of the `.3mf` file to print (without the extension).
* `bed` specifies which plate should be selected.  Currently supports `auto`, `hot_plate`, or `textured_plate`.
* `ams` should be blank if you are using the External feeder or be a valid `ams mapping` if using one or more spools from the AMS / AMS-Lite.  

Example:
```py
# print a file at the root of the SDCard using spools 2 and 3 in the AMS on the PEI hot plate
printer.print_3mf_file("my_cool_model", "hot_plate", "[-1, 1, 2, -1]")

# print a file in the jobs directory of the SDCard using spool 1  in the AMS on the textured plate
printer.print_3mf_file("jobs/my_cool_model", "textured_plate", "[0, -1, -1, -1]")

# print a file at the root of the SDCard using the External feeder on the PEI hot plate
printer.print_3mf_file("my_cool_model", "hot_plate", "")
```

`stop_printing()`
Halts a print job if one is running.

`pause_printing()`
Pauses the print job if one is running.

`resume_printing()`
Resumes the print job if one is paused.

`jsonSerializer()`
This method allows you to override the `json.dumps`default serializer for converting `BambuPrinter` into a serialized json document.

Example:
```py
print(json.dumps(printer, default=printer.jsonSerializer, indent=4, sort_keys=True))
```

### Properties
```py
self._internalException = None
self._lastMessageTime = None

self._config = config
self._state = PrinterState

self._client = None
self._on_update = None

self._bed_temp = 0.0
self._bed_temp_target = 0.0
self._tool_temp = 0.0
self._tool_temp_target = 0.0
self._chamber_temp = 0.0
self._chamber_temp_target = 0.0

self._fan_gear = 0
self._heatbreak_fan_speed = 0
self._fan_speed = 0

self._light_state = "N/A"
self._wifi_signal = "N/A"
self._speed_level = 0

self._gcode_state = "N/A"
self._gcode_file = "N/A"
self._print_type = "N/A"
self._percent_complete = 0
self._time_remaining = 0
self._layer_count = 0
self._current_layer = 0

self._current_stage = 0
self._current_stage_text = "N/A"

self._spools = ()
self._target_spool = 255
self._active_spool = 255
self._spool_state = "N/A"
self._ams_status = None
```
`on_update` (setter only)
Set a callback method that is invoked whenever new data is received from the printer.  Your `BambuPrinter` instance is passed into your callback method for convienence.

Example:
```py
def on_update(printer):

    print(f"tool=[{round(printer.tool_temp, 1)}/{round(printer.tool_temp_target, 1)}] " +
          f"bed=[{round(printer.bed_temp, 1)}/{round(printer.bed_temp_target, 1)}] " + 
          f"fan=[{parseFan(printer.fan_speed)}] print=[{printer.gcode_state}] speed=[{printer.speed_level}] " +
          f"light=[{'on' if printer.light_state else 'off'}]")
    
    print(f"stg_cur=[{parseStage(printer.current_stage)}] file=[{printer.gcode_file}] " +
          f"layers=[{printer.layer_count}] layer=[{printer.current_layer}] " +
          f"%=[{printer.percent_complete}] eta=[{printer.time_remaining} min] " +
          f"spool=[{printer.active_spool} ({printer.spool_state})]")

printer.on_update = on_update
```

`config` (getter & setter)
Returns a reference to your `BambuConfig` configuration value object or allows you to set one (do not attempt to set a new `config` value while a session is active).  See [Constructor(s)](###Constructor(s)) for examples.

`state` (getter only)
Returns the current `PrinterState`.
```py
class PrinterState(Enum):
    CONNECTED = 1,
    DISCONNECTED = 2,
    PAUSED = 3,
    QUIT = 4
```

`client` (getter and setter)
Provides direct access to the underlying MQTT client class.  Usage of this property should not be necessary but is provided just in case.

`bed_temp` (getter only)
Returns the current bed temperature.

`bed_temp_target` (getter and setter)
Returns the target bed temperature or allows you set a new one.

`tool_temp` (getter only)
Returns the current tool0 temperature.

`tool_temp_target` (getter and setter)
Returns the target tool0 temperature or allows you set a new one.

`chamber_temp` (getter only)
Returns the chamber temperature (if supported).

`fan_speed` (getter and setter)
Returns or sets the cooling fan speed in %.

`fan_gear` (getter only)
Returns the fan gear speed (if supported).

`heatbreak_fan_speed` (getter only)
Returns the heatbreak / extruder fan speed in %.

`light_state` (getter and setter)
Returns the current boolean chamber light state or allows you to turn it on `(True)` or off `(False)`.

`speed_level` (getter and setter)
Returns the current printer speed level or allows you set a new one.

Example:
```py
printer.pause_session()
speed = input("New speed (1=silent 2=standard 3=sport 4=ludicrous): ")
printer.resume_session()

if len(speed) > 0 and speed in ("1", "2", "3", "4"):
    printer.speed_level = int(speed)
```

`gcode_state` (getter only)
Returns the currect GCode processing state of the printer.  Can be `IDLE`, `RUNNING`, `FAILED`, `PAUSED`, `FINISH`, etc.

`gcode_file` (getter and setter)
Returns the current active gcode / 3mf filename and can be set to trigger execution of a gcode (.gcode only) file on the printer's SDCard.

`spools` (getter only)
Returns a `Tuple` of `BambuSpool` objects currently active on the Printer.  The `id` attributes in the `BambuSpool` objects correspond to the `active_spool`, `target_spool`, `slot`, etc references you see within `BambuPrinter`.

######Listing not complete - more to come soon

## BambuConfig
`BambuConfig` is used by `bambu-printer-manager` for maintaining various configuration item values it requires to run properly.  The most common used properties are `hostname`, `access_code`, and `serial_number`.

`BambuConfig` must be set in your instantiated `BambuPrinter` object's `config` property prior to calling the `BambuPrinter` `start_session()` method.
### Properties
```py
hostname=None, 
access_code=None, 
serial_number=None, 
mqtt_port=8883, 
mqtt_client_id="studio_client_id:0c1f",
mqtt_username="bblp",
verbose=False
```
`verbose` (getter and setter)
Setting `verbose` to `True` will enable (exhaustive) file and stdout logging

## BambuSpool
`BambuSpool` is the value object used for reporting on the spools currently available for use with your printer and is returned as a `Tuple` from the `BambuPrinter` `spools` property. 

The `id` attributes (base 0) correspond to the AMS / AMS-lite loaded spools as well as the External feeder `id=254`.
### Properties
```py
self.id = id
self.name = name
self.type = type
self.sub_brands = sub_brands
self.color = color
``` 
##### -
#### This page is a work in progress
