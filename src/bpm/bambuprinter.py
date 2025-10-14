import json
from webcolors import hex_to_name, name_to_hex
import paho.mqtt.client as mqtt

from threading import Thread
import threading

import ssl
import time
import traceback
import math

from typing import Optional

from .bambucommands import *
from .bambuspool import BambuSpool
from .bambutools import PrinterState, PlateType, PrintOption, AMSControlCommand, AMSUserSetting
from .bambutools import parseStage, parseFan
from .bambuconfig import BambuConfig

from .ftpsclient.ftpsclient import IoTFTPSClient

import os
import atexit
import logging.config
import logging.handlers
import copy

logger = logging.getLogger("bambuprintermanager")
    
class BambuPrinter:
    """
    `BambuPrinter` is the main class within `bambu-printer-manager` for interacting with and
    managing your Bambu Lab 3d printer. It provides an object oriented abstraction layer 
    between your project and the `mqtt` and `ftps` based mechanisms in place for communicating
    with your printer.
    """
    def __init__(self, config: Optional[BambuConfig] = BambuConfig()):
        """
        Sets up all internal storage attributes for `BambuPrinter` and bootstraps the
        logging engine.

        Parameters
        ----------
        * config : Optional[BambuConfig] = BambuConfig()

        Attributes
        ----------
        * _mqtt_client_thread: `PRIVATE` Thread handle for the mqtt client thread
        * _watchdog_thread: `PRIVATE` Thread handle for the watchdog thread
        * _internalExcepton: `READ ONLY` Returns the underlying `Exception` object if a failure occurred.
        * _lastMessageTime: `READ ONLY` Epoch timestamp (in seconds) for the last time an update was received from the printer.
        * _recent_update: `READ ONLY` Indicates that a message from the printer has been recently processed.
        * _config: `READ/WRITE` `bambuconfig.BambuConfig` Configuration object associated with this instance.
        * _state: `READ/WRITE` `bambutools.PrinterState` enum reports on health / status of the connection to the printer.
        * _client: `READ ONLY` Provides access to the underlying `paho.mqtt.client` library.
        * _on_update: `READ/WRITE` Callback used for pushing updates.  Includes a self reference to `BambuPrinter` as an argument.
        * _bed_temp: `READ ONLY` The current printer bed temperature.
        * _bed_temp_target: `READ/WRITE` The target bed temperature for the printer.
        * _bed_temp_target_time: `READ ONLY` Epoch timetamp for when target bed temperature was last set.
        * _tool_temp: `READ ONLY` The current printer tool temperature.
        * _tool_temp_target: `READ/WRITE` The target tool temperature for the printer.
        * _tool_temp_target_time: `READ ONLY` Epoch timetamp for when target tool temperature was last set.
        * _chamber_temp `READ/WRITE` Not currently integrated but can be used as a stub for external chambers.
        * _chamber_temp_target `READ/WRITE` Not currently integrated but can be used as a stub for external chambers.
        * _chamber_temp_target_time: `READ ONLY` Epoch timetamp for when target chamber temperature was last set.
        * _fan_gear `READ ONLY` Combined fan(s) reporting value.  Can be bit shifted for individual speeds.
        * _heat_break_fan_speed `READ_ONLY` The heatbreak (heater block) fan speed in percent.
        * _fan_speed `READ ONLY` The parts cooling fan speed in percent.
        * _fan_speed_target `READ/WRITE` The parts cooling fan target speed in percent.
        * _fan_speed_target_time: `READ ONLY` Epoch timetamp for when target fan speed was last set.
        * _light_state `READ/WRITE` Boolean value indicating the state of the work light.
        * _wifi_signal `READ ONLY` The current Wi-Fi signal strength of the printer.
        * _speed_level `READ/WRITE` System Print Speed (1=Quiet, 2=Standard, 3=Sport, 4=Ludicrous).
        * _gcode_state `READ ONLY` State reported for job status (FAILED/RUNNING/PAUSE/IDLE/FINISH).
        * _gcode_file `READ ONLY` The name of the current or last printed gcode file.
        * _3mf_file `READ ONLY` The name of the 3mf file currently being printed.
        * _plate_num `READ ONLY` The selected plate # for the current 3mf file.
        * _subtask_name `READ ONLY` The name of the active subtask.
        * _print_type `READ ONLY` Not entirely sure.  Reports "idle" when no job is active.
        * _percent_complete `READ ONLY` Percentage complete for the current active job.
        * _time_remaining `READ ONLY` The number of estimated minutes remaining for the active job.
        * _start_time `READ ONLY` The start time of the last (or current) active job in epoch minutes.
        * _elapsed_time `READ ONLY` The number of elapsed minutes for the last (or current) active job.
        * _layer_count `READ ONLY` The total number of layers for the current active job.
        * _current_layer `READ ONLY` The current layer being printed for the current active job.
        * _current_stage `READ ONLY` Maps to `bambutools.parseStage`.
        * _current_stage_text `READ ONLY` Parsed `current_stage` value.
        * _spools `READ ONLY` A Tuple of all loaded spools.  Can contain up to 5 `BambuSpool` objects.
        * _target_spool `READ_ONLY` The spool # the printer is transitioning to (`0-3`=AMS, `254`=External, `255`=None).
        * _active_spool `READ_ONLY` The spool # the printer is using right now (`0-3`=AMS, `254`=External, `255`=None).
        * _spool_state `READ ONLY` Indicates whether the spool is Loaded, Loading, Unloaded, or Unloading.
        * _ams_status `READ ONLY` Bitwise encoded status of the AMS (not currently used).
        * _ams_exists `READ ONLY` Boolean value represents the detected presense of an AMS.
        * _ams_rfid_status `READ ONLY` Bitwise encoded status of the AMS RFID reader (not currently used).
        * _sdcard_contents `READ ONLY` `dict` (json) value of all files on the SDCard (requires `get_sdcard_contents` be called first).
        * _sdcard_3mf_files `READ ONLY` `dict` (json) value of all `.3mf` files on the SDCard (requires `get_sdcard_3mf_files` be called first).
        * _hms_data `READ ONLY` `dict` (json) value of any active hms codes with descriptions attached if they are known codes.
        * _hms_message `READ ONLY` all hms_data `desc` fields concatinated into a single string for ease of use.
        * _print_type `READ ONLY` can be `cloud` or `local`
        * _skipped_objects `READ ONLY` array of objects that have been skipped / cancelled
        * _nozzle_type `READ/WRITE` the type of nozzle loaded into the printer
        * _nozzle_diameter `READ/WRITE the diameter of the nozzle loaded into the printer

        The attributes (where appropriate) are included whenever the class is serialized
        using its `toJson()` method.  
        
        When accessing the class level attributes, use their associated properties as the 
        class level attributes are marked private.
        """
        setup_logging()

        self._mqtt_client_thread = None
        self._watchdog_thread = None

        self._internalException = None
        self._lastMessageTime = None
        self._recent_update = False

        self._config = config
        self._state = PrinterState.NO_STATE

        self._client = None
        self._on_update = None

        self._bed_temp = 0.0
        self._bed_temp_target = 0.0
        self._bed_temp_target_time = 0

        self._tool_temp = 0.0
        self._tool_temp_target = 0.0
        self._tool_temp_target_time = 0

        self._chamber_temp = 0.0
        self._chamber_temp_target = 0.0
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
        self._plate_num = 0
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

        self._spools = ()
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
        logger.debug("session start_session")
        if self.config.hostname is None or self.config.access_code is None or self.config.serial_number is None:
            raise Exception("hostname, access_code, and serial_number are required")
        if self.client and self.client.is_connected():
            raise Exception("a session is already active")

        def on_connect(client, userdata, flags, reason_code, properties):
            logger.debug("session on_connect")
            if self.state != PrinterState.PAUSED:
                self.state = PrinterState.CONNECTED
                client.subscribe(f"device/{self.config.serial_number}/report")
                logger.debug(f"subscribed to [device/{self.config.serial_number}/report]")
        def on_disconnect(client, userdata, flags, reason_code, properties):
            logger.debug("session on_disconnect")
            if self._internalException:
                logger.exception("an internal exception occurred")
                self.state = PrinterState.QUIT
                raise self._internalException
            if self.state != PrinterState.PAUSED:
                self.state = PrinterState.DISCONNECTED
        def on_message(client, userdata, msg):
            logger.debug("session on_message", extra={"state": self.state.name})
            if self._lastMessageTime and self._recent_update: self._lastMessageTime = time.time()
            self._on_message(json.loads(msg.payload.decode("utf-8")))
        def loop_forever(printer):
            logger.debug("session loop_forever")
            try:
                printer.client.loop_forever(retry_first_connection=True)            
            except Exception as e:
                logger.exception("an internal exception occurred")
                printer._internalException = e
                if printer.client and printer.client.is_connected(): printer.client.disconnect() 
            printer.state = PrinterState.QUIT

        self.client =  mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

        self.client.on_connect = on_connect
        self.client.on_disconnect = on_disconnect
        self.client.on_message = on_message

        self.client.tls_set(tls_version=ssl.PROTOCOL_TLS, cert_reqs=ssl.CERT_NONE)
        self.client.tls_insecure_set(True)
        self.client.reconnect_delay_set(min_delay=1, max_delay=1)

        self.client.username_pw_set(self.config.mqtt_username, password=self.config.access_code)
        self.client.user_data_set(self.config.mqtt_client_id)

        try:
            self.client.connect(self.config.hostname, self.config.mqtt_port, 60)
        except Exception as e:
            self._internalException = e
            logger.warning(f"unable to connect to printer - reason: {e}", extra={"exception": traceback.format_exc()})
            self.state = PrinterState.QUIT
            return

        self._mqtt_client_thread = threading.Thread(target=loop_forever, name="bambuprinter-session", args=(self,))
        self._mqtt_client_thread.start()

        self._start_watchdog()

    def pause_session(self):
        """
        Pauses the `BambuPrinter` session is it is active.  Under the covers this
        method unsubscribes from the `/report` topic, essentially disabling all
        printer data refreshes.
        """
        if self.state != PrinterState.PAUSED:
            self.client.unsubscribe(f"device/{self.config.serial_number}/report")
            logger.debug(f"unsubscribed from [device/{self.config.serial_number}/report]")
            self.state = PrinterState.PAUSED

    def resume_session(self):
        """
        Resumes a previously paused session by re-subscribing to the /report topic.
        """
        if self.client and self.client.is_connected() and self.state == PrinterState.PAUSED:
            self.client.subscribe(f"device/{self.config.serial_number}/report")
            logger.debug(f"subscribed to [device/{self.config.serial_number}/report]")
            self._lastMessageTime = time.time()
            self.state = PrinterState.CONNECTED
            return
        self.state = PrinterState.QUIT

    def quit(self):
        """
        Shuts down all threads.  Your `BambuPrinter` instance should probably be 
        considered dead after making this call although you may be able to restart a
        session with [start_session](./#bpm.bambuprinter.BambuPrinter.start_session)().
        """
        if self.client and self.client.is_connected():
            self.client.disconnect()
            logger.debug("mqtt client was connected and is now disconnected")
        else:
            logger.debug("mqtt client was already disconnected")

        self._state == PrinterState.QUIT
        if self.on_update: self.on_update(self)

        if self._mqtt_client_thread.is_alive(): self._mqtt_client_thread.join()
        if self._watchdog_thread.is_alive(): self._watchdog_thread.join()
        logger.debug("all threads have terminated")

    def refresh(self):
        """
        Triggers a full data refresh from the printer (if it is connected).  You should use this
        method sparingly as resorting to it indicates something is not working properly.
        """
        if self.state == PrinterState.CONNECTED:
            logger.debug(f"publishing ANNOUNCE_PUSH to [device/{self.config.serial_number}/request]")
            self.client.publish(f"device/{self.config.serial_number}/request", json.dumps(ANNOUNCE_PUSH))
            logger.debug(f"publishing ANNOUNCE_VERSION to [device/{self.config.serial_number}/request]")
            self.client.publish(f"device/{self.config.serial_number}/request", json.dumps(ANNOUNCE_VERSION))

    def unload_filament(self):
        """
        Requests the printer to unload whatever filament / spool may be currently loaded.
        """
        self.client.publish(f"device/{self.config.serial_number}/request", json.dumps(UNLOAD_FILAMENT))
        logger.debug(f"published UNLOAD_FILAMENT to [device/{self.config.serial_number}/request]")

    def load_filament(self, slot: int):
        """
        Requests the printer to load filament into the extruder using the requested spool (slot #)

        Parameters
        ----------
        slot : int

        * `0` - AMS Spool #1
        * `1` - AMS Spool #2
        * `2` - AMS Spool #3
        * `3` - AMS Spool #4
        * `254` - External Spool
        """
        msg = AMS_FILAMENT_CHANGE
        msg["print"]["target"] = int(slot)
        self.client.publish(f"device/{self.config.serial_number}/request", json.dumps(msg))
        logger.debug(f"published AMS_FILAMENT_CHANGE to [device/{self.config.serial_number}/request]", extra={"target": slot, "bambu_msg": msg})

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
        self.client.publish(f"device/{self.config.serial_number}/request", json.dumps(cmd))
        logger.debug(f"published SEND_GCODE_TEMPLATE to [device/{self.config.serial_number}/request]", extra={"gcode": gcode})

    def print_3mf_file(self, 
                        name: str, 
                        plate: int,
                        bed: PlateType, 
                        use_ams: bool, 
                        ams_mapping: Optional[str] = "", 
                        bedlevel: Optional[bool] = True, 
                        flow: Optional[bool] = True, 
                        timelapse: Optional[bool] = False):
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

        file = copy.deepcopy(PRINT_3MF_FILE)

        subtask = name[name.rindex("/") + 1::] if "/" in name else name
        subtask = subtask[::-1].replace(".3mf"[::-1], "", 1)[::-1] if subtask.endswith(".3mf") else subtask 
        subtask = subtask[::-1].replace(".gcode"[::-1], "", 1)[::-1] if subtask.endswith(".gcode") else subtask 

        file["print"]["file"] = self._3mf_file
        file["print"]["url"] = f"file:///sdcard{self._3mf_file}"
        file["print"]["subtask_name"] = subtask
        file["print"]["bed_type"] = bed.name.lower()
        file["print"]["param"] = file["print"]["param"].replace("#", str(self._plate_num))
        file["print"]["use_ams"] = use_ams
        if len(ams_mapping) > 0:
            file["print"]["ams_mapping"] = json.loads(ams_mapping)
        file["print"]["bed_leveling"] = bedlevel
        file["print"]["flow_cali"] = flow
        file["print"]["timelapse"] = timelapse
        self.client.publish(f"device/{self.config.serial_number}/request", json.dumps(file))
        logger.debug(f"published PRINT_3MF_FILE to [device/{self.config.serial_number}/request]", extra={"print_command": file})

    def stop_printing(self):
        """
        Requests the printer to stop printing if a job is currently running.
        """
        self.client.publish(f"device/{self.config.serial_number}/request", json.dumps(STOP_PRINT))
        logger.debug(f"published STOP_PRINT to [device/{self.config.serial_number}/request]")

    def pause_printing(self):
        """
        Pauses the current print job if one is running.
        """
        self.client.publish(f"device/{self.config.serial_number}/request", json.dumps(PAUSE_PRINT))
        logger.debug(f"published PAUSE_PRINT to [device/{self.config.serial_number}/request]")

    def resume_printing(self):
        """
        Resumes the current print job if one is paused.
        """
        self.client.publish(f"device/{self.config.serial_number}/request", json.dumps(RESUME_PRINT))
        logger.debug(f"published RESUME_PRINT to [device/{self.config.serial_number}/request]")

    def get_sdcard_3mf_files(self):
        """
        Returns a `dict` (json document) of all `.3mf` files on the printer's SD card. 
        The private class level `_sdcard_3mf_files` attribute is also populated.
        
        Usage
        -----
        The return value of this method is very useful for binding to things like a clientside `TreeView`
        """
        return self._sdcard_3mf_files

    def get_sdcard_contents(self):
        """
        Returns a `dict` (json document) of ALL files on the printer's SD card. 
        The private class level `_sdcard_contents` attribute is also populated.
        
        Usage
        -----
        The return value of this method is very useful for binding to things like a clientside `TreeView`
        """
        ftps = IoTFTPSClient(self._config.hostname, 990, self._config.mqtt_username, self._config.access_code, ssl_implicit=True)
        fs = self._get_sftp_files(ftps, "/")
        logger.debug("read all sdcard files", extra={"fs": fs})
        self._sdcard_contents = fs

        def search_for_and_remove_all_other_files(mask: str, entry: dict):
            if "children" in entry:
                entry["children"] = list(filter(lambda i: i['id'].endswith(mask) or 'children' in i.keys(), entry["children"]))
                for child in entry["children"]:
                    search_for_and_remove_all_other_files(mask, child)

        self._sdcard_3mf_files = json.loads(json.dumps(self._sdcard_contents)) 
        search_for_and_remove_all_other_files(".3mf", self._sdcard_3mf_files)

        return fs

    def delete_sdcard_file(self, file: str):
        """
        Delete the specified file on the printer's SDCard and returns an updated dict of all files on the printer
        
        Parameters
        ----------
        * file : str - the full path filename to be deleted
        """
        logger.debug(f"deleting remote file: [{file}]", extra={"file": file})
        ftps = IoTFTPSClient(self._config.hostname, 990, self._config.mqtt_username, self._config.access_code, ssl_implicit=True)
        ftps.delete_file(file)

        def search_for_and_remove_file(file: str, entry: dict):
            if "children" in entry:
                entry["children"] = list(filter(lambda i: i['id'] != file, entry["children"]))
                for child in entry["children"]:
                    search_for_and_remove_file(file, child)

        search_for_and_remove_file(file, self._sdcard_contents)
        search_for_and_remove_file(file, self._sdcard_3mf_files)
        return self._sdcard_contents

    def upload_sdcard_file(self, src: str, dest: str) -> {}:
        """
        Uploads the local filesystem file to the printer and returns an updated dict of all files on the printer

        Parameters
        ----------
        * src : str - the full path filename on the host to be uploaded to the printer
        * dest : str - the full path filename on the printer to upload to
        """
        logger.debug(f"uploading file src: [{src}] dest: [{dest}]")
        ftps = IoTFTPSClient(self._config.hostname, 990, self._config.mqtt_username, self._config.access_code, ssl_implicit=True)
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
        logger.debug(f"downloading file src: [{src}] dest: [{dest}]")
        ftps = IoTFTPSClient(self._config.hostname, 990, self._config.mqtt_username, self._config.access_code, ssl_implicit=True)
        ftps.download_file(src, dest)
        return 
    
    def make_sdcard_directory(self, dir: str) -> {}:
        """
        Creates the specified directory on the printer and returns an updated dict of all files on the printer

        Parameters
        ----------
        * dir : str - the full path directory name to be created
        """
        ftps = IoTFTPSClient(self._config.hostname, 990, self._config.mqtt_username, self._config.access_code, ssl_implicit=True)
        logger.debug(f"creating remote directory [{dir}]")
        ftps.mkdir(dir)
        return self.get_sdcard_contents()

    def rename_sdcard_file(self, src: str, dest: str) -> {}:
        """
        Renames the specified file on the printer and returns an updated dict of all files on the printer

        Parameters
        ----------
        * src : str - the full path name to be renamed
        * dest : str - the full path name to be renamed to
        """
        ftps = IoTFTPSClient(self._config.hostname, 990, self._config.mqtt_username, self._config.access_code, ssl_implicit=True)
        logger.debug(f"renaming printer file [{src}] to [{dest}]")
        ftps.move_file(src, dest)
        return self.get_sdcard_contents()

    def sdcard_file_exists(self, path: str) -> bool:
        """
        Checks to see if a file exists on the printer at the `path` specified

        Parameters
        ----------
        * path : str - the full path name to check
        """
        ftps = IoTFTPSClient(self._config.hostname, 990, self._config.mqtt_username, self._config.access_code, ssl_implicit=True)
        logger.debug(f"checking if printer file [{path}] exists")
        return ftps.fexists(path)

    def set_print_option(self, option: PrintOption, enabled: bool):
        """
        Enable or disable one of the `PrintOption` options
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

        self.client.publish(f"device/{self.config.serial_number}/request", json.dumps(cmd))
        logger.debug(f"published PRINT_OPTION_COMMAND to [device/{self.config.serial_number}/request]", extra={"bambu_msg": cmd})

    def set_ams_user_setting(self, setting: AMSUserSetting, enabled: bool, ams_id : Optional[int] = 0):
        """
        Enable or disable one of the `AMSUserSetting` options
        """        
        cmd = copy.deepcopy(AMS_USER_SETTING)
        cmd["print"]["ams_id"] = ams_id
        cmd["print"][AMSUserSetting.CALIBRATE_REMAIN_FLAG.name.lower()] = self.config.calibrate_remain_flag
        cmd["print"][AMSUserSetting.STARTUP_READ_OPTION.name.lower()] = self.config.startup_read_option
        cmd["print"][AMSUserSetting.TRAY_READ_OPTION.name.lower()] = self.config.tray_read_option

        cmd["print"][setting.name.lower()] = enabled

        if setting == AMSUserSetting.STARTUP_READ_OPTION:
            self.config.startup_read_option = enabled
        elif setting == AMSUserSetting.TRAY_READ_OPTION:
            self.config.tray_read_option = enabled
        elif setting == AMSUserSetting.CALIBRATE_REMAIN_FLAG:
            self.config.calibrate_remain_flag = enabled

        self.client.publish(f"device/{self.config.serial_number}/request", json.dumps(cmd))
        logger.debug(f"published AMS_USER_SETTING to [device/{self.config.serial_number}/request]", extra={"bambu_msg": cmd})

    def set_spool_k_factor(self, 
                           tray_id : int, 
                           k_value : float, 
                           n_coef : Optional[float]  = 1.399999976158142, 
                           nozzle_temp : Optional[int] = -1,
                           bed_temp : Optional[int] = -1, 
                           max_volumetric_speed : Optional[int] = -1):
        """
        Sets the linear advance k factor for a specific spool / tray
        """
        cmd = copy.deepcopy(EXTRUSION_CALI_SET)
        cmd["print"]["tray_id"] = tray_id
        cmd["print"]["k_value"] = k_value
        cmd["print"]["n_coef"] = n_coef 

        if nozzle_temp != -1:
            cmd["print"]["nozzle_temp"] = nozzle_temp
        if bed_temp != -1:
            cmd["print"]["bed_temp"] = bed_temp
        if max_volumetric_speed != -1:
            cmd["print"]["max_volumetric_speed"] = max_volumetric_speed
        
        self.client.publish(f"device/{self.config.serial_number}/request", json.dumps(cmd))
        logger.debug(f"published EXTRUSION_CALI_SET to [device/{self.config.serial_number}/request]", extra={"bambu_msg": cmd})

    def set_spool_details(self, 
                           tray_id : int, 
                           tray_info_idx : str, 
                           tray_id_name : Optional[str] = "",
                           tray_type : Optional[str]  = "", 
                           tray_color : Optional[str] = "",
                           nozzle_temp_min : Optional[int] = -1, 
                           nozzle_temp_max : Optional[int] = -1):
        """
        Sets spool / tray details such as filament type, color, and nozzle min/max temperature.
        For the external tray (254), send `no_filament` as the `tray_info_idx` value to empty the tray.
        """
        cmd = copy.deepcopy(AMS_FILAMENT_SETTING)

        ams_id = math.floor(tray_id / 4)
        if tray_id == 254: ams_id = 255

        cmd["print"]["ams_id"] = ams_id
        cmd["print"]["tray_id"] = tray_id

        if tray_info_idx == "no_filament":
            tray_info_idx = ""
            tray_id_name = ""
            tray_type = ""
            tray_color = "FFFFFF00"
            nozzle_temp_min = 0
            nozzle_temp_max = 0
            cmd["print"]["setting_id"] = ""  
            cmd["print"]["slot_id"] = tray_id
            cmd["print"]["tray_type"] = tray_type

        cmd["print"]["tray_info_idx"] = tray_info_idx

        if tray_id_name != "":
            cmd["print"]["tray_id_name"] = tray_id_name
        if tray_type != "":
            cmd["print"]["tray_type"] = tray_type
        if tray_color != "":
            color = ""
            try:
                color = f"{name_to_hex(tray_color)}FF".replace("#", "").upper()
            except:
                color = tray_color
            cmd["print"]["tray_color"] = color
        if nozzle_temp_min != -1:
            cmd["print"]["nozzle_temp_min"] = nozzle_temp_min
        if nozzle_temp_max != -1:
            cmd["print"]["nozzle_temp_max"] = nozzle_temp_max
        
        self.client.publish(f"device/{self.config.serial_number}/request", json.dumps(cmd))
        logger.debug(f"published AMS_FILAMENT_SETTING to [device/{self.config.serial_number}/request]", extra={"bambu_msg": cmd})

    def send_ams_control_command(self, ams_control_cmd : AMSControlCommand):
        """
        Send an AMS Control Command - will pause, resume, or reset the AMS.
        """
        ams_cmd = ams_control_cmd.name.lower()
        cmd = copy.deepcopy(AMS_CONTROL)
        cmd["print"]["param"] = ams_cmd

        self.client.publish(f"device/{self.config.serial_number}/request", json.dumps(cmd))
        logger.debug(f"published AMS_CONTROL to [device/{self.config.serial_number}/request]", extra={"bambu_msg": cmd})

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
        self.client.publish(f"device/{self.config.serial_number}/request", json.dumps(cmd))
        logger.debug(f"published SKIP_OBJECTS to [device/{self.config.serial_number}/request]", extra={"bambu_msg": cmd})

    def set_buildplate_marker_detector(self, 
                           enabled : bool):
        """
        Enables or disables the buildplate_marker_detector
        """
        cmd = copy.deepcopy(XCAM_CONTROL_SET)
        cmd["xcam"]["control"] = enabled
        cmd["xcam"]["enable"] = enabled
        
        self.client.publish(f"device/{self.config.serial_number}/request", json.dumps(cmd))
        logger.debug(f"published XCAM_CONTROL_SET to [device/{self.config.serial_number}/request]", extra={"bambu_msg": cmd})


    def toJson(self):
        """
        Returns a `dict` (json document) representing this object's private class
        level attributes that are serializable (most are).
        """
        response = json.dumps(self, default=self.jsonSerializer, indent=4, sort_keys=True)
        return json.loads(response)

    def jsonSerializer(self, obj):
        """
        Helper method used by `toJson()` to serialize this object.  
        """
        try:
            if isinstance(obj, mqtt.Client) or isinstance(obj, Thread):
                return "these are not the droids you are looking for"
            if str(obj.__class__).replace("<class '", "").replace("'>", "") == "mappingproxy":
                return "this space intentionally left blank"
            return obj.__dict__
        except Exception as e:
            logger.warning("unable to serialize object", extra={"obj": obj})
            return "not available"


    def _start_watchdog(self): 
        def watchdog_thread(printer):
            try:
                while printer.state != PrinterState.QUIT:
                    if printer.state == PrinterState.CONNECTED and (printer._lastMessageTime is None or printer._lastMessageTime + printer.config.watchdog_timeout < time.time()):
                        if printer._lastMessageTime: logger.warning("BambuPrinter watchdog timeout")
                        printer._lastMessageTime = time.time()
                        printer._recent_update = False
                        printer.client.publish(f"device/{printer.config.serial_number}/request", json.dumps(ANNOUNCE_PUSH))
                        printer.client.publish(f"device/{printer.config.serial_number}/request", json.dumps(ANNOUNCE_VERSION))
                    time.sleep(.1)
            except Exception as e:
                logger.exception("an internal exception occurred")
                printer._internalException = e
                if printer.client and printer.client.is_connected(): printer.client.disconnect()

        self._watchdog_thread = threading.Thread(target=watchdog_thread, name="bambuprinter-session-watchdog", args=(self,))
        self._watchdog_thread.start()

    def _on_message(self, message: str):
        logger.debug("_on_message", extra={"bambu_msg": message})

        if "system" in message:
            system = message["system"]

        elif "print" in message:
            status = message["print"]

            if "command" in status and status["command"] == "project_file":
                self._start_time = 0
                if self._3mf_file:
                    logger.debug("project_file request acknowledged")
                else:
                    url = status.get("url", None)
                    subtask = status.get("subtask_name", None)
                    if url and subtask and url.startswith("https://"):
                        self._3mf_file = f"/cache/{subtask}.3mf"
                    else:
                        if "file" in status:
                            self._3mf_file = status.get("file", "")
                        else:
                            logger.warning("unable to determine file being printed")

            # let's sleep for a couple seconds and do a full refresh
            # if ams filament settings have changed
            if "command" in status and status["command"] == "ams_filament_setting":
                time.sleep(2)
                logger.debug(f"filament change triggered publishing ANNOUNCE_PUSH to [device/{self.config.serial_number}/request]")
                self.client.publish(f"device/{self.config.serial_number}/request", json.dumps(ANNOUNCE_PUSH))

            if "bed_temper" in status: self._bed_temp = float(status["bed_temper"])
            if "bed_target_temper" in status: 
                bed_temp_target = float(status["bed_target_temper"]) 
                if bed_temp_target != self._bed_temp_target:
                    self._bed_temp_target = bed_temp_target
                    self._bed_temp_target_time = round(time.time())

            if "nozzle_temper" in status: self._tool_temp = float(status["nozzle_temper"])
            if "nozzle_target_temper" in status: 
                tool_temp_target = float(status["nozzle_target_temper"])
                if tool_temp_target != self._tool_temp_target:
                    self._tool_temp_target = tool_temp_target
                    self._tool_temp_target_time = round(time.time())

            if not self._config.external_chamber and "chamber_temper" in status: self._chamber_temp = float(status["chamber_temper"])

            if "fan_gear" in status: self._fan_gear = int(status["fan_gear"])
            if "heatbreak_fan_speed" in status: self._heatbreak_fan_speed = int(status["heatbreak_fan_speed"])
            if "cooling_fan_speed" in status: self._fan_speed = parseFan(int(status["cooling_fan_speed"]))

            if "wifi_signal" in status: self._wifi_signal = status["wifi_signal"] 
            if "lights_report" in status: self._light_state = (status["lights_report"])[0]["mode"]
            if "spd_lvl" in status: self._speed_level = status["spd_lvl"]

            if "gcode_state" in status: 
                self._gcode_state = status["gcode_state"]
                if self._gcode_state in ("FINISH", "FAILED") and self._3mf_file:
                    self._3mf_file = ""

            if "subtask_name" in status: self._subtask_name = status["subtask_name"]
            if "gcode_file" in status: self._gcode_file = status["gcode_file"]
            if "print_type" in status: self._print_type = status["print_type"]
            if "mc_percent" in status: self._percent_complete = status["mc_percent"]
            if "mc_remaining_time" in status: self._time_remaining = int(status["mc_remaining_time"])
            if "total_layer_num" in status: self._layer_count = status["total_layer_num"]
            if "layer_num" in status: self._current_layer = status["layer_num"]
            
            if "stg_cur" in status: 
                self._current_stage = int(status["stg_cur"])
                self._current_stage_text = parseStage(self._current_stage)

            if "ams_status" in status: self._ams_status = status["ams_status"]
            if "ams_rfid_status" in status: self._ams_rfid_status = status["ams_rfid_status"]

            if "ams" in status and "ams" in status["ams"] and "ams_exist_bits" in status["ams"]:
                self._ams_exists = int(status["ams"]["ams_exist_bits"]) == 1
                if self._ams_exists:
                    spools = []
                    ams = (status["ams"]["ams"])[0]

                    self.config.startup_read_option = status["ams"].get("power_on_flag", False)
                    self.config.tray_read_option = status["ams"].get("insert_flag", False)

                    for tray in ams["tray"]:
                        try:
                            tray_color = hex_to_name("#" + tray["tray_color"][:6])
                        except:
                            try:
                                tray_color = "#" + tray["tray_color"]
                            except:
                                tray_color = ""
                        
                        if tray.get("id"):
                            spool = BambuSpool( 
                                                int(tray["id"]),  
                                                tray.get("tray_id_name", ""),  
                                                tray.get("tray_type", ""), 
                                                tray.get("tray_sub_brands", ""), 
                                                tray_color,
                                                tray.get("tray_info_idx", ""),
                                                tray.get("k", 0.0),
                                                tray.get("bed_temp", 0),
                                                tray.get("nozzle_temp_min", 0),
                                                tray.get("nozzle_temp_max", 0) 
                                              )
                            spools.append(spool)
                    self._spools = tuple(spools)

            if "vt_tray" in status:
                tray = status["vt_tray"]
                try:
                    tray_color = hex_to_name("#" + tray["tray_color"][:6])
                except:
                    try:
                        tray_color = "#" + tray["tray_color"]
                    except:
                        tray_color = ""

                if tray.get("id", None):
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
                                        tray.get("nozzle_temp_max", 0)
                                      )
                    if not self._ams_exists: 
                        spools = (spool,)
                    else:
                        spools = list(self.spools)
                        spools.append(spool)

                    self._spools = tuple(spools)

            tray_tar = None
            tray_now = None
            tray_pre = None

            if "ams" in status and "tray_tar" in status["ams"]:
                tray_tar = int(status["ams"]["tray_tar"])
                self._target_spool = tray_tar

            if "ams" in status and "tray_now" in status["ams"]:
                tray_now = int(status["ams"]["tray_now"])
                self._active_spool = tray_now

            if "ams" in status and "tray_pre" in status["ams"]:
                tray_pre = int(status["ams"]["tray_pre"])

            if not tray_tar is None or not tray_now is None or not tray_pre is None:
                if self._target_spool == 255 and self._active_spool == 255:
                    self._spool_state = "Unloaded"
                elif self._target_spool == 255 and self._active_spool != 255:
                    self._spool_state = "Unloading"
                elif self._active_spool != 255 and self._target_spool != 255 and self._target_spool != self._active_spool:
                    self._spool_state = "Unloading"
                elif self._target_spool != 255 and self._active_spool == 255:
                    self._spool_state = "Loading"
                else:
                    self._spool_state = "Loaded"

            self._hms_data = status.get("hms", [])
            self._hms_message = ""
 
            for hms in self._hms_data:
                hms_attr = hex(hms.get("attr", 0))[2:].zfill(8).upper()
                hms_code = hex(hms.get("code", 0))[2:].zfill(8).upper()
                for entry in HMS_STATUS["data"]["device_hms"]["en"]:
                    if entry["ecode"] == f"{hms_attr}{hms_code}":
                        hms["desc"] = entry["intro"]
                        self._hms_message = f"{self._hms_message}{entry['intro']} "
                        break

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
                self.config.buildplate_marker_detector = status["xcam"]["buildplate_marker_detector"]

        elif "info" in message and "result" in message["info"] and message["info"]["result"] == "success": 
            self._recent_update = True
            info = message["info"]
            for module in info["module"]:
                if "ota" in module["name"]: 
                    self.config.serial_number = module["sn"]
                    self.config.firmware_version = module["sw_ver"]
                if "ams" in module["name"]:
                    self.config.ams_firmware_version = module["sw_ver"]

        elif "xcam" in message and "result" in message["xcam"] and message["xcam"]["result"] == "SUCCESS": 
            # logger.debug("xcam update message received", extra={"bambu_msg": message})
            pass

        else:
            logger.warning("unknown message type received", extra={"bambu_msg": message})
            
        if self._gcode_state in ("PREPARE", "RUNNING", "PAUSE"):
            if (self._start_time == 0): self._start_time = int(round(time.time() / 60, 0))
            self._elapsed_time = int(round(time.time() / 60, 0)) - self._start_time

        if self.on_update: self.on_update(self)

    def _get_sftp_files(self, ftps: IoTFTPSClient, directory: str, mask: Optional[str] = None):
        try:
            files = sorted(ftps.list_files_ex(directory))
        except Exception as e:
            logger.warning("unexpected ftps exception")
            return None

        dir = {}

        dir["id"] = directory + ("/" if directory != "/" else "")
        dir["name"] = directory[directory.rindex("/") + 1:] if "/" in directory and directory != "/" else directory

        items = []

        for file in files:
            if file[0][:1] == "d":
                item = {}
                item = self._get_sftp_files(ftps, directory + ("/" if directory != "/" else "") + file[1], mask=mask)
                items.append(item)
            else:
                if not mask or (mask and file[1].lower().endswith(mask)):
                    item = {}
                    item["id"] = dir["id"] + file[1]
                    item["name"] = file[1]
                    items.append(item)

        if len(items) > 0: dir["children"] = items
        return dir


    @property 
    def config(self) -> BambuConfig:
        return self._config
    @config.setter 
    def config(self, value: BambuConfig):
        self._config = value

    @property 
    def state(self):
        return self._state
    @state.setter 
    def state(self, value: PrinterState):
        self._state = value

    @property 
    def client(self):
        return self._client
    @client.setter 
    def client(self, value: mqtt.Client):
        self._client = value

    @property 
    def on_update(self):
        return self._on_update
    @on_update.setter 
    def on_update(self, value):
        self._on_update = value

    @property 
    def recent_update(self):
        return self._recent_update

    @property 
    def bed_temp(self):
        return self._bed_temp

    @property 
    def bed_temp_target(self):
        return self._bed_temp_target
    @bed_temp_target.setter 
    def bed_temp_target(self, value: float):
        value = float(value)
        if value < 0.0: value = 0.0
        gcode = SEND_GCODE_TEMPLATE
        gcode["print"]["param"] = f"M140 S{value}\n"
        self.client.publish(f"device/{self.config.serial_number}/request", json.dumps(gcode))
        self._bed_temp_target_time = round(time.time())

    @property 
    def tool_temp(self):
        return self._tool_temp

    @property 
    def tool_temp_target(self):
        return self._tool_temp_target
    @tool_temp_target.setter 
    def tool_temp_target(self, value: float):
        value = float(value)
        if value < 0.0: value = 0.0
        gcode = SEND_GCODE_TEMPLATE
        gcode["print"]["param"] = f"M104 S{value}\n"
        self.client.publish(f"device/{self.config.serial_number}/request", json.dumps(gcode))
        self._tool_temp_target_time = round(time.time())

    @property 
    def chamber_temp(self):
        return self._chamber_temp
    @chamber_temp.setter 
    def chamber_temp(self, value: float):
        self._chamber_temp = value

    @property 
    def chamber_temp_target(self):
        return self._chamber_temp_target
    @chamber_temp_target.setter 
    def chamber_temp_target(self, value: float):
        self._chamber_temp_target = value
        self._chamber_temp_target_time = round(time.time())

    @property 
    def fan_speed(self):
        return self._fan_speed

    @property 
    def fan_speed_target(self):
        return self._fan_speed_target
    @fan_speed_target.setter 
    def fan_speed_target(self, value: int):
        value = int(value)
        if value < 0: value = 0
        self._fan_speed_target = value
        speed = round(value * 2.55, 0)
        gcode = SEND_GCODE_TEMPLATE
        gcode["print"]["param"] = f"M106 P1 S{speed}\nM106 P2 S{speed}\nM106 P3 S{speed}\n"
        self.client.publish(f"device/{self.config.serial_number}/request", json.dumps(gcode))
        self._fan_speed_target_time = round(time.time())

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
    def heatbreak_fan_speed(self):
        return self._heatbreak_fan_speed

    @property 
    def wifi_signal(self):
        return self._wifi_signal

    @property 
    def light_state(self):
        return self._light_state == "on"
    @light_state.setter 
    def light_state(self, value: bool):
        value = bool(value)
        cmd = CHAMBER_LIGHT_TOGGLE
        if value:
            cmd["system"]["led_mode"] = "on"
        else:
            cmd["system"]["led_mode"] = "off"
        self.client.publish(f"device/{self.config.serial_number}/request", json.dumps(cmd))

    @property 
    def speed_level(self):
        return self._speed_level
    @speed_level.setter 
    def speed_level(self, value: str):
        value = str(value)
        cmd = SPEED_PROFILE_TEMPLATE
        cmd["print"]["param"] = value
        self.client.publish(f"device/{self.config.serial_number}/request", json.dumps(cmd))

    @property 
    def gcode_state(self):
        return self._gcode_state

    @property 
    def subtask_name(self):
        return self._subtask_name

    @property 
    def current_3mf_file(self):
        return self._3mf_file

    @property 
    def current_plate_num(self):
        return self._plate_num

    @property 
    def subtask_name(self):
        return self._subtask_name

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
    def percent_complete(self) -> int:
        return int(self._percent_complete) if str(self._percent_complete).isnumeric() else int(0)

    @property 
    def time_remaining(self) -> int:
        return self._time_remaining

    @property 
    def start_time(self) -> int:
        return self._start_time

    @property 
    def elapsed_time(self) -> int:
        return self._elapsed_time

    @property 
    def layer_count(self):
        return self._layer_count

    @property 
    def current_layer(self):
        return self._current_layer

    @property 
    def current_stage(self):
        return self._current_stage

    @property 
    def current_stage_text(self):
        return parseStage(self._current_stage)

    @property 
    def spools(self):
        return self._spools

    @property 
    def target_spool(self):
        return self._target_spool

    @property 
    def active_spool(self):
        return self._active_spool

    @property 
    def spool_state(self):
        return self._spool_state

    @property 
    def ams_status(self):
        return self._ams_status

    @property 
    def ams_exists(self):
        return self._ams_exists

    @property 
    def ams_rfid_status(self):
        return self._ams_rfid_status

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
    def print_type(self):
        return self._print_type

    @property
    def skipped_objects(self):
        return self._skipped_objects


def setup_logging():
    config_file = os.path.dirname(os.path.realpath(__file__)) + "/bambuprintermanagerlogger.json"
    with open(config_file) as f_in:
        config = json.load(f_in)

    logging.config.dictConfig(config)
    queue_handler = logging.getHandlerByName("queue_handler")
    if queue_handler is not None:
        queue_handler.listener.start()
        atexit.register(queue_handler.listener.stop)