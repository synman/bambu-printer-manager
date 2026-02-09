from dataclasses import dataclass


@dataclass
class BambuSpool:
    """
    This value object is used by `BambuPrinter` to enumerate "spools" connected to the printer.
    It is used primarily within `BambuPrinter`'s `_spools` attribute and is returned as part of a
    Tuple when there are spools active on machine.
    """

    id: int
    """Spool id can be `0-23` for AMS spools or `254`-`255` for the External spool(s)."""

    name: str = ""
    """The name of the spool, typically only populated if a Bambu Lab RFID tag is recognized by the AMS."""

    type: str = ""
    """The type of filament in the spool. Will either be read by the RFID tag or set on the Printer display."""

    sub_brands: str = ""
    """For Bambu Lab filaments, specifies the specialization of the filament (Matte, Pro, Tough, etc)."""

    color: str = ""
    """Will either be a color hex code or a color name if `webcolors` is able to recognize the color code."""

    tray_info_idx: str = ""
    """The underlying index for the selected filament in Bambu Studio."""

    k: float = 0.0
    """The K-Factor to use for determining optimial linear advance (flow rate)."""

    bed_temp: int = 0
    """The target bed temperature to use."""

    nozzle_temp_min: int = 0
    """The minimum usable nozzle temperature to use."""

    nozzle_temp_max: int = 0
    """The maximum usable nozzle temperature to use."""

    drying_temp: int = 0
    """The drying temperature for the filament spool."""

    drying_time: int = 0
    """The drying time for the filament spool."""

    remaining_percent: int = 0
    """The estimated remaining filament percentage."""

    state: int = 0
    """The current state of the spool."""

    total_length: int = 0
    """The total length of filament on the spool in millimeters."""

    tray_weight: int = 0
    """The weight of the filament spool in grams."""

    slot_id: int = -1
    """The slot # within the ams or the external tray id for this spool (0 to 23 or 254 to 255)."""

    ams_id: int = -1
    """The AMS id associated with this spool. -1 represents no AMS associated with it."""
