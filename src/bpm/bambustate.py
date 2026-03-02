"""
`bambustate` provides a unified, thread-safe representation of a Bambu Lab printer's
operational state, synchronized via MQTT telemetry.
"""

# region imports
import logging
from dataclasses import asdict, dataclass, field, replace
from typing import TYPE_CHECKING, Any, Self

from bpm.bambuconfig import PrinterCapabilities
from bpm.bambuspool import BambuSpool
from bpm.bambutools import (
    ActiveTool,
    AirConditioningMode,
    AMSDryFanStatus,
    AMSDrySubStatus,
    AMSHeatingState,
    AMSModel,
    ExtruderInfoState,
    ExtruderStatus,
    LoggerName,
    NozzleFlowType,
    NozzleType,
    TrayState,
    build_nozzle_identifier,
    decodeError,
    decodeHMS,
    getAMSModelBySerial,
    parse_nozzle_identifier,
    parse_nozzle_type,
    parseAMSInfo,
    parseAMSStatus,
    parseExtruderInfo,
    parseExtruderStatus,
    parseExtruderTrayState,
    scaleFanSpeed,
    unpackTemperature,
)

if TYPE_CHECKING:
    from bpm.bambuprinter import BambuPrinter

# endregion

logger = logging.getLogger(LoggerName)


@dataclass(frozen=True)
class NozzleCharacteristics:
    """Normalized nozzle characteristics across telemetry and encoded identifiers.

    This dataclass captures nozzle material, diameter, and optional flow-family
    metadata. It is intended to provide a single canonical representation that
    can be built from telemetry fields (for example `nozzle_type`,
    `nozzle_diameter`) and optional encoded nozzle identifiers (for example
    `HS00-0.4`).
    """

    material: NozzleType = NozzleType.UNKNOWN
    """Canonical nozzle material/type parsed from telemetry or encoded ID."""
    diameter_mm: float = 0.0
    """Nozzle diameter in millimeters."""
    flow: NozzleFlowType = NozzleFlowType.UNKNOWN
    """Optional nozzle flow family (standard/high-flow/TPU high-flow)."""
    encoded_id: str = ""
    """Raw encoded identifier such as `HS00-0.4` when available."""
    telemetry_type_raw: str = ""
    """Original raw `nozzle_type` string from telemetry payloads."""

    @classmethod
    def from_telemetry(
        cls,
        nozzle_type: str | None,
        nozzle_diameter: str | float | int | None,
        nozzle_id: str | None = None,
        flow_type: NozzleFlowType = NozzleFlowType.UNKNOWN,
    ) -> Self:
        """Build a `NozzleCharacteristics` instance from telemetry fields.

        Parameters
        ----------
        nozzle_type : str | None
            Raw nozzle type string (for example `hardened_steel`).
        nozzle_diameter : str | float | int | None
            Raw nozzle diameter value in millimeters.
        nozzle_id : str | None
            Optional encoded identifier (for example `HS00-0.4`).

        Returns
        -------
        Self
            Normalized nozzle characteristics instance.
        """
        material = parse_nozzle_type(nozzle_type)
        diameter = float(nozzle_diameter) if nozzle_diameter is not None else 0.0

        flow = flow_type

        telemetry_type = (nozzle_type or "").strip()
        if telemetry_type:
            parsed_flow_from_type, parsed_material_from_type, _ = parse_nozzle_identifier(
                telemetry_type
            )
            if parsed_flow_from_type != NozzleFlowType.UNKNOWN:
                flow = parsed_flow_from_type
            if (
                material == NozzleType.UNKNOWN
                and parsed_material_from_type != NozzleType.UNKNOWN
            ):
                material = parsed_material_from_type

        encoded = (nozzle_id or "").strip()
        if encoded:
            parsed_flow, parsed_material, _ = parse_nozzle_identifier(encoded)
            if parsed_flow != NozzleFlowType.UNKNOWN:
                flow = parsed_flow
            if material == NozzleType.UNKNOWN and parsed_material != NozzleType.UNKNOWN:
                material = parsed_material

        return cls(
            material=material,
            diameter_mm=diameter,
            flow=flow,
            encoded_id=encoded,
            telemetry_type_raw=(nozzle_type or ""),
        )

    def to_identifier(self) -> str:
        """Return the best available encoded nozzle identifier.

        Returns the original `encoded_id` when present. Otherwise, it attempts
        to build one from normalized material/flow/diameter values.
        """
        if self.encoded_id:
            return self.encoded_id
        if self.flow == NozzleFlowType.UNKNOWN:
            return ""
        return build_nozzle_identifier(self.flow, self.material, self.diameter_mm)


@dataclass
class ExtruderState:
    """State for an individual physical extruder toolhead."""

    id: int = 0
    """Physical ID."""
    temp: float = 0.0
    """Current Temp."""
    temp_target: int = 0
    """Target Temp."""
    info_bits: int = 0
    """Raw bitmask."""
    state: ExtruderInfoState = ExtruderInfoState.NO_NOZZLE
    """Filament status."""
    status: ExtruderStatus = ExtruderStatus.IDLE
    """Op state."""
    nozzle: NozzleCharacteristics = field(default_factory=NozzleCharacteristics)
    """Normalized nozzle characteristics."""
    active_tray_id: int = -1
    """The active tray for this extruder."""
    target_tray_id: int = -1
    """The target tray for this extruder."""
    tray_state: TrayState = TrayState.LOADED
    """The tray state of this extruder"""
    assigned_to_ams_id: int = -1
    """The id of the ams associated with this extruder"""


@dataclass
class AMSUnitState:
    """State information about an individual AMS unit."""

    ams_id: int
    """Unique ID."""
    chip_id: str = ""
    """Hardware serial."""
    model: AMSModel = AMSModel.UNKNOWN
    """`AMSModel` for this unit"""
    temp_actual: float = 0.0
    """Actual temp."""
    temp_target: int = 0
    """Target drying temp."""
    humidity_index: int = 0
    """Humidity index."""
    humidity_raw: int = 0
    """Raw humidity."""
    ams_info: int = 0
    """Underlying ams info value"""
    heater_state: AMSHeatingState = AMSHeatingState.OFF
    """The computed state of the AMS's heater"""
    dry_fan1_status: AMSDryFanStatus = AMSDryFanStatus.OFF
    """Drying fan 1 status (bits 18-19 of ams_info)"""
    dry_fan2_status: AMSDryFanStatus = AMSDryFanStatus.OFF
    """Drying fan 2 status (bits 20-21 of ams_info)"""
    dry_sub_status: AMSDrySubStatus = AMSDrySubStatus.OFF
    """Drying sub-status phase (bits 22-25 of ams_info)"""
    dry_time: int = 0
    """Minutes left."""
    tray_exists: list[bool] = field(default_factory=lambda: [False] * 4)
    """Slot presence."""
    assigned_to_extruder: ActiveTool = ActiveTool.SINGLE_EXTRUDER
    """Target tool computed from raw_extruder_id"""


@dataclass
class BambuClimate:
    """Contains all climate related attributes"""

    bed_temp: float = 0.0
    """Bed temp."""
    bed_temp_target: int = 0
    """Bed target."""
    airduct_mode: int = -1
    """Raw current mode."""
    airduct_sub_mode: int = -1
    """Raw sub mode."""
    chamber_temp: float = 0.0
    """Chamber temp."""
    chamber_temp_target: int = 0
    """Chamber target."""
    air_conditioning_mode: AirConditioningMode = AirConditioningMode.NOT_SUPPORTED
    """The mode the printer's AC is in if equipped with one."""
    part_cooling_fan_speed_percent: int = 0
    """Part fan %."""
    part_cooling_fan_speed_target_percent: int = 0
    """Part target %."""
    aux_fan_speed_percent: int = 0
    """aux fan %."""
    exhaust_fan_speed_percent: int = 0
    """Exhaust (chamber) fan %."""
    heatbreak_fan_speed_percent: int = 0
    """Heatbreak fan %."""
    zone_intake_open: bool = False
    """Heater power."""
    zone_part_fan_percent: int = 0
    """Internal %."""
    zone_aux_percent: int = 0
    """aux %."""
    zone_exhaust_percent: int = 0
    """Exhaust %."""
    zone_top_vent_open: bool = False
    """Top vent status - derived from exhaust fan on and cooling ac mode."""
    is_chamber_door_open: bool = False
    """ For printers that support it (see `PrinterCapabilities.has_chamber_door_sensor`), reports whether the chamber door is open """
    is_chamber_lid_open: bool = False
    """ For printers that support it (see `PrinterCapabilities.has_chamber_door_sensor`), reports whether the chamber lid is open """


@dataclass
class BambuState:
    """Representation of the Bambu printer state synchronized via MQTT."""

    gcode_state: str = "IDLE"
    """Execution state."""
    active_ams_id: int = -1
    """Current active AMS unit id"""
    active_tray_id: int = 255
    """Current tray."""
    active_tray_state: TrayState = TrayState.UNLOADED
    """Loading enum."""
    active_tray_state_name: str = TrayState.UNLOADED.name
    """Loading string."""
    target_tray_id: int = -1
    """Next tray."""
    active_tool: ActiveTool = ActiveTool.SINGLE_EXTRUDER
    """Active toolhead."""
    is_external_spool_active: bool = False
    """Ext spool flag."""
    active_nozzle_temp: float = 0.0
    """Nozzle temp."""
    active_nozzle_temp_target: int = 0
    """Nozzle target."""
    ams_status_raw: int = 0
    """Raw AMS status."""
    ams_status_text: str = ""
    """Human AMS status."""
    ams_exist_bits: int = 0
    """AMS mask."""
    ams_connected_count: int = 0
    """AMS count."""
    ams_units: list[AMSUnitState] = field(default_factory=list)
    """Unit details."""
    extruders: list[ExtruderState] = field(default_factory=list)
    """Extruder details."""
    spools: list[BambuSpool] = field(default_factory=list)
    """All spools associated with this printer"""
    print_error: int = 0
    """Main error."""
    hms_errors: list[dict] = field(default_factory=list)
    """HMS list."""
    wifi_signal_strength: str = ""
    """Wi-Fi signal strength in dBm"""
    climate: BambuClimate = field(default_factory=BambuClimate)
    """Contains all climate related attributes"""
    stat: str = "0"
    fun: str = "0"

    @classmethod
    def fromJson(cls, data: dict[str, Any], printer: "BambuPrinter") -> "BambuState":
        """Parses root MQTT payloads into a hierachical BambuState object."""

        current_state = printer.printer_state
        config = printer.config
        aji = printer.active_job_info

        base = current_state if current_state else cls()
        info = data.get("info", {})
        p = data.get("print", {})

        if (
            p.get("command", "") == "ams_filament_drying"
            and p.get("result", "") == "success"
        ):
            ams_id = p.get("ams_id", -1)
            ams = next((u for u in base.ams_units if u.ams_id == ams_id), None)
            if ams:
                ams.temp_target = int(p.get("temp", 0))

        ams_root = p.get("ams", {})
        device = p.get("device", {})

        extruder_root = device.get("extruder", {})
        nozzle_root = device.get("nozzle", {})
        ctc_root = device.get("ctc", {})
        airduct_root = device.get("airduct", {})

        modules = info.get("module", [])
        updates = {}

        # CAPABILITIES
        caps = asdict(config.capabilities)
        if ctc_root:
            caps["has_chamber_temp"] = True
        if "ams" in ams_root or "ams" in p:
            caps["has_ams"] = True
        if airduct_root:
            caps["has_air_filtration"] = True
        if len(extruder_root.get("info", [])) > 1:
            caps["has_dual_extruder"] = True

        caps["has_camera"] = True

        xcam_data = p.get("xcam", None)
        if xcam_data:
            caps["has_lidar"] = xcam_data.get("first_layer_inspector", False)
        else:
            caps["has_lidar"] = config.capabilities.has_lidar

        new_caps = PrinterCapabilities(**caps)

        climate = asdict(base.climate)
        updates["climate"] = BambuClimate(**climate)

        # STATUS & PROGRESS
        updates["gcode_state"] = p.get("gcode_state", base.gcode_state)

        updates["fun"] = p.get("fun", base.fun)
        fun = int(updates["fun"], 16)
        new_caps.has_chamber_door_sensor = bool((fun >> 12) & 0x01)
        new_caps.has_spaghetti_detector_support = bool((fun >> 42) & 0x01)
        new_caps.has_purgechutepileup_detector_support = bool((fun >> 43) & 0x01)
        new_caps.has_nozzleclumping_detector_support = bool((fun >> 44) & 0x01)
        new_caps.has_airprinting_detector_support = bool((fun >> 45) & 0x01)

        if new_caps.has_chamber_door_sensor:
            updates["stat"] = p.get("stat", base.stat)
            stat = int(updates["stat"], 16)
            updates["climate"].is_chamber_door_open = bool((stat >> 23) & 0x01)
            updates["climate"].is_chamber_lid_open = bool((stat >> 24) & 0x01)

        # AIRDUCT
        if airduct_root:
            updates["climate"].airduct_mode = int(
                airduct_root.get("modeCur", base.climate.airduct_mode)
            )
            updates["climate"].airduct_sub_mode = int(
                airduct_root.get("subMode", base.climate.airduct_sub_mode)
            )

            if updates["climate"].airduct_mode == 1:
                updates["climate"].air_conditioning_mode = AirConditioningMode.HEAT_MODE
            elif updates["climate"].airduct_mode == 0:
                updates["climate"].air_conditioning_mode = AirConditioningMode.COOL_MODE
                base.climate.chamber_temp_target = 0
            else:
                updates[
                    "climate"
                ].air_conditioning_mode = AirConditioningMode.NOT_SUPPORTED

            parts = {part["id"]: part["state"] for part in airduct_root.get("parts", [])}

            updates["climate"].zone_part_fan_percent = parts.get(
                16, base.climate.zone_part_fan_percent
            )
            updates["climate"].zone_aux_percent = parts.get(
                32, base.climate.zone_aux_percent
            )
            updates["climate"].zone_exhaust_percent = parts.get(
                48, base.climate.zone_exhaust_percent
            )

            zone_intake_open = parts.get(96, -1)
            updates["climate"].zone_intake_open = zone_intake_open not in (-1, 0)

            updates["climate"].zone_top_vent_open = bool(
                updates["climate"].zone_exhaust_percent > 0
                and not updates["climate"].zone_intake_open
            )

        # THERMALS & CTC DECODING
        updates["climate"].bed_temp = float(p.get("bed_temper", base.climate.bed_temp))
        updates["climate"].bed_temp_target = int(
            p.get("bed_target_temper", base.climate.bed_temp_target)
        )

        ctc_temp_target = 0
        if ctc_root:
            ctc_temp_raw = unpackTemperature(ctc_root.get("info", {}).get("temp", 0.0))
            ctc_temp = ctc_temp_raw[0]
            ctc_temp_target = int(ctc_temp_raw[1])
            updates["climate"].chamber_temp = ctc_temp
            updates["climate"].chamber_temp_target = ctc_temp_target
        elif not config.external_chamber:
            chamber_temp = int(p.get("chamber_temper", base.climate.chamber_temp))
            if chamber_temp != 5:
                updates["climate"].chamber_temp = chamber_temp

        if (
            ctc_temp_target == 0
            and updates["climate"].air_conditioning_mode != AirConditioningMode.HEAT_MODE
        ):
            updates["climate"].chamber_temp_target = base.climate.chamber_temp_target

        if p.get("command", "") == "set_ctt" and p.get("result", "") == "success":
            ctc_temp_target = int(p.get("ctt_val", -1))
            updates["climate"].chamber_temp_target = ctc_temp_target
            if ctc_temp_target < 45:
                updates["climate"].air_conditioning_mode = AirConditioningMode.COOL_MODE

        # EXTRUDERS
        new_extruders = []
        if "info" in extruder_root:
            nozzle_by_id: dict[int, dict[str, Any]] = {}
            nozzle_info = nozzle_root.get("info", [])
            for nozzle_item in nozzle_info:
                raw_nozzle_id = nozzle_item.get("id")
                nozzle_id = int(raw_nozzle_id) & 0xFF
                nozzle_by_id[nozzle_id] = nozzle_item

            for new_ext in extruder_root["info"]:
                raw_t = int(new_ext.get("temp", 0))
                act_t, tar_t = unpackTemperature(raw_t)

                sn = int(new_ext.get("snow", -1))
                hn = int(new_ext.get("hnow", -1))

                st = int(new_ext.get("star", -1))
                ht = int(new_ext.get("htar", -1))

                ext = ExtruderState()
                ext.id = int(new_ext.get("id", 0))

                ext.temp = act_t
                ext.temp_target = int(tar_t)

                ext.info_bits = int(new_ext.get("info", 0))
                ext.state = parseExtruderInfo(ext.info_bits)
                ext.status = parseExtruderStatus(int(new_ext.get("stat", 0)))

                nozzle_id_key = int(new_ext.get("hnow", ext.id))
                nozzle_info = nozzle_by_id.get(nozzle_id_key)
                if nozzle_info is None:
                    nozzle_info = nozzle_by_id.get(ext.id)

                ext.nozzle = NozzleCharacteristics.from_telemetry(
                    nozzle_type=(
                        str(nozzle_info.get("type"))
                        if nozzle_info is not None and nozzle_info.get("type") is not None
                        else None
                    ),
                    nozzle_diameter=(
                        nozzle_info.get("diameter")
                        if nozzle_info is not None
                        and nozzle_info.get("diameter") is not None
                        else None
                    ),
                    nozzle_id=(
                        str(nozzle_info.get("id"))
                        if nozzle_info is not None and nozzle_info.get("id") is not None
                        else None
                    ),
                )

                ext.active_tray_id = parseExtruderTrayState(ext.id, hn, sn)
                ext.target_tray_id = parseExtruderTrayState(ext.id, ht, st)

                if base.extruders and len(base.extruders) > ext.id:
                    base_tray_state = base.extruders[ext.id].tray_state
                else:
                    base_tray_state = (
                        TrayState.LOADED
                        if ext.state != ExtruderInfoState.EMPTY
                        else TrayState.UNLOADED
                    )

                if (
                    ext.state == ExtruderInfoState.LOADED
                    and ext.status == ExtruderStatus.ACTIVE
                ):
                    ext.tray_state = TrayState.LOADED
                elif (
                    ext.state == ExtruderInfoState.EMPTY
                    and ext.status == ExtruderStatus.IDLE
                ):
                    ext.tray_state = TrayState.UNLOADED
                elif (
                    ext.state == ExtruderInfoState.LOADED
                    and ext.status == ExtruderStatus.HEATING
                    and base_tray_state not in (TrayState.LOADING, TrayState.UNLOADED)
                ):
                    ext.tray_state = TrayState.UNLOADING
                elif ext.status is not ExtruderStatus.IDLE:
                    ext.tray_state = TrayState.LOADING
                else:
                    ext.tray_state = base.active_tray_state

                new_extruders.append(ext)
        else:
            ext = base.extruders[0] if base.extruders else ExtruderState()
            ext.id = ActiveTool.SINGLE_EXTRUDER
            ext.temp = float(p.get("nozzle_temper", base.active_nozzle_temp))
            ext.temp_target = int(
                p.get("nozzle_target_temper", base.active_nozzle_temp_target)
            )
            ext.state = ExtruderInfoState.NOT_AVAILABLE
            ext.status = ExtruderStatus.NOT_AVAILABLE
            ext.active_tray_id = base.active_tray_id
            ext.target_tray_id = base.target_tray_id
            ext.tray_state = base.active_tray_state
            ext.nozzle = NozzleCharacteristics.from_telemetry(
                nozzle_type=p.get(
                    "nozzle_type",
                    ext.nozzle.telemetry_type_raw,
                ),
                nozzle_diameter=p.get("nozzle_diameter", ext.nozzle.diameter_mm),
                nozzle_id=p.get("nozzle_id", ext.nozzle.encoded_id),
                flow_type=NozzleFlowType.STANDARD,
            )
            new_extruders.append(ext)

        updates["extruders"] = new_extruders if new_extruders else base.extruders

        # TOOL SELECTION
        if "state" in extruder_root:
            raw_t_idx = (int(extruder_root["state"]) >> 4) & 0xF
            if new_caps.has_dual_extruder:
                updates["active_tool"] = ActiveTool(raw_t_idx)
            else:
                updates["active_tool"] = ActiveTool.SINGLE_EXTRUDER
        else:
            updates["active_tool"] = base.active_tool

        # AMS UNITS
        cur_ams = {u.ams_id: u for u in base.ams_units}

        for m in modules:
            if (
                m.get("name", "").startswith("n3f/")
                or m.get("name", "").startswith("n3s/")
                or m.get("name", "").startswith("ams")
            ):
                ams_id = int(m["name"].split("/")[-1])
                u = cur_ams.get(ams_id, AMSUnitState(ams_id=ams_id))
                u.chip_id = m.get("sn", u.chip_id)
                u.model = getAMSModelBySerial(u.chip_id)
                cur_ams[ams_id] = u

        for ams_u in ams_root.get("ams", []):
            id = int(ams_u.get("id", 0))
            u = cur_ams.get(id, AMSUnitState(ams_id=id))
            u.temp_actual = float(ams_u.get("temp", u.temp_actual))
            u.humidity_index = int(float(ams_u.get("humidity", u.humidity_index)))
            u.humidity_raw = int(float(ams_u.get("humidity_raw", u.humidity_raw)))
            u.dry_time = int(float(ams_u.get("dry_time", u.dry_time)))

            # ugly hack for capturing target temp
            if u.dry_time > 0 and u.temp_target < int(u.temp_actual) - 1:
                u.temp_target = int(u.temp_actual)
            elif u.dry_time == 0:
                u.temp_target = 0

            if "info" in ams_u:
                u.ams_info = int(ams_u["info"], 16)
                p_ams = parseAMSInfo(ams_u["info"])

                u.heater_state = p_ams["heater_state"]
                u.dry_fan1_status = p_ams["dry_fan1_status"]
                u.dry_fan2_status = p_ams["dry_fan2_status"]
                u.dry_sub_status = p_ams["dry_sub_status"]

                # Update AMS model from parsed info if not already set
                if u.model == AMSModel.UNKNOWN:
                    u.model = p_ams["ams_type"]

                if new_caps.has_dual_extruder:
                    u.assigned_to_extruder = ActiveTool(p_ams.get("extruder_id", 15))
                    updates["extruders"][
                        u.assigned_to_extruder.value
                    ].assigned_to_ams_id = u.ams_id

                rb = ams_root.get("tray_exist_bits")
                if rb is not None:
                    eb = int(rb, 16) if isinstance(rb, str) else int(rb)

                    # Calculate the bit shift based on the unit ID
                    # Standard AMS: 0, 1, 2, 3 -> shift 0, 4, 8, 12
                    # AMS-HT: 128, 129, 130, 131 -> shift 16, 20, 24, 28
                    if id >= 128:
                        shift = 16 + (4 * (id - 128))
                        # AMS-HT is a 1-slot unit, so we check only range(1)
                        u.tray_exists = [bool((eb >> shift) & (1 << j)) for j in range(1)]
                    else:
                        shift = 4 * id
                        # Standard AMS is a 4-slot unit, so we check range(4)
                        u.tray_exists = [bool((eb >> shift) & (1 << j)) for j in range(4)]

            cur_ams[id] = u

        updates["ams_units"] = list(cur_ams.values())

        # ACTIVE / TARGET TRAYS AND TOOL TEMP
        # if multi-extruder return the active one
        a_ext = next(
            (e for e in updates["extruders"] if e.id == updates["active_tool"].value),
            None,
        )
        if a_ext:
            updates["active_ams_id"] = (
                a_ext.assigned_to_ams_id if a_ext.active_tray_id not in (254, 255) else -1
            )
            updates["active_tray_id"] = a_ext.active_tray_id
            updates["target_tray_id"] = a_ext.target_tray_id

            updates["active_tray_state"] = a_ext.tray_state

            updates["active_nozzle_temp"] = a_ext.temp
            updates["active_nozzle_temp_target"] = a_ext.temp_target
        else:
            # otherwise process a single extruder printer update
            updates["active_nozzle_temp"] = float(
                p.get("nozzle_temper", base.active_nozzle_temp)
            )
            updates["active_nozzle_temp_target"] = int(
                p.get("nozzle_target_temper", base.active_nozzle_temp_target)
            )
            updates["active_tray_id"] = int(ams_root.get("tray_now", base.active_tray_id))
            if updates["active_tray_id"] == 255:
                updates["active_tray_id"] = -1
                updates["active_tray_state"] = TrayState.UNLOADED
            elif aji.stage_id == 24:
                updates["active_tray_state"] = TrayState.LOADING
            elif aji.stage_id == 22:
                updates["active_tray_state"] = TrayState.UNLOADING
            else:
                updates["active_tray_state"] = TrayState.LOADED

            updates["active_ams_id"] = (
                updates["active_tray_id"] >> 2
                if updates["active_tray_id"] not in (254, 255)
                else base.active_ams_id
            )

        if "active_tray_id" in updates:
            updates["is_external_spool_active"] = updates["active_tray_id"] in [254, 255]
        else:
            updates["is_external_spool_active"] = False

        if "active_tray_state" in updates:
            updates["active_tray_state_name"] = updates["active_tray_state"].name

        # GLOBAL METADATA & FANS
        raw_exist = ams_root.get("ams_exist_bits", base.ams_exist_bits)
        updates["ams_exist_bits"] = (
            int(raw_exist, 16) if isinstance(raw_exist, str) else int(raw_exist)
        )
        updates["ams_connected_count"] = bin(updates["ams_exist_bits"]).count("1")
        updates["ams_status_raw"] = int(p.get("ams_status", base.ams_status_raw))
        updates["ams_status_text"] = parseAMSStatus(updates["ams_status_raw"])

        part_cooling_fan_speed_percent = -1

        if not config.capabilities.has_chamber_temp:
            part_cooling_fan_speed_percent = (
                scaleFanSpeed(p.get("cooling_fan_speed"))
                if p.get("cooling_fan_speed", -1) != -1
                else -1
            )
        else:
            part_cooling_fan_speed_percent = updates["climate"].zone_part_fan_percent

        if part_cooling_fan_speed_percent == -1:
            part_cooling_fan_speed_percent = base.climate.part_cooling_fan_speed_percent

        updates["climate"].part_cooling_fan_speed_percent = part_cooling_fan_speed_percent
        updates["climate"].part_cooling_fan_speed_target_percent = updates[
            "climate"
        ].part_cooling_fan_speed_percent

        heatbreak_fan_speed_percent = scaleFanSpeed(p.get("heatbreak_fan_speed", -1))
        if heatbreak_fan_speed_percent == -1:
            heatbreak_fan_speed_percent = base.climate.heatbreak_fan_speed_percent
        updates["climate"].heatbreak_fan_speed_percent = heatbreak_fan_speed_percent

        exhaust_fan_speed_percent = -1
        if not config.capabilities.has_chamber_temp:
            exhaust_fan_speed_percent = scaleFanSpeed(p.get("big_fan2_speed", -1))
        else:
            exhaust_fan_speed_percent = updates["climate"].zone_exhaust_percent

        if exhaust_fan_speed_percent == -1:
            exhaust_fan_speed_percent = base.climate.exhaust_fan_speed_percent
        updates["climate"].exhaust_fan_speed_percent = exhaust_fan_speed_percent

        aux_fan_speed_percent = -1
        if not config.capabilities.has_chamber_temp:
            aux_fan_speed_percent = scaleFanSpeed(p.get("big_fan1_speed", -1))
        else:
            aux_fan_speed_percent = updates["climate"].zone_aux_percent

        if aux_fan_speed_percent == -1:
            aux_fan_speed_percent = base.climate.aux_fan_speed_percent
        updates["climate"].aux_fan_speed_percent = aux_fan_speed_percent

        updates["wifi_signal_strength"] = p.get("wifi_signal", base.wifi_signal_strength)

        # ERROR HANDLING
        updates["print_error"] = int(p.get("print_error", base.print_error))

        if updates["print_error"] != 0:
            decoded_error = decodeError(updates["print_error"])
        else:
            decoded_error = {}
            base.hms_errors = []

        updates["hms_errors"] = decodeHMS(p.get("hms", base.hms_errors))
        if decoded_error and decoded_error not in updates["hms_errors"]:
            updates["hms_errors"].insert(0, decoded_error)

        # capabilities mapped to BambuConfig
        config.capabilities = new_caps

        return replace(base, **updates)
