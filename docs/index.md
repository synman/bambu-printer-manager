[![PyPI version](https://badge.fury.io/py/bambu-printer-manager.svg)](https://badge.fury.io/py/bambu-printer-manager)

# bambu-printer-manager
`bambu-printer-manager` is an all in one pure python wrapper for interacting with and managing Bambu Labs printers.  

## Project Composition

    bpm/  
        bambucommands.py            # collection of constants representing Bambu Lab `mqtt` request commands 
        bambuconfig.py              # contains the `BambuConfig` class used for storing configuration data
        bambulogger.py              # internal class used for logging
        bambuprinterlogger.json     # internal configuration file for configuration of logging
        bambuprinter.py             # the main `bambu-printer-manager` class `BambuPrinter` lives here
        bambuspool.py               # contains the `BambuSpool` class used for storing spool data
        bambutools.py               # contains a collection of methods used as tools (mostly internal)

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