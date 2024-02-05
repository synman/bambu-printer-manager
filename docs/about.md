[![PyPI version](https://badge.fury.io/py/bambu-printer-manager.svg)](https://badge.fury.io/py/bambu-printer-manager)

# About bambu-printer-manager 
`bambu-printer-manager` is an all in one pure python wrapper for interacting with and managing Bambu Labs printers.

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