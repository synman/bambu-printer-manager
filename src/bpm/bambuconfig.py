import os
import atexit
import logging.config
import logging.handlers
import json

from typing import Optional

from bpm.bambutools import getModelBySerial, PrinterModel

logger = logging.getLogger("bambuprinter")

class BambuConfig:
    """
    This is the main configuration class for `BambuPrinter` and is how it knows where to connect to a printer,
    what access code, and serial # to use.  `BambuConfig` can also be used to change the log level of 
    `bambu-printer-manager`'s logging engine.
    """
    def __init__(self, hostname: Optional[str] = None, 
                 access_code: Optional[str] = None, 
                 serial_number: Optional[str] = None, 
                 mqtt_port: Optional[int] = 8883, 
                 mqtt_client_id: Optional[str] = "studio_client_id:0c1f",
                 mqtt_username: Optional[str] = "bblp",
                 watchdog_timeout: Optional[int] = 30,
                 external_chamber: Optional[bool] = False,
                 verbose: Optional[bool] = False):
        """
        Sets up all internal storage attributes for `BambuConfig`.

        Parameters
        ----------
        * hostname : Optional[str] = None
        * access_code : Optional[str] = None 
        * serial_number : Optional[str] = None
        * mqtt_port : Optional[int] = 8883
        * mqtt_client_id : Optional[str] = "studio_client_id:0c1f"
        * mqtt_username : Optional[str] = "bblp"
        * watchdog_timeout : Optional[int] = 30
        * external_chamber : Optional[bool] = False
        * verbose : Optional[bool] = False

        `external_chamber` can be used to tell `BambuPrinter` not to use any of the chamber 
        temperature data received from the printer.  This can be useful if you are using an
        external chamber temperature sensor / heater and want to inject the sensor value and
        target temperatures into `BambuPrinter` directly.

        `verbose` triggers a global log level change (within the scope of `bambu-printer-manager`)
        based on its value.  `True` will set a log level of `DEBUG` and `False` (the default) will 
        set the log level to `WARNING`.
        
        Attributes
        ---------
        * All parameters listed above
        * _firmware_version : str - Reported printer firmware version
        * _ams_firmware_version : str - Reported AMS firmware version
        * _printer_model : bambutools.PrinterModel - Model # derived from serial #
        * _auto_recovery : bool - auto recovery from lost steps print option
        * _filament_tangle_detect : bool - detect spool tangles print option
        * _sound_enable : bool - printer speaker print option
        * _auto_switch_filament : bool - AMS auto switch filamement on runout print option
        * _startup_read_option : bool - AMS will automatically read RFID on boot
        * _tray_read_option : bool - AMS will automatically read RFID on tray/spool change
        * _calibrate_remain_flag : bool - AMS will calculate remaining amount of filament in spool (unverified)
        """        
        setup_logging()

        self._hostname = hostname
        self._access_code = access_code
        self.serial_number = serial_number
        self._mqtt_port = mqtt_port
        self._mqtt_client_id = mqtt_client_id
        self._mqtt_username = mqtt_username
        self._watchdog_timeout = watchdog_timeout
        self._external_chamber =external_chamber
        self._verbose = verbose

        self._firmware_version = ""
        self._ams_firmware_version = ""
        self._printer_model = PrinterModel.UNKNOWN
        self._auto_recovery = True
        self._filament_tangle_detect = True 
        self._sound_enable = True 
        self._auto_switch_filament = True 
        self._startup_read_option = True 
        self._tray_read_option = True 
        self._calibrate_remain_flag = True

    @property 
    def hostname(self) -> str:
        return self._hostname
    @hostname.setter 
    def hostname(self, value: str):
        self._hostname = str(value)

    @property 
    def access_code(self) -> str:
        return self._access_code
    @access_code.setter 
    def access_code(self, value: str):
        self._access_code = str(value)

    @property 
    def serial_number(self) -> str:
        return self._serial_number
    @serial_number.setter 
    def serial_number(self, value: str):
        self._serial_number = str(value)
        self._printer_model = getModelBySerial(self._serial_number)

    @property 
    def printer_model(self) -> PrinterModel:
        return getModelBySerial(self._serial_number)

    @property 
    def mqtt_port(self) -> int:
        return self._mqtt_port
    @mqtt_port.setter 
    def mqtt_port(self, value: int):
        self._mqtt_port = int(value)

    @property 
    def mqtt_client_id(self) -> str:
        return self._mqtt_client_id
    @mqtt_client_id.setter 
    def mqtt_client_id(self, value: str):
        self._mqtt_client_id = str(value)

    @property 
    def mqtt_username(self) -> str:
        return self._mqtt_username
    @mqtt_username.setter 
    def mqtt_username(self, value: str):
        self._mqtt_username = str(value)

    @property 
    def watchdog_timeout(self) -> int:
        return self._watchdog_timeout
    @watchdog_timeout.setter 
    def watchdog_timeout(self, value: int):
        self._watchdog_timeout = int(value)

    @property 
    def firmware_version(self) -> str:
        return self._firmware_version
    @firmware_version.setter 
    def firmware_version(self, value: str):
        self._firmware_version = str(value)        

    @property 
    def ams_firmware_version(self) -> str:
        return self._ams_firmware_version
    @ams_firmware_version.setter 
    def ams_firmware_version(self, value: str):
        self._ams_firmware_version = str(value)        

    @property 
    def external_chamber(self) -> bool:
        return self._external_chamber
    @external_chamber.setter 
    def external_chamber(self, value: bool):
        self._external_chamber = bool(value)

    @property 
    def auto_recovery(self) -> bool:
        return self._auto_recovery
    @auto_recovery.setter 
    def auto_recovery(self, value: bool):
        self._auto_recovery = bool(value)

    @property 
    def filament_tangle_detect(self) -> bool:
        return self._filament_tangle_detect
    @filament_tangle_detect.setter 
    def filament_tangle_detect(self, value: bool):
        self._filament_tangle_detect = bool(value)

    @property 
    def sound_enable(self) -> bool:
        return self._sound_enable
    @sound_enable.setter 
    def sound_enable(self, value: bool):
        self._sound_enable = bool(value)

    @property 
    def auto_switch_filament(self) -> bool:
        return self._auto_switch_filament
    @auto_switch_filament.setter 
    def auto_switch_filament(self, value: bool):
        self._auto_switch_filament = bool(value)


    @property 
    def startup_read_option(self) -> bool:
        return self._startup_read_option
    @startup_read_option.setter 
    def startup_read_option(self, value: bool):
        self._startup_read_option = bool(value)

    @property 
    def tray_read_option(self) -> bool:
        return self._tray_read_option
    @tray_read_option.setter 
    def tray_read_option(self, value: bool):
        self._tray_read_option = bool(value)

    @property 
    def calibrate_remain_flag(self) -> bool:
        return self._calibrate_remain_flag
    @calibrate_remain_flag.setter 
    def calibrate_remain_flag(self, value: bool):
        self._calibrate_remain_flag = bool(value)


    @property 
    def verbose(self) -> bool:
        return self._verbose
    @verbose.setter 
    def verbose(self, value: bool):
        self._verbose = bool(value)
        stderrHandler = logging.getHandlerByName("stderr")
        fileHandler = logging.getHandlerByName("file")
        if self._verbose:
            stderrHandler.setLevel(logging.DEBUG)
            fileHandler.setLevel(logging.DEBUG)
        else:
            if stderrHandler.level != logging.WARNING:
                stderrHandler.setLevel(logging.WARNING)
                fileHandler.setLevel(logging.WARNING)
        logger.info("log level changed", extra={"new_level": logging.getLevelName(stderrHandler.level)})


def setup_logging():
    config_file = os.path.dirname(os.path.realpath(__file__)) + "/bambuprinterlogger.json"
    with open(config_file) as f_in:
        config = json.load(f_in)

    logging.config.dictConfig(config)
    queue_handler = logging.getHandlerByName("queue_handler")
    if queue_handler is not None:
        queue_handler.listener.start()
        atexit.register(queue_handler.listener.stop)      