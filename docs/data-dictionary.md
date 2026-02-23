# Bambu Printer Manager - Data Dictionary

## Overview

This comprehensive data dictionary documents all attributes manifested in the bambu-printer-manager library. Each attribute includes its ancestry (parent class), telemetry source (MQTT JSON path), type information, valid ranges, and purpose.

## Reference Implementations

Attributes are validated against these implementations:

- **[BambuStudio](https://github.com/bambulab/BambuStudio)** - Bambu Lab's slicer/client (C++)
- **[OrcaSlicer](https://github.com/OrcaSlicer/OrcaSlicer)** - Community fork with enhanced features (C++)
- **[ha-bambulab](https://github.com/greghesp/ha-bambulab)** - Home Assistant integration (Python)

## Dataclass Hierarchy

```
BambuState (root)
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
```

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

#### aux_fan_speed_percent
- **Type**: `int`
- **Telemetry**: `print.big_fan1_speed` (scaled) or `airduct.parts[32].state`
- **Valid Range**: `0-100`
- **Unit**: %
- **Purpose**: Auxiliary fan speed
- **Reference**: BambuStudio fan control

#### exhaust_fan_speed_percent
- **Type**: `int`
- **Telemetry**: `print.big_fan2_speed` (scaled) or `airduct.parts[48].state`
- **Valid Range**: `0-100`
- **Unit**: %
- **Purpose**: Exhaust/chamber fan speed
- **Reference**: BambuStudio fan control

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

#### nozzle_temp_max
- **Type**: `int`
- **Telemetry**: `tray[].nozzle_temp_max`
- **Unit**: °C
- **Purpose**: Maximum safe nozzle temperature
- **Reference**: BambuStudio filament profiles

#### drying_temp
- **Type**: `int`
- **Telemetry**: `tray[].drying_temp`
- **Unit**: °C
- **Purpose**: Recommended drying temperature
- **Reference**: BambuStudio filament drying settings

#### drying_time
- **Type**: `int`
- **Telemetry**: `tray[].drying_time`
- **Unit**: Hours
- **Purpose**: Recommended drying duration
- **Reference**: BambuStudio filament drying settings

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
| 1.0 | 2026-02-23 | Initial comprehensive data dictionary |

---

## See Also

- [BambuStudio Source](https://github.com/bambulab/BambuStudio)
- [OrcaSlicer Source](https://github.com/OrcaSlicer/OrcaSlicer)
- [ha-bambulab Integration](https://github.com/greghesp/ha-bambulab)
