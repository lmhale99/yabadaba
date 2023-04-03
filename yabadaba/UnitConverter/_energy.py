@property
def J(self) -> float:
    """joule"""
    return (self.kg * self.m**2) / self.s**2

@property
def mJ(self) -> float:
    """milligram"""
    return 1e-3 * self.J

@property
def uJ(self) -> float:
    """microgram"""
    return 1e-6 * self.J

@property
def nJ(self) -> float:
    """nanogram"""
    return 1e-9 * self.J

@property
def pJ(self) -> float:
    """picogram"""
    return 1e-12 * self.J

@property
def fJ(self) -> float:
    """femtogram"""
    return 1e-15 * self.J

@property
def kJ(self) -> float:
    """kilojoule"""
    return 1e3 * self.J

@property
def MJ(self) -> float:
    """megajoule"""
    return 1e6 * self.J

@property
def GJ(self) -> float:
    """gigajoule"""
    return 1e9 * self.J

@property
def erg(self) -> float:
    """erg"""
    return 1e-7 * self.J

@property
def eV(self) -> float:
    """electron volt"""
    return 1.602176634e-19 * self.J

@property
def meV(self) -> float:
    """millielectron volt"""
    return 1e-3 * self.eV

@property
def keV(self) -> float:
    """kiloelectron volt"""
    return 1e3 * self.eV

@property
def MeV(self) -> float:
    """megaelectron volt"""
    return 1e6 * self.eV

@property
def GeV(self) -> float:
    """gigaelectron volt"""
    return 1e9 * self.eV

@property
def TeV(self) -> float:
    """teraelectron volt"""
    return 1e12 * self.eV

@property
def btu(self) -> float:
    """British thermal unit"""
    return 1055.06 * self.J

@property
def smallcal(self) -> float:
    """small calorie (a.k.a. gram calorie)"""
    return 4.184 * self.J

@property
def kcal(self) -> float:
    """kilocalorie (a.k.a large Calorie, dietary Calorie)"""
    return 4184. * self.J

@property
def Wh(self) -> float:
    """watt-hour"""
    return 3600. * self.J

@property
def kWh(self) -> float:
    """kilowatt-hour"""
    return 1e3 * self.Wh
