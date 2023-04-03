@property
def A(self) -> float:
    """ampere"""
    return self.C / self.s

@property
def mA(self) -> float:
    """milliampere"""
    return 1e-3 * self.A

@property
def uA(self) -> float:
    """microampere"""
    return 1e-6 * self.A

@property
def nA(self) -> float:
    """nanoampere"""
    return 1e-9 * self.A

@property
def pA(self) -> float:
    """picoampere"""
    return 1e-12 * self.A

@property
def fA(self) -> float:
    """femtoampere"""
    return 1e-15 * self.A