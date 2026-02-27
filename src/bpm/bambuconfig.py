"""
`bambuconfig` contains the `BambuConfig` class used for managing configuration data
"""

import logging
from dataclasses import dataclass, field
from pathlib import Path

from bpm.bambutools import LoggerName, PrinterModel, getPrinterModelBySerial

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
    has_sound_enable_support: bool = False
    """Indicates whether prompt sound control is supported by firmware telemetry flags."""
    has_auto_recovery_support: bool = False
    """Indicates whether auto-recovery control is supported by explicit support telemetry keys."""
    has_auto_switch_filament_support: bool = False
    """Indicates whether AMS auto-switch control is supported by explicit support telemetry keys."""
    has_filament_tangle_detect_support: bool = False
    """Indicates whether filament tangle detection control is supported by firmware telemetry flags."""
    has_nozzle_blob_detect_support: bool = False
    """Indicates whether nozzle blob detection control is supported by firmware telemetry flags."""
    has_air_print_detect_support: bool = False
    """Indicates whether air-print detection control is supported by firmware telemetry flags."""
    has_buildplate_marker_detector_support: bool = False
    """Indicates whether buildplate marker detector control is supported by xcam telemetry."""
    has_spaghetti_detector_support: bool = False
    """Indicates whether spaghetti detector control is supported by xcam telemetry."""
    has_purgechutepileup_detector_support: bool = False
    """Indicates whether purge-chute pileup detector control is supported by xcam telemetry."""
    has_nozzleclumping_detector_support: bool = False
    """Indicates whether nozzle-clumping detector control is supported by xcam telemetry."""
    has_airprinting_detector_support: bool = False
    """Indicates whether air-printing detector control is supported by xcam telemetry."""


@dataclass
class BambuConfig:
    """
    This is the main configuration class for `BambuPrinter` and is how it knows where to connect to a printer,
    what access code, and serial # to use. Further, it contains a number of printer behavioral settings and
    capabability values.
    """

    # Required Parameters
    hostname: str
    """IP address or DNS name of the printer on the local subnet."""
    access_code: str
    """8-character LAN-only access code for MQTT authentication."""
    serial_number: str
    """Unique hardware identifier used to derive the printer model."""

    # Optional Parameters
    mqtt_port: int = 8883
    """Network port for the SSL-encrypted MQTT broker (Default: 8883)."""
    mqtt_client_id: str = "studio_client_id:0c1f"
    """Unique identifier used during the MQTT handshake protocol."""
    mqtt_username: str = "bblp"
    """Authentication username for the local MQTT broker (Default: 'bblp')."""
    watchdog_timeout: int = 30
    """Duration in seconds before a connection is flagged as stale."""
    external_chamber: bool = False
    """If True, ignores internal CTC telemetry to allow manual sensor injection."""
    capabilities: PrinterCapabilities = field(default_factory=PrinterCapabilities)
    """Pre-defined or discovered hardware feature set."""
    bpm_cache_path: Path | None = None
    """The underlying directory BPM uses for managing cache / metadata."""
    printer_model: PrinterModel = PrinterModel.UNKNOWN
    """Read-only classification of the printer hardware (e.g. A1, H2D) derived from the serial number prefix."""
    firmware_version: str = ""
    """Semantic version string of the main printer firmware."""
    ams_firmware_version: str = ""
    """Semantic version string of the primary AMS controller."""
    auto_recovery: bool = False
    """Firmware-level toggle for resuming prints after step-loss."""
    filament_tangle_detect: bool = False
    """Master switch for AMS tension-based monitor logic."""
    sound_enable: bool = False
    """Controls the machine's internal speaker for user notifications."""
    auto_switch_filament: bool = False
    """Enables automatic AMS failover to redundant spools."""
    startup_read_option: bool = False
    """Configures whether the AMS unit performs a full RFID scan of all slots upon printer power-on."""
    tray_read_option: bool = False
    """Toggles the automatic RFID identification sequence when a new filament spool is inserted or detected."""
    calibrate_remain_flag: bool = False
    """Enablement for the spool-weight based estimation of the remaining filament length in the AMS."""
    buildplate_marker_detector: bool = False
    """Toggles the AI vision ArUco marker scanning system used to verify build surface compatibility."""
    spaghetti_detector: bool = False
    """Toggles AI spaghetti detection for failed-print strand detection."""
    spaghetti_detector_sensitivity: str = "medium"
    """Sensitivity level for spaghetti detection pause behavior (low|medium|high)."""
    purgechutepileup_detector: bool = False
    """Toggles AI purge-chute pileup detection."""
    purgechutepileup_detector_sensitivity: str = "medium"
    """Sensitivity level for purge-chute pileup pause behavior (low|medium|high)."""
    nozzleclumping_detector: bool = False
    """Toggles AI nozzle clumping detection."""
    nozzleclumping_detector_sensitivity: str = "medium"
    """Sensitivity level for nozzle clumping pause behavior (low|medium|high)."""
    airprinting_detector: bool = False
    """Toggles AI air-printing detection."""
    airprinting_detector_sensitivity: str = "medium"
    """Sensitivity level for air-printing pause behavior (low|medium|high)."""
    nozzle_blob_detect: bool = False
    """Toggles the AI vision system used to detect nozzle blobs / clumps."""
    air_print_detect: bool = False
    """Toggles air-print detection to detect clogging or filament grinding conditions."""
    verbose: bool = False
    """Provides an additional log level for dumping all messages"""

    def __post_init__(self):
        """
        Post-initialization logic to handle defaults.
        """
        self.printer_model = getPrinterModelBySerial(self.serial_number)

        # Default bpm_cache_path and creation
        if self.bpm_cache_path is None:
            self.bpm_cache_path = Path("~/.bpm").expanduser()
        self.set_new_bpm_cache_path(self.bpm_cache_path)

    def set_new_bpm_cache_path(self, path: Path):
        """Enables changing the bpm cache directory at runtime.  Will orphan previous contents."""
        self.bpm_cache_path = path
        metadata = self.bpm_cache_path / "metadata"
        metadata.mkdir(parents=True, exist_ok=True)
