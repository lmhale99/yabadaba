@property
def ms(self) -> float:
    """millisecond"""
    return 1e-3 * self.s

@property
def us(self) -> float:
    """microsecond"""
    return 1e-6 * self.s

@property
def ns(self) -> float:
    """nanosecond"""
    return 1e-9 * self.s

@property
def ps(self) -> float:
    """picosecond"""
    return 1e-12 * self.s

@property
def fs(self) -> float:
    """femtosecond"""
    return 1e-15 * self.s

@property
def minute(self) -> float:
    """minute"""
    return 60. * self.s

@property
def hour(self) -> float:
    """hour"""
    return 60. * self.minute

@property
def day(self) -> float:
    """solar day"""
    return 24. * self.hour

@property
def week(self) -> float:
    """week"""
    return 7. * self.day

@property
def year(self) -> float:
    """sidereal year"""
    return 365.256363004 * self.day