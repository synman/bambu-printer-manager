from typing import Optional

class BambuSpool:
    """
    This value object is used by `BambuPrinter` to enumerate "spools" connected to the printer.
    It is used primarily within `BambuPrinter`'s `_spools` attribute and is returned as part of a 
    Tuple when there are spools active on machine.
    """    
    def __repr__(self):
        return str(self)
    def __str__(self):
        return (f"id=[{self.id}] name=[{self.name}] type=[{self.type}] sub brands=[{self.sub_brands}] color=[{self.color}]")
    
    def __init__(self, id: int, name: str, type: str, sub_brands: str, color: str):
        """
        Sets up all internal storage attributes for `BambuSpool`.

        Parameters
        ----------
        * id : int - Spool id can be `0-3` for AMS spools or `254` for the External spool.
        * name : str - The name of the spool, typically only populated if a Bambu Lab RFID tag is recognized by the AMS.
        * type : str - The type of filament in the spool.  Will either be read by the RFID tag or set on the Printer display.
        * sub_brands : str - For Bambu Lab filaments, specifies the specialization of the filament (Matte, Pro, Tough, etc).
        * color : str - will either be a color hex code or a color name if `webcolors` is able to recognize the color code.
        """
        self.id = id
        self.name = name
        self.type = type
        self.sub_brands = sub_brands
        self.color = color

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