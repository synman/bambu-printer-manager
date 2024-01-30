import json
from webcolors import hex_to_name
import paho.mqtt.client as mqtt
import threading
import ssl
import time

from .bambucommands import *
from .bambuspool import BambuSpool
from .bambutools import PrinterState
from .bambutools import parseStage, parseFan
from .bambuconfig import BambuConfig

import os
import atexit
import logging.config
import logging.handlers

logger = logging.getLogger("bambuprinter")

class BambuPrinter:
    def __init__(self, config=BambuConfig()):
        setup_logging()

        self._internalException = None
        self._lastMessageTime = None

        self._config = config
        self._state = PrinterState

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

        self._light_state = "N/A"
        self._wifi_signal = "N/A"
        self._speed_level = 0

        self._gcode_state = "N/A"
        self._gcode_file = "N/A"
        self._print_type = "N/A"
        self._percent_complete = 0
        self._time_remaining = 0
        self._layer_count = 0
        self._current_layer = 0
        
        self._current_stage = 0
        self._current_stage_text = "N/A"

        self._spools = ()
        self._target_spool = 255
        self._active_spool = 255
        self._spool_state = "N/A"
        self._ams_status = None

    def start_session(self):
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
            if self._lastMessageTime: self._lastMessageTime = time.time()
            self._on_message(json.loads(msg.payload.decode("utf-8")))
        def loop_forever(printer):
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

        self.client.connect(self.config.hostname, self.config.mqtt_port, 60)
        threading.Thread(target=loop_forever, name="bambuprinter-session", args=(self,)).start()

        self._start_watchdog()

    def pause_session(self):
        if self.state != PrinterState.PAUSED:
            self.client.unsubscribe(f"device/{self.config.serial_number}/report")
            logger.debug(f"unsubscribed from [device/{self.config.serial_number}/report]")
            self.state = PrinterState.PAUSED

    def resume_session(self):
        if self.client and self.client.is_connected() and self.state == PrinterState.PAUSED:
            self.client.subscribe(f"device/{self.config.serial_number}/report")
            logger.debug(f"subscribed to [device/{self.config.serial_number}/report]")
            self._lastMessageTime = time.time()
            self.state = PrinterState.CONNECTED
            return
        self.state = PrinterState.QUIT

    def quit(self):
        if self.client and self.client.is_connected():
            self.client.disconnect()
            while self.state != PrinterState.QUIT:
                time.sleep(.1)
            logger.debug("mqtt client was connected")
        else:
            self.state == PrinterState.QUIT
            logger.debug("mqtt client was already disconnected")

    def refresh(self):
        if self.state == PrinterState.CONNECTED:
            self.client.publish(f"device/{self.config.serial_number}/request", json.dumps(ANNOUNCE_PUSH))
            logger.debug(f"published ANNOUNCE_PUSH to [device/{self.config.serial_number}/request]")
            self.client.publish(f"device/{self.config.serial_number}/request", json.dumps(ANNOUNCE_VERSION))
            logger.debug(f"published ANNOUNCE_VERSION to [device/{self.config.serial_number}/request]")

    def unload_filament(self):
        self.client.publish(f"device/{self.config.serial_number}/request", json.dumps(UNLOAD_FILAMENT))
        logger.debug(f"published UNLOAD_FILAMENT to [device/{self.config.serial_number}/request]")

    def load_filament(self, slot):
        msg = AMS_FILAMENT_CHANGE
        msg["print"]["target"] = int(slot)
        self.client.publish(f"device/{self.config.serial_number}/request", json.dumps(msg))
        logger.debug(f"published AMS_FILAMENT_CHANGE to [device/{self.config.serial_number}/request]", extra={"target": slot})

    def send_gcode(self, gcode):
        cmd = SEND_GCODE_TEMPLATE
        cmd["print"]["param"] = f"{gcode} \n"
        self.client.publish(f"device/{self.config.serial_number}/request", json.dumps(cmd))
        logger.debug(f"published SEND_GCODE_TEMPLATE to [device/{self.config.serial_number}/request]", extra={"gcode": gcode})

    def print_3mf_file(self, name, bed, ams, bedlevel=True, flow=True, timelapse=False):
        file = PRINT_3MF_FILE
        file["print"]["file"] = f"{name}.gcode.3mf"
        file["print"]["url"] = f"file:///sdcard/{name}.gcode.3mf"
        file["print"]["subtask_name"] = name[name.rindex("/") + 1::]
        if bed == "0":
            file["print"]["bed_type"] = "auto"
        elif bed == "1":
            file["print"]["bed_type"] = "hot_plate"
        elif bed == "2":
            file["print"]["bed_type"] = "textured_plate"
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
        self.client.publish(f"device/{self.config.serial_number}/request", json.dumps(STOP_PRINT))
        logger.debug(f"published STOP_PRINT to [device/{self.config.serial_number}/request]")

    def pause_printing(self):
        self.client.publish(f"device/{self.config.serial_number}/request", json.dumps(PAUSE_PRINT))
        logger.debug(f"published PAUSE_PRINT to [device/{self.config.serial_number}/request]")

    def resume_printing(self):
        self.client.publish(f"device/{self.config.serial_number}/request", json.dumps(RESUME_PRINT))
        logger.debug(f"published RESUME_PRINT to [device/{self.config.serial_number}/request]")


    def toJson(self):
        response = json.dumps(self, default=self.jsonSerializer, indent=4, sort_keys=True)
        return json.loads(response)

    def jsonSerializer(self, obj):
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
                        printer.client.publish(f"device/{printer.config.serial_number}/request", json.dumps(ANNOUNCE_PUSH))
                        printer.client.publish(f"device/{printer.config.serial_number}/request", json.dumps(ANNOUNCE_VERSION))
                        printer._lastMessageTime = time.time()
                    time.sleep(.1)
            except Exception as e:
                logger.exception("an internal exception occurred")
                printer._internalException = e
                if printer.client and printer.client.is_connected(): printer.client.disconnect()

        threading.Thread(target=watchdog_thread, name="bambuprinter-session-watchdog", args=(self,)).start()

    def _on_message(self, message):
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
                print(json.dumps(message, indent=4, sort_keys=True).replace("\n", "\r\n"))

            if "ams" in status and "ams" in status["ams"]:
                spools = []
                ams = (status["ams"]["ams"])[0]
                # print(json.dumps(status, indent=4, sort_keys=True).replace("\n", "\r\n"))
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
            info = message["info"]
            for module in info["module"]:
                if "ota" in module["name"]: 
                    self.config.serial_number = module["sn"]
                    self.config.firmware_version = module["sw_ver"]
                if "ams" in module["name"]:
                    self.config.ams_firmware_version = module["sw_ver"]
        else:
            print(json.dumps(message, indent=4, sort_keys=True).replace("\n", "\r\n"))
            
        if self.on_update: self.on_update(self)

        logger.debug("message processed", extra={"bambu_msg": message})
        if self.config.verbose:
            print("\r" + json.dumps(message, indent=4, sort_keys=True).replace("\n", "\r\n") + "\r")


    @property 
    def config(self):
        return self._config
    @config.setter 
    def config(self, value):
        self._config = value

    @property 
    def state(self):
        return self._state
    @state.setter 
    def state(self, value):
        self._state = value

    @property 
    def client(self):
        return self._client
    @client.setter 
    def client(self, value):
        self._client = value

    @property 
    def on_update(self):
        return self._on_update
    @on_update.setter 
    def on_update(self, value):
        self._on_update = value

    @property 
    def bed_temp(self):
        return self._bed_temp

    @property 
    def bed_temp_target(self):
        return self._bed_temp_target
    @bed_temp_target.setter 
    def bed_temp_target(self, value):
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
    def tool_temp_target(self, value):
        gcode = SEND_GCODE_TEMPLATE
        gcode["print"]["param"] = f"M104 S{value}\n"
        self.client.publish(f"device/{self.config.serial_number}/request", json.dumps(gcode))

    @property 
    def chamber_temp(self):
        return self._chamber_temp

    @property 
    def chamber_temp_target(self):
        return self._chamber_temp_target
    @chamber_temp.setter 
    def chamber_temp_target(self, value):
        self._chamber_temp_target = value

    @property 
    def fan_speed(self):
        return self._fan_speed

    @property 
    def fan_speed_target(self):
        return self._fan_speed_target
    @fan_speed_target.setter 
    def fan_speed_target(self, value):
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
    def light_state(self, value):
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
    def speed_level(self, value):
        cmd = SPEED_PROFILE_TEMPLATE
        cmd["print"]["param"] = str(value)
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


def setup_logging():
    config_file = os.path.dirname(os.path.realpath(__file__)) + "/bambuprinterlogger.json"
    with open(config_file) as f_in:
        config = json.load(f_in)

    logging.config.dictConfig(config)
    queue_handler = logging.getHandlerByName("queue_handler")
    if queue_handler is not None:
        queue_handler.listener.start()
        atexit.register(queue_handler.listener.stop)