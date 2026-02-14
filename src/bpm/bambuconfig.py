import logging
from dataclasses import dataclass

from bpm.bambutools import PrinterModel, getPrinterModelBySerial

LoggerName = "bambu_printer_manager"
logger = logging.getLogger(LoggerName)


@dataclass
class PrinterCapabilities:
    """Hardware capabilities discovered during the initial handshake or telemetry analysis."""

    has_ams: bool = False
    """Indicates an active AMS unit is detected on the hardware bus via the `ams` block."""
    has_lidar: bool = False
    """Confirmed presence of the Micro LiDAR sensor based on `xcam` telemetry existence."""
    has_camera: bool = False
    """Verified availability of the onboard AI camera module."""
    has_dual_extruder: bool = False
    """Identifies the H2D dual-path architecture where independent hotend monitoring is required."""
    has_air_filtration: bool = False
    """Indicates the motorized airduct and filtration subsystem is physically installed."""
    has_chamber_temp: bool = False
    """Confirmed presence of the Chamber Thermal Controller (CTC) ambient sensor."""
    has_chamber_door_sensor: bool = False
    """Verification that the front glass enclosure is equipped with a hall-effect sensor."""


class BambuConfig:
    """
    This is the main configuration class for `BambuPrinter` and is how it knows where to connect to a printer,
    what access code, and serial # to use. Further, it contains a number of printer behavioral settings that
    can be changed based on client needs. `BambuConfig` can also be used to change the log level of
    `bambu-printer-manager`'s logging engine.
    """

    def __init__(
        self,
        hostname: str,
        access_code: str,
        serial_number: str,
        mqtt_port: int = 8883,
        mqtt_client_id: str = "studio_client_id:0c1f",
        mqtt_username: str = "bblp",
        watchdog_timeout: int = 30,
        external_chamber: bool = False,
        verbose: bool = False,
        capabilities: PrinterCapabilities | None = None,
    ):
        """
        Initializes the configuration profile for the Bambu Lab printer client.

        Parameters
        ----------
        * hostname : IP address or DNS name of the printer on the local subnet.
        * access_code : 8-character LAN-only access code for MQTT authentication.
        * serial_number : Unique hardware identifier used to derive the printer model.
        * mqtt_port : Network port for the SSL-encrypted MQTT broker (Default: 8883).
        * mqtt_client_id : Unique identifier used during the MQTT handshake protocol.
        * mqtt_username : Authentication username for the local MQTT broker (Default: 'bblp').
        * watchdog_timeout : Duration in seconds before a connection is flagged as stale.
        * external_chamber : If True, ignores internal CTC telemetry to allow manual sensor injection.
        * verbose : Controls log verbosity; True sets level to DEBUG, False to WARNING.
        * capabilities : Pre-defined or discovered hardware feature set.

        Attributes
        ----------
        * firmware_version : Semantic version string of the main printer firmware.
        * ams_firmware_version : Semantic version string of the primary AMS controller.
        * printer_model : Enum classification (e.g. A1, H2D) derived from the serial prefix.
        * auto_recovery : Firmware-level toggle for resuming prints after step-loss.
        * filament_tangle_detect : Master switch for AMS tension-based monitor logic.
        * sound_enable : Controls the machine's internal speaker for user notifications.
        * auto_switch_filament : Enables automatic AMS failover to redundant spools.
        * buildplate_marker_detector : Toggles ArUco scanning for build surface verification.
        * capabilities : Data structure containing all verified hardware features.
        """

        self._hostname = hostname
        self._access_code = access_code
        self.serial_number = serial_number if serial_number else ""
        self._mqtt_port = mqtt_port
        self._mqtt_client_id = mqtt_client_id
        self._mqtt_username = mqtt_username
        self._watchdog_timeout = watchdog_timeout
        self._external_chamber = external_chamber
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
        self._buildplate_marker_detector = True

        if capabilities is None:
            capabilities = PrinterCapabilities()
        self._capabilities = capabilities

    @property
    def hostname(self) -> str:
        """The network address (IP or FQDN) used to establish the MQTT connection with the printer."""
        return self._hostname

    @hostname.setter
    def hostname(self, value: str):
        self._hostname = str(value)

    @property
    def access_code(self) -> str:
        """The 8-character security credential required for LAN-mode authentication and MQTT encryption."""
        return self._access_code

    @access_code.setter
    def access_code(self, value: str):
        self._access_code = str(value)

    @property
    def serial_number(self) -> str:
        """Unique hardware identifier. Setting this value automatically triggers a re-evaluation of the printer model classification."""
        return self._serial_number

    @serial_number.setter
    def serial_number(self, value: str):
        self._serial_number = str(value)
        self._printer_model = getPrinterModelBySerial(self._serial_number)

    @property
    def printer_model(self) -> PrinterModel:
        """Read-only classification of the printer hardware (e.g. A1, H2D) derived from the serial number prefix."""
        return getPrinterModelBySerial(self._serial_number)

    @property
    def mqtt_port(self) -> int:
        """The TCP port utilized for the SSL-encrypted MQTT broker communication (typically 8883)."""
        return self._mqtt_port

    @mqtt_port.setter
    def mqtt_port(self, value: int):
        self._mqtt_port = int(value)

    @property
    def mqtt_client_id(self) -> str:
        """Unique identifier for the MQTT session, used to manage state persistence and message routing."""
        return self._mqtt_client_id

    @mqtt_client_id.setter
    def mqtt_client_id(self, value: str):
        self._mqtt_client_id = str(value)

    @property
    def mqtt_username(self) -> str:
        """The authentication username required by the printer-hosted MQTT broker (Default: 'bblp')."""
        return self._mqtt_username

    @mqtt_username.setter
    def mqtt_username(self, value: str):
        self._mqtt_username = str(value)

    @property
    def watchdog_timeout(self) -> int:
        """The interval in seconds before the communication channel is flagged as inactive and a reconnection is attempted."""
        return self._watchdog_timeout

    @watchdog_timeout.setter
    def watchdog_timeout(self, value: int):
        self._watchdog_timeout = int(value)

    @property
    def firmware_version(self) -> str:
        """The semantic version string of the main Application Processor (AP) firmware executing on the printer."""
        return self._firmware_version

    @firmware_version.setter
    def firmware_version(self, value: str):
        self._firmware_version = str(value)

    @property
    def ams_firmware_version(self) -> str:
        """The semantic version string of the primary AMS controller firmware discovered on the hardware bus."""
        return self._ams_firmware_version

    @ams_firmware_version.setter
    def ams_firmware_version(self, value: str):
        self._ams_firmware_version = str(value)

    @property
    def external_chamber(self) -> bool:
        """When enabled, tells the client to ignore internal CTC telemetry in favor of manually injected external thermal data."""
        return self._external_chamber

    @external_chamber.setter
    def external_chamber(self, value: bool):
        self._external_chamber = bool(value)

    @property
    def auto_recovery(self) -> bool:
        """Firmware-level toggle for the automatic resumption of print jobs after a detected X/Y axis step-loss event."""
        return self._auto_recovery

    @auto_recovery.setter
    def auto_recovery(self, value: bool):
        self._auto_recovery = bool(value)

    @property
    def filament_tangle_detect(self) -> bool:
        """Master switch for the AMS tension-monitoring logic used to detect mechanical resistance in the filament path."""
        return self._filament_tangle_detect

    @filament_tangle_detect.setter
    def filament_tangle_detect(self, value: bool):
        self._filament_tangle_detect = bool(value)

    @property
    def sound_enable(self) -> bool:
        """Configuration for the machine's internal hardware speaker for audible notifications and AI alerts."""
        return self._sound_enable

    @sound_enable.setter
    def sound_enable(self, value: bool):
        self._sound_enable = bool(value)

    @property
    def auto_switch_filament(self) -> bool:
        """Enables automatic failover to a compatible filament spool in the AMS when the current source runs out."""
        return self._auto_switch_filament

    @auto_switch_filament.setter
    def auto_switch_filament(self, value: bool):
        self._auto_switch_filament = bool(value)

    @property
    def startup_read_option(self) -> bool:
        """Configures whether the AMS unit performs a full RFID scan of all slots upon printer power-on."""
        return self._startup_read_option

    @startup_read_option.setter
    def startup_read_option(self, value: bool):
        self._startup_read_option = bool(value)

    @property
    def tray_read_option(self) -> bool:
        """Toggles the automatic RFID identification sequence when a new filament spool is inserted or detected."""
        return self._tray_read_option

    @tray_read_option.setter
    def tray_read_option(self, value: bool):
        self._tray_read_option = bool(value)

    @property
    def calibrate_remain_flag(self) -> bool:
        """Enablement for the spool-weight based estimation of the remaining filament length in the AMS."""
        return self._calibrate_remain_flag

    @calibrate_remain_flag.setter
    def calibrate_remain_flag(self, value: bool):
        self._calibrate_remain_flag = bool(value)

    @property
    def buildplate_marker_detector(self) -> bool:
        """Toggles the AI vision ArUco marker scanning system used to verify build surface compatibility."""
        return self._buildplate_marker_detector

    @buildplate_marker_detector.setter
    def buildplate_marker_detector(self, value: bool):
        self._buildplate_marker_detector = bool(value)

    @property
    def capabilities(self) -> PrinterCapabilities:
        """Data structure containing the verified set of hardware features discovered during system analysis."""
        return self._capabilities

    @capabilities.setter
    def capabilities(self, value: PrinterCapabilities):
        self._capabilities = value

    @property
    def verbose(self) -> bool:
        """Controls the global log verbosity for the library. Setting this value shifts the logger level between DEBUG and WARNING."""
        return self._verbose

    @verbose.setter
    def verbose(self, value: bool):
        self._verbose = bool(value)
        if self._verbose:
            logger.setLevel(logging.DEBUG)
            logging.basicConfig(level=logging.DEBUG)
        else:
            if logger.level != logging.WARNING:
                logger.setLevel(logging.WARNING)
                logging.basicConfig(level=logging.WARNING)
        logger.info(
            f"log level changed - new_level: {logging.getLevelName(logger.level)}"
        )
