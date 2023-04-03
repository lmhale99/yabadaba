@property
def mC(self) -> float:
    """millicoulomb"""
    return 1e-3 * self.C

@property
def uC(self) -> float:
    """microcoulomb"""
    return 1e-6 * self.C

@property
def nC(self) -> float:
    """nanocoulomb"""
    return 1e-9 * self.C

@property
def Ah(self) -> float:
    """amp-hour"""
    return 3600. * self.C

@property
def mAh(self) -> float:
    """milliamp-hour"""
    return 1e-3 * self.Ah