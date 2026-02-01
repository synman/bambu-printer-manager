import contextlib
import copy
import json
import logging
import math
import re
import ssl
import threading
import time
import traceback
from threading import Thread
from typing import Any

import paho.mqtt.client as mqtt
from typing_extensions import deprecated
from webcolors import hex_to_name, name_to_hex

from bpm.bambucommands import (
    AMS_CHANGE_FILAMENT,
    AMS_CONTROL,
    AMS_FILAMENT_DRYING,
    AMS_FILAMENT_SETTING,
    AMS_USER_SETTING,
    ANNOUNCE_PUSH,
    ANNOUNCE_VERSION,
    CHAMBER_LIGHT_TOGGLE,
    EXTRUSION_CALI_SEL,
    EXTRUSION_CALI_SET,
    HMS_STATUS,
    PAUSE_PRINT,
    PRINT_3MF_FILE,
    PRINT_OPTION_COMMAND,
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
from bpm.bambuconfig import BambuConfig, LoggerName
from bpm.bambuspool import BambuSpool
from bpm.bambustate import BambuState
from bpm.bambutools import (
    ActiveTool,
    AMSControlCommand,
    AMSUserSetting,
    NozzleDiameter,
    NozzleType,
    PlateType,
    PrintOption,
    ServiceState,
    parseStage,
    scaleFanSpeed,
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

        self._bed_temp = 0.0
        self._bed_temp_target = 0
        self._bed_temp_target_time = 0

        self._tool_temp = 0.0
        self._tool_temp_target = 0
        self._tool_temp_target_time = 0

        self._chamber_temp = 0.0
        self._chamber_temp_target = 0
        self._chamber_temp_target_time = 0

        self._fan_gear = 0
        self._heatbreak_fan_speed = 0
        self._fan_speed = 0
        self._fan_speed_target = 0
        self._fan_speed_target_time = 0

        self._light_state = ""
        self._wifi_signal = ""
        self._speed_level = 0

        self._gcode_state = ""
        self._gcode_file = ""
        self._3mf_file = ""
        self._3mf_file_md5 = ""
        self._plate_num = 0
        self._plate_type = PlateType.NONE
        self._subtask_name = ""
        self._print_type = ""
        self._percent_complete = 0
        self._time_remaining = 0
        self._start_time = 0
        self._elapsed_time = 0
        self._layer_count = 0
        self._current_layer = 0

        self._current_stage = 0
        self._current_stage_text = ""

        self._spools = []
        self._printer_state = BambuState()
        self._target_spool = 255
        self._active_spool = 255
        self._spool_state = ""
        self._ams_status = None
        self._ams_exists = False
        self._ams_rfid_status = None

        self._sdcard_contents = None
        self._sdcard_3mf_files = None

        self._hms_data = None
        self._hms_message = ""
        self._last_hms_message = ""

        self._print_type = ""
        self._skipped_objects = []

        self._nozzle_type = ""
        self._nozzle_diameter = 0.0

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
                logger.debug(f"subscribed to [device/{self.config.serial_number}/report]")

        def on_disconnect(client, userdata, flags, reason_code, properties):
            logger.debug("on_disconnect - session on_disconnect")
            if self._internalException:
                logger.exception("on_disconnect - an internal exception occurred")
                self.service_state = ServiceState.QUIT
                raise self._internalException
            if self.service_state != ServiceState.PAUSED:
                self.service_state = ServiceState.DISCONNECTED

        def on_message(client, userdata, msg):
            # logger.debug(f"on_message - topic: [{msg.topic}]")
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

        try:
            self.client.connect(self.config.hostname, self.config.mqtt_port, 60)
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
        Opens a connection to the printer's FTP server to support file management.

        Acts as a context manager, so can be used with the with statement. In that case,
        the connection will be closed automatically, otherwise the calling code has to make
        sure to close it again.
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

    def unload_filament(self, ams_id: int = 0):
        """
        Requests the printer to unload whatever filament / spool may be currently loaded.
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
        Submits a request to execute the `name` 3mf file on the printer's SDCard.

        Parameters
        ----------
        * name : str                         - path, filename, and extension to execute
        * plate : int                        - the plate # from your slicer to use (usually 1)
        * bed : PlateType                    - the bambutools.PlateType to use
        * use_ams : bool                     - Use the AMS for this print
        * ams_mapping : Optional[str]        - an `AMS Mapping` that specifies which AMS spools to use (external spool is used if blank)
        * bedlevel : Optional[bool] = True   - boolean value indicates whether or not the printer should auto-level the bed
        * flow : Optional[bool] = True       - boolean value indicates if the printer should perform an extrusion flow calibration
        * timelapse : Optional[bool] = False - boolean value indicates if printer should take timelapse photos during the job

        Example
        -------
        * `print_3mf_file("/jobs/my_project.3mf", 1, PlateType.HOT_PLATE, False, "")` - Print the my_project.3mf file in the SDCard /jobs directory using the external spool with bed leveling and extrusion flow calibration enabled and timelapse disabled
        * `print_3mf_file("/jobs/my_project.gcode.3mf", 1, PlateType.HOT_PLATE, True, "[-1,-1,2,-1]")` - Same as above but use AMS spool #3

        AMS Mapping
        -----------
        * `[0,-1,-1,-1]` - use AMS spool #1 only
        * `[-1,1,-1,-1]` - use AMS spool #2 only
        * `[0,-1,-1,3]`  - use AMS spools #1 and #4
        * `[0,1,2,3]`    - use all 4 AMS spools
        """
        self._3mf_file = f"{name}"
        self._plate_num = int(plate)
        self._plate_type = bed

        file = copy.deepcopy(PRINT_3MF_FILE)

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

        file["print"]["file"] = self._3mf_file
        file["print"]["url"] = f"file:///sdcard{self._3mf_file}"
        file["print"]["subtask_name"] = subtask
        file["print"]["bed_type"] = bed.name.lower()
        file["print"]["param"] = file["print"]["param"].replace("#", str(self._plate_num))
        file["print"]["use_ams"] = use_ams
        if ams_mapping and len(ams_mapping) > 0:
            file["print"]["ams_mapping"] = json.loads(ams_mapping)
        file["print"]["bed_leveling"] = bedlevel
        file["print"]["flow_cali"] = flow
        file["print"]["timelapse"] = timelapse
        self.client.publish(
            f"device/{self.config.serial_number}/request", json.dumps(file)
        )
        logger.debug(
            f"print_3mf_file - published PRINT_3MF_FILE to [device/{self.config.serial_number}/request] print_command: [{file}]"
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

    def get_sdcard_3mf_files(self):
        """
        Returns a `dict` (json document) of all `.3mf` files on the printer's SD card.

        Usage
        -----
        The return value of this method is very useful for binding to things like a clientside `TreeView`
        """
        logger.debug("get_sdcard_3mf_files - returning sdcard_3mf_files")
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

    def delete_sdcard_file(self, file: str):
        """
        Delete the specified file on the printer's SDCard and returns an updated dict of all files on the printer

        Parameters
        ----------
        * file : str - the full path filename to be deleted
        """
        logger.debug(f"deleting remote file: [{file}]")

        with self.ftp_connection() as ftps:
            ftps.delete_file(file)

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
        return self.get_sdcard_contents()

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

    def set_print_option(self, option: PrintOption, enabled: bool):
        """
        Enable or disable one of the `PrintOption` options
        """
        cmd = PRINT_OPTION_COMMAND
        cmd["print"][option.name.lower()] = "true" if enabled else "false"

        if option == PrintOption.AUTO_RECOVERY:
            cmd["print"]["option"] = "1" if enabled else "0"
            self.config.auto_recovery = enabled
        elif option == PrintOption.AUTO_SWITCH_FILAMENT:
            self.config.auto_switch_filament = enabled
        elif option == PrintOption.FILAMENT_TANGLE_DETECT:
            self.config.filament_tangle_detect = enabled
        elif option == PrintOption.SOUND_ENABLE:
            self.config.sound_enable = enabled

        self.client.publish(
            f"device/{self.config.serial_number}/request", json.dumps(cmd)
        )
        logger.debug(
            f"set_print_option - published PRINT_OPTION_COMMAND to [device/{self.config.serial_number}/request] bambu_msg: [{cmd}]"
        )

    def set_ams_user_setting(
        self, setting: AMSUserSetting, enabled: bool, ams_id: int | None = 0
    ):
        """
        Enable or disable one of the `AMSUserSetting` options
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

    @deprecated(
        "This method is deprecated. The closest alternative is `select_extrusion_calibration_profile`."
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
        Sets the linear advance k factor for a specific spool / tray

        broken in recent firmware -- will require implementing
        k factor list management
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

    def set_spool_details(
        self,
        tray_id: int,
        tray_info_idx: str,
        tray_id_name: str | None = "",
        tray_type: str | None = "",
        tray_color: str | None = "",
        nozzle_temp_min: int | None = -1,
        nozzle_temp_max: int | None = -1,
    ):
        """
        Sets spool / tray details such as filament type, color, and nozzle min/max temperature.
        For the external tray (254), send `no_filament` as the `tray_info_idx` value to empty the tray.
        """
        cmd = copy.deepcopy(AMS_FILAMENT_SETTING)

        ams_id = math.floor(tray_id / 4)
        if tray_id == 254 or tray_id == 255:
            ams_id = tray_id
            tray_id = 0

        cmd["print"]["ams_id"] = ams_id
        cmd["print"]["tray_id"] = tray_id
        cmd["print"]["slot_id"] = tray_id % 4

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

    def send_ams_control_command(self, ams_control_cmd: AMSControlCommand):
        """
        Send an AMS Control Command - will pause, resume, or reset the AMS.
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

    def skip_objects(self, objects):
        """
        skip a list of objects extracted from the 3mf's plate_x.json file

        Parameters
        ----------
        objects : list
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

    def set_buildplate_marker_detector(self, enabled: bool):
        """
        Enables or disables the buildplate_marker_detector
        """
        cmd = copy.deepcopy(XCAM_CONTROL_SET)
        cmd["xcam"]["control"] = enabled
        cmd["xcam"]["enable"] = enabled

        self.client.publish(
            f"device/{self.config.serial_number}/request", json.dumps(cmd)
        )
        logger.debug(
            f"set_buildplate_marker_detector - published XCAM_CONTROL_SET to [device/{self.config.serial_number}/request] bambu_msg: [{cmd}]"
        )

    def set_nozzle_details(
        self, nozzle_diameter: NozzleDiameter, nozzle_type: NozzleType
    ):
        """
        Sets the nozzle details.
        """
        cmd = copy.deepcopy(SET_ACCESSORIES)
        cmd["system"]["nozzle_diameter"] = nozzle_diameter.value
        cmd["system"]["nozzle_type"] = nozzle_type.name.lower()

        self.client.publish(
            f"device/{self.config.serial_number}/request", json.dumps(cmd)
        )
        logger.debug(
            f"set_nozzle_details - published SET_ACCESSORIES to [device/{self.config.serial_number}/request] bambu_msg: [{cmd}]"
        )

    def send_anything(self, anything: str):
        """
        puts an arbritary string on the request topic
        """
        self.client.publish(
            f"device/{self.config.serial_number}/request",
            json.dumps(json.loads(anything)),
        )
        logger.debug(
            f"send_anything - published message to [device/{self.config.serial_number}/request] message: [{anything}]"
        )

    def turn_on_ams_dryer(
        self,
        target_temp: int,
        duration: int,
        target_humidity: int = 0,
        cooling_temp: int = 45,
        rotate_tray: bool = False,
        ams_id: int = 0,
    ):
        """
        Sends a command to the printer to turn on the AMS dryer with specified parameters.

        Parameters
        ----------
        * target_temp : int - The target drying temperature.
        * duration : int - The drying duration in minutes.
        * target_humidity : int - The target humidity level.
        * cooling_temp : int - The cooling temperature after drying (default is 45).
        * rotate_tray : bool - Whether to rotate the tray during drying (default is False).
        * ams_id : int - The AMS ID to control (default is 0).
        """
        cmd = copy.deepcopy(AMS_FILAMENT_DRYING)
        cmd["print"]["ams_id"] = ams_id
        cmd["print"]["mode"] = 1  # Turn on drying mode
        cmd["print"]["temp"] = target_temp
        cmd["print"]["duration"] = duration
        cmd["print"]["humidity"] = target_humidity
        cmd["print"]["cooling_temp"] = cooling_temp
        cmd["print"]["rotate_tray"] = rotate_tray
        self.client.publish(
            f"device/{self.config.serial_number}/request", json.dumps(cmd)
        )

        ams = self.printer_state.ams_units[ams_id]
        ams.temp_target = target_temp

        logger.debug(
            f"turn_on_ams_dryer - published AMS_FILAMENT_DRYING to [device/{self.config.serial_number}/request] command: [{cmd}]"
        )

    def turn_off_ams_dryer(self, ams_id: int = 0):
        """
        Sends a command to the printer to turn off the AMS dryer.
        """
        cmd = copy.deepcopy(AMS_FILAMENT_DRYING)
        cmd["print"]["ams_id"] = ams_id
        cmd["print"]["mode"] = 0  # Turn off drying mode
        self.client.publish(
            f"device/{self.config.serial_number}/request", json.dumps(cmd)
        )

        ams = self.printer_state.ams_units[ams_id]
        ams.temp_target = 0

        logger.debug(
            f"turn_off_ams_dryer - published AMS_FILAMENT_DRYING to [device/{self.config.serial_number}/request] command: [{cmd}]"
        )

    def set_active_tool(self, id: int):
        """
        sets the current active tool / extruder for machines (H2 series)
        that have multiple extruders
        """
        cmd = copy.deepcopy(SET_ACTIVE_TOOL)
        cmd["print"]["extruder_index"] = id
        self.client.publish(
            f"device/{self.config.serial_number}/request", json.dumps(cmd)
        )
        logger.debug(
            f"set_active_tool - published SET_ACTIVE_TOOL to [device/{self.config.serial_number}/request] command: [{cmd}]"
        )

    def get_current_bind_list(self, state: "BambuState") -> list[dict[str, Any]]:
        """
        Generates the manual_ams_bind list based on current AMS toolhead assignments.

        This method implements the H2D cross-over hardware targeting:
        - RIGHT_EXTRUDER (0) -> Hardware Index 1
        - LEFT_EXTRUDER (1)  -> Hardware Index 0

        Includes sentinel placeholder logic for single-AMS configurations to satisfy
        dual-extruder firmware array requirements.
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

        if tray_id in (254, 255):
            ams_id = tray_id
            tray_id = 0

        cmd["print"]["ams_id"] = ams_id
        cmd["print"]["tray_id"] = tray_id
        cmd["print"]["slot_id"] = tray_id % 4
        cmd["print"]["cali_idx"] = cali_idx

        self.client.publish(
            f"device/{self.config.serial_number}/request", json.dumps(cmd)
        )
        logger.debug(
            f"select_extrusion_calibration_profile - published EXTRUSION_CALI_SEL to [device/{self.config.serial_number}/request] cmd: [{cmd}]"
        )

    def toJson(self):
        """
        Returns a `dict` (json document) representing this object's private class
        level attributes that are serializable (most are).
        """
        response = json.dumps(self, default=self.jsonSerializer, indent=4, sort_keys=True)
        # logger.debug(f"toJson - json: [{response}]")

        return json.loads(response)

    def jsonSerializer(self, obj):
        """
        Helper method used by `toJson()` to serialize this object.
        """
        try:
            if isinstance(obj, mqtt.Client) or isinstance(obj, Thread):
                return "these are not the droids you are looking for"
            if (
                str(obj.__class__).replace("<class '", "").replace("'>", "")
                == "mappingproxy"
            ):
                return "this space intentionally left blank"
            return obj.__dict__
        except Exception:
            logger.warning(
                f"jsonSerializer - unable to serialize object - 'obj': [{obj}]"
            )
            return "not available"

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
                            logger.warning("BambuPrinter watchdog timeout")
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
        # logger.debug(f"_on_message - bambu_msg: [{msg}]")

        message = json.loads(msg)
        self._printer_state = BambuState.fromJson(
            message, self._printer_state, self._config
        )

        if "system" in message:
            # system = message["system"]
            logger.warning(
                f"\r_on_message - system message type received - bambu_msg: [{message}]"
            )

        elif "print" in message:
            if (
                "command" in message["print"]
                and not message["print"]["command"] == "push_status"
            ):
                logger.warning(
                    f"\r_on_message - command message type received - bambu_msg: [{message}]"
                )

            status = message["print"]

            if (
                status.get("command", "") == "project_file"
                and status.get("result", "") == "success"
            ):
                self._start_time = 0

                url = status.get("url", "")
                parts = url.split("://", 1)
                if len(parts) == 2:
                    self._3mf_file = parts[1]

                self._3mf_file_md5 = status.get("md5", "")
                self._subtask_name = status.get("subtask_name", "")

                param = status.get("param", None)
                if param:
                    match = re.search(r"plate_(\d{1,2})", param)
                    if match:
                        self._plate_num = int(match.group(1))

                bed_type = status.get("bed_type", None)
                self._plate_type = (
                    PlateType[bed_type.upper()]
                    if bed_type and bed_type.upper() in PlateType.__members__
                    else PlateType.NONE
                )

            # let's sleep for a couple seconds and do a full refresh
            # if ams filament settings have changed
            if "command" in status and status["command"] == "ams_filament_setting":
                time.sleep(2)
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

            if "bed_temper" in status:
                self._bed_temp = float(status["bed_temper"])
            if "bed_target_temper" in status:
                bed_temp_target = int(status["bed_target_temper"])
                if bed_temp_target != self._bed_temp_target:
                    self._bed_temp_target = bed_temp_target
                    self._bed_temp_target_time = round(time.time())

            if "nozzle_temper" in status:
                self._tool_temp = float(status["nozzle_temper"])
            if "nozzle_target_temper" in status:
                tool_temp_target = int(status["nozzle_target_temper"])
                if tool_temp_target != self._tool_temp_target:
                    self._tool_temp_target = tool_temp_target
                    self._tool_temp_target_time = round(time.time())

            if not self._config.external_chamber and "chamber_temper" in status:
                self._chamber_temp = float(status["chamber_temper"])

            if "fan_gear" in status:
                self._fan_gear = int(status["fan_gear"])
            if "heatbreak_fan_speed" in status:
                self._heatbreak_fan_speed = int(status["heatbreak_fan_speed"])
            if "cooling_fan_speed" in status:
                self._fan_speed = scaleFanSpeed(int(status["cooling_fan_speed"]))

            if "wifi_signal" in status:
                self._wifi_signal = status["wifi_signal"]
            if "lights_report" in status:
                self._light_state = (status["lights_report"])[0]["mode"]
            if "spd_lvl" in status:
                self._speed_level = status["spd_lvl"]

            if "gcode_state" in status:
                self._gcode_state = status["gcode_state"]
                if self._gcode_state in ("FINISH", "FAILED") and self._3mf_file:
                    self._3mf_file = ""
                    self._3mf_file_md5 = ""
                    self._plate_num = None
                    self._plate_type = PlateType.NONE
                    self._subtask_name = ""

            if "subtask_name" in status:
                self._subtask_name = status["subtask_name"]
            if "gcode_file" in status:
                self._gcode_file = status["gcode_file"]
            if "print_type" in status:
                self._print_type = status["print_type"]
            if "mc_percent" in status:
                self._percent_complete = status["mc_percent"]
            if "mc_remaining_time" in status:
                self._time_remaining = int(status["mc_remaining_time"])
            if "total_layer_num" in status:
                self._layer_count = status["total_layer_num"]
            if "layer_num" in status:
                self._current_layer = status["layer_num"]

            if "stg_cur" in status:
                self._current_stage = int(status["stg_cur"])
                self._current_stage_text = parseStage(self._current_stage)

            if "ams_status" in status:
                self._ams_status = status["ams_status"]
            if "ams_rfid_status" in status:
                self._ams_rfid_status = status["ams_rfid_status"]

            if (
                "ams" in status
                and "ams" in status["ams"]
                and "ams_exist_bits" in status["ams"]
            ):
                self._ams_exists = int(status["ams"]["ams_exist_bits"]) == 1
                if self._ams_exists:
                    spools = []

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

                            if tray.get("id"):
                                spool = BambuSpool(
                                    int(tray["id"]) + int(ams["id"]) * 4,
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
                                )
                                spools.append(spool)

                    self._spools = tuple(spools)

            if "vt_tray" in status:
                tray = status.get("vt_tray", {})
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
                )
                if not self._ams_exists:
                    spools = (spool,)
                else:
                    spools = list(self.spools)
                    spools.append(spool)
                self._spools = tuple(spools)

            if "vir_slot" in status:
                spools = list(self.spools)

                virt_spools = status.get("vir_slot", [])
                spool = None

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
                            )
                            tray_found = True
                            break
                    if not tray_found:
                        spool = BambuSpool
                        spool.id = ext_spool_id
                    spools.append(spool)
                self._spools = tuple(spools)

            tray_tar = None
            tray_now = None
            tray_pre = None

            if "ams" in status and status["ams"]:
                if "tray_tar" in status["ams"]:
                    tray_tar = int(status["ams"]["tray_tar"])
                    self._target_spool = tray_tar

                if "tray_now" in status["ams"]:
                    tray_now = int(status["ams"]["tray_now"])
                    self._active_spool = tray_now

                if "tray_pre" in status["ams"]:
                    tray_pre = int(status["ams"]["tray_pre"])

                # logger.warning(f"\rtray tar: {tray_pre} {tray_tar} {tray_now}")

            if tray_tar is not None or tray_now is not None or tray_pre is not None:
                if self._target_spool == 255 and self._active_spool == 255:
                    self._spool_state = "Unloaded"
                elif self._target_spool == 255 and self._active_spool != 255:
                    self._spool_state = "Unloading"
                elif (
                    self._active_spool != 255
                    and self._target_spool != 255
                    and self._target_spool != self._active_spool
                ):
                    self._spool_state = "Unloading"
                elif self._target_spool != 255 and self._active_spool == 255:
                    self._spool_state = "Loading"
                else:
                    self._spool_state = "Loaded"

            if "print_error" in status:
                err = status["print_error"]
                if err == 0 and self._hms_data or self._hms_message:
                    logger.debug("_on_message - clearing hms data and message")
                    self._hms_data = []
                    self._last_hms_message = self._hms_message
                    self._hms_message = ""
                else:
                    if err != 0 and self._last_hms_message:
                        logger.debug("_on_message - restoring last hms message")
                        self._hms_message = self._last_hms_message

            if "hms" in status and status["hms"]:
                logger.debug(f"_on_message - parsing hms data: [{status['hms']}]")

                self._hms_data = status.get("hms", [])
                self._hms_message = ""
                wiki_code = ""

                for hms in self._hms_data:
                    attr_raw = hms.get("attr", 0)
                    code_raw = hms.get("code", 0)

                    attr_masked = attr_raw & 0xFF00FFFF

                    h_attr = f"{attr_masked:08X}"
                    h_code = f"{code_raw:08X}"

                    wiki_code = f"{h_attr[:4]}_{h_attr[4:]}_{h_code[:4]}_{h_code[4:]}"
                    wiki_url = f"https://wiki.bambulab.com/en/h2/troubleshooting/hmscode/{wiki_code}"
                    logger.debug(
                        f"_on_message - hms ecode: [{h_attr}{h_code}] wiki: [{wiki_code}]"
                    )

                    for entry in HMS_STATUS["data"]["device_hms"]["en"]:
                        if (
                            entry["ecode"]
                            == f"{h_attr[:4]}{h_attr[4:]}{h_code[:4]}{h_code[4:]}"
                        ):
                            self._hms_message = (
                                f"{self._hms_message}{entry['intro']} ({wiki_url}) "
                            )
                            logger.debug(
                                f"_on_message - found hms message: [{entry['intro']}]"
                            )
                            break
                if self._hms_message == "":
                    self._hms_message = (
                        f"HMS Error [{wiki_code.replace('_', '-')}] - message NOT found"
                    )

                self._hms_message = self._hms_message.rstrip()

            if "home_flag" in status:
                flag = int(status["home_flag"])
                self.config.sound_enable = (flag >> 17) & 0x1 != 0
                self.config.auto_recovery = (flag >> 4) & 0x1 != 0
                self.config.auto_switch_filament = (flag >> 10) & 0x1 != 0
                self.config.filament_tangle_detect = (flag >> 20) & 0x1 != 0
                self.config.calibrate_remain_flag = (flag >> 7) & 0x1 != 0

            if "print_type" in status:
                self._print_type = status["print_type"]

            if "s_obj" in status:
                self._skipped_objects = status["s_obj"]

            if "nozzle_type" in status:
                self._nozzle_type = status["nozzle_type"]
            if "nozzle_diameter" in status:
                self._nozzle_diameter = status["nozzle_diameter"]

            if "xcam" in status and "buildplate_marker_detector" in status["xcam"]:
                self.config.buildplate_marker_detector = status["xcam"][
                    "buildplate_marker_detector"
                ]

        elif "info" in message and "module" in message["info"]:
            self._recent_update = True
            info = message["info"]
            for module in info["module"]:
                if "ota" in module["name"]:
                    self.config.serial_number = module["sn"]
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

        if self._gcode_state in ("PREPARE", "RUNNING", "PAUSE"):
            if self._start_time == 0:
                self._start_time = int(round(time.time() / 60, 0))
            self._elapsed_time = int(round(time.time() / 60, 0)) - self._start_time

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

    @property
    def config(self) -> BambuConfig:
        return self._config

    @config.setter
    def config(self, value: BambuConfig):
        self._config = value

    @property
    @deprecated("This property is deprecated (v1.0.0). Use `service_state`.")
    def state(self):
        return self._service_state.value

    @property
    def service_state(self):
        return self._service_state

    @service_state.setter
    def service_state(self, value: ServiceState):
        self._service_state = value
        self._notify_update()  # make sure we notify about EVERY state change!

    @property
    def client(self) -> mqtt.Client:
        if self._client:
            return self._client
        else:
            return mqtt.Client()

    @client.setter
    def client(self, value: mqtt.Client):
        self._client = value

    @property
    def on_update(self):
        """
        sets or returns the callback function that is called when the printer state is updated

        Parameters
        ----------
        * value : method - (setter) The method to call.
        """
        return self._on_update

    @on_update.setter
    def on_update(self, value):
        self._on_update = value

    @property
    def recent_update(self):
        return self._recent_update

    @property
    @deprecated("This property is deprecated (v1.0.0). Use `BambuState.bed_temp`.")
    def bed_temp(self):
        """
        returns the current bed temperature
        !!! danger "Deprecated"
        This property is deprecated (v1.0.0). Use `BambuState.bed_temp` instead.
        """
        return self._printer_state.climate.bed_temp

    @property
    @deprecated("This property is deprecated (v1.0.0). Use `BambuState.bed_temp_target`.")
    def bed_temp_target(self):
        """
        returns or sets the bed temperature target
        !!! danger "Deprecated"
        This property is deprecated (v1.0.0). Use `BambuState.bed_temp_target` and `set_bed_temp_target`.
        """
        return self._printer_state.climate.bed_temp_target

    @bed_temp_target.setter
    @deprecated("This property is deprecated (v1.0.0). Use `set_bed_temp_target`.")
    def bed_temp_target(self, value: int):
        self.set_bed_temp_target(value)

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

    @property
    @deprecated("This property is deprecated (v1.0.0). Use `BambuState.nozzle_temp`.")
    def tool_temp(self):
        """
        returns or sets the tool temperature
        !!! danger "Deprecated"
        This property is deprecated (v1.0.0). Use `BambuState.nozzle_temp`.
        """
        return self._printer_state.active_nozzle_temp

    @property
    @deprecated(
        "This property is deprecated (v1.0.0). Use `BambuState.nozzle_temp_target`."
    )
    def tool_temp_target(self):
        """
        returns or sets the nozzle temperature target
        !!! danger "Deprecated"
        This property is deprecated (v1.0.0). Use `BambuState.nozzle_temp`.
        """
        return self._printer_state.active_nozzle_temp_target

    @tool_temp_target.setter
    @deprecated("This property is deprecated (v1.0.0). Use `set_nozzle_temp_target`.")
    def tool_temp_target(self, value: int):
        self.set_nozzle_temp_target(value)

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

    @property
    @deprecated("This property is deprecated (v1.0.0). Use `BambuState.chamber_temp`.")
    def chamber_temp(self):
        """
        returns or sets the nozzle temperature target
        !!! danger "Deprecated"
        This property is deprecated (v1.0.0). Use `BambuState.chamber_temp` and `set_chamber_temp`.
        """
        return self._printer_state.climate.chamber_temp

    @chamber_temp.setter
    @deprecated("This property is deprecated (v1.0.0). Use `set_chamber_temp`.")
    def chamber_temp(self, value: float):
        self.set_chamber_temp(value)

    def set_chamber_temp(self, value: float):
        """
        for printers that do not have managed chambers, this enables you to inject
        a chamber temperature value from an external source

        Parameters
        ----------
        * value : float - The chamber temperature.
        """
        self._printer_state.climate.chamber_temp = value

    @property
    @deprecated(
        "This property is deprecated (v1.0.0). Use `BambuState.chamber_temp_target`."
    )
    def chamber_temp_target(self):
        """
        returns or sets the chamber temperature target
        !!! danger "Deprecated"
        This property is deprecated (v1.0.0). Use `BambuState.chamber_temp_target` and `set_chamber_temp_target`.
        """
        return self._printer_state.climate.chamber_temp_target

    @chamber_temp_target.setter
    @deprecated("This property is deprecated (v1.0.0). Use `set_chamber_temp_target`.")
    def chamber_temp_target(self, value: int):
        self.set_chamber_temp_target(value)

    def set_chamber_temp_target(self, value: int, temper_check: bool = True):
        """
        set chamber temperature target if printer supports it, otherwise just
        store the value

        Parameters
        ----------
        * value : float - The target chamber temperature.
        * temper_check : OPTIONAL bool - perform a temperature check?
        """
        cmd = copy.deepcopy(SET_CHAMBER_AC_MODE)
        if self.printer_state.capabilities.has_chamber_temp:
            if value < 40:
                cmd["print"]["modeId"] = 0
                value = 0
            else:
                cmd["print"]["modeId"] = 1
            self.client.publish(
                f"device/{self.config.serial_number}/request", json.dumps(cmd)
            )
            logger.debug(
                f"set_chamber_temp_target - published SET_CHAMBER_AC_MODE to [device/{self.config.serial_number}/request] command: [{cmd}]"
            )

            cmd = copy.deepcopy(SET_CHAMBER_TEMP_TARGET)
            cmd["print"]["ctt_val"] = value
            cmd["print"]["temper_check"] = temper_check

            self.client.publish(
                f"device/{self.config.serial_number}/request", json.dumps(cmd)
            )
            logger.debug(
                f"set_chamber_temp_target - published SET_CHAMBER_TEMP_TARGET to [device/{self.config.serial_number}/request] command: [{cmd}]"
            )
        else:
            self._printer_state.climate.chamber_temp_target = value
        self._chamber_temp_target_time = round(time.time())

    @property
    @deprecated(
        "This property is deprecated (v1.0.0). Use `BambuState.part_cooling_fan_speed_percent`."
    )
    def fan_speed(self):
        """
        returns the part fan speed in percent
        !!! danger "Deprecated"
        This property is deprecated (v1.0.0). Use `BambuState.part_cooling_fan_speed_percent`.
        """
        return self._printer_state.climate.part_cooling_fan_speed_percent

    @property
    @deprecated(
        "This property is deprecated (v1.0.0). Use `BambuState.part_cooling_fan_speed_target_percent`."
    )
    def fan_speed_target(self):
        """
        returns or sets the part cooling fan target speed in percent
        !!! danger "Deprecated"
        This property is deprecated (v1.0.0). Use `BambuState.part_cooling_fan_speed_target_percent` and `set_part_cooling_fan_speed_target_percent`.
        """
        return self._printer_state.climate.part_cooling_fan_speed_target_percent

    @fan_speed_target.setter
    @deprecated(
        "This property is deprecated (v1.0.0). Use `set_part_cooling_fan_speed_target_percent`."
    )
    def fan_speed_target(self, value: int):
        self.set_part_cooling_fan_speed_target_percent(value)

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

    @property
    def bed_temp_target_time(self):
        return self._bed_temp_target_time

    @property
    def tool_temp_target_time(self):
        return self._tool_temp_target_time

    @property
    def chamber_temp_target_time(self):
        return self._chamber_temp_target_time

    @property
    def fan_speed_target_time(self):
        return self._fan_speed_target_time

    @property
    def fan_gear(self):
        return self._fan_gear

    @property
    @deprecated(
        "This property is deprecated (v1.0.0). Use `BambuState.heatbreak_fan_speed_percent`."
    )
    def heatbreak_fan_speed(self):
        """
        returns the heatbreak fan's current speed in percent
        !!! danger "Deprecated"
        This property is deprecated (v1.0.0). Use `BambuState.heatbreak_fan_speed_percent`.
        """
        return self._printer_state.climate.heatbreak_fan_speed_percent

    @property
    def wifi_signal(self):
        return self._wifi_signal

    @property
    def light_state(self):
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
        # cmd["system"]["led_node"] = "chamber_light2"
        # self.client.publish(
        #     f"device/{self.config.serial_number}/request", json.dumps(cmd)
        # )

    @property
    def speed_level(self):
        return self._speed_level

    @speed_level.setter
    def speed_level(self, value: str):
        value = str(value)
        cmd = SPEED_PROFILE_TEMPLATE
        cmd["print"]["param"] = value
        self.client.publish(
            f"device/{self.config.serial_number}/request", json.dumps(cmd)
        )

    @property
    @deprecated("This property is deprecated (v1.0.0). Use `BambuState.gcode_state`.")
    def gcode_state(self):
        return self._printer_state.gcode_state

    @property
    def subtask_name(self):
        return self._subtask_name

    @property
    def current_3mf_file(self):
        return self._3mf_file

    @property
    def current_3mf_file_md5(self):
        return self._3mf_file_md5

    @property
    def current_plate_num(self):
        return self._plate_num

    @property
    def current_plate_type(self):
        return self._plate_type

    @property
    def gcode_file(self):
        return self._gcode_file

    @gcode_file.setter
    def gcode_file(self, value):
        self._gcode_file = value

    @property
    def print_type(self):
        return self._print_type

    @property
    @deprecated(
        "This property is deprecated (v1.0.0). Use `BambuState.print_percentage`."
    )
    def percent_complete(self) -> int:
        return self.printer_state.print_percentage

    @property
    @deprecated(
        "This property is deprecated (v1.0.0). Use `BambuState.remaining_minutes`."
    )
    def time_remaining(self) -> int:
        return int(self._printer_state.remaining_minutes)

    @property
    def start_time(self) -> int:
        return self._start_time

    @property
    def elapsed_time(self) -> int:
        return self._elapsed_time

    @property
    @deprecated("This property is deprecated (v1.0.0). Use `BambuState.total_layers`.")
    def layer_count(self):
        return self._printer_state.total_layers

    @property
    @deprecated("This property is deprecated (v1.0.0). Use `BambuState.current_layer`.")
    def current_layer(self):
        return self._printer_state.current_layer

    @property
    @deprecated(
        "This property is deprecated (v1.0.0). Use `BambuState.current_stage_id`."
    )
    def current_stage(self):
        return self._printer_state.current_stage_id

    @property
    @deprecated(
        "This property is deprecated (v1.0.0). Use `BambuState.current_stage_name`."
    )
    def current_stage_text(self):
        return self.printer_state.current_stage_name

    @property
    def spools(self):
        return self._spools

    @property
    def printer_state(self) -> BambuState:
        return self._printer_state if self._printer_state else BambuState()

    @deprecated("This property is deprecated (v1.0.0). Use `BambuState.target_tray_id`.")
    def target_spool(self):
        return self._printer_state.target_tray_id

    @property
    @deprecated("This property is deprecated (v1.0.0). Use `BambuState.active_tray_id`.")
    def active_spool(self):
        return self._printer_state.active_tray_id

    @property
    @deprecated(
        "This property is deprecated (v1.0.0). Use `BambuState.active_tray_state`."
    )
    def spool_state(self):
        return self._printer_state.active_tray_state

    @property
    @deprecated("This property is deprecated (v1.0.0). Use `BambuState.ams_status_text`.")
    def ams_status(self):
        return self._printer_state.ams_status_text

    @property
    @deprecated(
        "This property is deprecated (v1.0.0). Use `BambuState.ams_connected_count > 0`."
    )
    def ams_exists(self):
        return self._printer_state.ams_connected_count > 0

    @property
    @deprecated(
        "This property is deprecated (v1.0.0). Use `BambuState.ams_units[0].rfid_ready`."
    )
    def ams_rfid_status(self):
        return (
            self._printer_state.ams_units[0].rfid_ready
            if self._printer_state.ams_connected_count > 0
            else ""
        )

    @property
    def internalException(self):
        return self._internalException

    @property
    def cached_sd_card_contents(self):
        return self._sdcard_contents

    @property
    def cached_sd_card_3mf_files(self):
        return self._sdcard_3mf_files

    @property
    def hms_data(self):
        return self._hms_data

    @property
    def skipped_objects(self):
        return self._skipped_objects

    @property
    def nozzle_diameter(self) -> NozzleDiameter:
        try:
            return NozzleDiameter(float(self._nozzle_diameter))
        except (ValueError, TypeError, KeyError) as e:
            logger.warning(f"nozzle_diameter - exception: [{e}]")
            return NozzleDiameter.UNKNOWN

    @property
    def nozzle_type(self) -> NozzleType:
        if not self._nozzle_type:
            return NozzleType.UNKNOWN
        try:
            return NozzleType[self._nozzle_type.upper()]
        except (ValueError, TypeError, KeyError) as e:
            logger.warning(f"nozzle_type - exception: [{e}]")
            return NozzleType.UNKNOWN

    def _notify_update(self):
        if self.on_update:
            self.on_update(self)
