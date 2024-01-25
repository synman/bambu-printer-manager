ANNOUNCE_PUSH =             {
                                "pushing":{
                                    "command":"pushall",
                                    "push_target":1,
                                    "sequence_id":"0",
                                    "version":1
                                }
                            }

ANNOUNCE_VERSION =          {
                                "info":{
                                    "command":"get_version",
                                    "sequence_id":"0"
                                }
                            }

CHAMBER_LIGHT_TOGGLE =      {
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

SPEED_PROFILE_TEMPLATE =    {
                                "print": {
                                    "sequence_id": "0",
                                    "command": "print_speed", 
                                    "param": "2"
                                }
                            }

PAUSE_PRINT =               {
                                "print": {
                                    "sequence_id": "0", 
                                    "command": "pause"
                                }
                            }

RESUME_PRINT =              {
                                "print": {
                                    "sequence_id": "0", 
                                    "command": "resume"
                                }
                            }

STOP_PRINT =                {
                                    "print": {
                                        "sequence_id": "0", 
                                        "command": "stop"
                                    }
                            }

SEND_GCODE_TEMPLATE =       {
                                "print": {
                                    "sequence_id": "0", 
                                    "command": "gcode_line", 
                                    "param": ""
                                }
                            }

MOVE_RIGHT =                {
                                "print": {
                                    "sequence_id": "0", 
                                    "command": "gcode_line", 
                                    "param": "G91\nG1 X100 F3600\n"
                                }
                            }

MOVE_LEFT =                 {
                                "print": {
                                    "sequence_id": "0", 
                                    "command": "gcode_line", 
                                    "param": "G91\nG1 X-100 F3600\n"
                                }
                            }

UNLOAD_FILAMENT =           {
                                "print": {
                                    "sequence_id": "0",
                                    "command": "unload_filament"
                                }
                            }

AMS_FILAMENT_CHANGE =       {
                                "print": {
                                    "sequence_id": "0",
                                    "command": "ams_change_filament",
                                    "target": 0, 
                                    "curr_temp": 250, 
                                    "tar_temp": 250
                                }
                            }

PRINT_3MF_FILE =            {
                                "print": {
                                    "ams_mapping": [],
                                    "bed_leveling": True,
                                    "bed_type": "hot_plate",
                                    "command": "project_file",
                                    "file": "Oreo.gcode.3mf",
                                    "flow_cali": True,
                                    "layer_inspect": True,
                                    "md5": "",
                                    "param": "Metadata/plate_1.gcode",
                                    "profile_id": "0",
                                    "project_id": "0",
                                    "reason": "success",
                                    "result": "success",
                                    "sequence_id": "0",
                                    "subtask_id": "0",
                                    "subtask_name": "Oreo",
                                    "task_id": "0",
                                    "timelapse": False,
                                    "url": "file:///sdcard/Oreo.gcode.3mf",
                                    "use_ams": False,
                                    "vibration_cali": False
                                }
                            }

# X1 only currently
GET_ACCESSORIES = {"system": {"sequence_id": "0", "command": "get_accessories", "accessory_type": "none"}}