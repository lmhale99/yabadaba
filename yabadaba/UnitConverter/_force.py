@property
def N(self) -> float:
    """newton"""
    return (self.kg * self.m) / self.s**2

@property
def mN(self) -> float:
    """millinewton"""
    return 1e-3 * self.N

@property
def uN(self) -> float:
    """micronewton"""
    return 1e-6 * self.N

@property
def nN(self) -> float:
    """nanonewton"""
    return 1e-9 * self.N

@property
def pN(self) -> float:
    """piconewton"""
    return 1e-12 * self.N

@property
def fN(self) -> float:
    """femtonewton"""
    return 1e-15 * self.N

@property
def kN(self) -> float:
    """kilonewton"""
    return 1e3 * self.N

@property
def MN(self) -> float:
    """meganewton"""
    return 1e6 * self.N

@property
def GN(self) -> float:
    """giganewton"""
    return 1e9 * self.N

@property
def dyn(self) -> float:
    """dyne"""
    return 1e-5 * self.N

@property
def lbf(self) -> float:
    """pound-force (international avoirdupois pound)"""
    return self.lbm * (9.80665 * self.m / self.s**2)