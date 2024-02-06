import os
import atexit
import logging.config
import logging.handlers
import json

from typing import Optional

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
        * verbose : Optional[bool] = False
        """        
        setup_logging()

        self.hostname = hostname
        self.access_code = access_code
        self.serial_number = serial_number
        self.mqtt_port = mqtt_port
        self.mqtt_client_id = mqtt_client_id
        self.mqtt_username = mqtt_username
        self.firmware_version = "N/A"
        self.ams_firmware_version = "N/A"
        self.verbose = verbose

    @property 
    def hostname(self):
        return self._hostname
    @hostname.setter 
    def hostname(self, value):
        self._hostname = value

    @property 
    def access_code(self):
        return self._access_code
    @access_code.setter 
    def access_code(self, value):
        self._access_code = value

    @property 
    def serial_number(self):
        return self._serial_number
    @serial_number.setter 
    def serial_number(self, value):
        self._serial_number = value

    @property 
    def mqtt_port(self):
        return self._mqtt_port
    @mqtt_port.setter 
    def mqtt_port(self, value):
        self._mqtt_port = value

    @property 
    def mqtt_client_id(self):
        return self._mqtt_client_id
    @mqtt_client_id.setter 
    def mqtt_client_id(self, value):
        self._mqtt_client_id = value

    @property 
    def mqtt_username(self):
        return self._mqtt_username
    @mqtt_username.setter 
    def mqtt_username(self, value):
        self._mqtt_username = value

    @property 
    def firmware_version(self):
        return self._firmware_version
    @firmware_version.setter 
    def firmware_version(self, value):
        self._firmware_version = value        

    @property 
    def ams_firmware_version(self):
        return self._ams_firmware_version
    @ams_firmware_version.setter 
    def ams_firmware_version(self, value):
        self._ams_firmware_version = value        

    @property 
    def verbose(self):
        return self._verbose
    @verbose.setter 
    def verbose(self, value):
        self._verbose = value  
        stderrHandler = logging.getHandlerByName("stderr")
        fileHandler = logging.getHandlerByName("file")
        if self._verbose:
            stderrHandler.setLevel(logging.DEBUG)
            fileHandler.setLevel(logging.DEBUG)
        else:
            if stderrHandler.level != logging.ERROR:
                stderrHandler.setLevel(logging.ERROR)
                fileHandler.setLevel(logging.ERROR)
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