@property 
def W(self) -> float:
    """watt"""
    return self.J / self.s

@property
def mW(self) -> float:
    """milliwatt"""
    return 1e-3 * self.W

@property
def uW(self) -> float:
    """microwatt"""
    return 1e-6 * self.W

@property
def nW(self) -> float:
    """nanowatt"""
    return 1e-9 * self.W

@property
def pW(self) -> float:
    """picowatt"""
    return 1e-12 * self.W

@property
def kW(self) -> float:
    """kilowatt"""
    return 1e3 * self.W

@property
def MW(self) -> float:
    """megawatt"""
    return 1e6 * self.W

@property
def GW(self) -> float:
    """gigawatt"""
    return 1e9 * self.W

@property
def TW(self) -> float:
    """terawatt"""
    return 1e12 * self.W

@property
def horsepower_imperial(self) -> float:
    """imperial horsepower"""
    return 33000 * self.foot * self.lbf / self.minute

@property
def horsepower_metric(self) -> float:
    """metric horsepower"""
    return (75 * self.kg) * (9.80665 * self.m / self.s**2) * (1 * self.m / self.s)