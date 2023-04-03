@property
def g(self) -> float:
    """gram"""
    return 1e-3 * self.kg

@property
def mg(self) -> float:
    """milligram"""
    return 1e-3 * self.g

@property
def ug(self) -> float:
    """microgram"""
    return 1e-6 * self.g

@property
def ng(self) -> float:
    """nanogram"""
    return 1e-9 * self.g

@property
def pg(self) -> float:
    """picogram"""
    return 1e-12 * self.g

@property
def fg(self) -> float:
    """femtogram"""
    return 1e-15 * self.g

@property
def tonne(self) -> float:
    """tonne"""
    return 1e3 * self.kg

@property
def amu(self) -> float:
    """atomic mass unit"""
    return 1.66053906660e-27 * self.kg

@property
def Da(self) -> float:
    """dalton"""
    return self.amu

@property
def kDa(self) -> float:
    """kilodalton"""
    return 1e3 * self.Da

@property
def lbm(self) -> float:
    """pound mass (international avoirdupois pound)"""
    return 0.45359237 * self.kg