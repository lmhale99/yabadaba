@property
def cm(self) -> float:
    """centimeter"""
    return 1e-2 * self.m

@property
def mm(self) -> float:
    """millimeter"""
    return  1e-3 * self.m
    
@property
def um(self) -> float:
    """micrometer"""
    return 1e-6 * self.m
    
@property
def nm(self) -> float:
    """nanometer"""
    return 1e-9 * self.m
    
@property
def pm(self) -> float:
    """picometer"""
    return 1e-12 * self.m
    
@property
def fm(self) -> float:
    """femtometer"""
    return 1e-15 * self.m
    
@property
def km(self) -> float:
    """kilometer"""
    return 1e3 * self.m
    
@property
def angstrom(self) -> float:
    """angstrom"""
    return 1e-10 * self.m
    
@property
def Å(self) -> float:
    """angstrom"""
    return self.angstrom
    
@property
def lightyear(self) -> float:
    """lightyear"""
    return 9460730472580800. * self.m
    
@property
def astro_unit(self) -> float:
    """astronomical unit"""
    return 149597870700. * self.m 
    
@property
def pc(self) -> float:
    """parsec"""
    return (648000. / self.pi) * self.astro_unit
    
@property
def kpc(self) -> float:
    """kiloparsec"""
    return 1e3 * self.pc
    
@property
def Mpc(self) -> float:
    """megaparsec"""
    return 1e6 * self.pc
    
@property
def Gpc(self) -> float:
    """gigaparsec"""
    return 1e9 * self.pc
    
@property
def inch(self) -> float:
    """inch"""
    return 2.54 * self.cm
    
@property
def foot(self) -> float:
    """foot"""
    return 12. * self.inch
    
@property
def mile(self) -> float:
    """mile"""
    return 5280. * self.foot
    
@property
def thou(self) -> float:
    """thousandth of an inch, mil"""
    return 1e-3 * self.inch