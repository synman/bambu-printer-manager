[![PyPI version](https://badge.fury.io/py/bambu-printer-manager.svg)](https://badge.fury.io/py/bambu-printer-manager)

# bambu-printer-manager
`bambu-printer-manager` is an all in one pure python wrapper for interacting with and managing Bambu Lab printers.

## Become a Sponsor
While caffiene and sleepness nights drive the delivery of this project, they unfortunately do not cover the financial expense necessary to further its development.  Please consider becoming a `bambu-printer-manager` sponsor today!
<iframe src="https://github.com/sponsors/synman/button" title="Sponsor synman" height="32" width="114" style="border: 0; border-radius: 6px;"></iframe>

## Project Composition

    bpm/
        bambucommands.py       # collection of constants mainly representing Bambu Lab `mqtt` request commands
        bambuconfig.py         # contains the `BambuConfig` class used for managing configuration data
        bambuprinter.py        # the main `bambu-printer-manager` class `BambuPrinter` lives here
        bambuproject.py        # provides `ActiveJobInfo` and `ProjectInfo` for tracking print job details
        bambuspool.py          # contains the `BambuSpool` class used for managing spool data
        bambustate.py          # contains the `BambuState` and `AMSUnitState` classes
        bambutools.py          # contains a collection of methods used as tools (mostly internal)

        ftpsclient/
            _client.py         # internal class used for performing `FTPS` operations

### Dependencies
```
Python 3.11+

* mkdocstrings, webcolors, and paho-mqtt install automatically as predefined dependencies
```
### Installation
```
pip install bambu-printer-manager
```
### Imports
```py
from bpm.bambuconfig import BambuConfig
from bpm.bambuprinter import BambuPrinter
from bpm.bambutools import parseStage
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
### Future Compatibility
This library is evolving and expect to see shifting variables and classes leading up to v1.0.0. Deprecated methods and attributes will be removed upon its release.

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
from bpm.bambutools import parseStage

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

while printer.service_state != ServiceState.CONNECTED:
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
    # Access state via printer.printer_state
    state = printer.printer_state
    job = printer.active_job_info

    print(f"tool=[{round(state.active_nozzle_temp, 1)}/{round(state.active_nozzle_temp_target, 1)}] " +
          f"bed=[{round(state.climate.bed_temp, 1)}/{round(state.climate.bed_temp_target, 1)}] " +
          f"fan=[{state.climate.part_cooling_fan_speed_percent}%] " +
          f"print=[{state.gcode_state}] speed=[{printer.speed_level}] " +
          f"light=[{'on' if printer.light_state else 'off'}]")

    print(f"stg_cur=[{parseStage(job.stage_id)}] file=[{job.gcode_file}] " +
          f"layers=[{job.total_layers}] layer=[{job.current_layer}] " +
          f"%=[{job.print_percentage}] eta=[{job.remaining_minutes} min] " +
          f"spool=[{state.active_tray_id} ({state.active_tray_state_name})]")

    time.sleep(1)
```

#### Callback Pattern
```py
import sys
import os

from bpm.bambuconfig import BambuConfig
from bpm.bambuprinter import BambuPrinter
from bpm.bambutools import parseStage

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
    state = printer.printer_state
    job = printer.active_job_info

    print(f"tool=[{round(state.active_nozzle_temp, 1)}/{round(state.active_nozzle_temp_target, 1)}] " +
          f"bed=[{round(state.climate.bed_temp, 1)}/{round(state.climate.bed_temp_target, 1)}] " +
          f"fan=[{state.climate.part_cooling_fan_speed_percent}%] " +
          f"print=[{state.gcode_state}] speed=[{printer.speed_level}] " +
          f"light=[{'on' if printer.light_state else 'off'}]")

    print(f"stg_cur=[{parseStage(job.stage_id)}] file=[{job.gcode_file}] " +
          f"layers=[{job.total_layers}] layer=[{job.current_layer}] " +
          f"%=[{job.print_percentage}] eta=[{job.remaining_minutes} min] " +
          f"spool=[{state.active_tray_id} ({state.active_tray_state_name})]")

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
from bpm.bambutools import ServiceState, parseStage

gcodeState = ""
firmware = "N/A"
ams_firmware = "N/A"

def on_update(printer):
    global firmware, ams_firmware, gcodeState

    state = printer.printer_state
    job = printer.active_job_info

    if gcodeState != state.gcode_state:
        gcodeState = state.gcode_state

    if firmware != printer.config.firmware_version:
        firmware = printer.config.firmware_version
        print(f"\r\nprinter firmware: [{firmware}] serial #: [{printer.config.serial_number}]\r")
    if ams_firmware != printer.config.ams_firmware_version:
        ams_firmware = printer.config.ams_firmware_version
        print(f"ams firmware: [{ams_firmware}]\r")

    print(f"\r\ntool=[{round(state.active_nozzle_temp, 1)}/{round(state.active_nozzle_temp_target, 1)}] " +
         f"bed=[{round(state.climate.bed_temp, 1)}/{round(state.climate.bed_temp_target, 1)}] " +
         f"fan=[{state.climate.part_cooling_fan_speed_percent}%] " +
         f"print=[{state.gcode_state}] speed=[{printer.speed_level}] " +
         f"light=[{'on' if printer.light_state else 'off'}]")

    print(f"\rstg_cur=[{parseStage(job.stage_id)}] file=[{job.gcode_file}] " +
          f"layers=[{job.total_layers}] layer=[{job.current_layer}] " +
          f"%=[{job.print_percentage}] eta=[{job.remaining_minutes} min] " +
          f"spool=[{state.active_tray_id} ({state.active_tray_state_name})]\r")

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
        print(f"\r\nwifi signal strength: [{printer.printer_state.wifi_signal_strength}]")

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
            printer.set_nozzle_temp_target(int(temp))

    if key == "b":
        printer.pause_session()
        temp = input("\r\nBed Target Temperature: ")
        printer.resume_session()
        if temp.isnumeric():
            printer.set_bed_temp_target(int(temp))

    if key == "f":
        printer.pause_session()
        speed = input("\r\nFan Speed (%): ")
        printer.resume_session()
        if speed.isnumeric():
            printer.set_part_cooling_fan_speed_target_percent(int(speed))

    if key == "r":
        printer.refresh()

    if key == "u" and confirm("UNLOAD_FILAMENT"):
        printer.unload_filament()

    if key == "s":
        printer.pause_session()
        slot = input("\r\nTarget Slot: ")
        printer.resume_session()
        if len(slot) > 0:
            printer.load_filament(int(slot))

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
                    # Note: PlateType enum usage would require import, kept simple with int/string for now
                    # assuming the user knows how to map it or we'd need to import PlateType
                    # For this example, we'll assume the user passes a valid int that matches the enum
                    from bpm.bambutools import PlateType
                    try:
                        plate_type = PlateType(int(bed))
                        printer.print_3mf_file(name, 1, plate_type, True, ams)
                    except ValueError:
                        print("Invalid bed type")
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
        if printer.service_state == ServiceState.PAUSED:
            printer.resume_session()
            print("\rsession resumed\r")
        else:
            printer.pause_session()
            print("\rsession paused\r")

printer.quit()
```

## Contributing

The best way you can contribute to this project is to make a monetary donation to its author. All funds received will go to the purchase of Bambu Lab hardware to support the continued development of this project. Please show your support by becoming a [Sponsor](https://github.com/sponsors/synman) today!

Developers are encouraged to submit a Pull Request to [devel](https://github.com/synman/bambu-printer-manager/compare)!

Please make sure to install pre-commit and lint and format your contributions through it:

```bash
pip install .[develop]
pre-commit install
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.1 | 2026-02-25 | Updated documentation with comprehensive examples and reference implementations |
| 1.0 | 2026-02-23 | Initial project documentation and getting started guide |
