@property
def Hz(self) -> float:
    """hertz"""
    return 1. / self.s

@property
def mHz(self) -> float:
    """megahertz"""
    return 1e-3 * self.Hz

@property
def kHz(self) -> float:
    """kilohertz"""
    return 1e3 * self.Hz

@property
def MHz(self) -> float:
    """megahertz"""
    return 1e6 * self.Hz
    
@property
def GHz(self) -> float:
    """gigahertz"""
    return 1e9 * self.Hz

@property
def THz(self) -> float:
    """terahertz"""
    return 1e12 * self.Hz

@property
def PHz(self) -> float:
    """petahertz"""
    return 1e15 * self.Hz

@property
def rtHz(self) -> float:
    """root Hertz"""
    return self.Hz**0.5 

@property
def rpm(self) -> float:
    """revolutions per minute"""
    return 1 / self.minute

############ Angular frequency below ################

@property
def Hz·2π(self) -> float:
    """hertz times 2 pi"""
    return self.Hz * 2 * self.pi

@property
def mHz·2π(self) -> float:
    """millihertz times 2 pi"""
    return self.mHz * 2 * self.pi

@property
def kHz·2π(self) -> float:
    """kilohertz times 2 pi"""
    return self.kHz * 2 * self.pi

@property
def MHz·2π(self) -> float:
    """megahertz times 2 pi"""
    return self.MHz * 2 * self.pi

@property
def GHz·2π(self) -> float:
    """gigahertz times 2 pi"""
    return self.GHz * 2 * self.pi

@property
def THz·2π(self) -> float:
    """terahertz times 2 pi"""
    return self.THz * 2 * self.pi

@property
def PHz·2π(self) -> float:
    """petahertz times 2 pi"""
    return self.PHz * 2 * self.pi

@property
def rpm·2π(self) -> float:
    """revolutions per minute times 2 pi"""
    return self.rpm * 2 * self.pi