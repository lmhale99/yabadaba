@property 
def ohm(self) -> float:
    """ohm"""
    return self.V / self.A

@property
def Ω(self) -> float:
    """ohm"""
    return self.ohm

@property
def mohm(self) -> float:
    """milliohm"""
    return 1e-3 * self.ohm

@property
def mΩ(self) -> float:
    """milliohm"""
    return self.mohm

@property
def kohm(self) -> float:
    """kiloohm"""
    return 1e3 * self.ohm

@property
def kΩ(self) -> float:
    """kiloohm"""
    return self.kohm

@property
def Mohm(self) -> float:
    """megaohm"""
    return 1e6 * self.ohm

@property
def MΩ(self) -> float:
    """megaohm"""
    return self.Mohm

@property
def Gohm(self) -> float:
    """gigaohm"""
    return 1e9 * self.ohm

@property
def GΩ(self) -> float:
    """gigaohm"""
    return self.Gohm

@property
def S(self) -> float:
    """siemens"""
    return 1. / self.ohm

@property
def mS(self) -> float:
    """millisiemens"""
    return 1e-3 * self.S

@property
def uS(self) -> float:
    """microsiemens"""
    return 1e-6 * self.S

@property
def nS(self) -> float:
    """nanosiemens"""
    return 1e-9 * self.S