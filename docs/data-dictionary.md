# Bambu Printer Manager - Data Dictionary

## Overview

This comprehensive data dictionary documents all attributes manifested in the bambu-printer-manager library. Each attribute includes its ancestry (parent class), telemetry source (MQTT JSON path), type information, valid ranges, and purpose.

### Related Documentation

- **[MQTT Protocol Reference](mqtt-protocol-reference.md)** — Details how to control printer attributes via MQTT commands with field breakdowns, example JSON payloads, and usage patterns
- **[Code Reference](reference/bpm/bambuprinter.md)** — API/class/function reference generated from source modules
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
BambuPrinter (runtime root / orchestration)
├── config: BambuConfig
├── printer_state: BambuState
└── active_job_info: ActiveJobInfo

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

## Data Dictionary Index

Quick alphabetical reference to all documented fields. Fields marked with * appear in multiple classes.

| Field | Class | Description | Source Material |
|-------|-------|-------------|-----------------|
| [access_code](#access_code) | BambuConfig | 8-character LAN-only access code for MQTT authentication | [Field Definition](#access_code) · [BambuConfig](reference/bpm/bambuconfig.md#bpm.bambuconfig.BambuConfig) |
| [info_bits](#info_bits) | ExtruderState | Raw bitmask containing filament sensor states | [Field Definition](#info_bits) · [ExtruderState](reference/bpm/bambustate.md#bpm.bambustate.ExtruderState) |
| [active_ams_id](#active_ams_id) | BambuState | Currently active AMS unit ID | [Field Definition](#active_ams_id) · [BambuState](reference/bpm/bambustate.md#bpm.bambustate.BambuState) |
| [is_chamber_door_open](#is_chamber_door_open) | BambuClimate | Chamber door open sensor (H2 series) | [Field Definition](#is_chamber_door_open) · [BambuClimate](reference/bpm/bambustate.md#bpm.bambustate.BambuClimate) |
| [active_nozzle_temp](#active_nozzle_temp) | BambuState | Current nozzle temperature | [Field Definition](#active_nozzle_temp) · [BambuState](reference/bpm/bambustate.md#bpm.bambustate.BambuState) |
| [is_chamber_lid_open](#is_chamber_lid_open) | BambuClimate | Chamber lid open sensor (H2 series) | [Field Definition](#is_chamber_lid_open) · [BambuClimate](reference/bpm/bambustate.md#bpm.bambustate.BambuClimate) |
| [active_nozzle_temp_target](#active_nozzle_temp_target) | BambuState | Target nozzle temperature | [Field Definition](#active_nozzle_temp_target) · [BambuState](reference/bpm/bambustate.md#bpm.bambustate.BambuState) |
| [is_external_spool_active](#is_external_spool_active) | BambuState | Indicates external spool usage | [Field Definition](#is_external_spool_active) · [BambuState](reference/bpm/bambustate.md#bpm.bambustate.BambuState) |
| [active_tool](#active_tool) | BambuState | Currently active extruder in dual-extruder systems | [Field Definition](#active_tool) · [BambuState](reference/bpm/bambustate.md#bpm.bambustate.BambuState) |
| [active_tray_id](#active_tray_id) | BambuState, ExtruderState | Currently active tray for this extruder | [Field Definition](#active_tray_id) · [BambuState](reference/bpm/bambustate.md#bpm.bambustate.BambuState), [ExtruderState](reference/bpm/bambustate.md#bpm.bambustate.ExtruderState) |
| [k](#k) | BambuSpool | K-Factor for linear advance (flow rate) | [Field Definition](#k) · [BambuSpool](reference/bpm/bambuspool.md#bpm.bambuspool.BambuSpool) |
| [active_tray_state](#active_tray_state) | BambuState | Filament loading operational state | [Field Definition](#active_tray_state) · [BambuState](reference/bpm/bambustate.md#bpm.bambustate.BambuState) |
| [active_tray_state_name](#active_tray_state_name) | BambuState | Human-readable tray state | [Field Definition](#active_tray_state_name) · [BambuState](reference/bpm/bambustate.md#bpm.bambustate.BambuState) |
| [md5](#md5) | ProjectInfo | The MD5 checksum of this 3MF file | [Field Definition](#md5) · [ProjectInfo](reference/bpm/bambuproject.md#bpm.bambuproject.ProjectInfo) |
| [air_conditioning_mode](#air_conditioning_mode) | BambuClimate | Chamber climate control mode | [Field Definition](#air_conditioning_mode) · [BambuClimate](reference/bpm/bambustate.md#bpm.bambustate.BambuClimate) |
| [metadata](#metadata) | ProjectInfo | The associated metadata of this 3MF file | [Field Definition](#metadata) · [ProjectInfo](reference/bpm/bambuproject.md#bpm.bambuproject.ProjectInfo) |
| [airduct_mode](#airduct_mode) | BambuClimate | Raw airduct mode value | [Field Definition](#airduct_mode) · [BambuClimate](reference/bpm/bambustate.md#bpm.bambustate.BambuClimate) |
| [model](#model) | AMSUnitState | AMS hardware model type | [Field Definition](#model) · [AMSUnitState](reference/bpm/bambustate.md#bpm.bambustate.AMSUnitState) |
| [airduct_sub_mode](#airduct_sub_mode) | BambuClimate | Raw airduct sub-mode value | [Field Definition](#airduct_sub_mode) · [BambuClimate](reference/bpm/bambustate.md#bpm.bambustate.BambuClimate) |
| [monotonic_start_time](#monotonic_start_time) | ActiveJobInfo | The monotonic timestamp of when this job started | [Field Definition](#monotonic_start_time) · [ActiveJobInfo](reference/bpm/bambuproject.md#bpm.bambuproject.ActiveJobInfo) |
| [ams_connected_count](#ams_connected_count) | BambuState | Number of connected AMS units | [Field Definition](#ams_connected_count) · [BambuState](reference/bpm/bambustate.md#bpm.bambustate.BambuState) |
| [mqtt_client_id](#mqtt_client_id) | BambuConfig | Unique identifier used during the MQTT handshake protocol | [Field Definition](#mqtt_client_id) · [BambuConfig](reference/bpm/bambuconfig.md#bpm.bambuconfig.BambuConfig) |
| [ams_exist_bits](#ams_exist_bits) | BambuState | Bitmask of connected AMS units | [Field Definition](#ams_exist_bits) · [BambuState](reference/bpm/bambustate.md#bpm.bambustate.BambuState) |
| [mqtt_port](#mqtt_port) | BambuConfig | Network port for the SSL-encrypted MQTT broker | [Field Definition](#mqtt_port) · [BambuConfig](reference/bpm/bambuconfig.md#bpm.bambuconfig.BambuConfig) |
| [ams_firmware_version](#ams_firmware_version) | BambuConfig | Semantic version string of the primary AMS controller | [Field Definition](#ams_firmware_version) · [BambuConfig](reference/bpm/bambuconfig.md#bpm.bambuconfig.BambuConfig) |
| [mqtt_username](#mqtt_username) | BambuConfig | Authentication username for the local MQTT broker | [Field Definition](#mqtt_username) · [BambuConfig](reference/bpm/bambuconfig.md#bpm.bambuconfig.BambuConfig) |
| [ams_id](#ams_id) | AMSUnitState, BambuSpool | Associated AMS unit | [Field Definition](#ams_id) · [AMSUnitState](reference/bpm/bambustate.md#bpm.bambustate.AMSUnitState), [BambuSpool](reference/bpm/bambuspool.md#bpm.bambuspool.BambuSpool) |
| [ams_info](#ams_info) | AMSUnitState | Raw AMS info bitmask containing all drying/assignment data | [Field Definition](#ams_info) · [AMSUnitState](reference/bpm/bambustate.md#bpm.bambustate.AMSUnitState) |
| [name](#name) | BambuSpool, ProjectInfo | The filename portion of the 3MF id | [Field Definition](#name) · [BambuSpool](reference/bpm/bambuspool.md#bpm.bambuspool.BambuSpool), [ProjectInfo](reference/bpm/bambuproject.md#bpm.bambuproject.ProjectInfo) |
| [ams_status_raw](#ams_status_raw) | BambuState | Raw AMS status bitmask | [Field Definition](#ams_status_raw) · [BambuState](reference/bpm/bambustate.md#bpm.bambustate.BambuState) |
| [nozzle_temp_max](#nozzle_temp_max) | BambuSpool | Maximum safe nozzle temperature | [Field Definition](#nozzle_temp_max) · [BambuSpool](reference/bpm/bambuspool.md#bpm.bambuspool.BambuSpool) |
| [ams_status_text](#ams_status_text) | BambuState | Human-readable AMS status | [Field Definition](#ams_status_text) · [BambuState](reference/bpm/bambustate.md#bpm.bambustate.BambuState) |
| [nozzle_temp_min](#nozzle_temp_min) | BambuSpool | Minimum safe nozzle temperature | [Field Definition](#nozzle_temp_min) · [BambuSpool](reference/bpm/bambuspool.md#bpm.bambuspool.BambuSpool) |
| [ams_units](#ams_units) | BambuState | Complete state of all connected AMS units | [Field Definition](#ams_units) · [BambuState](reference/bpm/bambustate.md#bpm.bambustate.BambuState) |
| [assigned_to_ams_id](#assigned_to_ams_id) | ExtruderState | AMS unit assigned to this extruder | [Field Definition](#assigned_to_ams_id) · [ExtruderState](reference/bpm/bambustate.md#bpm.bambustate.ExtruderState) |
| [part_cooling_fan_speed_percent](#part_cooling_fan_speed_percent) | BambuClimate | Part cooling fan speed | [Field Definition](#part_cooling_fan_speed_percent) · [BambuClimate](reference/bpm/bambustate.md#bpm.bambustate.BambuClimate) |
| [assigned_to_extruder](#assigned_to_extruder) | AMSUnitState | Target extruder for H2D dual-extruder systems | [Field Definition](#assigned_to_extruder) · [AMSUnitState](reference/bpm/bambustate.md#bpm.bambustate.AMSUnitState) |
| [part_cooling_fan_speed_target_percent](#part_cooling_fan_speed_target_percent) | BambuClimate | Target part cooling fan speed | [Field Definition](#part_cooling_fan_speed_target_percent) · [BambuClimate](reference/bpm/bambustate.md#bpm.bambustate.BambuClimate) |
| [auto_recovery](#auto_recovery) | BambuConfig | Firmware-level toggle for resuming prints after step-loss | [Field Definition](#auto_recovery) · [BambuConfig](reference/bpm/bambuconfig.md#bpm.bambuconfig.BambuConfig) |
| [plate_num](#plate_num) | ProjectInfo, ActiveJobInfo | The plate number this job is targeting | [Field Definition](#plate_num) · [ProjectInfo](reference/bpm/bambuproject.md#bpm.bambuproject.ProjectInfo), [ActiveJobInfo](reference/bpm/bambuproject.md#bpm.bambuproject.ActiveJobInfo) |
| [auto_switch_filament](#auto_switch_filament) | BambuConfig | Enables automatic AMS failover to redundant spools | [Field Definition](#auto_switch_filament) · [BambuConfig](reference/bpm/bambuconfig.md#bpm.bambuconfig.BambuConfig) |
| [plate_type](#plate_type) | ActiveJobInfo | The plate type associated with the job | [Field Definition](#plate_type) · [ActiveJobInfo](reference/bpm/bambuproject.md#bpm.bambuproject.ActiveJobInfo) |
| [bpm_cache_path](#bpm_cache_path) | BambuConfig | The underlying directory BPM uses for managing cache/metadata | [Field Definition](#bpm_cache_path) · [BambuConfig](reference/bpm/bambuconfig.md#bpm.bambuconfig.BambuConfig) |
| [plates](#plates) | ProjectInfo | The set of plate numbers discovered in the 3MF package | [Field Definition](#plates) · [ProjectInfo](reference/bpm/bambuproject.md#bpm.bambuproject.ProjectInfo) |
| [aux_fan_speed_percent](#aux_fan_speed_percent) | BambuClimate | Auxiliary fan speed | [Field Definition](#aux_fan_speed_percent) · [BambuClimate](reference/bpm/bambustate.md#bpm.bambustate.BambuClimate) |
| [print_error](#print_error) | BambuState | Main error code (32-bit HMS error) | [Field Definition](#print_error) · [BambuState](reference/bpm/bambustate.md#bpm.bambustate.BambuState) |
| [print_percentage](#print_percentage) | ActiveJobInfo | Overall print completion percentage | [Field Definition](#print_percentage) · [ActiveJobInfo](reference/bpm/bambuproject.md#bpm.bambuproject.ActiveJobInfo) |
| [bed_temp](#bed_temp) | BambuClimate, BambuSpool | Recommended bed temperature | [Field Definition](#bed_temp) · [BambuClimate](reference/bpm/bambustate.md#bpm.bambustate.BambuClimate), [BambuSpool](reference/bpm/bambuspool.md#bpm.bambuspool.BambuSpool) |
| [print_type](#print_type) | ActiveJobInfo | Indicates whether this is a cloud or local job | [Field Definition](#print_type) · [ActiveJobInfo](reference/bpm/bambuproject.md#bpm.bambuproject.ActiveJobInfo) |
| [bed_temp_target](#bed_temp_target) | BambuClimate | Target bed temperature | [Field Definition](#bed_temp_target) · [BambuClimate](reference/bpm/bambustate.md#bpm.bambustate.BambuClimate) |
| [printer_model](#printer_model) | BambuConfig | Classification of the printer hardware (e.g., A1, H2D) derived from the serial number prefix | [Field Definition](#printer_model) · [BambuConfig](reference/bpm/bambuconfig.md#bpm.bambuconfig.BambuConfig) |
| [buildplate_marker_detector](#buildplate_marker_detector) | BambuConfig | Toggles the AI vision ArUco marker scanning system used to verify build surface compatibility | [Field Definition](#buildplate_marker_detector) · [BambuConfig](reference/bpm/bambuconfig.md#bpm.bambuconfig.BambuConfig) |
| [project_file_command](#project_file_command) | ActiveJobInfo | The project_file command that triggered this job (if one did) | [Field Definition](#project_file_command) · [ActiveJobInfo](reference/bpm/bambuproject.md#bpm.bambuproject.ActiveJobInfo) |
| [calibrate_remain_flag](#calibrate_remain_flag) | BambuConfig | Enablement for the spool-weight based estimation of the remaining filament length in the AMS | [Field Definition](#calibrate_remain_flag) · [BambuConfig](reference/bpm/bambuconfig.md#bpm.bambuconfig.BambuConfig) |
| [project_info](#project_info) | ActiveJobInfo | The 3MF details for the active job | [Field Definition](#project_info) · [ActiveJobInfo](reference/bpm/bambuproject.md#bpm.bambuproject.ActiveJobInfo) |
| [capabilities](#capabilities) | BambuConfig | Pre-defined or discovered hardware feature set | [Field Definition](#capabilities) · [BambuConfig](reference/bpm/bambuconfig.md#bpm.bambuconfig.BambuConfig) |
| [remaining_minutes](#remaining_minutes) | ActiveJobInfo | Time remaining in minutes for the current job | [Field Definition](#remaining_minutes) · [ActiveJobInfo](reference/bpm/bambuproject.md#bpm.bambuproject.ActiveJobInfo) |
| [chamber_temp](#chamber_temp) | BambuClimate | Current chamber temperature | [Field Definition](#chamber_temp) · [BambuClimate](reference/bpm/bambustate.md#bpm.bambustate.BambuClimate) |
| [remaining_percent](#remaining_percent) | BambuSpool | Estimated remaining filament | [Field Definition](#remaining_percent) · [BambuSpool](reference/bpm/bambuspool.md#bpm.bambuspool.BambuSpool) |
| [chamber_temp_target](#chamber_temp_target) | BambuClimate | Target chamber temperature | [Field Definition](#chamber_temp_target) · [BambuClimate](reference/bpm/bambustate.md#bpm.bambustate.BambuClimate) |
| [chip_id](#chip_id) | AMSUnitState | Hardware serial number | [Field Definition](#chip_id) · [AMSUnitState](reference/bpm/bambustate.md#bpm.bambustate.AMSUnitState) |
| [serial_number](#serial_number) | BambuConfig | Unique hardware identifier used to derive the printer model | [Field Definition](#serial_number) · [BambuConfig](reference/bpm/bambuconfig.md#bpm.bambuconfig.BambuConfig) |
| [climate](#climate) | BambuState | All temperature, fan, and environmental data | [Field Definition](#climate) · [BambuState](reference/bpm/bambustate.md#bpm.bambustate.BambuState) |
| [size](#size) | ProjectInfo | The size of this 3MF file | [Field Definition](#size) · [ProjectInfo](reference/bpm/bambuproject.md#bpm.bambuproject.ProjectInfo) |
| [color](#color) | BambuSpool | Filament color | [Field Definition](#color) · [BambuSpool](reference/bpm/bambuspool.md#bpm.bambuspool.BambuSpool) |
| [slot_id](#slot_id) | BambuSpool | Physical slot number | [Field Definition](#slot_id) · [BambuSpool](reference/bpm/bambuspool.md#bpm.bambuspool.BambuSpool) |
| [current_layer](#current_layer) | ActiveJobInfo | Current layer index during print | [Field Definition](#current_layer) · [ActiveJobInfo](reference/bpm/bambuproject.md#bpm.bambuproject.ActiveJobInfo) |
| [sound_enable](#sound_enable) | BambuConfig | Controls the machine's internal speaker for user notifications | [Field Definition](#sound_enable) · [BambuConfig](reference/bpm/bambuconfig.md#bpm.bambuconfig.BambuConfig) |
| [dry_fan1_status](#dry_fan1_status) | AMSUnitState | Primary drying fan state | [Field Definition](#dry_fan1_status) · [AMSUnitState](reference/bpm/bambustate.md#bpm.bambustate.AMSUnitState) |
| [spools](#spools) | BambuState | All filament spools with properties | [Field Definition](#spools) · [BambuState](reference/bpm/bambustate.md#bpm.bambustate.BambuState) |
| [stage_id](#stage_id) | ActiveJobInfo | Current Stage numeric ID | [Field Definition](#stage_id) · [ActiveJobInfo](reference/bpm/bambuproject.md#bpm.bambuproject.ActiveJobInfo) |
| [dry_fan2_status](#dry_fan2_status) | AMSUnitState | Secondary drying fan state | [Field Definition](#dry_fan2_status) · [AMSUnitState](reference/bpm/bambustate.md#bpm.bambustate.AMSUnitState) |
| [stage_name](#stage_name) | ActiveJobInfo | Current Stage human-readable name | [Field Definition](#stage_name) · [ActiveJobInfo](reference/bpm/bambuproject.md#bpm.bambuproject.ActiveJobInfo) |
| [dry_sub_status](#dry_sub_status) | AMSUnitState | Specific drying cycle phase | [Field Definition](#dry_sub_status) · [AMSUnitState](reference/bpm/bambustate.md#bpm.bambustate.AMSUnitState) |
| [startup_read_option](#startup_read_option) | BambuConfig | Configures whether the AMS unit performs a full RFID scan of all slots upon printer power-on | [Field Definition](#startup_read_option) · [BambuConfig](reference/bpm/bambuconfig.md#bpm.bambuconfig.BambuConfig) |
| [dry_time](#dry_time) | AMSUnitState | Remaining drying time | [Field Definition](#dry_time) · [AMSUnitState](reference/bpm/bambustate.md#bpm.bambustate.AMSUnitState) |
| [stat](#stat) | BambuState | Raw status bitmask (hex string) - contains chamber door/lid sensor bits | [Field Definition](#stat) · [BambuState](reference/bpm/bambustate.md#bpm.bambustate.BambuState) |
| [state](#state) | ExtruderState, BambuSpool | Spool operational state | [Field Definition](#state) · [ExtruderState](reference/bpm/bambustate.md#bpm.bambustate.ExtruderState), [BambuSpool](reference/bpm/bambuspool.md#bpm.bambuspool.BambuSpool) |
| [drying_temp](#drying_temp) | BambuSpool | Recommended drying temperature | [Field Definition](#drying_temp) · [BambuSpool](reference/bpm/bambuspool.md#bpm.bambuspool.BambuSpool) |
| [status](#status) | ExtruderState | Operational extruder state | [Field Definition](#status) · [ExtruderState](reference/bpm/bambustate.md#bpm.bambustate.ExtruderState) |
| [drying_time](#drying_time) | BambuSpool | Recommended drying duration | [Field Definition](#drying_time) · [BambuSpool](reference/bpm/bambuspool.md#bpm.bambuspool.BambuSpool) |
| [sub_brands](#sub_brands) | BambuSpool | Filament variant/specialization | [Field Definition](#sub_brands) · [BambuSpool](reference/bpm/bambuspool.md#bpm.bambuspool.BambuSpool) |
| [subtask_name](#subtask_name) | ActiveJobInfo | The subtask name for this job | [Field Definition](#subtask_name) · [ActiveJobInfo](reference/bpm/bambuproject.md#bpm.bambuproject.ActiveJobInfo) |
| [elapsed_minutes](#elapsed_minutes) | ActiveJobInfo | The elapsed time in minutes for this (or the last) job | [Field Definition](#elapsed_minutes) · [ActiveJobInfo](reference/bpm/bambuproject.md#bpm.bambuproject.ActiveJobInfo) |
| [exhaust_fan_speed_percent](#exhaust_fan_speed_percent) | BambuClimate | Exhaust/chamber fan speed | [Field Definition](#exhaust_fan_speed_percent) · [BambuClimate](reference/bpm/bambustate.md#bpm.bambustate.BambuClimate) |
| [target_tray_id](#target_tray_id) | BambuState, ExtruderState | Target tray for this extruder | [Field Definition](#target_tray_id) · [BambuState](reference/bpm/bambustate.md#bpm.bambustate.BambuState), [ExtruderState](reference/bpm/bambustate.md#bpm.bambustate.ExtruderState) |
| [external_chamber](#external_chamber) | BambuConfig | If True, ignores internal CTC telemetry to allow manual sensor injection | [Field Definition](#external_chamber) · [BambuConfig](reference/bpm/bambuconfig.md#bpm.bambuconfig.BambuConfig) |
| [temp](#temp) | ExtruderState | Current extruder temperature | [Field Definition](#temp) · [ExtruderState](reference/bpm/bambustate.md#bpm.bambustate.ExtruderState) |
| [extruders](#extruders) | BambuState | State of all physical extruders | [Field Definition](#extruders) · [BambuState](reference/bpm/bambustate.md#bpm.bambustate.BambuState) |
| [temp_actual](#temp_actual) | AMSUnitState | Current AMS internal temperature | [Field Definition](#temp_actual) · [AMSUnitState](reference/bpm/bambustate.md#bpm.bambustate.AMSUnitState) |
| [temp_target](#temp_target) | ExtruderState, AMSUnitState | Target drying temperature | [Field Definition](#temp_target) · [ExtruderState](reference/bpm/bambustate.md#bpm.bambustate.ExtruderState), [AMSUnitState](reference/bpm/bambustate.md#bpm.bambustate.AMSUnitState) |
| [filament_tangle_detect](#filament_tangle_detect) | BambuConfig | Master switch for AMS tension-based monitor logic | [Field Definition](#filament_tangle_detect) · [BambuConfig](reference/bpm/bambuconfig.md#bpm.bambuconfig.BambuConfig) |
| [timestamp](#timestamp) | ProjectInfo | The epoch timestamp of this 3MF file | [Field Definition](#timestamp) · [ProjectInfo](reference/bpm/bambuproject.md#bpm.bambuproject.ProjectInfo) |
| [firmware_version](#firmware_version) | BambuConfig | Semantic version string of the main printer firmware | [Field Definition](#firmware_version) · [BambuConfig](reference/bpm/bambuconfig.md#bpm.bambuconfig.BambuConfig) |
| [total_layers](#total_layers) | ActiveJobInfo | The total number of layers for this job | [Field Definition](#total_layers) · [ActiveJobInfo](reference/bpm/bambuproject.md#bpm.bambuproject.ActiveJobInfo) |
| [fun](#fun) | BambuState | Raw function bitmask (hex string) - contains capability flags | [Field Definition](#fun) · [BambuState](reference/bpm/bambustate.md#bpm.bambustate.BambuState) |
| [total_length](#total_length) | BambuSpool | Total filament length on spool | [Field Definition](#total_length) · [BambuSpool](reference/bpm/bambuspool.md#bpm.bambuspool.BambuSpool) |
| [tray_exists](#tray_exists) | AMSUnitState | Which tray slots have filament present | [Field Definition](#tray_exists) · [AMSUnitState](reference/bpm/bambustate.md#bpm.bambustate.AMSUnitState) |
| [gcode_file](#gcode_file) | ActiveJobInfo | The underlying G-code filename from this job feeding the printer | [Field Definition](#gcode_file) · [ActiveJobInfo](reference/bpm/bambuproject.md#bpm.bambuproject.ActiveJobInfo) |
| [tray_info_idx](#tray_info_idx) | BambuSpool | Filament preset index in Bambu Studio | [Field Definition](#tray_info_idx) · [BambuSpool](reference/bpm/bambuspool.md#bpm.bambuspool.BambuSpool) |
| [gcode_state](#gcode_state) | BambuState | Current G-code execution state | [Field Definition](#gcode_state) · [BambuState](reference/bpm/bambustate.md#bpm.bambustate.BambuState) |
| [tray_read_option](#tray_read_option) | BambuConfig | Toggles the automatic RFID identification sequence when a new filament spool is inserted or detected | [Field Definition](#tray_read_option) · [BambuConfig](reference/bpm/bambuconfig.md#bpm.bambuconfig.BambuConfig) |
| [tray_state](#tray_state) | ExtruderState | Loading state for this extruder's tray | [Field Definition](#tray_state) · [ExtruderState](reference/bpm/bambustate.md#bpm.bambustate.ExtruderState) |
| [has_air_filtration](#has_air_filtration) | PrinterCapabilities | Indicates the motorized airduct and filtration subsystem is physically installed | [Field Definition](#has_air_filtration) · [PrinterCapabilities](reference/bpm/bambuconfig.md#bpm.bambuconfig.PrinterCapabilities) |
| [tray_weight](#tray_weight) | BambuSpool | Current spool weight | [Field Definition](#tray_weight) · [BambuSpool](reference/bpm/bambuspool.md#bpm.bambuspool.BambuSpool) |
| [has_ams](#has_ams) | PrinterCapabilities | Indicates an active AMS unit is detected on the hardware bus via the `ams` block | [Field Definition](#has_ams) · [PrinterCapabilities](reference/bpm/bambuconfig.md#bpm.bambuconfig.PrinterCapabilities) |
| [type](#type) | BambuSpool | Filament material type | [Field Definition](#type) · [BambuSpool](reference/bpm/bambuspool.md#bpm.bambuspool.BambuSpool) |
| [has_camera](#has_camera) | PrinterCapabilities | Verified availability of the onboard AI camera module | [Field Definition](#has_camera) · [PrinterCapabilities](reference/bpm/bambuconfig.md#bpm.bambuconfig.PrinterCapabilities) |
| [has_chamber_door_sensor](#has_chamber_door_sensor) | PrinterCapabilities | Verification that the front glass enclosure is equipped with a hall-effect sensor | [Field Definition](#has_chamber_door_sensor) · [PrinterCapabilities](reference/bpm/bambuconfig.md#bpm.bambuconfig.PrinterCapabilities) |
| [verbose](#verbose) | BambuConfig | Provides an additional log level for dumping all messages | [Field Definition](#verbose) · [BambuConfig](reference/bpm/bambuconfig.md#bpm.bambuconfig.BambuConfig) |
| [has_chamber_temp](#has_chamber_temp) | PrinterCapabilities | Confirmed presence of the Chamber Thermal Controller (CTC) ambient sensor | [Field Definition](#has_chamber_temp) · [PrinterCapabilities](reference/bpm/bambuconfig.md#bpm.bambuconfig.PrinterCapabilities) |
| [has_dual_extruder](#has_dual_extruder) | PrinterCapabilities | Identifies the H2D dual-path architecture where independent hotend monitoring is required | [Field Definition](#has_dual_extruder) · [PrinterCapabilities](reference/bpm/bambuconfig.md#bpm.bambuconfig.PrinterCapabilities) |
| [watchdog_timeout](#watchdog_timeout) | BambuConfig | Duration before a connection is flagged as stale | [Field Definition](#watchdog_timeout) · [BambuConfig](reference/bpm/bambuconfig.md#bpm.bambuconfig.BambuConfig) |
| [has_lidar](#has_lidar) | PrinterCapabilities | Confirmed presence of the Micro LiDAR sensor based on `xcam` telemetry existence | [Field Definition](#has_lidar) · [PrinterCapabilities](reference/bpm/bambuconfig.md#bpm.bambuconfig.PrinterCapabilities) |
| [wifi_signal_strength](#wifi_signal_strength) | BambuState | Wi-Fi signal strength indicator | [Field Definition](#wifi_signal_strength) · [BambuState](reference/bpm/bambustate.md#bpm.bambustate.BambuState) |
| [heatbreak_fan_speed_percent](#heatbreak_fan_speed_percent) | BambuClimate | Heatbreak cooling fan speed | [Field Definition](#heatbreak_fan_speed_percent) · [BambuClimate](reference/bpm/bambustate.md#bpm.bambustate.BambuClimate) |
| [heater_state](#heater_state) | AMSUnitState | AMS drying/heater operational state | [Field Definition](#heater_state) · [AMSUnitState](reference/bpm/bambustate.md#bpm.bambustate.AMSUnitState) |
| [zone_aux_percent](#zone_aux_percent) | BambuClimate | Auxiliary fan zone control | [Field Definition](#zone_aux_percent) · [BambuClimate](reference/bpm/bambustate.md#bpm.bambustate.BambuClimate) |
| [hms_errors](#hms_errors) | BambuState | List of active HMS errors | [Field Definition](#hms_errors) · [BambuState](reference/bpm/bambustate.md#bpm.bambustate.BambuState) |
| [zone_exhaust_percent](#zone_exhaust_percent) | BambuClimate | Exhaust fan zone control | [Field Definition](#zone_exhaust_percent) · [BambuClimate](reference/bpm/bambustate.md#bpm.bambustate.BambuClimate) |
| [hostname](#hostname) | BambuConfig | IP address or DNS name of the printer on the local subnet | [Field Definition](#hostname) · [BambuConfig](reference/bpm/bambuconfig.md#bpm.bambuconfig.BambuConfig) |
| [zone_intake_open](#zone_intake_open) | BambuClimate | Heater intake damper state | [Field Definition](#zone_intake_open) · [BambuClimate](reference/bpm/bambustate.md#bpm.bambustate.BambuClimate) |
| [humidity_index](#humidity_index) | AMSUnitState | Humidity level index | [Field Definition](#humidity_index) · [AMSUnitState](reference/bpm/bambustate.md#bpm.bambustate.AMSUnitState) |
| [zone_part_fan_percent](#zone_part_fan_percent) | BambuClimate | Internal part fan zone control | [Field Definition](#zone_part_fan_percent) · [BambuClimate](reference/bpm/bambustate.md#bpm.bambustate.BambuClimate) |
| [humidity_raw](#humidity_raw) | AMSUnitState | Raw humidity percentage | [Field Definition](#humidity_raw) · [AMSUnitState](reference/bpm/bambustate.md#bpm.bambustate.AMSUnitState) |
| [zone_top_vent_open](#zone_top_vent_open) | BambuClimate | Top vent open state (derived) | [Field Definition](#zone_top_vent_open) · [BambuClimate](reference/bpm/bambustate.md#bpm.bambustate.BambuClimate) |
| [id](#id) | ExtruderState, AMSUnitState, BambuSpool, ProjectInfo | The unique identifier for this project (3MF storage location) | [Field Definition](#id) · [ExtruderState](reference/bpm/bambustate.md#bpm.bambustate.ExtruderState), [AMSUnitState](reference/bpm/bambustate.md#bpm.bambustate.AMSUnitState), [BambuSpool](reference/bpm/bambuspool.md#bpm.bambuspool.BambuSpool), [ProjectInfo](reference/bpm/bambuproject.md#bpm.bambuproject.ProjectInfo) |
| [ams](#ams) | BambuState (raw print field) | AMS aggregate payload root used for AMS unit parsing and spool reconstruction | [Field Definition](#ams) · [BambuState](reference/bpm/bambustate.md#bpm.bambustate.BambuState) |
| [mc_percent](#mc_percent) | BambuState (raw print field) | Raw print completion percentage from firmware | [Field Definition](#mc_percent) · [BambuState](reference/bpm/bambustate.md#bpm.bambustate.BambuState) |
| [ams_rfid_status](#ams_rfid_status) | BambuState (raw print field) | Raw AMS RFID subsystem status code | [Field Definition](#ams_rfid_status) · [BambuState](reference/bpm/bambustate.md#bpm.bambustate.BambuState) |
| [mc_remaining_time](#mc_remaining_time) | BambuState (raw print field) | Raw remaining-time estimate from firmware | [Field Definition](#mc_remaining_time) · [BambuState](reference/bpm/bambustate.md#bpm.bambustate.BambuState) |
| [cooling_fan_speed](#cooling_fan_speed) | BambuState (raw print field) | Raw part-cooling fan signal used by fallback fan mapping logic | [Field Definition](#cooling_fan_speed) · [BambuState](reference/bpm/bambustate.md#bpm.bambustate.BambuState) |
| [net](#net) | BambuState (raw print field) | Raw network configuration/status block | [Field Definition](#net) · [BambuState](reference/bpm/bambustate.md#bpm.bambustate.BambuState) |
| [device](#device) | BambuState (raw print field) | Device subsystem container for dual-extruder, CTC, and airduct telemetry blocks | [Field Definition](#device) · [BambuState](reference/bpm/bambustate.md#bpm.bambustate.BambuState) |
| [device_airduct](#device_airduct) | BambuState (raw print field) | Airduct/HVAC payload used for mode and per-zone actuator state | [Field Definition](#device_airduct) · [BambuState](reference/bpm/bambustate.md#bpm.bambustate.BambuState) |
| [device_ctc](#device_ctc) | BambuState (raw print field) | Chamber Thermal Controller payload used for chamber current/target temperatures | [Field Definition](#device_ctc) · [BambuState](reference/bpm/bambustate.md#bpm.bambustate.BambuState) |
| [device_extruder](#device_extruder) | BambuState (raw print field) | Multi-extruder status block with active tool and per-extruder telemetry list | [Field Definition](#device_extruder) · [BambuState](reference/bpm/bambustate.md#bpm.bambustate.BambuState) |
| [fail_reason](#fail_reason) | BambuState (raw print field) | Raw firmware failure reason code/string | [Field Definition](#fail_reason) · [BambuState](reference/bpm/bambustate.md#bpm.bambustate.BambuState) |
| [online](#online) | BambuState (raw print field) | Raw subsystem online/offline status block (e.g. `ahb`, `rfid`, `version`) | [Field Definition](#online) · [BambuState](reference/bpm/bambustate.md#bpm.bambustate.BambuState) |
| [fan_gear](#fan_gear) | BambuState (raw print field) | Firmware fan profile/gear indicator for diagnostics and UI parity | [Field Definition](#fan_gear) · [BambuState](reference/bpm/bambustate.md#bpm.bambustate.BambuState) |
| [upgrade_state](#upgrade_state) | BambuState (raw print field) | Firmware upgrade state block including status/progress and module details | [Field Definition](#upgrade_state) · [BambuState](reference/bpm/bambustate.md#bpm.bambustate.BambuState) |
| [force_upgrade](#force_upgrade) | BambuState (raw print field) | Indicates forced-upgrade requirement state from firmware | [Field Definition](#force_upgrade) · [BambuState](reference/bpm/bambustate.md#bpm.bambustate.BambuState) |
| [upload](#upload) | BambuState (raw print field) | Raw file upload status block including progress and status text | [Field Definition](#upload) · [BambuState](reference/bpm/bambustate.md#bpm.bambustate.BambuState) |
| [home_flag](#home_flag) | BambuState (raw print field) | Packed option bitfield for device behavior toggles | [Field Definition](#home_flag) · [BambuState](reference/bpm/bambustate.md#bpm.bambustate.BambuState) |
| [vir_slot](#vir_slot) | BambuState (raw print field) | Virtual external tray entries (typically IDs `254`/`255`) used to construct spool entries | [Field Definition](#vir_slot) · [BambuState](reference/bpm/bambustate.md#bpm.bambustate.BambuState) |
| [ipcam](#ipcam) | BambuState (raw print field) | Camera service/configuration block (recording, mode bits, stream capabilities) | [Field Definition](#ipcam) · [BambuState](reference/bpm/bambustate.md#bpm.bambustate.BambuState) |
| [vt_tray](#vt_tray) | BambuState (raw print field) | External/manual tray payload block used to construct spool entries | [Field Definition](#vt_tray) · [BambuState](reference/bpm/bambustate.md#bpm.bambustate.BambuState) |
| [lights_report](#lights_report) | BambuState (raw print field) | Light status report entries (for example chamber light mode) | [Field Definition](#lights_report) · [BambuState](reference/bpm/bambustate.md#bpm.bambustate.BambuState) |
| [xcam](#xcam) | BambuState (raw print field) | AI camera/inspection status and feature flags | [Field Definition](#xcam) · [BambuState](reference/bpm/bambustate.md#bpm.bambustate.BambuState) |
| [stg](#stg) | BambuState (raw print field) | Firmware stage sequence/state vector | [Field Definition](#stg) · [BambuState](reference/bpm/bambustate.md#bpm.bambustate.BambuState) |
| [s_obj](#s_obj) | BambuState (raw print field) | Skipped-object payload list consumed by runtime skipped-object cache | [Field Definition](#s_obj) · [BambuState](reference/bpm/bambustate.md#bpm.bambustate.BambuState) |
| [filam_bak](#filam_bak) | BambuState (raw print field) | Firmware filament backup/alternate list block | [Field Definition](#filam_bak) · [BambuState](reference/bpm/bambustate.md#bpm.bambustate.BambuState) |

---

## BambuConfig

Main configuration class for [`BambuPrinter`](reference/bpm/bambuprinter.md#bpm.bambuprinter.BambuPrinter) containing connection parameters, behavioral settings, and hardware capabilities.

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
- **Purpose**: Master switch for AMS tension-based filament tangle monitor logic. Only meaningful when an AMS unit is present and actively feeding — has no effect during external spool or standalone prints.
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
- **Purpose**: Enables automatic AMS failover when the active spool runs out, switching to another AMS slot loaded with the **same filament type AND color**. Both conditions (type and color) must match. Applies to AMS-hosted spools only — the external spool holder is not eligible.
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
- **Purpose**: Enablement for spool-weight based estimation of remaining filament length. Requires an AMS unit with built-in weight sensors. **AMS 2 Pro only** — AMS Lite and AMS HT do not have weight sensors and will not respond to this setting.
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
- **Override**: Can be ignored if [`BambuConfig.external_chamber`](reference/bpm/bambuconfig.md#bpm.bambuconfig.BambuConfig.external_chamber) is True

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
- **MQTT Structure**: [MQTT Protocol Reference](mqtt-protocol-reference.md)

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
- **Telemetry**:
  - Single-extruder (X1/P1/A1): Computed from `active_tray_id >> 2`
  - Multi-extruder (H2D): `a_ext.assigned_to_ams_id` (physical AMS port assigned to the active extruder)
- **Valid Range**: `-1` (no AMS), `0-3` (standard AMS), `128-131` (AMS HT)
- **Purpose**: Currently active AMS unit ID
- **Reference**: AMS slot addressing scheme

#### active_tray_id
- **Type**: `int`
- **Telemetry**:
  - Multi-extruder (H2D): Computed via `parseExtruderTrayState` from extruder info
  - Single-extruder (X1/P1/A1): `print.ams.tray_now`; value `255` normalized to `-1`
- **Valid Range**:
  - `0-15`: Standard AMS slots (4 trays × 4 units)
  - `254-255`: External spool
  - `-1`: No tray
- **Purpose**: Current filament tray identifier
- **Reference**: BambuStudio tray indexing
- **MQTT Structure**: [MQTT Protocol Reference](mqtt-protocol-reference.md)

#### active_tray_state
- **Type**: `TrayState` (IntEnum)
- **Telemetry**:
  - Multi-extruder (H2D): Computed from extruder info/status
  - Single-extruder (X1/P1/A1): Computed from `stage_id` — stage 24 → `LOADING`, stage 22 → `UNLOADING`, valid tray → `LOADED`, no tray → `UNLOADED`
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
- **Telemetry**: `print.ams.tray_tar`; value `255` normalized to `-1`
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
- **MQTT Structure**: [MQTT Protocol Reference](mqtt-protocol-reference.md)

#### active_nozzle_temp_target
- **Type**: `int`
- **Telemetry**: `print.nozzle_target_temper` or extruder target
- **Unit**: °C
- **Purpose**: Target nozzle temperature
- **Reference**: BambuStudio thermal control
- **MQTT Control**: [Set Nozzle Temperature Target](mqtt-protocol-reference.md#set-nozzle-temperature-target)
- **MQTT Structure**: [MQTT Protocol Reference](mqtt-protocol-reference.md)

### AMS Status Attributes

#### ams_status_raw
- **Type**: `int`
- **Telemetry**: `print.ams_status`
- **Purpose**: Raw AMS status bitmask
- **Reference**: BambuStudio AMS status codes
- **MQTT Structure**: [MQTT Protocol Reference](mqtt-protocol-reference.md)

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
- **MQTT Structure**: [MQTT Protocol Reference](mqtt-protocol-reference.md)

#### hms_errors
- **Type**: `list[dict]`
- **Telemetry**: `print.hms` + decoded `print_error`
- **Structure**: Each error contains `code`, `msg`, `module`, `severity`, `is_critical`, `type`, `url`
- **Schema** (`print.hms[]`):

| Field | Type | Description |
| ----- | ---- | ----------- |
| `attr` | int | [Raw HMS attribute/status payload from firmware](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambustate.py#L589) |
| `code` | int | [HMS event/error code](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambustate.py#L589) |
| `action` | int | [Firmware action indicator for the HMS event](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambustate.py#L589) |
| `timestamp` | int | [Event timestamp (epoch seconds)](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L1914) |
- **Purpose**: List of active HMS errors
- **Reference**: BambuStudio HMS system, ha-bambulab error decoding
- **MQTT Structure**: [MQTT Protocol Reference](mqtt-protocol-reference.md)

### Network Attributes

#### wifi_signal_strength
- **Type**: `str`
- **Telemetry**: `print.wifi_signal`
- **Unit**: dBm
- **Purpose**: Wi-Fi signal strength indicator
- **Reference**: BambuStudio network monitoring
- **MQTT Structure**: [MQTT Protocol Reference](mqtt-protocol-reference.md)

### Top-Level MQTT Fields (Raw)

These fields appear in `print.push_status` payloads and are consumed directly,
mapped into other attributes, or used as runtime control/diagnostic inputs.

#### ams
- **Type**: `dict`
- **Telemetry**: `print.ams`
- **Purpose**: AMS aggregate payload root used for AMS unit parsing and spool reconstruction
- **Mapped To**: [ams_units](#ams_units), [ams_exist_bits](#ams_exist_bits), [active_tray_id](#active_tray_id), [spools](#spools)
- **Schema**:

| Field | Type | Description |
| ----- | ---- | ----------- |
| `ams` | list[dict] | [AMS unit list (`print.ams.ams[]`)](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambustate.py#L220) |
| `ams_exist_bits` | string \| int | [Connected AMS bitmask](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambustate.py#L526) |
| `tray_exist_bits` | string \| int | [Per-slot tray presence bitmask](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambustate.py#L455) |
| `tray_is_bbl_bits` | string \| int | [Bambu tray bitmask](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambustate.py#L220) |
| `tray_tar` | string \| int | [Target tray identifier](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambustate.py#L220) |
| `tray_now` | string \| int | [Active tray identifier](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambustate.py#L500) |
| `tray_pre` | string \| int | [Previous tray identifier](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambustate.py#L220) |
| `tray_read_done_bits` | string \| int | [Tray-read completion bitmask](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambustate.py#L220) |
| `tray_reading_bits` | string \| int | [Tray-read in-progress bitmask](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambustate.py#L220) |
| `version` | int | [AMS payload version marker](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambustate.py#L220) |
| `insert_flag` | bool | [Tray insertion behavior flag](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L1714) |
| `power_on_flag` | bool | [Startup tray-read behavior flag](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L1712) |
- **`ams[]` Schema**:

| Field | Type | Description |
| ----- | ---- | ----------- |
| `id` | string \| int | [AMS unit identifier](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambustate.py#L423) |
| `chip_id` | string | [AMS hardware serial](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambustate.py#L418) |
| `check` | int | [AMS check/status code](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambustate.py#L422) |
| `humidity` | string \| int | [Humidity index](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambustate.py#L426) |
| `humidity_raw` | string \| int | [Raw humidity value](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambustate.py#L427) |
| `temp` | string \| float | [AMS temperature](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambustate.py#L218) |
| `dry_time` | int | [Remaining dry time (minutes)](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambustate.py#L428) |
| `info` | string | [AMS info bitfield (hex string)](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambustate.py#L208) |
| `tray` | list[dict] | [Tray list for this AMS unit](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L1717) |
- **`ams[].tray[]` Schema**:

| Field | Type | Description |
| ----- | ---- | ----------- |
| `id` | string | [Slot ID](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L1726) |
| `state` | int | [Tray state code](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L1746) |
| `remain` | int | [Remaining filament estimate](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L1745) |
| `k` | float | [K-factor used for flow tuning](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L1739) |
| `n` | int | [N coefficient paired with K-factor](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L1717) |
| `cali_idx` | int | [Selected calibration profile index](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L1281) |
| `total_len` | int | [Total filament length](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L1747) |
| `tag_uid` | string | [RFID tag UID](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L1717) |
| `tray_id_name` | string | [Human-readable/user tray name](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L1004) |
| `tray_info_idx` | string | [Filament preset index](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L1002) |
| `tray_type` | string | [Filament material/type](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L1005) |
| `tray_sub_brands` | string | [Filament sub-brand/family](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L1736) |
| `tray_color` | string | [Filament color code](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L1013) |
| `tray_weight` | string | [Tray/spool weight metadata](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L1748) |
| `tray_diameter` | string | [Filament diameter metadata](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L1717) |
| `tray_temp` | string | [Tray-level temperature metadata](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L1717) |
| `tray_time` | string | [Tray-level time metadata](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L1717) |
| `bed_temp_type` | string | [Bed temperature profile type selector](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L1717) |
| `bed_temp` | string | [Recommended bed temperature](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L957) |
| `nozzle_temp_min` | string | [Recommended minimum nozzle temperature](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L1015) |
| `nozzle_temp_max` | string | [Recommended maximum nozzle temperature](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L1016) |
| `xcam_info` | string | [Camera/inspection metadata blob](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L1717) |
| `tray_uuid` | string | [Tray UUID](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L1717) |
| `ctype` | int | [Color type indicator](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L1717) |
| `cols` | list[string] | [Additional color palette values](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L1717) |

#### device
- **Type**: `dict`
- **Telemetry**: `print.device`
- **Purpose**: Device subsystem container for dual-extruder, CTC, and airduct telemetry blocks
- **Mapped To**: [extruders](#extruders), [active_tool](#active_tool), [chamber_temp](#chamber_temp), [chamber_temp_target](#chamber_temp_target), [airduct_mode](#airduct_mode), [airduct_sub_mode](#airduct_sub_mode)
- **Schema**:

| Field | Type | Description |
| ----- | ---- | ----------- |
| `extruder` | dict | [Extruder subsystem block (`print.device.extruder`)](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambustate.py#L223) |
| `ctc` | dict | [Chamber thermal controller block (`print.device.ctc`)](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambustate.py#L224) |
| `airduct` | dict | [Airduct subsystem block (`print.device.airduct`)](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambustate.py#L225) |

#### device_extruder
- **Type**: `dict`
- **Telemetry**: `print.device.extruder`
- **Purpose**: Multi-extruder status block with active tool and per-extruder telemetry list
- **Mapped To**: [extruders](#extruders), [active_tool](#active_tool)
- **Schema**:

| Field | Type | Description |
| ----- | ---- | ----------- |
| `state` | int | [Active extruder/tool selector bitfield](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambustate.py#L399) |
| `info` | list[dict] | [Per-extruder telemetry list (`print.device.extruder.info[]`)](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambustate.py#L208) |

#### device_ctc
- **Type**: `dict`
- **Telemetry**: `print.device.ctc`
- **Purpose**: Chamber Thermal Controller payload used for chamber current/target temperatures
- **Mapped To**: [chamber_temp](#chamber_temp), [chamber_temp_target](#chamber_temp_target)
- **Schema**:

| Field | Type | Description |
| ----- | ---- | ----------- |
| `info` | dict | [CTC data container](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambustate.py#L208) |
| `info.temp` | int \| float | [Packed current/target chamber temperature value parsed by [`unpackTemperature()`](reference/bpm/bambutools.md#bpm.bambutools.unpackTemperature)](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambustate.py#L208) |

#### device_airduct
- **Type**: `dict`
- **Telemetry**: `print.device.airduct`
- **Purpose**: Airduct/HVAC payload used for mode and per-zone actuator state
- **Mapped To**: [airduct_mode](#airduct_mode), [airduct_sub_mode](#airduct_sub_mode), [zone_part_fan_percent](#zone_part_fan_percent), [zone_aux_percent](#zone_aux_percent), [zone_exhaust_percent](#zone_exhaust_percent), [zone_intake_open](#zone_intake_open), [zone_top_vent_open](#zone_top_vent_open)
- **Schema**:

| Field | Type | Description |
| ----- | ---- | ----------- |
| `modeCur` | int | [Current airduct mode](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambustate.py#L272) |
| `subMode` | int | [Current airduct sub-mode](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambustate.py#L275) |
| `parts` | list[dict] | [Per-zone actuator state list](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambustate.py#L288) |
| `parts[].id` | int | [Zone/actuator identifier (`16`, `32`, `48`, `96`)](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambustate.py#L288) |
| `parts[].state` | int | [Zone actuator value](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambustate.py#L288) |

#### mc_percent
- **Type**: `int`
- **Telemetry**: `print.mc_percent`
- **Purpose**: Raw print completion percentage from firmware
- **Mapped To**: [print_percentage](#print_percentage)

#### mc_remaining_time
- **Type**: `int`
- **Telemetry**: `print.mc_remaining_time`
- **Unit**: minutes
- **Purpose**: Raw remaining-time estimate from firmware
- **Mapped To**: [remaining_minutes](#remaining_minutes)

#### cooling_fan_speed
- **Type**: `str | int`
- **Telemetry**: `print.cooling_fan_speed`
- **Purpose**: Raw part-cooling fan signal used by fallback fan mapping logic
- **Mapped To**: [part_cooling_fan_speed_percent](#part_cooling_fan_speed_percent)

#### fan_gear
- **Type**: `int`
- **Telemetry**: `print.fan_gear`
- **Purpose**: Firmware fan profile/gear indicator for diagnostics and UI parity

#### stg
- **Type**: `list[int]`
- **Telemetry**: `print.stg`
- **Purpose**: Firmware stage sequence/state vector

#### s_obj
- **Type**: `list[Any]`
- **Telemetry**: `print.s_obj`
- **Purpose**: Skipped-object payload list consumed by runtime skipped-object cache

#### filam_bak
- **Type**: `list[Any]`
- **Telemetry**: `print.filam_bak`
- **Purpose**: Firmware filament backup/alternate list block

#### ams_rfid_status
- **Type**: `int`
- **Telemetry**: `print.ams_rfid_status`
- **Purpose**: Raw AMS RFID subsystem status code

#### vt_tray
- **Type**: `dict`
- **Telemetry**: `print.vt_tray`
- **Purpose**: External/manual tray payload block used to construct spool entries
- **Mapped To**: [spools](#spools)
- **Schema**:

| Field | Type | Description |
| ----- | ---- | ----------- |
| `id` | string | [External tray identifier (typically `254`/`255`)](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L1767) |
| `state` | int | [Tray state code](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L1780) |
| `remain` | int | [Remaining filament estimate](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L1745) |
| `k` | float | [K-factor used for flow tuning](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L1739) |
| `n` | int | [N coefficient paired with K-factor](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L1757) |
| `cali_idx` | int | [Selected calibration profile index](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L1281) |
| `tag_uid` | string | [RFID tag UID](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L1757) |
| `tray_id_name` | string | [Human-readable/user tray name](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L1004) |
| `tray_info_idx` | string | [Filament preset index](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L1002) |
| `tray_type` | string | [Filament material/type](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L1005) |
| `tray_sub_brands` | string | [Filament sub-brand/family](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L1736) |
| `tray_color` | string | [Filament color code](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L1013) |
| `tray_weight` | string | [Tray/spool weight metadata](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L1748) |
| `tray_diameter` | string | [Filament diameter metadata](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L1757) |
| `tray_temp` | string | [Tray-level temperature metadata](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L1757) |
| `tray_time` | string | [Tray-level time metadata](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L1757) |
| `bed_temp_type` | string | [Bed temperature profile type selector](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L1757) |
| `bed_temp` | string | [Recommended bed temperature](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L957) |
| `nozzle_temp_min` | string | [Recommended minimum nozzle temperature](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L1015) |
| `nozzle_temp_max` | string | [Recommended maximum nozzle temperature](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L1016) |
| `xcam_info` | string | [Camera/inspection metadata blob](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L1757) |
| `tray_uuid` | string | [Tray UUID](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L1757) |

#### vir_slot
- **Type**: `list[dict]`
- **Telemetry**: `print.vir_slot[]`
- **Purpose**: Virtual external tray entries (typically IDs `254`/`255`) used to construct spool entries
- **Mapped To**: [spools](#spools)
- **Schema**:

| Field | Type | Description |
| ----- | ---- | ----------- |
| `id` | string | [Virtual tray identifier (typically `254` or `255`)](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L1804) |
| `state` | int | [Tray state code](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L1826) |
| `remain` | int | [Remaining filament estimate](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L1745) |
| `k` | float | [K-factor used for flow tuning](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L1739) |
| `n` | int | [N coefficient paired with K-factor](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L1798) |
| `cali_idx` | int | [Selected calibration profile index](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L1281) |
| `total_len` | int | [Total filament length for this tray profile](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L1747) |
| `tag_uid` | string | [RFID tag UID](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L1798) |
| `tray_id_name` | string | [Human-readable/user tray name](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L1004) |
| `tray_info_idx` | string | [Filament preset index](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L1002) |
| `tray_type` | string | [Filament material/type](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L1005) |
| `tray_sub_brands` | string | [Filament sub-brand/family](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L1736) |
| `tray_color` | string | [Filament color code](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L1013) |
| `tray_weight` | string | [Tray/spool weight metadata](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L1748) |
| `tray_diameter` | string | [Filament diameter metadata](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L1798) |
| `tray_temp` | string | [Tray-level temperature metadata](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L1798) |
| `tray_time` | string | [Tray-level time metadata](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L1798) |
| `bed_temp_type` | string | [Bed temperature profile type selector](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L1798) |
| `bed_temp` | string | [Recommended bed temperature](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L957) |
| `nozzle_temp_min` | string | [Recommended minimum nozzle temperature](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L1015) |
| `nozzle_temp_max` | string | [Recommended maximum nozzle temperature](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L1016) |
| `xcam_info` | string | [Camera/inspection metadata blob](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L1798) |
| `tray_uuid` | string | [Tray UUID](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L1798) |
| `ctype` | int | [Color type indicator](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L1798) |
| `cols` | list[string] | [Additional color palette values](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L1798) |

#### fail_reason
- **Type**: `str | int`
- **Telemetry**: `print.fail_reason`
- **Purpose**: Raw firmware failure reason code/string

#### home_flag
- **Type**: `int`
- **Telemetry**: `print.home_flag`
- **Purpose**: Packed option bitfield for device behavior toggles
- **Mapped To**: [sound_enable](#sound_enable), [auto_recovery](#auto_recovery), [auto_switch_filament](#auto_switch_filament), [filament_tangle_detect](#filament_tangle_detect), [calibrate_remain_flag](#calibrate_remain_flag)

#### online
- **Type**: `dict`
- **Telemetry**: `print.online`
- **Purpose**: Raw subsystem online/offline status block (e.g. `ahb`, `rfid`, `version`)
- **Schema**:

| Field | Type | Description |
| ----- | ---- | ----------- |
| `ahb` | bool | [Online state for `ahb` subsystem](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambustate.py#L200) |
| `rfid` | bool | [Online state for RFID subsystem](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambustate.py#L200) |
| `version` | int | [Online payload version/revision marker](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambustate.py#L200) |

#### upgrade_state
- **Type**: `dict`
- **Telemetry**: `print.upgrade_state`
- **Purpose**: Firmware upgrade state block including status/progress and module details
- **Schema**:

| Field | Type | Description |
| ----- | ---- | ----------- |
| `sequence_id` | string \| int | [Upgrade event sequence identifier](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambustate.py#L200) |
| `progress` | string \| int | [Upgrade progress value](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambustate.py#L200) |
| `status` | string | [Upgrade state label](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambustate.py#L200) |
| `consistency_request` | bool | [Consistency-check request flag](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambustate.py#L200) |
| `dis_state` | int | [Device/dispatcher state code](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambustate.py#L200) |
| `err_code` | int | [Upgrade error code](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambustate.py#L200) |
| `force_upgrade` | bool | [Forced-upgrade requirement flag](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambustate.py#L200) |
| `message` | string | [Upgrade status/error message](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambustate.py#L200) |
| `module` | string | [Active module target label](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambustate.py#L227) |
| `new_version_state` | int | [New-version availability state](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambustate.py#L200) |
| `cur_state_code` | int | [Current upgrade state code](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambustate.py#L200) |
| `idx2` | int | [Firmware-provided opaque index/value](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambustate.py#L200) |
| `new_ver_list` | list[Any] | [Firmware-provided version list](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambustate.py#L200) |
| `mc_for_ams_firmware` | dict | [AMS firmware grouping block](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambustate.py#L200) |
| `mc_for_ams_firmware.current_run_firmware_id` | int | [Current running AMS firmware target ID](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambustate.py#L200) |
| `mc_for_ams_firmware.current_firmware_id` | int | [Current AMS firmware ID](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambustate.py#L200) |
| `mc_for_ams_firmware.status` | string | [AMS firmware upgrade state label](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambustate.py#L200) |
| `mc_for_ams_firmware.firmware` | list[dict] | [AMS firmware target list](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambustate.py#L200) |

  | `mc_for_ams_firmware.firmware[]` Field | Type | Description |
  |-----------------------------------------|------|-------------|
  | `id` | int | Firmware target identifier |
  | `name` | string | Firmware target display name |

#### force_upgrade
- **Type**: `bool`
- **Telemetry**: `print.force_upgrade`
- **Purpose**: Indicates forced-upgrade requirement state from firmware

#### ipcam
- **Type**: `dict`
- **Telemetry**: `print.ipcam`
- **Purpose**: Camera service/configuration block (recording, mode bits, stream capabilities)
- **Schema**:

| Field | Type | Description |
| ----- | ---- | ----------- |
| `ipcam_dev` | string | [Camera device enabled/disabled flag](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambustate.py#L200) |
| `ipcam_record` | string | [Recording mode](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambustate.py#L200) |
| `timelapse` | string | [Timelapse mode](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L637) |
| `resolution` | string | [Stream/recording resolution](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambustate.py#L200) |
| `tutk_server` | string | [TUTK relay mode](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambustate.py#L200) |
| `mode_bits` | int | [Camera capability/mode bitfield](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambustate.py#L200) |

#### lights_report
- **Type**: `list[dict]`
- **Telemetry**: `print.lights_report`
- **Purpose**: Light status report entries (for example chamber light mode)
- **Schema**:

| Field | Type | Description |
| ----- | ---- | ----------- |
| `node` | string | [Light node identifier (for example `chamber_light`)](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambustate.py#L200) |
| `mode` | string | [Current node mode/state (for example `on`/`off`)](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L1132) |

#### xcam
- **Type**: `dict`
- **Telemetry**: `print.xcam`
- **Purpose**: AI camera/inspection status and feature flags
- **Schema**:

| Field | Type | Description |
| ----- | ---- | ----------- |
| `buildplate_marker_detector` | bool | [Buildplate marker detector state](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L1855) |
| `first_layer_inspector` | bool | [First-layer inspector/lidar capability state](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambustate.py#L247) |

#### net
- **Type**: `dict`
- **Telemetry**: `print.net`
- **Purpose**: Raw network configuration/status block
- **Schema**:

| Field | Type | Description |
| ----- | ---- | ----------- |
| `conf` | int | [Network configuration/status code](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambustate.py#L200) |
| `info` | list[dict] | [Interface/address info list](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambustate.py#L208) |

  | `info[]` Field | Type | Description |
  |----------------|------|-------------|
  | `ip` | int | IPv4 address value (integer encoded) |
  | `mask` | int | IPv4 subnet mask value (integer encoded) |

#### upload
- **Type**: `dict`
- **Telemetry**: `print.upload`
- **Purpose**: Raw file upload status block including progress and status text
- **Schema**:

| Field | Type | Description |
| ----- | ---- | ----------- |
| `status` | string | [Upload status/state text](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambustate.py#L200) |
| `progress` | int | [Upload progress value](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambustate.py#L200) |
| `message` | string | [Upload status/error message](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambustate.py#L200) |

### Collections

#### ams_units
- **Type**: `list[AMSUnitState]`
- **Telemetry**: `print.ams.ams[]` + `info.module[]`
- **Purpose**: Complete state of all connected AMS units
- **Reference**: See [AMSUnitState](#amsunitstate) section
- **MQTT Structure**: [MQTT Protocol Reference](mqtt-protocol-reference.md)

#### extruders
- **Type**: `list[ExtruderState]`
- **Telemetry**: `print.device.extruder.info[]`
- **Purpose**: State of all physical extruders
- **Reference**: See [ExtruderState](#extruderstate) section

#### spools
- **Type**: `list[BambuSpool]`
- **Telemetry**: Aggregated from AMS trays and external spools
- **Purpose**: All filament spools with properties
- **Reference**: See [BambuSpool](#bambuspool) section / [Code Reference](reference/bpm/bambuspool.md#bpm.bambuspool.BambuSpool)
- **MQTT Structure**: [MQTT Protocol Reference](mqtt-protocol-reference.md)

#### climate
- **Type**: [`BambuClimate`](reference/bpm/bambustate.md#bpm.bambustate.BambuClimate)
- **Telemetry**: Multiple sources (see BambuClimate section)
- **Purpose**: All temperature, fan, and environmental data
- **Reference**: See [BambuClimate](#bambuclimate) section / [Code Reference](reference/bpm/bambustate.md#bpm.bambustate.BambuClimate)

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
- **Telemetry**: `extruder.info[].temp` (unpacked via [`unpackTemperature()`](reference/bpm/bambutools.md#bpm.bambutools.unpackTemperature))
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
- **Telemetry**:
  - Multi-extruder (H2D): Computed from `extruder.info[].hnow`, `extruder.info[].snow`
  - Single-extruder (id == SINGLE_EXTRUDER): `print.ams.tray_now`
- **Valid Range**: `-1`, `0-15`, `254-255`
- **Purpose**: Currently active tray for this extruder
- **Reference**: BambuStudio tray tracking algorithm

#### target_tray_id
- **Type**: `int`
- **Telemetry**:
  - Multi-extruder (H2D): Computed from `extruder.info[].htar`, `extruder.info[].star`
  - Single-extruder (id == SINGLE_EXTRUDER): `print.ams.tray_tar`
- **Valid Range**: Same as `active_tray_id`
- **Purpose**: Target tray for this extruder
- **Reference**: BambuStudio tray targeting

#### tray_state
- **Type**: `TrayState` (IntEnum)
- **Telemetry**:
  - Multi-extruder (H2D): Computed from `state` + `status` combination
  - Single-extruder (id == SINGLE_EXTRUDER): Computed from `stage_id` — stage 24 → `LOADING`, stage 22 → `UNLOADING`, valid tray → `LOADED`, no tray → `UNLOADED`
- **Purpose**: Loading state for this extruder's tray
- **Reference**: State machine derived from BambuStudio

#### assigned_to_ams_id
- **Type**: `int`
- **Telemetry**:
  - Multi-extruder (H2D): Set when AMS unit reports H2D extruder assignment
  - Single-extruder: Computed as `active_tray_id >> 2` when a valid tray is loaded; `-1` when no tray (external spool or idle)
- **Valid Range**: `-1`, `0-3`, `128-131`
- **Purpose**: AMS unit assigned to this extruder
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
- **Reference**: BambuStudio fan control, scaled via [`scaleFanSpeed()`](reference/bpm/bambutools.md#bpm.bambutools.scaleFanSpeed) (0-15 → 0-100)

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
- **Content**: Extracted from 3MF files including:
  - Model information (map, bed_type, nozzle_diameter, layer_height) from `Metadata/plate_*.json`
  - Print settings and estimates (first_layer_time, is_seq_print) from `Metadata/plate_*.json`
  - Filament requirements and colors (filament array with color, id, type) from `Metadata/slice_info.config`
  - AMS mapping (ams_mapping array) from `Metadata/slice_info.config`
  - Object hierarchy with bounding boxes (bbox_objects array) populated from both sources
  - Thumbnail images (base64 encoded) from `Metadata/plate_*.png` and `Metadata/top_*.png`
- **Key Subfields**:
  - `map.bbox_objects` - Array of objects in the model; each object has `id` (from XML identify_id), `name`, `area`, `bbox`. Used with [Skip Objects During Print](mqtt-protocol-reference.md#skip-objects-during-print). The `id` values are extracted from `slice_info.config` identify_id and matched by array index.
  - `map.bed_type` - Type of print bed (e.g., "textured_plate")
  - `filament` - Array of filaments with `id` (1-indexed), `type`, `color`. Filament IDs are used to correlate with ams_mapping positions.
  - `ams_mapping` - Variable-length array where each position (0-indexed) corresponds to a filament id (1-indexed). Values are absolute tray IDs: 0-103 for standard 4-slot units (formula: ams_id * 4 + slot_id), 128-135 for single-slot units (N3S/AMS HT), -1 for unmapped filaments. Generated by slicer color-distance matching. Used by print_3mf_file to determine spool assignments.
- **AMS Mapping Correlation**:

  | Filament ID | Array Index | Example Value | Assignment |
  |-------------|-------------|---------------|------------|
  | 1 | `ams_mapping[0]` | `0` | AMS 0, slot 0 |
  | 2 | `ams_mapping[1]` | `-1` | Unmapped |

#### plates
- **Type**: `list[int]`
- **Default**: `[]`
- **Purpose**: The set of plate numbers discovered in the 3MF package
- **Valid Values**: Positive plate indices (typically `1..N`)
- **Usage**: Drives UI plate selection and validation for multi-plate projects
- **Reference**: Parsed from `Metadata/plate_*.gcode` and related metadata artifacts
  | 3 | `ams_mapping[2]` | `2` | AMS 0, slot 2 |
  | 4 | `ams_mapping[3]` | `-1` | Unmapped |
- **Extraction Details**:
  - `bbox_objects` structural data (name, area, bbox) from `Metadata/plate_*.json`
  - Object `id` field populated from `identify_id` attribute in `Metadata/slice_info.config` XML, matched by index
  - `filament` array extracted from `slice_info.config` filament elements, ordered as they appear in slicer
  - `ams_mapping` built from `filament_maps` metadata in `slice_info.config`, with filament id-based index assignment
- **Print Command Usage**: [print_3mf command implementation](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L535) uses `ams_mapping` to determine which AMS trays/spools to load for each slicer filament

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
- **Update**: Populated via [`get_project_info()`](reference/bpm/bambuproject.md#bpm.bambuproject.get_project_info) method
- **Note**: A fallback FTP lookup is attempted once when `gcode_state` transitions to `PREPARE` or `RUNNING`: searches the SD card 3MF file list by `subtask_name` and calls `get_project_info()`. Guarded by `project_info_fetch_attempted` to prevent repeated FTP calls on every MQTT push_status message.

#### project_info_fetch_attempted
- **Type**: `bool`
- **Default**: `False`
- **Purpose**: Guards the fallback `project_info` fetch so FTP is only attempted once per job, preventing repeated FTP calls on every MQTT push_status message while `project_info.id` is empty

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

### AMSControlCommand
**Source**: `src/bpm/bambutools.py`

| Value | Name | Description |
|-------|------|-------------|
| 0 | PAUSE | Pause AMS action |
| 1 | RESUME | Resume AMS action |
| 2 | RESET | Reset AMS subsystem state |

### AMSSeries
**Source**: `src/bpm/bambutools.py`

| Value | Name | Description |
|-------|------|-------------|
| 0 | UNKNOWN | Unknown AMS generation |
| 1 | GEN_1 | Gen 1 AMS family |
| 2 | GEN_2 | Gen 2 AMS family |

### AMSUserSetting
**Source**: `src/bpm/bambutools.py`

| Value | Name | Description |
|-------|------|-------------|
| 0 | CALIBRATE_REMAIN_FLAG | Toggle filament remaining calibration |
| 1 | STARTUP_READ_OPTION | Toggle startup tray read behavior |
| 2 | TRAY_READ_OPTION | Toggle tray insert read behavior |

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

### NozzleDiameter
**Source**: `src/bpm/bambutools.py`

| Value | Name | Description |
|-------|------|-------------|
| 0.0 | UNKNOWN | Unknown or unsupported nozzle diameter |
| 0.2 | POINT_TWO_MM | 0.2mm nozzle |
| 0.4 | POINT_FOUR_MM | 0.4mm nozzle |
| 0.6 | POINT_SIX_MM | 0.6mm nozzle |
| 0.8 | POINT_EIGHT_MM | 0.8mm nozzle |

### NozzleType
**Source**: `src/bpm/bambutools.py`

| Value | Name | Description |
|-------|------|-------------|
| 0 | UNKNOWN | Unknown nozzle type |
| 1 | STAINLESS_STEEL | Stainless steel nozzle |
| 2 | HARDENED_STEEL | Hardened steel nozzle |
| 3 | TUNGSTEN_CARBIDE | Tungsten carbide nozzle |
| 4 | BRASS | Brass nozzle |
| 5 | E3D | E3D nozzle |

### PlateType
**Source**: `src/bpm/bambutools.py`

| Value | Name | Description |
|-------|------|-------------|
| 0 | AUTO | Use slicer/printer default selection |
| 1 | COOL_PLATE | Cool plate |
| 2 | ENG_PLATE | Engineering plate |
| 3 | HOT_PLATE | Hot plate |
| 4 | TEXTURED_PLATE | Textured plate |
| 999 | NONE | No plate selected |

### PrinterModel
**Source**: `src/bpm/bambutools.py`

| Value | Name | Description |
|-------|------|-------------|
| 0 | UNKNOWN | Unknown printer model |
| 1 | X1C | X1 Carbon |
| 2 | X1 | X1 |
| 3 | X1E | X1E |
| 4 | P1P | P1P |
| 5 | P1S | P1S |
| 6 | A1_MINI | A1 Mini |
| 7 | A1 | A1 |
| 8 | P2S | P2S |
| 9 | H2S | H2S |
| 10 | H2D | H2D |

### PrinterSeries
**Source**: `src/bpm/bambutools.py`

| Value | Name | Description |
|-------|------|-------------|
| 0 | UNKNOWN | Unknown printer family |
| 1 | X1 | X1 family |
| 2 | P1 | P1 family |
| 3 | A1 | A1 family |
| 4 | P2 | P2 family |
| 5 | H2 | H2 family |

### PrintOption
**Source**: `src/bpm/bambutools.py`

| Value | Name | Description |
|-------|------|-------------|
| 0 | AUTO_RECOVERY | Resume print automatically after power loss or hardware fault. |
| 1 | FILAMENT_TANGLE_DETECT | Pause if AMS sensors detect a filament tangle. AMS-only; no effect on external spool prints. Guarded by `has_filament_tangle_detect_support`. |
| 2 | SOUND_ENABLE | Enable audible beep notifications for print events. Guarded by `has_sound_enable_support`. |
| 3 | AUTO_SWITCH_FILAMENT | Auto-switch to another AMS slot when the active spool runs out, if a slot with the same filament type AND color is available. AMS-hosted spools only. |
| 4 | NOZZLE_BLOB_DETECT | Legacy firmware-level (home_flag) nozzle blob detection. On supported printers, prefer `set_nozzleclumping_detector()` (xcam AI) which adds sensitivity control. Guarded by `has_nozzle_blob_detect_support`. |
| 5 | AIR_PRINT_DETECT | Legacy firmware-level (home_flag) air-printing detection. On supported printers, prefer `set_airprinting_detector()` (xcam AI) which adds sensitivity control. Guarded by `has_air_print_detect_support`. |

### ServiceState
**Source**: `src/bpm/bambutools.py`

| Value | Name | Description |
|-------|------|-------------|
| 0 | NO_STATE | Uninitialized |
| 1 | CONNECTED | Connected to MQTT broker |
| 2 | DISCONNECTED | Disconnected from broker |
| 3 | PAUSED | Session paused |
| 4 | QUIT | Session terminated |

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

### Additional Utility / Parsing Functions

The following helpers are part of the mapped data pipeline and support class-level
state population or metadata derivation.

| Function | Source Module | Purpose |
|----------|---------------|---------|
| [`getAMSHeatingState(ams_info: int)`](reference/bpm/bambutools.md#bpm.bambutools.getAMSHeatingState) | `bambutools.py` | Decode AMS heater state from bit field |
| [`getAMSModelBySerial(serial: str)`](reference/bpm/bambutools.md#bpm.bambutools.getAMSModelBySerial) | `bambutools.py` | Infer AMS model from serial prefix |
| [`getAMSSeriesByModel(model: AMSModel)`](reference/bpm/bambutools.md#bpm.bambutools.getAMSSeriesByModel) | `bambutools.py` | Convert AMS model to AMS generation |
| [`getPrinterModelBySerial(serial: str)`](reference/bpm/bambutools.md#bpm.bambutools.getPrinterModelBySerial) | `bambutools.py` | Infer printer model from serial prefix |
| [`getPrinterSeriesByModel(model: PrinterModel)`](reference/bpm/bambutools.md#bpm.bambutools.getPrinterSeriesByModel) | `bambutools.py` | Convert model to printer family |
| [`parseAMSStatus(status_int: int)`](reference/bpm/bambutools.md#bpm.bambutools.parseAMSStatus) | `bambutools.py` | Convert AMS status integer to readable state |
| [`parseExtruderTrayState(extruder: int, idx, status)`](reference/bpm/bambutools.md#bpm.bambutools) | `bambutools.py` | Convert extruder tray bits to tray ID |
| [`parseRFIDStatus(status)`](reference/bpm/bambutools.md#bpm.bambutools.parseRFIDStatus) | `bambutools.py` | Convert RFID state code to readable status |
| [`parseStage(stage_int: int)`](reference/bpm/bambutools.md#bpm.bambutools.parseStage) | `bambutools.py` | Convert print stage ID to stage name |
| [`sortFileTreeAlphabetically(source)`](reference/bpm/bambutools.md#bpm.bambutools.sortFileTreeAlphabetically) | `bambutools.py` | Stable sort for SD-card tree output |
| [`get_file_md5(file_path: str \| Path)`](reference/bpm/bambutools.md#bpm.bambutools.get_file_md5) | `bambutools.py` | Compute file checksum for cache integrity |
| [`get_3mf_entry_by_name(node, target_name)`](reference/bpm/bambuproject.md#bpm.bambuproject) | `bambuproject.py` | Locate 3MF tree node by filename |
| [`get_3mf_entry_by_id(node, target_id)`](reference/bpm/bambuproject.md#bpm.bambuproject) | `bambuproject.py` | Locate 3MF tree node by identifier |
| [`get_project_info(...)`](reference/bpm/bambuproject.md#bpm.bambuproject.get_project_info) | `bambuproject.py` | Build [`ProjectInfo`](reference/bpm/bambuproject.md#bpm.bambuproject.ProjectInfo) from printer or local 3MF source |
| [`BambuState.fromJson(data, printer)`](reference/bpm/bambustate.md#bpm.bambustate.BambuState.fromJson) | `bambustate.py` | Primary state parser mapping MQTT payloads to dataclasses |

---

## Class & Method Coverage Index

This index verifies current class/method/property coverage for the `src/bpm`
surface area and links each area to its documentation section.

### Class Coverage

| Class | Coverage |
| ----- | -------- |
| [`BambuConfig`](reference/bpm/bambuconfig.md#bpm.bambuconfig.BambuConfig) | Documented in [BambuConfig](#bambuconfig) |
| [`PrinterCapabilities`](reference/bpm/bambuconfig.md#bpm.bambuconfig.PrinterCapabilities) | Documented in [PrinterCapabilities](#printercapabilities) |
| [`BambuState`](reference/bpm/bambustate.md#bpm.bambustate.BambuState) | Documented in [BambuState](#bambustate) |
| [`ExtruderState`](reference/bpm/bambustate.md#bpm.bambustate.ExtruderState) | Documented in [ExtruderState](#extruderstate) |
| [`AMSUnitState`](reference/bpm/bambustate.md#bpm.bambustate.AMSUnitState) | Documented in [AMSUnitState](#amsunitstate) |
| [`BambuClimate`](reference/bpm/bambustate.md#bpm.bambustate.BambuClimate) | Documented in [BambuClimate](#bambuclimate) |
| [`BambuSpool`](reference/bpm/bambuspool.md#bpm.bambuspool.BambuSpool) | Documented in [BambuSpool](#bambuspool) |
| [`ProjectInfo`](reference/bpm/bambuproject.md#bpm.bambuproject.ProjectInfo) | Documented in [ProjectInfo](#projectinfo) |
| [`ActiveJobInfo`](reference/bpm/bambuproject.md#bpm.bambuproject.ActiveJobInfo) | Documented in [ActiveJobInfo](#activejobinfo) |
| [`BambuPrinter`](reference/bpm/bambuprinter.md#bpm.bambuprinter.BambuPrinter) | Method/property coverage indexed below; command payloads documented in [MQTT Protocol Reference](mqtt-protocol-reference.md) |
| `FtpListItem` | Covered in FTPS class index below |
| `ImplicitTLS` | Covered in FTPS class index below |
| `IoTFTPSClient` | Covered in FTPS class index below |

### Non-Printer Methods / Constructors

| Module / Class | Methods |
|----------------|---------|
| [`BambuConfig`](reference/bpm/bambuconfig.md#bpm.bambuconfig.BambuConfig) | [`__post_init__`](reference/bpm/bambuconfig.md#bpm.bambuconfig.BambuConfig.__post_init__), [`set_new_bpm_cache_path`](reference/bpm/bambuconfig.md#bpm.bambuconfig.BambuConfig.set_new_bpm_cache_path) |
| [`BambuState`](reference/bpm/bambustate.md#bpm.bambustate.BambuState) | [`fromJson`](reference/bpm/bambustate.md#bpm.bambustate.BambuState.fromJson) |
| `bambuproject` | `get_3mf_entry_by_name`, `get_3mf_entry_by_id`, [`get_project_info`](reference/bpm/bambuproject.md#bpm.bambuproject.get_project_info) |
| [`get_project_info`](reference/bpm/bambuproject.md#bpm.bambuproject.get_project_info) internal helpers | `get_nodes_by_plate_id`, `_split_config_list`, `_extract_list_from_config`, `_extract_list_from_gcode_header`, `_normalize_hex_color`, `_ensure_ams_mapping` |

### [`BambuPrinter`](reference/bpm/bambuprinter.md#bpm.bambuprinter.BambuPrinter) Public Methods

| Category | Methods |
|----------|---------|
| Session lifecycle | `start_session`, `pause_session`, `resume_session`, `quit`, `refresh` |
| Temperature/fans | `set_bed_temp_target`, `set_nozzle_temp_target`, `set_chamber_temp`, `set_chamber_temp_target`, `set_part_cooling_fan_speed_target_percent`, `set_aux_fan_speed_target_percent`, `set_exhaust_fan_speed_target_percent` |
| Filament / AMS | `unload_filament`, `load_filament`, `set_ams_user_setting`, `set_spool_k_factor`, `set_spool_details`, `send_ams_control_command`, `turn_on_ams_dryer`, `turn_off_ams_dryer`, `refresh_spool_rfid`, `select_extrusion_calibration_profile`, `get_current_bind_list` |
| Print control | `print_3mf_file`, `stop_printing`, `pause_printing`, `resume_printing`, `set_print_option`, `set_active_tool`, `set_nozzle_details`, `set_buildplate_marker_detector`, `skip_objects` |
| Raw/send helpers | `send_gcode`, `send_anything` |
| SD card / FTPS | `ftp_connection`, `get_sdcard_contents`, `get_sdcard_3mf_files`, `delete_sdcard_file`, `delete_sdcard_folder`, `upload_sdcard_file`, `download_sdcard_file`, `make_sdcard_directory`, `rename_sdcard_file`, `sdcard_file_exists` |
| Serialization/introspection | `toJson`, `jsonSerializer` |

### [`BambuPrinter`](reference/bpm/bambuprinter.md#bpm.bambuprinter.BambuPrinter) Properties / Accessors

| Property | Notes |
|----------|-------|
| `config` | Config object getter/setter |
| `service_state` | Connection state getter/setter |
| `client` | MQTT client getter/setter |
| `on_update` | Update callback getter/setter |
| `recent_update` | Read-only recent update marker |
| `bed_temp_target_time`, `tool_temp_target_time`, `chamber_temp_target_time`, `fan_speed_target_time` | Read-only target-change timestamps |
| `light_state` | Light mode getter/setter |
| `speed_level` | Speed profile getter/setter |
| `printer_state` | Current parsed [`BambuState`](reference/bpm/bambustate.md#bpm.bambustate.BambuState) |
| `active_job_info` | Current parsed [`ActiveJobInfo`](reference/bpm/bambuproject.md#bpm.bambuproject.ActiveJobInfo) |
| `internalException` | Last internal exception getter |
| `cached_sd_card_contents`, `cached_sd_card_3mf_files` | SD card cache getters |
| `skipped_objects` | Last skipped object list |
| `nozzle_diameter`, `nozzle_type` | Normalized nozzle metadata getters |

### FTPS Classes & Methods

| Class | Methods / Properties |
|-------|----------------------|
| [`FtpListItem`](reference/bpm/ftpsclient/ftpsclient.md#bpm.ftpsclient.ftpsclient) | Dataclass fields: `path`, `name`, `size`, `is_dir`, `timestamp`, `owner`, `group`, `permissions` |
| [`ImplicitTLS`](reference/bpm/ftpsclient/ftpsclient.md#bpm.ftpsclient.ftpsclient.ImplicitTLS) | `__init__`, [`sock`](reference/bpm/ftpsclient/ftpsclient.md#bpm.ftpsclient.ftpsclient.ImplicitTLS.sock) (getter/setter), `ntransfercmd` |
| [`IoTFTPSClient`](reference/bpm/ftpsclient/ftpsclient.md#bpm.ftpsclient.ftpsclient.IoTFTPSClient) | `__init__`, `__repr__`, [`instantiate_ftps_session`](reference/bpm/ftpsclient/ftpsclient.md#bpm.ftpsclient.ftpsclient.IoTFTPSClient.instantiate_ftps_session), [`disconnect`](reference/bpm/ftpsclient/ftpsclient.md#bpm.ftpsclient.ftpsclient.IoTFTPSClient.disconnect), [`download_file`](reference/bpm/ftpsclient/ftpsclient.md#bpm.ftpsclient.ftpsclient.IoTFTPSClient.download_file), [`upload_file`](reference/bpm/ftpsclient/ftpsclient.md#bpm.ftpsclient.ftpsclient.IoTFTPSClient.upload_file), [`delete_file`](reference/bpm/ftpsclient/ftpsclient.md#bpm.ftpsclient.ftpsclient.IoTFTPSClient.delete_file), [`delete_folder`](reference/bpm/ftpsclient/ftpsclient.md#bpm.ftpsclient.ftpsclient.IoTFTPSClient.delete_folder), [`move_file`](reference/bpm/ftpsclient/ftpsclient.md#bpm.ftpsclient.ftpsclient.IoTFTPSClient.move_file), `mkdir`, `fexists`, [`list_files`](reference/bpm/ftpsclient/ftpsclient.md#bpm.ftpsclient.ftpsclient.IoTFTPSClient.list_files), [`list_files_ex`](reference/bpm/ftpsclient/ftpsclient.md#bpm.ftpsclient.ftpsclient.IoTFTPSClient.list_files_ex) |

### Internal Methods (Parsing/Infrastructure)

| Method | Purpose |
|--------|---------|
| [`_notify_update`](reference/bpm/bambuprinter.md#bpm.bambuprinter.BambuPrinter) | Execute update callback safely |
| [`_start_watchdog`](reference/bpm/bambuprinter.md#bpm.bambuprinter.BambuPrinter) | Session timeout and re-announce loop |
| [`_on_message`](reference/bpm/bambuprinter.md#bpm.bambuprinter.BambuPrinter) | Primary inbound MQTT message handler |
| [`_get_sftp_files`](reference/bpm/bambuprinter.md#bpm.bambuprinter.BambuPrinter) | FTPS file listing helper |

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
| 1.2 | 2026-02-25 | Added missing `ProjectInfo.plates`, expanded enum coverage (all current enums), added utility/parsing function index, and added class/method/property coverage index including `BambuPrinter` |
| 1.1 | 2026-02-25 | Added BambuConfig, PrinterCapabilities, ProjectInfo, ActiveJobInfo dataclasses; comprehensive MQTT Control references; field-level consistency |
| 1.0 | 2026-02-23 | Initial comprehensive data dictionary |
