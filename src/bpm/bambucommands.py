"""
`bambucommands` contains all the internal command structures that are used by `BambuPrinter` to interact 
with your printer.  They are not documented but can be found [here](https://github.com/synman/bambu-printer-manager/blob/main/src/bpm/bambucommands.py).
"""
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


X1_FLOWRATE_CALI_RESULTS =  {
                                "print": {
                                    "sequence_id": "0", 
                                    "command": "flowrate_get_result"
                                }
                            }

X1_EXTRUSION_CALI_RESULTS = {
                                "print": {
                                    "sequence_id": "0", 
                                    "command": "extrusion_cali_get_result"
                                }
                            }

EXTRUSION_CALI           = {
                                "print": {
                                    "sequence_id": "0", 
                                    "command": "extrusion_cali",
                                    "tray_id": 0,
                                    "nozzle_temp": 250,
                                    "bed_temp": 65,
                                    "max_volumetric_speed": 22,
                                }
                            }

EXTRUSION_CALI_SET        = {
                                "print": {
                                    "sequence_id": "0", 
                                    "command": "extrusion_cali_set",
                                    "tray_id": 0,
                                    "k_value": 0.020,
                                }
                            }

PRINT_OPTION_COMMAND =      {
                                "print": {
                                    "command":"print_option",
                                    "sequence_id":"0"
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

AMS_FILAMENT_SETTING =      {
                              "print": {
                                "command": "ams_filament_setting",
                                "ams_id": 255,
                                "tray_id": 254,
                                "tray_info_idx": ""
                              }
                            }

AMS_USER_SETTING =          {
                              "print": {
                                "ams_id": 0,
                                "command": "ams_user_setting",
                                "sequence_id": "0",
                                "calibrate_remain_flag": True,
                                "startup_read_option": True,
                                "tray_read_option": True
                              }
                            }

AMS_CONTROL =               {
                              "print": {
                                  "sequence_id": "0",
                                  "command": "ams_control",
                                  "param": "resume" # "resume", "reset" or "pause"
                              }
                            }

PRINT_3MF_FILE =            {
                                "print": {
                                    "command": "project_file",
                                    "sequence_id": "0",
                                    "use_ams": False,
                                    "ams_mapping": "",
                                    "bed_type": "auto",
                                    "url": "file:///sdcard/Oreo.gcode.3mf",
                                    "file": "Oreo.gcode.3mf",
                                    "param": "Metadata/plate_#.gcode",
                                    "md5": "",
                                    "profile_id": "0",
                                    "project_id": "0",
                                    "subtask_id": "0",
                                    "subtask_name": "Oreo",
                                    "task_id": "0",
                                    "timelapse": False,
                                    "bed_leveling": True,
                                    "flow_cali": True,
                                    "layer_inspect": True,
                                    "vibration_cali": True
                                }
                            }

SKIP_OBJECTS =              {
                              "print": {
                                "sequence_id": "0",
                                "command": "skip_objects",
                                "obj_list": [],
                              }
                            }

SET_ACCESSORIES =           {
                              "print": {
                                "accessory_type": "nozzle",
                                "command": "set_accessories",
                                "nozzle_diameter": 0.4000000059604645,
                                "nozzle_type": "hardened_steel",
                                "sequence_id": "0",
                              }
                            }

XCAM_CONTROL_SET =          {
                              "xcam": {
                                "command": "xcam_control_set",
                                "control": True,
                                "enable": True,
                                "module_name": "buildplate_marker_detector",
                                "print_halt": True,
                                "sequence_id": "0"
                            }
    }

# X1 only currently
GET_ACCESSORIES = {"system": {"sequence_id": "0", "command": "get_accessories", "accessory_type": "none"}}

# 
# https://e.bambulab.com/query.php?lang=en
# 
HMS_STATUS = {
  "result": 0,
  "t": 1761224255,
  "ver": 202510221200,
  "data": {
    "device_error": {
      "ver": 202510221200,
      "en": [
        {
          "ecode": "0582409C",
          "intro": "The firmware of AMS-HT C does not match the printer; the device cannot continue working. Please update it on the \"Firmware\" page."
        },
        {
          "ecode": "0584409C",
          "intro": "The firmware of AMS-HT E does not match the printer; the device cannot continue working. Please update it on the \"Firmware\" page."
        },
        {
          "ecode": "0581409C",
          "intro": "The firmware of AMS-HT B does not match the printer; the device cannot continue working. Please update it on the \"Firmware\" page."
        },
        {
          "ecode": "0586409C",
          "intro": "The firmware of AMS-HT G does not match the printer; the device cannot continue working. Please update it on the \"Firmware\" page."
        },
        {
          "ecode": "0585409C",
          "intro": "The firmware of AMS-HT F does not match the printer; the device cannot continue working. Please update it on the \"Firmware\" page."
        },
        {
          "ecode": "0503409D",
          "intro": "The firmware of AMS D does not match the printer; the device cannot continue working. Please update it on the \"Firmware\" page."
        },
        {
          "ecode": "0580409C",
          "intro": "The firmware of AMS-HT A does not match the printer; the device cannot continue working. Please update it on the \"Firmware\" page."
        },
        {
          "ecode": "0583409C",
          "intro": "The firmware of AMS-HT D does not match the printer; the device cannot continue working. Please update it on the \"Firmware\" page."
        },
        {
          "ecode": "0501409D",
          "intro": "The firmware of AMS B does not match the printer; the device cannot continue working. Please update it on the \"Firmware\" page."
        },
        {
          "ecode": "0C00402C",
          "intro": "Device data link error. Please reboot the printer"
        },
        {
          "ecode": "05004031",
          "intro": "The accessory firmware does not match the printer. Please update it on the \"Firmware\" page."
        },
        {
          "ecode": "07FF8007",
          "intro": "Please observe the nozzle. If the filament has been extruded, select \"Done\"; if it has not, please push the filament forward slightly, and then select \"Retry\"."
        },
        {
          "ecode": "05004033",
          "intro": "The AMS firmware does not match the printer. Please update it on the \"Firmware\" page."
        },
        {
          "ecode": "05004016",
          "intro": "The MicroSD Card is write-protected. Please replace the MicroSD Card."
        },
        {
          "ecode": "0500403C",
          "intro": "The current nozzle setting does not match the slicing file. Continuing to print may affect print quality. It is recommended to re-slice before starting the print."
        },
        {
          "ecode": "0502C024",
          "intro": "The flow dynamic calibration records have exceeded the storage limit. Please delete some historical records in the slicer software before adding new calibration data."
        },
        {
          "ecode": "07024025",
          "intro": "Failed to read the filament information."
        },
        {
          "ecode": "0500803C",
          "intro": "The current nozzle setting does not match the slicing file. Continuing to print may affect print quality. It is recommended to re-slice before starting the print."
        },
        {
          "ecode": "0300400D",
          "intro": "Resume failed after power loss."
        },
        {
          "ecode": "0500400E",
          "intro": "Printing was cancelled."
        },
        {
          "ecode": "0502C014",
          "intro": "The AMS Remaining Filament Estimation is enabled by default and cannot be disabled."
        },
        {
          "ecode": "05844096",
          "intro": "The device cannot detect AMS-HT F. Please reconnect the AMS-HT cable or restart the printer."
        },
        {
          "ecode": "05824096",
          "intro": "The device cannot detect AMS-HT C. Please reconnect the AMS-HT cable or restart the printer."
        },
        {
          "ecode": "05864096",
          "intro": "The device cannot detect AMS-HT G. Please reconnect the AMS-HT cable or restart the printer."
        },
        {
          "ecode": "05014098",
          "intro": "The device cannot detect AMS B. Please reconnect the AMS cable or restart the printer."
        },
        {
          "ecode": "05854096",
          "intro": "The device cannot detect AMS-HT E. Please reconnect the AMS-HT cable or restart the printer."
        },
        {
          "ecode": "05874096",
          "intro": "The device cannot detect AMS-HT H. Please reconnect the AMS-HT cable or restart the printer."
        },
        {
          "ecode": "05834096",
          "intro": "The device cannot detect AMS-HT D. Please reconnect the AMS-HT cable or restart the printer."
        },
        {
          "ecode": "05814096",
          "intro": "The device cannot detect AMS-HT B. Please reconnect the AMS-HT cable or restart the printer."
        },
        {
          "ecode": "05004098",
          "intro": "The device cannot detect AMS A. Please reconnect the AMS cable or restart the printer."
        },
        {
          "ecode": "05024098",
          "intro": "The device cannot detect AMS C. Please reconnect the AMS cable or restart the printer."
        },
        {
          "ecode": "05034098",
          "intro": "The device cannot detect AMS D. Please reconnect the AMS cable or restart the printer."
        },
        {
          "ecode": "05804096",
          "intro": "The device cannot detect AMS-HT A. Please reconnect the AMS-HT cable or restart the printer."
        },
        {
          "ecode": "0500C011",
          "intro": ""
        },
        {
          "ecode": "0502400C",
          "intro": ""
        },
        {
          "ecode": "05024009",
          "intro": ""
        },
        {
          "ecode": "05024007",
          "intro": ""
        },
        {
          "ecode": "0C008002",
          "intro": ""
        },
        {
          "ecode": "0502400B",
          "intro": ""
        },
        {
          "ecode": "05024008",
          "intro": ""
        },
        {
          "ecode": "0502400A",
          "intro": ""
        },
        {
          "ecode": "058440A2",
          "intro": "AMS-HT E communication is abnormal. Please reconnect the module cable or restart the printer."
        },
        {
          "ecode": "058640A2",
          "intro": "AMS-HT G communication is abnormal. Please reconnect the module cable or restart the printer."
        },
        {
          "ecode": "058740A2",
          "intro": "AMS-HT H communication is abnormal. Please reconnect the module cable or restart the printer."
        },
        {
          "ecode": "050240A3",
          "intro": "AMS(or AMS lite) C communication is abnormal. Please reconnect the module cable or restart the printer."
        },
        {
          "ecode": "050040A3",
          "intro": "AMS(or AMS lite) A communication is abnormal. Please reconnect the module cable or restart the printer."
        },
        {
          "ecode": "050340A3",
          "intro": "AMS(or AMS lite) D communication is abnormal. Please reconnect the module cable or restart the printer."
        },
        {
          "ecode": "058140A2",
          "intro": "AMS-HT B communication is abnormal. Please reconnect the module cable or restart the printer."
        },
        {
          "ecode": "058040A2",
          "intro": "AMS-HT A communication is abnormal. Please reconnect the module cable or restart the printer."
        },
        {
          "ecode": "058340A2",
          "intro": "AMS-HT D communication is abnormal. Please reconnect the module cable or restart the printer."
        },
        {
          "ecode": "05008041",
          "intro": "The filament in hotend is too cold. Extrusion may damage the extruder. Still feeding in/out the filament?"
        },
        {
          "ecode": "05008040",
          "intro": "Toolhead front cover is detached. Moving the toolhead may damage the printer. Do you want to continue?"
        },
        {
          "ecode": "058540A2",
          "intro": "AMS-HT F communication is abnormal. Please reconnect the module cable or restart the printer."
        },
        {
          "ecode": "058240A2",
          "intro": "AMS-HT C communication is abnormal. Please reconnect the module cable or restart the printer."
        },
        {
          "ecode": "050140A3",
          "intro": "AMS(or AMS lite) B communication is abnormal. Please reconnect the module cable or restart the printer."
        },
        {
          "ecode": "18018023",
          "intro": "AMS-HT B cooling failed. The ambient temperature may be too high. Please operate the device in a suitable environment."
        },
        {
          "ecode": "07048023",
          "intro": "AMS E cooling failed. The ambient temperature may be too high. Please operate the device in a suitable environment."
        },
        {
          "ecode": "07038023",
          "intro": "AMS D cooling failed. The ambient temperature may be too high. Please operate the device in a suitable environment."
        },
        {
          "ecode": "07008023",
          "intro": "AMS A cooling failed. The ambient temperature may be too high. Please operate the device in a suitable environment."
        },
        {
          "ecode": "18028023",
          "intro": "AMS-HT C cooling failed. The ambient temperature may be too high. Please operate the device in a suitable environment."
        },
        {
          "ecode": "07068023",
          "intro": "AMS G cooling failed. The ambient temperature may be too high. Please operate the device in a suitable environment."
        },
        {
          "ecode": "18068023",
          "intro": "AMS-HT G cooling failed. The ambient temperature may be too high. Please operate the device in a suitable environment."
        },
        {
          "ecode": "18038023",
          "intro": "AMS-HT D cooling failed. The ambient temperature may be too high. Please operate the device in a suitable environment."
        },
        {
          "ecode": "18058023",
          "intro": "AMS-HT F cooling failed. The ambient temperature may be too high. Please operate the device in a suitable environment."
        },
        {
          "ecode": "0500400F",
          "intro": "AMS is initializing and cannot be upgraded at the moment. Please try again later."
        },
        {
          "ecode": "05004010",
          "intro": "AMS is drying and cannot be upgraded at the moment. Please try again later."
        },
        {
          "ecode": "05004011",
          "intro": "The printer is loading or unloading filament and cannot be upgraded at the moment. Please try again later."
        },
        {
          "ecode": "18048023",
          "intro": "AMS-HT E cooling failed. The ambient temperature may be too high. Please operate the device in a suitable environment."
        },
        {
          "ecode": "07058023",
          "intro": "AMS F cooling failed. The ambient temperature may be too high. Please operate the device in a suitable environment."
        },
        {
          "ecode": "18008023",
          "intro": "AMS-HT A cooling failed. The ambient temperature may be too high. Please operate the device in a suitable environment."
        },
        {
          "ecode": "07028023",
          "intro": "AMS C cooling failed. The ambient temperature may be too high. Please operate the device in a suitable environment."
        },
        {
          "ecode": "07018023",
          "intro": "AMS B cooling failed. The ambient temperature may be too high. Please operate the device in a suitable environment."
        },
        {
          "ecode": "18078023",
          "intro": "AMS-HT H cooling failed. The ambient temperature may be too high. Please operate the device in a suitable environment."
        },
        {
          "ecode": "07078023",
          "intro": "AMS H cooling failed. The ambient temperature may be too high. Please operate the device in a suitable environment."
        },
        {
          "ecode": "05004012",
          "intro": "The device is printing and cannot be upgraded at the moment. Please try again later."
        },
        {
          "ecode": "05004013",
          "intro": "AMS is in operation and cannot be upgraded at the moment. Please try again when it is idle."
        },
        {
          "ecode": "05004030",
          "intro": "The device is currently upgrading. Please try again when it is idle."
        },
        {
          "ecode": "05004040",
          "intro": "The printer has reached its power limit. Please connect a dedicated power adapter to this AMS to enable drying."
        },
        {
          "ecode": "05004041",
          "intro": "The AMS drying cannot be started during printing."
        },
        {
          "ecode": "05004042",
          "intro": "Due to power limitations, starting AMS drying will pause current operations such as nozzle heating and fan running. Do you want to proceed with drying?"
        },
        {
          "ecode": "03004014",
          "intro": "Homing Z axis failed: temperature control abnormality."
        },
        {
          "ecode": "18078005",
          "intro": "The AMS-HT failed to send out filament. You can clip the end of your filament flat, and reinsert. If this message persists, please check the PTFE tubes in AMS for any signs of wear and tear."
        },
        {
          "ecode": "18058004",
          "intro": "AMS-HT failed to pull back filament. This could be due to a stuck spool or the end of the filament being stuck in the path."
        },
        {
          "ecode": "05004007",
          "intro": "The device requires a repair upgrade, and printing is currently unavailable."
        },
        {
          "ecode": "18048005",
          "intro": "The AMS-HT failed to send out filament. You can clip the end of your filament flat, and reinsert. If this message persists, please check the PTFE tubes in AMS for any signs of wear and tear."
        },
        {
          "ecode": "18038004",
          "intro": "AMS-HT failed to pull back filament. This could be due to a stuck spool or the end of the filament being stuck in the path."
        },
        {
          "ecode": "18068005",
          "intro": "The AMS-HT failed to send out filament. You can clip the end of your filament flat, and reinsert. If this message persists, please check the PTFE tubes in AMS for any signs of wear and tear."
        },
        {
          "ecode": "18048004",
          "intro": "AMS-HT failed to pull back filament. This could be due to a stuck spool or the end of the filament being stuck in the path."
        },
        {
          "ecode": "18068004",
          "intro": "AMS-HT failed to pull back filament. This could be due to a stuck spool or the end of the filament being stuck in the path."
        },
        {
          "ecode": "18038005",
          "intro": "The AMS-HT failed to send out filament. You can clip the end of your filament flat, and reinsert. If this message persists, please check the PTFE tubes in AMS for any signs of wear and tear."
        },
        {
          "ecode": "18078004",
          "intro": "AMS-HT failed to pull back filament. This could be due to a stuck spool or the end of the filament being stuck in the path."
        },
        {
          "ecode": "18028005",
          "intro": "The AMS-HT failed to send out filament. You can clip the end of your filament flat, and reinsert. If this message persists, please check the PTFE tubes in AMS for any signs of wear and tear."
        },
        {
          "ecode": "18018006",
          "intro": "Unable to feed filament into the extruder. This could be due to an entangled filament or a stuck spool. If not, please check if the AMS-HT PTFE tube is connected."
        },
        {
          "ecode": "18008006",
          "intro": "Unable to feed filament into the extruder. This could be due to an entangled filament or a stuck spool. If not, please check if the AMS-HT PTFE tube is connected."
        },
        {
          "ecode": "18078006",
          "intro": "Unable to feed filament into the extruder. This could be due to an entangled filament or a stuck spool. If not, please check if the AMS-HT PTFE tube is connected."
        },
        {
          "ecode": "18048006",
          "intro": "Unable to feed filament into the extruder. This could be due to an entangled filament or a stuck spool. If not, please check if the AMS-HT PTFE tube is connected."
        },
        {
          "ecode": "18058006",
          "intro": "Unable to feed filament into the extruder. This could be due to an entangled filament or a stuck spool. If not, please check if the AMS-HT PTFE tube is connected."
        },
        {
          "ecode": "18038006",
          "intro": "Unable to feed filament into the extruder. This could be due to an entangled filament or a stuck spool. If not, please check if the AMS-HT PTFE tube is connected."
        },
        {
          "ecode": "18068006",
          "intro": "Unable to feed filament into the extruder. This could be due to an entangled filament or a stuck spool. If not, please check if the AMS-HT PTFE tube is connected."
        },
        {
          "ecode": "18018004",
          "intro": "AMS-HT failed to pull back filament. This could be due to a stuck spool or the end of the filament being stuck in the path."
        },
        {
          "ecode": "18008004",
          "intro": "AMS-HT failed to pull back filament. This could be due to a stuck spool or the end of the filament being stuck in the path."
        },
        {
          "ecode": "18058005",
          "intro": "The AMS-HT failed to send out filament. You can clip the end of your filament flat, and reinsert. If this message persists, please check the PTFE tubes in AMS for any signs of wear and tear."
        },
        {
          "ecode": "18028004",
          "intro": "AMS-HT failed to pull back filament. This could be due to a stuck spool or the end of the filament being stuck in the path."
        },
        {
          "ecode": "18008005",
          "intro": "The AMS-HT failed to send out filament. You can clip the end of your filament flat, and reinsert. If this message persists, please check the PTFE tubes in AMS for any signs of wear and tear."
        },
        {
          "ecode": "18018005",
          "intro": "The AMS-HT failed to send out filament. You can clip the end of your filament flat, and reinsert. If this message persists, please check the PTFE tubes in AMS for any signs of wear and tear."
        },
        {
          "ecode": "18028006",
          "intro": "Unable to feed filament into the extruder. This could be due to an entangled filament or a stuck spool. If not, please check if the AMS-HT PTFE tube is connected."
        },
        {
          "ecode": "07048003",
          "intro": "Failed to pull out the filament from the extruder. This might be caused by clogged extruder or filament broken inside the extruder."
        },
        {
          "ecode": "07068004",
          "intro": "AMS failed to pull back filament. This could be due to a stuck spool or the end of the filament being stuck in the path."
        },
        {
          "ecode": "07FF8005",
          "intro": "Failed to feed the filament outside the AMS. Please clip the end of the filament flat and check to see if the spool is stuck."
        },
        {
          "ecode": "07048004",
          "intro": "AMS failed to pull back filament. This could be due to a stuck spool or the end of the filament being stuck in the path."
        },
        {
          "ecode": "18008003",
          "intro": "Failed to pull out the filament from the extruder. This might be caused by clogged extruder or filament broken inside the extruder."
        },
        {
          "ecode": "18058003",
          "intro": "Failed to pull out the filament from the extruder. This might be caused by clogged extruder or filament broken inside the extruder."
        },
        {
          "ecode": "07068003",
          "intro": "Failed to pull out the filament from the extruder. This might be caused by clogged extruder or filament broken inside the extruder."
        },
        {
          "ecode": "07018005",
          "intro": "The AMS failed to send out filament. You can clip the end of your filament flat, and reinsert. If this message persists, please check the PTFE tubes in AMS for any signs of wear and tear."
        },
        {
          "ecode": "18038003",
          "intro": "Failed to pull out the filament from the extruder. This might be caused by clogged extruder or filament broken inside the extruder."
        },
        {
          "ecode": "07018003",
          "intro": "Failed to pull out the filament from the extruder. This might be caused by clogged extruder or filament broken inside the extruder."
        },
        {
          "ecode": "07038004",
          "intro": "AMS failed to pull back filament. This could be due to a stuck spool or the end of the filament being stuck in the path."
        },
        {
          "ecode": "07008003",
          "intro": "Failed to pull out the filament from the extruder. This might be caused by clogged extruder or filament broken inside the extruder."
        },
        {
          "ecode": "07058003",
          "intro": "Failed to pull out the filament from the extruder. This might be caused by clogged extruder or filament broken inside the extruder."
        },
        {
          "ecode": "18028003",
          "intro": "Failed to pull out the filament from the extruder. This might be caused by clogged extruder or filament broken inside the extruder."
        },
        {
          "ecode": "07068005",
          "intro": "The AMS failed to send out filament. You can clip the end of your filament flat, and reinsert. If this message persists, please check the PTFE tubes in AMS for any signs of wear and tear."
        },
        {
          "ecode": "07008004",
          "intro": "AMS failed to pull back filament. This could be due to a stuck spool or the end of the filament being stuck in the path."
        },
        {
          "ecode": "07078003",
          "intro": "Failed to pull out the filament from the extruder. This might be caused by clogged extruder or filament broken inside the extruder."
        },
        {
          "ecode": "18FF8005",
          "intro": "Failed to feed the filament outside the AMS-HT. Please clip the end of the filament flat and check to see if the spool is stuck."
        },
        {
          "ecode": "07028004",
          "intro": "AMS failed to pull back filament. This could be due to a stuck spool or the end of the filament being stuck in the path."
        },
        {
          "ecode": "07058005",
          "intro": "The AMS failed to send out filament. You can clip the end of your filament flat, and reinsert. If this message persists, please check the PTFE tubes in AMS for any signs of wear and tear."
        },
        {
          "ecode": "07048005",
          "intro": "The AMS failed to send out filament. You can clip the end of your filament flat, and reinsert. If this message persists, please check the PTFE tubes in AMS for any signs of wear and tear."
        },
        {
          "ecode": "07028003",
          "intro": "Failed to pull out the filament from the extruder. This might be caused by clogged extruder or filament broken inside the extruder."
        },
        {
          "ecode": "18068003",
          "intro": "Failed to pull out the filament from the extruder. This might be caused by clogged extruder or filament broken inside the extruder."
        },
        {
          "ecode": "07018004",
          "intro": "AMS failed to pull back filament. This could be due to a stuck spool or the end of the filament being stuck in the path."
        },
        {
          "ecode": "07008005",
          "intro": "The AMS failed to send out filament. You can clip the end of your filament flat, and reinsert. If this message persists, please check the PTFE tubes in AMS for any signs of wear and tear."
        },
        {
          "ecode": "07078005",
          "intro": "The AMS failed to send out filament. You can clip the end of your filament flat, and reinsert. If this message persists, please check the PTFE tubes in AMS for any signs of wear and tear."
        },
        {
          "ecode": "07078004",
          "intro": "AMS failed to pull back filament. This could be due to a stuck spool or the end of the filament being stuck in the path."
        },
        {
          "ecode": "07058004",
          "intro": "AMS failed to pull back filament. This could be due to a stuck spool or the end of the filament being stuck in the path."
        },
        {
          "ecode": "18078003",
          "intro": "Failed to pull out the filament from the extruder. This might be caused by clogged extruder or filament broken inside the extruder."
        },
        {
          "ecode": "07038005",
          "intro": "The AMS failed to send out filament. You can clip the end of your filament flat, and reinsert. If this message persists, please check the PTFE tubes in AMS for any signs of wear and tear."
        },
        {
          "ecode": "18048003",
          "intro": "Failed to pull out the filament from the extruder. This might be caused by clogged extruder or filament broken inside the extruder."
        },
        {
          "ecode": "07038003",
          "intro": "Failed to pull out the filament from the extruder. This might be caused by clogged extruder or filament broken inside the extruder."
        },
        {
          "ecode": "18018003",
          "intro": "Failed to pull out the filament from the extruder. This might be caused by clogged extruder or filament broken inside the extruder."
        },
        {
          "ecode": "07028005",
          "intro": "The AMS failed to send out filament. You can clip the end of your filament flat, and reinsert. If this message persists, please check the PTFE tubes in AMS for any signs of wear and tear."
        },
        {
          "ecode": "07048006",
          "intro": "Unable to feed filament into the extruder. This could be due to an entangled filament or a stuck spool. If not, please check if the AMS PTFE tube is connected."
        },
        {
          "ecode": "07078006",
          "intro": "Unable to feed filament into the extruder. This could be due to an entangled filament or a stuck spool. If not, please check if the AMS PTFE tube is connected."
        },
        {
          "ecode": "07058006",
          "intro": "Unable to feed filament into the extruder. This could be due to an entangled filament or a stuck spool. If not, please check if the AMS PTFE tube is connected."
        },
        {
          "ecode": "07008006",
          "intro": "Unable to feed filament into the extruder. This could be due to an entangled filament or a stuck spool. If not, please check if the AMS PTFE tube is connected."
        },
        {
          "ecode": "07038006",
          "intro": "Unable to feed filament into the extruder. This could be due to an entangled filament or a stuck spool. If not, please check if the AMS PTFE tube is connected."
        },
        {
          "ecode": "07018006",
          "intro": "Unable to feed filament into the extruder. This could be due to an entangled filament or a stuck spool. If not, please check if the AMS PTFE tube is connected."
        },
        {
          "ecode": "07028006",
          "intro": "Unable to feed filament into the extruder. This could be due to an entangled filament or a stuck spool. If not, please check if the AMS PTFE tube is connected."
        },
        {
          "ecode": "07068006",
          "intro": "Unable to feed filament into the extruder. This could be due to an entangled filament or a stuck spool. If not, please check if the AMS PTFE tube is connected."
        },
        {
          "ecode": "0502400D",
          "intro": "Failed to start a new task: filament loading/unloading not completed."
        },
        {
          "ecode": "0500409D",
          "intro": "The firmware of AMS A does not match the printer; the device cannot continue working. Please upgrade it on the \"Firmware\" page."
        },
        {
          "ecode": "0587409C",
          "intro": "The firmware of AMS-HT H does not match the printer; the device cannot continue working. Please upgrade it on the \"Firmware\" page."
        },
        {
          "ecode": "0502409D",
          "intro": "The firmware of AMS C does not match the printer; the device cannot continue working. Please upgrade it on the \"Firmware\" page."
        },
        {
          "ecode": "03004008",
          "intro": "The AMS failed to change filament."
        },
        {
          "ecode": "05004017",
          "intro": "Binding failed. Please retry or restart the printer and retry."
        },
        {
          "ecode": "1800C06D",
          "intro": "AMS-HT A is assisting in filament insertion. Unable to start drying. Please try again later."
        },
        {
          "ecode": "0702C06A",
          "intro": "AMS C is reading RFID. Unable to start drying. Please try again later."
        },
        {
          "ecode": "1807C06A",
          "intro": "AMS-HT H is reading RFID. Unable to start drying. Please try again later."
        },
        {
          "ecode": "05014020",
          "intro": "Cloud access rejected. If you have tried multiple times and are still failing, please contact customer support."
        },
        {
          "ecode": "1807C069",
          "intro": "An error occurred during AMS-HT H drying. Please go to Assistant for more details."
        },
        {
          "ecode": "1805C06D",
          "intro": "AMS-HT F is assisting in filament insertion. Unable to start drying. Please try again later."
        },
        {
          "ecode": "1000C001",
          "intro": "High bed temperature may lead to filament clogging in the nozzle. You may open the chamber door."
        },
        {
          "ecode": "18038016",
          "intro": "The extruder is not extruding normally; please refer to the Assistant. After trouble shooting. If the defects are acceptable, please resume."
        },
        {
          "ecode": "07068012",
          "intro": "Failed to get AMS mapping table; please select \"Resume\" to retry."
        },
        {
          "ecode": "05004015",
          "intro": "There is not enough free storage space for the print job. Please format or clear files from the MicroSD card to free up space."
        },
        {
          "ecode": "03008007",
          "intro": "There was an unfinished print job when the printer lost power. If the model is still adhered to the build plate, you can try resuming the print job."
        },
        {
          "ecode": "1805C069",
          "intro": "An error occurred during AMS-HT F drying. Please go to Assistant for more details."
        },
        {
          "ecode": "1803C06E",
          "intro": "AMS-HT D motor is performing self-test. Unable to start drying. Please try again later."
        },
        {
          "ecode": "05014022",
          "intro": "Cloud response is invalid. If you have tried multiple times and are still failing, please contact customer support."
        },
        {
          "ecode": "03004001",
          "intro": "The printer timed out waiting for the nozzle to cool down before homing."
        },
        {
          "ecode": "18068010",
          "intro": "The AMS-HT assist motor is overloaded. This could be due to entangled filament or a stuck spool."
        },
        {
          "ecode": "0500401F",
          "intro": "Authorization timed out. Please make sure that your phone or PC has access to the internet, and ensure that the Bambu Studio/Bambu Handy APP is running in the foreground during the binding operation."
        },
        {
          "ecode": "1804C069",
          "intro": "An error occurred during AMS-HT E drying. Please go to Assistant for more details."
        },
        {
          "ecode": "1802C06E",
          "intro": "AMS-HT C motor is performing self-test. Unable to start drying. Please try again later."
        },
        {
          "ecode": "18004025",
          "intro": "Failed to read the filament information."
        },
        {
          "ecode": "1000C002",
          "intro": "Printing CF material with stainless steel may cause nozzle damage."
        },
        {
          "ecode": "18078010",
          "intro": "The AMS-HT assist motor is overloaded. This could be due to entangled filament or a stuck spool."
        },
        {
          "ecode": "0500402F",
          "intro": "The MicroSD card sector data is damaged. Please use the SD card repair tool to repair or format it. If it still cannot be identified, please replace the MicroSD card."
        },
        {
          "ecode": "07038017",
          "intro": "AMS D is drying. Please stop drying process before loading/unloading material."
        },
        {
          "ecode": "0300800A",
          "intro": "A Filament pile-up was detected by AI Print Monitoring. Please clean filament from the waste chute."
        },
        {
          "ecode": "07038013",
          "intro": "Timeout purging old filament: Please check if the filament is stuck or the extruder is clogged."
        },
        {
          "ecode": "07FF8006",
          "intro": "Please feed filament into the PTFE tube until it can not be pushed any farther."
        },
        {
          "ecode": "1801C06A",
          "intro": "AMS-HT B is reading RFID. Unable to start drying. Please try again later."
        },
        {
          "ecode": "05014018",
          "intro": "Binding configuration information parsing failed; please try again."
        },
        {
          "ecode": "07048012",
          "intro": "Failed to get AMS mapping table; please select \"Resume\" to retry."
        },
        {
          "ecode": "18034025",
          "intro": "Failed to read the filament information."
        },
        {
          "ecode": "0500C010",
          "intro": "MicroSD Card read/write exception: please reinsert or replace the MicroSD Card."
        },
        {
          "ecode": "0300800C",
          "intro": "Skipped step detected: auto-recover complete; please resume print and check if there are any layer shift problems."
        },
        {
          "ecode": "07034001",
          "intro": "Filament is still loaded from the AMS after it has been disabled. Please unload the filament, load from the spool holder, and restart printing."
        },
        {
          "ecode": "0500402D",
          "intro": "System exception"
        },
        {
          "ecode": "0300400B",
          "intro": "Internal communication exception"
        },
        {
          "ecode": "1804C06C",
          "intro": "AMS-HT E is in Feed Assist Mode. Unable to start drying. Please try again later."
        },
        {
          "ecode": "18028011",
          "intro": "AMS-HT filament ran out. Please insert a new filament into the same AMS-HT slot."
        },
        {
          "ecode": "07FFC006",
          "intro": "Please feed filament into the PTFE tube until it can not be pushed any farther."
        },
        {
          "ecode": "05014025",
          "intro": "Cloud response is invalid. If you have tried multiple times and are still failing, please contact customer support."
        },
        {
          "ecode": "07FF8013",
          "intro": "Timeout purging old filament: Please check if the filament is stuck or the extruder is clogged."
        },
        {
          "ecode": "18078007",
          "intro": "Extruding filament failed. The extruder might be clogged."
        },
        {
          "ecode": "1800C06B",
          "intro": "AMS-HT A is changing filament. Unable to start drying. Please try again later."
        },
        {
          "ecode": "1800C06E",
          "intro": "AMS-HT A motor is performing self-test. Unable to start drying. Please try again later."
        },
        {
          "ecode": "07008013",
          "intro": "Timeout purging old filament: Please check if the filament is stuck or the extruder is clogged."
        },
        {
          "ecode": "0C008009",
          "intro": "Build plate localization marker was not found."
        },
        {
          "ecode": "0501401A",
          "intro": "Cloud access failed. Possible reasons include network instability caused by interference, inability to access the internet, or router firewall configuration restrictions. You can try moving the printer closer to the router or checking the router configuration before trying again."
        },
        {
          "ecode": "18018010",
          "intro": "The AMS-HT assist motor is overloaded. This could be due to entangled filament or a stuck spool."
        },
        {
          "ecode": "03008016",
          "intro": "The nozzle is clogged with filament. Please cancel this print and clean the nozzle or select \"Resume\" to resume the print job."
        },
        {
          "ecode": "07078012",
          "intro": "Failed to get AMS mapping table; please select \"Resume\" to retry."
        },
        {
          "ecode": "05014031",
          "intro": "Device discovery binding is in progress, and the QR code cannot be displayed on the screen. You can wait for the binding to finish or abort the device discovery binding process in the APP/Studio and retry scanning the QR code on the screen for binding."
        },
        {
          "ecode": "0703C06E",
          "intro": "AMS D motor is performing self-test. Unable to start drying. Please try again later."
        },
        {
          "ecode": "03008004",
          "intro": "Filament ran out. Please load new filament."
        },
        {
          "ecode": "05004008",
          "intro": "Starting printing failed; please power cycle the printer and resend the print job."
        },
        {
          "ecode": "07014025",
          "intro": "Failed to read the filament information."
        },
        {
          "ecode": "07FFC00A",
          "intro": "Please observe the nozzle. If the filament has been extruded, select \"Continue\"; if not, please push the filament forward slightly and then select \"Retry\"."
        },
        {
          "ecode": "1804C06D",
          "intro": "AMS-HT E is assisting in filament insertion. Unable to start drying. Please try again later."
        },
        {
          "ecode": "0700C06C",
          "intro": "AMS A is in Feed Assist Mode. Unable to start drying. Please try again later."
        },
        {
          "ecode": "03008000",
          "intro": "Printing was paused for unknown reason. You can select \"Resume\" to resume the print job."
        },
        {
          "ecode": "0500401A",
          "intro": "Cloud access failed. Possible reasons include network instability caused by interference, inability to access the internet, or router firewall configuration restrictions. You can try moving the printer closer to the router or checking the router configuration before trying again."
        },
        {
          "ecode": "0700C06A",
          "intro": "AMS A is reading RFID. Unable to start drying. Please try again later."
        },
        {
          "ecode": "0703C06B",
          "intro": "AMS D is changing filament. Unable to start drying. Please try again later."
        },
        {
          "ecode": "05004014",
          "intro": "Slicing for the print job failed. Please check your settings and restart the print job."
        },
        {
          "ecode": "1801C06E",
          "intro": "AMS-HT B motor is performing self-test. Unable to start drying. Please try again later."
        },
        {
          "ecode": "0703C06A",
          "intro": "AMS D is reading RFID. Unable to start drying. Please try again later."
        },
        {
          "ecode": "05014024",
          "intro": "Cloud access failed. Possible reasons include network instability caused by interference, inability to access the internet, or router firewall configuration restrictions. You can try moving the printer closer to the router or checking the router configuration before you try again."
        },
        {
          "ecode": "18028016",
          "intro": "The extruder is not extruding normally; please refer to the Assistant. After trouble shooting. If the defects are acceptable, please resume."
        },
        {
          "ecode": "07054025",
          "intro": "Failed to read the filament information."
        },
        {
          "ecode": "0C00402D",
          "intro": "The toolhead camera is not working properly; please reboot the device."
        },
        {
          "ecode": "0701C06D",
          "intro": "AMS B is assisting in filament insertion. Unable to start drying. Please try again later."
        },
        {
          "ecode": "18058012",
          "intro": "Failed to get AMS mapping table; please select \"Resume\" to retry."
        },
        {
          "ecode": "07008002",
          "intro": "The cutter is stuck. Please make sure the cutter handle is out."
        },
        {
          "ecode": "18058007",
          "intro": "Extruding filament failed. The extruder might be clogged."
        },
        {
          "ecode": "18068007",
          "intro": "Extruding filament failed. The extruder might be clogged."
        },
        {
          "ecode": "1807C06E",
          "intro": "AMS-HT H motor is performing self-test. Unable to start drying. Please try again later."
        },
        {
          "ecode": "18068011",
          "intro": "AMS-HT filament ran out. Please insert a new filament into the same AMS-HT slot."
        },
        {
          "ecode": "10018004",
          "intro": "Prime Tower is not enabled and time-lapse mode is set to Smooth in slicing file. This may cause surface defects. Would you like to enable it?"
        },
        {
          "ecode": "0C008001",
          "intro": "First layer defects were detected. If the defects are acceptable, select \"Resume\" to resume the print job."
        },
        {
          "ecode": "03004009",
          "intro": "Homing XY axis failed."
        },
        {
          "ecode": "18038007",
          "intro": "Extruding filament failed. The extruder might be clogged."
        },
        {
          "ecode": "07018002",
          "intro": "The cutter is stuck. Please make sure the cutter handle is out."
        },
        {
          "ecode": "18014025",
          "intro": "Failed to read the filament information."
        },
        {
          "ecode": "07068016",
          "intro": "The extruder is not extruding normally; please refer to the Assistant. After trouble shooting. If the defects are acceptable, please resume."
        },
        {
          "ecode": "0300400E",
          "intro": "The motor self-check failed."
        },
        {
          "ecode": "1000C003",
          "intro": "Enabling Timelapse in traditional mode may cause defects; please activate this feature as needed."
        },
        {
          "ecode": "1805C06E",
          "intro": "AMS-HT F motor is performing self-test. Unable to start drying. Please try again later."
        },
        {
          "ecode": "0C008005",
          "intro": "Purged filament has piled up in the waste chute, which may cause a tool head collision."
        },
        {
          "ecode": "05008013",
          "intro": "The print file is not available. Please check to see if the storage media has been removed."
        },
        {
          "ecode": "03004006",
          "intro": "The nozzle is clogged."
        },
        {
          "ecode": "05004018",
          "intro": "Binding configuration information parsing failed; please try again."
        },
        {
          "ecode": "07064025",
          "intro": "Failed to read the filament information."
        },
        {
          "ecode": "18074025",
          "intro": "Failed to read the filament information."
        },
        {
          "ecode": "0500402E",
          "intro": "The system does not support the file system currently used by the MicroSD card. Please replace the MicroSD card or format it to FAT32."
        },
        {
          "ecode": "1805C06C",
          "intro": "AMS-HT F is in Feed Assist Mode. Unable to start drying. Please try again later."
        },
        {
          "ecode": "1802C06D",
          "intro": "AMS-HT C is assisting in filament insertion. Unable to start drying. Please try again later."
        },
        {
          "ecode": "1806C06B",
          "intro": "AMS-HT G is changing filament. Unable to start drying. Please try again later."
        },
        {
          "ecode": "1803C06D",
          "intro": "AMS-HT D is assisting in filament insertion. Unable to start drying. Please try again later."
        },
        {
          "ecode": "1804C06B",
          "intro": "AMS-HT E is changing filament. Unable to start drying. Please try again later."
        },
        {
          "ecode": "03004067",
          "intro": "Calibration result is over the threshold."
        },
        {
          "ecode": "18024025",
          "intro": "Failed to read the filament information."
        },
        {
          "ecode": "0500401B",
          "intro": "Cloud response is invalid. If you have tried multiple times and are still failing, please contact customer support."
        },
        {
          "ecode": "1805C06B",
          "intro": "AMS-HT F is changing filament. Unable to start drying. Please try again later."
        },
        {
          "ecode": "1806C069",
          "intro": "An error occurred during AMS-HT G drying. Please go to Assistant for more details."
        },
        {
          "ecode": "07FF8010",
          "intro": "Check if the external filament spool or filament is stuck."
        },
        {
          "ecode": "03004020",
          "intro": "The nozzle presence detection failed. Please check the Assistant for details."
        },
        {
          "ecode": "0300800E",
          "intro": "The print file is not available. Please check to see if the storage media has been removed."
        },
        {
          "ecode": "05004020",
          "intro": "Cloud access rejected. If you have tried multiple times and are still failing, please contact customer support."
        },
        {
          "ecode": "0300800F",
          "intro": "The door seems to be open, so printing was paused."
        },
        {
          "ecode": "07018001",
          "intro": "Failed to cut the filament. Please check the cutter."
        },
        {
          "ecode": "03008001",
          "intro": "Printing paused due to the pause command added to the printing file."
        },
        {
          "ecode": "0C00C006",
          "intro": "Purged filament may have piled up in the waste chute."
        },
        {
          "ecode": "1802C069",
          "intro": "An error occurred during AMS-HT C drying. Please go to Assistant for more details."
        },
        {
          "ecode": "07008001",
          "intro": "Failed to cut the filament. Please check the cutter."
        },
        {
          "ecode": "07008016",
          "intro": "The extruder is not extruding normally; please refer to the Assistant. After trouble shooting. If the defects are acceptable, please resume."
        },
        {
          "ecode": "0700C06E",
          "intro": "AMS A motor is performing self-test. Unable to start drying. Please try again later."
        },
        {
          "ecode": "0501401F",
          "intro": "Authorization timed out. Please make sure that your phone or PC has access to the internet, and ensure that the Bambu Studio/Bambu Handy APP is running in the foreground during the binding operation."
        },
        {
          "ecode": "1807C06D",
          "intro": "AMS-HT H is assisting in filament insertion. Unable to start drying. Please try again later."
        },
        {
          "ecode": "1805C06A",
          "intro": "AMS-HT F is reading RFID. Unable to start drying. Please try again later."
        },
        {
          "ecode": "0500400C",
          "intro": "Please insert a MicroSD card and restart the print job."
        },
        {
          "ecode": "07068010",
          "intro": "The AMS assist motor is overloaded. This could be due to entangled filament or a stuck spool."
        },
        {
          "ecode": "05014033",
          "intro": "Your APP region does not match with your printer; please download the APP in the corresponding region and register your account again."
        },
        {
          "ecode": "07008012",
          "intro": "Failed to get AMS mapping table; please select \"Resume\" to retry."
        },
        {
          "ecode": "18028010",
          "intro": "The AMS-HT assist motor is overloaded. This could be due to entangled filament or a stuck spool."
        },
        {
          "ecode": "1801C06B",
          "intro": "AMS-HT B is changing filament. Unable to start drying. Please try again later."
        },
        {
          "ecode": "0C00C003",
          "intro": "Possible defects were detected in the first layer."
        },
        {
          "ecode": "0703C06C",
          "intro": "AMS D is in Feed Assist Mode. Unable to start drying. Please try again later."
        },
        {
          "ecode": "03008014",
          "intro": "The nozzle is covered with filament, or the build plate is installed incorrectly. Please cancel this print and clean the nozzle or adjust the build plate according to the actual status. You can also select \"Resume\" to resume the print job."
        },
        {
          "ecode": "05004028",
          "intro": "Cloud response is invalid. If you have tried multiple times and are still failing, please contact customer support."
        },
        {
          "ecode": "07048011",
          "intro": "AMS filament ran out. Please insert a new filament into the same AMS slot."
        },
        {
          "ecode": "05014028",
          "intro": "Cloud response is invalid. If you have tried multiple times and are still failing, please contact customer support."
        },
        {
          "ecode": "07078010",
          "intro": "The AMS assist motor is overloaded. This could be due to entangled filament or a stuck spool."
        },
        {
          "ecode": "1806C06C",
          "intro": "AMS-HT G is in Feed Assist Mode. Unable to start drying. Please try again later."
        },
        {
          "ecode": "07044025",
          "intro": "Failed to read the filament information."
        },
        {
          "ecode": "18058010",
          "intro": "The AMS-HT assist motor is overloaded. This could be due to entangled filament or a stuck spool."
        },
        {
          "ecode": "05004024",
          "intro": "Cloud access failed. Possible reasons include network instability caused by interference, inability to access the internet, or router firewall configuration restrictions. You can try moving the printer closer to the router or checking the router configuration before you try again."
        },
        {
          "ecode": "0500400D",
          "intro": "Please run a self-test and restart the print job."
        },
        {
          "ecode": "0701C06A",
          "intro": "AMS B is reading RFID. Unable to start drying. Please try again later."
        },
        {
          "ecode": "05024004",
          "intro": "Some features are not supported by the current device. Please check the Studio feature settings or update the firmware to the latest version."
        },
        {
          "ecode": "18048007",
          "intro": "Extruding filament failed. The extruder might be clogged."
        },
        {
          "ecode": "05004019",
          "intro": "The printer has already been bound. Please unbind it and try again."
        },
        {
          "ecode": "05004029",
          "intro": "Cloud access is rejected. If you have tried multiple times and are still failing, please contact customer support."
        },
        {
          "ecode": "07018007",
          "intro": "Extruding filament failed. The extruder might be clogged."
        },
        {
          "ecode": "07078007",
          "intro": "Extruding filament failed. The extruder might be clogged."
        },
        {
          "ecode": "0C00C004",
          "intro": "Possible spaghetti failure was detected."
        },
        {
          "ecode": "05024001",
          "intro": "Current filament will be used in this print job. Settings cannot be changed."
        },
        {
          "ecode": "07068007",
          "intro": "Extruding filament failed. The extruder might be clogged."
        },
        {
          "ecode": "18068016",
          "intro": "The extruder is not extruding normally; please refer to the Assistant. After trouble shooting. If the defects are acceptable, please resume."
        },
        {
          "ecode": "18FF8012",
          "intro": "Failed to get AMS mapping table; please select \"Resume\" to retry."
        },
        {
          "ecode": "05004038",
          "intro": "The nozzle diameter in sliced file is not consistent with the current nozzle setting. This file can't be printed."
        },
        {
          "ecode": "07038002",
          "intro": "The cutter is stuck. Please make sure the cutter handle is out."
        },
        {
          "ecode": "05014029",
          "intro": "Cloud access is rejected. If you have tried multiple times and are still failing, please contact customer support."
        },
        {
          "ecode": "07074025",
          "intro": "Failed to read the filament information."
        },
        {
          "ecode": "18048012",
          "intro": "Failed to get AMS mapping table; please select \"Resume\" to retry."
        },
        {
          "ecode": "05014035",
          "intro": "The device is in the process of binding and cannot respond to new binding requests."
        },
        {
          "ecode": "07028002",
          "intro": "The cutter is stuck. Please make sure the cutter handle is out."
        },
        {
          "ecode": "07028012",
          "intro": "Failed to get AMS mapping table; please select \"Resume\" to retry."
        },
        {
          "ecode": "18048011",
          "intro": "AMS-HT filament ran out. Please insert a new filament into the same AMS-HT slot."
        },
        {
          "ecode": "1800C06C",
          "intro": "AMS-HT A is in Feed Assist Mode. Unable to start drying. Please try again later."
        },
        {
          "ecode": "10014002",
          "intro": "Timelapse is not supported as the Print sequence is set to \"By object\"."
        },
        {
          "ecode": "0700C069",
          "intro": "An error occurred during AMS A drying. Please go to Assistant for more details."
        },
        {
          "ecode": "03008009",
          "intro": "Heatbed temperature malfunction"
        },
        {
          "ecode": "07048016",
          "intro": "The extruder is not extruding normally; please refer to the Assistant. After trouble shooting. If the defects are acceptable, please resume."
        },
        {
          "ecode": "07018016",
          "intro": "The extruder is not extruding normally; please refer to the Assistant. After trouble shooting. If the defects are acceptable, please resume."
        },
        {
          "ecode": "18018012",
          "intro": "Failed to get AMS mapping table; please select \"Resume\" to retry."
        },
        {
          "ecode": "07038016",
          "intro": "The extruder is not extruding normally; please refer to the Assistant. After trouble shooting. If the defects are acceptable, please resume."
        },
        {
          "ecode": "0701C06E",
          "intro": "AMS B motor is performing self-test. Unable to start drying. Please try again later."
        },
        {
          "ecode": "05004001",
          "intro": "Failed to connect to Bambu Cloud. Please check your network connection."
        },
        {
          "ecode": "0702C06D",
          "intro": "AMS C is assisting in filament insertion. Unable to start drying. Please try again later."
        },
        {
          "ecode": "18018017",
          "intro": "AMS-HT B is drying. Please stop drying process before loading/unloading material."
        },
        {
          "ecode": "07018011",
          "intro": "AMS filament ran out. Please insert a new filament into the same AMS slot."
        },
        {
          "ecode": "05004022",
          "intro": "Cloud response is invalid. If you have tried multiple times and are still failing, please contact customer support."
        },
        {
          "ecode": "1801C069",
          "intro": "An error occurred during AMS-HT B drying. Please go to Assistant for more details."
        },
        {
          "ecode": "18028017",
          "intro": "AMS-HT C is drying. Please stop drying process before loading/unloading material."
        },
        {
          "ecode": "07028010",
          "intro": "The AMS assist motor is overloaded. This could be due to entangled filament or a stuck spool."
        },
        {
          "ecode": "05014017",
          "intro": "Binding failed. Please retry or restart the printer and retry."
        },
        {
          "ecode": "03008002",
          "intro": "First layer defects were detected by the Micro Lidar. Please check the quality of the printed model before continuing your print."
        },
        {
          "ecode": "18054025",
          "intro": "Failed to read the filament information."
        },
        {
          "ecode": "05004009",
          "intro": "Print jobs are not allowed to be sent while updating logs."
        },
        {
          "ecode": "05014026",
          "intro": "Cloud access rejected. If you have tried multiple times and are still failing, please contact customer support."
        },
        {
          "ecode": "18038017",
          "intro": "AMS-HT D is drying. Please stop drying process before loading/unloading material."
        },
        {
          "ecode": "07FF4001",
          "intro": "Filament is still loaded from the AMS after it has been disabled. Please unload the filament, load from the spool holder, and restart printing."
        },
        {
          "ecode": "05004005",
          "intro": "Print jobs are not allowed to be sent while updating firmware."
        },
        {
          "ecode": "0500400B",
          "intro": "There was a problem downloading a file. Please check your network connection and resend the print job."
        },
        {
          "ecode": "07038007",
          "intro": "Extruding filament failed. The extruder might be clogged."
        },
        {
          "ecode": "03008019",
          "intro": "No build plate is placed."
        },
        {
          "ecode": "0500402C",
          "intro": "Failed to obtain IP address, which may be caused by wireless interference resulting in data transmission failure or the DHCP address pool of the router being full. Please move the printer closer to the router and try again. If the issue persists, please check router settings to see whether the IP addresses have been exhausted."
        },
        {
          "ecode": "1801C06D",
          "intro": "AMS-HT B is assisting in filament insertion. Unable to start drying. Please try again later."
        },
        {
          "ecode": "03008013",
          "intro": "Printing was paused by the user. You can select \"Resume\" to continue printing."
        },
        {
          "ecode": "18008011",
          "intro": "AMS-HT filament ran out. Please insert a new filament into the same AMS-HT slot."
        },
        {
          "ecode": "07034025",
          "intro": "Failed to read the filament information."
        },
        {
          "ecode": "03004066",
          "intro": "Calibration of motion precision failed."
        },
        {
          "ecode": "18008016",
          "intro": "The extruder is not extruding normally; please refer to the Assistant. After trouble shooting. If the defects are acceptable, please resume."
        },
        {
          "ecode": "03004013",
          "intro": "Printing cannot be initiated while AMS is drying."
        },
        {
          "ecode": "05004021",
          "intro": "Cloud access failed, which may be caused by network instability due to interference. You can try moving the printer closer to the router before you try again."
        },
        {
          "ecode": "07FFC003",
          "intro": "Please pull out the filament on the spool holder. If this message persists, please check to see if there is filament broken in the extruder or PTFE tube. (Connect a PTFE tube if you are about to use an AMS)"
        },
        {
          "ecode": "07004025",
          "intro": "Failed to read the filament information."
        },
        {
          "ecode": "07038011",
          "intro": "AMS filament ran out. Please insert a new filament into the same AMS slot."
        },
        {
          "ecode": "05004043",
          "intro": "Due to power limitations, only one AMS is allowed to use the device's power for drying."
        },
        {
          "ecode": "07028011",
          "intro": "AMS filament ran out. Please insert a new filament into the same AMS slot."
        },
        {
          "ecode": "1800C06A",
          "intro": "AMS-HT A is reading RFID. Unable to start drying. Please try again later."
        },
        {
          "ecode": "05014019",
          "intro": "The printer has already been bound. Please unbind it and try again."
        },
        {
          "ecode": "1807C06B",
          "intro": "AMS-HT H is changing filament. Unable to start drying. Please try again later."
        },
        {
          "ecode": "0300800D",
          "intro": "Detected that the extruder is not extruding normally. If the defects are acceptable, select \"Resume\" to resume the print job."
        },
        {
          "ecode": "07FF8012",
          "intro": "Failed to get AMS mapping table; please select \"Resume\" to retry."
        },
        {
          "ecode": "1806C06A",
          "intro": "AMS-HT G is reading RFID. Unable to start drying. Please try again later."
        },
        {
          "ecode": "03004005",
          "intro": "The hotend cooling fan speed is abnormal."
        },
        {
          "ecode": "18018011",
          "intro": "AMS-HT filament ran out. Please insert a new filament into the same AMS-HT slot."
        },
        {
          "ecode": "03008008",
          "intro": "Nozzle temperature malfunction"
        },
        {
          "ecode": "0701C06B",
          "intro": "AMS B is changing filament. Unable to start drying. Please try again later."
        },
        {
          "ecode": "0700C06B",
          "intro": "AMS A is changing filament. Unable to start drying. Please try again later."
        },
        {
          "ecode": "07008011",
          "intro": "AMS filament ran out. Please insert a new filament into the same AMS slot."
        },
        {
          "ecode": "10018003",
          "intro": "The time-lapse mode is set to Traditional in the slicing file. This may cause surface defects. Would you like to enable it?"
        },
        {
          "ecode": "07008017",
          "intro": "AMS A is drying. Please stop drying process before loading/unloading material."
        },
        {
          "ecode": "0500402B",
          "intro": "Router connection failed due to incorrect password. Please check the password and try again."
        },
        {
          "ecode": "07028017",
          "intro": "AMS C is drying. Please stop drying process before loading/unloading material."
        },
        {
          "ecode": "05014023",
          "intro": "Cloud access rejected. If you have tried multiple times and are still failing, please contact customer support."
        },
        {
          "ecode": "1803C06B",
          "intro": "AMS-HT D is changing filament. Unable to start drying. Please try again later."
        },
        {
          "ecode": "05004004",
          "intro": "Device is busy and cannot start new task. Please wait for current task to complete before sending new task."
        },
        {
          "ecode": "03008017",
          "intro": "Foreign objects detected on heatbed. Please check and clean the heatbed. Then, select \"Resume\" to resume the print job."
        },
        {
          "ecode": "07048007",
          "intro": "Extruding filament failed. The extruder might be clogged."
        },
        {
          "ecode": "05014038",
          "intro": "The regional settings do not match the printer; please check the printer's regional settings."
        },
        {
          "ecode": "07FF8002",
          "intro": "The cutter is stuck. Please make sure the cutter handle is out."
        },
        {
          "ecode": "05004037",
          "intro": "Your sliced file is not compatible with current printer model. This file can't be printed on this printer."
        },
        {
          "ecode": "18038011",
          "intro": "AMS-HT filament ran out. Please insert a new filament into the same AMS-HT slot."
        },
        {
          "ecode": "05014027",
          "intro": "Cloud access failed; this may be caused by network instability due to interference. You can try moving the printer closer to the router before you try again."
        },
        {
          "ecode": "0703C069",
          "intro": "An error occurred during AMS D drying. Please go to Assistant for more details."
        },
        {
          "ecode": "0701C06C",
          "intro": "AMS B is in Feed Assist Mode. Unable to start drying. Please try again later."
        },
        {
          "ecode": "0702C069",
          "intro": "An error occurred during AMS C drying. Please go to Assistant for more details."
        },
        {
          "ecode": "18058011",
          "intro": "AMS-HT filament ran out. Please insert a new filament into the same AMS-HT slot."
        },
        {
          "ecode": "03008006",
          "intro": "The build plate marker was not detected. Please confirm the build plate is correctly positioned on the heatbed with all four corners aligned, and the marker is visible."
        },
        {
          "ecode": "05014032",
          "intro": "QR code binding is in progress, so device discovery binding cannot be performed. You can scan the QR code on the screen for binding or exit the QR code display page on screen and try device discovery binding."
        },
        {
          "ecode": "18018007",
          "intro": "Extruding filament failed. The extruder might be clogged."
        },
        {
          "ecode": "0500402A",
          "intro": "Failed to connect to the router, which may be caused by wireless interference or being too far away from the router. Please try again or move the printer closer to the router and try again."
        },
        {
          "ecode": "07018012",
          "intro": "Failed to get AMS mapping table; please select \"Resume\" to retry."
        },
        {
          "ecode": "18008010",
          "intro": "The AMS-HT assist motor is overloaded. This could be due to entangled filament or a stuck spool."
        },
        {
          "ecode": "07078011",
          "intro": "AMS filament ran out. Please insert a new filament into the same AMS slot."
        },
        {
          "ecode": "05014039",
          "intro": "Device login has expired; please try to bind again."
        },
        {
          "ecode": "0500401E",
          "intro": "Cloud response is invalid. If you have tried multiple times and are still failing, please contact customer support."
        },
        {
          "ecode": "18064025",
          "intro": "Failed to read the filament information."
        },
        {
          "ecode": "07048010",
          "intro": "The AMS assist motor is overloaded. This could be due to entangled filament or a stuck spool."
        },
        {
          "ecode": "18078012",
          "intro": "Failed to get AMS mapping table; please select \"Resume\" to retry."
        },
        {
          "ecode": "03008003",
          "intro": "Spaghetti defects were detected by the AI Print Monitoring. Please check the quality of the printed model before continuing your print."
        },
        {
          "ecode": "18048010",
          "intro": "The AMS-HT assist motor is overloaded. This could be due to entangled filament or a stuck spool."
        },
        {
          "ecode": "1803C06A",
          "intro": "AMS-HT D is reading RFID. Unable to start drying. Please try again later."
        },
        {
          "ecode": "18018016",
          "intro": "The extruder is not extruding normally; please refer to the Assistant. After trouble shooting. If the defects are acceptable, please resume."
        },
        {
          "ecode": "18068012",
          "intro": "Failed to get AMS mapping table; please select \"Resume\" to retry."
        },
        {
          "ecode": "0702C06C",
          "intro": "AMS C is in Feed Assist Mode. Unable to start drying. Please try again later."
        },
        {
          "ecode": "10014001",
          "intro": "Timelapse is not supported as Spiral Vase mode is enabled in slicing presets."
        },
        {
          "ecode": "0702C06B",
          "intro": "AMS C is changing filament. Unable to start drying. Please try again later."
        },
        {
          "ecode": "18058016",
          "intro": "The extruder is not extruding normally; please refer to the Assistant. After trouble shooting. If the defects are acceptable, please resume."
        },
        {
          "ecode": "07018010",
          "intro": "The AMS assist motor is overloaded. This could be due to entangled filament or a stuck spool."
        },
        {
          "ecode": "1804C06E",
          "intro": "AMS-HT E motor is performing self-test. Unable to start drying. Please try again later."
        },
        {
          "ecode": "07058007",
          "intro": "Extruding filament failed. The extruder might be clogged."
        },
        {
          "ecode": "07058010",
          "intro": "The AMS assist motor is overloaded. This could be due to entangled filament or a stuck spool."
        },
        {
          "ecode": "07028016",
          "intro": "The extruder is not extruding normally; please refer to the Assistant. After trouble shooting. If the defects are acceptable, please resume."
        },
        {
          "ecode": "18078011",
          "intro": "AMS-HT filament ran out. Please insert a new filament into the same AMS-HT slot."
        },
        {
          "ecode": "07FF8004",
          "intro": "Failed to pull back the filament from the toolhead to AMS. Please check whether the filament or the spool is stuck."
        },
        {
          "ecode": "07068011",
          "intro": "AMS filament ran out. Please insert a new filament into the same AMS slot."
        },
        {
          "ecode": "07FF8011",
          "intro": "External filament has run out; please load a new filament."
        },
        {
          "ecode": "0500401C",
          "intro": "Cloud access is rejected. If you have tried multiple times and are still failing, please contact customer support."
        },
        {
          "ecode": "03008010",
          "intro": "The hotend cooling fan speed is abnormal."
        },
        {
          "ecode": "07024001",
          "intro": "Filament is still loaded from the AMS after it has been disabled. Please unload the filament, load from the spool holder, and restart printing."
        },
        {
          "ecode": "0700C06D",
          "intro": "AMS A is assisting in filament insertion. Unable to start drying. Please try again later."
        },
        {
          "ecode": "03008005",
          "intro": "Toolhead front cover fell off. Please remount the front cover and check to make sure your print is going okay."
        },
        {
          "ecode": "1802C06A",
          "intro": "AMS-HT C is reading RFID. Unable to start drying. Please try again later."
        },
        {
          "ecode": "1803C06C",
          "intro": "AMS-HT D is in Feed Assist Mode. Unable to start drying. Please try again later."
        },
        {
          "ecode": "1806C06D",
          "intro": "AMS-HT G is assisting in filament insertion. Unable to start drying. Please try again later."
        },
        {
          "ecode": "05004023",
          "intro": "Cloud access rejected. If you have tried multiple times and are still failing, please contact customer support."
        },
        {
          "ecode": "05008030",
          "intro": ""
        },
        {
          "ecode": "0501401D",
          "intro": "Cloud access failed, which may be caused by network instability due to interference. You can try moving the printer closer to the router before you try again."
        },
        {
          "ecode": "0501401B",
          "intro": "Cloud response is invalid. If you have tried multiple times and are still failing, please contact customer support."
        },
        {
          "ecode": "07028013",
          "intro": "Timeout purging old filament: Please check if the filament is stuck or the extruder is clogged."
        },
        {
          "ecode": "18008017",
          "intro": "AMS-HT A is drying. Please stop drying process before loading/unloading material."
        },
        {
          "ecode": "07058012",
          "intro": "Failed to get AMS mapping table; please select \"Resume\" to retry."
        },
        {
          "ecode": "07014001",
          "intro": "Filament is still loaded from the AMS after it has been disabled. Please unload the filament, load from the spool holder, and restart printing."
        },
        {
          "ecode": "0701C069",
          "intro": "An error occurred during AMS B drying. Please go to Assistant for more details."
        },
        {
          "ecode": "05004026",
          "intro": "Cloud access rejected. If you have tried multiple times and are still failing, please contact customer support."
        },
        {
          "ecode": "1801C06C",
          "intro": "AMS-HT B is in Feed Assist Mode. Unable to start drying. Please try again later."
        },
        {
          "ecode": "07008007",
          "intro": "Extruding filament failed. The extruder might be clogged."
        },
        {
          "ecode": "18008007",
          "intro": "Extruding filament failed. The extruder might be clogged."
        },
        {
          "ecode": "0702C06E",
          "intro": "AMS C motor is performing self-test. Unable to start drying. Please try again later."
        },
        {
          "ecode": "07FFC008",
          "intro": "Please pull out the filament on the spool holder. If this message persists, please check to see if there is filament broken in the extruder. (Connect a PTFE tube if you are about to use an AMS)"
        },
        {
          "ecode": "07028007",
          "intro": "Extruding filament failed. The extruder might be clogged."
        },
        {
          "ecode": "0500400A",
          "intro": "The file name is not supported. Please rename and restart the print job."
        },
        {
          "ecode": "07028001",
          "intro": "Failed to cut the filament. Please check the cutter."
        },
        {
          "ecode": "07008010",
          "intro": "The AMS assist motor is overloaded. This could be due to entangled filament or a stuck spool."
        },
        {
          "ecode": "18078016",
          "intro": "The extruder is not extruding normally; please refer to the Assistant. After trouble shooting. If the defects are acceptable, please resume."
        },
        {
          "ecode": "18028012",
          "intro": "Failed to get AMS mapping table; please select \"Resume\" to retry."
        },
        {
          "ecode": "05004027",
          "intro": "Cloud access failed; this may be caused by network instability due to interference. You can try moving the printer closer to the router before you try again."
        },
        {
          "ecode": "07FFC009",
          "intro": "Please feed filament into the PTFE tube until it can not be pushed any farther."
        },
        {
          "ecode": "07018017",
          "intro": "AMS B is drying. Please stop drying process before loading/unloading material."
        },
        {
          "ecode": "07038010",
          "intro": "The AMS assist motor is overloaded. This could be due to entangled filament or a stuck spool."
        },
        {
          "ecode": "1802C06C",
          "intro": "AMS-HT C is in Feed Assist Mode. Unable to start drying. Please try again later."
        },
        {
          "ecode": "05004025",
          "intro": "Cloud response is invalid. If you have tried multiple times and are still failing, please contact customer support."
        },
        {
          "ecode": "05008036",
          "intro": "Your sliced file is not consistent with the current printer model. Continue?"
        },
        {
          "ecode": "07038001",
          "intro": "Failed to cut the filament. Please check the cutter."
        },
        {
          "ecode": "18044025",
          "intro": "Failed to read the filament information."
        },
        {
          "ecode": "03008011",
          "intro": "Detected build plate is not the same as the Gcode file. Please adjust slicer settings or use the correct plate."
        },
        {
          "ecode": "0500401D",
          "intro": "Cloud access failed, which may be caused by network instability due to interference. You can try moving the printer closer to the router before you try again."
        },
        {
          "ecode": "0703C06D",
          "intro": "AMS D is assisting in filament insertion. Unable to start drying. Please try again later."
        },
        {
          "ecode": "0300400A",
          "intro": "Mechanical resonance frequency identification failed."
        },
        {
          "ecode": "18008012",
          "intro": "Failed to get AMS mapping table; please select \"Resume\" to retry."
        },
        {
          "ecode": "18048016",
          "intro": "The extruder is not extruding normally; please refer to the Assistant. After trouble shooting. If the defects are acceptable, please resume."
        },
        {
          "ecode": "18038010",
          "intro": "The AMS-HT assist motor is overloaded. This could be due to entangled filament or a stuck spool."
        },
        {
          "ecode": "0501401C",
          "intro": "Cloud access is rejected. If you have tried multiple times and are still failing, please contact customer support."
        },
        {
          "ecode": "03008018",
          "intro": "Chamber temperature malfunction."
        },
        {
          "ecode": "07058016",
          "intro": "The extruder is not extruding normally; please refer to the Assistant. After trouble shooting. If the defects are acceptable, please resume."
        },
        {
          "ecode": "05004002",
          "intro": "Unsupported print file path or name. Please resend the print job."
        },
        {
          "ecode": "07078016",
          "intro": "The extruder is not extruding normally; please refer to the Assistant. After trouble shooting. If the defects are acceptable, please resume."
        },
        {
          "ecode": "05014021",
          "intro": "Cloud access failed, which may be caused by network instability due to interference. You can try moving the printer closer to the router before you try again."
        },
        {
          "ecode": "1806C06E",
          "intro": "AMS-HT G motor is performing self-test. Unable to start drying. Please try again later."
        },
        {
          "ecode": "1800C069",
          "intro": "An error occurred during AMS-HT A drying. Please go to Assistant for more details."
        },
        {
          "ecode": "1804C06A",
          "intro": "AMS-HT E is reading RFID. Unable to start drying. Please try again later."
        },
        {
          "ecode": "1807C06C",
          "intro": "AMS-HT H is in Feed Assist Mode. Unable to start drying. Please try again later."
        },
        {
          "ecode": "03004002",
          "intro": "Auto Bed Leveling failed; the task has been stopped."
        },
        {
          "ecode": "1803C069",
          "intro": "An error occurred during AMS-HT D drying. Please go to Assistant for more details."
        },
        {
          "ecode": "1802C06B",
          "intro": "AMS-HT C is changing filament. Unable to start drying. Please try again later."
        },
        {
          "ecode": "05004006",
          "intro": "There is not enough free storage space for the print job. Restoring to factory settings can free up available space."
        },
        {
          "ecode": "0501401E",
          "intro": "Cloud response is invalid. If you have tried multiple times and are still failing, please contact customer support."
        },
        {
          "ecode": "05004003",
          "intro": "Printing stopped because the printer was unable to parse the file. Please resend your print job."
        },
        {
          "ecode": "05014034",
          "intro": "The slicing progress has not been updated for a long time, and the printing task has exited. Please confirm the parameters and reinitiate printing."
        },
        {
          "ecode": "18028007",
          "intro": "Extruding filament failed. The extruder might be clogged."
        },
        {
          "ecode": "18038012",
          "intro": "Failed to get AMS mapping table; please select \"Resume\" to retry."
        },
        {
          "ecode": "0300400C",
          "intro": "The task was canceled."
        },
        {
          "ecode": "07038012",
          "intro": "Failed to get AMS mapping table; please select \"Resume\" to retry."
        },
        {
          "ecode": "07058011",
          "intro": "AMS filament ran out. Please insert a new filament into the same AMS slot."
        },
        {
          "ecode": "07004001",
          "intro": "The AMS has been disabled for a print, but it still has filament loaded. Please unload the AMS filament and switch to the spool holder filament for printing."
        },
        {
          "ecode": "07FF8003",
          "intro": "Please pull out the filament on the spool holder. If this message persists, please check to see if there is filament broken in the extruder. (Connect a PTFE tube if you are about to use an AMS.)"
        },
        {
          "ecode": "03004000",
          "intro": "Z axis homing failed; the task has been stopped."
        },
        {
          "ecode": "07018013",
          "intro": "Timeout purging old filament: Please check if the filament is stuck or the extruder is clogged."
        },
        {
          "ecode": "07FF8001",
          "intro": "Failed to cut the filament. Please check the cutter."
        },
        {
          "ecode": "0300800B",
          "intro": "The cutter is stuck. Please make sure the cutter handle is out and check the filament sensor cable connection."
        }
      ]
    },
    "device_hms": {
      "ver": 202510221200,
      "en": [
        {
          "ecode": "1803220000010082",
          "intro": "Failed to read the filament information from AMS-HT D slot 3. A third party RFID tag was detected."
        },
        {
          "ecode": "0700230000010082",
          "intro": "Failed to read the filament information from AMS A slot 4. A third party RFID tag was detected."
        },
        {
          "ecode": "1800220000010082",
          "intro": "Failed to read the filament information from AMS-HT A slot 3. A third party RFID tag was detected."
        },
        {
          "ecode": "0707230000010082",
          "intro": "Failed to read the filament information from AMS H slot 4. A third party RFID tag was detected."
        },
        {
          "ecode": "1805220000010082",
          "intro": "Failed to read the filament information from AMS-HT F slot 3. A third party RFID tag was detected."
        },
        {
          "ecode": "1803230000010082",
          "intro": "Failed to read the filament information from AMS-HT D slot 4. A third party RFID tag was detected."
        },
        {
          "ecode": "1800210000010082",
          "intro": "Failed to read the filament information from AMS-HT A slot 2. A third party RFID tag was detected."
        },
        {
          "ecode": "1803200000010082",
          "intro": "Failed to read the filament information from AMS-HT D slot 1. A third party RFID tag was detected."
        },
        {
          "ecode": "1805210000010082",
          "intro": "Failed to read the filament information from AMS-HT F slot 2. A third party RFID tag was detected."
        },
        {
          "ecode": "0707200000010082",
          "intro": "Failed to read the filament information from AMS H slot 1. A third party RFID tag was detected."
        },
        {
          "ecode": "1806230000010082",
          "intro": "Failed to read the filament information from AMS-HT G slot 4. A third party RFID tag was detected."
        },
        {
          "ecode": "0705210000010082",
          "intro": "Failed to read the filament information from AMS F slot 2. A third party RFID tag was detected."
        },
        {
          "ecode": "0704200000010082",
          "intro": "Failed to read the filament information from AMS E slot 1. A third party RFID tag was detected."
        },
        {
          "ecode": "1804220000010082",
          "intro": "Failed to read the filament information from AMS-HT E slot 3. A third party RFID tag was detected."
        },
        {
          "ecode": "1804200000010082",
          "intro": "Failed to read the filament information from AMS-HT E slot 1. A third party RFID tag was detected."
        },
        {
          "ecode": "0704230000010082",
          "intro": "Failed to read the filament information from AMS E slot 4. A third party RFID tag was detected."
        },
        {
          "ecode": "1803210000010082",
          "intro": "Failed to read the filament information from AMS-HT D slot 2. A third party RFID tag was detected."
        },
        {
          "ecode": "0703210000010082",
          "intro": "Failed to read the filament information from AMS D slot 2. A third party RFID tag was detected."
        },
        {
          "ecode": "0702220000010082",
          "intro": "Failed to read the filament information from AMS C slot 3. A third party RFID tag was detected."
        },
        {
          "ecode": "1802220000010082",
          "intro": "Failed to read the filament information from AMS-HT C slot 3. A third party RFID tag was detected."
        },
        {
          "ecode": "0701210000010082",
          "intro": "Failed to read the filament information from AMS B slot 2. A third party RFID tag was detected."
        },
        {
          "ecode": "1804230000010082",
          "intro": "Failed to read the filament information from AMS-HT E slot 4. A third party RFID tag was detected."
        },
        {
          "ecode": "1805200000010082",
          "intro": "Failed to read the filament information from AMS-HT F slot 1. A third party RFID tag was detected."
        },
        {
          "ecode": "0704220000010082",
          "intro": "Failed to read the filament information from AMS E slot 3. A third party RFID tag was detected."
        },
        {
          "ecode": "0707220000010082",
          "intro": "Failed to read the filament information from AMS H slot 3. A third party RFID tag was detected."
        },
        {
          "ecode": "0700210000010082",
          "intro": "Failed to read the filament information from AMS A slot 2. A third party RFID tag was detected."
        },
        {
          "ecode": "0703220000010082",
          "intro": "Failed to read the filament information from AMS D slot 3. A third party RFID tag was detected."
        },
        {
          "ecode": "0702230000010082",
          "intro": "Failed to read the filament information from AMS C slot 4. A third party RFID tag was detected."
        },
        {
          "ecode": "0702210000010082",
          "intro": "Failed to read the filament information from AMS C slot 2. A third party RFID tag was detected."
        },
        {
          "ecode": "1802230000010082",
          "intro": "Failed to read the filament information from AMS-HT C slot 4. A third party RFID tag was detected."
        },
        {
          "ecode": "1804210000010082",
          "intro": "Failed to read the filament information from AMS-HT E slot 2. A third party RFID tag was detected."
        },
        {
          "ecode": "1801230000010082",
          "intro": "Failed to read the filament information from AMS-HT B slot 4. A third party RFID tag was detected."
        },
        {
          "ecode": "1802200000010082",
          "intro": "Failed to read the filament information from AMS-HT C slot 1. A third party RFID tag was detected."
        },
        {
          "ecode": "1807200000010082",
          "intro": "Failed to read the filament information from AMS-HT H slot 1. A third party RFID tag was detected."
        },
        {
          "ecode": "1806220000010082",
          "intro": "Failed to read the filament information from AMS-HT G slot 3. A third party RFID tag was detected."
        },
        {
          "ecode": "0706230000010082",
          "intro": "Failed to read the filament information from AMS G slot 4. A third party RFID tag was detected."
        },
        {
          "ecode": "1801200000010082",
          "intro": "Failed to read the filament information from AMS-HT B slot 1. A third party RFID tag was detected."
        },
        {
          "ecode": "0701200000010082",
          "intro": "Failed to read the filament information from AMS B slot 1. A third party RFID tag was detected."
        },
        {
          "ecode": "0706220000010082",
          "intro": "Failed to read the filament information from AMS G slot 3. A third party RFID tag was detected."
        },
        {
          "ecode": "1806200000010082",
          "intro": "Failed to read the filament information from AMS-HT G slot 1. A third party RFID tag was detected."
        },
        {
          "ecode": "0705230000010082",
          "intro": "Failed to read the filament information from AMS F slot 4. A third party RFID tag was detected."
        },
        {
          "ecode": "1807230000010082",
          "intro": "Failed to read the filament information from AMS-HT H slot 4. A third party RFID tag was detected."
        },
        {
          "ecode": "0700200000010082",
          "intro": "Failed to read the filament information from AMS A slot 1. A third party RFID tag was detected."
        },
        {
          "ecode": "0707210000010082",
          "intro": "Failed to read the filament information from AMS H slot 2. A third party RFID tag was detected."
        },
        {
          "ecode": "1800230000010082",
          "intro": "Failed to read the filament information from AMS-HT A slot 4. A third party RFID tag was detected."
        },
        {
          "ecode": "1806210000010082",
          "intro": "Failed to read the filament information from AMS-HT G slot 2. A third party RFID tag was detected."
        },
        {
          "ecode": "1807220000010082",
          "intro": "Failed to read the filament information from AMS-HT H slot 3. A third party RFID tag was detected."
        },
        {
          "ecode": "0705200000010082",
          "intro": "Failed to read the filament information from AMS F slot 1. A third party RFID tag was detected."
        },
        {
          "ecode": "1807210000010082",
          "intro": "Failed to read the filament information from AMS-HT H slot 2. A third party RFID tag was detected."
        },
        {
          "ecode": "0705220000010082",
          "intro": "Failed to read the filament information from AMS F slot 3. A third party RFID tag was detected."
        },
        {
          "ecode": "1802210000010082",
          "intro": "Failed to read the filament information from AMS-HT C slot 2. A third party RFID tag was detected."
        },
        {
          "ecode": "0701230000010082",
          "intro": "Failed to read the filament information from AMS B slot 4. A third party RFID tag was detected."
        },
        {
          "ecode": "0703200000010082",
          "intro": "Failed to read the filament information from AMS D slot 1. A third party RFID tag was detected."
        },
        {
          "ecode": "0702200000010082",
          "intro": "Failed to read the filament information from AMS C slot 1. A third party RFID tag was detected."
        },
        {
          "ecode": "0701220000010082",
          "intro": "Failed to read the filament information from AMS B slot 3. A third party RFID tag was detected."
        },
        {
          "ecode": "1805230000010082",
          "intro": "Failed to read the filament information from AMS-HT F. A third party RFID tag was detected."
        },
        {
          "ecode": "1800200000010082",
          "intro": "Failed to read the filament information from AMS-HT A slot 1. A third party RFID tag was detected."
        },
        {
          "ecode": "0706210000010082",
          "intro": "Failed to read the filament information from AMS G slot 2. A third party RFID tag was detected."
        },
        {
          "ecode": "0706200000010082",
          "intro": "Failed to read the filament information from AMS G slot 1. A third party RFID tag was detected."
        },
        {
          "ecode": "1801220000010082",
          "intro": "Failed to read the filament information from AMS-HT B slot 3. A third party RFID tag was detected."
        },
        {
          "ecode": "0703230000010082",
          "intro": "Failed to read the filament information from AMS D slot 4. A third party RFID tag was detected."
        },
        {
          "ecode": "0700220000010082",
          "intro": "Failed to read the filament information from AMS A slot 3. A third party RFID tag was detected."
        },
        {
          "ecode": "1801210000010082",
          "intro": "Failed to read the filament information from AMS-HT B slot 2. A third party RFID tag was detected."
        },
        {
          "ecode": "0704210000010082",
          "intro": "Failed to read the filament information from AMS E slot 2. A third party RFID tag was detected."
        },
        {
          "ecode": "0584040000010045",
          "intro": "The firmware of AMS-HT E does not match the printer. Please update it on the \"Firmware\" page."
        },
        {
          "ecode": "0501040000010044",
          "intro": "The firmware of AMS B does not match the printer. Please update it on the \"Firmware\" page."
        },
        {
          "ecode": "0585040000010045",
          "intro": "The firmware of AMS-HT F does not match the printer. Please update it on the \"Firmware\" page."
        },
        {
          "ecode": "0503040000010044",
          "intro": "The firmware of AMS D does not match the printer. Please update it on the \"Firmware\" page."
        },
        {
          "ecode": "0502040000010044",
          "intro": "The firmware of AMS C does not match the printer. Please update it on the \"Firmware\" page."
        },
        {
          "ecode": "0586040000010045",
          "intro": "The firmware of AMS-HT G does not match the printer. Please update it on the \"Firmware\" page."
        },
        {
          "ecode": "0583040000010045",
          "intro": "The firmware of AMS-HT D does not match the printer. Please update it on the \"Firmware\" page."
        },
        {
          "ecode": "0580040000010045",
          "intro": "The firmware of AMS-HT A does not match the printer. Please update it on the \"Firmware\" page."
        },
        {
          "ecode": "0587040000010045",
          "intro": "The firmware of AMS-HT H does not match the printer. Please update it on the \"Firmware\" page."
        },
        {
          "ecode": "0500040000010044",
          "intro": "The firmware of AMS A does not match the printer. Please update it on the \"Firmware\" page."
        },
        {
          "ecode": "0582040000010045",
          "intro": "The firmware of AMS-HT C does not match the printer. Please update it on the \"Firmware\" page."
        },
        {
          "ecode": "0581040000010045",
          "intro": "The firmware of AMS-HT B does not match the printer. Please update it on the \"Firmware\" page."
        },
        {
          "ecode": "0581050000010010",
          "intro": "The firmware of AMS-HT B does not match the printer. Please update it on the \"Firmware\" page."
        },
        {
          "ecode": "0504050000010010",
          "intro": "The firmware of AMS E does not match the printer. Please update it on the \"Firmware\" page."
        },
        {
          "ecode": "0580050000010010",
          "intro": "The firmware of AMS-HT A does not match the printer. Please update it on the \"Firmware\" page."
        },
        {
          "ecode": "0500010000020002",
          "intro": "Liveview camera is not connected. Please check the hardware and cable connections."
        },
        {
          "ecode": "0502050000010010",
          "intro": "The firmware of AMS C does not match the printer. Please update it on the \"Firmware\" page."
        },
        {
          "ecode": "0C0003000002000C",
          "intro": "The build plate localization marker was not detected. Please check if the build plate is aligned correctly"
        },
        {
          "ecode": "0501050000010010",
          "intro": "The firmware of AMS B does not match the printer. Please update it on the \"Firmware\" page."
        },
        {
          "ecode": "050005000001000F",
          "intro": "The accessory firmware does not match the printer. Please update it on the \"Firmware\" page."
        },
        {
          "ecode": "0586050000010010",
          "intro": "The firmware of AMS-HT G does not match the printer. Please update it on the \"Firmware\" page."
        },
        {
          "ecode": "0505050000010010",
          "intro": "The firmware of AMS F does not match the printer. Please update it on the \"Firmware\" page."
        },
        {
          "ecode": "0500050000010010",
          "intro": "The firmware of AMS A does not match the printer. Please update it on the \"Firmware\" page."
        },
        {
          "ecode": "0503050000010010",
          "intro": "The firmware of AMS D does not match the printer. Please update it on the \"Firmware\" page."
        },
        {
          "ecode": "0506050000010010",
          "intro": "The firmware of AMS G does not match the printer. Please update it on the \"Firmware\" page."
        },
        {
          "ecode": "0582050000010010",
          "intro": "The firmware of AMS-HT C does not match the printer. Please update it on the \"Firmware\" page."
        },
        {
          "ecode": "0583050000010010",
          "intro": "The firmware of AMS-HT D does not match the printer. Please update it on the \"Firmware\" page."
        },
        {
          "ecode": "12FF200000030007",
          "intro": "Checking the filament location of all AMS slots; please wait."
        },
        {
          "ecode": "0507050000010010",
          "intro": "The firmware of AMS H does not match the printer. Please update it on the \"Firmware\" page."
        },
        {
          "ecode": "0584050000010010",
          "intro": "The firmware of AMS-HT E does not match the printer. Please update it on the \"Firmware\" page."
        },
        {
          "ecode": "0587050000010010",
          "intro": "The firmware of AMS-HT H does not match the printer. Please update it on the \"Firmware\" page."
        },
        {
          "ecode": "0585050000010010",
          "intro": "The firmware of AMS-HT F does not match the printer. Please update it on the \"Firmware\" page."
        },
        {
          "ecode": "050003000002000D",
          "intro": "The SD Card controller is malfunctioning."
        },
        {
          "ecode": "0C0003000001000A",
          "intro": "Your printer is in factory mode. Please contact Technical Support."
        },
        {
          "ecode": "0C00020000010005",
          "intro": "A new Micro Lidar was detected. Please calibrate it on the Calibration page before use."
        },
        {
          "ecode": "0500020000020008",
          "intro": "Time synchronization failed"
        },
        {
          "ecode": "0C0003000003000B",
          "intro": "Inspecting the first layer: please wait a moment."
        },
        {
          "ecode": "0500030000020055",
          "intro": "User information has expired, please log in again."
        },
        {
          "ecode": "0500070000020201",
          "intro": ""
        },
        {
          "ecode": "0500070000020003",
          "intro": ""
        },
        {
          "ecode": "0500070000020101",
          "intro": ""
        },
        {
          "ecode": "0500070000020001",
          "intro": ""
        },
        {
          "ecode": "0500070000020002",
          "intro": ""
        },
        {
          "ecode": "0503000000030027",
          "intro": ""
        },
        {
          "ecode": "0503000000030028",
          "intro": ""
        },
        {
          "ecode": "0503000000030029",
          "intro": ""
        },
        {
          "ecode": "0501040000030002",
          "intro": "Threaded rods need lubrication now."
        },
        {
          "ecode": "0500050000010021",
          "intro": "Time-lapse kit authentication failed. Please reconnect the cable or restart the printer."
        },
        {
          "ecode": "0500050000020030",
          "intro": ""
        },
        {
          "ecode": "0C00010000020016",
          "intro": ""
        },
        {
          "ecode": "0500030000020013",
          "intro": ""
        },
        {
          "ecode": "050005000001000C",
          "intro": ""
        },
        {
          "ecode": "0500030000020014",
          "intro": ""
        },
        {
          "ecode": "0500030000020016",
          "intro": ""
        },
        {
          "ecode": "05000600000200A0",
          "intro": ""
        },
        {
          "ecode": "050005000001000A",
          "intro": ""
        },
        {
          "ecode": "05000600000200A1",
          "intro": ""
        },
        {
          "ecode": "0C0001000002001B",
          "intro": ""
        },
        {
          "ecode": "0500030000020018",
          "intro": ""
        },
        {
          "ecode": "0500060000020054",
          "intro": ""
        },
        {
          "ecode": "0500060000020062",
          "intro": ""
        },
        {
          "ecode": "0C0001000002000E",
          "intro": ""
        },
        {
          "ecode": "0500030000020012",
          "intro": ""
        },
        {
          "ecode": "0500030000020011",
          "intro": ""
        },
        {
          "ecode": "0500050000010009",
          "intro": ""
        },
        {
          "ecode": "0500060000020061",
          "intro": ""
        },
        {
          "ecode": "050005000001000B",
          "intro": ""
        },
        {
          "ecode": "0500030000020010",
          "intro": ""
        },
        {
          "ecode": "0500030000030007",
          "intro": ""
        },
        {
          "ecode": "0C0001000002001A",
          "intro": ""
        },
        {
          "ecode": "0500030000020015",
          "intro": ""
        },
        {
          "ecode": "0500030000020017",
          "intro": ""
        },
        {
          "ecode": "0500050000010008",
          "intro": ""
        },
        {
          "ecode": "0500060000020041",
          "intro": ""
        },
        {
          "ecode": "0C00010000020015",
          "intro": ""
        },
        {
          "ecode": "0500060000020044",
          "intro": ""
        },
        {
          "ecode": "0500010000020003",
          "intro": ""
        },
        {
          "ecode": "0500060000020051",
          "intro": ""
        },
        {
          "ecode": "0500030000010053",
          "intro": ""
        },
        {
          "ecode": "1800020000020002",
          "intro": "AMS-HT A The odometer has no signal. The odometer connector may have poor contact."
        },
        {
          "ecode": "0500040000010049",
          "intro": "Communication error detected with AMS, AMS lite or AMS HT. Please reconnect the module cable or restart the printer when it is idle."
        },
        {
          "ecode": "0501040000030001",
          "intro": "Carbon rods need cleaning now."
        },
        {
          "ecode": "0705250000020001",
          "intro": "AMS F uses printer power for drying during loading/printing. For better drying performance, please connect a power adapter."
        },
        {
          "ecode": "0702250000020001",
          "intro": "AMS C uses printer power for drying during loading/printing. For better drying performance, please connect a power adapter."
        },
        {
          "ecode": "0707250000020001",
          "intro": "AMS H uses printer power for drying during loading/printing. For better drying performance, please connect a power adapter."
        },
        {
          "ecode": "0700250000020001",
          "intro": "AMS A uses printer power for drying during loading/printing. For better drying performance, please connect a power adapter."
        },
        {
          "ecode": "0703250000020001",
          "intro": "AMS D uses printer power for drying during loading/printing. For better drying performance, please connect a power adapter."
        },
        {
          "ecode": "0706250000020001",
          "intro": "AMS G uses printer power for drying during loading/printing. For better drying performance, please connect a power adapter."
        },
        {
          "ecode": "0701250000020001",
          "intro": "AMS B uses printer power for drying during loading/printing. For better drying performance, please connect a power adapter."
        },
        {
          "ecode": "0704250000020001",
          "intro": "AMS E uses printer power for drying during loading/printing. For better drying performance, please connect a power adapter."
        },
        {
          "ecode": "1802250000020001",
          "intro": "AMS-HT C uses printer power for drying during loading/printing. For better drying performance, please connect a power adapter."
        },
        {
          "ecode": "1805250000020001",
          "intro": "AMS-HT F uses printer power for drying during loading/printing. For better drying performance, please connect a power adapter."
        },
        {
          "ecode": "1807960000020004",
          "intro": "AMS-HT H The temperature control error is too large, which may be due to the lid being open or an abnormality with the heater."
        },
        {
          "ecode": "1801250000020001",
          "intro": "AMS-HT B uses printer power for drying during loading/printing. For better drying performance, please connect a power adapter."
        },
        {
          "ecode": "1802960000020004",
          "intro": "AMS-HT C The temperature control error is too large, which may be due to the lid being open or an abnormality with the heater."
        },
        {
          "ecode": "0702960000020004",
          "intro": "AMS C The temperature control error is too large, which may be due to the lid being open or an abnormality with the heater."
        },
        {
          "ecode": "1804250000020001",
          "intro": "AMS-HT E uses printer power for drying during loading/printing. For better drying performance, please connect a power adapter."
        },
        {
          "ecode": "0704960000020004",
          "intro": "AMS E The temperature control error is too large, which may be due to the lid being open or an abnormality with the heater."
        },
        {
          "ecode": "0706960000020004",
          "intro": "AMS G The temperature control error is too large, which may be due to the lid being open or an abnormality with the heater."
        },
        {
          "ecode": "0705960000020004",
          "intro": "AMS F The temperature control error is too large, which may be due to the lid being open or an abnormality with the heater."
        },
        {
          "ecode": "1800960000020004",
          "intro": "AMS-HT A The temperature control error is too large, which may be due to the lid being open or an abnormality with the heater."
        },
        {
          "ecode": "0701960000020004",
          "intro": "AMS B The temperature control error is too large, which may be due to the lid being open or an abnormality with the heater."
        },
        {
          "ecode": "1801960000020004",
          "intro": "AMS-HT B The temperature control error is too large, which may be due to the lid being open or an abnormality with the heater."
        },
        {
          "ecode": "1805960000020004",
          "intro": "AMS-HT F The temperature control error is too large, which may be due to the lid being open or an abnormality with the heater."
        },
        {
          "ecode": "1800250000020001",
          "intro": "AMS-HT A uses printer power for drying during loading/printing. For better drying performance, please connect a power adapter."
        },
        {
          "ecode": "1806960000020004",
          "intro": "AMS-HT G The temperature control error is too large, which may be due to the lid being open or an abnormality with the heater."
        },
        {
          "ecode": "0700960000020004",
          "intro": "AMS A The temperature control error is too large, which may be due to the lid being open or an abnormality with the heater."
        },
        {
          "ecode": "0703960000020004",
          "intro": "AMS D The temperature control error is too large, which may be due to the lid being open or an abnormality with the heater."
        },
        {
          "ecode": "1803250000020001",
          "intro": "AMS-HT D uses printer power for drying during loading/printing. For better drying performance, please connect a power adapter."
        },
        {
          "ecode": "1803960000020004",
          "intro": "AMS-HT D The temperature control error is too large, which may be due to the lid being open or an abnormality with the heater."
        },
        {
          "ecode": "1807250000020001",
          "intro": "AMS-HT H uses printer power for drying during loading/printing. For better drying performance, please connect a power adapter."
        },
        {
          "ecode": "0707960000020004",
          "intro": "AMS H The temperature control error is too large, which may be due to the lid being open or an abnormality with the heater."
        },
        {
          "ecode": "1806250000020001",
          "intro": "AMS-HT G uses printer power for drying during loading/printing. For better drying performance, please connect a power adapter."
        },
        {
          "ecode": "1804960000020004",
          "intro": "AMS-HT E The temperature control error is too large, which may be due to the lid being open or an abnormality with the heater."
        },
        {
          "ecode": "0700910000010004",
          "intro": "The current sensor of AMS A exhaust valve 2 is abnormal; please get in touch with customer support to replace the AMS mainboard."
        },
        {
          "ecode": "0702900000010004",
          "intro": "The current sensor of AMS C exhaust valve 1 is abnormal; please get in touch with customer support to replace the AMS mainboard."
        },
        {
          "ecode": "0706910000010004",
          "intro": "The current sensor of AMS G exhaust valve 2 is abnormal; please get in touch with customer support to replace the AMS mainboard."
        },
        {
          "ecode": "0701910000010004",
          "intro": "The current sensor of AMS B exhaust valve 2 is abnormal; please get in touch with customer support to replace the AMS mainboard."
        },
        {
          "ecode": "1801910000010004",
          "intro": "The current sensor of AMS-HT B exhaust valve 2 is abnormal; please get in touch with customer support to replace the AMS-HT mainboard."
        },
        {
          "ecode": "1806910000010004",
          "intro": "The current sensor of AMS-HT G exhaust valve 2 is abnormal; please get in touch with customer support to replace the AMS-HT mainboard."
        },
        {
          "ecode": "0703910000010004",
          "intro": "The current sensor of AMS D exhaust valve 2 is abnormal; please get in touch with customer support to replace the AMS mainboard."
        },
        {
          "ecode": "0700900000010004",
          "intro": "The current sensor of AMS A exhaust valve 1 is abnormal; please get in touch with customer support to replace the AMS mainboard."
        },
        {
          "ecode": "0704910000010004",
          "intro": "The current sensor of AMS E exhaust valve 2 is abnormal; please get in touch with customer support to replace the AMS mainboard."
        },
        {
          "ecode": "0705910000010004",
          "intro": "The current sensor of AMS F exhaust valve 2 is abnormal; please get in touch with customer support to replace the AMS mainboard."
        },
        {
          "ecode": "0702910000010004",
          "intro": "The current sensor of AMS C exhaust valve 2 is abnormal; please get in touch with customer support to replace the AMS mainboard."
        },
        {
          "ecode": "0703900000010004",
          "intro": "The current sensor of AMS D exhaust valve 1 is abnormal; please get in touch with customer support to replace the AMS mainboard."
        },
        {
          "ecode": "1801900000010004",
          "intro": "The current sensor of AMS-HT B exhaust valve 1 is abnormal; please get in touch with customer support to replace the AMS-HT mainboard."
        },
        {
          "ecode": "1807900000010004",
          "intro": "The current sensor of AMS-HT H exhaust valve 1 is abnormal; please get in touch with customer support to replace the AMS-HT mainboard."
        },
        {
          "ecode": "1802910000010004",
          "intro": "The current sensor of AMS-HT C exhaust valve 2 is abnormal; please get in touch with customer support to replace the AMS-HT mainboard."
        },
        {
          "ecode": "0701900000010004",
          "intro": "The current sensor of AMS B exhaust valve 1 is abnormal; please get in touch with customer support to replace the AMS mainboard."
        },
        {
          "ecode": "0707910000010004",
          "intro": "The current sensor of AMS H exhaust valve 2 is abnormal; please get in touch with customer support to replace the AMS mainboard."
        },
        {
          "ecode": "1803900000010004",
          "intro": "The current sensor of AMS-HT D exhaust valve 1 is abnormal; please get in touch with customer support to replace the AMS-HT mainboard."
        },
        {
          "ecode": "1807910000010004",
          "intro": "The current sensor of AMS-HT H exhaust valve 2 is abnormal; please get in touch with customer support to replace the AMS-HT mainboard."
        },
        {
          "ecode": "1800910000010004",
          "intro": "The current sensor of AMS-HT A exhaust valve 2 is abnormal; please get in touch with customer support to replace the AMS-HT mainboard."
        },
        {
          "ecode": "1800900000010004",
          "intro": "The current sensor of AMS-HT A exhaust valve 1 is abnormal; please get in touch with customer support to replace the AMS-HT mainboard."
        },
        {
          "ecode": "0704900000010004",
          "intro": "The current sensor of AMS E exhaust valve 1 is abnormal; please get in touch with customer support to replace the AMS mainboard."
        },
        {
          "ecode": "1803910000010004",
          "intro": "The current sensor of AMS-HT D exhaust valve 2 is abnormal; please get in touch with customer support to replace the AMS-HT mainboard."
        },
        {
          "ecode": "0705900000010004",
          "intro": "The current sensor of AMS F exhaust valve 1 is abnormal; please get in touch with customer support to replace the AMS mainboard."
        },
        {
          "ecode": "1805900000010004",
          "intro": "The current sensor of AMS-HT F exhaust valve 1 is abnormal; please get in touch with customer support to replace the AMS-HT mainboard."
        },
        {
          "ecode": "0706900000010004",
          "intro": "The current sensor of AMS G exhaust valve 1 is abnormal; please get in touch with customer support to replace the AMS mainboard."
        },
        {
          "ecode": "1804900000010004",
          "intro": "The current sensor of AMS-HT E exhaust valve 1 is abnormal; please get in touch with customer support to replace the AMS-HT mainboard."
        },
        {
          "ecode": "0707900000010004",
          "intro": "The current sensor of AMS H exhaust valve 1 is abnormal; please get in touch with customer support to replace the AMS mainboard."
        },
        {
          "ecode": "1802900000010004",
          "intro": "The current sensor of AMS-HT C exhaust valve 1 is abnormal; please get in touch with customer support to replace the AMS-HT mainboard."
        },
        {
          "ecode": "1805910000010004",
          "intro": "The current sensor of AMS-HT F exhaust valve 2 is abnormal; please get in touch with customer support to replace the AMS-HT mainboard."
        },
        {
          "ecode": "1804910000010004",
          "intro": "The current sensor of AMS-HT E exhaust valve 2 is abnormal; please get in touch with customer support to replace the AMS-HT mainboard."
        },
        {
          "ecode": "1806900000010004",
          "intro": "The current sensor of AMS-HT G exhaust valve 1 is abnormal; please get in touch with customer support to replace the AMS-HT mainboard."
        },
        {
          "ecode": "0701610000020001",
          "intro": "The AMS B Slot 2 is overloaded. The filament may be tangled or the filament buffer may be stuck."
        },
        {
          "ecode": "0703600000020001",
          "intro": "The AMS D Slot 1 is overloaded. The filament may be tangled or the filament buffer may be stuck."
        },
        {
          "ecode": "1801610000020001",
          "intro": "The AMS-HT B Slot 2 is overloaded. The filament may be tangled or the filament buffer may be stuck."
        },
        {
          "ecode": "1805630000020001",
          "intro": "The AMS-HT F Slot 4 is overloaded. The filament may be tangled or the filament buffer may be stuck."
        },
        {
          "ecode": "0705610000020001",
          "intro": "The AMS F Slot 2 is overloaded. The filament may be tangled or the filament buffer may be stuck."
        },
        {
          "ecode": "1807620000020001",
          "intro": "The AMS-HT H Slot 3 is overloaded. The filament may be tangled or the filament buffer may be stuck."
        },
        {
          "ecode": "0703620000020001",
          "intro": "The AMS D Slot 3 is overloaded. The filament may be tangled or the filament buffer may be stuck."
        },
        {
          "ecode": "1802600000020001",
          "intro": "The AMS-HT C Slot 1 is overloaded. The filament may be tangled or the filament buffer may be stuck."
        },
        {
          "ecode": "0707620000020001",
          "intro": "The AMS H Slot 3 is overloaded. The filament may be tangled or the filament buffer may be stuck."
        },
        {
          "ecode": "1800600000020001",
          "intro": "The AMS-HT A Slot 1 is overloaded. The filament may be tangled or the filament buffer may be stuck."
        },
        {
          "ecode": "1800620000020001",
          "intro": "The AMS-HT A Slot 3 is overloaded. The filament may be tangled or the filament buffer may be stuck."
        },
        {
          "ecode": "1800610000020001",
          "intro": "The AMS-HT A Slot 2 is overloaded. The filament may be tangled or the filament buffer may be stuck."
        },
        {
          "ecode": "0700630000020001",
          "intro": "The AMS A Slot 4 is overloaded. The filament may be tangled or the filament buffer may be stuck."
        },
        {
          "ecode": "0702630000020001",
          "intro": "The AMS C Slot 4 is overloaded. The filament may be tangled or the filament buffer may be stuck."
        },
        {
          "ecode": "0701620000020001",
          "intro": "The AMS B Slot 3 is overloaded. The filament may be tangled or the filament buffer may be stuck."
        },
        {
          "ecode": "0706620000020001",
          "intro": "The AMS G Slot 3 is overloaded. The filament may be tangled or the filament buffer may be stuck."
        },
        {
          "ecode": "0702620000020001",
          "intro": "The AMS C Slot 3 is overloaded. The filament may be tangled or the filament buffer may be stuck."
        },
        {
          "ecode": "0704600000020001",
          "intro": "The AMS E Slot 1 is overloaded. The filament may be tangled or the filament buffer may be stuck."
        },
        {
          "ecode": "0700600000020001",
          "intro": "The AMS A Slot 1 is overloaded. The filament may be tangled or the filament buffer may be stuck."
        },
        {
          "ecode": "1805620000020001",
          "intro": "The AMS-HT F Slot 3 is overloaded. The filament may be tangled or the filament buffer may be stuck."
        },
        {
          "ecode": "1802630000020001",
          "intro": "The AMS-HT C Slot 4 is overloaded. The filament may be tangled or the filament buffer may be stuck."
        },
        {
          "ecode": "0700610000020001",
          "intro": "The AMS A Slot 2 is overloaded. The filament may be tangled or the filament buffer may be stuck."
        },
        {
          "ecode": "0707600000020001",
          "intro": "The AMS H Slot 1 is overloaded. The filament may be tangled or the filament buffer may be stuck."
        },
        {
          "ecode": "1803610000020001",
          "intro": "The AMS-HT D Slot 2 is overloaded. The filament may be tangled or the filament buffer may be stuck."
        },
        {
          "ecode": "0706610000020001",
          "intro": "The AMS G Slot 2 is overloaded. The filament may be tangled or the filament buffer may be stuck."
        },
        {
          "ecode": "1800630000020001",
          "intro": "The AMS-HT A Slot 4 is overloaded. The filament may be tangled or the filament buffer may be stuck."
        },
        {
          "ecode": "0702610000020001",
          "intro": "The AMS C Slot 2 is overloaded. The filament may be tangled or the filament buffer may be stuck."
        },
        {
          "ecode": "1803600000020001",
          "intro": "The AMS-HT D Slot 1 is overloaded. The filament may be tangled or the filament buffer may be stuck."
        },
        {
          "ecode": "0703630000020001",
          "intro": "The AMS D Slot 4 is overloaded. The filament may be tangled or the filament buffer may be stuck."
        },
        {
          "ecode": "1805610000020001",
          "intro": "The AMS-HT F Slot 2 is overloaded. The filament may be tangled or the filament buffer may be stuck."
        },
        {
          "ecode": "0700620000020001",
          "intro": "The AMS A Slot 3 is overloaded. The filament may be tangled or the filament buffer may be stuck."
        },
        {
          "ecode": "1806610000020001",
          "intro": "The AMS-HT G Slot 2 is overloaded. The filament may be tangled or the filament buffer may be stuck."
        },
        {
          "ecode": "1803620000020001",
          "intro": "The AMS-HT D Slot 3 is overloaded. The filament may be tangled or the filament buffer may be stuck."
        },
        {
          "ecode": "1801630000020001",
          "intro": "The AMS-HT B Slot 4 is overloaded. The filament may be tangled or the filament buffer may be stuck."
        },
        {
          "ecode": "0706630000020001",
          "intro": "The AMS G Slot 4 is overloaded. The filament may be tangled or the filament buffer may be stuck."
        },
        {
          "ecode": "1806600000020001",
          "intro": "The AMS-HT G Slot 1 is overloaded. The filament may be tangled or the filament buffer may be stuck."
        },
        {
          "ecode": "1806630000020001",
          "intro": "The AMS-HT G Slot 4 is overloaded. The filament may be tangled or the filament buffer may be stuck."
        },
        {
          "ecode": "0701600000020001",
          "intro": "The AMS B Slot 1 is overloaded. The filament may be tangled or the filament buffer may be stuck."
        },
        {
          "ecode": "1807600000020001",
          "intro": "The AMS-HT H Slot 1 is overloaded. The filament may be tangled or the filament buffer may be stuck."
        },
        {
          "ecode": "1801620000020001",
          "intro": "The AMS-HT B Slot 3 is overloaded. The filament may be tangled or the filament buffer may be stuck."
        },
        {
          "ecode": "1807610000020001",
          "intro": "The AMS-HT H Slot 2 is overloaded. The filament may be tangled or the filament buffer may be stuck."
        },
        {
          "ecode": "0705630000020001",
          "intro": "The AMS F Slot 4 is overloaded. The filament may be tangled or the filament buffer may be stuck."
        },
        {
          "ecode": "0704610000020001",
          "intro": "The AMS E Slot 2 is overloaded. The filament may be tangled or the filament buffer may be stuck."
        },
        {
          "ecode": "0701630000020001",
          "intro": "The AMS B Slot 4 is overloaded. The filament may be tangled or the filament buffer may be stuck."
        },
        {
          "ecode": "0705600000020001",
          "intro": "The AMS F Slot 1 is overloaded. The filament may be tangled or the filament buffer may be stuck."
        },
        {
          "ecode": "1803630000020001",
          "intro": "The AMS-HT D Slot 4 is overloaded. The filament may be tangled or the filament buffer may be stuck."
        },
        {
          "ecode": "1804600000020001",
          "intro": "The AMS-HT E Slot 1 is overloaded. The filament may be tangled or the filament buffer may be stuck."
        },
        {
          "ecode": "0703610000020001",
          "intro": "The AMS D Slot 2 is overloaded. The filament may be tangled or the filament buffer may be stuck."
        },
        {
          "ecode": "1804620000020001",
          "intro": "The AMS-HT E Slot 3 is overloaded. The filament may be tangled or the filament buffer may be stuck."
        },
        {
          "ecode": "1802620000020001",
          "intro": "The AMS-HT C Slot 3 is overloaded. The filament may be tangled or the filament buffer may be stuck."
        },
        {
          "ecode": "0705620000020001",
          "intro": "The AMS F Slot 3 is overloaded. The filament may be tangled or the filament buffer may be stuck."
        },
        {
          "ecode": "1804630000020001",
          "intro": "The AMS-HT E Slot 4 is overloaded. The filament may be tangled or the filament buffer may be stuck."
        },
        {
          "ecode": "1805600000020001",
          "intro": "The AMS-HT F Slot 1 is overloaded. The filament may be tangled or the filament buffer may be stuck."
        },
        {
          "ecode": "1806620000020001",
          "intro": "The AMS-HT G Slot 3 is overloaded. The filament may be tangled or the filament buffer may be stuck."
        },
        {
          "ecode": "0704620000020001",
          "intro": "The AMS E Slot 3 is overloaded. The filament may be tangled or the filament buffer may be stuck."
        },
        {
          "ecode": "0702600000020001",
          "intro": "The AMS C Slot 1 is overloaded. The filament may be tangled or the filament buffer may be stuck."
        },
        {
          "ecode": "0704630000020001",
          "intro": "The AMS E Slot 4 is overloaded. The filament may be tangled or the filament buffer may be stuck."
        },
        {
          "ecode": "0706600000020001",
          "intro": "The AMS G Slot 1 is overloaded. The filament may be tangled or the filament buffer may be stuck."
        },
        {
          "ecode": "1804610000020001",
          "intro": "The AMS-HT E Slot 2 is overloaded. The filament may be tangled or the filament buffer may be stuck."
        },
        {
          "ecode": "1801600000020001",
          "intro": "The AMS-HT B Slot 1 is overloaded. The filament may be tangled or the filament buffer may be stuck."
        },
        {
          "ecode": "1802610000020001",
          "intro": "The AMS-HT C Slot 2 is overloaded. The filament may be tangled or the filament buffer may be stuck."
        },
        {
          "ecode": "1807630000020001",
          "intro": "The AMS-HT H Slot 4 is overloaded. The filament may be tangled or the filament buffer may be stuck."
        },
        {
          "ecode": "0707630000020001",
          "intro": "The AMS H Slot 4 is overloaded. The filament may be tangled or the filament buffer may be stuck."
        },
        {
          "ecode": "0707610000020001",
          "intro": "The AMS H Slot 2 is overloaded. The filament may be tangled or the filament buffer may be stuck."
        },
        {
          "ecode": "050003000002000E",
          "intro": "Some modules are incompatible with the printer's firmware version, which may affect use. Please go to the \"Firmware\" page to update after connected to the internet, or you may update offline according to wiki."
        },
        {
          "ecode": "0500050000010007",
          "intro": "MQTT Command verification failed. Please update Studio (including the network plugin) or Handy to the latest version, then restart the software and try again."
        },
        {
          "ecode": "0701230000020012",
          "intro": "AMS B slot 4 feeder unit motor is stalled, cannot rotate the spool."
        },
        {
          "ecode": "0703210000020013",
          "intro": "AMS D slot 2 feeder unit motor has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "1803210000020015",
          "intro": "AMS-HT D slot 2 filament status is abnormal, which may be due to a filament breakage inside the AMS."
        },
        {
          "ecode": "0701220000020016",
          "intro": "AMS B slot 3 assist motor has slipped. Please pull out the filament, cut off the worn part, and then try again."
        },
        {
          "ecode": "1807200000020015",
          "intro": "AMS-HT H slot 1 filament status is abnormal, which may be due to a filament breakage inside the AMS."
        },
        {
          "ecode": "0706230000020015",
          "intro": "AMS G slot 4 filament status is abnormal, which may be due to a filament breakage inside the AMS."
        },
        {
          "ecode": "0705200000020015",
          "intro": "AMS F slot 1 filament status is abnormal, which may be due to a filament breakage inside the AMS."
        },
        {
          "ecode": "1801210000020012",
          "intro": "AMS-HT B slot 2 feeder unit motor is stalled, cannot rotate the spool."
        },
        {
          "ecode": "1805220000020015",
          "intro": "AMS-HT F slot 3 filament status is abnormal, which may be due to a filament breakage inside the AMS."
        },
        {
          "ecode": "0702200000020015",
          "intro": "AMS C slot 1 filament status is abnormal, which may be due to a filament breakage inside the AMS."
        },
        {
          "ecode": "1807200000020013",
          "intro": "AMS-HT H slot 1 feeder unit motor has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "0707200000020012",
          "intro": "AMS H slot 1 feeder unit motor is stalled, cannot rotate the spool."
        },
        {
          "ecode": "1806210000020013",
          "intro": "AMS-HT G slot 2 feeder unit motor has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "0703200000020006",
          "intro": "AMS D has detected a breakage of the PTFE tube during filament loading. Please check whether the PTFE tubes inside and outside the AMS have fallen off or been damaged."
        },
        {
          "ecode": "0701200000020012",
          "intro": "AMS B slot 1 feeder unit motor is stalled, cannot rotate the spool."
        },
        {
          "ecode": "0700220000020014",
          "intro": "AMS A slot 3 filament odometer has no signal, which may be due to poor contact in the odometer connector or a odometer fault."
        },
        {
          "ecode": "0702200000020006",
          "intro": "AMS C has detected a breakage of the PTFE tube during filament loading. Please check whether the PTFE tubes inside and outside the AMS have fallen off or been damaged."
        },
        {
          "ecode": "1805210000020016",
          "intro": "AMS-HT F slot 2 assist motor has slipped. Please pull out the filament, cut off the worn part, and then try again."
        },
        {
          "ecode": "1805210000020014",
          "intro": "AMS-HT F slot 2 filament odometer has no signal, which may be due to poor contact in the odometer connector or a odometer fault."
        },
        {
          "ecode": "0705200000020016",
          "intro": "AMS F slot 1 assist motor has slipped. Please pull out the filament, cut off the worn part, and then try again."
        },
        {
          "ecode": "1806230000020013",
          "intro": "AMS-HT G slot 4 feeder unit motor has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "1802220000020016",
          "intro": "AMS-HT C slot 3 assist motor has slipped. Please pull out the filament, cut off the worn part, and then try again."
        },
        {
          "ecode": "1801200000020014",
          "intro": "AMS-HT B slot 1 filament odometer has no signal, which may be due to poor contact in the odometer connector or a odometer fault."
        },
        {
          "ecode": "1802210000020012",
          "intro": "AMS-HT C slot 2 feeder unit motor is stalled, cannot rotate the spool."
        },
        {
          "ecode": "1800210000020014",
          "intro": "AMS-HT A slot 2 filament odometer has no signal, which may be due to poor contact in the odometer connector or a odometer fault."
        },
        {
          "ecode": "1802200000020012",
          "intro": "AMS-HT C slot 1 feeder unit motor is stalled, cannot rotate the spool."
        },
        {
          "ecode": "1801230000020015",
          "intro": "AMS-HT B slot 4 filament status is abnormal, which may be due to a filament breakage inside the AMS."
        },
        {
          "ecode": "0700220000020013",
          "intro": "AMS A slot 3 feeder unit motor has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "1804210000020012",
          "intro": "AMS-HT E slot 2 feeder unit motor is stalled, cannot rotate the spool."
        },
        {
          "ecode": "1805200000020015",
          "intro": "AMS-HT F slot 1 filament status is abnormal, which may be due to a filament breakage inside the AMS."
        },
        {
          "ecode": "0703200000020012",
          "intro": "AMS D slot 1 feeder unit motor is stalled, cannot rotate the spool."
        },
        {
          "ecode": "1803230000020012",
          "intro": "AMS-HT D slot 4 feeder unit motor is stalled, cannot rotate the spool."
        },
        {
          "ecode": "1801200000020025",
          "intro": "AMS-HT B slot 1 feed resistance is too high. Please reduce the feed resistance, decrease the rotation resistance of the spool, and avoid having the filament tube too long and excessively bent."
        },
        {
          "ecode": "1805210000020025",
          "intro": "AMS-HT F slot 2 feed resistance is too high. Please reduce the feed resistance, decrease the rotation resistance of the spool, and avoid having the filament tube too long and excessively bent."
        },
        {
          "ecode": "1801220000020025",
          "intro": "AMS-HT B slot 3 feed resistance is too high. Please reduce the feed resistance, decrease the rotation resistance of the spool, and avoid having the filament tube too long and excessively bent."
        },
        {
          "ecode": "0704210000020025",
          "intro": "AMS E slot 2 feed resistance is too high. Please reduce the feed resistance, decrease the rotation resistance of the spool, and avoid having the filament tube too long and excessively bent."
        },
        {
          "ecode": "1800210000020025",
          "intro": "AMS-HT A slot 2 feed resistance is too high. Please reduce the feed resistance, decrease the rotation resistance of the spool, and avoid having the filament tube too long and excessively bent."
        },
        {
          "ecode": "1800200000020025",
          "intro": "AMS-HT A slot 1 feed resistance is too high. Please reduce the feed resistance, decrease the rotation resistance of the spool, and avoid having the filament tube too long and excessively bent."
        },
        {
          "ecode": "0700210000020025",
          "intro": "AMS A slot 2 feed resistance is too high. Please reduce the feed resistance, decrease the rotation resistance of the spool, and avoid having the filament tube too long and excessively bent."
        },
        {
          "ecode": "1802220000020006",
          "intro": "AMS-HT C has detected a breakage of the PTFE tube during filament loading. Please check whether the PTFE tubes inside and outside the AMS have fallen off or been damaged."
        },
        {
          "ecode": "0702230000020006",
          "intro": "AMS C has detected a breakage of the PTFE tube during filament loading. Please check whether the PTFE tubes inside and outside the AMS have fallen off or been damaged."
        },
        {
          "ecode": "0705230000020006",
          "intro": "AMS F has detected a breakage of the PTFE tube during filament loading. Please check whether the PTFE tubes inside and outside the AMS have fallen off or been damaged."
        },
        {
          "ecode": "0704220000020012",
          "intro": "AMS E slot 3 feeder unit motor is stalled, cannot rotate the spool."
        },
        {
          "ecode": "0704220000020016",
          "intro": "AMS E slot 3 assist motor has slipped. Please pull out the filament, cut off the worn part, and then try again."
        },
        {
          "ecode": "1807200000020006",
          "intro": "AMS-HT H has detected a breakage of the PTFE tube during filament loading. Please check whether the PTFE tubes inside and outside the AMS have fallen off or been damaged."
        },
        {
          "ecode": "0704200000020014",
          "intro": "AMS E slot 1 filament odometer has no signal, which may be due to poor contact in the odometer connector or a odometer fault."
        },
        {
          "ecode": "1800200000020015",
          "intro": "AMS-HT A slot 1 filament status is abnormal, which may be due to a filament breakage inside the AMS."
        },
        {
          "ecode": "1806220000020015",
          "intro": "AMS-HT G slot 3 filament status is abnormal, which may be due to a filament breakage inside the AMS."
        },
        {
          "ecode": "0704200000020016",
          "intro": "AMS E slot 1 assist motor has slipped. Please pull out the filament, cut off the worn part, and then try again."
        },
        {
          "ecode": "1805210000020012",
          "intro": "AMS-HT F slot 2 feeder unit motor is stalled, cannot rotate the spool."
        },
        {
          "ecode": "1804210000020014",
          "intro": "AMS-HT E slot 2 filament odometer has no signal, which may be due to poor contact in the odometer connector or a odometer fault."
        },
        {
          "ecode": "0700200000020012",
          "intro": "AMS A slot 1 feeder unit motor is stalled, cannot rotate the spool."
        },
        {
          "ecode": "0704230000020012",
          "intro": "AMS E slot 4 feeder unit motor is stalled, cannot rotate the spool."
        },
        {
          "ecode": "0706210000020016",
          "intro": "AMS G slot 2 assist motor has slipped. Please pull out the filament, cut off the worn part, and then try again."
        },
        {
          "ecode": "1807210000020012",
          "intro": "AMS-HT H slot 2 feeder unit motor is stalled, cannot rotate the spool."
        },
        {
          "ecode": "1804220000020015",
          "intro": "AMS-HT E slot 3 filament status is abnormal, which may be due to a filament breakage inside the AMS."
        },
        {
          "ecode": "0700210000020014",
          "intro": "AMS A slot 2 filament odometer has no signal, which may be due to poor contact in the odometer connector or a odometer fault."
        },
        {
          "ecode": "0702200000020012",
          "intro": "AMS C slot 1 feeder unit motor is stalled, cannot rotate the spool."
        },
        {
          "ecode": "0705220000020012",
          "intro": "AMS F slot 3 feeder unit motor is stalled, cannot rotate the spool."
        },
        {
          "ecode": "1803200000020012",
          "intro": "AMS-HT D slot 1 feeder unit motor is stalled, cannot rotate the spool."
        },
        {
          "ecode": "1806200000020014",
          "intro": "AMS-HT G slot 1 filament odometer has no signal, which may be due to poor contact in the odometer connector or a odometer fault."
        },
        {
          "ecode": "0700230000020016",
          "intro": "AMS A slot 4 assist motor has slipped. Please pull out the filament, cut off the worn part, and then try again."
        },
        {
          "ecode": "0705200000020013",
          "intro": "AMS F slot 1 feeder unit motor has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "1804200000020012",
          "intro": "AMS-HT E slot 1 feeder unit motor is stalled, cannot rotate the spool."
        },
        {
          "ecode": "1805230000020015",
          "intro": "AMS-HT F slot 4 filament status is abnormal, which may be due to a filament breakage inside the AMS."
        },
        {
          "ecode": "0707220000020015",
          "intro": "AMS H slot 3 filament status is abnormal, which may be due to a filament breakage inside the AMS."
        },
        {
          "ecode": "1804230000020015",
          "intro": "AMS-HT E slot 4 filament status is abnormal, which may be due to a filament breakage inside the AMS."
        },
        {
          "ecode": "1806200000020015",
          "intro": "AMS-HT G slot 1 filament status is abnormal, which may be due to a filament breakage inside the AMS."
        },
        {
          "ecode": "1801210000020015",
          "intro": "AMS-HT B slot 2 filament status is abnormal, which may be due to a filament breakage inside the AMS."
        },
        {
          "ecode": "0702220000020016",
          "intro": "AMS C slot 3 assist motor has slipped. Please pull out the filament, cut off the worn part, and then try again."
        },
        {
          "ecode": "1807210000020013",
          "intro": "AMS-HT H slot 2 feeder unit motor has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "0704230000020014",
          "intro": "AMS E slot 4 filament odometer has no signal, which may be due to poor contact in the odometer connector or a odometer fault."
        },
        {
          "ecode": "1803200000020006",
          "intro": "AMS-HT D has detected a breakage of the PTFE tube during filament loading. Please check whether the PTFE tubes inside and outside the AMS have fallen off or been damaged."
        },
        {
          "ecode": "0701210000020014",
          "intro": "AMS B slot 2 filament odometer has no signal, which may be due to poor contact in the odometer connector or a odometer fault."
        },
        {
          "ecode": "0707210000020013",
          "intro": "AMS H slot 2 feeder unit motor has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "0704220000020015",
          "intro": "AMS E slot 3 filament status is abnormal, which may be due to a filament breakage inside the AMS."
        },
        {
          "ecode": "1800200000020012",
          "intro": "AMS-HT A slot 1 feeder unit motor is stalled, cannot rotate the spool."
        },
        {
          "ecode": "0700230000020015",
          "intro": "AMS A slot 4 filament status is abnormal, which may be due to a filament breakage inside the AMS."
        },
        {
          "ecode": "1801220000020012",
          "intro": "AMS-HT B slot 3 feeder unit motor is stalled, cannot rotate the spool."
        },
        {
          "ecode": "0701220000020014",
          "intro": "AMS B slot 3 filament odometer has no signal, which may be due to poor contact in the odometer connector or a odometer fault."
        },
        {
          "ecode": "1805200000020006",
          "intro": "AMS-HT F has detected a breakage of the PTFE tube during filament loading. Please check whether the PTFE tubes inside and outside the AMS have fallen off or been damaged."
        },
        {
          "ecode": "0705230000020016",
          "intro": "AMS F slot 4 assist motor has slipped. Please pull out the filament, cut off the worn part, and then try again."
        },
        {
          "ecode": "0706210000020012",
          "intro": "AMS G slot 2 feeder unit motor is stalled, cannot rotate the spool."
        },
        {
          "ecode": "1800210000020013",
          "intro": "AMS-HT A slot 2 feeder unit motor has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "1805210000020015",
          "intro": "AMS-HT F slot 2 filament status is abnormal, which may be due to a filament breakage inside the AMS."
        },
        {
          "ecode": "1803220000020012",
          "intro": "AMS-HT D slot 3 feeder unit motor is stalled, cannot rotate the spool."
        },
        {
          "ecode": "1806220000020012",
          "intro": "AMS-HT G slot 3 feeder unit motor is stalled, cannot rotate the spool."
        },
        {
          "ecode": "0707220000020016",
          "intro": "AMS H slot 3 assist motor has slipped. Please pull out the filament, cut off the worn part, and then try again."
        },
        {
          "ecode": "1801210000020013",
          "intro": "AMS-HT B slot 2 feeder unit motor has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "0705210000020015",
          "intro": "AMS F slot 2 filament status is abnormal, which may be due to a filament breakage inside the AMS."
        },
        {
          "ecode": "0702230000020016",
          "intro": "AMS C slot 4 assist motor has slipped. Please pull out the filament, cut off the worn part, and then try again."
        },
        {
          "ecode": "0707200000020014",
          "intro": "AMS H slot 1 filament odometer has no signal, which may be due to poor contact in the odometer connector or a odometer fault."
        },
        {
          "ecode": "0703230000020015",
          "intro": "AMS D slot 4 filament status is abnormal, which may be due to a filament breakage inside the AMS."
        },
        {
          "ecode": "1804210000020013",
          "intro": "AMS-HT E slot 2 feeder unit motor has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "0701200000020014",
          "intro": "AMS B slot 1 filament odometer has no signal, which may be due to poor contact in the odometer connector or a odometer fault."
        },
        {
          "ecode": "1806210000020014",
          "intro": "AMS-HT G slot 2 filament odometer has no signal, which may be due to poor contact in the odometer connector or a odometer fault."
        },
        {
          "ecode": "0705230000020014",
          "intro": "AMS F slot 4 filament odometer has no signal, which may be due to poor contact in the odometer connector or a odometer fault."
        },
        {
          "ecode": "0700220000020015",
          "intro": "AMS A slot 3 filament status is abnormal, which may be due to a filament breakage inside the AMS."
        },
        {
          "ecode": "0700230000020012",
          "intro": "AMS A slot 4 feeder unit motor is stalled, cannot rotate the spool."
        },
        {
          "ecode": "1801200000020006",
          "intro": "AMS-HT B has detected a breakage of the PTFE tube during filament loading. Please check whether the PTFE tubes inside and outside the AMS have fallen off or been damaged."
        },
        {
          "ecode": "1805200000020013",
          "intro": "AMS-HT F slot 1 feeder unit motor has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "1807220000020016",
          "intro": "AMS-HT H slot 3 assist motor has slipped. Please pull out the filament, cut off the worn part, and then try again."
        },
        {
          "ecode": "0704200000020006",
          "intro": "AMS E has detected a breakage of the PTFE tube during filament loading. Please check whether the PTFE tubes inside and outside the AMS have fallen off or been damaged."
        },
        {
          "ecode": "1807220000020014",
          "intro": "AMS-HT H slot 3 filament odometer has no signal, which may be due to poor contact in the odometer connector or a odometer fault."
        },
        {
          "ecode": "1805230000020012",
          "intro": "AMS-HT F slot 4 feeder unit motor is stalled, cannot rotate the spool."
        },
        {
          "ecode": "0703230000020016",
          "intro": "AMS D slot 4 assist motor has slipped. Please pull out the filament, cut off the worn part, and then try again."
        },
        {
          "ecode": "1806200000020016",
          "intro": "AMS-HT G slot 1 assist motor has slipped. Please pull out the filament, cut off the worn part, and then try again."
        },
        {
          "ecode": "1804200000020014",
          "intro": "AMS-HT E slot 1 filament odometer has no signal, which may be due to poor contact in the odometer connector or a odometer fault."
        },
        {
          "ecode": "0704230000020015",
          "intro": "AMS E slot 4 filament status is abnormal, which may be due to a filament breakage inside the AMS."
        },
        {
          "ecode": "1802220000020014",
          "intro": "AMS-HT C slot 3 filament odometer has no signal, which may be due to poor contact in the odometer connector or a odometer fault."
        },
        {
          "ecode": "0702220000020012",
          "intro": "AMS C slot 3 feeder unit motor is stalled, cannot rotate the spool."
        },
        {
          "ecode": "1806210000020016",
          "intro": "AMS-HT G slot 2 assist motor has slipped. Please pull out the filament, cut off the worn part, and then try again."
        },
        {
          "ecode": "1805200000020012",
          "intro": "AMS-HT F slot 1 feeder unit motor is stalled, cannot rotate the spool."
        },
        {
          "ecode": "0703200000020014",
          "intro": "AMS D slot 1 filament odometer has no signal, which may be due to poor contact in the odometer connector or a odometer fault."
        },
        {
          "ecode": "0701210000020016",
          "intro": "AMS B slot 2 assist motor has slipped. Please pull out the filament, cut off the worn part, and then try again."
        },
        {
          "ecode": "1802230000020014",
          "intro": "AMS-HT C slot 4 filament odometer has no signal, which may be due to poor contact in the odometer connector or a odometer fault."
        },
        {
          "ecode": "0706210000020013",
          "intro": "AMS G slot 2 feeder unit motor has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "0702200000020016",
          "intro": "AMS C slot 1 assist motor has slipped. Please pull out the filament, cut off the worn part, and then try again."
        },
        {
          "ecode": "1800220000020015",
          "intro": "AMS-HT A slot 3 filament status is abnormal, which may be due to a filament breakage inside the AMS."
        },
        {
          "ecode": "1801220000020014",
          "intro": "AMS-HT B slot 3 filament odometer has no signal, which may be due to poor contact in the odometer connector or a odometer fault."
        },
        {
          "ecode": "0706200000020006",
          "intro": "AMS G has detected a breakage of the PTFE tube during filament loading. Please check whether the PTFE tubes inside and outside the AMS have fallen off or been damaged."
        },
        {
          "ecode": "0702230000020012",
          "intro": "AMS C slot 4 feeder unit motor is stalled, cannot rotate the spool."
        },
        {
          "ecode": "1807230000020015",
          "intro": "AMS-HT H slot 4 filament status is abnormal, which may be due to a filament breakage inside the AMS."
        },
        {
          "ecode": "0703220000020013",
          "intro": "AMS D slot 3 feeder unit motor has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "0700200000020016",
          "intro": "AMS A slot 1 assist motor has slipped. Please pull out the filament, cut off the worn part, and then try again."
        },
        {
          "ecode": "1804220000020016",
          "intro": "AMS-HT E slot 3 assist motor has slipped. Please pull out the filament, cut off the worn part, and then try again."
        },
        {
          "ecode": "1800210000020012",
          "intro": "AMS-HT A slot 2 feeder unit motor is stalled, cannot rotate the spool."
        },
        {
          "ecode": "0700210000020015",
          "intro": "AMS A slot 2 filament status is abnormal, which may be due to a filament breakage inside the AMS."
        },
        {
          "ecode": "1802220000020015",
          "intro": "AMS-HT C slot 3 filament status is abnormal, which may be due to a filament breakage inside the AMS."
        },
        {
          "ecode": "0700220000020012",
          "intro": "AMS A slot 3 feeder unit motor is stalled, cannot rotate the spool."
        },
        {
          "ecode": "1803220000020015",
          "intro": "AMS-HT D slot 3 filament status is abnormal, which may be due to a filament breakage inside the AMS."
        },
        {
          "ecode": "0707210000020012",
          "intro": "AMS H slot 2 feeder unit motor is stalled, cannot rotate the spool."
        },
        {
          "ecode": "0705200000020006",
          "intro": "AMS F has detected a breakage of the PTFE tube during filament loading. Please check whether the PTFE tubes inside and outside the AMS have fallen off or been damaged."
        },
        {
          "ecode": "1805220000020016",
          "intro": "AMS-HT F slot 3 assist motor has slipped. Please pull out the filament, cut off the worn part, and then try again."
        },
        {
          "ecode": "0701230000020013",
          "intro": "AMS B slot 4 feeder unit motor has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "0703230000020014",
          "intro": "AMS D slot 4 filament odometer has no signal, which may be due to poor contact in the odometer connector or a odometer fault."
        },
        {
          "ecode": "1806210000020015",
          "intro": "AMS-HT G slot 2 filament status is abnormal, which may be due to a filament breakage inside the AMS."
        },
        {
          "ecode": "0700200000020006",
          "intro": "AMS A has detected a breakage of the PTFE tube during filament loading. Please check whether the PTFE tubes inside and outside the AMS have fallen off or been damaged."
        },
        {
          "ecode": "1801210000020014",
          "intro": "AMS-HT B slot 2 filament odometer has no signal, which may be due to poor contact in the odometer connector or a odometer fault."
        },
        {
          "ecode": "1805200000020016",
          "intro": "AMS-HT F slot 1 assist motor has slipped. Please pull out the filament, cut off the worn part, and then try again."
        },
        {
          "ecode": "0705210000020013",
          "intro": "AMS F slot 2 feeder unit motor has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "1802200000020013",
          "intro": "AMS-HT C slot 1 feeder unit motor has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "1806220000020013",
          "intro": "AMS-HT G slot 3 feeder unit motor has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "0704220000020013",
          "intro": "AMS E slot 3 feeder unit motor has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "0705210000020016",
          "intro": "AMS F slot 2 assist motor has slipped. Please pull out the filament, cut off the worn part, and then try again."
        },
        {
          "ecode": "0704200000020015",
          "intro": "AMS E slot 1 filament status is abnormal, which may be due to a filament breakage inside the AMS."
        },
        {
          "ecode": "1804230000020014",
          "intro": "AMS-HT E slot 4 filament odometer has no signal, which may be due to poor contact in the odometer connector or a odometer fault."
        },
        {
          "ecode": "0704220000020025",
          "intro": "AMS E slot 3 feed resistance is too high. Please reduce the feed resistance, decrease the rotation resistance of the spool, and avoid having the filament tube too long and excessively bent."
        },
        {
          "ecode": "0702220000020025",
          "intro": "AMS C slot 3 feed resistance is too high. Please reduce the feed resistance, decrease the rotation resistance of the spool, and avoid having the filament tube too long and excessively bent."
        },
        {
          "ecode": "1803220000020025",
          "intro": "AMS-HT D slot 3 feed resistance is too high. Please reduce the feed resistance, decrease the rotation resistance of the spool, and avoid having the filament tube too long and excessively bent."
        },
        {
          "ecode": "1804220000020025",
          "intro": "AMS-HT E slot 3 feed resistance is too high. Please reduce the feed resistance, decrease the rotation resistance of the spool, and avoid having the filament tube too long and excessively bent."
        },
        {
          "ecode": "1805200000020025",
          "intro": "AMS-HT F slot 1 feed resistance is too high. Please reduce the feed resistance, decrease the rotation resistance of the spool, and avoid having the filament tube too long and excessively bent."
        },
        {
          "ecode": "1806210000020025",
          "intro": "AMS-HT G slot 2 feed resistance is too high. Please reduce the feed resistance, decrease the rotation resistance of the spool, and avoid having the filament tube too long and excessively bent."
        },
        {
          "ecode": "1803200000020025",
          "intro": "AMS-HT D slot 1 feed resistance is too high. Please reduce the feed resistance, decrease the rotation resistance of the spool, and avoid having the filament tube too long and excessively bent."
        },
        {
          "ecode": "1806230000020025",
          "intro": "AMS-HT G slot 4 feed resistance is too high. Please reduce the feed resistance, decrease the rotation resistance of the spool, and avoid having the filament tube too long and excessively bent."
        },
        {
          "ecode": "1802220000020025",
          "intro": "AMS-HT C slot 3 feed resistance is too high. Please reduce the feed resistance, decrease the rotation resistance of the spool, and avoid having the filament tube too long and excessively bent."
        },
        {
          "ecode": "1804230000020025",
          "intro": "AMS-HT E slot 4 feed resistance is too high. Please reduce the feed resistance, decrease the rotation resistance of the spool, and avoid having the filament tube too long and excessively bent."
        },
        {
          "ecode": "0702200000020025",
          "intro": "AMS C slot 1 feed resistance is too high. Please reduce the feed resistance, decrease the rotation resistance of the spool, and avoid having the filament tube too long and excessively bent."
        },
        {
          "ecode": "0701200000020025",
          "intro": "AMS B slot 1 feed resistance is too high. Please reduce the feed resistance, decrease the rotation resistance of the spool, and avoid having the filament tube too long and excessively bent."
        },
        {
          "ecode": "1806220000020025",
          "intro": "AMS-HT G slot 3 feed resistance is too high. Please reduce the feed resistance, decrease the rotation resistance of the spool, and avoid having the filament tube too long and excessively bent."
        },
        {
          "ecode": "1800220000020025",
          "intro": "AMS-HT A slot 3 feed resistance is too high. Please reduce the feed resistance, decrease the rotation resistance of the spool, and avoid having the filament tube too long and excessively bent."
        },
        {
          "ecode": "0701230000020025",
          "intro": "AMS B slot 4 feed resistance is too high. Please reduce the feed resistance, decrease the rotation resistance of the spool, and avoid having the filament tube too long and excessively bent."
        },
        {
          "ecode": "1807230000020025",
          "intro": "AMS-HT H slot 4 feed resistance is too high. Please reduce the feed resistance, decrease the rotation resistance of the spool, and avoid having the filament tube too long and excessively bent."
        },
        {
          "ecode": "0703200000020025",
          "intro": "AMS D slot 1 feed resistance is too high. Please reduce the feed resistance, decrease the rotation resistance of the spool, and avoid having the filament tube too long and excessively bent."
        },
        {
          "ecode": "0707220000020025",
          "intro": "AMS H slot 3 feed resistance is too high. Please reduce the feed resistance, decrease the rotation resistance of the spool, and avoid having the filament tube too long and excessively bent."
        },
        {
          "ecode": "0707230000020025",
          "intro": "AMS H slot 4 feed resistance is too high. Please reduce the feed resistance, decrease the rotation resistance of the spool, and avoid having the filament tube too long and excessively bent."
        },
        {
          "ecode": "0705230000020025",
          "intro": "AMS F slot 4 feed resistance is too high. Please reduce the feed resistance, decrease the rotation resistance of the spool, and avoid having the filament tube too long and excessively bent."
        },
        {
          "ecode": "1803210000020025",
          "intro": "AMS-HT D slot 2 feed resistance is too high. Please reduce the feed resistance, decrease the rotation resistance of the spool, and avoid having the filament tube too long and excessively bent."
        },
        {
          "ecode": "0702210000020025",
          "intro": "AMS C slot 2 feed resistance is too high. Please reduce the feed resistance, decrease the rotation resistance of the spool, and avoid having the filament tube too long and excessively bent."
        },
        {
          "ecode": "0706220000020025",
          "intro": "AMS G slot 3 feed resistance is too high. Please reduce the feed resistance, decrease the rotation resistance of the spool, and avoid having the filament tube too long and excessively bent."
        },
        {
          "ecode": "1807210000020006",
          "intro": "AMS-HT H has detected a breakage of the PTFE tube during filament loading. Please check whether the PTFE tubes inside and outside the AMS have fallen off or been damaged."
        },
        {
          "ecode": "0706220000020006",
          "intro": "AMS G has detected a breakage of the PTFE tube during filament loading. Please check whether the PTFE tubes inside and outside the AMS have fallen off or been damaged."
        },
        {
          "ecode": "1800220000020006",
          "intro": "AMS-HT A has detected a breakage of the PTFE tube during filament loading. Please check whether the PTFE tubes inside and outside the AMS have fallen off or been damaged."
        },
        {
          "ecode": "0702220000020006",
          "intro": "AMS C has detected a breakage of the PTFE tube during filament loading. Please check whether the PTFE tubes inside and outside the AMS have fallen off or been damaged."
        },
        {
          "ecode": "0700220000020006",
          "intro": "AMS A has detected a breakage of the PTFE tube during filament loading. Please check whether the PTFE tubes inside and outside the AMS have fallen off or been damaged."
        },
        {
          "ecode": "1804230000020006",
          "intro": "AMS-HT E has detected a breakage of the PTFE tube during filament loading. Please check whether the PTFE tubes inside and outside the AMS have fallen off or been damaged."
        },
        {
          "ecode": "0706210000020006",
          "intro": "AMS G has detected a breakage of the PTFE tube during filament loading. Please check whether the PTFE tubes inside and outside the AMS have fallen off or been damaged."
        },
        {
          "ecode": "1800210000020006",
          "intro": "AMS-HT A has detected a breakage of the PTFE tube during filament loading. Please check whether the PTFE tubes inside and outside the AMS have fallen off or been damaged."
        },
        {
          "ecode": "0705210000020006",
          "intro": "AMS F has detected a breakage of the PTFE tube during filament loading. Please check whether the PTFE tubes inside and outside the AMS have fallen off or been damaged."
        },
        {
          "ecode": "1805220000020006",
          "intro": "AMS-HT F has detected a breakage of the PTFE tube during filament loading. Please check whether the PTFE tubes inside and outside the AMS have fallen off or been damaged."
        },
        {
          "ecode": "0703230000020006",
          "intro": "AMS D has detected a breakage of the PTFE tube during filament loading. Please check whether the PTFE tubes inside and outside the AMS have fallen off or been damaged."
        },
        {
          "ecode": "0701220000020006",
          "intro": "AMS B has detected a breakage of the PTFE tube during filament loading. Please check whether the PTFE tubes inside and outside the AMS have fallen off or been damaged."
        },
        {
          "ecode": "1804210000020006",
          "intro": "AMS-HT E has detected a breakage of the PTFE tube during filament loading. Please check whether the PTFE tubes inside and outside the AMS have fallen off or been damaged."
        },
        {
          "ecode": "1805230000020006",
          "intro": "AMS-HT F has detected a breakage of the PTFE tube during filament loading. Please check whether the PTFE tubes inside and outside the AMS have fallen off or been damaged."
        },
        {
          "ecode": "0705220000020006",
          "intro": "AMS F has detected a breakage of the PTFE tube during filament loading. Please check whether the PTFE tubes inside and outside the AMS have fallen off or been damaged."
        },
        {
          "ecode": "1807230000020006",
          "intro": "AMS-HT H has detected a breakage of the PTFE tube during filament loading. Please check whether the PTFE tubes inside and outside the AMS have fallen off or been damaged."
        },
        {
          "ecode": "0703200000020013",
          "intro": "AMS D slot 1 feeder unit motor has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "1802210000020014",
          "intro": "AMS-HT C slot 2 filament odometer has no signal, which may be due to poor contact in the odometer connector or a odometer fault."
        },
        {
          "ecode": "0707220000020012",
          "intro": "AMS H slot 3 feeder unit motor is stalled, cannot rotate the spool."
        },
        {
          "ecode": "0707210000020014",
          "intro": "AMS H slot 2 filament odometer has no signal, which may be due to poor contact in the odometer connector or a odometer fault."
        },
        {
          "ecode": "1806200000020013",
          "intro": "AMS-HT G slot 1 feeder unit motor has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "0704210000020015",
          "intro": "AMS E slot 2 filament status is abnormal, which may be due to a filament breakage inside the AMS."
        },
        {
          "ecode": "1800220000020013",
          "intro": "AMS-HT A slot 3 feeder unit motor has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "1800230000020016",
          "intro": "AMS-HT A slot 4 assist motor has slipped. Please pull out the filament, cut off the worn part, and then try again."
        },
        {
          "ecode": "0701200000020015",
          "intro": "AMS B slot 1 filament status is abnormal, which may be due to a filament breakage inside the AMS."
        },
        {
          "ecode": "0704210000020014",
          "intro": "AMS E slot 2 filament odometer has no signal, which may be due to poor contact in the odometer connector or a odometer fault."
        },
        {
          "ecode": "0702210000020015",
          "intro": "AMS C slot 2 filament status is abnormal, which may be due to a filament breakage inside the AMS."
        },
        {
          "ecode": "1802230000020012",
          "intro": "AMS-HT C slot 4 feeder unit motor is stalled, cannot rotate the spool."
        },
        {
          "ecode": "0700200000020014",
          "intro": "AMS A slot 1 filament odometer has no signal, which may be due to poor contact in the odometer connector or a odometer fault."
        },
        {
          "ecode": "1807200000020014",
          "intro": "AMS-HT H slot 1 filament odometer has no signal, which may be due to poor contact in the odometer connector or a odometer fault."
        },
        {
          "ecode": "1806230000020015",
          "intro": "AMS-HT G slot 4 filament status is abnormal, which may be due to a filament breakage inside the AMS."
        },
        {
          "ecode": "0707210000020015",
          "intro": "AMS H slot 2 filament status is abnormal, which may be due to a filament breakage inside the AMS."
        },
        {
          "ecode": "0700210000020012",
          "intro": "AMS A slot 2 feeder unit motor is stalled, cannot rotate the spool."
        },
        {
          "ecode": "1807200000020012",
          "intro": "AMS-HT H slot 1 feeder unit motor is stalled, cannot rotate the spool."
        },
        {
          "ecode": "1800200000020016",
          "intro": "AMS-HT A slot 1 assist motor has slipped. Please pull out the filament, cut off the worn part, and then try again."
        },
        {
          "ecode": "0701220000020015",
          "intro": "AMS B slot 3 filament status is abnormal, which may be due to a filament breakage inside the AMS."
        },
        {
          "ecode": "1805230000020013",
          "intro": "AMS-HT F slot 4 feeder unit motor has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "0701230000020014",
          "intro": "AMS B slot 4 filament odometer has no signal, which may be due to poor contact in the odometer connector or a odometer fault."
        },
        {
          "ecode": "1804200000020016",
          "intro": "AMS-HT E slot 1 assist motor has slipped. Please pull out the filament, cut off the worn part, and then try again."
        },
        {
          "ecode": "0706220000020015",
          "intro": "AMS G slot 3 filament status is abnormal, which may be due to a filament breakage inside the AMS."
        },
        {
          "ecode": "0706220000020013",
          "intro": "AMS G slot 3 feeder unit motor has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "0706230000020014",
          "intro": "AMS G slot 4 filament odometer has no signal, which may be due to poor contact in the odometer connector or a odometer fault."
        },
        {
          "ecode": "1804220000020014",
          "intro": "AMS-HT E slot 3 filament odometer has no signal, which may be due to poor contact in the odometer connector or a odometer fault."
        },
        {
          "ecode": "0705230000020013",
          "intro": "AMS F slot 4 feeder unit motor has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "1801230000020014",
          "intro": "AMS-HT B slot 4 filament odometer has no signal, which may be due to poor contact in the odometer connector or a odometer fault."
        },
        {
          "ecode": "1806230000020014",
          "intro": "AMS-HT G slot 4 filament odometer has no signal, which may be due to poor contact in the odometer connector or a odometer fault."
        },
        {
          "ecode": "0700220000020016",
          "intro": "AMS A slot 3 assist motor has slipped. Please pull out the filament, cut off the worn part, and then try again."
        },
        {
          "ecode": "0700200000020015",
          "intro": "AMS A slot 1 filament status is abnormal, which may be due to a filament breakage inside the AMS."
        },
        {
          "ecode": "1806230000020016",
          "intro": "AMS-HT G slot 4 assist motor has slipped. Please pull out the filament, cut off the worn part, and then try again."
        },
        {
          "ecode": "0700200000020013",
          "intro": "AMS A slot 1 feeder unit motor has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "1802230000020015",
          "intro": "AMS-HT C slot 4 filament status is abnormal, which may be due to a filament breakage inside the AMS."
        },
        {
          "ecode": "1807210000020016",
          "intro": "AMS-HT H slot 2 assist motor has slipped. Please pull out the filament, cut off the worn part, and then try again."
        },
        {
          "ecode": "0701210000020012",
          "intro": "AMS B slot 2 feeder unit motor is stalled, cannot rotate the spool."
        },
        {
          "ecode": "0705210000020014",
          "intro": "AMS F slot 2 filament odometer has no signal, which may be due to poor contact in the odometer connector or a odometer fault."
        },
        {
          "ecode": "0707220000020013",
          "intro": "AMS H slot 3 feeder unit motor has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "0702200000020013",
          "intro": "AMS C slot 1 feeder unit motor has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "0704200000020012",
          "intro": "AMS E slot 1 feeder unit motor is stalled, cannot rotate the spool."
        },
        {
          "ecode": "1801230000020013",
          "intro": "AMS-HT B slot 4 feeder unit motor has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "0702230000020013",
          "intro": "AMS C slot 4 feeder unit motor has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "1806210000020012",
          "intro": "AMS-HT G slot 2 feeder unit motor is stalled, cannot rotate the spool."
        },
        {
          "ecode": "1801200000020013",
          "intro": "AMS-HT B slot 1 feeder unit motor has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "1806220000020016",
          "intro": "AMS-HT G slot 3 assist motor has slipped. Please pull out the filament, cut off the worn part, and then try again."
        },
        {
          "ecode": "1802210000020015",
          "intro": "AMS-HT C slot 2 filament status is abnormal, which may be due to a filament breakage inside the AMS."
        },
        {
          "ecode": "0706200000020014",
          "intro": "AMS G slot 1 filament odometer has no signal, which may be due to poor contact in the odometer connector or a odometer fault."
        },
        {
          "ecode": "0707220000020014",
          "intro": "AMS H slot 3 filament odometer has no signal, which may be due to poor contact in the odometer connector or a odometer fault."
        },
        {
          "ecode": "1803230000020016",
          "intro": "AMS-HT D slot 4 assist motor has slipped. Please pull out the filament, cut off the worn part, and then try again."
        },
        {
          "ecode": "0702210000020014",
          "intro": "AMS C slot 2 filament odometer has no signal, which may be due to poor contact in the odometer connector or a odometer fault."
        },
        {
          "ecode": "1804200000020013",
          "intro": "AMS-HT E slot 1 feeder unit motor has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "1805220000020012",
          "intro": "AMS-HT F slot 3 feeder unit motor is stalled, cannot rotate the spool."
        },
        {
          "ecode": "1800220000020016",
          "intro": "AMS-HT A slot 3 assist motor has slipped. Please pull out the filament, cut off the worn part, and then try again."
        },
        {
          "ecode": "0700210000020013",
          "intro": "AMS A slot 2 feeder unit motor has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "1800220000020014",
          "intro": "AMS-HT A slot 3 filament odometer has no signal, which may be due to poor contact in the odometer connector or a odometer fault."
        },
        {
          "ecode": "0707200000020015",
          "intro": "AMS H slot 1 filament status is abnormal, which may be due to a filament breakage inside the AMS."
        },
        {
          "ecode": "0705210000020012",
          "intro": "AMS F slot 2 feeder unit motor is stalled, cannot rotate the spool."
        },
        {
          "ecode": "0706220000020016",
          "intro": "AMS G slot 3 assist motor has slipped. Please pull out the filament, cut off the worn part, and then try again."
        },
        {
          "ecode": "1801220000020013",
          "intro": "AMS-HT B slot 3 feeder unit motor has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "0703220000020014",
          "intro": "AMS D slot 3 filament odometer has no signal, which may be due to poor contact in the odometer connector or a odometer fault."
        },
        {
          "ecode": "0706200000020015",
          "intro": "AMS G slot 1 filament status is abnormal, which may be due to a filament breakage inside the AMS."
        },
        {
          "ecode": "0703210000020012",
          "intro": "AMS D slot 2 feeder unit motor is stalled, cannot rotate the spool."
        },
        {
          "ecode": "0704200000020013",
          "intro": "AMS E slot 1 feeder unit motor has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "1807220000020012",
          "intro": "AMS-HT H slot 3 feeder unit motor is stalled, cannot rotate the spool."
        },
        {
          "ecode": "1807230000020014",
          "intro": "AMS-HT H slot 4 filament odometer has no signal, which may be due to poor contact in the odometer connector or a odometer fault."
        },
        {
          "ecode": "0707200000020006",
          "intro": "AMS H has detected a breakage of the PTFE tube during filament loading. Please check whether the PTFE tubes inside and outside the AMS have fallen off or been damaged."
        },
        {
          "ecode": "1801220000020016",
          "intro": "AMS-HT B slot 3 assist motor has slipped. Please pull out the filament, cut off the worn part, and then try again."
        },
        {
          "ecode": "0702210000020012",
          "intro": "AMS C slot 2 feeder unit motor is stalled, cannot rotate the spool."
        },
        {
          "ecode": "0701210000020015",
          "intro": "AMS B slot 2 filament status is abnormal, which may be due to a filament breakage inside the AMS."
        },
        {
          "ecode": "1801210000020016",
          "intro": "AMS-HT B slot 2 assist motor has slipped. Please pull out the filament, cut off the worn part, and then try again."
        },
        {
          "ecode": "0705220000020014",
          "intro": "AMS F slot 3 filament odometer has no signal, which may be due to poor contact in the odometer connector or a odometer fault."
        },
        {
          "ecode": "1804220000020013",
          "intro": "AMS-HT E slot 3 feeder unit motor has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "0707230000020013",
          "intro": "AMS H slot 4 feeder unit motor has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "1805220000020013",
          "intro": "AMS-HT F slot 3 feeder unit motor has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "1800230000020014",
          "intro": "AMS-HT A slot 4 filament odometer has no signal, which may be due to poor contact in the odometer connector or a odometer fault."
        },
        {
          "ecode": "1807230000020013",
          "intro": "AMS-HT H slot 4 feeder unit motor has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "0701200000020006",
          "intro": "AMS B has detected a breakage of the PTFE tube during filament loading. Please check whether the PTFE tubes inside and outside the AMS have fallen off or been damaged."
        },
        {
          "ecode": "0701200000020016",
          "intro": "AMS B slot 1 assist motor has slipped. Please pull out the filament, cut off the worn part, and then try again."
        },
        {
          "ecode": "1803210000020013",
          "intro": "AMS-HT D slot 2 feeder unit motor has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "0706200000020016",
          "intro": "AMS G slot 1 assist motor has slipped. Please pull out the filament, cut off the worn part, and then try again."
        },
        {
          "ecode": "0704230000020013",
          "intro": "AMS E slot 4 feeder unit motor has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "1800210000020016",
          "intro": "AMS-HT A slot 2 assist motor has slipped. Please pull out the filament, cut off the worn part, and then try again."
        },
        {
          "ecode": "0703210000020015",
          "intro": "AMS D slot 2 filament status is abnormal, which may be due to a filament breakage inside the AMS."
        },
        {
          "ecode": "0705200000020012",
          "intro": "AMS F slot 1 feeder unit motor is stalled, cannot rotate the spool."
        },
        {
          "ecode": "1805210000020013",
          "intro": "AMS-HT F slot 2 feeder unit motor has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "0706200000020012",
          "intro": "AMS G slot 1 feeder unit motor is stalled, cannot rotate the spool."
        },
        {
          "ecode": "0704220000020014",
          "intro": "AMS E slot 3 filament odometer has no signal, which may be due to poor contact in the odometer connector or a odometer fault."
        },
        {
          "ecode": "1803200000020016",
          "intro": "AMS-HT D slot 1 assist motor has slipped. Please pull out the filament, cut off the worn part, and then try again."
        },
        {
          "ecode": "1800200000020014",
          "intro": "AMS-HT A slot 1 filament odometer has no signal, which may be due to poor contact in the odometer connector or a odometer fault."
        },
        {
          "ecode": "0704210000020013",
          "intro": "AMS E slot 2 feeder unit motor has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "0707230000020014",
          "intro": "AMS H slot 4 filament odometer has no signal, which may be due to poor contact in the odometer connector or a odometer fault."
        },
        {
          "ecode": "0700230000020013",
          "intro": "AMS A slot 4 feeder unit motor has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "1804200000020015",
          "intro": "AMS-HT E slot 1 filament status is abnormal, which may be due to a filament breakage inside the AMS."
        },
        {
          "ecode": "1800230000020012",
          "intro": "AMS-HT A slot 4 feeder unit motor is stalled, cannot rotate the spool."
        },
        {
          "ecode": "1800230000020013",
          "intro": "AMS-HT A slot 4 feeder unit motor has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "0706230000020016",
          "intro": "AMS G slot 4 assist motor has slipped. Please pull out the filament, cut off the worn part, and then try again."
        },
        {
          "ecode": "1803200000020014",
          "intro": "AMS-HT D slot 1 filament odometer has no signal, which may be due to poor contact in the odometer connector or a odometer fault."
        },
        {
          "ecode": "0703210000020016",
          "intro": "AMS D slot 2 assist motor has slipped. Please pull out the filament, cut off the worn part, and then try again."
        },
        {
          "ecode": "0705230000020015",
          "intro": "AMS F slot 4 filament status is abnormal, which may be due to a filament breakage inside the AMS."
        },
        {
          "ecode": "1802200000020006",
          "intro": "AMS-HT C has detected a breakage of the PTFE tube during filament loading. Please check whether the PTFE tubes inside and outside the AMS have fallen off or been damaged."
        },
        {
          "ecode": "1800200000020006",
          "intro": "AMS-HT A has detected a breakage of the PTFE tube during filament loading. Please check whether the PTFE tubes inside and outside the AMS have fallen off or been damaged."
        },
        {
          "ecode": "1804210000020015",
          "intro": "AMS-HT E slot 2 filament status is abnormal, which may be due to a filament breakage inside the AMS."
        },
        {
          "ecode": "1807200000020016",
          "intro": "AMS-HT H slot 1 assist motor has slipped. Please pull out the filament, cut off the worn part, and then try again."
        },
        {
          "ecode": "1807230000020012",
          "intro": "AMS-HT H slot 4 feeder unit motor is stalled, cannot rotate the spool."
        },
        {
          "ecode": "0705230000020012",
          "intro": "AMS F slot 4 feeder unit motor is stalled, cannot rotate the spool."
        },
        {
          "ecode": "0702200000020014",
          "intro": "AMS C slot 1 filament odometer has no signal, which may be due to poor contact in the odometer connector or a odometer fault."
        },
        {
          "ecode": "1804200000020006",
          "intro": "AMS-HT E has detected a breakage of the PTFE tube during filament loading. Please check whether the PTFE tubes inside and outside the AMS have fallen off or been damaged."
        },
        {
          "ecode": "0707230000020015",
          "intro": "AMS H slot 4 filament status is abnormal, which may be due to a filament breakage inside the AMS."
        },
        {
          "ecode": "0704210000020012",
          "intro": "AMS E slot 2 feeder unit motor is stalled, cannot rotate the spool."
        },
        {
          "ecode": "1806200000020025",
          "intro": "AMS-HT G slot 1 feed resistance is too high. Please reduce the feed resistance, decrease the rotation resistance of the spool, and avoid having the filament tube too long and excessively bent."
        },
        {
          "ecode": "0704230000020025",
          "intro": "AMS E slot 4 feed resistance is too high. Please reduce the feed resistance, decrease the rotation resistance of the spool, and avoid having the filament tube too long and excessively bent."
        },
        {
          "ecode": "0702230000020025",
          "intro": "AMS C slot 4 feed resistance is too high. Please reduce the feed resistance, decrease the rotation resistance of the spool, and avoid having the filament tube too long and excessively bent."
        },
        {
          "ecode": "1807200000020025",
          "intro": "AMS-HT H slot 1 feed resistance is too high. Please reduce the feed resistance, decrease the rotation resistance of the spool, and avoid having the filament tube too long and excessively bent."
        },
        {
          "ecode": "1804200000020025",
          "intro": "AMS-HT E slot 1 feed resistance is too high. Please reduce the feed resistance, decrease the rotation resistance of the spool, and avoid having the filament tube too long and excessively bent."
        },
        {
          "ecode": "1804210000020025",
          "intro": "AMS-HT E slot 2 feed resistance is too high. Please reduce the feed resistance, decrease the rotation resistance of the spool, and avoid having the filament tube too long and excessively bent."
        },
        {
          "ecode": "0703210000020025",
          "intro": "AMS D slot 2 feed resistance is too high. Please reduce the feed resistance, decrease the rotation resistance of the spool, and avoid having the filament tube too long and excessively bent."
        },
        {
          "ecode": "0700230000020025",
          "intro": "AMS A slot 4 feed resistance is too high. Please reduce the feed resistance, decrease the rotation resistance of the spool, and avoid having the filament tube too long and excessively bent."
        },
        {
          "ecode": "1802210000020025",
          "intro": "AMS-HT C slot 2 feed resistance is too high. Please reduce the feed resistance, decrease the rotation resistance of the spool, and avoid having the filament tube too long and excessively bent."
        },
        {
          "ecode": "0706200000020025",
          "intro": "AMS G slot 1 feed resistance is too high. Please reduce the feed resistance, decrease the rotation resistance of the spool, and avoid having the filament tube too long and excessively bent."
        },
        {
          "ecode": "1802230000020025",
          "intro": "AMS-HT C slot 4 feed resistance is too high. Please reduce the feed resistance, decrease the rotation resistance of the spool, and avoid having the filament tube too long and excessively bent."
        },
        {
          "ecode": "0705200000020025",
          "intro": "AMS F slot 1 feed resistance is too high. Please reduce the feed resistance, decrease the rotation resistance of the spool, and avoid having the filament tube too long and excessively bent."
        },
        {
          "ecode": "1805220000020025",
          "intro": "AMS-HT F slot 3 feed resistance is too high. Please reduce the feed resistance, decrease the rotation resistance of the spool, and avoid having the filament tube too long and excessively bent."
        },
        {
          "ecode": "1803230000020025",
          "intro": "AMS-HT D slot 4 feed resistance is too high. Please reduce the feed resistance, decrease the rotation resistance of the spool, and avoid having the filament tube too long and excessively bent."
        },
        {
          "ecode": "1802200000020025",
          "intro": "AMS-HT C slot 1 feed resistance is too high. Please reduce the feed resistance, decrease the rotation resistance of the spool, and avoid having the filament tube too long and excessively bent."
        },
        {
          "ecode": "0701210000020025",
          "intro": "AMS B slot 2 feed resistance is too high. Please reduce the feed resistance, decrease the rotation resistance of the spool, and avoid having the filament tube too long and excessively bent."
        },
        {
          "ecode": "1801230000020025",
          "intro": "AMS-HT B slot 4 feed resistance is too high. Please reduce the feed resistance, decrease the rotation resistance of the spool, and avoid having the filament tube too long and excessively bent."
        },
        {
          "ecode": "1801210000020025",
          "intro": "AMS-HT B slot 2 feed resistance is too high. Please reduce the feed resistance, decrease the rotation resistance of the spool, and avoid having the filament tube too long and excessively bent."
        },
        {
          "ecode": "1800230000020025",
          "intro": "AMS-HT A slot 4 feed resistance is too high. Please reduce the feed resistance, decrease the rotation resistance of the spool, and avoid having the filament tube too long and excessively bent."
        },
        {
          "ecode": "0704200000020025",
          "intro": "AMS E slot 1 feed resistance is too high. Please reduce the feed resistance, decrease the rotation resistance of the spool, and avoid having the filament tube too long and excessively bent."
        },
        {
          "ecode": "1807220000020025",
          "intro": "AMS-HT H slot 3 feed resistance is too high. Please reduce the feed resistance, decrease the rotation resistance of the spool, and avoid having the filament tube too long and excessively bent."
        },
        {
          "ecode": "0700220000020025",
          "intro": "AMS A slot 3 feed resistance is too high. Please reduce the feed resistance, decrease the rotation resistance of the spool, and avoid having the filament tube too long and excessively bent."
        },
        {
          "ecode": "1805230000020025",
          "intro": "AMS-HT F slot 4 feed resistance is too high. Please reduce the feed resistance, decrease the rotation resistance of the spool, and avoid having the filament tube too long and excessively bent."
        },
        {
          "ecode": "0706230000020006",
          "intro": "AMS G has detected a breakage of the PTFE tube during filament loading. Please check whether the PTFE tubes inside and outside the AMS have fallen off or been damaged."
        },
        {
          "ecode": "1800230000020006",
          "intro": "AMS-HT A has detected a breakage of the PTFE tube during filament loading. Please check whether the PTFE tubes inside and outside the AMS have fallen off or been damaged."
        },
        {
          "ecode": "0707230000020006",
          "intro": "AMS H has detected a breakage of the PTFE tube during filament loading. Please check whether the PTFE tubes inside and outside the AMS have fallen off or been damaged."
        },
        {
          "ecode": "0700210000020006",
          "intro": "AMS A has detected a breakage of the PTFE tube during filament loading. Please check whether the PTFE tubes inside and outside the AMS have fallen off or been damaged."
        },
        {
          "ecode": "1801230000020006",
          "intro": "AMS-HT B has detected a breakage of the PTFE tube during filament loading. Please check whether the PTFE tubes inside and outside the AMS have fallen off or been damaged."
        },
        {
          "ecode": "0701230000020006",
          "intro": "AMS B has detected a breakage of the PTFE tube during filament loading. Please check whether the PTFE tubes inside and outside the AMS have fallen off or been damaged."
        },
        {
          "ecode": "0707220000020006",
          "intro": "AMS H has detected a breakage of the PTFE tube during filament loading. Please check whether the PTFE tubes inside and outside the AMS have fallen off or been damaged."
        },
        {
          "ecode": "1807220000020006",
          "intro": "AMS-HT H has detected a breakage of the PTFE tube during filament loading. Please check whether the PTFE tubes inside and outside the AMS have fallen off or been damaged."
        },
        {
          "ecode": "0704210000020006",
          "intro": "AMS E has detected a breakage of the PTFE tube during filament loading. Please check whether the PTFE tubes inside and outside the AMS have fallen off or been damaged."
        },
        {
          "ecode": "1803220000020006",
          "intro": "AMS-HT D has detected a breakage of the PTFE tube during filament loading. Please check whether the PTFE tubes inside and outside the AMS have fallen off or been damaged."
        },
        {
          "ecode": "1806210000020006",
          "intro": "AMS-HT G has detected a breakage of the PTFE tube during filament loading. Please check whether the PTFE tubes inside and outside the AMS have fallen off or been damaged."
        },
        {
          "ecode": "1806220000020006",
          "intro": "AMS-HT G has detected a breakage of the PTFE tube during filament loading. Please check whether the PTFE tubes inside and outside the AMS have fallen off or been damaged."
        },
        {
          "ecode": "1804220000020006",
          "intro": "AMS-HT E has detected a breakage of the PTFE tube during filament loading. Please check whether the PTFE tubes inside and outside the AMS have fallen off or been damaged."
        },
        {
          "ecode": "1806230000020006",
          "intro": "AMS-HT G has detected a breakage of the PTFE tube during filament loading. Please check whether the PTFE tubes inside and outside the AMS have fallen off or been damaged."
        },
        {
          "ecode": "0700230000020006",
          "intro": "AMS A has detected a breakage of the PTFE tube during filament loading. Please check whether the PTFE tubes inside and outside the AMS have fallen off or been damaged."
        },
        {
          "ecode": "1802200000020014",
          "intro": "AMS-HT C slot 1 filament odometer has no signal, which may be due to poor contact in the odometer connector or a odometer fault."
        },
        {
          "ecode": "0705220000020013",
          "intro": "AMS F slot 3 feeder unit motor has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "1801230000020012",
          "intro": "AMS-HT B slot 4 feeder unit motor is stalled, cannot rotate the spool."
        },
        {
          "ecode": "0706210000020014",
          "intro": "AMS G slot 2 filament odometer has no signal, which may be due to poor contact in the odometer connector or a odometer fault."
        },
        {
          "ecode": "0700230000020014",
          "intro": "AMS A slot 4 filament odometer has no signal, which may be due to poor contact in the odometer connector or a odometer fault."
        },
        {
          "ecode": "0701230000020015",
          "intro": "AMS B slot 4 filament status is abnormal, which may be due to a filament breakage inside the AMS."
        },
        {
          "ecode": "0703220000020012",
          "intro": "AMS D slot 3 feeder unit motor is stalled, cannot rotate the spool."
        },
        {
          "ecode": "0701200000020013",
          "intro": "AMS B slot 1 feeder unit motor has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "0702230000020014",
          "intro": "AMS C slot 4 filament odometer has no signal, which may be due to poor contact in the odometer connector or a odometer fault."
        },
        {
          "ecode": "1807210000020014",
          "intro": "AMS-HT H slot 2 filament odometer has no signal, which may be due to poor contact in the odometer connector or a odometer fault."
        },
        {
          "ecode": "0701220000020012",
          "intro": "AMS B slot 3 feeder unit motor is stalled, cannot rotate the spool."
        },
        {
          "ecode": "0706230000020012",
          "intro": "AMS G slot 4 feeder unit motor is stalled, cannot rotate the spool."
        },
        {
          "ecode": "0706220000020012",
          "intro": "AMS G slot 3 feeder unit motor is stalled, cannot rotate the spool."
        },
        {
          "ecode": "0707230000020012",
          "intro": "AMS H slot 4 feeder unit motor is stalled, cannot rotate the spool."
        },
        {
          "ecode": "0701220000020013",
          "intro": "AMS B slot 3 feeder unit motor has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "0705220000020015",
          "intro": "AMS F slot 3 filament status is abnormal, which may be due to a filament breakage inside the AMS."
        },
        {
          "ecode": "1803200000020015",
          "intro": "AMS-HT D slot 1 filament status is abnormal, which may be due to a filament breakage inside the AMS."
        },
        {
          "ecode": "0705220000020016",
          "intro": "AMS F slot 3 assist motor has slipped. Please pull out the filament, cut off the worn part, and then try again."
        },
        {
          "ecode": "1800210000020015",
          "intro": "AMS-HT A slot 2 filament status is abnormal, which may be due to a filament breakage inside the AMS."
        },
        {
          "ecode": "1803210000020016",
          "intro": "AMS-HT D slot 2 assist motor has slipped. Please pull out the filament, cut off the worn part, and then try again."
        },
        {
          "ecode": "0703210000020014",
          "intro": "AMS D slot 2 filament odometer has no signal, which may be due to poor contact in the odometer connector or a odometer fault."
        },
        {
          "ecode": "0707200000020013",
          "intro": "AMS H slot 1 feeder unit motor has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "1803210000020012",
          "intro": "AMS-HT D slot 2 feeder unit motor is stalled, cannot rotate the spool."
        },
        {
          "ecode": "1802200000020015",
          "intro": "AMS-HT C slot 1 filament status is abnormal, which may be due to a filament breakage inside the AMS."
        },
        {
          "ecode": "1805220000020014",
          "intro": "AMS-HT F slot 3 filament odometer has no signal, which may be due to poor contact in the odometer connector or a odometer fault."
        },
        {
          "ecode": "0701210000020013",
          "intro": "AMS B slot 2 feeder unit motor has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "1806220000020014",
          "intro": "AMS-HT G slot 3 filament odometer has no signal, which may be due to poor contact in the odometer connector or a odometer fault."
        },
        {
          "ecode": "1803220000020013",
          "intro": "AMS-HT D slot 3 feeder unit motor has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "0702220000020015",
          "intro": "AMS C slot 3 filament status is abnormal, which may be due to a filament breakage inside the AMS."
        },
        {
          "ecode": "1807230000020016",
          "intro": "AMS-HT H slot 4 assist motor has slipped. Please pull out the filament, cut off the worn part, and then try again."
        },
        {
          "ecode": "1804230000020012",
          "intro": "AMS-HT E slot 4 feeder unit motor is stalled, cannot rotate the spool."
        },
        {
          "ecode": "1803200000020013",
          "intro": "AMS-HT D slot 1 feeder unit motor has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "1801200000020012",
          "intro": "AMS-HT B slot 1 feeder unit motor is stalled, cannot rotate the spool."
        },
        {
          "ecode": "1800220000020012",
          "intro": "AMS-HT A slot 3 feeder unit motor is stalled, cannot rotate the spool."
        },
        {
          "ecode": "1804230000020016",
          "intro": "AMS-HT E slot 4 assist motor has slipped. Please pull out the filament, cut off the worn part, and then try again."
        },
        {
          "ecode": "0703200000020016",
          "intro": "AMS D slot 1 assist motor has slipped. Please pull out the filament, cut off the worn part, and then try again."
        },
        {
          "ecode": "0700210000020016",
          "intro": "AMS A slot 2 assist motor has slipped. Please pull out the filament, cut off the worn part, and then try again."
        },
        {
          "ecode": "1803230000020015",
          "intro": "AMS-HT D slot 4 filament status is abnormal, which may be due to a filament breakage inside the AMS."
        },
        {
          "ecode": "0702220000020013",
          "intro": "AMS C slot 3 feeder unit motor has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "1807220000020013",
          "intro": "AMS-HT H slot 3 feeder unit motor has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "1805230000020016",
          "intro": "AMS-HT F slot 4 assist motor has slipped. Please pull out the filament, cut off the worn part, and then try again."
        },
        {
          "ecode": "1804220000020012",
          "intro": "AMS-HT E slot 3 feeder unit motor is stalled, cannot rotate the spool."
        },
        {
          "ecode": "0707210000020016",
          "intro": "AMS H slot 2 assist motor has slipped. Please pull out the filament, cut off the worn part, and then try again."
        },
        {
          "ecode": "1802200000020016",
          "intro": "AMS-HT C slot 1 assist motor has slipped. Please pull out the filament, cut off the worn part, and then try again."
        },
        {
          "ecode": "0703220000020016",
          "intro": "AMS D slot 3 assist motor has slipped. Please pull out the filament, cut off the worn part, and then try again."
        },
        {
          "ecode": "0706210000020015",
          "intro": "AMS G slot 2 filament status is abnormal, which may be due to a filament breakage inside the AMS."
        },
        {
          "ecode": "1801200000020015",
          "intro": "AMS-HT B slot 1 filament status is abnormal, which may be due to a filament breakage inside the AMS."
        },
        {
          "ecode": "1803230000020014",
          "intro": "AMS-HT D slot 4 filament odometer has no signal, which may be due to poor contact in the odometer connector or a odometer fault."
        },
        {
          "ecode": "1802230000020016",
          "intro": "AMS-HT C slot 4 assist motor has slipped. Please pull out the filament, cut off the worn part, and then try again."
        },
        {
          "ecode": "1800230000020015",
          "intro": "AMS-HT A slot 4 filament status is abnormal, which may be due to a filament breakage inside the AMS."
        },
        {
          "ecode": "0703230000020012",
          "intro": "AMS D slot 4 feeder unit motor is stalled, cannot rotate the spool."
        },
        {
          "ecode": "1804230000020013",
          "intro": "AMS-HT E slot 4 feeder unit motor has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "0703230000020013",
          "intro": "AMS D slot 4 feeder unit motor has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "0702210000020016",
          "intro": "AMS C slot 2 assist motor has slipped. Please pull out the filament, cut off the worn part, and then try again."
        },
        {
          "ecode": "1802220000020013",
          "intro": "AMS-HT C slot 3 feeder unit motor has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "0702220000020014",
          "intro": "AMS C slot 3 filament odometer has no signal, which may be due to poor contact in the odometer connector or a odometer fault."
        },
        {
          "ecode": "0707230000020016",
          "intro": "AMS H slot 4 assist motor has slipped. Please pull out the filament, cut off the worn part, and then try again."
        },
        {
          "ecode": "0702210000020013",
          "intro": "AMS C slot 2 feeder unit motor has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "1804210000020016",
          "intro": "AMS-HT E slot 2 assist motor has slipped. Please pull out the filament, cut off the worn part, and then try again."
        },
        {
          "ecode": "1801200000020016",
          "intro": "AMS-HT B slot 1 assist motor has slipped. Please pull out the filament, cut off the worn part, and then try again."
        },
        {
          "ecode": "1807220000020015",
          "intro": "AMS-HT H slot 3 filament status is abnormal, which may be due to a filament breakage inside the AMS."
        },
        {
          "ecode": "0703220000020015",
          "intro": "AMS D slot 3 filament status is abnormal, which may be due to a filament breakage inside the AMS."
        },
        {
          "ecode": "1805200000020014",
          "intro": "AMS-HT F slot 1 filament odometer has no signal, which may be due to poor contact in the odometer connector or a odometer fault."
        },
        {
          "ecode": "0701230000020016",
          "intro": "AMS B slot 4 assist motor has slipped. Please pull out the filament, cut off the worn part, and then try again."
        },
        {
          "ecode": "0706220000020014",
          "intro": "AMS G slot 3 filament odometer has no signal, which may be due to poor contact in the odometer connector or a odometer fault."
        },
        {
          "ecode": "1802230000020013",
          "intro": "AMS-HT C slot 4 feeder unit motor has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "0707200000020016",
          "intro": "AMS H slot 1 assist motor has slipped. Please pull out the filament, cut off the worn part, and then try again."
        },
        {
          "ecode": "1800200000020013",
          "intro": "AMS-HT A slot 1 feeder unit motor has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "1806200000020012",
          "intro": "AMS-HT G slot 1 feeder unit motor is stalled, cannot rotate the spool."
        },
        {
          "ecode": "0705200000020014",
          "intro": "AMS F slot 1 filament odometer has no signal, which may be due to poor contact in the odometer connector or a odometer fault."
        },
        {
          "ecode": "0702230000020015",
          "intro": "AMS C slot 4 filament status is abnormal, which may be due to a filament breakage inside the AMS."
        },
        {
          "ecode": "1801230000020016",
          "intro": "AMS-HT B slot 4 assist motor has slipped. Please pull out the filament, cut off the worn part, and then try again."
        },
        {
          "ecode": "1803220000020016",
          "intro": "AMS-HT D slot 3 assist motor has slipped. Please pull out the filament, cut off the worn part, and then try again."
        },
        {
          "ecode": "0704230000020016",
          "intro": "AMS E slot 4 assist motor has slipped. Please pull out the filament, cut off the worn part, and then try again."
        },
        {
          "ecode": "1806200000020006",
          "intro": "AMS-HT G has detected a breakage of the PTFE tube during filament loading. Please check whether the PTFE tubes inside and outside the AMS have fallen off or been damaged."
        },
        {
          "ecode": "1806230000020012",
          "intro": "AMS-HT G slot 4 feeder unit motor is stalled, cannot rotate the spool."
        },
        {
          "ecode": "1803210000020014",
          "intro": "AMS-HT D slot 2 filament odometer has no signal, which may be due to poor contact in the odometer connector or a odometer fault."
        },
        {
          "ecode": "0706200000020013",
          "intro": "AMS G slot 1 feeder unit motor has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "1803220000020014",
          "intro": "AMS-HT D slot 3 filament odometer has no signal, which may be due to poor contact in the odometer connector or a odometer fault."
        },
        {
          "ecode": "1807210000020015",
          "intro": "AMS-HT H slot 2 filament status is abnormal, which may be due to a filament breakage inside the AMS."
        },
        {
          "ecode": "1803230000020013",
          "intro": "AMS-HT D slot 4 feeder unit motor has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "0703200000020015",
          "intro": "AMS D slot 1 filament status is abnormal, which may be due to a filament breakage inside the AMS."
        },
        {
          "ecode": "0704210000020016",
          "intro": "AMS E slot 2 assist motor has slipped. Please pull out the filament, cut off the worn part, and then try again."
        },
        {
          "ecode": "1802220000020012",
          "intro": "AMS-HT C slot 3 feeder unit motor is stalled, cannot rotate the spool."
        },
        {
          "ecode": "0706230000020013",
          "intro": "AMS G slot 4 feeder unit motor has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "1802210000020013",
          "intro": "AMS-HT C slot 2 feeder unit motor has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "1802210000020016",
          "intro": "AMS-HT C slot 2 assist motor has slipped. Please pull out the filament, cut off the worn part, and then try again."
        },
        {
          "ecode": "1801220000020015",
          "intro": "AMS-HT B slot 3 filament status is abnormal, which may be due to a filament breakage inside the AMS."
        },
        {
          "ecode": "1805230000020014",
          "intro": "AMS-HT F slot 4 filament odometer has no signal, which may be due to poor contact in the odometer connector or a odometer fault."
        },
        {
          "ecode": "0707200000020025",
          "intro": "AMS H slot 1 feed resistance is too high. Please reduce the feed resistance, decrease the rotation resistance of the spool, and avoid having the filament tube too long and excessively bent."
        },
        {
          "ecode": "0707210000020025",
          "intro": "AMS H slot 2 feed resistance is too high. Please reduce the feed resistance, decrease the rotation resistance of the spool, and avoid having the filament tube too long and excessively bent."
        },
        {
          "ecode": "0703230000020025",
          "intro": "AMS D slot 4 feed resistance is too high. Please reduce the feed resistance, decrease the rotation resistance of the spool, and avoid having the filament tube too long and excessively bent."
        },
        {
          "ecode": "0703220000020025",
          "intro": "AMS D slot 3 feed resistance is too high. Please reduce the feed resistance, decrease the rotation resistance of the spool, and avoid having the filament tube too long and excessively bent."
        },
        {
          "ecode": "0700200000020025",
          "intro": "AMS A slot 1 feed resistance is too high. Please reduce the feed resistance, decrease the rotation resistance of the spool, and avoid having the filament tube too long and excessively bent."
        },
        {
          "ecode": "0705220000020025",
          "intro": "AMS F slot 3 feed resistance is too high. Please reduce the feed resistance, decrease the rotation resistance of the spool, and avoid having the filament tube too long and excessively bent."
        },
        {
          "ecode": "0701220000020025",
          "intro": "AMS B slot 3 feed resistance is too high. Please reduce the feed resistance, decrease the rotation resistance of the spool, and avoid having the filament tube too long and excessively bent."
        },
        {
          "ecode": "0706230000020025",
          "intro": "AMS G slot 4 feed resistance is too high. Please reduce the feed resistance, decrease the rotation resistance of the spool, and avoid having the filament tube too long and excessively bent."
        },
        {
          "ecode": "0706210000020025",
          "intro": "AMS G slot 2 feed resistance is too high. Please reduce the feed resistance, decrease the rotation resistance of the spool, and avoid having the filament tube too long and excessively bent."
        },
        {
          "ecode": "1807210000020025",
          "intro": "AMS-HT H slot 2 feed resistance is too high. Please reduce the feed resistance, decrease the rotation resistance of the spool, and avoid having the filament tube too long and excessively bent."
        },
        {
          "ecode": "0705210000020025",
          "intro": "AMS F slot 2 feed resistance is too high. Please reduce the feed resistance, decrease the rotation resistance of the spool, and avoid having the filament tube too long and excessively bent."
        },
        {
          "ecode": "0704230000020006",
          "intro": "AMS E has detected a breakage of the PTFE tube during filament loading. Please check whether the PTFE tubes inside and outside the AMS have fallen off or been damaged."
        },
        {
          "ecode": "1805210000020006",
          "intro": "AMS-HT F has detected a breakage of the PTFE tube during filament loading. Please check whether the PTFE tubes inside and outside the AMS have fallen off or been damaged."
        },
        {
          "ecode": "0704220000020006",
          "intro": "AMS E has detected a breakage of the PTFE tube during filament loading. Please check whether the PTFE tubes inside and outside the AMS have fallen off or been damaged."
        },
        {
          "ecode": "0701210000020006",
          "intro": "AMS B has detected a breakage of the PTFE tube during filament loading. Please check whether the PTFE tubes inside and outside the AMS have fallen off or been damaged."
        },
        {
          "ecode": "1803230000020006",
          "intro": "AMS-HT D has detected a breakage of the PTFE tube during filament loading. Please check whether the PTFE tubes inside and outside the AMS have fallen off or been damaged."
        },
        {
          "ecode": "0703220000020006",
          "intro": "AMS D has detected a breakage of the PTFE tube during filament loading. Please check whether the PTFE tubes inside and outside the AMS have fallen off or been damaged."
        },
        {
          "ecode": "1801210000020006",
          "intro": "AMS-HT B has detected a breakage of the PTFE tube during filament loading. Please check whether the PTFE tubes inside and outside the AMS have fallen off or been damaged."
        },
        {
          "ecode": "0702210000020006",
          "intro": "AMS C has detected a breakage of the PTFE tube during filament loading. Please check whether the PTFE tubes inside and outside the AMS have fallen off or been damaged."
        },
        {
          "ecode": "1801220000020006",
          "intro": "AMS-HT B has detected a breakage of the PTFE tube during filament loading. Please check whether the PTFE tubes inside and outside the AMS have fallen off or been damaged."
        },
        {
          "ecode": "1802230000020006",
          "intro": "AMS-HT C has detected a breakage of the PTFE tube during filament loading. Please check whether the PTFE tubes inside and outside the AMS have fallen off or been damaged."
        },
        {
          "ecode": "0707210000020006",
          "intro": "AMS H has detected a breakage of the PTFE tube during filament loading. Please check whether the PTFE tubes inside and outside the AMS have fallen off or been damaged."
        },
        {
          "ecode": "1802210000020006",
          "intro": "AMS-HT C has detected a breakage of the PTFE tube during filament loading. Please check whether the PTFE tubes inside and outside the AMS have fallen off or been damaged."
        },
        {
          "ecode": "1803210000020006",
          "intro": "AMS-HT D has detected a breakage of the PTFE tube during filament loading. Please check whether the PTFE tubes inside and outside the AMS have fallen off or been damaged."
        },
        {
          "ecode": "0703210000020006",
          "intro": "AMS D has detected a breakage of the PTFE tube during filament loading. Please check whether the PTFE tubes inside and outside the AMS have fallen off or been damaged."
        },
        {
          "ecode": "18FF700000020008",
          "intro": "Failed to get AMS mapping table; please select \"Resume\" to retry."
        },
        {
          "ecode": "07FF700000020008",
          "intro": "Failed to get AMS mapping table; please select \"Resume\" to retry."
        },
        {
          "ecode": "07FE700000020008",
          "intro": "Failed to get AMS mapping table; please select \"Resume\" to retry."
        },
        {
          "ecode": "18FE700000020008",
          "intro": "Failed to get AMS mapping table; please select \"Resume\" to retry."
        },
        {
          "ecode": "0300960000010003",
          "intro": "The front door Hall sensor is abnormal; please check whether the connection wire is loose."
        },
        {
          "ecode": "1800400000020001",
          "intro": "AMS-HT A Filament buffer position signal lost: the cable or position sensor may be malfunctioning."
        },
        {
          "ecode": "0707400000020001",
          "intro": "AMS H Filament buffer position signal lost: the cable or position sensor may be malfunctioning."
        },
        {
          "ecode": "1806400000020001",
          "intro": "AMS-HT G Filament buffer position signal lost: the cable or position sensor may be malfunctioning."
        },
        {
          "ecode": "1802400000020001",
          "intro": "AMS-HT C Filament buffer position signal lost: the cable or position sensor may be malfunctioning."
        },
        {
          "ecode": "1804400000020001",
          "intro": "AMS-HT E Filament buffer position signal lost: the cable or position sensor may be malfunctioning."
        },
        {
          "ecode": "1807400000020001",
          "intro": "AMS-HT H Filament buffer position signal lost: the cable or position sensor may be malfunctioning."
        },
        {
          "ecode": "0700400000020001",
          "intro": "AMS A Filament buffer position signal lost: the cable or position sensor may be malfunctioning."
        },
        {
          "ecode": "1803400000020001",
          "intro": "AMS-HT D Filament buffer position signal lost: the cable or position sensor may be malfunctioning."
        },
        {
          "ecode": "0701400000020001",
          "intro": "AMS B Filament buffer position signal lost: the cable or position sensor may be malfunctioning."
        },
        {
          "ecode": "050003000001000E",
          "intro": "Some external modules are incompatible with the printer's firmware version, which may affect normal operation. Please go to the \"Firmware\" page while connected to the internet to upgrade."
        },
        {
          "ecode": "1801400000020001",
          "intro": "AMS-HT B Filament buffer position signal lost: the cable or position sensor may be malfunctioning."
        },
        {
          "ecode": "0705400000020001",
          "intro": "AMS F Filament buffer position signal lost: the cable or position sensor may be malfunctioning."
        },
        {
          "ecode": "1805400000020001",
          "intro": "AMS-HT F Filament buffer position signal lost: the cable or position sensor may be malfunctioning."
        },
        {
          "ecode": "0706400000020001",
          "intro": "AMS G Filament buffer position signal lost: the cable or position sensor may be malfunctioning."
        },
        {
          "ecode": "0702400000020001",
          "intro": "AMS C Filament buffer position signal lost: the cable or position sensor may be malfunctioning."
        },
        {
          "ecode": "0703400000020001",
          "intro": "AMS D Filament buffer position signal lost: the cable or position sensor may be malfunctioning."
        },
        {
          "ecode": "0704400000020001",
          "intro": "AMS E Filament buffer position signal lost: the cable or position sensor may be malfunctioning."
        },
        {
          "ecode": "0700900000010002",
          "intro": "AMS A The coil resistance of exhaust valve 1 is abnormal, which may be due to abnormal wiring or damage."
        },
        {
          "ecode": "1803910000010002",
          "intro": "AMS-HT D The coil resistance of exhaust valve 2 is abnormal, which may be due to abnormal wiring or damage."
        },
        {
          "ecode": "0706900000010002",
          "intro": "AMS G The coil resistance of exhaust valve 1 is abnormal, which may be due to abnormal wiring or damage."
        },
        {
          "ecode": "1800910000010002",
          "intro": "AMS-HT A The coil resistance of exhaust valve 2 is abnormal, which may be due to abnormal wiring or damage."
        },
        {
          "ecode": "1804910000010002",
          "intro": "AMS-HT E The coil resistance of exhaust valve 2 is abnormal, which may be due to abnormal wiring or damage."
        },
        {
          "ecode": "0703910000010002",
          "intro": "AMS D The coil resistance of exhaust valve 2 is abnormal, which may be due to abnormal wiring or damage."
        },
        {
          "ecode": "1806900000010002",
          "intro": "AMS-HT G The coil resistance of exhaust valve 1 is abnormal, which may be due to abnormal wiring or damage."
        },
        {
          "ecode": "0701900000010002",
          "intro": "AMS B The coil resistance of exhaust valve 1 is abnormal, which may be due to abnormal wiring or damage."
        },
        {
          "ecode": "1806910000010002",
          "intro": "AMS-HT G The coil resistance of exhaust valve 2 is abnormal, which may be due to abnormal wiring or damage."
        },
        {
          "ecode": "0705900000010002",
          "intro": "AMS F The coil resistance of exhaust valve 1 is abnormal, which may be due to abnormal wiring or damage."
        },
        {
          "ecode": "1802900000010002",
          "intro": "AMS-HT C The coil resistance of exhaust valve 1 is abnormal, which may be due to abnormal wiring or damage."
        },
        {
          "ecode": "0706910000010002",
          "intro": "AMS G The coil resistance of exhaust valve 2 is abnormal, which may be due to abnormal wiring or damage."
        },
        {
          "ecode": "0705910000010002",
          "intro": "AMS F The coil resistance of exhaust valve 2 is abnormal, which may be due to abnormal wiring or damage."
        },
        {
          "ecode": "1802910000010002",
          "intro": "AMS-HT C The coil resistance of exhaust valve 2 is abnormal, which may be due to abnormal wiring or damage."
        },
        {
          "ecode": "1801900000010002",
          "intro": "AMS-HT B The coil resistance of exhaust valve 1 is abnormal, which may be due to abnormal wiring or damage."
        },
        {
          "ecode": "0703900000010002",
          "intro": "AMS D The coil resistance of exhaust valve 1 is abnormal, which may be due to abnormal wiring or damage."
        },
        {
          "ecode": "1801910000010002",
          "intro": "AMS-HT B The coil resistance of exhaust valve 2 is abnormal, which may be due to abnormal wiring or damage."
        },
        {
          "ecode": "1805910000010002",
          "intro": "AMS-HT F The coil resistance of exhaust valve 2 is abnormal, which may be due to abnormal wiring or damage."
        },
        {
          "ecode": "0704910000010002",
          "intro": "AMS E The coil resistance of exhaust valve 2 is abnormal, which may be due to abnormal wiring or damage."
        },
        {
          "ecode": "0701910000010002",
          "intro": "AMS B The coil resistance of exhaust valve 2 is abnormal, which may be due to abnormal wiring or damage."
        },
        {
          "ecode": "1804900000010002",
          "intro": "AMS-HT E The coil resistance of exhaust valve 1 is abnormal, which may be due to abnormal wiring or damage."
        },
        {
          "ecode": "1805900000010002",
          "intro": "AMS-HT F The coil resistance of exhaust valve 1 is abnormal, which may be due to abnormal wiring or damage."
        },
        {
          "ecode": "0702900000010002",
          "intro": "AMS C The coil resistance of exhaust valve 1 is abnormal, which may be due to abnormal wiring or damage."
        },
        {
          "ecode": "1807900000010002",
          "intro": "AMS-HT H The coil resistance of exhaust valve 1 is abnormal, which may be due to abnormal wiring or damage."
        },
        {
          "ecode": "0707900000010002",
          "intro": "AMS H The coil resistance of exhaust valve 1 is abnormal, which may be due to abnormal wiring or damage."
        },
        {
          "ecode": "0700910000010002",
          "intro": "AMS A The coil resistance of exhaust valve 2 is abnormal, which may be due to abnormal wiring or damage."
        },
        {
          "ecode": "0707910000010002",
          "intro": "AMS H The coil resistance of exhaust valve 2 is abnormal, which may be due to abnormal wiring or damage."
        },
        {
          "ecode": "0704900000010002",
          "intro": "AMS E The coil resistance of exhaust valve 1 is abnormal, which may be due to abnormal wiring or damage."
        },
        {
          "ecode": "1807910000010002",
          "intro": "AMS-HT H The coil resistance of exhaust valve 2 is abnormal, which may be due to abnormal wiring or damage."
        },
        {
          "ecode": "0702910000010002",
          "intro": "AMS C The coil resistance of exhaust valve 2 is abnormal, which may be due to abnormal wiring or damage."
        },
        {
          "ecode": "1803900000010002",
          "intro": "AMS-HT D The coil resistance of exhaust valve 1 is abnormal, which may be due to abnormal wiring or damage."
        },
        {
          "ecode": "1800900000010002",
          "intro": "AMS-HT A The coil resistance of exhaust valve 1 is abnormal, which may be due to abnormal wiring or damage."
        },
        {
          "ecode": "0707230000020023",
          "intro": "AMS H slot 4 the tube inside the AMS is broken, or feed-out hall sensor is faulty and cannot detect the filament."
        },
        {
          "ecode": "0702230000020023",
          "intro": "AMS C slot 4 the tube inside the AMS is broken, or feed-out hall sensor is faulty and cannot detect the filament."
        },
        {
          "ecode": "1804210000020023",
          "intro": "AMS-HT E slot 2 the tube inside the AMS is broken, or feed-out hall sensor is faulty and cannot detect the filament."
        },
        {
          "ecode": "1801230000020023",
          "intro": "AMS-HT B slot 4 the tube inside the AMS is broken, or feed-out hall sensor is faulty and cannot detect the filament."
        },
        {
          "ecode": "1802220000020023",
          "intro": "AMS-HT C slot 3 the tube inside the AMS is broken, or feed-out hall sensor is faulty and cannot detect the filament."
        },
        {
          "ecode": "0704200000020023",
          "intro": "AMS E slot 1 the tube inside the AMS is broken, or feed-out hall sensor is faulty and cannot detect the filament."
        },
        {
          "ecode": "1805210000020023",
          "intro": "AMS-HT F slot 2 the tube inside the AMS is broken, or feed-out hall sensor is faulty and cannot detect the filament."
        },
        {
          "ecode": "0702210000020023",
          "intro": "AMS C slot 2 the tube inside the AMS is broken, or feed-out hall sensor is faulty and cannot detect the filament."
        },
        {
          "ecode": "1800210000020023",
          "intro": "AMS-HT A slot 2 the tube inside the AMS is broken, or feed-out hall sensor is faulty and cannot detect the filament."
        },
        {
          "ecode": "1803200000020023",
          "intro": "AMS-HT D slot 1 the tube inside the AMS is broken, or feed-out hall sensor is faulty and cannot detect the filament."
        },
        {
          "ecode": "1802210000020023",
          "intro": "AMS-HT C slot 2 the tube inside the AMS is broken, or feed-out hall sensor is faulty and cannot detect the filament."
        },
        {
          "ecode": "0704210000020023",
          "intro": "AMS E slot 2 the tube inside the AMS is broken, or feed-out hall sensor is faulty and cannot detect the filament."
        },
        {
          "ecode": "0700210000020023",
          "intro": "AMS A slot 2 the tube inside the AMS is broken, or feed-out hall sensor is faulty and cannot detect the filament."
        },
        {
          "ecode": "0703220000020023",
          "intro": "AMS D slot 3 the tube inside the AMS is broken, or feed-out hall sensor is faulty and cannot detect the filament."
        },
        {
          "ecode": "1801200000020023",
          "intro": "AMS-HT B slot 1 the tube inside the AMS is broken, or feed-out hall sensor is faulty and cannot detect the filament."
        },
        {
          "ecode": "0701220000020023",
          "intro": "AMS B slot 3 the tube inside the AMS is broken, or feed-out hall sensor is faulty and cannot detect the filament."
        },
        {
          "ecode": "1806210000020023",
          "intro": "AMS-HT G slot 2 the tube inside the AMS is broken, or feed-out hall sensor is faulty and cannot detect the filament."
        },
        {
          "ecode": "1807200000020023",
          "intro": "AMS-HT H slot 1 the tube inside the AMS is broken, or feed-out hall sensor is faulty and cannot detect the filament."
        },
        {
          "ecode": "0700230000020023",
          "intro": "AMS A slot 4 the tube inside the AMS is broken, or feed-out hall sensor is faulty and cannot detect the filament."
        },
        {
          "ecode": "0705980000020002",
          "intro": "AMS F The power adapter voltage is too high, which may damage the heater circuit. Please replace the power adapter."
        },
        {
          "ecode": "0587050000010017",
          "intro": "AMS-HT H certification failed. Please reconnect the cable or restart the printer."
        },
        {
          "ecode": "1806980000020002",
          "intro": "AMS-HT G The power adapter voltage is too high, which may damage the heater circuit. Please replace the power adapter."
        },
        {
          "ecode": "0706980000020001",
          "intro": "AMS G The power adapter voltage is too low, which may result in insufficient drying temperature. Please replace the power adapter."
        },
        {
          "ecode": "1805980000020002",
          "intro": "AMS-HT F The power adapter voltage is too high, which may damage the heater circuit. Please replace the power adapter."
        },
        {
          "ecode": "1802230000020023",
          "intro": "AMS-HT C slot 4 the tube inside the AMS is broken, or feed-out hall sensor is faulty and cannot detect the filament."
        },
        {
          "ecode": "0700220000020023",
          "intro": "AMS A slot 3 the tube inside the AMS is broken, or feed-out hall sensor is faulty and cannot detect the filament."
        },
        {
          "ecode": "1802200000020023",
          "intro": "AMS-HT C slot 1 the tube inside the AMS is broken, or feed-out hall sensor is faulty and cannot detect the filament."
        },
        {
          "ecode": "0703210000020023",
          "intro": "AMS D slot 2 the tube inside the AMS is broken, or feed-out hall sensor is faulty and cannot detect the filament."
        },
        {
          "ecode": "1806230000020023",
          "intro": "AMS-HT G slot 4 the tube inside the AMS is broken, or feed-out hall sensor is faulty and cannot detect the filament."
        },
        {
          "ecode": "1806200000020023",
          "intro": "AMS-HT G slot 1 the tube inside the AMS is broken, or feed-out hall sensor is faulty and cannot detect the filament."
        },
        {
          "ecode": "1805200000020023",
          "intro": "AMS-HT F slot 1 the tube inside the AMS is broken, or feed-out hall sensor is faulty and cannot detect the filament."
        },
        {
          "ecode": "0706230000020023",
          "intro": "AMS G slot 4 the tube inside the AMS is broken, or feed-out hall sensor is faulty and cannot detect the filament."
        },
        {
          "ecode": "0700200000020023",
          "intro": "AMS A slot 1 the tube inside the AMS is broken, or feed-out hall sensor is faulty and cannot detect the filament."
        },
        {
          "ecode": "0704220000020023",
          "intro": "AMS E slot 3 the tube inside the AMS is broken, or feed-out hall sensor is faulty and cannot detect the filament."
        },
        {
          "ecode": "0500030000010004",
          "intro": "The Filament Buffer module is malfunctioning. Please restart the device."
        },
        {
          "ecode": "0706220000020023",
          "intro": "AMS G slot 3 the tube inside the AMS is broken, or feed-out hall sensor is faulty and cannot detect the filament."
        },
        {
          "ecode": "1807210000020023",
          "intro": "AMS-HT H slot 2 the tube inside the AMS is broken, or feed-out hall sensor is faulty and cannot detect the filament."
        },
        {
          "ecode": "0707220000020023",
          "intro": "AMS H slot 3 the tube inside the AMS is broken, or feed-out hall sensor is faulty and cannot detect the filament."
        },
        {
          "ecode": "1804230000020023",
          "intro": "AMS-HT E slot 4 the tube inside the AMS is broken, or feed-out hall sensor is faulty and cannot detect the filament."
        },
        {
          "ecode": "0702200000020023",
          "intro": "AMS C slot 1 the tube inside the AMS is broken, or feed-out hall sensor is faulty and cannot detect the filament."
        },
        {
          "ecode": "0702220000020023",
          "intro": "AMS C slot 3 the tube inside the AMS is broken, or feed-out hall sensor is faulty and cannot detect the filament."
        },
        {
          "ecode": "0701230000020023",
          "intro": "AMS B slot 4 the tube inside the AMS is broken, or feed-out hall sensor is faulty and cannot detect the filament."
        },
        {
          "ecode": "1801220000020023",
          "intro": "AMS-HT B slot 3 the tube inside the AMS is broken, or feed-out hall sensor is faulty and cannot detect the filament."
        },
        {
          "ecode": "1800220000020023",
          "intro": "AMS-HT A slot 3 the tube inside the AMS is broken, or feed-out hall sensor is faulty and cannot detect the filament."
        },
        {
          "ecode": "1805220000020023",
          "intro": "AMS-HT F slot 3 the tube inside the AMS is broken, or feed-out hall sensor is faulty and cannot detect the filament."
        },
        {
          "ecode": "0705220000020023",
          "intro": "AMS F slot 3 the tube inside the AMS is broken, or feed-out hall sensor is faulty and cannot detect the filament."
        },
        {
          "ecode": "0705210000020023",
          "intro": "AMS F slot 2 the tube inside the AMS is broken, or feed-out hall sensor is faulty and cannot detect the filament."
        },
        {
          "ecode": "0704230000020023",
          "intro": "AMS E slot 4 the tube inside the AMS is broken, or feed-out hall sensor is faulty and cannot detect the filament."
        },
        {
          "ecode": "1803230000020023",
          "intro": "AMS-HT D slot 4 the tube inside the AMS is broken, or feed-out hall sensor is faulty and cannot detect the filament."
        },
        {
          "ecode": "0706200000020023",
          "intro": "AMS G slot 1 the tube inside the AMS is broken, or feed-out hall sensor is faulty and cannot detect the filament."
        },
        {
          "ecode": "0705230000020023",
          "intro": "AMS F slot 4 the tube inside the AMS is broken, or feed-out hall sensor is faulty and cannot detect the filament."
        },
        {
          "ecode": "1803210000020023",
          "intro": "AMS-HT D slot 2 the tube inside the AMS is broken, or feed-out hall sensor is faulty and cannot detect the filament."
        },
        {
          "ecode": "1807220000020023",
          "intro": "AMS-HT H slot 3 the tube inside the AMS is broken, or feed-out hall sensor is faulty and cannot detect the filament."
        },
        {
          "ecode": "1804200000020023",
          "intro": "AMS-HT E slot 1 the tube inside the AMS is broken, or feed-out hall sensor is faulty and cannot detect the filament."
        },
        {
          "ecode": "0701200000020023",
          "intro": "AMS B slot 1 the tube inside the AMS is broken, or feed-out hall sensor is faulty and cannot detect the filament."
        },
        {
          "ecode": "0707200000020023",
          "intro": "AMS H slot 1 the tube inside the AMS is broken, or feed-out hall sensor is faulty and cannot detect the filament."
        },
        {
          "ecode": "1801210000020023",
          "intro": "AMS-HT B slot 2 the tube inside the AMS is broken, or feed-out hall sensor is faulty and cannot detect the filament."
        },
        {
          "ecode": "1804220000020023",
          "intro": "AMS-HT E slot 3 the tube inside the AMS is broken, or feed-out hall sensor is faulty and cannot detect the filament."
        },
        {
          "ecode": "0580050000010017",
          "intro": "AMS-HT A certification failed. Please reconnect the cable or restart the printer."
        },
        {
          "ecode": "1804980000020002",
          "intro": "AMS-HT E The power adapter voltage is too high, which may damage the heater circuit. Please replace the power adapter."
        },
        {
          "ecode": "0702980000020002",
          "intro": "AMS C The power adapter voltage is too high, which may damage the heater circuit. Please replace the power adapter."
        },
        {
          "ecode": "0500050000010014",
          "intro": "AMS A certification failed. Please reconnect the cable or restart the printer."
        },
        {
          "ecode": "0701980000020001",
          "intro": "AMS B The power adapter voltage is too low, which may result in insufficient drying temperature. Please replace the power adapter."
        },
        {
          "ecode": "1803980000020001",
          "intro": "AMS-HT D The power adapter voltage is too low, which may result in insufficient drying temperature. Please replace the power adapter."
        },
        {
          "ecode": "0707980000020002",
          "intro": "AMS H The power adapter voltage is too high, which may damage the heater circuit. Please replace the power adapter."
        },
        {
          "ecode": "0581050000010017",
          "intro": "AMS-HT B certification failed. Please reconnect the cable or restart the printer."
        },
        {
          "ecode": "0585050000010017",
          "intro": "AMS-HT F certification failed. Please reconnect the cable or restart the printer."
        },
        {
          "ecode": "0703980000020001",
          "intro": "AMS D The power adapter voltage is too low, which may result in insufficient drying temperature. Please replace the power adapter."
        },
        {
          "ecode": "1807980000020001",
          "intro": "AMS-HT H The power adapter voltage is too low, which may result in insufficient drying temperature. Please replace the power adapter."
        },
        {
          "ecode": "1803980000020002",
          "intro": "AMS-HT D The power adapter voltage is too high, which may damage the heater circuit. Please replace the power adapter."
        },
        {
          "ecode": "1806980000020001",
          "intro": "AMS-HT G The power adapter voltage is too low, which may result in insufficient drying temperature. Please replace the power adapter."
        },
        {
          "ecode": "0701980000020002",
          "intro": "AMS B The power adapter voltage is too high, which may damage the heater circuit. Please replace the power adapter."
        },
        {
          "ecode": "1802980000020002",
          "intro": "AMS-HT C The power adapter voltage is too high, which may damage the heater circuit. Please replace the power adapter."
        },
        {
          "ecode": "0501050000010014",
          "intro": "AMS B certification failed. Please reconnect the cable or restart the printer."
        },
        {
          "ecode": "0584050000010017",
          "intro": "AMS-HT E certification failed. Please reconnect the cable or restart the printer."
        },
        {
          "ecode": "0502050000010014",
          "intro": "AMS C certification failed. Please reconnect the cable or restart the printer."
        },
        {
          "ecode": "0586050000010017",
          "intro": "AMS-HT G certification failed. Please reconnect the cable or restart the printer."
        },
        {
          "ecode": "1801980000020002",
          "intro": "AMS-HT B The power adapter voltage is too high, which may damage the heater circuit. Please replace the power adapter."
        },
        {
          "ecode": "1804980000020001",
          "intro": "AMS-HT E The power adapter voltage is too low, which may result in insufficient drying temperature. Please replace the power adapter."
        },
        {
          "ecode": "1805980000020001",
          "intro": "AMS-HT F The power adapter voltage is too low, which may result in insufficient drying temperature. Please replace the power adapter."
        },
        {
          "ecode": "0700980000020002",
          "intro": "AMS A The power adapter voltage is too high, which may damage the heater circuit. Please replace the power adapter."
        },
        {
          "ecode": "0700980000020001",
          "intro": "AMS A The power adapter voltage is too low, which may result in insufficient drying temperature. Please replace the power adapter."
        },
        {
          "ecode": "0503050000010014",
          "intro": "AMS D certification failed. Please reconnect the cable or restart the printer."
        },
        {
          "ecode": "1802980000020001",
          "intro": "AMS-HT C The power adapter voltage is too low, which may result in insufficient drying temperature. Please replace the power adapter."
        },
        {
          "ecode": "0702980000020001",
          "intro": "AMS C The power adapter voltage is too low, which may result in insufficient drying temperature. Please replace the power adapter."
        },
        {
          "ecode": "0704980000020001",
          "intro": "AMS E The power adapter voltage is too low, which may result in insufficient drying temperature. Please replace the power adapter."
        },
        {
          "ecode": "1807980000020002",
          "intro": "AMS-HT H The power adapter voltage is too high, which may damage the heater circuit. Please replace the power adapter."
        },
        {
          "ecode": "0703980000020002",
          "intro": "AMS D The power adapter voltage is too high, which may damage the heater circuit. Please replace the power adapter."
        },
        {
          "ecode": "0582050000010017",
          "intro": "AMS-HT C certification failed. Please reconnect the cable or restart the printer."
        },
        {
          "ecode": "0704980000020002",
          "intro": "AMS E The power adapter voltage is too high, which may damage the heater circuit. Please replace the power adapter."
        },
        {
          "ecode": "1800200000020023",
          "intro": "AMS-HT A slot 1 the tube inside the AMS is broken, or feed-out hall sensor is faulty and cannot detect the filament."
        },
        {
          "ecode": "0707210000020023",
          "intro": "AMS H slot 2 the tube inside the AMS is broken, or feed-out hall sensor is faulty and cannot detect the filament."
        },
        {
          "ecode": "0705200000020023",
          "intro": "AMS F slot 1 the tube inside the AMS is broken, or feed-out hall sensor is faulty and cannot detect the filament."
        },
        {
          "ecode": "1807230000020023",
          "intro": "AMS-HT H slot 4 the tube inside the AMS is broken, or feed-out hall sensor is faulty and cannot detect the filament."
        },
        {
          "ecode": "0703200000020023",
          "intro": "AMS D slot 1 the tube inside the AMS is broken, or feed-out hall sensor is faulty and cannot detect the filament."
        },
        {
          "ecode": "1803220000020023",
          "intro": "AMS-HT D slot 3 the tube inside the AMS is broken, or feed-out hall sensor is faulty and cannot detect the filament."
        },
        {
          "ecode": "0703230000020023",
          "intro": "AMS D slot 4 the tube inside the AMS is broken, or feed-out hall sensor is faulty and cannot detect the filament."
        },
        {
          "ecode": "1805230000020023",
          "intro": "AMS-HT F slot 4 the tube inside the AMS is broken, or feed-out hall sensor is faulty and cannot detect the filament."
        },
        {
          "ecode": "1806220000020023",
          "intro": "AMS-HT G slot 3 the tube inside the AMS is broken, or feed-out hall sensor is faulty and cannot detect the filament."
        },
        {
          "ecode": "1800230000020023",
          "intro": "AMS-HT A slot 4 the tube inside the AMS is broken, or feed-out hall sensor is faulty and cannot detect the filament."
        },
        {
          "ecode": "0706210000020023",
          "intro": "AMS G slot 2 the tube inside the AMS is broken, or feed-out hall sensor is faulty and cannot detect the filament."
        },
        {
          "ecode": "0701210000020023",
          "intro": "AMS B slot 2 the tube inside the AMS is broken, or feed-out hall sensor is faulty and cannot detect the filament."
        },
        {
          "ecode": "0706980000020002",
          "intro": "AMS G The power adapter voltage is too high, which may damage the heater circuit. Please replace the power adapter."
        },
        {
          "ecode": "1800980000020001",
          "intro": "AMS-HT A The power adapter voltage is too low, which may result in insufficient drying temperature. Please replace the power adapter."
        },
        {
          "ecode": "0705980000020001",
          "intro": "AMS F The power adapter voltage is too low, which may result in insufficient drying temperature. Please replace the power adapter."
        },
        {
          "ecode": "0707980000020001",
          "intro": "AMS H The power adapter voltage is too low, which may result in insufficient drying temperature. Please replace the power adapter."
        },
        {
          "ecode": "1800980000020002",
          "intro": "AMS-HT A The power adapter voltage is too high, which may damage the heater circuit. Please replace the power adapter."
        },
        {
          "ecode": "1801980000020001",
          "intro": "AMS-HT B The power adapter voltage is too low, which may result in insufficient drying temperature. Please replace the power adapter."
        },
        {
          "ecode": "0583050000010017",
          "intro": "AMS-HT D certification failed. Please reconnect the cable or restart the printer."
        },
        {
          "ecode": "0C00010000010001",
          "intro": "Micro Lidar is offline. Please check the hardware connection."
        },
        {
          "ecode": "0C00010000010005",
          "intro": "Micro Lidar parameter is abnormal. Please contact customer support."
        },
        {
          "ecode": "0C00010000010003",
          "intro": "Synchronization between the Micro Lidar and MC is abnormal. Please restart your printer."
        },
        {
          "ecode": "0C00010000010004",
          "intro": "Micro Lidar lens seems to be dirty. Please clean the lens."
        },
        {
          "ecode": "0C00010000020002",
          "intro": "Micro Lidar camera is malfunctioning. Please refer to the Wiki for troubleshooting."
        },
        {
          "ecode": "0700920000020003",
          "intro": "The AMS A heater 1 cooling fan cannot start because the power adapter is not connected."
        },
        {
          "ecode": "1805930000020003",
          "intro": "The AMS-HT F heater 2 cooling fan cannot start because the power adapter is not connected."
        },
        {
          "ecode": "0700930000020003",
          "intro": "The AMS A heater 2 cooling fan cannot start because the power adapter is not connected."
        },
        {
          "ecode": "1805920000020003",
          "intro": "The AMS-HT F heater 1 cooling fan cannot start because the power adapter is not connected."
        },
        {
          "ecode": "1804930000020003",
          "intro": "The AMS-HT E heater 2 cooling fan cannot start because the power adapter is not connected."
        },
        {
          "ecode": "0707930000020003",
          "intro": "The AMS H heater 2 cooling fan cannot start because the power adapter is not connected."
        },
        {
          "ecode": "1803920000020003",
          "intro": "The AMS-HT D heater 1 cooling fan cannot start because the power adapter is not connected."
        },
        {
          "ecode": "0C00040000010025",
          "intro": "The device malfunctioned; please restart."
        },
        {
          "ecode": "0701920000020003",
          "intro": "The AMS B heater 1 cooling fan cannot start because the power adapter is not connected."
        },
        {
          "ecode": "0706930000020003",
          "intro": "The AMS G heater 2 cooling fan cannot start because the power adapter is not connected."
        },
        {
          "ecode": "0C00030000020019",
          "intro": "The Vision Encoder Plate is either not placed or incorrectly placed. Please ensure it is correctly positioned on the heatbed."
        },
        {
          "ecode": "1804920000020003",
          "intro": "The AMS-HT E heater 1 cooling fan cannot start because the power adapter is not connected."
        },
        {
          "ecode": "0704930000020003",
          "intro": "The AMS E heater 2 cooling fan cannot start because the power adapter is not connected."
        },
        {
          "ecode": "0706920000020003",
          "intro": "The AMS G heater 1 cooling fan cannot start because the power adapter is not connected."
        },
        {
          "ecode": "0703930000020003",
          "intro": "The AMS D heater 2 cooling fan cannot start because the power adapter is not connected."
        },
        {
          "ecode": "0705930000020003",
          "intro": "The AMS F heater 2 cooling fan cannot start because the power adapter is not connected."
        },
        {
          "ecode": "0704920000020003",
          "intro": "The AMS E heater 1 cooling fan cannot start because the power adapter is not connected."
        },
        {
          "ecode": "1806920000020003",
          "intro": "The AMS-HT G heater 1 cooling fan cannot start because the power adapter is not connected."
        },
        {
          "ecode": "1801930000020003",
          "intro": "The AMS-HT B heater 2 cooling fan cannot start because the power adapter is not connected."
        },
        {
          "ecode": "1807920000020003",
          "intro": "The AMS-HT H heater 1 cooling fan cannot start because the power adapter is not connected."
        },
        {
          "ecode": "1807930000020003",
          "intro": "The AMS-HT H heater 2 cooling fan cannot start because the power adapter is not connected."
        },
        {
          "ecode": "0703920000020003",
          "intro": "The AMS D heater 1 cooling fan cannot start because the power adapter is not connected."
        },
        {
          "ecode": "1802930000020003",
          "intro": "The AMS-HT C heater 2 cooling fan cannot start because the power adapter is not connected."
        },
        {
          "ecode": "0701930000020003",
          "intro": "The AMS B heater 2 cooling fan cannot start because the power adapter is not connected."
        },
        {
          "ecode": "0707920000020003",
          "intro": "The AMS H heater 1 cooling fan cannot start because the power adapter is not connected."
        },
        {
          "ecode": "1801920000020003",
          "intro": "The AMS-HT B heater 1 cooling fan cannot start because the power adapter is not connected."
        },
        {
          "ecode": "1806930000020003",
          "intro": "The AMS-HT G heater 2 cooling fan cannot start because the power adapter is not connected."
        },
        {
          "ecode": "1800920000020003",
          "intro": "The AMS-HT A heater 1 cooling fan cannot start because the power adapter is not connected."
        },
        {
          "ecode": "1800930000020003",
          "intro": "The AMS-HT A heater 2 cooling fan cannot start because the power adapter is not connected."
        },
        {
          "ecode": "0702930000020003",
          "intro": "The AMS C heater 2 cooling fan cannot start because the power adapter is not connected."
        },
        {
          "ecode": "0702920000020003",
          "intro": "The AMS C heater 1 cooling fan cannot start because the power adapter is not connected."
        },
        {
          "ecode": "1803930000020003",
          "intro": "The AMS-HT D heater 2 cooling fan cannot start because the power adapter is not connected."
        },
        {
          "ecode": "0705920000020003",
          "intro": "The AMS F heater 1 cooling fan cannot start because the power adapter is not connected."
        },
        {
          "ecode": "1802920000020003",
          "intro": "The AMS-HT C heater 1 cooling fan cannot start because the power adapter is not connected."
        },
        {
          "ecode": "0702560000030001",
          "intro": "AMS C is undergoing dry cooling; please wait for it to cool down before operating."
        },
        {
          "ecode": "0701210000020002",
          "intro": "AMS B Slot 2 is empty; please insert a new filament."
        },
        {
          "ecode": "1803700000020001",
          "intro": "Failed to pull out the filament from the extruder. Possible causes: clogged extruder or broken filament."
        },
        {
          "ecode": "1804220000020011",
          "intro": "AMS-HT E slot 3 pulls filament back to AMS timeout."
        },
        {
          "ecode": "1801700000020007",
          "intro": "AMS-HT filament ran out. Please put a new filament into the same slot in AMS and resume."
        },
        {
          "ecode": "0701310000010004",
          "intro": "Encryption chip failure"
        },
        {
          "ecode": "0702020000010001",
          "intro": "AMS C Filament speed and length error: The filament odometry may be faulty."
        },
        {
          "ecode": "0706230000010086",
          "intro": "Failed to read the filament information from AMS G slot 4. The RFID tag cannot rotate due to a jam during the filament loading or unloading. Please pull out the filament and try again."
        },
        {
          "ecode": "1804220000020007",
          "intro": "AMS-HT E Slot 3 feed-out Hall sensor is disconnected. The connector may have poor contact."
        },
        {
          "ecode": "0701210000020009",
          "intro": "Failed to extrude AMS B Slot 2 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "0704500000020001",
          "intro": "AMS E communication is abnormal; please check the connection cable."
        },
        {
          "ecode": "0706210000020022",
          "intro": "AMS G slot 2 assist motor is stalled，due to excessive resistance in the tube near the toolhead."
        },
        {
          "ecode": "1802100000020002",
          "intro": "The AMS-HT C slot 1 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "1800210000020001",
          "intro": "AMS-HT A Slot 2 filament has run out. Please insert a new filament."
        },
        {
          "ecode": "0702230000020010",
          "intro": "AMS C slot 4 feeds filament out of AMS timeout."
        },
        {
          "ecode": "1803810000010003",
          "intro": "AMS-HT D The heater 2 is short-circuited, which may be due to a wiring short or heater damage."
        },
        {
          "ecode": "0300010000010002",
          "intro": "The heatbed temperature is abnormal; the heater may have an open circuit, or the thermal switch may be open."
        },
        {
          "ecode": "1800010000020009",
          "intro": "AMS-HT A The assist motor has unbalanced tree-phase resistaance. The assist motor may be faulty."
        },
        {
          "ecode": "1800200000020019",
          "intro": "AMS-HT A slot 1 assist motor is stalled，due to excessive resistance in the tube between AMS and the filament buffer."
        },
        {
          "ecode": "1804230000020003",
          "intro": "AMS-HT E Slot 4's filament may be broken in AMS-HT."
        },
        {
          "ecode": "0706220000020009",
          "intro": "Failed to extrude AMS G Slot 3 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "1800200000020002",
          "intro": "AMS-HT A Slot 1 is empty; please insert a new filament."
        },
        {
          "ecode": "1201230000020001",
          "intro": "AMS B Slot4 filament has run out; please insert a new filament."
        },
        {
          "ecode": "030091000001000A",
          "intro": "The temperature of chamber heater 1 is abnormal. The AC board may be broken."
        },
        {
          "ecode": "0701200000020020",
          "intro": "AMS B slot 1 assist motor is stalled，due to excessive resistance in the tube near the filament buffer。"
        },
        {
          "ecode": "1804220000020018",
          "intro": "AMS-HT E slot 3 assist motor is stalled，due to excessive resistance in the tube near AMS."
        },
        {
          "ecode": "1203210000030001",
          "intro": "AMS D Slot2 filament has run out. Purging the old filament; please wait."
        },
        {
          "ecode": "0700200000020005",
          "intro": "AMS A Slot 1 filament has run out, and purging the old filament went abnormally; please check whether the filament is stuck in the tool head."
        },
        {
          "ecode": "1807230000020004",
          "intro": "AMS-HT H Slot 4 filament may be broken in the tool head."
        },
        {
          "ecode": "0707960000010001",
          "intro": "AMS H The drying process may experience thermal runaway. Please turn off the AMS power supply."
        },
        {
          "ecode": "1801100000020004",
          "intro": "AMS-HT B The brushed motor 1 has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "1807230000020007",
          "intro": "AMS-HT H Slot 4 feed-out Hall sensor is disconnected. The connector may have poor contact."
        },
        {
          "ecode": "1805010000010005",
          "intro": "AMS-HT F The current sensor of assist motor may be faulty."
        },
        {
          "ecode": "1806210000020017",
          "intro": "AMS-HT G slot 2 assist motor is stalled，due to excessive resistance in the tube between AMS and the printer."
        },
        {
          "ecode": "1801200000020009",
          "intro": "Failed to extrude AMS-HT B Slot 1 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "1800700000020003",
          "intro": "Failed to extrude the filament. Possible cause: extruder or nozzle clog."
        },
        {
          "ecode": "1807010000020008",
          "intro": "AMS-HT H The assist motor phase winding has an open circuit. The assist motor may be faulty."
        },
        {
          "ecode": "1803220000030001",
          "intro": "AMS-HT D Slot 3 filament has run out. Please wait while old filament is purged."
        },
        {
          "ecode": "1803200000030001",
          "intro": "AMS-HT D Slot 1 filament has run out. Please wait while old filament is purged."
        },
        {
          "ecode": "0706200000020011",
          "intro": "AMS G slot 1 pulls filament back to AMS timeout."
        },
        {
          "ecode": "0703230000010086",
          "intro": "Failed to read the filament information from AMS D slot 4. The RFID tag cannot rotate due to a jam during the filament loading or unloading. Please pull out the filament and try again."
        },
        {
          "ecode": "1202800000020001",
          "intro": "AMS C Slot1 filament may be tangled or stuck."
        },
        {
          "ecode": "1806230000020001",
          "intro": "AMS-HT G Slot 4 filament has run out. Please insert a new filament."
        },
        {
          "ecode": "1802210000010085",
          "intro": "Failed to read the filament information from AMS-HT C slot 2. RFID tag verification failed. You can try to use Bambu Lab filament."
        },
        {
          "ecode": "1805210000030002",
          "intro": "AMS-HT F Slot 2 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "1802300000020002",
          "intro": "The RFID-tag on AMS-HT C Slot1 is damaged, or its content cannot be identified."
        },
        {
          "ecode": "0701210000010083",
          "intro": "Failed to read the filament information from AMS B slot 2. The RFID tag may be damaged."
        },
        {
          "ecode": "1203110000010003",
          "intro": "The AMS D Slot2 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "07FF600000020001",
          "intro": "External spool may be tangled or jammed."
        },
        {
          "ecode": "0701220000010081",
          "intro": "Failed to read the filament information from AMS B slot 3. The AMS main board may be malfunctioning."
        },
        {
          "ecode": "0C00010000020008",
          "intro": "Failed to get image from Live View Camera. Spaghetti and waste chute pileup detection is not available at this time."
        },
        {
          "ecode": "1804130000020002",
          "intro": "The AMS-HT E slot 4 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "0300170000020002",
          "intro": "The hotend cooling fan speed is slow. It may be stuck and need cleaning."
        },
        {
          "ecode": "0707310000020002",
          "intro": "The RFID-tag on AMS H Slot2 is damaged, or its content cannot be identified."
        },
        {
          "ecode": "0703220000020005",
          "intro": "AMS D Slot 3 filament has run out, and purging the old filament went abnormally; please check whether the filament is stuck in the tool head."
        },
        {
          "ecode": "0701220000020009",
          "intro": "Failed to extrude AMS B Slot 3 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "1805300000030003",
          "intro": "RFID cannot be read because of a hardware or structural error."
        },
        {
          "ecode": "0703960000010001",
          "intro": "AMS D The drying process may experience thermal runaway. Please turn off the AMS power supply."
        },
        {
          "ecode": "0705100000010003",
          "intro": "The AMS F slot 1 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "1806120000010001",
          "intro": "The AMS-HT G slot 3 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "1806810000010002",
          "intro": "AMS-HT G The heater 2 is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "0704210000020020",
          "intro": "AMS E slot 2 assist motor is stalled，due to excessive resistance in the tube near the filament buffer。"
        },
        {
          "ecode": "1800700000020006",
          "intro": "Timeout purging old filament. Possible cause: filament stuck or the extruder/nozzle clog."
        },
        {
          "ecode": "0700010000020008",
          "intro": "AMS A The assist motor phase winding has an open circuit. The assist motor may be faulty."
        },
        {
          "ecode": "1804200000020005",
          "intro": "AMS-HT E Slot 1 filament has run out, and purging the old filament went abnormally; please check whether the filament is stuck in the tool head."
        },
        {
          "ecode": "0707230000020005",
          "intro": "AMS H Slot 4 filament has run out, and purging the old filament went abnormally; please check whether the filament is stuck in the tool head."
        },
        {
          "ecode": "1806220000020005",
          "intro": "AMS-HT G Slot 3 filament has run out, and purging the old filament went abnormally; please check whether the filament is stuck in the tool head."
        },
        {
          "ecode": "0706230000020004",
          "intro": "AMS G Slot 4 filament may be broken in the tool head."
        },
        {
          "ecode": "1801220000020010",
          "intro": "AMS-HT B slot 3 feeds filament out of AMS timeout."
        },
        {
          "ecode": "1802700000020002",
          "intro": "Failed to feed the filament into the toolhead. Possible cause: filament or spool stuck."
        },
        {
          "ecode": "1803130000010003",
          "intro": "The AMS-HT D slot 4 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "1807210000020020",
          "intro": "AMS-HT H slot 2 assist motor is stalled，due to excessive resistance in the tube near the filament buffer。"
        },
        {
          "ecode": "1806350000010001",
          "intro": "The temperature and humidity sensor has an error. The chip may be faulty."
        },
        {
          "ecode": "1804900000020001",
          "intro": "AMS-HT E The operation of the exhaust valve 1 is abnormal, which may be due to excessive resistance."
        },
        {
          "ecode": "0705230000020002",
          "intro": "AMS F Slot 4 is empty; please insert a new filament."
        },
        {
          "ecode": "1200830000020001",
          "intro": "AMS A Slot4 filament may be tangled or stuck."
        },
        {
          "ecode": "1805810000010001",
          "intro": "AMS-HT F The current sensor of heater 2 is abnormal."
        },
        {
          "ecode": "0703800000010001",
          "intro": "AMS D The current sensor of heater 1 is abnormal."
        },
        {
          "ecode": "1201230000020002",
          "intro": "AMS B Slot 4 is empty; please insert a new filament."
        },
        {
          "ecode": "0701230000020001",
          "intro": "AMS B Slot 4 filament has run out. Please insert a new filament."
        },
        {
          "ecode": "1805010000010003",
          "intro": "The AMS-HT F assist motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "1203200000020001",
          "intro": "AMS D Slot1 filament has run out; please insert a new filament."
        },
        {
          "ecode": "0707130000010001",
          "intro": "The AMS H slot 4 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "1800220000020003",
          "intro": "AMS-HT A Slot 3's filament may be broken in AMS-HT."
        },
        {
          "ecode": "1806800000010003",
          "intro": "AMS-HT G The heater 1 is short-circuited, which may be due to a wiring short or heater damage."
        },
        {
          "ecode": "1804210000020007",
          "intro": "AMS-HT E Slot 2 feed-out Hall sensor is disconnected. The connector may have poor contact."
        },
        {
          "ecode": "1805220000030002",
          "intro": "AMS-HT F Slot 3 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "0704130000020002",
          "intro": "The AMS E slot 4 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "0706210000020007",
          "intro": "AMS G Slot 2 feed-out Hall sensor is disconnected. The connector may have poor contact."
        },
        {
          "ecode": "0707210000020018",
          "intro": "AMS H slot 2 assist motor is stalled，due to excessive resistance in the tube near AMS."
        },
        {
          "ecode": "0701130000020002",
          "intro": "The AMS B slot 4 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "1805120000020002",
          "intro": "The AMS-HT F slot 3 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "1800100000010001",
          "intro": "The AMS-HT A slot 1 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "0706230000020003",
          "intro": "AMS G Slot 4's filament may be broken in AMS."
        },
        {
          "ecode": "1806800000010002",
          "intro": "AMS-HT G The heater 1 is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "1803200000010083",
          "intro": "Failed to read the filament information from AMS-HT D slot 1. The RFID tag may be damaged."
        },
        {
          "ecode": "0706310000020002",
          "intro": "The RFID-tag on AMS G Slot2 is damaged, or its content cannot be identified."
        },
        {
          "ecode": "0702230000020022",
          "intro": "AMS C slot 4 assist motor is stalled，due to excessive resistance in the tube near the toolhead."
        },
        {
          "ecode": "1803700000020006",
          "intro": "Timeout purging old filament. Possible cause: filament stuck or the extruder/nozzle clog."
        },
        {
          "ecode": "0500040000010003",
          "intro": "The content of print file is unreadable; please resend the print job."
        },
        {
          "ecode": "1804240000020009",
          "intro": "AMS-HT E front cover is open. This may affect the drying performance or cause the filament to absorb moisture."
        },
        {
          "ecode": "1803200000020020",
          "intro": "AMS-HT D slot 1 assist motor is stalled，due to excessive resistance in the tube near the filament buffer。"
        },
        {
          "ecode": "0706310000010004",
          "intro": "Encryption chip failure"
        },
        {
          "ecode": "0702010000020006",
          "intro": "AMS C The assist motor three-phase wires are not connected. The assist motor connector may have poor contact."
        },
        {
          "ecode": "1804800000010004",
          "intro": "AMS-HT E The heater 1 is heating abnormally."
        },
        {
          "ecode": "0700220000020011",
          "intro": "AMS A slot 3 pulls filament back to AMS timeout."
        },
        {
          "ecode": "1807210000020017",
          "intro": "AMS-HT H slot 2 assist motor is stalled，due to excessive resistance in the tube between AMS and the printer."
        },
        {
          "ecode": "1201230000030002",
          "intro": "AMS B Slot4 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "0704950000010001",
          "intro": "AMS E The temperature sensor of heater 2 is malfunctioning, which may be due to poor connector contact."
        },
        {
          "ecode": "0700210000020004",
          "intro": "AMS A Slot 2 filament may be broken in the tool head."
        },
        {
          "ecode": "0705220000020009",
          "intro": "Failed to extrude AMS F Slot 3 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "0700220000020008",
          "intro": "AMS A Slot 3 feed-in Hall sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "0300090000010002",
          "intro": "The extruder servo motor has a short-circuit. It may have failed."
        },
        {
          "ecode": "1202100000020002",
          "intro": "The AMS C Slot1 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "1803210000020009",
          "intro": "Failed to extrude AMS-HT D Slot 2 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "0701230000020011",
          "intro": "AMS B slot 4 pulls filament back to AMS timeout."
        },
        {
          "ecode": "0700200000010085",
          "intro": "Failed to read the filament information from AMS A slot 1. RFID tag verification failed. You can try to use Bambu Lab filament."
        },
        {
          "ecode": "0704700000020005",
          "intro": "Failed to feed the filament outside the AMS. Please clip the end of the filament flat and check to see if the spool is stuck."
        },
        {
          "ecode": "0702950000010001",
          "intro": "AMS C The temperature sensor of heater 2 is malfunctioning, which may be due to poor connector contact."
        },
        {
          "ecode": "1202230000020006",
          "intro": "Failed to extrude AMS C Slot4 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "1802240000020009",
          "intro": "AMS-HT C front cover is open. This may affect the drying performance or cause the filament to absorb moisture."
        },
        {
          "ecode": "0706210000020004",
          "intro": "AMS G Slot 2 filament may be broken in the tool head."
        },
        {
          "ecode": "1807210000020005",
          "intro": "AMS-HT H Slot 2 filament has run out, and purging the old filament went abnormally; please check whether the filament is stuck in the tool head."
        },
        {
          "ecode": "0700230000030001",
          "intro": "AMS A Slot 4 filament has run out. Please wait while old filament is purged."
        },
        {
          "ecode": "1800220000020020",
          "intro": "AMS-HT A slot 3 assist motor is stalled，due to excessive resistance in the tube near the filament buffer。"
        },
        {
          "ecode": "0706210000030001",
          "intro": "AMS G Slot 2 filament has run out. Please wait while old filament is purged."
        },
        {
          "ecode": "0700310000010001",
          "intro": "The AMS A RFID 2 board has an error."
        },
        {
          "ecode": "1804700000020004",
          "intro": "Failed to pull back the filament from the toolhead to AMS-HT. Possible cause: filament or spool stuck."
        },
        {
          "ecode": "0C0003000003000D",
          "intro": "Detected that the extruder may not be extruding normally. Please check and decide if printing should be stopped."
        },
        {
          "ecode": "1202130000010003",
          "intro": "The AMS C Slot4 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "0704110000010003",
          "intro": "The AMS E slot 2 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "1203210000020005",
          "intro": "AMS D Slot2 filament has run out, and purging the old filament went abnormally; please check to see if filament is stuck in the toolhead."
        },
        {
          "ecode": "1803230000030001",
          "intro": "AMS-HT D Slot 4 filament has run out. Please wait while old filament is purged."
        },
        {
          "ecode": "0703200000020019",
          "intro": "AMS D slot 1 assist motor is stalled，due to excessive resistance in the tube between AMS and the filament buffer."
        },
        {
          "ecode": "1804230000030002",
          "intro": "AMS-HT E Slot 4 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "0703210000020020",
          "intro": "AMS D slot 2 assist motor is stalled，due to excessive resistance in the tube near the filament buffer。"
        },
        {
          "ecode": "0702120000020002",
          "intro": "The AMS C slot 3 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "0701230000010084",
          "intro": "Failed to read the filament information from AMS B slot 4. The RFID tag may be damaged or positioned at the edge of the RFID detection device. Please remove 5cm filament and try again."
        },
        {
          "ecode": "1803220000010081",
          "intro": "Failed to read the filament information from AMS-HT D slot 3. The AMS main board may be malfunctioning."
        },
        {
          "ecode": "0706230000020011",
          "intro": "AMS G slot 4 pulls filament back to AMS timeout."
        },
        {
          "ecode": "0700120000020002",
          "intro": "The AMS A slot 3 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "0702230000010085",
          "intro": "Failed to read the filament information from AMS C slot 4. RFID tag verification failed. You can try to use Bambu Lab filament."
        },
        {
          "ecode": "0702210000020005",
          "intro": "AMS C Slot 2 filament has run out, and purging the old filament went abnormally; please check whether the filament is stuck in the tool head."
        },
        {
          "ecode": "0300080000010003",
          "intro": "The resistance of Motor-Z is abnormal; the motor may have failed."
        },
        {
          "ecode": "0500020000020006",
          "intro": "Streaming function error. Please check the network and try again. You can restart or update the printer if the issue persists."
        },
        {
          "ecode": "1806220000020018",
          "intro": "AMS-HT G slot 3 assist motor is stalled，due to excessive resistance in the tube near AMS."
        },
        {
          "ecode": "0705010000020002",
          "intro": "The AMS F assist motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "1803800000010002",
          "intro": "AMS-HT D The heater 1 is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "1800220000020024",
          "intro": "AMS-HT A slot 3 failed to rotate the filament spool when pulling filament back to AMS."
        },
        {
          "ecode": "1801230000020003",
          "intro": "AMS-HT B Slot 4's filament may be broken in AMS-HT."
        },
        {
          "ecode": "0300080000010002",
          "intro": "Motor-Z has a short-circuit. It may have failed."
        },
        {
          "ecode": "1804810000010002",
          "intro": "AMS-HT E The heater 2 is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "1800200000020003",
          "intro": "AMS-HT A Slot 1's filament may be broken in AMS-HT."
        },
        {
          "ecode": "1805230000020019",
          "intro": "AMS-HT F slot 4 assist motor is stalled，due to excessive resistance in the tube between AMS and the filament buffer."
        },
        {
          "ecode": "0702800000010003",
          "intro": "AMS C The heater 1 is short-circuited, which may be due to a wiring short or heater damage."
        },
        {
          "ecode": "1801220000020021",
          "intro": "AMS-HT B slot 3 assist motor is stalled，due to excessive resistance in the tube between the filament buffer and the toolhead."
        },
        {
          "ecode": "1804230000030001",
          "intro": "AMS-HT E Slot 4 filament has run out. Please wait while old filament is purged."
        },
        {
          "ecode": "1801010000020002",
          "intro": "The AMS-HT B assist motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "1800200000010085",
          "intro": "Failed to read the filament information from AMS-HT A slot 1. RFID tag verification failed. You can try to use Bambu Lab filament."
        },
        {
          "ecode": "0703210000020022",
          "intro": "AMS D slot 2 assist motor is stalled，due to excessive resistance in the tube near the toolhead."
        },
        {
          "ecode": "0700130000010003",
          "intro": "The AMS A slot 4 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "0500030000010009",
          "intro": "A system hang occurred. It has been recovered by automatic restart."
        },
        {
          "ecode": "1804330000020002",
          "intro": "The RFID-tag on AMS-HT E Slot4 is damaged, or its content cannot be identified."
        },
        {
          "ecode": "0C00030000020010",
          "intro": "Foreign objects detected on heatbed; Please check and clean the heatbed."
        },
        {
          "ecode": "1803200000030002",
          "intro": "AMS-HT D Slot 1 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "0703220000020001",
          "intro": "AMS D Slot 3 filament has run out. Please insert a new filament."
        },
        {
          "ecode": "0704230000020005",
          "intro": "AMS E Slot 4 filament has run out, and purging the old filament went abnormally; please check whether the filament is stuck in the tool head."
        },
        {
          "ecode": "1807230000020002",
          "intro": "AMS-HT H Slot 4 is empty; please insert a new filament."
        },
        {
          "ecode": "1805950000010001",
          "intro": "AMS-HT F The temperature sensor of heater 2 is malfunctioning, which may be due to poor connector contact."
        },
        {
          "ecode": "1806700000020007",
          "intro": "AMS-HT filament ran out. Please put a new filament into the same slot in AMS and resume."
        },
        {
          "ecode": "0701120000020004",
          "intro": "AMS B The brushed motor 3 has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "0702200000020020",
          "intro": "AMS C slot 1 assist motor is stalled，due to excessive resistance in the tube near the filament buffer。"
        },
        {
          "ecode": "0500050000010006",
          "intro": "The factory data of AP board is abnormal; please replace the AP board with a new one."
        },
        {
          "ecode": "1800350000010002",
          "intro": "AMS-HT A The humidity sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "0706200000030002",
          "intro": "AMS G Slot 1 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "1201210000020001",
          "intro": "AMS B Slot2 filament has run out; please insert a new filament."
        },
        {
          "ecode": "1807220000020003",
          "intro": "AMS-HT H Slot 3's filament may be broken in AMS-HT."
        },
        {
          "ecode": "0703560000030001",
          "intro": "AMS D is undergoing dry cooling; please wait for it to cool down before operating."
        },
        {
          "ecode": "0500030000010003",
          "intro": "The AMS module is malfunctioning. Please restart the device."
        },
        {
          "ecode": "0707210000010084",
          "intro": "Failed to read the filament information from AMS H slot 2. The RFID tag may be damaged or positioned at the edge of the RFID detection device. Please remove 5cm filament and try again."
        },
        {
          "ecode": "1806020000020002",
          "intro": "AMS-HT G The odometer has no signal. The odometer connector may have poor contact."
        },
        {
          "ecode": "1805230000010081",
          "intro": "Failed to read the filament information from AMS-HT F slot 4. The AMS main board may be malfunctioning."
        },
        {
          "ecode": "1800220000020017",
          "intro": "AMS-HT A slot 3 assist motor is stalled，due to excessive resistance in the tube between AMS and the printer."
        },
        {
          "ecode": "1804010000020008",
          "intro": "AMS-HT E The assist motor phase winding has an open circuit. The assist motor may be faulty."
        },
        {
          "ecode": "1800200000020008",
          "intro": "AMS-HT A Slot 1 feed-in Hall sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "0703310000010001",
          "intro": "The AMS D RFID 2 board has an error."
        },
        {
          "ecode": "1804220000020005",
          "intro": "AMS-HT E Slot 3 filament has run out, and purging the old filament went abnormally; please check whether the filament is stuck in the tool head."
        },
        {
          "ecode": "1800200000020007",
          "intro": "AMS-HT A Slot 1 feed-out Hall sensor is disconnected. The connector may have poor contact."
        },
        {
          "ecode": "1801220000030002",
          "intro": "AMS-HT B Slot 3 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "0706700000020007",
          "intro": "AMS filament ran out. Please put a new filament into the same slot in AMS and resume."
        },
        {
          "ecode": "1801020000020002",
          "intro": "AMS-HT B The odometer has no signal. The odometer connector may have poor contact."
        },
        {
          "ecode": "1803210000010086",
          "intro": "Failed to read the filament information from AMS-HT D slot 2. The RFID tag cannot rotate due to a jam during the filament loading or unloading. Please pull out the filament and try again."
        },
        {
          "ecode": "0702310000020002",
          "intro": "The RFID-tag on AMS C Slot2 is damaged, or its content cannot be identified."
        },
        {
          "ecode": "0703230000020003",
          "intro": "AMS D Slot 4's filament may be broken in AMS."
        },
        {
          "ecode": "0707960000010003",
          "intro": "AMS H Unable to start drying; please pull out the filament from filament hub and try again."
        },
        {
          "ecode": "1802200000020024",
          "intro": "AMS-HT C slot 1 failed to rotate the filament spool when pulling filament back to AMS."
        },
        {
          "ecode": "1806230000020010",
          "intro": "AMS-HT G slot 4 feeds filament out of AMS timeout."
        },
        {
          "ecode": "0706230000020010",
          "intro": "AMS G slot 4 feeds filament out of AMS timeout."
        },
        {
          "ecode": "1202300000010004",
          "intro": "RFID cannot be read because of an encryption chip failure in AMS C."
        },
        {
          "ecode": "1805210000020021",
          "intro": "AMS-HT F slot 2 assist motor is stalled，due to excessive resistance in the tube between the filament buffer and the toolhead."
        },
        {
          "ecode": "1803210000020002",
          "intro": "AMS-HT D Slot 2 is empty; please insert a new filament."
        },
        {
          "ecode": "0701700000020002",
          "intro": "Failed to feed the filament into the toolhead. Possible cause: filament or spool stuck."
        },
        {
          "ecode": "1201220000020005",
          "intro": "AMS B Slot3 filament has run out, and purging the old filament went abnormally; please check to see if filament is stuck in the toolhead."
        },
        {
          "ecode": "0703210000010085",
          "intro": "Failed to read the filament information from AMS D slot 2. RFID tag verification failed. You can try to use Bambu Lab filament."
        },
        {
          "ecode": "1804700000020007",
          "intro": "AMS-HT filament ran out. Please put a new filament into the same slot in AMS and resume."
        },
        {
          "ecode": "1805700000020004",
          "intro": "Failed to pull back the filament from the toolhead to AMS-HT. Possible cause: filament or spool stuck."
        },
        {
          "ecode": "0701920000020002",
          "intro": "AMS B The cooling fan speed of heater 1 is too low, which could be due to excessive fan resistance."
        },
        {
          "ecode": "1806120000020004",
          "intro": "AMS-HT G The brushed motor 3 has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "0704010000010005",
          "intro": "AMS E The current sensor of assist motor may be faulty."
        },
        {
          "ecode": "0700450000020001",
          "intro": "The filament cutter sensor is malfunctioning; please check whether the connector is properly plugged in."
        },
        {
          "ecode": "1807560000030001",
          "intro": "AMS-HT H is undergoing dry cooling; please wait for it to cool down before operating."
        },
        {
          "ecode": "1200810000020001",
          "intro": "AMS A Slot2 filament may be tangled or stuck."
        },
        {
          "ecode": "0700940000010001",
          "intro": "AMS A The temperature sensor of heater 1 is malfunctioning, which may be due to poor connector contact."
        },
        {
          "ecode": "0705010000010001",
          "intro": "The AMS F assist motor has slipped. The extrusion wheel may be worn down, or the filament may be too thin."
        },
        {
          "ecode": "1806330000020002",
          "intro": "The RFID-tag on AMS-HT G Slot4 is damaged, or its content cannot be identified."
        },
        {
          "ecode": "1803230000020001",
          "intro": "AMS-HT D Slot 4 filament has run out. Please insert a new filament."
        },
        {
          "ecode": "03001A0000020001",
          "intro": "The nozzle is covered with filament, or the build plate is crooked."
        },
        {
          "ecode": "1807200000020002",
          "intro": "AMS-HT H Slot 1 is empty; please insert a new filament."
        },
        {
          "ecode": "1802200000020001",
          "intro": "AMS-HT C Slot 1 filament has run out. Please insert a new filament."
        },
        {
          "ecode": "0701950000010001",
          "intro": "AMS B The temperature sensor of heater 2 is malfunctioning, which may be due to poor connector contact."
        },
        {
          "ecode": "0704200000020002",
          "intro": "AMS E Slot 1 is empty; please insert a new filament."
        },
        {
          "ecode": "1200210000030001",
          "intro": "AMS A Slot2 filament has run out. Purging the old filament; please wait."
        },
        {
          "ecode": "1805350000010001",
          "intro": "The temperature and humidity sensor has an error. The chip may be faulty."
        },
        {
          "ecode": "1200230000020001",
          "intro": "AMS A Slot4 filament has run out; please insert a new filament."
        },
        {
          "ecode": "0705220000020005",
          "intro": "AMS F Slot 3 filament has run out, and purging the old filament went abnormally; please check whether the filament is stuck in the tool head."
        },
        {
          "ecode": "0702120000010001",
          "intro": "The AMS C slot 3 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "0500040000010006",
          "intro": "Failed to resume previous print"
        },
        {
          "ecode": "1807930000010001",
          "intro": "AMS-HT H The cooling fan of heater 2 is blocked, which may be due to the fan being stuck."
        },
        {
          "ecode": "0706220000010084",
          "intro": "Failed to read the filament information from AMS G slot 3. The RFID tag may be damaged or positioned at the edge of the RFID detection device. Please remove 5cm filament and try again."
        },
        {
          "ecode": "0706930000010001",
          "intro": "AMS G The cooling fan of heater 2 is blocked, which may be due to the fan being stuck."
        },
        {
          "ecode": "1807210000030001",
          "intro": "AMS-HT H Slot 2 filament has run out. Please wait while old filament is purged."
        },
        {
          "ecode": "1804700000020008",
          "intro": "Failed to get AMS mapping table; please select \"Resume\" to retry."
        },
        {
          "ecode": "0700220000020020",
          "intro": "AMS A slot 3 assist motor is stalled，due to excessive resistance in the tube near the filament buffer。"
        },
        {
          "ecode": "0500040000020007",
          "intro": "The bed temperature exceeds the filament's vitrification temperature, which may cause a nozzle clog. Please keep the front door of the printer open or lower the bed temperature."
        },
        {
          "ecode": "1803220000010083",
          "intro": "Failed to read the filament information from AMS-HT D slot 3. The RFID tag may be damaged."
        },
        {
          "ecode": "0704100000020004",
          "intro": "AMS E The brushed motor 1 has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "0704200000020022",
          "intro": "AMS E slot 1 assist motor is stalled，due to excessive resistance in the tube near the toolhead."
        },
        {
          "ecode": "1203230000020006",
          "intro": "Failed to extrude AMS D Slot4 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "1806320000020002",
          "intro": "The RFID-tag on AMS-HT G Slot3 is damaged, or its content cannot be identified."
        },
        {
          "ecode": "1807500000020001",
          "intro": "AMS-HT H communication is abnormal; please check the connection cable."
        },
        {
          "ecode": "0700230000020008",
          "intro": "AMS A Slot 4 feed-in Hall sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "0701220000010085",
          "intro": "Failed to read the filament information from AMS B slot 3. RFID tag verification failed. You can try to use Bambu Lab filament."
        },
        {
          "ecode": "0700230000020024",
          "intro": "AMS A slot 4 failed to rotate the filament spool when pulling filament back to AMS."
        },
        {
          "ecode": "1200710000010001",
          "intro": "AMS A Filament speed and length error: The slot 2 filament odometry may be faulty."
        },
        {
          "ecode": "1202200000020002",
          "intro": "AMS C Slot 1 is empty; please insert a new filament."
        },
        {
          "ecode": "0701200000020021",
          "intro": "AMS B slot 1 assist motor is stalled，due to excessive resistance in the tube between the filament buffer and the toolhead."
        },
        {
          "ecode": "1805120000020004",
          "intro": "AMS-HT F The brushed motor 3 has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "1806010000020008",
          "intro": "AMS-HT G The assist motor phase winding has an open circuit. The assist motor may be faulty."
        },
        {
          "ecode": "0701310000030003",
          "intro": "RFID cannot be read because of a hardware or structural error."
        },
        {
          "ecode": "1800700000020002",
          "intro": "Failed to feed the filament into the toolhead. Possible cause: filament or spool stuck."
        },
        {
          "ecode": "1800310000010001",
          "intro": "The AMS-HT A RFID 2 board has an error."
        },
        {
          "ecode": "1803800000010001",
          "intro": "AMS-HT D The current sensor of heater 1 is abnormal."
        },
        {
          "ecode": "0C0001000001000A",
          "intro": "The Micro Lidar LED may be broken."
        },
        {
          "ecode": "1807800000010001",
          "intro": "AMS-HT H The current sensor of heater 1 is abnormal."
        },
        {
          "ecode": "0707130000020002",
          "intro": "The AMS H slot 4 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "0C00030000030008",
          "intro": "Possible spaghetti defects were detected. Please check the print quality and decide if the job should be stopped."
        },
        {
          "ecode": "1800200000020001",
          "intro": "AMS-HT A Slot 1 filament has run out. Please insert a new filament."
        },
        {
          "ecode": "0701210000010081",
          "intro": "Failed to read the filament information from AMS B slot 2. The AMS main board may be malfunctioning."
        },
        {
          "ecode": "1801200000010083",
          "intro": "Failed to read the filament information from AMS-HT B slot 1. The RFID tag may be damaged."
        },
        {
          "ecode": "1807920000020002",
          "intro": "AMS-HT H The cooling fan speed of heater 1 is too low, which could be due to excessive fan resistance."
        },
        {
          "ecode": "1802200000020002",
          "intro": "AMS-HT C Slot 1 is empty; please insert a new filament."
        },
        {
          "ecode": "1802230000020004",
          "intro": "AMS-HT C Slot 4 filament may be broken in the tool head."
        },
        {
          "ecode": "0703010000020011",
          "intro": "AMS D The motor assist parameter is lost. Please pull out the filament from the filament hub and then restart the AMS."
        },
        {
          "ecode": "0702230000020019",
          "intro": "AMS C slot 4 assist motor is stalled，due to excessive resistance in the tube between AMS and the filament buffer."
        },
        {
          "ecode": "0706210000020020",
          "intro": "AMS G slot 2 assist motor is stalled，due to excessive resistance in the tube near the filament buffer。"
        },
        {
          "ecode": "1202200000030001",
          "intro": "AMS C Slot1 filament has run out. Purging the old filament; please wait."
        },
        {
          "ecode": "1201300000030003",
          "intro": "AMS B Slot1 RFID cannot be read because of a structural error."
        },
        {
          "ecode": "1802100000020004",
          "intro": "AMS-HT C The brushed motor 1 has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "0704020000020002",
          "intro": "AMS E The odometer has no signal. The odometer connector may have poor contact."
        },
        {
          "ecode": "1803210000010085",
          "intro": "Failed to read the filament information from AMS-HT D slot 2. RFID tag verification failed. You can try to use Bambu Lab filament."
        },
        {
          "ecode": "0707200000020024",
          "intro": "AMS H slot 1 failed to rotate the filament spool when pulling filament back to AMS."
        },
        {
          "ecode": "1806950000010001",
          "intro": "AMS-HT G The temperature sensor of heater 2 is malfunctioning, which may be due to poor connector contact."
        },
        {
          "ecode": "1803200000020002",
          "intro": "AMS-HT D Slot 1 is empty; please insert a new filament."
        },
        {
          "ecode": "0705700000020001",
          "intro": "Failed to pull out the filament from the extruder. Possible causes: clogged extruder or broken filament."
        },
        {
          "ecode": "0702010000010001",
          "intro": "The AMS C assist motor has slipped. The extrusion wheel may be worn down, or the filament may be too thin."
        },
        {
          "ecode": "0703300000020002",
          "intro": "The RFID-tag on AMS D Slot1 is damaged, or its content cannot be identified."
        },
        {
          "ecode": "1805200000030001",
          "intro": "AMS-HT F Slot 1 filament has run out. Please wait while old filament is purged."
        },
        {
          "ecode": "0705210000010081",
          "intro": "Failed to read the filament information from AMS F slot 2. The AMS main board may be malfunctioning."
        },
        {
          "ecode": "1202330000020002",
          "intro": "The RFID-tag on AMS C Slot 4 is damaged."
        },
        {
          "ecode": "1801120000010003",
          "intro": "The AMS-HT B slot 3 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "1801120000010001",
          "intro": "The AMS-HT B slot 3 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "03000D0000010007",
          "intro": "The build plate is not placed properly. Please adjust it."
        },
        {
          "ecode": "0707220000010085",
          "intro": "Failed to read the filament information from AMS H slot 3. RFID tag verification failed. You can try to use Bambu Lab filament."
        },
        {
          "ecode": "0300060000010003",
          "intro": "The resistance of Motor-A is abnormal; the motor may have failed."
        },
        {
          "ecode": "1802700000020005",
          "intro": "Failed to feed the filament outside the AMS-HT. Please clip the end of the filament flat and check to see if the spool is stuck."
        },
        {
          "ecode": "1801010000020007",
          "intro": "AMS-HT B The assist motor encoder wires are not connected. The assist motor connector may have poor contact."
        },
        {
          "ecode": "1806130000020004",
          "intro": "AMS-HT G The brushed motor 4 has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "1804230000010081",
          "intro": "Failed to read the filament information from AMS-HT E slot 4. The AMS main board may be malfunctioning."
        },
        {
          "ecode": "1200230000020002",
          "intro": "AMS A Slot 4 is empty; please insert a new filament."
        },
        {
          "ecode": "1805220000020004",
          "intro": "AMS-HT F Slot 3 filament may be broken in the tool head."
        },
        {
          "ecode": "0705230000020003",
          "intro": "AMS F Slot 4's filament may be broken in AMS."
        },
        {
          "ecode": "0703210000020001",
          "intro": "AMS D Slot 2 filament has run out. Please insert a new filament."
        },
        {
          "ecode": "0300060000010002",
          "intro": "Motor-A has a short-circuit. It may have failed."
        },
        {
          "ecode": "1201210000020006",
          "intro": "Failed to extrude AMS B Slot2 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "1202220000020004",
          "intro": "AMS C Slot3 filament may be broken in the tool head."
        },
        {
          "ecode": "1203820000020001",
          "intro": "AMS D Slot3 filament may be tangled or stuck."
        },
        {
          "ecode": "0703010000020002",
          "intro": "The AMS D assist motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "0706010000010005",
          "intro": "AMS G The current sensor of assist motor may be faulty."
        },
        {
          "ecode": "1805220000020017",
          "intro": "AMS-HT F slot 3 assist motor is stalled，due to excessive resistance in the tube between AMS and the printer."
        },
        {
          "ecode": "0705220000010084",
          "intro": "Failed to read the filament information from AMS F slot 3. The RFID tag may be damaged or positioned at the edge of the RFID detection device. Please remove 5cm filament and try again."
        },
        {
          "ecode": "1803200000020007",
          "intro": "AMS-HT D Slot 1 feed-out Hall sensor is disconnected. The connector may have poor contact."
        },
        {
          "ecode": "0704230000030002",
          "intro": "AMS E Slot 4 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "0705200000020011",
          "intro": "AMS F slot 1 pulls filament back to AMS timeout."
        },
        {
          "ecode": "1802230000010085",
          "intro": "Failed to read the filament information from AMS-HT C slot 4. RFID tag verification failed. You can try to use Bambu Lab filament."
        },
        {
          "ecode": "0701200000010086",
          "intro": "Failed to read the filament information from AMS B slot 1. The RFID tag cannot rotate due to a jam during the filament loading or unloading. Please pull out the filament and try again."
        },
        {
          "ecode": "1202210000020002",
          "intro": "AMS C Slot 2 is empty; please insert a new filament."
        },
        {
          "ecode": "1807220000010083",
          "intro": "Failed to read the filament information from AMS-HT H slot 3. The RFID tag may be damaged."
        },
        {
          "ecode": "1805220000020002",
          "intro": "AMS-HT F Slot 3 is empty; please insert a new filament."
        },
        {
          "ecode": "1801700000020002",
          "intro": "Failed to feed the filament into the toolhead. Possible cause: filament or spool stuck."
        },
        {
          "ecode": "0702300000010004",
          "intro": "Encryption chip failure"
        },
        {
          "ecode": "0705220000020018",
          "intro": "AMS F slot 3 assist motor is stalled，due to excessive resistance in the tube near AMS."
        },
        {
          "ecode": "0707700000020001",
          "intro": "Failed to pull out the filament from the extruder. Possible causes: clogged extruder or broken filament."
        },
        {
          "ecode": "0703210000020024",
          "intro": "AMS D slot 2 failed to rotate the filament spool when pulling filament back to AMS."
        },
        {
          "ecode": "1805200000010081",
          "intro": "Failed to read the filament information from AMS-HT F slot 1. The AMS main board may be malfunctioning."
        },
        {
          "ecode": "1802100000010003",
          "intro": "The AMS-HT C slot 1 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "0707700000020005",
          "intro": "Failed to feed the filament outside the AMS. Please clip the end of the filament flat and check to see if the spool is stuck."
        },
        {
          "ecode": "0702200000010081",
          "intro": "Failed to read the filament information from AMS C slot 1. The AMS main board may be malfunctioning."
        },
        {
          "ecode": "0703230000010084",
          "intro": "Failed to read the filament information from AMS D slot 4. The RFID tag may be damaged or positioned at the edge of the RFID detection device. Please remove 5cm filament and try again."
        },
        {
          "ecode": "0706210000020005",
          "intro": "AMS G Slot 2 filament has run out, and purging the old filament went abnormally; please check whether the filament is stuck in the tool head."
        },
        {
          "ecode": "1807230000020008",
          "intro": "AMS-HT H Slot 4 feed-in Hall sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "1802220000020022",
          "intro": "AMS-HT C slot 3 assist motor is stalled，due to excessive resistance in the tube near the toolhead."
        },
        {
          "ecode": "0500040000030008",
          "intro": "The door seems to be open."
        },
        {
          "ecode": "1203500000020001",
          "intro": "AMS D communication is abnormal; please check the connection cable."
        },
        {
          "ecode": "1200210000020005",
          "intro": "AMS A Slot2 filament has run out, and purging the old filament went abnormally; please check to see if filament is stuck in the toolhead."
        },
        {
          "ecode": "0701700000020001",
          "intro": "Failed to pull out the filament from the extruder. Possible causes: clogged extruder or broken filament."
        },
        {
          "ecode": "0700110000020004",
          "intro": "AMS A The brushed motor 2 has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "0703700000020004",
          "intro": "Failed to pull back the filament from the toolhead to AMS. Possible cause: filament or spool stuck."
        },
        {
          "ecode": "050004000002001E",
          "intro": "The RFID-tag on AMS D Slot3 cannot be identified."
        },
        {
          "ecode": "1804220000020020",
          "intro": "AMS-HT E slot 3 assist motor is stalled，due to excessive resistance in the tube near the filament buffer。"
        },
        {
          "ecode": "1805930000020002",
          "intro": "AMS-HT F The cooling fan speed of heater 2 is too low, which could be due to excessive fan resistance."
        },
        {
          "ecode": "1806210000020010",
          "intro": "AMS-HT G slot 2 feeds filament out of AMS timeout."
        },
        {
          "ecode": "030091000001000C",
          "intro": "The chamber heater 1 has worked at full load for a long time. The temperature control system may be abnormal."
        },
        {
          "ecode": "0703130000020002",
          "intro": "The AMS D slot 4 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "0701130000010003",
          "intro": "The AMS B slot 4 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "0704100000010001",
          "intro": "The AMS E slot 1 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "1806230000020024",
          "intro": "AMS-HT G slot 4 failed to rotate the filament spool when pulling filament back to AMS."
        },
        {
          "ecode": "1804230000020018",
          "intro": "AMS-HT E slot 4 assist motor is stalled，due to excessive resistance in the tube near AMS."
        },
        {
          "ecode": "0705800000010001",
          "intro": "AMS F The current sensor of heater 1 is abnormal."
        },
        {
          "ecode": "0707230000020019",
          "intro": "AMS H slot 4 assist motor is stalled，due to excessive resistance in the tube between AMS and the filament buffer."
        },
        {
          "ecode": "1800810000010003",
          "intro": "AMS-HT A The heater 2 is short-circuited, which may be due to a wiring short or heater damage."
        },
        {
          "ecode": "1800800000010002",
          "intro": "AMS-HT A The heater 1 is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "0703700000020007",
          "intro": "AMS filament ran out. Please put a new filament into the same slot in AMS and resume."
        },
        {
          "ecode": "0700100000020004",
          "intro": "AMS A The brushed motor 1 has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "1803210000010083",
          "intro": "Failed to read the filament information from AMS-HT D slot 2. The RFID tag may be damaged."
        },
        {
          "ecode": "0702230000020018",
          "intro": "AMS C slot 4 assist motor is stalled，due to excessive resistance in the tube near AMS."
        },
        {
          "ecode": "1807220000020007",
          "intro": "AMS-HT H Slot 3 feed-out Hall sensor is disconnected. The connector may have poor contact."
        },
        {
          "ecode": "0703120000020004",
          "intro": "AMS D The brushed motor 3 has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "0705230000020007",
          "intro": "AMS F Slot 4 feed-out Hall sensor is disconnected. The connector may have poor contact."
        },
        {
          "ecode": "0707900000010003",
          "intro": "AMS H The exhaust valve 1 is not connected, which may be due to poor connector contact."
        },
        {
          "ecode": "0702220000020004",
          "intro": "AMS C Slot 3 filament may be broken in the tool head."
        },
        {
          "ecode": "0707810000010003",
          "intro": "AMS H The heater 2 is short-circuited, which may be due to a wiring short or heater damage."
        },
        {
          "ecode": "0702130000020004",
          "intro": "AMS C The brushed motor 4 has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "1805900000020001",
          "intro": "AMS-HT F The operation of the exhaust valve 1 is abnormal, which may be due to excessive resistance."
        },
        {
          "ecode": "0704960000010001",
          "intro": "AMS E The drying process may experience thermal runaway. Please turn off the AMS power supply."
        },
        {
          "ecode": "1807210000020019",
          "intro": "AMS-HT H slot 2 assist motor is stalled，due to excessive resistance in the tube between AMS and the filament buffer."
        },
        {
          "ecode": "1804220000020017",
          "intro": "AMS-HT E slot 3 assist motor is stalled，due to excessive resistance in the tube between AMS and the printer."
        },
        {
          "ecode": "1805210000020018",
          "intro": "AMS-HT F slot 2 assist motor is stalled，due to excessive resistance in the tube near AMS."
        },
        {
          "ecode": "1805960000020002",
          "intro": "AMS-HT F Environmental temperature is too low, which will affect the drying capability."
        },
        {
          "ecode": "1800200000020010",
          "intro": "AMS-HT A slot 1 feeds filament out of AMS timeout."
        },
        {
          "ecode": "1203200000020002",
          "intro": "AMS D Slot 1 is empty; please insert a new filament."
        },
        {
          "ecode": "1806200000020011",
          "intro": "AMS-HT G slot 1 pulls filament back to AMS timeout."
        },
        {
          "ecode": "1203200000020003",
          "intro": "AMS D Slot1 filament may be broken in the PTFE tube."
        },
        {
          "ecode": "0700700000020007",
          "intro": "AMS filament ran out. Please put a new filament into the same slot in AMS and resume."
        },
        {
          "ecode": "0703210000010081",
          "intro": "Failed to read the filament information from AMS D slot 2. The AMS main board may be malfunctioning."
        },
        {
          "ecode": "1805200000020005",
          "intro": "AMS-HT F Slot 1 filament has run out, and purging the old filament went abnormally; please check whether the filament is stuck in the tool head."
        },
        {
          "ecode": "1202330000010001",
          "intro": "AMS C Slot 4 RFID coil is broken or the RF hardware circuit has an error."
        },
        {
          "ecode": "1804700000020003",
          "intro": "Failed to extrude the filament. Possible cause: extruder or nozzle clog."
        },
        {
          "ecode": "1804210000010083",
          "intro": "Failed to read the filament information from AMS-HT E slot 2. The RFID tag may be damaged."
        },
        {
          "ecode": "0706200000020002",
          "intro": "AMS G Slot 1 is empty; please insert a new filament."
        },
        {
          "ecode": "1803010000020008",
          "intro": "AMS-HT D The assist motor phase winding has an open circuit. The assist motor may be faulty."
        },
        {
          "ecode": "0700210000020020",
          "intro": "AMS A slot 2 assist motor is stalled，due to excessive resistance in the tube near the filament buffer。"
        },
        {
          "ecode": "0707120000020004",
          "intro": "AMS H The brushed motor 3 has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "1803210000020024",
          "intro": "AMS-HT D slot 2 failed to rotate the filament spool when pulling filament back to AMS."
        },
        {
          "ecode": "1802210000020021",
          "intro": "AMS-HT C slot 2 assist motor is stalled，due to excessive resistance in the tube between the filament buffer and the toolhead."
        },
        {
          "ecode": "1201730000010001",
          "intro": "AMS B Filament speed and length error: The slot 4 filament odometry may be faulty."
        },
        {
          "ecode": "0706900000010003",
          "intro": "AMS G The exhaust valve 1 is not connected, which may be due to poor connector contact."
        },
        {
          "ecode": "1202320000030003",
          "intro": "AMS C Slot3 RFID cannot be read because of a structural error."
        },
        {
          "ecode": "0700220000020010",
          "intro": "AMS A slot 3 feeds filament out of AMS timeout."
        },
        {
          "ecode": "1802500000020001",
          "intro": "AMS-HT C communication is abnormal; please check the connection cable."
        },
        {
          "ecode": "0707210000020017",
          "intro": "AMS H slot 2 assist motor is stalled，due to excessive resistance in the tube between AMS and the printer."
        },
        {
          "ecode": "1802220000030002",
          "intro": "AMS-HT C Slot 3 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "1802930000010001",
          "intro": "AMS-HT C The cooling fan of heater 2 is blocked, which may be due to the fan being stuck."
        },
        {
          "ecode": "0705110000010001",
          "intro": "The AMS F slot 2 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "03000A0000010005",
          "intro": "Force sensor 1 detected unexpected continuous force. The heatbed may be stuck, or the analog front end may be broken."
        },
        {
          "ecode": "1806220000020017",
          "intro": "AMS-HT G slot 3 assist motor is stalled，due to excessive resistance in the tube between AMS and the printer."
        },
        {
          "ecode": "1806010000020006",
          "intro": "AMS-HT G The assist motor three-phase wires are not connected. The assist motor connector may have poor contact."
        },
        {
          "ecode": "0706230000030002",
          "intro": "AMS G Slot 4 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "1804120000010003",
          "intro": "The AMS-HT E slot 3 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "1801310000020002",
          "intro": "The RFID-tag on AMS-HT B Slot2 is damaged, or its content cannot be identified."
        },
        {
          "ecode": "0702700000020001",
          "intro": "Failed to pull out the filament from the extruder. Possible causes: clogged extruder or broken filament."
        },
        {
          "ecode": "1802310000020002",
          "intro": "The RFID-tag on AMS-HT C Slot2 is damaged, or its content cannot be identified."
        },
        {
          "ecode": "0704210000020011",
          "intro": "AMS E slot 2 pulls filament back to AMS timeout."
        },
        {
          "ecode": "1804210000020004",
          "intro": "AMS-HT E Slot 2 filament may be broken in the tool head."
        },
        {
          "ecode": "1803020000020002",
          "intro": "AMS-HT D The odometer has no signal. The odometer connector may have poor contact."
        },
        {
          "ecode": "0706010000020008",
          "intro": "AMS G The assist motor phase winding has an open circuit. The assist motor may be faulty."
        },
        {
          "ecode": "0705220000020001",
          "intro": "AMS F Slot 3 filament has run out. Please insert a new filament."
        },
        {
          "ecode": "0705220000020019",
          "intro": "AMS F slot 3 assist motor is stalled，due to excessive resistance in the tube between AMS and the filament buffer."
        },
        {
          "ecode": "0700930000010001",
          "intro": "AMS A The cooling fan of heater 2 is blocked, which may be due to the fan being stuck."
        },
        {
          "ecode": "03000D0000020009",
          "intro": "The build plate may not be properly placed. If this message appears repeatedly, please check the Wiki for more explanations."
        },
        {
          "ecode": "1802130000010003",
          "intro": "The AMS-HT C slot 4 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "0701960000020002",
          "intro": "AMS B Environmental temperature is too low, which will affect the drying capability."
        },
        {
          "ecode": "0704210000020009",
          "intro": "Failed to extrude AMS E Slot 2 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "0300160000010001",
          "intro": "The extruder servo motor's current sensor is abnormal. A failure of the hardware sampling circuit may cause this."
        },
        {
          "ecode": "0701220000020005",
          "intro": "AMS B Slot 3 filament has run out, and purging the old filament went abnormally; please check whether the filament is stuck in the tool head."
        },
        {
          "ecode": "0700210000020024",
          "intro": "AMS A slot 2 failed to rotate the filament spool when pulling filament back to AMS."
        },
        {
          "ecode": "1802200000010086",
          "intro": "Failed to read the filament information from AMS-HT C slot 1. The RFID tag cannot rotate due to a jam during the filament loading or unloading. Please pull out the filament and try again."
        },
        {
          "ecode": "0701220000030001",
          "intro": "AMS B Slot 3 filament has run out. Please wait while old filament is purged."
        },
        {
          "ecode": "0706200000020024",
          "intro": "AMS G slot 1 failed to rotate the filament spool when pulling filament back to AMS."
        },
        {
          "ecode": "1806200000010081",
          "intro": "Failed to read the filament information from AMS-HT G slot 1. The AMS main board may be malfunctioning."
        },
        {
          "ecode": "1803200000010084",
          "intro": "Failed to read the filament information from AMS-HT D slot 1. The RFID tag may be damaged or positioned at the edge of the RFID detection device. Please remove 5cm filament and try again."
        },
        {
          "ecode": "0705220000020024",
          "intro": "AMS F slot 3 failed to rotate the filament spool when pulling filament back to AMS."
        },
        {
          "ecode": "1802200000020007",
          "intro": "AMS-HT C Slot 1 feed-out Hall sensor is disconnected. The connector may have poor contact."
        },
        {
          "ecode": "0702210000020002",
          "intro": "AMS C Slot 2 is empty; please insert a new filament."
        },
        {
          "ecode": "1800220000010081",
          "intro": "Failed to read the filament information from AMS-HT A slot 3. The AMS main board may be malfunctioning."
        },
        {
          "ecode": "1800930000020002",
          "intro": "AMS-HT A The cooling fan speed of heater 2 is too low, which could be due to excessive fan resistance."
        },
        {
          "ecode": "0500040000030009",
          "intro": "The bed temperature exceeds filament's vitrification temperature, which may cause nozzle clog. Please keep the front door of the printer open. Door open detection has been temporarily turned off."
        },
        {
          "ecode": "0703230000010081",
          "intro": "Failed to read the filament information from AMS D slot 4. The AMS main board may be malfunctioning."
        },
        {
          "ecode": "1801930000010001",
          "intro": "AMS-HT B The cooling fan of heater 2 is blocked, which may be due to the fan being stuck."
        },
        {
          "ecode": "0701910000010003",
          "intro": "AMS B The exhaust valve 2 is not connected, which may be due to poor connector contact."
        },
        {
          "ecode": "0702800000010002",
          "intro": "AMS C The heater 1 is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "1806220000010086",
          "intro": "Failed to read the filament information from AMS-HT G slot 3. The RFID tag cannot rotate due to a jam during the filament loading or unloading. Please pull out the filament and try again."
        },
        {
          "ecode": "0701220000010086",
          "intro": "Failed to read the filament information from AMS B slot 3. The RFID tag cannot rotate due to a jam during the filament loading or unloading. Please pull out the filament and try again."
        },
        {
          "ecode": "1800010000020011",
          "intro": "AMS-HT A The motor assist parameter is lost. Please pull out the filament from the filament hub and then restart the AMS."
        },
        {
          "ecode": "0703230000020017",
          "intro": "AMS D slot 4 assist motor is stalled，due to excessive resistance in the tube between AMS and the printer."
        },
        {
          "ecode": "0700200000020009",
          "intro": "Failed to extrude AMS A Slot 1 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "0701220000020002",
          "intro": "AMS B Slot 3 is empty; please insert a new filament."
        },
        {
          "ecode": "0702210000020004",
          "intro": "AMS C Slot 2 filament may be broken in the tool head."
        },
        {
          "ecode": "1802110000010001",
          "intro": "The AMS-HT C slot 2 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "0702020000020002",
          "intro": "AMS C The odometer has no signal. The odometer connector may have poor contact."
        },
        {
          "ecode": "1805210000020003",
          "intro": "AMS-HT F Slot 2's filament may be broken in AMS-HT."
        },
        {
          "ecode": "1807220000020004",
          "intro": "AMS-HT H Slot 3 filament may be broken in the tool head."
        },
        {
          "ecode": "1800220000010084",
          "intro": "Failed to read the filament information from AMS-HT A slot 3. The RFID tag may be damaged or positioned at the edge of the RFID detection device. Please remove 5cm filament and try again."
        },
        {
          "ecode": "0500040000020020",
          "intro": ""
        },
        {
          "ecode": "0707220000010086",
          "intro": "Failed to read the filament information from AMS H slot 3. The RFID tag cannot rotate due to a jam during the filament loading or unloading. Please pull out the filament and try again."
        },
        {
          "ecode": "0703220000020021",
          "intro": "AMS D slot 3 assist motor is stalled，due to excessive resistance in the tube between the filament buffer and the toolhead."
        },
        {
          "ecode": "1805200000020004",
          "intro": "AMS-HT F Slot 1 filament may be broken in the tool head."
        },
        {
          "ecode": "0300930000010008",
          "intro": "Chamber temperature is abnormal. The temperature sensor at power supply may have an open circuit."
        },
        {
          "ecode": "03000D0000020001",
          "intro": "Heatbed homing abnormal: there may be a bulge on the heatbed or the nozzle tip may not be clean."
        },
        {
          "ecode": "1200730000010001",
          "intro": "AMS A Filament speed and length error: The slot 4 filament odometry may be faulty."
        },
        {
          "ecode": "0702200000020004",
          "intro": "AMS C Slot 1 filament may be broken in the tool head."
        },
        {
          "ecode": "1800010000010005",
          "intro": "AMS-HT A The current sensor of assist motor may be faulty."
        },
        {
          "ecode": "1804920000010001",
          "intro": "AMS-HT E The cooling fan of heater 1 is blocked, which may be due to the fan being stuck."
        },
        {
          "ecode": "1802200000020022",
          "intro": "AMS-HT C slot 1 assist motor is stalled，due to excessive resistance in the tube near the toolhead."
        },
        {
          "ecode": "0701200000010085",
          "intro": "Failed to read the filament information from AMS B slot 1. RFID tag verification failed. You can try to use Bambu Lab filament."
        },
        {
          "ecode": "1806800000010001",
          "intro": "AMS-HT G The current sensor of heater 1 is abnormal."
        },
        {
          "ecode": "0701110000010001",
          "intro": "The AMS B slot 2 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "0704230000030001",
          "intro": "AMS E Slot 4 filament has run out. Please wait while old filament is purged."
        },
        {
          "ecode": "0705200000010084",
          "intro": "Failed to read the filament information from AMS F slot 1. The RFID tag may be damaged or positioned at the edge of the RFID detection device. Please remove 5cm filament and try again."
        },
        {
          "ecode": "1801210000020001",
          "intro": "AMS-HT B Slot 2 filament has run out. Please insert a new filament."
        },
        {
          "ecode": "0701130000020004",
          "intro": "AMS B The brushed motor 4 has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "0703100000020004",
          "intro": "AMS D The brushed motor 1 has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "1802950000010001",
          "intro": "AMS-HT C The temperature sensor of heater 2 is malfunctioning, which may be due to poor connector contact."
        },
        {
          "ecode": "1807900000010003",
          "intro": "AMS-HT H The exhaust valve 1 is not connected, which may be due to poor connector contact."
        },
        {
          "ecode": "1202200000030002",
          "intro": "AMS C Slot1 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "0702220000020010",
          "intro": "AMS C slot 3 feeds filament out of AMS timeout."
        },
        {
          "ecode": "1806230000020017",
          "intro": "AMS-HT G slot 4 assist motor is stalled，due to excessive resistance in the tube between AMS and the printer."
        },
        {
          "ecode": "0300020000010002",
          "intro": "The nozzle temperature is abnormal; the heater may have an open circuit."
        },
        {
          "ecode": "1803950000010001",
          "intro": "AMS-HT D The temperature sensor of heater 2 is malfunctioning, which may be due to poor connector contact."
        },
        {
          "ecode": "1807810000010001",
          "intro": "AMS-HT H The current sensor of heater 2 is abnormal."
        },
        {
          "ecode": "1800200000020011",
          "intro": "AMS-HT A slot 1 pulls filament back to AMS timeout."
        },
        {
          "ecode": "0702200000020019",
          "intro": "AMS C slot 1 assist motor is stalled，due to excessive resistance in the tube between AMS and the filament buffer."
        },
        {
          "ecode": "1806900000020001",
          "intro": "AMS-HT G The operation of the exhaust valve 1 is abnormal, which may be due to excessive resistance."
        },
        {
          "ecode": "1804910000020001",
          "intro": "AMS-HT E The operation of the exhaust valve 2 is abnormal, which may be due to excessive resistance."
        },
        {
          "ecode": "1800220000020007",
          "intro": "AMS-HT A Slot 3 feed-out Hall sensor is disconnected. The connector may have poor contact."
        },
        {
          "ecode": "1803200000020021",
          "intro": "AMS-HT D slot 1 assist motor is stalled，due to excessive resistance in the tube between the filament buffer and the toolhead."
        },
        {
          "ecode": "1802210000020017",
          "intro": "AMS-HT C slot 2 assist motor is stalled，due to excessive resistance in the tube between AMS and the printer."
        },
        {
          "ecode": "1803230000010083",
          "intro": "Failed to read the filament information from AMS-HT D slot 4. The RFID tag may be damaged."
        },
        {
          "ecode": "1802200000020003",
          "intro": "AMS-HT C Slot 1's filament may be broken in AMS-HT."
        },
        {
          "ecode": "1807230000020018",
          "intro": "AMS-HT H slot 4 assist motor is stalled，due to excessive resistance in the tube near AMS."
        },
        {
          "ecode": "0705210000020004",
          "intro": "AMS F Slot 2 filament may be broken in the tool head."
        },
        {
          "ecode": "0702230000020017",
          "intro": "AMS C slot 4 assist motor is stalled，due to excessive resistance in the tube between AMS and the printer."
        },
        {
          "ecode": "0705230000030002",
          "intro": "AMS F Slot 4 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "0704010000020008",
          "intro": "AMS E The assist motor phase winding has an open circuit. The assist motor may be faulty."
        },
        {
          "ecode": "1802210000030002",
          "intro": "AMS-HT C Slot 2 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "0705200000010081",
          "intro": "Failed to read the filament information from AMS F slot 1. The AMS main board may be malfunctioning."
        },
        {
          "ecode": "1807200000020010",
          "intro": "AMS-HT H slot 1 feeds filament out of AMS timeout."
        },
        {
          "ecode": "1801220000020002",
          "intro": "AMS-HT B Slot 3 is empty; please insert a new filament."
        },
        {
          "ecode": "1806220000020019",
          "intro": "AMS-HT G slot 3 assist motor is stalled，due to excessive resistance in the tube between AMS and the filament buffer."
        },
        {
          "ecode": "0703950000010001",
          "intro": "AMS D The temperature sensor of heater 2 is malfunctioning, which may be due to poor connector contact."
        },
        {
          "ecode": "0706210000020003",
          "intro": "AMS G Slot 2's filament may be broken in AMS."
        },
        {
          "ecode": "0701230000020002",
          "intro": "AMS B Slot 4 is empty; please insert a new filament."
        },
        {
          "ecode": "1807230000020011",
          "intro": "AMS-HT H slot 4 pulls filament back to AMS timeout."
        },
        {
          "ecode": "0700220000020001",
          "intro": "AMS A Slot 3 filament has run out. Please insert a new filament."
        },
        {
          "ecode": "1800210000020017",
          "intro": "AMS-HT A slot 2 assist motor is stalled，due to excessive resistance in the tube between AMS and the printer."
        },
        {
          "ecode": "0703310000010004",
          "intro": "Encryption chip failure"
        },
        {
          "ecode": "0706230000020018",
          "intro": "AMS G slot 4 assist motor is stalled，due to excessive resistance in the tube near AMS."
        },
        {
          "ecode": "1803220000020005",
          "intro": "AMS-HT D Slot 3 filament has run out, and purging the old filament went abnormally; please check whether the filament is stuck in the tool head."
        },
        {
          "ecode": "1806200000020002",
          "intro": "AMS-HT G Slot 1 is empty; please insert a new filament."
        },
        {
          "ecode": "1806120000010003",
          "intro": "The AMS-HT G slot 3 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "1803230000020008",
          "intro": "AMS-HT D Slot 4 feed-in Hall sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "03000D0000020003",
          "intro": "The build plate may not be properly placed. If this message appears repeatedly, please check the Wiki for more explanations."
        },
        {
          "ecode": "1801010000010001",
          "intro": "The AMS-HT B assist motor has slipped. The extrusion wheel may be worn down, or the filament may be too thin."
        },
        {
          "ecode": "1203810000020001",
          "intro": "AMS D Slot2 filament may be tangled or stuck."
        },
        {
          "ecode": "0300920000010006",
          "intro": "The temperature of chamber heater 2 is abnormal. The sensor may have a short circuit."
        },
        {
          "ecode": "1203220000020004",
          "intro": "AMS D Slot3 filament may be broken in the tool head."
        },
        {
          "ecode": "0705230000020021",
          "intro": "AMS F slot 4 assist motor is stalled，due to excessive resistance in the tube between the filament buffer and the toolhead."
        },
        {
          "ecode": "0705120000020004",
          "intro": "AMS F The brushed motor 3 has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "1803210000020021",
          "intro": "AMS-HT D slot 2 assist motor is stalled，due to excessive resistance in the tube between the filament buffer and the toolhead."
        },
        {
          "ecode": "1803010000020009",
          "intro": "AMS-HT D The assist motor has unbalanced tree-phase resistaance. The assist motor may be faulty."
        },
        {
          "ecode": "0707010000010003",
          "intro": "The AMS H assist motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "0706220000020018",
          "intro": "AMS G slot 3 assist motor is stalled，due to excessive resistance in the tube near AMS."
        },
        {
          "ecode": "1203230000020001",
          "intro": "AMS D Slot4 filament has run out; please insert a new filament."
        },
        {
          "ecode": "1807230000030001",
          "intro": "AMS-HT H Slot 4 filament has run out. Please wait while old filament is purged."
        },
        {
          "ecode": "0701200000020007",
          "intro": "AMS B Slot 1 feed-out Hall sensor is disconnected. The connector may have poor contact."
        },
        {
          "ecode": "1801810000010004",
          "intro": "AMS-HT B The heater 2 is heating abnormally."
        },
        {
          "ecode": "1802210000020010",
          "intro": "AMS-HT C slot 2 feeds filament out of AMS timeout."
        },
        {
          "ecode": "0707200000020009",
          "intro": "Failed to extrude AMS H Slot 1 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "0702010000020009",
          "intro": "AMS C The assist motor has unbalanced tree-phase resistaance. The assist motor may be faulty."
        },
        {
          "ecode": "1800920000020002",
          "intro": "AMS-HT A The cooling fan speed of heater 1 is too low, which could be due to excessive fan resistance."
        },
        {
          "ecode": "1803500000020001",
          "intro": "AMS-HT D communication is abnormal; please check the connection cable."
        },
        {
          "ecode": "1804220000010084",
          "intro": "Failed to read the filament information from AMS-HT E slot 3. The RFID tag may be damaged or positioned at the edge of the RFID detection device. Please remove 5cm filament and try again."
        },
        {
          "ecode": "0702910000010003",
          "intro": "AMS C The exhaust valve 2 is not connected, which may be due to poor connector contact."
        },
        {
          "ecode": "1807110000020004",
          "intro": "AMS-HT H The brushed motor 2 has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "0701810000010001",
          "intro": "AMS B The current sensor of heater 2 is abnormal."
        },
        {
          "ecode": "1806220000010083",
          "intro": "Failed to read the filament information from AMS-HT G slot 3. The RFID tag may be damaged."
        },
        {
          "ecode": "1803210000020018",
          "intro": "AMS-HT D slot 2 assist motor is stalled，due to excessive resistance in the tube near AMS."
        },
        {
          "ecode": "1202220000020001",
          "intro": "AMS C Slot3 filament has run out; please insert a new filament."
        },
        {
          "ecode": "0706940000010001",
          "intro": "AMS G The temperature sensor of heater 1 is malfunctioning, which may be due to poor connector contact."
        },
        {
          "ecode": "0707220000020005",
          "intro": "AMS H Slot 3 filament has run out, and purging the old filament went abnormally; please check whether the filament is stuck in the tool head."
        },
        {
          "ecode": "03000B0000010001",
          "intro": "Heatbed force sensor 2 is too sensitive. It may be stuck between the strain arm and heatbed support, or the adjusting screw may be too tight."
        },
        {
          "ecode": "0701110000020002",
          "intro": "The AMS B slot 2 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "1803700000020003",
          "intro": "Failed to extrude the filament. Possible cause: extruder or nozzle clog."
        },
        {
          "ecode": "0300410000010001",
          "intro": "The system voltage is unstable. Triggering the power failure protection function."
        },
        {
          "ecode": "1807220000020024",
          "intro": "AMS-HT H slot 3 failed to rotate the filament spool when pulling filament back to AMS."
        },
        {
          "ecode": "0701310000010001",
          "intro": "The AMS B RFID 2 board has an error."
        },
        {
          "ecode": "0707230000020017",
          "intro": "AMS H slot 4 assist motor is stalled，due to excessive resistance in the tube between AMS and the printer."
        },
        {
          "ecode": "1800120000020004",
          "intro": "AMS-HT A The brushed motor 3 has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "1806200000020022",
          "intro": "AMS-HT G slot 1 assist motor is stalled，due to excessive resistance in the tube near the toolhead."
        },
        {
          "ecode": "0700230000020022",
          "intro": "AMS A slot 4 assist motor is stalled，due to excessive resistance in the tube near the toolhead."
        },
        {
          "ecode": "0705200000020021",
          "intro": "AMS F slot 1 assist motor is stalled，due to excessive resistance in the tube between the filament buffer and the toolhead."
        },
        {
          "ecode": "1801200000020011",
          "intro": "AMS-HT B slot 1 pulls filament back to AMS timeout."
        },
        {
          "ecode": "1805230000030002",
          "intro": "AMS-HT F Slot 4 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "0704230000020003",
          "intro": "AMS E Slot 4's filament may be broken in AMS."
        },
        {
          "ecode": "1805230000020024",
          "intro": "AMS-HT F slot 4 failed to rotate the filament spool when pulling filament back to AMS."
        },
        {
          "ecode": "0706200000030001",
          "intro": "AMS G Slot 1 filament has run out. Please wait while old filament is purged."
        },
        {
          "ecode": "0704970000030001",
          "intro": "AMS E chamber temperature is too high; auxiliary feeding or RFID reading is currently not allowed."
        },
        {
          "ecode": "1807200000020017",
          "intro": "AMS-HT H slot 1 assist motor is stalled，due to excessive resistance in the tube between AMS and the printer."
        },
        {
          "ecode": "1806020000010001",
          "intro": "AMS-HT G Filament speed and length error: The filament odometry may be faulty."
        },
        {
          "ecode": "1805200000020003",
          "intro": "AMS-HT F Slot 1's filament may be broken in AMS-HT."
        },
        {
          "ecode": "0707210000020010",
          "intro": "AMS H slot 2 feeds filament out of AMS timeout."
        },
        {
          "ecode": "0702220000020011",
          "intro": "AMS C slot 3 pulls filament back to AMS timeout."
        },
        {
          "ecode": "1801200000020010",
          "intro": "AMS-HT B slot 1 feeds filament out of AMS timeout."
        },
        {
          "ecode": "1804110000020004",
          "intro": "AMS-HT E The brushed motor 2 has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "1802910000010003",
          "intro": "AMS-HT C The exhaust valve 2 is not connected, which may be due to poor connector contact."
        },
        {
          "ecode": "03000D0000010009",
          "intro": "The build plate is not placed properly. Please adjust it."
        },
        {
          "ecode": "0701210000020024",
          "intro": "AMS B slot 2 failed to rotate the filament spool when pulling filament back to AMS."
        },
        {
          "ecode": "0703350000010001",
          "intro": "The temperature and humidity sensor has an error. The chip may be faulty."
        },
        {
          "ecode": "0703220000030001",
          "intro": "AMS D Slot 3 filament has run out. Please wait while old filament is purged."
        },
        {
          "ecode": "1800200000010086",
          "intro": "Failed to read the filament information from AMS-HT A slot 1. The RFID tag cannot rotate due to a jam during the filament loading or unloading. Please pull out the filament and try again."
        },
        {
          "ecode": "1806560000030001",
          "intro": "AMS-HT G is undergoing dry cooling; please wait for it to cool down before operating."
        },
        {
          "ecode": "1801220000020009",
          "intro": "Failed to extrude AMS-HT B Slot 3 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "1801210000020017",
          "intro": "AMS-HT B slot 2 assist motor is stalled，due to excessive resistance in the tube between AMS and the printer."
        },
        {
          "ecode": "0700900000010003",
          "intro": "AMS A The exhaust valve 1 is not connected, which may be due to poor connector contact."
        },
        {
          "ecode": "1200200000020001",
          "intro": "AMS A Slot1 filament has run out; please insert a new filament."
        },
        {
          "ecode": "1803230000020007",
          "intro": "AMS-HT D Slot 4 feed-out Hall sensor is disconnected. The connector may have poor contact."
        },
        {
          "ecode": "1801010000020010",
          "intro": "AMS-HT B The assist motor resistance is abnormal. The assist motor may be faulty."
        },
        {
          "ecode": "1804010000010011",
          "intro": "AMS-HT E The assist motor calibration parameter error. Please pull out the filament from the filament hub and then restart the AMS."
        },
        {
          "ecode": "1804900000010003",
          "intro": "AMS-HT E The exhaust valve 1 is not connected, which may be due to poor connector contact."
        },
        {
          "ecode": "0700220000020017",
          "intro": "AMS A slot 3 assist motor is stalled，due to excessive resistance in the tube between AMS and the printer."
        },
        {
          "ecode": "0707200000010083",
          "intro": "Failed to read the filament information from AMS H slot 1. The RFID tag may be damaged."
        },
        {
          "ecode": "1203700000010001",
          "intro": "AMS D Filament speed and length error: The slot 1 filament odometry may be faulty."
        },
        {
          "ecode": "0700210000020002",
          "intro": "AMS A Slot 2 is empty; please insert a new filament."
        },
        {
          "ecode": "1805210000020010",
          "intro": "AMS-HT F slot 2 feeds filament out of AMS timeout."
        },
        {
          "ecode": "0705200000030002",
          "intro": "AMS F Slot 1 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "0704220000020008",
          "intro": "AMS E Slot 3 feed-in Hall sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "0702960000020002",
          "intro": "AMS C Environmental temperature is too low, which will affect the drying capability."
        },
        {
          "ecode": "1806210000020007",
          "intro": "AMS-HT G Slot 2 feed-out Hall sensor is disconnected. The connector may have poor contact."
        },
        {
          "ecode": "0703920000010001",
          "intro": "AMS D The cooling fan of heater 1 is blocked, which may be due to the fan being stuck."
        },
        {
          "ecode": "1805230000020007",
          "intro": "AMS-HT F Slot 4 feed-out Hall sensor is disconnected. The connector may have poor contact."
        },
        {
          "ecode": "0500030000010021",
          "intro": "Hardware incompatible; please check the Micro Lidar."
        },
        {
          "ecode": "1807200000020004",
          "intro": "AMS-HT H Slot 1 filament may be broken in the tool head."
        },
        {
          "ecode": "0705200000020004",
          "intro": "AMS F Slot 1 filament may be broken in the tool head."
        },
        {
          "ecode": "1804200000020008",
          "intro": "AMS-HT E Slot 1 feed-in Hall sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "0300180000010006",
          "intro": "The heatbed leveling data is abnormal. Please check whether there are any foreign objects on the heatbed and Z slider. If so, please remove them and try again."
        },
        {
          "ecode": "1806210000020018",
          "intro": "AMS-HT G slot 2 assist motor is stalled，due to excessive resistance in the tube near AMS."
        },
        {
          "ecode": "0701210000020005",
          "intro": "AMS B Slot 2 filament has run out, and purging the old filament went abnormally; please check whether the filament is stuck in the tool head."
        },
        {
          "ecode": "1804930000020002",
          "intro": "AMS-HT E The cooling fan speed of heater 2 is too low, which could be due to excessive fan resistance."
        },
        {
          "ecode": "1201300000010001",
          "intro": "AMS B Slot 1 RFID coil is broken or the RF hardware circuit has an error."
        },
        {
          "ecode": "1801220000020007",
          "intro": "AMS-HT B Slot 3 feed-out Hall sensor is disconnected. The connector may have poor contact."
        },
        {
          "ecode": "1202310000010001",
          "intro": "AMS C Slot 2 RFID coil is broken or the RF hardware circuit has an error."
        },
        {
          "ecode": "1802300000030003",
          "intro": "RFID cannot be read because of a hardware or structural error."
        },
        {
          "ecode": "1807220000020021",
          "intro": "AMS-HT H slot 3 assist motor is stalled，due to excessive resistance in the tube between the filament buffer and the toolhead."
        },
        {
          "ecode": "1801200000020004",
          "intro": "AMS-HT B Slot 1 filament may be broken in the tool head."
        },
        {
          "ecode": "1802210000020002",
          "intro": "AMS-HT C Slot 2 is empty; please insert a new filament."
        },
        {
          "ecode": "0703010000020010",
          "intro": "AMS D The assist motor resistance is abnormal. The assist motor may be faulty."
        },
        {
          "ecode": "1804210000020017",
          "intro": "AMS-HT E slot 2 assist motor is stalled，due to excessive resistance in the tube between AMS and the printer."
        },
        {
          "ecode": "0700200000020017",
          "intro": "AMS A slot 1 assist motor is stalled，due to excessive resistance in the tube between AMS and the printer."
        },
        {
          "ecode": "1800960000010001",
          "intro": "AMS-HT A The drying process may experience thermal runaway. Please turn off the AMS power supply."
        },
        {
          "ecode": "0704230000010085",
          "intro": "Failed to read the filament information from AMS E slot 4. RFID tag verification failed. You can try to use Bambu Lab filament."
        },
        {
          "ecode": "1800220000020009",
          "intro": "Failed to extrude AMS-HT A Slot 3 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "1804120000020002",
          "intro": "The AMS-HT E slot 3 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "1803130000020002",
          "intro": "The AMS-HT D slot 4 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "1803800000010004",
          "intro": "AMS-HT D The heater 1 is heating abnormally."
        },
        {
          "ecode": "1806220000010085",
          "intro": "Failed to read the filament information from AMS-HT G slot 3. RFID tag verification failed. You can try to use Bambu Lab filament."
        },
        {
          "ecode": "0704700000020002",
          "intro": "Failed to feed the filament into the toolhead. Possible cause: filament or spool stuck."
        },
        {
          "ecode": "0705230000030001",
          "intro": "AMS F Slot 4 filament has run out. Please wait while old filament is purged."
        },
        {
          "ecode": "0706200000020001",
          "intro": "AMS G Slot 1 filament has run out. Please insert a new filament."
        },
        {
          "ecode": "0703130000010003",
          "intro": "The AMS D slot 4 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "0300900000010004",
          "intro": "Chamber heating failed. The speed of the heating fan is too low."
        },
        {
          "ecode": "1201110000010001",
          "intro": "The AMS B Slot2 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "1807220000020011",
          "intro": "AMS-HT H slot 3 pulls filament back to AMS timeout."
        },
        {
          "ecode": "1804200000020002",
          "intro": "AMS-HT E Slot 1 is empty; please insert a new filament."
        },
        {
          "ecode": "1202200000020001",
          "intro": "AMS C Slot1 filament has run out; please insert a new filament."
        },
        {
          "ecode": "0703230000020022",
          "intro": "AMS D slot 4 assist motor is stalled，due to excessive resistance in the tube near the toolhead."
        },
        {
          "ecode": "0700560000030001",
          "intro": "AMS A is undergoing dry cooling; please wait for it to cool down before operating."
        },
        {
          "ecode": "0702210000020022",
          "intro": "AMS C slot 2 assist motor is stalled，due to excessive resistance in the tube near the toolhead."
        },
        {
          "ecode": "1803210000020011",
          "intro": "AMS-HT D slot 2 pulls filament back to AMS timeout."
        },
        {
          "ecode": "0700210000020017",
          "intro": "AMS A slot 2 assist motor is stalled，due to excessive resistance in the tube between AMS and the printer."
        },
        {
          "ecode": "0702200000020017",
          "intro": "AMS C slot 1 assist motor is stalled，due to excessive resistance in the tube between AMS and the printer."
        },
        {
          "ecode": "1800700000020007",
          "intro": "AMS-HT filament ran out. Please put a new filament into the same slot in AMS and resume."
        },
        {
          "ecode": "1803230000020024",
          "intro": "AMS-HT D slot 4 failed to rotate the filament spool when pulling filament back to AMS."
        },
        {
          "ecode": "1802100000010001",
          "intro": "The AMS-HT C slot 1 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "0704900000020001",
          "intro": "AMS E The operation of the exhaust valve 1 is abnormal, which may be due to excessive resistance."
        },
        {
          "ecode": "1203730000010001",
          "intro": "AMS D Filament speed and length error: The slot 4 filament odometry may be faulty."
        },
        {
          "ecode": "1806100000020004",
          "intro": "AMS-HT G The brushed motor 1 has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "0706230000020007",
          "intro": "AMS G Slot 4 feed-out Hall sensor is disconnected. The connector may have poor contact."
        },
        {
          "ecode": "0700960000010001",
          "intro": "AMS A The drying process may experience thermal runaway. Please turn off the AMS power supply."
        },
        {
          "ecode": "0702210000010081",
          "intro": "Failed to read the filament information from AMS C slot 2. The AMS main board may be malfunctioning."
        },
        {
          "ecode": "0705200000020017",
          "intro": "AMS F slot 1 assist motor is stalled，due to excessive resistance in the tube between AMS and the printer."
        },
        {
          "ecode": "0704200000020004",
          "intro": "AMS E Slot 1 filament may be broken in the tool head."
        },
        {
          "ecode": "0707220000030001",
          "intro": "AMS H Slot 3 filament has run out. Please wait while old filament is purged."
        },
        {
          "ecode": "1203210000020003",
          "intro": "AMS D Slot2 filament may be broken in the PTFE tube."
        },
        {
          "ecode": "1804700000020002",
          "intro": "Failed to feed the filament into the toolhead. Possible cause: filament or spool stuck."
        },
        {
          "ecode": "0704210000010084",
          "intro": "Failed to read the filament information from AMS E slot 2. The RFID tag may be damaged or positioned at the edge of the RFID detection device. Please remove 5cm filament and try again."
        },
        {
          "ecode": "18FF200000020002",
          "intro": "External filament is missing; please load a new filament."
        },
        {
          "ecode": "0705210000030001",
          "intro": "AMS F Slot 2 filament has run out. Please wait while old filament is purged."
        },
        {
          "ecode": "1201210000020002",
          "intro": "AMS B Slot 2 is empty; please insert a new filament."
        },
        {
          "ecode": "1807230000010081",
          "intro": "Failed to read the filament information from AMS-HT H slot 4. The AMS main board may be malfunctioning."
        },
        {
          "ecode": "0704230000020017",
          "intro": "AMS E slot 4 assist motor is stalled，due to excessive resistance in the tube between AMS and the printer."
        },
        {
          "ecode": "1202300000030003",
          "intro": "AMS C Slot1 RFID cannot be read because of a structural error."
        },
        {
          "ecode": "1804960000010003",
          "intro": "AMS-HT E Unable to start drying; please pull out the filament from filament hub and try again."
        },
        {
          "ecode": "0706800000010004",
          "intro": "AMS G The heater 1 is heating abnormally."
        },
        {
          "ecode": "1801310000030003",
          "intro": "RFID cannot be read because of a hardware or structural error."
        },
        {
          "ecode": "1807010000010001",
          "intro": "The AMS-HT H assist motor has slipped. The extrusion wheel may be worn down, or the filament may be too thin."
        },
        {
          "ecode": "0707230000010083",
          "intro": "Failed to read the filament information from AMS H slot 4. The RFID tag may be damaged."
        },
        {
          "ecode": "1802320000020002",
          "intro": "The RFID-tag on AMS-HT C Slot3 is damaged, or its content cannot be identified."
        },
        {
          "ecode": "0701300000010004",
          "intro": "Encryption chip failure"
        },
        {
          "ecode": "0705220000020022",
          "intro": "AMS F slot 3 assist motor is stalled，due to excessive resistance in the tube near the toolhead."
        },
        {
          "ecode": "1802960000020002",
          "intro": "AMS-HT C Environmental temperature is too low, which will affect the drying capability."
        },
        {
          "ecode": "0704220000020003",
          "intro": "AMS E Slot 3's filament may be broken in AMS."
        },
        {
          "ecode": "0702200000010086",
          "intro": "Failed to read the filament information from AMS C slot 1. The RFID tag cannot rotate due to a jam during the filament loading or unloading. Please pull out the filament and try again."
        },
        {
          "ecode": "1806210000020009",
          "intro": "Failed to extrude AMS-HT G Slot 2 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "1807200000020003",
          "intro": "AMS-HT H Slot 1's filament may be broken in AMS-HT."
        },
        {
          "ecode": "0706220000010081",
          "intro": "Failed to read the filament information from AMS G slot 3. The AMS main board may be malfunctioning."
        },
        {
          "ecode": "0700910000020001",
          "intro": "AMS A The operation of the exhaust valve 2 is abnormal, which may be due to excessive resistance."
        },
        {
          "ecode": "1201120000010001",
          "intro": "The AMS B Slot3 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "1800310000030003",
          "intro": "RFID cannot be read because of a hardware or structural error."
        },
        {
          "ecode": "1806210000010084",
          "intro": "Failed to read the filament information from AMS-HT G slot 2. The RFID tag may be damaged or positioned at the edge of the RFID detection device. Please remove 5cm filament and try again."
        },
        {
          "ecode": "1806910000020001",
          "intro": "AMS-HT G The operation of the exhaust valve 2 is abnormal, which may be due to excessive resistance."
        },
        {
          "ecode": "0701230000030001",
          "intro": "AMS B Slot 4 filament has run out. Please wait while old filament is purged."
        },
        {
          "ecode": "1802700000020007",
          "intro": "AMS-HT filament ran out. Please put a new filament into the same slot in AMS and resume."
        },
        {
          "ecode": "0700230000010085",
          "intro": "Failed to read the filament information from AMS A slot 4. RFID tag verification failed. You can try to use Bambu Lab filament."
        },
        {
          "ecode": "0702220000020024",
          "intro": "AMS C slot 3 failed to rotate the filament spool when pulling filament back to AMS."
        },
        {
          "ecode": "0500030000010008",
          "intro": "A system hang occurred. Please restart the device."
        },
        {
          "ecode": "1201310000010001",
          "intro": "AMS B Slot 2 RFID coil is broken or the RF hardware circuit has an error."
        },
        {
          "ecode": "1804010000010003",
          "intro": "The AMS-HT E assist motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "1800210000010081",
          "intro": "Failed to read the filament information from AMS-HT A slot 2. The AMS main board may be malfunctioning."
        },
        {
          "ecode": "1203210000020006",
          "intro": "Failed to extrude AMS D Slot2 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "12FF200000020005",
          "intro": "Filament may be broken in the tool head."
        },
        {
          "ecode": "0700230000020011",
          "intro": "AMS A slot 4 pulls filament back to AMS timeout."
        },
        {
          "ecode": "1800210000020007",
          "intro": "AMS-HT A Slot 2 feed-out Hall sensor is disconnected. The connector may have poor contact."
        },
        {
          "ecode": "03000D0000020007",
          "intro": "The build plate may not be properly placed. If this message appears repeatedly, please check the Wiki for more explanations."
        },
        {
          "ecode": "0701220000020020",
          "intro": "AMS B slot 3 assist motor is stalled，due to excessive resistance in the tube near the filament buffer。"
        },
        {
          "ecode": "0700200000020024",
          "intro": "AMS A slot 1 failed to rotate the filament spool when pulling filament back to AMS."
        },
        {
          "ecode": "1807100000010001",
          "intro": "The AMS-HT H slot 1 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "1807200000010085",
          "intro": "Failed to read the filament information from AMS-HT H slot 1. RFID tag verification failed. You can try to use Bambu Lab filament."
        },
        {
          "ecode": "0700230000020001",
          "intro": "AMS A Slot 4 filament has run out. Please insert a new filament."
        },
        {
          "ecode": "1803130000020004",
          "intro": "AMS-HT D The brushed motor 4 has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "0702200000020002",
          "intro": "AMS C Slot 1 is empty; please insert a new filament."
        },
        {
          "ecode": "1801100000010001",
          "intro": "The AMS-HT B slot 1 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "0701230000020024",
          "intro": "AMS B slot 4 failed to rotate the filament spool when pulling filament back to AMS."
        },
        {
          "ecode": "1200220000020003",
          "intro": "AMS A Slot3 filament may be broken in the PTFE tube."
        },
        {
          "ecode": "0700010000010011",
          "intro": "AMS A The assist motor calibration parameter error. Please pull out the filament from the filament hub and then restart the AMS."
        },
        {
          "ecode": "0702810000010003",
          "intro": "AMS C The heater 2 is short-circuited, which may be due to a wiring short or heater damage."
        },
        {
          "ecode": "1806200000020017",
          "intro": "AMS-HT G slot 1 assist motor is stalled，due to excessive resistance in the tube between AMS and the printer."
        },
        {
          "ecode": "0500040000020018",
          "intro": "The RFID-tag on AMS C Slot1 cannot be identified."
        },
        {
          "ecode": "1800230000010085",
          "intro": "Failed to read the filament information from AMS-HT A slot 4. RFID tag verification failed. You can try to use Bambu Lab filament."
        },
        {
          "ecode": "0706920000010001",
          "intro": "AMS G The cooling fan of heater 1 is blocked, which may be due to the fan being stuck."
        },
        {
          "ecode": "1806230000020008",
          "intro": "AMS-HT G Slot 4 feed-in Hall sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "0701230000020008",
          "intro": "AMS B Slot 4 feed-in Hall sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "1800210000020003",
          "intro": "AMS-HT A Slot 2's filament may be broken in AMS-HT."
        },
        {
          "ecode": "1800210000020021",
          "intro": "AMS-HT A slot 2 assist motor is stalled，due to excessive resistance in the tube between the filament buffer and the toolhead."
        },
        {
          "ecode": "0703810000010003",
          "intro": "AMS D The heater 2 is short-circuited, which may be due to a wiring short or heater damage."
        },
        {
          "ecode": "1801220000020020",
          "intro": "AMS-HT B slot 3 assist motor is stalled，due to excessive resistance in the tube near the filament buffer。"
        },
        {
          "ecode": "1803010000010004",
          "intro": "The AMS-HT D assist motor speed control is malfunctioning. The speed sensor may be faulty."
        },
        {
          "ecode": "1804220000020003",
          "intro": "AMS-HT E Slot 3's filament may be broken in AMS-HT."
        },
        {
          "ecode": "1805100000010001",
          "intro": "The AMS-HT F slot 1 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "1806230000010081",
          "intro": "Failed to read the filament information from AMS-HT G slot 4. The AMS main board may be malfunctioning."
        },
        {
          "ecode": "1806960000010001",
          "intro": "AMS-HT G The drying process may experience thermal runaway. Please turn off the AMS power supply."
        },
        {
          "ecode": "1203300000020002",
          "intro": "The RFID-tag on AMS D Slot 1 is damaged."
        },
        {
          "ecode": "12FF800000020001",
          "intro": "The filament on the spool holder may be tangled or stuck."
        },
        {
          "ecode": "1201320000030003",
          "intro": "AMS B Slot3 RFID cannot be read because of a structural error."
        },
        {
          "ecode": "0500040000020013",
          "intro": "The RFID-tag on AMS A Slot4 cannot be identified."
        },
        {
          "ecode": "0701810000010004",
          "intro": "AMS B The heater 2 is heating abnormally."
        },
        {
          "ecode": "1201200000030002",
          "intro": "AMS B Slot1 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "1801300000010004",
          "intro": "Encryption chip failure"
        },
        {
          "ecode": "1807210000020007",
          "intro": "AMS-HT H Slot 2 feed-out Hall sensor is disconnected. The connector may have poor contact."
        },
        {
          "ecode": "0707120000010003",
          "intro": "The AMS H slot 3 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "1806930000010001",
          "intro": "AMS-HT G The cooling fan of heater 2 is blocked, which may be due to the fan being stuck."
        },
        {
          "ecode": "1807930000020002",
          "intro": "AMS-HT H The cooling fan speed of heater 2 is too low, which could be due to excessive fan resistance."
        },
        {
          "ecode": "1800210000020024",
          "intro": "AMS-HT A slot 2 failed to rotate the filament spool when pulling filament back to AMS."
        },
        {
          "ecode": "1804300000010004",
          "intro": "Encryption chip failure"
        },
        {
          "ecode": "1807230000010084",
          "intro": "Failed to read the filament information from AMS-HT H slot 4. The RFID tag may be damaged or positioned at the edge of the RFID detection device. Please remove 5cm filament and try again."
        },
        {
          "ecode": "0707920000020002",
          "intro": "AMS H The cooling fan speed of heater 1 is too low, which could be due to excessive fan resistance."
        },
        {
          "ecode": "0702220000020008",
          "intro": "AMS C Slot 3 feed-in Hall sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "0700800000010001",
          "intro": "AMS A The current sensor of heater 1 is abnormal."
        },
        {
          "ecode": "1805210000020017",
          "intro": "AMS-HT F slot 2 assist motor is stalled，due to excessive resistance in the tube between AMS and the printer."
        },
        {
          "ecode": "0704230000020008",
          "intro": "AMS E Slot 4 feed-in Hall sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "1201330000010001",
          "intro": "AMS B Slot 4 RFID coil is broken or the RF hardware circuit has an error."
        },
        {
          "ecode": "0707200000010084",
          "intro": "Failed to read the filament information from AMS H slot 1. The RFID tag may be damaged or positioned at the edge of the RFID detection device. Please remove 5cm filament and try again."
        },
        {
          "ecode": "0702810000010004",
          "intro": "AMS C The heater 2 is heating abnormally."
        },
        {
          "ecode": "1800010000020007",
          "intro": "AMS-HT A The assist motor encoder wires are not connected. The assist motor connector may have poor contact."
        },
        {
          "ecode": "07FF200000020002",
          "intro": "External filament is missing; please load a new filament."
        },
        {
          "ecode": "1202230000030002",
          "intro": "AMS C Slot4 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "1802800000010001",
          "intro": "AMS-HT C The current sensor of heater 1 is abnormal."
        },
        {
          "ecode": "0300110000020001",
          "intro": "The resonance frequency of the Y axis is low. The timing belt may be loose."
        },
        {
          "ecode": "0300150000010001",
          "intro": "The current sensor of Motor-Z is abnormal. This may be caused by a failure of the hardware sampling circuit."
        },
        {
          "ecode": "1805230000020005",
          "intro": "AMS-HT F Slot 4 filament has run out, and purging the old filament went abnormally; please check whether the filament is stuck in the tool head."
        },
        {
          "ecode": "0703130000020004",
          "intro": "AMS D The brushed motor 4 has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "0707300000030003",
          "intro": "RFID cannot be read because of a hardware or structural error."
        },
        {
          "ecode": "1806210000010081",
          "intro": "Failed to read the filament information from AMS-HT G slot 2. The AMS main board may be malfunctioning."
        },
        {
          "ecode": "1803810000010004",
          "intro": "AMS-HT D The heater 2 is heating abnormally."
        },
        {
          "ecode": "1801220000020003",
          "intro": "AMS-HT B Slot 3's filament may be broken in AMS-HT."
        },
        {
          "ecode": "1202500000020001",
          "intro": "AMS C communication is abnormal; please check the connection cable."
        },
        {
          "ecode": "0701700000020004",
          "intro": "Failed to pull back the filament from the toolhead to AMS. Possible cause: filament or spool stuck."
        },
        {
          "ecode": "0702210000020007",
          "intro": "AMS C Slot 2 feed-out Hall sensor is disconnected. The connector may have poor contact."
        },
        {
          "ecode": "0300200000010002",
          "intro": "Y-axis homing abnormal: please check if the toolhead is stuck or the Y carriage has too much resistance."
        },
        {
          "ecode": "0703010000010003",
          "intro": "The AMS D assist motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "1805130000010001",
          "intro": "The AMS-HT F slot 4 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "0706700000020002",
          "intro": "Failed to feed the filament into the toolhead. Possible cause: filament or spool stuck."
        },
        {
          "ecode": "0706220000020021",
          "intro": "AMS G slot 3 assist motor is stalled，due to excessive resistance in the tube between the filament buffer and the toolhead."
        },
        {
          "ecode": "1802210000020001",
          "intro": "AMS-HT C Slot 2 filament has run out. Please insert a new filament."
        },
        {
          "ecode": "0701120000020002",
          "intro": "The AMS B slot 3 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "0706200000020018",
          "intro": "AMS G slot 1 assist motor is stalled，due to excessive resistance in the tube near AMS."
        },
        {
          "ecode": "1203300000010001",
          "intro": "AMS D Slot 1 RFID coil is broken or the RF hardware circuit has an error."
        },
        {
          "ecode": "1803700000020004",
          "intro": "Failed to pull back the filament from the toolhead to AMS-HT. Possible cause: filament or spool stuck."
        },
        {
          "ecode": "0706120000020002",
          "intro": "The AMS G slot 3 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "1806200000020001",
          "intro": "AMS-HT G Slot 1 filament has run out. Please insert a new filament."
        },
        {
          "ecode": "0700200000010084",
          "intro": "Failed to read the filament information from AMS A slot 1. The RFID tag may be damaged or positioned at the edge of the RFID detection device. Please remove 5cm filament and try again."
        },
        {
          "ecode": "1800220000030001",
          "intro": "AMS-HT A Slot 3 filament has run out. Please wait while old filament is purged."
        },
        {
          "ecode": "03000D0000010002",
          "intro": "Heatbed homing failed. The environmental vibration is too great."
        },
        {
          "ecode": "1800310000020002",
          "intro": "The RFID-tag on AMS-HT A Slot2 is damaged, or its content cannot be identified."
        },
        {
          "ecode": "1802210000020019",
          "intro": "AMS-HT C slot 2 assist motor is stalled，due to excessive resistance in the tube between AMS and the filament buffer."
        },
        {
          "ecode": "1807220000020002",
          "intro": "AMS-HT H Slot 3 is empty; please insert a new filament."
        },
        {
          "ecode": "0700500000020001",
          "intro": "AMS A communication is abnormal; please check the connection cable."
        },
        {
          "ecode": "0300030000010001",
          "intro": "The hotend cooling fan speed is too slow or stopped. It may be stuck or the connector may not be plugged in properly."
        },
        {
          "ecode": "0500030000030022",
          "intro": "MicroSD Card performance degradation has been detected. It may affect print jobs, logs, and video records. Please format or change the MicroSD card."
        },
        {
          "ecode": "0704220000020018",
          "intro": "AMS E slot 3 assist motor is stalled，due to excessive resistance in the tube near AMS."
        },
        {
          "ecode": "1800110000020004",
          "intro": "AMS-HT A The brushed motor 2 has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "0701960000010001",
          "intro": "AMS B The drying process may experience thermal runaway. Please turn off the AMS power supply."
        },
        {
          "ecode": "0700300000020002",
          "intro": "The RFID-tag on AMS A Slot1 is damaged, or its content cannot be identified."
        },
        {
          "ecode": "0704230000020011",
          "intro": "AMS E slot 4 pulls filament back to AMS timeout."
        },
        {
          "ecode": "0705010000020010",
          "intro": "AMS F The assist motor resistance is abnormal. The assist motor may be faulty."
        },
        {
          "ecode": "0705200000010086",
          "intro": "Failed to read the filament information from AMS F slot 1. The RFID tag cannot rotate due to a jam during the filament loading or unloading. Please pull out the filament and try again."
        },
        {
          "ecode": "0704200000010081",
          "intro": "Failed to read the filament information from AMS E slot 1. The AMS main board may be malfunctioning."
        },
        {
          "ecode": "0701230000010083",
          "intro": "Failed to read the filament information from AMS B slot 4. The RFID tag may be damaged."
        },
        {
          "ecode": "0704220000010085",
          "intro": "Failed to read the filament information from AMS E slot 3. RFID tag verification failed. You can try to use Bambu Lab filament."
        },
        {
          "ecode": "1202100000010003",
          "intro": "The AMS C Slot1 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "0702200000020005",
          "intro": "AMS C Slot 1 filament has run out, and purging the old filament went abnormally; please check whether the filament is stuck in the tool head."
        },
        {
          "ecode": "1201130000020002",
          "intro": "The AMS B Slot4 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "0707200000010081",
          "intro": "Failed to read the filament information from AMS H slot 1. The AMS main board may be malfunctioning."
        },
        {
          "ecode": "1802310000010004",
          "intro": "Encryption chip failure"
        },
        {
          "ecode": "1202220000020003",
          "intro": "AMS C Slot3 filament may be broken in the PTFE tube."
        },
        {
          "ecode": "0707220000020017",
          "intro": "AMS H slot 3 assist motor is stalled，due to excessive resistance in the tube between AMS and the printer."
        },
        {
          "ecode": "0705220000020017",
          "intro": "AMS F slot 3 assist motor is stalled，due to excessive resistance in the tube between AMS and the printer."
        },
        {
          "ecode": "0702200000020022",
          "intro": "AMS C slot 1 assist motor is stalled，due to excessive resistance in the tube near the toolhead."
        },
        {
          "ecode": "0703220000020003",
          "intro": "AMS D Slot 3's filament may be broken in AMS."
        },
        {
          "ecode": "0706230000020008",
          "intro": "AMS G Slot 4 feed-in Hall sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "0701800000010002",
          "intro": "AMS B The heater 1 is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "03001B0000010001",
          "intro": "The signal of the heatbed acceleration sensor is weak. The sensor may have fallen off or been damaged."
        },
        {
          "ecode": "1203210000020002",
          "intro": "AMS D Slot 2 is empty; please insert a new filament."
        },
        {
          "ecode": "1802210000020005",
          "intro": "AMS-HT C Slot 2 filament has run out, and purging the old filament went abnormally; please check whether the filament is stuck in the tool head."
        },
        {
          "ecode": "0700210000020022",
          "intro": "AMS A slot 2 assist motor is stalled，due to excessive resistance in the tube near the toolhead."
        },
        {
          "ecode": "0701220000020024",
          "intro": "AMS B slot 3 failed to rotate the filament spool when pulling filament back to AMS."
        },
        {
          "ecode": "0700700000020004",
          "intro": "Failed to pull back the filament from the toolhead to AMS. Possible cause: filament or spool stuck."
        },
        {
          "ecode": "1807210000030002",
          "intro": "AMS-HT H Slot 2 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "1201220000020006",
          "intro": "Failed to extrude AMS B Slot3 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "1807210000020004",
          "intro": "AMS-HT H Slot 2 filament may be broken in the tool head."
        },
        {
          "ecode": "1806200000020024",
          "intro": "AMS-HT G slot 1 failed to rotate the filament spool when pulling filament back to AMS."
        },
        {
          "ecode": "03000D0000010006",
          "intro": "The build plate is not placed properly. Please adjust it."
        },
        {
          "ecode": "1802220000020008",
          "intro": "AMS-HT C Slot 3 feed-in Hall sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "1201100000020002",
          "intro": "The AMS B Slot1 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "1805560000030001",
          "intro": "AMS-HT F is undergoing dry cooling; please wait for it to cool down before operating."
        },
        {
          "ecode": "0700220000020004",
          "intro": "AMS A Slot 3 filament may be broken in the tool head."
        },
        {
          "ecode": "0705950000010001",
          "intro": "AMS F The temperature sensor of heater 2 is malfunctioning, which may be due to poor connector contact."
        },
        {
          "ecode": "1801210000020018",
          "intro": "AMS-HT B slot 2 assist motor is stalled，due to excessive resistance in the tube near AMS."
        },
        {
          "ecode": "0702210000020019",
          "intro": "AMS C slot 2 assist motor is stalled，due to excessive resistance in the tube between AMS and the filament buffer."
        },
        {
          "ecode": "0702010000010003",
          "intro": "The AMS C assist motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "1201230000020005",
          "intro": "AMS B Slot4 filament has run out, and purging the old filament went abnormally; please check to see if filament is stuck in the toolhead."
        },
        {
          "ecode": "0704220000020005",
          "intro": "AMS E Slot 3 filament has run out, and purging the old filament went abnormally; please check whether the filament is stuck in the tool head."
        },
        {
          "ecode": "1803110000010001",
          "intro": "The AMS-HT D slot 2 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "1801300000010001",
          "intro": "The AMS-HT B RFID 1 board has an error."
        },
        {
          "ecode": "0700010000010004",
          "intro": "The AMS A assist motor speed control is malfunctioning. The speed sensor may be faulty."
        },
        {
          "ecode": "1803220000020009",
          "intro": "Failed to extrude AMS-HT D Slot 3 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "1802220000010084",
          "intro": "Failed to read the filament information from AMS-HT C slot 3. The RFID tag may be damaged or positioned at the edge of the RFID detection device. Please remove 5cm filament and try again."
        },
        {
          "ecode": "0701300000030003",
          "intro": "RFID cannot be read because of a hardware or structural error."
        },
        {
          "ecode": "0703120000020002",
          "intro": "The AMS D slot 3 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "0704210000020002",
          "intro": "AMS E Slot 2 is empty; please insert a new filament."
        },
        {
          "ecode": "0707200000020003",
          "intro": "AMS H Slot 1's filament may be broken in AMS."
        },
        {
          "ecode": "1802200000020008",
          "intro": "AMS-HT C Slot 1 feed-in Hall sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "1801210000010081",
          "intro": "Failed to read the filament information from AMS-HT B slot 2. The AMS main board may be malfunctioning."
        },
        {
          "ecode": "0500020000020001",
          "intro": "Failed to connect to the internet. Please check the network connection."
        },
        {
          "ecode": "1805200000010086",
          "intro": "Failed to read the filament information from AMS-HT F slot 1. The RFID tag cannot rotate due to a jam during the filament loading or unloading. Please pull out the filament and try again."
        },
        {
          "ecode": "1807700000020007",
          "intro": "AMS-HT filament ran out. Please put a new filament into the same slot in AMS and resume."
        },
        {
          "ecode": "1201310000020002",
          "intro": "The RFID-tag on AMS B Slot 2 is damaged."
        },
        {
          "ecode": "1807230000020017",
          "intro": "AMS-HT H slot 4 assist motor is stalled，due to excessive resistance in the tube between AMS and the printer."
        },
        {
          "ecode": "0704120000020004",
          "intro": "AMS E The brushed motor 3 has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "1801200000020022",
          "intro": "AMS-HT B slot 1 assist motor is stalled，due to excessive resistance in the tube near the toolhead."
        },
        {
          "ecode": "0705200000020008",
          "intro": "AMS F Slot 1 feed-in Hall sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "1800210000020019",
          "intro": "AMS-HT A slot 2 assist motor is stalled，due to excessive resistance in the tube between AMS and the filament buffer."
        },
        {
          "ecode": "1804350000010001",
          "intro": "The temperature and humidity sensor has an error. The chip may be faulty."
        },
        {
          "ecode": "0300930000010004",
          "intro": "Chamber temperature is abnormal. The chamber heater's temperature sensor at the air outlet may have an open circuit."
        },
        {
          "ecode": "1802230000010086",
          "intro": "Failed to read the filament information from AMS-HT C slot 4. The RFID tag cannot rotate due to a jam during the filament loading or unloading. Please pull out the filament and try again."
        },
        {
          "ecode": "1805210000020024",
          "intro": "AMS-HT F slot 2 failed to rotate the filament spool when pulling filament back to AMS."
        },
        {
          "ecode": "0700700000020006",
          "intro": "Timeout purging old filament. Possible cause: filament stuck or the extruder/nozzle clog."
        },
        {
          "ecode": "0300020000010003",
          "intro": "The nozzle temperature is abnormal; the heater is over temperature."
        },
        {
          "ecode": "0701100000010001",
          "intro": "The AMS B slot 1 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "0707220000020003",
          "intro": "AMS H Slot 3's filament may be broken in AMS."
        },
        {
          "ecode": "1804230000020004",
          "intro": "AMS-HT E Slot 4 filament may be broken in the tool head."
        },
        {
          "ecode": "0701200000020019",
          "intro": "AMS B slot 1 assist motor is stalled，due to excessive resistance in the tube between AMS and the filament buffer."
        },
        {
          "ecode": "1803930000010001",
          "intro": "AMS-HT D The cooling fan of heater 2 is blocked, which may be due to the fan being stuck."
        },
        {
          "ecode": "0705200000020010",
          "intro": "AMS F slot 1 feeds filament out of AMS timeout."
        },
        {
          "ecode": "0707010000020007",
          "intro": "AMS H The assist motor encoder wires are not connected. The assist motor connector may have poor contact."
        },
        {
          "ecode": "0706230000020019",
          "intro": "AMS G slot 4 assist motor is stalled，due to excessive resistance in the tube between AMS and the filament buffer."
        },
        {
          "ecode": "1806700000020008",
          "intro": "Failed to get AMS mapping table; please select \"Resume\" to retry."
        },
        {
          "ecode": "1800010000020008",
          "intro": "AMS-HT A The assist motor phase winding has an open circuit. The assist motor may be faulty."
        },
        {
          "ecode": "1803220000020022",
          "intro": "AMS-HT D slot 3 assist motor is stalled，due to excessive resistance in the tube near the toolhead."
        },
        {
          "ecode": "0706110000020002",
          "intro": "The AMS G slot 2 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "1806010000020007",
          "intro": "AMS-HT G The assist motor encoder wires are not connected. The assist motor connector may have poor contact."
        },
        {
          "ecode": "0703210000020008",
          "intro": "AMS D Slot 2 feed-in Hall sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "1806300000030003",
          "intro": "RFID cannot be read because of a hardware or structural error."
        },
        {
          "ecode": "0707210000010083",
          "intro": "Failed to read the filament information from AMS H slot 2. The RFID tag may be damaged."
        },
        {
          "ecode": "0500010000030005",
          "intro": "The Micro SD card is in Read-Only mode. Video recording and Timelapse recording cannot be performed. Please refer to the Wiki for assistance."
        },
        {
          "ecode": "0700230000020003",
          "intro": "AMS A Slot 4's filament may be broken in AMS."
        },
        {
          "ecode": "1807010000020009",
          "intro": "AMS-HT H The assist motor has unbalanced tree-phase resistaance. The assist motor may be faulty."
        },
        {
          "ecode": "0702200000010084",
          "intro": "Failed to read the filament information from AMS C slot 1. The RFID tag may be damaged or positioned at the edge of the RFID detection device. Please remove 5cm filament and try again."
        },
        {
          "ecode": "0706230000020024",
          "intro": "AMS G slot 4 failed to rotate the filament spool when pulling filament back to AMS."
        },
        {
          "ecode": "0500050000010001",
          "intro": "The factory data of the AP board is abnormal; please replace the AP board with a new one."
        },
        {
          "ecode": "1805210000010084",
          "intro": "Failed to read the filament information from AMS-HT F slot 2. The RFID tag may be damaged or positioned at the edge of the RFID detection device. Please remove 5cm filament and try again."
        },
        {
          "ecode": "1806230000020011",
          "intro": "AMS-HT G slot 4 pulls filament back to AMS timeout."
        },
        {
          "ecode": "0703210000020017",
          "intro": "AMS D slot 2 assist motor is stalled，due to excessive resistance in the tube between AMS and the printer."
        },
        {
          "ecode": "1802810000010004",
          "intro": "AMS-HT C The heater 2 is heating abnormally."
        },
        {
          "ecode": "1200720000010001",
          "intro": "AMS A Filament speed and length error: The slot 3 filament odometry may be faulty."
        },
        {
          "ecode": "0705220000010086",
          "intro": "Failed to read the filament information from AMS F slot 3. The RFID tag cannot rotate due to a jam during the filament loading or unloading. Please pull out the filament and try again."
        },
        {
          "ecode": "0700010000020002",
          "intro": "The AMS A assist motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "0700210000020008",
          "intro": "AMS A Slot 2 feed-in Hall sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "1806700000020003",
          "intro": "Failed to extrude the filament. Possible cause: extruder or nozzle clog."
        },
        {
          "ecode": "1803210000020003",
          "intro": "AMS-HT D Slot 2's filament may be broken in AMS-HT."
        },
        {
          "ecode": "1806220000020011",
          "intro": "AMS-HT G slot 3 pulls filament back to AMS timeout."
        },
        {
          "ecode": "1802200000020009",
          "intro": "Failed to extrude AMS-HT C Slot 1 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "0707230000010084",
          "intro": "Failed to read the filament information from AMS H slot 4. The RFID tag may be damaged or positioned at the edge of the RFID detection device. Please remove 5cm filament and try again."
        },
        {
          "ecode": "1807010000010011",
          "intro": "AMS-HT H The assist motor calibration parameter error. Please pull out the filament from the filament hub and then restart the AMS."
        },
        {
          "ecode": "1802210000020007",
          "intro": "AMS-HT C Slot 2 feed-out Hall sensor is disconnected. The connector may have poor contact."
        },
        {
          "ecode": "1800230000020021",
          "intro": "AMS-HT A slot 4 assist motor is stalled，due to excessive resistance in the tube between the filament buffer and the toolhead."
        },
        {
          "ecode": "1801200000020008",
          "intro": "AMS-HT B Slot 1 feed-in Hall sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "0704230000020004",
          "intro": "AMS E Slot 4 filament may be broken in the tool head."
        },
        {
          "ecode": "0703910000010003",
          "intro": "AMS D The exhaust valve 2 is not connected, which may be due to poor connector contact."
        },
        {
          "ecode": "0702230000010084",
          "intro": "Failed to read the filament information from AMS C slot 4. The RFID tag may be damaged or positioned at the edge of the RFID detection device. Please remove 5cm filament and try again."
        },
        {
          "ecode": "0700800000010002",
          "intro": "AMS A The heater 1 is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "0707230000020007",
          "intro": "AMS H Slot 4 feed-out Hall sensor is disconnected. The connector may have poor contact."
        },
        {
          "ecode": "0701100000020004",
          "intro": "AMS B The brushed motor 1 has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "1806310000010001",
          "intro": "The AMS-HT G RFID 2 board has an error."
        },
        {
          "ecode": "0703320000020002",
          "intro": "The RFID-tag on AMS D Slot3 is damaged, or its content cannot be identified."
        },
        {
          "ecode": "0702220000020022",
          "intro": "AMS C slot 3 assist motor is stalled，due to excessive resistance in the tube near the toolhead."
        },
        {
          "ecode": "0706220000020007",
          "intro": "AMS G Slot 3 feed-out Hall sensor is disconnected. The connector may have poor contact."
        },
        {
          "ecode": "1806210000020004",
          "intro": "AMS-HT G Slot 2 filament may be broken in the tool head."
        },
        {
          "ecode": "1803110000020002",
          "intro": "The AMS-HT D slot 2 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "0704200000030001",
          "intro": "AMS E Slot 1 filament has run out. Please wait while old filament is purged."
        },
        {
          "ecode": "1804220000020024",
          "intro": "AMS-HT E slot 3 failed to rotate the filament spool when pulling filament back to AMS."
        },
        {
          "ecode": "0701810000010003",
          "intro": "AMS B The heater 2 is short-circuited, which may be due to a wiring short or heater damage."
        },
        {
          "ecode": "0300920000010001",
          "intro": "The temperature of chamber heater 2 is abnormal. The heater may have a short circuit."
        },
        {
          "ecode": "0701700000020005",
          "intro": "Failed to feed the filament outside the AMS. Please clip the end of the filament flat and check to see if the spool is stuck."
        },
        {
          "ecode": "0700210000020009",
          "intro": "Failed to extrude AMS A Slot 2 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "0705230000020008",
          "intro": "AMS F Slot 4 feed-in Hall sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "0704210000020024",
          "intro": "AMS E slot 2 failed to rotate the filament spool when pulling filament back to AMS."
        },
        {
          "ecode": "1202210000020005",
          "intro": "AMS C Slot2 filament has run out, and purging the old filament went abnormally; please check to see if filament is stuck in the toolhead."
        },
        {
          "ecode": "1800130000010001",
          "intro": "The AMS-HT A slot 4 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "0703220000030002",
          "intro": "AMS D Slot 3 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "1202110000010003",
          "intro": "The AMS C Slot2 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "0707210000020007",
          "intro": "AMS H Slot 2 feed-out Hall sensor is disconnected. The connector may have poor contact."
        },
        {
          "ecode": "1803100000010001",
          "intro": "The AMS-HT D slot 1 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "1201100000010001",
          "intro": "The AMS B Slot1 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "0703230000020011",
          "intro": "AMS D slot 4 pulls filament back to AMS timeout."
        },
        {
          "ecode": "0702230000020021",
          "intro": "AMS C slot 4 assist motor is stalled，due to excessive resistance in the tube between the filament buffer and the toolhead."
        },
        {
          "ecode": "03000B0000010005",
          "intro": "Force sensor 2 detected unexpected continuous force. The heatbed may be stuck, or the analog front end may be broken."
        },
        {
          "ecode": "1803220000020001",
          "intro": "AMS-HT D Slot 3 filament has run out. Please insert a new filament."
        },
        {
          "ecode": "0300910000010002",
          "intro": "The temperature of chamber heater 1 is abnormal. The heater may have an open circuit or the thermal fuse may have burned out."
        },
        {
          "ecode": "1805130000020002",
          "intro": "The AMS-HT F slot 4 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "1202210000030002",
          "intro": "AMS C Slot2 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "1805130000010003",
          "intro": "The AMS-HT F slot 4 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "0703220000010086",
          "intro": "Failed to read the filament information from AMS D slot 3. The RFID tag cannot rotate due to a jam during the filament loading or unloading. Please pull out the filament and try again."
        },
        {
          "ecode": "0707230000020011",
          "intro": "AMS H slot 4 pulls filament back to AMS timeout."
        },
        {
          "ecode": "1806200000030002",
          "intro": "AMS-HT G Slot 1 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "0705800000010002",
          "intro": "AMS F The heater 1 is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "1804210000010086",
          "intro": "Failed to read the filament information from AMS-HT E slot 2. The RFID tag cannot rotate due to a jam during the filament loading or unloading. Please pull out the filament and try again."
        },
        {
          "ecode": "0707210000020021",
          "intro": "AMS H slot 2 assist motor is stalled，due to excessive resistance in the tube between the filament buffer and the toolhead."
        },
        {
          "ecode": "1806200000010085",
          "intro": "Failed to read the filament information from AMS-HT G slot 1. RFID tag verification failed. You can try to use Bambu Lab filament."
        },
        {
          "ecode": "1807210000010081",
          "intro": "Failed to read the filament information from AMS-HT H slot 2. The AMS main board may be malfunctioning."
        },
        {
          "ecode": "0700200000030001",
          "intro": "AMS A Slot 1 filament has run out. Please wait while old filament is purged."
        },
        {
          "ecode": "1807200000030001",
          "intro": "AMS-HT H Slot 1 filament has run out. Please wait while old filament is purged."
        },
        {
          "ecode": "1801220000020011",
          "intro": "AMS-HT B slot 3 pulls filament back to AMS timeout."
        },
        {
          "ecode": "0706220000020010",
          "intro": "AMS G slot 3 feeds filament out of AMS timeout."
        },
        {
          "ecode": "0707210000020009",
          "intro": "Failed to extrude AMS H Slot 2 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "1807920000010001",
          "intro": "AMS-HT H The cooling fan of heater 1 is blocked, which may be due to the fan being stuck."
        },
        {
          "ecode": "0705230000010086",
          "intro": "Failed to read the filament information from AMS F slot 4. The RFID tag cannot rotate due to a jam during the filament loading or unloading. Please pull out the filament and try again."
        },
        {
          "ecode": "0703210000020011",
          "intro": "AMS D slot 2 pulls filament back to AMS timeout."
        },
        {
          "ecode": "1202230000020005",
          "intro": "AMS C Slot4 filament has run out, and purging the old filament went abnormally; please check to see if filament is stuck in the toolhead."
        },
        {
          "ecode": "1807220000020009",
          "intro": "Failed to extrude AMS-HT H Slot 3 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "0707700000020002",
          "intro": "Failed to feed the filament into the toolhead. Possible cause: filament or spool stuck."
        },
        {
          "ecode": "1806210000020005",
          "intro": "AMS-HT G Slot 2 filament has run out, and purging the old filament went abnormally; please check whether the filament is stuck in the tool head."
        },
        {
          "ecode": "0702700000020007",
          "intro": "AMS filament ran out. Please put a new filament into the same slot in AMS and resume."
        },
        {
          "ecode": "1804940000010001",
          "intro": "AMS-HT E The temperature sensor of heater 1 is malfunctioning, which may be due to poor connector contact."
        },
        {
          "ecode": "1807350000010001",
          "intro": "The temperature and humidity sensor has an error. The chip may be faulty."
        },
        {
          "ecode": "1201120000010003",
          "intro": "The AMS B Slot3 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "0701200000020018",
          "intro": "AMS B slot 1 assist motor is stalled，due to excessive resistance in the tube near AMS."
        },
        {
          "ecode": "1802800000010002",
          "intro": "AMS-HT C The heater 1 is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "1807020000010001",
          "intro": "AMS-HT H Filament speed and length error: The filament odometry may be faulty."
        },
        {
          "ecode": "1203320000010001",
          "intro": "AMS D Slot 3 RFID coil is broken or the RF hardware circuit has an error."
        },
        {
          "ecode": "0703210000010083",
          "intro": "Failed to read the filament information from AMS D slot 2. The RFID tag may be damaged."
        },
        {
          "ecode": "0703210000020010",
          "intro": "AMS D slot 2 feeds filament out of AMS timeout."
        },
        {
          "ecode": "0700230000020009",
          "intro": "Failed to extrude AMS A Slot 4 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "1806210000020021",
          "intro": "AMS-HT G slot 2 assist motor is stalled，due to excessive resistance in the tube between the filament buffer and the toolhead."
        },
        {
          "ecode": "1801010000010004",
          "intro": "The AMS-HT B assist motor speed control is malfunctioning. The speed sensor may be faulty."
        },
        {
          "ecode": "0700220000030002",
          "intro": "AMS A Slot 3 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "1805700000020008",
          "intro": "Failed to get AMS mapping table; please select \"Resume\" to retry."
        },
        {
          "ecode": "1200310000020002",
          "intro": "The RFID-tag on AMS A Slot 2 is damaged."
        },
        {
          "ecode": "0707200000030002",
          "intro": "AMS H Slot 1 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "0701940000010001",
          "intro": "AMS B The temperature sensor of heater 1 is malfunctioning, which may be due to poor connector contact."
        },
        {
          "ecode": "0704220000020019",
          "intro": "AMS E slot 3 assist motor is stalled，due to excessive resistance in the tube between AMS and the filament buffer."
        },
        {
          "ecode": "1801210000020003",
          "intro": "AMS-HT B Slot 2's filament may be broken in AMS-HT."
        },
        {
          "ecode": "1807810000010004",
          "intro": "AMS-HT H The heater 2 is heating abnormally."
        },
        {
          "ecode": "0701200000020008",
          "intro": "AMS B Slot 1 feed-in Hall sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "1802220000020007",
          "intro": "AMS-HT C Slot 3 feed-out Hall sensor is disconnected. The connector may have poor contact."
        },
        {
          "ecode": "0705220000020011",
          "intro": "AMS F slot 3 pulls filament back to AMS timeout."
        },
        {
          "ecode": "1804800000010001",
          "intro": "AMS-HT E The current sensor of heater 1 is abnormal."
        },
        {
          "ecode": "1806230000010086",
          "intro": "Failed to read the filament information from AMS-HT G slot 4. The RFID tag cannot rotate due to a jam during the filament loading or unloading. Please pull out the filament and try again."
        },
        {
          "ecode": "1804970000030001",
          "intro": "AMS-HT E chamber temperature is too high; auxiliary feeding or RFID reading is currently not allowed."
        },
        {
          "ecode": "1200220000020004",
          "intro": "AMS A Slot3 filament may be broken in the tool head."
        },
        {
          "ecode": "0707110000010003",
          "intro": "The AMS H slot 2 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "0704560000030001",
          "intro": "AMS E is undergoing dry cooling; please wait for it to cool down before operating."
        },
        {
          "ecode": "0706900000020001",
          "intro": "AMS G The operation of the exhaust valve 1 is abnormal, which may be due to excessive resistance."
        },
        {
          "ecode": "0C00020000020006",
          "intro": "Nozzle height seems to be too high. Please check if there is residual filament attached to the nozzle."
        },
        {
          "ecode": "1807200000020024",
          "intro": "AMS-HT H slot 1 failed to rotate the filament spool when pulling filament back to AMS."
        },
        {
          "ecode": "1200220000020006",
          "intro": "Failed to extrude AMS A Slot3 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "1801200000020007",
          "intro": "AMS-HT B Slot 1 feed-out Hall sensor is disconnected. The connector may have poor contact."
        },
        {
          "ecode": "1802200000010085",
          "intro": "Failed to read the filament information from AMS-HT C slot 1. RFID tag verification failed. You can try to use Bambu Lab filament."
        },
        {
          "ecode": "0707230000020010",
          "intro": "AMS H slot 4 feeds filament out of AMS timeout."
        },
        {
          "ecode": "1805010000010011",
          "intro": "AMS-HT F The assist motor calibration parameter error. Please pull out the filament from the filament hub and then restart the AMS."
        },
        {
          "ecode": "1802220000020018",
          "intro": "AMS-HT C slot 3 assist motor is stalled，due to excessive resistance in the tube near AMS."
        },
        {
          "ecode": "0704130000010003",
          "intro": "The AMS E slot 4 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "1800230000030002",
          "intro": "AMS-HT A Slot 4 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "1804910000010003",
          "intro": "AMS-HT E The exhaust valve 2 is not connected, which may be due to poor connector contact."
        },
        {
          "ecode": "0701230000010081",
          "intro": "Failed to read the filament information from AMS B slot 4. The AMS main board may be malfunctioning."
        },
        {
          "ecode": "1804200000020007",
          "intro": "AMS-HT E Slot 1 feed-out Hall sensor is disconnected. The connector may have poor contact."
        },
        {
          "ecode": "1801800000010003",
          "intro": "AMS-HT B The heater 1 is short-circuited, which may be due to a wiring short or heater damage."
        },
        {
          "ecode": "0705210000010086",
          "intro": "Failed to read the filament information from AMS F slot 2. The RFID tag cannot rotate due to a jam during the filament loading or unloading. Please pull out the filament and try again."
        },
        {
          "ecode": "0704810000010003",
          "intro": "AMS E The heater 2 is short-circuited, which may be due to a wiring short or heater damage."
        },
        {
          "ecode": "0707220000020008",
          "intro": "AMS H Slot 3 feed-in Hall sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "0701220000020017",
          "intro": "AMS B slot 3 assist motor is stalled，due to excessive resistance in the tube between AMS and the printer."
        },
        {
          "ecode": "0706210000020017",
          "intro": "AMS G slot 2 assist motor is stalled，due to excessive resistance in the tube between AMS and the printer."
        },
        {
          "ecode": "0705120000010001",
          "intro": "The AMS F slot 3 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "12FF200000020001",
          "intro": "Filament at the spool holder has run out; please insert a new filament."
        },
        {
          "ecode": "0702220000010081",
          "intro": "Failed to read the filament information from AMS C slot 3. The AMS main board may be malfunctioning."
        },
        {
          "ecode": "0700220000010081",
          "intro": "Failed to read the filament information from AMS A slot 3. The AMS main board may be malfunctioning."
        },
        {
          "ecode": "0702920000020002",
          "intro": "AMS C The cooling fan speed of heater 1 is too low, which could be due to excessive fan resistance."
        },
        {
          "ecode": "0300170000010001",
          "intro": "The hotend cooling fan speed is too slow or stopped. It may be stuck or the connector may not be plugged in properly."
        },
        {
          "ecode": "1806700000020005",
          "intro": "Failed to feed the filament outside the AMS-HT. Please clip the end of the filament flat and check to see if the spool is stuck."
        },
        {
          "ecode": "1807240000020009",
          "intro": "AMS-HT H front cover is open. This may affect the drying performance or cause the filament to absorb moisture."
        },
        {
          "ecode": "0706810000010004",
          "intro": "AMS G The heater 2 is heating abnormally."
        },
        {
          "ecode": "0701700000020007",
          "intro": "AMS filament ran out. Please put a new filament into the same slot in AMS and resume."
        },
        {
          "ecode": "0701010000020008",
          "intro": "AMS B The assist motor phase winding has an open circuit. The assist motor may be faulty."
        },
        {
          "ecode": "0700210000020005",
          "intro": "AMS A Slot 2 filament has run out, and purging the old filament went abnormally; please check whether the filament is stuck in the tool head."
        },
        {
          "ecode": "0704940000010001",
          "intro": "AMS E The temperature sensor of heater 1 is malfunctioning, which may be due to poor connector contact."
        },
        {
          "ecode": "050004000002001C",
          "intro": "The RFID-tag on AMS D Slot1 cannot be identified."
        },
        {
          "ecode": "1800300000030003",
          "intro": "RFID cannot be read because of a hardware or structural error."
        },
        {
          "ecode": "1805910000010003",
          "intro": "AMS-HT F The exhaust valve 2 is not connected, which may be due to poor connector contact."
        },
        {
          "ecode": "0707210000030002",
          "intro": "AMS H Slot 2 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "0700210000010086",
          "intro": "Failed to read the filament information from AMS A slot 2. The RFID tag cannot rotate due to a jam during the filament loading or unloading. Please pull out the filament and try again."
        },
        {
          "ecode": "0700230000020019",
          "intro": "AMS A slot 4 assist motor is stalled，due to excessive resistance in the tube between AMS and the filament buffer."
        },
        {
          "ecode": "0700200000020011",
          "intro": "AMS A slot 1 pulls filament back to AMS timeout."
        },
        {
          "ecode": "1800810000010004",
          "intro": "AMS-HT A The heater 2 is heating abnormally."
        },
        {
          "ecode": "1801010000010005",
          "intro": "AMS-HT B The current sensor of assist motor may be faulty."
        },
        {
          "ecode": "0702810000010002",
          "intro": "AMS C The heater 2 is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "0705210000020019",
          "intro": "AMS F slot 2 assist motor is stalled，due to excessive resistance in the tube between AMS and the filament buffer."
        },
        {
          "ecode": "1807200000020001",
          "intro": "AMS-HT H Slot 1 filament has run out. Please insert a new filament."
        },
        {
          "ecode": "1805020000020002",
          "intro": "AMS-HT F The odometer has no signal. The odometer connector may have poor contact."
        },
        {
          "ecode": "0707230000020021",
          "intro": "AMS H slot 4 assist motor is stalled，due to excessive resistance in the tube between the filament buffer and the toolhead."
        },
        {
          "ecode": "0704210000020017",
          "intro": "AMS E slot 2 assist motor is stalled，due to excessive resistance in the tube between AMS and the printer."
        },
        {
          "ecode": "1802230000020011",
          "intro": "AMS-HT C slot 4 pulls filament back to AMS timeout."
        },
        {
          "ecode": "1804220000010081",
          "intro": "Failed to read the filament information from AMS-HT E slot 3. The AMS main board may be malfunctioning."
        },
        {
          "ecode": "1806300000010004",
          "intro": "Encryption chip failure"
        },
        {
          "ecode": "1203230000020002",
          "intro": "AMS D Slot 4 is empty; please insert a new filament."
        },
        {
          "ecode": "1801230000010083",
          "intro": "Failed to read the filament information from AMS-HT B slot 4. The RFID tag may be damaged."
        },
        {
          "ecode": "1803230000010081",
          "intro": "Failed to read the filament information from AMS-HT D slot 4. The AMS main board may be malfunctioning."
        },
        {
          "ecode": "0706010000020006",
          "intro": "AMS G The assist motor three-phase wires are not connected. The assist motor connector may have poor contact."
        },
        {
          "ecode": "1803200000020001",
          "intro": "AMS-HT D Slot 1 filament has run out. Please insert a new filament."
        },
        {
          "ecode": "1807110000020002",
          "intro": "The AMS-HT H slot 2 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "1203310000010001",
          "intro": "AMS D Slot 2 RFID coil is broken or the RF hardware circuit has an error."
        },
        {
          "ecode": "0705700000020006",
          "intro": "Timeout purging old filament. Possible cause: filament stuck or the extruder/nozzle clog."
        },
        {
          "ecode": "0706800000010003",
          "intro": "AMS G The heater 1 is short-circuited, which may be due to a wiring short or heater damage."
        },
        {
          "ecode": "1802930000020002",
          "intro": "AMS-HT C The cooling fan speed of heater 2 is too low, which could be due to excessive fan resistance."
        },
        {
          "ecode": "1203300000030003",
          "intro": "AMS D Slot1 RFID cannot be read because of a structural error."
        },
        {
          "ecode": "1800210000020009",
          "intro": "Failed to extrude AMS-HT A Slot 2 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "0707800000010001",
          "intro": "AMS H The current sensor of heater 1 is abnormal."
        },
        {
          "ecode": "1801800000010004",
          "intro": "AMS-HT B The heater 1 is heating abnormally."
        },
        {
          "ecode": "0701230000010085",
          "intro": "Failed to read the filament information from AMS B slot 4. RFID tag verification failed. You can try to use Bambu Lab filament."
        },
        {
          "ecode": "0706100000020002",
          "intro": "The AMS G slot 1 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "0705010000010004",
          "intro": "The AMS F assist motor speed control is malfunctioning. The speed sensor may be faulty."
        },
        {
          "ecode": "1804210000020009",
          "intro": "Failed to extrude AMS-HT E Slot 2 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "0707300000010004",
          "intro": "Encryption chip failure"
        },
        {
          "ecode": "1203200000030001",
          "intro": "AMS D Slot1 filament has run out. Purging the old filament; please wait."
        },
        {
          "ecode": "0706230000020021",
          "intro": "AMS G slot 4 assist motor is stalled，due to excessive resistance in the tube between the filament buffer and the toolhead."
        },
        {
          "ecode": "1806960000010003",
          "intro": "AMS-HT G Unable to start drying; please pull out the filament from filament hub and try again."
        },
        {
          "ecode": "1806010000020010",
          "intro": "AMS-HT G The assist motor resistance is abnormal. The assist motor may be faulty."
        },
        {
          "ecode": "1804230000010083",
          "intro": "Failed to read the filament information from AMS-HT E slot 4. The RFID tag may be damaged."
        },
        {
          "ecode": "0707200000020022",
          "intro": "AMS H slot 1 assist motor is stalled，due to excessive resistance in the tube near the toolhead."
        },
        {
          "ecode": "050004000002001B",
          "intro": "The RFID-tag on AMS C Slot4 cannot be identified."
        },
        {
          "ecode": "0707200000020018",
          "intro": "AMS H slot 1 assist motor is stalled，due to excessive resistance in the tube near AMS."
        },
        {
          "ecode": "1804200000020011",
          "intro": "AMS-HT E slot 1 pulls filament back to AMS timeout."
        },
        {
          "ecode": "1800230000030001",
          "intro": "AMS-HT A Slot 4 filament has run out. Please wait while old filament is purged."
        },
        {
          "ecode": "0700300000010001",
          "intro": "The AMS A RFID 1 board has an error."
        },
        {
          "ecode": "0706210000020009",
          "intro": "Failed to extrude AMS G Slot 2 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "1803230000020005",
          "intro": "AMS-HT D Slot 4 filament has run out, and purging the old filament went abnormally; please check whether the filament is stuck in the tool head."
        },
        {
          "ecode": "1200220000020001",
          "intro": "AMS A Slot3 filament has run out; please insert a new filament."
        },
        {
          "ecode": "03000D000001000B",
          "intro": "The Z axis motor seems to be stuck when moving. Please check if there is any foreign matter on the Z sliders or Z timing belt wheels."
        },
        {
          "ecode": "0702220000020005",
          "intro": "AMS C Slot 3 filament has run out, and purging the old filament went abnormally; please check whether the filament is stuck in the tool head."
        },
        {
          "ecode": "0300910000010003",
          "intro": "The temperature of chamber heater 1 is abnormal. The heater is over temperature."
        },
        {
          "ecode": "0704010000010004",
          "intro": "The AMS E assist motor speed control is malfunctioning. The speed sensor may be faulty."
        },
        {
          "ecode": "1807200000020007",
          "intro": "AMS-HT H Slot 1 feed-out Hall sensor is disconnected. The connector may have poor contact."
        },
        {
          "ecode": "0707210000020024",
          "intro": "AMS H slot 2 failed to rotate the filament spool when pulling filament back to AMS."
        },
        {
          "ecode": "0701210000030002",
          "intro": "AMS B Slot 2 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "0704210000010083",
          "intro": "Failed to read the filament information from AMS E slot 2. The RFID tag may be damaged."
        },
        {
          "ecode": "0707200000020008",
          "intro": "AMS H Slot 1 feed-in Hall sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "0701200000010084",
          "intro": "Failed to read the filament information from AMS B slot 1. The RFID tag may be damaged or positioned at the edge of the RFID detection device. Please remove 5cm filament and try again."
        },
        {
          "ecode": "1203320000030003",
          "intro": "AMS D Slot3 RFID cannot be read because of a structural error."
        },
        {
          "ecode": "0500010000030007",
          "intro": "Unable to record time-lapse photography without MicroSD card inserted."
        },
        {
          "ecode": "1805210000020020",
          "intro": "AMS-HT F slot 2 assist motor is stalled，due to excessive resistance in the tube near the filament buffer。"
        },
        {
          "ecode": "0706700000020005",
          "intro": "Failed to feed the filament outside the AMS. Please clip the end of the filament flat and check to see if the spool is stuck."
        },
        {
          "ecode": "1803120000010001",
          "intro": "The AMS-HT D slot 3 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "0701220000020011",
          "intro": "AMS B slot 3 pulls filament back to AMS timeout."
        },
        {
          "ecode": "0500030000020020",
          "intro": "Micro SD Card capacity is insufficient to cache print files."
        },
        {
          "ecode": "1800230000020002",
          "intro": "AMS-HT A Slot 4 is empty; please insert a new filament."
        },
        {
          "ecode": "1806200000020020",
          "intro": "AMS-HT G slot 1 assist motor is stalled，due to excessive resistance in the tube near the filament buffer。"
        },
        {
          "ecode": "1202120000010001",
          "intro": "The AMS C Slot3 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "0702310000030003",
          "intro": "RFID cannot be read because of a hardware or structural error."
        },
        {
          "ecode": "1800220000010086",
          "intro": "Failed to read the filament information from AMS-HT A slot 3. The RFID tag cannot rotate due to a jam during the filament loading or unloading. Please pull out the filament and try again."
        },
        {
          "ecode": "1800100000020004",
          "intro": "AMS-HT A The brushed motor 1 has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "0706230000020005",
          "intro": "AMS G Slot 4 filament has run out, and purging the old filament went abnormally; please check whether the filament is stuck in the tool head."
        },
        {
          "ecode": "1800200000010083",
          "intro": "Failed to read the filament information from AMS-HT A slot 1. The RFID tag may be damaged."
        },
        {
          "ecode": "0701230000030002",
          "intro": "AMS B Slot 4 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "1806220000020022",
          "intro": "AMS-HT G slot 3 assist motor is stalled，due to excessive resistance in the tube near the toolhead."
        },
        {
          "ecode": "0704220000020011",
          "intro": "AMS E slot 3 pulls filament back to AMS timeout."
        },
        {
          "ecode": "0706200000010086",
          "intro": "Failed to read the filament information from AMS G slot 1. The RFID tag cannot rotate due to a jam during the filament loading or unloading. Please pull out the filament and try again."
        },
        {
          "ecode": "1807220000020017",
          "intro": "AMS-HT H slot 3 assist motor is stalled，due to excessive resistance in the tube between AMS and the printer."
        },
        {
          "ecode": "1800230000020003",
          "intro": "AMS-HT A Slot 4's filament may be broken in AMS-HT."
        },
        {
          "ecode": "1807200000020019",
          "intro": "AMS-HT H slot 1 assist motor is stalled，due to excessive resistance in the tube between AMS and the filament buffer."
        },
        {
          "ecode": "0707950000010001",
          "intro": "AMS H The temperature sensor of heater 2 is malfunctioning, which may be due to poor connector contact."
        },
        {
          "ecode": "1802220000020021",
          "intro": "AMS-HT C slot 3 assist motor is stalled，due to excessive resistance in the tube between the filament buffer and the toolhead."
        },
        {
          "ecode": "1806100000010001",
          "intro": "The AMS-HT G slot 1 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "0702700000020005",
          "intro": "Failed to feed the filament outside the AMS. Please clip the end of the filament flat and check to see if the spool is stuck."
        },
        {
          "ecode": "1201500000020001",
          "intro": "AMS B communication is abnormal; please check the connection cable."
        },
        {
          "ecode": "0705310000020002",
          "intro": "The RFID-tag on AMS F Slot2 is damaged, or its content cannot be identified."
        },
        {
          "ecode": "0706230000010084",
          "intro": "Failed to read the filament information from AMS G slot 4. The RFID tag may be damaged or positioned at the edge of the RFID detection device. Please remove 5cm filament and try again."
        },
        {
          "ecode": "0706200000020003",
          "intro": "AMS G Slot 1's filament may be broken in AMS."
        },
        {
          "ecode": "1803230000020010",
          "intro": "AMS-HT D slot 4 feeds filament out of AMS timeout."
        },
        {
          "ecode": "0706200000020008",
          "intro": "AMS G Slot 1 feed-in Hall sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "0704010000020010",
          "intro": "AMS E The assist motor resistance is abnormal. The assist motor may be faulty."
        },
        {
          "ecode": "0702700000020004",
          "intro": "Failed to pull back the filament from the toolhead to AMS. Possible cause: filament or spool stuck."
        },
        {
          "ecode": "1805010000010001",
          "intro": "The AMS-HT F assist motor has slipped. The extrusion wheel may be worn down, or the filament may be too thin."
        },
        {
          "ecode": "1807200000010086",
          "intro": "Failed to read the filament information from AMS-HT H slot 1. The RFID tag cannot rotate due to a jam during the filament loading or unloading. Please pull out the filament and try again."
        },
        {
          "ecode": "1807210000020003",
          "intro": "AMS-HT H Slot 2's filament may be broken in AMS-HT."
        },
        {
          "ecode": "0705200000020003",
          "intro": "AMS F Slot 1's filament may be broken in AMS."
        },
        {
          "ecode": "1800210000020022",
          "intro": "AMS-HT A slot 2 assist motor is stalled，due to excessive resistance in the tube near the toolhead."
        },
        {
          "ecode": "0707230000030002",
          "intro": "AMS H Slot 4 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "1803200000020022",
          "intro": "AMS-HT D slot 1 assist motor is stalled，due to excessive resistance in the tube near the toolhead."
        },
        {
          "ecode": "1802210000010083",
          "intro": "Failed to read the filament information from AMS-HT C slot 2. The RFID tag may be damaged."
        },
        {
          "ecode": "050004000002001F",
          "intro": "The RFID-tag on AMS D Slot4 cannot be identified."
        },
        {
          "ecode": "1801230000020002",
          "intro": "AMS-HT B Slot 4 is empty; please insert a new filament."
        },
        {
          "ecode": "1802230000020024",
          "intro": "AMS-HT C slot 4 failed to rotate the filament spool when pulling filament back to AMS."
        },
        {
          "ecode": "0700200000020020",
          "intro": "AMS A slot 1 assist motor is stalled，due to excessive resistance in the tube near the filament buffer。"
        },
        {
          "ecode": "0703230000020001",
          "intro": "AMS D Slot 4 filament has run out. Please insert a new filament."
        },
        {
          "ecode": "1806220000020021",
          "intro": "AMS-HT G slot 3 assist motor is stalled，due to excessive resistance in the tube between the filament buffer and the toolhead."
        },
        {
          "ecode": "0702800000010004",
          "intro": "AMS C The heater 1 is heating abnormally."
        },
        {
          "ecode": "0704200000010084",
          "intro": "Failed to read the filament information from AMS E slot 1. The RFID tag may be damaged or positioned at the edge of the RFID detection device. Please remove 5cm filament and try again."
        },
        {
          "ecode": "0706210000010083",
          "intro": "Failed to read the filament information from AMS G slot 2. The RFID tag may be damaged."
        },
        {
          "ecode": "0706200000010085",
          "intro": "Failed to read the filament information from AMS G slot 1. RFID tag verification failed. You can try to use Bambu Lab filament."
        },
        {
          "ecode": "0704200000020009",
          "intro": "Failed to extrude AMS E Slot 1 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "1802110000020004",
          "intro": "AMS-HT C The brushed motor 2 has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "1802210000020022",
          "intro": "AMS-HT C slot 2 assist motor is stalled，due to excessive resistance in the tube near the toolhead."
        },
        {
          "ecode": "1804020000010001",
          "intro": "AMS-HT E Filament speed and length error: The filament odometry may be faulty."
        },
        {
          "ecode": "1801210000020002",
          "intro": "AMS-HT B Slot 2 is empty; please insert a new filament."
        },
        {
          "ecode": "1801300000030003",
          "intro": "RFID cannot be read because of a hardware or structural error."
        },
        {
          "ecode": "0702970000030001",
          "intro": "AMS C chamber temperature is too high; auxiliary feeding or RFID reading is currently not allowed."
        },
        {
          "ecode": "0500040000010004",
          "intro": "The print file is unauthorized."
        },
        {
          "ecode": "0702210000020001",
          "intro": "AMS C Slot 2 filament has run out. Please insert a new filament."
        },
        {
          "ecode": "0300940000030002",
          "intro": "Chamber temperature setting value exceed the limit, the boundary value will be set."
        },
        {
          "ecode": "0703800000010002",
          "intro": "AMS D The heater 1 is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "1804200000020019",
          "intro": "AMS-HT E slot 1 assist motor is stalled，due to excessive resistance in the tube between AMS and the filament buffer."
        },
        {
          "ecode": "1804110000020002",
          "intro": "The AMS-HT E slot 2 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "1806200000020003",
          "intro": "AMS-HT G Slot 1's filament may be broken in AMS-HT."
        },
        {
          "ecode": "0707210000010085",
          "intro": "Failed to read the filament information from AMS H slot 2. RFID tag verification failed. You can try to use Bambu Lab filament."
        },
        {
          "ecode": "1807220000010085",
          "intro": "Failed to read the filament information from AMS-HT H slot 3. RFID tag verification failed. You can try to use Bambu Lab filament."
        },
        {
          "ecode": "0705220000020003",
          "intro": "AMS F Slot 3's filament may be broken in AMS."
        },
        {
          "ecode": "1802230000020008",
          "intro": "AMS-HT C Slot 4 feed-in Hall sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "0705100000010001",
          "intro": "The AMS F slot 1 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "0500030000010025",
          "intro": "The current firmware is abnormal. Please update again."
        },
        {
          "ecode": "1201230000020003",
          "intro": "AMS B Slot4 filament may be broken in the PTFE tube."
        },
        {
          "ecode": "1800120000010003",
          "intro": "The AMS-HT A slot 3 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "0700700000020002",
          "intro": "Failed to feed the filament into the toolhead. Possible cause: filament or spool stuck."
        },
        {
          "ecode": "0700210000010083",
          "intro": "Failed to read the filament information from AMS A slot 2. The RFID tag may be damaged."
        },
        {
          "ecode": "1802220000010086",
          "intro": "Failed to read the filament information from AMS-HT C slot 3. The RFID tag cannot rotate due to a jam during the filament loading or unloading. Please pull out the filament and try again."
        },
        {
          "ecode": "0500020000020003",
          "intro": "Failed to connect to the internet; please check the network connection."
        },
        {
          "ecode": "1801220000030001",
          "intro": "AMS-HT B Slot 3 filament has run out. Please wait while old filament is purged."
        },
        {
          "ecode": "0700110000010003",
          "intro": "The AMS A slot 2 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "0702010000020002",
          "intro": "The AMS C assist motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "1800230000010086",
          "intro": "Failed to read the filament information from AMS-HT A slot 4. The RFID tag cannot rotate due to a jam during the filament loading or unloading. Please pull out the filament and try again."
        },
        {
          "ecode": "0704810000010004",
          "intro": "AMS E The heater 2 is heating abnormally."
        },
        {
          "ecode": "1802200000020005",
          "intro": "AMS-HT C Slot 1 filament has run out, and purging the old filament went abnormally; please check whether the filament is stuck in the tool head."
        },
        {
          "ecode": "1803200000010086",
          "intro": "Failed to read the filament information from AMS-HT D slot 1. The RFID tag cannot rotate due to a jam during the filament loading or unloading. Please pull out the filament and try again."
        },
        {
          "ecode": "0705810000010004",
          "intro": "AMS F The heater 2 is heating abnormally."
        },
        {
          "ecode": "0703210000030002",
          "intro": "AMS D Slot 2 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "1800220000010083",
          "intro": "Failed to read the filament information from AMS-HT A slot 3. The RFID tag may be damaged."
        },
        {
          "ecode": "0707220000020010",
          "intro": "AMS H slot 3 feeds filament out of AMS timeout."
        },
        {
          "ecode": "0701220000020018",
          "intro": "AMS B slot 3 assist motor is stalled，due to excessive resistance in the tube near AMS."
        },
        {
          "ecode": "0705200000020020",
          "intro": "AMS F slot 1 assist motor is stalled，due to excessive resistance in the tube near the filament buffer。"
        },
        {
          "ecode": "1806230000020007",
          "intro": "AMS-HT G Slot 4 feed-out Hall sensor is disconnected. The connector may have poor contact."
        },
        {
          "ecode": "0707210000020008",
          "intro": "AMS H Slot 2 feed-in Hall sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "1203310000020002",
          "intro": "The RFID-tag on AMS D Slot 2 is damaged."
        },
        {
          "ecode": "0702930000020002",
          "intro": "AMS C The cooling fan speed of heater 2 is too low, which could be due to excessive fan resistance."
        },
        {
          "ecode": "1801910000010003",
          "intro": "AMS-HT B The exhaust valve 2 is not connected, which may be due to poor connector contact."
        },
        {
          "ecode": "1804810000010004",
          "intro": "AMS-HT E The heater 2 is heating abnormally."
        },
        {
          "ecode": "0702220000020003",
          "intro": "AMS C Slot 3's filament may be broken in AMS."
        },
        {
          "ecode": "0707010000010011",
          "intro": "AMS H The assist motor calibration parameter error. Please pull out the filament from the filament hub and then restart the AMS."
        },
        {
          "ecode": "1803920000010001",
          "intro": "AMS-HT D The cooling fan of heater 1 is blocked, which may be due to the fan being stuck."
        },
        {
          "ecode": "1804210000020002",
          "intro": "AMS-HT E Slot 2 is empty; please insert a new filament."
        },
        {
          "ecode": "0701220000010084",
          "intro": "Failed to read the filament information from AMS B slot 3. The RFID tag may be damaged or positioned at the edge of the RFID detection device. Please remove 5cm filament and try again."
        },
        {
          "ecode": "1807210000020021",
          "intro": "AMS-HT H slot 2 assist motor is stalled，due to excessive resistance in the tube between the filament buffer and the toolhead."
        },
        {
          "ecode": "0703330000020002",
          "intro": "The RFID-tag on AMS D Slot4 is damaged, or its content cannot be identified."
        },
        {
          "ecode": "0706300000030003",
          "intro": "RFID cannot be read because of a hardware or structural error."
        },
        {
          "ecode": "0C0001000001000B",
          "intro": "Failed to calibrate Micro Lidar. Please make sure the calibration chart is clean and not obscured. Then, run machine calibration again."
        },
        {
          "ecode": "1202810000020001",
          "intro": "AMS C Slot2 filament may be tangled or stuck."
        },
        {
          "ecode": "1805810000010004",
          "intro": "AMS-HT F The heater 2 is heating abnormally."
        },
        {
          "ecode": "0701200000020017",
          "intro": "AMS B slot 1 assist motor is stalled，due to excessive resistance in the tube between AMS and the printer."
        },
        {
          "ecode": "0703300000030003",
          "intro": "RFID cannot be read because of a hardware or structural error."
        },
        {
          "ecode": "0701120000010001",
          "intro": "The AMS B slot 3 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "1805230000020017",
          "intro": "AMS-HT F slot 4 assist motor is stalled，due to excessive resistance in the tube between AMS and the printer."
        },
        {
          "ecode": "0707220000020019",
          "intro": "AMS H slot 3 assist motor is stalled，due to excessive resistance in the tube between AMS and the filament buffer."
        },
        {
          "ecode": "1805350000010002",
          "intro": "AMS-HT F The humidity sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "0701210000020021",
          "intro": "AMS B slot 2 assist motor is stalled，due to excessive resistance in the tube between the filament buffer and the toolhead."
        },
        {
          "ecode": "1806200000030001",
          "intro": "AMS-HT G Slot 1 filament has run out. Please wait while old filament is purged."
        },
        {
          "ecode": "0702200000020003",
          "intro": "AMS C Slot 1's filament may be broken in AMS."
        },
        {
          "ecode": "1805230000020011",
          "intro": "AMS-HT F slot 4 pulls filament back to AMS timeout."
        },
        {
          "ecode": "18FF200000020004",
          "intro": "Please pull the external filament from the extruder."
        },
        {
          "ecode": "0706130000020004",
          "intro": "AMS G The brushed motor 4 has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "1201230000020006",
          "intro": "Failed to extrude AMS B Slot4 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "0700930000020002",
          "intro": "AMS A The cooling fan speed of heater 2 is too low, which could be due to excessive fan resistance."
        },
        {
          "ecode": "0701210000020017",
          "intro": "AMS B slot 2 assist motor is stalled，due to excessive resistance in the tube between AMS and the printer."
        },
        {
          "ecode": "0702010000010011",
          "intro": "AMS C The assist motor calibration parameter error. Please pull out the filament from the filament hub and then restart the AMS."
        },
        {
          "ecode": "1801210000030001",
          "intro": "AMS-HT B Slot 2 filament has run out. Please wait while old filament is purged."
        },
        {
          "ecode": "1805110000010001",
          "intro": "The AMS-HT F slot 2 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "1804920000020002",
          "intro": "AMS-HT E The cooling fan speed of heater 1 is too low, which could be due to excessive fan resistance."
        },
        {
          "ecode": "0702210000020010",
          "intro": "AMS C slot 2 feeds filament out of AMS timeout."
        },
        {
          "ecode": "0705010000020008",
          "intro": "AMS F The assist motor phase winding has an open circuit. The assist motor may be faulty."
        },
        {
          "ecode": "1202710000010001",
          "intro": "AMS C Filament speed and length error: The slot 2 filament odometry may be faulty."
        },
        {
          "ecode": "1805210000020022",
          "intro": "AMS-HT F slot 2 assist motor is stalled，due to excessive resistance in the tube near the toolhead."
        },
        {
          "ecode": "0707220000010081",
          "intro": "Failed to read the filament information from AMS H slot 3. The AMS main board may be malfunctioning."
        },
        {
          "ecode": "1802230000020009",
          "intro": "Failed to extrude AMS-HT C Slot 4 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "1800950000010001",
          "intro": "AMS-HT A The temperature sensor of heater 2 is malfunctioning, which may be due to poor connector contact."
        },
        {
          "ecode": "1801310000010001",
          "intro": "The AMS-HT B RFID 2 board has an error."
        },
        {
          "ecode": "0705110000010003",
          "intro": "The AMS F slot 2 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "1804220000020002",
          "intro": "AMS-HT E Slot 3 is empty; please insert a new filament."
        },
        {
          "ecode": "0703200000020008",
          "intro": "AMS D Slot 1 feed-in Hall sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "1805700000020005",
          "intro": "Failed to feed the filament outside the AMS-HT. Please clip the end of the filament flat and check to see if the spool is stuck."
        },
        {
          "ecode": "0707220000020022",
          "intro": "AMS H slot 3 assist motor is stalled，due to excessive resistance in the tube near the toolhead."
        },
        {
          "ecode": "0703210000030001",
          "intro": "AMS D Slot 2 filament has run out. Please wait while old filament is purged."
        },
        {
          "ecode": "1805210000020001",
          "intro": "AMS-HT F Slot 2 filament has run out. Please insert a new filament."
        },
        {
          "ecode": "0700210000010085",
          "intro": "Failed to read the filament information from AMS A slot 2. RFID tag verification failed. You can try to use Bambu Lab filament."
        },
        {
          "ecode": "1804200000010085",
          "intro": "Failed to read the filament information from AMS-HT E slot 1. RFID tag verification failed. You can try to use Bambu Lab filament."
        },
        {
          "ecode": "0C00030000030010",
          "intro": "Your printer seems to be printing without extruding."
        },
        {
          "ecode": "0702230000020024",
          "intro": "AMS C slot 4 failed to rotate the filament spool when pulling filament back to AMS."
        },
        {
          "ecode": "1200120000010001",
          "intro": "The AMS A Slot3 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "1203300000010004",
          "intro": "RFID cannot be read because of an encryption chip failure in AMS D."
        },
        {
          "ecode": "0704230000020019",
          "intro": "AMS E slot 4 assist motor is stalled，due to excessive resistance in the tube between AMS and the filament buffer."
        },
        {
          "ecode": "1201330000020002",
          "intro": "The RFID-tag on AMS B Slot 4 is damaged."
        },
        {
          "ecode": "1802300000010004",
          "intro": "Encryption chip failure"
        },
        {
          "ecode": "0704200000020019",
          "intro": "AMS E slot 1 assist motor is stalled，due to excessive resistance in the tube between AMS and the filament buffer."
        },
        {
          "ecode": "1806200000020018",
          "intro": "AMS-HT G slot 1 assist motor is stalled，due to excessive resistance in the tube near AMS."
        },
        {
          "ecode": "1803210000020017",
          "intro": "AMS-HT D slot 2 assist motor is stalled，due to excessive resistance in the tube between AMS and the printer."
        },
        {
          "ecode": "0707910000020001",
          "intro": "AMS H The operation of the exhaust valve 2 is abnormal, which may be due to excessive resistance."
        },
        {
          "ecode": "0703220000020018",
          "intro": "AMS D slot 3 assist motor is stalled，due to excessive resistance in the tube near AMS."
        },
        {
          "ecode": "1804230000020022",
          "intro": "AMS-HT E slot 4 assist motor is stalled，due to excessive resistance in the tube near the toolhead."
        },
        {
          "ecode": "0500010000020001",
          "intro": "The media pipeline is malfunctioning. Please restart the printer. If multiple attempts fail, please contact customer support."
        },
        {
          "ecode": "1802230000020002",
          "intro": "AMS-HT C Slot 4 is empty; please insert a new filament."
        },
        {
          "ecode": "1806010000010005",
          "intro": "AMS-HT G The current sensor of assist motor may be faulty."
        },
        {
          "ecode": "1201120000020002",
          "intro": "The AMS B Slot3 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "0705200000020001",
          "intro": "AMS F Slot 1 filament has run out. Please insert a new filament."
        },
        {
          "ecode": "1807970000030001",
          "intro": "AMS-HT H chamber temperature is too high; auxiliary feeding or RFID reading is currently not allowed."
        },
        {
          "ecode": "0701130000010001",
          "intro": "The AMS B slot 4 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "1803970000030001",
          "intro": "AMS-HT D chamber temperature is too high; auxiliary feeding or RFID reading is currently not allowed."
        },
        {
          "ecode": "1800230000020018",
          "intro": "AMS-HT A slot 4 assist motor is stalled，due to excessive resistance in the tube near AMS."
        },
        {
          "ecode": "0704210000020003",
          "intro": "AMS E Slot 2's filament may be broken in AMS."
        },
        {
          "ecode": "1202110000010001",
          "intro": "The AMS C Slot2 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "0705210000020017",
          "intro": "AMS F slot 2 assist motor is stalled，due to excessive resistance in the tube between AMS and the printer."
        },
        {
          "ecode": "0701020000010001",
          "intro": "AMS B Filament speed and length error: The filament odometry may be faulty."
        },
        {
          "ecode": "1802220000010083",
          "intro": "Failed to read the filament information from AMS-HT C slot 3. The RFID tag may be damaged."
        },
        {
          "ecode": "0700220000020009",
          "intro": "Failed to extrude AMS A Slot 3 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "0703220000020009",
          "intro": "Failed to extrude AMS D Slot 3 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "1807230000020020",
          "intro": "AMS-HT H slot 4 assist motor is stalled，due to excessive resistance in the tube near the filament buffer。"
        },
        {
          "ecode": "1806010000010004",
          "intro": "The AMS-HT G assist motor speed control is malfunctioning. The speed sensor may be faulty."
        },
        {
          "ecode": "1202100000010001",
          "intro": "The AMS C Slot1 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "0707110000020002",
          "intro": "The AMS H slot 2 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "1202200000020005",
          "intro": "AMS C Slot1 filament has run out, and purging the old filament went abnormally; please check to see if filament is stuck in the toolhead."
        },
        {
          "ecode": "1807950000010001",
          "intro": "AMS-HT H The temperature sensor of heater 2 is malfunctioning, which may be due to poor connector contact."
        },
        {
          "ecode": "1800200000020024",
          "intro": "AMS-HT A slot 1 failed to rotate the filament spool when pulling filament back to AMS."
        },
        {
          "ecode": "1803300000030003",
          "intro": "RFID cannot be read because of a hardware or structural error."
        },
        {
          "ecode": "0300130000010001",
          "intro": "The current sensor of Motor-A is abnormal. This may be caused by a failure of the hardware sampling circuit."
        },
        {
          "ecode": "1806210000020001",
          "intro": "AMS-HT G Slot 2 filament has run out. Please insert a new filament."
        },
        {
          "ecode": "1805200000020007",
          "intro": "AMS-HT F Slot 1 feed-out Hall sensor is disconnected. The connector may have poor contact."
        },
        {
          "ecode": "0706120000010003",
          "intro": "The AMS G slot 3 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "1807230000020009",
          "intro": "Failed to extrude AMS-HT H Slot 4 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "1803220000020003",
          "intro": "AMS-HT D Slot 3's filament may be broken in AMS-HT."
        },
        {
          "ecode": "0500040000020019",
          "intro": "The RFID-tag on AMS C Slot2 cannot be identified."
        },
        {
          "ecode": "0706810000010002",
          "intro": "AMS G The heater 2 is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "1801220000020024",
          "intro": "AMS-HT B slot 3 failed to rotate the filament spool when pulling filament back to AMS."
        },
        {
          "ecode": "0700230000010086",
          "intro": "Failed to read the filament information from AMS A slot 4. The RFID tag cannot rotate due to a jam during the filament loading or unloading. Please pull out the filament and try again."
        },
        {
          "ecode": "0701210000010086",
          "intro": "Failed to read the filament information from AMS B slot 2. The RFID tag cannot rotate due to a jam during the filament loading or unloading. Please pull out the filament and try again."
        },
        {
          "ecode": "1801910000020001",
          "intro": "AMS-HT B The operation of the exhaust valve 2 is abnormal, which may be due to excessive resistance."
        },
        {
          "ecode": "1806110000010003",
          "intro": "The AMS-HT G slot 2 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "0705300000020002",
          "intro": "The RFID-tag on AMS F Slot1 is damaged, or its content cannot be identified."
        },
        {
          "ecode": "0707220000020007",
          "intro": "AMS H Slot 3 feed-out Hall sensor is disconnected. The connector may have poor contact."
        },
        {
          "ecode": "0706350000010002",
          "intro": "AMS G The humidity sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "0701100000010003",
          "intro": "The AMS B slot 1 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "1802120000020002",
          "intro": "The AMS-HT C slot 3 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "1805120000010003",
          "intro": "The AMS-HT F slot 3 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "0702960000010001",
          "intro": "AMS C The drying process may experience thermal runaway. Please turn off the AMS power supply."
        },
        {
          "ecode": "0707200000020007",
          "intro": "AMS H Slot 1 feed-out Hall sensor is disconnected. The connector may have poor contact."
        },
        {
          "ecode": "1805110000020002",
          "intro": "The AMS-HT F slot 2 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "0707230000020022",
          "intro": "AMS H slot 4 assist motor is stalled，due to excessive resistance in the tube near the toolhead."
        },
        {
          "ecode": "1802210000020004",
          "intro": "AMS-HT C Slot 2 filament may be broken in the tool head."
        },
        {
          "ecode": "0705210000020008",
          "intro": "AMS F Slot 2 feed-in Hall sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "0700200000030002",
          "intro": "AMS A Slot 1 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "0704220000030001",
          "intro": "AMS E Slot 3 filament has run out. Please wait while old filament is purged."
        },
        {
          "ecode": "0704810000010002",
          "intro": "AMS E The heater 2 is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "1200230000030001",
          "intro": "AMS A Slot4 filament has run out. Purging the old filament; please wait."
        },
        {
          "ecode": "0704210000030002",
          "intro": "AMS E Slot 2 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "0700120000020004",
          "intro": "AMS A The brushed motor 3 has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "1807130000020004",
          "intro": "AMS-HT H The brushed motor 4 has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "1800230000020019",
          "intro": "AMS-HT A slot 4 assist motor is stalled，due to excessive resistance in the tube between AMS and the filament buffer."
        },
        {
          "ecode": "1801700000020003",
          "intro": "Failed to extrude the filament. Possible cause: extruder or nozzle clog."
        },
        {
          "ecode": "1802010000020002",
          "intro": "The AMS-HT C assist motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "1801210000020008",
          "intro": "AMS-HT B Slot 2 feed-in Hall sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "0701230000020010",
          "intro": "AMS B slot 4 feeds filament out of AMS timeout."
        },
        {
          "ecode": "1806200000020008",
          "intro": "AMS-HT G Slot 1 feed-in Hall sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "1200320000030003",
          "intro": "AMS A Slot3 RFID cannot be read because of a structural error."
        },
        {
          "ecode": "1803220000020004",
          "intro": "AMS-HT D Slot 3 filament may be broken in the tool head."
        },
        {
          "ecode": "0300200000010003",
          "intro": "X axis homing abnormal: the timing belt may be loose."
        },
        {
          "ecode": "1803230000010084",
          "intro": "Failed to read the filament information from AMS-HT D slot 4. The RFID tag may be damaged or positioned at the edge of the RFID detection device. Please remove 5cm filament and try again."
        },
        {
          "ecode": "1201200000030001",
          "intro": "AMS B Slot1 filament has run out. Purging the old filament; please wait."
        },
        {
          "ecode": "1807700000020001",
          "intro": "Failed to pull out the filament from the extruder. Possible causes: clogged extruder or broken filament."
        },
        {
          "ecode": "0705130000020002",
          "intro": "The AMS F slot 4 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "0C00020000010001",
          "intro": "The horizontal laser is not lit. Please check if it's covered or hardware connection has a problem."
        },
        {
          "ecode": "0707230000020018",
          "intro": "AMS H slot 4 assist motor is stalled，due to excessive resistance in the tube near AMS."
        },
        {
          "ecode": "0703210000020004",
          "intro": "AMS D Slot 2 filament may be broken in the tool head."
        },
        {
          "ecode": "1801200000020001",
          "intro": "AMS-HT B Slot 1 filament has run out. Please insert a new filament."
        },
        {
          "ecode": "0705350000010001",
          "intro": "The temperature and humidity sensor has an error. The chip may be faulty."
        },
        {
          "ecode": "0704220000020010",
          "intro": "AMS E slot 3 feeds filament out of AMS timeout."
        },
        {
          "ecode": "1803200000020003",
          "intro": "AMS-HT D Slot 1's filament may be broken in AMS-HT."
        },
        {
          "ecode": "1800210000020008",
          "intro": "AMS-HT A Slot 2 feed-in Hall sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "12FF200000020006",
          "intro": "Failed to extrude the filament; the extruder may be clogged."
        },
        {
          "ecode": "1801110000020004",
          "intro": "AMS-HT B The brushed motor 2 has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "1202330000030003",
          "intro": "AMS C Slot4 RFID cannot be read because of a structural error."
        },
        {
          "ecode": "0706010000010003",
          "intro": "The AMS G assist motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "1805230000010083",
          "intro": "Failed to read the filament information from AMS-HT F slot 4. The RFID tag may be damaged."
        },
        {
          "ecode": "0300090000010003",
          "intro": "The resistance of the extruder servo motor is abnormal; the motor may have failed."
        },
        {
          "ecode": "03000F0000010001",
          "intro": "Abnormal accelerometer data detected. Please try restarting the printer."
        },
        {
          "ecode": "1805220000010084",
          "intro": "Failed to read the filament information from AMS-HT F slot 3. The RFID tag may be damaged or positioned at the edge of the RFID detection device. Please remove 5cm filament and try again."
        },
        {
          "ecode": "1803230000020018",
          "intro": "AMS-HT D slot 4 assist motor is stalled，due to excessive resistance in the tube near AMS."
        },
        {
          "ecode": "1805240000020009",
          "intro": "AMS-HT F front cover is open. This may affect the drying performance or cause the filament to absorb moisture."
        },
        {
          "ecode": "0705130000010003",
          "intro": "The AMS F slot 4 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "0704300000030003",
          "intro": "RFID cannot be read because of a hardware or structural error."
        },
        {
          "ecode": "1802220000020003",
          "intro": "AMS-HT C Slot 3's filament may be broken in AMS-HT."
        },
        {
          "ecode": "0703010000020009",
          "intro": "AMS D The assist motor has unbalanced tree-phase resistaance. The assist motor may be faulty."
        },
        {
          "ecode": "0C00020000020003",
          "intro": "The horizontal laser is not bright enough at homing position. Please clean or replace the heatbed if this message appears repeatedly."
        },
        {
          "ecode": "1806960000020002",
          "intro": "AMS-HT G Environmental temperature is too low, which will affect the drying capability."
        },
        {
          "ecode": "0704330000020002",
          "intro": "The RFID-tag on AMS E Slot4 is damaged, or its content cannot be identified."
        },
        {
          "ecode": "0705300000010001",
          "intro": "The AMS F RFID 1 board has an error."
        },
        {
          "ecode": "0702930000010001",
          "intro": "AMS C The cooling fan of heater 2 is blocked, which may be due to the fan being stuck."
        },
        {
          "ecode": "1805920000010001",
          "intro": "AMS-HT F The cooling fan of heater 1 is blocked, which may be due to the fan being stuck."
        },
        {
          "ecode": "1802210000020018",
          "intro": "AMS-HT C slot 2 assist motor is stalled，due to excessive resistance in the tube near AMS."
        },
        {
          "ecode": "0705110000020004",
          "intro": "AMS F The brushed motor 2 has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "0300180000000000",
          "intro": ""
        },
        {
          "ecode": "0706010000010001",
          "intro": "The AMS G assist motor has slipped. The extrusion wheel may be worn down, or the filament may be too thin."
        },
        {
          "ecode": "1804230000020019",
          "intro": "AMS-HT E slot 4 assist motor is stalled，due to excessive resistance in the tube between AMS and the filament buffer."
        },
        {
          "ecode": "1800900000020001",
          "intro": "AMS-HT A The operation of the exhaust valve 1 is abnormal, which may be due to excessive resistance."
        },
        {
          "ecode": "1203230000020004",
          "intro": "AMS D Slot4 filament may be broken in the tool head."
        },
        {
          "ecode": "1804210000020008",
          "intro": "AMS-HT E Slot 2 feed-in Hall sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "0702220000020017",
          "intro": "AMS C slot 3 assist motor is stalled，due to excessive resistance in the tube between AMS and the printer."
        },
        {
          "ecode": "0706220000020008",
          "intro": "AMS G Slot 3 feed-in Hall sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "1202110000020002",
          "intro": "The AMS C Slot2 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "1807210000020009",
          "intro": "Failed to extrude AMS-HT H Slot 2 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "0705220000010083",
          "intro": "Failed to read the filament information from AMS F slot 3. The RFID tag may be damaged."
        },
        {
          "ecode": "0707700000020003",
          "intro": "Failed to extrude the filament. Possible cause: extruder or nozzle clog."
        },
        {
          "ecode": "1806130000020002",
          "intro": "The AMS-HT G slot 4 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "1804500000020001",
          "intro": "AMS-HT E communication is abnormal; please check the connection cable."
        },
        {
          "ecode": "1800960000010003",
          "intro": "AMS-HT A Unable to start drying; please pull out the filament from filament hub and try again."
        },
        {
          "ecode": "1801230000010084",
          "intro": "Failed to read the filament information from AMS-HT B slot 4. The RFID tag may be damaged or positioned at the edge of the RFID detection device. Please remove 5cm filament and try again."
        },
        {
          "ecode": "1804220000020009",
          "intro": "Failed to extrude AMS-HT E Slot 3 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "0706210000020021",
          "intro": "AMS G slot 2 assist motor is stalled，due to excessive resistance in the tube between the filament buffer and the toolhead."
        },
        {
          "ecode": "0300090000010001",
          "intro": "The extruder servo motor has an open circuit. The connection may be loose, or the motor may have failed."
        },
        {
          "ecode": "1803230000010086",
          "intro": "Failed to read the filament information from AMS-HT D slot 4. The RFID tag cannot rotate due to a jam during the filament loading or unloading. Please pull out the filament and try again."
        },
        {
          "ecode": "1800220000020018",
          "intro": "AMS-HT A slot 3 assist motor is stalled，due to excessive resistance in the tube near AMS."
        },
        {
          "ecode": "1200200000020002",
          "intro": "AMS A Slot 1 is empty; please insert a new filament."
        },
        {
          "ecode": "1203220000020006",
          "intro": "Failed to extrude AMS D Slot3 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "0707010000020006",
          "intro": "AMS H The assist motor three-phase wires are not connected. The assist motor connector may have poor contact."
        },
        {
          "ecode": "0703220000020011",
          "intro": "AMS D slot 3 pulls filament back to AMS timeout."
        },
        {
          "ecode": "0703230000020007",
          "intro": "AMS D Slot 4 feed-out Hall sensor is disconnected. The connector may have poor contact."
        },
        {
          "ecode": "1806970000030001",
          "intro": "AMS-HT G chamber temperature is too high; auxiliary feeding or RFID reading is currently not allowed."
        },
        {
          "ecode": "1801210000020020",
          "intro": "AMS-HT B slot 2 assist motor is stalled，due to excessive resistance in the tube near the filament buffer。"
        },
        {
          "ecode": "1806220000010084",
          "intro": "Failed to read the filament information from AMS-HT G slot 3. The RFID tag may be damaged or positioned at the edge of the RFID detection device. Please remove 5cm filament and try again."
        },
        {
          "ecode": "1800010000010011",
          "intro": "AMS-HT A The assist motor calibration parameter error. Please pull out the filament from the filament hub and then restart the AMS."
        },
        {
          "ecode": "050003000002000C",
          "intro": "Wireless hardware error: please turn off/on WiFi or restart the device."
        },
        {
          "ecode": "0704230000020021",
          "intro": "AMS E slot 4 assist motor is stalled，due to excessive resistance in the tube between the filament buffer and the toolhead."
        },
        {
          "ecode": "1804350000010002",
          "intro": "AMS-HT E The humidity sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "0701230000020003",
          "intro": "AMS B Slot 4's filament may be broken in AMS."
        },
        {
          "ecode": "0704700000020001",
          "intro": "Failed to pull out the filament from the extruder. Possible causes: clogged extruder or broken filament."
        },
        {
          "ecode": "1804220000010085",
          "intro": "Failed to read the filament information from AMS-HT E slot 3. RFID tag verification failed. You can try to use Bambu Lab filament."
        },
        {
          "ecode": "1804210000020011",
          "intro": "AMS-HT E slot 2 pulls filament back to AMS timeout."
        },
        {
          "ecode": "0705220000020002",
          "intro": "AMS F Slot 3 is empty; please insert a new filament."
        },
        {
          "ecode": "1801200000020020",
          "intro": "AMS-HT B slot 1 assist motor is stalled，due to excessive resistance in the tube near the filament buffer。"
        },
        {
          "ecode": "0706230000020009",
          "intro": "Failed to extrude AMS G Slot 4 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "03000D0000020006",
          "intro": "The build plate may not be properly placed. If this message appears repeatedly, please check the Wiki for more explanations."
        },
        {
          "ecode": "1804110000010003",
          "intro": "The AMS-HT E slot 2 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "0704210000020022",
          "intro": "AMS E slot 2 assist motor is stalled，due to excessive resistance in the tube near the toolhead."
        },
        {
          "ecode": "1804220000020008",
          "intro": "AMS-HT E Slot 3 feed-in Hall sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "1801210000020021",
          "intro": "AMS-HT B slot 2 assist motor is stalled，due to excessive resistance in the tube between the filament buffer and the toolhead."
        },
        {
          "ecode": "0701220000020004",
          "intro": "AMS B Slot 3 filament may be broken in the tool head."
        },
        {
          "ecode": "0500030000010005",
          "intro": "Internal service is malfunctioning. Please restart the device."
        },
        {
          "ecode": "1804210000010081",
          "intro": "Failed to read the filament information from AMS-HT E slot 2. The AMS main board may be malfunctioning."
        },
        {
          "ecode": "0705210000020021",
          "intro": "AMS F slot 2 assist motor is stalled，due to excessive resistance in the tube between the filament buffer and the toolhead."
        },
        {
          "ecode": "0702920000010001",
          "intro": "AMS C The cooling fan of heater 1 is blocked, which may be due to the fan being stuck."
        },
        {
          "ecode": "0707210000020019",
          "intro": "AMS H slot 2 assist motor is stalled，due to excessive resistance in the tube between AMS and the filament buffer."
        },
        {
          "ecode": "0705220000020021",
          "intro": "AMS F slot 3 assist motor is stalled，due to excessive resistance in the tube between the filament buffer and the toolhead."
        },
        {
          "ecode": "0300070000010003",
          "intro": "The resistance of Motor-B is abnormal; the motor may have failed."
        },
        {
          "ecode": "1806300000010001",
          "intro": "The AMS-HT G RFID 1 board has an error."
        },
        {
          "ecode": "0706120000020004",
          "intro": "AMS G The brushed motor 3 has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "1807220000020020",
          "intro": "AMS-HT H slot 3 assist motor is stalled，due to excessive resistance in the tube near the filament buffer。"
        },
        {
          "ecode": "1802010000020011",
          "intro": "AMS-HT C The motor assist parameter is lost. Please pull out the filament from the filament hub and then restart the AMS."
        },
        {
          "ecode": "0707200000020004",
          "intro": "AMS H Slot 1 filament may be broken in the tool head."
        },
        {
          "ecode": "0704200000020005",
          "intro": "AMS E Slot 1 filament has run out, and purging the old filament went abnormally; please check whether the filament is stuck in the tool head."
        },
        {
          "ecode": "1803200000020018",
          "intro": "AMS-HT D slot 1 assist motor is stalled，due to excessive resistance in the tube near AMS."
        },
        {
          "ecode": "0703230000020009",
          "intro": "Failed to extrude AMS D Slot 4 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "1800900000010003",
          "intro": "AMS-HT A The exhaust valve 1 is not connected, which may be due to poor connector contact."
        },
        {
          "ecode": "0704930000020002",
          "intro": "AMS E The cooling fan speed of heater 2 is too low, which could be due to excessive fan resistance."
        },
        {
          "ecode": "0703800000010003",
          "intro": "AMS D The heater 1 is short-circuited, which may be due to a wiring short or heater damage."
        },
        {
          "ecode": "0702350000010001",
          "intro": "The temperature and humidity sensor has an error. The chip may be faulty."
        },
        {
          "ecode": "1805210000010086",
          "intro": "Failed to read the filament information from AMS-HT F slot 2. The RFID tag cannot rotate due to a jam during the filament loading or unloading. Please pull out the filament and try again."
        },
        {
          "ecode": "0C00030000030007",
          "intro": "Possible first layer defects have been detected. Please check the first layer quality and decide if the job should be stopped."
        },
        {
          "ecode": "0702300000020002",
          "intro": "The RFID-tag on AMS C Slot1 is damaged, or its content cannot be identified."
        },
        {
          "ecode": "1805210000020019",
          "intro": "AMS-HT F slot 2 assist motor is stalled，due to excessive resistance in the tube between AMS and the filament buffer."
        },
        {
          "ecode": "0706010000020007",
          "intro": "AMS G The assist motor encoder wires are not connected. The assist motor connector may have poor contact."
        },
        {
          "ecode": "0705230000020004",
          "intro": "AMS F Slot 4 filament may be broken in the tool head."
        },
        {
          "ecode": "1804230000020002",
          "intro": "AMS-HT E Slot 4 is empty; please insert a new filament."
        },
        {
          "ecode": "1203200000030002",
          "intro": "AMS D Slot1 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "0705310000010001",
          "intro": "The AMS F RFID 2 board has an error."
        },
        {
          "ecode": "1802230000010081",
          "intro": "Failed to read the filament information from AMS-HT C slot 4. The AMS main board may be malfunctioning."
        },
        {
          "ecode": "0703220000020020",
          "intro": "AMS D slot 3 assist motor is stalled，due to excessive resistance in the tube near the filament buffer。"
        },
        {
          "ecode": "0701200000030002",
          "intro": "AMS B Slot 1 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "0704800000010004",
          "intro": "AMS E The heater 1 is heating abnormally."
        },
        {
          "ecode": "03000D0000020005",
          "intro": "The build plate may not be properly placed. If this message appears repeatedly, please check the Wiki for more explanations."
        },
        {
          "ecode": "0702100000010003",
          "intro": "The AMS C slot 1 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "0705200000020022",
          "intro": "AMS F slot 1 assist motor is stalled，due to excessive resistance in the tube near the toolhead."
        },
        {
          "ecode": "0701210000020011",
          "intro": "AMS B slot 2 pulls filament back to AMS timeout."
        },
        {
          "ecode": "1805220000010085",
          "intro": "Failed to read the filament information from AMS-HT F slot 3. RFID tag verification failed. You can try to use Bambu Lab filament."
        },
        {
          "ecode": "1803120000010003",
          "intro": "The AMS-HT D slot 3 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "0702940000010001",
          "intro": "AMS C The temperature sensor of heater 1 is malfunctioning, which may be due to poor connector contact."
        },
        {
          "ecode": "1805330000020002",
          "intro": "The RFID-tag on AMS-HT F Slot4 is damaged, or its content cannot be identified."
        },
        {
          "ecode": "1803910000010003",
          "intro": "AMS-HT D The exhaust valve 2 is not connected, which may be due to poor connector contact."
        },
        {
          "ecode": "1803700000020005",
          "intro": "Failed to feed the filament outside the AMS-HT. Please clip the end of the filament flat and check to see if the spool is stuck."
        },
        {
          "ecode": "1806210000020003",
          "intro": "AMS-HT G Slot 2's filament may be broken in AMS-HT."
        },
        {
          "ecode": "1802010000020006",
          "intro": "AMS-HT C The assist motor three-phase wires are not connected. The assist motor connector may have poor contact."
        },
        {
          "ecode": "07FF200000020004",
          "intro": "Please pull the external filament from the extruder."
        },
        {
          "ecode": "0C00020000020009",
          "intro": "The vertical laser is not bright enough at homing position. Please clean or replace the heatbed if this message appears repeatedly."
        },
        {
          "ecode": "030001000001000A",
          "intro": "The heatbed temperature control is abnormal; the AC board may be broken."
        },
        {
          "ecode": "1805200000030002",
          "intro": "AMS-HT F Slot 1 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "1805230000010084",
          "intro": "Failed to read the filament information from AMS-HT F slot 4. The RFID tag may be damaged or positioned at the edge of the RFID detection device. Please remove 5cm filament and try again."
        },
        {
          "ecode": "1800120000020002",
          "intro": "The AMS-HT A slot 3 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "0704130000010001",
          "intro": "The AMS E slot 4 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "1805200000020019",
          "intro": "AMS-HT F slot 1 assist motor is stalled，due to excessive resistance in the tube between AMS and the filament buffer."
        },
        {
          "ecode": "0300140000010001",
          "intro": "The current sensor of Motor-B is abnormal. This may be caused by a failure of the hardware sampling circuit."
        },
        {
          "ecode": "18FF200000020001",
          "intro": "External filament has run out; please load a new filament."
        },
        {
          "ecode": "1802230000020003",
          "intro": "AMS-HT C Slot 4's filament may be broken in AMS-HT."
        },
        {
          "ecode": "1806130000010001",
          "intro": "The AMS-HT G slot 4 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "1801130000010003",
          "intro": "The AMS-HT B slot 4 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "1203330000030003",
          "intro": "AMS D Slot4 RFID cannot be read because of a structural error."
        },
        {
          "ecode": "1806310000010004",
          "intro": "Encryption chip failure"
        },
        {
          "ecode": "0705210000020022",
          "intro": "AMS F slot 2 assist motor is stalled，due to excessive resistance in the tube near the toolhead."
        },
        {
          "ecode": "0700210000010084",
          "intro": "Failed to read the filament information from AMS A slot 2. The RFID tag may be damaged or positioned at the edge of the RFID detection device. Please remove 5cm filament and try again."
        },
        {
          "ecode": "1801920000010001",
          "intro": "AMS-HT B The cooling fan of heater 1 is blocked, which may be due to the fan being stuck."
        },
        {
          "ecode": "1801940000010001",
          "intro": "AMS-HT B The temperature sensor of heater 1 is malfunctioning, which may be due to poor connector contact."
        },
        {
          "ecode": "1802330000020002",
          "intro": "The RFID-tag on AMS-HT C Slot4 is damaged, or its content cannot be identified."
        },
        {
          "ecode": "1803930000020002",
          "intro": "AMS-HT D The cooling fan speed of heater 2 is too low, which could be due to excessive fan resistance."
        },
        {
          "ecode": "1203320000020002",
          "intro": "The RFID-tag on AMS D Slot 3 is damaged."
        },
        {
          "ecode": "1801230000020004",
          "intro": "AMS-HT B Slot 4 filament may be broken in the tool head."
        },
        {
          "ecode": "1805310000010001",
          "intro": "The AMS-HT F RFID 2 board has an error."
        },
        {
          "ecode": "0707220000020018",
          "intro": "AMS H slot 3 assist motor is stalled，due to excessive resistance in the tube near AMS."
        },
        {
          "ecode": "1800810000010001",
          "intro": "AMS-HT A The current sensor of heater 2 is abnormal."
        },
        {
          "ecode": "0707010000010001",
          "intro": "The AMS H assist motor has slipped. The extrusion wheel may be worn down, or the filament may be too thin."
        },
        {
          "ecode": "1802300000010001",
          "intro": "The AMS-HT C RFID 1 board has an error."
        },
        {
          "ecode": "1801210000020024",
          "intro": "AMS-HT B slot 2 failed to rotate the filament spool when pulling filament back to AMS."
        },
        {
          "ecode": "1800210000020020",
          "intro": "AMS-HT A slot 2 assist motor is stalled，due to excessive resistance in the tube near the filament buffer。"
        },
        {
          "ecode": "1202220000020005",
          "intro": "AMS C Slot3 filament has run out, and purging the old filament went abnormally; please check to see if filament is stuck in the toolhead."
        },
        {
          "ecode": "1804220000020010",
          "intro": "AMS-HT E slot 3 feeds filament out of AMS timeout."
        },
        {
          "ecode": "1802700000020006",
          "intro": "Timeout purging old filament. Possible cause: filament stuck or the extruder/nozzle clog."
        },
        {
          "ecode": "1801230000020001",
          "intro": "AMS-HT B Slot 4 filament has run out. Please insert a new filament."
        },
        {
          "ecode": "0704220000020020",
          "intro": "AMS E slot 3 assist motor is stalled，due to excessive resistance in the tube near the filament buffer。"
        },
        {
          "ecode": "0703210000020007",
          "intro": "AMS D Slot 2 feed-out Hall sensor is disconnected. The connector may have poor contact."
        },
        {
          "ecode": "1804960000020002",
          "intro": "AMS-HT E Environmental temperature is too low, which will affect the drying capability."
        },
        {
          "ecode": "1806220000010081",
          "intro": "Failed to read the filament information from AMS-HT G slot 3. The AMS main board may be malfunctioning."
        },
        {
          "ecode": "0700700000020008",
          "intro": "Failed to get AMS mapping table; please select \"Resume\" to retry."
        },
        {
          "ecode": "1807220000010086",
          "intro": "Failed to read the filament information from AMS-HT H slot 3. The RFID tag cannot rotate due to a jam during the filament loading or unloading. Please pull out the filament and try again."
        },
        {
          "ecode": "0700960000010003",
          "intro": "AMS A Unable to start drying; please pull out the filament from filament hub and try again."
        },
        {
          "ecode": "1803960000020002",
          "intro": "AMS-HT D Environmental temperature is too low, which will affect the drying capability."
        },
        {
          "ecode": "0707350000010001",
          "intro": "The temperature and humidity sensor has an error. The chip may be faulty."
        },
        {
          "ecode": "0707800000010002",
          "intro": "AMS H The heater 1 is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "12FF200000020007",
          "intro": "Failed to check the filament location in the tool head; please click for more help."
        },
        {
          "ecode": "0700220000010084",
          "intro": "Failed to read the filament information from AMS A slot 3. The RFID tag may be damaged or positioned at the edge of the RFID detection device. Please remove 5cm filament and try again."
        },
        {
          "ecode": "1807700000020002",
          "intro": "Failed to feed the filament into the toolhead. Possible cause: filament or spool stuck."
        },
        {
          "ecode": "1806930000020002",
          "intro": "AMS-HT G The cooling fan speed of heater 2 is too low, which could be due to excessive fan resistance."
        },
        {
          "ecode": "1807100000010003",
          "intro": "The AMS-HT H slot 1 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "1803700000020002",
          "intro": "Failed to feed the filament into the toolhead. Possible cause: filament or spool stuck."
        },
        {
          "ecode": "1807940000010001",
          "intro": "AMS-HT H The temperature sensor of heater 1 is malfunctioning, which may be due to poor connector contact."
        },
        {
          "ecode": "0701220000010083",
          "intro": "Failed to read the filament information from AMS B slot 3. The RFID tag may be damaged."
        },
        {
          "ecode": "1806230000020009",
          "intro": "Failed to extrude AMS-HT G Slot 4 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "1802200000020017",
          "intro": "AMS-HT C slot 1 assist motor is stalled，due to excessive resistance in the tube between AMS and the printer."
        },
        {
          "ecode": "0702960000010003",
          "intro": "AMS C Unable to start drying; please pull out the filament from filament hub and try again."
        },
        {
          "ecode": "0702230000020004",
          "intro": "AMS C Slot 4 filament may be broken in the tool head."
        },
        {
          "ecode": "1800910000010003",
          "intro": "AMS-HT A The exhaust valve 2 is not connected, which may be due to poor connector contact."
        },
        {
          "ecode": "1802120000020004",
          "intro": "AMS-HT C The brushed motor 3 has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "0700700000020001",
          "intro": "Failed to pull out the filament from the extruder. Possible causes: clogged extruder or broken filament."
        },
        {
          "ecode": "1803130000010001",
          "intro": "The AMS-HT D slot 4 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "1803020000010001",
          "intro": "AMS-HT D Filament speed and length error: The filament odometry may be faulty."
        },
        {
          "ecode": "1800330000020002",
          "intro": "The RFID-tag on AMS-HT A Slot4 is damaged, or its content cannot be identified."
        },
        {
          "ecode": "0702120000010003",
          "intro": "The AMS C slot 3 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "0703100000020002",
          "intro": "The AMS D slot 1 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "1807200000010084",
          "intro": "Failed to read the filament information from AMS-HT H slot 1. The RFID tag may be damaged or positioned at the edge of the RFID detection device. Please remove 5cm filament and try again."
        },
        {
          "ecode": "1800700000020004",
          "intro": "Failed to pull back the filament from the toolhead to AMS-HT. Possible cause: filament or spool stuck."
        },
        {
          "ecode": "1805300000010001",
          "intro": "The AMS-HT F RFID 1 board has an error."
        },
        {
          "ecode": "1801230000020005",
          "intro": "AMS-HT B Slot 4 filament has run out, and purging the old filament went abnormally; please check whether the filament is stuck in the tool head."
        },
        {
          "ecode": "0703200000010086",
          "intro": "Failed to read the filament information from AMS D slot 1. The RFID tag cannot rotate due to a jam during the filament loading or unloading. Please pull out the filament and try again."
        },
        {
          "ecode": "1807220000030002",
          "intro": "AMS-HT H Slot 3 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "1804310000020002",
          "intro": "The RFID-tag on AMS-HT E Slot2 is damaged, or its content cannot be identified."
        },
        {
          "ecode": "0706700000020003",
          "intro": "Failed to extrude the filament. Possible cause: extruder or nozzle clog."
        },
        {
          "ecode": "1806010000020002",
          "intro": "The AMS-HT G assist motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "0707100000020004",
          "intro": "AMS H The brushed motor 1 has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "0704010000020006",
          "intro": "AMS E The assist motor three-phase wires are not connected. The assist motor connector may have poor contact."
        },
        {
          "ecode": "1807700000020008",
          "intro": "Failed to get AMS mapping table; please select \"Resume\" to retry."
        },
        {
          "ecode": "1203330000010001",
          "intro": "AMS D Slot 4 RFID coil is broken or the RF hardware circuit has an error."
        },
        {
          "ecode": "0703230000030001",
          "intro": "AMS D Slot 4 filament has run out. Please wait while old filament is purged."
        },
        {
          "ecode": "0706200000020009",
          "intro": "Failed to extrude AMS G Slot 1 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "0704310000010001",
          "intro": "The AMS E RFID 2 board has an error."
        },
        {
          "ecode": "1200330000020002",
          "intro": "The RFID-tag on AMS A Slot 4 is damaged."
        },
        {
          "ecode": "1807120000010001",
          "intro": "The AMS-HT H slot 3 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "1805210000020007",
          "intro": "AMS-HT F Slot 2 feed-out Hall sensor is disconnected. The connector may have poor contact."
        },
        {
          "ecode": "0300010000010001",
          "intro": "The heatbed temperature is abnormal; the heater may have a short circuit."
        },
        {
          "ecode": "1201210000030001",
          "intro": "AMS B Slot2 filament has run out. Purging the old filament; please wait."
        },
        {
          "ecode": "0C00030000020004",
          "intro": "First layer inspection is not supported for the current print job."
        },
        {
          "ecode": "0300900000010002",
          "intro": "Chamber heating failed. Possible causes: the chamber is not fully enclosed, ambient temperature is too low, or the power supply heat dissipation vent is blocked."
        },
        {
          "ecode": "0700120000010001",
          "intro": "The AMS A slot 3 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "1806010000010011",
          "intro": "AMS-HT G The assist motor calibration parameter error. Please pull out the filament from the filament hub and then restart the AMS."
        },
        {
          "ecode": "1800020000010001",
          "intro": "AMS-HT A Filament speed and length error: The filament odometry may be faulty."
        },
        {
          "ecode": "0706230000020001",
          "intro": "AMS G Slot 4 filament has run out. Please insert a new filament."
        },
        {
          "ecode": "0702910000020001",
          "intro": "AMS C The operation of the exhaust valve 2 is abnormal, which may be due to excessive resistance."
        },
        {
          "ecode": "0703700000020005",
          "intro": "Failed to feed the filament outside the AMS. Please clip the end of the filament flat and check to see if the spool is stuck."
        },
        {
          "ecode": "1801210000020019",
          "intro": "AMS-HT B slot 2 assist motor is stalled，due to excessive resistance in the tube between AMS and the filament buffer."
        },
        {
          "ecode": "1201200000020006",
          "intro": "Failed to extrude AMS B Slot1 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "1802220000020010",
          "intro": "AMS-HT C slot 3 feeds filament out of AMS timeout."
        },
        {
          "ecode": "1803220000020011",
          "intro": "AMS-HT D slot 3 pulls filament back to AMS timeout."
        },
        {
          "ecode": "0700010000020009",
          "intro": "AMS A The assist motor has unbalanced tree-phase resistaance. The assist motor may be faulty."
        },
        {
          "ecode": "1200330000010001",
          "intro": "AMS A Slot 4 RFID coil is broken or the RF hardware circuit has an error."
        },
        {
          "ecode": "0700220000020003",
          "intro": "AMS A Slot 3's filament may be broken in AMS."
        },
        {
          "ecode": "1807800000010003",
          "intro": "AMS-HT H The heater 1 is short-circuited, which may be due to a wiring short or heater damage."
        },
        {
          "ecode": "1801810000010001",
          "intro": "AMS-HT B The current sensor of heater 2 is abnormal."
        },
        {
          "ecode": "0702010000020010",
          "intro": "AMS C The assist motor resistance is abnormal. The assist motor may be faulty."
        },
        {
          "ecode": "0703220000020022",
          "intro": "AMS D slot 3 assist motor is stalled，due to excessive resistance in the tube near the toolhead."
        },
        {
          "ecode": "0704230000010084",
          "intro": "Failed to read the filament information from AMS E slot 4. The RFID tag may be damaged or positioned at the edge of the RFID detection device. Please remove 5cm filament and try again."
        },
        {
          "ecode": "0702230000010083",
          "intro": "Failed to read the filament information from AMS C slot 4. The RFID tag may be damaged."
        },
        {
          "ecode": "1805210000010081",
          "intro": "Failed to read the filament information from AMS-HT F slot 2. The AMS main board may be malfunctioning."
        },
        {
          "ecode": "0705020000020002",
          "intro": "AMS F The odometer has no signal. The odometer connector may have poor contact."
        },
        {
          "ecode": "0705220000020008",
          "intro": "AMS F Slot 3 feed-in Hall sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "1802200000030002",
          "intro": "AMS-HT C Slot 1 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "0700920000020002",
          "intro": "AMS A The cooling fan speed of heater 1 is too low, which could be due to excessive fan resistance."
        },
        {
          "ecode": "1803310000020002",
          "intro": "The RFID-tag on AMS-HT D Slot2 is damaged, or its content cannot be identified."
        },
        {
          "ecode": "1800010000010004",
          "intro": "The AMS-HT A assist motor speed control is malfunctioning. The speed sensor may be faulty."
        },
        {
          "ecode": "0703210000020021",
          "intro": "AMS D slot 2 assist motor is stalled，due to excessive resistance in the tube between the filament buffer and the toolhead."
        },
        {
          "ecode": "0704210000020010",
          "intro": "AMS E slot 2 feeds filament out of AMS timeout."
        },
        {
          "ecode": "0701800000010001",
          "intro": "AMS B The current sensor of heater 1 is abnormal."
        },
        {
          "ecode": "1801220000010081",
          "intro": "Failed to read the filament information from AMS-HT B slot 3. The AMS main board may be malfunctioning."
        },
        {
          "ecode": "0704910000020001",
          "intro": "AMS E The operation of the exhaust valve 2 is abnormal, which may be due to excessive resistance."
        },
        {
          "ecode": "1802230000020010",
          "intro": "AMS-HT C slot 4 feeds filament out of AMS timeout."
        },
        {
          "ecode": "0701200000020001",
          "intro": "AMS B Slot 1 filament has run out. Please insert a new filament."
        },
        {
          "ecode": "1805010000020011",
          "intro": "AMS-HT F The motor assist parameter is lost. Please pull out the filament from the filament hub and then restart the AMS."
        },
        {
          "ecode": "1200200000030001",
          "intro": "AMS A Slot1 filament has run out. Purging the old filament; please wait."
        },
        {
          "ecode": "1803310000030003",
          "intro": "RFID cannot be read because of a hardware or structural error."
        },
        {
          "ecode": "1800010000020006",
          "intro": "AMS-HT A The assist motor three-phase wires are not connected. The assist motor connector may have poor contact."
        },
        {
          "ecode": "1802010000020010",
          "intro": "AMS-HT C The assist motor resistance is abnormal. The assist motor may be faulty."
        },
        {
          "ecode": "1807010000020002",
          "intro": "The AMS-HT H assist motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "0701930000010001",
          "intro": "AMS B The cooling fan of heater 2 is blocked, which may be due to the fan being stuck."
        },
        {
          "ecode": "0702210000020003",
          "intro": "AMS C Slot 2's filament may be broken in AMS."
        },
        {
          "ecode": "0701010000020010",
          "intro": "AMS B The assist motor resistance is abnormal. The assist motor may be faulty."
        },
        {
          "ecode": "0707210000020001",
          "intro": "AMS H Slot 2 filament has run out. Please insert a new filament."
        },
        {
          "ecode": "1803230000020003",
          "intro": "AMS-HT D Slot 4's filament may be broken in AMS-HT."
        },
        {
          "ecode": "0706210000010084",
          "intro": "Failed to read the filament information from AMS G slot 2. The RFID tag may be damaged or positioned at the edge of the RFID detection device. Please remove 5cm filament and try again."
        },
        {
          "ecode": "0703210000020003",
          "intro": "AMS D Slot 2's filament may be broken in AMS."
        },
        {
          "ecode": "0707310000010001",
          "intro": "The AMS H RFID 2 board has an error."
        },
        {
          "ecode": "0701200000020022",
          "intro": "AMS B slot 1 assist motor is stalled，due to excessive resistance in the tube near the toolhead."
        },
        {
          "ecode": "1805220000010083",
          "intro": "Failed to read the filament information from AMS-HT F slot 3. The RFID tag may be damaged."
        },
        {
          "ecode": "0707200000030001",
          "intro": "AMS H Slot 1 filament has run out. Please wait while old filament is purged."
        },
        {
          "ecode": "0702120000020004",
          "intro": "AMS C The brushed motor 3 has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "1203220000020001",
          "intro": "AMS D Slot3 filament has run out; please insert a new filament."
        },
        {
          "ecode": "1805020000010001",
          "intro": "AMS-HT F Filament speed and length error: The filament odometry may be faulty."
        },
        {
          "ecode": "0700100000010001",
          "intro": "The AMS A slot 1 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "0702210000020008",
          "intro": "AMS C Slot 2 feed-in Hall sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "0705200000020009",
          "intro": "Failed to extrude AMS F Slot 1 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "1806230000010085",
          "intro": "Failed to read the filament information from AMS-HT G slot 4. RFID tag verification failed. You can try to use Bambu Lab filament."
        },
        {
          "ecode": "1802220000020019",
          "intro": "AMS-HT C slot 3 assist motor is stalled，due to excessive resistance in the tube between AMS and the filament buffer."
        },
        {
          "ecode": "0706230000010085",
          "intro": "Failed to read the filament information from AMS G slot 4. RFID tag verification failed. You can try to use Bambu Lab filament."
        },
        {
          "ecode": "1802210000010086",
          "intro": "Failed to read the filament information from AMS-HT C slot 2. The RFID tag cannot rotate due to a jam during the filament loading or unloading. Please pull out the filament and try again."
        },
        {
          "ecode": "0700910000010003",
          "intro": "AMS A The exhaust valve 2 is not connected, which may be due to poor connector contact."
        },
        {
          "ecode": "0703010000020008",
          "intro": "AMS D The assist motor phase winding has an open circuit. The assist motor may be faulty."
        },
        {
          "ecode": "03000D000001000C",
          "intro": "The heatbed leveling data is abnormal. Please check whether there are any foreign objects on the heatbed and Z slider. If so, please remove them and try again."
        },
        {
          "ecode": "1807110000010001",
          "intro": "The AMS-HT H slot 2 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "1202210000020001",
          "intro": "AMS C Slot2 filament has run out; please insert a new filament."
        },
        {
          "ecode": "1200110000010001",
          "intro": "The AMS A Slot2 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "1802010000010005",
          "intro": "AMS-HT C The current sensor of assist motor may be faulty."
        },
        {
          "ecode": "1800220000020021",
          "intro": "AMS-HT A slot 3 assist motor is stalled，due to excessive resistance in the tube between the filament buffer and the toolhead."
        },
        {
          "ecode": "0705230000020010",
          "intro": "AMS F slot 4 feeds filament out of AMS timeout."
        },
        {
          "ecode": "0706200000010084",
          "intro": "Failed to read the filament information from AMS G slot 1. The RFID tag may be damaged or positioned at the edge of the RFID detection device. Please remove 5cm filament and try again."
        },
        {
          "ecode": "0702310000010001",
          "intro": "The AMS C RFID 2 board has an error."
        },
        {
          "ecode": "1802210000010084",
          "intro": "Failed to read the filament information from AMS-HT C slot 2. The RFID tag may be damaged or positioned at the edge of the RFID detection device. Please remove 5cm filament and try again."
        },
        {
          "ecode": "0706100000010001",
          "intro": "The AMS G slot 1 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "0700200000020010",
          "intro": "AMS A slot 1 feeds filament out of AMS timeout."
        },
        {
          "ecode": "0500030000010023",
          "intro": "The Chamber Temperature Control module is malfunctioning. Please restart the device."
        },
        {
          "ecode": "1807220000030001",
          "intro": "AMS-HT H Slot 3 filament has run out. Please wait while old filament is purged."
        },
        {
          "ecode": "1803230000020021",
          "intro": "AMS-HT D slot 4 assist motor is stalled，due to excessive resistance in the tube between the filament buffer and the toolhead."
        },
        {
          "ecode": "0704220000020004",
          "intro": "AMS E Slot 3 filament may be broken in the tool head."
        },
        {
          "ecode": "1805210000020005",
          "intro": "AMS-HT F Slot 2 filament has run out, and purging the old filament went abnormally; please check whether the filament is stuck in the tool head."
        },
        {
          "ecode": "1804230000020024",
          "intro": "AMS-HT E slot 4 failed to rotate the filament spool when pulling filament back to AMS."
        },
        {
          "ecode": "0701100000020002",
          "intro": "The AMS B slot 1 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "1802130000010001",
          "intro": "The AMS-HT C slot 4 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "1804100000020004",
          "intro": "AMS-HT E The brushed motor 1 has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "0703200000020009",
          "intro": "Failed to extrude AMS D Slot 1 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "0701010000010011",
          "intro": "AMS B The assist motor calibration parameter error. Please pull out the filament from the filament hub and then restart the AMS."
        },
        {
          "ecode": "1803110000020004",
          "intro": "AMS-HT D The brushed motor 2 has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "1801230000020009",
          "intro": "Failed to extrude AMS-HT B Slot 4 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "1201820000020001",
          "intro": "AMS B Slot3 filament may be tangled or stuck."
        },
        {
          "ecode": "050004000002001A",
          "intro": "The RFID-tag on AMS C Slot3 cannot be identified."
        },
        {
          "ecode": "1201110000020002",
          "intro": "The AMS B Slot2 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "0703910000020001",
          "intro": "AMS D The operation of the exhaust valve 2 is abnormal, which may be due to excessive resistance."
        },
        {
          "ecode": "1200110000020002",
          "intro": "The AMS A Slot2 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "0701300000010001",
          "intro": "The AMS B RFID 1 board has an error."
        },
        {
          "ecode": "1802210000020003",
          "intro": "AMS-HT C Slot 2's filament may be broken in AMS-HT."
        },
        {
          "ecode": "1802200000010084",
          "intro": "Failed to read the filament information from AMS-HT C slot 1. The RFID tag may be damaged or positioned at the edge of the RFID detection device. Please remove 5cm filament and try again."
        },
        {
          "ecode": "0702230000020001",
          "intro": "AMS C Slot 4 filament has run out. Please insert a new filament."
        },
        {
          "ecode": "0706110000010001",
          "intro": "The AMS G slot 2 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "1202720000010001",
          "intro": "AMS C Filament speed and length error: The slot 3 filament odometry may be faulty."
        },
        {
          "ecode": "1805800000010003",
          "intro": "AMS-HT F The heater 1 is short-circuited, which may be due to a wiring short or heater damage."
        },
        {
          "ecode": "0705200000010085",
          "intro": "Failed to read the filament information from AMS F slot 1. RFID tag verification failed. You can try to use Bambu Lab filament."
        },
        {
          "ecode": "0700810000010004",
          "intro": "AMS A The heater 2 is heating abnormally."
        },
        {
          "ecode": "0701230000020007",
          "intro": "AMS B Slot 4 feed-out Hall sensor is disconnected. The connector may have poor contact."
        },
        {
          "ecode": "0705210000010085",
          "intro": "Failed to read the filament information from AMS F slot 2. RFID tag verification failed. You can try to use Bambu Lab filament."
        },
        {
          "ecode": "0700200000020001",
          "intro": "AMS A Slot 1 filament has run out. Please insert a new filament."
        },
        {
          "ecode": "1803210000020020",
          "intro": "AMS-HT D slot 2 assist motor is stalled，due to excessive resistance in the tube near the filament buffer。"
        },
        {
          "ecode": "0704230000020020",
          "intro": "AMS E slot 4 assist motor is stalled，due to excessive resistance in the tube near the filament buffer。"
        },
        {
          "ecode": "0706700000020006",
          "intro": "Timeout purging old filament. Possible cause: filament stuck or the extruder/nozzle clog."
        },
        {
          "ecode": "0702220000020020",
          "intro": "AMS C slot 3 assist motor is stalled，due to excessive resistance in the tube near the filament buffer。"
        },
        {
          "ecode": "1801300000020002",
          "intro": "The RFID-tag on AMS-HT B Slot1 is damaged, or its content cannot be identified."
        },
        {
          "ecode": "1806200000020009",
          "intro": "Failed to extrude AMS-HT G Slot 1 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "1800210000030002",
          "intro": "AMS-HT A Slot 2 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "1801200000020017",
          "intro": "AMS-HT B slot 1 assist motor is stalled，due to excessive resistance in the tube between AMS and the printer."
        },
        {
          "ecode": "0705310000010004",
          "intro": "Encryption chip failure"
        },
        {
          "ecode": "1806200000020010",
          "intro": "AMS-HT G slot 1 feeds filament out of AMS timeout."
        },
        {
          "ecode": "0703230000020019",
          "intro": "AMS D slot 4 assist motor is stalled，due to excessive resistance in the tube between AMS and the filament buffer."
        },
        {
          "ecode": "1806210000010085",
          "intro": "Failed to read the filament information from AMS-HT G slot 2. RFID tag verification failed. You can try to use Bambu Lab filament."
        },
        {
          "ecode": "0700810000010002",
          "intro": "AMS A The heater 2 is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "1200700000010001",
          "intro": "AMS A Filament speed and length error: The slot 1 filament odometry may be faulty."
        },
        {
          "ecode": "0701500000020001",
          "intro": "AMS B communication is abnormal; please check the connection cable."
        },
        {
          "ecode": "0700810000010003",
          "intro": "AMS A The heater 2 is short-circuited, which may be due to a wiring short or heater damage."
        },
        {
          "ecode": "1200210000020006",
          "intro": "Failed to extrude AMS A Slot2 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "1804220000010083",
          "intro": "Failed to read the filament information from AMS-HT E slot 3. The RFID tag may be damaged."
        },
        {
          "ecode": "1806200000020004",
          "intro": "AMS-HT G Slot 1 filament may be broken in the tool head."
        },
        {
          "ecode": "0704200000020007",
          "intro": "AMS E Slot 1 feed-out Hall sensor is disconnected. The connector may have poor contact."
        },
        {
          "ecode": "0705230000020001",
          "intro": "AMS F Slot 4 filament has run out. Please insert a new filament."
        },
        {
          "ecode": "0700200000020019",
          "intro": "AMS A slot 1 assist motor is stalled，due to excessive resistance in the tube between AMS and the filament buffer."
        },
        {
          "ecode": "1803010000010001",
          "intro": "The AMS-HT D assist motor has slipped. The extrusion wheel may be worn down, or the filament may be too thin."
        },
        {
          "ecode": "0706210000020010",
          "intro": "AMS G slot 2 feeds filament out of AMS timeout."
        },
        {
          "ecode": "0707110000020004",
          "intro": "AMS H The brushed motor 2 has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "1802230000020017",
          "intro": "AMS-HT C slot 4 assist motor is stalled，due to excessive resistance in the tube between AMS and the printer."
        },
        {
          "ecode": "1800210000010086",
          "intro": "Failed to read the filament information from AMS-HT A slot 2. The RFID tag cannot rotate due to a jam during the filament loading or unloading. Please pull out the filament and try again."
        },
        {
          "ecode": "0705700000020007",
          "intro": "AMS filament ran out. Please put a new filament into the same slot in AMS and resume."
        },
        {
          "ecode": "0702200000010085",
          "intro": "Failed to read the filament information from AMS C slot 1. RFID tag verification failed. You can try to use Bambu Lab filament."
        },
        {
          "ecode": "0704230000020007",
          "intro": "AMS E Slot 4 feed-out Hall sensor is disconnected. The connector may have poor contact."
        },
        {
          "ecode": "1806210000020008",
          "intro": "AMS-HT G Slot 2 feed-in Hall sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "0700960000020002",
          "intro": "AMS A Environmental temperature is too low, which will affect the drying capability."
        },
        {
          "ecode": "0300020000010009",
          "intro": "Nozzle temperature control is abnormal. The hot end may not be installed. To heat the heating assembly without the hotend, enable Maintenance Mode in the settings."
        },
        {
          "ecode": "0704210000020019",
          "intro": "AMS E slot 2 assist motor is stalled，due to excessive resistance in the tube between AMS and the filament buffer."
        },
        {
          "ecode": "0707320000020002",
          "intro": "The RFID-tag on AMS H Slot3 is damaged, or its content cannot be identified."
        },
        {
          "ecode": "0706700000020004",
          "intro": "Failed to pull back the filament from the toolhead to AMS. Possible cause: filament or spool stuck."
        },
        {
          "ecode": "0706350000010001",
          "intro": "The temperature and humidity sensor has an error. The chip may be faulty."
        },
        {
          "ecode": "1800450000020002",
          "intro": "The filament cutter's cutting distance is too large. The XY motor may lose steps."
        },
        {
          "ecode": "1806220000020007",
          "intro": "AMS-HT G Slot 3 feed-out Hall sensor is disconnected. The connector may have poor contact."
        },
        {
          "ecode": "0703210000020019",
          "intro": "AMS D slot 2 assist motor is stalled，due to excessive resistance in the tube between AMS and the filament buffer."
        },
        {
          "ecode": "1804120000020004",
          "intro": "AMS-HT E The brushed motor 3 has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "0703200000020007",
          "intro": "AMS D Slot 1 feed-out Hall sensor is disconnected. The connector may have poor contact."
        },
        {
          "ecode": "0500030000010001",
          "intro": "The MC module is malfunctioning; please restart the device or check device cable connection."
        },
        {
          "ecode": "1805220000020024",
          "intro": "AMS-HT F slot 3 failed to rotate the filament spool when pulling filament back to AMS."
        },
        {
          "ecode": "1803210000020019",
          "intro": "AMS-HT D slot 2 assist motor is stalled，due to excessive resistance in the tube between AMS and the filament buffer."
        },
        {
          "ecode": "1801700000020006",
          "intro": "Timeout purging old filament. Possible cause: filament stuck or the extruder/nozzle clog."
        },
        {
          "ecode": "1203130000010001",
          "intro": "The AMS D Slot4 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "0703220000020019",
          "intro": "AMS D slot 3 assist motor is stalled，due to excessive resistance in the tube between AMS and the filament buffer."
        },
        {
          "ecode": "0704200000020021",
          "intro": "AMS E slot 1 assist motor is stalled，due to excessive resistance in the tube between the filament buffer and the toolhead."
        },
        {
          "ecode": "0704010000020002",
          "intro": "The AMS E assist motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "1800510000030001",
          "intro": "The AMS is disabled; please load filament from the spool holder."
        },
        {
          "ecode": "1803300000010001",
          "intro": "The AMS-HT D RFID 1 board has an error."
        },
        {
          "ecode": "1801230000010081",
          "intro": "Failed to read the filament information from AMS-HT B slot 4. The AMS main board may be malfunctioning."
        },
        {
          "ecode": "1804200000020022",
          "intro": "AMS-HT E slot 1 assist motor is stalled，due to excessive resistance in the tube near the toolhead."
        },
        {
          "ecode": "1806310000030003",
          "intro": "RFID cannot be read because of a hardware or structural error."
        },
        {
          "ecode": "1800220000020011",
          "intro": "AMS-HT A slot 3 pulls filament back to AMS timeout."
        },
        {
          "ecode": "0707300000020002",
          "intro": "The RFID-tag on AMS H Slot1 is damaged, or its content cannot be identified."
        },
        {
          "ecode": "0704900000010003",
          "intro": "AMS E The exhaust valve 1 is not connected, which may be due to poor connector contact."
        },
        {
          "ecode": "0707500000020001",
          "intro": "AMS H communication is abnormal; please check the connection cable."
        },
        {
          "ecode": "1203120000010001",
          "intro": "The AMS D Slot3 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "1801020000010001",
          "intro": "AMS-HT B Filament speed and length error: The filament odometry may be faulty."
        },
        {
          "ecode": "0705230000020020",
          "intro": "AMS F slot 4 assist motor is stalled，due to excessive resistance in the tube near the filament buffer。"
        },
        {
          "ecode": "1200820000020001",
          "intro": "AMS A Slot3 filament may be tangled or stuck."
        },
        {
          "ecode": "0707310000010004",
          "intro": "Encryption chip failure"
        },
        {
          "ecode": "0702210000020024",
          "intro": "AMS C slot 2 failed to rotate the filament spool when pulling filament back to AMS."
        },
        {
          "ecode": "1807220000020001",
          "intro": "AMS-HT H Slot 3 filament has run out. Please insert a new filament."
        },
        {
          "ecode": "1807210000020002",
          "intro": "AMS-HT H Slot 2 is empty; please insert a new filament."
        },
        {
          "ecode": "0705210000030002",
          "intro": "AMS F Slot 2 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "1804010000020006",
          "intro": "AMS-HT E The assist motor three-phase wires are not connected. The assist motor connector may have poor contact."
        },
        {
          "ecode": "0707200000020020",
          "intro": "AMS H slot 1 assist motor is stalled，due to excessive resistance in the tube near the filament buffer。"
        },
        {
          "ecode": "0702200000020018",
          "intro": "AMS C slot 1 assist motor is stalled，due to excessive resistance in the tube near AMS."
        },
        {
          "ecode": "0701200000020005",
          "intro": "AMS B Slot 1 filament has run out, and purging the old filament went abnormally; please check whether the filament is stuck in the tool head."
        },
        {
          "ecode": "0704210000020005",
          "intro": "AMS E Slot 2 filament has run out, and purging the old filament went abnormally; please check whether the filament is stuck in the tool head."
        },
        {
          "ecode": "1200130000010003",
          "intro": "The AMS A Slot4 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "1801200000020002",
          "intro": "AMS-HT B Slot 1 is empty; please insert a new filament."
        },
        {
          "ecode": "1807330000020002",
          "intro": "The RFID-tag on AMS-HT H Slot4 is damaged, or its content cannot be identified."
        },
        {
          "ecode": "1201200000020004",
          "intro": "AMS B Slot1 filament may be broken in the tool head."
        },
        {
          "ecode": "1800210000020010",
          "intro": "AMS-HT A slot 2 feeds filament out of AMS timeout."
        },
        {
          "ecode": "1802350000010001",
          "intro": "The temperature and humidity sensor has an error. The chip may be faulty."
        },
        {
          "ecode": "0705700000020008",
          "intro": "Failed to get AMS mapping table; please select \"Resume\" to retry."
        },
        {
          "ecode": "1807100000020004",
          "intro": "AMS-HT H The brushed motor 1 has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "0703810000010004",
          "intro": "AMS D The heater 2 is heating abnormally."
        },
        {
          "ecode": "0703010000010004",
          "intro": "The AMS D assist motor speed control is malfunctioning. The speed sensor may be faulty."
        },
        {
          "ecode": "1807100000020002",
          "intro": "The AMS-HT H slot 1 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "1803230000020009",
          "intro": "Failed to extrude AMS-HT D Slot 4 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "1803210000030002",
          "intro": "AMS-HT D Slot 2 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "1805200000010084",
          "intro": "Failed to read the filament information from AMS-HT F slot 1. The RFID tag may be damaged or positioned at the edge of the RFID detection device. Please remove 5cm filament and try again."
        },
        {
          "ecode": "0706010000020009",
          "intro": "AMS G The assist motor has unbalanced tree-phase resistaance. The assist motor may be faulty."
        },
        {
          "ecode": "0C0003000002000E",
          "intro": "Your nozzle seems to be covered with jammed or clogged material."
        },
        {
          "ecode": "1203100000010001",
          "intro": "The AMS D Slot1 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "1806200000010083",
          "intro": "Failed to read the filament information from AMS-HT G slot 1. The RFID tag may be damaged."
        },
        {
          "ecode": "0703220000020024",
          "intro": "AMS D slot 3 failed to rotate the filament spool when pulling filament back to AMS."
        },
        {
          "ecode": "1807910000020001",
          "intro": "AMS-HT H The operation of the exhaust valve 2 is abnormal, which may be due to excessive resistance."
        },
        {
          "ecode": "1800350000010001",
          "intro": "The temperature and humidity sensor has an error. The chip may be faulty."
        },
        {
          "ecode": "0704910000010003",
          "intro": "AMS E The exhaust valve 2 is not connected, which may be due to poor connector contact."
        },
        {
          "ecode": "0704920000010001",
          "intro": "AMS E The cooling fan of heater 1 is blocked, which may be due to the fan being stuck."
        },
        {
          "ecode": "0701210000020018",
          "intro": "AMS B slot 2 assist motor is stalled，due to excessive resistance in the tube near AMS."
        },
        {
          "ecode": "0703200000010081",
          "intro": "Failed to read the filament information from AMS D slot 1. The AMS main board may be malfunctioning."
        },
        {
          "ecode": "1802230000010083",
          "intro": "Failed to read the filament information from AMS-HT C slot 4. The RFID tag may be damaged."
        },
        {
          "ecode": "1805220000020001",
          "intro": "AMS-HT F Slot 3 filament has run out. Please insert a new filament."
        },
        {
          "ecode": "1801110000010003",
          "intro": "The AMS-HT B slot 2 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "1807810000010003",
          "intro": "AMS-HT H The heater 2 is short-circuited, which may be due to a wiring short or heater damage."
        },
        {
          "ecode": "0702900000010003",
          "intro": "AMS C The exhaust valve 1 is not connected, which may be due to poor connector contact."
        },
        {
          "ecode": "1803350000010001",
          "intro": "The temperature and humidity sensor has an error. The chip may be faulty."
        },
        {
          "ecode": "0705210000010084",
          "intro": "Failed to read the filament information from AMS F slot 2. The RFID tag may be damaged or positioned at the edge of the RFID detection device. Please remove 5cm filament and try again."
        },
        {
          "ecode": "1805310000010004",
          "intro": "Encryption chip failure"
        },
        {
          "ecode": "0707200000020010",
          "intro": "AMS H slot 1 feeds filament out of AMS timeout."
        },
        {
          "ecode": "1200320000010001",
          "intro": "AMS A Slot 3 RFID coil is broken or the RF hardware circuit has an error."
        },
        {
          "ecode": "1800200000030002",
          "intro": "AMS-HT A Slot 1 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "0700510000030001",
          "intro": "The AMS is disabled; please load filament from the spool holder."
        },
        {
          "ecode": "0706230000020020",
          "intro": "AMS G slot 4 assist motor is stalled，due to excessive resistance in the tube near the filament buffer。"
        },
        {
          "ecode": "0500020000020002",
          "intro": "Device login failed; please check your account information."
        },
        {
          "ecode": "0702100000020002",
          "intro": "The AMS C slot 1 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "0704100000020002",
          "intro": "The AMS E slot 1 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "0707200000020017",
          "intro": "AMS H slot 1 assist motor is stalled，due to excessive resistance in the tube between AMS and the printer."
        },
        {
          "ecode": "0705230000010083",
          "intro": "Failed to read the filament information from AMS F slot 4. The RFID tag may be damaged."
        },
        {
          "ecode": "0701920000010001",
          "intro": "AMS B The cooling fan of heater 1 is blocked, which may be due to the fan being stuck."
        },
        {
          "ecode": "1806100000020002",
          "intro": "The AMS-HT G slot 1 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "1803200000020009",
          "intro": "Failed to extrude AMS-HT D Slot 1 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "0C00020000020004",
          "intro": "Nozzle height seems to be too low. Please check if the nozzle is worn or tilted. Re-calibrate Lidar if the nozzle has been replaced."
        },
        {
          "ecode": "1805010000020010",
          "intro": "AMS-HT F The assist motor resistance is abnormal. The assist motor may be faulty."
        },
        {
          "ecode": "1201220000030001",
          "intro": "AMS B Slot3 filament has run out. Purging the old filament; please wait."
        },
        {
          "ecode": "0700100000010003",
          "intro": "The AMS A slot 1 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "0700010000010005",
          "intro": "AMS A The current sensor of assist motor may be faulty."
        },
        {
          "ecode": "1804220000010086",
          "intro": "Failed to read the filament information from AMS-HT E slot 3. The RFID tag cannot rotate due to a jam during the filament loading or unloading. Please pull out the filament and try again."
        },
        {
          "ecode": "1807200000020021",
          "intro": "AMS-HT H slot 1 assist motor is stalled，due to excessive resistance in the tube between the filament buffer and the toolhead."
        },
        {
          "ecode": "0500040000020017",
          "intro": "The RFID-tag on AMS B Slot4 cannot be identified."
        },
        {
          "ecode": "0702200000030001",
          "intro": "AMS C Slot 1 filament has run out. Please wait while old filament is purged."
        },
        {
          "ecode": "1805100000020002",
          "intro": "The AMS-HT F slot 1 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "1805200000020022",
          "intro": "AMS-HT F slot 1 assist motor is stalled，due to excessive resistance in the tube near the toolhead."
        },
        {
          "ecode": "1200100000020002",
          "intro": "The AMS A Slot1 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "1804210000020021",
          "intro": "AMS-HT E slot 2 assist motor is stalled，due to excessive resistance in the tube between the filament buffer and the toolhead."
        },
        {
          "ecode": "1801560000030001",
          "intro": "AMS-HT B is undergoing dry cooling; please wait for it to cool down before operating."
        },
        {
          "ecode": "0701230000020018",
          "intro": "AMS B slot 4 assist motor is stalled，due to excessive resistance in the tube near AMS."
        },
        {
          "ecode": "1805300000020002",
          "intro": "The RFID-tag on AMS-HT F Slot1 is damaged, or its content cannot be identified."
        },
        {
          "ecode": "1801210000020010",
          "intro": "AMS-HT B slot 2 feeds filament out of AMS timeout."
        },
        {
          "ecode": "0704110000020002",
          "intro": "The AMS E slot 2 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "0707200000020021",
          "intro": "AMS H slot 1 assist motor is stalled，due to excessive resistance in the tube between the filament buffer and the toolhead."
        },
        {
          "ecode": "1801350000010002",
          "intro": "AMS-HT B The humidity sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "1800220000010085",
          "intro": "Failed to read the filament information from AMS-HT A slot 3. RFID tag verification failed. You can try to use Bambu Lab filament."
        },
        {
          "ecode": "1807800000010004",
          "intro": "AMS-HT H The heater 1 is heating abnormally."
        },
        {
          "ecode": "0700810000010001",
          "intro": "AMS A The current sensor of heater 2 is abnormal."
        },
        {
          "ecode": "1801210000010083",
          "intro": "Failed to read the filament information from AMS-HT B slot 2. The RFID tag may be damaged."
        },
        {
          "ecode": "0707100000020002",
          "intro": "The AMS H slot 1 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "0300900000010005",
          "intro": "Chamber heating failed. The thermal resistance is too high."
        },
        {
          "ecode": "0705300000030003",
          "intro": "RFID cannot be read because of a hardware or structural error."
        },
        {
          "ecode": "0703300000010001",
          "intro": "The AMS D RFID 1 board has an error."
        },
        {
          "ecode": "1803210000020005",
          "intro": "AMS-HT D Slot 2 filament has run out, and purging the old filament went abnormally; please check whether the filament is stuck in the tool head."
        },
        {
          "ecode": "0701210000010085",
          "intro": "Failed to read the filament information from AMS B slot 2. RFID tag verification failed. You can try to use Bambu Lab filament."
        },
        {
          "ecode": "0701010000020002",
          "intro": "The AMS B assist motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "0706210000020024",
          "intro": "AMS G slot 2 failed to rotate the filament spool when pulling filament back to AMS."
        },
        {
          "ecode": "1800210000010085",
          "intro": "Failed to read the filament information from AMS-HT A slot 2. RFID tag verification failed. You can try to use Bambu Lab filament."
        },
        {
          "ecode": "0706200000020021",
          "intro": "AMS G slot 1 assist motor is stalled，due to excessive resistance in the tube between the filament buffer and the toolhead."
        },
        {
          "ecode": "1202300000010001",
          "intro": "AMS C Slot 1 RFID coil is broken or the RF hardware circuit has an error."
        },
        {
          "ecode": "1805700000020006",
          "intro": "Timeout purging old filament. Possible cause: filament stuck or the extruder/nozzle clog."
        },
        {
          "ecode": "1804810000010003",
          "intro": "AMS-HT E The heater 2 is short-circuited, which may be due to a wiring short or heater damage."
        },
        {
          "ecode": "1202220000020006",
          "intro": "Failed to extrude AMS C Slot3 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "1805230000020004",
          "intro": "AMS-HT F Slot 4 filament may be broken in the tool head."
        },
        {
          "ecode": "0701230000020021",
          "intro": "AMS B slot 4 assist motor is stalled，due to excessive resistance in the tube between the filament buffer and the toolhead."
        },
        {
          "ecode": "0706300000010004",
          "intro": "Encryption chip failure"
        },
        {
          "ecode": "1803210000020001",
          "intro": "AMS-HT D Slot 2 filament has run out. Please insert a new filament."
        },
        {
          "ecode": "0C00030000030006",
          "intro": "Purged filament may have piled up in the waste chute. Please check and clean the chute."
        },
        {
          "ecode": "1802230000020007",
          "intro": "AMS-HT C Slot 4 feed-out Hall sensor is disconnected. The connector may have poor contact."
        },
        {
          "ecode": "1203230000020003",
          "intro": "AMS D Slot4 filament may be broken in the PTFE tube."
        },
        {
          "ecode": "0707800000010003",
          "intro": "AMS H The heater 1 is short-circuited, which may be due to a wiring short or heater damage."
        },
        {
          "ecode": "0704220000020002",
          "intro": "AMS E Slot 3 is empty; please insert a new filament."
        },
        {
          "ecode": "1201230000030001",
          "intro": "AMS B Slot4 filament has run out. Purging the old filament; please wait."
        },
        {
          "ecode": "0703220000010085",
          "intro": "Failed to read the filament information from AMS D slot 3. RFID tag verification failed. You can try to use Bambu Lab filament."
        },
        {
          "ecode": "1803800000010003",
          "intro": "AMS-HT D The heater 1 is short-circuited, which may be due to a wiring short or heater damage."
        },
        {
          "ecode": "1801900000010003",
          "intro": "AMS-HT B The exhaust valve 1 is not connected, which may be due to poor connector contact."
        },
        {
          "ecode": "1805010000020006",
          "intro": "AMS-HT F The assist motor three-phase wires are not connected. The assist motor connector may have poor contact."
        },
        {
          "ecode": "1804800000010003",
          "intro": "AMS-HT E The heater 1 is short-circuited, which may be due to a wiring short or heater damage."
        },
        {
          "ecode": "1803200000010081",
          "intro": "Failed to read the filament information from AMS-HT D slot 1. The AMS main board may be malfunctioning."
        },
        {
          "ecode": "1807210000020024",
          "intro": "AMS-HT H slot 2 failed to rotate the filament spool when pulling filament back to AMS."
        },
        {
          "ecode": "1200210000020003",
          "intro": "AMS A Slot2 filament may be broken in the PTFE tube."
        },
        {
          "ecode": "1806210000010083",
          "intro": "Failed to read the filament information from AMS-HT G slot 2. The RFID tag may be damaged."
        },
        {
          "ecode": "0705910000020001",
          "intro": "AMS F The operation of the exhaust valve 2 is abnormal, which may be due to excessive resistance."
        },
        {
          "ecode": "1800210000030001",
          "intro": "AMS-HT A Slot 2 filament has run out. Please wait while old filament is purged."
        },
        {
          "ecode": "0707010000020010",
          "intro": "AMS H The assist motor resistance is abnormal. The assist motor may be faulty."
        },
        {
          "ecode": "0704200000020017",
          "intro": "AMS E slot 1 assist motor is stalled，due to excessive resistance in the tube between AMS and the printer."
        },
        {
          "ecode": "1200300000010001",
          "intro": "AMS A Slot 1 RFID coil is broken or the RF hardware circuit has an error."
        },
        {
          "ecode": "0703230000020020",
          "intro": "AMS D slot 4 assist motor is stalled，due to excessive resistance in the tube near the filament buffer。"
        },
        {
          "ecode": "0707020000020002",
          "intro": "AMS H The odometer has no signal. The odometer connector may have poor contact."
        },
        {
          "ecode": "0706200000020005",
          "intro": "AMS G Slot 1 filament has run out, and purging the old filament went abnormally; please check whether the filament is stuck in the tool head."
        },
        {
          "ecode": "1805220000020003",
          "intro": "AMS-HT F Slot 3's filament may be broken in AMS-HT."
        },
        {
          "ecode": "0701010000020007",
          "intro": "AMS B The assist motor encoder wires are not connected. The assist motor connector may have poor contact."
        },
        {
          "ecode": "1802900000020001",
          "intro": "AMS-HT C The operation of the exhaust valve 1 is abnormal, which may be due to excessive resistance."
        },
        {
          "ecode": "1804010000020010",
          "intro": "AMS-HT E The assist motor resistance is abnormal. The assist motor may be faulty."
        },
        {
          "ecode": "1201210000020005",
          "intro": "AMS B Slot2 filament has run out, and purging the old filament went abnormally; please check to see if filament is stuck in the toolhead."
        },
        {
          "ecode": "1202220000030002",
          "intro": "AMS C Slot3 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "1800200000020004",
          "intro": "AMS-HT A Slot 1 filament may be broken in the tool head."
        },
        {
          "ecode": "1800220000020022",
          "intro": "AMS-HT A slot 3 assist motor is stalled，due to excessive resistance in the tube near the toolhead."
        },
        {
          "ecode": "0705230000010085",
          "intro": "Failed to read the filament information from AMS F slot 4. RFID tag verification failed. You can try to use Bambu Lab filament."
        },
        {
          "ecode": "0705220000010085",
          "intro": "Failed to read the filament information from AMS F slot 3. RFID tag verification failed. You can try to use Bambu Lab filament."
        },
        {
          "ecode": "1807210000020008",
          "intro": "AMS-HT H Slot 2 feed-in Hall sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "0700700000020003",
          "intro": "Failed to extrude the filament. Possible cause: extruder or nozzle clog."
        },
        {
          "ecode": "0704200000020011",
          "intro": "AMS E slot 1 pulls filament back to AMS timeout."
        },
        {
          "ecode": "0705920000020002",
          "intro": "AMS F The cooling fan speed of heater 1 is too low, which could be due to excessive fan resistance."
        },
        {
          "ecode": "1802810000010001",
          "intro": "AMS-HT C The current sensor of heater 2 is abnormal."
        },
        {
          "ecode": "0707230000020004",
          "intro": "AMS H Slot 4 filament may be broken in the tool head."
        },
        {
          "ecode": "0706220000020022",
          "intro": "AMS G slot 3 assist motor is stalled，due to excessive resistance in the tube near the toolhead."
        },
        {
          "ecode": "1805810000010002",
          "intro": "AMS-HT F The heater 2 is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "1804220000030002",
          "intro": "AMS-HT E Slot 3 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "1806220000020003",
          "intro": "AMS-HT G Slot 3's filament may be broken in AMS-HT."
        },
        {
          "ecode": "0707940000010001",
          "intro": "AMS H The temperature sensor of heater 1 is malfunctioning, which may be due to poor connector contact."
        },
        {
          "ecode": "0300110000020002",
          "intro": "The resonance frequency of the Y-axis differs greatly from the last calibration. Please clean the Y-axis liner rod and conduct a calibration after printing."
        },
        {
          "ecode": "1800970000030001",
          "intro": "AMS-HT A chamber temperature is too high; auxiliary feeding or RFID reading is currently not allowed."
        },
        {
          "ecode": "030001000001000C",
          "intro": "The heatbed has worked at full load for a long time. The temperature control system may be abnormal."
        },
        {
          "ecode": "1806200000010084",
          "intro": "Failed to read the filament information from AMS-HT G slot 1. The RFID tag may be damaged or positioned at the edge of the RFID detection device. Please remove 5cm filament and try again."
        },
        {
          "ecode": "1805230000020022",
          "intro": "AMS-HT F slot 4 assist motor is stalled，due to excessive resistance in the tube near the toolhead."
        },
        {
          "ecode": "1803200000020004",
          "intro": "AMS-HT D Slot 1 filament may be broken in the tool head."
        },
        {
          "ecode": "1803120000020004",
          "intro": "AMS-HT D The brushed motor 3 has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "1800130000010003",
          "intro": "The AMS-HT A slot 4 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "1202820000020001",
          "intro": "AMS C Slot3 filament may be tangled or stuck."
        },
        {
          "ecode": "0703200000030002",
          "intro": "AMS D Slot 1 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "1806220000020002",
          "intro": "AMS-HT G Slot 3 is empty; please insert a new filament."
        },
        {
          "ecode": "1804210000010084",
          "intro": "Failed to read the filament information from AMS-HT E slot 2. The RFID tag may be damaged or positioned at the edge of the RFID detection device. Please remove 5cm filament and try again."
        },
        {
          "ecode": "1800230000010084",
          "intro": "Failed to read the filament information from AMS-HT A slot 4. The RFID tag may be damaged or positioned at the edge of the RFID detection device. Please remove 5cm filament and try again."
        },
        {
          "ecode": "0704210000020007",
          "intro": "AMS E Slot 2 feed-out Hall sensor is disconnected. The connector may have poor contact."
        },
        {
          "ecode": "0500040000020010",
          "intro": "The RFID-tag on AMS A Slot1 cannot be identified."
        },
        {
          "ecode": "1804200000020020",
          "intro": "AMS-HT E slot 1 assist motor is stalled，due to excessive resistance in the tube near the filament buffer。"
        },
        {
          "ecode": "0707100000010001",
          "intro": "The AMS H slot 1 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "1806940000010001",
          "intro": "AMS-HT G The temperature sensor of heater 1 is malfunctioning, which may be due to poor connector contact."
        },
        {
          "ecode": "0706220000020019",
          "intro": "AMS G slot 3 assist motor is stalled，due to excessive resistance in the tube between AMS and the filament buffer."
        },
        {
          "ecode": "1806210000010086",
          "intro": "Failed to read the filament information from AMS-HT G slot 2. The RFID tag cannot rotate due to a jam during the filament loading or unloading. Please pull out the filament and try again."
        },
        {
          "ecode": "0705210000020020",
          "intro": "AMS F slot 2 assist motor is stalled，due to excessive resistance in the tube near the filament buffer。"
        },
        {
          "ecode": "0701210000010084",
          "intro": "Failed to read the filament information from AMS B slot 2. The RFID tag may be damaged or positioned at the edge of the RFID detection device. Please remove 5cm filament and try again."
        },
        {
          "ecode": "0700310000010004",
          "intro": "Encryption chip failure"
        },
        {
          "ecode": "0704350000010002",
          "intro": "AMS E The humidity sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "0700210000020007",
          "intro": "AMS A Slot 2 feed-out Hall sensor is disconnected. The connector may have poor contact."
        },
        {
          "ecode": "1803200000020005",
          "intro": "AMS-HT D Slot 1 filament has run out, and purging the old filament went abnormally; please check whether the filament is stuck in the tool head."
        },
        {
          "ecode": "1804200000020024",
          "intro": "AMS-HT E slot 1 failed to rotate the filament spool when pulling filament back to AMS."
        },
        {
          "ecode": "1201330000030003",
          "intro": "AMS B Slot4 RFID cannot be read because of a structural error."
        },
        {
          "ecode": "0703210000020009",
          "intro": "Failed to extrude AMS D Slot 2 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "1805200000020024",
          "intro": "AMS-HT F slot 1 failed to rotate the filament spool when pulling filament back to AMS."
        },
        {
          "ecode": "1800300000010004",
          "intro": "Encryption chip failure"
        },
        {
          "ecode": "1800210000020004",
          "intro": "AMS-HT A Slot 2 filament may be broken in the tool head."
        },
        {
          "ecode": "1806010000010003",
          "intro": "The AMS-HT G assist motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "0706210000020002",
          "intro": "AMS G Slot 2 is empty; please insert a new filament."
        },
        {
          "ecode": "0701210000020008",
          "intro": "AMS B Slot 2 feed-in Hall sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "1202220000030001",
          "intro": "AMS C Slot3 filament has run out. Purging the old filament; please wait."
        },
        {
          "ecode": "1803200000020010",
          "intro": "AMS-HT D slot 1 feeds filament out of AMS timeout."
        },
        {
          "ecode": "0700210000020021",
          "intro": "AMS A slot 2 assist motor is stalled，due to excessive resistance in the tube between the filament buffer and the toolhead."
        },
        {
          "ecode": "0702700000020008",
          "intro": "Failed to get AMS mapping table; please select \"Resume\" to retry."
        },
        {
          "ecode": "0707130000020004",
          "intro": "AMS H The brushed motor 4 has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "1800200000030001",
          "intro": "AMS-HT A Slot 1 filament has run out. Please wait while old filament is purged."
        },
        {
          "ecode": "0705900000020001",
          "intro": "AMS F The operation of the exhaust valve 1 is abnormal, which may be due to excessive resistance."
        },
        {
          "ecode": "1807200000020009",
          "intro": "Failed to extrude AMS-HT H Slot 1 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "0706560000030001",
          "intro": "AMS G is undergoing dry cooling; please wait for it to cool down before operating."
        },
        {
          "ecode": "0706220000010083",
          "intro": "Failed to read the filament information from AMS G slot 3. The RFID tag may be damaged."
        },
        {
          "ecode": "1805200000020002",
          "intro": "AMS-HT F Slot 1 is empty; please insert a new filament."
        },
        {
          "ecode": "0700220000020021",
          "intro": "AMS A slot 3 assist motor is stalled，due to excessive resistance in the tube between the filament buffer and the toolhead."
        },
        {
          "ecode": "0707230000020024",
          "intro": "AMS H slot 4 failed to rotate the filament spool when pulling filament back to AMS."
        },
        {
          "ecode": "1801230000020007",
          "intro": "AMS-HT B Slot 4 feed-out Hall sensor is disconnected. The connector may have poor contact."
        },
        {
          "ecode": "0703200000020005",
          "intro": "AMS D Slot 1 filament has run out, and purging the old filament went abnormally; please check whether the filament is stuck in the tool head."
        },
        {
          "ecode": "0706810000010001",
          "intro": "AMS G The current sensor of heater 2 is abnormal."
        },
        {
          "ecode": "1801010000020011",
          "intro": "AMS-HT B The motor assist parameter is lost. Please pull out the filament from the filament hub and then restart the AMS."
        },
        {
          "ecode": "0700220000020019",
          "intro": "AMS A slot 3 assist motor is stalled，due to excessive resistance in the tube between AMS and the filament buffer."
        },
        {
          "ecode": "0705230000020005",
          "intro": "AMS F Slot 4 filament has run out, and purging the old filament went abnormally; please check whether the filament is stuck in the tool head."
        },
        {
          "ecode": "1202200000020003",
          "intro": "AMS C Slot1 filament may be broken in the PTFE tube."
        },
        {
          "ecode": "0705220000030002",
          "intro": "AMS F Slot 3 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "1803200000010085",
          "intro": "Failed to read the filament information from AMS-HT D slot 1. RFID tag verification failed. You can try to use Bambu Lab filament."
        },
        {
          "ecode": "0705230000020009",
          "intro": "Failed to extrude AMS F Slot 4 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "0701230000020005",
          "intro": "AMS B Slot 4 filament has run out, and purging the old filament went abnormally; please check whether the filament is stuck in the tool head."
        },
        {
          "ecode": "0705930000020002",
          "intro": "AMS F The cooling fan speed of heater 2 is too low, which could be due to excessive fan resistance."
        },
        {
          "ecode": "1804130000020004",
          "intro": "AMS-HT E The brushed motor 4 has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "0703200000020024",
          "intro": "AMS D slot 1 failed to rotate the filament spool when pulling filament back to AMS."
        },
        {
          "ecode": "1200210000030002",
          "intro": "AMS A Slot2 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "1802960000010003",
          "intro": "AMS-HT C Unable to start drying; please pull out the filament from filament hub and try again."
        },
        {
          "ecode": "1802120000010001",
          "intro": "The AMS-HT C slot 3 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "0705200000020005",
          "intro": "AMS F Slot 1 filament has run out, and purging the old filament went abnormally; please check whether the filament is stuck in the tool head."
        },
        {
          "ecode": "1201220000020004",
          "intro": "AMS B Slot3 filament may be broken in the tool head."
        },
        {
          "ecode": "0704310000010004",
          "intro": "Encryption chip failure"
        },
        {
          "ecode": "1803350000010002",
          "intro": "AMS-HT D The humidity sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "0706130000010001",
          "intro": "The AMS G slot 4 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "0704350000010001",
          "intro": "The temperature and humidity sensor has an error. The chip may be faulty."
        },
        {
          "ecode": "1806110000020004",
          "intro": "AMS-HT G The brushed motor 2 has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "0702200000020011",
          "intro": "AMS C slot 1 pulls filament back to AMS timeout."
        },
        {
          "ecode": "0702310000010004",
          "intro": "Encryption chip failure"
        },
        {
          "ecode": "1804200000010083",
          "intro": "Failed to read the filament information from AMS-HT E slot 1. The RFID tag may be damaged."
        },
        {
          "ecode": "1803910000020001",
          "intro": "AMS-HT D The operation of the exhaust valve 2 is abnormal, which may be due to excessive resistance."
        },
        {
          "ecode": "1803230000010085",
          "intro": "Failed to read the filament information from AMS-HT D slot 4. RFID tag verification failed. You can try to use Bambu Lab filament."
        },
        {
          "ecode": "0704230000020024",
          "intro": "AMS E slot 4 failed to rotate the filament spool when pulling filament back to AMS."
        },
        {
          "ecode": "0700450000020002",
          "intro": "The filament cutter's cutting distance is too large. The XY motor may lose steps."
        },
        {
          "ecode": "1805800000010002",
          "intro": "AMS-HT F The heater 1 is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "0702220000010084",
          "intro": "Failed to read the filament information from AMS C slot 3. The RFID tag may be damaged or positioned at the edge of the RFID detection device. Please remove 5cm filament and try again."
        },
        {
          "ecode": "0706220000010086",
          "intro": "Failed to read the filament information from AMS G slot 3. The RFID tag cannot rotate due to a jam during the filament loading or unloading. Please pull out the filament and try again."
        },
        {
          "ecode": "1200450000020003",
          "intro": "The filament cutter handle has not been released. The handle or blade may be jammed, or there could be an issue with the filament sensor connection."
        },
        {
          "ecode": "0707120000020002",
          "intro": "The AMS H slot 3 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "1203230000030001",
          "intro": "AMS D Slot4 filament has run out. Purging the old filament; please wait."
        },
        {
          "ecode": "0C00030000020002",
          "intro": "First layer inspection terminated due to abnormal Lidar data."
        },
        {
          "ecode": "0706200000010083",
          "intro": "Failed to read the filament information from AMS G slot 1. The RFID tag may be damaged."
        },
        {
          "ecode": "0705210000020005",
          "intro": "AMS F Slot 2 filament has run out, and purging the old filament went abnormally; please check whether the filament is stuck in the tool head."
        },
        {
          "ecode": "1805960000010001",
          "intro": "AMS-HT F The drying process may experience thermal runaway. Please turn off the AMS power supply."
        },
        {
          "ecode": "1803200000020017",
          "intro": "AMS-HT D slot 1 assist motor is stalled，due to excessive resistance in the tube between AMS and the printer."
        },
        {
          "ecode": "1200230000020003",
          "intro": "AMS A Slot4 filament may be broken in the PTFE tube."
        },
        {
          "ecode": "07FF700000020003",
          "intro": "Please check if the filament is coming out of the nozzle. If not, gently push the material and try to extrude again."
        },
        {
          "ecode": "0707810000010002",
          "intro": "AMS H The heater 2 is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "0702210000020020",
          "intro": "AMS C slot 2 assist motor is stalled，due to excessive resistance in the tube near the filament buffer。"
        },
        {
          "ecode": "0700400000020003",
          "intro": "The AMS Hub communication is abnormal; the cable may be not well connected."
        },
        {
          "ecode": "1800230000020020",
          "intro": "AMS-HT A slot 4 assist motor is stalled，due to excessive resistance in the tube near the filament buffer。"
        },
        {
          "ecode": "0706210000010086",
          "intro": "Failed to read the filament information from AMS G slot 2. The RFID tag cannot rotate due to a jam during the filament loading or unloading. Please pull out the filament and try again."
        },
        {
          "ecode": "0705500000020001",
          "intro": "AMS F communication is abnormal; please check the connection cable."
        },
        {
          "ecode": "1802230000020018",
          "intro": "AMS-HT C slot 4 assist motor is stalled，due to excessive resistance in the tube near AMS."
        },
        {
          "ecode": "1802220000020020",
          "intro": "AMS-HT C slot 3 assist motor is stalled，due to excessive resistance in the tube near the filament buffer。"
        },
        {
          "ecode": "0705230000010084",
          "intro": "Failed to read the filament information from AMS F slot 4. The RFID tag may be damaged or positioned at the edge of the RFID detection device. Please remove 5cm filament and try again."
        },
        {
          "ecode": "1807960000020002",
          "intro": "AMS-HT H Environmental temperature is too low, which will affect the drying capability."
        },
        {
          "ecode": "1203120000010003",
          "intro": "The AMS D Slot3 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "1802310000030003",
          "intro": "RFID cannot be read because of a hardware or structural error."
        },
        {
          "ecode": "0300050000010001",
          "intro": "The motor driver is overheating. Its radiator may be loose, or its cooling fan may be damaged."
        },
        {
          "ecode": "1806230000020022",
          "intro": "AMS-HT G slot 4 assist motor is stalled，due to excessive resistance in the tube near the toolhead."
        },
        {
          "ecode": "1800920000010001",
          "intro": "AMS-HT A The cooling fan of heater 1 is blocked, which may be due to the fan being stuck."
        },
        {
          "ecode": "1807120000020002",
          "intro": "The AMS-HT H slot 3 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "1201130000010001",
          "intro": "The AMS B Slot4 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "0703200000020002",
          "intro": "AMS D Slot 1 is empty; please insert a new filament."
        },
        {
          "ecode": "1804320000020002",
          "intro": "The RFID-tag on AMS-HT E Slot3 is damaged, or its content cannot be identified."
        },
        {
          "ecode": "0700220000020005",
          "intro": "AMS A Slot 3 filament has run out, and purging the old filament went abnormally; please check whether the filament is stuck in the tool head."
        },
        {
          "ecode": "0703200000020003",
          "intro": "AMS D Slot 1's filament may be broken in AMS."
        },
        {
          "ecode": "0700220000020018",
          "intro": "AMS A slot 3 assist motor is stalled，due to excessive resistance in the tube near AMS."
        },
        {
          "ecode": "0705700000020005",
          "intro": "Failed to feed the filament outside the AMS. Please clip the end of the filament flat and check to see if the spool is stuck."
        },
        {
          "ecode": "1806010000020011",
          "intro": "AMS-HT G The motor assist parameter is lost. Please pull out the filament from the filament hub and then restart the AMS."
        },
        {
          "ecode": "0706220000020017",
          "intro": "AMS G slot 3 assist motor is stalled，due to excessive resistance in the tube between AMS and the printer."
        },
        {
          "ecode": "1200300000010004",
          "intro": "RFID cannot be read because of an encryption chip failure in AMS A."
        },
        {
          "ecode": "1806900000010003",
          "intro": "AMS-HT G The exhaust valve 1 is not connected, which may be due to poor connector contact."
        },
        {
          "ecode": "1200510000030001",
          "intro": "AMS is disabled; please load filament from spool holder."
        },
        {
          "ecode": "0707010000010004",
          "intro": "The AMS H assist motor speed control is malfunctioning. The speed sensor may be faulty."
        },
        {
          "ecode": "1807230000020024",
          "intro": "AMS-HT H slot 4 failed to rotate the filament spool when pulling filament back to AMS."
        },
        {
          "ecode": "0500030000010006",
          "intro": "A system panic occurred. Please restart the device."
        },
        {
          "ecode": "1800230000020007",
          "intro": "AMS-HT A Slot 4 feed-out Hall sensor is disconnected. The connector may have poor contact."
        },
        {
          "ecode": "0705960000010001",
          "intro": "AMS F The drying process may experience thermal runaway. Please turn off the AMS power supply."
        },
        {
          "ecode": "1807700000020004",
          "intro": "Failed to pull back the filament from the toolhead to AMS-HT. Possible cause: filament or spool stuck."
        },
        {
          "ecode": "1804200000010081",
          "intro": "Failed to read the filament information from AMS-HT E slot 1. The AMS main board may be malfunctioning."
        },
        {
          "ecode": "1805010000010004",
          "intro": "The AMS-HT F assist motor speed control is malfunctioning. The speed sensor may be faulty."
        },
        {
          "ecode": "1802220000020005",
          "intro": "AMS-HT C Slot 3 filament has run out, and purging the old filament went abnormally; please check whether the filament is stuck in the tool head."
        },
        {
          "ecode": "0706500000020001",
          "intro": "AMS G communication is abnormal; please check the connection cable."
        },
        {
          "ecode": "1803100000020004",
          "intro": "AMS-HT D The brushed motor 1 has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "1802010000020007",
          "intro": "AMS-HT C The assist motor encoder wires are not connected. The assist motor connector may have poor contact."
        },
        {
          "ecode": "0703310000020002",
          "intro": "The RFID-tag on AMS D Slot2 is damaged, or its content cannot be identified."
        },
        {
          "ecode": "0702200000010083",
          "intro": "Failed to read the filament information from AMS C slot 1. The RFID tag may be damaged."
        },
        {
          "ecode": "1803230000020020",
          "intro": "AMS-HT D slot 4 assist motor is stalled，due to excessive resistance in the tube near the filament buffer。"
        },
        {
          "ecode": "1807230000020019",
          "intro": "AMS-HT H slot 4 assist motor is stalled，due to excessive resistance in the tube between AMS and the filament buffer."
        },
        {
          "ecode": "0300020000010007",
          "intro": "The nozzle temperature is abnormal; the sensor may have an open circuit."
        },
        {
          "ecode": "0701810000010002",
          "intro": "AMS B The heater 2 is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "0702210000020021",
          "intro": "AMS C slot 2 assist motor is stalled，due to excessive resistance in the tube between the filament buffer and the toolhead."
        },
        {
          "ecode": "0702130000010003",
          "intro": "The AMS C slot 4 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "0701200000020004",
          "intro": "AMS B Slot 1 filament may be broken in the tool head."
        },
        {
          "ecode": "0706200000020022",
          "intro": "AMS G slot 1 assist motor is stalled，due to excessive resistance in the tube near the toolhead."
        },
        {
          "ecode": "1803920000020002",
          "intro": "AMS-HT D The cooling fan speed of heater 1 is too low, which could be due to excessive fan resistance."
        },
        {
          "ecode": "0706200000020019",
          "intro": "AMS G slot 1 assist motor is stalled，due to excessive resistance in the tube between AMS and the filament buffer."
        },
        {
          "ecode": "1806230000020020",
          "intro": "AMS-HT G slot 4 assist motor is stalled，due to excessive resistance in the tube near the filament buffer。"
        },
        {
          "ecode": "0702500000020001",
          "intro": "AMS C communication is abnormal; please check the connection cable."
        },
        {
          "ecode": "0300900000010010",
          "intro": "The communication of chamber temperature controller is abnormal."
        },
        {
          "ecode": "1804220000020021",
          "intro": "AMS-HT E slot 3 assist motor is stalled，due to excessive resistance in the tube between the filament buffer and the toolhead."
        },
        {
          "ecode": "0703350000010002",
          "intro": "AMS D The humidity sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "1800810000010002",
          "intro": "AMS-HT A The heater 2 is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "1807230000020003",
          "intro": "AMS-HT H Slot 4's filament may be broken in AMS-HT."
        },
        {
          "ecode": "1807200000030002",
          "intro": "AMS-HT H Slot 1 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "0702900000020001",
          "intro": "AMS C The operation of the exhaust valve 1 is abnormal, which may be due to excessive resistance."
        },
        {
          "ecode": "0706010000010011",
          "intro": "AMS G The assist motor calibration parameter error. Please pull out the filament from the filament hub and then restart the AMS."
        },
        {
          "ecode": "0703200000020004",
          "intro": "AMS D Slot 1 filament may be broken in the tool head."
        },
        {
          "ecode": "1806120000020002",
          "intro": "The AMS-HT G slot 3 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "0707810000010001",
          "intro": "AMS H The current sensor of heater 2 is abnormal."
        },
        {
          "ecode": "1803230000020004",
          "intro": "AMS-HT D Slot 4 filament may be broken in the tool head."
        },
        {
          "ecode": "0700230000020007",
          "intro": "AMS A Slot 4 feed-out Hall sensor is disconnected. The connector may have poor contact."
        },
        {
          "ecode": "1203200000020004",
          "intro": "AMS D Slot1 filament may be broken in the tool head."
        },
        {
          "ecode": "1201700000010001",
          "intro": "AMS B Filament speed and length error: The slot 1 filament odometry may be faulty."
        },
        {
          "ecode": "1804110000010001",
          "intro": "The AMS-HT E slot 2 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "1805010000020008",
          "intro": "AMS-HT F The assist motor phase winding has an open circuit. The assist motor may be faulty."
        },
        {
          "ecode": "0702220000020002",
          "intro": "AMS C Slot 3 is empty; please insert a new filament."
        },
        {
          "ecode": "0705810000010002",
          "intro": "AMS F The heater 2 is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "1801210000010084",
          "intro": "Failed to read the filament information from AMS-HT B slot 2. The RFID tag may be damaged or positioned at the edge of the RFID detection device. Please remove 5cm filament and try again."
        },
        {
          "ecode": "0703220000010083",
          "intro": "Failed to read the filament information from AMS D slot 3. The RFID tag may be damaged."
        },
        {
          "ecode": "1805210000020004",
          "intro": "AMS-HT F Slot 2 filament may be broken in the tool head."
        },
        {
          "ecode": "1805200000020017",
          "intro": "AMS-HT F slot 1 assist motor is stalled，due to excessive resistance in the tube between AMS and the printer."
        },
        {
          "ecode": "0702210000010086",
          "intro": "Failed to read the filament information from AMS C slot 2. The RFID tag cannot rotate due to a jam during the filament loading or unloading. Please pull out the filament and try again."
        },
        {
          "ecode": "0704200000020001",
          "intro": "AMS E Slot 1 filament has run out. Please insert a new filament."
        },
        {
          "ecode": "0702220000020021",
          "intro": "AMS C slot 3 assist motor is stalled，due to excessive resistance in the tube between the filament buffer and the toolhead."
        },
        {
          "ecode": "0700300000030003",
          "intro": "RFID cannot be read because of a hardware or structural error."
        },
        {
          "ecode": "1202130000010001",
          "intro": "The AMS C Slot4 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "1803200000020019",
          "intro": "AMS-HT D slot 1 assist motor is stalled，due to excessive resistance in the tube between AMS and the filament buffer."
        },
        {
          "ecode": "0703230000020024",
          "intro": "AMS D slot 4 failed to rotate the filament spool when pulling filament back to AMS."
        },
        {
          "ecode": "0705200000020002",
          "intro": "AMS F Slot 1 is empty; please insert a new filament."
        },
        {
          "ecode": "0707330000020002",
          "intro": "The RFID-tag on AMS H Slot4 is damaged, or its content cannot be identified."
        },
        {
          "ecode": "1802220000020024",
          "intro": "AMS-HT C slot 3 failed to rotate the filament spool when pulling filament back to AMS."
        },
        {
          "ecode": "0700220000020007",
          "intro": "AMS A Slot 3 feed-out Hall sensor is disconnected. The connector may have poor contact."
        },
        {
          "ecode": "1804220000020019",
          "intro": "AMS-HT E slot 3 assist motor is stalled，due to excessive resistance in the tube between AMS and the filament buffer."
        },
        {
          "ecode": "0706220000020002",
          "intro": "AMS G Slot 3 is empty; please insert a new filament."
        },
        {
          "ecode": "1807230000010086",
          "intro": "Failed to read the filament information from AMS-HT H slot 4. The RFID tag cannot rotate due to a jam during the filament loading or unloading. Please pull out the filament and try again."
        },
        {
          "ecode": "0702350000010002",
          "intro": "AMS C The humidity sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "0700330000020002",
          "intro": "The RFID-tag on AMS A Slot4 is damaged, or its content cannot be identified."
        },
        {
          "ecode": "1805220000010086",
          "intro": "Failed to read the filament information from AMS-HT F slot 3. The RFID tag cannot rotate due to a jam during the filament loading or unloading. Please pull out the filament and try again."
        },
        {
          "ecode": "1802700000020008",
          "intro": "Failed to get AMS mapping table; please select \"Resume\" to retry."
        },
        {
          "ecode": "1806210000030002",
          "intro": "AMS-HT G Slot 2 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "0707230000030001",
          "intro": "AMS H Slot 4 filament has run out. Please wait while old filament is purged."
        },
        {
          "ecode": "1802220000020017",
          "intro": "AMS-HT C slot 3 assist motor is stalled，due to excessive resistance in the tube between AMS and the printer."
        },
        {
          "ecode": "0701210000020004",
          "intro": "AMS B Slot 2 filament may be broken in the tool head."
        },
        {
          "ecode": "0700130000020004",
          "intro": "AMS A The brushed motor 4 has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "1803200000020008",
          "intro": "AMS-HT D Slot 1 feed-in Hall sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "1200130000020002",
          "intro": "The AMS A Slot4 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "1806010000010001",
          "intro": "The AMS-HT G assist motor has slipped. The extrusion wheel may be worn down, or the filament may be too thin."
        },
        {
          "ecode": "0500030000010002",
          "intro": "The toolhead is malfunctioning. Please restart the device."
        },
        {
          "ecode": "0704220000020001",
          "intro": "AMS E Slot 3 filament has run out. Please insert a new filament."
        },
        {
          "ecode": "1803960000010001",
          "intro": "AMS-HT D The drying process may experience thermal runaway. Please turn off the AMS power supply."
        },
        {
          "ecode": "1804210000020019",
          "intro": "AMS-HT E slot 2 assist motor is stalled，due to excessive resistance in the tube between AMS and the filament buffer."
        },
        {
          "ecode": "0300940000030001",
          "intro": "Chamber cooling may be too slow. You can open the front door or top cover to help cooling if the air in the chamber is non-toxic."
        },
        {
          "ecode": "1201300000020002",
          "intro": "The RFID-tag on AMS B Slot 1 is damaged."
        },
        {
          "ecode": "1807310000030003",
          "intro": "RFID cannot be read because of a hardware or structural error."
        },
        {
          "ecode": "0704010000020011",
          "intro": "AMS E The motor assist parameter is lost. Please pull out the filament from the filament hub and then restart the AMS."
        },
        {
          "ecode": "1807200000010083",
          "intro": "Failed to read the filament information from AMS-HT H slot 1. The RFID tag may be damaged."
        },
        {
          "ecode": "0706100000020004",
          "intro": "AMS G The brushed motor 1 has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "1806200000010086",
          "intro": "Failed to read the filament information from AMS-HT G slot 1. The RFID tag cannot rotate due to a jam during the filament loading or unloading. Please pull out the filament and try again."
        },
        {
          "ecode": "0700200000020003",
          "intro": "AMS A Slot 1's filament may be broken in AMS."
        },
        {
          "ecode": "0707010000010005",
          "intro": "AMS H The current sensor of assist motor may be faulty."
        },
        {
          "ecode": "1807700000020005",
          "intro": "Failed to feed the filament outside the AMS-HT. Please clip the end of the filament flat and check to see if the spool is stuck."
        },
        {
          "ecode": "1806200000020021",
          "intro": "AMS-HT G slot 1 assist motor is stalled，due to excessive resistance in the tube between the filament buffer and the toolhead."
        },
        {
          "ecode": "1807230000020005",
          "intro": "AMS-HT H Slot 4 filament has run out, and purging the old filament went abnormally; please check whether the filament is stuck in the tool head."
        },
        {
          "ecode": "0704200000030002",
          "intro": "AMS E Slot 1 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "1805230000020002",
          "intro": "AMS-HT F Slot 4 is empty; please insert a new filament."
        },
        {
          "ecode": "0704230000010086",
          "intro": "Failed to read the filament information from AMS E slot 4. The RFID tag cannot rotate due to a jam during the filament loading or unloading. Please pull out the filament and try again."
        },
        {
          "ecode": "1804700000020006",
          "intro": "Timeout purging old filament. Possible cause: filament stuck or the extruder/nozzle clog."
        },
        {
          "ecode": "0706200000020010",
          "intro": "AMS G slot 1 feeds filament out of AMS timeout."
        },
        {
          "ecode": "1803220000010084",
          "intro": "Failed to read the filament information from AMS-HT D slot 3. The RFID tag may be damaged or positioned at the edge of the RFID detection device. Please remove 5cm filament and try again."
        },
        {
          "ecode": "0704230000020001",
          "intro": "AMS E Slot 4 filament has run out. Please insert a new filament."
        },
        {
          "ecode": "1807210000020022",
          "intro": "AMS-HT H slot 2 assist motor is stalled，due to excessive resistance in the tube near the toolhead."
        },
        {
          "ecode": "0300070000010001",
          "intro": "Motor-B has an open-circuit. The connection may be loose, or the motor may have failed."
        },
        {
          "ecode": "1807230000020022",
          "intro": "AMS-HT H slot 4 assist motor is stalled，due to excessive resistance in the tube near the toolhead."
        },
        {
          "ecode": "0703200000010084",
          "intro": "Failed to read the filament information from AMS D slot 1. The RFID tag may be damaged or positioned at the edge of the RFID detection device. Please remove 5cm filament and try again."
        },
        {
          "ecode": "0701350000010001",
          "intro": "The temperature and humidity sensor has an error. The chip may be faulty."
        },
        {
          "ecode": "0707800000010004",
          "intro": "AMS H The heater 1 is heating abnormally."
        },
        {
          "ecode": "0704210000020004",
          "intro": "AMS E Slot 2 filament may be broken in the tool head."
        },
        {
          "ecode": "0700210000020003",
          "intro": "AMS A Slot 2's filament may be broken in AMS."
        },
        {
          "ecode": "1802010000010004",
          "intro": "The AMS-HT C assist motor speed control is malfunctioning. The speed sensor may be faulty."
        },
        {
          "ecode": "1805200000020001",
          "intro": "AMS-HT F Slot 1 filament has run out. Please insert a new filament."
        },
        {
          "ecode": "1801120000020002",
          "intro": "The AMS-HT B slot 3 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "0705230000010081",
          "intro": "Failed to read the filament information from AMS F slot 4. The AMS main board may be malfunctioning."
        },
        {
          "ecode": "1803940000010001",
          "intro": "AMS-HT D The temperature sensor of heater 1 is malfunctioning, which may be due to poor connector contact."
        },
        {
          "ecode": "0701210000020007",
          "intro": "AMS B Slot 2 feed-out Hall sensor is disconnected. The connector may have poor contact."
        },
        {
          "ecode": "0706220000020011",
          "intro": "AMS G slot 3 pulls filament back to AMS timeout."
        },
        {
          "ecode": "1802210000020008",
          "intro": "AMS-HT C Slot 2 feed-in Hall sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "0700200000020004",
          "intro": "AMS A Slot 1 filament may be broken in the tool head."
        },
        {
          "ecode": "1201300000010004",
          "intro": "RFID cannot be read because of an encryption chip failure in AMS B."
        },
        {
          "ecode": "0700220000020022",
          "intro": "AMS A slot 3 assist motor is stalled，due to excessive resistance in the tube near the toolhead."
        },
        {
          "ecode": "0704220000020021",
          "intro": "AMS E slot 3 assist motor is stalled，due to excessive resistance in the tube between the filament buffer and the toolhead."
        },
        {
          "ecode": "0702220000010083",
          "intro": "Failed to read the filament information from AMS C slot 3. The RFID tag may be damaged."
        },
        {
          "ecode": "03000D0000010005",
          "intro": "The build plate is not placed properly. Please adjust it."
        },
        {
          "ecode": "1804230000010084",
          "intro": "Failed to read the filament information from AMS-HT E slot 4. The RFID tag may be damaged or positioned at the edge of the RFID detection device. Please remove 5cm filament and try again."
        },
        {
          "ecode": "1804010000020007",
          "intro": "AMS-HT E The assist motor encoder wires are not connected. The assist motor connector may have poor contact."
        },
        {
          "ecode": "0700220000010086",
          "intro": "Failed to read the filament information from AMS A slot 3. The RFID tag cannot rotate due to a jam during the filament loading or unloading. Please pull out the filament and try again."
        },
        {
          "ecode": "18FF600000020001",
          "intro": "External spool may be tangled or jammed."
        },
        {
          "ecode": "0707700000020007",
          "intro": "AMS filament ran out. Please put a new filament into the same slot in AMS and resume."
        },
        {
          "ecode": "0704010000010011",
          "intro": "AMS E The assist motor calibration parameter error. Please pull out the filament from the filament hub and then restart the AMS."
        },
        {
          "ecode": "0703220000010084",
          "intro": "Failed to read the filament information from AMS D slot 3. The RFID tag may be damaged or positioned at the edge of the RFID detection device. Please remove 5cm filament and try again."
        },
        {
          "ecode": "1805210000010085",
          "intro": "Failed to read the filament information from AMS-HT F slot 2. RFID tag verification failed. You can try to use Bambu Lab filament."
        },
        {
          "ecode": "0703100000010001",
          "intro": "The AMS D slot 1 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "1805220000020018",
          "intro": "AMS-HT F slot 3 assist motor is stalled，due to excessive resistance in the tube near AMS."
        },
        {
          "ecode": "1800200000010084",
          "intro": "Failed to read the filament information from AMS-HT A slot 1. The RFID tag may be damaged or positioned at the edge of the RFID detection device. Please remove 5cm filament and try again."
        },
        {
          "ecode": "1202230000020004",
          "intro": "AMS C Slot4 filament may be broken in the tool head."
        },
        {
          "ecode": "1806210000020011",
          "intro": "AMS-HT G slot 2 pulls filament back to AMS timeout."
        },
        {
          "ecode": "0701220000020022",
          "intro": "AMS B slot 3 assist motor is stalled，due to excessive resistance in the tube near the toolhead."
        },
        {
          "ecode": "1801200000030002",
          "intro": "AMS-HT B Slot 1 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "0700230000010081",
          "intro": "Failed to read the filament information from AMS A slot 4. The AMS main board may be malfunctioning."
        },
        {
          "ecode": "0706920000020002",
          "intro": "AMS G The cooling fan speed of heater 1 is too low, which could be due to excessive fan resistance."
        },
        {
          "ecode": "0705010000020011",
          "intro": "AMS F The motor assist parameter is lost. Please pull out the filament from the filament hub and then restart the AMS."
        },
        {
          "ecode": "1200220000020002",
          "intro": "AMS A Slot 3 is empty; please insert a new filament."
        },
        {
          "ecode": "1800230000020005",
          "intro": "AMS-HT A Slot 4 filament has run out, and purging the old filament went abnormally; please check whether the filament is stuck in the tool head."
        },
        {
          "ecode": "03000C0000010002",
          "intro": "The signal of heatbed force sensor 3 is weak. The force sensor may be broken or have poor electric connection."
        },
        {
          "ecode": "0706010000020011",
          "intro": "AMS G The motor assist parameter is lost. Please pull out the filament from the filament hub and then restart the AMS."
        },
        {
          "ecode": "1800700000020005",
          "intro": "Failed to feed the filament outside the AMS-HT. Please clip the end of the filament flat and check to see if the spool is stuck."
        },
        {
          "ecode": "0704700000020008",
          "intro": "Failed to get AMS mapping table; please select \"Resume\" to retry."
        },
        {
          "ecode": "0300200000010001",
          "intro": "X-axis homing abnormal: please check if the toolhead is stuck or the carbon rod resistance is too high."
        },
        {
          "ecode": "1800220000020002",
          "intro": "AMS-HT A Slot 3 is empty; please insert a new filament."
        },
        {
          "ecode": "1801200000010086",
          "intro": "Failed to read the filament information from AMS-HT B slot 1. The RFID tag cannot rotate due to a jam during the filament loading or unloading. Please pull out the filament and try again."
        },
        {
          "ecode": "0704700000020007",
          "intro": "AMS filament ran out. Please put a new filament into the same slot in AMS and resume."
        },
        {
          "ecode": "0701700000020003",
          "intro": "Failed to extrude the filament. Possible cause: extruder or nozzle clog."
        },
        {
          "ecode": "1800800000010003",
          "intro": "AMS-HT A The heater 1 is short-circuited, which may be due to a wiring short or heater damage."
        },
        {
          "ecode": "0705910000010003",
          "intro": "AMS F The exhaust valve 2 is not connected, which may be due to poor connector contact."
        },
        {
          "ecode": "1807310000020002",
          "intro": "The RFID-tag on AMS-HT H Slot2 is damaged, or its content cannot be identified."
        },
        {
          "ecode": "1804210000030001",
          "intro": "AMS-HT E Slot 2 filament has run out. Please wait while old filament is purged."
        },
        {
          "ecode": "1804210000020020",
          "intro": "AMS-HT E slot 2 assist motor is stalled，due to excessive resistance in the tube near the filament buffer。"
        },
        {
          "ecode": "1807320000020002",
          "intro": "The RFID-tag on AMS-HT H Slot3 is damaged, or its content cannot be identified."
        },
        {
          "ecode": "1200120000010003",
          "intro": "The AMS A Slot3 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "1202210000020006",
          "intro": "Failed to extrude AMS C Slot2 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "1802960000010001",
          "intro": "AMS-HT C The drying process may experience thermal runaway. Please turn off the AMS power supply."
        },
        {
          "ecode": "0703110000010003",
          "intro": "The AMS D slot 2 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "1802210000020024",
          "intro": "AMS-HT C slot 2 failed to rotate the filament spool when pulling filament back to AMS."
        },
        {
          "ecode": "0701230000020009",
          "intro": "Failed to extrude AMS B Slot 4 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "1802970000030001",
          "intro": "AMS-HT C chamber temperature is too high; auxiliary feeding or RFID reading is currently not allowed."
        },
        {
          "ecode": "1805500000020001",
          "intro": "AMS-HT F communication is abnormal; please check the connection cable."
        },
        {
          "ecode": "0703810000010001",
          "intro": "AMS D The current sensor of heater 2 is abnormal."
        },
        {
          "ecode": "1806810000010001",
          "intro": "AMS-HT G The current sensor of heater 2 is abnormal."
        },
        {
          "ecode": "0700210000020018",
          "intro": "AMS A slot 2 assist motor is stalled，due to excessive resistance in the tube near AMS."
        },
        {
          "ecode": "1804220000020001",
          "intro": "AMS-HT E Slot 3 filament has run out. Please insert a new filament."
        },
        {
          "ecode": "0707220000020020",
          "intro": "AMS H slot 3 assist motor is stalled，due to excessive resistance in the tube near the filament buffer。"
        },
        {
          "ecode": "03000C0000010001",
          "intro": "Heatbed force sensor 3 is too sensitive. It may be stuck between the strain arm and heatbed support, or the adjusting screw may be too tight."
        },
        {
          "ecode": "1804120000010001",
          "intro": "The AMS-HT E slot 3 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "1807220000010081",
          "intro": "Failed to read the filament information from AMS-HT H slot 3. The AMS main board may be malfunctioning."
        },
        {
          "ecode": "1805200000010083",
          "intro": "Failed to read the filament information from AMS-HT F slot 1. The RFID tag may be damaged."
        },
        {
          "ecode": "1202130000020002",
          "intro": "The AMS C Slot4 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "1804310000030003",
          "intro": "RFID cannot be read because of a hardware or structural error."
        },
        {
          "ecode": "1202310000020002",
          "intro": "The RFID-tag on AMS C Slot 2 is damaged."
        },
        {
          "ecode": "0702230000020002",
          "intro": "AMS C Slot 4 is empty; please insert a new filament."
        },
        {
          "ecode": "03000C0000010003",
          "intro": "The signal of heatbed force sensor 3 is too weak. The electronic connection to the sensor may be broken."
        },
        {
          "ecode": "0700210000020010",
          "intro": "AMS A slot 2 feeds filament out of AMS timeout."
        },
        {
          "ecode": "1802220000020004",
          "intro": "AMS-HT C Slot 3 filament may be broken in the tool head."
        },
        {
          "ecode": "0707220000020001",
          "intro": "AMS H Slot 3 filament has run out. Please insert a new filament."
        },
        {
          "ecode": "0703960000010003",
          "intro": "AMS D Unable to start drying; please pull out the filament from filament hub and try again."
        },
        {
          "ecode": "03000C0000010005",
          "intro": "Force sensor 3 detected unexpected continuous force. The heatbed may be stuck, or the analog front end may be broken."
        },
        {
          "ecode": "1802200000020011",
          "intro": "AMS-HT C slot 1 pulls filament back to AMS timeout."
        },
        {
          "ecode": "1804310000010001",
          "intro": "The AMS-HT E RFID 2 board has an error."
        },
        {
          "ecode": "1203230000020005",
          "intro": "AMS D Slot4 filament has run out, and purging the old filament went abnormally; please check to see if filament is stuck in the toolhead."
        },
        {
          "ecode": "0706200000020017",
          "intro": "AMS G slot 1 assist motor is stalled，due to excessive resistance in the tube between AMS and the printer."
        },
        {
          "ecode": "0500040000010002",
          "intro": "Failed to report print state; please check your network connection."
        },
        {
          "ecode": "1801200000030001",
          "intro": "AMS-HT B Slot 1 filament has run out. Please wait while old filament is purged."
        },
        {
          "ecode": "0C00030000020005",
          "intro": "First layer inspection timed out abnormally, and the current results may be inaccurate."
        },
        {
          "ecode": "1803210000020004",
          "intro": "AMS-HT D Slot 2 filament may be broken in the tool head."
        },
        {
          "ecode": "0705130000010001",
          "intro": "The AMS F slot 4 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "0707200000020001",
          "intro": "AMS H Slot 1 filament has run out. Please insert a new filament."
        },
        {
          "ecode": "1805230000020021",
          "intro": "AMS-HT F slot 4 assist motor is stalled，due to excessive resistance in the tube between the filament buffer and the toolhead."
        },
        {
          "ecode": "1804700000020005",
          "intro": "Failed to feed the filament outside the AMS-HT. Please clip the end of the filament flat and check to see if the spool is stuck."
        },
        {
          "ecode": "1805220000020009",
          "intro": "Failed to extrude AMS-HT F Slot 3 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "0700230000020005",
          "intro": "AMS A Slot 4 filament has run out, and purging the old filament went abnormally; please check whether the filament is stuck in the tool head."
        },
        {
          "ecode": "0706210000020008",
          "intro": "AMS G Slot 2 feed-in Hall sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "0702230000020011",
          "intro": "AMS C slot 4 pulls filament back to AMS timeout."
        },
        {
          "ecode": "1805230000020020",
          "intro": "AMS-HT F slot 4 assist motor is stalled，due to excessive resistance in the tube near the filament buffer。"
        },
        {
          "ecode": "0707230000020001",
          "intro": "AMS H Slot 4 filament has run out. Please insert a new filament."
        },
        {
          "ecode": "1804950000010001",
          "intro": "AMS-HT E The temperature sensor of heater 2 is malfunctioning, which may be due to poor connector contact."
        },
        {
          "ecode": "0705810000010001",
          "intro": "AMS F The current sensor of heater 2 is abnormal."
        },
        {
          "ecode": "0300040000020001",
          "intro": "The speed of the part cooling fan is too slow or stopped. It may be stuck, or the connector may not be plugged in properly."
        },
        {
          "ecode": "1804230000020005",
          "intro": "AMS-HT E Slot 4 filament has run out, and purging the old filament went abnormally; please check whether the filament is stuck in the tool head."
        },
        {
          "ecode": "0704210000020018",
          "intro": "AMS E slot 2 assist motor is stalled，due to excessive resistance in the tube near AMS."
        },
        {
          "ecode": "1201200000020003",
          "intro": "AMS B Slot1 filament may be broken in the PTFE tube."
        },
        {
          "ecode": "0706910000020001",
          "intro": "AMS G The operation of the exhaust valve 2 is abnormal, which may be due to excessive resistance."
        },
        {
          "ecode": "1804230000020001",
          "intro": "AMS-HT E Slot 4 filament has run out. Please insert a new filament."
        },
        {
          "ecode": "0706230000020022",
          "intro": "AMS G slot 4 assist motor is stalled，due to excessive resistance in the tube near the toolhead."
        },
        {
          "ecode": "1807350000010002",
          "intro": "AMS-HT H The humidity sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "1803120000020002",
          "intro": "The AMS-HT D slot 3 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "0705200000030001",
          "intro": "AMS F Slot 1 filament has run out. Please wait while old filament is purged."
        },
        {
          "ecode": "1203110000010001",
          "intro": "The AMS D Slot2 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "1800110000010003",
          "intro": "The AMS-HT A slot 2 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "0300020000010006",
          "intro": "The nozzle temperature is abnormal; the sensor may have a short circuit. Please check whether the connector is properly plugged in."
        },
        {
          "ecode": "0701010000010005",
          "intro": "AMS B The current sensor of assist motor may be faulty."
        },
        {
          "ecode": "0500040000020014",
          "intro": "The RFID-tag on AMS B Slot1 cannot be identified."
        },
        {
          "ecode": "1805210000020011",
          "intro": "AMS-HT F slot 2 pulls filament back to AMS timeout."
        },
        {
          "ecode": "0707200000020005",
          "intro": "AMS H Slot 1 filament has run out, and purging the old filament went abnormally; please check whether the filament is stuck in the tool head."
        },
        {
          "ecode": "0704220000010081",
          "intro": "Failed to read the filament information from AMS E slot 3. The AMS main board may be malfunctioning."
        },
        {
          "ecode": "1202230000030001",
          "intro": "AMS C Slot4 filament has run out. Purging the old filament; please wait."
        },
        {
          "ecode": "1800220000020001",
          "intro": "AMS-HT A Slot 3 filament has run out. Please insert a new filament."
        },
        {
          "ecode": "1800200000020020",
          "intro": "AMS-HT A slot 1 assist motor is stalled，due to excessive resistance in the tube near the filament buffer。"
        },
        {
          "ecode": "0703120000010003",
          "intro": "The AMS D slot 3 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "0700200000020002",
          "intro": "AMS A Slot 1 is empty; please insert a new filament."
        },
        {
          "ecode": "1803010000020010",
          "intro": "AMS-HT D The assist motor resistance is abnormal. The assist motor may be faulty."
        },
        {
          "ecode": "1805010000020007",
          "intro": "AMS-HT F The assist motor encoder wires are not connected. The assist motor connector may have poor contact."
        },
        {
          "ecode": "1807010000010003",
          "intro": "The AMS-HT H assist motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "1802920000010001",
          "intro": "AMS-HT C The cooling fan of heater 1 is blocked, which may be due to the fan being stuck."
        },
        {
          "ecode": "1802200000020010",
          "intro": "AMS-HT C slot 1 feeds filament out of AMS timeout."
        },
        {
          "ecode": "1801210000010085",
          "intro": "Failed to read the filament information from AMS-HT B slot 2. RFID tag verification failed. You can try to use Bambu Lab filament."
        },
        {
          "ecode": "0300010000010003",
          "intro": "The heatbed temperature is abnormal; the heater is over temperature."
        },
        {
          "ecode": "1802560000030001",
          "intro": "AMS-HT C is undergoing dry cooling; please wait for it to cool down before operating."
        },
        {
          "ecode": "1800010000010001",
          "intro": "The AMS-HT A assist motor has slipped. The extrusion wheel may be worn down, or the filament may be too thin."
        },
        {
          "ecode": "1804230000020007",
          "intro": "AMS-HT E Slot 4 feed-out Hall sensor is disconnected. The connector may have poor contact."
        },
        {
          "ecode": "0702700000020002",
          "intro": "Failed to feed the filament into the toolhead. Possible cause: filament or spool stuck."
        },
        {
          "ecode": "1804220000030001",
          "intro": "AMS-HT E Slot 3 filament has run out. Please wait while old filament is purged."
        },
        {
          "ecode": "0704200000010083",
          "intro": "Failed to read the filament information from AMS E slot 1. The RFID tag may be damaged."
        },
        {
          "ecode": "1805230000020010",
          "intro": "AMS-HT F slot 4 feeds filament out of AMS timeout."
        },
        {
          "ecode": "1803230000020011",
          "intro": "AMS-HT D slot 4 pulls filament back to AMS timeout."
        },
        {
          "ecode": "0707220000020009",
          "intro": "Failed to extrude AMS H Slot 3 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "0705010000020007",
          "intro": "AMS F The assist motor encoder wires are not connected. The assist motor connector may have poor contact."
        },
        {
          "ecode": "1201220000020003",
          "intro": "AMS B Slot3 filament may be broken in the PTFE tube."
        },
        {
          "ecode": "1200210000020002",
          "intro": "AMS A Slot 2 is empty; please insert a new filament."
        },
        {
          "ecode": "1800220000030002",
          "intro": "AMS-HT A Slot 3 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "0707210000020005",
          "intro": "AMS H Slot 2 filament has run out, and purging the old filament went abnormally; please check whether the filament is stuck in the tool head."
        },
        {
          "ecode": "1800230000020008",
          "intro": "AMS-HT A Slot 4 feed-in Hall sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "0704220000020017",
          "intro": "AMS E slot 3 assist motor is stalled，due to excessive resistance in the tube between AMS and the printer."
        },
        {
          "ecode": "0707310000030003",
          "intro": "RFID cannot be read because of a hardware or structural error."
        },
        {
          "ecode": "1800400000020003",
          "intro": "The AMS Hub communication is abnormal; the cable may be not well connected."
        },
        {
          "ecode": "0705210000020018",
          "intro": "AMS F slot 2 assist motor is stalled，due to excessive resistance in the tube near AMS."
        },
        {
          "ecode": "1801240000020009",
          "intro": "AMS-HT B front cover is open. This may affect the drying performance or cause the filament to absorb moisture."
        },
        {
          "ecode": "1807010000010005",
          "intro": "AMS-HT H The current sensor of assist motor may be faulty."
        },
        {
          "ecode": "0702220000030002",
          "intro": "AMS C Slot 3 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "0703010000020007",
          "intro": "AMS D The assist motor encoder wires are not connected. The assist motor connector may have poor contact."
        },
        {
          "ecode": "0701200000030001",
          "intro": "AMS B Slot 1 filament has run out. Please wait while old filament is purged."
        },
        {
          "ecode": "1800220000020005",
          "intro": "AMS-HT A Slot 3 filament has run out, and purging the old filament went abnormally; please check whether the filament is stuck in the tool head."
        },
        {
          "ecode": "0706700000020008",
          "intro": "Failed to get AMS mapping table; please select \"Resume\" to retry."
        },
        {
          "ecode": "1805210000020002",
          "intro": "AMS-HT F Slot 2 is empty; please insert a new filament."
        },
        {
          "ecode": "0701900000010003",
          "intro": "AMS B The exhaust valve 1 is not connected, which may be due to poor connector contact."
        },
        {
          "ecode": "0702210000020009",
          "intro": "Failed to extrude AMS C Slot 2 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "1807200000020008",
          "intro": "AMS-HT H Slot 1 feed-in Hall sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "1806230000020018",
          "intro": "AMS-HT G slot 4 assist motor is stalled，due to excessive resistance in the tube near AMS."
        },
        {
          "ecode": "0705130000020004",
          "intro": "AMS F The brushed motor 4 has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "0702110000010001",
          "intro": "The AMS C slot 2 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "1806230000010084",
          "intro": "Failed to read the filament information from AMS-HT G slot 4. The RFID tag may be damaged or positioned at the edge of the RFID detection device. Please remove 5cm filament and try again."
        },
        {
          "ecode": "0703970000030001",
          "intro": "AMS D chamber temperature is too high; auxiliary feeding or RFID reading is currently not allowed."
        },
        {
          "ecode": "1804100000010001",
          "intro": "The AMS-HT E slot 1 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "0C00010000020007",
          "intro": "Micro Lidar laser parameters have drifted. Please re-calibrate your printer."
        },
        {
          "ecode": "1200300000030003",
          "intro": "AMS A Slot1 RFID cannot be read because of a structural error."
        },
        {
          "ecode": "0703020000020002",
          "intro": "AMS D The odometer has no signal. The odometer connector may have poor contact."
        },
        {
          "ecode": "0701110000020004",
          "intro": "AMS B The brushed motor 2 has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "0700220000030001",
          "intro": "AMS A Slot 3 filament has run out. Please wait while old filament is purged."
        },
        {
          "ecode": "1802800000010004",
          "intro": "AMS-HT C The heater 1 is heating abnormally."
        },
        {
          "ecode": "1805220000020010",
          "intro": "AMS-HT F slot 3 feeds filament out of AMS timeout."
        },
        {
          "ecode": "0705210000020024",
          "intro": "AMS F slot 2 failed to rotate the filament spool when pulling filament back to AMS."
        },
        {
          "ecode": "0701230000020020",
          "intro": "AMS B slot 4 assist motor is stalled，due to excessive resistance in the tube near the filament buffer。"
        },
        {
          "ecode": "1801700000020001",
          "intro": "Failed to pull out the filament from the extruder. Possible causes: clogged extruder or broken filament."
        },
        {
          "ecode": "0704020000010001",
          "intro": "AMS E Filament speed and length error: The filament odometry may be faulty."
        },
        {
          "ecode": "0704200000010085",
          "intro": "Failed to read the filament information from AMS E slot 1. RFID tag verification failed. You can try to use Bambu Lab filament."
        },
        {
          "ecode": "1801960000020002",
          "intro": "AMS-HT B Environmental temperature is too low, which will affect the drying capability."
        },
        {
          "ecode": "0702100000010001",
          "intro": "The AMS C slot 1 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "0700200000010081",
          "intro": "Failed to read the filament information from AMS A slot 1. The AMS main board may be malfunctioning."
        },
        {
          "ecode": "1201200000020005",
          "intro": "AMS B Slot1 filament has run out, and purging the old filament went abnormally; please check to see if filament is stuck in the toolhead."
        },
        {
          "ecode": "0707110000010001",
          "intro": "The AMS H slot 2 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "1805220000020019",
          "intro": "AMS-HT F slot 3 assist motor is stalled，due to excessive resistance in the tube between AMS and the filament buffer."
        },
        {
          "ecode": "0703230000020002",
          "intro": "AMS D Slot 4 is empty; please insert a new filament."
        },
        {
          "ecode": "0707900000020001",
          "intro": "AMS H The operation of the exhaust valve 1 is abnormal, which may be due to excessive resistance."
        },
        {
          "ecode": "1800210000020005",
          "intro": "AMS-HT A Slot 2 filament has run out, and purging the old filament went abnormally; please check whether the filament is stuck in the tool head."
        },
        {
          "ecode": "1203100000010003",
          "intro": "The AMS D Slot1 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "0705320000020002",
          "intro": "The RFID-tag on AMS F Slot3 is damaged, or its content cannot be identified."
        },
        {
          "ecode": "0706220000020024",
          "intro": "AMS G slot 3 failed to rotate the filament spool when pulling filament back to AMS."
        },
        {
          "ecode": "1804210000020022",
          "intro": "AMS-HT E slot 2 assist motor is stalled，due to excessive resistance in the tube near the toolhead."
        },
        {
          "ecode": "1802210000020020",
          "intro": "AMS-HT C slot 2 assist motor is stalled，due to excessive resistance in the tube near the filament buffer。"
        },
        {
          "ecode": "0704230000010081",
          "intro": "Failed to read the filament information from AMS E slot 4. The AMS main board may be malfunctioning."
        },
        {
          "ecode": "0701220000020008",
          "intro": "AMS B Slot 3 feed-in Hall sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "030092000001000A",
          "intro": "The temperature of chamber heater 2 is abnormal. The AC board may be broken."
        },
        {
          "ecode": "0704110000010001",
          "intro": "The AMS E slot 2 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "0705200000020019",
          "intro": "AMS F slot 1 assist motor is stalled，due to excessive resistance in the tube between AMS and the filament buffer."
        },
        {
          "ecode": "1803560000030001",
          "intro": "AMS-HT D is undergoing dry cooling; please wait for it to cool down before operating."
        },
        {
          "ecode": "0703220000020004",
          "intro": "AMS D Slot 3 filament may be broken in the tool head."
        },
        {
          "ecode": "1806230000020004",
          "intro": "AMS-HT G Slot 4 filament may be broken in the tool head."
        },
        {
          "ecode": "1202210000030001",
          "intro": "AMS C Slot2 filament has run out. Purging the old filament; please wait."
        },
        {
          "ecode": "1801230000020019",
          "intro": "AMS-HT B slot 4 assist motor is stalled，due to excessive resistance in the tube between AMS and the filament buffer."
        },
        {
          "ecode": "1201200000020001",
          "intro": "AMS B Slot1 filament has run out; please insert a new filament."
        },
        {
          "ecode": "0701230000020017",
          "intro": "AMS B slot 4 assist motor is stalled，due to excessive resistance in the tube between AMS and the printer."
        },
        {
          "ecode": "1803230000020017",
          "intro": "AMS-HT D slot 4 assist motor is stalled，due to excessive resistance in the tube between AMS and the printer."
        },
        {
          "ecode": "1804130000010001",
          "intro": "The AMS-HT E slot 4 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "1200120000020002",
          "intro": "The AMS A Slot3 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "1800240000020009",
          "intro": "AMS-HT A front cover is open. This may affect the drying performance or cause the filament to absorb moisture."
        },
        {
          "ecode": "1800200000020018",
          "intro": "AMS-HT A slot 1 assist motor is stalled，due to excessive resistance in the tube near AMS."
        },
        {
          "ecode": "0705810000010003",
          "intro": "AMS F The heater 2 is short-circuited, which may be due to a wiring short or heater damage."
        },
        {
          "ecode": "1202310000030003",
          "intro": "AMS C Slot2 RFID cannot be read because of a structural error."
        },
        {
          "ecode": "1802910000020001",
          "intro": "AMS-HT C The operation of the exhaust valve 2 is abnormal, which may be due to excessive resistance."
        },
        {
          "ecode": "1807230000020010",
          "intro": "AMS-HT H slot 4 feeds filament out of AMS timeout."
        },
        {
          "ecode": "0700020000020002",
          "intro": "AMS A The odometer has no signal. The odometer connector may have poor contact."
        },
        {
          "ecode": "0702810000010001",
          "intro": "AMS C The current sensor of heater 2 is abnormal."
        },
        {
          "ecode": "1801010000020009",
          "intro": "AMS-HT B The assist motor has unbalanced tree-phase resistaance. The assist motor may be faulty."
        },
        {
          "ecode": "0706130000020002",
          "intro": "The AMS G slot 4 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "0C00030000020001",
          "intro": "Filament exposure metering failed because laser reflection is too weak on this material. First layer inspection may be inaccurate."
        },
        {
          "ecode": "0706810000010003",
          "intro": "AMS G The heater 2 is short-circuited, which may be due to a wiring short or heater damage."
        },
        {
          "ecode": "1807120000010003",
          "intro": "The AMS-HT H slot 3 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "1804200000020021",
          "intro": "AMS-HT E slot 1 assist motor is stalled，due to excessive resistance in the tube between the filament buffer and the toolhead."
        },
        {
          "ecode": "1803220000020002",
          "intro": "AMS-HT D Slot 3 is empty; please insert a new filament."
        },
        {
          "ecode": "0702130000010001",
          "intro": "The AMS C slot 4 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "1805210000030001",
          "intro": "AMS-HT F Slot 2 filament has run out. Please wait while old filament is purged."
        },
        {
          "ecode": "0704230000020018",
          "intro": "AMS E slot 4 assist motor is stalled，due to excessive resistance in the tube near AMS."
        },
        {
          "ecode": "1801220000020022",
          "intro": "AMS-HT B slot 3 assist motor is stalled，due to excessive resistance in the tube near the toolhead."
        },
        {
          "ecode": "0700010000020006",
          "intro": "AMS A The assist motor three-phase wires are not connected. The assist motor connector may have poor contact."
        },
        {
          "ecode": "1202830000020001",
          "intro": "AMS C Slot4 filament may be tangled or stuck."
        },
        {
          "ecode": "0701210000020022",
          "intro": "AMS B slot 2 assist motor is stalled，due to excessive resistance in the tube near the toolhead."
        },
        {
          "ecode": "1807960000010001",
          "intro": "AMS-HT H The drying process may experience thermal runaway. Please turn off the AMS power supply."
        },
        {
          "ecode": "0701220000020021",
          "intro": "AMS B slot 3 assist motor is stalled，due to excessive resistance in the tube between the filament buffer and the toolhead."
        },
        {
          "ecode": "0703220000010081",
          "intro": "Failed to read the filament information from AMS D slot 3. The AMS main board may be malfunctioning."
        },
        {
          "ecode": "0701330000020002",
          "intro": "The RFID-tag on AMS B Slot4 is damaged, or its content cannot be identified."
        },
        {
          "ecode": "0701220000020001",
          "intro": "AMS B Slot 3 filament has run out. Please insert a new filament."
        },
        {
          "ecode": "1806210000020020",
          "intro": "AMS-HT G slot 2 assist motor is stalled，due to excessive resistance in the tube near the filament buffer。"
        },
        {
          "ecode": "03001B0000010003",
          "intro": "The heatbed acceleration sensor detected unexpected continuous force. The sensor may be stuck, or the analog front end may be broken."
        },
        {
          "ecode": "1802230000010084",
          "intro": "Failed to read the filament information from AMS-HT C slot 4. The RFID tag may be damaged or positioned at the edge of the RFID detection device. Please remove 5cm filament and try again."
        },
        {
          "ecode": "1801010000020008",
          "intro": "AMS-HT B The assist motor phase winding has an open circuit. The assist motor may be faulty."
        },
        {
          "ecode": "1802220000020001",
          "intro": "AMS-HT C Slot 3 filament has run out. Please insert a new filament."
        },
        {
          "ecode": "1803230000020022",
          "intro": "AMS-HT D slot 4 assist motor is stalled，due to excessive resistance in the tube near the toolhead."
        },
        {
          "ecode": "0705230000020018",
          "intro": "AMS F slot 4 assist motor is stalled，due to excessive resistance in the tube near AMS."
        },
        {
          "ecode": "1802800000010003",
          "intro": "AMS-HT C The heater 1 is short-circuited, which may be due to a wiring short or heater damage."
        },
        {
          "ecode": "0705930000010001",
          "intro": "AMS F The cooling fan of heater 2 is blocked, which may be due to the fan being stuck."
        },
        {
          "ecode": "0703960000020002",
          "intro": "AMS D Environmental temperature is too low, which will affect the drying capability."
        },
        {
          "ecode": "0707200000020019",
          "intro": "AMS H slot 1 assist motor is stalled，due to excessive resistance in the tube between AMS and the filament buffer."
        },
        {
          "ecode": "0700300000010004",
          "intro": "Encryption chip failure"
        },
        {
          "ecode": "1807900000020001",
          "intro": "AMS-HT H The operation of the exhaust valve 1 is abnormal, which may be due to excessive resistance."
        },
        {
          "ecode": "1801100000010003",
          "intro": "The AMS-HT B slot 1 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "1201210000030002",
          "intro": "AMS B Slot2 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "1803220000020007",
          "intro": "AMS-HT D Slot 3 feed-out Hall sensor is disconnected. The connector may have poor contact."
        },
        {
          "ecode": "1800220000020004",
          "intro": "AMS-HT A Slot 3 filament may be broken in the tool head."
        },
        {
          "ecode": "0701900000020001",
          "intro": "AMS B The operation of the exhaust valve 1 is abnormal, which may be due to excessive resistance."
        },
        {
          "ecode": "1201130000010003",
          "intro": "The AMS B Slot4 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "0707210000010081",
          "intro": "Failed to read the filament information from AMS H slot 2. The AMS main board may be malfunctioning."
        },
        {
          "ecode": "1800800000010004",
          "intro": "AMS-HT A The heater 1 is heating abnormally."
        },
        {
          "ecode": "1805110000020004",
          "intro": "AMS-HT F The brushed motor 2 has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "0C00030000010009",
          "intro": "The first layer inspection module rebooted abnormally. The inspection result may be inaccurate."
        },
        {
          "ecode": "0703010000020006",
          "intro": "AMS D The assist motor three-phase wires are not connected. The assist motor connector may have poor contact."
        },
        {
          "ecode": "0700220000010085",
          "intro": "Failed to read the filament information from AMS A slot 3. RFID tag verification failed. You can try to use Bambu Lab filament."
        },
        {
          "ecode": "0707220000010084",
          "intro": "Failed to read the filament information from AMS H slot 3. The RFID tag may be damaged or positioned at the edge of the RFID detection device. Please remove 5cm filament and try again."
        },
        {
          "ecode": "0703200000020021",
          "intro": "AMS D slot 1 assist motor is stalled，due to excessive resistance in the tube between the filament buffer and the toolhead."
        },
        {
          "ecode": "030001000001000D",
          "intro": "An abnormality occured in heating modules of heatbed previously. To continue using your printer, please refer to the wiki to troubleshoot."
        },
        {
          "ecode": "0706220000030002",
          "intro": "AMS G Slot 3 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "1807200000020020",
          "intro": "AMS-HT H slot 1 assist motor is stalled，due to excessive resistance in the tube near the filament buffer。"
        },
        {
          "ecode": "03000B0000010004",
          "intro": "An external disturbance was detected on force sensor 2. The heatbed plate may have touched something outside the heatbed."
        },
        {
          "ecode": "1804230000010086",
          "intro": "Failed to read the filament information from AMS-HT E slot 4. The RFID tag cannot rotate due to a jam during the filament loading or unloading. Please pull out the filament and try again."
        },
        {
          "ecode": "0300010000030008",
          "intro": "The temperature of the heated bed exceeds the limit and automatically adjusts to the limit temperature."
        },
        {
          "ecode": "1801230000020011",
          "intro": "AMS-HT B slot 4 pulls filament back to AMS timeout."
        },
        {
          "ecode": "1806210000020024",
          "intro": "AMS-HT G slot 2 failed to rotate the filament spool when pulling filament back to AMS."
        },
        {
          "ecode": "0707100000010003",
          "intro": "The AMS H slot 1 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "0700210000010081",
          "intro": "Failed to read the filament information from AMS A slot 2. The AMS main board may be malfunctioning."
        },
        {
          "ecode": "1802120000010003",
          "intro": "The AMS-HT C slot 3 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "1801350000010001",
          "intro": "The temperature and humidity sensor has an error. The chip may be faulty."
        },
        {
          "ecode": "0700350000010001",
          "intro": "The temperature and humidity sensor has an error. The chip may be faulty."
        },
        {
          "ecode": "1806110000020002",
          "intro": "The AMS-HT G slot 2 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "1800010000020010",
          "intro": "AMS-HT A The assist motor resistance is abnormal. The assist motor may be faulty."
        },
        {
          "ecode": "0700970000030001",
          "intro": "AMS A chamber temperature is too high; auxiliary feeding or RFID reading is currently not allowed."
        },
        {
          "ecode": "1802220000030001",
          "intro": "AMS-HT C Slot 3 filament has run out. Please wait while old filament is purged."
        },
        {
          "ecode": "1801130000020002",
          "intro": "The AMS-HT B slot 4 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "1801800000010001",
          "intro": "AMS-HT B The current sensor of heater 1 is abnormal."
        },
        {
          "ecode": "0702200000020007",
          "intro": "AMS C Slot 1 feed-out Hall sensor is disconnected. The connector may have poor contact."
        },
        {
          "ecode": "0700900000020001",
          "intro": "AMS A The operation of the exhaust valve 1 is abnormal, which may be due to excessive resistance."
        },
        {
          "ecode": "1201110000010003",
          "intro": "The AMS B Slot2 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "0500040000020015",
          "intro": "The RFID-tag on AMS B Slot2 cannot be identified."
        },
        {
          "ecode": "1801230000020018",
          "intro": "AMS-HT B slot 4 assist motor is stalled，due to excessive resistance in the tube near AMS."
        },
        {
          "ecode": "1805970000030001",
          "intro": "AMS-HT F chamber temperature is too high; auxiliary feeding or RFID reading is currently not allowed."
        },
        {
          "ecode": "1802310000010001",
          "intro": "The AMS-HT C RFID 2 board has an error."
        },
        {
          "ecode": "0706300000010001",
          "intro": "The AMS G RFID 1 board has an error."
        },
        {
          "ecode": "0705960000010003",
          "intro": "AMS F Unable to start drying; please pull out the filament from filament hub and try again."
        },
        {
          "ecode": "0707220000020002",
          "intro": "AMS H Slot 3 is empty; please insert a new filament."
        },
        {
          "ecode": "0702010000020007",
          "intro": "AMS C The assist motor encoder wires are not connected. The assist motor connector may have poor contact."
        },
        {
          "ecode": "1800230000020004",
          "intro": "AMS-HT A Slot 4 filament may be broken in the tool head."
        },
        {
          "ecode": "0707120000010001",
          "intro": "The AMS H slot 3 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "1803220000020018",
          "intro": "AMS-HT D slot 3 assist motor is stalled，due to excessive resistance in the tube near AMS."
        },
        {
          "ecode": "1804230000020011",
          "intro": "AMS-HT E slot 4 pulls filament back to AMS timeout."
        },
        {
          "ecode": "1802200000010081",
          "intro": "Failed to read the filament information from AMS-HT C slot 1. The AMS main board may be malfunctioning."
        },
        {
          "ecode": "1802200000010083",
          "intro": "Failed to read the filament information from AMS-HT C slot 1. The RFID tag may be damaged."
        },
        {
          "ecode": "1804010000010001",
          "intro": "The AMS-HT E assist motor has slipped. The extrusion wheel may be worn down, or the filament may be too thin."
        },
        {
          "ecode": "1806300000020002",
          "intro": "The RFID-tag on AMS-HT G Slot1 is damaged, or its content cannot be identified."
        },
        {
          "ecode": "0701200000010083",
          "intro": "Failed to read the filament information from AMS B slot 1. The RFID tag may be damaged."
        },
        {
          "ecode": "1803200000020011",
          "intro": "AMS-HT D slot 1 pulls filament back to AMS timeout."
        },
        {
          "ecode": "0700110000010001",
          "intro": "The AMS A slot 2 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "0702220000010085",
          "intro": "Failed to read the filament information from AMS C slot 3. RFID tag verification failed. You can try to use Bambu Lab filament."
        },
        {
          "ecode": "1804210000020005",
          "intro": "AMS-HT E Slot 2 filament has run out, and purging the old filament went abnormally; please check whether the filament is stuck in the tool head."
        },
        {
          "ecode": "1201210000020004",
          "intro": "AMS B Slot2 filament may be broken in the tool head."
        },
        {
          "ecode": "1806920000010001",
          "intro": "AMS-HT G The cooling fan of heater 1 is blocked, which may be due to the fan being stuck."
        },
        {
          "ecode": "0703920000020002",
          "intro": "AMS D The cooling fan speed of heater 1 is too low, which could be due to excessive fan resistance."
        },
        {
          "ecode": "0705010000010011",
          "intro": "AMS F The assist motor calibration parameter error. Please pull out the filament from the filament hub and then restart the AMS."
        },
        {
          "ecode": "0705120000020002",
          "intro": "The AMS F slot 3 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "0704800000010003",
          "intro": "AMS E The heater 1 is short-circuited, which may be due to a wiring short or heater damage."
        },
        {
          "ecode": "0300920000010002",
          "intro": "The temperature of chamber heater 2 is abnormal. The heater may have an open circuit or the thermal fuse may be in effect."
        },
        {
          "ecode": "1805200000010085",
          "intro": "Failed to read the filament information from AMS-HT F slot 1. RFID tag verification failed. You can try to use Bambu Lab filament."
        },
        {
          "ecode": "1803100000010003",
          "intro": "The AMS-HT D slot 1 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "0702200000020021",
          "intro": "AMS C slot 1 assist motor is stalled，due to excessive resistance in the tube between the filament buffer and the toolhead."
        },
        {
          "ecode": "1807220000020022",
          "intro": "AMS-HT H slot 3 assist motor is stalled，due to excessive resistance in the tube near the toolhead."
        },
        {
          "ecode": "1807020000020002",
          "intro": "AMS-HT H The odometer has no signal. The odometer connector may have poor contact."
        },
        {
          "ecode": "1804100000010003",
          "intro": "The AMS-HT E slot 1 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "0703220000020007",
          "intro": "AMS D Slot 3 feed-out Hall sensor is disconnected. The connector may have poor contact."
        },
        {
          "ecode": "0701110000010003",
          "intro": "The AMS B slot 2 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "1807200000020022",
          "intro": "AMS-HT H slot 1 assist motor is stalled，due to excessive resistance in the tube near the toolhead."
        },
        {
          "ecode": "1806310000020002",
          "intro": "The RFID-tag on AMS-HT G Slot2 is damaged, or its content cannot be identified."
        },
        {
          "ecode": "0300910000010006",
          "intro": "The temperature of chamber heater 1 is abnormal. The sensor may have a short circuit."
        },
        {
          "ecode": "0700310000030003",
          "intro": "RFID cannot be read because of a hardware or structural error."
        },
        {
          "ecode": "1201220000020002",
          "intro": "AMS B Slot 3 is empty; please insert a new filament."
        },
        {
          "ecode": "1203720000010001",
          "intro": "AMS D Filament speed and length error: The slot 3 filament odometry may be faulty."
        },
        {
          "ecode": "1807300000020002",
          "intro": "The RFID-tag on AMS-HT H Slot1 is damaged, or its content cannot be identified."
        },
        {
          "ecode": "12FF200000020004",
          "intro": "Please pull the filament on the spool holder out from the extruder."
        },
        {
          "ecode": "1805010000020009",
          "intro": "AMS-HT F The assist motor has unbalanced tree-phase resistaance. The assist motor may be faulty."
        },
        {
          "ecode": "0705200000020007",
          "intro": "AMS F Slot 1 feed-out Hall sensor is disconnected. The connector may have poor contact."
        },
        {
          "ecode": "1203210000020001",
          "intro": "AMS D Slot2 filament has run out; please insert a new filament."
        },
        {
          "ecode": "1807230000030002",
          "intro": "AMS-HT H Slot 4 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "1800130000020002",
          "intro": "The AMS-HT A slot 4 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "0707210000020022",
          "intro": "AMS H slot 2 assist motor is stalled，due to excessive resistance in the tube near the toolhead."
        },
        {
          "ecode": "1804230000010085",
          "intro": "Failed to read the filament information from AMS-HT E slot 4. RFID tag verification failed. You can try to use Bambu Lab filament."
        },
        {
          "ecode": "1801970000030001",
          "intro": "AMS-HT B chamber temperature is too high; auxiliary feeding or RFID reading is currently not allowed."
        },
        {
          "ecode": "03000A0000010002",
          "intro": "The signal of heatbed force sensor 1 is weak. The force sensor may be broken or have poor electric connection."
        },
        {
          "ecode": "0706220000020004",
          "intro": "AMS G Slot 3 filament may be broken in the tool head."
        },
        {
          "ecode": "0705220000030001",
          "intro": "AMS F Slot 3 filament has run out. Please wait while old filament is purged."
        },
        {
          "ecode": "0707810000010004",
          "intro": "AMS H The heater 2 is heating abnormally."
        },
        {
          "ecode": "0705230000020024",
          "intro": "AMS F slot 4 failed to rotate the filament spool when pulling filament back to AMS."
        },
        {
          "ecode": "1800230000020010",
          "intro": "AMS-HT A slot 4 feeds filament out of AMS timeout."
        },
        {
          "ecode": "0701200000020024",
          "intro": "AMS B slot 1 failed to rotate the filament spool when pulling filament back to AMS."
        },
        {
          "ecode": "1802200000030001",
          "intro": "AMS-HT C Slot 1 filament has run out. Please wait while old filament is purged."
        },
        {
          "ecode": "0702700000020003",
          "intro": "Failed to extrude the filament. Possible cause: extruder or nozzle clog."
        },
        {
          "ecode": "1804220000020004",
          "intro": "AMS-HT E Slot 3 filament may be broken in the tool head."
        },
        {
          "ecode": "0705010000010003",
          "intro": "The AMS F assist motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "1804210000020003",
          "intro": "AMS-HT E Slot 2's filament may be broken in AMS-HT."
        },
        {
          "ecode": "1800400000020002",
          "intro": "Filament buffer position signal error: the position sensor may be malfunctioning."
        },
        {
          "ecode": "0701700000020006",
          "intro": "Timeout purging old filament. Possible cause: filament stuck or the extruder/nozzle clog."
        },
        {
          "ecode": "0703700000020002",
          "intro": "Failed to feed the filament into the toolhead. Possible cause: filament or spool stuck."
        },
        {
          "ecode": "1807210000010085",
          "intro": "Failed to read the filament information from AMS-HT H slot 2. RFID tag verification failed. You can try to use Bambu Lab filament."
        },
        {
          "ecode": "1806350000010002",
          "intro": "AMS-HT G The humidity sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "1200200000020003",
          "intro": "AMS A Slot1 filament may be broken in the PTFE tube."
        },
        {
          "ecode": "1202230000020003",
          "intro": "AMS C Slot4 filament may be broken in the PTFE tube."
        },
        {
          "ecode": "0704200000020020",
          "intro": "AMS E slot 1 assist motor is stalled，due to excessive resistance in the tube near the filament buffer。"
        },
        {
          "ecode": "1800100000010003",
          "intro": "The AMS-HT A slot 1 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "0703900000020001",
          "intro": "AMS D The operation of the exhaust valve 1 is abnormal, which may be due to excessive resistance."
        },
        {
          "ecode": "0707220000010083",
          "intro": "Failed to read the filament information from AMS H slot 3. The RFID tag may be damaged."
        },
        {
          "ecode": "1804220000020022",
          "intro": "AMS-HT E slot 3 assist motor is stalled，due to excessive resistance in the tube near the toolhead."
        },
        {
          "ecode": "12FF200000020002",
          "intro": "Filament on the spool holder is empty; please insert a new filament."
        },
        {
          "ecode": "0700320000020002",
          "intro": "The RFID-tag on AMS A Slot3 is damaged, or its content cannot be identified."
        },
        {
          "ecode": "1807230000010083",
          "intro": "Failed to read the filament information from AMS-HT H slot 4. The RFID tag may be damaged."
        },
        {
          "ecode": "0704800000010002",
          "intro": "AMS E The heater 1 is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "1805800000010004",
          "intro": "AMS-HT F The heater 1 is heating abnormally."
        },
        {
          "ecode": "1804310000010004",
          "intro": "Encryption chip failure"
        },
        {
          "ecode": "1201830000020001",
          "intro": "AMS B Slot4 filament may be tangled or stuck."
        },
        {
          "ecode": "0701210000030001",
          "intro": "AMS B Slot 2 filament has run out. Please wait while old filament is purged."
        },
        {
          "ecode": "0701010000010004",
          "intro": "The AMS B assist motor speed control is malfunctioning. The speed sensor may be faulty."
        },
        {
          "ecode": "1803240000020009",
          "intro": "AMS-HT D front cover is open. This may affect the drying performance or cause the filament to absorb moisture."
        },
        {
          "ecode": "0706220000030001",
          "intro": "AMS G Slot 3 filament has run out. Please wait while old filament is purged."
        },
        {
          "ecode": "1800010000020002",
          "intro": "The AMS-HT A assist motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "1807010000010004",
          "intro": "The AMS-HT H assist motor speed control is malfunctioning. The speed sensor may be faulty."
        },
        {
          "ecode": "0704010000010001",
          "intro": "The AMS E assist motor has slipped. The extrusion wheel may be worn down, or the filament may be too thin."
        },
        {
          "ecode": "1806210000020019",
          "intro": "AMS-HT G slot 2 assist motor is stalled，due to excessive resistance in the tube between AMS and the filament buffer."
        },
        {
          "ecode": "0700950000010001",
          "intro": "AMS A The temperature sensor of heater 2 is malfunctioning, which may be due to poor connector contact."
        },
        {
          "ecode": "1805220000020007",
          "intro": "AMS-HT F Slot 3 feed-out Hall sensor is disconnected. The connector may have poor contact."
        },
        {
          "ecode": "1805230000020001",
          "intro": "AMS-HT F Slot 4 filament has run out. Please insert a new filament."
        },
        {
          "ecode": "0700700000020005",
          "intro": "Failed to feed the filament outside the AMS. Please clip the end of the filament flat and check to see if the spool is stuck."
        },
        {
          "ecode": "1801200000020018",
          "intro": "AMS-HT B slot 1 assist motor is stalled，due to excessive resistance in the tube near AMS."
        },
        {
          "ecode": "1804960000010001",
          "intro": "AMS-HT E The drying process may experience thermal runaway. Please turn off the AMS power supply."
        },
        {
          "ecode": "0704200000020018",
          "intro": "AMS E slot 1 assist motor is stalled，due to excessive resistance in the tube near AMS."
        },
        {
          "ecode": "1800210000010083",
          "intro": "Failed to read the filament information from AMS-HT A slot 2. The RFID tag may be damaged."
        },
        {
          "ecode": "0701230000020019",
          "intro": "AMS B slot 4 assist motor is stalled，due to excessive resistance in the tube between AMS and the filament buffer."
        },
        {
          "ecode": "1804300000020002",
          "intro": "The RFID-tag on AMS-HT E Slot1 is damaged, or its content cannot be identified."
        },
        {
          "ecode": "1800800000010001",
          "intro": "AMS-HT A The current sensor of heater 1 is abnormal."
        },
        {
          "ecode": "1801220000010084",
          "intro": "Failed to read the filament information from AMS-HT B slot 3. The RFID tag may be damaged or positioned at the edge of the RFID detection device. Please remove 5cm filament and try again."
        },
        {
          "ecode": "0706010000020010",
          "intro": "AMS G The assist motor resistance is abnormal. The assist motor may be faulty."
        },
        {
          "ecode": "1807210000020018",
          "intro": "AMS-HT H slot 2 assist motor is stalled，due to excessive resistance in the tube near AMS."
        },
        {
          "ecode": "0700230000010083",
          "intro": "Failed to read the filament information from AMS A slot 4. The RFID tag may be damaged."
        },
        {
          "ecode": "1201220000020001",
          "intro": "AMS B Slot3 filament has run out; please insert a new filament."
        },
        {
          "ecode": "1803210000030001",
          "intro": "AMS-HT D Slot 2 filament has run out. Please wait while old filament is purged."
        },
        {
          "ecode": "0702200000020001",
          "intro": "AMS C Slot 1 filament has run out. Please insert a new filament."
        },
        {
          "ecode": "1801210000020007",
          "intro": "AMS-HT B Slot 2 feed-out Hall sensor is disconnected. The connector may have poor contact."
        },
        {
          "ecode": "1801920000020002",
          "intro": "AMS-HT B The cooling fan speed of heater 1 is too low, which could be due to excessive fan resistance."
        },
        {
          "ecode": "0705700000020004",
          "intro": "Failed to pull back the filament from the toolhead to AMS. Possible cause: filament or spool stuck."
        },
        {
          "ecode": "1806920000020002",
          "intro": "AMS-HT G The cooling fan speed of heater 1 is too low, which could be due to excessive fan resistance."
        },
        {
          "ecode": "0703930000010001",
          "intro": "AMS D The cooling fan of heater 2 is blocked, which may be due to the fan being stuck."
        },
        {
          "ecode": "0701010000020009",
          "intro": "AMS B The assist motor has unbalanced tree-phase resistaance. The assist motor may be faulty."
        },
        {
          "ecode": "0707700000020008",
          "intro": "Failed to get AMS mapping table; please select \"Resume\" to retry."
        },
        {
          "ecode": "1804200000010084",
          "intro": "Failed to read the filament information from AMS-HT E slot 1. The RFID tag may be damaged or positioned at the edge of the RFID detection device. Please remove 5cm filament and try again."
        },
        {
          "ecode": "0700230000020002",
          "intro": "AMS A Slot 4 is empty; please insert a new filament."
        },
        {
          "ecode": "0700230000020018",
          "intro": "AMS A slot 4 assist motor is stalled，due to excessive resistance in the tube near AMS."
        },
        {
          "ecode": "0707130000010003",
          "intro": "The AMS H slot 4 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "0704210000010085",
          "intro": "Failed to read the filament information from AMS E slot 2. RFID tag verification failed. You can try to use Bambu Lab filament."
        },
        {
          "ecode": "0703010000010005",
          "intro": "AMS D The current sensor of assist motor may be faulty."
        },
        {
          "ecode": "1803310000010001",
          "intro": "The AMS-HT D RFID 2 board has an error."
        },
        {
          "ecode": "0706910000010003",
          "intro": "AMS G The exhaust valve 2 is not connected, which may be due to poor connector contact."
        },
        {
          "ecode": "1805700000020001",
          "intro": "Failed to pull out the filament from the extruder. Possible causes: clogged extruder or broken filament."
        },
        {
          "ecode": "1807220000020018",
          "intro": "AMS-HT H slot 3 assist motor is stalled，due to excessive resistance in the tube near AMS."
        },
        {
          "ecode": "0702320000020002",
          "intro": "The RFID-tag on AMS C Slot3 is damaged, or its content cannot be identified."
        },
        {
          "ecode": "0700230000020017",
          "intro": "AMS A slot 4 assist motor is stalled，due to excessive resistance in the tube between AMS and the printer."
        },
        {
          "ecode": "0701310000020002",
          "intro": "The RFID-tag on AMS B Slot2 is damaged, or its content cannot be identified."
        },
        {
          "ecode": "0704230000020010",
          "intro": "AMS E slot 4 feeds filament out of AMS timeout."
        },
        {
          "ecode": "1800300000010001",
          "intro": "The AMS-HT A RFID 1 board has an error."
        },
        {
          "ecode": "0702300000030003",
          "intro": "RFID cannot be read because of a hardware or structural error."
        },
        {
          "ecode": "1800960000020002",
          "intro": "AMS-HT A Environmental temperature is too low, which will affect the drying capability."
        },
        {
          "ecode": "0704800000010001",
          "intro": "AMS E The current sensor of heater 1 is abnormal."
        },
        {
          "ecode": "0300020000010001",
          "intro": "The nozzle temperature is abnormal; the heater may have a short circuit."
        },
        {
          "ecode": "0702110000010003",
          "intro": "The AMS C slot 2 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "0702210000020017",
          "intro": "AMS C slot 2 assist motor is stalled，due to excessive resistance in the tube between AMS and the printer."
        },
        {
          "ecode": "1801800000010002",
          "intro": "AMS-HT B The heater 1 is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "1800220000020008",
          "intro": "AMS-HT A Slot 3 feed-in Hall sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "0706010000010004",
          "intro": "The AMS G assist motor speed control is malfunctioning. The speed sensor may be faulty."
        },
        {
          "ecode": "0705800000010004",
          "intro": "AMS F The heater 1 is heating abnormally."
        },
        {
          "ecode": "0705210000020003",
          "intro": "AMS F Slot 2's filament may be broken in AMS."
        },
        {
          "ecode": "0704120000010003",
          "intro": "The AMS E slot 3 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "0701700000020008",
          "intro": "Failed to get AMS mapping table; please select \"Resume\" to retry."
        },
        {
          "ecode": "0700230000020010",
          "intro": "AMS A slot 4 feeds filament out of AMS timeout."
        },
        {
          "ecode": "0500020000020004",
          "intro": "Unauthorized user: please check your account information."
        },
        {
          "ecode": "1806200000020005",
          "intro": "AMS-HT G Slot 1 filament has run out, and purging the old filament went abnormally; please check whether the filament is stuck in the tool head."
        },
        {
          "ecode": "0705210000020009",
          "intro": "Failed to extrude AMS F Slot 2 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "1807200000020018",
          "intro": "AMS-HT H slot 1 assist motor is stalled，due to excessive resistance in the tube near AMS."
        },
        {
          "ecode": "1200130000010001",
          "intro": "The AMS A Slot4 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "0702230000020008",
          "intro": "AMS C Slot 4 feed-in Hall sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "0702220000020001",
          "intro": "AMS C Slot 3 filament has run out. Please insert a new filament."
        },
        {
          "ecode": "1803220000020021",
          "intro": "AMS-HT D slot 3 assist motor is stalled，due to excessive resistance in the tube between the filament buffer and the toolhead."
        },
        {
          "ecode": "1801700000020005",
          "intro": "Failed to feed the filament outside the AMS-HT. Please clip the end of the filament flat and check to see if the spool is stuck."
        },
        {
          "ecode": "0706220000020001",
          "intro": "AMS G Slot 3 filament has run out. Please insert a new filament."
        },
        {
          "ecode": "0700020000010001",
          "intro": "AMS A Filament speed and length error: The filament odometry may be faulty."
        },
        {
          "ecode": "0702210000030001",
          "intro": "AMS C Slot 2 filament has run out. Please wait while old filament is purged."
        },
        {
          "ecode": "1801230000020022",
          "intro": "AMS-HT B slot 4 assist motor is stalled，due to excessive resistance in the tube near the toolhead."
        },
        {
          "ecode": "1805230000020009",
          "intro": "Failed to extrude AMS-HT F Slot 4 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "0702230000020020",
          "intro": "AMS C slot 4 assist motor is stalled，due to excessive resistance in the tube near the filament buffer。"
        },
        {
          "ecode": "0701010000020011",
          "intro": "AMS B The motor assist parameter is lost. Please pull out the filament from the filament hub and then restart the AMS."
        },
        {
          "ecode": "0701210000020001",
          "intro": "AMS B Slot 2 filament has run out. Please insert a new filament."
        },
        {
          "ecode": "1804700000020001",
          "intro": "Failed to pull out the filament from the extruder. Possible causes: clogged extruder or broken filament."
        },
        {
          "ecode": "1801230000030001",
          "intro": "AMS-HT B Slot 4 filament has run out. Please wait while old filament is purged."
        },
        {
          "ecode": "0700400000020002",
          "intro": "Filament buffer position signal error: the position sensor may be malfunctioning."
        },
        {
          "ecode": "0707230000010086",
          "intro": "Failed to read the filament information from AMS H slot 4. The RFID tag cannot rotate due to a jam during the filament loading or unloading. Please pull out the filament and try again."
        },
        {
          "ecode": "0705010000020006",
          "intro": "AMS F The assist motor three-phase wires are not connected. The assist motor connector may have poor contact."
        },
        {
          "ecode": "0705960000020002",
          "intro": "AMS F Environmental temperature is too low, which will affect the drying capability."
        },
        {
          "ecode": "1800560000030001",
          "intro": "AMS-HT A is undergoing dry cooling; please wait for it to cool down before operating."
        },
        {
          "ecode": "1801810000010002",
          "intro": "AMS-HT B The heater 2 is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "0702700000020006",
          "intro": "Timeout purging old filament. Possible cause: filament stuck or the extruder/nozzle clog."
        },
        {
          "ecode": "1203100000020002",
          "intro": "The AMS D Slot1 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "0700130000020002",
          "intro": "The AMS A slot 4 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "1201320000020002",
          "intro": "The RFID-tag on AMS B Slot 3 is damaged."
        },
        {
          "ecode": "1203830000020001",
          "intro": "AMS D Slot4 filament may be tangled or stuck."
        },
        {
          "ecode": "0704010000020007",
          "intro": "AMS E The assist motor encoder wires are not connected. The assist motor connector may have poor contact."
        },
        {
          "ecode": "1803210000020007",
          "intro": "AMS-HT D Slot 2 feed-out Hall sensor is disconnected. The connector may have poor contact."
        },
        {
          "ecode": "050003000001000B",
          "intro": "The screen is malfunctioning; please restart the device."
        },
        {
          "ecode": "1804200000020018",
          "intro": "AMS-HT E slot 1 assist motor is stalled，due to excessive resistance in the tube near AMS."
        },
        {
          "ecode": "0705210000020007",
          "intro": "AMS F Slot 2 feed-out Hall sensor is disconnected. The connector may have poor contact."
        },
        {
          "ecode": "1800700000020008",
          "intro": "Failed to get AMS mapping table; please select \"Resume\" to retry."
        },
        {
          "ecode": "1806800000010004",
          "intro": "AMS-HT G The heater 1 is heating abnormally."
        },
        {
          "ecode": "0706310000010001",
          "intro": "The AMS G RFID 2 board has an error."
        },
        {
          "ecode": "1803010000020006",
          "intro": "AMS-HT D The assist motor three-phase wires are not connected. The assist motor connector may have poor contact."
        },
        {
          "ecode": "1200300000020002",
          "intro": "The RFID-tag on AMS A Slot 1 is damaged."
        },
        {
          "ecode": "1801130000020004",
          "intro": "AMS-HT B The brushed motor 4 has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "0700200000020007",
          "intro": "AMS A Slot 1 feed-out Hall sensor is disconnected. The connector may have poor contact."
        },
        {
          "ecode": "1804230000020008",
          "intro": "AMS-HT E Slot 4 feed-in Hall sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "1802920000020002",
          "intro": "AMS-HT C The cooling fan speed of heater 1 is too low, which could be due to excessive fan resistance."
        },
        {
          "ecode": "0703210000020018",
          "intro": "AMS D slot 2 assist motor is stalled，due to excessive resistance in the tube near AMS."
        },
        {
          "ecode": "1200210000020001",
          "intro": "AMS A Slot2 filament has run out; please insert a new filament."
        },
        {
          "ecode": "0300920000010003",
          "intro": "The temperature of chamber heater 2 is abnormal. The heater is over temperature."
        },
        {
          "ecode": "0702300000010001",
          "intro": "The AMS C RFID 1 board has an error."
        },
        {
          "ecode": "0702110000020002",
          "intro": "The AMS C slot 2 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "1802010000020008",
          "intro": "AMS-HT C The assist motor phase winding has an open circuit. The assist motor may be faulty."
        },
        {
          "ecode": "1801230000020010",
          "intro": "AMS-HT B slot 4 feeds filament out of AMS timeout."
        },
        {
          "ecode": "03000C0000010004",
          "intro": "An external disturbance was detected on force sensor 3. The heatbed plate may have touched something outside the heatbed."
        },
        {
          "ecode": "1807220000020010",
          "intro": "AMS-HT H slot 3 feeds filament out of AMS timeout."
        },
        {
          "ecode": "1201210000020003",
          "intro": "AMS B Slot2 filament may be broken in the PTFE tube."
        },
        {
          "ecode": "0702800000010001",
          "intro": "AMS C The current sensor of heater 1 is abnormal."
        },
        {
          "ecode": "1800200000020022",
          "intro": "AMS-HT A slot 1 assist motor is stalled，due to excessive resistance in the tube near the toolhead."
        },
        {
          "ecode": "1802220000020011",
          "intro": "AMS-HT C slot 3 pulls filament back to AMS timeout."
        },
        {
          "ecode": "1804210000030002",
          "intro": "AMS-HT E Slot 2 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "0707230000020003",
          "intro": "AMS H Slot 4's filament may be broken in AMS."
        },
        {
          "ecode": "1800210000020011",
          "intro": "AMS-HT A slot 2 pulls filament back to AMS timeout."
        },
        {
          "ecode": "0704200000020024",
          "intro": "AMS E slot 1 failed to rotate the filament spool when pulling filament back to AMS."
        },
        {
          "ecode": "0706210000020019",
          "intro": "AMS G slot 2 assist motor is stalled，due to excessive resistance in the tube between AMS and the filament buffer."
        },
        {
          "ecode": "0706100000010003",
          "intro": "The AMS G slot 1 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "0703230000020008",
          "intro": "AMS D Slot 4 feed-in Hall sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "0707010000020008",
          "intro": "AMS H The assist motor phase winding has an open circuit. The assist motor may be faulty."
        },
        {
          "ecode": "0703100000010003",
          "intro": "The AMS D slot 1 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "0702210000010085",
          "intro": "Failed to read the filament information from AMS C slot 2. RFID tag verification failed. You can try to use Bambu Lab filament."
        },
        {
          "ecode": "1805310000020002",
          "intro": "The RFID-tag on AMS-HT F Slot2 is damaged, or its content cannot be identified."
        },
        {
          "ecode": "0704920000020002",
          "intro": "AMS E The cooling fan speed of heater 1 is too low, which could be due to excessive fan resistance."
        },
        {
          "ecode": "0702230000020003",
          "intro": "AMS C Slot 4's filament may be broken in AMS."
        },
        {
          "ecode": "1201810000020001",
          "intro": "AMS B Slot2 filament may be tangled or stuck."
        },
        {
          "ecode": "1804200000010086",
          "intro": "Failed to read the filament information from AMS-HT E slot 1. The RFID tag cannot rotate due to a jam during the filament loading or unloading. Please pull out the filament and try again."
        },
        {
          "ecode": "0703930000020002",
          "intro": "AMS D The cooling fan speed of heater 2 is too low, which could be due to excessive fan resistance."
        },
        {
          "ecode": "1803010000010011",
          "intro": "AMS-HT D The assist motor calibration parameter error. Please pull out the filament from the filament hub and then restart the AMS."
        },
        {
          "ecode": "1806220000020008",
          "intro": "AMS-HT G Slot 3 feed-in Hall sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "1801200000020005",
          "intro": "AMS-HT B Slot 1 filament has run out, and purging the old filament went abnormally; please check whether the filament is stuck in the tool head."
        },
        {
          "ecode": "1804010000020002",
          "intro": "The AMS-HT E assist motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "1807220000010084",
          "intro": "Failed to read the filament information from AMS-HT H slot 3. The RFID tag may be damaged or positioned at the edge of the RFID detection device. Please remove 5cm filament and try again."
        },
        {
          "ecode": "1802700000020004",
          "intro": "Failed to pull back the filament from the toolhead to AMS-HT. Possible cause: filament or spool stuck."
        },
        {
          "ecode": "1801230000020020",
          "intro": "AMS-HT B slot 4 assist motor is stalled，due to excessive resistance in the tube near the filament buffer。"
        },
        {
          "ecode": "0703310000030003",
          "intro": "RFID cannot be read because of a hardware or structural error."
        },
        {
          "ecode": "0703200000030001",
          "intro": "AMS D Slot 1 filament has run out. Please wait while old filament is purged."
        },
        {
          "ecode": "0300080000010001",
          "intro": "Motor-Z has an open-circuit. The connection may be loose, or the motor may have failed."
        },
        {
          "ecode": "1802200000020004",
          "intro": "AMS-HT C Slot 1 filament may be broken in the tool head."
        },
        {
          "ecode": "1200110000010003",
          "intro": "The AMS A Slot2 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "0700210000020001",
          "intro": "AMS A Slot 2 filament has run out. Please insert a new filament."
        },
        {
          "ecode": "1800300000020002",
          "intro": "The RFID-tag on AMS-HT A Slot1 is damaged, or its content cannot be identified."
        },
        {
          "ecode": "1804210000020010",
          "intro": "AMS-HT E slot 2 feeds filament out of AMS timeout."
        },
        {
          "ecode": "0300100000020001",
          "intro": "The resonance frequency of the X axis is low. The timing belt may be loose."
        },
        {
          "ecode": "0707220000020004",
          "intro": "AMS H Slot 3 filament may be broken in the tool head."
        },
        {
          "ecode": "0705940000010001",
          "intro": "AMS F The temperature sensor of heater 1 is malfunctioning, which may be due to poor connector contact."
        },
        {
          "ecode": "0706230000010081",
          "intro": "Failed to read the filament information from AMS G slot 4. The AMS main board may be malfunctioning."
        },
        {
          "ecode": "1806110000010001",
          "intro": "The AMS-HT G slot 2 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "0706210000020011",
          "intro": "AMS G slot 2 pulls filament back to AMS timeout."
        },
        {
          "ecode": "1203220000020005",
          "intro": "AMS D Slot3 filament has run out, and purging the old filament went abnormally; please check to see if filament is stuck in the toolhead."
        },
        {
          "ecode": "0706230000010083",
          "intro": "Failed to read the filament information from AMS G slot 4. The RFID tag may be damaged."
        },
        {
          "ecode": "1803010000020011",
          "intro": "AMS-HT D The motor assist parameter is lost. Please pull out the filament from the filament hub and then restart the AMS."
        },
        {
          "ecode": "0704230000020009",
          "intro": "Failed to extrude AMS E Slot 4 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "1800230000010083",
          "intro": "Failed to read the filament information from AMS-HT A slot 4. The RFID tag may be damaged."
        },
        {
          "ecode": "0701350000010002",
          "intro": "AMS B The humidity sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "1203200000020005",
          "intro": "AMS D Slot1 filament has run out, and purging the old filament went abnormally; please check to see if filament is stuck in the toolhead."
        },
        {
          "ecode": "0701010000020006",
          "intro": "AMS B The assist motor three-phase wires are not connected. The assist motor connector may have poor contact."
        },
        {
          "ecode": "1806700000020001",
          "intro": "Failed to pull out the filament from the extruder. Possible causes: clogged extruder or broken filament."
        },
        {
          "ecode": "1806220000030001",
          "intro": "AMS-HT G Slot 3 filament has run out. Please wait while old filament is purged."
        },
        {
          "ecode": "0700100000020002",
          "intro": "The AMS A slot 1 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "0705120000010003",
          "intro": "The AMS F slot 3 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "0703230000020005",
          "intro": "AMS D Slot 4 filament has run out, and purging the old filament went abnormally; please check whether the filament is stuck in the tool head."
        },
        {
          "ecode": "1802810000010003",
          "intro": "AMS-HT C The heater 2 is short-circuited, which may be due to a wiring short or heater damage."
        },
        {
          "ecode": "0704220000020024",
          "intro": "AMS E slot 3 failed to rotate the filament spool when pulling filament back to AMS."
        },
        {
          "ecode": "0700010000020007",
          "intro": "AMS A The assist motor encoder wires are not connected. The assist motor connector may have poor contact."
        },
        {
          "ecode": "1803010000020002",
          "intro": "The AMS-HT D assist motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "0706110000010003",
          "intro": "The AMS G slot 2 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "0702200000020008",
          "intro": "AMS C Slot 1 feed-in Hall sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "0706210000010085",
          "intro": "Failed to read the filament information from AMS G slot 2. RFID tag verification failed. You can try to use Bambu Lab filament."
        },
        {
          "ecode": "0704200000020010",
          "intro": "AMS E slot 1 feeds filament out of AMS timeout."
        },
        {
          "ecode": "1202320000020002",
          "intro": "The RFID-tag on AMS C Slot 3 is damaged."
        },
        {
          "ecode": "0701020000020002",
          "intro": "AMS B The odometer has no signal. The odometer connector may have poor contact."
        },
        {
          "ecode": "0707010000020002",
          "intro": "The AMS H assist motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "1201800000020001",
          "intro": "AMS B Slot1 filament may be tangled or stuck."
        },
        {
          "ecode": "0700230000030002",
          "intro": "AMS A Slot 4 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "0702010000010004",
          "intro": "The AMS C assist motor speed control is malfunctioning. The speed sensor may be faulty."
        },
        {
          "ecode": "1805220000030001",
          "intro": "AMS-HT F Slot 3 filament has run out. Please wait while old filament is purged."
        },
        {
          "ecode": "03000D0000010003",
          "intro": "The build plate is not placed properly. Please adjust it."
        },
        {
          "ecode": "1800200000010081",
          "intro": "Failed to read the filament information from AMS-HT A slot 1. The AMS main board may be malfunctioning."
        },
        {
          "ecode": "1807960000010003",
          "intro": "AMS-HT H Unable to start drying; please pull out the filament from filament hub and try again."
        },
        {
          "ecode": "0700450000020003",
          "intro": "The filament cutter handle has not been released. The handle or blade may be jammed, or there could be an issue with the filament sensor connection."
        },
        {
          "ecode": "0705230000020011",
          "intro": "AMS F slot 4 pulls filament back to AMS timeout."
        },
        {
          "ecode": "0704010000020009",
          "intro": "AMS E The assist motor has unbalanced tree-phase resistaance. The assist motor may be faulty."
        },
        {
          "ecode": "1804230000020020",
          "intro": "AMS-HT E slot 4 assist motor is stalled，due to excessive resistance in the tube near the filament buffer。"
        },
        {
          "ecode": "0700350000010002",
          "intro": "AMS A The humidity sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "0701010000010003",
          "intro": "The AMS B assist motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "1801220000020008",
          "intro": "AMS-HT B Slot 3 feed-in Hall sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "1804200000020010",
          "intro": "AMS-HT E slot 1 feeds filament out of AMS timeout."
        },
        {
          "ecode": "1802210000020009",
          "intro": "Failed to extrude AMS-HT C Slot 2 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "1805300000010004",
          "intro": "Encryption chip failure"
        },
        {
          "ecode": "1804800000010002",
          "intro": "AMS-HT E The heater 1 is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "1800700000020001",
          "intro": "Failed to pull out the filament from the extruder. Possible causes: clogged extruder or broken filament."
        },
        {
          "ecode": "03000D0000010004",
          "intro": "The build plate is not placed properly. Please adjust it."
        },
        {
          "ecode": "0704110000020004",
          "intro": "AMS E The brushed motor 2 has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "1803300000010004",
          "intro": "Encryption chip failure"
        },
        {
          "ecode": "1202120000020002",
          "intro": "The AMS C Slot3 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "0700220000010083",
          "intro": "Failed to read the filament information from AMS A slot 3. The RFID tag may be damaged."
        },
        {
          "ecode": "1802700000020003",
          "intro": "Failed to extrude the filament. Possible cause: extruder or nozzle clog."
        },
        {
          "ecode": "0701200000020010",
          "intro": "AMS B slot 1 feeds filament out of AMS timeout."
        },
        {
          "ecode": "1801230000020021",
          "intro": "AMS-HT B slot 4 assist motor is stalled，due to excessive resistance in the tube between the filament buffer and the toolhead."
        },
        {
          "ecode": "1805230000020008",
          "intro": "AMS-HT F Slot 4 feed-in Hall sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "0702200000020009",
          "intro": "Failed to extrude AMS C Slot 1 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "1200200000030002",
          "intro": "AMS A Slot1 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "1803900000020001",
          "intro": "AMS-HT D The operation of the exhaust valve 1 is abnormal, which may be due to excessive resistance."
        },
        {
          "ecode": "1801120000020004",
          "intro": "AMS-HT B The brushed motor 3 has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "1806230000010083",
          "intro": "Failed to read the filament information from AMS-HT G slot 4. The RFID tag may be damaged."
        },
        {
          "ecode": "1806700000020006",
          "intro": "Timeout purging old filament. Possible cause: filament stuck or the extruder/nozzle clog."
        },
        {
          "ecode": "1800930000010001",
          "intro": "AMS-HT A The cooling fan of heater 2 is blocked, which may be due to the fan being stuck."
        },
        {
          "ecode": "0C0003000002000F",
          "intro": "Parts skipped before first layer inspection; the inspection is not supported for the current print."
        },
        {
          "ecode": "1802220000010085",
          "intro": "Failed to read the filament information from AMS-HT C slot 3. RFID tag verification failed. You can try to use Bambu Lab filament."
        },
        {
          "ecode": "1203220000020002",
          "intro": "AMS D Slot 3 is empty; please insert a new filament."
        },
        {
          "ecode": "1801330000020002",
          "intro": "The RFID-tag on AMS-HT B Slot4 is damaged, or its content cannot be identified."
        },
        {
          "ecode": "1803810000010001",
          "intro": "AMS-HT D The current sensor of heater 2 is abnormal."
        },
        {
          "ecode": "0705220000020020",
          "intro": "AMS F slot 3 assist motor is stalled，due to excessive resistance in the tube near the filament buffer。"
        },
        {
          "ecode": "1200800000020001",
          "intro": "AMS A Slot1 filament may be tangled or stuck."
        },
        {
          "ecode": "0300010000010007",
          "intro": "The heatbed temperature is abnormal; the sensor may have an open circuit."
        },
        {
          "ecode": "0703220000020017",
          "intro": "AMS D slot 3 assist motor is stalled，due to excessive resistance in the tube between AMS and the printer."
        },
        {
          "ecode": "1804230000020017",
          "intro": "AMS-HT E slot 4 assist motor is stalled，due to excessive resistance in the tube between AMS and the printer."
        },
        {
          "ecode": "0704930000010001",
          "intro": "AMS E The cooling fan of heater 2 is blocked, which may be due to the fan being stuck."
        },
        {
          "ecode": "1203710000010001",
          "intro": "AMS D Filament speed and length error: The slot 2 filament odometry may be faulty."
        },
        {
          "ecode": "1806230000020003",
          "intro": "AMS-HT G Slot 4's filament may be broken in AMS-HT."
        },
        {
          "ecode": "1201710000010001",
          "intro": "AMS B Filament speed and length error: The slot 2 filament odometry may be faulty."
        },
        {
          "ecode": "0707020000010001",
          "intro": "AMS H Filament speed and length error: The filament odometry may be faulty."
        },
        {
          "ecode": "0704120000020002",
          "intro": "The AMS E slot 3 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "1806200000020019",
          "intro": "AMS-HT G slot 1 assist motor is stalled，due to excessive resistance in the tube between AMS and the filament buffer."
        },
        {
          "ecode": "1807700000020003",
          "intro": "Failed to extrude the filament. Possible cause: extruder or nozzle clog."
        },
        {
          "ecode": "1801320000020002",
          "intro": "The RFID-tag on AMS-HT B Slot3 is damaged, or its content cannot be identified."
        },
        {
          "ecode": "1801200000020021",
          "intro": "AMS-HT B slot 1 assist motor is stalled，due to excessive resistance in the tube between the filament buffer and the toolhead."
        },
        {
          "ecode": "1802810000010002",
          "intro": "AMS-HT C The heater 2 is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "0704960000020002",
          "intro": "AMS E Environmental temperature is too low, which will affect the drying capability."
        },
        {
          "ecode": "0706330000020002",
          "intro": "The RFID-tag on AMS G Slot4 is damaged, or its content cannot be identified."
        },
        {
          "ecode": "1804560000030001",
          "intro": "AMS-HT E is undergoing dry cooling; please wait for it to cool down before operating."
        },
        {
          "ecode": "0700800000010004",
          "intro": "AMS A The heater 1 is heating abnormally."
        },
        {
          "ecode": "0701220000030002",
          "intro": "AMS B Slot 3 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "0703500000020001",
          "intro": "AMS D communication is abnormal; please check the connection cable."
        },
        {
          "ecode": "1200310000030003",
          "intro": "AMS A Slot2 RFID cannot be read because of a structural error."
        },
        {
          "ecode": "0706200000020004",
          "intro": "AMS G Slot 1 filament may be broken in the tool head."
        },
        {
          "ecode": "0706230000030001",
          "intro": "AMS G Slot 4 filament has run out. Please wait while old filament is purged."
        },
        {
          "ecode": "1802900000010003",
          "intro": "AMS-HT C The exhaust valve 1 is not connected, which may be due to poor connector contact."
        },
        {
          "ecode": "0704210000010086",
          "intro": "Failed to read the filament information from AMS E slot 2. The RFID tag cannot rotate due to a jam during the filament loading or unloading. Please pull out the filament and try again."
        },
        {
          "ecode": "0706970000030001",
          "intro": "AMS G chamber temperature is too high; auxiliary feeding or RFID reading is currently not allowed."
        },
        {
          "ecode": "1802200000020018",
          "intro": "AMS-HT C slot 1 assist motor is stalled，due to excessive resistance in the tube near AMS."
        },
        {
          "ecode": "1804210000010085",
          "intro": "Failed to read the filament information from AMS-HT E slot 2. RFID tag verification failed. You can try to use Bambu Lab filament."
        },
        {
          "ecode": "0707210000010086",
          "intro": "Failed to read the filament information from AMS H slot 2. The RFID tag cannot rotate due to a jam during the filament loading or unloading. Please pull out the filament and try again."
        },
        {
          "ecode": "1200230000020006",
          "intro": "Failed to extrude AMS A Slot4 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "1800200000020017",
          "intro": "AMS-HT A slot 1 assist motor is stalled，due to excessive resistance in the tube between AMS and the printer."
        },
        {
          "ecode": "1805200000020010",
          "intro": "AMS-HT F slot 1 feeds filament out of AMS timeout."
        },
        {
          "ecode": "1803010000020007",
          "intro": "AMS-HT D The assist motor encoder wires are not connected. The assist motor connector may have poor contact."
        },
        {
          "ecode": "1807220000020019",
          "intro": "AMS-HT H slot 3 assist motor is stalled，due to excessive resistance in the tube between AMS and the filament buffer."
        },
        {
          "ecode": "1804230000020021",
          "intro": "AMS-HT E slot 4 assist motor is stalled，due to excessive resistance in the tube between the filament buffer and the toolhead."
        },
        {
          "ecode": "1803010000010005",
          "intro": "AMS-HT D The current sensor of assist motor may be faulty."
        },
        {
          "ecode": "0706800000010001",
          "intro": "AMS G The current sensor of heater 1 is abnormal."
        },
        {
          "ecode": "0705200000010083",
          "intro": "Failed to read the filament information from AMS F slot 1. The RFID tag may be damaged."
        },
        {
          "ecode": "0707700000020004",
          "intro": "Failed to pull back the filament from the toolhead to AMS. Possible cause: filament or spool stuck."
        },
        {
          "ecode": "1800500000020001",
          "intro": "AMS-HT A communication is abnormal; please check the connection cable."
        },
        {
          "ecode": "0702220000030001",
          "intro": "AMS C Slot 3 filament has run out. Please wait while old filament is purged."
        },
        {
          "ecode": "1800220000020019",
          "intro": "AMS-HT A slot 3 assist motor is stalled，due to excessive resistance in the tube between AMS and the filament buffer."
        },
        {
          "ecode": "0703210000010084",
          "intro": "Failed to read the filament information from AMS D slot 2. The RFID tag may be damaged or positioned at the edge of the RFID detection device. Please remove 5cm filament and try again."
        },
        {
          "ecode": "1200100000010003",
          "intro": "The AMS A Slot1 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "0707930000010001",
          "intro": "AMS H The cooling fan of heater 2 is blocked, which may be due to the fan being stuck."
        },
        {
          "ecode": "0701930000020002",
          "intro": "AMS B The cooling fan speed of heater 2 is too low, which could be due to excessive fan resistance."
        },
        {
          "ecode": "1800230000020024",
          "intro": "AMS-HT A slot 4 failed to rotate the filament spool when pulling filament back to AMS."
        },
        {
          "ecode": "03001A0000020002",
          "intro": "The nozzle is clogged with filament."
        },
        {
          "ecode": "1801200000020024",
          "intro": "AMS-HT B slot 1 failed to rotate the filament spool when pulling filament back to AMS."
        },
        {
          "ecode": "1807210000010084",
          "intro": "Failed to read the filament information from AMS-HT H slot 2. The RFID tag may be damaged or positioned at the edge of the RFID detection device. Please remove 5cm filament and try again."
        },
        {
          "ecode": "1803220000020019",
          "intro": "AMS-HT D slot 3 assist motor is stalled，due to excessive resistance in the tube between AMS and the filament buffer."
        },
        {
          "ecode": "1200220000030002",
          "intro": "AMS A Slot3 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "1202210000020003",
          "intro": "AMS C Slot2 filament may be broken in the PTFE tube."
        },
        {
          "ecode": "0702010000020011",
          "intro": "AMS C The motor assist parameter is lost. Please pull out the filament from the filament hub and then restart the AMS."
        },
        {
          "ecode": "03000D0000020008",
          "intro": "The build plate may not be properly placed. If this message appears repeatedly, please check the Wiki for more explanations."
        },
        {
          "ecode": "03000D0000020004",
          "intro": "The build plate may not be properly placed. If this message appears repeatedly, please check the Wiki for more explanations."
        },
        {
          "ecode": "1802230000030001",
          "intro": "AMS-HT C Slot 4 filament has run out. Please wait while old filament is purged."
        },
        {
          "ecode": "1806810000010004",
          "intro": "AMS-HT G The heater 2 is heating abnormally."
        },
        {
          "ecode": "1807010000020010",
          "intro": "AMS-HT H The assist motor resistance is abnormal. The assist motor may be faulty."
        },
        {
          "ecode": "0705350000010002",
          "intro": "AMS F The humidity sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "1800910000020001",
          "intro": "AMS-HT A The operation of the exhaust valve 2 is abnormal, which may be due to excessive resistance."
        },
        {
          "ecode": "0706300000020002",
          "intro": "The RFID-tag on AMS G Slot1 is damaged, or its content cannot be identified."
        },
        {
          "ecode": "0706110000020004",
          "intro": "AMS G The brushed motor 2 has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "0704200000020008",
          "intro": "AMS E Slot 1 feed-in Hall sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "0707700000020006",
          "intro": "Timeout purging old filament. Possible cause: filament stuck or the extruder/nozzle clog."
        },
        {
          "ecode": "1200200000020005",
          "intro": "AMS A Slot1 filament has run out, and purging the old filament went abnormally; please check to see if filament is stuck in the toolhead."
        },
        {
          "ecode": "0701800000010004",
          "intro": "AMS B The heater 1 is heating abnormally."
        },
        {
          "ecode": "1801220000010083",
          "intro": "Failed to read the filament information from AMS-HT B slot 3. The RFID tag may be damaged."
        },
        {
          "ecode": "1801200000010084",
          "intro": "Failed to read the filament information from AMS-HT B slot 1. The RFID tag may be damaged or positioned at the edge of the RFID detection device. Please remove 5cm filament and try again."
        },
        {
          "ecode": "0705100000020004",
          "intro": "AMS F The brushed motor 1 has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "1802010000020009",
          "intro": "AMS-HT C The assist motor has unbalanced tree-phase resistaance. The assist motor may be faulty."
        },
        {
          "ecode": "0700120000010003",
          "intro": "The AMS A slot 3 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "0705560000030001",
          "intro": "AMS F is undergoing dry cooling; please wait for it to cool down before operating."
        },
        {
          "ecode": "0700010000020010",
          "intro": "AMS A The assist motor resistance is abnormal. The assist motor may be faulty."
        },
        {
          "ecode": "03000D000002000A",
          "intro": "The build plate may not be properly placed. If this message appears repeatedly, please check the Wiki for more explanations."
        },
        {
          "ecode": "0705210000010083",
          "intro": "Failed to read the filament information from AMS F slot 2. The RFID tag may be damaged."
        },
        {
          "ecode": "0701210000020019",
          "intro": "AMS B slot 2 assist motor is stalled，due to excessive resistance in the tube between AMS and the filament buffer."
        },
        {
          "ecode": "1802210000030001",
          "intro": "AMS-HT C Slot 2 filament has run out. Please wait while old filament is purged."
        },
        {
          "ecode": "0707220000030002",
          "intro": "AMS H Slot 3 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "0702130000020002",
          "intro": "The AMS C slot 4 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "0703220000020010",
          "intro": "AMS D slot 3 feeds filament out of AMS timeout."
        },
        {
          "ecode": "0300010000010008",
          "intro": "An abnormality occurs during the heating process of the heatbed; the heating modules may be broken."
        },
        {
          "ecode": "1800230000020009",
          "intro": "Failed to extrude AMS-HT A Slot 4 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "1806220000030002",
          "intro": "AMS-HT G Slot 3 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "0300900000010003",
          "intro": "Chamber heating failed. The power supply temperature may be too high."
        },
        {
          "ecode": "1801810000010003",
          "intro": "AMS-HT B The heater 2 is short-circuited, which may be due to a wiring short or heater damage."
        },
        {
          "ecode": "1805220000020005",
          "intro": "AMS-HT F Slot 3 filament has run out, and purging the old filament went abnormally; please check whether the filament is stuck in the tool head."
        },
        {
          "ecode": "0705920000010001",
          "intro": "AMS F The cooling fan of heater 1 is blocked, which may be due to the fan being stuck."
        },
        {
          "ecode": "1807200000020011",
          "intro": "AMS-HT H slot 1 pulls filament back to AMS timeout."
        },
        {
          "ecode": "1807810000010002",
          "intro": "AMS-HT H The heater 2 is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "0300010000010006",
          "intro": "The heatbed temperature is abnormal; the sensor may have a short circuit."
        },
        {
          "ecode": "1806220000020001",
          "intro": "AMS-HT G Slot 3 filament has run out. Please insert a new filament."
        },
        {
          "ecode": "1202220000020002",
          "intro": "AMS C Slot 3 is empty; please insert a new filament."
        },
        {
          "ecode": "0702220000020019",
          "intro": "AMS C slot 3 assist motor is stalled，due to excessive resistance in the tube between AMS and the filament buffer."
        },
        {
          "ecode": "1203130000020002",
          "intro": "The AMS D Slot4 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "1203310000030003",
          "intro": "AMS D Slot2 RFID cannot be read because of a structural error."
        },
        {
          "ecode": "0704200000020003",
          "intro": "AMS E Slot 1's filament may be broken in AMS."
        },
        {
          "ecode": "0707210000030001",
          "intro": "AMS H Slot 2 filament has run out. Please wait while old filament is purged."
        },
        {
          "ecode": "1806230000020019",
          "intro": "AMS-HT G slot 4 assist motor is stalled，due to excessive resistance in the tube between AMS and the filament buffer."
        },
        {
          "ecode": "1807800000010002",
          "intro": "AMS-HT H The heater 1 is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "0707220000020021",
          "intro": "AMS H slot 3 assist motor is stalled，due to excessive resistance in the tube between the filament buffer and the toolhead."
        },
        {
          "ecode": "1802230000020021",
          "intro": "AMS-HT C slot 4 assist motor is stalled，due to excessive resistance in the tube between the filament buffer and the toolhead."
        },
        {
          "ecode": "0702220000020018",
          "intro": "AMS C slot 3 assist motor is stalled，due to excessive resistance in the tube near AMS."
        },
        {
          "ecode": "0500040000020012",
          "intro": "The RFID-tag on AMS A Slot3 cannot be identified."
        },
        {
          "ecode": "0707920000010001",
          "intro": "AMS H The cooling fan of heater 1 is blocked, which may be due to the fan being stuck."
        },
        {
          "ecode": "0702230000010081",
          "intro": "Failed to read the filament information from AMS C slot 4. The AMS main board may be malfunctioning."
        },
        {
          "ecode": "0706320000020002",
          "intro": "The RFID-tag on AMS G Slot3 is damaged, or its content cannot be identified."
        },
        {
          "ecode": "1803210000010081",
          "intro": "Failed to read the filament information from AMS-HT D slot 2. The AMS main board may be malfunctioning."
        },
        {
          "ecode": "0705970000030001",
          "intro": "AMS F chamber temperature is too high; auxiliary feeding or RFID reading is currently not allowed."
        },
        {
          "ecode": "1203220000030002",
          "intro": "AMS D Slot3 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "0703810000010002",
          "intro": "AMS D The heater 2 is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "0707010000020009",
          "intro": "AMS H The assist motor has unbalanced tree-phase resistaance. The assist motor may be faulty."
        },
        {
          "ecode": "0702230000020009",
          "intro": "Failed to extrude AMS C Slot 4 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "0300900000010001",
          "intro": "Chamber heating failed. The heater may not be blowing hot air."
        },
        {
          "ecode": "0702100000020004",
          "intro": "AMS C The brushed motor 1 has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "0707210000020011",
          "intro": "AMS H slot 2 pulls filament back to AMS timeout."
        },
        {
          "ecode": "0500040000020016",
          "intro": "The RFID-tag on AMS B Slot3 cannot be identified."
        },
        {
          "ecode": "1802230000020005",
          "intro": "AMS-HT C Slot 4 filament has run out, and purging the old filament went abnormally; please check whether the filament is stuck in the tool head."
        },
        {
          "ecode": "0703220000020002",
          "intro": "AMS D Slot 3 is empty; please insert a new filament."
        },
        {
          "ecode": "1807210000010083",
          "intro": "Failed to read the filament information from AMS-HT H slot 2. The RFID tag may be damaged."
        },
        {
          "ecode": "1800210000020002",
          "intro": "AMS-HT A Slot 2 is empty; please insert a new filament."
        },
        {
          "ecode": "1201720000010001",
          "intro": "AMS B Filament speed and length error: The slot 3 filament odometry may be faulty."
        },
        {
          "ecode": "1803900000010003",
          "intro": "AMS-HT D The exhaust valve 1 is not connected, which may be due to poor connector contact."
        },
        {
          "ecode": "0704310000030003",
          "intro": "RFID cannot be read because of a hardware or structural error."
        },
        {
          "ecode": "1800220000020010",
          "intro": "AMS-HT A slot 3 feeds filament out of AMS timeout."
        },
        {
          "ecode": "1805220000020020",
          "intro": "AMS-HT F slot 3 assist motor is stalled，due to excessive resistance in the tube near the filament buffer。"
        },
        {
          "ecode": "0701210000020020",
          "intro": "AMS B slot 2 assist motor is stalled，due to excessive resistance in the tube near the filament buffer。"
        },
        {
          "ecode": "1801960000010001",
          "intro": "AMS-HT B The drying process may experience thermal runaway. Please turn off the AMS power supply."
        },
        {
          "ecode": "03000A0000010001",
          "intro": "Heatbed force sensor 1 is too sensitive. It may be stuck between the strain arm and heatbed support, or the adjusting screw may be too tight."
        },
        {
          "ecode": "0706310000030003",
          "intro": "RFID cannot be read because of a hardware or structural error."
        },
        {
          "ecode": "0707230000020008",
          "intro": "AMS H Slot 4 feed-in Hall sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "0703700000020003",
          "intro": "Failed to extrude the filament. Possible cause: extruder or nozzle clog."
        },
        {
          "ecode": "1805940000010001",
          "intro": "AMS-HT F The temperature sensor of heater 1 is malfunctioning, which may be due to poor connector contact."
        },
        {
          "ecode": "1805930000010001",
          "intro": "AMS-HT F The cooling fan of heater 2 is blocked, which may be due to the fan being stuck."
        },
        {
          "ecode": "1202700000010001",
          "intro": "AMS C Filament speed and length error: The slot 1 filament odometry may be faulty."
        },
        {
          "ecode": "1804200000020017",
          "intro": "AMS-HT E slot 1 assist motor is stalled，due to excessive resistance in the tube between AMS and the printer."
        },
        {
          "ecode": "0700210000020019",
          "intro": "AMS A slot 2 assist motor is stalled，due to excessive resistance in the tube between AMS and the filament buffer."
        },
        {
          "ecode": "1805700000020007",
          "intro": "AMS-HT filament ran out. Please put a new filament into the same slot in AMS and resume."
        },
        {
          "ecode": "0705700000020003",
          "intro": "Failed to extrude the filament. Possible cause: extruder or nozzle clog."
        },
        {
          "ecode": "0707350000010002",
          "intro": "AMS H The humidity sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "0704200000010086",
          "intro": "Failed to read the filament information from AMS E slot 1. The RFID tag cannot rotate due to a jam during the filament loading or unloading. Please pull out the filament and try again."
        },
        {
          "ecode": "1806230000020005",
          "intro": "AMS-HT G Slot 4 filament has run out, and purging the old filament went abnormally; please check whether the filament is stuck in the tool head."
        },
        {
          "ecode": "1801010000010003",
          "intro": "The AMS-HT B assist motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "1801500000020001",
          "intro": "AMS-HT B communication is abnormal; please check the connection cable."
        },
        {
          "ecode": "1801210000020022",
          "intro": "AMS-HT B slot 2 assist motor is stalled，due to excessive resistance in the tube near the toolhead."
        },
        {
          "ecode": "1201200000020002",
          "intro": "AMS B Slot 1 is empty; please insert a new filament."
        },
        {
          "ecode": "0706220000010085",
          "intro": "Failed to read the filament information from AMS G slot 3. RFID tag verification failed. You can try to use Bambu Lab filament."
        },
        {
          "ecode": "1802200000020020",
          "intro": "AMS-HT C slot 1 assist motor is stalled，due to excessive resistance in the tube near the filament buffer。"
        },
        {
          "ecode": "1800110000010001",
          "intro": "The AMS-HT A slot 2 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "0300930000010002",
          "intro": "Chamber temperature is abnormal. The chamber heater's temperature sensor may have an open circuit."
        },
        {
          "ecode": "1800450000020001",
          "intro": "The filament cutter sensor is malfunctioning; please check whether the connector is properly plugged in."
        },
        {
          "ecode": "1805210000020009",
          "intro": "Failed to extrude AMS-HT F Slot 2 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "0703900000010003",
          "intro": "AMS D The exhaust valve 1 is not connected, which may be due to poor connector contact."
        },
        {
          "ecode": "0702010000010005",
          "intro": "AMS C The current sensor of assist motor may be faulty."
        },
        {
          "ecode": "1801230000030002",
          "intro": "AMS-HT B Slot 4 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "0704960000010003",
          "intro": "AMS E Unable to start drying; please pull out the filament from filament hub and try again."
        },
        {
          "ecode": "1803960000010003",
          "intro": "AMS-HT D Unable to start drying; please pull out the filament from filament hub and try again."
        },
        {
          "ecode": "1203210000020004",
          "intro": "AMS D Slot2 filament may be broken in the tool head."
        },
        {
          "ecode": "1807010000020007",
          "intro": "AMS-HT H The assist motor encoder wires are not connected. The assist motor connector may have poor contact."
        },
        {
          "ecode": "0702210000020011",
          "intro": "AMS C slot 2 pulls filament back to AMS timeout."
        },
        {
          "ecode": "0704210000020021",
          "intro": "AMS E slot 2 assist motor is stalled，due to excessive resistance in the tube between the filament buffer and the toolhead."
        },
        {
          "ecode": "1201220000030002",
          "intro": "AMS B Slot3 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "03001C0000010001",
          "intro": "The extrusion motor driver is abnormal. The MOSFET may have a short circuit."
        },
        {
          "ecode": "1804100000020002",
          "intro": "The AMS-HT E slot 1 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "0700210000020011",
          "intro": "AMS A slot 2 pulls filament back to AMS timeout."
        },
        {
          "ecode": "0701200000020011",
          "intro": "AMS B slot 1 pulls filament back to AMS timeout."
        },
        {
          "ecode": "0700210000030001",
          "intro": "AMS A Slot 2 filament has run out. Please wait while old filament is purged."
        },
        {
          "ecode": "0701300000020002",
          "intro": "The RFID-tag on AMS B Slot1 is damaged, or its content cannot be identified."
        },
        {
          "ecode": "1802700000020001",
          "intro": "Failed to pull out the filament from the extruder. Possible causes: clogged extruder or broken filament."
        },
        {
          "ecode": "1804200000020004",
          "intro": "AMS-HT E Slot 1 filament may be broken in the tool head."
        },
        {
          "ecode": "1200450000020002",
          "intro": "The filament cutter's cutting distance is too large. The X motor may lose steps."
        },
        {
          "ecode": "1802130000020004",
          "intro": "AMS-HT C The brushed motor 4 has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "1802940000010001",
          "intro": "AMS-HT C The temperature sensor of heater 1 is malfunctioning, which may be due to poor connector contact."
        },
        {
          "ecode": "1807220000020008",
          "intro": "AMS-HT H Slot 3 feed-in Hall sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "0707970000030001",
          "intro": "AMS H chamber temperature is too high; auxiliary feeding or RFID reading is currently not allowed."
        },
        {
          "ecode": "1800230000020011",
          "intro": "AMS-HT A slot 4 pulls filament back to AMS timeout."
        },
        {
          "ecode": "0707960000020002",
          "intro": "AMS H Environmental temperature is too low, which will affect the drying capability."
        },
        {
          "ecode": "1800450000020003",
          "intro": "The filament cutter handle has not been released. The handle or blade may be jammed, or there could be an issue with the filament sensor connection."
        },
        {
          "ecode": "0700220000020002",
          "intro": "AMS A Slot 3 is empty; please insert a new filament."
        },
        {
          "ecode": "1804230000020009",
          "intro": "Failed to extrude AMS-HT E Slot 4 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "0706200000010081",
          "intro": "Failed to read the filament information from AMS G slot 1. The AMS main board may be malfunctioning."
        },
        {
          "ecode": "1801220000020019",
          "intro": "AMS-HT B slot 3 assist motor is stalled，due to excessive resistance in the tube between AMS and the filament buffer."
        },
        {
          "ecode": "0700110000020002",
          "intro": "The AMS A slot 2 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "1805230000020018",
          "intro": "AMS-HT F slot 4 assist motor is stalled，due to excessive resistance in the tube near AMS."
        },
        {
          "ecode": "1807910000010003",
          "intro": "AMS-HT H The exhaust valve 2 is not connected, which may be due to poor connector contact."
        },
        {
          "ecode": "0703110000020002",
          "intro": "The AMS D slot 2 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "1802350000010002",
          "intro": "AMS-HT C The humidity sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "1805210000010083",
          "intro": "Failed to read the filament information from AMS-HT F slot 2. The RFID tag may be damaged."
        },
        {
          "ecode": "1805900000010003",
          "intro": "AMS-HT F The exhaust valve 1 is not connected, which may be due to poor connector contact."
        },
        {
          "ecode": "0703210000020002",
          "intro": "AMS D Slot 2 is empty; please insert a new filament."
        },
        {
          "ecode": "1800130000020004",
          "intro": "AMS-HT A The brushed motor 4 has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "1803310000010004",
          "intro": "Encryption chip failure"
        },
        {
          "ecode": "0707560000030001",
          "intro": "AMS H is undergoing dry cooling; please wait for it to cool down before operating."
        },
        {
          "ecode": "1200230000020004",
          "intro": "AMS A Slot4 filament may be broken in the tool head."
        },
        {
          "ecode": "1202200000020004",
          "intro": "AMS C Slot1 filament may be broken in the tool head."
        },
        {
          "ecode": "0701800000010003",
          "intro": "AMS B The heater 1 is short-circuited, which may be due to a wiring short or heater damage."
        },
        {
          "ecode": "1200100000010001",
          "intro": "The AMS A Slot1 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "0705110000020002",
          "intro": "The AMS F slot 2 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "0701220000020010",
          "intro": "AMS B slot 3 feeds filament out of AMS timeout."
        },
        {
          "ecode": "0703020000010001",
          "intro": "AMS D Filament speed and length error: The filament odometry may be faulty."
        },
        {
          "ecode": "0700010000020011",
          "intro": "AMS A The motor assist parameter is lost. Please pull out the filament from the filament hub and then restart the AMS."
        },
        {
          "ecode": "1200200000020004",
          "intro": "AMS A Slot1 filament may be broken in the tool head."
        },
        {
          "ecode": "1801310000010004",
          "intro": "Encryption chip failure"
        },
        {
          "ecode": "1802020000020002",
          "intro": "AMS-HT C The odometer has no signal. The odometer connector may have poor contact."
        },
        {
          "ecode": "1803220000020008",
          "intro": "AMS-HT D Slot 3 feed-in Hall sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "0701200000020009",
          "intro": "Failed to extrude AMS B Slot 1 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "0703230000020018",
          "intro": "AMS D slot 4 assist motor is stalled，due to excessive resistance in the tube near AMS."
        },
        {
          "ecode": "0705220000020007",
          "intro": "AMS F Slot 3 feed-out Hall sensor is disconnected. The connector may have poor contact."
        },
        {
          "ecode": "1801230000010086",
          "intro": "Failed to read the filament information from AMS-HT B slot 4. The RFID tag cannot rotate due to a jam during the filament loading or unloading. Please pull out the filament and try again."
        },
        {
          "ecode": "03000A0000010003",
          "intro": "The signal of heatbed force sensor 1 is too weak. The electronic connection to the sensor may be broken."
        },
        {
          "ecode": "0700200000020021",
          "intro": "AMS A slot 1 assist motor is stalled，due to excessive resistance in the tube between the filament buffer and the toolhead."
        },
        {
          "ecode": "1807210000020011",
          "intro": "AMS-HT H slot 2 pulls filament back to AMS timeout."
        },
        {
          "ecode": "1803700000020008",
          "intro": "Failed to get AMS mapping table; please select \"Resume\" to retry."
        },
        {
          "ecode": "0703010000010011",
          "intro": "AMS D The assist motor calibration parameter error. Please pull out the filament from the filament hub and then restart the AMS."
        },
        {
          "ecode": "0704210000020001",
          "intro": "AMS E Slot 2 filament has run out. Please insert a new filament."
        },
        {
          "ecode": "1201320000010001",
          "intro": "AMS B Slot 3 RFID coil is broken or the RF hardware circuit has an error."
        },
        {
          "ecode": "0707930000020002",
          "intro": "AMS H The cooling fan speed of heater 2 is too low, which could be due to excessive fan resistance."
        },
        {
          "ecode": "1200450000020001",
          "intro": "The filament cutter sensor is malfunctioning. Please check whether the connector is properly plugged in."
        },
        {
          "ecode": "0706230000020017",
          "intro": "AMS G slot 4 assist motor is stalled，due to excessive resistance in the tube between AMS and the printer."
        },
        {
          "ecode": "1800310000010004",
          "intro": "Encryption chip failure"
        },
        {
          "ecode": "0700230000020020",
          "intro": "AMS A slot 4 assist motor is stalled，due to excessive resistance in the tube near the filament buffer。"
        },
        {
          "ecode": "0702200000020010",
          "intro": "AMS C slot 1 feeds filament out of AMS timeout."
        },
        {
          "ecode": "0703230000030002",
          "intro": "AMS D Slot 4 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "1800210000020018",
          "intro": "AMS-HT A slot 2 assist motor is stalled，due to excessive resistance in the tube near AMS."
        },
        {
          "ecode": "1803330000020002",
          "intro": "The RFID-tag on AMS-HT D Slot4 is damaged, or its content cannot be identified."
        },
        {
          "ecode": "1805100000020004",
          "intro": "AMS-HT F The brushed motor 1 has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "0705220000020010",
          "intro": "AMS F slot 3 feeds filament out of AMS timeout."
        },
        {
          "ecode": "0707230000020009",
          "intro": "Failed to extrude AMS H Slot 4 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "1801130000010001",
          "intro": "The AMS-HT B slot 4 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "0706800000010002",
          "intro": "AMS G The heater 1 is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "0701230000010086",
          "intro": "Failed to read the filament information from AMS B slot 4. The RFID tag cannot rotate due to a jam during the filament loading or unloading. Please pull out the filament and try again."
        },
        {
          "ecode": "1804020000020002",
          "intro": "AMS-HT E The odometer has no signal. The odometer connector may have poor contact."
        },
        {
          "ecode": "0705210000020011",
          "intro": "AMS F slot 2 pulls filament back to AMS timeout."
        },
        {
          "ecode": "1803010000010003",
          "intro": "The AMS-HT D assist motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "1806230000020002",
          "intro": "AMS-HT G Slot 4 is empty; please insert a new filament."
        },
        {
          "ecode": "0707220000020024",
          "intro": "AMS H slot 3 failed to rotate the filament spool when pulling filament back to AMS."
        },
        {
          "ecode": "0701010000010001",
          "intro": "The AMS B assist motor has slipped. The extrusion wheel may be worn down, or the filament may be too thin."
        },
        {
          "ecode": "050004000002001D",
          "intro": "The RFID-tag on AMS D Slot2 cannot be identified."
        },
        {
          "ecode": "1800200000020005",
          "intro": "AMS-HT A Slot 1 filament has run out, and purging the old filament went abnormally; please check whether the filament is stuck in the tool head."
        },
        {
          "ecode": "0707210000020003",
          "intro": "AMS H Slot 2's filament may be broken in AMS."
        },
        {
          "ecode": "0700230000020004",
          "intro": "AMS A Slot 4 filament may be broken in the tool head."
        },
        {
          "ecode": "0705210000020001",
          "intro": "AMS F Slot 2 filament has run out. Please insert a new filament."
        },
        {
          "ecode": "0703210000010086",
          "intro": "Failed to read the filament information from AMS D slot 2. The RFID tag cannot rotate due to a jam during the filament loading or unloading. Please pull out the filament and try again."
        },
        {
          "ecode": "0703010000010001",
          "intro": "The AMS D assist motor has slipped. The extrusion wheel may be worn down, or the filament may be too thin."
        },
        {
          "ecode": "1805220000020021",
          "intro": "AMS-HT F slot 3 assist motor is stalled，due to excessive resistance in the tube between the filament buffer and the toolhead."
        },
        {
          "ecode": "0701910000020001",
          "intro": "AMS B The operation of the exhaust valve 2 is abnormal, which may be due to excessive resistance."
        },
        {
          "ecode": "0707200000020002",
          "intro": "AMS H Slot 1 is empty; please insert a new filament."
        },
        {
          "ecode": "1801200000020003",
          "intro": "AMS-HT B Slot 1's filament may be broken in AMS-HT."
        },
        {
          "ecode": "0700010000010003",
          "intro": "The AMS A assist motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "1201100000010003",
          "intro": "The AMS B Slot1 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "0706200000020007",
          "intro": "AMS G Slot 1 feed-out Hall sensor is disconnected. The connector may have poor contact."
        },
        {
          "ecode": "1807200000020005",
          "intro": "AMS-HT H Slot 1 filament has run out, and purging the old filament went abnormally; please check whether the filament is stuck in the tool head."
        },
        {
          "ecode": "1805130000020004",
          "intro": "AMS-HT F The brushed motor 4 has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "0701120000010003",
          "intro": "The AMS B slot 3 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "1802010000010003",
          "intro": "The AMS-HT C assist motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "0704220000010083",
          "intro": "Failed to read the filament information from AMS E slot 3. The RFID tag may be damaged."
        },
        {
          "ecode": "0703230000020004",
          "intro": "AMS D Slot 4 filament may be broken in the tool head."
        },
        {
          "ecode": "03000D000001000A",
          "intro": "The build plate is not placed properly. Please adjust it."
        },
        {
          "ecode": "1801930000020002",
          "intro": "AMS-HT B The cooling fan speed of heater 2 is too low, which could be due to excessive fan resistance."
        },
        {
          "ecode": "1806810000010003",
          "intro": "AMS-HT G The heater 2 is short-circuited, which may be due to a wiring short or heater damage."
        },
        {
          "ecode": "0705200000020024",
          "intro": "AMS F slot 1 failed to rotate the filament spool when pulling filament back to AMS."
        },
        {
          "ecode": "1802210000010081",
          "intro": "Failed to read the filament information from AMS-HT C slot 2. The AMS main board may be malfunctioning."
        },
        {
          "ecode": "1806210000020022",
          "intro": "AMS-HT G slot 2 assist motor is stalled，due to excessive resistance in the tube near the toolhead."
        },
        {
          "ecode": "0300060000010001",
          "intro": "Motor-A has an open-circuit. There may be a loose connection, or the motor may have failed."
        },
        {
          "ecode": "1801220000020005",
          "intro": "AMS-HT B Slot 3 filament has run out, and purging the old filament went abnormally; please check whether the filament is stuck in the tool head."
        },
        {
          "ecode": "0300400000020001",
          "intro": "Data transmission over the serial port is abnormal; the software system may be faulty."
        },
        {
          "ecode": "1805120000010001",
          "intro": "The AMS-HT F slot 3 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "0706020000020002",
          "intro": "AMS G The odometer has no signal. The odometer connector may have poor contact."
        },
        {
          "ecode": "1202300000020002",
          "intro": "The RFID-tag on AMS C Slot 1 is damaged."
        },
        {
          "ecode": "1804300000010001",
          "intro": "The AMS-HT E RFID 1 board has an error."
        },
        {
          "ecode": "0704220000020009",
          "intro": "Failed to extrude AMS E Slot 3 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "0703230000010083",
          "intro": "Failed to read the filament information from AMS D slot 4. The RFID tag may be damaged."
        },
        {
          "ecode": "1805230000020003",
          "intro": "AMS-HT F Slot 4's filament may be broken in AMS-HT."
        },
        {
          "ecode": "0704300000010004",
          "intro": "Encryption chip failure"
        },
        {
          "ecode": "0705230000020017",
          "intro": "AMS F slot 4 assist motor is stalled，due to excessive resistance in the tube between AMS and the printer."
        },
        {
          "ecode": "0706960000010003",
          "intro": "AMS G Unable to start drying; please pull out the filament from filament hub and try again."
        },
        {
          "ecode": "0701320000020002",
          "intro": "The RFID-tag on AMS B Slot3 is damaged, or its content cannot be identified."
        },
        {
          "ecode": "0704220000010086",
          "intro": "Failed to read the filament information from AMS E slot 3. The RFID tag cannot rotate due to a jam during the filament loading or unloading. Please pull out the filament and try again."
        },
        {
          "ecode": "1802110000010003",
          "intro": "The AMS-HT C slot 2 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "0706210000020001",
          "intro": "AMS G Slot 2 filament has run out. Please insert a new filament."
        },
        {
          "ecode": "1806220000020009",
          "intro": "Failed to extrude AMS-HT G Slot 3 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "1807210000010086",
          "intro": "Failed to read the filament information from AMS-HT H slot 2. The RFID tag cannot rotate due to a jam during the filament loading or unloading. Please pull out the filament and try again."
        },
        {
          "ecode": "0705800000010003",
          "intro": "AMS F The heater 1 is short-circuited, which may be due to a wiring short or heater damage."
        },
        {
          "ecode": "1804200000030001",
          "intro": "AMS-HT E Slot 1 filament has run out. Please wait while old filament is purged."
        },
        {
          "ecode": "0701210000020010",
          "intro": "AMS B slot 2 feeds filament out of AMS timeout."
        },
        {
          "ecode": "0707200000020011",
          "intro": "AMS H slot 1 pulls filament back to AMS timeout."
        },
        {
          "ecode": "1201230000020004",
          "intro": "AMS B Slot4 filament may be broken in the tool head."
        },
        {
          "ecode": "1806010000020009",
          "intro": "AMS-HT G The assist motor has unbalanced tree-phase resistaance. The assist motor may be faulty."
        },
        {
          "ecode": "0700200000010083",
          "intro": "Failed to read the filament information from AMS A slot 1. The RFID tag may be damaged."
        },
        {
          "ecode": "0706220000020005",
          "intro": "AMS G Slot 3 filament has run out, and purging the old filament went abnormally; please check whether the filament is stuck in the tool head."
        },
        {
          "ecode": "0300930000010001",
          "intro": "Chamber temperature is abnormal. The chamber heater's temperature sensor may have a short circuit."
        },
        {
          "ecode": "1202230000020001",
          "intro": "AMS C Slot4 filament has run out; please insert a new filament."
        },
        {
          "ecode": "0500020000020007",
          "intro": "Liveview service login failed; please check your network connection."
        },
        {
          "ecode": "1806700000020004",
          "intro": "Failed to pull back the filament from the toolhead to AMS-HT. Possible cause: filament or spool stuck."
        },
        {
          "ecode": "0702210000020018",
          "intro": "AMS C slot 2 assist motor is stalled，due to excessive resistance in the tube near AMS."
        },
        {
          "ecode": "1801200000010085",
          "intro": "Failed to read the filament information from AMS-HT B slot 1. RFID tag verification failed. You can try to use Bambu Lab filament."
        },
        {
          "ecode": "0703230000020021",
          "intro": "AMS D slot 4 assist motor is stalled，due to excessive resistance in the tube between the filament buffer and the toolhead."
        },
        {
          "ecode": "1203330000020002",
          "intro": "The RFID-tag on AMS D Slot 4 is damaged."
        },
        {
          "ecode": "0704700000020004",
          "intro": "Failed to pull back the filament from the toolhead to AMS. Possible cause: filament or spool stuck."
        },
        {
          "ecode": "1202730000010001",
          "intro": "AMS C Filament speed and length error: The slot 4 filament odometry may be faulty."
        },
        {
          "ecode": "1807120000020004",
          "intro": "AMS-HT H The brushed motor 3 has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "0C00020000020007",
          "intro": "The vertical laser is not lit. Please check if it's covered or hardware connection has a problem."
        },
        {
          "ecode": "1802230000020001",
          "intro": "AMS-HT C Slot 4 filament has run out. Please insert a new filament."
        },
        {
          "ecode": "0707200000010086",
          "intro": "Failed to read the filament information from AMS H slot 1. The RFID tag cannot rotate due to a jam during the filament loading or unloading. Please pull out the filament and try again."
        },
        {
          "ecode": "1805200000020020",
          "intro": "AMS-HT F slot 1 assist motor is stalled，due to excessive resistance in the tube near the filament buffer。"
        },
        {
          "ecode": "1805320000020002",
          "intro": "The RFID-tag on AMS-HT F Slot3 is damaged, or its content cannot be identified."
        },
        {
          "ecode": "1801220000020018",
          "intro": "AMS-HT B slot 3 assist motor is stalled，due to excessive resistance in the tube near AMS."
        },
        {
          "ecode": "1804200000030002",
          "intro": "AMS-HT E Slot 1 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "0700400000020004",
          "intro": "The filament buffer signal is abnormal; the spring may be stuck, or the filament may be tangled."
        },
        {
          "ecode": "1203120000020002",
          "intro": "The AMS D Slot3 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "1805220000020008",
          "intro": "AMS-HT F Slot 3 feed-in Hall sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "0707010000020011",
          "intro": "AMS H The motor assist parameter is lost. Please pull out the filament from the filament hub and then restart the AMS."
        },
        {
          "ecode": "0703120000010001",
          "intro": "The AMS D slot 3 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "1200200000020006",
          "intro": "Failed to extrude AMS A Slot1 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "1800200000020021",
          "intro": "AMS-HT A slot 1 assist motor is stalled，due to excessive resistance in the tube between the filament buffer and the toolhead."
        },
        {
          "ecode": "1802230000030002",
          "intro": "AMS-HT C Slot 4 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "1807230000020001",
          "intro": "AMS-HT H Slot 4 filament has run out. Please insert a new filament."
        },
        {
          "ecode": "0700220000020024",
          "intro": "AMS A slot 3 failed to rotate the filament spool when pulling filament back to AMS."
        },
        {
          "ecode": "1202210000020004",
          "intro": "AMS C Slot2 filament may be broken in the tool head."
        },
        {
          "ecode": "1803210000020008",
          "intro": "AMS-HT D Slot 2 feed-in Hall sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "1805220000020011",
          "intro": "AMS-HT F slot 3 pulls filament back to AMS timeout."
        },
        {
          "ecode": "0702220000020007",
          "intro": "AMS C Slot 3 feed-out Hall sensor is disconnected. The connector may have poor contact."
        },
        {
          "ecode": "1806700000020002",
          "intro": "Failed to feed the filament into the toolhead. Possible cause: filament or spool stuck."
        },
        {
          "ecode": "0705100000020002",
          "intro": "The AMS F slot 1 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "03000B0000010003",
          "intro": "The signal of heatbed force sensor 2 is too weak. The electronic connection to the sensor may be broken."
        },
        {
          "ecode": "07FF200000020001",
          "intro": "External filament has run out; please load a new filament."
        },
        {
          "ecode": "0707210000020004",
          "intro": "AMS H Slot 2 filament may be broken in the tool head."
        },
        {
          "ecode": "0701970000030001",
          "intro": "AMS B chamber temperature is too high; auxiliary feeding or RFID reading is currently not allowed."
        },
        {
          "ecode": "0700200000010086",
          "intro": "Failed to read the filament information from AMS A slot 1. The RFID tag cannot rotate due to a jam during the filament loading or unloading. Please pull out the filament and try again."
        },
        {
          "ecode": "1200230000020005",
          "intro": "AMS A Slot4 filament has run out, and purging the old filament went abnormally; please check to see if filament is stuck in the toolhead."
        },
        {
          "ecode": "0705900000010003",
          "intro": "AMS F The exhaust valve 1 is not connected, which may be due to poor connector contact."
        },
        {
          "ecode": "1807200000010081",
          "intro": "Failed to read the filament information from AMS-HT H slot 1. The AMS main board may be malfunctioning."
        },
        {
          "ecode": "1801230000010085",
          "intro": "Failed to read the filament information from AMS-HT B slot 4. RFID tag verification failed. You can try to use Bambu Lab filament."
        },
        {
          "ecode": "1800210000010084",
          "intro": "Failed to read the filament information from AMS-HT A slot 2. The RFID tag may be damaged or positioned at the edge of the RFID detection device. Please remove 5cm filament and try again."
        },
        {
          "ecode": "0702230000030002",
          "intro": "AMS C Slot 4 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "1800940000010001",
          "intro": "AMS-HT A The temperature sensor of heater 1 is malfunctioning, which may be due to poor connector contact."
        },
        {
          "ecode": "1801220000020001",
          "intro": "AMS-HT B Slot 3 filament has run out. Please insert a new filament."
        },
        {
          "ecode": "1807700000020006",
          "intro": "Timeout purging old filament. Possible cause: filament stuck or the extruder/nozzle clog."
        },
        {
          "ecode": "1806500000020001",
          "intro": "AMS-HT G communication is abnormal; please check the connection cable."
        },
        {
          "ecode": "1807300000010004",
          "intro": "Encryption chip failure"
        },
        {
          "ecode": "0300120000020001",
          "intro": "The front cover of the toolhead fell off."
        },
        {
          "ecode": "1803210000020022",
          "intro": "AMS-HT D slot 2 assist motor is stalled，due to excessive resistance in the tube near the toolhead."
        },
        {
          "ecode": "0702330000020002",
          "intro": "The RFID-tag on AMS C Slot4 is damaged, or its content cannot be identified."
        },
        {
          "ecode": "0703200000020011",
          "intro": "AMS D slot 1 pulls filament back to AMS timeout."
        },
        {
          "ecode": "1202230000020002",
          "intro": "AMS C Slot 4 is empty; please insert a new filament."
        },
        {
          "ecode": "1200210000020004",
          "intro": "AMS A Slot2 filament may be broken in the tool head."
        },
        {
          "ecode": "1800230000020022",
          "intro": "AMS-HT A slot 4 assist motor is stalled，due to excessive resistance in the tube near the toolhead."
        },
        {
          "ecode": "0706020000010001",
          "intro": "AMS G Filament speed and length error: The filament odometry may be faulty."
        },
        {
          "ecode": "1807300000030003",
          "intro": "RFID cannot be read because of a hardware or structural error."
        },
        {
          "ecode": "1802230000020020",
          "intro": "AMS-HT C slot 4 assist motor is stalled，due to excessive resistance in the tube near the filament buffer。"
        },
        {
          "ecode": "0700200000020008",
          "intro": "AMS A Slot 1 feed-in Hall sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "1805810000010003",
          "intro": "AMS-HT F The heater 2 is short-circuited, which may be due to a wiring short or heater damage."
        },
        {
          "ecode": "0706960000010001",
          "intro": "AMS G The drying process may experience thermal runaway. Please turn off the AMS power supply."
        },
        {
          "ecode": "0701220000020019",
          "intro": "AMS B slot 3 assist motor is stalled，due to excessive resistance in the tube between AMS and the filament buffer."
        },
        {
          "ecode": "0701560000030001",
          "intro": "AMS B is undergoing dry cooling; please wait for it to cool down before operating."
        },
        {
          "ecode": "1803810000010002",
          "intro": "AMS-HT D The heater 2 is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "1802110000020002",
          "intro": "The AMS-HT C slot 2 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "0707210000020020",
          "intro": "AMS H slot 2 assist motor is stalled，due to excessive resistance in the tube near the filament buffer。"
        },
        {
          "ecode": "1804010000020009",
          "intro": "AMS-HT E The assist motor has unbalanced tree-phase resistaance. The assist motor may be faulty."
        },
        {
          "ecode": "1801210000020009",
          "intro": "Failed to extrude AMS-HT B Slot 2 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "1801210000030002",
          "intro": "AMS-HT B Slot 2 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "1805230000030001",
          "intro": "AMS-HT F Slot 4 filament has run out. Please wait while old filament is purged."
        },
        {
          "ecode": "0300930000010007",
          "intro": "Chamber temperature is abnormal. The temperature sensor at the power supply may have a short circuit."
        },
        {
          "ecode": "0704210000010081",
          "intro": "Failed to read the filament information from AMS E slot 2. The AMS main board may be malfunctioning."
        },
        {
          "ecode": "1805200000020021",
          "intro": "AMS-HT F slot 1 assist motor is stalled，due to excessive resistance in the tube between the filament buffer and the toolhead."
        },
        {
          "ecode": "1805700000020003",
          "intro": "Failed to extrude the filament. Possible cause: extruder or nozzle clog."
        },
        {
          "ecode": "0707200000010085",
          "intro": "Failed to read the filament information from AMS H slot 1. RFID tag verification failed. You can try to use Bambu Lab filament."
        },
        {
          "ecode": "1200220000030001",
          "intro": "AMS A Slot3 filament has run out. Purging the old filament; please wait."
        },
        {
          "ecode": "1803100000020002",
          "intro": "The AMS-HT D slot 1 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "0705310000030003",
          "intro": "RFID cannot be read because of a hardware or structural error."
        },
        {
          "ecode": "0701230000020022",
          "intro": "AMS B slot 4 assist motor is stalled，due to excessive resistance in the tube near the toolhead."
        },
        {
          "ecode": "0700210000030002",
          "intro": "AMS A Slot 2 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "1202200000020006",
          "intro": "Failed to extrude AMS C Slot1 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "0500020000020005",
          "intro": "Failed to connect to the internet; please check the network connection."
        },
        {
          "ecode": "1806220000020004",
          "intro": "AMS-HT G Slot 3 filament may be broken in the tool head."
        },
        {
          "ecode": "0704010000010003",
          "intro": "The AMS E assist motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "1203110000020002",
          "intro": "The AMS D Slot2 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "1804810000010001",
          "intro": "AMS-HT E The current sensor of heater 2 is abnormal."
        },
        {
          "ecode": "0706210000010081",
          "intro": "Failed to read the filament information from AMS G slot 2. The AMS main board may be malfunctioning."
        },
        {
          "ecode": "0703110000010001",
          "intro": "The AMS D slot 2 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "1807110000010003",
          "intro": "The AMS-HT H slot 2 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "0705700000020002",
          "intro": "Failed to feed the filament into the toolhead. Possible cause: filament or spool stuck."
        },
        {
          "ecode": "0700200000020022",
          "intro": "AMS A slot 1 assist motor is stalled，due to excessive resistance in the tube near the toolhead."
        },
        {
          "ecode": "0704220000020007",
          "intro": "AMS E Slot 3 feed-out Hall sensor is disconnected. The connector may have poor contact."
        },
        {
          "ecode": "0705210000020002",
          "intro": "AMS F Slot 2 is empty; please insert a new filament."
        },
        {
          "ecode": "0702230000020005",
          "intro": "AMS C Slot 4 filament has run out, and purging the old filament went abnormally; please check whether the filament is stuck in the tool head."
        },
        {
          "ecode": "1802230000020022",
          "intro": "AMS-HT C slot 4 assist motor is stalled，due to excessive resistance in the tube near the toolhead."
        },
        {
          "ecode": "1202320000010001",
          "intro": "AMS C Slot 3 RFID coil is broken or the RF hardware circuit has an error."
        },
        {
          "ecode": "0700130000010001",
          "intro": "The AMS A slot 4 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "1805220000010081",
          "intro": "Failed to read the filament information from AMS-HT F slot 3. The AMS main board may be malfunctioning."
        },
        {
          "ecode": "1801100000020002",
          "intro": "The AMS-HT B slot 1 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "1202120000010003",
          "intro": "The AMS C Slot3 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "1803230000030002",
          "intro": "AMS-HT D Slot 4 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "0704310000020002",
          "intro": "The RFID-tag on AMS E Slot2 is damaged, or its content cannot be identified."
        },
        {
          "ecode": "0703200000020020",
          "intro": "AMS D slot 1 assist motor is stalled，due to excessive resistance in the tube near the filament buffer。"
        },
        {
          "ecode": "1806210000030001",
          "intro": "AMS-HT G Slot 2 filament has run out. Please wait while old filament is purged."
        },
        {
          "ecode": "1804210000020001",
          "intro": "AMS-HT E Slot 2 filament has run out. Please insert a new filament."
        },
        {
          "ecode": "1807010000020011",
          "intro": "AMS-HT H The motor assist parameter is lost. Please pull out the filament from the filament hub and then restart the AMS."
        },
        {
          "ecode": "1803700000020007",
          "intro": "AMS-HT filament ran out. Please put a new filament into the same slot in AMS and resume."
        },
        {
          "ecode": "1806240000020009",
          "intro": "AMS-HT G front cover is open. This may affect the drying performance or cause the filament to absorb moisture."
        },
        {
          "ecode": "0300910000010001",
          "intro": "The temperature of chamber heater 1 is abnormal. The heater may have a short circuit."
        },
        {
          "ecode": "0706210000030002",
          "intro": "AMS G Slot 2 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "0701230000020004",
          "intro": "AMS B Slot 4 filament may be broken in the tool head."
        },
        {
          "ecode": "1801220000020017",
          "intro": "AMS-HT B slot 3 assist motor is stalled，due to excessive resistance in the tube between AMS and the printer."
        },
        {
          "ecode": "0702010000020008",
          "intro": "AMS C The assist motor phase winding has an open circuit. The assist motor may be faulty."
        },
        {
          "ecode": "0300070000010002",
          "intro": "Motor-B has a short-circuit. It may have failed."
        },
        {
          "ecode": "1800230000020017",
          "intro": "AMS-HT A slot 4 assist motor is stalled，due to excessive resistance in the tube between AMS and the printer."
        },
        {
          "ecode": "1802220000020009",
          "intro": "Failed to extrude AMS-HT C Slot 3 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "0703200000010085",
          "intro": "Failed to read the filament information from AMS D slot 1. RFID tag verification failed. You can try to use Bambu Lab filament."
        },
        {
          "ecode": "0707210000020002",
          "intro": "AMS H Slot 2 is empty; please insert a new filament."
        },
        {
          "ecode": "1807220000020005",
          "intro": "AMS-HT H Slot 3 filament has run out, and purging the old filament went abnormally; please check whether the filament is stuck in the tool head."
        },
        {
          "ecode": "1203230000030002",
          "intro": "AMS D Slot4 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "0705210000020010",
          "intro": "AMS F slot 2 feeds filament out of AMS timeout."
        },
        {
          "ecode": "1803210000020010",
          "intro": "AMS-HT D slot 2 feeds filament out of AMS timeout."
        },
        {
          "ecode": "1805230000010086",
          "intro": "Failed to read the filament information from AMS-HT F slot 4. The RFID tag cannot rotate due to a jam during the filament loading or unloading. Please pull out the filament and try again."
        },
        {
          "ecode": "1806230000030001",
          "intro": "AMS-HT G Slot 4 filament has run out. Please wait while old filament is purged."
        },
        {
          "ecode": "1806910000010003",
          "intro": "AMS-HT G The exhaust valve 2 is not connected, which may be due to poor connector contact."
        },
        {
          "ecode": "1802130000020002",
          "intro": "The AMS-HT C slot 4 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "1807230000010085",
          "intro": "Failed to read the filament information from AMS-HT H slot 4. RFID tag verification failed. You can try to use Bambu Lab filament."
        },
        {
          "ecode": "0705230000020019",
          "intro": "AMS F slot 4 assist motor is stalled，due to excessive resistance in the tube between AMS and the filament buffer."
        },
        {
          "ecode": "0700230000010084",
          "intro": "Failed to read the filament information from AMS A slot 4. The RFID tag may be damaged or positioned at the edge of the RFID detection device. Please remove 5cm filament and try again."
        },
        {
          "ecode": "1801210000010086",
          "intro": "Failed to read the filament information from AMS-HT B slot 2. The RFID tag cannot rotate due to a jam during the filament loading or unloading. Please pull out the filament and try again."
        },
        {
          "ecode": "1802220000010081",
          "intro": "Failed to read the filament information from AMS-HT C slot 3. The AMS main board may be malfunctioning."
        },
        {
          "ecode": "0706230000020002",
          "intro": "AMS G Slot 4 is empty; please insert a new filament."
        },
        {
          "ecode": "1807130000010003",
          "intro": "The AMS-HT H slot 4 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "1801220000020004",
          "intro": "AMS-HT B Slot 3 filament may be broken in the tool head."
        },
        {
          "ecode": "1807310000010004",
          "intro": "Encryption chip failure"
        },
        {
          "ecode": "1200310000010001",
          "intro": "AMS A Slot 2 RFID coil is broken or the RF hardware circuit has an error."
        },
        {
          "ecode": "1804200000020001",
          "intro": "AMS-HT E Slot 1 filament has run out. Please insert a new filament."
        },
        {
          "ecode": "1805800000010001",
          "intro": "AMS-HT F The current sensor of heater 1 is abnormal."
        },
        {
          "ecode": "1802210000020011",
          "intro": "AMS-HT C slot 2 pulls filament back to AMS timeout."
        },
        {
          "ecode": "1804010000020011",
          "intro": "AMS-HT E The motor assist parameter is lost. Please pull out the filament from the filament hub and then restart the AMS."
        },
        {
          "ecode": "0703200000010083",
          "intro": "Failed to read the filament information from AMS D slot 1. The RFID tag may be damaged."
        },
        {
          "ecode": "1803220000020017",
          "intro": "AMS-HT D slot 3 assist motor is stalled，due to excessive resistance in the tube between AMS and the printer."
        },
        {
          "ecode": "0500040000020011",
          "intro": "The RFID-tag on AMS A Slot2 cannot be identified."
        },
        {
          "ecode": "1804930000010001",
          "intro": "AMS-HT E The cooling fan of heater 2 is blocked, which may be due to the fan being stuck."
        },
        {
          "ecode": "0705200000020018",
          "intro": "AMS F slot 1 assist motor is stalled，due to excessive resistance in the tube near AMS."
        },
        {
          "ecode": "1807010000020006",
          "intro": "AMS-HT H The assist motor three-phase wires are not connected. The assist motor connector may have poor contact."
        },
        {
          "ecode": "1801210000020005",
          "intro": "AMS-HT B Slot 2 filament has run out, and purging the old filament went abnormally; please check whether the filament is stuck in the tool head."
        },
        {
          "ecode": "1801110000010001",
          "intro": "The AMS-HT B slot 2 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "1203130000010003",
          "intro": "The AMS D Slot4 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "0705010000020009",
          "intro": "AMS F The assist motor has unbalanced tree-phase resistaance. The assist motor may be faulty."
        },
        {
          "ecode": "1800230000020001",
          "intro": "AMS-HT A Slot 4 filament has run out. Please insert a new filament."
        },
        {
          "ecode": "0707300000010001",
          "intro": "The AMS H RFID 1 board has an error."
        },
        {
          "ecode": "1200220000020005",
          "intro": "AMS A Slot3 filament has run out, and purging the old filament went abnormally; please check to see if filament is stuck in the toolhead."
        },
        {
          "ecode": "0704700000020003",
          "intro": "Failed to extrude the filament. Possible cause: extruder or nozzle clog."
        },
        {
          "ecode": "0700200000020018",
          "intro": "AMS A slot 1 assist motor is stalled，due to excessive resistance in the tube near AMS."
        },
        {
          "ecode": "0300030000020002",
          "intro": "The hotend cooling fan is running slowly. It may be obstructed. Please check for debris and clean if necessary."
        },
        {
          "ecode": "1805200000020011",
          "intro": "AMS-HT F slot 1 pulls filament back to AMS timeout."
        },
        {
          "ecode": "0706220000020003",
          "intro": "AMS G Slot 3's filament may be broken in AMS."
        },
        {
          "ecode": "0703200000020022",
          "intro": "AMS D slot 1 assist motor is stalled，due to excessive resistance in the tube near the toolhead."
        },
        {
          "ecode": "1800200000020009",
          "intro": "Failed to extrude AMS-HT A Slot 1 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "1805010000020002",
          "intro": "The AMS-HT F assist motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "1803230000020019",
          "intro": "AMS-HT D slot 4 assist motor is stalled，due to excessive resistance in the tube between AMS and the filament buffer."
        },
        {
          "ecode": "1803210000010084",
          "intro": "Failed to read the filament information from AMS-HT D slot 2. The RFID tag may be damaged or positioned at the edge of the RFID detection device. Please remove 5cm filament and try again."
        },
        {
          "ecode": "0701200000020003",
          "intro": "AMS B Slot 1's filament may be broken in AMS."
        },
        {
          "ecode": "0703230000020010",
          "intro": "AMS D slot 4 feeds filament out of AMS timeout."
        },
        {
          "ecode": "0706200000020020",
          "intro": "AMS G slot 1 assist motor is stalled，due to excessive resistance in the tube near the filament buffer。"
        },
        {
          "ecode": "1800230000010081",
          "intro": "Failed to read the filament information from AMS-HT A slot 4. The AMS main board may be malfunctioning."
        },
        {
          "ecode": "1805110000010003",
          "intro": "The AMS-HT F slot 2 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "0703110000020004",
          "intro": "AMS D The brushed motor 2 has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "0705300000010004",
          "intro": "Encryption chip failure"
        },
        {
          "ecode": "1805910000020001",
          "intro": "AMS-HT F The operation of the exhaust valve 2 is abnormal, which may be due to excessive resistance."
        },
        {
          "ecode": "0500010000030006",
          "intro": "Unformatted MicroSD Card: please format it."
        },
        {
          "ecode": "0705330000020002",
          "intro": "The RFID-tag on AMS F Slot4 is damaged, or its content cannot be identified."
        },
        {
          "ecode": "0704220000030002",
          "intro": "AMS E Slot 3 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "1801210000020011",
          "intro": "AMS-HT B slot 2 pulls filament back to AMS timeout."
        },
        {
          "ecode": "0704220000010084",
          "intro": "Failed to read the filament information from AMS E slot 3. The RFID tag may be damaged or positioned at the edge of the RFID detection device. Please remove 5cm filament and try again."
        },
        {
          "ecode": "0704230000020002",
          "intro": "AMS E Slot 4 is empty; please insert a new filament."
        },
        {
          "ecode": "0701200000020002",
          "intro": "AMS B Slot 1 is empty; please insert a new filament."
        },
        {
          "ecode": "1203220000030001",
          "intro": "AMS D Slot3 filament has run out. Purging the old filament; please wait."
        },
        {
          "ecode": "1805310000030003",
          "intro": "RFID cannot be read because of a hardware or structural error."
        },
        {
          "ecode": "1801900000020001",
          "intro": "AMS-HT B The operation of the exhaust valve 1 is abnormal, which may be due to excessive resistance."
        },
        {
          "ecode": "0706120000010001",
          "intro": "The AMS G slot 3 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "1801220000010085",
          "intro": "Failed to read the filament information from AMS-HT B slot 3. RFID tag verification failed. You can try to use Bambu Lab filament."
        },
        {
          "ecode": "1802230000020019",
          "intro": "AMS-HT C slot 4 assist motor is stalled，due to excessive resistance in the tube between AMS and the filament buffer."
        },
        {
          "ecode": "0300100000020002",
          "intro": "The resonance frequency of the X-axis differs significantly from the last calibration. Please clean the carbon rod and conduct a calibration after printing."
        },
        {
          "ecode": "1801220000010086",
          "intro": "Failed to read the filament information from AMS-HT B slot 3. The RFID tag cannot rotate due to a jam during the filament loading or unloading. Please pull out the filament and try again."
        },
        {
          "ecode": "03000B0000010002",
          "intro": "The signal of heatbed force sensor 2 is weak. The force sensor may be broken or have poor electric connection."
        },
        {
          "ecode": "0703800000010004",
          "intro": "AMS D The heater 1 is heating abnormally."
        },
        {
          "ecode": "1806200000020007",
          "intro": "AMS-HT G Slot 1 feed-out Hall sensor is disconnected. The connector may have poor contact."
        },
        {
          "ecode": "1804200000020003",
          "intro": "AMS-HT E Slot 1's filament may be broken in AMS-HT."
        },
        {
          "ecode": "0706210000020018",
          "intro": "AMS G slot 2 assist motor is stalled，due to excessive resistance in the tube near AMS."
        },
        {
          "ecode": "0704230000010083",
          "intro": "Failed to read the filament information from AMS E slot 4. The RFID tag may be damaged."
        },
        {
          "ecode": "0704810000010001",
          "intro": "AMS E The current sensor of heater 2 is abnormal."
        },
        {
          "ecode": "0707230000020020",
          "intro": "AMS H slot 4 assist motor is stalled，due to excessive resistance in the tube near the filament buffer。"
        },
        {
          "ecode": "1801210000020004",
          "intro": "AMS-HT B Slot 2 filament may be broken in the tool head."
        },
        {
          "ecode": "1804010000010005",
          "intro": "AMS-HT E The current sensor of assist motor may be faulty."
        },
        {
          "ecode": "0707230000020002",
          "intro": "AMS H Slot 4 is empty; please insert a new filament."
        },
        {
          "ecode": "0500010000030004",
          "intro": "Not enough space on MicroSD Card; please clear some space."
        },
        {
          "ecode": "0701220000020003",
          "intro": "AMS B Slot 3's filament may be broken in AMS."
        },
        {
          "ecode": "1805200000020009",
          "intro": "Failed to extrude AMS-HT F Slot 1 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "1801200000010081",
          "intro": "Failed to read the filament information from AMS-HT B slot 1. The AMS main board may be malfunctioning."
        },
        {
          "ecode": "1802010000010011",
          "intro": "AMS-HT C The assist motor calibration parameter error. Please pull out the filament from the filament hub and then restart the AMS."
        },
        {
          "ecode": "1806100000010003",
          "intro": "The AMS-HT G slot 1 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "1805920000020002",
          "intro": "AMS-HT F The cooling fan speed of heater 1 is too low, which could be due to excessive fan resistance."
        },
        {
          "ecode": "0707220000020011",
          "intro": "AMS H slot 3 pulls filament back to AMS timeout."
        },
        {
          "ecode": "1805200000020008",
          "intro": "AMS-HT F Slot 1 feed-in Hall sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "1806210000020002",
          "intro": "AMS-HT G Slot 2 is empty; please insert a new filament."
        },
        {
          "ecode": "0703940000010001",
          "intro": "AMS D The temperature sensor of heater 1 is malfunctioning, which may be due to poor connector contact."
        },
        {
          "ecode": "0703300000010004",
          "intro": "Encryption chip failure"
        },
        {
          "ecode": "1805100000010003",
          "intro": "The AMS-HT F slot 1 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "1803320000020002",
          "intro": "The RFID-tag on AMS-HT D Slot3 is damaged, or its content cannot be identified."
        },
        {
          "ecode": "1801110000020002",
          "intro": "The AMS-HT B slot 2 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "0702200000020024",
          "intro": "AMS C slot 1 failed to rotate the filament spool when pulling filament back to AMS."
        },
        {
          "ecode": "1807310000010001",
          "intro": "The AMS-HT H RFID 2 board has an error."
        },
        {
          "ecode": "0700010000010001",
          "intro": "The AMS A assist motor has slipped. The extrusion wheel may be worn down, or the filament may be too thin."
        },
        {
          "ecode": "0703230000010085",
          "intro": "Failed to read the filament information from AMS D slot 4. RFID tag verification failed. You can try to use Bambu Lab filament."
        },
        {
          "ecode": "1200500000020001",
          "intro": "AMS A communication is abnormal; please check the connection cable."
        },
        {
          "ecode": "1806220000020024",
          "intro": "AMS-HT G slot 3 failed to rotate the filament spool when pulling filament back to AMS."
        },
        {
          "ecode": "0705020000010001",
          "intro": "AMS F Filament speed and length error: The filament odometry may be faulty."
        },
        {
          "ecode": "0700310000020002",
          "intro": "The RFID-tag on AMS A Slot2 is damaged, or its content cannot be identified."
        },
        {
          "ecode": "0C00020000020008",
          "intro": "The vertical laser line is too wide. Please check if the heatbed is dirty."
        },
        {
          "ecode": "0702230000030001",
          "intro": "AMS C Slot 4 filament has run out. Please wait while old filament is purged."
        },
        {
          "ecode": "0704210000020008",
          "intro": "AMS E Slot 2 feed-in Hall sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "050003000001000A",
          "intro": "System state is abnormal; please restore to factory settings."
        },
        {
          "ecode": "1802200000020019",
          "intro": "AMS-HT C slot 1 assist motor is stalled，due to excessive resistance in the tube between AMS and the filament buffer."
        },
        {
          "ecode": "0703210000020005",
          "intro": "AMS D Slot 2 filament has run out, and purging the old filament went abnormally; please check whether the filament is stuck in the tool head."
        },
        {
          "ecode": "1801230000020024",
          "intro": "AMS-HT B slot 4 failed to rotate the filament spool when pulling filament back to AMS."
        },
        {
          "ecode": "1807230000020021",
          "intro": "AMS-HT H slot 4 assist motor is stalled，due to excessive resistance in the tube between the filament buffer and the toolhead."
        },
        {
          "ecode": "1807210000020001",
          "intro": "AMS-HT H Slot 2 filament has run out. Please insert a new filament."
        },
        {
          "ecode": "1803110000010003",
          "intro": "The AMS-HT D slot 2 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "1804210000020024",
          "intro": "AMS-HT E slot 2 failed to rotate the filament spool when pulling filament back to AMS."
        },
        {
          "ecode": "1203200000020006",
          "intro": "Failed to extrude AMS D Slot1 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "0702220000010086",
          "intro": "Failed to read the filament information from AMS C slot 3. The RFID tag cannot rotate due to a jam during the filament loading or unloading. Please pull out the filament and try again."
        },
        {
          "ecode": "1200320000020002",
          "intro": "The RFID-tag on AMS A Slot 3 is damaged."
        },
        {
          "ecode": "0704130000020004",
          "intro": "AMS E The brushed motor 4 has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "1805210000020008",
          "intro": "AMS-HT F Slot 2 feed-in Hall sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "0500040000010001",
          "intro": "Failed to download print job; please check your network connection."
        },
        {
          "ecode": "1801200000020019",
          "intro": "AMS-HT B slot 1 assist motor is stalled，due to excessive resistance in the tube between AMS and the filament buffer."
        },
        {
          "ecode": "0702200000030002",
          "intro": "AMS C Slot 1 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "1807130000010001",
          "intro": "The AMS-HT H slot 4 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "0701960000010003",
          "intro": "AMS B Unable to start drying; please pull out the filament from filament hub and try again."
        },
        {
          "ecode": "1801010000020006",
          "intro": "AMS-HT B The assist motor three-phase wires are not connected. The assist motor connector may have poor contact."
        },
        {
          "ecode": "1803300000020002",
          "intro": "The RFID-tag on AMS-HT D Slot1 is damaged, or its content cannot be identified."
        },
        {
          "ecode": "1806230000030002",
          "intro": "AMS-HT G Slot 4 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "0706700000020001",
          "intro": "Failed to pull out the filament from the extruder. Possible causes: clogged extruder or broken filament."
        },
        {
          "ecode": "0704120000010001",
          "intro": "The AMS E slot 3 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "0707910000010003",
          "intro": "AMS H The exhaust valve 2 is not connected, which may be due to poor connector contact."
        },
        {
          "ecode": "1806220000020020",
          "intro": "AMS-HT G slot 3 assist motor is stalled，due to excessive resistance in the tube near the filament buffer。"
        },
        {
          "ecode": "0702220000020009",
          "intro": "Failed to extrude AMS C Slot 3 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "1806220000020010",
          "intro": "AMS-HT G slot 3 feeds filament out of AMS timeout."
        },
        {
          "ecode": "1804010000010004",
          "intro": "The AMS-HT E assist motor speed control is malfunctioning. The speed sensor may be faulty."
        },
        {
          "ecode": "1806130000010003",
          "intro": "The AMS-HT G slot 4 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "1803220000030002",
          "intro": "AMS-HT D Slot 3 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "0703200000020018",
          "intro": "AMS D slot 1 assist motor is stalled，due to excessive resistance in the tube near AMS."
        },
        {
          "ecode": "0707230000010085",
          "intro": "Failed to read the filament information from AMS H slot 4. RFID tag verification failed. You can try to use Bambu Lab filament."
        },
        {
          "ecode": "1801010000010011",
          "intro": "AMS-HT B The assist motor calibration parameter error. Please pull out the filament from the filament hub and then restart the AMS."
        },
        {
          "ecode": "1801960000010003",
          "intro": "AMS-HT B Unable to start drying; please pull out the filament from filament hub and try again."
        },
        {
          "ecode": "1802200000020021",
          "intro": "AMS-HT C slot 1 assist motor is stalled，due to excessive resistance in the tube between the filament buffer and the toolhead."
        },
        {
          "ecode": "1801230000020008",
          "intro": "AMS-HT B Slot 4 feed-in Hall sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "0704210000030001",
          "intro": "AMS E Slot 2 filament has run out. Please wait while old filament is purged."
        },
        {
          "ecode": "0706960000020002",
          "intro": "AMS G Environmental temperature is too low, which will affect the drying capability."
        },
        {
          "ecode": "1805220000020022",
          "intro": "AMS-HT F slot 3 assist motor is stalled，due to excessive resistance in the tube near the toolhead."
        },
        {
          "ecode": "0704320000020002",
          "intro": "The RFID-tag on AMS E Slot3 is damaged, or its content cannot be identified."
        },
        {
          "ecode": "1801950000010001",
          "intro": "AMS-HT B The temperature sensor of heater 2 is malfunctioning, which may be due to poor connector contact."
        },
        {
          "ecode": "1200330000030003",
          "intro": "AMS A Slot4 RFID cannot be read because of a structural error."
        },
        {
          "ecode": "0500050000030002",
          "intro": "The device is in the engineering state; please pay attention to information security related matters."
        },
        {
          "ecode": "1801700000020004",
          "intro": "Failed to pull back the filament from the toolhead to AMS-HT. Possible cause: filament or spool stuck."
        },
        {
          "ecode": "1803220000010086",
          "intro": "Failed to read the filament information from AMS-HT D slot 3. The RFID tag cannot rotate due to a jam during the filament loading or unloading. Please pull out the filament and try again."
        },
        {
          "ecode": "0703130000010001",
          "intro": "The AMS D slot 4 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "0701200000010081",
          "intro": "Failed to read the filament information from AMS B slot 1. The AMS main board may be malfunctioning."
        },
        {
          "ecode": "0701210000020003",
          "intro": "AMS B Slot 2's filament may be broken in AMS."
        },
        {
          "ecode": "0704230000020022",
          "intro": "AMS E slot 4 assist motor is stalled，due to excessive resistance in the tube near the toolhead."
        },
        {
          "ecode": "0705220000020004",
          "intro": "AMS F Slot 3 filament may be broken in the tool head."
        },
        {
          "ecode": "1804210000020018",
          "intro": "AMS-HT E slot 2 assist motor is stalled，due to excessive resistance in the tube near AMS."
        },
        {
          "ecode": "0703200000020017",
          "intro": "AMS D slot 1 assist motor is stalled，due to excessive resistance in the tube between AMS and the printer."
        },
        {
          "ecode": "1800120000010001",
          "intro": "The AMS-HT A slot 3 motor has slipped. The extrusion wheel may be malfunctioning, or the filament may be too thin."
        },
        {
          "ecode": "1803220000020024",
          "intro": "AMS-HT D slot 3 failed to rotate the filament spool when pulling filament back to AMS."
        },
        {
          "ecode": "1203800000020001",
          "intro": "AMS D Slot1 filament may be tangled or stuck."
        },
        {
          "ecode": "1801230000020017",
          "intro": "AMS-HT B slot 4 assist motor is stalled，due to excessive resistance in the tube between AMS and the printer."
        },
        {
          "ecode": "1804230000020010",
          "intro": "AMS-HT E slot 4 feeds filament out of AMS timeout."
        },
        {
          "ecode": "0706130000010003",
          "intro": "The AMS G slot 4 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "1802010000010001",
          "intro": "The AMS-HT C assist motor has slipped. The extrusion wheel may be worn down, or the filament may be too thin."
        },
        {
          "ecode": "1800400000020004",
          "intro": "The filament buffer signal is abnormal; the spring may be stuck, or the filament may be tangled."
        },
        {
          "ecode": "0703700000020001",
          "intro": "Failed to pull out the filament from the extruder. Possible causes: clogged extruder or broken filament."
        },
        {
          "ecode": "0704700000020006",
          "intro": "Timeout purging old filament. Possible cause: filament stuck or the extruder/nozzle clog."
        },
        {
          "ecode": "1803220000020020",
          "intro": "AMS-HT D slot 3 assist motor is stalled，due to excessive resistance in the tube near the filament buffer。"
        },
        {
          "ecode": "0706220000020020",
          "intro": "AMS G slot 3 assist motor is stalled，due to excessive resistance in the tube near the filament buffer。"
        },
        {
          "ecode": "0706950000010001",
          "intro": "AMS G The temperature sensor of heater 2 is malfunctioning, which may be due to poor connector contact."
        },
        {
          "ecode": "0705230000020022",
          "intro": "AMS F slot 4 assist motor is stalled，due to excessive resistance in the tube near the toolhead."
        },
        {
          "ecode": "0703220000020008",
          "intro": "AMS D Slot 3 feed-in Hall sensor is disconnected, which may be due to poor connector contact."
        },
        {
          "ecode": "1806230000020021",
          "intro": "AMS-HT G slot 4 assist motor is stalled，due to excessive resistance in the tube between the filament buffer and the toolhead."
        },
        {
          "ecode": "1802220000020002",
          "intro": "AMS-HT C Slot 3 is empty; please insert a new filament."
        },
        {
          "ecode": "0700230000020021",
          "intro": "AMS A slot 4 assist motor is stalled，due to excessive resistance in the tube between the filament buffer and the toolhead."
        },
        {
          "ecode": "0705010000010005",
          "intro": "AMS F The current sensor of assist motor may be faulty."
        },
        {
          "ecode": "1803200000020024",
          "intro": "AMS-HT D slot 1 failed to rotate the filament spool when pulling filament back to AMS."
        },
        {
          "ecode": "0706930000020002",
          "intro": "AMS G The cooling fan speed of heater 2 is too low, which could be due to excessive fan resistance."
        },
        {
          "ecode": "0700800000010003",
          "intro": "AMS A The heater 1 is short-circuited, which may be due to a wiring short or heater damage."
        },
        {
          "ecode": "1803230000020002",
          "intro": "AMS-HT D Slot 4 is empty; please insert a new filament."
        },
        {
          "ecode": "0707230000010081",
          "intro": "Failed to read the filament information from AMS H slot 4. The AMS main board may be malfunctioning."
        },
        {
          "ecode": "1804130000010003",
          "intro": "The AMS-HT E slot 4 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "1200230000030002",
          "intro": "AMS A Slot4 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "0703700000020008",
          "intro": "Failed to get AMS mapping table; please select \"Resume\" to retry."
        },
        {
          "ecode": "0703700000020006",
          "intro": "Timeout purging old filament. Possible cause: filament stuck or the extruder/nozzle clog."
        },
        {
          "ecode": "0704300000020002",
          "intro": "The RFID-tag on AMS E Slot1 is damaged, or its content cannot be identified."
        },
        {
          "ecode": "1807300000010001",
          "intro": "The AMS-HT H RFID 1 board has an error."
        },
        {
          "ecode": "0702210000010083",
          "intro": "Failed to read the filament information from AMS C slot 2. The RFID tag may be damaged."
        },
        {
          "ecode": "0704220000020022",
          "intro": "AMS E slot 3 assist motor is stalled，due to excessive resistance in the tube near the toolhead."
        },
        {
          "ecode": "0300940000020003",
          "intro": "Chamber failed to reach the desired temperature. The machine will stop waiting for the chamber temperature."
        },
        {
          "ecode": "1802020000010001",
          "intro": "AMS-HT C Filament speed and length error: The filament odometry may be faulty."
        },
        {
          "ecode": "1800320000020002",
          "intro": "The RFID-tag on AMS-HT A Slot3 is damaged, or its content cannot be identified."
        },
        {
          "ecode": "1800100000020002",
          "intro": "The AMS-HT A slot 1 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "1800110000020002",
          "intro": "The AMS-HT A slot 2 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "0702110000020004",
          "intro": "AMS C The brushed motor 2 has no signal, which may be due to poor contact in the motor connector or a motor fault."
        },
        {
          "ecode": "1801700000020008",
          "intro": "Failed to get AMS mapping table; please select \"Resume\" to retry."
        },
        {
          "ecode": "0703200000020010",
          "intro": "AMS D slot 1 feeds filament out of AMS timeout."
        },
        {
          "ecode": "1803220000010085",
          "intro": "Failed to read the filament information from AMS-HT D slot 3. RFID tag verification failed. You can try to use Bambu Lab filament."
        },
        {
          "ecode": "1804300000030003",
          "intro": "RFID cannot be read because of a hardware or structural error."
        },
        {
          "ecode": "1201310000030003",
          "intro": "AMS B Slot2 RFID cannot be read because of a structural error."
        },
        {
          "ecode": "0C00020000020002",
          "intro": "The horizontal laser line is too wide. Please check if the heatbed is dirty."
        },
        {
          "ecode": "1805230000010085",
          "intro": "Failed to read the filament information from AMS-HT F slot 4. RFID tag verification failed. You can try to use Bambu Lab filament."
        },
        {
          "ecode": "0701220000020007",
          "intro": "AMS B Slot 3 feed-out Hall sensor is disconnected. The connector may have poor contact."
        },
        {
          "ecode": "1807210000020010",
          "intro": "AMS-HT H slot 2 feeds filament out of AMS timeout."
        },
        {
          "ecode": "1805960000010003",
          "intro": "AMS-HT F Unable to start drying; please pull out the filament from filament hub and try again."
        },
        {
          "ecode": "0702210000030002",
          "intro": "AMS C Slot 2 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "0702230000020007",
          "intro": "AMS C Slot 4 feed-out Hall sensor is disconnected. The connector may have poor contact."
        },
        {
          "ecode": "03000D0000010008",
          "intro": "The build plate is not placed properly. Please adjust it."
        },
        {
          "ecode": "03000A0000010004",
          "intro": "An external disturbance was detected on force sensor 1. The heatbed plate may have touched something outside the heatbed."
        },
        {
          "ecode": "1203220000020003",
          "intro": "AMS D Slot3 filament may be broken in the PTFE tube."
        },
        {
          "ecode": "0300200000010004",
          "intro": "Y axis homing abnormal: the timing belt may be loose."
        },
        {
          "ecode": "1805700000020002",
          "intro": "Failed to feed the filament into the toolhead. Possible cause: filament or spool stuck."
        },
        {
          "ecode": "1807130000020002",
          "intro": "The AMS-HT H slot 4 motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "0300930000010003",
          "intro": "Chamber temperature is abnormal. The chamber heater's temperature sensor at the air outlet may have a short circuit."
        },
        {
          "ecode": "1803220000020010",
          "intro": "AMS-HT D slot 3 feeds filament out of AMS timeout."
        },
        {
          "ecode": "1804200000020009",
          "intro": "Failed to extrude AMS-HT E Slot 1 filament; the extruder may be clogged or the filament may be too thin, causing the extruder to slip."
        },
        {
          "ecode": "0704300000010001",
          "intro": "The AMS E RFID 1 board has an error."
        },
        {
          "ecode": "0705220000010081",
          "intro": "Failed to read the filament information from AMS F slot 3. The AMS main board may be malfunctioning."
        },
        {
          "ecode": "1800010000010003",
          "intro": "The AMS-HT A assist motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "0706010000020002",
          "intro": "The AMS G assist motor is overloaded. The filament may be tangled or stuck."
        },
        {
          "ecode": "1203210000030002",
          "intro": "AMS D Slot2 filament has run out and automatically switched to the slot with the same filament."
        },
        {
          "ecode": "0700920000010001",
          "intro": "AMS A The cooling fan of heater 1 is blocked, which may be due to the fan being stuck."
        },
        {
          "ecode": "1805200000020018",
          "intro": "AMS-HT F slot 1 assist motor is stalled，due to excessive resistance in the tube near AMS."
        },
        {
          "ecode": "0702230000010086",
          "intro": "Failed to read the filament information from AMS C slot 4. The RFID tag cannot rotate due to a jam during the filament loading or unloading. Please pull out the filament and try again."
        },
        {
          "ecode": "0703200000020001",
          "intro": "AMS D Slot 1 filament has run out. Please insert a new filament."
        },
        {
          "ecode": "0704100000010003",
          "intro": "The AMS E slot 1 motor torque control is malfunctioning. The current sensor may be faulty."
        },
        {
          "ecode": "0702210000010084",
          "intro": "Failed to read the filament information from AMS C slot 2. The RFID tag may be damaged or positioned at the edge of the RFID detection device. Please remove 5cm filament and try again."
        },
        {
          "ecode": "03001B0000010002",
          "intro": "External disturbance was detected on the heatbed acceleeration sensor. The sensor signal wire may not be affixed."
        }
      ]
    }
  }
}
