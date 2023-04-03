@property 
def V(self) -> float:
    """volt"""
    return self.J / self.C

@property
def mV(self) -> float:
    """millivolt"""
    return 1e-3 * self.V

@property
def uV(self) -> float:
    """microvolt"""
    return 1e-6 * self.V

@property
def nV(self) -> float:
    """nanovolt"""
    return 1e-9 * self.V

@property
def kV(self) -> float:
    """kilovolt"""
    return 1e3 * self.V

@property
def MV(self) -> float:
    """megavolt"""
    return 1e6 * self.V

@property
def GV(self) -> float:
    """gigavolt"""
    return 1e9 * self.V

@property
def TV(self) -> float:
    """teravolt"""
    return 1e12 * self.V