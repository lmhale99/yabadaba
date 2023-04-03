@property
def L(self) -> float:
    """liter"""
    return 1e-3 * self.m**3

@property
def mL(self) -> float:
    """milliliter"""
    return 1e-3 * self.L

@property
def uL(self) -> float:
    """microliter"""
    return 1e-6 * self.L

@property
def nL(self) -> float:
    """nanoliter"""
    return 1e-9 * self.L

@property
def pL(self) -> float:
    """picoliter"""
    return 1e-12 * self.L

@property
def fL(self) -> float:
    """femtoliter"""
    return 1e-15 * self.L

@property
def aL(self) -> float:
    """attoliter"""
    return 1e-18 * self.L

@property
def kL(self) -> float:
    """kiloliter"""
    return 1e3 * self.L

@property
def ML(self) -> float:
    """megaliter"""
    return 1e6 * self.L

@property
def GL(self) -> float:
    """gigaliter"""
    return 1e9 * self.L