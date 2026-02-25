# Bambu Printer App - API Reference

## Overview

This REST API provides complete control over Bambu Lab printers via HTTP requests. Built with Flask and powered by [bambu-printer-manager](https://github.com/synman/bambu-printer-manager), it exposes printer status, control commands, file management, and telemetry data.

**Base URL**: `http://localhost:5000/api`

**Response Format**: All endpoints return JSON

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
- [Advanced Settings](#advanced-settings)
- [Telemetry & Data](#telemetry-data)
- [System & Diagnostics](#system-diagnostics)

---

## Printer Status & Information

### GET /api/printer

Get complete printer state and configuration.

**Response**: Complete JSON object containing:
- Printer state (`BambuState`)
- Active job information
- AMS units status
- Extruder states
- Climate data
- Spool information
- Capabilities

**Example Response**:
```json
{
  "state": {
    "gcode_state": "RUNNING",
    "active_tool": 0,
    "active_nozzle_temp": 220.5,
    "active_nozzle_temp_target": 220,
    "ams_units": [...],
    "extruders": [...],
    "spools": [...],
    "climate": {...}
  },
  "config": {...},
  "capabilities": {...},
  "active_job_info": {...}
}
```

**Error Response**: `304 Not Modified` if no telemetry data available

---

### GET /api/health_check

Health check endpoint returning printer status and connection state.

**Response**:
```json
{
  "status": "success",
  "printer": {
    // Full printer JSON
  }
}
```

**Error Response**: `500 Internal Server Error` if printer disconnected

---

## Temperature Control

### GET /api/set_tool_target_temp

Set target temperature for active extruder/toolhead.

**Parameters**:
- `temp` (int, required): Target temperature in °C (0-300)

**Example**: `/api/set_tool_target_temp?temp=220`

**Response**: `{"status": "success"}`

---

### GET /api/set_bed_target_temp

Set target bed temperature.

**Parameters**:
- `temp` (int, required): Target temperature in °C (0-120)

**Example**: `/api/set_bed_target_temp?temp=60`

**Response**: `{"status": "success"}`

---

### GET /api/set_chamber_target_temp

Set target chamber temperature (printers with heated chamber only).

**Parameters**:
- `temp` (int, required): Target temperature in °C (0-65)

**Example**: `/api/set_chamber_target_temp?temp=45`

**Response**: `{"status": "success"}`

**Note**: Requires printer with chamber heater capability (X1E, H2 series)

---

## Fan Control

### GET /api/set_fan_speed_target

Set part cooling fan speed.

**Parameters**:
- `percent` (int, required): Fan speed percentage (0-100)

**Example**: `/api/set_fan_speed_target?percent=75`

**Response**: `{"status": "success"}`

---

### GET /api/set_aux_fan_speed_target

Set auxiliary fan speed.

**Parameters**:
- `percent` (int, required): Fan speed percentage (0-100)

**Example**: `/api/set_aux_fan_speed_target?percent=50`

**Response**: `{"status": "success"}`

---

### GET /api/set_exhaust_fan_speed_target

Set exhaust/chamber fan speed.

**Parameters**:
- `percent` (int, required): Fan speed percentage (0-100)

**Example**: `/api/set_exhaust_fan_speed_target?percent=100`

**Response**: `{"status": "success"}`

---

## Print Job Control

### GET /api/print_3mf

Start a 3MF print job.

**Parameters**:
- `filename` (string, required): Path to 3MF file on SD card
- `platenum` (int, optional, default=0): Plate number to print
- `plate` (string, optional, default="AUTO"): Plate type
  - Options: `AUTO`, `COOL_PLATE`, `ENG_PLATE`, `HOT_PLATE`, `TEXTURED_PLATE`
- `use_ams` (bool, optional, default=false): Use AMS for filament
- `ams_mapping` (string, optional): JSON array of absolute tray IDs per filament (e.g., "[0,1,2,3]" or "[0,4,128]" for multi-AMS). Values: 0-103 (4-slot units), 128-135 (1-slot units), -1 (unmapped)
- `bl` (bool, optional, default=false): Enable bed leveling
- `flow` (bool, optional, default=false): Enable flow calibration
- `tl` (bool, optional, default=false): Enable timelapse

**Example**:
```
/api/print_3mf?filename=/test.3mf&platenum=1&plate=COOL_PLATE&use_ams=true&ams_mapping=[0,1,2,3]&bl=true&flow=true&tl=true
```

**Response**: `{"status": "success"}`

---

### GET /api/pause_printing

Pause the current print job.

**Response**: `{"status": "success"}`

---

### GET /api/resume_printing

Resume a paused print job.

**Response**: `{"status": "success"}`

---

### GET /api/stop_printing

Stop/cancel the current print job.

**Response**: `{"status": "success"}`

---

### GET /api/skip_objects

Skip specific objects during printing (Paint-on supports, exclude objects).

**Parameters**:
- `objects` (string, required): Comma-separated list of object names/IDs

**Example**: `/api/skip_objects?objects=support_1,support_2,brim`

**Response**: `{"status": "success"}`

---

## Filament Management

### GET /api/load_filament

Load filament from specified AMS slot or external spool.

**Parameters**:
- `slot` (int, required): Tray slot ID
  - `0-15`: AMS slots (4 slots × 4 units)
  - `254-255`: External spool

**Example**: `/api/load_filament?slot=2`

**Response**: `{"status": "success"}`

---

### GET /api/unload_filament

Unload current filament.

**Response**: `{"status": "success"}`

---

### GET /api/refresh_spool_rfid

Refresh RFID tag data for a specific spool.

**Parameters**:
- `slot_id` (int, required): Slot ID within AMS (0-3)
- `ams_id` (int, required): AMS unit ID (0-3 or 128-131)

**Example**: `/api/refresh_spool_rfid?slot_id=0&ams_id=0`

**Response**: `{"status": "success"}`

---

### GET /api/set_spool_details

Set custom spool details (type, color, temperatures).

**Parameters**:
- `tray_id` (int, required): Global tray ID (0-15 or 254-255)
- `tray_info_idx` (string, required): Filament preset index
- `tray_id_name` (string, optional): Custom spool name
- `tray_type` (string, optional): Filament type (PLA, PETG, ABS, etc.)
- `tray_color` (string, optional): Hex color code (#RRGGBB)
- `nozzle_temp_min` (int, optional): Minimum nozzle temp (°C)
- `nozzle_temp_max` (int, optional): Maximum nozzle temp (°C)

**Example**:
```
/api/set_spool_details?tray_id=0&tray_info_idx=GFL99&tray_id_name=My%20PLA&tray_type=PLA&tray_color=%23FF5733&nozzle_temp_min=200&nozzle_temp_max=230
```

**Response**: `{"status": "success"}`

**Note**: Returns after 2 second delay to allow printer to process

---

### GET /api/set_spool_k_factor

Select extrusion calibration profile for a spool.

**Parameters**:
- `tray_id` (int, required): Global tray ID (0-15 or 254-255)

**Example**: `/api/set_spool_k_factor?tray_id=0`

**Response**: `{"status": "success"}`

**Note**: Applies K-factor (linear advance) calibration

---

## File Management

### GET /api/get_sdcard_contents

Retrieve complete SD card file tree.

**Response**:
```json
{
  "name": "/",
  "id": "/",
  "children": [
    {
      "name": "folder1",
      "id": "/folder1/",
      "children": [...]
    },
    {
      "name": "test.3mf",
      "id": "/test.3mf",
      "size": 12345
    }
  ]
}
```

---

### GET /api/refresh_sdcard_contents

Trigger refresh of SD card contents from printer.

**Response**: `{"status": "success"}`

**Note**: Refreshed data available via `/api/get_sdcard_contents`

---

### GET /api/get_sdcard_3mf_files

Get list of only 3MF files on SD card.

**Response**:
```json
[
  "/test.3mf",
  "/folder/model.3mf"
]
```

---

### GET /api/refresh_sdcard_3mf_files

Trigger refresh of 3MF file list from printer.

**Response**: `{"status": "success"}`

---

### GET /api/delete_sdcard_file

Delete a file or folder from SD card.

**Parameters**:
- `file` (string, required): Path to file/folder
  - Files: `/path/to/file.3mf`
  - Folders: `/path/to/folder/` (trailing slash)

**Example**: `/api/delete_sdcard_file?file=/old_print.3mf`

**Response**:
```json
{
  "status": "success",
  "deleted": "/old_print.3mf"
}
```

---

### GET /api/make_sdcard_directory

Create a new directory on SD card.

**Parameters**:
- `dir` (string, required): Path for new directory (with trailing slash)

**Example**: `/api/make_sdcard_directory?dir=/projects/new_folder/`

**Response**:
```json
{
  "status": "success",
  "created": "/projects/new_folder/"
}
```

---

### GET /api/rename_sdcard_file

Rename or move a file/folder on SD card.

**Parameters**:
- `src` (string, required): Source path
- `dest` (string, required): Destination path

**Example**: `/api/rename_sdcard_file?src=/old.3mf&dest=/new.3mf`

**Response**:
```json
{
  "status": "success",
  "renamed": {
    "from": "/old.3mf",
    "to": "/new.3mf"
  }
}
```

---

### POST /api/upload_file_to_host

Upload a file to the API server's upload directory.

**Method**: POST (multipart/form-data)

**Form Data**:
- `myFile` (file, required): File to upload

**Response**: `{"status": "success"}`

**Note**: Files saved to `./uploads/` directory

---

### GET /api/upload_file_to_printer

Transfer a file from server uploads directory to printer SD card.

**Parameters**:
- `src` (string, required): Filename in uploads directory
- `dest` (string, required): Destination path on SD card

**Example**: `/api/upload_file_to_printer?src=model.3mf&dest=/prints/model.3mf`

**Response**:
```json
{
  "status": "success",
  "uploaded": {
    "source": "model.3mf",
    "destination": "/prints/model.3mf",
    "size": 12345
  }
}
```

---

### GET /api/download_file_from_printer

Download a file from printer SD card to server.

**Parameters**:
- `src` (string, required): Path on SD card

**Example**: `/api/download_file_from_printer?src=/test.3mf`

**Response**: Binary file download

**Note**: File saved to `./uploads/` and sent to client

---

### GET /api/get_3mf_props_for_file

Get metadata and properties for a specific 3MF file.

**Parameters**:
- `file` (string, required): Path to 3MF file
- `plate` (int, optional, default=1): Plate number

**Example**: `/api/get_3mf_props_for_file?file=/test.3mf&plate=1`

**Response**:
```json
{
  "id": "abc123",
  "name": "test.3mf",
  "subtask_name": "plate_1",
  "weight": 15.5,
  "bed_type": 1,
  "filament_used_g": [12.5, 3.0],
  "filament_colors": ["#FF0000", "#0000FF"],
  "prediction": 3600,
  "objects": ["part1", "part2"]
}
```

**Error Response**: `404 Not Found` if file doesn't exist

---

### GET /api/get_current_3mf_props

Get metadata for currently printing 3MF file.

**Response**:
```json
{
  "status": "success",
  "id": "abc123",
  "name": "current_print.3mf",
  // ... additional properties
}
```

**Error Response**: `404 Not Found` if no active job

---

## Tool Control (Dual Extruder)

### GET /api/toggle_active_tool

Switch between left and right extruders (H2D dual extruder only).

**Response**: `{"status": "success"}`

**Note**: Toggles between extruder 0 (right) and 1 (left)

---

### GET /api/set_nozzle_details

Set nozzle type and diameter.

**Parameters**:
- `nozzle_diameter` (float, required): Nozzle diameter
  - Options: `0.2`, `0.4`, `0.6`, `0.8`
- `nozzle_type` (string, required): Nozzle material type
  - Options: `STAINLESS_STEEL`, `HARDENED_STEEL`, `HS01`, `HH01`

**Example**: `/api/set_nozzle_details?nozzle_diameter=0.4&nozzle_type=HARDENED_STEEL`

**Response**: `{"status": "success"}`

**Note**: Returns after 1 second delay

---

## AMS Control

### GET /api/send_ams_control_command

Send control command to AMS system.

**Parameters**:
- `cmd` (string, required): Command to send
  - Options: `PAUSE`, `RESUME`, `RESET`

**Example**: `/api/send_ams_control_command?cmd=RESET`

**Response**: `{"status": "success"}`

---

### GET /api/set_ams_user_setting

Configure AMS user settings.

**Parameters**:
- `setting` (string, required): Setting to modify
  - Options:
    - `CALIBRATE_REMAIN_FLAG`: Calibrate remaining filament
    - `STARTUP_READ_OPTION`: Read RFID on startup
    - `TRAY_READ_OPTION`: Read RFID on tray insert
- `enabled` (bool, required): Enable/disable setting

**Example**: `/api/set_ams_user_setting?setting=STARTUP_READ_OPTION&enabled=true`

**Response**: `{"status": "success"}`

---

## Advanced Settings

### GET /api/send_gcode

Send raw G-code commands to printer.

**Parameters**:
- `gcode` (string, required): G-code commands (use `|` for newlines)

**Example**: `/api/send_gcode?gcode=G28|G1 Z10 F600|M104 S200`

**Response**: `{"status": "success"}`

**Note**: Multiple commands separated by `|` are converted to newlines

**⚠️ Warning**: Direct G-code can damage printer if used incorrectly

---

### GET /api/set_print_option

Configure print options/features.

**Parameters**:
- `option` (string, required): Print option to set
  - Options:
    - `AUTO_RECOVERY`: Auto-recovery from power loss
    - `FILAMENT_TANGLE_DETECT`: Filament tangle detection
    - `SOUND_ENABLE`: Enable sound/beeps
    - `AUTO_SWITCH_FILAMENT`: Auto-switch filament when runout
- `enabled` (bool, required): Enable/disable option

**Example**: `/api/set_print_option?option=AUTO_RECOVERY&enabled=true`

**Response**: `{"status": "success"}`

---

### GET /api/set_light_state

Control chamber LED light.

**Parameters**:
- `state` (string, required): Light state (`on` or `off`)

**Example**: `/api/set_light_state?state=on`

**Response**: `{"status": "success"}`

**Note**: Automatically controlled by app based on print state and door sensors

---

### GET /api/set_speed_level

Set print speed override level.

**Parameters**:
- `level` (string, required): Speed level
  - Options: `1` (silent), `2` (standard), `3` (sport), `4` (ludicrous)

**Example**: `/api/set_speed_level?level=2`

**Response**: `{"status": "success"}`

---

## Telemetry & Data

### GET /api/get_all_data

Get complete historical telemetry data for charting.

**Response**:
```json
{
  "tool": {
    "minVal": 0,
    "maxVal": 250,
    "zoom": 0,
    "maxAge": -3600,
    "xAxis": {
      "data": [-3600, -3599, -3598, ..., 0]
    },
    "series": {
      "data": [25.5, 26.0, 27.5, ..., 220.0]
    }
  },
  "bed": { /* same structure */ },
  "chamber": { /* same structure */ },
  "fan": { /* same structure */ },
  "printer": { /* current printer state */ }
}
```

**Notes**:
- X-axis values are seconds in the past (negative values)
- Series data contains temperature/percentage values
- `zoom` indicates current zoom level (0 = all data)
- `maxAge` is oldest data point in seconds

---

### GET /api/zoom_in

Zoom in on telemetry chart (show less historical data).

**Parameters**:
- `name` (string, required): Chart name
  - Options: `tool`, `bed`, `chamber`, `fan`

**Example**: `/api/zoom_in?name=tool`

**Response**: `{"status": "success", "printer": {}}`

**Note**: Reduces visible time range by 500 seconds per call

---

### GET /api/zoom_out

Zoom out on telemetry chart (show more historical data).

**Parameters**:
- `name` (string, required): Chart name
  - Options: `tool`, `bed`, `chamber`, `fan`

**Example**: `/api/zoom_out?name=tool`

**Response**: `{"status": "success", "printer": {}}`

**Note**: Increases visible time range by 500 seconds per call

---

### GET /api/dump_data_collections

Dump all internal data collections (debugging).

**Response**: JSONL format (newline-delimited JSON objects)

---

## System & Diagnostics

### GET /api/toggle_session

Pause/resume MQTT connection to printer.

**Response**:
```json
{
  "status": "success",
  "state": "PAUSED" // or "CONNECTED"
}
```

**Note**: Useful for debugging or reducing network traffic

---

### GET /api/trigger_printer_refresh

Force reconnection to printer or refresh telemetry.

**Response**: `{"status": "success", "printer": {}}`

**Notes**:
- If disconnected: Initiates reconnection
- If connected: Sends refresh command

---

### GET /api/toggle_verbosity

Toggle debug logging level.

**Parameters**:
- `verbose` (bool, required): Enable verbose logging

**Example**: `/api/toggle_verbosity?verbose=true`

**Response**:
```json
{
  "status": "success",
  "level": "DEBUG", // or "INFO"
  "verbose": true
}
```

---

### GET /api/dump_log

Retrieve application log file.

**Response**: Plain text log contents

**Note**: Returns contents of `./output.log`

---

### GET /api/truncate_log

Clear/truncate application log file.

**Response**: `{"status": "success"}`

**Note**: Deletes contents of `./output.log`

---

### GET /api/fake_error

Trigger intentional error for testing error handling.

**Response**: `500 Internal Server Error`

**Response Body**:
```json
{
  "status": "error",
  "message": "ZeroDivisionError: division by zero",
  "stacktrace": "Traceback (most recent call last):\n..."
}
```

**Note**: Development/testing endpoint only

---

## Error Handling

All endpoints may return error responses:

### 304 Not Modified
Returned when printer data is not yet available:
```json
{
  "status": "error",
  "reason": "no data to send"
}
```

### 404 Not Found
Returned when requested resource doesn't exist:
```json
{
  "status": "error",
  "message": "No file found",
  "file": "/path/to/missing.3mf"
}
```

### 500 Internal Server Error
Returned on exceptions:
```json
{
  "status": "error",
  "message": "TypeError: expected string",
  "stacktrace": "Traceback..."
}
```

---

## Rate Limiting & Performance

- **No enforced rate limits**: Use responsibly
- **Concurrent requests**: Server uses 8 worker threads
- **Telemetry updates**: Printer state updates via MQTT (real-time)
- **File operations**: FTPS-based, can be slow for large files

---

## Environment Variables

Required environment variables:

```bash
BAMBU_HOSTNAME=192.168.1.100       # Printer IP address
BAMBU_ACCESS_CODE=12345678         # 8-character access code
BAMBU_SERIAL_NUMBER=00M12345678901 # Printer serial number
INTEGRATED_EXTERNAL_HEATER=FALSE   # External chamber heater (TRUE/FALSE)
```

---

## Examples

### Python
```python
import requests

# Get printer status
response = requests.get("http://localhost:5000/api/printer")
printer = response.json()
print(f"Nozzle temp: {printer['state']['active_nozzle_temp']}°C")

# Set bed temperature
requests.get("http://localhost:5000/api/set_bed_target_temp?temp=60")

# Start print job
params = {
    "filename": "/test.3mf",
    "platenum": 1,
    "plate": "COOL_PLATE",
    "use_ams": "true",
    "bl": "true"
}
requests.get("http://localhost:5000/api/print_3mf", params=params)
```

### JavaScript (axios)
```javascript
// Get printer status
const response = await axios.get('http://localhost:5000/api/printer');
const printer = response.data;
console.log(`Bed temp: ${printer.state.climate.bed_temp}°C`);

// Control light
await axios.get('http://localhost:5000/api/set_light_state', {
  params: { state: 'on' }
});

// Upload and print file
const formData = new FormData();
formData.append('myFile', fileInput.files[0]);
await axios.post('http://localhost:5000/api/upload_file_to_host', formData);

await axios.get('http://localhost:5000/api/upload_file_to_printer', {
  params: { src: filename, dest: `/prints/${filename}` }
});
await axios.get('http://localhost:5000/api/print_3mf', {
  params: { filename: `/prints/${filename}` }
});
```

### cURL
```bash
# Get printer info
curl http://localhost:5000/api/printer

# Set chamber temperature
curl "http://localhost:5000/api/set_chamber_target_temp?temp=45"

# Upload file
curl -F "myFile=@model.3mf" http://localhost:5000/api/upload_file_to_host

# Download SD card file
curl -o downloaded.3mf "http://localhost:5000/api/download_file_from_printer?src=/test.3mf"
```

---

## WebSocket Support

Currently not implemented. All updates are polling-based via `/api/printer` or `/api/get_all_data`.

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
| 1.1 | 2026-02-25 | Updated reference implementations; added comprehensive external sources |
| 1.0 | 2026-02-23 | Initial REST API reference documentation |

---

## Support

For issues, questions, or contributions:
- Open an issue: [bambu-printer-app Issues](https://github.com/synman/bambu-printer-app/issues)
- Library issues: [bambu-printer-manager Issues](https://github.com/synman/bambu-printer-manager/issues)
