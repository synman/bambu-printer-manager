# Bambu Printer App - API Reference

## Overview

This REST API provides complete control over Bambu Lab printers via HTTP requests. Built with Flask and Socket.IO, powered by [bambu-printer-manager](https://github.com/synman/bambu-printer-manager), it exposes printer status, control commands, file management, and real-time telemetry data.

**Base URL**: `http://localhost:5000/api`

**Response Format**: All endpoints return JSON unless noted otherwise.

**Standard Success Response**: `{"status": "success"}`

**Standard Error Response**: `{"status": "error", "reason": "description"}`

---

## Table of Contents

- [Printer Status & Information](#printer-status-information)
- [Temperature Control](#temperature-control)
- [Fan Control](#fan-control)
- [Print Job Control](#print-job-control)
- [Filament Management](#filament-management)
- [File Management](#file-management)
- [Tool Control (Dual Extruder)](#tool-control-dual-extruder)
- [AMS Control](#ams-control)
- [Detection & Safety](#detection-safety)
- [Advanced Settings](#advanced-settings)
- [Telemetry & Data](#telemetry-data)
- [System & Diagnostics](#system-diagnostics)
- [Socket.IO Events](#socketio-events)
- [build\_all\_data() Response Schema](#build_all_data-response-schema)
- [Error Handling](#error-handling)
- [Environment Variables](#environment-variables)
- [Examples](#examples)
- [Related Resources](#related-resources)
- [Version History](#version-history)

---

## Printer Status & Information

### GET /api/printer

Returns the complete serialised `BambuPrinter` object via `BambuPrinter.toJson()`.

**Condition**: Both `printer.recent_update` and `printer.printer_state.spools` must be truthy (i.e. a healthy MQTT data stream has been established and at least one spool entry is present).

**Success Response** (`200 OK`): Full JSON document produced by `BambuPrinter.toJson()`, which recursively serialises all public attributes — `_config`, `_service_state`, `_printer_state`, `_active_job_info`, `_sdcard_contents`, `_sdcard_3mf_files`, etc.

**Error Response** (`304 Not Modified`):
```json
{"status": "error", "reason": "no data to send"}
```

---

### GET /api/health_check

Health check that always attempts to return printer JSON regardless of connection state.

**Logic**: If `not printer.recent_update and not printer.printer_state.spools` (both false at once), the response is assembled as a `500` error tuple; otherwise `200` success. In both cases `printer.toJson()` is appended to the response.

**Success Response** (`200 OK`):
```json
{
  "status": "success",
  "printer": { }
}
```
`printer` contains the full `BambuPrinter.toJson()` result.

**Error Response** (`500 Internal Server Error`) when no live data is available.

---

## Temperature Control

### GET /api/set_tool_target_temp

Set the nozzle temperature target for the currently active extruder.

**Library method**: `BambuPrinter.set_nozzle_temp_target(value, tool_num)`

The active tool index is read from `printer.printer_state.active_tool.value`:

- Single-extruder printers (`active_tool = -1`): sends `M104 S{temp}` (no `T` argument).
- H2D dual-extruder (`active_tool = 0` or `1`): sends `M104 S{temp} T{active_tool}`.

**Parameters**:

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `temp` | int | yes | `0` | Target nozzle temperature in °C. Values below 0 are clamped to 0. |

**Example**: `/api/set_tool_target_temp?temp=220`

**Response**: `{"status": "success"}`

---

### GET /api/set_bed_target_temp

Set the heated bed temperature target.

**Library method**: `BambuPrinter.set_bed_temp_target(value)`

**Parameters**:

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `temp` | int | yes | `0` | Target bed temperature in °C. |

**Example**: `/api/set_bed_target_temp?temp=60`

**Response**: `{"status": "success"}`

---

### GET /api/set_chamber_target_temp

Set the chamber temperature target.

**Library method**: `BambuPrinter.set_chamber_temp_target(value)`

If the printer has `capabilities.has_chamber_temp`, sends `SET_CHAMBER_TEMP_TARGET` followed by `SET_CHAMBER_AC_MODE` (mode `0` for targets below 40 °C, mode `1` for 40 °C and above). Otherwise only stores the value locally — used by the external `ChamberMonitor` integration.

**Parameters**:

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `temp` | int | yes | `0` | Target chamber temperature in °C. |

**Example**: `/api/set_chamber_target_temp?temp=45`

**Response**: `{"status": "success"}`

---

## Fan Control

### GET /api/set_fan_speed_target

Set part-cooling fan speed.

**Library method**: `BambuPrinter.set_part_cooling_fan_speed_target_percent(value)`

**Parameters**:

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `percent` | int | yes | `0` | Target speed as a percentage (0–100). |

**Example**: `/api/set_fan_speed_target?percent=75`

**Response**: `{"status": "success"}`

---

### GET /api/set_aux_fan_speed_target

Set auxiliary fan speed.

**Library method**: `BambuPrinter.set_aux_fan_speed_target_percent(value)`

**Parameters**:

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `percent` | int | yes | `0` | Target speed as a percentage (0–100). |

**Example**: `/api/set_aux_fan_speed_target?percent=50`

**Response**: `{"status": "success"}`

---

### GET /api/set_exhaust_fan_speed_target

Set exhaust/chamber fan speed.

**Library method**: `BambuPrinter.set_exhaust_fan_speed_target_percent(value)`

**Parameters**:

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `percent` | int | yes | `0` | Target speed as a percentage (0–100). |

**Example**: `/api/set_exhaust_fan_speed_target?percent=100`

**Response**: `{"status": "success"}`

---

## Print Job Control

### GET /api/print_3mf

Start a 3MF print job.

**Library method**: `BambuPrinter.print_3mf_file(name, plate, bed, use_ams, ams_mapping, bedlevel, flow, timelapse)`

**Parameters**:

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `filename` | string | yes | `""` | Full path to the `.3mf` file on the printer SD card (e.g. `/test.3mf`). |
| `platenum` | int | no | `0` | Plate index within the `.3mf` to print (0-based). |
| `plate` | string | **yes** | — | Plate/surface type. Must be a valid `PlateType` enum name: `AUTO`, `COOL_PLATE`, `ENG_PLATE`, `HOT_PLATE`, `TEXTURED_PLATE`, `NONE`. Omitting or supplying an invalid value causes a `500` error. |
| `use_ams` | bool | no | `false` | Pass `true` to enable AMS filament feeding. Exact string `"true"` required. |
| `ams_mapping` | string | no | `null` | JSON-encoded array of absolute tray IDs, one per filament slot. Values: `0–103` (4-slot AMS, `ams_id * 4 + slot_id`), `128–135` (single-slot AMS HT), `254` (external spool), `-1` (unmapped). Example: `"[0,4,-1]"`. |
| `bl` | bool | no | `false` | Pass `true` to enable bed levelling before print. |
| `flow` | bool | no | `false` | Pass `true` to enable flow-rate calibration before print. |
| `tl` | bool | no | `false` | Pass `true` to enable timelapse recording. |

**Example**:
```
/api/print_3mf?filename=/test.3mf&platenum=1&plate=COOL_PLATE&use_ams=true&ams_mapping=[0,4]&bl=true&flow=true&tl=false
```

**Response**: `{"status": "success"}`

---

### GET /api/pause_printing

Pause the current print job.

**Library method**: `BambuPrinter.pause_printing()`

**Response**: `{"status": "success"}`

---

### GET /api/resume_printing

Resume a paused print job.

**Library method**: `BambuPrinter.resume_printing()`

**Response**: `{"status": "success"}`

---

### GET /api/stop_printing

Cancel/stop the current print job.

**Library method**: `BambuPrinter.stop_printing()`

**Response**: `{"status": "success"}`

---

### GET /api/skip_objects

Skip one or more objects during an active print (uses the printer's exclude-object feature).

**Library method**: `BambuPrinter.skip_objects(objects)`

The `objects` list is split on commas and passed directly to the library. The integer `identify_id` values for each object are obtained from `get_3mf_props_for_file` → `metadata.map.bbox_objects[n].id`.

**Parameters**:

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `objects` | string | yes | `""` | Comma-separated list of integer object `identify_id` values to skip. |

**Example**: `/api/skip_objects?objects=1,3,7`

**Response**: `{"status": "success"}`

---

## Filament Management

### GET /api/load_filament

Load filament from the specified AMS slot or external spool.

**Library method**: `BambuPrinter.load_filament(slot_id)`

**Parameters**:

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `slot` | int | yes | `0` | AMS slot index (`0`–`3` within a unit) or `254` for external spool. Passed as `slot_id` to the library. |

**Example**: `/api/load_filament?slot=2`

**Response**: `{"status": "success"}`

---

### GET /api/unload_filament

Unload the currently loaded filament.

**Library method**: `BambuPrinter.unload_filament()`

**Response**: `{"status": "success"}`

---

### GET /api/refresh_spool_rfid

Request the printer to re-read the RFID tag for a specific AMS slot.

**Library method**: `BambuPrinter.refresh_spool_rfid(slot_id, ams_id=ams_id)`

Only RFID-equipped Bambu Lab spools carry tag data. The printer pushes updated telemetry after scanning, which triggers `on_printer_update` and a `printer_update` Socket.IO event.

**Parameters**:

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `slot_id` | int | yes | `0` | Slot position within the AMS unit (0–3). |
| `ams_id` | int | yes | `0` | AMS unit ID (typically 0–3). |

**Example**: `/api/refresh_spool_rfid?slot_id=1&ams_id=0`

**Response**: `{"status": "success"}`

---

### GET /api/set_spool_details

Set custom filament details for an AMS tray.

**Library method**: `BambuPrinter.set_spool_details(tray_id, tray_info_idx, tray_id_name, tray_type, tray_color, nozzle_temp_min, nozzle_temp_max)`

The endpoint sleeps 2 seconds after issuing the command to allow the printer to process the update before responding.

**Parameters**:

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `tray_id` | int | yes | `0` | Global tray ID. `0`–`15` for 4-slot AMS units; `254` or `255` for external spools. |
| `tray_info_idx` | string | yes | `""` | Bambu filament preset index (e.g. `GFL99`). |
| `tray_id_name` | string | no | `""` | Display name for the spool. Omit to leave unchanged. |
| `tray_type` | string | no | `""` | Filament material type string (e.g. `PLA`, `PETG-CF`). |
| `tray_color` | string | no | `""` | Spool colour as a hex string (e.g. `#FF5733`). |
| `nozzle_temp_min` | int | no | `-1` | Minimum recommended nozzle temperature in °C. Pass `-1` to leave unchanged. |
| `nozzle_temp_max` | int | no | `-1` | Maximum recommended nozzle temperature in °C. Pass `-1` to leave unchanged. |

**Example**:
```
/api/set_spool_details?tray_id=0&tray_info_idx=GFL99&tray_id_name=My%20PLA&tray_type=PLA&tray_color=%23FF5733&nozzle_temp_min=200&nozzle_temp_max=230
```

**Response** (after 2-second delay): `{"status": "success"}`

---

### GET /api/set_spool_k_factor

Stub endpoint — no operation is currently performed.

The implementation body is commented out in source. The endpoint accepts `tray_id` but ignores it and immediately returns success.

**Response**: `{"status": "success"}`

---

## File Management

All file operations use FTPS to communicate with the printer SD card.

### GET /api/get_sdcard_contents

Return the cached SD card file tree (populated by the last `get_sdcard_contents()` call).

**Library method**: `BambuPrinter.get_sdcard_contents()` — performs a live FTPS listing and updates the internal cache.

**Response**: Alphabetically sorted tree structure:
```json
{
  "name": "/",
  "id": "/",
  "children": [
    {
      "name": "Projects",
      "id": "/Projects/",
      "children": [
        {
          "name": "model.3mf",
          "id": "/Projects/model.3mf",
          "size": 1048576
        }
      ]
    },
    {
      "name": "test.3mf",
      "id": "/test.3mf",
      "size": 204800
    }
  ]
}
```

Folder nodes have a `children` array; file nodes have a `size` field (bytes). Folders sort before files at every level.

---

### GET /api/refresh_sdcard_contents

Refresh the SD card file listing from the printer via FTPS and return success.

**Library method**: `BambuPrinter.get_sdcard_contents()` — also rebuilds the 3MF-only cache.

**Response**: `{"status": "success"}`

---

### GET /api/get_sdcard_3mf_files

Return the SD card tree filtered to `.3mf` files only (all other file types stripped, empty folders retained).

**Library method**: `BambuPrinter.get_sdcard_3mf_files()` — also triggers a full `get_sdcard_contents()` refresh internally.

**Response**: Same tree structure as `get_sdcard_contents` but with non-`.3mf` files removed.

---

### GET /api/refresh_sdcard_3mf_files

Refresh the SD card listing (both full and 3MF-only caches) via FTPS and return success.

**Library method**: `BambuPrinter.get_sdcard_3mf_files()` which internally calls `get_sdcard_contents()`.

**Response**: `{"status": "success"}`

---

### GET /api/delete_sdcard_file

Delete a file or folder from the SD card via FTPS.

**Library method**: `BambuPrinter.delete_sdcard_file(file)` for files; `BambuPrinter.delete_sdcard_folder(path)` for folders (when `file` ends with `/`). The folder variant recursively deletes all contents before removing the directory.

After deletion, both the full file cache and the 3MF cache are updated in-memory. The response is the updated `_sdcard_contents` tree.

**Parameters**:

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `file` | string | yes | SD card path. Files: `/path/file.3mf`. Folders: `/path/folder/` (trailing slash selects folder deletion). |

**Example**: `/api/delete_sdcard_file?file=/old_print.3mf`

**Response**: Updated SD card file tree (same structure as `get_sdcard_contents`).

---

### GET /api/make_sdcard_directory

Create a new directory on the SD card via FTPS.

**Library method**: `BambuPrinter.make_sdcard_directory(dir)` — creates the directory then calls `get_sdcard_contents()`.

**Parameters**:

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `dir` | string | yes | Full path for the new directory (trailing slash recommended). |

**Example**: `/api/make_sdcard_directory?dir=/Projects/new_folder/`

**Response**: Updated SD card file tree (same structure as `get_sdcard_contents`).

---

### GET /api/rename_sdcard_file

Rename or move a file/folder on the SD card via FTPS.

**Library method**: `BambuPrinter.rename_sdcard_file(src, dest)` — renames then calls `get_sdcard_contents()`.

**Parameters**:

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `src` | string | yes | Source path on SD card. |
| `dest` | string | yes | Destination path on SD card. |

**Example**: `/api/rename_sdcard_file?src=/old.3mf&dest=/archive/old.3mf`

**Response**: Updated SD card file tree (same structure as `get_sdcard_contents`).

---

### POST /api/upload_file_to_host

Upload a file to the API server's local `./uploads/` directory.

Accepts both `GET` and `POST` methods; multipart form data is required in practice.

**Form Data**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `myFile` | file | yes | File to upload. Saved as `./uploads/{original filename}`. |

**Response**: `{"status": "success"}`

---

### GET /api/upload_file_to_printer

Transfer a file from the server's `./uploads/` directory to the printer SD card via FTPS.

**Library method**: `BambuPrinter.upload_sdcard_file(f"uploads/{src}", dest)` — uploads the file, then if it is a `.3mf` file runs `get_project_info` to cache its metadata, then calls `get_sdcard_contents()` to refresh the file tree.

Accepts both `GET` and `POST` methods.

**Parameters**:

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `src` | string | yes | Filename in the `./uploads/` directory (basename only). |
| `dest` | string | yes | Full destination path on SD card (e.g. `/prints/model.3mf`). |

**Example**: `/api/upload_file_to_printer?src=model.3mf&dest=/prints/model.3mf`

**Response**: Updated SD card file tree (same structure as `get_sdcard_contents`).

---

### GET /api/download_file_from_printer

Download a file from the printer SD card. The file is saved to `./uploads/` and then streamed to the client.

**Library method**: `BambuPrinter.download_sdcard_file(src, f"uploads/{filename}")`

Accepts both `GET` and `POST` methods.

**Parameters**:

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `src` | string | yes | Full path on the SD card (e.g. `/test.3mf`). The filename is extracted after the last `/`. |

**Example**: `/api/download_file_from_printer?src=/test.3mf`

**Response**: Binary file download (content-type determined by Flask's `send_from_directory`).

---

### GET /api/get_3mf_props_for_file

Parse and return metadata for a specific `.3mf` file.

**Library method**: `get_project_info(file, printer, plate_num=plate, use_cached_list=True)`

Returns a `dataclasses.asdict(ProjectInfo)` result.

**Parameters**:

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `file` | string | yes | `""` | Full SD card path to the `.3mf` file. |
| `plate` | int | no | `1` | Plate number to retrieve metadata for (1-based). |

**Example**: `/api/get_3mf_props_for_file?file=/test.3mf&plate=1`

**Success Response** (`200 OK`):
```json
{
  "id": "/test.3mf",
  "name": "test.3mf",
  "size": 204800,
  "timestamp": 1700000000,
  "md5": "A1B2C3D4...",
  "plate_num": 1,
  "plates": [1, 2],
  "metadata": {
    "thumbnail": "data:image/png;base64,...",
    "topimg": "data:image/png;base64,...",
    "filament": [
      {"id": 1, "type": "PLA", "color": "#FF0000"},
      {"id": 2, "type": "PETG", "color": "#0000FF"}
    ],
    "ams_mapping": ["0", "4", "-1"],
    "map": {
      "filament_ids": ["..."],
      "filament_colors": ["#FF0000", "#0000FF"],
      "bbox_objects": [
        {"id": 1, "name": "Part_1", "val": [0.0, 0.0, 50.0, 50.0]},
        {"id": 2, "name": "Support_1", "val": [0.0, 0.0, 50.0, 50.0]}
      ]
    }
  }
}
```

The `metadata.ams_mapping` values use the same encoding as `print_3mf`'s `ams_mapping` parameter: `0–103` for standard AMS slots, `128–135` for single-slot AMS HT units, `254` for external spool, `"-1"` for unmapped. Pass this list (JSON-serialised) directly to `print_3mf` as the `ams_mapping` parameter.

The `metadata.map.bbox_objects[n].id` integer is the `identify_id` required by `skip_objects`.

**Error Response** (`404 Not Found`):
```json
{"status": "error", "message": "No file found", "file": "/test.3mf"}
```

---

### GET /api/get_current_3mf_props

Return metadata for the currently active print job.

Checks `printer.active_job_info.project_info` and returns it if `project_info.id` is non-empty.

**Success Response** (`200 OK`): `dataclasses.asdict(ProjectInfo)` with `"status": "success"` merged in. Same schema as `get_3mf_props_for_file`.

**Error Response** (`404 Not Found`):
```json
{"status": "error", "message": "No Job Found"}
```

---

## Tool Control (Dual Extruder)

These endpoints are only meaningful on H2D / H2D Pro printers with dual extruders.

### GET /api/toggle_active_tool

Switch between right (`0`) and left (`1`) extruders on H2D / H2D Pro printers.

**Library method**: `BambuPrinter.set_active_tool(tool)`

Computes the target tool as `abs(active_tool.value - 1)`:

- If `active_tool` is `RIGHT_EXTRUDER (0)` → switches to `1` (left).
- If `active_tool` is `LEFT_EXTRUDER (1)` → switches to `0` (right).

**Response**: `{"status": "success"}`

---

### GET /api/set_nozzle_details

Set the nozzle diameter and material type for the active extruder.

**Library method**: `BambuPrinter.set_nozzle_details(nozzle_diameter, nozzle_type)`

The endpoint sleeps 1 second after issuing the command before responding.

`nozzle_diameter` is parsed via `NozzleDiameter(float(...))` and `nozzle_type` via `NozzleType[...]`. Supplying an invalid value for either raises a `ValueError` / `KeyError` which is caught by the `500` error handler.

**Parameters**:

| Name | Type | Required | Allowed values | Description |
|------|------|----------|----------------|-------------|
| `nozzle_diameter` | float | yes | `0.2`, `0.4`, `0.6`, `0.8` | Nozzle diameter in mm (`NozzleDiameter` enum values). |
| `nozzle_type` | string | yes | `STAINLESS_STEEL`, `HARDENED_STEEL`, `TUNGSTEN_CARBIDE`, `BRASS`, `E3D` | Nozzle material (`NozzleType` enum name). |

**Example**: `/api/set_nozzle_details?nozzle_diameter=0.4&nozzle_type=HARDENED_STEEL`

**Response** (after 1-second delay): `{"status": "success"}`

---

### GET /api/refresh_nozzles

Request the printer to push current nozzle info in its next `push_status` message.

**Library method**: `BambuPrinter.refresh_nozzles()`

Relevant only on models with `support_refresh_nozzle` capability (H2D, H2D Pro).

**Response**: `{"status": "success"}`

---

## Detection & Safety

### GET /api/set_buildplate_marker_detector

Enable or disable the build-plate marker detector.

**Library method**: `BambuPrinter.set_buildplate_marker_detector(enabled)`

**Parameters**:

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `enabled` | bool | yes | Exact string `"true"` enables; anything else disables. |

**Example**: `/api/set_buildplate_marker_detector?enabled=true`

**Response**: `{"status": "success"}`

---

### GET /api/set_spaghetti_detector

Enable or disable the spaghetti / first-layer failure detector.

**Library method**: `BambuPrinter.set_spaghetti_detector(enabled, sensitivity)`

**Parameters**:

| Name | Type | Required | Default | Allowed values | Description |
|------|------|----------|---------|----------------|-------------|
| `enabled` | bool | yes | — | `"true"` / other | Enable or disable. |
| `sensitivity` | string | no | `"medium"` | `"low"`, `"medium"`, `"high"` | Detection sensitivity (`DetectorSensitivity` string value). |

**Example**: `/api/set_spaghetti_detector?enabled=true&sensitivity=high`

**Response**: `{"status": "success"}`

---

### GET /api/set_purgechutepileup_detector

Enable or disable the purge-chute pile-up detector.

**Library method**: `BambuPrinter.set_purgechutepileup_detector(enabled, sensitivity)`

**Parameters**:

| Name | Type | Required | Default | Allowed values | Description |
|------|------|----------|---------|----------------|-------------|
| `enabled` | bool | yes | — | `"true"` / other | Enable or disable. |
| `sensitivity` | string | no | `"medium"` | `"low"`, `"medium"`, `"high"` | Detection sensitivity. |

**Example**: `/api/set_purgechutepileup_detector?enabled=true&sensitivity=medium`

**Response**: `{"status": "success"}`

---

### GET /api/set_nozzleclumping_detector

Enable or disable the nozzle-clumping detector.

**Library method**: `BambuPrinter.set_nozzleclumping_detector(enabled, sensitivity)`

**Parameters**:

| Name | Type | Required | Default | Allowed values | Description |
|------|------|----------|---------|----------------|-------------|
| `enabled` | bool | yes | — | `"true"` / other | Enable or disable. |
| `sensitivity` | string | no | `"medium"` | `"low"`, `"medium"`, `"high"` | Detection sensitivity. |

**Example**: `/api/set_nozzleclumping_detector?enabled=true&sensitivity=low`

**Response**: `{"status": "success"}`

---

### GET /api/set_airprinting_detector

Enable or disable the air-printing detector.

**Library method**: `BambuPrinter.set_airprinting_detector(enabled, sensitivity)`

**Parameters**:

| Name | Type | Required | Default | Allowed values | Description |
|------|------|----------|---------|----------------|-------------|
| `enabled` | bool | yes | — | `"true"` / other | Enable or disable. |
| `sensitivity` | string | no | `"medium"` | `"low"`, `"medium"`, `"high"` | Detection sensitivity. |

**Example**: `/api/set_airprinting_detector?enabled=true&sensitivity=medium`

**Response**: `{"status": "success"}`

---

## AMS Control

### GET /api/send_ams_control_command

Send a control command to the AMS system.

**Library method**: `BambuPrinter.send_ams_control_command(ams_cmd)`

The `cmd` value is resolved via `AMSControlCommand[cmd.upper()]`. Invalid names raise a `KeyError` → `500`.

**Parameters**:

| Name | Type | Required | Allowed values | Description |
|------|------|----------|----------------|-------------|
| `cmd` | string | yes | `PAUSE`, `RESUME`, `RESET` | AMS control command (`AMSControlCommand` enum name). |

**Example**: `/api/send_ams_control_command?cmd=RESET`

**Response**: `{"status": "success"}`

---

### GET /api/set_ams_user_setting

Configure an AMS user setting.

**Library method**: `BambuPrinter.set_ams_user_setting(setting, enabled)`

The `setting` value is resolved via `AMSUserSetting[setting.upper()]`. Invalid names raise a `KeyError` → `500`.

**Parameters**:

| Name | Type | Required | Allowed values | Description |
|------|------|----------|----------------|-------------|
| `setting` | string | yes | `CALIBRATE_REMAIN_FLAG`, `STARTUP_READ_OPTION`, `TRAY_READ_OPTION` | Setting to modify (`AMSUserSetting` enum name). |
| `enabled` | bool | yes | `"true"` / other | Enable or disable the setting. |

**Example**: `/api/set_ams_user_setting?setting=STARTUP_READ_OPTION&enabled=true`

**Response**: `{"status": "success"}`

---

## Advanced Settings

### GET /api/send_gcode

Send one or more raw G-code commands to the printer.

**Library method**: `BambuPrinter.send_gcode(gcode)` — wraps the command in `SEND_GCODE_TEMPLATE` and publishes via MQTT.

Pipe characters (`|`) in the `gcode` parameter are converted to newlines (`\n`) before being sent, allowing multiple commands in a single URL.

**Parameters**:

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `gcode` | string | yes | `""` | G-code string. Use `\|` in the URL to separate multiple commands. |

**Example**: `/api/send_gcode?gcode=G28|G1 Z10 F600|M104 S200`

**Response**: `{"status": "success"}`

!!! warning
    Direct G-code bypasses all safety interlocks. Incorrect commands can damage the printer.

---

### GET /api/set_print_option

Enable or disable a printer option.

**Library method**: `BambuPrinter.set_print_option(option, enabled)`

The `option` value is resolved via `PrintOption[option.upper()]`. Invalid names raise a `KeyError` → `500`.

**Parameters**:

| Name | Type | Required | Allowed values | Description |
|------|------|----------|----------------|-------------|
| `option` | string | yes | `AUTO_RECOVERY`, `FILAMENT_TANGLE_DETECT`, `SOUND_ENABLE`, `AUTO_SWITCH_FILAMENT`, `NOZZLE_BLOB_DETECT`, `AIR_PRINT_DETECT` | Option to modify (`PrintOption` enum name). |
| `enabled` | bool | yes | `"true"` / other | Enable or disable the option. |

**Example**: `/api/set_print_option?option=AUTO_RECOVERY&enabled=true`

**Response**: `{"status": "success"}`

---

### GET /api/set_light_state

Control the chamber and column LED lights.

**Library method**: `BambuPrinter.light_state = bool`

Setting the property publishes `CHAMBER_LIGHT_TOGGLE` commands for three light nodes: `chamber_light`, `chamber_light2`, and `column_light`.

**Parameters**:

| Name | Type | Required | Allowed values | Description |
|------|------|----------|----------------|-------------|
| `state` | string | yes | `"on"`, any other string | `"on"` turns all lights on; any other value turns them off. |

**Example**: `/api/set_light_state?state=on`

**Response**: `{"status": "success"}`

**Note**: The application also automatically controls lights based on print state transitions and chamber door sensor events (when `capabilities.has_chamber_door_sensor` is true).

---

### GET /api/set_speed_level

Set the print speed profile.

**Library method**: `BambuPrinter.speed_level = str`

Publishes `SPEED_PROFILE_TEMPLATE` with the string value directly as the `param` field.

**Parameters**:

| Name | Type | Required | Allowed values | Description |
|------|------|----------|----------------|-------------|
| `level` | string | yes | `"1"` (silent), `"2"` (standard), `"3"` (sport), `"4"` (ludicrous) | Speed profile index as a string. |

**Example**: `/api/set_speed_level?level=2`

**Response**: `{"status": "success"}`

---

## Telemetry & Data

### GET /api/get_all_data

Return the full telemetry history used for charting, combined with the current printer state.

Calls `build_all_data()` internally. See [build\_all\_data() Response Schema](#build_all_data-response-schema) for the complete schema.

**Response** (`200 OK`): `build_all_data()` result. See schema section below.

---

### GET /api/zoom_in

Zoom in on a telemetry chart (reduce the visible history window by 500 seconds per call).

Finds the named collection in `ds.collections` and decrements its `zoom` by 500 seconds. Minimum zoom window is 500 seconds. If the collection has fewer than 500 seconds of data, the call is a no-op.

If `zoom` is currently `0` (show all data), it is first set to `min(3600, max_age)` before decrementing.

**Parameters**:

| Name | Type | Required | Allowed values | Description |
|------|------|----------|----------------|-------------|
| `name` | string | yes | `tool`, `bed`, `chamber`, `fan`, `aux_fan`, `exhaust_fan`, `heatbreak_fan`, `tool_0`, `tool_1` | Collection name to zoom. Typically `tool`, `bed`, `chamber`, or `fan`. |

**Example**: `/api/zoom_in?name=tool`

**Response**: `{"status": "success", "printer": {}}`

---

### GET /api/zoom_out

Zoom out on a telemetry chart (increase the visible history window by 500 seconds per call).

If `zoom + 500 >= max_age`, zoom resets to `0` (show all data).

**Parameters**:

| Name | Type | Required | Allowed values | Description |
|------|------|----------|----------------|-------------|
| `name` | string | yes | `tool`, `bed`, `chamber`, `fan`, `aux_fan`, `exhaust_fan`, `heatbreak_fan`, `tool_0`, `tool_1` | Collection name to zoom. |

**Example**: `/api/zoom_out?name=bed`

**Response**: `{"status": "success", "printer": {}}`

---

### GET /api/dump_data_ds.collections

Dump all internal `DataCollection` objects as newline-delimited JSON (JSONL), one collection per line.

**Response**: Plain text, MIME type `application/jsonl+json`. Each line is one JSON-serialised `DataCollection` object.

---

## System & Diagnostics

### GET /api/toggle_session

Pause or resume the MQTT connection to the printer.

**Library methods**: `BambuPrinter.pause_session()` / `BambuPrinter.resume_session()`

- If `service_state` is `CONNECTED` → calls `pause_session()`.
- If `service_state` is `PAUSED` → calls `resume_session()`.

**Response**:
```json
{
  "status": "success",
  "state": "PAUSED"
}
```
`state` is the `ServiceState` enum name after the toggle: `"PAUSED"` or `"CONNECTED"`.

---

### GET /api/trigger_printer_refresh

Force a printer reconnection or refresh.

**Library methods**: `BambuPrinter.quit()` + `start_session()` when disconnected; `BambuPrinter.refresh()` when connected.

- If `service_state` is not `CONNECTED` and not `PAUSED`: calls `quit()`, waits 1 second, calls `start_session()`, then blocks until `CONNECTED`.
- Otherwise: calls `refresh()` to request a `push_status` from the printer.

**Response**: `{"status": "success", "printer": {}}`

Note: `printer` is always an empty dict in this response. Call `/api/printer` or `/api/get_all_data` for current state.

---

### GET /api/toggle_verbosity

Toggle the root logger between `DEBUG` and `INFO` level, and optionally set `config.verbose`.

The level always toggles based on the **current** level (not the `verbose` parameter): `INFO → DEBUG`, `DEBUG → INFO`. The `verbose` parameter independently sets `printer.config.verbose`.

**Parameters**:

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `verbose` | bool | no | `"false"` | Exact string `"true"` sets `printer.config.verbose = True`; anything else sets it `False`. Does **not** control which log level is selected. |

**Example**: `/api/toggle_verbosity?verbose=true`

**Response**:
```json
{
  "status": "success",
  "level": "DEBUG",
  "verbose": true
}
```
`level` is the new log level name (`"DEBUG"` or `"INFO"`). `verbose` mirrors the value passed in.

---

### GET /api/dump_log

Retrieve the contents of `./output.log`.

**Response**: Plain text, MIME type `application/jsonl+json`. Empty string if the file does not exist.

---

### GET /api/truncate_log

Clear (truncate to zero bytes) `./output.log`.

**Response**: `{"status": "success"}`

---

### GET /api/fake_error

Intentionally raise a `ZeroDivisionError` to test the `500` error handler.

**Response** (`500 Internal Server Error`):
```json
{
  "status": "error",
  "message": "ZeroDivisionError: division by zero",
  "stacktrace": "Traceback (most recent call last):\n  ..."
}
```

---

## Socket.IO Events

The server uses **Flask-SocketIO** with `async_mode="threading"` and `cors_allowed_origins="*"`. Connect to the server root at `http://localhost:5000` using any Socket.IO v4 client.

### Event: `printer_update`

**Direction**: Server → Client

**Trigger**: Emitted inside `on_printer_update(printer)` every time `BambuPrinter` calls its `on_update` callback. This happens on every incoming MQTT `push_status` message from the printer. It is also emitted by the `ChamberMonitor` thread when an external MQTT chamber temperature update is received.

Before emitting, `on_printer_update` performs several automatic side-effects:

- If `gcode_state` transitions to `"FINISH"` and `integrated_external_heater` is `True` and `chamber_temp_target != 0` → calls `set_chamber_temp_target(0)`.
- If `gcode_state` transitions to `"FINISH"` and the light is on → turns off the light.
- If `gcode_state` transitions to `"PREPARE"` or `"RUNNING"` from a non-`"PAUSE"` state → resets `gcode_state_durations`.
- If `gcode_state` transitions to `"RUNNING"` and the light is off → turns on the light.
- If the printer has a chamber door sensor and the door state changes → turns the light on when the door opens, and off when it closes (unless a job is running).

**Payload**: The full `build_all_data()` result. See [build\_all\_data() Response Schema](#build_all_data-response-schema).

**Frontend usage**:
```javascript
import { io } from 'socket.io-client';

const socket = io('http://localhost:5000');

socket.on('printer_update', (data) => {
  // data is identical to the /api/get_all_data response
  const printer = data.printer;
  const toolSeries = data.tool.series;   // multi-series array
  const bedSeries  = data.bed.series;    // single-series object {data: [...]}
});
```

---

## build_all_data() Response Schema

`build_all_data()` is called by both `GET /api/get_all_data` and the `printer_update` Socket.IO event. It assembles historical sensor time-series data sampled every ~2.5 seconds with a 60-minute rolling retention window.

### Top-level keys

| Key | Type | Description |
|-----|------|-------------|
| `tool` | object | Extruder temperature history. Multi-series. |
| `bed` | object | Heated-bed temperature history. Single series. |
| `chamber` | object | Chamber temperature history. Single series. |
| `fan` | object | All fan speed histories. Multi-series. |
| `gcode_state_durations` | object | Cumulative seconds spent in each `gcode_state` since the last job start. |
| `printer` | object | Full `BambuPrinter.toJson()` result, or error object when no live data. |

### Chart object structure (bed, chamber)

`bed` and `chamber` use a **single-series** structure:

```json
{
  "minVal": 19.0,
  "maxVal": 65.0,
  "zoom": 0,
  "maxAge": -3595,
  "xAxis": {
    "data": [-3595, -3590, -3585, ..., 0]
  },
  "series": {
    "data": [22.3, 22.3, 59.1, ..., 60.0]
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `minVal` | float | Y-axis minimum (data minimum minus a padding margin). |
| `maxVal` | float | Y-axis maximum (data maximum plus a padding margin). |
| `zoom` | int | Active zoom window in seconds. `0` = show all available data. |
| `maxAge` | int | X-axis value of the oldest visible data point (negative seconds). Absent when no data points exist. |
| `xAxis.data` | int[] | Time offsets in seconds relative to now. `0` = current time; negative values are in the past. |
| `series.data` | float[] | Temperature values in °C, aligned 1-to-1 with `xAxis.data`. |

### Chart object structure (tool)

`tool` uses a **multi-series** structure. Series data is sourced from per-extruder temperature tracking (`extruders[0].temp`, `extruders[1].temp`).

- **Single-extruder printers** (X1, P1, A1, P2, H2S): one series labelled `"Tool"`.
- **Dual-extruder H2D / H2D Pro**: two series labelled `"Right"` and `"Left"`.

Only series that have collected data points are included (no phantom series on single-extruder printers).

```json
{
  "minVal": 19.0,
  "maxVal": 230.0,
  "zoom": 1500,
  "maxAge": -1503,
  "xAxis": {
    "data": [-1503, -1500, -1495, ..., 0]
  },
  "series": [
    {
      "data": [22.1, 22.1, 220.0, ..., 220.5],
      "label": "Right",
      "color": "#e15759"
    },
    {
      "data": [22.0, 22.0, 215.0, ..., 215.2],
      "label": "Left",
      "color": "#76b7b2"
    }
  ]
}
```

Gaps between sparse samples are filled by step-interpolation (`_step_fill`): the last known value is held until a new sample is available.

| Series label | Color | Source |
|---|---|---|
| `"Tool"` (single extruder) | `#e15759` | `extruders[0].temp` |
| `"Right"` (H2D) | `#e15759` | `extruders[0].temp` |
| `"Left"` (H2D) | `#76b7b2` | `extruders[1].temp` |

### Chart object structure (fan)

`fan` uses a **multi-series** structure combining all four fan speed collections. The merged x-axis is the sorted union of all individual fan x-axes. Gaps are step-filled.

The `zoom` and `maxAge` fields on the `fan` object come from the `fan` (part-cooling) collection only.

```json
{
  "minVal": -0.1,
  "maxVal": 101.0,
  "zoom": 0,
  "maxAge": -3595,
  "xAxis": {
    "data": [-3595, -3590, ..., 0]
  },
  "series": [
    {
      "data": [0.0, 0.0, 80.0, ..., 80.0],
      "label": "Part Cooling",
      "color": "#af7aa1"
    },
    {
      "data": [60.0, 60.0, 60.0, ..., 60.0],
      "label": "Auxiliary",
      "color": "#4e79a7"
    },
    {
      "data": [100.0, 100.0, 100.0, ..., 100.0],
      "label": "Exhaust",
      "color": "#f28e2c"
    },
    {
      "data": [40.0, 40.0, 40.0, ..., 40.0],
      "label": "Heatbreak",
      "color": "#59a14f"
    }
  ]
}
```

| Series label | Color | Source (`BambuClimate` field) |
|---|---|---|
| `"Part Cooling"` | `#af7aa1` | `climate.part_cooling_fan_speed_percent` |
| `"Auxiliary"` | `#4e79a7` | `climate.aux_fan_speed_percent` |
| `"Exhaust"` | `#f28e2c` | `climate.exhaust_fan_speed_percent` |
| `"Heatbreak"` | `#59a14f` | `climate.heatbreak_fan_speed_percent` |

All fan values are in percent (0–100). Raw printer values on 0–15 scale are converted via `scaleFanSpeed()` before storage.

### gcode_state_durations

Cumulative elapsed seconds per `gcode_state` since the last job start (or application startup). Reset to an empty dict when `gcode_state` transitions to `PREPARE` or `RUNNING` from a non-`PAUSE` state.

```json
{
  "gcode_state_durations": {
    "IDLE": 42.5,
    "PREPARE": 30.0,
    "RUNNING": 3600.0,
    "PAUSE": 120.0,
    "FINISH": 0.0
  }
}
```

### printer key

When `printer.recent_update` is truthy and `printer.printer_state.spools` is non-empty:
```json
{ "printer": { ... } }
```
Full `BambuPrinter.toJson()` result.

When no live data is available:
```json
{ "printer": {"status": "error", "reason": "no data to send"} }
```

---

## Error Handling

All endpoints are protected by Flask's `@app.errorhandler(500)` which returns:

```json
{
  "status": "error",
  "message": "ExceptionType: message text",
  "stacktrace": "Traceback (most recent call last):\n  ..."
}
```

### 304 Not Modified

Returned only by `GET /api/printer` when no live data is available:
```json
{"status": "error", "reason": "no data to send"}
```

### 404 Not Found

Returned by `GET /api/get_3mf_props_for_file` and `GET /api/get_current_3mf_props`:
```json
{"status": "error", "message": "No file found", "file": "/path/to/file.3mf"}
```
```json
{"status": "error", "message": "No Job Found"}
```

### 500 Internal Server Error

Returned on any unhandled exception (including invalid enum names, missing required parameters, FTPS failures):
```json
{
  "status": "error",
  "message": "KeyError: 'INVALID_OPTION'",
  "stacktrace": "Traceback..."
}
```

---

## Environment Variables

Required at startup:

```bash
BAMBU_HOSTNAME=192.168.1.100       # Printer IP address
BAMBU_ACCESS_CODE=12345678         # 8-character printer access code
BAMBU_SERIAL_NUMBER=00M12345678901 # Full printer serial number
INTEGRATED_EXTERNAL_HEATER=FALSE   # Set TRUE to enable ChamberMonitor integration
```

Optional — only used when `INTEGRATED_EXTERNAL_HEATER=TRUE`:

```bash
CHAMBER_MQTT_HOST=192.168.1.50
CHAMBER_MQTT_PORT=1883
CHAMBER_MQTT_USER=user
CHAMBER_MQTT_PASS=password
CHAMBER_TARGET_TOPIC=chamber/target
CHAMBER_TEMPERATURE_TOPIC=chamber/temperature
CHAMBER_REQUESTED_STATE_TOPIC=chamber/set
CHAMBER_CURRENT_STATE_TOPIC=chamber/state
CHAMBER_STATE_ON_VALUE=ON
CHAMBER_STATE_OFF_VALUE=OFF
```

---

## Examples

### Python
```python
import requests

# Get printer status
response = requests.get("http://localhost:5000/api/printer")
printer = response.json()

# Set bed temperature
requests.get("http://localhost:5000/api/set_bed_target_temp?temp=60")

# Start print job (plate is required)
params = {
    "filename": "/test.3mf",
    "platenum": 1,
    "plate": "COOL_PLATE",
    "use_ams": "true",
    "ams_mapping": "[0,4]",
    "bl": "true",
}
requests.get("http://localhost:5000/api/print_3mf", params=params)
```

### JavaScript (Socket.IO + axios)
```javascript
import { io } from 'socket.io-client';
import axios from 'axios';

const BASE = 'http://localhost:5000';

// Real-time updates via Socket.IO
const socket = io(BASE);
socket.on('printer_update', (data) => {
  const printer = data.printer;
  // data.tool.series is an array of {data, label, color}
  const toolSeries = data.tool.series;
  // data.bed.series is a plain object {data: [...]}
  const bedTemps = data.bed.series.data;
  console.log('gcode_state:', printer._printer_state?.gcode_state);
});

// Control endpoints
await axios.get(`${BASE}/api/set_light_state`, { params: { state: 'on' } });
await axios.get(`${BASE}/api/set_speed_level`, { params: { level: '2' } });

// Upload and print
const formData = new FormData();
formData.append('myFile', fileInput.files[0]);
await axios.post(`${BASE}/api/upload_file_to_host`, formData);
await axios.get(`${BASE}/api/upload_file_to_printer`, {
  params: { src: 'model.3mf', dest: '/prints/model.3mf' },
});
await axios.get(`${BASE}/api/print_3mf`, {
  params: { filename: '/prints/model.3mf', plate: 'AUTO', platenum: 1 },
});
```

### cURL
```bash
# Printer info
curl http://localhost:5000/api/printer

# Set chamber temperature
curl "http://localhost:5000/api/set_chamber_target_temp?temp=45"

# Send G-code (multiple commands with |)
curl "http://localhost:5000/api/send_gcode?gcode=G28|G1 Z10 F600"

# Upload file
curl -F "myFile=@model.3mf" http://localhost:5000/api/upload_file_to_host

# Download SD card file
curl -o downloaded.3mf "http://localhost:5000/api/download_file_from_printer?src=/test.3mf"
```

---

## Data Models

For comprehensive documentation of all data structures, attributes, and telemetry fields returned by this API, see the [Data Dictionary](data-dictionary.md).

---

## Related Resources

### Project Documentation

- [bambu-printer-manager GitHub](https://github.com/synman/bambu-printer-manager)
- [bambu-printer-manager Documentation](https://synman.github.io/bambu-printer-manager/)
- [Data Dictionary](data-dictionary.md) - Complete attribute reference
- [MQTT Protocol Reference](mqtt-protocol-reference.md) - MQTT command reference

### Reference Implementations

- **[BambuStudio](https://github.com/bambulab/BambuStudio)** - Official Bambu Lab client
- **[OrcaSlicer](https://github.com/OrcaSlicer/OrcaSlicer)** - Community fork with enhanced features
- **[ha-bambulab](https://github.com/greghesp/ha-bambulab)** - Home Assistant integration
- **[ha-bambulab pybambu](https://github.com/greghesp/ha-bambulab/tree/main/custom_components/bambu_lab/pybambu)** - Python MQTT client
- **[Bambu-HomeAssistant-Flows](https://github.com/WolfwithSword/Bambu-HomeAssistant-Flows)** - Workflow patterns
- **[OpenBambuAPI](https://github.com/Doridian/OpenBambuAPI)** - Alternative API implementation
- **[X1Plus](https://github.com/X1Plus/X1Plus)** - Community firmware
- **[bambu-node](https://github.com/THE-SIMPLE-MARK/bambu-node)** - Node.js implementation

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.3 | 2026-06-10 | Full rewrite from source: corrected `build_all_data()` multi-series schema for `tool` and `fan`, fixed file-operation response bodies (all return updated SD card tree, not custom dicts), documented Socket.IO `printer_update` event, added `gcode_state_durations`, corrected `set_spool_k_factor` stub status, corrected `print_3mf` `plate` required/default behaviour, corrected `toggle_verbosity` level-toggle logic, added `NOZZLE_BLOB_DETECT`/`AIR_PRINT_DETECT` to `set_print_option`, expanded environment variables section |
| 1.2 | 2026-03-02 | Added Detection & Safety section (buildplate, spaghetti, purgechute, nozzleclumping, airprinting detectors, refresh_nozzles); fixed dump_data_ds.collections route name |
| 1.1 | 2026-02-25 | Updated reference implementations; added comprehensive external sources |
| 1.0 | 2026-02-23 | Initial REST API reference documentation |

---

## Support

For issues, questions, or contributions:
- Open an issue: [bambu-printer-app Issues](https://github.com/synman/bambu-printer-app/issues)
- Library issues: [bambu-printer-manager Issues](https://github.com/synman/bambu-printer-manager/issues)
