class BambuSpool:
    """
    This value object is used by `BambuPrinter` to enumerate "spools" connected to the printer.
    It is used primarily within `BambuPrinter`'s `_spools` attribute and is returned as part of a
    Tuple when there are spools active on machine.
    """

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"id=[{self.id}] tray_info_idx=[{self.tray_info_idx}] name=[{self.name}] type=[{self.type}] sub brands=[{self.sub_brands}] color=[{self.color}] k=[{self.k}] bed_temp=[{self.bed_temp}] nozzle_temp_min=[{self.nozzle_temp_min}] nozzle_temp_max=[{self.nozzle_temp_max}]"

    def __init__(
        self,
        id: int,
        name: str,
        type: str,
        sub_brands: str,
        color: str,
        tray_info_idx: str,
        k: float,
        bed_temp: int,
        nozzle_temp_min: int,
        nozzle_temp_max: int,
        drying_temp: int = 0,
        drying_time: int = 0,
        remaining_percent: int = 0,
        state: int = 0,
        total_length: int = 0,
        tray_weight: int = 0,
    ):
        """
        Sets up all internal storage attributes for `BambuSpool`.

        Parameters
        ----------
        * id : int - Spool id can be `0-3` for AMS spools or `254` for the External spool.
        * name : str - The name of the spool, typically only populated if a Bambu Lab RFID tag is recognized by the AMS.
        * type : str - The type of filament in the spool.  Will either be read by the RFID tag or set on the Printer display.
        * sub_brands : str - For Bambu Lab filaments, specifies the specialization of the filament (Matte, Pro, Tough, etc).
        * color : str - Will either be a color hex code or a color name if `webcolors` is able to recognize the color code.
        * tray_info_idx : str - The underlying index for the selected filament in Bambu Studio.
        * k : float - The K-Factor to use for determining optimial linear advance (flow rate).
        * bed_temp : int - The target bed temperature to use.
        * nozzle_temp_min : int - The minimum usable nozzle temperature to use.
        * nozzle_temp_max : int - The maximum usable nozzle temperature to use.
        * drying_temp : int - The drying temperature for the filament spool.
        * drying_time : int - The drying time for the filament spool.
        * remaining_percent : int - The estimated remaining filament percentage.
        * state : int - The current state of the spool.
        * total_length : int - The total length of filament on the spool in millimeters.
        * tray_weight : int - The weight of the filament spool in grams.
        """
        self.id = id
        self.name = name
        self.type = type
        self.sub_brands = sub_brands
        self.color = color
        self.tray_info_idx = tray_info_idx
        self.k = k
        self.bed_temp = bed_temp
        self.nozzle_temp_min = nozzle_temp_min
        self.nozzle_temp_max = nozzle_temp_max
        self.drying_temp = drying_temp
        self.drying_time = drying_time
        self.remaining_percent = remaining_percent
        self.state = state
        self.total_length = total_length
        self.tray_weight = tray_weight

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

    @property
    def sub_brands(self):
        return self._sub_brands

    @sub_brands.setter
    def sub_brands(self, value):
        self._sub_brands = value

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value

    @property
    def tray_info_idx(self):
        return self._tray_info_idx

    @tray_info_idx.setter
    def tray_info_idx(self, value):
        self._tray_info_idx = value

    @property
    def k(self):
        return self._k

    @k.setter
    def k(self, value):
        self._k = value

    @property
    def bed_temp(self):
        return self._bed_temp

    @bed_temp.setter
    def bed_temp(self, value):
        self._bed_temp = value

    @property
    def nozzle_temp_min(self):
        return self._nozzle_temp_min

    @nozzle_temp_min.setter
    def nozzle_temp_min(self, value):
        self._nozzle_temp_min = value

    @property
    def nozzle_temp_max(self):
        return self._nozzle_temp_max

    @nozzle_temp_max.setter
    def nozzle_temp_max(self, value):
        self._nozzle_temp_max = value

    @property
    def drying_temp(self):
        return self._drying_temp

    @drying_temp.setter
    def drying_temp(self, value):
        self._drying_temp = value

    @property
    def drying_time(self):
        return self._drying_time

    @drying_time.setter
    def drying_time(self, value):
        self._drying_time = value

    @property
    def remaining_percent(self):
        return self._remaining_percent

    @remaining_percent.setter
    def remaining_percent(self, value):
        self._remaining_percent = value

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = value

    @property
    def total_length(self):
        return self._total_length

    @total_length.setter
    def total_length(self, value):
        self._total_length = value

    @property
    def tray_weight(self):
        return self._tray_weight

    @tray_weight.setter
    def tray_weight(self, value):
        self._tray_weight = value
