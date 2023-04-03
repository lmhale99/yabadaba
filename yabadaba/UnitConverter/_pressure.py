@property
def Pa(self) -> float:
    """pascal"""
    return self.N / self.m**2

@property
def hPa(self) -> float:
    """hectopascal"""
    return 1e2 * self.Pa

@property
def kPa(self) -> float:
    """kilopascal"""
    return 1e3 * self.Pa

@property
def MPa(self) -> float:
    """megapascal"""
    return 1e6 * self.Pa

@property
def GPa(self) -> float:
    """gigapascal"""
    return 1e9 * self.Pa

@property
def bar(self) -> float:
    """bar"""
    return 1e5 * self.Pa

@property
def mbar(self) -> float:
    """millibar"""
    return 1e-3 * self.bar

@property
def cbar(self) -> float:
    """centibar"""
    return 1e-2 * self.bar

@property
def dbar(self) -> float:
    """decibar"""
    return 0.1 * self.bar

@property
def kbar(self) -> float:
    """kilobar"""
    return 1e3 * self.bar

@property
def Mbar(self) -> float:
    """megabar"""
    return 1e6 * self.bar

@property
def atm(self) -> float:
    """standard atmosphere pressure"""
    return 101325. * self.Pa

@property
def torr(self) -> float:
    """torr"""
    return (1. / 760.) * self.atm

@property
def mtorr(self) -> float:
    """millitorr"""
    return 1e-3 * self.torr

@property
def psi(self) -> float:
    """pounds force per square inch"""
    return self.lbf / self.inch**2