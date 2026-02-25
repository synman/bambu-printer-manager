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
    "use_ams": false,
    "ams_mapping": "[0,-1,-1,-1]",
    "bed_type": "auto",
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
| `ams_mapping` | string | `"[0,1,-1,-1]"` | JSON array mapping AMS slots to extruders (-1 = skip) |
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
- `[-1,-1,-1,-1]` = External spool only (no AMS)
- `[0,-1,-1,-1]` = AMS slot 1 only
- `[0,1,2,3]` = All 4 AMS slots
- `[-1,-1,-1,3]` = AMS slot 4 only

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
| `auto_switch_filament` | string | `"true"`/`"false"` | Auto-switch to backup filament |
| `filament_tangle_detect` | string | `"true"`/`"false"` | Pause if filament tangles |
| `sound_enable` | string | `"true"`/`"false"` | Beep for notifications |
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

**Data Dictionary Correlation**: None (direct execution)

**Python Method**: `BambuPrinter.skip_objects(objects: list)`

**Example Usage**:
```python
printer.skip_objects([0, 2, 4])  # Skip objects 1, 3, and 5
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
| 1.1 | 2026-02-25 | Added auto_switch_filament to Set Print Options; updated reference implementations; comprehensive external sources |
| 1.0 | 2026-02-23 | Initial comprehensive MQTT protocol reference |
