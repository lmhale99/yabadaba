@property
def F(self) -> float:
    """farad"""
    return self.C / self.V

@property
def uF(self) -> float:
    """microfarad"""
    return 1e-6 * self.F

@property
def nF(self) -> float:
    """nanofarad"""
    return 1e-9 * self.F

@property
def pF(self) -> float:
    """picofarad"""
    return 1e-12 * self.F

@property
def fF(self) -> float:
    """femtofarad"""
    return 1e-15 * self.F

@property
def aF(self) -> float:
    """attofarad"""
    return 1e-18 * self.F

@property
def H(self) -> float:
    """henry"""
    return self.m**2 * self.kg / self.C**2

@property
def mH(self) -> float:
    """millihenry"""
    return 1e-3 * self.H

@property
def uH(self) -> float:
    """microhenry"""
    return 1e-6 * self.H

@property
def nH(self) -> float:
    """nanohenry"""
    return 1e-9 * self.H