"""
`bambuproject` provides a means of accessing the current active print job's
attributes as well as the metadata associated with the underlying `3mf` file
being used to drive the job.
"""

import base64
import json
import logging
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

    pi = ProjectInfo()
    ret = None

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

            pi.id = lmd["id"]
            pi.name = lmd["name"]
            pi.plate_num = plate_num
            pi.md5 = lmd["md5"]
            pi.timestamp = lmd["timestamp"]
            pi.size = lmd["size"]
            pi.metadata = lmd["metadata"]

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

    with ZipFile(localfile) as zf:
        with zf.open("Metadata/slice_info.config") as f:
            slice_info_cfg = ET.fromstring(f.read().decode("utf-8"))

        for num in range(1, 10):
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
                pi.metadata["filament"] = filament_list

                filament_maps = []
                slice_info_metadata = get_nodes_by_plate_id(
                    slice_info_cfg, num, "metadata"
                )
                for slice_meta in slice_info_metadata:
                    if slice_meta.get("key", "") == "filament_maps":
                        filament_maps = slice_meta.get("value", "").split(" ")
                        for f in range(0, len(filament_maps)):
                            filament_maps[f] = "-1"
                        break
                if filament_maps:
                    for filament in pi.metadata["filament"]:
                        filament_maps[filament["id"] - 1] = filament["id"]
                    pi.metadata["ams_mapping"] = filament_maps

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
                pi.plate_num = num
                pi.size = entry["size"]
                pi.timestamp = entry["timestamp"]
                pi.md5 = get_file_md5(localfile)

                md = cache_path / "metadata" / f"{filename}-{num}.json"
                with md.open("w") as f:
                    json.dump(asdict(pi), f, indent=4)

                if pi.plate_num == plate_num:
                    ret = pi

            except KeyError as ke:
                if printer.config.verbose:
                    logger.debug(f"get_project_info - Key Error for [{file}] - [{ke}]")
                continue

    if not local_file:
        localfile.unlink(missing_ok=True)

    logger.debug(f"get_project_info - cached 3mf metadata for [{file}]")

    return ret
