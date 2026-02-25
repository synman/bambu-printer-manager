# Bambu Printer Manager - Data Dictionary

## Overview

This comprehensive data dictionary documents all attributes manifested in the bambu-printer-manager library. Each attribute includes its ancestry (parent class), telemetry source (MQTT JSON path), type information, valid ranges, and purpose.

### Related Documentation

- **[MQTT Protocol Reference](mqtt-protocol-reference.md)** — Details how to control printer attributes via MQTT commands with field breakdowns, example JSON payloads, and usage patterns
- **[API Reference](api-reference.md)** — REST API endpoints and client container implementation
- **[Container Setup](container.md)** — Docker deployment guide with authentication configuration

## Reference Implementations

Attributes are validated against these authoritative public repositories:

- **[BambuStudio](https://github.com/bambulab/BambuStudio)** - Official Bambu Lab client implementation with complete telemetry mapping and protocol definitions
- **[OrcaSlicer](https://github.com/OrcaSlicer/OrcaSlicer)** - Community fork with enhanced telemetry handling and data structure examples
- **[ha-bambulab](https://github.com/greghesp/ha-bambulab)** - Home Assistant integration with comprehensive MQTT topic and payload documentation
- **[ha-bambulab pybambu](https://github.com/greghesp/ha-bambulab/tree/main/custom_components/bambu_lab/pybambu)** - Low-level Python MQTT client implementation and message parsing
- **[Bambu-HomeAssistant-Flows](https://github.com/WolfwithSword/Bambu-HomeAssistant-Flows)** - Workflow patterns and integration examples using Bambu Lab printers
- **[OpenBambuAPI](https://github.com/Doridian/OpenBambuAPI)** - Alternative API implementation with detailed protocol documentation
- **[X1Plus](https://github.com/X1Plus/X1Plus)** - Community firmware and protocol analysis for extended printer capabilities
- **[bambu-node](https://github.com/THE-SIMPLE-MARK/bambu-node)** - Node.js implementation providing cross-language verification and alternative patterns

## Dataclass Hierarchy

```
BambuConfig (configuration root)
├── hostname, access_code, serial_number
├── mqtt_port, client_id, username
├── watchdog_timeout, external_chamber
├── bpm_cache_path, printer_model
├── firmware_version, ams_firmware_version
└── capabilities: PrinterCapabilities
    ├── has_ams, has_lidar, has_camera
    ├── has_dual_extruder, has_air_filtration
    └── has_chamber_temp, has_chamber_door_sensor

BambuState (telemetry root)
├── gcode_state, active_tool, etc.
├── ams_units: list[AMSUnitState]
│   ├── ams_id, model, temps, humidity
│   └── heater_state, dry_fan1/2_status, dry_sub_status
├── extruders: list[ExtruderState]
│   ├── id, temps, state, status
│   └── active_tray_id, target_tray_id, tray_state
├── spools: list[BambuSpool]
│   └── Filament properties, color, temps, remaining
└── climate: BambuClimate
    ├── bed_temp, chamber_temp, nozzle_temp
    ├── fans: part_cooling, aux, exhaust, heatbreak
    └── doors: chamber_door, lid, top_vent

ActiveJobInfo (project root)
├── project_info: ProjectInfo
│   ├── id, name, size, timestamp, md5
│   └── plate_num, metadata
├── project_file_command
├── stage_id, stage_name
├── current_layer, total_layers
├── print_percentage
├── elapsed_minutes, remaining_minutes
├── monotonic_start_time
└── subtask_name, gcode_file, print_type, plate_num, plate_type
```

---

## Alphabetical Field Index

Quick alphabetical reference to all documented fields. Fields marked with * appear in multiple classes.

| Field | Class | Field | Class |
|-------|-------|-------|-------|
| **A** | | **I** (cont.) | |
| [access_code](#access_code) | BambuConfig | [info_bits](#info_bits) | ExtruderState |
| [active_ams_id](#active_ams_id) | BambuState | [is_chamber_door_open](#is_chamber_door_open) | BambuClimate |
| [active_nozzle_temp](#active_nozzle_temp) | BambuState | [is_chamber_lid_open](#is_chamber_lid_open) | BambuClimate |
| [active_nozzle_temp_target](#active_nozzle_temp_target) | BambuState | [is_external_spool_active](#is_external_spool_active) | BambuState |
| [active_tool](#active_tool) | BambuState | **K** | |
| [active_tray_id](#active_tray_id)* | BambuState, ExtruderState | [k](#k) | BambuSpool |
| [active_tray_state](#active_tray_state) | BambuState | **M** | |
| [active_tray_state_name](#active_tray_state_name) | BambuState | [md5](#md5) | ProjectInfo |
| [air_conditioning_mode](#air_conditioning_mode) | BambuClimate | [metadata](#metadata) | ProjectInfo |
| [airduct_mode](#airduct_mode) | BambuClimate | [model](#model) | AMSUnitState |
| [airduct_sub_mode](#airduct_sub_mode) | BambuClimate | [monotonic_start_time](#monotonic_start_time) | ActiveJobInfo |
| [ams_connected_count](#ams_connected_count) | BambuState | [mqtt_client_id](#mqtt_client_id) | BambuConfig |
| [ams_exist_bits](#ams_exist_bits) | BambuState | [mqtt_port](#mqtt_port) | BambuConfig |
| [ams_firmware_version](#ams_firmware_version) | BambuConfig | [mqtt_username](#mqtt_username) | BambuConfig |
| [ams_id](#ams_id)* | AMSUnitState, BambuSpool | **N** | |
| [ams_info](#ams_info) | AMSUnitState | [name](#name)* | BambuSpool, ProjectInfo |
| [ams_status_raw](#ams_status_raw) | BambuState | [nozzle_temp_max](#nozzle_temp_max) | BambuSpool |
| [ams_status_text](#ams_status_text) | BambuState | [nozzle_temp_min](#nozzle_temp_min) | BambuSpool |
| [ams_units](#ams_units) | BambuState | **P** | |
| [assigned_to_ams_id](#assigned_to_ams_id) | ExtruderState | [part_cooling_fan_speed_percent](#part_cooling_fan_speed_percent) | BambuClimate |
| [assigned_to_extruder](#assigned_to_extruder) | AMSUnitState | [part_cooling_fan_speed_target_percent](#part_cooling_fan_speed_target_percent) | BambuClimate |
| [auto_recovery](#auto_recovery) | BambuConfig | [plate_num](#plate_num)* | ProjectInfo, ActiveJobInfo |
| [auto_switch_filament](#auto_switch_filament) | BambuConfig | [plate_type](#plate_type) | ActiveJobInfo |
| [aux_fan_speed_percent](#aux_fan_speed_percent) | BambuClimate | [print_error](#print_error) | BambuState |
| **B** | | [print_percentage](#print_percentage) | ActiveJobInfo |
| [bed_temp](#bed_temp)* | BambuClimate, BambuSpool | [print_type](#print_type) | ActiveJobInfo |
| [bed_temp_target](#bed_temp_target) | BambuClimate | [printer_model](#printer_model) | BambuConfig |
| [bpm_cache_path](#bpm_cache_path) | BambuConfig | [project_file_command](#project_file_command) | ActiveJobInfo |
| [buildplate_marker_detector](#buildplate_marker_detector) | BambuConfig | [project_info](#project_info) | ActiveJobInfo |
| **C** | | **R** | |
| [calibrate_remain_flag](#calibrate_remain_flag) | BambuConfig | [remaining_minutes](#remaining_minutes) | ActiveJobInfo |
| [capabilities](#capabilities) | BambuConfig | [remaining_percent](#remaining_percent) | BambuSpool |
| [chamber_temp](#chamber_temp) | BambuClimate | **S** | |
| [chamber_temp_target](#chamber_temp_target) | BambuClimate | [serial_number](#serial_number) | BambuConfig |
| [chip_id](#chip_id) | AMSUnitState | [size](#size) | ProjectInfo |
| [climate](#climate) | BambuState | [slot_id](#slot_id) | BambuSpool |
| [color](#color) | BambuSpool | [sound_enable](#sound_enable) | BambuConfig |
| [current_layer](#current_layer) | ActiveJobInfo | [spools](#spools) | BambuState |
| **D** | | [stage_id](#stage_id) | ActiveJobInfo |
| [dry_fan1_status](#dry_fan1_status) | AMSUnitState | [stage_name](#stage_name) | ActiveJobInfo |
| [dry_fan2_status](#dry_fan2_status) | AMSUnitState | [startup_read_option](#startup_read_option) | BambuConfig |
| [dry_sub_status](#dry_sub_status) | AMSUnitState | [stat](#stat) | BambuState |
| [dry_time](#dry_time) | AMSUnitState | [state](#state)* | ExtruderState, BambuSpool |
| [drying_temp](#drying_temp) | BambuSpool | [status](#status) | ExtruderState |
| [drying_time](#drying_time) | BambuSpool | [sub_brands](#sub_brands) | BambuSpool |
| **E** | | [subtask_name](#subtask_name) | ActiveJobInfo |
| [elapsed_minutes](#elapsed_minutes) | ActiveJobInfo | **T** | |
| [exhaust_fan_speed_percent](#exhaust_fan_speed_percent) | BambuClimate | [target_tray_id](#target_tray_id)* | BambuState, ExtruderState |
| [external_chamber](#external_chamber) | BambuConfig | [temp](#temp) | ExtruderState |
| [extruders](#extruders) | BambuState | [temp_actual](#temp_actual) | AMSUnitState |
| **F** | | [temp_target](#temp_target)* | ExtruderState, AMSUnitState |
| [filament_tangle_detect](#filament_tangle_detect) | BambuConfig | [timestamp](#timestamp) | ProjectInfo |
| [firmware_version](#firmware_version) | BambuConfig | [total_layers](#total_layers) | ActiveJobInfo |
| [fun](#fun) | BambuState | [total_length](#total_length) | BambuSpool |
| **G** | | [tray_exists](#tray_exists) | AMSUnitState |
| [gcode_file](#gcode_file) | ActiveJobInfo | [tray_info_idx](#tray_info_idx) | BambuSpool |
| [gcode_state](#gcode_state) | BambuState | [tray_read_option](#tray_read_option) | BambuConfig |
| **H** | | [tray_state](#tray_state) | ExtruderState |
| [has_air_filtration](#has_air_filtration) | PrinterCapabilities | [tray_weight](#tray_weight) | BambuSpool |
| [has_ams](#has_ams) | PrinterCapabilities | [type](#type) | BambuSpool |
| [has_camera](#has_camera) | PrinterCapabilities | **V** | |
| [has_chamber_door_sensor](#has_chamber_door_sensor) | PrinterCapabilities | [verbose](#verbose) | BambuConfig |
| [has_chamber_temp](#has_chamber_temp) | PrinterCapabilities | **W** | |
| [has_dual_extruder](#has_dual_extruder) | PrinterCapabilities | [watchdog_timeout](#watchdog_timeout) | BambuConfig |
| [has_lidar](#has_lidar) | PrinterCapabilities | [wifi_signal_strength](#wifi_signal_strength) | BambuState |
| [heatbreak_fan_speed_percent](#heatbreak_fan_speed_percent) | BambuClimate | **Z** | |
| [heater_state](#heater_state) | AMSUnitState | [zone_aux_percent](#zone_aux_percent) | BambuClimate |
| [hms_errors](#hms_errors) | BambuState | [zone_exhaust_percent](#zone_exhaust_percent) | BambuClimate |
| [hostname](#hostname) | BambuConfig | [zone_intake_open](#zone_intake_open) | BambuClimate |
| [humidity_index](#humidity_index) | AMSUnitState | [zone_part_fan_percent](#zone_part_fan_percent) | BambuClimate |
| [humidity_raw](#humidity_raw) | AMSUnitState | [zone_top_vent_open](#zone_top_vent_open) | BambuClimate |
| **I** | | | |
| [id](#id)* | ExtruderState, AMSUnitState, BambuSpool, ProjectInfo | | |

---

## BambuConfig

Main configuration class for `BambuPrinter` containing connection parameters, behavioral settings, and hardware capabilities.

**Source**: `src/bpm/bambuconfig.py`

### Required Parameters

#### hostname
- **Type**: `str`
- **Purpose**: IP address or DNS name of the printer on the local subnet
- **Example**: `"192.168.1.100"` or `"bambu-h2d-printer"`
- **Reference**: MQTT broker connection endpoint

#### access_code
- **Type**: `str`
- **Purpose**: 8-character LAN-only access code for MQTT authentication
- **Valid Format**: 8 alphanumeric characters
- **Security**: Never log or transmit outside local network
- **Reference**: Found in printer LCD Settings → LAN Access

#### serial_number
- **Type**: `str`
- **Purpose**: Unique hardware identifier used to derive the printer model
- **Format**: Varies by model (e.g., H2D starts with specific prefix)
- **Usage**: Automatically determines `printer_model` in `__post_init__`
- **Reference**: BambuStudio device identification

### Network Configuration

#### mqtt_port
- **Type**: `int`
- **Default**: `8883`
- **Purpose**: Network port for the SSL-encrypted MQTT broker
- **Reference**: Standard Bambu Lab MQTT TLS port

#### mqtt_client_id
- **Type**: `str`
- **Default**: `"studio_client_id:0c1f"`
- **Purpose**: Unique identifier used during the MQTT handshake protocol
- **Reference**: BambuStudio client identification pattern

#### mqtt_username
- **Type**: `str`
- **Default**: `"bblp"`
- **Purpose**: Authentication username for the local MQTT broker
- **Reference**: Bambu Lab Printer username constant

### Operational Settings

#### watchdog_timeout
- **Type**: `int`
- **Default**: `30`
- **Unit**: seconds
- **Purpose**: Duration before a connection is flagged as stale
- **Reference**: Connection health monitoring

#### external_chamber
- **Type**: `bool`
- **Default**: `False`
- **Purpose**: If True, ignores internal CTC telemetry to allow manual sensor injection
- **Use Case**: Custom chamber temperature monitoring with external sensors
- **Reference**: CTC (Chamber Thermal Controller) override

#### capabilities
- **Type**: `PrinterCapabilities | None`
- **Default**: `None` (auto-creates default instance in `__post_init__`)
- **Purpose**: Pre-defined or discovered hardware feature set
- **Reference**: See [PrinterCapabilities](#printercapabilities) section

#### bpm_cache_path
- **Type**: `Path | None`
- **Default**: `None` (defaults to `~/.bpm` in `__post_init__`)
- **Purpose**: The underlying directory BPM uses for managing cache/metadata
- **Auto-Creation**: Creates `metadata/` subdirectory on initialization
- **Reference**: Project metadata and 3MF caching location

### Read-Only Attributes

#### printer_model
- **Type**: `PrinterModel` (IntEnum)
- **Default**: `PrinterModel.UNKNOWN`
- **Purpose**: Classification of the printer hardware (e.g., A1, H2D) derived from the serial number prefix
- **Initialization**: Set in `__post_init__` via `getPrinterModelBySerial()`
- **Reference**: BambuStudio printer type detection

#### firmware_version
- **Type**: `str`
- **Default**: `""`
- **Purpose**: Semantic version string of the main printer firmware
- **Example**: `"01.09.00.00"`
- **Reference**: Retrieved from telemetry during connection

#### ams_firmware_version
- **Type**: `str`
- **Default**: `""`
- **Purpose**: Semantic version string of the primary AMS controller
- **Example**: `"00.00.06.60"`
- **Reference**: Retrieved from AMS telemetry

### Feature Flags

#### auto_recovery
- **Type**: `bool`
- **Default**: `False`
- **Purpose**: Firmware-level toggle for resuming prints after step-loss
- **MQTT Control**: [Set Print Options](mqtt-protocol-reference.md#set-print-options)
- **Reference**: BambuStudio recovery settings

#### filament_tangle_detect
- **Type**: `bool`
- **Default**: `False`
- **Purpose**: Master switch for AMS tension-based monitor logic
- **MQTT Control**: [Set Print Options](mqtt-protocol-reference.md#set-print-options)
- **Reference**: AMS filament runout/tangle detection

#### sound_enable
- **Type**: `bool`
- **Default**: `False`
- **Purpose**: Controls the machine's internal speaker for user notifications
- **MQTT Control**: [Set Print Options](mqtt-protocol-reference.md#set-print-options)
- **Reference**: Printer audio feedback system

#### auto_switch_filament
- **Type**: `bool`
- **Default**: `False`
- **Purpose**: Enables automatic AMS failover to redundant spools
- **MQTT Control**: [Set Print Options](mqtt-protocol-reference.md#set-print-options)
- **Reference**: AMS automatic spool switching

#### startup_read_option
- **Type**: `bool`
- **Default**: `False`
- **Purpose**: Configures whether the AMS unit performs a full RFID scan of all slots upon printer power-on
- **MQTT Control**: [AMS User Settings](mqtt-protocol-reference.md#ams-user-settings)
- **Reference**: AMS initialization behavior

#### tray_read_option
- **Type**: `bool`
- **Default**: `False`
- **Purpose**: Toggles the automatic RFID identification sequence when a new filament spool is inserted or detected
- **MQTT Control**: [AMS User Settings](mqtt-protocol-reference.md#ams-user-settings)
- **Reference**: AMS hot-swap RFID reading

#### calibrate_remain_flag
- **Type**: `bool`
- **Default**: `False`
- **Purpose**: Enablement for the spool-weight based estimation of the remaining filament length in the AMS
- **MQTT Control**: [AMS User Settings](mqtt-protocol-reference.md#ams-user-settings)
- **Reference**: AMS filament remaining calculation

#### buildplate_marker_detector
- **Type**: `bool`
- **Default**: `False`
- **Purpose**: Toggles the AI vision ArUco marker scanning system used to verify build surface compatibility
- **MQTT Control**: [Buildplate Marker Detection](mqtt-protocol-reference.md#buildplate-marker-detection)
- **Reference**: Camera-based plate detection feature

#### verbose
- **Type**: `bool`
- **Default**: `False`
- **Purpose**: Provides an additional log level for dumping all messages
- **MQTT Control**: None (local configuration only)
- **Reference**: Debug logging control

---

## PrinterCapabilities

Hardware capabilities discovered during the initial handshake or telemetry analysis.

**Source**: `src/bpm/bambuconfig.py`

### Hardware Detection Attributes

#### has_ams
- **Type**: `bool`
- **Default**: `False`
- **Purpose**: Indicates an active AMS unit is detected on the hardware bus via the `ams` block
- **Detection**: Presence of `ams` telemetry data
- **Reference**: AMS (Automatic Material System) availability

#### has_lidar
- **Type**: `bool`
- **Default**: `False`
- **Purpose**: Confirmed presence of the Micro LiDAR sensor based on `xcam` telemetry existence
- **Detection**: `xcam` status in telemetry
- **Reference**: First-layer inspection and spaghetti detection feature

#### has_camera
- **Type**: `bool`
- **Default**: `False`
- **Purpose**: Verified availability of the onboard AI camera module
- **Detection**: Camera telemetry streams or status
- **Reference**: Time-lapse and monitoring capabilities

#### has_dual_extruder
- **Type**: `bool`
- **Default**: `False`
- **Purpose**: Identifies the H2D dual-path architecture where independent hotend monitoring is required
- **Detection**: Printer model is H2D or dual extruder telemetry present
- **Reference**: Multi-material printing support

#### has_air_filtration
- **Type**: `bool`
- **Default**: `False`
- **Purpose**: Indicates the motorized airduct and filtration subsystem is physically installed
- **Detection**: Exhaust fan control availability
- **Reference**: Active carbon filter and VOC management

#### has_chamber_temp
- **Type**: `bool`
- **Default**: `False`
- **Purpose**: Confirmed presence of the Chamber Thermal Controller (CTC) ambient sensor
- **Detection**: `chamber_temper` telemetry field existence
- **Reference**: Enclosed chamber temperature monitoring
- **Override**: Can be ignored if `BambuConfig.external_chamber` is True

#### has_chamber_door_sensor
- **Type**: `bool`
- **Default**: `False`
- **Purpose**: Verification that the front glass enclosure is equipped with a hall-effect sensor
- **Detection**: Chamber door status in telemetry
- **Reference**: Safety interlock and environmental control

---

## BambuState

Root state object representing complete printer telemetry.

**Source**: `src/bpm/bambustate.py`
**Telemetry Root**: `data.get("print", {})`

### Core State Attributes

#### gcode_state
- **Type**: `str`
- **Telemetry**: `print.gcode_state`
- **Valid Values**: `IDLE`, `PREPARE`, `RUNNING`, `PAUSE`, `FINISH`, `FAILED`, `UNKNOWN`
- **Purpose**: Current G-code execution state
- **Reference**: BambuStudio `GCodeState` enum

#### active_tool
- **Type**: `ActiveTool` (IntEnum)
- **Telemetry**: `print.device.extruder.state` (bits 4-7)
- **Valid Values**:
  - `SINGLE_EXTRUDER (-1)`: X1/P1/A1 single toolhead
  - `RIGHT_EXTRUDER (0)`: H2D primary toolhead
  - `LEFT_EXTRUDER (1)`: H2D secondary toolhead
  - `NOT_ACTIVE (15)`: Transitional state
- **Purpose**: Currently active extruder in dual-extruder systems
- **Reference**: BambuStudio `ActiveTool` mapping
- **MQTT Control**: [Select Active Extruder](mqtt-protocol-reference.md#select-active-extruder-dual-extruder)

#### active_ams_id
- **Type**: `int`
- **Telemetry**: Computed from `active_tray_id >> 2`
- **Valid Range**: `-1` (no AMS), `0-3` (standard AMS), `128-131` (AMS HT)
- **Purpose**: Currently active AMS unit ID
- **Reference**: AMS slot addressing scheme

#### active_tray_id
- **Type**: `int`
- **Telemetry**: `print.ams.tray_now` or computed from extruder
- **Valid Range**:
  - `0-15`: Standard AMS slots (4 trays × 4 units)
  - `254-255`: External spool
  - `-1`: No tray
- **Purpose**: Current filament tray identifier
- **Reference**: BambuStudio tray indexing

#### active_tray_state
- **Type**: `TrayState` (IntEnum)
- **Telemetry**: Computed from extruder info/status
- **Valid Values**:
  - `UNLOADED (0)`
  - `LOADED (1)`
  - `LOADING (2)`
  - `UNLOADING (3)`
- **Purpose**: Filament loading operational state
- **Reference**: BambuStudio `TrayState`

#### active_tray_state_name
- **Type**: `str`
- **Telemetry**: Derived from `active_tray_state.name`
- **Purpose**: Human-readable tray state
- **Reference**: N/A (convenience attribute)

#### target_tray_id
- **Type**: `int`
- **Telemetry**: Computed from extruder target tray
- **Valid Range**: Same as `active_tray_id`
- **Purpose**: Next tray to be loaded
- **Reference**: BambuStudio tray targeting

#### is_external_spool_active
- **Type**: `bool`
- **Telemetry**: Computed from `active_tray_id in [254, 255]`
- **Purpose**: Indicates external spool usage
- **Reference**: N/A (derived)

#### active_nozzle_temp
- **Type**: `float`
- **Telemetry**: `print.nozzle_temper` or active extruder temp
- **Unit**: °C
- **Purpose**: Current nozzle temperature
- **Reference**: BambuStudio thermal monitoring

#### active_nozzle_temp_target
- **Type**: `int`
- **Telemetry**: `print.nozzle_target_temper` or extruder target
- **Unit**: °C
- **Purpose**: Target nozzle temperature
- **Reference**: BambuStudio thermal control
- **MQTT Control**: [Set Nozzle Temperature Target](mqtt-protocol-reference.md#set-nozzle-temperature-target)

### AMS Status Attributes

#### ams_status_raw
- **Type**: `int`
- **Telemetry**: `print.ams_status`
- **Purpose**: Raw AMS status bitmask
- **Reference**: BambuStudio AMS status codes

#### ams_status_text
- **Type**: `str`
- **Telemetry**: Parsed from `ams_status_raw`
- **Valid Values**: `Idle`, `Filament Changing`, `RFID Identifying`, `Assist/Engaged`, `Calibration`, `Self Check`, `Debug`, `Unknown`
- **Purpose**: Human-readable AMS status
- **Reference**: BambuStudio AMS state machine

#### ams_exist_bits
- **Type**: `int`
- **Telemetry**: `print.ams.ams_exist_bits`
- **Purpose**: Bitmask of connected AMS units
- **Reference**: BambuStudio AMS detection

#### ams_connected_count
- **Type**: `int`
- **Telemetry**: Computed from `bin(ams_exist_bits).count("1")`
- **Valid Range**: `0-4` standard, `0-8` with AMS HT
- **Purpose**: Number of connected AMS units
- **Reference**: N/A (derived)

### Error Handling Attributes

#### print_error
- **Type**: `int`
- **Telemetry**: `print.print_error`
- **Purpose**: Main error code (32-bit HMS error)
- **Decoding**: `decodeError(print_error)` extracts module, severity, message
- **Reference**: BambuStudio HMS error handling

#### hms_errors
- **Type**: `list[dict]`
- **Telemetry**: `print.hms` + decoded `print_error`
- **Structure**: Each error contains `code`, `msg`, `module`, `severity`, `is_critical`, `type`, `url`
- **Purpose**: List of active HMS errors
- **Reference**: BambuStudio HMS system, ha-bambulab error decoding

### Network Attributes

#### wifi_signal_strength
- **Type**: `str`
- **Telemetry**: `print.wifi_signal`
- **Unit**: dBm
- **Purpose**: Wi-Fi signal strength indicator
- **Reference**: BambuStudio network monitoring

### Collections

#### ams_units
- **Type**: `list[AMSUnitState]`
- **Telemetry**: `print.ams.ams[]` + `info.module[]`
- **Purpose**: Complete state of all connected AMS units
- **Reference**: See [AMSUnitState](#amsunitstate) section

#### extruders
- **Type**: `list[ExtruderState]`
- **Telemetry**: `print.device.extruder.info[]`
- **Purpose**: State of all physical extruders
- **Reference**: See [ExtruderState](#extruderstate) section

#### spools
- **Type**: `list[BambuSpool]`
- **Telemetry**: Aggregated from AMS trays and external spools
- **Purpose**: All filament spools with properties
- **Reference**: See [BambuSpool](#bambuspool) section

#### climate
- **Type**: `BambuClimate`
- **Telemetry**: Multiple sources (see BambuClimate section)
- **Purpose**: All temperature, fan, and environmental data
- **Reference**: See [BambuClimate](#bambuclimate) section

### Internal/Debug Attributes

#### stat
- **Type**: `str`
- **Telemetry**: `print.stat`
- **Purpose**: Raw status bitmask (hex string) - contains chamber door/lid sensor bits
- **Reference**: BambuStudio status flags

#### fun
- **Type**: `str`
- **Telemetry**: `print.fun`
- **Purpose**: Raw function bitmask (hex string) - contains capability flags
- **Reference**: BambuStudio feature detection

---

## ExtruderState

Physical extruder/toolhead state.

**Source**: `src/bpm/bambustate.py`
**Telemetry Root**: `print.device.extruder.info[id]`

### Identification

#### id
- **Type**: `int`
- **Telemetry**: `extruder.info[].id`
- **Valid Values**: `0` (right/primary), `1` (left/secondary)
- **Purpose**: Physical extruder identifier
- **Reference**: BambuStudio extruder indexing

### Temperature Attributes

#### temp
- **Type**: `float`
- **Telemetry**: `extruder.info[].temp` (unpacked via `unpackTemperature()`)
- **Unit**: °C
- **Purpose**: Current extruder temperature
- **Reference**: BambuStudio thermal monitoring

#### temp_target
- **Type**: `int`
- **Telemetry**: `extruder.info[].temp` (high 16 bits)
- **Unit**: °C
- **Purpose**: Target extruder temperature
- **MQTT Control**: [Set Nozzle Temperature Target](mqtt-protocol-reference.md#set-nozzle-temperature-target)
- **Reference**: BambuStudio thermal control

### State Attributes

#### info_bits
- **Type**: `int`
- **Telemetry**: `extruder.info[].info`
- **Purpose**: Raw bitmask containing filament sensor states
- **Bit Structure**:
  - Bit 3: Nozzle present
  - Bit 2: Buffer loaded
  - Bit 1: Filament loaded
- **Reference**: BambuStudio `ExtruderInfo` parsing

#### state
- **Type**: `ExtruderInfoState` (IntEnum)
- **Telemetry**: Parsed from `info_bits`
- **Valid Values**:
  - `NO_NOZZLE (0)`: No nozzle detected
  - `EMPTY (1)`: Nozzle present, no filament
  - `BUFFER_LOADED (2)`: Filament in buffer
  - `LOADED (3)`: Filament fully loaded
- **Purpose**: Filament presence state
- **Reference**: BambuStudio `parseExtruderInfo()`

#### status
- **Type**: `ExtruderStatus` (IntEnum)
- **Telemetry**: `extruder.info[].stat` (parsed)
- **Valid Values**:
  - `IDLE (0)`: Not active
  - `HEATING (1)`: Heating in progress
  - `ACTIVE (2)`: Actively extruding
  - `SUCCESS (3)`: Operation completed
- **Purpose**: Operational extruder state
- **Reference**: BambuStudio `BBL_EXTRUDER_STATE` enum

### Tray Assignment Attributes

#### active_tray_id
- **Type**: `int`
- **Telemetry**: Computed from `extruder.info[].hnow`, `extruder.info[].snow`
- **Valid Range**: `-1`, `0-15`, `254-255`
- **Purpose**: Currently active tray for this extruder
- **Reference**: BambuStudio tray tracking algorithm

#### target_tray_id
- **Type**: `int`
- **Telemetry**: Computed from `extruder.info[].htar`, `extruder.info[].star`
- **Valid Range**: Same as `active_tray_id`
- **Purpose**: Target tray for this extruder
- **Reference**: BambuStudio tray targeting

#### tray_state
- **Type**: `TrayState` (IntEnum)
- **Telemetry**: Computed from `state` + `status` combination
- **Purpose**: Loading state for this extruder's tray
- **Reference**: State machine derived from BambuStudio

#### assigned_to_ams_id
- **Type**: `int`
- **Telemetry**: Set when AMS unit reports H2D extruder assignment
- **Valid Range**: `-1`, `0-3`, `128-131`
- **Purpose**: AMS unit assigned to this extruder (H2D dual-extruder)
- **Reference**: BambuStudio dual-extruder AMS routing

---

## AMSUnitState

Individual AMS unit state and drying control.

**Source**: `src/bpm/bambustate.py`
**Telemetry Root**: `print.ams.ams[id]`

### Identification

#### ams_id
- **Type**: `int`
- **Telemetry**: `ams[].id`
- **Valid Range**:
  - `0-3`: Standard AMS units
  - `128-131`: AMS HT units
- **Purpose**: Unique AMS unit identifier
- **Reference**: BambuStudio AMS addressing

#### chip_id
- **Type**: `str`
- **Telemetry**: `info.module[].sn` where module name starts with `n3f/`, `n3s/`, or `ams`
- **Purpose**: Hardware serial number
- **Reference**: BambuStudio module enumeration

#### model
- **Type**: `AMSModel` (IntEnum)
- **Telemetry**: Parsed from `ams[].info` bits 0-3, or derived from `chip_id` prefix
- **Valid Values**:
  - `UNKNOWN (0)`
  - `AMS_1 (1)`: First generation (SN: 006xxx)
  - `AMS_LITE (2)`: Lite variant (SN: 03Cxxx)
  - `AMS_2_PRO (3)`: Second gen Pro / N3F (SN: 19Cxxx)
  - `AMS_HT (4)`: High-Temp / N3S (SN: 19Fxxx)
- **Purpose**: AMS hardware model type
- **Reference**: BambuStudio `AMSModel` enum, serial prefix mapping

### Temperature Attributes

#### temp_actual
- **Type**: `float`
- **Telemetry**: `ams[].temp`
- **Unit**: °C
- **Purpose**: Current AMS internal temperature
- **Reference**: BambuStudio thermal monitoring

#### temp_target
- **Type**: `int`
- **Telemetry**: `ams[].target_temp` or captured during drying command
- **Unit**: °C
- **Purpose**: Target drying temperature
- **Reference**: BambuStudio drying control

### Humidity Attributes

#### humidity_index
- **Type**: `int`
- **Telemetry**: `ams[].humidity`
- **Valid Range**: `1-5` (levels)
- **Purpose**: Humidity level index
- **Reference**: BambuStudio humidity display

#### humidity_raw
- **Type**: `int`
- **Telemetry**: `ams[].humidity_raw`
- **Valid Range**: `0-100` (%)
- **Purpose**: Raw humidity percentage
- **Reference**: BambuStudio sensor data

### AMS Info Bit Field Attributes

All attributes below are extracted from the 32-bit `ams[].info` hex value.

**Reference**: BambuStudio `DevFilaSystem.cpp` `ParseAmsInfo()` function

#### ams_info
- **Type**: `int`
- **Telemetry**: `ams[].info` (hex string converted to int)
- **Purpose**: Raw AMS info bitmask containing all drying/assignment data
- **Reference**: BambuStudio AMS telemetry

#### heater_state
- **Type**: `AMSHeatingState` (IntEnum)
- **Telemetry**: `ams[].info` bits 4-7
- **Valid Values**:
  - `OFF (0)`: No drying active
  - `CHECKING (1)`: Checking drying status
  - `DRYING (2)`: Active drying phase
  - `COOLING (3)`: Cooling after drying
  - `STOPPING (4)`: Stopping drying process
  - `ERROR (5)`: Error state
  - `CANNOT_STOP_HEAT_OOC (6)`: Heat control out of control
  - `PRODUCT_TEST (7)`: Product testing mode
- **Purpose**: AMS drying/heater operational state
- **Reference**: BambuStudio `DryStatus` enum (AMS 2 Pro and AMS HT only)

#### dry_fan1_status
- **Type**: `AMSDryFanStatus` (IntEnum)
- **Telemetry**: `ams[].info` bits 18-19
- **Valid Values**:
  - `OFF (0)`: Fan off
  - `ON (1)`: Fan running
- **Purpose**: Primary drying fan state
- **Reference**: BambuStudio `DryFanStatus` enum

#### dry_fan2_status
- **Type**: `AMSDryFanStatus` (IntEnum)
- **Telemetry**: `ams[].info` bits 20-21
- **Valid Values**: Same as `dry_fan1_status`
- **Purpose**: Secondary drying fan state
- **Reference**: BambuStudio `DryFanStatus` enum

#### dry_sub_status
- **Type**: `AMSDrySubStatus` (IntEnum)
- **Telemetry**: `ams[].info` bits 22-25
- **Valid Values**:
  - `OFF (0)`: No active drying phase
  - `HEATING (1)`: Heating phase
  - `DEHUMIDIFY (2)`: Dehumidification phase
- **Purpose**: Specific drying cycle phase
- **Reference**: BambuStudio `DrySubStatus` enum

#### dry_time
- **Type**: `int`
- **Telemetry**: `ams[].dry_time`
- **Unit**: Minutes
- **Purpose**: Remaining drying time
- **Reference**: BambuStudio drying timer

### Tray Management

#### tray_exists
- **Type**: `list[bool]`
- **Telemetry**: `print.ams.tray_exist_bits` (parsed per-AMS)
- **Size**: `4` for standard AMS, `1` for AMS HT
- **Bit Mapping**:
  - Standard AMS (id 0-3): shift = `4 * id`, check 4 bits
  - AMS HT (id 128-131): shift = `16 + (4 * (id - 128))`, check 1 bit
- **Purpose**: Which tray slots have filament present
- **Reference**: BambuStudio tray existence detection

#### assigned_to_extruder
- **Type**: `ActiveTool` (IntEnum)
- **Telemetry**: `ams[].info` bits 8-11 (extruder_id)
- **Purpose**: Target extruder for H2D dual-extruder systems
- **Reference**: BambuStudio H2D AMS routing

---

## BambuClimate

All environmental, thermal, and fan control data.

**Source**: `src/bpm/bambustate.py`
**Telemetry Root**: Multiple sources

### Bed Temperature

#### bed_temp
- **Type**: `float`
- **Telemetry**: `print.bed_temper`
- **Unit**: °C
- **Purpose**: Current bed temperature
- **Reference**: BambuStudio thermal monitoring

#### bed_temp_target
- **Type**: `int`
- **Telemetry**: `print.bed_target_temper`
- **Unit**: °C
- **Purpose**: Target bed temperature
- **Reference**: BambuStudio thermal control
- **MQTT Control**: [Set Bed Temperature Target](mqtt-protocol-reference.md#set-bed-temperature-target)

### Chamber Temperature

#### chamber_temp
- **Type**: `float`
- **Telemetry**: `print.device.ctc.info.temp` (unpacked) or `print.chamber_temper`
- **Unit**: °C
- **Purpose**: Current chamber temperature
- **Reference**: BambuStudio CTC decoding

#### chamber_temp_target
- **Type**: `int`
- **Telemetry**: `print.device.ctc.info.temp` (high 16 bits) or set via `set_ctt` command
- **Unit**: °C
- **Purpose**: Target chamber temperature
- **Reference**: BambuStudio chamber control
- **MQTT Control**: [Set Chamber Temperature Target](mqtt-protocol-reference.md#set-chamber-temperature-target)

### Air Conditioning Control

#### air_conditioning_mode
- **Type**: `AirConditioningMode` (IntEnum)
- **Telemetry**: Derived from `print.device.airduct.modeCur`
- **Valid Values**:
  - `NOT_SUPPORTED (-1)`: No AC system
  - `COOL_MODE (0)`: Cooling/vent mode
  - `HEAT_MODE (1)`: Heating/recirculation mode
- **Purpose**: Chamber climate control mode
- **Reference**: BambuStudio airduct mode mapping

#### airduct_mode
- **Type**: `int`
- **Telemetry**: `print.device.airduct.modeCur`
- **Purpose**: Raw airduct mode value
- **Reference**: BambuStudio airduct control
- **MQTT Control**: [Chamber Air Conditioning Mode](mqtt-protocol-reference.md#chamber-air-conditioning-mode)

#### airduct_sub_mode
- **Type**: `int`
- **Telemetry**: `print.device.airduct.subMode`
- **Purpose**: Raw airduct sub-mode value
- **Reference**: BambuStudio airduct control

### Fan Speed Attributes

All fan speeds are scaled 0-100%.

#### part_cooling_fan_speed_percent
- **Type**: `int`
- **Telemetry**: `print.cooling_fan_speed` (scaled) or `airduct.parts[16].state`
- **Valid Range**: `0-100`
- **Unit**: %
- **Purpose**: Part cooling fan speed
- **Reference**: BambuStudio fan control, scaled via `scaleFanSpeed()` (0-15 → 0-100)

#### part_cooling_fan_speed_target_percent
- **Type**: `int`
- **Telemetry**: Currently mirrors `part_cooling_fan_speed_percent`
- **Valid Range**: `0-100`
- **Unit**: %
- **Purpose**: Target part cooling fan speed
- **Reference**: BambuStudio fan targets
- **MQTT Control**: [Part Cooling Fan (Layer Cooling)](mqtt-protocol-reference.md#part-cooling-fan-layer-cooling)

#### aux_fan_speed_percent
- **Type**: `int`
- **Telemetry**: `print.big_fan1_speed` (scaled) or `airduct.parts[32].state`
- **Valid Range**: `0-100`
- **Unit**: %
- **Purpose**: Auxiliary fan speed
- **Reference**: BambuStudio fan control
- **MQTT Control**: [Aux Fan (Hotend Cooling)](mqtt-protocol-reference.md#aux-fan-hotend-cooling)

#### exhaust_fan_speed_percent
- **Type**: `int`
- **Telemetry**: `print.big_fan2_speed` (scaled) or `airduct.parts[48].state`
- **Valid Range**: `0-100`
- **Unit**: %
- **Purpose**: Exhaust/chamber fan speed
- **Reference**: BambuStudio fan control
- **MQTT Control**: [Exhaust Fan](mqtt-protocol-reference.md#exhaust-fan)

#### heatbreak_fan_speed_percent
- **Type**: `int`
- **Telemetry**: `print.heatbreak_fan_speed` (scaled)
- **Valid Range**: `0-100`
- **Unit**: %
- **Purpose**: Heatbreak cooling fan speed
- **Reference**: BambuStudio fan control

### Zone Control Attributes

#### zone_intake_open
- **Type**: `bool`
- **Telemetry**: `print.device.airduct.parts[96].state` (non-zero = open)
- **Purpose**: Heater intake damper state
- **Reference**: BambuStudio zone control

#### zone_part_fan_percent
- **Type**: `int`
- **Telemetry**: `print.device.airduct.parts[16].state`
- **Valid Range**: `0-100`
- **Unit**: %
- **Purpose**: Internal part fan zone control
- **Reference**: BambuStudio zone mapping

#### zone_aux_percent
- **Type**: `int`
- **Telemetry**: `print.device.airduct.parts[32].state`
- **Valid Range**: `0-100`
- **Unit**: %
- **Purpose**: Auxiliary fan zone control
- **Reference**: BambuStudio zone mapping

#### zone_exhaust_percent
- **Type**: `int`
- **Telemetry**: `print.device.airduct.parts[48].state`
- **Valid Range**: `0-100`
- **Unit**: %
- **Purpose**: Exhaust fan zone control
- **Reference**: BambuStudio zone mapping

#### zone_top_vent_open
- **Type**: `bool`
- **Telemetry**: Computed from `zone_exhaust_percent > 0 and not zone_intake_open`
- **Purpose**: Top vent open state (derived)
- **Reference**: Logic derived from BambuStudio behavior

### Door/Lid Sensors

#### is_chamber_door_open
- **Type**: `bool`
- **Telemetry**: `print.stat` bit 23
- **Purpose**: Chamber door open sensor (H2 series)
- **Capability**: Requires `PrinterCapabilities.has_chamber_door_sensor`
- **Reference**: BambuStudio `fun` bit 12 detection, `stat` bit 23 state

#### is_chamber_lid_open
- **Type**: `bool`
- **Telemetry**: `print.stat` bit 24
- **Purpose**: Chamber lid open sensor (H2 series)
- **Capability**: Requires `PrinterCapabilities.has_chamber_door_sensor`
- **Reference**: BambuStudio `stat` bit 24 state

---

## BambuSpool

Filament spool properties and state.

**Source**: `src/bpm/bambuspool.py`
**Telemetry Root**: `print.ams.ams[].tray[]` or virtual spool

### Identification

#### id
- **Type**: `int`
- **Telemetry**: Computed from AMS/tray combination
- **Valid Range**: `0-23` (AMS slots), `254-255` (external)
- **Purpose**: Global spool identifier
- **Reference**: BambuStudio spool indexing

#### slot_id
- **Type**: `int`
- **Telemetry**: Tray index within AMS
- **Valid Range**: `0-3` (standard AMS), `0` (AMS HT), `254-255` (external)
- **Purpose**: Physical slot number
- **Reference**: BambuStudio tray addressing

#### ams_id
- **Type**: `int`
- **Telemetry**: Parent AMS unit ID
- **Valid Range**: `-1` (external), `0-3`, `128-131`
- **Purpose**: Associated AMS unit
- **Reference**: BambuStudio AMS association

### Filament Properties

#### name
- **Type**: `str`
- **Telemetry**: `tray[].tray_info_idx` (mapped) or RFID tag data
- **Purpose**: Filament product name
- **Reference**: BambuStudio filament database

#### type
- **Type**: `str`
- **Telemetry**: `tray[].tray_type`
- **Examples**: `PLA`, `PETG`, `ABS`, `TPU`, `ASA`, `PA`, `PET`, etc.
- **Purpose**: Filament material type
- **Reference**: BambuStudio material types

#### sub_brands
- **Type**: `str`
- **Telemetry**: `tray[].tray_sub_brands`
- **Examples**: `Matte`, `Pro`, `Tough`, `Support`, etc.
- **Purpose**: Filament variant/specialization
- **Reference**: Bambu Lab product variants

#### color
- **Type**: `str`
- **Telemetry**: `tray[].tray_color` (hex code converted via `webcolors`)
- **Format**: Hex `#RRGGBB` or color name
- **Purpose**: Filament color
- **Reference**: BambuStudio color handling

#### tray_info_idx
- **Type**: `str`
- **Telemetry**: `tray[].tray_info_idx`
- **Purpose**: Filament preset index in Bambu Studio
- **Reference**: BambuStudio filament database indexing

### Temperature Settings

#### bed_temp
- **Type**: `int`
- **Telemetry**: `tray[].bed_temp` or `tray[].bed_temp_type`
- **Unit**: °C
- **Purpose**: Recommended bed temperature
- **Reference**: BambuStudio filament profiles

#### nozzle_temp_min
- **Type**: `int`
- **Telemetry**: `tray[].nozzle_temp_min`
- **Unit**: °C
- **Purpose**: Minimum safe nozzle temperature
- **Reference**: BambuStudio filament profiles
- **MQTT Control**: [Set Filament Details / Spool Settings](mqtt-protocol-reference.md#set-filament-details-spool-settings)

#### nozzle_temp_max
- **Type**: `int`
- **Telemetry**: `tray[].nozzle_temp_max`
- **Unit**: °C
- **Purpose**: Maximum safe nozzle temperature
- **Reference**: BambuStudio filament profiles
- **MQTT Control**: [Set Filament Details / Spool Settings](mqtt-protocol-reference.md#set-filament-details-spool-settings)

#### drying_temp
- **Type**: `int`
- **Telemetry**: `tray[].drying_temp`
- **Unit**: °C
- **Purpose**: Recommended drying temperature
- **Reference**: BambuStudio filament drying settings
- **MQTT Control**: [AMS Filament Drying](mqtt-protocol-reference.md#ams-filament-drying)

#### drying_time
- **Type**: `int`
- **Telemetry**: `tray[].drying_time`
- **Unit**: Hours
- **Purpose**: Recommended drying duration
- **Reference**: BambuStudio filament drying settings
- **MQTT Control**: [AMS Filament Drying](mqtt-protocol-reference.md#ams-filament-drying)

### Print Settings

#### k
- **Type**: `float`
- **Telemetry**: `tray[].k`
- **Purpose**: K-Factor for linear advance (flow rate)
- **Reference**: BambuStudio pressure advance tuning

### Spool Status

#### remaining_percent
- **Type**: `int`
- **Telemetry**: `tray[].remain`
- **Valid Range**: `0-100`
- **Unit**: %
- **Purpose**: Estimated remaining filament
- **Reference**: BambuStudio filament tracking

#### state
- **Type**: `int`
- **Telemetry**: `tray[].state`
- **Purpose**: Spool operational state
- **Reference**: BambuStudio tray state

#### total_length
- **Type**: `int`
- **Telemetry**: Computed from spool capacity
- **Unit**: mm
- **Purpose**: Total filament length on spool
- **Reference**: BambuStudio filament tracking

#### tray_weight
- **Type**: `int`
- **Telemetry**: `tray[].tray_weight`
- **Unit**: grams
- **Purpose**: Current spool weight
- **Reference**: BambuStudio weighing system

---

## ProjectInfo

Details of the associated project (3MF file) including metadata and identification.

**Source**: `src/bpm/bambuproject.py`

### Identification Attributes

#### id
- **Type**: `str`
- **Default**: `""`
- **Purpose**: The unique identifier for this project (3MF storage location)
- **Format**: Full path on printer or FTPS server (e.g., `/cache/my_model.3mf`)
- **Reference**: FTPS file path or project identifier

#### name
- **Type**: `str`
- **Default**: `""`
- **Purpose**: The filename portion of the 3MF id
- **Example**: `"my_model.3mf"`
- **Reference**: Extracted from the `id` path

#### size
- **Type**: `int`
- **Default**: `0`
- **Unit**: bytes
- **Purpose**: The size of this 3MF file
- **Reference**: File system metadata

#### timestamp
- **Type**: `int`
- **Default**: `0`
- **Unit**: epoch seconds
- **Purpose**: The epoch timestamp of this 3MF file
- **Reference**: File modification time

#### md5
- **Type**: `str`
- **Default**: `""`
- **Purpose**: The MD5 checksum of this 3MF file
- **Format**: 32-character hexadecimal string
- **Usage**: Cache validation and file integrity verification
- **Reference**: Computed via `get_file_md5()` utility

### Print Configuration

#### plate_num
- **Type**: `int`
- **Default**: `1`
- **Valid Range**: `1-N` (depends on model capabilities)
- **Purpose**: The plate number this 3MF targets
- **Reference**: BambuStudio multi-plate support

#### metadata
- **Type**: `dict`
- **Default**: `{}` (empty dict)
- **Purpose**: The associated metadata of this 3MF file
- **Content**: Extracted from 3MF XML structure including:
  - Model information
  - Print settings
  - Filament requirements
  - Time/weight estimates
  - Thumbnail images (base64 encoded)
- **Reference**: BambuStudio 3MF metadata schema
- **Extraction**: Parsed from `Metadata/plate_*.xml` within 3MF archive

---

## ActiveJobInfo

Details of the currently active job running on the printer, including progress, stage, and project information.

**Source**: `src/bpm/bambuproject.py`
**Telemetry Root**: Computed from multiple telemetry sources

### Project Reference

#### project_info
- **Type**: `ProjectInfo | None`
- **Default**: `ProjectInfo()` (empty instance)
- **Purpose**: The 3MF details for the active job
- **Reference**: See [ProjectInfo](#projectinfo) section
- **Update**: Populated via `get_project_info()` method

#### project_file_command
- **Type**: `dict`
- **Default**: `{}` (empty dict)
- **Purpose**: The project_file command that triggered this job (if one did)
- **Content**: MQTT command payload used to start the print
- **Reference**: Original MQTT `project_file` command structure

### Stage Information

#### stage_id
- **Type**: `int`
- **Default**: `0`
- **Telemetry**: `print.mc_print_stage`
- **Purpose**: Current Stage numeric ID
- **Valid Values**: See `Stage` enum (0=Printing, 1=Auto Bed Leveling, etc.)
- **Reference**: BambuStudio `Stage` enumeration

#### stage_name
- **Type**: `str`
- **Default**: `""`
- **Telemetry**: Computed from `stage_id` via `Stage` enum
- **Purpose**: Current Stage human-readable name
- **Examples**: `"Printing"`, `"Auto Bed Leveling"`, `"Heatbed Preheating"`
- **Reference**: BambuStudio stage naming

### Progress Tracking

#### current_layer
- **Type**: `int`
- **Default**: `0`
- **Telemetry**: `print.layer_num`
- **Valid Range**: `0` to `total_layers`
- **Purpose**: Current layer index during print
- **Reference**: BambuStudio progress tracking

#### total_layers
- **Type**: `int`
- **Default**: `0`
- **Telemetry**: `print.total_layer_num`
- **Purpose**: The total number of layers for this job
- **Reference**: Sliced G-code layer count

#### print_percentage
- **Type**: `int`
- **Default**: `0`
- **Telemetry**: `print.mc_percent`
- **Valid Range**: `0-100`
- **Unit**: %
- **Purpose**: Overall print completion percentage
- **Reference**: BambuStudio progress calculation

### Time Tracking

#### elapsed_minutes
- **Type**: `int`
- **Default**: `0`
- **Telemetry**: Computed from `print.mc_remaining_time` and `print_percentage`
- **Unit**: minutes
- **Purpose**: The elapsed time in minutes for this (or the last) job
- **Reference**: Calculated from telemetry timing data

#### remaining_minutes
- **Type**: `int`
- **Default**: `0`
- **Telemetry**: `print.mc_remaining_time`
- **Unit**: minutes
- **Purpose**: Time remaining in minutes for the current job
- **Reference**: BambuStudio time estimation

#### monotonic_start_time
- **Type**: `float`
- **Default**: `-1.0`
- **Purpose**: The monotonic timestamp of when this job started
- **Reference**: Python `time.monotonic()` value at job start
- **Usage**: Accurate elapsed time calculation independent of system clock changes

### Job Details

#### subtask_name
- **Type**: `str`
- **Default**: `""`
- **Telemetry**: `print.subtask_name`
- **Purpose**: The subtask name for this job
- **Reference**: BambuStudio job naming

#### gcode_file
- **Type**: `str`
- **Default**: `""`
- **Telemetry**: `print.gcode_file`
- **Purpose**: The underlying G-code filename from this job feeding the printer
- **Format**: Path to plate-specific G-code extracted from 3MF
- **Example**: `"/cache/my_model_plate_1.gcode"`
- **Reference**: BambuStudio G-code extraction

#### print_type
- **Type**: `str`
- **Default**: `""`
- **Telemetry**: `print.print_type`
- **Valid Values**: `"local"`, `"cloud"` (should always be `"local"` for BPM)
- **Purpose**: Indicates whether this is a cloud or local job
- **Reference**: BambuStudio print source type

#### plate_num
- **Type**: `int`
- **Default**: `-1`
- **Telemetry**: `print.profile_id` or `print.task_id`
- **Valid Range**: `1-N` or `-1` (unknown)
- **Purpose**: The plate number this job is targeting
- **Reference**: Multi-plate print job identification

#### plate_type
- **Type**: `PlateType` (IntEnum)
- **Default**: `PlateType.NONE`
- **Telemetry**: `print.bed_type`
- **Valid Values**: See `PlateType` enum (Cool Plate, Engineering Plate, etc.)
- **Purpose**: The plate type associated with the job
- **Reference**: BambuStudio plate type enumeration

---

## Enumerations Reference

### ActiveTool
**Source**: `src/bpm/bambutools.py`

| Value | Name | Description |
|-------|------|-------------|
| -1 | SINGLE_EXTRUDER | Standard single toolhead (X1/P1/A1) |
| 0 | RIGHT_EXTRUDER | Primary toolhead in H2D systems |
| 1 | LEFT_EXTRUDER | Secondary toolhead in H2D systems |
| 15 | NOT_ACTIVE | Transitional state |

### AirConditioningMode
**Source**: `src/bpm/bambutools.py`

| Value | Name | Description |
|-------|------|-------------|
| -1 | NOT_SUPPORTED | No AC system |
| 0 | COOL_MODE | Cooling/vent mode, top vent may open |
| 1 | HEAT_MODE | Heating mode, recirculation active |

### AMSModel
**Source**: `src/bpm/bambutools.py`

| Value | Name | Serial Prefix | Description |
|-------|------|--------------|-------------|
| 0 | UNKNOWN | N/A | Unknown model |
| 1 | AMS_1 | 006 | First generation AMS |
| 2 | AMS_LITE | 03C | Lite variant |
| 3 | AMS_2_PRO | 19C | Second gen Pro (N3F) |
| 4 | AMS_HT | 19F | High-Temp variant (N3S) |

### AMSHeatingState
**Source**: `src/bpm/bambutools.py`
**Reference**: BambuStudio `DryStatus` enum

| Value | Name | Description |
|-------|------|-------------|
| 0 | OFF | No drying active |
| 1 | CHECKING | Checking drying status |
| 2 | DRYING | Active drying phase |
| 3 | COOLING | Cooling after drying |
| 4 | STOPPING | Stopping drying process |
| 5 | ERROR | Error state |
| 6 | CANNOT_STOP_HEAT_OOC | Heat control out of control |
| 7 | PRODUCT_TEST | Product testing mode |

### AMSDrySubStatus
**Source**: `src/bpm/bambutools.py`
**Reference**: BambuStudio `DrySubStatus` enum

| Value | Name | Description |
|-------|------|-------------|
| 0 | OFF | No active drying phase |
| 1 | HEATING | Heating phase of drying |
| 2 | DEHUMIDIFY | Dehumidification phase |

### AMSDryFanStatus
**Source**: `src/bpm/bambutools.py`
**Reference**: BambuStudio `DryFanStatus` enum

| Value | Name | Description |
|-------|------|-------------|
| 0 | OFF | Fan is off |
| 1 | ON | Fan is running |

### ExtruderInfoState
**Source**: `src/bpm/bambutools.py`

| Value | Name | Description |
|-------|------|-------------|
| 0 | NO_NOZZLE | No nozzle detected |
| 1 | EMPTY | Nozzle present, no filament |
| 2 | BUFFER_LOADED | Filament in buffer |
| 3 | LOADED | Filament fully loaded |

### ExtruderStatus
**Source**: `src/bpm/bambutools.py`
**Reference**: BambuStudio `BBL_EXTRUDER_STATE` enum

| Value | Name | Description |
|-------|------|-------------|
| 0 | IDLE | Not active |
| 1 | HEATING | Heating in progress |
| 2 | ACTIVE | Actively extruding |
| 3 | SUCCESS | Operation completed |

### TrayState
**Source**: `src/bpm/bambutools.py`

| Value | Name | Description |
|-------|------|-------------|
| 0 | UNLOADED | Tray unloaded |
| 1 | LOADED | Tray loaded |
| 2 | LOADING | Loading in progress |
| 3 | UNLOADING | Unloading in progress |

---

## Parsing Functions Reference

### Temperature Unpacking

#### unpackTemperature(raw_temp: int) -> tuple[float, float]
**Source**: `src/bpm/bambutools.py`

- **Input**: 32-bit packed temperature integer
- **Output**: `(current_temp, target_temp)` tuple
- **Algorithm**:
  - Current = low 16 bits (`raw_temp & 0xFFFF`)
  - Target = high 16 bits (`(raw_temp >> 16) & 0xFFFF`)
- **Reference**: BambuStudio temperature encoding

### AMS Info Parsing

#### parseAMSInfo(info_hex: str) -> dict
**Source**: `src/bpm/bambutools.py`
**Reference**: BambuStudio `DevFilaSystem::ParseAmsInfo()`

Extracts 6 bit fields from 32-bit AMS info value:

| Bits | Field | Type | Description |
|------|-------|------|-------------|
| 0-3 | ams_type | AMSModel | Hardware model |
| 4-7 | heater_state | AMSHeatingState | Drying state |
| 8-11 | extruder_id | int | H2D toolhead assignment |
| 18-19 | dry_fan1_status | AMSDryFanStatus | Fan 1 state |
| 20-21 | dry_fan2_status | AMSDryFanStatus | Fan 2 state |
| 22-25 | dry_sub_status | AMSDrySubStatus | Drying phase |

### Extruder Parsing

#### parseExtruderInfo(info_int: int) -> ExtruderInfoState
**Source**: `src/bpm/bambutools.py`

- **Bit 3**: Nozzle present flag
- **Bit 2**: Buffer loaded flag
- **Bit 1**: Filament loaded flag
- **Reference**: BambuStudio extruder sensor logic

#### parseExtruderStatus(stat_int: int) -> ExtruderStatus
**Source**: `src/bpm/bambutools.py`

- **Bits 8-9**: Working state (`0x02`/`0x03` = ACTIVE)
- **Bit 0**: Heating flag
- **Reference**: BambuStudio `BBL_EXTRUDER_STATE`

### Fan Speed Scaling

#### scaleFanSpeed(raw_val: Any) -> int
**Source**: `src/bpm/bambutools.py`

- **Input**: 0-15 proprietary fan speed
- **Output**: 0-100 percentage
- **Formula**: `round((val / 15.0) * 100)`
- **Reference**: BambuStudio fan speed mapping

### Error Decoding

#### decodeError(error: int) -> dict
**Source**: `src/bpm/bambutools.py`

Decodes 32-bit HMS error into structured dictionary:

- **Bits 24-31**: Module ID
- **Bits 16-23**: Severity mask
- **Bits 0-15**: Error code
- **Output**: `{code, msg, module, severity, is_critical, type, url}`
- **Reference**: BambuStudio HMS error database

#### decodeHMS(hms_list: list) -> list[dict]
**Source**: `src/bpm/bambutools.py`

Processes HMS error list from telemetry:

- **Input**: `[{attr: int, code: int}, ...]`
- **Output**: List of decoded error dictionaries
- **Reference**: BambuStudio HMS processing

---

## Telemetry Message Structure

### Standard Telemetry Update
```json
{
  "print": {
    "gcode_state": "RUNNING",
    "mc_percent": 45,
    "nozzle_temper": 220.5,
    "bed_temper": 60.0,
    "ams": {
      "tray_now": "3",
      "ams_exist_bits": "F",
      "ams": [
        {
          "id": 0,
          "temp": 25.5,
          "humidity": 3,
          "info": "2003"
        }
      ]
    },
    "device": {
      "extruder": {
        "state": 0,
        "info": [
          {
            "id": 0,
            "temp": 14418176,
            "info": 11,
            "stat": 0
          }
        ]
      }
    }
  }
}
```

### AMS Drying Status Update
```json
{
  "print": {
    "ams": {
      "ams": [
        {
          "id": 0,
          "temp": 65.2,
          "dry_time": 180,
          "info": "142024"
        }
      ]
    }
  }
}
```

### HMS Error Update
```json
{
  "print": {
    "print_error": 50397185,
    "hms": [
      {
        "attr": 50397185,
        "code": 100
      }
    ]
  }
}
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.1 | 2026-02-25 | Added BambuConfig, PrinterCapabilities, ProjectInfo, ActiveJobInfo dataclasses; comprehensive MQTT Control references; field-level consistency |
| 1.0 | 2026-02-23 | Initial comprehensive data dictionary |
