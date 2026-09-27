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
| [Clear Print Error](#clear-print-error) | Print Job | Clear an active print_error and its UI acknowledgment |
| [Exhaust Fan](#exhaust-fan) | Fan | Set exhaust fan speed |
| [Extrusion Calibration Profile](#extrusion-calibration-profile) | Calibration | Select extrusion calibration profile for tray |
| [Extrusion Cali Set (Spool K Factor)](#extrusion-cali-set-spool-k-factor) | Calibration | Deprecated: set a tray's linear-advance k factor |
| [Load Filament / Change Filament](#load-filament-change-filament) | Filament | Load or change filament in AMS slot |
| [Pause Print](#pause-print) | Print Job | Pause the current print job |
| [Part Cooling Fan (Layer Cooling)](#part-cooling-fan-layer-cooling) | Fan | Set part cooling fan speed |
| [Refresh Nozzle State](#refresh-nozzle-state) | Extruder | Request the printer push current nozzle state |
| [Rename Printer](#rename-printer) | System | Rename the printer |
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
| [X-Cam Detectors (Spaghetti / Purge-Chute / Nozzle-Clumping / Air-Printing)](#x-cam-detectors) | Settings | Enable/disable AI-vision print-failure detectors |

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
| `url` | string | `"ftp:///path.3mf"` | FTP URL to print file on SD card. **A1/P1 series only**: `bpm` sends `file:///sdcard{path}` instead of an `ftp://` URL. |
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

### Clear Print Error

**MQTT Topic**: `device/{serial}/request`

Clearing an active `print_error` is two separate commands:

**1. `clean_print_error` (`print` namespace)** — clears the error itself:
```json
{
  "print": {
    "sequence_id": "0",
    "command": "clean_print_error",
    "subtask_id": "",
    "print_error": 50348044
  }
}
```

| Field | Type | Purpose |
|-------|------|---------|
| `subtask_id` | string | The failed job's subtask id (from `ActiveJobInfo`), or `""` to clear without a specific job context |
| `print_error` | integer | The error code to clear (e.g. `50348044` = `0x0300400C`, "task was canceled"), or `0` to clear any active error |

**Python Method**: `BambuPrinter.clean_print_error(subtask_id: str = "", print_error: int = 0)`

**2. `uiop` (`system` namespace)** — the UI dialog-close acknowledgment Bambu Studio sends alongside it. Without this, the printer stays in a "waiting for UI acknowledgment" state and any open Bambu Studio session will re-raise `print_error` on every `push_status` until it is received:
```json
{
  "system": {
    "sequence_id": "0",
    "command": "uiop",
    "name": "print_error",
    "action": "close",
    "source": 1,
    "type": "dialog",
    "err": "0300400C"
  }
}
```

| Field | Type | Purpose |
|-------|------|---------|
| `err` | string | The error code being cleared, as an uppercase 8-character hex string (`f"{print_error:08X}"`) |

**Python Method**: `BambuPrinter.clean_print_error_uiop(print_error: int = 0)` — always call this immediately after `clean_print_error()` to ensure the error stays cleared.

Source: Bambu Studio `src/slic3r/GUI/DeviceManager.cpp`, `command_clean_print_error_uiop()`.

**Example Usage**:
```python
printer.clean_print_error(print_error=50348044)
printer.clean_print_error_uiop(print_error=50348044)
```

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
| `ams_id` | integer | 0-3, 128+, 254, 255 | AMS unit (0-3 AMS / AMS 2 Pro / AMS Lite, 128+ AMS HT), or an external holder: 254 (the left/deputy holder, or the only one), 255 (the right/main holder of a dual-nozzle printer) |
| `slot_id` | integer | 0-3, 255 | Slot within the unit (0 for an AMS HT or a holder); 255 marks an unload |
| `target` | integer | 0-15, 128+, 254, 255 | Load: the absolute tray id `ams_id * 4 + slot_id` for an AMS unit, else `ams_id` itself (AMS HT, holders). Unload: 255 |
| `soft_temp` | integer | 0 | Softening temperature (currently unused) |
| `tar_temp` | integer | -1, 210 | Target temperature: -1 (auto) on a bpm load, 210 on an unload |
| `curr_temp` | integer | -1, 210 | Current temperature: -1 (auto) on a bpm load, 210 on an unload |

**Data Dictionary Correlation**: [`active_tray_id`](data-dictionary.md#amsunitstate), [`active_tray_state`](data-dictionary.md#amsunitstate), [`ams_units[].trays[].active`](data-dictionary.md#amsunitstate)

**Data Dictionary Reference**: Related attributes in [AMSUnitState](data-dictionary.md#amsunitstate) section

Encoding source: Bambu Studio `MachineObject::command_ams_change_filament` (`src/slic3r/GUI/DeviceManager.cpp`) and its callers in `StatusPanel.cpp`, read 2026-09-26 from the `master` branch. For a holder load Studio sends `ams_id` 254 or 255 with `slot_id` 0, so `target` is 254 or 255. Studio's unload is `slot_id` 255 with `target` 255 and the unit's `ams_id`, so a holder load must never be sent as `slot_id` 255.

**Python Method**: `BambuPrinter.load_filament(slot_id: int, ams_id: int = 0)` (a holder may also be passed as `slot_id` 254/255)

**Example Usage**:
```python
printer.load_filament(2, 0)      # AMS 0 slot 2: ams_id 0, slot_id 2, target 2
printer.load_filament(1, 1)      # AMS 1 slot 1: ams_id 1, slot_id 1, target 5
printer.load_filament(0, 128)    # AMS HT: ams_id 128, slot_id 0, target 128
printer.load_filament(254)       # left/only holder: ams_id 254, slot_id 0, target 254
printer.load_filament(0, 255)    # right holder (dual nozzle): ams_id 255, slot_id 0, target 255
```

**Reply**: the printer answers on `device/{serial}/report` with the same command name. A refusal carries `result: fail` and an `err_code` that `HMS_STATUS` `device_error` explains. Captured on an H2D, 2026-09-26, loading from an AMS HT that was drying:

```json
{"print": {"command": "ams_change_filament", "ams_id": 128, "slot_id": 0, "target": 0,
           "result": "fail", "err_code": 83935311, "errno": -9, "is_from_mqtt": true,
           "sequence_id": "0", "soft_temp": 0, "tar_temp": -1, "curr_temp": -1}}
```

`83935311` is `0x0500C04F`: "The AMS is drying and cannot perform this operation at the moment." `print_error` and `hms` do not change. bpm adds it to `BambuState.hms_errors` as a `command_error` entry (see the [data dictionary](data-dictionary.md#hms_errors)). An unload uses the same command with `slot_id` and `target` 255 and `curr_temp`/`tar_temp` 210, Studio's defaults; `unload_filament(ams_id)` names the unit. The A1 refuses an unload without the temperatures (`result: fail`, `reason: "error string"`, no `err_code`; measured 2026-09-26), while the H2D accepts one.

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
    "tray_id_name": "",
    "tray_info_idx": "GFL99",
    "tray_type": "NORMAL"
  }
}
```

**Fields:**

| Field | Type | Example | Purpose |
|-------|------|---------|---------|
| `ams_id` | integer | 0 | AMS unit, derived from `tray_id` (`floor(tray_id / 4)`). For `tray_id` 254/255 this becomes `ams_id` 254/255 too — **except** a single-nozzle printer's external spool (`tray_id` 254), which is sent as `ams_id` **255** (the A1 ignores the command at `ams_id` 254; only the A1 has been measured). |
| `slot_id` | integer | 0-3 | Slot within AMS, `tray_id % 4` (`0` for `tray_id` 254/255) |
| `tray_id` | integer | 0-15 or 254/255 | Absolute tray ID as passed by the caller (254=external deputy/left or the only holder, 255=external main/right) |
| `tray_id_name` | string | `""` | Friendly filament name, passed through unchanged (`""` when omitted) |
| `tray_info_idx` | string | `"GFL99"` | Filament type ID from printer database. `"no_filament"` clears the tray: the library resets `tray_id_name`/`tray_type` to `""`, `tray_color` to `"FFFFFF00"`, and both temps to `0` before sending. |
| `tray_type` | string | `"NORMAL"` | Filament material type |
| `tray_color` | string | `"FF0000FF"` | RGBA hex color (RedGreenBlueAlpha). Only a CSS color name (e.g. `"red"`) is converted, via `webcolors.name_to_hex()` + an appended `"FF"` alpha byte, upper-cased. `webcolors.name_to_hex()` raises on any hex string, so a 6/8-hex-digit value (or anything else that isn't a recognized CSS name) falls into the `except` branch and is sent through completely unchanged — no alpha appended, no case change. Pass a full 8-digit `RRGGBBAA` hex string directly. |
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
    "filament": "PETG",
    "temp": 55,
    "cooling_temp": 45,
    "duration": 12,
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
| `filament` | string | `"PETG"` | Filament type being dried; Bambu Studio sends the tray's filament type, and the stop command sends `""` |
| `temp` | integer | 30-70°C | Drying temperature |
| `cooling_temp` | integer | 30-50°C | Cooling temperature after drying |
| `duration` | integer | 12 (hours) | How long to dry, in **hours**. Bambu Studio builds this field from its hour input (`CtrlAmsStartDryingHour`, `tag_duration_hour`). The remaining time the printer reports back (`dry_time`) is in minutes. |
| `humidity` | integer | 0-100% | Target humidity (for compatible sensors) |
| `rotate_tray` | boolean | `true` | Rotate tray during drying |
| `close_power_conflict` | boolean | `false` | Handle power conflicts |

**Data Dictionary Reference**: Related attributes in [AMSDryerState](data-dictionary.md#amsdryerstate) section for drying operations

**Data Dictionary Correlation**:
- `ams_units[ams_id].dryer.state` (OFF, CHECKING, DRYING, COOLING, STOPPING, ERROR); `dryer` is `None` on a unit without a dryer
- `ams_units[ams_id].temp_actual` (measured) and `ams_units[ams_id].dryer.temp_target` (the order)
- `ams_units[ams_id].dryer.remaining_minutes` (drying time remaining, in minutes)

**Python Method**: `BambuPrinter.turn_on_ams_dryer(target_temp, duration, target_humidity, cooling_temp, rotate_tray, ams_id, filament_type)`

**Example Usage**:
```python
printer.turn_on_ams_dryer(target_temp=55, duration=2, ams_id=0)  # Dry for 2 hours
```

---

## Accessory Control

### Set Nozzle Type & Diameter

**MQTT Topic**: `device/{serial}/request`

`BambuPrinter.set_nozzle_details(nozzle_diameter, nozzle_type, nozzle_flow=NozzleFlowType.STANDARD, extruder_id=-1)` sends one of two different commands depending on hardware, both notifying the firmware which nozzle is installed:

**Single-extruder printers — `set_accessories`**

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

| Field | Type | Example | Purpose |
|-------|------|---------|---------|
| `accessory_type` | string | `"nozzle"` | Type of accessory being configured |
| `nozzle_diameter` | float | 0.2, 0.4, 0.6, 0.8 | Nozzle diameter in mm (`NozzleDiameter` enum value) |
| `nozzle_type` | string | `"hardened_steel"`, `"stainless_steel"`, `"tungsten_carbide"`, `"brass"`, `"E3D"` | Nozzle material type, converted via `nozzle_type_to_telemetry()` |

**Dual-extruder printers (H2D / H2D Pro) — `set_nozzle`**

```json
{
  "print": {
    "command": "set_nozzle",
    "diameter": 0.4,
    "id": 0,
    "sequence_id": "0",
    "type": "HH01",
    "wear": 0
  }
}
```

| Field | Type | Example | Purpose |
|-------|------|---------|---------|
| `id` | integer | 0, 1 | Extruder the nozzle is installed in — `extruder_id`, or the currently active tool when `extruder_id` is `-1` |
| `diameter` | float | 0.4 | Nozzle diameter in mm |
| `type` | string | `"HH01"` | Encoded flow+material identifier built by `build_nozzle_identifier(nozzle_flow, nozzle_type, nozzle_diameter)` — e.g. flow `H` (high-flow) + material `01` (hardened steel) |
| `wear` | integer | 0 | Always sent as `0`; not settable via this method |

**Data Dictionary Reference**: Related configuration in [BambuState](data-dictionary.md#bambustate) section

**Data Dictionary Correlation**:
- `nozzle_diameter`
- `nozzle_type`

**Python Method**: `BambuPrinter.set_nozzle_details(nozzle_diameter, nozzle_type, nozzle_flow, extruder_id)`

**Example Usage**:
```python
from bpm.bambutools import NozzleDiameter, NozzleType, NozzleFlowType
printer.set_nozzle_details(NozzleDiameter.POINT_EIGHT_MM, NozzleType.HARDENED_STEEL)
# Dual-extruder printer, targeting the left extruder explicitly:
printer.set_nozzle_details(NozzleDiameter.POINT_FOUR_MM, NozzleType.HARDENED_STEEL, NozzleFlowType.HIGH_FLOW, extruder_id=1)
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
| `extruder_index` | integer | 0-1 | Which extruder (0=right/primary, 1=left/secondary on H2D — matches `ActiveTool.RIGHT_EXTRUDER`/`LEFT_EXTRUDER`) |

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

**Message Structure** — a single `set_print_option(PrintOption.AUTO_RECOVERY, True)` call:
```json
{
  "print": {
    "command": "print_option",
    "sequence_id": "0",
    "auto_recovery": true,
    "option": 1
  }
}
```

Only the field for the `PrintOption` just changed is set on a given call — the six options are never all present together, unlike a single combined payload. `auto_recovery` etc. are genuine JSON booleans (`true`/`false`); `option` is a genuine JSON integer (`1`/`0`), not a string.

**Implementation quirk**: unlike every other command template in `bambucommands.py`, `PRINT_OPTION_COMMAND` is **not** deep-copied before each publish — `set_print_option` mutates the same module-level dict object every call. A field set by an earlier call in the process's lifetime is never removed, so a later call for a *different* option republishes it too, still carrying its last value (e.g. calling `AUTO_RECOVERY` then `SOUND_ENABLE` sends `{"auto_recovery": true, "sound_enable": false, ...}` on the second call). `option` is likewise sticky once set. This is a property of the running process's call history, not of any single option.

**Fields:**

| Field | Type | Value | Purpose | Sent when |
|-------|------|-------|---------|-----------|
| `auto_recovery` | boolean | `true`/`false` | Resume print after power loss | `option == PrintOption.AUTO_RECOVERY` |
| `auto_switch_filament` | boolean | `true`/`false` | Auto-switch to another AMS slot when active spool runs out. Target slot must have the **same filament type AND color**. AMS-hosted spools only. | `option == PrintOption.AUTO_SWITCH_FILAMENT` |
| `filament_tangle_detect` | boolean | `true`/`false` | Pause if AMS sensors detect a tangle. AMS-only; no effect on external spool prints. | `option == PrintOption.FILAMENT_TANGLE_DETECT` |
| `sound_enable` | boolean | `true`/`false` | Beep for notifications | `option == PrintOption.SOUND_ENABLE` |
| `nozzle_blob_detect` | boolean | `true`/`false` | Legacy firmware-level nozzle blob detection. On supported printers, prefer xcam `nozzleclumping_detector` (adds sensitivity control). | `option == PrintOption.NOZZLE_BLOB_DETECT` |
| `air_print_detect` | boolean | `true`/`false` | Legacy firmware-level air-printing detection. On supported printers, prefer xcam `airprinting_detector` (adds sensitivity control). | `option == PrintOption.AIR_PRINT_DETECT` |
| `option` | integer | `1` / `0` | Set **only** alongside `auto_recovery` (`PrintOption.AUTO_RECOVERY`); every other `PrintOption` leaves it untouched (but still present if a prior call in the process set it — see the accumulation quirk above). |

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
| `param` | string | `"1"`, `"2"`, `"3"`, `"4"` | Speed profile preset — the `SpeedLevel` enum's integer value, as a string |

**Speed Profile Values** (`SpeedLevel` enum, also the value reported back in telemetry as `spd_lvl`):
- `"1"` - `QUIET` (silent mode: slowest, quietest, highest quality)
- `"2"` - `STANDARD` (balanced speed and quality)
- `"3"` - `SPORT` (faster speeds)
- `"4"` - `LUDICROUS` (highest speed, lowest quality)

**Data Dictionary Reference**: Does not directly correlate to state attributes (affects print behavior)

**Implementation Notes**:
- The profile is applied to the next print job
- Current print continues with existing speed settings
- Equivalent to selecting speed preset from printer display menu

**Python Method**: `BambuPrinter.speed_level` (property setter). Accepts a `SpeedLevel` enum member, an integer `1`–`4`, or a case-insensitive name string (`"quiet"`, `"standard"`, `"sport"`, `"ludicrous"`) — a string is resolved via `SpeedLevel[value.upper()]`, a lookup **by name**, so a digit string like `"2"` raises `KeyError`. The getter returns the `SpeedLevel` member for a recognised value, or the raw int otherwise (e.g. `0` before the first telemetry push).

**Example Usage**:
```python
from bpm.bambutools import SpeedLevel

printer.speed_level = SpeedLevel.SPORT   # enum member
printer.speed_level = 3                  # integer code — same effect
printer.speed_level = "sport"            # name string, case-insensitive
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

This section documents how `ProjectInfo.metadata`'s per-filament fields relate to the `ams_mapping` value that must actually be sent to `print_3mf_file()` / the `project_file` command.

**`metadata.ams_mapping` is NOT a usable tray assignment.** It is a placeholder in the SHAPE of `print_3mf_file`'s `ams_mapping` parameter only: index `id - 1` holds `str(id)` for every filament, and `"-1"` fills any gap. A `.3mf` carries no tray/slot assignment at all — the real mapping has to be built by the caller from the spools currently loaded on the printer, matched to each filament by type and color. `get_project_info()` does not perform this match; it only reports what the slicer recorded.

### Data Flow: Filament to Real AMS Tray Assignment

**Source**: [`ProjectInfo.metadata`](data-dictionary.md#projectinfo) populated via `get_project_info()` (`bambuproject.py`)

**Components**:

1. **Filament Array** (`metadata.filament`)
   - Source: `Metadata/slice_info.config` XML, parsed from `<filament>` elements
   - Fields per filament:
     - `id` (integer, 1-indexed): Position in slicer filament list (filament 1, 2, 3, etc.)
     - `type` (string): Material type (e.g., "ABS", "PLA")
     - `color` (string): Hex color code (e.g., "#87909A")
   - Order: Filaments listed in the order they appear in the 3MF slicer specification

2. **AMS Mapping Placeholder** (`metadata.ams_mapping`)
   - Format: `list[str]`, same length as `metadata.filament`
   - Array Index: 0-indexed position (maps to filament id minus 1)
   - Array Value: `str(id)` for every filament present, `"-1"` for gaps — **never** a real tray id
   - Real tray ids for the caller to construct instead, once matched to a loaded spool:
     - **Standard 4-slot units** (AMS 2 Pro, AMS Lite, N3F): `ams_id * 4 + slot_id` → 0–103
     - **Single-slot units** (AMS HT/N3S): `ams_id` (starting at 128) → 128–135
     - `254` / `255`: external spool holder (deputy/left, main/right) — see [Load Filament / Change Filament](#load-filament-change-filament)
     - `-1`: leave unmapped

3. **Logical Extruder Array** (`metadata.filament_extruders`)
   - Source: `filament_maps` in `Metadata/slice_info.config` — the field the slicer's color-distance matching actually populates, at index `id - 1`
   - This is a **1-based logical extruder number** (1 or 2 on H2D), not a tray id. Combined with `metadata.physical_extruder_map` (`0`=main/right, `1`=deputy/left; `[1, 0]` on H2D) it identifies which physical extruder each filament prints from — used internally by `print_3mf_file`'s external-spool branch (see `metadata.external_spool_trays`), not for AMS tray resolution.

### Example Correlation

Given this ProjectInfo metadata:
```json
{
  "filament": [
    {"id": 1, "type": "ABS", "color": "#87909A"},
    {"id": 2, "type": "PLA", "color": "#FFFFFF"},
    {"id": 3, "type": "ABS", "color": "#000000"}
  ],
  "ams_mapping": ["1", "2", "3"]
}
```
`ams_mapping` here says nothing about trays — it is the id-shaped placeholder described above. To print this job from AMS, the caller inspects `printer.printer_state.ams_units[*].trays[*]` for spools matching each filament's `type`/`color`, and builds the real mapping from what it finds (e.g. `"[0,-1,2]"` if filament 1 is loaded in AMS 0 slot 0, filament 2 has no match, and filament 3 is in AMS 0 slot 2).

### Python Usage

`metadata.ams_mapping` must **not** be passed through as-is. Resolve the real value from loaded spools first, then pass the result as a JSON string:
```python
from bpm.bambutools import PlateType

# resolved_mapping is built by the caller — e.g. "[0,-1,2]" — by matching
# project_info.metadata['filament'] entries to printer.printer_state spools,
# NEVER by copying project_info.metadata['ams_mapping'] verbatim.
printer.print_3mf_file(
    name="/cache/my_project.3mf",
    plate=1,
    bed=PlateType.TEXTURED_PLATE,
    use_ams=True,
    ams_mapping=resolved_mapping,
)
```

The printer uses the resolved mapping to:
1. Load the correct AMS trays before printing
2. Route material to the correct nozzle during multi-material prints
3. Handle external spool fallback when AMS is offline

### References

**Source Code**:
- Placeholder construction: `get_project_info()` in `bambuproject.py`
- Mapping consumption: `BambuPrinter.print_3mf_file()` in `bambuprinter.py`

**Authoritative Implementation**: [ha-bambulab PrintJob._update_task_data_from_printer_worker()](https://github.com/greghesp/ha-bambulab/blob/main/custom_components/bambu_lab/pybambu/models.py#L2800) shows an independent implementation resolving filament usage against AMS trays

---

### Print 3MF File

**MQTT Topic**: `device/{serial}/request`

**Command Name**: `project_file`

**Message Structure** (generated by `print_3mf_file()`, non-H2-family printer):
```json
{
  "print": {
    "file": "/cache/my_project.3mf",
    "url": "ftp:///cache/my_project.3mf",
    "subtask_name": "my_project",
    "bed_type": "textured_plate",
    "use_ams": true,
    "ams_mapping": [0, -1, 2, -1],
    "ams_mapping2": [{"ams_id": 0, "slot_id": 0}, {"ams_id": 255, "slot_id": 255}, {"ams_id": 0, "slot_id": 2}, {"ams_id": 255, "slot_id": 255}],
    "bed_leveling": true,
    "flow_cali": true,
    "timelapse": false,
    "param": "Metadata/plate_1.gcode"
  }
}
```

**Fields**:

| Field | Type | Range/Example | Purpose |
|-------|------|-------------|---------|
| `file` | string | `/cache/my.3mf` | Path to 3MF file on printer SD card |
| `url` | string | `ftp:///cache/my.3mf` | FTP URL reference to file. **A1/P1 series only**: `file:///sdcard/cache/my.3mf` instead. |
| `subtask_name` | string | Project filename | Human-readable project name, with a trailing `.3mf`/`.gcode` stripped from `name`'s basename |
| `bed_type` | string | `textured_plate`, `cool_plate`, `hot_plate` | Print bed surface type — `bed.name.lower()` |
| `use_ams` | boolean | `true`, `false` | Whether to use AMS system |
| `ams_mapping` | array of int | `[0,-1,2,-1]` | Absolute tray ID per filament (0-103=4-slot units, 128-135=1-slot units, -1=unmapped). For an external-spool print (`ams_mapping` empty/omitted and `use_ams=false`) this is instead a flat array of `-1`, sized per `has_dual_extruder`: a single-element `[-1]` on a single-nozzle printer, or one `-1` per plate filament (length of the resolved external-spool-tray list) on a dual-nozzle printer — see [Load Filament / Change Filament](#load-filament-change-filament) and `print_3mf_file`'s own docstring for the full external-spool encoding. |
| `ams_mapping2` | array of `{ams_id, slot_id}` | see above | Auto-generated from `ams_mapping` for firmware compatibility: `{"ams_id": tray_id // 4, "slot_id": tray_id % 4}` for a standard tray id, `{"ams_id": tray_id, "slot_id": 0}` for `254`/`255`/an AMS HT id, `{"ams_id": 255, "slot_id": 255}` for an unmapped (`-1`) filament. |
| `bed_leveling` | boolean or `0`/`1` | `true`, `false` | Enable auto bed levelling. **H2-family printers** (H2S, H2D, H2D Pro, H2C, X2D) send this — and `flow_cali`, `layer_inspect`, `vibration_cali` below — as integer `0`/`1` instead of a JSON boolean; `use_ams` and `timelapse` stay boolean on every model. |
| `flow_cali` | boolean or `0`/`1` | `true`, `false` | Enable extrusion flow calibration |
| `timelapse` | boolean | `true`, `false` | Enable timelapse photography |
| `param` | string | `Metadata/plate_1.gcode` | `Metadata/plate_#.gcode` with `#` replaced by the requested plate number |

**Data Dictionary Correlation**: [`ProjectInfo.metadata.filament`](data-dictionary.md#projectinfo)

**AMS Mapping Correlation**: `ams_mapping` must be **resolved by the caller from the printer's currently loaded spools**, never copied from `ProjectInfo.metadata['ams_mapping']` — that field is a filament-id-shaped placeholder, not a tray assignment. See [AMS Filament/Spool Mapping Reference](#ams-filamentspool-mapping-reference) above for the full explanation and worked example.

**Python Method**: `BambuPrinter.print_3mf_file(name, plate, bed, use_ams, ams_mapping, bedlevel, flow, timelapse)`

**Example Usage**:
```python
from bpm.bambutools import PlateType
from bpm.bambuproject import get_project_info

# Get project metadata from 3MF file
project_info = get_project_info("/cache/my_project.3mf", printer, plate_num=1)

# Match each project_info.metadata['filament'] entry to a spool currently loaded
# on the printer (by type + color) and build the REAL tray-id mapping — never
# json.dumps(project_info.metadata['ams_mapping']), which is a placeholder.
ams_mapping_str = "[0,-1,2]"  # resolved from printer.printer_state.ams_units, not from metadata

printer.print_3mf_file(
    name=project_info.id,
    plate=1,
    bed=PlateType.TEXTURED_PLATE,
    use_ams=True,
    ams_mapping=ams_mapping_str,
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
| `modeId` | integer | 0-1 | `AirConditioningMode` enum: `0`=`COOL_MODE`, `1`=`HEAT_MODE`. `set_chamber_temp_target()` only ever sends one of these two — never `2` or `3` — choosing `0` below 40 °C and `1` at or above it. |

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

### X-Cam Detectors

Four additional X-Cam AI-vision print-failure detectors share the same `xcam_control_set` command as buildplate marker detection above, differing only in `module_name` and by carrying a `halt_print_sensitivity` field:

| Detector | `module_name` | Python Method |
|---|---|---|
| Spaghetti / failed-print detector | `"spaghetti_detector"` | `BambuPrinter.set_spaghetti_detector(enabled, sensitivity)` |
| Purge-chute pile-up detector | `"pileup_detector"` | `BambuPrinter.set_purgechutepileup_detector(enabled, sensitivity)` |
| Nozzle-clumping / blob detector | `"clump_detector"` | `BambuPrinter.set_nozzleclumping_detector(enabled, sensitivity)` |
| Air-printing / no-extrusion detector | `"airprint_detector"` | `BambuPrinter.set_airprinting_detector(enabled, sensitivity)` |

**Message Structure**:
```json
{
  "xcam": {
    "command": "xcam_control_set",
    "control": true,
    "enable": true,
    "module_name": "spaghetti_detector",
    "print_halt": true,
    "halt_print_sensitivity": "medium",
    "sequence_id": "0"
  }
}
```

**Fields:**

| Field | Type | Value | Purpose |
|-------|------|-------|---------|
| `module_name` | string | see table above | Which detector this command targets |
| `enable` / `control` | boolean | `true`/`false` | Enable/disable the detector (both set to the same value) |
| `print_halt` | boolean | `true` | Always `true` — the print halts when the detector fires |
| `halt_print_sensitivity` | string | `"low"`, `"medium"` (default), `"high"` | `DetectorSensitivity` enum value |

**Data Dictionary Reference**: Related to [BambuState](data-dictionary.md#bambustate) sensor configuration (`config.spaghetti_detector`, `config.purgechutepileup_detector`, `config.nozzleclumping_detector`, `config.airprinting_detector`, and each detector's paired `_sensitivity` field)

**Python Method**: see table above. Each also persists its `enabled` state and `sensitivity` to the corresponding `BambuConfig` attributes.

**Example Usage**:
```python
from bpm.bambutools import DetectorSensitivity
printer.set_spaghetti_detector(True, DetectorSensitivity.HIGH)
printer.set_nozzleclumping_detector(True)  # sensitivity defaults to MEDIUM
```

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
| `led_node` | string | `"chamber_light"`, `"chamber_light2"`, `"column_light"` | Which light to control |
| `led_mode` | string | `"on"`, `"off"` | Light state |
| `led_on_time` | integer | milliseconds | Duration light stays on (when blinking) |
| `led_off_time` | integer | milliseconds | Duration light stays off (when blinking) |
| `loop_times` | integer | 0 = infinite | Number of blink cycles (0 = steady state) |
| `interval_time` | integer | milliseconds | Interval between blinks |

**Implementation Notes**:
- The `light_state` setter publishes three separate `ledctrl` commands in sequence — `led_node` `"chamber_light"`, then `"chamber_light2"`, then `"column_light"` — so all chamber and column lights toggle together
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

### Rename Printer

**MQTT Topic**: `device/{serial}/request`

**Command Name**: none — this is an `update` message, not a `print`/`system`/`xcam` command

**Message Structure**:
```json
{
  "update": {
    "name": "My H2D",
    "sequence_id": "0"
  }
}
```

**Fields:**

| Field | Type | Purpose |
|-------|------|---------|
| `name` | string | The new display name for the printer |

**Python Method**: `BambuPrinter.rename_printer(new_name: str)`

**Example Usage**:
```python
printer.rename_printer("My H2D")
```

---

### Refresh Nozzle State

**MQTT Topic**: `device/{serial}/request`

**Command Name**: `refresh_nozzle`

**Message Structure**:
```json
{"print": {"sequence_id": "0", "command": "refresh_nozzle"}}
```

Requests the printer push its current nozzle state in its next `push_status` message. Relevant only on models with `support_refresh_nozzle` capability (H2D, H2D Pro) where nozzles can be manually swapped.

**Python Method**: `BambuPrinter.refresh_nozzles()`

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
| `param` | string | `"resume"`, `"pause"`, `"reset"`, `"done"`, `"abort"` | AMS control action |

During a filament load, Bambu Studio's prompt buttons send this command alone: "Finished, Continue" and the Retry buttons send `resume`, "Filament Extruded, Continue" sends `done`, and "Abort" (the load view's "Stop") sends `abort`. The printer replies on the report topic, e.g. `{"command": "ams_control", "param": "resume", "result": "SUCCESS", "reason": "SUCCESS"}` (captured on an H2D 2026-09-26).

**Data Dictionary Correlation**: [`ams_status_raw`](data-dictionary.md#amsunitstate), [`ams_status_text`](data-dictionary.md#amsunitstate)

**Data Dictionary Reference**: Related to [AMSUnitState](data-dictionary.md#amsunitstate) status management

**Data Dictionary Correlation**: `ams_units[].ams_status`

**Python Method**: `BambuPrinter.send_ams_control_command(ams_control_cmd: AMSControlCommand, resume_print: bool = True)`. With `RESUME` it also sends a print `resume` unless `resume_print` is False. `BambuPrinter.send_hms_action(id)` presses a prompt button and sends only the `ams_control`.

**Example Usage**:
```python
from bpm.bambutools import AMSControlCommand
printer.send_ams_control_command(AMSControlCommand.PAUSE)
printer.send_ams_control_command(AMSControlCommand.RESUME)
printer.send_ams_control_command(AMSControlCommand.RESET)
printer.send_ams_control_command(AMSControlCommand.DONE)
printer.send_ams_control_command(AMSControlCommand.ABORT)
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

### Extrusion Cali Set (Spool K Factor)

**MQTT Topic**: `device/{serial}/request`

**Command Name**: `extrusion_cali_set`

!!! warning "Deprecated"
    Broken on recent Bambu firmware. Use [Extrusion Calibration Profile](#extrusion-calibration-profile) above instead.

**Message Structure** — `set_spool_k_factor` deep-copies the `EXTRUSION_CALI_SET` template and only overwrites the fields below the static `filaments` array; the `filaments` entry and top-level `nozzle_diameter` are always sent unchanged from the template, regardless of which tray is actually being calibrated:
```json
{
  "print": {
    "command": "extrusion_cali_set",
    "filaments": [
      {
        "ams_id": 0,
        "extruder_id": 1,
        "filament_id": "GFL99",
        "k_value": "0.015000",
        "n_coef": "0.000000",
        "name": "015_K",
        "nozzle_diameter": "0.6",
        "nozzle_id": "HH00-0.6",
        "setting_id": "GFSL99_06",
        "slot_id": 0,
        "tray_id": -1
      }
    ],
    "nozzle_diameter": "0.6",
    "sequence_id": "0",
    "tray_id": 0,
    "slot_id": 0,
    "k_value": 0.02,
    "n_coef": 1.399999976158142,
    "nozzle_temp": 220,
    "bed_temp": 60,
    "max_volumetric_speed": 12
  }
}
```

**Fields:**

| Field | Type | Purpose |
|-------|------|---------|
| `filaments` | array | Static template entry, sent unchanged on every call — not derived from the actual tray/filament being calibrated |
| `nozzle_diameter` (top-level) | string | Static template value (`"0.6"`), sent unchanged on every call |
| `tray_id` | integer | Absolute tray ID (`ams_id * 4 + slot_id`, or `254` for external) |
| `slot_id` | integer | `tray_id % 4` |
| `k_value` | float | Linear advance (pressure advance) k factor |
| `n_coef` | float | Pressure advance n coefficient (default `1.4`) |
| `nozzle_temp` | integer | Nozzle temperature in °C — only sent when not `-1` |
| `bed_temp` | integer | Bed temperature in °C — only sent when not `-1` |
| `max_volumetric_speed` | integer | Max volumetric speed — only sent when not `-1` |

**Python Method**: `BambuPrinter.set_spool_k_factor(tray_id, k_value, n_coef=1.4, nozzle_temp=-1, bed_temp=-1, max_volumetric_speed=-1)`. Not called by bambu-printer-app's `/api/set_spool_k_factor`, which is a no-op stub.

---

## Data Flow Example

**Scenario**: Change active filament, set nozzle temperature, and start a print

```python
from bpm.bambutools import PlateType, AMSUserSetting, PrintOption

# Enable auto-switch filament
printer.set_print_option(PrintOption.AUTO_SWITCH_FILAMENT, True)

# Load filament from AMS 0, Slot 0 (load_filament takes slot_id, ams_id — no extruder_id parameter)
printer.load_filament(slot_id=0, ams_id=0)

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
   {"print": {"command": "print_option", "sequence_id": "0", "auto_switch_filament": true}}
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
| 1.3 | 2026-09-27 | Verification pass against current source: added Clear Print Error, Rename Printer, Refresh Nozzle State, the dual-extruder `set_nozzle` command, X-Cam Detectors, and Extrusion Cali Set sections; corrected the extruder-index direction, print speed profile values/exposure, `airduct_mode`/chamber-light-node values, `print_option`'s real per-call boolean shape (and its shared-dict accumulation quirk), the AMS Filament/Spool Mapping Reference's description of `ams_mapping` (placeholder, not a real tray assignment), `ams_filament_setting`'s single-nozzle/color-conversion details, `NozzleDiameter`/`load_filament` example bugs, and `project_file`'s A1/P1 URL scheme, `ams_mapping2`, and H2-family integer typing |
| 1.2 | 2026-02-25 | Added 4 missing commands: AMS Get RFID, Chamber Light Control, Extrusion Calibration Profile, Set Print Speed Profile |
| 1.1 | 2026-02-25 | Added auto_switch_filament to Set Print Options; updated reference implementations; comprehensive external sources |
| 1.0 | 2026-02-23 | Initial comprehensive MQTT protocol reference |
