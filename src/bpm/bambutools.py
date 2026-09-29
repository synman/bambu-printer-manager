"""
`bambutools` contains a collection of methods used as tools (mostly internal).
"""

import hashlib
import json
import logging
from enum import Enum, IntEnum
from pathlib import Path
from threading import Thread
from typing import Any

from bpm.bambucommands import HMS_ACTIONS, HMS_STATUS

"""
`bambutools' hosts various classes and methods used internally and externally
by `bambu-printer-manager`.
"""
LoggerName = "bpm"
logger = logging.getLogger(LoggerName)


class ActiveTool(IntEnum):
    """
    The currently active extruder index.

    * `SINGLE_EXTRUDER (-1)`: Standard single-toolhead architecture (X1/P1/A1).
    * `RIGHT_EXTRUDER (0)`: The primary/right toolhead in H2D (Dual Extruder) systems.
    * `LEFT_EXTRUDER (1)`: The secondary/left toolhead in H2D (Dual Extruder) systems.
    * `NOT_ACTIVE (15)`: The multi-extruder system is in a transitional state.
    """

    SINGLE_EXTRUDER = -1
    RIGHT_EXTRUDER = 0
    LEFT_EXTRUDER = 1
    NOT_ACTIVE = 15


class AirConditioningMode(IntEnum):
    """
    The mode the printer's air conditioning sub system is in.

    * `NOT_SUPPORTED (-1)`: This printer is not equipped with this feature.
    * `COOL_MODE (0)`: The printer is currently not heating. The top vent may be open if the exhaust fan is running.
    * `HEAT_MODE (1)`: The printer is actively heating the chamber with the recirculation fan active.
    """

    NOT_SUPPORTED = -1
    COOL_MODE = 0
    HEAT_MODE = 1


class AMSControlCommand(Enum):
    """
    AMS Control Commands enum. The lowercase name is the `ams_control` `param` sent.

    * `DONE`: filament extruded, the load may continue (Studio's "Filament Extruded, Continue").
    * `ABORT`: cancel the running load or unload (Studio's "Abort" and the load view's "Stop").
    """

    PAUSE = 0
    RESUME = 1
    RESET = 2
    DONE = 3
    ABORT = 4


class FilamentStep(IntEnum):
    """
    The step of a filament load or unload, named as Bambu Studio's `DevFilamentStep`.

    `FILAMENT_STEP_TEXT` holds Studio's label for each step.
    """

    IDLE = 0
    HEAT_NOZZLE = 1
    CUT_FILAMENT = 2
    PULL_CURR_FILAMENT = 3
    PUSH_NEW_FILAMENT = 4
    PURGE_OLD_FILAMENT = 5
    CONFIRM_EXTRUDED = 6
    CHECK_POSITION = 7


FILAMENT_STEP_TEXT = {
    FilamentStep.IDLE: "",
    FilamentStep.HEAT_NOZZLE: "Heat the nozzle",
    FilamentStep.CUT_FILAMENT: "Cut filament",
    FilamentStep.PULL_CURR_FILAMENT: "Pull back current filament",
    FilamentStep.PUSH_NEW_FILAMENT: "Push new filament into extruder",
    FilamentStep.PURGE_OLD_FILAMENT: "Purge old filament",
    FilamentStep.CONFIRM_EXTRUDED: "Confirm extruded",
    FilamentStep.CHECK_POSITION: "Check filament location",
}
"""Bambu Studio's step labels (`Widgets/FilamentLoad.cpp`)."""


class FilamentStepType(IntEnum):
    """
    The kind of filament change under way, as Bambu Studio's `FilamentStepType`.

    * `LOAD`: a load from an AMS slot.
    * `UNLOAD`: an unload (the target slot is none).
    * `VT_LOAD`: a load from an external spool holder (254 or 255).
    """

    LOAD = 0
    UNLOAD = 1
    VT_LOAD = 2


class HMSAction(IntEnum):
    """
    The dialog buttons Bambu Studio knows, by the ids its HMS action table uses
    (`DeviceErrorDialog.hpp` `ActionButton`). Ids the table carries but this enum
    lacks are buttons Studio does not show.
    """

    RESUME_PRINTING = 2
    RESUME_PRINTING_DEFECTS = 3
    RESUME_PRINTING_PROBELM_SOLVED = 4
    STOP_PRINTING = 5
    CHECK_ASSISTANT = 6
    FILAMENT_EXTRUDED = 7
    RETRY_FILAMENT_EXTRUDED = 8
    CONTINUE = 9
    LOAD_VIRTUAL_TRAY = 10
    OK_BUTTON = 11
    FILAMENT_LOAD_RESUME = 12
    JUMP_TO_LIVEVIEW = 13
    NO_REMINDER_NEXT_TIME = 23
    REFRESH_NOZZLE = 24
    IGNORE_NO_REMINDER_NEXT_TIME = 25
    IGNORE_RESUME = 27
    PROBLEM_SOLVED_RESUME = 28
    TURN_OFF_FIRE_ALARM = 29
    RETRY_PROBLEM_SOLVED = 34
    STOP_DRYING = 35
    CANCLE = 37
    REMOVE_CLOSE_BTN = 39
    PROCEED = 41
    OK_JUMP_RACK = 49
    ABORT = 51
    DISABLE_PURIFICATION = 54
    DONT_REMIND_NEXT_TIME = 57
    DBL_CHECK_CANCEL = 10000
    DBL_CHECK_DONE = 10001
    DBL_CHECK_RETRY = 10002
    DBL_CHECK_RESUME = 10003
    DBL_CHECK_OK = 10004


HMS_ACTION_LABEL = {
    HMSAction.RESUME_PRINTING: "Resume Printing",
    HMSAction.RESUME_PRINTING_DEFECTS: "Resume (defects acceptable)",
    HMSAction.RESUME_PRINTING_PROBELM_SOLVED: "Resume (problem solved)",
    HMSAction.STOP_PRINTING: "Stop Printing",
    HMSAction.CHECK_ASSISTANT: "Check Assistant",
    HMSAction.FILAMENT_EXTRUDED: "Filament Extruded, Continue",
    HMSAction.RETRY_FILAMENT_EXTRUDED: "Not Extruded Yet, Retry",
    HMSAction.CONTINUE: "Finished, Continue",
    HMSAction.LOAD_VIRTUAL_TRAY: "Load Filament",
    HMSAction.OK_BUTTON: "OK",
    HMSAction.FILAMENT_LOAD_RESUME: "Filament Loaded, Resume",
    HMSAction.JUMP_TO_LIVEVIEW: "View Liveview",
    HMSAction.NO_REMINDER_NEXT_TIME: "No Reminder Next Time",
    HMSAction.REFRESH_NOZZLE: "Recheck",
    HMSAction.IGNORE_NO_REMINDER_NEXT_TIME: "Ignore. Don't Remind Next Time",
    HMSAction.IGNORE_RESUME: "Ignore this and Resume",
    HMSAction.PROBLEM_SOLVED_RESUME: "Problem Solved and Resume",
    HMSAction.TURN_OFF_FIRE_ALARM: "Got it, Turn off the Fire Alarm.",
    HMSAction.RETRY_PROBLEM_SOLVED: "Retry (problem solved)",
    HMSAction.STOP_DRYING: "Stop Drying",
    HMSAction.CANCLE: "Cancel",
    HMSAction.REMOVE_CLOSE_BTN: "",
    HMSAction.PROCEED: "Proceed",
    HMSAction.OK_JUMP_RACK: "OK",
    HMSAction.ABORT: "Abort",
    HMSAction.DISABLE_PURIFICATION: "Disable Purification for This Print",
    HMSAction.DONT_REMIND_NEXT_TIME: "Don't Remind Me",
    HMSAction.DBL_CHECK_CANCEL: "Cancel",
    HMSAction.DBL_CHECK_DONE: "Done",
    HMSAction.DBL_CHECK_RETRY: "Retry",
    HMSAction.DBL_CHECK_RESUME: "Resume",
    HMSAction.DBL_CHECK_OK: "Confirm",
}
"""Bambu Studio's button text (`DeviceErrorDialog::init_button_list`)."""

HMS_ACTION_COMMAND = {
    HMSAction.FILAMENT_EXTRUDED: "done",
    HMSAction.RETRY_FILAMENT_EXTRUDED: "resume",
    HMSAction.CONTINUE: "resume",
    HMSAction.RETRY_PROBLEM_SOLVED: "resume",
    HMSAction.ABORT: "abort",
    HMSAction.OK_BUTTON: "clean_print_error",
    HMSAction.CHECK_ASSISTANT: "assistant",
    HMSAction.CANCLE: "close",
    HMSAction.DBL_CHECK_CANCEL: "close",
    HMSAction.DBL_CHECK_DONE: "done",
    HMSAction.DBL_CHECK_RETRY: "resume",
    HMSAction.DBL_CHECK_OK: "clean_print_error",
}
"""What bpm sends for a button, matching Studio's `DeviceErrorDialog::on_button_click`:
`done`, `resume` and `abort` are `ams_control` params, `clean_print_error` clears the
error, `assistant` opens the error's `url` and `close` sends nothing. A known button not
listed here sends a command bpm does not implement, so it carries no command."""


HMS_RETRY_CODES = {
    "0701-8004",
    "0701-8005",
    "0701-8007",
    "0701-8012",
    "0702-8012",
    "0703-8012",
    "07FF-8012",
    "07FF-8013",
}
"""Errors Bambu Studio answers with Retry and Confirm instead of its table's buttons
(`DeviceErrorDialog.cpp` `message_containing_retry`)."""

HMS_LIVEVIEW_CODES = {"0300-8003", "0300-8002", "0300-800A"}
"""Errors Bambu Studio adds a View Liveview button to (`s_jump_liveview_error_codes`)."""


def hmsActions(serial_number: str, print_error: int) -> list[dict]:
    """
    The dialog buttons Bambu Studio shows for `print_error` on this printer, in order.

    As `DeviceErrorDialog::apply_result`: an `HMS_RETRY_CODES` error gets Retry and
    Confirm. Otherwise the error is looked up as `%08X` in `HMS_ACTIONS` under the
    serial's first three characters, and an `HMS_LIVEVIEW_CODES` error adds View
    Liveview. Ids Studio does not know, and `REMOVE_CLOSE_BTN`, are dropped.

    Returns a list of `{"id": int, "name": str, "label": str, "command": str}`.
    `command` is empty for a button bpm cannot send (see `HMS_ACTION_COMMAND`).
    """
    if not print_error:
        return []
    ecode = f"{print_error & 0xFFFFFFFF:08X}"
    code = f"{ecode[:4]}-{ecode[4:]}"
    if code in HMS_RETRY_CODES:
        ids = (HMSAction.DBL_CHECK_RETRY, HMSAction.DBL_CHECK_OK)
    else:
        table = HMS_ACTIONS.get(str(serial_number)[:3].upper())
        ids = tuple(table["codes"].get(ecode, ())) if table else ()
        if code in HMS_LIVEVIEW_CODES:
            ids += (HMSAction.JUMP_TO_LIVEVIEW,)
    actions = []
    for action_id in ids:
        if action_id not in HMSAction._value2member_map_:
            continue
        action = HMSAction(action_id)
        if action == HMSAction.REMOVE_CLOSE_BTN:
            continue
        actions.append(
            {
                "id": action.value,
                "name": action.name,
                "label": HMS_ACTION_LABEL[action],
                "command": HMS_ACTION_COMMAND.get(action, ""),
            }
        )
    return actions


class AMSModel(IntEnum):
    """
    AMS model enum
    """

    UNKNOWN = 0
    AMS_1 = 1
    AMS_LITE = 2
    AMS_2_PRO = 3  # N3F in BambuStudio
    AMS_HT = 4  # N3S in BambuStudio


class AMSSeries(Enum):
    """
    AMS Series enum
    """

    UNKNOWN = 0
    GEN_1 = 1
    GEN_2 = 2


class AMSUserSetting(Enum):
    """
    AMS User Settings enum
    """

    CALIBRATE_REMAIN_FLAG = 0
    STARTUP_READ_OPTION = 1
    TRAY_READ_OPTION = 2


class AMSHeatingState(IntEnum):
    """
    AMS Drying/Heater states extracted from bits 4-7 of ams_info.
    Mapped directly from BambuStudio's DryStatus enum.
    Only supported on AMS 2 Pro (N3F) and AMS HT (N3S) models.
    """

    OFF = 0  # No drying active
    CHECKING = 1  # Checking drying status
    DRYING = 2  # Active drying phase
    COOLING = 3  # Cooling after drying
    STOPPING = 4  # Stopping drying process
    ERROR = 5  # Error state
    CANNOT_STOP_HEAT_OOC = 6  # Heat control out of control
    PRODUCT_TEST = 7  # Product testing mode


class AMSDryerSubStatus(IntEnum):
    """
    AMS drying sub-status extracted from bits 22-25 of ams_info.
    Indicates the specific phase of the drying cycle.
    Mapped from BambuStudio's DrySubStatus enum.
    """

    OFF = 0  # No active drying phase
    HEATING = 1  # Heating phase of drying
    DEHUMIDIFY = 2  # Dehumidification phase of drying


class AMSDryerRefusal(IntEnum):
    """
    Why an AMS dryer cannot start now, from each AMS block's `dry_sf_reason` list.
    Mapped from BambuStudio's DevAms::CannotDryReason. The printer sends an empty
    list when a dry can start, and `DRYING_IN_PROGRESS` alone while one runs.
    """

    TASK_OCCUPIED = 0
    INSUFFICIENT_POWER = 1
    AMS_BUSY = 2  # calibrating, reading RFID, loading or unloading
    FILAMENT_AT_OUTLET = 3  # filament fed past the AMS outlet
    INITIATING_DRYING = 4
    NOT_SUPPORTED_IN_2D_MODE = 5
    DRYING_IN_PROGRESS = 6
    UPGRADING = 7
    INSUFFICIENT_POWER_PLUG_IN = 8
    FILAMENT_AT_OUTLET_MANUAL_UNLOAD = 10


# BambuStudio's text for each refusal (AMSDryControl.cpp get_cannot_reason_text).
AMS_DRYER_REFUSAL_TEXT = {
    AMSDryerRefusal.INSUFFICIENT_POWER: (
        "Insufficient power",
        "Too many AMS drying simultaneously. Please plug in the power or stop other drying processes before starting.",
    ),
    AMSDryerRefusal.AMS_BUSY: (
        "AMS is busy",
        "AMS is calibrating | reading RFID | loading/unloading material, please wait.",
    ),
    AMSDryerRefusal.FILAMENT_AT_OUTLET: (
        "Filament in AMS outlet",
        "The high drying temperature may cause AMS blockage, please unload first.",
    ),
    AMSDryerRefusal.INITIATING_DRYING: ("Initiating AMS drying", ""),
    AMSDryerRefusal.NOT_SUPPORTED_IN_2D_MODE: ("Not supported in 2D mode", ""),
    AMSDryerRefusal.DRYING_IN_PROGRESS: (
        "Task in progress",
        "The AMS might be in use during Task.",
    ),
    AMSDryerRefusal.UPGRADING: (
        "Upgrading",
        "Firmware update in progress, please wait...",
    ),
    AMSDryerRefusal.INSUFFICIENT_POWER_PLUG_IN: (
        "Insufficient power",
        "Please plug in the power and then use the drying function.",
    ),
    AMSDryerRefusal.FILAMENT_AT_OUTLET_MANUAL_UNLOAD: (
        "Filament in AMS outlet",
        "The high drying temperature may cause AMS blockage. Please unload the filament manually before proceeding.",
    ),
}
AMS_DRYER_REFUSAL_DEFAULT_TEXT = (
    "System is busy",
    "Initiating other drying processes, please wait a few seconds...",
)


def dryerRefusalMessage(reasons: list[int]) -> str:
    """
    Explains why a dryer cannot start, the way BambuStudio does
    (AMSDryControl.cpp update_state and organize_cannot_reasons_text).

    Returns "" when a dry can start: no reasons, or only `DRYING_IN_PROGRESS`.
    Otherwise one line per reason shown: the first of task in progress, AMS busy
    or filament at the outlet; then insufficient power; then the remaining
    known reasons in the order received. When none of those apply (task
    occupied or a value this table does not know), Studio's "System is busy".
    """
    if not reasons or set(reasons) == {AMSDryerRefusal.DRYING_IN_PROGRESS}:
        return ""

    def line(reason: int) -> str:
        title, detail = AMS_DRYER_REFUSAL_TEXT.get(reason, AMS_DRYER_REFUSAL_DEFAULT_TEXT)
        return f"{title}. {detail}" if detail else f"{title}."

    lines = []
    for primary in (
        AMSDryerRefusal.DRYING_IN_PROGRESS,
        AMSDryerRefusal.AMS_BUSY,
        AMSDryerRefusal.FILAMENT_AT_OUTLET,
        AMSDryerRefusal.FILAMENT_AT_OUTLET_MANUAL_UNLOAD,
    ):
        if primary in reasons:
            lines.append(line(primary))
            break
    if AMSDryerRefusal.INSUFFICIENT_POWER in reasons:
        lines.append(line(AMSDryerRefusal.INSUFFICIENT_POWER))
    for reason in reasons:
        if reason in (
            AMSDryerRefusal.INSUFFICIENT_POWER_PLUG_IN,
            AMSDryerRefusal.NOT_SUPPORTED_IN_2D_MODE,
            AMSDryerRefusal.INITIATING_DRYING,
            AMSDryerRefusal.UPGRADING,
        ):
            lines.append(line(reason))
    if not lines:
        lines.append(line(-1))
    return "\n".join(lines)


class AMSDryerFanStatus(IntEnum):
    """
    AMS drying fan status extracted from bits 18-21 of ams_info.
    Two independent fans (fan1: bits 18-19, fan2: bits 20-21).
    Mapped from BambuStudio's DryFanStatus enum.
    """

    OFF = 0  # Fan is off
    ON = 1  # Fan is running


class ExtensionToolType(Enum):
    """
    Toolhead extension-tool type reported in `device.ext_tool.type`.
    Values are the raw type codes mapped from BambuStudio's DevExtensionTool
    (TOOL_TYPE_* enum). An unrecognized code resolves to `UNKNOWN`; the raw
    code is preserved in `ExtensionToolState.type_raw`.

    * `NONE ("")`: No extension tool attached (or the attached tool is unpowered).
    * `CUTTING_MODULE ("CP00")`: Blade cutting module.
    * `LASER_MODULE ("LB00")`: Laser module.
    * `ENHANCED_COOLING_FAN ("F000")`: Toolhead Enhanced Cooling Fan.
    * `UNKNOWN ("?")`: Unrecognized type code (future extension tool).
    """

    NONE = ""
    CUTTING_MODULE = "CP00"
    LASER_MODULE = "LB00"
    ENHANCED_COOLING_FAN = "F000"
    UNKNOWN = "?"

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN


class ExtensionToolMountState(IntEnum):
    """
    Toolhead extension-tool mount state reported in `device.ext_tool.mount_3d`.
    Values are mapped from BambuStudio's DevExtensionTool MountState enum.

    * `UNKNOWN (-1)`: No telemetry received yet, or unrecognized value.
    * `NOT_MOUNTED (0)`: No extension tool mounted.
    * `MOUNTED (1)`: Extension tool mounted and communicating.
    * `NO_MODULE (2)`: Mount detected but no module present.
    * `NO_CABLE (3)`: Module mounted but its cable is not connected.
    """

    UNKNOWN = -1
    NOT_MOUNTED = 0
    MOUNTED = 1
    NO_MODULE = 2
    NO_CABLE = 3

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN


class ExtruderInfoState(IntEnum):
    """
    Consolidated logical states for extruder sensor status.
    Values represent unique state IDs to prevent bitmask collisions.
    """

    NO_NOZZLE = 0
    EMPTY = 1
    BUFFER_LOADED = 2
    LOADED = 3
    NOT_AVAILABLE = 4


class ExtruderStatus(IntEnum):
    """
    Operational states for physical extruders.
    Values are mapped directly from the Bambu Studio source code (BBL_EXTRUDER_STATE).
    """

    IDLE = 0
    HEATING = 1
    ACTIVE = 2
    SUCCESS = 3
    NOT_AVAILABLE = 4


class NozzleDiameter(Enum):
    """
    Nozzle Diameter enum
    """

    UNKNOWN = 0.0
    POINT_TWO_MM = 0.2
    POINT_FOUR_MM = 0.4
    POINT_SIX_MM = 0.6
    POINT_EIGHT_MM = 0.8


class NozzleType(Enum):
    """
    Canonical cross-model nozzle material type from telemetry.

    This enum intentionally models only material/type categories that appear in
    telemetry and accessory APIs. Encoded variant identifiers such as `HS01`
    are parsed via `parse_nozzle_identifier()` / `parse_nozzle_type()`.
    """

    UNKNOWN = 0
    STAINLESS_STEEL = 1
    HARDENED_STEEL = 2
    TUNGSTEN_CARBIDE = 3
    BRASS = 4
    E3D = 5


class NozzleFlowType(Enum):
    """
    Canonical nozzle flow families used by BambuStudio/Orca nozzle identifiers.

    Encoded as the second character in identifiers such as `HS00-0.4`.
    """

    UNKNOWN = "?"
    STANDARD = "S"
    HIGH_FLOW = "H"
    TPU_HIGH_FLOW = "U"


class NozzleMaterialCode(Enum):
    """
    Canonical material codes used in encoded nozzle identifiers.

    Encoded as characters 3-4 in identifiers such as `HS00-0.4`.
    """

    UNKNOWN = "??"
    STAINLESS_STEEL = "00"
    HARDENED_STEEL = "01"
    TUNGSTEN_CARBIDE = "05"


_FLOW_CODE_TO_TYPE: dict[str, NozzleFlowType] = {
    "S": NozzleFlowType.STANDARD,
    "H": NozzleFlowType.HIGH_FLOW,
    "U": NozzleFlowType.TPU_HIGH_FLOW,
    "A": NozzleFlowType.STANDARD,
    "X": NozzleFlowType.STANDARD,
    "E": NozzleFlowType.HIGH_FLOW,
}

_TYPE_TO_MATERIAL_CODE: dict[NozzleType, NozzleMaterialCode] = {
    NozzleType.STAINLESS_STEEL: NozzleMaterialCode.STAINLESS_STEEL,
    NozzleType.HARDENED_STEEL: NozzleMaterialCode.HARDENED_STEEL,
    NozzleType.TUNGSTEN_CARBIDE: NozzleMaterialCode.TUNGSTEN_CARBIDE,
}

_MATERIAL_CODE_TO_TYPE: dict[str, NozzleType] = {
    NozzleMaterialCode.STAINLESS_STEEL.value: NozzleType.STAINLESS_STEEL,
    NozzleMaterialCode.HARDENED_STEEL.value: NozzleType.HARDENED_STEEL,
    NozzleMaterialCode.TUNGSTEN_CARBIDE.value: NozzleType.TUNGSTEN_CARBIDE,
}

_NOZZLE_TYPE_TELEMETRY_TO_ENUM: dict[str, NozzleType] = {
    "stainless_steel": NozzleType.STAINLESS_STEEL,
    "hardened_steel": NozzleType.HARDENED_STEEL,
    "tungsten_carbide": NozzleType.TUNGSTEN_CARBIDE,
    "brass": NozzleType.BRASS,
    "e3d": NozzleType.E3D,
}

_NOZZLE_TYPE_ENUM_TO_TELEMETRY: dict[NozzleType, str] = {
    NozzleType.STAINLESS_STEEL: "stainless_steel",
    NozzleType.HARDENED_STEEL: "hardened_steel",
    NozzleType.TUNGSTEN_CARBIDE: "tungsten_carbide",
    NozzleType.BRASS: "brass",
    NozzleType.E3D: "E3D",
}


def parse_nozzle_identifier(nozzle_id: str) -> tuple[NozzleFlowType, NozzleType, str]:
    """
    Parse a Bambu-style nozzle identifier into flow family, material, and diameter.

    Supported encoded formats include values such as `HS00-0.4`, `HH01-0.6`,
    and `HU00-0.4`.

    Returns
    -------
    tuple[NozzleFlowType, NozzleType, str]
        A tuple of `(flow_type, nozzle_type, diameter)`.
        Unknown/unsupported parts are returned as `UNKNOWN` enum values.
    """

    if not nozzle_id:
        return (NozzleFlowType.UNKNOWN, NozzleType.UNKNOWN, "")

    clean = nozzle_id.strip()
    if "-" in clean:
        encoded, diameter = clean.split("-", 1)
    else:
        encoded, diameter = clean, ""

    if len(encoded) < 4:
        return (NozzleFlowType.UNKNOWN, NozzleType.UNKNOWN, diameter)

    flow = _FLOW_CODE_TO_TYPE.get(encoded[1], NozzleFlowType.UNKNOWN)
    material_code = encoded[2:4]
    nozzle_type = _MATERIAL_CODE_TO_TYPE.get(material_code, NozzleType.UNKNOWN)

    return (flow, nozzle_type, diameter)


def build_nozzle_identifier(
    flow_type: NozzleFlowType, nozzle_type: NozzleType, diameter: float | str
) -> str:
    """
    Build a canonical Bambu-style nozzle identifier.

    Examples
    --------
    `HS00-0.4`, `HH01-0.6`, `HU00-0.4`
    """

    material = _TYPE_TO_MATERIAL_CODE.get(nozzle_type)
    if material is None:
        raise ValueError(f"Unsupported nozzle_type for encoded ID: {nozzle_type}")

    if flow_type not in {
        NozzleFlowType.STANDARD,
        NozzleFlowType.HIGH_FLOW,
        NozzleFlowType.TPU_HIGH_FLOW,
    }:
        raise ValueError(f"Unsupported flow_type for encoded ID: {flow_type}")

    if isinstance(diameter, float):
        diameter_str = f"{diameter:.1f}"
    else:
        diameter_str = str(diameter)

    return f"H{flow_type.value}{material.value}-{diameter_str}"


def parse_nozzle_type(value: str | None) -> NozzleType:
    """
    Resolve a nozzle type from cross-model telemetry strings or encoded IDs.

    Supports direct telemetry values (for example `hardened_steel`) and encoded
    forms (for example `HH01-0.4`, `HS00`, `HU05`).
    """

    if value is None:
        return NozzleType.UNKNOWN

    clean = value.strip()
    if not clean:
        return NozzleType.UNKNOWN

    telemetry_key = clean.lower()
    if telemetry_key in _NOZZLE_TYPE_TELEMETRY_TO_ENUM:
        return _NOZZLE_TYPE_TELEMETRY_TO_ENUM[telemetry_key]

    if clean in _MATERIAL_CODE_TO_TYPE:
        return _MATERIAL_CODE_TO_TYPE[clean]

    _, nozzle_type, _ = parse_nozzle_identifier(clean)
    if nozzle_type != NozzleType.UNKNOWN:
        return nozzle_type

    try:
        return NozzleType[clean.upper()]
    except (KeyError, ValueError):
        return NozzleType.UNKNOWN


def nozzle_type_to_telemetry(value: NozzleType) -> str:
    """
    Convert canonical `NozzleType` to telemetry/API string.
    """

    return _NOZZLE_TYPE_ENUM_TO_TELEMETRY.get(value, "unknown")


class PlateType(Enum):
    """
    Used by `BambuPrinter.print_3mf_file` to specify which plate should be used when
    starting a print job.
    """

    AUTO = 0
    COOL_PLATE = 1
    ENG_PLATE = 2
    HOT_PLATE = 3
    TEXTURED_PLATE = 4
    NONE = 999


class SpeedLevel(IntEnum):
    """
    Print speed profile levels. Maps human-readable names to the firmware integer codes
    sent in the `print_speed` MQTT command (`param` field) and reported back in `spd_lvl`.

    Used by `BambuPrinter.speed_level` getter (returns the active level) and setter
    (accepts a `SpeedLevel` to change the active profile).
    """

    QUIET = 1
    STANDARD = 2
    SPORT = 3
    LUDICROUS = 4


class DetectorSensitivity(Enum):
    """
    Sensitivity level for X-Cam AI vision detectors (spaghetti, pile-up, clump, air-print).
    The string value is sent directly in the `halt_print_sensitivity` MQTT field.
    """

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class PrinterModel(Enum):
    """
    Printer model enum
    """

    UNKNOWN = "unknown"
    X1C = "x1c"
    X1 = "x1"
    X1E = "x1e"
    P1P = "p1p"
    P1S = "p1s"
    A1_MINI = "a1_mini"
    A1 = "a1"
    P2S = "p2s"
    H2S = "h2s"
    H2D = "h2d"


class PrinterSeries(Enum):
    """
    Printer Series enum
    """

    UNKNOWN = 0
    X1 = 1
    P1 = 2
    A1 = 3
    P2 = 4
    H2 = 5


class PrintOption(Enum):
    """
    Print Option enum
    """

    AUTO_RECOVERY = 0
    FILAMENT_TANGLE_DETECT = 1
    SOUND_ENABLE = 2
    AUTO_SWITCH_FILAMENT = 3
    NOZZLE_BLOB_DETECT = 4
    AIR_PRINT_DETECT = 5


class ServiceState(Enum):
    """
    This enum is used by `bambu-printer-manager` to track the underlying state
    of the `mqtt` connection to the printer.
    """

    NO_STATE = 0
    CONNECTED = 1
    DISCONNECTED = 2
    PAUSED = 3
    QUIT = 4


class TrayState(IntEnum):
    """
    Operational status of the filament tray.
    """

    UNLOADED = 0
    LOADED = 1
    LOADING = 2
    UNLOADING = 3


def decodeError(error: int) -> dict:
    """
    Decodes a raw print_error integer into a full HMS dictionary.
    """
    if error == 0:
        return {}

    raw_hex = f"{error:08X}".upper()
    wiki_slug = "-".join(raw_hex[i : i + 4] for i in range(0, 8, 4))
    res = {
        "code": f"HMS_{wiki_slug}",
        "msg": "Unknown HMS Error",
        "module": "System",
        "severity": "Error",
        "is_critical": False,
        "type": "device_error",
        # e.bambulab.com has pages only for 16-digit HMS codes; an 8-digit print_error
        # lands on its home page, so point at Bambu's table of these codes instead
        "url": "https://wiki.bambulab.com/en/hms/error-code",
    }

    real_module = (error >> 24) & 0xFF
    module_map = {
        0x03: "Mainboard",
        0x05: "AMS",
        0x12: "AMS",
        0x07: "Toolhead",
        0x0B: "Webcam",
        0x10: "HMS",
    }
    res["module"] = module_map.get(real_module, "System")

    msg_list = HMS_STATUS.get("data", {}).get("device_error", {}).get("en", [])
    modules = ["03", "05", "07", "0B", "0C", "10", "12"]
    if raw_hex[:2] in modules:
        modules.remove(raw_hex[:2])
    modules.insert(0, raw_hex[:2])

    for module in modules:
        current_hex = f"{module}{raw_hex[2:]}"
        for entry in msg_list:
            if entry.get("ecode", "").upper() == current_hex.upper():
                res["msg"] = entry.get("intro", res["msg"])
                break
        if res["msg"] != "Unknown HMS Error":
            break

    mask = (error >> 16) & 0xFF
    if mask in (0x00, 0x01):
        res["severity"] = "Fatal" if mask == 0x00 else "Error"
        res["is_critical"] = True
    elif mask == 0x02:
        res["severity"] = "Warning"
        res["is_critical"] = False
    else:
        res["severity"] = "Info"
        res["is_critical"] = False

    return res


def decodeHMS(hms_list: list) -> list[dict]:
    """
    Decodes the raw HMS list from telemetry into a structured list of dictionaries.
    """
    decoded_errors = []
    for item in hms_list:
        if isinstance(item, dict) and isinstance(item.get("code"), str):
            decoded_errors.append(item)
            continue
        try:
            attr = int(item.get("attr", 0))
            code = int(item.get("code", 0))
        except (AttributeError, ValueError, TypeError):
            continue
        if attr == 0:
            continue

        ecode = f"{attr:08X}{code:08X}"
        wiki_slug = "-".join(ecode[i : i + 4] for i in range(0, 16, 4))
        res = {
            "code": f"HMS_{wiki_slug}",
            "msg": "Unknown HMS Error",
            "module": "System",
            "severity": "Error",
            "is_critical": False,
            "type": "device_hms",
            "url": f"https://e.bambulab.com/?e={ecode}",
        }

        mid = (attr >> 24) & 0xFF
        mask = (attr >> 16) & 0xFF
        module_map = {
            0x03: "Mainboard",
            0x05: "AMS",
            0x12: "AMS",
            0x07: "Toolhead",
            0x0B: "Webcam",
            0x10: "HMS",
        }
        res["module"] = module_map.get(mid, "System")

        msg_list = HMS_STATUS.get("data", {}).get("device_hms", {}).get("en", [])
        for entry in msg_list:
            if entry.get("ecode", "").upper() == ecode:
                res["msg"] = entry.get("intro", res["msg"])
                break

        if mask in (0x00, 0x01):
            res["severity"], res["is_critical"] = (
                ("Fatal" if mask == 0x00 else "Error"),
                True,
            )
        elif mask == 0x02:
            res["severity"] = "Warning"
        else:
            res["severity"] = "Info"
        decoded_errors.append(res)
    return decoded_errors


def getAMSHeatingState(ams_info: int) -> AMSHeatingState:
    """
    Decodes the AMS drying/heater state from bits 4-7 of the ams_info value.

    This implementation follows BambuStudio's DevFilaSystem parsing logic,
    extracting DryStatus from the info field.

    Args:
        ams_info: Numeric AMS info value containing drying status in bits 4-7.

    Returns:
        AMSHeatingState enum representing the current drying/heater state.
        Only AMS 2 Pro (N3F) and AMS HT (N3S) support active drying states.
    """
    # Extract DryStatus from bits 4-7 (right-shift by 4, mask 0x0F)
    dry_status = (ams_info >> 4) & 0x0F

    return AMSHeatingState(dry_status)


def getAMSModelBySerial(serial: str) -> AMSModel:
    """
    Returns the hardware model based on the serial number prefix.
    """
    prefix = serial[:3].upper()
    if prefix == "19C":
        return AMSModel.AMS_2_PRO
    if prefix == "19F":
        return AMSModel.AMS_HT
    if prefix == "006":
        return AMSModel.AMS_1
    if prefix == "03C":
        return AMSModel.AMS_LITE
    return AMSModel.UNKNOWN


def getAMSSeriesByModel(model: AMSModel) -> AMSSeries:
    """
    Returns the AMS series enum based on the provided model.
    """
    if model in (AMSModel.AMS_1, AMSModel.AMS_LITE):
        return AMSSeries.GEN_1
    if model in (AMSModel.AMS_HT, AMSModel.AMS_2_PRO):
        return AMSSeries.GEN_2
    return AMSSeries.UNKNOWN


def getPrinterModelBySerial(serial: str) -> PrinterModel:
    """
    Returns the Printer model enum based on the provided serial #.
    """
    mapping = {
        "00M": PrinterModel.X1C,
        "00W": PrinterModel.X1,
        "03W": PrinterModel.X1E,
        "01S": PrinterModel.P1P,
        "01P": PrinterModel.P1S,
        "030": PrinterModel.A1_MINI,
        "039": PrinterModel.A1,
        "22E": PrinterModel.P2S,
        "093": PrinterModel.H2S,
        "094": PrinterModel.H2D,
    }
    prefix = serial[:3]
    return mapping.get(prefix, PrinterModel.UNKNOWN)


def getPrinterSeriesByModel(model: PrinterModel) -> PrinterSeries:
    """
    Returns the Printer series enum based on the provided model.
    """
    try:
        return PrinterSeries[model.name[:2]]
    except (KeyError, AttributeError):
        return PrinterSeries.UNKNOWN


def parseAMSInfo(info_hex: str) -> dict:
    """
    Extracts all documented telemetry attributes from the AMS info hex string.

    Based on BambuStudio's DevFilaSystemParser::ParseAmsInfo implementation.
    Complete bit field mapping (32-bit integer):
    - Bits 0-3: AMS type (1=AMS, 2=AMS_LITE, 3=AMS_2_PRO/N3F, 4=AMS_HT/N3S)
    - Bits 4-7: Dry status (OFF/CHECKING/DRYING/COOLING/STOPPING/ERROR/etc)
    - Bits 8-11: Extruder ID (for H2D toolhead assignment)
    - Bits 18-19: Dry fan 1 status (OFF=0, ON=1)
    - Bits 20-21: Dry fan 2 status (OFF=0, ON=1)
    - Bits 22-25: Dry sub-status (OFF/HEATING/DEHUMIDIFY)

    Args:
        info_hex: Hexadecimal string representation of AMS info value

    Returns:
        Dictionary with all extracted telemetry fields
    """
    info = int(info_hex, 16)

    ams_type = info & 0x0F  # Bits 0-3
    dry_status = (info >> 4) & 0x0F  # Bits 4-7
    extruder_id = (info >> 8) & 0x0F  # Bits 8-11
    dry_fan1_status = (info >> 18) & 0x03  # Bits 18-19
    dry_fan2_status = (info >> 20) & 0x03  # Bits 20-21
    dry_sub_status = (info >> 22) & 0x0F  # Bits 22-25

    ret = {
        "ams_type": AMSModel(ams_type) if ams_type in range(5) else AMSModel.UNKNOWN,
        "heater_state": AMSHeatingState(dry_status),
        "extruder_id": extruder_id,
        "dry_fan1_status": AMSDryerFanStatus(dry_fan1_status),
        "dry_fan2_status": AMSDryerFanStatus(dry_fan2_status),
        "dry_sub_status": AMSDryerSubStatus(dry_sub_status),
    }

    # print(f"\r\n{ret}\r\n")
    return ret


def parseAMSStatus(status_int: int) -> str:
    """
    Maps the ams_status code to human-readable descriptions.
    """
    main_status = (status_int >> 8) & 0xFF
    status_map = {
        0x00: "Idle",
        0x01: "Filament Changing",
        0x02: "RFID Identifying",
        0x03: "Assist/Engaged",
        0x04: "Calibration",
        0x10: "Self Check",
        0x20: "Debug",
        0xFF: "Unknown",
    }
    return status_map.get(main_status, "Idle")


def parseFilamentStep(
    ams_status: int,
    target_tray_id: int,
    filament_at_extruder: bool = True,
    previous: FilamentStep = FilamentStep.IDLE,
) -> tuple[FilamentStep, FilamentStepType]:
    """
    Names the filament load or unload step, as Bambu Studio's `StatusPanel` does.

    Parameters
    ----------
    * ams_status : int - raw `ams_status`; the high byte 1 is a filament change and the
        low byte is the step code.
    * target_tray_id : int - the loading extruder's target tray: 254 or 255 is an external
        holder (`VT_LOAD`), -1 is no target (`UNLOAD`), anything else is an AMS load.
    * filament_at_extruder : bool - the printer's `hw_switch_state` (True when unknown).
        Studio names codes 0x05 and 0x07 of an AMS load differently when it is False.
    * previous : FilamentStep - the step before; code 0x09 is a wait that keeps it.

    Returns `(FilamentStep, FilamentStepType)`; `IDLE` when no change runs or the code
    is not one Studio names for that kind of change.
    """
    if (ams_status >> 8) & 0xFF != 0x01:
        return FilamentStep.IDLE, FilamentStepType.LOAD
    sub = ams_status & 0xFF
    if target_tray_id in (254, 255):
        vt_steps = {
            0x02: FilamentStep.HEAT_NOZZLE,
            0x05: FilamentStep.PUSH_NEW_FILAMENT,
            0x06: FilamentStep.CONFIRM_EXTRUDED,
            0x07: FilamentStep.PURGE_OLD_FILAMENT,
        }
        return vt_steps.get(sub, FilamentStep.IDLE), FilamentStepType.VT_LOAD
    unload = target_tray_id == -1
    step_type = FilamentStepType.UNLOAD if unload else FilamentStepType.LOAD
    with_temp = not unload and not filament_at_extruder
    steps = {
        0x02: FilamentStep.HEAT_NOZZLE,
        0x03: FilamentStep.CUT_FILAMENT,
        0x04: FilamentStep.PULL_CURR_FILAMENT,
        0x05: FilamentStep.CUT_FILAMENT if with_temp else FilamentStep.PUSH_NEW_FILAMENT,
        0x06: FilamentStep.PUSH_NEW_FILAMENT,
        0x07: FilamentStep.PULL_CURR_FILAMENT
        if with_temp
        else FilamentStep.PURGE_OLD_FILAMENT,
        0x08: FilamentStep.CHECK_POSITION,
        0x0B: FilamentStep.CHECK_POSITION,
    }
    if sub == 0x09:
        return previous, step_type
    if sub not in steps:
        return FilamentStep.IDLE, FilamentStepType.UNLOAD
    return steps[sub], step_type


def parseExtruderInfo(info_int: int) -> ExtruderInfoState:
    """
    Decodes the extruder 'info' bit-packed status using unique ExtruderInfoState names.
    """
    if not (info_int & 0x08):
        return ExtruderInfoState.NO_NOZZLE
    if info_int & 0x02:
        return ExtruderInfoState.LOADED
    if info_int & 0x04:
        return ExtruderInfoState.BUFFER_LOADED
    return ExtruderInfoState.EMPTY


def parseExtruderStatus(stat_int: int) -> ExtruderStatus:
    """
    Decodes the operational extruder state using the exhaustive Enum map.
    """
    working_bits = (stat_int >> 8) & 0x03
    if working_bits in (0x02, 0x03):
        return ExtruderStatus.ACTIVE
    if stat_int & 0x01:
        return ExtruderStatus.HEATING
    return ExtruderStatus.IDLE


def parseExtruderTrayState(extruder: int, hotend, slot) -> int:
    """
    Decodes an extruder's tray from its `device.extruder.info[]` `hnow`/`snow` (or
    `htar`/`star`) pair.

    Parameters
    ----------
    * extruder : int - the extruder id (0 right, 1 left).
    * hotend : int - `hnow` or `htar`; 254 means the external holder.
    * slot : int - `snow` or `star`.

    Returns the extruder's external holder (255 right, 254 left) when `hotend` is 254 or
    `slot` is 0xFF00 (right) / 0xFE00 (left); -1 when the low byte is 255 (no tray, e.g.
    0xFFFF right or 0xFEFF left, an unload's target); otherwise the slot's low byte.
    """
    if (
        hotend == 254
        or (extruder == 0 and slot == 65280)
        or (extruder == 1 and slot == 65024)
    ):
        return 255 - extruder
    # the low byte 255 is no slot (0xFFFF right, 0xFEFF left): no tray, an unload's target
    if slot & 0xFF == 255:
        return -1
    else:
        return slot & 0xFF


VIRTUAL_TRAY_MAIN_ID = 255
"""Virtual tray id of the main (right on H2D) extruder's external spool holder."""

VIRTUAL_TRAY_DEPUTY_ID = 254
"""Virtual tray id of the deputy (left on H2D) extruder's external spool holder."""


def resolve_external_spool_trays(
    filament_extruders: list[int],
    physical_extruder_map: list[int],
    used_filament_ids: list[int],
) -> list[int]:
    """
    Name the external spool holder that feeds each filament of a sliced plate on a
    dual-nozzle printer.

    The slicer fixes which extruder prints each filament, so the holder is derived
    from the plate, never chosen by the caller.  `filament_extruders` (the plate's
    `filament_maps` in `slice_info.config`) gives each filament's 1-based *logical*
    extruder, and `physical_extruder_map` (from the plate gcode config block) maps
    that logical extruder to a physical one, `0` for the main extruder and `1` for
    the deputy.  On H2D the main extruder is the right one and the map is `1,0`, so
    logical extruder 1 is the LEFT extruder.

    Parameters
    ----------
    * filament_extruders : list[int] - 1-based logical extruder per filament,
        index `i` is filament id `i + 1`.
    * physical_extruder_map : list[int] - physical extruder per logical extruder,
        index `j` is logical extruder `j + 1`.
    * used_filament_ids : list[int] - 1-based ids of the filaments the plate uses.

    Returns
    -------
    A list the length of `filament_extruders`: `VIRTUAL_TRAY_MAIN_ID` (255) or
    `VIRTUAL_TRAY_DEPUTY_ID` (254) at each used filament's index, `-1` elsewhere.

    Raises
    ------
    `ValueError` when the plate carries no extruder assignment or no physical map,
    or names an extruder or filament id outside them.  A wrong holder prints on the
    wrong side, so this never guesses.
    """
    if not filament_extruders:
        raise ValueError("plate has no filament extruder assignment (filament_maps)")
    if not physical_extruder_map:
        raise ValueError("plate has no physical_extruder_map")

    trays = [-1] * len(filament_extruders)
    for filament_id in used_filament_ids:
        index = filament_id - 1
        if not 0 <= index < len(filament_extruders):
            raise ValueError(
                f"filament id [{filament_id}] is outside the plate's filaments"
            )

        logical = filament_extruders[index]
        if not 1 <= logical <= len(physical_extruder_map):
            raise ValueError(
                f"filament id [{filament_id}] uses logical extruder [{logical}] outside physical_extruder_map"
            )

        physical = physical_extruder_map[logical - 1]
        if physical == 0:
            trays[index] = VIRTUAL_TRAY_MAIN_ID
        elif physical == 1:
            trays[index] = VIRTUAL_TRAY_DEPUTY_ID
        else:
            raise ValueError(f"physical extruder [{physical}] is neither 0 nor 1")

    return trays


def parseRFIDStatus(status):
    """
    Can be used to parse `ams_rfid_status`
    """
    rfid_map = {
        0: "RFID Idle",
        1: "RFID Reading",
        2: "GCode Translating",
        3: "GCode Running",
        4: "RFID Assistant",
        5: "Switch Filament",
        6: "Has Filament",
    }
    return rfid_map.get(status, "Unknown")


def parseStage(stage_int: int) -> str:
    """
    Maps stg_cur numeric codes to human-readable print stages.
    """
    stage_map = {
        -1: "",
        0: "",
        1: "Auto bed leveling",
        2: "Heatbed preheating",
        3: "Sweeping XY mech mode",
        4: "Changing filament",
        5: "M400 pause",
        6: "Filament runout pause",
        7: "Heating hotend",
        8: "Calibrating extrusion",
        9: "Scanning bed surface",
        10: "Inspecting first layer",
        11: "Identifying build plate",
        12: "Calibrating Micro Lidar",
        13: "Homing toolhead",
        14: "Cleaning nozzle tip",
        15: "Temp check",
        16: "Paused by user",
        17: "Front cover falling",
        18: "Lidar calibration (alt)",
        19: "Calibrating flow",
        20: "Nozzle temp malfunction",
        21: "Bed temp malfunction",
        22: "Filament unloading",
        23: "Skip step pause",
        24: "Filament loading",
        25: "Motor noise calibration",
        26: "AMS lost pause",
        27: "Fan speed pause",
        28: "Chamber control error",
        29: "Cooling chamber",
        30: "Custom Gcode pause",
        31: "Motor noise showoff",
        32: "Nozzle cover pause",
        33: "Cutter error pause",
        34: "First layer error pause",
        35: "Nozzle clog pause",
        36: "Absolute accuracy pre-check",
        37: "Chamber control",
        38: "Absolute accuracy post-check",
        39: "Nozzle Offset Calibration",
        40: "Bed level high temperature",
        41: "Check quick release",
        42: "Check door and cover",
        43: "Laser calibration",
        44: "Check platform",
        45: "Check birdeye camera position",
        46: "Calibrate birdeye camera",
        47: "Bed level phase 1",
        48: "Bed level phase 2",
        49: "Heating chamber",
        50: "Heated bed cooling",
        51: "Print calibration lines",
        52: "Check material",
        53: "Calibrating live view camera",
        54: "Waiting for heatbed temperature",
        55: "Check material position",
        56: "Calibrating cutter model offset",
        57: "Measuring surface",
        58: "Thermal preconditioning",
        70: "Leading filament",
        71: "Reached toolhead",
        72: "Hotend type detection",
        73: "Build-plate alignment",
        74: "Heatbed object detection",
        75: "Heatbed object detection",
        76: "Cutting",
        77: "Tool switching",
        100: "Printing",
        245: "Enhanced fan full speed",
        246: "Enhanced fan half speed",
        247: "Enhanced fan off",
        255: "Completed",
    }
    return stage_map.get(stage_int, f"Stage [{stage_int}]")


def scaleFanSpeed(raw_val: Any) -> int:
    """
    Scales proprietary 0-15 fan speed values to a 0-100 percentage.
    """
    try:
        val = int(raw_val)
        return min(max(round((val / 15.0) * 100), 0), 100)
    except Exception:
        return 0


def sortFileTreeAlphabetically(source) -> dict:
    """
    Sorts a dict of file/directory nodes hierarchically.
    """

    def sort_node_list(node_list):
        for item in node_list:
            if item.get("id", "").endswith("/") and "children" in item:
                item["children"] = sort_node_list(item["children"])
        return sorted(
            node_list,
            key=lambda i: (not i.get("id", "").endswith("/"), i.get("name", "").lower()),
        )

    source["children"] = sort_node_list(source["children"])
    return source


def unpackTemperature(raw_temp: int) -> tuple[float, float]:
    """
    Unpacks a 32-bit packed temperature integer into a tuple of (Actual, Target).
    """
    return float(raw_temp & 0xFFFF), float((raw_temp >> 16) & 0xFFFF)


def get_file_md5(file_path: str | Path) -> str:
    """
    Generates an MD5 hex hash for a given file.

    Args:
        file_path: The path to the file (string or Path object).

    Returns:
        The 32-character MD5 hexadecimal string.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    path = Path(file_path)

    if not path.is_file():
        raise FileNotFoundError(f"No file found at: {path}")

    md5_hash = hashlib.md5()

    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            md5_hash.update(chunk)

    return md5_hash.hexdigest().upper()


def jsonSerializer(obj: Any) -> Any:
    """
    Module-level JSON serializer for use with `json.dumps(default=jsonSerializer)`.

    Handles dataclasses, objects with `__dict__`, and falls back to `str()`.
    Skips MQTT clients, threads, and `mappingproxy` instances that cannot be
    serialized meaningfully.
    """
    try:
        if isinstance(obj, Thread):
            return ""
        if getattr(obj.__class__, "__module__", "").startswith("paho.mqtt"):
            return ""
        if str(obj.__class__).replace("<class '", "").replace("'>", "") == "mappingproxy":
            return ""
        return getattr(obj, "__dict__", str(obj))
    except Exception:
        return ""


# ---------------------------------------------------------------------------
# Disk-persistence framework
# ---------------------------------------------------------------------------
# General-purpose helpers for persisting any JSON-serializable runtime value
# to a named cache directory.  All state that BPM needs to survive across
# process restarts should flow through these four functions.
#
# Pattern:
#   cache_dir  = printer_cache_dir(config.bpm_cache_path, config.serial_number) / "<subdir>"
#   key        = make_cache_key(<raw identifier>)
#   cache_write(cache_dir, key, {"field": value})
#   data       = cache_read(cache_dir, key)          # returns None on miss
#   cache_delete(cache_dir, key)
# ---------------------------------------------------------------------------


def printer_cache_dir(bpm_cache_path: Path | None, serial_number: str | None) -> Path:
    """
    One printer's own cache folder: ``bpm_cache_path/<serial>``, or ``bpm_cache_path``
    itself when no serial is set.

    Every cached file is filed per printer so containers sharing one cache folder never
    read each other's job record, start time or project metadata.
    """
    base = bpm_cache_path or Path()
    return base / serial_number if serial_number else base


def make_cache_key(raw: str, max_len: int = 80) -> str | None:
    """
    Sanitize a raw string into a filesystem-safe cache key.

    Strips leading/trailing whitespace, replaces ``/`` and spaces with ``_``,
    and truncates to *max_len* characters.  Returns ``None`` when the result
    would be an empty string (i.e. the input carried no usable content).

    Args:
        raw:     The source identifier (e.g. subtask name, gcode file path).
        max_len: Maximum length of the returned key (default 80).

    Returns:
        A non-empty sanitized string, or ``None``.
    """
    sanitized = raw.strip().replace("/", "_").replace(" ", "_")
    return sanitized[:max_len] or None


def cache_write(cache_dir: Path, key: str, value: Any) -> None:
    """
    Persist *value* to ``cache_dir/<key>.json``.

    *value* must be JSON-serializable (dict, list, scalar).  The cache
    directory is created if it does not already exist.  All errors are
    silently swallowed so callers never need to guard this call.

    Args:
        cache_dir: Directory under ``bpm_cache_path`` (e.g. ``…/elapsed``).
        key:       Filename stem produced by :func:`make_cache_key`.
        value:     Any JSON-serializable object to persist.
    """
    try:
        cache_dir.mkdir(parents=True, exist_ok=True)
        (cache_dir / f"{key}.json").write_text(json.dumps(value))
    except Exception:
        pass


def cache_read(cache_dir: Path, key: str, default: Any = None) -> Any:
    """
    Load a persisted value from ``cache_dir/<key>.json``.

    Returns *default* (``None`` unless overridden) on any error — missing
    file, corrupt JSON, permission error, etc.  Callers should always
    treat ``None`` / *default* as a cache miss and fall back gracefully.

    Args:
        cache_dir: Directory under ``bpm_cache_path``.
        key:       Filename stem produced by :func:`make_cache_key`.
        default:   Value to return on any read failure (default ``None``).

    Returns:
        The deserialized value, or *default*.
    """
    try:
        return json.loads((cache_dir / f"{key}.json").read_text())
    except Exception:
        return default


def cache_delete(cache_dir: Path, key: str) -> None:
    """
    Remove ``cache_dir/<key>.json`` if it exists.

    Silently ignores missing files and all other errors.

    Args:
        cache_dir: Directory under ``bpm_cache_path``.
        key:       Filename stem produced by :func:`make_cache_key`.
    """
    try:
        (cache_dir / f"{key}.json").unlink(missing_ok=True)
    except Exception:
        pass
