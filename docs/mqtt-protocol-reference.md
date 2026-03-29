# MQTT Protocol Reference

This document provides a comprehensive breakdown of MQTT message structures used by bambu-printer-manager to communicate with Bambu Lab printers. Each message correlates directly to attributes in the [Data Dictionary](data-dictionary.md).

### Related Documentation

- **[Data Dictionary](data-dictionary.md)** — Complete reference of all printer state attributes, telemetry paths, and data types
- **[API Reference](api-reference.md)** — REST API endpoints mapping to MQTT operations
- **[Container Setup](container.md)** — Docker deployment with full MQTT integration examples

## Communication Architecture

**MQTT Topics:**

- **Request**: `device/{serial_number}/request` - Commands sent TO the printer
- **Report**: `device/{serial_number}/report` - All telemetry received FROM the printer (actively subscribed)

**Message Format**: All messages are JSON objects sent via MQTT with UTF-8 encoding.

**Sequence IDs**: All request commands include a `sequence_id` field (typically `"0"`) for tracking.

**Push vs Report**: There is no separate `/push` topic. "Push" messages are telemetry messages with `command="push_status"` received on the `/report` topic. These represent real-time state changes pushed by the printer. The outbound `pushing` command namespace in requests allows you to control push behavior (start/stop push updates).

---

## Alphabetical Command Index

| Command | Category | Description |
|---------|----------|-------------|
| [AMS Control Commands](#ams-control-commands) | AMS | Resume, pause, or reset AMS |
| [AMS Filament Drying](#ams-filament-drying) | Filament | Configure AMS drying parameters |
| [AMS Get RFID](#ams-get-rfid) | AMS | Read RFID tag from AMS slot |
| [AMS User Settings](#ams-user-settings) | AMS | Configure AMS startup and tray read options |
| [Aux Fan (Hotend Cooling)](#aux-fan-hotend-cooling) | Fan | Set auxiliary fan speed |
| [Buildplate Marker Detection](#buildplate-marker-detection) | Settings | Enable/disable buildplate marker detection |
| [Chamber Air Conditioning Mode](#chamber-air-conditioning-mode) | Settings | Control chamber AC/ventilation mode |
| [Chamber Light Control](#chamber-light-control) | System | Toggle chamber lights on/off |
| [Exhaust Fan](#exhaust-fan) | Fan | Set exhaust fan speed |
| [Extrusion Calibration Profile](#extrusion-calibration-profile) | Calibration | Select extrusion calibration profile for tray |
| [Load Filament / Change Filament](#load-filament-change-filament) | Filament | Load or change filament in AMS slot |
| [Pause Print](#pause-print) | Print Job | Pause the current print job |
| [Part Cooling Fan (Layer Cooling)](#part-cooling-fan-layer-cooling) | Fan | Set part cooling fan speed |
| [Resume Print](#resume-print) | Print Job | Resume a paused print job |
| [Select Active Extruder (Dual Extruder)](#select-active-extruder-dual-extruder) | Extruder | Switch between extruders |
| [Send Raw G-Code](#send-raw-g-code) | Advanced | Send raw G-code commands |
| [Set Bed Temperature Target](#set-bed-temperature-target) | Temperature | Set target bed temperature |
| [Set Chamber Temperature Target](#set-chamber-temperature-target) | Temperature | Set target chamber temperature |
| [Set Filament Details / Spool Settings](#set-filament-details-spool-settings) | Filament | Configure filament spool properties |
| [Set Nozzle Temperature Target](#set-nozzle-temperature-target) | Temperature | Set target nozzle temperature |
| [Set Nozzle Type & Diameter](#set-nozzle-type-diameter) | Accessory | Configure nozzle size |
| [Set Print Options](#set-print-options) | Print Job | Configure print behavior options |
| [Set Print Speed Profile](#set-print-speed-profile) | Advanced | Configure print speed preset |
| [Skip Objects During Print](#skip-objects-during-print) | Print Job | Skip objects or regions during print |
| [Start Print (3MF File)](#start-print-3mf-file) | Print Job | Upload and start a 3MF print file |
| [Stop Print](#stop-print) | Print Job | Stop and abort the current print job |

---

## Temperature Control

### Set Bed Temperature Target

**MQTT Topic**: `device/{serial}/request`

**Command Name**: `gcode_line` (via SEND_GCODE_TEMPLATE)

**Message Structure**:
```json
{
  "print": {
    "sequence_id": "0",
    "command": "gcode_line",
    "param": "M140 S60\n"
  }
}
```

**Fields:**

| Field | Type | Example | Purpose |
|-------|------|---------|---------|
| `command` | string | `"gcode_line"` | Instructs printer to execute raw G-code |
| `param` | string | `"M140 S60\n"` | M140 G-code command: S = temperature in °C (0-120 typical) |

**Data Dictionary Correlation**: [`bed_temp_target`](data-dictionary.md#bambustate), [`bed_temp`](data-dictionary.md#bambustate)

**Data Dictionary Reference**: Related attributes in [Bed Temperature](data-dictionary.md#bed-temperature) section

**Python Method**: `BambuPrinter.set_bed_temp_target(value: int)`

**Example Usage**:
```python
printer.set_bed_temp_target(60)  # Set bed to 60°C
```

---

### Set Nozzle Temperature Target

**MQTT Topic**: `device/{serial}/request`

**Command Name**: `gcode_line` (via SEND_GCODE_TEMPLATE)

**Message Structure**:
```json
{
  "print": {
    "sequence_id": "0",
    "command": "gcode_line",
    "param": "M104 S220\n"
  }
}
```

**Fields:**

| Field | Type | Example Values | Purpose |
|-------|------|----------------|---------|
| `param` | string | `"M104 S220\n"` | G-code command: S = temperature in °C (0-280 typical) |
| `param` (with tool) | string | `"M104 S220 T1\n"` | Same with T parameter specifying tool number (0-indexed) |

**Implementation Notes**:
- The T parameter is only included when `tool_num >= 0` is provided to the Python method
- When `tool_num == -1` (default), the T parameter is omitted (applies to active tool)

**Data Dictionary Correlation**: [`active_nozzle_temp_target`](data-dictionary.md#extruderstate)

**Data Dictionary Reference**: Related attributes in [ExtruderState](data-dictionary.md#extruderstate) section

**Python Method**: `BambuPrinter.set_nozzle_temp_target(value: int, tool_num: int = -1)`

**Example Usage**:
```python
printer.set_nozzle_temp_target(220)           # Set active nozzle to 220°C
printer.set_nozzle_temp_target(210, tool_num=1)  # Set extruder 2 to 210°C
```

---

### Set Chamber Temperature Target

**MQTT Topic**: `device/{serial}/request`

**Command Name**: `set_ctt` (chamber temperature target)

**Message Structure**:
```json
{
  "print": {
    "command": "set_ctt",
    "ctt_val": 40,
    "sequence_id": "0",
    "temper_check": true
  }
}
```

**Fields:**

| Field | Type | Range | Purpose |
|-------|------|-------|---------|
| `ctt_val` | integer | 20-60°C | Target chamber temperature |
| `temper_check` | boolean | `true`/`false` | Enable/disable temperature validation |

**Data Dictionary Correlation**: [`chamber_temp_target`](data-dictionary.md#bambustate), [`chamber_temp`](data-dictionary.md#bambustate)

**Data Dictionary Reference**: Related attributes in [Chamber Temperature](data-dictionary.md#chamber-temperature) section

**Python Method**: `BambuPrinter.set_chamber_temp_target(value: int, temper_check: bool = True)`

**Capability Gate**: Only supported on printers with `has_chamber_temp` capability

**Example Usage**:
```python
printer.set_chamber_temp_target(45)  # Set chamber to 45°C
```

---

## Fan Control

### Part Cooling Fan (Layer Cooling)

**MQTT Topic**: `device/{serial}/request`

**Command Name**: `gcode_line`

**Message Structure**:
```json
{
  "print": {
    "sequence_id": "0",
    "command": "gcode_line",
    "param": "M106 P1 S191\n"
  }
}
```

**Fields:**

| Field | Type | Example | Purpose |
|-------|------|---------|---------|
| `param` | string | `"M106 P1 S191\n"` | G-code: P1 = part cooling fan, S = speed 0-255 (191 ≈ 75%) |

**Data Dictionary Correlation**: [`part_cooling_fan_speed_percent`](data-dictionary.md#bambustate), [`part_cooling_fan_speed_target_percent`](data-dictionary.md#bambustate)

**Data Dictionary Reference**: Related attributes in [Fan Speed Attributes](data-dictionary.md#fan-speed-attributes) section

**Python Method**: `BambuPrinter.set_part_cooling_fan_speed_target_percent(value: int)`

**Input Validation**: Accepts 0-100% and automatically converts to 0-255 (multiplies by 2.55)

**Example Usage**:
```python
printer.set_part_cooling_fan_speed_target_percent(75)  # 75% speed
```

---

### Aux Fan (Hotend Cooling)

**MQTT Topic**: `device/{serial}/request`

**Command Name**: `gcode_line`

**Message Structure**:
```json
{
  "print": {
    "sequence_id": "0",
    "command": "gcode_line",
    "param": "M106 P2 S255\n"
  }
}
```

**Fields:**

| Field | Type | Example | Purpose |
|-------|------|---------|---------|
| `param` | string | `"M106 P2 S255\n"` | G-code: P2 = auxiliary/chamber fan, S = speed 0-255 |

**Data Dictionary Correlation**: [`aux_fan_speed_percent`](data-dictionary.md#bambustate)

**Data Dictionary Reference**: Related attributes in [Fan Speed Attributes](data-dictionary.md#fan-speed-attributes) section

**Python Method**: `BambuPrinter.set_aux_fan_speed_target_percent(value: int)`

**Example Usage**:
```python
printer.set_aux_fan_speed_target_percent(100)  # Full speed
```

---

### Exhaust Fan

**MQTT Topic**: `device/{serial}/request`

**Command Name**: `gcode_line`

**Message Structure**:
```json
{
  "print": {
    "sequence_id": "0",
    "command": "gcode_line",
    "param": "M106 P3 S255\n"
  }
}
```

**Fields:**

| Field | Type | Example | Purpose |
|-------|------|---------|---------|
| `param` | string | `"M106 P3 S255\n"` | G-code: P3 = exhaust/chamber fan, S = speed 0-255 |

**Data Dictionary Correlation**: [`exhaust_fan_speed_percent`](data-dictionary.md#bambustate)

**Data Dictionary Reference**: Related attributes in [Fan Speed Attributes](data-dictionary.md#fan-speed-attributes) section

**Python Method**: `BambuPrinter.set_exhaust_fan_speed_target_percent(value: int)`

**Example Usage**:
```python
printer.set_exhaust_fan_speed_target_percent(50)  # 50% speed
```

---

## Print Job Control

### Pause Print

**MQTT Topic**: `device/{serial}/request`

**Command Name**: `pause`

**Message Structure**:
```json
{
  "print": {
    "sequence_id": "0",
    "command": "pause"
  }
}
```

**Data Dictionary Reference**: Related to [Core State Attributes](data-dictionary.md#core-state-attributes) in BambuState

**Python Method**: `BambuPrinter.pause_printing()`

---

### Resume Print

**MQTT Topic**: `device/{serial}/request`

**Command Name**: `resume`

**Message Structure**:
```json
{
  "print": {
    "sequence_id": "0",
    "command": "resume"
  }
}
```

**Data Dictionary Reference**: Related to [Core State Attributes](data-dictionary.md#core-state-attributes) in BambuState

**Python Method**: `BambuPrinter.resume_printing()`

---

### Stop Print

**MQTT Topic**: `device/{serial}/request`

**Command Name**: `stop`

**Message Structure**:
```json
{
  "print": {
    "sequence_id": "0",
    "command": "stop"
  }
}
```

**Data Dictionary Reference**: Related to [Core State Attributes](data-dictionary.md#core-state-attributes) in BambuState

**Python Method**: `BambuPrinter.stop_printing()`

---

### Start Print (3MF File)

**MQTT Topic**: `device/{serial}/request`

**Command Name**: `project_file`

**Message Structure**:
```json
{
  "print": {
    "command": "project_file",
    "sequence_id": "0",
    "use_ams": true,
    "ams_mapping": "[0,1,2,3]",
    "bed_type": "textured_plate",
    "url": "ftp:///jobs/model.gcode.3mf",
    "file": "/jobs/model.gcode.3mf",
    "param": "Metadata/plate_1.gcode",
    "md5": "",
    "profile_id": "0",
    "project_id": "0",
    "subtask_id": "0",
    "subtask_name": "model",
    "task_id": "0",
    "timelapse": false,
    "bed_leveling": true,
    "flow_cali": true,
    "layer_inspect": true,
    "vibration_cali": true
  }
}
```

**Fields:**

| Field | Type | Example | Purpose |
|-------|------|---------|---------|
| `url` | string | `"ftp:///path.3mf"` | FTP URL to print file on SD card |
| `file` | string | `"/path.3mf"` | Local file path on printer |
| `param` | string | `"Metadata/plate_1.gcode"` | Plate metadata path (# replaced with plate number) |
| `use_ams` | boolean | `true`/`false` | Use AMS for print |
| `ams_mapping` | string | `"[0,1,4,128]"` | JSON array of absolute tray IDs per filament (0-103=4-slot units, 128-135=1-slot units, -1=unmapped) |
| `bed_type` | string | `"auto"`, `"hot_plate"`, `"textured_plate"` | Bed plate type |
| `bed_leveling` | boolean | `true` | Auto bed leveling before print |
| `flow_cali` | boolean | `true` | Extrusion flow calibration before print |
| `timelapse` | boolean | `false` | Capture timelapse during print |
| `layer_inspect` | boolean | `true` | Enable layer inspection |
| `vibration_cali` | boolean | `true` | Vibration calibration on start |

**Data Dictionary Correlation**: [`active_job_info`](data-dictionary.md#bambustate), [`gcode_state`](data-dictionary.md#bambustate)

**Data Dictionary Reference**: Related attributes in [BambuState](data-dictionary.md#bambustate) section

**Data Dictionary Correlation**:
- `active_job_info` (all fields updated after start)
- `gcode_state` → RUNNING

**Python Method**: `BambuPrinter.print_3mf_file(name, plate, bed, use_ams, ams_mapping, bedlevel, flow, timelapse)`

**AMS Mapping Examples**:

| ams_mapping | Description |
|-------------|-------------|
| `[0,1,2,3]` | 4 filaments, all from AMS 0 slots 0-3 |
| `[0,4,5,6]` | 4 filaments: AMS 0 slot 0, then AMS 1 slots 0-2 |
| `[0,-1,2,-1]` | 4 filaments: slot 0, unmapped, slot 2, unmapped (from AMS 0) |
| `[0,4,128]` | 3 filaments: AMS 0 slot 0, AMS 1 slot 0, AMS HT unit |

---

## Filament Management

### Load Filament / Change Filament

**MQTT Topic**: `device/{serial}/request`

**Command Name**: `ams_change_filament`

**Message Structure**:
```json
{
  "print": {
    "sequence_id": "0",
    "command": "ams_change_filament",
    "ams_id": 0,
    "slot_id": 0,
    "target": 0,
    "soft_temp": 0,
    "tar_temp": -1,
    "curr_temp": -1
  }
}
```

**Fields:**

| Field | Type | Range | Purpose |
|-------|------|-------|---------|
| `ams_id` | integer | 0-3 | Which AMS unit (4 max per printer) |
| `slot_id` | integer | 0-3 | Slot within AMS (4 slots per unit) |
| `target` | integer | 0-3 (or 255) | Which extruder to load into (255 = skip load) |
| `soft_temp` | integer | 0 | Softening temperature (currently unused) |
| `tar_temp` | integer | -1 | Target temperature (-1 = auto) |
| `curr_temp` | integer | -1 | Current temperature (-1 = auto) |

**Data Dictionary Correlation**: [`active_tray_id`](data-dictionary.md#amsunitstate), [`active_tray_state`](data-dictionary.md#amsunitstate), [`ams_units[].trays[].active`](data-dictionary.md#amsunitstate)

**Data Dictionary Reference**: Related attributes in [AMSUnitState](data-dictionary.md#amsunitstate) section

**Python Method**: `BambuPrinter.load_filament(slot_id: int, ams_id: int = 0)`

**Example Usage**:
```python
printer.load_filament(2, 0)  # Load slot 2 (0-indexed) from AMS 0
printer.load_filament(254)   # Load external spool
```

---

### Set Filament Details / Spool Settings

**MQTT Topic**: `device/{serial}/request`

**Command Name**: `ams_filament_setting`

**Message Structure**:
```json
{
  "print": {
    "ams_id": 0,
    "command": "ams_filament_setting",
    "nozzle_temp_max": 240,
    "nozzle_temp_min": 200,
    "sequence_id": "0",
    "slot_id": 0,
    "tray_color": "FF0000FF",
    "tray_id": 0,
    "tray_info_idx": "GFL99",
    "tray_type": "NORMAL"
  }
}
```

**Fields:**

| Field | Type | Example | Purpose |
|-------|------|---------|---------|
| `ams_id` | integer | 0 | AMS unit (0-3) |
| `slot_id` | integer | 0-3 | Slot within AMS |
| `tray_id` | integer | 0-3 or 254/255 | Global tray ID (254=external, 255=nozzle) |
| `tray_info_idx` | string | `"GFL99"` | Filament type ID from printer database |
| `tray_type` | string | `"NORMAL"` | Filament material type |
| `tray_color` | string | `"FF0000FF"` | RGBA hex color (RedGreenBlueAlpha) |
| `nozzle_temp_min` | integer | 200-280 | Minimum nozzle temperature |
| `nozzle_temp_max` | integer | 200-280 | Maximum nozzle temperature |

**Data Dictionary Correlation**: [`nozzle_temp_min`](data-dictionary.md#bambuspool), [`nozzle_temp_max`](data-dictionary.md#bambuspool), [`color`](data-dictionary.md#bambuspool)

**Data Dictionary Reference**: Related attributes in [BambuSpool](data-dictionary.md#bambuspool) section

**Data Dictionary Correlation**:
- `ams_units[ams_id].trays[slot_id].color`
- `ams_units[ams_id].trays[slot_id].nozzle_temp_min`
- `ams_units[ams_id].trays[slot_id].nozzle_temp_max`
- `ams_units[ams_id].trays[slot_id].filament_type`

**Python Method**: `BambuPrinter.set_spool_details(tray_id, tray_info_idx, tray_id_name, tray_type, tray_color, nozzle_temp_min, nozzle_temp_max, ams_id)`

**Special Case - Empty External Tray**:
```python
printer.set_spool_details(254, "no_filament")  # Clear external spool
```

---

### AMS Filament Drying

**MQTT Topic**: `device/{serial}/request`

**Command Name**: `ams_filament_drying`

**Message Structure**:
```json
{
  "print": {
    "sequence_id": "0",
    "command": "ams_filament_drying",
    "ams_id": 0,
    "mode": 1,
    "temp": 55,
    "cooling_temp": 45,
    "duration": 120,
    "humidity": 20,
    "rotate_tray": true,
    "close_power_conflict": false
  }
}
```

**Fields:**

| Field | Type | Example | Purpose |
|-------|------|---------|---------|
| `ams_id` | integer | 0 | Target AMS unit |
| `mode` | integer | 0-2 | Drying mode (0=off, 1=dry, 2=cool) |
| `temp` | integer | 30-70°C | Drying temperature |
| `cooling_temp` | integer | 30-50°C | Cooling temperature after drying |
| `duration` | integer | minutes | How long to dry |
| `humidity` | integer | 0-100% | Target humidity (for compatible sensors) |
| `rotate_tray` | boolean | `true` | Rotate tray during drying |
| `close_power_conflict` | boolean | `false` | Handle power conflicts |

**Data Dictionary Reference**: Related attributes in [AMSUnitState](data-dictionary.md#amsunitstate) section for drying operations

**Data Dictionary Correlation**:
- `ams_units[ams_id].dryer_power_on`
- `ams_units[ams_id].dryer_temp` (for enabled dryers)

**Python Method**: `BambuPrinter.turn_on_ams_dryer(target_temp, duration, target_humidity, cooling_temp, rotate_tray, ams_id)`

**Example Usage**:
```python
printer.turn_on_ams_dryer(target_temp=55, duration=120, ams_id=0)  # Dry for 2 hours
```

---

## Accessory Control

### Set Nozzle Type & Diameter

**MQTT Topic**: `device/{serial}/request`

**Command Name**: `set_accessories`

**Message Structure**:
```json
{
  "system": {
    "accessory_type": "nozzle",
    "command": "set_accessories",
    "nozzle_diameter": 0.4,
    "nozzle_type": "hardened_steel"
  }
}
```

**Fields:**

| Field | Type | Example | Purpose |
|-------|------|---------|---------|
| `accessory_type` | string | `"nozzle"` | Type of accessory being configured |
| `nozzle_diameter` | float | 0.4, 0.6, 0.8 | Nozzle diameter in mm |
| `nozzle_type` | string | `"hardened_steel"`, `"stainless_steel"` | Nozzle material type |

**Data Dictionary Reference**: Related configuration in [BambuState](data-dictionary.md#bambustate) section

**Data Dictionary Correlation**:
- `nozzle_diameter`
- `nozzle_type`

**Python Method**: `BambuPrinter.set_nozzle_details(nozzle_diameter, nozzle_type)`

**Example Usage**:
```python
from bpm.bambutools import NozzleDiameter, NozzleType
printer.set_nozzle_details(NozzleDiameter.DIAMETER_0_8, NozzleType.HARDENED_STEEL)
```

---

## Tool / Extruder Control

### Select Active Extruder (Dual Extruder)

**MQTT Topic**: `device/{serial}/request`

**Command Name**: `select_extruder`

**Message Structure**:
```json
{
  "print": {
    "command": "select_extruder",
    "extruder_index": 0,
    "sequence_id": "0"
  }
}
```

**Fields:**

| Field | Type | Range | Purpose |
|-------|------|-------|---------|
| `extruder_index` | integer | 0-1 | Which extruder (0=left, 1=right) |

**Data Dictionary Correlation**: [`active_tool`](data-dictionary.md#bambustate)

**Data Dictionary Reference**: Related to [BambuState](data-dictionary.md#bambustate) active tool selection

**Data Dictionary Correlation**: `active_tool`

**Python Method**: `BambuPrinter.set_active_tool(id: int)`

**Example Usage**:
```python
printer.set_active_tool(1)  # Switch to extruder 2
```

---

## Advanced Settings

### Send Raw G-Code

**MQTT Topic**: `device/{serial}/request`

**Command Name**: `gcode_line`

**Message Structure**:
```json
{
  "print": {
    "sequence_id": "0",
    "command": "gcode_line",
    "param": "G28\nG29\n"
  }
}
```

**Fields:**

| Field | Type | Example | Purpose |
|-------|------|---------|---------|
| `param` | string | `"G28\n"` | Raw G-code commands separated by newlines |

**Data Dictionary Reference**: No specific attributes; affects printer motion and internal state directly

**Python Method**: `BambuPrinter.send_gcode(gcode: str)`

**Example Usage**:
```python
printer.send_gcode("G28")  # Home all axes
printer.send_gcode("G91\nG0 X10")  # Relative move 10mm in X
```

---

### Set Print Options

**MQTT Topic**: `device/{serial}/request`

**Command Name**: `print_option`

**Message Structure**:
```json
{
  "print": {
    "command": "print_option",
    "sequence_id": "0",
    "auto_recovery": "true",
    "auto_switch_filament": "true",
    "filament_tangle_detect": "true",
    "sound_enable": "true",
    "option": "1"
  }
}
```

**Fields:**

| Field | Type | Value | Purpose |
|-------|------|-------|---------|
| `auto_recovery` | string | `"true"`/`"false"` | Resume print after power loss |
| `auto_switch_filament` | string | `"true"`/`"false"` | Auto-switch to another AMS slot when active spool runs out. Target slot must have the **same filament type AND color**. AMS-hosted spools only. |
| `filament_tangle_detect` | string | `"true"`/`"false"` | Pause if AMS sensors detect a tangle. AMS-only; no effect on external spool prints. |
| `sound_enable` | string | `"true"`/`"false"` | Beep for notifications |
| `nozzle_blob_detect` | string | `"true"`/`"false"` | Legacy firmware-level nozzle blob detection. On supported printers, prefer xcam `nozzleclumping_detector` (adds sensitivity control). |
| `air_print_detect` | string | `"true"`/`"false"` | Legacy firmware-level air-printing detection. On supported printers, prefer xcam `airprinting_detector` (adds sensitivity control). |
| `option` | string | `"1"` / `"0"` | Meta-control flag |

**Data Dictionary Correlation**:
- `auto_recovery`
- `auto_switch_filament`
- `filament_tangle_detect`
- `sound_enable`

**Python Method**: `BambuPrinter.set_print_option(option: PrintOption, enabled: bool)`

**Example Usage**:
```python
from bpm.bambutools import PrintOption
printer.set_print_option(PrintOption.AUTO_RECOVERY, True)
printer.set_print_option(PrintOption.SOUND_ENABLE, False)
```

---

### Set Print Speed Profile

**MQTT Topic**: `device/{serial}/request`

**Command Name**: `print_speed`

**Message Structure**:
```json
{
  "print": {
    "sequence_id": "0",
    "command": "print_speed",
    "param": "2"
  }
}
```

**Fields:**

| Field | Type | Value | Purpose |
|-------|------|-------|---------|
| `param` | string | `"0"`, `"1"`, `"2"`, `"3"` | Speed profile preset (0-3) |

**Speed Profile Values**:
- `"0"` - Silent mode (slowest, quietest, highest quality)
- `"1"` - Standard mode (balanced speed and quality)
- `"2"` - Sport mode (faster speeds)
- `"3"` - Ludicrous mode (highest speed, lowest quality)

**Data Dictionary Reference**: Does not directly correlate to state attributes (affects print behavior)

**Implementation Notes**:
- The profile is applied to the next print job
- Current print continues with existing speed settings
- Equivalent to selecting speed preset from printer display menu

**Python Method**: Currently imported but not directly exposed; use raw MQTT or G-code commands for speed control

**Example Usage**:
```python
# Via direct GCODE instead
printer.send_gcode("M220 S100")  # Set speed to 100% (default)
printer.send_gcode("M220 S80")   # Reduce speed to 80%
```

---

### Skip Objects During Print

**MQTT Topic**: `device/{serial}/request`

**Command Name**: `skip_objects`

**Message Structure**:
```json
{
  "print": {
    "sequence_id": "0",
    "command": "skip_objects",
    "obj_list": [1, 3, 5]
  }
}
```

**Fields:**

| Field | Type | Example | Purpose |
|-------|------|---------|---------|
| `obj_list` | array of int | `[0, 2]` | List of object indices to skip (0-indexed) |

**Data Dictionary Correlation**: [`ProjectInfo.metadata.map.bbox_objects`](data-dictionary.md#projectinfo)

**Metadata Reference**:
The `obj_list` values must match the `id` field of objects in `ProjectInfo.metadata.map.bbox_objects`. These object IDs (e.g., 130, 174) are extracted from the 3MF file's `Metadata/slice_info.config` XML during project parsing via the `get_project_info()` method.

**Object ID Source** (3MF Processing):
- Structural object data (name, area, bbox) comes from `Metadata/plate_*.json`
- Object identify_id values extracted from `Metadata/slice_info.config` XML
- `identify_id` is assigned to each bbox_object's `id` field by array index match
- These resulting `id` values are what you pass to `skip_objects`

---

## AMS Filament/Spool Mapping Reference

This section documents how the `filament` array, `ams_mapping` array, and filament properties correlate to determine which AMS trays/spools are used during printing.

### Data Flow: Filament to AMS Tray Assignment

**Source**: [`ProjectInfo.metadata`](data-dictionary.md#projectinfo) populated via [`get_project_info()`](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuproject.py#L105)

**Components**:

1. **Filament Array** (`metadata.filament`)
   - Source: `Metadata/slice_info.config` XML, parsed from `<filament>` elements
   - Fields per filament:
     - `id` (integer, 1-indexed): Position in slicer filament list (filament 1, 2, 3, etc.)
     - `type` (string): Material type (e.g., "ABS", "PLA")
     - `color` (string): Hex color code (e.g., "#87909A")
   - Order: Filaments listed in the order they appear in the 3MF slicer specification

2. **AMS Mapping Array** (`metadata.ams_mapping`)
   - Source: `filament_maps` metadata from `Metadata/slice_info.config`, generated by slicer color-distance matching
   - Format: Array of absolute tray IDs calculated from installed AMS units
   - Array Index: 0-indexed position (maps to filament id minus 1)
   - Array Value: Absolute tray ID based on AMS unit type
     - **Standard 4-slot units** (AMS 2, AMS LITE, N3F): tray_id = ams_id * 4 + slot_id → value range 0-103
     - **Single-slot units** (N3S/AMS HT): tray_id = ams_id (starting at 128) → value range 128-135
     - `-1`: Unmapped filament (when use_ams=false or slicer could not auto-map)
   - Length: Matches number of filaments in the print
   - Note: External spools are managed via `use_ams` parameter, not through ams_mapping values

### Example Correlation

Given this ProjectInfo metadata:
```json
{
  "filament": [
    {"id": 1, "type": "ABS", "color": "#87909A"},
    {"id": 2, "type": "PLA", "color": "#FFFFFF"},
    {"id": 3, "type": "ABS", "color": "#000000"}
  ],
  "ams_mapping": [0, -1, 2]
}
```

**Spool Assignment**:

| Filament | Material | Mapping Index | Tray ID | Assignment |
|----------|----------|---------------|---------|------------|
| Filament 1 | ABS #87909A | `ams_mapping[0]` | `0` | AMS 0, slot 0 |
| Filament 2 | PLA #FFFFFF | `ams_mapping[1]` | `-1` | Unmapped (external spool) |
| Filament 3 | ABS #000000 | `ams_mapping[2]` | `2` | AMS 0, slot 2 |

### Python Usage

When calling `print_3mf_file()`, pass `ams_mapping` as a JSON string:
```python
from bpm.bambutools import PlateType
printer.print_3mf_file(
    name="/cache/my_project.3mf",
    plate=1,
    bed=PlateType.TEXTURED_PLATE,
    use_ams=True,
    ams_mapping="[0,-1,2]"  # Matches ProjectInfo.metadata['ams_mapping']
)
```

The printer uses this mapping to:
1. Load the correct AMS trays before printing
2. Route material to the correct nozzle during multi-material prints
3. Handle external spool fallback when AMS is offline

### References

**Source Code**:
- Mapping extraction: [bambuproject.py get_project_info()](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuproject.py#L105) lines 213-221
- Mapping usage: [bambuprinter.py print_3mf_file()](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py#L535) lines 602-603

**Authoritative Implementation**: [ha-bambulab PrintJob._update_task_data_from_printer_worker()](https://github.com/greghesp/ha-bambulab/blob/main/custom_components/bambu_lab/pybambu/models.py#L2800) shows how AMS mapping is used to correlate filament usage with AMS trays during printing

---

### Print 3MF File

**MQTT Topic**: `device/{serial}/request`

**Command Name**: `project_file`

**Message Structure** (generated by `print_3mf_file()`):
```json
{
  "print": {
    "file": "/cache/my_project.3mf",
    "url": "ftp:///cache/my_project.3mf",
    "subtask_name": "my_project",
    "bed_type": "textured_plate",
    "use_ams": true,
    "ams_mapping": [0, -1, 2, -1],
    "bed_leveling": true,
    "flow_cali": true,
    "timelapse": false,
    "param": "/profile_cali/cali_model_params#1.txt"
  }
}
```

**Fields**:

| Field | Type | Range/Example | Purpose |
|-------|------|-------------|---------|
| `file` | string | `/cache/my.3mf` | Path to 3MF file on printer SD card |
| `url` | string | `ftp:///cache/my.3mf` | FTP URL reference to file |
| `subtask_name` | string | Project filename | Human-readable project name |
| `bed_type` | string | `textured_plate`, `cool_plate`, `hot_plate` | Print bed surface type |
| `use_ams` | boolean | `true`, `false` | Whether to use AMS system |
| `ams_mapping` | array of int | `[0,-1,2,-1]` | Absolute tray ID per filament (0-103=4-slot units, 128-135=1-slot units, -1=unmapped) |
| `bed_leveling` | boolean | `true`, `false` | Enable auto bed leveling |
| `flow_cali` | boolean | `true`, `false` | Enable extrusion flow calibration |
| `timelapse` | boolean | `true`, `false` | Enable timelapse photography |
| `param` | string | Path template | Calibration parameter file path |

**Data Dictionary Correlation**: [`ProjectInfo.metadata.filament` and `ProjectInfo.metadata.ams_mapping`](data-dictionary.md#projectinfo)

**AMS Mapping Correlation**: The `ams_mapping` array must be sourced from `ProjectInfo.metadata['ams_mapping']`. See [AMS Filament/Spool Mapping Reference](#ams-filamentspool-mapping-reference) above for complete correlation logic.

**Python Method**: `BambuPrinter.print_3mf_file(name, plate, bed, use_ams, ams_mapping, bedlevel, flow, timelapse)`

**Example Usage**:
```python
from bpm.bambutools import PlateType
from bpm.bambuproject import get_project_info

# Get project metadata from 3MF file
project_info = get_project_info("/cache/my_project.3mf", printer, plate_num=1)

# Start print using metadata
import json
ams_mapping_str = json.dumps(project_info.metadata['ams_mapping'])
printer.print_3mf_file(
    name=project_info.id,
    plate=1,
    bed=PlateType.TEXTURED_PLATE,
    use_ams=True,
    ams_mapping=ams_mapping_str  # Passes filament-to-AMS mapping
)
```

---

### Chamber Air Conditioning Mode

**MQTT Topic**: `device/{serial}/request`

**Command Name**: `set_airduct`

**Message Structure**:
```json
{
  "print": {
    "command": "set_airduct",
    "modeId": 1,
    "sequence_id": "0"
  }
}
```

**Fields:**

| Field | Type | Range | Purpose |
|-------|------|-------|---------|
| `modeId` | integer | 0-3 | AC mode: 0=Off, 1=Cool, 2=Dry, 3=Auto |

**Data Dictionary Correlation**: [`airduct_mode`](data-dictionary.md#bambuclimate)

**Data Dictionary Reference**: Related to [BambuClimate](data-dictionary.md#bambuclimate) AC control

**Data Dictionary Correlation**: `airduct_mode`

**Note**: This command is automatically sent within `set_chamber_temp_target()` based on temperature thresholds. No standalone method exists.

---

### Buildplate Marker Detection

**MQTT Topic**: `device/{serial}/request`

**Command Name**: `xcam_control_set`

**Message Structure**:
```json
{
  "xcam": {
    "command": "xcam_control_set",
    "control": true,
    "enable": true,
    "module_name": "buildplate_marker_detector",
    "print_halt": true,
    "sequence_id": "0"
  }
}
```

**Fields:**

| Field | Type | Value | Purpose |
|-------|------|-------|---------|
| `module_name` | string | `"buildplate_marker_detector"` | Specifies marker detection module |
| `enable` | boolean | `true`/`false` | Enable/disable marker detection |
| `control` | boolean | `true`/`false` | Control flag |
| `print_halt` | boolean | `true` | Halt print on marker detection |

**Data Dictionary Reference**: Related to [BambuState](data-dictionary.md#bambustate) sensor configuration

**Data Dictionary Correlation**: `buildplate_marker_detector`

**Python Method**: `BambuPrinter.set_buildplate_marker_detector(enabled: bool)`

---

### Chamber Light Control

**MQTT Topic**: `device/{serial}/request`

**Command Name**: `ledctrl`

**Message Structure**:
```json
{
  "system": {
    "sequence_id": "0",
    "command": "ledctrl",
    "led_node": "chamber_light",
    "led_mode": "on",
    "led_on_time": 500,
    "led_off_time": 500,
    "loop_times": 0,
    "interval_time": 0
  }
}
```

**Fields:**

| Field | Type | Value | Purpose |
|-------|------|-------|---------|
| `led_node` | string | `"chamber_light"`, `"chamber_light2"` | Which light to control |
| `led_mode` | string | `"on"`, `"off"` | Light state |
| `led_on_time` | integer | milliseconds | Duration light stays on (when blinking) |
| `led_off_time` | integer | milliseconds | Duration light stays off (when blinking) |
| `loop_times` | integer | 0 = infinite | Number of blink cycles (0 = steady state) |
| `interval_time` | integer | milliseconds | Interval between blinks |

**Implementation Notes**:
- The printer sends both `chamber_light` and `chamber_light2` commands to ensure all chamber lights are toggled
- When `led_mode` is `"on"` or `"off"`, the other timing parameters are typically ignored (steady state)
- The light state property toggles ALL chamber lights on the machine

**Data Dictionary Reference**: Related to [BambuState.light_state](data-dictionary.md#bambustate)

**Python Method**: `BambuPrinter.light_state` (property getter/setter)

**Example Usage**:
```python
printer.light_state = True   # Turn on all chamber lights
printer.light_state = False  # Turn off all chamber lights
is_on = printer.light_state  # Check if lights are on
```

---

## AMS User Settings

**MQTT Topic**: `device/{serial}/request`

**Command Name**: `ams_user_setting`

**Message Structure**:
```json
{
  "print": {
    "ams_id": 0,
    "command": "ams_user_setting",
    "sequence_id": "0",
    "calibrate_remain_flag": true,
    "startup_read_option": true,
    "tray_read_option": true
  }
}
```

**Fields:**

| Field | Type | Value | Purpose |
|-------|------|-------|---------|
| `startup_read_option` | boolean | `true`/`false` | Read AMS on printer startup |
| `tray_read_option` | boolean | `true`/`false` | Read tray RFID on load |
| `calibrate_remain_flag` | boolean | `true`/`false` | Track filament calibration history |

**Data Dictionary Reference**: Related attributes in [AMSUnitState](data-dictionary.md#amsunitstate) user preferences

**Data Dictionary Correlation**:
- `calibrate_remain_flag`
- `startup_read_option`
- `tray_read_option`

**Python Method**: `BambuPrinter.set_ams_user_setting(setting: AMSUserSetting, enabled: bool, ams_id: int = 0)`

---

## AMS Control Commands

**MQTT Topic**: `device/{serial}/request`

**Command Name**: `ams_control`

**Message Structure**:
```json
{
  "print": {
    "sequence_id": "0",
    "command": "ams_control",
    "param": "resume"
  }
}
```

**Fields:**

| Field | Type | Value | Purpose |
|-------|------|-------|---------|
| `param` | string | `"resume"`, `"pause"`, `"reset"` | AMS control action |

**Data Dictionary Correlation**: [`ams_status_raw`](data-dictionary.md#amsunitstate), [`ams_status_text`](data-dictionary.md#amsunitstate)

**Data Dictionary Reference**: Related to [AMSUnitState](data-dictionary.md#amsunitstate) status management

**Data Dictionary Correlation**: `ams_units[].ams_status`

**Python Method**: `BambuPrinter.send_ams_control_command(ams_control_cmd: AMSControlCommand)`

**Example Usage**:
```python
from bpm.bambutools import AMSControlCommand
printer.send_ams_control_command(AMSControlCommand.PAUSE)
printer.send_ams_control_command(AMSControlCommand.RESUME)
printer.send_ams_control_command(AMSControlCommand.RESET)
```

---

### AMS Get RFID

**MQTT Topic**: `device/{serial}/request`

**Command Name**: `ams_get_rfid`

**Message Structure**:
```json
{
  "print": {
    "sequence_id": "0",
    "command": "ams_get_rfid",
    "ams_id": 0,
    "slot_id": 0
  }
}
```

**Fields:**

| Field | Type | Range | Purpose |
|-------|------|-------|---------|
| `ams_id` | integer | 0-3 | Target AMS unit (4 max per printer) |
| `slot_id` | integer | 0-3 | Slot within AMS to read (4 slots per unit) |

**Data Dictionary Correlation**: [`BambuSpool`](data-dictionary.md#bambuspool) attributes populated from RFID read

**Data Dictionary Reference**: Related attributes in [BambuSpool](data-dictionary.md#bambuspool) section (filament_id, color, nozzle temps, etc.)

**Python Method**: `BambuPrinter.refresh_spool_rfid(slot_id: int, ams_id: int = 0)`

**Example Usage**:
```python
printer.refresh_spool_rfid(slot_id=2, ams_id=0)  # Read RFID from AMS 0, Slot 2
```

---

### Extrusion Calibration Profile

**MQTT Topic**: `device/{serial}/request`

**Command Name**: `extrusion_cali_sel`

**Message Structure**:
```json
{
  "print": {
    "sequence_id": "0",
    "command": "extrusion_cali_sel",
    "ams_id": 0,
    "tray_id": 0,
    "slot_id": 0,
    "cali_idx": -1
  }
}
```

**Fields:**

| Field | Type | Value | Purpose |
|-------|------|-------|---------|
| `ams_id` | integer | 0-3, 254, 255 | Source AMS unit (254/255 = external spool) |
| `tray_id` | integer | 0-3, 254, 255 | Tray/spool ID (derived from slot or external index) |
| `slot_id` | integer | 0-3 | Slot within AMS (slot_id = tray_id % 4) |
| `cali_idx` | integer | -1 or 0+ | Calibration profile index (-1 = use default) |

**Implementation Notes**:
- For external spools (254/255), `cali_idx` is set directly
- For AMS slots, `ams_id` is calculated as `floor(tray_id / 4)`
- The printer uses the selected calibration profile to adjust extrusion on the next print with that filament

**Data Dictionary Correlation**: Related to [ExtruderState.k_factor_profile](data-dictionary.md#extruderstate) and spool calibration data

**Data Dictionary Reference**: Related attributes in [BambuSpool](data-dictionary.md#bambuspool) extrusion calibration section

**Python Method**: `BambuPrinter.select_extrusion_calibration_profile(tray_id: int, cali_idx: int = -1)`

**Example Usage**:
```python
printer.select_extrusion_calibration_profile(tray_id=2)  # Use default profile for slot 2
printer.select_extrusion_calibration_profile(tray_id=254, cali_idx=5)  # Use profile 5 for external spool
```

---

## Data Flow Example

**Scenario**: Change active filament, set nozzle temperature, and start a print

```python
from bpm.bambutools import PlateType, AMSUserSetting, PrintOption

# Enable auto-switch filament
printer.set_print_option(PrintOption.AUTO_SWITCH_FILAMENT, True)

# Load filament from AMS 0, Slot 1 to Extruder 0
printer.load_filament(ams_id=0, slot_id=0, extruder_id=0)

# Set nozzle temperature for the loaded filament
printer.set_nozzle_temp_target(220)

# Set bed temperature
printer.set_bed_temp_target(60)

# Chamber temperature (if supported)
printer.set_chamber_temp_target(35)

# Start print with AMS mapping
printer.print_3mf_file(
    name="/jobs/model.gcode.3mf",
    plate=1,
    bed=PlateType.HOT_PLATE,
    use_ams=True,
    ams_mapping="[0,-1,-1,-1]",  # Use AMS 0 only
    bedlevel=True,
    flow=True,
    timelapse=False
)
```

**MQTT Messages Generated** (in order):

1. **Enable auto-switch filament**:
   ```json
   {"print": {"command": "print_option", "sequence_id": "0", "auto_switch_filament": "true"}}
   ```

2. **Load filament**:
   ```json
   {"print": {"command": "ams_change_filament", "ams_id": 0, "slot_id": 0, "target": 0, ...}}
   ```

3. **Set nozzle temp**:
   ```json
   {"print": {"command": "gcode_line", "param": "M104 S220\n", "sequence_id": "0"}}
   ```

4. **Set bed temp**:
   ```json
   {"print": {"command": "gcode_line", "param": "M140 S60\n", "sequence_id": "0"}}
   ```

5. **Set chamber temp**:
   ```json
   {"print": {"command": "set_ctt", "ctt_val": 35, "sequence_id": "0"}}
   ```

6. **Start print**:
   ```json
   {"print": {"command": "project_file", "url": "ftp:///jobs/model.gcode.3mf", ...}}
   ```

---

## Error Handling

### Sequence ID Tracking

While the library currently uses `"0"` for all sequence IDs, the printer acknowledges commands and can track them via `sequence_id`. For production implementations, increment `sequence_id` for each command to enable request/response correlation.

### Message Validation

- All messages must be valid JSON
- Required fields vary by command type - use provided templates
- Deep copy templates before modification to avoid state contamination

### MQTT Topic Permissions

- **Publish**: `device/{serial}/request` - Send commands from client
- **Subscribe**: `device/{serial}/report` - Receive all telemetry (including push_status messages)

---

## Reference

### Internal Documentation

- **Source**: [bambucommands.py](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambucommands.py)
- **Implementation**: [bambuprinter.py](https://github.com/synman/bambu-printer-manager/blob/devel/src/bpm/bambuprinter.py)
- **Data Dictionary**: [data-dictionary.md](data-dictionary.md)
- **API Reference**: [api-reference.md](api-reference.md)

### External Reference Implementations

- **[BambuStudio](https://github.com/bambulab/BambuStudio)** - Official Bambu Lab client with protocol definitions
- **[OrcaSlicer](https://github.com/OrcaSlicer/OrcaSlicer)** - Community fork with enhanced telemetry
- **[ha-bambulab](https://github.com/greghesp/ha-bambulab)** - Home Assistant integration
- **[ha-bambulab pybambu](https://github.com/greghesp/ha-bambulab/tree/main/custom_components/bambu_lab/pybambu)** - Python MQTT client
- **[Bambu-HomeAssistant-Flows](https://github.com/WolfwithSword/Bambu-HomeAssistant-Flows)** - Workflow patterns
- **[OpenBambuAPI](https://github.com/Doridian/OpenBambuAPI)** - Alternative API implementation
- **[X1Plus](https://github.com/X1Plus/X1Plus)** - Community firmware analysis
- **[bambu-node](https://github.com/THE-SIMPLE-MARK/bambu-node)** - Node.js implementation

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.2 | 2026-02-25 | Added 4 missing commands: AMS Get RFID, Chamber Light Control, Extrusion Calibration Profile, Set Print Speed Profile |
| 1.1 | 2026-02-25 | Added auto_switch_filament to Set Print Options; updated reference implementations; comprehensive external sources |
| 1.0 | 2026-02-23 | Initial comprehensive MQTT protocol reference |
