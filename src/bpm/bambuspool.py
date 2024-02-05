class BambuSpool:
    def __repr__(self):
        return str(self)
    def __str__(self):
        return (f"id=[{self.id}] name=[{self.name}] type=[{self.type}] sub brands=[{self.sub_brands}] color=[{self.color}]")
    
    def __init__(self, id, name, type, sub_brands, color):
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