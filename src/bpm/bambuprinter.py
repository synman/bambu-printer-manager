import json
from webcolors import hex_to_name
import paho.mqtt.client as mqtt
import threading
import ssl
import time
import traceback

from typing import Optional

from .bambucommands import *
from .bambuspool import BambuSpool
from .bambutools import PrinterState, PlateType
from .bambutools import parseStage, parseFan
from .bambuconfig import BambuConfig

from .ftpsclient._client import IoTFTPSClient

import os
import atexit
import logging.config
import logging.handlers

logger = logging.getLogger("bambuprinter")
    
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
        * _internalExcepton: `READ ONLY` Returns the underlying `Exception` object if a failure occurred.
        * _lastMessageTime: `READ ONLY` Epoch timestamp (in seconds) for the last time an update was received from the printer.
        * _recent_update: `READ ONLY` Indicates that a message from the printer has been recently processed.
        * _config: `READ/WRITE` `bambuconfig.BambuConfig` Configuration object associated with this instance.
        * _state: `READ/WRITE` `bambutools.PrinterState` enum reports on health / status of the connection to the printer.
        * _client: `READ ONLY` Provides access to the underlying `paho.mqtt.client` library.
        * _on_update: `READ/WRITE` Callback used for pushing updates.  Includes a self reference to `BambuPrinter` as an argument.
        * _bed_tamp: `READ ONLY` The current printer bed temperature.
        * _bed_temp_target: `READ/WRITE` The target bed temperature for the printer.
        * _tool_tamp: `READ ONLY` The current printer tool temperature.
        * _tool_temp_target: `READ/WRITE` The target tool temperature for the printer.
        * _chamber_temp `READ/WRITE` Not currently integrated but can be used as a stub for external chambers.
        * _chamber_temp_target `READ/WRITE` Not currently integrated but can be used as a stub for external chambers.
        * _fan_gear `READ ONLY` Combined fan(s) reporting value.  Can be bit shifted for individual speeds.
        * _heat_break_fan_speed `READ_ONLY` The heatbreak (heater block) fan speed in percent.
        * _fan_speed `READ ONLY` The parts cooling fan speed in percent.
        * _fan_speed_target `READ/WRITE` The parts cooling fan target speed in percent.
        * _light_state `READ/WRITE` Boolean value indicating the state of the work light.
        * _wifi_signal `READ ONLY` The current Wi-Fi signal strength of the printer.
        * _speed_level `READ/WRITE` System Print Speed (1=Quiet, 2=Standard, 3=Sport, 4=Ludicrous).
        * _gcode_state `READ ONLY` State reported for job status (FAILED/RUNNING/PAUSE/IDLE/FINISH).
        * _gcode_file `READ ONLY` The name of the current or last printed gcode file.
        * _print_type `READ ONLY` Not entirely sure.  Reports "idle" when no job is active.
        * _percent_complete `READ ONLY` Percentage complete for the current active job.
        * _time_remaining `'READ ONLY` The number of estimated minutes remaining for the active job.
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
        * _sdcard_contents `READ ONLY` `dict` (json) value of all files on the SDCard (requires `get_sdcard_contents` be called first).
        * _sdcard_3mf_files `READ ONLY` `dict` (json) value of all `.gcode.3mf` files on the SDCard (requires `get_sdcard_3mf_files` be called first).

        The attributes (where appropriate) are included whenever the class is serialized
        using its `toJson()` method.  
        
        When accessing the class level attributes, use the associated getter/setter properties as they are private.
        """
        setup_logging()

        self._internalException = None
        self._lastMessageTime = None
        self._recent_update = False

        self._config = config
        self._state = PrinterState.NO_STATE

        self._client = None
        self._on_update = None

        self._bed_temp = 0.0
        self._bed_temp_target = 0.0
        self._tool_temp = 0.0
        self._tool_temp_target = 0.0
        self._chamber_temp = 0.0
        self._chamber_temp_target = 0.0

        self._fan_gear = 0
        self._heatbreak_fan_speed = 0
        self._fan_speed = 0
        self._fan_speed_target = 0

        self._light_state = ""
        self._wifi_signal = ""
        self._speed_level = 0

        self._gcode_state = ""
        self._gcode_file = ""
        self._print_type = ""
        self._percent_complete = 0
        self._time_remaining = 0
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

        self._sdcard_contents = None
        self._sdcard_3mf_files = None

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

        def on_connect(client, userdata, flags, rc):
            logger.debug("session on_connect")
            if self.state != PrinterState.PAUSED:
                self.state = PrinterState.CONNECTED
                client.subscribe(f"device/{self.config.serial_number}/report")
                logger.debug(f"subscribed to [device/{self.config.serial_number}/report]")
        def on_disconnect(client, userdata, rc):
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

        self.client = mqtt.Client()

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

        threading.Thread(target=loop_forever, name="bambuprinter-session", args=(self,)).start()

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
            while self.state != PrinterState.QUIT:
                time.sleep(.1)
            logger.debug("mqtt client was connected and is now disconnected")
        else:
            self.state == PrinterState.QUIT
            logger.debug("mqtt client was already disconnected")

    def refresh(self):
        """
        Triggers a full data refresh from the printer (if it is connected).  You should use this
        method sparingly as resorting to it indicates something is not working properly.
        """
        if self.state == PrinterState.CONNECTED:
            self.client.publish(f"device/{self.config.serial_number}/request", json.dumps(ANNOUNCE_PUSH))
            logger.debug(f"published ANNOUNCE_PUSH to [device/{self.config.serial_number}/request]")
            self.client.publish(f"device/{self.config.serial_number}/request", json.dumps(ANNOUNCE_VERSION))
            logger.debug(f"published ANNOUNCE_VERSION to [device/{self.config.serial_number}/request]")

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
        cmd = SEND_GCODE_TEMPLATE
        cmd["print"]["param"] = f"{gcode} \n"
        self.client.publish(f"device/{self.config.serial_number}/request", json.dumps(cmd))
        logger.debug(f"published SEND_GCODE_TEMPLATE to [device/{self.config.serial_number}/request]", extra={"gcode": gcode})

    def print_3mf_file(self, name: str, bed: PlateType, ams: str, bedlevel: Optional[bool] = True, flow: Optional[bool] = True, timelapse: Optional[bool] = False):
        """
        Submits a request to execute the `name`.gcode.3mf file on the printer's SDCard. 

        Parameters
        ----------
        * name : str                         - path and filename to execute minus the `.gcode.3mf` extension
        * bed : PlateType                    - the bambutools.PlateType to use
        * ams : str                          - an `AMS Mapping` that specifies which AMS spools to use (external spool is used if blank)
        * bedlevel :  Optional[bool] = True  - boolean value indicates whether or not the printer should auto-level the bed
        * flow :      Optional[bool] = True  - boolean value indicates if the printer should perform an extrusion flow calibration
        * timelapse : Optional[bool] = False - boolean value indicates if printer should take timelapse photos during the job
        
        Example
        -------
        * `print_3mf_file("/jobs/my_project", "")` - Print the my_project.gcode.3mf file in the SDCard /jobs directory using the external spool with bed leveling and extrusion flow calibration enabled and timelapse disabled
        * `print_3mf_file("/jobs/my_project", "[-1,-1,2,-1]")` - Same as above but use AMS spool #3

        AMS Mapping
        -----------
        * `[0,-1,-1,-1]` - use AMS spool #1 only
        * `[-1,1,-1,-1]` - use AMS spool #2 only
        * `[0,-1,-1,3]`  - use AMS spools #1 and #4
        * `[0,1,2,3]`    - use all 4 AMS spools
        """
        file = PRINT_3MF_FILE
        file["print"]["file"] = f"{name}.gcode.3mf"
        file["print"]["url"] = f"file:///sdcard/{name}.gcode.3mf"
        file["print"]["subtask_name"] = name[name.rindex("/") + 1::] if "/" in name else name
        file["print"]["bed_type"] = bed.name.lower()
        if len(ams) > 2:
            file["print"]["use_ams"] = True
            file["print"]["ams_mapping"] = json.loads(ams)
        else:
            file["print"]["use_ams"] = False
            file["print"]["ams_mapping"] = ""
        file["print"]["bed_leveling"] = bedlevel
        file["print"]["flow_cali"] = flow
        file["print"]["timelapse"] = timelapse
        self.client.publish(f"device/{self.config.serial_number}/request", json.dumps(file))
        logger.debug(f"published PRINT_3MF_FILE to [device/{self.config.serial_number}/request]", extra={"3mf_name": name, "bed": bed, "ams": ams})

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

    def get_sdcard_3mf_files(self) -> {}:
        """
        Returns a `dict` (json document) of all `.gcode.3mf` files on the printer's SD card. 
        The private class level `_sdcard_3mf_files` attribute is also populated.
        
        Usage
        -----
        The return value of this method is very useful for binding to things like a clientside `TreeView`
        """
        def getDirFiles(ftps: IoTFTPSClient, directory: str) -> {}:
            try:
                files = sorted(ftps.list_files_ex(directory))
            except Exception as e:
                return None

            dir = {}

            dir["id"] = directory 
            dir["name"] = directory

            items = []

            for file in files:
                if file[0][:1] == "d":
                    item = {}
                    item = getDirFiles(ftps, directory + ("/" if directory != "/" else "") + file[1])
                    if item.get("children"): items.append(item)
                else:
                    if file[1].lower().endswith(".gcode.3mf"):
                        item = {}
                        item["id"] = dir["id"] + ("/" if dir["id"] != "/" else "") + file[1]
                        item["name"] = file[1]
                        items.append(item)

            if len(items) > 0: dir["children"] = items
            return dir

        ftps = IoTFTPSClient(f"bambu-a1-printer", 990, "bblp", f"42050576", ssl_implicit=True)
        fs = getDirFiles(ftps, "/")
        logger.debug("read 3mf sdcard files", extra={"fs": fs})
        self._sdcard_3mf_files = fs
        return fs


    def get_sdcard_contents(self):
        """
        Returns a `dict` (json document) of ALL files on the printer's SD card. 
        The private class level `_sdcard_contents` attribute is also populated.
        
        Usage
        -----
        The return value of this method is very useful for binding to things like a clientside `TreeView`
        """
        def getDirFiles(ftps: IoTFTPSClient, directory: str) -> {}:
            try:
                files = sorted(ftps.list_files_ex(directory))
            except Exception as e:
                return None

            dir = {}

            dir["id"] = directory 
            dir["name"] = directory

            items = []

            for file in files:
                item = {}
                if file[0][:1] == "d":
                    item = getDirFiles(ftps, directory + ("/" if directory != "/" else "") + file[1])
                else:
                    item["id"] = dir["id"] + ("/" if dir["id"] != "/" else "") + file[1]
                    item["name"] = file[1]
                items.append(item)

            if len(items) > 0: dir["children"] = items
            return dir

        ftps = IoTFTPSClient(f"bambu-a1-printer", 990, "bblp", f"42050576", ssl_implicit=True)
        fs = getDirFiles(ftps, "/")
        logger.debug("read all sdcard files", extra={"fs": fs})
        self._sdcard_contents = fs
        return fs

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
            if isinstance(obj, mqtt.Client):
                return ""
            if str(obj.__class__).replace("<class '", "").replace("'>", "") == "mappingproxy":
                return "bambutools.PrinterState"
            return obj.__dict__
        except Exception as e:
            logger.warn("unable to serialize object", extra={"obj": obj})
            return "not available"

    def _start_watchdog(self): 
        def watchdog_thread(printer):
            try:
                while printer.state != PrinterState.QUIT:
                    if printer.state == PrinterState.CONNECTED and (printer._lastMessageTime is None or printer._lastMessageTime + 15 < time.time()):
                        if printer._lastMessageTime: logger.warn("BambuPrinter watchdog timeout")
                        printer._lastMessageTime = time.time()
                        printer._recent_update = False
                        printer.client.publish(f"device/{printer.config.serial_number}/request", json.dumps(ANNOUNCE_PUSH))
                        printer.client.publish(f"device/{printer.config.serial_number}/request", json.dumps(ANNOUNCE_VERSION))
                    time.sleep(.1)
            except Exception as e:
                logger.exception("an internal exception occurred")
                printer._internalException = e
                if printer.client and printer.client.is_connected(): printer.client.disconnect()

        threading.Thread(target=watchdog_thread, name="bambuprinter-session-watchdog", args=(self,)).start()

    def _on_message(self, message: str):
        logger.debug("_on_message", extra={"bambu_msg": message})

        if "system" in message:
            system = message["system"]

        elif "print" in message:
            status = message["print"]
                    
            if "bed_temper" in status: self._bed_temp = float(status["bed_temper"])
            if "bed_target_temper" in status: self._bed_temp_target = float(status["bed_target_temper"])
            if "nozzle_temper" in status: self._tool_temp = float(status["nozzle_temper"])
            if "nozzle_target_temper" in status: self._tool_temp_target = float(status["nozzle_target_temper"])

            if "fan_gear" in status: self._fan_gear = int(status["fan_gear"])
            if "heatbreak_fan_speed" in status: self._heatbreak_fan_speed = int(status["heatbreak_fan_speed"])
            if "cooling_fan_speed" in status: self._fan_speed = parseFan(int(status["cooling_fan_speed"]))

            if "wifi_signal" in status: self._wifi_signal = status["wifi_signal"] 
            if "lights_report" in status: self._light_state = (status["lights_report"])[0]["mode"]
            if "spd_lvl" in status: self._speed_level = status["spd_lvl"]
            if "gcode_state" in status: self._gcode_state = status["gcode_state"]
            if "gcode_file" in status: self._gcode_file = status["gcode_file"]
            if "print_type" in status: self._print_type = status["print_type"]
            if "mc_percent" in status: self._percent_complete = status["mc_percent"]
            if "mc_remaining_time" in status: self._time_remaining = status["mc_remaining_time"]
            if "total_layer_num" in status: self._layer_count = status["total_layer_num"]
            if "layer_num" in status: self._current_layer = status["layer_num"]

            if "stg_cur" in status: 
                self._current_stage = int(status["stg_cur"])
                self._current_stage_text = parseStage(self._current_stage)

            if "command" in status and status["command"] == "project_file":
                logger.debug("project_file request acknowledged")

            if "ams" in status and "ams" in status["ams"]:
                if status["ams"]["ams_exist_bits"]:
                    self._ams_exists = int(status["ams"]["ams_exist_bits"]) == 1
                    if self._ams_exists:
                        spools = []
                        ams = (status["ams"]["ams"])[0]
                        for tray in ams["tray"]:
                            try:
                                tray_color = hex_to_name("#" + tray["tray_color"][:6])
                            except:
                                try:
                                    tray_color = "#" + tray["tray_color"]
                                except:
                                    tray_color = "N/A"
                            
                            spool = BambuSpool(int(tray["id"]),  tray["tray_id_name"] if "tray_id_name" in tray else "",  tray["tray_type"] if "tray_type" in tray else "", tray["tray_sub_brands"] if "tray_sub_brands" in tray else "", tray_color)
                            spools.append(spool)
                        self._spools = tuple(spools)
                # else: 
                #     self._ams_exists = False

            if "vt_tray" in status:
                tray = status["vt_tray"]
                try:
                    tray_color = hex_to_name("#" + tray["tray_color"][:6])
                except:
                    try:
                        tray_color = "#" + tray["tray_color"]
                    except:
                        tray_color = "N/A"

                spool = BambuSpool(int(tray["id"]), tray["tray_id_name"],  tray["tray_type"], tray["tray_sub_brands"], tray_color)

                if range(len(self.spools), 1, 2): 
                    spools = (spool,)
                else:
                    spools = list(self.spools)
                    spools.append(spool)
                self._spools = tuple(spools)

            tray_tar = None
            tray_now = None

            if "ams" in status and "tray_tar" in status["ams"]:
                tray_tar = int(status["ams"]["tray_tar"])
                if tray_tar != 255: 
                    self._target_spool = int(tray_tar)

            if "ams" in status and "tray_now" in status["ams"]:
                tray_now = int(status["ams"]["tray_now"])
                if tray_now != 255: 
                    if self.active_spool != tray_now: 
                        self._spool_state = f"Loading"
                        self._active_spool = tray_now

            if not tray_tar is None and tray_tar != tray_now: 
                self._spool_state = f"Unloading"
                if not tray_now is None: self._active_spool = tray_now

            if "ams" in status and "tray_pre" in status["ams"]:
                tray_pre = int(status["ams"]["tray_pre"])
                if self.spool_state == "Unloading":
                    self._spool_state = "Unloaded"

            if "ams_status" in status:
                self._ams_status = int(status["ams_status"])
                if self._ams_status == 768:
                    self._spool_state = "Loaded"
                    
        elif "info" in message and "result" in message["info"] and message["info"]["result"] == "success": 
            self._recent_update = True
            info = message["info"]
            for module in info["module"]:
                if "ota" in module["name"]: 
                    self.config.serial_number = module["sn"]
                    self.config.firmware_version = module["sw_ver"]
                if "ams" in module["name"]:
                    self.config.ams_firmware_version = module["sw_ver"]
        else:
            logger.warn("unknown message type received")
            
        if self.on_update: self.on_update(self)

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
    def gcode_file(self):
        return self._gcode_file
    @gcode_file.setter 
    def gcode_file(self, value):
        self._gcode_file = value

    @property 
    def print_type(self):
        return self._print_type

    @property 
    def percent_complete(self):
        return self._percent_complete

    @property 
    def time_remaining(self):
        return self._time_remaining

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
    def internalException(self):
        return self._internalException

    @property
    def cached_sd_card_contents(self):
        return self._sdcard_contents

    @property
    def cached_sd_card_3mf_files(self):
        return self._sdcard_3mf_files

def setup_logging():
    config_file = os.path.dirname(os.path.realpath(__file__)) + "/bambuprinterlogger.json"
    with open(config_file) as f_in:
        config = json.load(f_in)

    logging.config.dictConfig(config)
    queue_handler = logging.getHandlerByName("queue_handler")
    if queue_handler is not None:
        queue_handler.listener.start()
        atexit.register(queue_handler.listener.stop)