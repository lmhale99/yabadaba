import math

@property
def NA(self) -> float:
    """Avogadro's number"""
    return 6.02214076e23

@property
def pi(self) -> float:
    """pi"""
    return math.pi

@property
def π(self) -> float:
    """pi"""
    return math.pi

@property
def c0(self) -> float:
    """speed of light in vacuum"""
    return 299792458. * self.m / self.s

@property
def mu0(self) -> float:
    """magnetic constant, permeability of vacuum"""
    return 1.25663706212e-6 * self.N / self.A**2

@property
def μ0(self) -> float:
    """magnetic constant, permeability of vacuum"""
    return self.mu0

@property
def eps0(self) -> float:
    """electric constant, permittivity of vacuum"""
    return 1. / (self.mu0 * self.c0**2)

@property
def ε0(self) -> float:
    """electric constant, permittivity of vacuum"""
    return self.eps0

@property
def Z0(self) -> float:
    """vacuum impedance, 377 ohms"""
    return self.mu0 * self.c0

@property
def hPlanck(self) -> float:
    """planck constant"""
    return 6.62607015e-34 * self.J * self.s

@property
def hbar(self) -> float:
    """reduced planck constant"""
    return self.hPlanck / (2. * self.pi)

@property
def ħ(self) -> float:
    """reduced planck constant"""
    return self.hbar

@property
def kB(self) -> float:
    """Boltzmann constant"""
    return 1.380649e-23 * self.J / self.K

@property
def GNewton(self) -> float:
    """Gravitational constant"""
    return 6.67430e-11 * self.m**3 / (self.kg * self.s**2)

@property
def sigmaSB(self) -> float:
    """Stefan-Boltzmann constant"""
    return (self.pi**2 / 60.) * self.kB**4 / (self.hbar**3 * self.c0**2)

@property
def σSB(self) -> float:
    """Stefan-Boltzmann constant"""
    return self.sigmaSB

@property
def alphaFS(self) -> float:
    """fine-structure constant"""
    return 7.2973525693e-3

@property
def αFS(self) -> float:
    """fine-structure constant"""
    return self.alphaFS

############# Constants--chemistry, atomic physics, electrons #############

@property
def Rgas(self) -> float:
    """ideal gas constant (see README)"""
    return self.kB

@property
def e(self) -> float:
    """charge of proton"""
    return 1.602176634e-19 * self.C 

@property
def uBohr(self) -> float:
    """Bohr magneton"""
    return 9.2740100783e-24 * self.J / self.T

@property
def uNuc(self) -> float:
    """nuclear magneton"""
    return 5.0507837461e-27 * self.J / self.T

@property
def aBohr(self) -> float:
    """Bohr radius"""
    return 5.29177210903e-11 * self.m

@property
def me(self) -> float:
    """electron mass"""
    return 9.1093837015e-31 * self.kg

@property
def mp(self) -> float:
    """proton mass"""
    return 1.67262192369e-27 * self.kg

@property
def mn(self) -> float:
    """neutron mass"""
    return 1.67492749804e-27 * self.kg

@property
def Rinf(self) -> float:
    """Rydberg constant"""
    return 10973731.568160 / self.m

@property
def Ry(self) -> float:
    """Rydberg energy, approximately 13.6 eV"""
    return 2.1798723611035e-18 * self.J

@property
def Hartree(self) -> float:
    """Hartree energy, approximately 27.2 eV"""
    return 2 * self.Ry

@property
def ARichardson(self) -> float:
    """Richardson constant"""
    return (4. * self.pi * self.e * self.me * self.kB**2) / self.hPlanck**3

@property
def Phi0(self) -> float:
    """magnetic flux quantum"""
    return self.hPlanck / (2 * self.e)

@property
def KJos(self) -> float:
    """Josephson constant"""
    return (2 * self.e) / self.hPlanck

@property
def RKlitz(self) -> float:
    """von Klitzing constant"""
    return self.hPlanck / self.e**2

@property
def debye(self) -> float:
    """debye dipole moment, approximately 0.0208 e nm"""
    return 1e-21 * self.C * self.m**2 / (self.s * self.c0)

############## Constants--astronomical and properties of earth ##############

@property
def REarth(self) -> float:
    """radius of earth"""
    return 6371. * self.km

@property
def g0(self) -> float:
    """standard earth gravitational acceleration"""
    return 9.80665 * self.m / self.s**2

@property
def Msolar(self) -> float:
    """mass of the sun)"""
    return 1.98847e30 * self.kg

@property
def MEarth(self) -> float:
    """mass of earth"""
    return 5.9722e24 * self.kg