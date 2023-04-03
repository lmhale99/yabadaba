@property
def mol(self) -> float:
    """mole"""
    return self.NA

@property
def mmol(self) -> float:
    """millimole"""
    return 1e-3 * self.mol

@property
def umol(self) -> float:
    """micromole"""
    return 1e-6 * self.mol

@property
def nmol(self) -> float:
    """nanomole"""
    return 1e-9 * self.mol

@property
def pmol(self) -> float:
    """picomole"""
    return 1e-12 * self.mol

@property
def fmol(self) -> float:
    """femtomole"""
    return 1e-15 * self.mol

@property
def M(self) -> float:
    """molar"""
    return self.mol / self.L

@property
def mM(self) -> float:
    """millimolar"""
    return 1e-3 * self.M

@property
def uM(self) -> float:
    """micromolar"""
    return 1e-6 * self.M

@property
def nM(self) -> float:
    """nanomolar"""
    return 1e-9 * self.M

@property
def pM(self) -> float:
    """picomolar"""
    return 1e-12 * self.M

@property
def fM(self) -> float:
    """femtomolar"""
    return 1e-15 * self.M