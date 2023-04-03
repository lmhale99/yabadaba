@property
def Gal(self) -> float:
    """galileo"""
    return 1. * self.cm / self.s**2

@property
def mGal(self) -> float:
    """milligalileo"""
    return 1e-3 * self.Gal

@property
def uGal(self) -> float:
    """microgalileo"""
    return 1e-6 * self.Gal

@property
def eotvos(self) -> float:
    """eotvos"""
    return 1e-9 / self.s**2