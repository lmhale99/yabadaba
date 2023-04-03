@property 
def T(self) -> float:
    """tesla"""
    return (self.V * self.s) / self.m**2

@property
def mT(self) -> float:
    """millitesla"""
    return 1e-3 * self.T

@property
def uT(self) -> float:
    """microtesla"""
    return 1e-6 * self.T

@property
def nT(self) -> float:
    """nanotesla"""
    return 1e-9 * self.T

@property
def G(self) -> float:
    """gauss"""
    return 1e-4 * self.T

@property
def mG(self) -> float:
    """milligauss"""
    return 1e-3 * self.G

@property
def uG(self) -> float:
    """microgauss"""
    return 1e-6 * self.G

@property
def kG(self) -> float:
    """kilogauss"""
    return 1e3 * self.G

@property
def Oe(self) -> float:
    """oersted"""
    return (1000. / (4. * self.pi)) * self.A / self.m

@property
def Wb(self) -> float:
    """weber"""
    return self.J / self.A