@property 
def degFinterval(self) -> float:
    """temperature difference in degrees Fahrenheit"""
    return (5./9.) * self.K

@property
def degCinterval(self) -> float:
    """temperature difference in degrees Celsius"""
    return self.K

@property
def mK(self) -> float:
    """millikelvin"""
    return 1e-3 * self.K

@property
def uK(self) -> float:
    """microkelvin"""
    return 1e-6 * self.K

@property
def nK(self) -> float:
    """nanokelvin"""
    return 1e-9 * self.K

@property
def pK(self) -> float:
    """picokelvin"""
    return 1e-12 * self.K