[![PyPI version](https://badge.fury.io/py/bambu-printer-manager.svg)](https://badge.fury.io/py/bambu-printer-manager)

# bambu-printer-manager
`bambu-printer-manager` is an all in one pure python wrapper for interacting with and managing Bambu Lab printers.

## Documentation
All documentation for `bambu-printer-manager` can be found [here](https://synman.github.io/bambu-printer-manager/).
[DeepWiki](https://deepwiki.com/synman/bambu-printer-manager) is another good source.

## Become a Sponsor
While caffiene and sleepness nights drive the delivery of this project, they unfortunately do not cover the financial expense necessary to further its development.  Please consider becoming a `bambu-printer-manager` sponsor today!

[![Sponsor](https://img.shields.io/badge/Sponsor-%E2%9D%A4-red?style=for-the-badge&logo=github)](https://github.com/sponsors/synman)

## Project Composition

    bpm/
        bambucommands.py                # collection of constants mainly representing Bambu Lab `mqtt` request commands
        bambuconfig.py                  # contains the `BambuConfig` class used for storing configuration data
        bambuprinter.py                 # the main `bambu-printer-manager` class `BambuPrinter` lives here
        bambuproject.py                 # provides `ActiveJobInfo` and `ProjectInfo` for tracking print job details
        bambuspool.py                   # contains the `BambuSpool` class used for storing spool data
        bambustate.py                   # contains the `BambuState` and `AMSUnitState` classes
        bambutools.py                   # contains a collection of methods used as tools (mostly internal)

        ftpsclient/
            _client.py              # internal class used for performing `FTPS` operations

### Dependencies
```
Python 3.11+

* mkdocstrings, webcolors, and paho-mqtt install automatically as predefined dependencies
```

### Installation
```
pip install bambu-printer-manager
```

### Basic Usage
```py
import time
import sys
import os

from bpm.bambuconfig import BambuConfig
from bpm.bambuprinter import BambuPrinter
from bpm.bambutools import parseStage, ServiceState

# Setup configuration
config = BambuConfig(
    hostname=os.getenv('BAMBU_HOSTNAME'),
    access_code=os.getenv('BAMBU_ACCESS_CODE'),
    serial_number=os.getenv('BAMBU_SERIAL_NUMBER')
)
printer = BambuPrinter(config=config)

# Start session
printer.start_session()

# Wait for connection
while printer.service_state != ServiceState.CONNECTED:
    time.sleep(1)

# Main loop
while True:
    state = printer.printer_state
    print(f"Tool Temp: {state.active_nozzle_temp}/{state.active_nozzle_temp_target}")
    time.sleep(1)
```

## Need Help?
Open an issue [here](https://github.com/synman/bambu-printer-manager/issues).

## Want to Contribute?
The best way you can contribute to this project is to make a monetary donation to its author. All funds received will go to the purchase of Bambu Lab hardware to support the continued development of this project. Please show your support by becoming a [Sponsor](https://github.com/sponsors/synman) today!

Developers are encouraged to submit a Pull Request to [devel](https://github.com/synman/bambu-printer-manager/compare)!

Please make sure to install pre-commit and lint and format your contributions through it:

```
pip install .[develop]
pre-commit install
```
