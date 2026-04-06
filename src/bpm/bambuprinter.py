"""
The main `bambu-printer-manager` class `BambuPrinter` lives here.
"""

import contextlib
import copy
import json
import logging
import math
import re
import ssl
import sys
import threading
import time
import traceback
from pathlib import Path
from typing import Any

import paho.mqtt.client as mqtt

if sys.version_info >= (3, 13):
    from warnings import deprecated
else:
    from typing_extensions import deprecated

from webcolors import hex_to_name, name_to_hex

from bpm.bambucommands import (
    AMS_CHANGE_FILAMENT,
    AMS_CONTROL,
    AMS_FILAMENT_DRYING,
    AMS_FILAMENT_SETTING,
    AMS_GET_RFID,
    AMS_USER_SETTING,
    ANNOUNCE_PUSH,
    ANNOUNCE_VERSION,
    CHAMBER_LIGHT_TOGGLE,
    CLEAN_PRINT_ERROR_TEMPLATE,
    CLEAN_PRINT_ERROR_UIOP_TEMPLATE,
    EXTRUSION_CALI_SEL,
    EXTRUSION_CALI_SET,
    PAUSE_PRINT,
    PRINT_3MF_FILE,
    PRINT_OPTION_COMMAND,
    REFRESH_NOZZLE,
    RENAME_PRINTER,
    RESUME_PRINT,
    SEND_GCODE_TEMPLATE,
    SET_ACCESSORIES,
    SET_ACTIVE_TOOL,
    SET_CHAMBER_AC_MODE,
    SET_CHAMBER_TEMP_TARGET,
    SKIP_OBJECTS,
    SPEED_PROFILE_TEMPLATE,
    STOP_PRINT,
    XCAM_CONTROL_SET,
)
from bpm.bambuconfig import BambuConfig
from bpm.bambuproject import ActiveJobInfo, get_3mf_entry_by_name, get_project_info
from bpm.bambuspool import BambuSpool
from bpm.bambustate import BambuState
from bpm.bambutools import (
    ActiveTool,
    AMSControlCommand,
    AMSUserSetting,
    DetectorSensitivity,
    LoggerName,
    NozzleDiameter,
    NozzleType,
    PlateType,
    PrinterSeries,
    PrintOption,
    ServiceState,
    SpeedLevel,
    cache_delete,
    cache_read,
    cache_write,
    getPrinterSeriesByModel,
    jsonSerializer,
    make_cache_key,
    nozzle_type_to_telemetry,
    parse_nozzle_type,
    parseStage,
    sortFileTreeAlphabetically,
)
from bpm.ftpsclient.ftpsclient import IoTFTPSClient

logger = logging.getLogger(LoggerName)


class BambuPrinter:
    """
    `BambuPrinter` is the main class within `bambu-printer-manager`
    It is responsible for interacting with and managing your Bambu Lab 3d printer.
    It provides an object oriented abstraction layer between your project and the
    `mqtt` and `ftps` based mechanisms in place for communicating with your printer.
    """

    def __init__(self, config: BambuConfig | None = None):
        """
        Sets up all internal storage attributes for `BambuPrinter` and bootstraps the
        logging engine.

        Parameters
        ----------
        * config : Optional[BambuConfig] = None
            An optional `BambuConfig` instance that provides configuration information
            for the printer connection.  If not provided, a default `BambuConfig` instance
            will be created.
        """
        self._mqtt_client_thread = None
        self._watchdog_thread = None

        self._internalException = None
        self._lastMessageTime = None
        self._recent_update = False

        if config is None:
            config = BambuConfig("", "", "")
        self._config = config
        self._service_state = ServiceState.NO_STATE

        self._client = None
        self._on_update = None

        self._tool_temp_target_time = 0
        self._bed_temp_target_time = 0
        self._chamber_temp_target_time = 0
        self._fan_speed_target_time = 0

        self._light_state = ""
        self._speed_level = 0

        self._printer_state = BambuState()
        self._active_job_info = ActiveJobInfo()

        self._sdcard_contents = None
        self._sdcard_3mf_files = None

        self._print_type = ""
        self._skipped_objects = []

        self._nozzle_type = ""
        self._nozzle_diameter = 0.0

    # region public methods

    def start_session(self):
        """
        Initiates a connection to the Bambu Lab printer and provides a stateful
        session, with built-in recovery in the event `BambuPrinter`
        becomes disconnected from the machine.

        This method is required to be called before any commands or data
        collection / callbacks can take place with the machine.
        """
        logger.debug("start_session - starting session")
        if (
            self.config.hostname is None
            or self.config.access_code is None
            or self.config.serial_number is None
        ):
            raise Exception("hostname, access_code, and serial_number are required")
        if self.client and self.client.is_connected():
            raise Exception("a session is already active")

        def on_connect(client, userdata, flags, reason_code, properties):
            logger.debug("on_connect - session on_connect")
            if self.service_state != ServiceState.PAUSED:
                self.service_state = ServiceState.CONNECTED
                client.subscribe(f"device/{self.config.serial_number}/report")
                logger.debug(
                    f"on_connect -subscribed to [device/{self.config.serial_number}/report]"
                )

        def on_disconnect(client, userdata, flags, reason_code, properties):
            logger.debug("on_disconnect - session on_disconnect")
            if self._internalException:
                logger.exception("on_disconnect - an internal exception occurred")
                self.service_state = ServiceState.QUIT
                raise self._internalException
            if self.service_state != ServiceState.PAUSED:
                self.service_state = ServiceState.DISCONNECTED

        def on_message(client, userdata, msg):
            if self._lastMessageTime and self._recent_update:
                self._lastMessageTime = time.monotonic()
            self._on_message(msg.payload.decode("utf-8"))

        def loop_forever(printer: BambuPrinter):
            logger.debug("loop_forever - starting mqtt loop_forever")
            try:
                printer.client.loop_forever(retry_first_connection=True)
            except Exception as e:
                logger.exception("loop_forever - an internal exception occurred")
                printer._internalException = e
                if printer.client and printer.client.is_connected():
                    printer.client.disconnect()
            printer.service_state = ServiceState.QUIT

        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)  # type: ignore

        self.client.on_connect = on_connect
        self.client.on_disconnect = on_disconnect
        self.client.on_message = on_message

        self.client.tls_set(tls_version=ssl.PROTOCOL_TLS, cert_reqs=ssl.CERT_NONE)
        self.client.tls_insecure_set(True)
        self.client.reconnect_delay_set(min_delay=1, max_delay=1)

        self.client.username_pw_set(
            self.config.mqtt_username, password=self.config.access_code
        )

        self.client.user_data_set(self.config.mqtt_client_id)
        self.client.connect_timeout = self.config.mqtt_connection_timeout

        try:
            self.client.connect(self.config.hostname, self.config.mqtt_port)
        except Exception as e:
            self._internalException = e
            logger.warning(
                f"start_session - unable to connect to printer - reason: [{e}] stacktrace: [{traceback.format_exc()}]"
            )
            self.service_state = ServiceState.QUIT
            return

        self._mqtt_client_thread = threading.Thread(
            target=loop_forever, name="bambuprinter-session", args=(self,)
        )
        self._mqtt_client_thread.start()

        self._start_watchdog()

    def pause_session(self):
        """
        Pauses the `BambuPrinter` session is it is active.  Under the covers this
        method unsubscribes from the `/report` topic, essentially disabling all
        printer data refreshes.
        """
        if self.service_state != ServiceState.PAUSED:
            self.client.unsubscribe(f"device/{self.config.serial_number}/report")
            logger.debug(
                f"pause_session - unsubscribed from [device/{self.config.serial_number}/report]"
            )
            self.service_state = ServiceState.PAUSED

    def resume_session(self):
        """
        Resumes a previously paused session by re-subscribing to the /report topic.
        """
        if (
            self.client
            and self.client.is_connected()
            and self.service_state == ServiceState.PAUSED
        ):
            self.client.subscribe(f"device/{self.config.serial_number}/report")
            logger.debug(
                f"resume_session - subscribed to [device/{self.config.serial_number}/report]"
            )
            self._lastMessageTime = time.monotonic()
            self.service_state = ServiceState.CONNECTED
            return
        self.service_state = ServiceState.QUIT

    def quit(self):
        """
        Shuts down all threads.  Your `BambuPrinter` instance should probably be
        considered dead after making this call although you may be able to restart a
        session with [start_session](#bpm.bambuprinter.BambuPrinter.start_session)().
        """
        if self.client and self.client.is_connected():
            self.client.disconnect()
            logger.debug("quit - mqtt client was connected and is now disconnected")
        else:
            logger.debug("quit - mqtt client was already disconnected")

        self._service_state = ServiceState.QUIT
        self._notify_update()

        if self._mqtt_client_thread and self._mqtt_client_thread.is_alive():
            self._mqtt_client_thread.join()
        if self._watchdog_thread and self._watchdog_thread.is_alive():
            self._watchdog_thread.join()
        logger.debug("quit - all threads have terminated")

    @contextlib.contextmanager
    def ftp_connection(self):
        """
        Open an FTPS connection to the printer's SD card for file management operations.

        Intended to be used as a context manager so the connection is closed
        automatically on exit.  All SD card file operations (`upload_sdcard_file`,
        `download_sdcard_file`, `delete_sdcard_file`, etc.) use this internally.

        Example
        -------
        ```python
        with printer.ftp_connection() as ftps:
            ftps.upload_file("/local/myfile.3mf", "/jobs/myfile.3mf")
        ```
        """
        ftps = None
        try:
            ftps = IoTFTPSClient(
                self._config.hostname,
                990,
                self._config.mqtt_username,
                self._config.access_code,
                ssl_implicit=True,
            )
            yield ftps
        finally:
            if ftps and ftps.ftps_session:
                ftps.disconnect()

    def refresh(self):
        """
        Triggers a full data refresh from the printer (if it is connected).  You should use this
        method sparingly as resorting to it indicates something is not working properly.
        """
        if self.service_state == ServiceState.CONNECTED:
            logger.debug(
                f"refresh - publishing ANNOUNCE_VERSION to [device/{self.config.serial_number}/request]"
            )
            self.client.publish(
                f"device/{self.config.serial_number}/request",
                json.dumps(ANNOUNCE_VERSION),
            )
            logger.debug(
                f"refresh - publishing ANNOUNCE_PUSH to [device/{self.config.serial_number}/request]"
            )
            self.client.publish(
                f"device/{self.config.serial_number}/request",
                json.dumps(ANNOUNCE_PUSH),
            )

    def clean_print_error(self, subtask_id: str = "", print_error: int = 0):
        """
        Clears an active print_error on the printer. Sends a clean_print_error
        command acknowledged by a push_status with print_error reset to 0.

        subtask_id: the subtask_id of the failed job (from ActiveJobInfo). Pass
            empty string to clear without a specific subtask context.
        print_error: the integer error code to clear (e.g. 50348044 for 0x0300400C
            "task was canceled"). Pass 0 to clear any active error.
        """
        import copy

        cmd = copy.deepcopy(CLEAN_PRINT_ERROR_TEMPLATE)
        cmd["print"]["subtask_id"] = subtask_id
        cmd["print"]["print_error"] = print_error
        self.client.publish(
            f"device/{self.config.serial_number}/request",
            json.dumps(cmd),
        )
        logger.debug(
            f"clean_print_error - published CLEAN_PRINT_ERROR to "
            f"[device/{self.config.serial_number}/request] subtask_id=[{subtask_id}] print_error=[{print_error}]"
        )

    def clean_print_error_uiop(self, print_error: int = 0):
        """
        Sends the UI dialog-close acknowledgment that BambuStudio sends alongside
        clean_print_error when dismissing an error dialog.

        Without this signal the printer remains in a "waiting for UI acknowledgment"
        state. Any open BambuStudio session will re-raise print_error on every
        push_status until it receives this acknowledgment. Always call this immediately
        after clean_print_error() to ensure the error stays cleared regardless of
        whether BambuStudio is open.

        print_error: the integer error code being cleared (e.g. 50348044 for
            HMS_0300-400C "task was canceled"). Used to populate the "err" field as
            an uppercase 8-character hex string (e.g. "0300400C").

        Source: BambuStudio src/slic3r/GUI/DeviceManager.cpp,
            command_clean_print_error_uiop() (lines 1253–1268).
        """
        import copy

        cmd = copy.deepcopy(CLEAN_PRINT_ERROR_UIOP_TEMPLATE)
        cmd["system"]["err"] = f"{print_error:08X}"
        self.client.publish(
            f"device/{self.config.serial_number}/request",
            json.dumps(cmd),
        )
        logger.debug(
            f"clean_print_error_uiop - published uiop dialog-close to "
            f"[device/{self.config.serial_number}/request] err=[{print_error:08X}]"
        )

    def delete_sdcard_file(self, file: str):
        """
        Delete the specified file on the printer's SDCard and returns an updated dict of all files on the printer

        Parameters
        ----------
        * file : str - the full path filename to be deleted
        """
        logger.debug(f"delete_sdcard_file - deleting remote file: [{file}]")

        with self.ftp_connection() as ftps:
            ftps.delete_file(file)

        # Invalidate all cached plate metadata for this file
        filename = file.lstrip("/").replace("/", "-")
        serial = self.config.serial_number
        cache_path = self.config.bpm_cache_path if self.config.bpm_cache_path else Path()
        if serial:
            cache_path = cache_path / serial
        for cached in (
            (cache_path / "metadata").glob(f"{filename}-*.json")
            if (cache_path / "metadata").exists()
            else []
        ):
            cached.unlink(missing_ok=True)
            logger.debug(f"delete_sdcard_file - removed cache entry [{cached.name}]")

        def search_for_and_remove_file(file: str, entry: dict):
            if "children" in entry:
                entry["children"] = list(
                    filter(lambda i: i["id"] != file, entry["children"])
                )
                for child in entry["children"]:
                    search_for_and_remove_file(file, child)

        if self._sdcard_contents:
            search_for_and_remove_file(file, self._sdcard_contents)
        if self._sdcard_3mf_files:
            search_for_and_remove_file(file, self._sdcard_3mf_files)

        logger.debug(f"delete_sdcard_file - deleted file [{file}] from sdcard")
        return self._sdcard_contents

    def delete_sdcard_folder(self, path: str):
        """
        Delete the specified folder on the printer's SDCard and returns an updated dict of all files on the printer

        Parameters
        ----------
        * path : str - the full path to folder to be deleted
        """
        logger.debug(f"delete_sdcard_folder - deleting remote folder: [{path}]")

        def delete_all_contents(ftps: IoTFTPSClient, path: str):
            fs = ftps.list_files_ex(path)
            if fs is not None:
                for item in fs:
                    if item.is_dir:
                        delete_all_contents(ftps, item.path)
                    else:
                        ftps.delete_file(item.path)
            ftps.delete_folder(path)

        with self.ftp_connection() as ftps:
            delete_all_contents(ftps, path)

        # Invalidate all cached plate metadata for files under this folder
        prefix = path.strip("/").replace("/", "-")
        serial = self.config.serial_number
        cache_path = self.config.bpm_cache_path if self.config.bpm_cache_path else Path()
        if serial:
            cache_path = cache_path / serial
        metadata_dir = cache_path / "metadata"
        if metadata_dir.exists():
            for cached in metadata_dir.glob(f"{prefix}-*.json"):
                cached.unlink(missing_ok=True)
                logger.debug(
                    f"delete_sdcard_folder - removed cache entry [{cached.name}]"
                )

        def search_for_and_remove_folder(path: str, entry: dict):
            if not path.endswith("/"):
                path = f"{path}/"
            if "children" in entry:
                entry["children"] = list(
                    filter(lambda i: not i["id"].startswith(path), entry["children"])
                )
                for child in entry["children"]:
                    search_for_and_remove_folder(path, child)

        if self._sdcard_contents is not None:
            search_for_and_remove_folder(path, self._sdcard_contents)
        if self._sdcard_3mf_files is not None:
            search_for_and_remove_folder(path, self._sdcard_3mf_files)
        return self._sdcard_contents

    def download_sdcard_file(self, src: str, dest: str):
        """
        Downloads a file from the printer

        Parameters
        ----------
        * src : str - the full path filename on the printer to be downloaded to the host
        * dest : str - the full path filename on the host to store the downloaded file
        """
        logger.debug(
            f"download_sdcard_file - downloading file src: [{src}] dest: [{dest}]"
        )
        with self.ftp_connection() as ftps:
            ftps.download_file(src, dest)

    def get_current_bind_list(self, state: "BambuState") -> list[dict[str, Any]]:
        """
        Build the `manual_ams_bind` list required by the H2D dual-extruder firmware.

        Maps each connected AMS unit to its assigned extruder using the H2D's
        hardware register inversion (RIGHT_EXTRUDER logical index 0 → hardware index 1,
        LEFT_EXTRUDER logical index 1 → hardware index 0).

        When only one AMS unit is connected the firmware still requires a two-entry
        array; a sentinel placeholder entry (Unit ID 1) is appended automatically to
        satisfy that requirement.

        Parameters
        ----------
        * state : BambuState - Current printer state supplying `ams_units` and
            `ams_connected_count`.

        Returns
        -------
        list[dict] - List of dicts with keys `ams_f_bind` (int), `ams_s_bind` (int),
            and `extruder` (int, hardware index).
        """
        bind_list = []

        # 1. Map physical units based on current logical assignments
        for unit in state.ams_units:
            # Hardware register inversion logic
            hw_target = 1 if unit.assigned_to_extruder == ActiveTool.RIGHT_EXTRUDER else 0

            bind_list.append(
                {"ams_f_bind": int(unit.ams_id), "ams_s_bind": 0, "extruder": hw_target}
            )

        # 2. Dual-Extruder Array Completeness Requirement
        # If only one AMS is connected, firmware requires a placeholder for the unused register.
        if state.ams_connected_count == 1 and len(bind_list) == 1:
            existing_assignment = bind_list[0]

            # Determine the unassigned hardware register
            placeholder_hw_target = 0 if existing_assignment["extruder"] == 1 else 1

            # Add sentinel placeholder (Unit ID 1) to complete the dual-path mapping
            bind_list.append(
                {
                    "ams_f_bind": 1,  # Placeholder Unit ID
                    "ams_s_bind": 0,
                    "extruder": placeholder_hw_target,
                }
            )

        return bind_list

    # def set_ams_to_extruder_binding(self, ams: int, extruder: int):
    #     """
    #     sets the current active tool / extruder for machines (H2 series)
    #     that have multiple extruders
    #     """
    #     cmd = copy.deepcopy(SET_AMS_TO_EXTRUDER_BINDING)
    #     extruder0 = cmd["print"]["bind_list"][1]
    #     extruder1 = cmd["print"]["bind_list"][0]

    #     if extruder == 0:
    #         extruder
    #     self.client.publish(
    #         f"device/{self.config.serial_number}/request", json.dumps(cmd)
    #     )
    #     logger.debug(
    #         f"set_active_tool - published SET_AMS_TO_EXTRUDER_BINDING to [device/{self.config.serial_number}/request] command: [{cmd}]"
    #     )

    def get_sdcard_3mf_files(self):
        """
        Returns a `dict` (json document) of all `.3mf` files on the printer's SD card.

        Usage
        -----
        The return value of this method is very useful for binding to things like a clientside `TreeView`
        """
        logger.debug("get_sdcard_3mf_files - returning sdcard_3mf_files")
        self.get_sdcard_contents()
        return self._sdcard_3mf_files

    def get_sdcard_contents(self):
        """
        Returns a `dict` (json document) of ALL files on the printer's SD card.
        The private class level `_sdcard_contents` attribute is also populated.

        Usage
        -----
        The return value of this method is very useful for binding to things like a clientside `TreeView`
        """

        with self.ftp_connection() as ftps:
            fs = self._get_sftp_files(ftps, "/")
        if fs is None:
            logger.warning("get_sdcard_contents - failed to retrieve files from sdcard")
            self._sdcard_contents = None
            self._sdcard_3mf_files = None
            return None

        self._sdcard_contents = sortFileTreeAlphabetically(fs)

        def search_for_and_remove_all_other_files(mask: str, entry: dict):
            if "children" in entry:
                entry["children"] = [
                    x
                    for x in entry["children"]
                    if x["id"].endswith(mask) or "children" in x
                ]
                for child in entry["children"]:
                    search_for_and_remove_all_other_files(mask, child)

        self._sdcard_3mf_files = json.loads(json.dumps(self._sdcard_contents))
        search_for_and_remove_all_other_files(".3mf", self._sdcard_3mf_files)

        logger.debug("get_sdcard_contents - retrieved all files from sdcard")
        return fs

    def load_filament(self, slot_id: int, ams_id: int = 0):
        """
        Requests the printer to load filament into the extruder using the requested spool (slot #)

        Parameters
        ----------
        slot_id : int

        * `0` - AMS Spool #1
        * `1` - AMS Spool #2
        * `2` - AMS Spool #3
        * `3` - AMS Spool #4
        * `254` - External Spool
        """
        # TODO: refactor to support multiple AMSs

        msg = copy.deepcopy(AMS_CHANGE_FILAMENT)

        msg["print"]["ams_id"] = ams_id
        msg["print"]["target"] = slot_id
        msg["print"]["slot_id"] = slot_id
        msg["print"]["soft_temp"] = 0
        msg["print"]["tar_temp"] = -1
        msg["print"]["curr_temp"] = -1

        self.client.publish(
            f"device/{self.config.serial_number}/request", json.dumps(msg)
        )
        logger.debug(
            f"load_filament - published AMS_CHANGE_FILAMENT to [device/{self.config.serial_number}/request] - target: [{slot_id}], bambu_msg: [{msg}]"
        )

    def make_sdcard_directory(self, dir: str):
        """
        Creates the specified directory on the printer and returns an updated dict of all files on the printer

        Parameters
        ----------
        * dir : str - the full path directory name to be created
        """
        logger.debug(f"make_sdcard_directory - creating remote directory [{dir}]")
        with self.ftp_connection() as ftps:
            ftps.mkdir(dir)
        return self.get_sdcard_contents()

    def pause_printing(self):
        """
        Pauses the current print job if one is running.
        """
        self.client.publish(
            f"device/{self.config.serial_number}/request",
            json.dumps(PAUSE_PRINT),
        )
        logger.debug(
            f"pause_printing - published PAUSE_PRINT to [device/{self.config.serial_number}/request]"
        )

    def print_3mf_file(
        self,
        name: str,
        plate: int,
        bed: PlateType,
        use_ams: bool,
        ams_mapping: str | None = "",
        bedlevel: bool | None = True,
        flow: bool | None = True,
        timelapse: bool | None = False,
    ):
        """
        Submits a request to print a `.3mf` file already stored on the printer's SD card.

        The `ams_mapping` value to pass here is available directly from
        `ProjectInfo.metadata["ams_mapping"]` returned by `get_project_info`.
        It is the same absolute-tray-ID encoding used by BambuStudio / OrcaSlicer and
        stored in the 3MF's `Metadata/slice_info.config`.

        Parameters
        ----------
        * name : str - Full SD card path to the `.3mf` file, including leading `/`
            (e.g. `"/jobs/my_project.3mf"` or `"/jobs/my_project.gcode.3mf"`).
        * plate : int - The 1-indexed plate number from the slicer to print.
            Available plate numbers are in `ProjectInfo.plates`.
        * bed : PlateType - Bed surface type to use (e.g. `PlateType.HOT_PLATE`).
            Pass `PlateType.AUTO` to let the printer decide based on slicer metadata.
        * use_ams : bool - `True` to route filament through the AMS; `False` to use
            the external spool regardless of `ams_mapping` content.
        * ams_mapping : Optional[str] = `""` - JSON array string mapping each project
            filament (0-indexed) to an absolute AMS tray ID.  Sourced from
            `ProjectInfo.metadata["ams_mapping"]` (serialised to JSON string).
            `ams_mapping2` (per-filament `{"ams_id": int, "slot_id": int}` dicts) is
            auto-generated from this value for firmware compatibility.
            Pass `""` or `None` to omit the mapping entirely.
        * bedlevel : Optional[bool] = `True` - Auto-level the bed before printing.
        * flow : Optional[bool] = `True` - Run extrusion flow calibration before printing.
        * timelapse : Optional[bool] = `False` - Record a timelapse during printing.

        Examples
        --------
        * `print_3mf_file("/jobs/my_project.3mf", 1, PlateType.HOT_PLATE, False, "")` — AMS disabled
        * `print_3mf_file("/jobs/my_project.gcode.3mf", 1, PlateType.HOT_PLATE, True, "[0,1,2]")` — 3 filaments from AMS trays 1–3

        AMS Mapping Encoding
        --------------------
        The `ams_mapping` string is a JSON integer array.  Each element is an absolute
        **tray ID** whose encoding depends on the AMS unit type:

        | AMS type                        | Formula                   | Range   |
        |---------------------------------|---------------------------|---------|
        | Standard 4-slot (AMS 2 / LITE / N3F) | `ams_id * 4 + slot_id` | 0–103  |
        | Single-slot (N3S / AMS HT)      | `ams_id` (starts at 128)  | 128–135 |
        | External spool                  | `254`                     | —       |
        | Unmapped / no AMS               | `-1`                      | —       |

        | ams_mapping    | Meaning                                          |
        |----------------|--------------------------------------------------|
        | `"[0]"`        | 1 filament → AMS 0 slot 0                        |
        | `"[0,1,4]"`    | 3 filaments → AMS 0 slots 0–1, AMS 1 slot 0     |
        | `"[0,-1,5]"`   | 3 filaments → AMS 0 slot 0, unmapped, AMS 1 slot 1 |
        | `"[0,1,2,3]"`  | 4 filaments → all 4 slots of AMS 0              |
        | `"[0,4,128]"`  | 3 filaments → AMS 0 slot 0, AMS 1 slot 0, AMS HT |

        The array is generated by the slicer (BambuStudio / OrcaSlicer) via
        color-distance matching and stored in `Metadata/slice_info.config` inside
        the `.3mf`.  `get_project_info` parses it into `ProjectInfo.metadata["ams_mapping"]`.

        See BambuStudio `DevMapping.cpp` / `DeviceManager.cpp` for the encoding logic.
        See OpenBambuAPI spec: <https://github.com/Doridian/OpenBambuAPI/blob/main/mqtt.md#ams-mapping-configuration-ams_mapping>
        """
        _3mf_file = f"{name}"
        _plate_num = int(plate)

        cmd = copy.deepcopy(PRINT_3MF_FILE)

        subtask = name[name.rindex("/") + 1 : :] if "/" in name else name
        subtask = (
            subtask[::-1].replace(".3mf"[::-1], "", 1)[::-1]
            if subtask.endswith(".3mf")
            else subtask
        )
        subtask = (
            subtask[::-1].replace(".gcode"[::-1], "", 1)[::-1]
            if subtask.endswith(".gcode")
            else subtask
        )

        cmd["print"]["file"] = _3mf_file

        if getPrinterSeriesByModel(self.config.printer_model) in (
            PrinterSeries.A1,
            PrinterSeries.P1,
        ):
            cmd["print"]["url"] = f"file:///sdcard{_3mf_file}"
        else:
            cmd["print"]["url"] = f"ftp://{_3mf_file}"

        cmd["print"]["subtask_name"] = subtask
        cmd["print"]["bed_type"] = bed.name.lower()
        cmd["print"]["param"] = cmd["print"]["param"].replace("#", str(_plate_num))
        cmd["print"]["use_ams"] = use_ams

        def decode_ams_mapping_entry(tray_id: int) -> tuple[int, int]:
            if tray_id < 0:
                return 255, 255

            if tray_id in (254, 255):
                return tray_id, 0

            # Legacy HT shorthand from some clients: 128..253 => ams_id, slot 0
            if 128 <= tray_id <= 253:
                return tray_id, 0

            # Standard protocol tray IDs (including normalized HT values like 512)
            return tray_id // 4, tray_id % 4

        # Parse ams_mapping JSON array. Values are absolute tray IDs from BambuStudio/OrcaSlicer:
        # 0-103 for 4-slot units, 128-135 for 1-slot units, -1 for unmapped.
        # See: https://github.com/bambulab/BambuStudio/blob/main/src/slic3r/GUI/DeviceCore/DevMapping.cpp
        if ams_mapping and len(ams_mapping) > 0:
            parsed_ams_mapping = [int(x) for x in json.loads(ams_mapping)]
            parsed_ams_mapping2 = []
            for tray_id in parsed_ams_mapping:
                ams_id, slot_id = decode_ams_mapping_entry(tray_id)
                parsed_ams_mapping2.append({"ams_id": ams_id, "slot_id": slot_id})

            cmd["print"]["ams_mapping"] = parsed_ams_mapping
            cmd["print"]["ams_mapping2"] = parsed_ams_mapping2

        cmd["print"]["bed_leveling"] = bedlevel
        cmd["print"]["flow_cali"] = flow
        cmd["print"]["timelapse"] = timelapse
        self.client.publish(
            f"device/{self.config.serial_number}/request", json.dumps(cmd)
        )
        logger.debug(
            f"print_3mf_file - published PRINT_3MF_FILE to [device/{self.config.serial_number}/request] print_command: [{cmd}]"
        )

    def refresh_nozzles(self):
        """
        Requests the printer to push back current nozzle state.
        Used for multi-extruder models (H2D, H2D Pro) where nozzles are manually swapped.
        """
        cmd = copy.deepcopy(REFRESH_NOZZLE)

        self.client.publish(
            f"device/{self.config.serial_number}/request", json.dumps(cmd)
        )
        logger.debug(
            f"refresh_nozzles - published REFRESH_NOZZLE to [device/{self.config.serial_number}/request] bambu_msg: [{cmd}]"
        )

    def refresh_spool_rfid(self, slot_id: int, ams_id: int = 0):
        """
        Request the printer to re-read the RFID tag for the specified AMS slot.

        Only RFID-equipped Bambu Lab spools carry tag data.  The printer will push
        an updated telemetry message containing the spool details after scanning.

        Parameters
        ----------
        * slot_id : int - The slot within the AMS unit to scan (0–3 for standard AMS).
        * ams_id : int = 0 - The AMS unit containing the slot (default is 0).
        """
        cmd = copy.deepcopy(AMS_GET_RFID)
        cmd["print"]["ams_id"] = ams_id
        cmd["print"]["slot_id"] = slot_id

        self.client.publish(
            f"device/{self.config.serial_number}/request", json.dumps(cmd)
        )
        logger.debug(
            f"refresh_spool_rfid - published AMS_GET_RFID to [device/{self.config.serial_number}/request] command: [{cmd}]"
        )

    def rename_printer(self, new_name: str):
        """
        Rename the printer to the specified new name.
        """
        cmd = copy.deepcopy(RENAME_PRINTER)
        cmd["update"]["name"] = new_name

        self.client.publish(
            f"device/{self.config.serial_number}/request", json.dumps(cmd)
        )
        logger.debug(
            f"rename_printerq - published RENAME_PRINTER to [device/{self.config.serial_number}/request] command: [{cmd}]"
        )

    def rename_sdcard_file(self, src: str, dest: str):
        """
        Renames the specified file on the printer and returns an updated dict of all files on the printer

        Parameters
        ----------
        * src : str - the full path name to be renamed
        * dest : str - the full path name to be renamed to
        """
        logger.debug(f"rename_sdcard_file - renaming printer file [{src}] to [{dest}]")
        with self.ftp_connection() as ftps:
            ftps.move_file(src, dest)
        return self.get_sdcard_contents()

    def resume_printing(self):
        """
        Resumes the current print job if one is paused.
        """
        self.client.publish(
            f"device/{self.config.serial_number}/request",
            json.dumps(RESUME_PRINT),
        )
        logger.debug(
            f"resume_printing - published RESUME_PRINT to [device/{self.config.serial_number}/request]"
        )

    def sdcard_file_exists(self, path: str) -> bool:
        """
        Checks to see if a file exists on the printer at the `path` specified

        Parameters
        ----------
        * path : str - the full path name to check
        """
        logger.debug(f"sdcard_file_exists - checking if printer file [{path}] exists")
        with self.ftp_connection() as ftps:
            return ftps.fexists(path)

    def select_extrusion_calibration_profile(self, tray_id: int, cali_idx: int = -1):
        """
        Sets the k factor profile for the specified tray.

        Parameters
        ----------
        tray_id : int - tray id
        cali_idx : calibration index , optional, defaults to -1 (the default profile)
        """
        cmd = copy.deepcopy(EXTRUSION_CALI_SEL)

        ams_id = math.floor(tray_id / 4)
        slot_id = tray_id % 4
        if tray_id == 254 or tray_id == 255:
            ams_id = tray_id
            slot_id = 0

        cmd["print"]["ams_id"] = ams_id
        cmd["print"]["tray_id"] = tray_id
        cmd["print"]["slot_id"] = slot_id
        cmd["print"]["cali_idx"] = cali_idx

        self.client.publish(
            f"device/{self.config.serial_number}/request", json.dumps(cmd)
        )
        logger.debug(
            f"select_extrusion_calibration_profile - published EXTRUSION_CALI_SEL to [device/{self.config.serial_number}/request] cmd: [{cmd}]"
        )

    def send_ams_control_command(self, ams_control_cmd: AMSControlCommand):
        """
        Send an AMS control command to pause, resume, or reset the AMS.

        When `AMSControlCommand.RESUME` is sent, `resume_printing()` is also called
        automatically to restart the paused print job.

        Parameters
        ----------
        * ams_control_cmd : AMSControlCommand - The control command to send
            (`AMSControlCommand.PAUSE`, `AMSControlCommand.RESUME`, or `AMSControlCommand.RESET`).
        """
        ams_cmd = ams_control_cmd.name.lower()
        cmd = copy.deepcopy(AMS_CONTROL)
        cmd["print"]["param"] = ams_cmd

        self.client.publish(
            f"device/{self.config.serial_number}/request", json.dumps(cmd)
        )
        logger.debug(
            f"send_ams_control_commandpublished AMS_CONTROL to [device/{self.config.serial_number}/request] bambu_msg: [{cmd}]"
        )

        # trigger resume print for good measure
        if ams_control_cmd == AMSControlCommand.RESUME:
            self.resume_printing()

    def send_anything(self, anything: str):
        """
        Publish an arbitrary JSON string directly to the printer's MQTT request topic.

        Intended for advanced use / debugging — bypasses all validation and command
        abstraction.  The string is parsed then re-serialised before publishing, so
        it must be valid JSON.

        Parameters
        ----------
        * anything : str - A valid JSON string to publish.
        """
        self.client.publish(
            f"device/{self.config.serial_number}/request",
            json.dumps(json.loads(anything)),
        )
        logger.debug(
            f"send_anything - published message to [device/{self.config.serial_number}/request] message: [{anything}]"
        )

    def send_gcode(self, gcode: str):
        """
        Submit one, or more, gcode commands to the printer.  To submit multiple gcode commands, separate them with a newline (\\n) character.

        Parameters
        ----------
        gcode : str

        Examples
        --------
        * `send_gcode("G91\\nG0 X0\\nG0 X50")` - queues 3 gcode commands on the printer for processing
        * `send_gcode("G28")` - queues 1 gcode command on the printer for processing
        """
        cmd = copy.deepcopy(SEND_GCODE_TEMPLATE)
        cmd["print"]["param"] = f"{gcode} \n"
        self.client.publish(
            f"device/{self.config.serial_number}/request", json.dumps(cmd)
        )
        logger.debug(
            f"send_gcode - published SEND_GCODE_TEMPLATE to [device/{self.config.serial_number}/request] gcode: [{gcode}]"
        )

    def set_active_tool(self, id: int):
        """
        Set the active extruder on multi-tool machines (H2D / H2D Pro).

        Sends a `SET_ACTIVE_TOOL` command that switches which extruder the printer
        uses for subsequent moves and extrusions.

        Parameters
        ----------
        * id : int - The extruder index to activate (`0` = right extruder, `1` = left extruder
            on H2D; see `ActiveTool` enum for named constants).
        """
        cmd = copy.deepcopy(SET_ACTIVE_TOOL)
        cmd["print"]["extruder_index"] = id
        self.client.publish(
            f"device/{self.config.serial_number}/request", json.dumps(cmd)
        )
        logger.debug(
            f"set_active_tool - published SET_ACTIVE_TOOL to [device/{self.config.serial_number}/request] command: [{cmd}]"
        )

    def set_airprinting_detector(
        self, enabled: bool, sensitivity: DetectorSensitivity = DetectorSensitivity.MEDIUM
    ):
        """
        Enable or disable the air-printing / no-extrusion detector (X-Cam AI vision).

        When triggered, the printer halts the print because the nozzle is detected to
        be extruding into open air rather than onto the bed or model.  State is persisted
        to `config.airprinting_detector` and `config.airprinting_detector_sensitivity`.

        Parameters
        ----------
        * enabled : bool - `True` to enable the detector, `False` to disable it.
        * sensitivity : DetectorSensitivity = `DetectorSensitivity.MEDIUM` - Detection threshold.
        """
        cmd = copy.deepcopy(XCAM_CONTROL_SET)
        cmd["xcam"]["module_name"] = "airprint_detector"
        cmd["xcam"]["control"] = enabled
        cmd["xcam"]["enable"] = enabled
        cmd["xcam"]["print_halt"] = True
        cmd["xcam"]["halt_print_sensitivity"] = sensitivity.value

        self.client.publish(
            f"device/{self.config.serial_number}/request", json.dumps(cmd)
        )

        self.config.airprinting_detector = enabled
        self.config.airprinting_detector_sensitivity = sensitivity.value

        logger.debug(
            f"set_airprinting_detector - published XCAM_CONTROL_SET to [device/{self.config.serial_number}/request] bambu_msg: [{cmd}]"
        )

    def set_ams_user_setting(
        self, setting: AMSUserSetting, enabled: bool, ams_id: int = 0
    ):
        """
        Enable or disable one of the `AMSUserSetting` options on the specified AMS unit.

        The three settings — `CALIBRATE_REMAIN_FLAG`, `STARTUP_READ_OPTION`, and
        `TRAY_READ_OPTION` — are all sent together in a single command, with only
        `setting` toggled to the new value.  The corresponding `BambuConfig` attribute
        is also updated.

        Parameters
        ----------
        * setting : AMSUserSetting - The AMS user setting to change.
        * enabled : bool - `True` to enable the setting, `False` to disable it.
        * ams_id : int = 0 - The AMS unit to target (default is 0).
        """
        cmd = copy.deepcopy(AMS_USER_SETTING)
        cmd["print"]["ams_id"] = ams_id
        cmd["print"][AMSUserSetting.CALIBRATE_REMAIN_FLAG.name.lower()] = (
            self.config.calibrate_remain_flag
        )
        cmd["print"][AMSUserSetting.STARTUP_READ_OPTION.name.lower()] = (
            self.config.startup_read_option
        )
        cmd["print"][AMSUserSetting.TRAY_READ_OPTION.name.lower()] = (
            self.config.tray_read_option
        )

        cmd["print"][setting.name.lower()] = enabled

        if setting == AMSUserSetting.STARTUP_READ_OPTION:
            self.config.startup_read_option = enabled
        elif setting == AMSUserSetting.TRAY_READ_OPTION:
            self.config.tray_read_option = enabled
        elif setting == AMSUserSetting.CALIBRATE_REMAIN_FLAG:
            self.config.calibrate_remain_flag = enabled

        self.client.publish(
            f"device/{self.config.serial_number}/request", json.dumps(cmd)
        )
        logger.debug(
            f"set_ams_user_setting - published AMS_USER_SETTING to [device/{self.config.serial_number}/request] bambu_msg: [{cmd}]"
        )

    def set_aux_fan_speed_target_percent(self, value: int):
        """
        sets the aux (chamber recirculation) fan speed target represented in percent

        Parameters
        ----------
        * value : int - The target speed in percent
        """
        if value < 0:
            value = 0
        self._printer_state.climate.zone_aux_percent = value
        speed = round(value * 2.55, 0)
        gcode = SEND_GCODE_TEMPLATE
        gcode["print"]["param"] = f"M106 P2 S{speed}\n"
        self.client.publish(
            f"device/{self.config.serial_number}/request", json.dumps(gcode)
        )
        logger.debug(
            f"set_aux_fan_speed_target_percent - published SEND_GCODE_TEMPLATE to [device/{self.config.serial_number}/request] command: [{gcode}]"
        )
        # self._fan_speed_target_time = round(time.time())

    def set_bed_temp_target(self, value: int):
        """
        Sets the bed temperature target.

        Parameters
        ----------
        * value : float - The target bed temperature.
        """
        if value < 0:
            value = 0
        gcode = SEND_GCODE_TEMPLATE
        gcode["print"]["param"] = f"M140 S{value}\n"
        self.client.publish(
            f"device/{self.config.serial_number}/request", json.dumps(gcode)
        )
        logger.debug(
            f"set_bed_temp_target - published SEND_GCODE_TEMPLATE to [device/{self.config.serial_number}/request] command: [{gcode}]"
        )
        self._bed_temp_target_time = round(time.time())

    def set_buildplate_marker_detector(self, enabled: bool):
        """
        Enable or disable the buildplate marker detector (X-Cam AI vision).

        When enabled, the printer's camera checks for the calibration marker on the
        build plate before starting a print.  The state is also written to
        `config.buildplate_marker_detector`.

        Parameters
        ----------
        * enabled : bool - `True` to enable the detector, `False` to disable it.
        """
        cmd = copy.deepcopy(XCAM_CONTROL_SET)
        cmd["xcam"]["module_name"] = "buildplate_marker_detector"
        cmd["xcam"]["control"] = enabled
        cmd["xcam"]["enable"] = enabled

        self.client.publish(
            f"device/{self.config.serial_number}/request", json.dumps(cmd)
        )

        self.config.buildplate_marker_detector = enabled

        logger.debug(
            f"set_buildplate_marker_detector - published XCAM_CONTROL_SET to [device/{self.config.serial_number}/request] bambu_msg: [{cmd}]"
        )

    def set_chamber_temp(self, value: float):
        """
        for printers that do not have managed chambers, this enables you to inject
        a chamber temperature value from an external source

        Parameters
        ----------
        * value : float - The chamber temperature.
        """
        self._printer_state.climate.chamber_temp = value

    def set_chamber_temp_target(self, value: int, temper_check: bool = True):
        """
        set chamber temperature target if printer supports it, otherwise just
        store the value

        Parameters
        ----------
        * value : float - The target chamber temperature.
        * temper_check : OPTIONAL bool - perform a temperature check?
        """
        if self.config.capabilities.has_chamber_temp:
            cmd = copy.deepcopy(SET_CHAMBER_TEMP_TARGET)
            cmd["print"]["ctt_val"] = value
            cmd["print"]["temper_check"] = temper_check

            self.client.publish(
                f"device/{self.config.serial_number}/request", json.dumps(cmd)
            )
            logger.debug(
                f"set_chamber_temp_target - published SET_CHAMBER_TEMP_TARGET to [device/{self.config.serial_number}/request] command: [{cmd}]"
            )

            cmd = copy.deepcopy(SET_CHAMBER_AC_MODE)

            if value < 40:
                cmd["print"]["modeId"] = 0
            else:
                cmd["print"]["modeId"] = 1
            self.client.publish(
                f"device/{self.config.serial_number}/request", json.dumps(cmd)
            )
            logger.debug(
                f"set_chamber_temp_target - published SET_CHAMBER_AC_MODE to [device/{self.config.serial_number}/request] command: [{cmd}]"
            )

        self._printer_state.climate.chamber_temp_target = value
        self._chamber_temp_target_time = round(time.time())

    def set_exhaust_fan_speed_target_percent(self, value: int):
        """
        sets the exhaust (chamber) fan speed target represented in percent

        Parameters
        ----------
        * value : int - The target speed in percent
        """
        if value < 0:
            value = 0
        self._printer_state.climate.zone_exhaust_percent = value
        speed = round(value * 2.55, 0)
        gcode = SEND_GCODE_TEMPLATE
        gcode["print"]["param"] = f"M106 P3 S{speed}\n"
        self.client.publish(
            f"device/{self.config.serial_number}/request", json.dumps(gcode)
        )
        logger.debug(
            f"set_exhaust_fan_speed_target_percent - published SEND_GCODE_TEMPLATE to [device/{self.config.serial_number}/request] command: [{gcode}]"
        )
        # self._fan_speed_target_time = round(time.time())

    def set_nozzle_details(
        self, nozzle_diameter: NozzleDiameter, nozzle_type: NozzleType
    ):
        """
        Inform the printer of the nozzle currently installed.

        Sends a `SET_ACCESSORIES` command so the firmware can apply the correct
        temperature limits, flow rates, and material compatibility checks.

        Parameters
        ----------
        * nozzle_diameter : NozzleDiameter - The physical nozzle diameter
            (e.g. `NozzleDiameter.DIAMETER_0_4`).
        * nozzle_type : NozzleType - The nozzle material / type
            (e.g. `NozzleType.HARDENED_STEEL`, `NozzleType.STAINLESS_STEEL`).
        """
        cmd = copy.deepcopy(SET_ACCESSORIES)
        cmd["system"]["nozzle_diameter"] = nozzle_diameter.value
        cmd["system"]["nozzle_type"] = nozzle_type_to_telemetry(nozzle_type)

        self.client.publish(
            f"device/{self.config.serial_number}/request", json.dumps(cmd)
        )
        logger.debug(
            f"set_nozzle_details - published SET_ACCESSORIES to [device/{self.config.serial_number}/request] bambu_msg: [{cmd}]"
        )

    def set_nozzle_temp_target(self, value: int, tool_num: int = -1):
        """
        Sets the nozzle temperature target.

        Parameters
        ----------
        * value : float - The target nozzle temperature.
        * tool_num : int - The tool number (default is 0).
        """
        if value < 0:
            value = 0
        gcode = SEND_GCODE_TEMPLATE
        gcode["print"]["param"] = (
            f"M104 S{value}{'' if tool_num == -1 else ' T' + str(tool_num)}\n"
        )
        self.client.publish(
            f"device/{self.config.serial_number}/request", json.dumps(gcode)
        )
        logger.debug(
            f"set_nozzle_temp_target - published SEND_GCODE_TEMPLATE to [device/{self.config.serial_number}/request] command: [{gcode}]"
        )
        self._tool_temp_target_time = round(time.time())

    def set_nozzleclumping_detector(
        self, enabled: bool, sensitivity: DetectorSensitivity = DetectorSensitivity.MEDIUM
    ):
        """
        Enable or disable the nozzle clumping / blob detector (X-Cam AI vision).

        When triggered, the printer halts the print to prevent damage from filament
        build-up on the nozzle.  State is persisted to `config.nozzleclumping_detector`
        and `config.nozzleclumping_detector_sensitivity`.

        Parameters
        ----------
        * enabled : bool - `True` to enable the detector, `False` to disable it.
        * sensitivity : DetectorSensitivity = `DetectorSensitivity.MEDIUM` - Detection threshold.
        """
        cmd = copy.deepcopy(XCAM_CONTROL_SET)
        cmd["xcam"]["module_name"] = "clump_detector"
        cmd["xcam"]["control"] = enabled
        cmd["xcam"]["enable"] = enabled
        cmd["xcam"]["print_halt"] = True
        cmd["xcam"]["halt_print_sensitivity"] = sensitivity.value

        self.client.publish(
            f"device/{self.config.serial_number}/request", json.dumps(cmd)
        )

        self.config.nozzleclumping_detector = enabled
        self.config.nozzleclumping_detector_sensitivity = sensitivity.value

        logger.debug(
            f"set_nozzleclumping_detector - published XCAM_CONTROL_SET to [device/{self.config.serial_number}/request] bambu_msg: [{cmd}]"
        )

    def set_part_cooling_fan_speed_target_percent(self, value: int):
        """
        sets the part cooling fan speed target represented in percent

        Parameters
        ----------
        * value : int - The target speed in percent
        """
        if value < 0:
            value = 0
        self._printer_state.climate.part_cooling_fan_speed_target_percent = value
        speed = round(value * 2.55, 0)
        gcode = SEND_GCODE_TEMPLATE
        gcode["print"]["param"] = f"M106 P1 S{speed}\n"
        self.client.publish(
            f"device/{self.config.serial_number}/request", json.dumps(gcode)
        )
        logger.debug(
            f"set_part_cooling_fan_speed_target_percent - published SEND_GCODE_TEMPLATE to [device/{self.config.serial_number}/request] command: [{gcode}]"
        )
        self._fan_speed_target_time = round(time.time())

    def set_print_option(self, option: PrintOption, enabled: bool):
        """
        Enable or disable one of the `PrintOption` options.

        The corresponding `BambuConfig` attribute is also updated so the new state
        persists in the local configuration object.

        Parameters
        ----------
        * option : PrintOption - The print option to change (e.g. `PrintOption.AUTO_RECOVERY`).
        * enabled : bool - `True` to enable the option, `False` to disable it.
        """
        cmd = PRINT_OPTION_COMMAND
        cmd["print"][option.name.lower()] = enabled

        if option == PrintOption.AUTO_RECOVERY:
            cmd["print"]["option"] = 1 if enabled else 0
            self.config.auto_recovery = enabled
        elif option == PrintOption.AUTO_SWITCH_FILAMENT:
            self.config.auto_switch_filament = enabled
        elif option == PrintOption.FILAMENT_TANGLE_DETECT:
            self.config.filament_tangle_detect = enabled
        elif option == PrintOption.SOUND_ENABLE:
            self.config.sound_enable = enabled
        elif option == PrintOption.NOZZLE_BLOB_DETECT:
            self.config.nozzle_blob_detect = enabled
        elif option == PrintOption.AIR_PRINT_DETECT:
            self.config.air_print_detect = enabled

        self.client.publish(
            f"device/{self.config.serial_number}/request", json.dumps(cmd)
        )
        logger.debug(
            f"set_print_option - published PRINT_OPTION_COMMAND to [device/{self.config.serial_number}/request] bambu_msg: [{cmd}]"
        )

    def set_purgechutepileup_detector(
        self, enabled: bool, sensitivity: DetectorSensitivity = DetectorSensitivity.MEDIUM
    ):
        """
        Enable or disable the purge chute pile-up detector (X-Cam AI vision).

        When triggered, the printer halts the print to prevent purge waste from
        blocking the toolhead.  State is persisted to `config.purgechutepileup_detector`
        and `config.purgechutepileup_detector_sensitivity`.

        Parameters
        ----------
        * enabled : bool - `True` to enable the detector, `False` to disable it.
        * sensitivity : DetectorSensitivity = `DetectorSensitivity.MEDIUM` - Detection threshold.
        """
        cmd = copy.deepcopy(XCAM_CONTROL_SET)
        cmd["xcam"]["module_name"] = "pileup_detector"
        cmd["xcam"]["control"] = enabled
        cmd["xcam"]["enable"] = enabled
        cmd["xcam"]["print_halt"] = True
        cmd["xcam"]["halt_print_sensitivity"] = sensitivity.value

        self.client.publish(
            f"device/{self.config.serial_number}/request", json.dumps(cmd)
        )

        self.config.purgechutepileup_detector = enabled
        self.config.purgechutepileup_detector_sensitivity = sensitivity.value

        logger.debug(
            f"set_purgechutepileup_detector - published XCAM_CONTROL_SET to [device/{self.config.serial_number}/request] bambu_msg: [{cmd}]"
        )

    def set_spaghetti_detector(
        self, enabled: bool, sensitivity: DetectorSensitivity = DetectorSensitivity.MEDIUM
    ):
        """
        Enable or disable the spaghetti / failed print detector (X-Cam AI vision).

        When triggered, the printer halts the print.  Sensitivity controls how
        aggressively the camera flags anomalies.  State is persisted to
        `config.spaghetti_detector` and `config.spaghetti_detector_sensitivity`.

        Parameters
        ----------
        * enabled : bool - `True` to enable the detector, `False` to disable it.
        * sensitivity : DetectorSensitivity = `DetectorSensitivity.MEDIUM` - Detection threshold.
        """
        cmd = copy.deepcopy(XCAM_CONTROL_SET)
        cmd["xcam"]["module_name"] = "spaghetti_detector"
        cmd["xcam"]["control"] = enabled
        cmd["xcam"]["enable"] = enabled
        cmd["xcam"]["print_halt"] = True
        cmd["xcam"]["halt_print_sensitivity"] = sensitivity.value

        self.client.publish(
            f"device/{self.config.serial_number}/request", json.dumps(cmd)
        )

        self.config.spaghetti_detector = enabled
        self.config.spaghetti_detector_sensitivity = sensitivity.value

        logger.debug(
            f"set_spaghetti_detector - published XCAM_CONTROL_SET to [device/{self.config.serial_number}/request] bambu_msg: [{cmd}]"
        )

    def set_spool_details(
        self,
        tray_id: int,
        tray_info_idx: str,
        tray_id_name: str | None = "",
        tray_type: str | None = "",
        tray_color: str | None = "",
        nozzle_temp_min: int | None = -1,
        nozzle_temp_max: int | None = -1,
        ams_id: int | None = 0,
    ):
        """
        Sets spool / tray details such as filament type, color, and nozzle temperature range.

        `ams_id` and `slot_id` are derived automatically from `tray_id`.
        For the external tray (254), pass `"no_filament"` as `tray_info_idx` to
        clear the tray entirely.  Colors may be supplied as CSS color names (e.g.
        `"red"`) or as 6- or 8-character hex strings (e.g. `"FF0000"` / `"FF0000FF"`).

        Parameters
        ----------
        * tray_id : int - Absolute tray ID.  For standard 4-slot AMS: `ams_id * 4 + slot_id`.
                    Use `254` for the external spool holder.
        * tray_info_idx : str - Filament info index string as defined by Bambu Lab (e.g. `"GFA00"`).
                    Pass `"no_filament"` to clear the tray.
        * tray_id_name : Optional[str] - Friendly filament name (e.g. `"Bambu PLA Basic"`).
        * tray_type : Optional[str] - Short filament type string (e.g. `"PLA"`, `"PETG"`, `"ABS"`).
        * tray_color : Optional[str] - Filament color as a CSS name or RRGGBB/RRGGBBAA hex string.
        * nozzle_temp_min : Optional[int] = -1 - Minimum nozzle temperature in °C (pass -1 to leave unchanged).
        * nozzle_temp_max : Optional[int] = -1 - Maximum nozzle temperature in °C (pass -1 to leave unchanged).
        * ams_id : Optional[int] = 0 - Unused; derived automatically from `tray_id`.
        """
        cmd = copy.deepcopy(AMS_FILAMENT_SETTING)

        ams_id = math.floor(tray_id / 4)
        slot_id = tray_id % 4
        if tray_id == 254 or tray_id == 255:
            ams_id = tray_id
            slot_id = 0

        cmd["print"]["ams_id"] = ams_id
        cmd["print"]["tray_id"] = tray_id
        cmd["print"]["slot_id"] = slot_id

        if tray_info_idx == "no_filament":
            tray_info_idx = ""
            tray_id_name = ""
            tray_type = ""
            tray_color = "FFFFFF00"
            nozzle_temp_min = 0
            nozzle_temp_max = 0

        cmd["print"]["tray_info_idx"] = tray_info_idx
        cmd["print"]["tray_id_name"] = tray_id_name
        cmd["print"]["tray_type"] = tray_type

        if tray_color and tray_color != "":
            color = ""
            try:
                color = f"{name_to_hex(tray_color)}FF".replace("#", "").upper()
            except Exception:
                color = tray_color
            cmd["print"]["tray_color"] = color

        cmd["print"]["nozzle_temp_min"] = nozzle_temp_min
        cmd["print"]["nozzle_temp_max"] = nozzle_temp_max

        self.client.publish(
            f"device/{self.config.serial_number}/request", json.dumps(cmd)
        )
        logger.debug(
            f"set_spool_details - published AMS_FILAMENT_SETTING to [device/{self.config.serial_number}/request] bambu_msg: [{cmd}]"
        )

    def set_spool_k_factor(
        self,
        tray_id: int,
        k_value: float,
        n_coef: float | None = 1.399999976158142,
        nozzle_temp: int | None = -1,
        bed_temp: int | None = -1,
        max_volumetric_speed: int | None = -1,
    ):
        """
        Set the linear advance (pressure advance) k factor for a specific spool tray.

        !!! warning "Deprecated"
            Broken in recent Bambu firmware.  Use
            [`select_extrusion_calibration_profile`][bpm.bambuprinter.BambuPrinter.select_extrusion_calibration_profile]
            instead.

        Parameters
        ----------
        * tray_id : int - Absolute tray ID (`ams_id * 4 + slot_id`, or `254` for external).
        * k_value : float - The linear advance k factor to apply.
        * n_coef : Optional[float] = 1.4 - Pressure advance n coefficient.
        * nozzle_temp : Optional[int] = -1 - Nozzle temperature in °C (pass -1 to omit).
        * bed_temp : Optional[int] = -1 - Bed temperature in °C (pass -1 to omit).
        * max_volumetric_speed : Optional[int] = -1 - Max volumetric speed (pass -1 to omit).
        """
        cmd = copy.deepcopy(EXTRUSION_CALI_SET)

        cmd["print"]["tray_id"] = tray_id
        cmd["print"]["slot_id"] = tray_id % 4

        cmd["print"]["k_value"] = k_value
        cmd["print"]["n_coef"] = n_coef

        if nozzle_temp != -1:
            cmd["print"]["nozzle_temp"] = nozzle_temp
        if bed_temp != -1:
            cmd["print"]["bed_temp"] = bed_temp
        if max_volumetric_speed != -1:
            cmd["print"]["max_volumetric_speed"] = max_volumetric_speed

        self.client.publish(
            f"device/{self.config.serial_number}/request", json.dumps(cmd)
        )
        logger.debug(
            f"set_spool_k_factor - published EXTRUSION_CALI_SET to [device/{self.config.serial_number}/request] bambu_msg: [{cmd}]"
        )

    def skip_objects(self, objects):
        """
        Instructs the printer to skip (cancel) a list of objects during the current print job.

        The printhead physically avoids skipped objects for the remainder of the print.
        This is equivalent to the "Cancel Object" feature in BambuStudio.

        **Object ID mapping**

        Object IDs sent here are the `identify_id` values from `Metadata/slice_info.config`
        inside the `.3mf`.  `get_project_info` extracts them and writes each one into the
        corresponding `bbox_objects[N]["id"]` entry in `ProjectInfo.metadata["map"]`.

        To get the IDs for the current plate:

        ```python
        info = get_project_info(file_id, printer, plate_num=1)
        ids = [obj["id"] for obj in info.metadata["map"]["bbox_objects"] if "id" in obj]
        printer.skip_objects(ids)   # cancel all objects on the plate
        ```

        The `bbox_objects` list also carries `name` and bounding-box coordinates so a UI
        can let the user pick individual objects before calling this method.

        Parameters
        ----------
        * objects : list[int | str] - One or more `identify_id` values to cancel.
            Values are coerced to `int` before being sent to the printer.
        """
        objs = []
        for obj in objects:
            objs.append(int(obj))

        cmd = copy.deepcopy(SKIP_OBJECTS)
        cmd["print"]["obj_list"] = objs
        self.client.publish(
            f"device/{self.config.serial_number}/request", json.dumps(cmd)
        )
        logger.debug(
            f"skip_objects - published SKIP_OBJECTS to [device/{self.config.serial_number}/request] bambu_msg: [{cmd}]"
        )

    def stop_printing(self):
        """
        Requests the printer to stop printing if a job is currently running.
        """
        self.client.publish(
            f"device/{self.config.serial_number}/request",
            json.dumps(STOP_PRINT),
        )
        logger.debug(
            f"stop_printing - published STOP_PRINT to [device/{self.config.serial_number}/request]"
        )

    def toJson(self):
        """
        Returns a `dict` (json document) representing this object's private class
        level attributes that are serializable (most are).
        """
        response = json.dumps(self, default=jsonSerializer, indent=4, sort_keys=True)
        # logger.debug(f"toJson - json: [{response}]")

        return json.loads(response)

    def turn_off_ams_dryer(self, ams_id: int = 0):
        """
        Sends a command to the printer to turn off the AMS dryer.

        Also resets `ams_unit.temp_target` to `0` in the local printer state.
        Raises an exception if `ams_id` does not match a connected AMS unit.

        Parameters
        ----------
        * ams_id : int = 0 - The AMS unit whose dryer should be turned off (default is 0).
        """
        cmd = copy.deepcopy(AMS_FILAMENT_DRYING)
        cmd["print"]["ams_id"] = ams_id
        cmd["print"]["mode"] = 0  # Turn off drying mode
        self.client.publish(
            f"device/{self.config.serial_number}/request", json.dumps(cmd)
        )

        ams = next((u for u in self._printer_state.ams_units if u.ams_id == ams_id), None)
        if not ams:
            raise Exception("invalid ams_id provided")

        ams.temp_target = 0

        logger.debug(
            f"turn_off_ams_dryer - published AMS_FILAMENT_DRYING to [device/{self.config.serial_number}/request] command: [{cmd}]"
        )

    def turn_on_ams_dryer(
        self,
        target_temp: int,
        duration: int,
        target_humidity: int = 0,
        cooling_temp: int = 45,
        rotate_tray: bool = False,
        ams_id: int = 0,
        filament_type: str = "",
    ):
        """
        Sends a command to the printer to turn on the AMS dryer with specified parameters.

        Parameters
        ----------
        * target_temp : int - The target drying temperature.
        * duration : int - The drying duration in hours.
        * target_humidity : int - The target humidity level.
        * cooling_temp : int - The cooling temperature after drying (default is 45).
        * rotate_tray : bool - Whether to rotate the tray during drying (default is False).
        * ams_id : int - The AMS ID to control (default is 0).
        * filament_type : str - The filament type string (e.g. 'ABS'). Passed to firmware for validation.
        """
        cmd = copy.deepcopy(AMS_FILAMENT_DRYING)
        cmd["print"]["ams_id"] = ams_id
        cmd["print"]["mode"] = 1  # Turn on drying mode
        cmd["print"]["filament"] = filament_type
        cmd["print"]["temp"] = target_temp
        cmd["print"]["duration"] = duration
        cmd["print"]["humidity"] = target_humidity
        cmd["print"]["cooling_temp"] = cooling_temp
        cmd["print"]["rotate_tray"] = rotate_tray
        self.client.publish(
            f"device/{self.config.serial_number}/request", json.dumps(cmd)
        )

        ams = next((u for u in self._printer_state.ams_units if u.ams_id == ams_id), None)
        if not ams:
            raise Exception("invalid ams_id provided")

        ams.temp_target = target_temp

        logger.debug(
            f"turn_on_ams_dryer - published AMS_FILAMENT_DRYING to [device/{self.config.serial_number}/request] command: [{cmd}]"
        )

    def unload_filament(self, ams_id: int = 0):
        """
        Requests the printer to unload whatever filament / spool is currently loaded.

        Parameters
        ----------
        * ams_id : int = 0 - The AMS unit to unload from (default is 0).
        """
        msg = copy.deepcopy(AMS_CHANGE_FILAMENT)
        msg["print"]["ams_id"] = ams_id

        self.client.publish(
            f"device/{self.config.serial_number}/request",
            json.dumps(msg),
        )
        logger.debug(
            f"unload_filament - published AMS_CHANGE_FILAMENT to [device/{self.config.serial_number}/request] - bambu_msg: [{msg}]"
        )

    def upload_sdcard_file(self, src: str, dest: str):
        """
        Uploads the local filesystem file to the printer and returns an updated dict of all files on the printer

        Parameters
        ----------
        * src : str - the full path filename on the host to be uploaded to the printer
        * dest : str - the full path filename on the printer to upload to
        """
        logger.debug(f"upload_sdcard_file - uploading file src: [{src}] dest: [{dest}]")
        with self.ftp_connection() as ftps:
            ftps.upload_file(src, dest)

        if src.endswith(".3mf"):
            get_project_info(dest, self, local_file=src)

        remote_files = self.get_sdcard_contents()
        return remote_files

    # endregion

    # region public properties

    @property
    def config(self) -> BambuConfig:
        """The settings used to connect to and configure the printer's behavior."""
        return self._config

    @config.setter
    def config(self, value: BambuConfig):
        self._config = value

    @property
    def service_state(self):
        """The current service connection state."""
        return self._service_state

    @service_state.setter
    def service_state(self, value: ServiceState):
        self._service_state = value
        self._notify_update()  # make sure we notify about EVERY state change!

    @property
    def client(self) -> mqtt.Client:
        """The networking client used to communicate with the printer.

        This is a private property
        """
        if self._client:
            return self._client
        else:
            # return mqtt.Client()
            return mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)  # type: ignore

    @client.setter
    def client(self, value: mqtt.Client):
        self._client = value

    @property
    def on_update(self):
        """The callback function executed whenever the printer's state is updated."""
        return self._on_update

    @on_update.setter
    def on_update(self, value):
        self._on_update = value

    @property
    def recent_update(self):
        """Indicates if the printer's state has been updated recently."""
        return self._recent_update

    @property
    def bed_temp_target_time(self):
        """Timestamp of the last change to the heatbed target temperature."""
        return self._bed_temp_target_time

    @property
    def tool_temp_target_time(self):
        """Timestamp of the last change to the nozzle target temperature."""
        return self._tool_temp_target_time

    @property
    def chamber_temp_target_time(self):
        """Timestamp of the last change to the chamber target temperature."""
        return self._chamber_temp_target_time

    @property
    def fan_speed_target_time(self):
        """Timestamp of the last change to the part fan target speed."""
        return self._fan_speed_target_time

    @property
    def light_state(self):
        """The status of the printer lights. Toggling this will update all lights on the machine."""
        return self._light_state == "on"

    @light_state.setter
    def light_state(self, value: bool):
        value = bool(value)
        cmd = copy.deepcopy(CHAMBER_LIGHT_TOGGLE)

        if value:
            cmd["system"]["led_mode"] = "on"
        else:
            cmd["system"]["led_mode"] = "off"

        self.client.publish(
            f"device/{self.config.serial_number}/request", json.dumps(cmd)
        )
        logger.debug(
            f"light_state.setter - publishing CHAMBER_LIGHT_TOGGLE to [device/{self.config.serial_number}/request] - chamber_light"
        )

        cmd["system"]["led_node"] = "chamber_light2"
        self.client.publish(
            f"device/{self.config.serial_number}/request", json.dumps(cmd)
        )
        logger.debug(
            f"light_state.setter - publishing CHAMBER_LIGHT_TOGGLE to [device/{self.config.serial_number}/request] - chamber_light2"
        )

        cmd["system"]["led_node"] = "column_light"
        self.client.publish(
            f"device/{self.config.serial_number}/request", json.dumps(cmd)
        )
        logger.debug(
            f"light_state.setter - publishing CHAMBER_LIGHT_TOGGLE to [device/{self.config.serial_number}/request] - column_light"
        )

    @property
    def speed_level(self) -> SpeedLevel | int:
        """The active print speed mode. Returns a SpeedLevel enum member when the firmware
        value is recognised (1–4); returns the raw integer otherwise (e.g. 0 at startup
        before the first telemetry push)."""
        try:
            return SpeedLevel(self._speed_level)
        except ValueError:
            return self._speed_level

    @speed_level.setter
    def speed_level(self, value: "SpeedLevel | int | str"):
        """Set the active print speed mode.

        Accepts a SpeedLevel enum member, an integer code (1–4), or a case-insensitive
        name string ('quiet', 'standard', 'sport', 'ludicrous').
        """
        if isinstance(value, SpeedLevel):
            code = str(value.value)
        elif isinstance(value, int):
            code = str(value)
        else:
            code = str(SpeedLevel[str(value).upper()].value)
        cmd = SPEED_PROFILE_TEMPLATE
        cmd["print"]["param"] = code
        self.client.publish(
            f"device/{self.config.serial_number}/request", json.dumps(cmd)
        )

    @property
    def printer_state(self) -> BambuState:
        """The current status and sensor data for the printer."""
        return self._printer_state

    @property
    def active_job_info(self) -> ActiveJobInfo:
        """Details related to the current / last active job"""
        return self._active_job_info

    @property
    def internalException(self):
        """The last error captured during printer communication."""
        return self._internalException

    @property
    def cached_sd_card_contents(self):
        """A list of all files and folders found on the printer's SD card."""
        return self._sdcard_contents

    @property
    def cached_sd_card_3mf_files(self):
        """A list of only the 3mf files found on the SD card."""
        return self._sdcard_3mf_files

    @property
    @deprecated("This property is deprecated (v1.0.0). No replacement yet.")
    def skipped_objects(self):
        """A list of objects that have been excluded from the current print."""
        return self._skipped_objects

    @property
    @deprecated(
        "This property is deprecated (v1.0.0). Use `_printer_state.active_nozzle.diameter_mm` instead."
    )
    def nozzle_diameter(self) -> NozzleDiameter:
        """The diameter of the nozzle currently installed on the printer.

        !!! danger "Deprecated"
            This property is deprecated (v1.0.0). Use `_printer_state.active_nozzle.diameter_mm` instead.
        """
        try:
            return NozzleDiameter(float(self._nozzle_diameter))
        except (ValueError, TypeError, KeyError) as e:
            logger.warning(f"nozzle_diameter - exception: [{e}]")
            return NozzleDiameter.UNKNOWN

    @property
    @deprecated(
        "This property is deprecated (v1.0.0). Use `_printer_state.active_nozzle.material` instead."
    )
    def nozzle_type(self) -> NozzleType:
        """The type of nozzle currently installed on the printer.

        !!! danger "Deprecated"
            This property is deprecated (v1.0.0). Use `_printer_state.active_nozzle.material` instead.
        """
        if not self._nozzle_type:
            return NozzleType.UNKNOWN
        return parse_nozzle_type(str(self._nozzle_type))

    # endregion

    # region private methods

    def _elapsed_key(self) -> str | None:
        raw = (
            self._active_job_info.subtask_name or self._active_job_info.gcode_file or ""
        ).strip()
        return make_cache_key(raw)

    def _persist_job_start(self) -> None:
        key = self._elapsed_key()
        if key and self._active_job_info.wall_start_time >= 0:
            cache_write(
                self.config.bpm_cache_path / "elapsed",
                key,
                {"wall_start_time": self._active_job_info.wall_start_time},
            )

    def _load_job_start(self) -> float:
        key = self._elapsed_key()
        if not key:
            return -1.0
        data = cache_read(self.config.bpm_cache_path / "elapsed", key)
        if data and "wall_start_time" in data:
            return float(data["wall_start_time"])
        return -1.0

    def _notify_update(self):
        if self.on_update:
            self.on_update(self)

    def _start_watchdog(self):
        def watchdog_thread(printer):
            try:
                while printer.service_state != ServiceState.QUIT:
                    if printer.service_state == ServiceState.CONNECTED and (
                        printer._lastMessageTime is None
                        or printer._lastMessageTime + printer.config.watchdog_timeout
                        < time.monotonic()
                    ):
                        if printer._lastMessageTime:
                            logger.debug("watchdog_thread - watchdog timeout")
                        printer._lastMessageTime = time.monotonic()
                        printer._recent_update = False
                        printer.client.publish(
                            f"device/{printer.config.serial_number}/request",
                            json.dumps(ANNOUNCE_VERSION),
                        )
                        printer.client.publish(
                            f"device/{printer.config.serial_number}/request",
                            json.dumps(ANNOUNCE_PUSH),
                        )
                    time.sleep(0.1)
            except Exception as e:
                logger.exception("watchdog_thread - an internal exception occurred")
                printer._internalException = e
                if printer.client and printer.client.is_connected():
                    printer.client.disconnect()

        self._watchdog_thread = threading.Thread(
            target=watchdog_thread, name="bambuprinter-session-watchdog", args=(self,)
        )
        self._watchdog_thread.start()

    def _on_message(self, msg: str):
        if self.config.verbose:
            logger.debug(f"_on_message - bambu_msg: [{msg}]")

        message = json.loads(msg)

        if "system" in message:
            # system = message["system"]
            logger.info(
                f"_on_message - system message type received - bambu_msg: [{message}]"
            )

        elif "print" in message:
            if (
                "command" in message["print"]
                and not message["print"]["command"] == "push_status"
            ):
                logger.info(
                    f"_on_message - command message type received - bambu_msg: [{message}]"
                )

            status = message["print"]

            if (
                status.get("command", "") == "project_file"
                and str(status.get("result", "")).lower() == "success"
            ):
                self._active_job_info.project_file_command = message
                md5 = status.get("md5", None)
                subtask_name = status.get("subtask_name", "")
                plate_num = 1

                param = status.get("param", None)
                if param:
                    match = re.search(r"plate_(\d{1,2})", param)
                    if match:
                        plate_num = int(match.group(1))

                bed_type = status.get("bed_type", None)
                plate_type = (
                    PlateType[bed_type.upper()]
                    if bed_type and bed_type.upper() in PlateType.__members__
                    else PlateType.NONE
                )

                # media/usb0 and sdcard
                url = status.get("url", "")
                parts = (
                    url.replace("/media/usb0", "").replace("/sdcard", "").split("://", 1)
                )
                if len(parts) == 2:
                    try:
                        self._active_job_info.project_info = get_project_info(
                            parts[1], self, md5, plate_num
                        )
                    except Exception as e:
                        logger.warning(f"get_project_info failed for [{parts[1]}]: {e}")
                self._active_job_info.subtask_name = subtask_name
                self._active_job_info.plate_num = plate_num
                self._active_job_info.plate_type = plate_type

            # if ams filament settings have changed
            if "command" in status and status["command"] == "ams_filament_setting":

                def _delayed_refresh():
                    # let's sleep for a couple seconds and do a full refresh
                    time.sleep(2.5)
                    logger.debug(
                        f"filament change triggered publishing ANNOUNCE_VERSION to [device/{self.config.serial_number}/request]"
                    )
                    self.client.publish(
                        f"device/{self.config.serial_number}/request",
                        json.dumps(ANNOUNCE_VERSION),
                    )
                    logger.debug(
                        f"filament change triggered publishing ANNOUNCE_PUSH to [device/{self.config.serial_number}/request]"
                    )
                    self.client.publish(
                        f"device/{self.config.serial_number}/request",
                        json.dumps(ANNOUNCE_PUSH),
                    )

                threading.Thread(
                    target=_delayed_refresh, name="bambuprinter-ams-refresh"
                ).start()

            if "bed_target_temper" in status:
                bed_temp_target = int(status["bed_target_temper"])
                if bed_temp_target != self._printer_state.climate.bed_temp_target:
                    self._bed_temp_target_time = round(time.time())

            if "nozzle_target_temper" in status:
                tool_temp_target = int(status["nozzle_target_temper"])
                if tool_temp_target != self._printer_state.active_nozzle_temp_target:
                    self._tool_temp_target_time = round(time.time())

            if "lights_report" in status:
                self._light_state = (status["lights_report"])[0]["mode"]
            if "spd_lvl" in status:
                self._speed_level = status["spd_lvl"]
            if "stg_cur" in status:
                self._active_job_info.stage_id = status["stg_cur"]
                self._active_job_info.stage_name = parseStage(
                    self._active_job_info.stage_id
                )
            if "subtask_name" in status:
                self._active_job_info.subtask_name = status["subtask_name"]
            if "gcode_file" in status:
                self._active_job_info.gcode_file = status["gcode_file"]
            if "print_type" in status:
                self._active_job_info.print_type = status["print_type"]
            if "layer_num" in status:
                self._active_job_info.current_layer = int(status["layer_num"])
            if "total_layer_num" in status:
                self._active_job_info.total_layers = int(status["total_layer_num"])
            if "mc_percent" in status:
                self._active_job_info.print_percentage = int(status["mc_percent"])

            gcode_state = self._printer_state.gcode_state
            if "gcode_state" in status:
                gcode_state = status["gcode_state"]
                if gcode_state != self._printer_state.gcode_state:
                    if gcode_state in ("FAILED", "FINISH"):
                        self._active_job_info.wall_start_time = -1.0
                        key = self._elapsed_key()
                        if key:
                            cache_delete(
                                self.config.bpm_cache_path / "elapsed",
                                key,
                            )
                    elif gcode_state in ("PREPARE", "RUNNING"):
                        if self._active_job_info.wall_start_time == -1.0:
                            # Try to recover persisted start time first; fall back to now
                            persisted = self._load_job_start()
                            self._active_job_info.wall_start_time = (
                                persisted if persisted > 0 else time.time()
                            )
                            self._persist_job_start()
                        if (
                            (
                                not self._active_job_info.project_info
                                or not self._active_job_info.project_info.id
                            )
                            and not self._active_job_info.project_info_fetch_attempted
                            and self._active_job_info.gcode_file
                            and self._active_job_info.subtask_name
                        ):
                            self._active_job_info.project_info_fetch_attempted = True
                            match = re.search(
                                r"plate_(\d{1,2})", self._active_job_info.gcode_file
                            )
                            plate_num = (
                                int(match.group(1))
                                if match
                                else self._active_job_info.plate_num
                                if self._active_job_info.plate_num > 0
                                else 1
                            )
                            remote_files = self.get_sdcard_3mf_files()
                            file_entry = get_3mf_entry_by_name(
                                remote_files,
                                f"{self._active_job_info.subtask_name}.gcode.3mf",
                            )
                            if not file_entry:
                                file_entry = get_3mf_entry_by_name(
                                    remote_files,
                                    f"{self._active_job_info.subtask_name}.3mf",
                                )
                            if file_entry:
                                try:
                                    self._active_job_info.project_info = get_project_info(
                                        file_entry["id"], self, plate_num=plate_num
                                    )
                                except Exception as e:
                                    logger.warning(
                                        f"get_project_info fallback failed for [{file_entry['id']}]: {e}"
                                    )

            if "mc_remaining_time" in status:
                remaining_minutes = int(status["mc_remaining_time"])
                if remaining_minutes != self._active_job_info.remaining_minutes:
                    self._active_job_info.remaining_minutes = remaining_minutes
                    if gcode_state == "RUNNING":
                        self._active_job_info.elapsed_minutes = int(
                            max(0.0, time.time() - self._active_job_info.wall_start_time)
                            / 60.0
                        )

            if (
                "ams" in status
                and "ams" in status["ams"]
                and "ams_exist_bits" in status["ams"]
            ):
                if int(str(status["ams"]["ams_exist_bits"]), 0) & 0x1:
                    spools: list[BambuSpool] = []
                    self.config.startup_read_option = status["ams"].get(
                        "power_on_flag", False
                    )
                    self.config.tray_read_option = status["ams"].get("insert_flag", False)

                    for ams in status["ams"]["ams"]:
                        for tray in ams["tray"]:
                            try:
                                tray_color = hex_to_name("#" + tray["tray_color"][:6])
                            except Exception:
                                try:
                                    tray_color = "#" + tray["tray_color"]
                                except Exception:
                                    tray_color = ""
                            ams_id = int(ams.get("id", -1))
                            slot_id = int(tray.get("id", -1))
                            if slot_id != -1 and ams_id != -1:
                                if ams_id >= 128:
                                    tray_id = int(ams_id / 128 + 15)
                                else:
                                    tray_id = int(ams_id * 4 + slot_id)
                                spool = BambuSpool(
                                    tray_id,
                                    tray.get("tray_id_name", ""),
                                    tray.get("tray_type", ""),
                                    tray.get("tray_sub_brands", ""),
                                    tray_color,
                                    tray.get("tray_info_idx", ""),
                                    tray.get("k", 0.0),
                                    tray.get("bed_temp", 0),
                                    tray.get("nozzle_temp_min", 0),
                                    tray.get("nozzle_temp_max", 0),
                                    tray.get("drying_temp", 0),
                                    tray.get("drying_time", 0),
                                    tray.get("remain", -1),
                                    tray.get("state", -1),
                                    tray.get("total_len", 0),
                                    tray.get("tray_weight", 0),
                                    slot_id,
                                    ams_id,
                                )
                                spools.append(spool)

                    self._printer_state.spools = spools

            if "vt_tray" in status:
                spools = self._printer_state.spools
                tray = status.get("vt_tray", {})
                if (tray.get("id", -1)) != -1:
                    try:
                        tray_color = hex_to_name("#" + tray["tray_color"][:6])
                    except Exception:
                        try:
                            tray_color = "#" + tray["tray_color"]
                        except Exception:
                            tray_color = ""

                    spool = BambuSpool(
                        int(tray.get("id")),
                        tray.get("tray_id_name", ""),
                        tray.get("tray_type", ""),
                        tray.get("tray_sub_brands", ""),
                        tray_color,
                        tray.get("tray_info_idx", ""),
                        tray.get("k", 0.0),
                        tray.get("bed_temp", 0),
                        tray.get("nozzle_temp_min", 0),
                        tray.get("nozzle_temp_max", 0),
                        tray.get("drying_temp", 0),
                        tray.get("drying_time", 0),
                        -1,
                        tray.get("state", -1),
                        tray.get("total_len", 0),
                        tray.get("tray_weight", 0),
                        int(tray.get("id", -1)),
                        -1,
                    )
                    spools.append(spool)
                    self._printer_state.spools = spools

            if "vir_slot" in status:
                spools = self._printer_state.spools

                virt_spools = status.get("vir_slot", [])
                spool: BambuSpool

                for ext_spool_id in (254, 255):
                    tray_found = False
                    for tray in virt_spools:
                        if int(tray.get("id", -1)) == ext_spool_id:
                            try:
                                tray_color = hex_to_name("#" + tray["tray_color"][:6])
                            except Exception:
                                try:
                                    tray_color = "#" + tray["tray_color"]
                                except Exception:
                                    tray_color = ""
                            spool = BambuSpool(
                                int(tray.get("id", -1)),
                                tray.get("tray_id_name", ""),
                                tray.get("tray_type", ""),
                                tray.get("tray_sub_brands", ""),
                                tray_color,
                                tray.get("tray_info_idx", ""),
                                tray.get("k", 0.0),
                                tray.get("bed_temp", 0),
                                tray.get("nozzle_temp_min", 0),
                                tray.get("nozzle_temp_max", 0),
                                tray.get("drying_temp", 0),
                                tray.get("drying_time", 0),
                                -1,
                                tray.get("state", -1),
                                tray.get("total_len", 0),
                                tray.get("tray_weight", 0),
                                int(tray.get("id", -1)),
                                -1,
                            )
                            tray_found = True
                            break
                    if not tray_found:
                        spool = BambuSpool(ext_spool_id)
                    spools.append(spool)
                self._printer_state.spools = spools

            if "home_flag" in status:
                flag = int(status["home_flag"])
                self.config.auto_recovery = (flag >> 4) & 0x1 != 0
                self.config.auto_switch_filament = (flag >> 10) & 0x1 != 0
                self.config.calibrate_remain_flag = (flag >> 7) & 0x1 != 0
                self.config.capabilities.has_auto_recovery_support = True
                self.config.capabilities.has_auto_switch_filament_support = (
                    self.config.capabilities.has_ams
                )
                self.config.capabilities.has_sound_enable_support = (
                    flag >> 18
                ) & 0x1 != 0
                self.config.capabilities.has_filament_tangle_detect_support = (
                    flag >> 19
                ) & 0x1 != 0
                self.config.capabilities.has_nozzle_blob_detect_support = (
                    flag >> 25
                ) & 0x1 != 0
                self.config.capabilities.has_air_print_detect_support = (
                    flag >> 29
                ) & 0x1 != 0

                if self.config.capabilities.has_sound_enable_support:
                    self.config.sound_enable = (flag >> 17) & 0x1 != 0
                if self.config.capabilities.has_filament_tangle_detect_support:
                    self.config.filament_tangle_detect = (flag >> 20) & 0x1 != 0
                if self.config.capabilities.has_nozzle_blob_detect_support:
                    self.config.nozzle_blob_detect = (flag >> 24) & 0x1 != 0
                if self.config.capabilities.has_air_print_detect_support:
                    self.config.air_print_detect = (flag >> 28) & 0x1 != 0

            if "s_obj" in status:
                self._skipped_objects = status["s_obj"]

            if "nozzle_type" in status:
                self._nozzle_type = status["nozzle_type"]
            if "nozzle_diameter" in status:
                self._nozzle_diameter = status["nozzle_diameter"]

            if "xcam" in status and "buildplate_marker_detector" in status["xcam"]:
                self.config.capabilities.has_buildplate_marker_detector_support = True
                self.config.buildplate_marker_detector = status["xcam"][
                    "buildplate_marker_detector"
                ]

            if "xcam" in status:
                xcam = status["xcam"]
                has_fun_support = "fun" in status

                if "cfg" in xcam:
                    if not has_fun_support:
                        self.config.capabilities.has_spaghetti_detector_support = True
                        self.config.capabilities.has_purgechutepileup_detector_support = (
                            True
                        )
                        self.config.capabilities.has_nozzleclumping_detector_support = (
                            True
                        )
                        self.config.capabilities.has_airprinting_detector_support = True
                    xcam_cfg = int(xcam["cfg"])
                    self.config.spaghetti_detector = (xcam_cfg >> 7) & 0x1 != 0
                    self.config.purgechutepileup_detector = (xcam_cfg >> 10) & 0x1 != 0
                    self.config.nozzleclumping_detector = (xcam_cfg >> 13) & 0x1 != 0
                    self.config.airprinting_detector = (xcam_cfg >> 16) & 0x1 != 0

                    sensitivity_value = (xcam_cfg >> 8) & 0x3
                    sensitivity_map = {
                        0: "low",
                        1: "medium",
                        2: "high",
                    }
                    if sensitivity_value in sensitivity_map:
                        self.config.spaghetti_detector_sensitivity = sensitivity_map[
                            sensitivity_value
                        ]

                    sensitivity_value = (xcam_cfg >> 11) & 0x3
                    if sensitivity_value in sensitivity_map:
                        self.config.purgechutepileup_detector_sensitivity = (
                            sensitivity_map[sensitivity_value]
                        )

                    sensitivity_value = (xcam_cfg >> 14) & 0x3
                    if sensitivity_value in sensitivity_map:
                        self.config.nozzleclumping_detector_sensitivity = sensitivity_map[
                            sensitivity_value
                        ]

                    sensitivity_value = (xcam_cfg >> 17) & 0x3
                    if sensitivity_value in sensitivity_map:
                        self.config.airprinting_detector_sensitivity = sensitivity_map[
                            sensitivity_value
                        ]

                else:
                    if "spaghetti_detector" in xcam:
                        if not has_fun_support:
                            self.config.capabilities.has_spaghetti_detector_support = True
                        self.config.spaghetti_detector = xcam["spaghetti_detector"]

                        if xcam.get("print_halt"):
                            self.config.spaghetti_detector_sensitivity = "medium"

                    if "pileup_detector" in xcam:
                        if not has_fun_support:
                            self.config.capabilities.has_purgechutepileup_detector_support = True
                        self.config.purgechutepileup_detector = xcam["pileup_detector"]

                        if xcam.get("print_halt"):
                            self.config.purgechutepileup_detector_sensitivity = "medium"

                    if "clump_detector" in xcam:
                        if not has_fun_support:
                            self.config.capabilities.has_nozzleclumping_detector_support = True
                        self.config.nozzleclumping_detector = xcam["clump_detector"]

                        if xcam.get("print_halt"):
                            self.config.nozzleclumping_detector_sensitivity = "medium"

                    if "airprint_detector" in xcam:
                        if not has_fun_support:
                            self.config.capabilities.has_airprinting_detector_support = (
                                True
                            )
                        self.config.airprinting_detector = xcam["airprint_detector"]

                        if xcam.get("print_halt"):
                            self.config.airprinting_detector_sensitivity = "medium"

        elif "info" in message and "module" in message["info"]:
            self._recent_update = True
            info = message["info"]
            for module in info["module"]:
                if "ota" in module["name"]:
                    self.config.firmware_version = module["sw_ver"]
                if "ams" in module.get("product_name", "").lower():
                    self.config.ams_firmware_version = module["sw_ver"]
        elif (
            "xcam" in message
            and "result" in message["xcam"]
            and message["xcam"]["result"] == "SUCCESS"
        ):
            # logger.debug("xcam update message received", extra={"bambu_msg": message})
            pass

        else:
            logger.warning(
                f"\r_on_message - unknown message type received - bambu_msg: [{message}]"
            )

        self._printer_state = BambuState.fromJson(message, self)
        self._notify_update()

    def _get_sftp_files(
        self,
        ftps: IoTFTPSClient,
        directory: str,
        mask: str | None = None,
    ) -> dict:
        try:
            files = ftps.list_files_ex(directory)
        except Exception:
            logger.exception("_get_sftp_files - unexpected ftps exception")
            return {}

        dir: dict = {
            "id": directory + ("/" if directory != "/" else ""),
            "name": (
                directory[directory.rindex("/") + 1 :]
                if "/" in directory and directory != "/"
                else directory
            ),
        }

        items = []

        for entry in files if files else {}:
            if entry.is_dir:
                item = self._get_sftp_files(ftps, entry.path)
                if not item:
                    continue

                item["timestamp"] = entry.timestamp.timestamp()
                items.append(item)

            else:
                if mask and not entry.name.lower().endswith(mask):
                    continue

                items.append(
                    {
                        "id": entry.path,
                        "name": entry.name,
                        "size": entry.size,
                        "timestamp": entry.timestamp.timestamp(),
                    }
                )

        dir["children"] = items
        return dir


# endregion
