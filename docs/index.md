[![PyPI version](https://badge.fury.io/py/bambu-printer-manager.svg)](https://badge.fury.io/py/bambu-printer-manager)

# bambu-printer-manager
`bambu-printer-manager` is an all in one pure python wrapper for interacting with and managing Bambu Lab printers.

## Become a Sponsor
While caffiene and sleepness nights drive the delivery of this project, they unfortunately do not cover the financial expense necessary to further its development.  Please consider becoming a `bambu-printer-manager` sponsor today!
<iframe src="https://github.com/sponsors/synman/button" title="Sponsor synman" height="32" width="114" style="border: 0; border-radius: 6px;"></iframe>

## Project Composition

    bpm/
        bambucommands.py                # collection of constants mainly representing Bambu Lab `mqtt` request commands
        bambuconfig.py                  # contains the `BambuConfig` class used for storing configuration data
        bambuprintermanagerlogger.json  # internal configuration file for configuration of logging
        bambuprinter.py                 # the main `bambu-printer-manager` class `BambuPrinter` lives here
        bambuspool.py                   # contains the `BambuSpool` class used for storing spool data
        bambutools.py                   # contains a collection of methods used as tools (mostly internal)

        ftpsclient/
            _client.py              # internal class used for performing `FTPS` operations

### Dependencies
```
Python 3.12.1+

* mkdocstrings, webcolors and paho-mqtt install automatically as predefined dependencies
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

### Usage Patterns
You can either poll `BambuPrinter` periodically for data updates or rely on a callback when
new data becomes available.  The preferred pattern should be callback based, however both
of these approaches will work fine.

Please consider the examples provided here as mere starting points.

#### Data Polling Example
```py
import time
import sys
import os

from bpm.bambuconfig import BambuConfig
from bpm.bambuprinter import BambuPrinter
from bpm.bambutools import PrinterState

hostname = os.getenv('BAMBU_HOSTNAME')
access_code = os.getenv('BAMBU_ACCESS_CODE')
serial_number = os.getenv('BAMBU_SERIAL_NUMBER')

if not hostname or not access_code or not serial_number:
    print()
    print("BAMBU_HOSTNAME, BAMBU_ACCESS_CODE, and BAMBU_SERIAL_NUMBER environment variables must be set")
    print()
    sys.exit(1)

config = BambuConfig(hostname=hostname, access_code=access_code, serial_number=serial_number)
printer = BambuPrinter(config=config)

printer.start_session()

while printer.state != PrinterState.CONNECTED:
    print("waiting for bpm to connect to printer", flush=True)
    if printer.internalException:
        print(f"retrying connection - reason: {printer.internalException if not printer.internalException is None else "no internal exception"}")
        printer.start_session()
    time.sleep(1)

print("\r\nrefreshing sdcard 3mf files", flush=True)
printer.get_sdcard_3mf_files()
print("sdcard 3mf files refreshed\r\n", flush=True)

print("bpm is ready for business\r\n")

while True:
    print(f"tool=[{round(printer.tool_temp, 1)}/{round(printer.tool_temp_target, 1)}] " +
          f"bed=[{round(printer.bed_temp, 1)}/{round(printer.bed_temp_target, 1)}] " +
          f"fan=[{parseFan(printer.fan_speed)}] print=[{printer.gcode_state}] speed=[{printer.speed_level}] " +
          f"light=[{'on' if printer.light_state else 'off'}]")

    print(f"stg_cur=[{parseStage(printer.current_stage)}] file=[{printer.gcode_file}] " +
          f"layers=[{printer.layer_count}] layer=[{printer.current_layer}] " +
          f"%=[{printer.percent_complete}] eta=[{printer.time_remaining} min] " +
          f"spool=[{printer.active_spool} ({printer.spool_state})]")

    time.sleep(1)

@app.route('/api/printer')
def get_printer_info():
    global printer
    # checking both the spools tuple and recent_update
    # states ensure we have a healthy data stream
    if printer.recent_update and printer.spools:
        return printer.toJson()
    else:
        return {"status": "warn", "reason": "no data to send"}
```
#### Callback Pattern
```py
import sys
import os

from bpm.bambuconfig import BambuConfig
from bpm.bambuprinter import BambuPrinter
from bpm.bambutools import parseStage
from bpm.bambutools import parseFan

hostname = os.getenv('BAMBU_HOSTNAME')
access_code = os.getenv('BAMBU_ACCESS_CODE')
serial_number = os.getenv('BAMBU_SERIAL_NUMBER')

if not hostname or not access_code or not serial_number:
    print()
    print("BAMBU_HOSTNAME, BAMBU_ACCESS_CODE, and BAMBU_SERIAL_NUMBER environment variables must be set")
    print()
    sys.exit(1)

config = BambuConfig(hostname=hostname, access_code=access_code, serial_number=serial_number)
printer = BambuPrinter(config=config)

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
printer.start_session()

# go do other stuff
```

#### CLI w/ Callback
```py
import json
import traceback
import time
import sys
import os

from console.utils import wait_key

from bpm.bambuconfig import BambuConfig
from bpm.bambuprinter import BambuPrinter
from bpm.bambutools import PrinterState
from bpm.bambutools import parseStage
from bpm.bambutools import parseFan

gcodeState = ""
firmware = "N/A"
ams_firmware = "N/A"

def on_update(printer):
    global firmware, ams_firmware, gcodeState

    if gcodeState != printer.gcode_state:
        gcodeState = printer.gcode_state

    if firmware != printer.config.firmware_version:
        firmware = printer.config.firmware_version
        print(f"\r\nprinter firmware: [{firmware}] serial #: [{printer.config.serial_number}]\r")
    if ams_firmware != printer.config.ams_firmware_version:
        ams_firmware = printer.config.ams_firmware_version
        print(f"ams firmware: [{ams_firmware}]\r")

    print(f"\r\ntool=[{round(printer.tool_temp * 1.0, 1)}/{round(printer.tool_temp_target * 1.0, 1)}] " +
         f"bed=[{round(printer.bed_temp * 1.0, 1)}/{round(printer.bed_temp_target * 1.0, 1)}] " +
         f"fan=[{parseFan(printer.fan_speed)}] print=[{printer.gcode_state}] speed=[{printer.speed_level}] " +
         f"light=[{'on' if printer.light_state else 'off'}]")

    print(f"\rstg_cur=[{parseStage(printer.current_stage)}] file=[{printer.gcode_file}] " +
          f"layers=[{printer.layer_count}] layer=[{printer.current_layer}] " +
          f"%=[{printer.percent_complete}] eta=[{printer.time_remaining} min] " +
          f"spool=[{printer.active_spool} ({printer.spool_state})]\r")

print("\r")

hostname = os.getenv('BAMBU_HOSTNAME')
access_code = os.getenv('BAMBU_ACCESS_CODE')
serial_number = os.getenv('BAMBU_SERIAL_NUMBER')

if not hostname or not access_code or not serial_number:
    print()
    print("BAMBU_HOSTNAME, BAMBU_ACCESS_CODE, and BAMBU_SERIAL_NUMBER environment variables must be set")
    print()
    sys.exit(1)

config = BambuConfig(hostname=hostname, access_code=access_code, serial_number=serial_number)
printer = BambuPrinter(config=config)

printer.on_update = on_update
printer.start_session()

def confirm(request):
    printer.pause_session()
    resp = input(f"Confirm [{request}] (y/n): ")
    printer.resume_session()
    return resp == "y" or resp == "Y"

special = False

while True:
    key = wait_key()
    if key == "\x1b":
        special = True
        continue
    if special:
        if key == "[": continue
        if key == "C":  # right arrow
            # client.publish("device/{}/request".format(SERIAL), json.dumps(MOVE_RIGHT))
            print("\rmove right\r")
        if key == "D":  # left arrow
            # client.publish("device/{}/request".format(SERIAL), json.dumps(MOVE_LEFT))
            print("\rmove left\r")
        special = False
        continue

    if not special and key == "\r":
        print("\r")

    if key == "?":
        print("\r\nCommands:\r\n")
        print("   ? = this list\r")
        print("   b = bed target temperature\r")
        print("   d = dump printer json object\r")
        print("   g = send gcode command\r")
        print("   f = fan speed (in percent)\r")
        print("   l = toggle light\r")
        print("   p = print 3MF file\r")
        print("   q = quit\r")
        print("   Q = restart without exiting")
        print("   r = request full data refresh\r")
        print("   s = change filament / spool\r")
        print("   S = change speed (1 to 4)\r")
        print("   t = tool target temperature\r")
        print("   u = unload filament / spool\r")
        print("   v = toggle verbose reporting\r")
        print("   w = wifi signal strength\r")
        print("   ! = abort job\r")
        print("   ~ = toggle subscription\n\r")

    if key == "d":
        print(json.dumps(printer, default=printer.jsonSerializer, indent=4, sort_keys=True).replace("\n", "\r\n"))

    if key == "w":
        print(f"\r\nwifi signal strength: [{printer.wifi_signal}]")

    if key == "v":
        printer.config.verbose = not printer.config.verbose

    if key == "q":
        break

    if key == "Q":
        printer.quit()
        printer.start_session()

    if key == "l":
        printer.light_state = not printer.light_state

    if key == "t":
        printer.pause_session()
        temp = input("\r\nTool0 Target Temperature: ")
        printer.resume_session()
        if temp.isnumeric() and confirm("CHANGE_TOOL_TEMP"):
            printer.tool_temp_target = temp

    if key == "b":
        printer.pause_session()
        temp = input("\r\nBed Target Temperature: ")
        printer.resume_session()
        if temp.isnumeric():
            printer.bed_temp_target = temp

    if key == "f":
        printer.pause_session()
        speed = input("\r\nFan Speed (%): ")
        printer.resume_session()
        if speed.isnumeric():
            printer.fan_speed = speed

    if key == "r":
        printer.refresh()

    if key == "u" and confirm("UNLOAD_FILAMENT"):
        printer.unload_filament()

    if key == "s":
        printer.pause_session()
        slot = input("\r\nTarget Slot: ")
        printer.resume_session()
        if len(slot) > 0:
            printer.load_filament(slot)

    if key == "g":
        printer.pause_session()
        gcode = input("\r\nGcode: ")
        printer.resume_session()
        if len(gcode) > 0:
            printer.send_gcode(gcode)

    if key == "p":
        printer.pause_session()
        name = input("\r\n3MF filename to print: ")
        if len(name) > 0:
            bed = input("\rBed type (1=High Temp Plate, 2=Textured PEI Plate): ")
            if len(bed) > 0 and bed.isnumeric():
                ams = "[{}]".format(input("\rAMS mapping ([-1/0], [-1/1], [-1/2], [-1/3]): "))
                if len(ams) > 0:
                    printer.resume_session()
                    printer.print_3mf_file(name, bed, ams)
                    continue
        printer.resume_session()

    if key == "S":
        printer.pause_session()
        speed = input("\r\nNew speed (1=silent 2=standard 3=sport 4=ludicrous): ")
        printer.resume_session()
        if len(speed) > 0 and speed in ("1", "2", "3", "4"):
            printer.speed_level = speed

    if key == "!" and confirm("STOP"):
        printer.stop_printing()

    if key == "~":
        if printer.state == PrinterState.PAUSED:
            printer.resume_session()
            print("\rsession resumed\r")
        else:
            printer.pause_session()
            print("\rsession paused\r")

printer.quit()
```
