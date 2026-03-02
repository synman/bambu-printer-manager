"""
`bambuproject` provides a means of accessing the current active print job's attributes
as well as the metadata associated with the underlying `3mf` file being used to drive
the job.
"""

import base64
import fnmatch
import json
import logging
import re
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any
from zipfile import ZipFile

from bpm.bambutools import LoggerName, PlateType, get_file_md5

if TYPE_CHECKING:
    from bpm.bambuprinter import BambuPrinter

logger = logging.getLogger(LoggerName)


@dataclass
class ProjectInfo:
    """The details of the associated project (`3mf`)."""

    id: str = ""
    """The unique identifier for this project (`3mf` storage location)."""
    name: str = ""
    """The filename portion of the `3mf` id."""
    size: int = 0
    """The size of this `3mf`."""
    timestamp: int = 0
    """The epoch timestamp of this `3mf`."""
    md5: str = ""
    """The md5 checksum of this `3mf`."""
    plate_num: int = 1
    """The plate number this `3mf` targets."""
    metadata: dict = field(default_factory=dict)
    """The associated metadata of this `3mf`."""
    plates: list[int] = field(default_factory=list)
    """The plate numbers contained within this `3mf`."""


@dataclass
class ActiveJobInfo:
    """The details of the currently active job running on the printer."""

    project_info: ProjectInfo | None = field(default_factory=ProjectInfo)
    """The `3mf` details for the active job."""
    project_file_command: dict = field(default_factory=dict)
    """The project_file command that triggered this job (if one did)"""
    stage_id: int = 0
    """Current Stage numeric ID. """
    stage_name: str = ""
    """Current Stage human name. """
    current_layer: int = 0
    """Layer index."""
    total_layers: int = 0
    """The total number of layers for this job."""
    print_percentage: int = 0
    """Completion %."""
    elapsed_minutes: int = 0
    """The elapsed time in minutes for this (or the last) job"""
    remaining_minutes: int = 0
    """Time remaining in minutes for the current job."""
    monotonic_start_time: float = -1.0
    """The monotonic time stamp of when this job started"""
    subtask_name: str = ""
    """The subtask name for this job."""
    gcode_file: str = ""
    """The underlying gcode filename from this job feeding the printer."""
    print_type: str = ""
    """Indicates whether this is a cloud or local job (should always be local)."""
    plate_num: int = -1
    """The plate number this job is targetting."""
    plate_type: PlateType = PlateType.NONE
    """The plate type associated with the job"""
    project_info_fetch_attempted: bool = False
    """True once a fallback fetch of project_info has been attempted, to prevent repeated FTP calls."""


@staticmethod
def get_3mf_entry_by_name(node: dict | Any, target_name: str):
    if node.get("name") == target_name:
        return node
    if "children" in node and isinstance(node["children"], list):
        for child in node["children"]:
            found_entry = get_3mf_entry_by_name(child, target_name)
            if found_entry is not None:
                return found_entry
    return None


@staticmethod
def get_3mf_entry_by_id(node: dict | Any, target_id: str):
    if node.get("id") == target_id:
        return node
    if "children" in node and isinstance(node["children"], list):
        for child in node["children"]:
            found_entry = get_3mf_entry_by_id(child, target_id)
            if found_entry is not None:
                return found_entry
    return None


@staticmethod
def get_project_info(
    project_file_id: str,
    printer: "BambuPrinter",
    project_file_md5: str | None = None,
    plate_num: int = 1,
    local_file: str = "",
    use_cached_list: bool = False,
) -> ProjectInfo | None:
    """
    Returns a populated `ProjectInfo` class instance if the provided `project_file` can be located
    on the Printer or is already cached locally. `project_file_md5` if provided will dramatically
    speed up the method if the file is already cached (and matched). `plate_num` must be taken
    into account if you need the metadata for anything other than plate #1.
    """

    def get_nodes_by_plate_id(xml_root, plate_id, node_name):
        for plate in xml_root.findall("plate"):
            meta = plate.find("./metadata[@key='index']")
            if meta is not None and meta.get("value") == str(plate_id):
                return plate.findall(node_name)
        return []

    def _split_config_list(value: str) -> list[str]:
        raw = value.strip()
        if not raw:
            return []

        if raw.startswith("[") and raw.endswith("]"):
            raw = raw[1:-1]

        parts = [part.strip().strip('"').strip("'") for part in re.split(r"[;,]", raw)]
        return [part for part in parts if part]

    def _extract_list_from_config(config_text: str, key: str) -> list[str]:
        if not config_text:
            return []

        for line in config_text.splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            if not stripped.startswith(f"{key}"):
                continue
            if "=" not in stripped:
                continue
            _, value = stripped.split("=", 1)
            values = _split_config_list(value)
            if values:
                return values

        xml_match = re.search(rf'key="{re.escape(key)}"\s+value="([^"]*)"', config_text)
        if xml_match:
            return _split_config_list(xml_match.group(1))

        return []

    def _extract_list_from_gcode_header(gcode_text: str, key: str) -> list[str]:
        if not gcode_text:
            return []

        pattern = re.compile(rf"^\s*;\s*{re.escape(key)}\s*=\s*(.*)$", re.IGNORECASE)
        for line in gcode_text.splitlines():
            match = pattern.match(line)
            if match:
                return _split_config_list(match.group(1))

        return []

    def _normalize_hex_color(value: str) -> str:
        color = value.strip().upper()
        if not color:
            return color

        if color.startswith("#"):
            color = color[1:]

        if len(color) == 8:
            color = color[:6]

        if len(color) == 6 and re.fullmatch(r"[0-9A-F]{6}", color):
            return f"#{color}"

        return value.strip()

    def _ensure_ams_mapping(metadata: dict[str, Any]) -> None:
        if "ams_mapping" in metadata and isinstance(metadata["ams_mapping"], list):
            normalized_mapping: list[str] = []
            for item in metadata["ams_mapping"]:
                try:
                    normalized_mapping.append(str(int(item)))
                except (TypeError, ValueError):
                    normalized_mapping.append("-1")
            metadata["ams_mapping"] = normalized_mapping
            return

        filament_list = metadata.get("filament", [])
        map_ids = metadata.get("map", {}).get("filament_ids", [])

        mapping_size = 0
        if isinstance(map_ids, list) and map_ids:
            mapping_size = len(map_ids)
        elif isinstance(filament_list, list) and filament_list:
            max_filament_id = 0
            for filament in filament_list:
                try:
                    max_filament_id = max(max_filament_id, int(filament.get("id", 0)))
                except (TypeError, ValueError):
                    continue
            mapping_size = max_filament_id if max_filament_id > 0 else len(filament_list)

        if mapping_size <= 0:
            metadata["ams_mapping"] = []
            return

        ams_mapping: list[str] = ["-1"] * mapping_size
        if isinstance(filament_list, list):
            for filament in filament_list:
                try:
                    filament_id = int(filament.get("id", 0))
                except (TypeError, ValueError):
                    continue
                map_index = filament_id - 1
                if 0 <= map_index < len(ams_mapping):
                    ams_mapping[map_index] = str(filament_id)

        metadata["ams_mapping"] = ams_mapping

    file = project_file_id

    if not file.startswith("/"):
        file = f"/{file}"

    filename = file.split("/")[-1]
    cache_path = (
        printer.config.bpm_cache_path if printer.config.bpm_cache_path else Path()
    )
    metadata = cache_path / "metadata" / f"{filename}-{plate_num}.json"
    localfile = cache_path / filename

    if local_file:
        localfile = Path(local_file)

    remote_files = None

    if not metadata.exists() and not local_file:
        metapath = cache_path / "metadata"
        matches = list(metapath.glob(f"{filename}-?.json"))
        if matches:
            metadata = matches[0]
            plate_num_match = re.search(
                rf"{re.escape(filename)}-(\d+)\.json", metadata.name
            )
            if plate_num_match:
                plate_num = int(plate_num_match.group(1))
            logger.info(
                f"get_project_info - using fallback metadata file: [{metadata.name}] plate: [{plate_num}]"
            )

    if metadata.exists() and not local_file:
        lmd = None
        rmd = None

        if not project_file_md5:
            remote_files = (
                printer.get_sdcard_3mf_files()
                if not use_cached_list
                else printer.cached_sd_card_3mf_files
            )
            rmd = get_3mf_entry_by_id(remote_files, file)

        with metadata.open("r") as f:
            lmd = json.load(f)

        if (
            lmd
            and "plate_num" in lmd
            and lmd["plate_num"] == plate_num
            and rmd
            and rmd["timestamp"] == lmd["timestamp"]
            and rmd["size"] == lmd["size"]
        ) or (
            project_file_md5
            and "md5" in lmd
            and lmd["md5"] == project_file_md5.upper()
            and "plate_num" in lmd
            and lmd["plate_num"] == plate_num
        ):
            logger.debug(f"get_project_info - using cached 3mf metadata for [{file}]")

            pi = ProjectInfo()

            pi.id = lmd["id"]
            pi.name = lmd["name"]
            pi.plates = lmd.get("plates", [])
            pi.plate_num = plate_num
            pi.md5 = lmd["md5"]
            pi.timestamp = lmd["timestamp"]
            pi.size = lmd["size"]
            pi.metadata = lmd["metadata"]
            _ensure_ams_mapping(pi.metadata)

            return pi

    if not local_file:
        localfile.unlink(missing_ok=True)

    for num in range(1, 10):
        md = cache_path / "metadata" / f"{filename}-{num}.json"
        md.unlink(missing_ok=True)

    if not local_file and printer.sdcard_file_exists(file):
        printer.download_sdcard_file(file, str(localfile))
    elif not local_file:
        raise Exception(f"get_project_info - [{file}] not found in sdcard_3mf_files")

    thumbnail_png = None
    top_view_png = None
    plate_map = None
    slice_info_cfg = None
    project_settings_cfg = ""

    plate_nums = []
    with ZipFile(localfile, "r") as zf:
        all_files = zf.namelist()
        plate_pattern = "Metadata/plate_?.json"
        plate_files = fnmatch.filter(all_files, plate_pattern)
        for plate_file in plate_files:
            num = plate_file.split("/")[-1].split(".")[0].split("_")[-1]
            if num.isnumeric():
                plate_nums.append(int(num))

    if plate_num not in plate_nums:
        num = plate_nums[0] if plate_nums else 1
        logger.debug(
            f"get_project_info - requested plate_num [{plate_num}] not found in 3mf metadata - defaulting to plate_num [{num}]"
        )
        plate_num = num

    with ZipFile(localfile, "r") as zf:
        with zf.open("Metadata/slice_info.config") as f:
            slice_info_cfg = ET.fromstring(f.read().decode("utf-8"))

        try:
            with zf.open("Metadata/project_settings.config") as f:
                project_settings_cfg = f.read().decode("utf-8", errors="ignore")
        except KeyError:
            project_settings_cfg = ""

        ret = None

        for num in plate_nums:
            pi = ProjectInfo()
            try:
                with zf.open(f"Metadata/plate_{num}.json") as f:
                    plate_map = f.read()

                with zf.open(f"Metadata/plate_{num}.png") as f:
                    thumbnail_png = f.read()
                with zf.open(f"Metadata/top_{num}.png") as f:
                    top_view_png = f.read()

                pi.metadata = {}
                pi.metadata["thumbnail"] = (
                    f"data:image/png;base64,{base64.b64encode(thumbnail_png).decode()}"
                )
                pi.metadata["topimg"] = (
                    f"data:image/png;base64,{base64.b64encode(top_view_png).decode()}"
                )

                pi.metadata["map"] = json.loads(plate_map)
                objects = get_nodes_by_plate_id(slice_info_cfg, num, "object")
                idx = 0

                for object in objects:
                    obj_id = object.get("identify_id", None)
                    if obj_id:
                        pi.metadata["map"]["bbox_objects"][idx]["id"] = int(obj_id)
                    else:
                        logger.warning(
                            f"get_project_info - Object at index [{idx}] missing 'identify_id' attribute; skipping id assignment"
                        )
                    idx += 1

                filament_list = []
                filaments = get_nodes_by_plate_id(slice_info_cfg, num, "filament")
                for filament in filaments:
                    id = int(filament.get("id", -1))
                    type = filament.get("type", "")
                    color = filament.get("color", "")
                    filament_list.append({"id": id, "type": type, "color": color})

                if not filament_list:
                    map_ids = pi.metadata["map"].get("filament_ids", [])
                    map_colors = pi.metadata["map"].get("filament_colors", [])

                    ps_types = _extract_list_from_config(
                        project_settings_cfg,
                        "filament_type",
                    )
                    ps_colors = _extract_list_from_config(
                        project_settings_cfg,
                        "filament_colour",
                    )

                    plate_gcode_header = ""
                    try:
                        with zf.open(f"Metadata/plate_{num}.gcode") as f:
                            plate_gcode_header = f.read().decode("utf-8", errors="ignore")
                    except KeyError:
                        plate_gcode_header = ""

                    gcode_types = _extract_list_from_gcode_header(
                        plate_gcode_header,
                        "filament_type",
                    )
                    gcode_colors = _extract_list_from_gcode_header(
                        plate_gcode_header,
                        "filament_colour",
                    )

                    fallback_filament_map: dict[int, dict[str, Any]] = {}

                    for idx, raw_id in enumerate(map_ids):
                        numeric_id = -1
                        if isinstance(raw_id, int):
                            numeric_id = raw_id
                        elif isinstance(raw_id, str) and raw_id.isdigit():
                            numeric_id = int(raw_id)

                        filament_id = numeric_id if numeric_id > 0 else idx + 1

                        filament_type = ""
                        if 0 <= numeric_id < len(ps_types):
                            filament_type = ps_types[numeric_id]
                        elif idx < len(ps_types):
                            filament_type = ps_types[idx]
                        elif 0 <= numeric_id < len(gcode_types):
                            filament_type = gcode_types[numeric_id]
                        elif idx < len(gcode_types):
                            filament_type = gcode_types[idx]

                        color = ""
                        if idx < len(map_colors):
                            color = map_colors[idx]
                        if not color and 0 <= numeric_id < len(ps_colors):
                            color = ps_colors[numeric_id]
                        if not color and idx < len(ps_colors):
                            color = ps_colors[idx]
                        if not color and 0 <= numeric_id < len(gcode_colors):
                            color = gcode_colors[numeric_id]
                        if not color and idx < len(gcode_colors):
                            color = gcode_colors[idx]

                        fallback_filament_map[filament_id] = {
                            "id": filament_id,
                            "type": filament_type,
                            "color": _normalize_hex_color(color),
                        }

                    if not fallback_filament_map and ps_types:
                        for idx, filament_type in enumerate(ps_types):
                            color = ""
                            if idx < len(ps_colors):
                                color = ps_colors[idx]
                            elif idx < len(gcode_colors):
                                color = gcode_colors[idx]

                            fallback_filament_map[idx + 1] = {
                                "id": idx + 1,
                                "type": filament_type,
                                "color": _normalize_hex_color(color),
                            }

                    filament_list = [
                        fallback_filament_map[key]
                        for key in sorted(fallback_filament_map.keys())
                    ]

                pi.metadata["filament"] = filament_list

                filament_maps = []
                slice_info_metadata = get_nodes_by_plate_id(
                    slice_info_cfg, num, "metadata"
                )
                for slice_meta in slice_info_metadata:
                    if slice_meta.get("key", "") == "filament_maps":
                        # Extract ams_mapping from 3mf metadata (generated by BambuStudio/OrcaSlicer)
                        # Values are absolute tray IDs per DevMapping.cpp encoding:
                        # - 0-103: 4-slot units (formula: ams_id * 4 + slot_id)
                        # - 128-135: 1-slot units (N3S/AMS HT)
                        # - -1: unmapped filament
                        filament_maps = slice_meta.get("value", "").split(" ")
                        for f in range(0, len(filament_maps)):
                            filament_maps[f] = "-1"
                        break
                if filament_maps:
                    for filament in pi.metadata["filament"]:
                        map_index = filament["id"] - 1
                        if 0 <= map_index < len(filament_maps):
                            filament_maps[map_index] = str(filament["id"])
                    pi.metadata["ams_mapping"] = filament_maps

                _ensure_ams_mapping(pi.metadata)

                if not remote_files:
                    remote_files = (
                        printer.get_sdcard_3mf_files()
                        if not use_cached_list
                        else printer.cached_sd_card_3mf_files
                    )
                entry = get_3mf_entry_by_id(remote_files, file)
                if entry is None:
                    raise Exception(
                        f"get_project_info - Entry for file [{file}] not found in sdcard_3mf_files"
                    )

                pi.id = entry["id"]
                pi.name = entry["name"]
                pi.plates = plate_nums
                pi.plate_num = num
                pi.size = entry["size"]
                pi.timestamp = entry["timestamp"]
                pi.md5 = get_file_md5(localfile)

                md = cache_path / "metadata" / f"{filename}-{num}.json"
                with md.open("w") as f:
                    logger.debug(
                        f"get_project_info - caching 3mf metadata for [{file}] plate [{num}]"
                    )
                    json.dump(asdict(pi), f, indent=4)

                if pi.plate_num == plate_num:
                    logger.debug(
                        f"get_project_info - set return value for [{pi.id}] plate [{pi.plate_num}]"
                    )
                    ret = pi

            except KeyError as ke:
                if printer.config.verbose:
                    logger.debug(
                        f"get_project_info - Key Error for [{file}] plate [{num}] - [{ke}]"
                    )
                continue

    if not local_file:
        localfile.unlink(missing_ok=True)

    return ret
