import math
import numpy as np
import scipy.integrate
from collections import OrderedDict
import sys
# Use the sys.path.insert(1,'path/to/TdAlps') to include the package TdAlps to then import it
import aux
#sys.path.insert(1,aux.TDALPS_PATH)
import TdAlps

# This dictionary contains the values for the physical constants we need
sm={
    'sw': math.sqrt(0.23121), # sin(theta_weak)
    'hbar': 6.582119569*10**(-25), # h/2pi in GeVs
    'c': 29979245800, # speed of light in cm/s
    'me': 0.0005109989461, # eletron mass in GeV
    'mmu': 0.1056583745, # muon mass in GeV
    'mtau': 1.77686, # tauon mass in GeV
    'mu': 0.00216, # up quark mass in GeV
    'md': 0.00467, # down quark mass in GeV
    'ms': 0.093, # strange quark mass in GeV
    'mc': 1.27, #charm quark mass in GeV
    'mb': 4.18, # bottom quark mass in GeV
    'mt': 163.6, # top quark mass in GeV
    'mZ': 91.1876, # Z boson mass in GeV
    'mB+': 5.27934, # charged B meson mass in GeV
    'mK+': 0.493677, # charged kaon mass in GeV
    'mpi+': 0.13957039, # charged pion mass in GeV
    'mpi0': 0.1349768, # neutral pion mass in GeV
    'fpi': 0.130, # pion decay constant
    'tauB+': 1.638*10**(-12), # charged B meson lifetime in s
    'GF': 1.166*10**(-5), # Fermi constant
    'alpha': 1/137, # electromagnetic coupling 
    'Vtb': 0.999, # absolute value of CKM element tb
    'Vts': 0.0404, # absolute value of CKM element ts
    'Xt': 1.462, # effective B->Knunu vertex coupling from [1409.4557]
    'BrBtoKnunu+': 4.5*10**(-6), # Branching ratio of B->K nu nu decay
    'NBBBaBar': 471*10**6, # number of BB pairs produced at BaBar
    'NBBBelleII': 5*10**10, # number of BB pairs produced at Belle II
    'mp': 0.9383, # proton mass in GeV
    'mn': 0.9396 # neutron mass in GeV
}

def fz(t):
    """auxiliary function for calculating form factors"""
    tplus = (sm['mB+']+sm['mK+'])**2
    tminus = (sm['mB+']-sm['mK+'])**2
    tzero = tplus * (1-math.sqrt(1-tminus/tplus))
    return (math.sqrt(tplus-t) - math.sqrt(tplus-tzero))/(math.sqrt(tplus-t) + math.sqrt(tplus-tzero))

def formFactorFplusBplus(qsqr):
    """the f_+ form factor of the B+->K+ decay
    
    qsqr - the momentum transfer in the transition
    using parameters from hep-ph:[1811.00983]"""
    tmp = 0.329
    tmp += -0.876 * (fz(qsqr) - fz(0))
    tmp += 0.006 * (fz(qsqr) - fz(0))**2
    tmp = tmp/(1-qsqr/5.325**2)
    return tmp

def formFactorFzeroBplus(qsqr):
    """the f_0 form factor of the B+->K+ decay
    
    qsqr - the momentum transfer in the transition
    using parameters from hep-ph:[1811.00983]"""
    tmp = 0.329
    tmp += 0.195 * (fz(qsqr) - fz(0))
    tmp += -0.446 * (fz(qsqr) - fz(0))**2
    tmp = tmp/(1-qsqr/5.54**2)
    return tmp

def dGammadqsqrBtoKnunu(qsqr, alphaEM):
    """the partial decay rate of the decay B+->K+ nunu

    at a specific momentum transfer qsqr and 
    value of the electromagnetic coupling alphaEM
    following [1409.4557]"""
    return (sm['GF']**2 * (math.sqrt(sm['mB+']**4+sm['mK+']**4+qsqr**2-2*(sm['mB+']**2 * sm['mK+']**2 + sm['mK+']**2 * qsqr + qsqr * sm['mB+']**2)))**3 * abs(sm['Vtb'])**2 * abs(sm['Vts'])**2 * alphaEM**2 * sm['Xt']**2 * abs(formFactorFplusBplus(qsqr))**2)/(256 * sm['mB+']**3 * math.pi**5 * sm['sw']**4)

def GammaBtoKnunu(alphaEM):
    """the partial decay rate of the decay B+->K+ nunu

    for the value of the electromagnetic coupling alphaEM"""
    return scipy.integrate.quad(dGammadqsqrBtoKnunu,0,(sm['mB+']-sm['mK+'])**2,args=(alphaEM))[0]

def BrBtoKnunu(sB,alphaEM):
    """the branching ratio of the process B+->K+ nunu

    in a specific [0.x, 0.x+1] bin around sB = qsqr/mB**2,
    the transfered momentum normalised by the B meson mass squared
    for the value of the electromagnetic coupling alphaEM
    useful for reinterpreting hep-ex:[1303.7465]"""
    qsqrmin = math.floor(10*(sB-0.00001))*0.1*sm['mB+']**2
    qsqrmax = min(math.ceil(10*(sB-0.00001))*0.1*sm['mB+']**2,(sm['mB+']-sm['mK+'])**2)
    return sm['BrBtoKnunu+'] * scipy.integrate.quad(dGammadqsqrBtoKnunu,qsqrmin,qsqrmax,args=(alphaEM))[0]/GammaBtoKnunu(alphaEM)

def B2(tau):
    """the loop function B2(tau)"""
    return 1-(tau-1)*funcB(tau)**2

def B1(tau):
    """the loop function B1(tau)"""
    return 1-tau*funcB(tau)**2

def funcB(tau):
    """an auxiliary function for the loop functions"""
    if tau>=1:
        return math.asin(1/math.sqrt(tau))
    else:
        return math.pi/2 + 1j/2 * math.log((1+math.sqrt(1-tau))/(1-math.sqrt(1-tau)))
    
def Gammaatoll(ma, cll, ml, Lambda):
    """decay rate of an ALP to a pair of leptons
    
    ma - ALP mass
    cll - coupling of ALP to leptons
    ml - mass of leptons
    Lambda - cutoff scale of the ALP-EFT
    following hep-ph: [2012.12272]"""
    if ma <= 2 * ml:
        return 0
    gamma = ml**2 * abs(cll)**2 * math.sqrt(ma**2 - 4 * ml**2) * 2 * math.pi / (Lambda**2) 
    if gamma.imag  != 0:
        if gamma.imag/gamma.real > 10**-10:
            print("The Decay rate to leptons with mass " + str(ml) + " is complex: " + str(gamma))
    return float(gamma)

def Gammaatoqq(ma, cqq, mq, Lambda):
    """decay rate of an ALP to a pair of quarks
    
    ma - ALP mass
    cqq - coupling of ALP to quarks
    mq - mass of leptons
    Lambda - cutoff scale of the ALP-EFT
    following hep-ph: [2012.12272]"""
    if ma <= 2 * mq:
        return 0
    gamma = 3 * mq**2 * abs(cqq)**2 * math.sqrt(ma**2 - 4 * mq**2) * 2 * math.pi / (Lambda**2) 
    if gamma.imag  != 0:
        if gamma.imag/gamma.real > 10**-10:
            print("The Decay rate to quarks with mass " + str(mq) + " is complex: " + str(gamma))
    return float(gamma)

def Gammaatogamgam(ma, coeffs, Lambda):
    """decay rate of an ALP to a pair of photons
    
    ma - ALP mass
    coeffs - Ordered dictionary of couplings from the TdAlps package
    Lambda - cutoff scale of the ALP-EFT
    following hep-ph: [2012.12272]"""
    cgamgam = readCgg(coeffs)
    alphaEM = readAlphaEM(coeffs)
    effcgg = cgamgam
    if ma >= sm['mZ']:
        effcgg += 2 * alphaEM/math.pi * coeffs['WW']/sm['sw']**2 * B2(4*sm['mW']**2/ma**2)
        effcgg += 3 * (2/3)**2 * readCtt(coeffs) * B1(4*sm['mt']**2/ma**2)
    if ma >= sm['mc']:
        effcgg += 3 * (2/3)**2 * readCcc(coeffs) * B1(4*sm['mc']**2/ma**2) 
    if ma >= sm['mb']:
        effcgg += 3 * (-1/3)**2 * readCbb(coeffs) * B1(4*sm['mb']**2/ma**2)
    if ma >= 1:
        effcgg += 3 * (2/3)**2 * readCuu(coeffs) * B1(4*sm['mu']**2/ma**2)
        effcgg += 3 * (-1/3)**2 * readCdd(coeffs) * B1(4*sm['md']**2/ma**2)
        effcgg += 3 * (-1/3)**2 * readCss(coeffs) * B1(4*sm['ms']**2/ma**2)
    if ma >= sm['me']:
        effcgg += readCee(coeffs) * B1(4*sm['me']**2/ma**2)
    if ma >= sm['mmu']:
        effcgg += readCmumu(coeffs) * B1(4*sm['mmu']**2/ma**2)
    if ma >= sm['mtau']:
        effcgg += readCtautau(coeffs) * B1(4*sm['mtau']**2/ma**2)
    if ma <= 1:
        tmp = -(5/3 + sm['mpi+']**2/(sm['mpi+']**2-ma**2) * (sm['md']-sm['mu'])/(sm['md']+sm['mu']))*readCGG(coeffs)
        tmp += -ma**2/(sm['mpi+']**2-ma**2) * (readCuu(coeffs) - readCdd(coeffs))/2
        effcgg += tmp
    gamma = abs(effcgg)**2 * alphaEM**2 * ma**3 /(4 * math.pi * Lambda**2) 
    if gamma.imag  != 0:
        if gamma.imag/gamma.real > 10**-10:
            print("The Decay rate to photons is complex: " + str(gamma))
    return float(gamma)
    
def Gammaatohad(ma, coeffs, Lambda):
    """decay rate of an ALP to hadrons
    
    ma - ALP mass
    coeffs - Ordered dictionary of couplings from the TdAlps package
    Lambda - cutoff scale of the ALP-EFT
    following hep-ph: [2012.12272]"""
    if ma <= 1:
        return 0
    alphaS = readAlphaS(coeffs)
    cGGeff = readCGG(coeffs)
    cGGeff += 1/2 * readCuu(coeffs) * B1(4*sm['mu']**2/ma**2)
    cGGeff += 1/2 * readCdd(coeffs) * B1(4*sm['md']**2/ma**2)
    cGGeff += 1/2 * readCss(coeffs) * B1(4*sm['ms']**2/ma**2)
    nQ = 3
    try:
        cGGeff += 1/2 * readCcc(coeffs) * B1(4*sm['mc']**2/ma**2)
        nQ += 1
        cGGeff += 1/2 * readCbb(coeffs) * B1(4*sm['mb']**2/ma**2)
        nQ += 1
        cGGeff += 1/2 * readCtt(coeffs) * B1(4*sm['mt']**2/ma**2)
        nQ += 1
    except:
        pass
    gamma = abs(cGGeff)**2 * alphaS**2 * ma**3 * (1 + (95/4-7*nQ/6) * alphaS/math.pi) * 2/(math.pi * Lambda**2)# *(16*math.pi**2)
    gamma += Gammaatoqq(ma, readCuu(coeffs), sm['mu'], Lambda)
    gamma += Gammaatoqq(ma, readCdd(coeffs), sm['md'], Lambda)
    gamma += Gammaatoqq(ma, readCss(coeffs), sm['ms'], Lambda)
    if gamma.imag  != 0:
        if gamma.imag/gamma.real > 10**-10:
            print("The Decay rate to hadrons is complex: " + str(gamma))
    return float(gamma)

def Gammaato3pi000(ma, coeffs, Lambda):
    """decay rate of an ALP to three neutral pions
    
    ma - ALP mass
    coeffs - Ordered dictionary of couplings from the TdAlps package
    Lambda - cutoff scale of the ALP-EFT
    following hep-ph: [2012.12272]"""
    if ma<3*sm['mpi0']:
        return 0
    if ma>2:
        return 0
    gamma  = ma * sm['mpi+']**4/(6144*math.pi**3*sm['fpi']**2*(4*math.pi*Lambda)**2)
    gamma *= (readCuu(coeffs)-readCdd(coeffs)+ 2 * readCGG(coeffs) * (sm['md']-sm['mu'])/(sm['md']+sm['mu']))**2
    gamma *= g00(sm['mpi+']**2/ma**2)
    if gamma.imag  != 0:
        if gamma.imag/gamma.real > 10**-10:
            print("The Decay rate to hadrons is complex: " + str(gamma))
    return float(gamma)

def Gammaato3pi0pm(ma, coeffs, Lambda):
    """decay rate of an ALP to three pions: one neutral, two charged
    
    ma - ALP mass
    coeffs - Ordered dictionary of couplings from the TdAlps package
    Lambda - cutoff scale of the ALP-EFT
    following hep-ph: [2012.12272]"""
    if ma < sm['mpi0']+2*sm['mpi+']:
        return 0
    if ma>2:
        return 0
    gamma  = ma * sm['mpi+']**4/(384*math.pi*sm['fpi']**2*Lambda**2)
    gamma *= (readCuu(coeffs)-readCdd(coeffs)+ 2 * readCGG(coeffs) * (sm['md']-sm['mu'])/(sm['md']+sm['mu']))**2
    gamma *= gpm(sm['mpi+']**2/ma**2)
    if gamma.imag  != 0:
        if gamma.imag/gamma.real > 10**-10:
            print("The Decay rate to hadrons is complex: " + str(gamma))
    return float(gamma)
    
def g00(r):
    """Auxiliary function used in the decay rate of ALP->3pi0

    following hep-ph: [2012.12272]"""
    if ((r<0) or (r>1/9)):
        return 0
    integrand = lambda z: math.sqrt(1-4*r/z) * math.sqrt(1+z**2+r**2-2*r-2*z-2*z*r)
    lim_0 = 4*r
    lim_1 = (1-math.sqrt(r))**2
    integral = scipy.integrate.quad(integrand,lim_0,lim_1)
    factor = 2/(1-r)**2
    return factor*integral[0]
    
def gpm(r):
    """Auxiliary function used in the decay rate of ALP->pi0pi+pi-

    following hep-ph: [2012.12272]"""
    if ((r<0) or (r>1/9)):
        return 0
    integrand = lambda z: math.sqrt(1-4*r/z) * math.sqrt(1+z**2+r**2-2*r-2*z-2*z*r) * (z-r)**2
    lim_0 = 4*r
    lim_1 = (1-math.sqrt(r))**2
    integral = scipy.integrate.quad(integrand,lim_0,lim_1)
    factor = 12/(1-r)**2
    return factor*integral[0] 

def BrBtoKaplus(ma, cbs, Lambda):
    """Branching ratio of the decay B+ -> K+ a (ALP)
    
    ma - ALP mass
    cbs - coupling of the ALP to the FCNC b->s
    Lambda - cutoff scale of the ALP-EFT
    using the Lagrangian of hep-ph: [2012.12272]"""
    return abs(cbs)**2 * math.pi/(4 * Lambda**2) * abs(formFactorFzeroBplus(ma**2))**2 * (sm['mB+']**2-sm['mK+']**2)**2/sm['mB+']**3 * math.sqrt(sm['mB+']**4+sm['mK+']**4+ma**4-2*(sm['mB+']**2 * sm['mK+']**2 + sm['mK+']**2 * ma**2 + ma**2 * sm['mB+']**2))/sm['hbar']*sm['tauB+']

def Gammaa(ma, ctL, ctR, Lambda):
    """Decay rate of the ALP as induced only by top couplings
    
    ma - ALP mass
    ctL - coupling of the lefthanded top-quark to the ALP in the UV
    ctR - coupling of the righthanded top-quark to the ALP in the UV
    Lambda - cutoff scale of the ALP-EFT
    following hep-ph: [2012.12272]"""
    lscs = getLSfromctt(ctL,ctR, Lambda, ma)
    GammaTot = 0
    if ma>2*sm['me']:
        GammaTot += Gammaatoll(ma,readCee(lscs),sm['me'],Lambda)
    if ma>2*sm['mmu']:
        GammaTot += Gammaatoll(ma,readCmumu(lscs),sm['mmu'],Lambda)
    if ma>2*sm['mtau']:
        GammaTot += Gammaatoll(ma,readCtautau(lscs),sm['mtau'],Lambda)
    if ma>2*sm['mc']:
        GammaTot += Gammaatoqq(ma,readCcc(lscs),sm['mc'],Lambda)
    if ma>2*sm['mb']:
        GammaTot += Gammaatoqq(ma,readCbb(lscs),sm['mb'],Lambda)
    if ma>1:
        GammaTot += Gammaatohad(ma,lscs,Lambda)
    if ma<2:
        GammaTot += Gammaato3pi0pm(ma,lscs,Lambda)
        GammaTot += Gammaato3pi000(ma,lscs,Lambda)
    GammaTot += Gammaatogamgam(ma,lscs,Lambda)
    if GammaTot.imag  != 0:
        print("The Decay rate to hadrons is complex: " + str(GammaTot))
    return float(GammaTot)

def ctaua(ma, ctL, ctR, Lambda):
    """Lifetime of the ALP as induced only by top couplings
    
    ma - ALP mass
    ctL - coupling of the lefthanded top-quark to the ALP in the UV
    ctR - coupling of the righthanded top-quark to the ALP in the UV
    Lambda - cutoff scale of the ALP-EFT
    following hep-ph: [2012.12272]"""
    gamma = Gammaa(ma,ctL,ctR,Lambda)
    if gamma == 0:
        print("The decay width of a with ma=" + str(ma) + "GeV and cff=" + str(cff) + ", cWW="+ str(cww)+ ", cBB=" + str(cbb) + " is zero.")
        return 0
    return sm['c']*sm['hbar']/gamma

def ctauamumu(ma, ctL, ctR, Lambda):
    """Lifetime of the ALP as induced only by top couplings
    
    ma - ALP mass
    ctL - coupling of the lefthanded top-quark to the ALP in the UV
    ctR - coupling of the righthanded top-quark to the ALP in the UV
    Lambda - cutoff scale of the ALP-EFT
    following hep-ph: [2012.12272]"""
    # gamma = Gammaa(ma,ctL,ctR,Lambda)
    lscs = getLSfromctt(ctL,ctR, Lambda, ma)
    gamma= float(Gammaatoll(ma,readCmumu(lscs),sm['mmu'],Lambda))
    if gamma == 0:
        print("The decay width of a with ma=" + str(ma) + "GeV and cff=" + str(cff) + ", cWW="+ str(cww)+ ", cBB=" + str(cbb) + " is zero.")
        return 0
    return sm['c']*sm['hbar']/gamma

def getLSfromctt(ctL,ctR, Lambda, mu):
    """Returns low-energy coefficient dictionary from UV ALP-top couplings
    
    Interface function to the TdAlps package
    ctL - coupling of the lefthanded top-quark to the ALP in the UV
    ctR - coupling of the righthanded top-quark to the ALP in the UV
    Lambda - cutoff scale of the ALP-EFT where ctL and ctR are defines
    mu - low-energy scale to which the couplings are run
    the running is based on hep-ph: [2012.12272]"""
    with aux.HiddenPrints():
        HC = OrderedDict()
        HC['Q'] = np.array([[0,0,0],[0,0,0],[0,0,-ctL]])
        HC['u'] = np.array([[0,0,0],[0,0,0],[0,0,ctR]])
        HC['d'] = np.array([[0,0,0],[0,0,0],[0,0,0]])
        HC['L'] = np.array([[0,0,0],[0,0,0],[0,0,0]])
        HC['e'] = np.array([[0,0,0],[0,0,0],[0,0,0]])
        HC['GG'] = 0
        HC['WW'] = 0
        HC['BB'] = 0
        if mu<1:
            mu=1
    return TdAlps.RunRotateMatchRun(HC, Lambda, mu, 3)

def readCuu(coeffs):
    """Reads out the ALP-up quark coupling value from TdAlps-based coupling dictionary coeffs"""
    if 'U' in coeffs:
        if np.array(coeffs['U']).ndim>1:
            return -coeffs['U'][0][0]+coeffs['u'][0][0]
        return -coeffs['U']+coeffs['u']
    elif 'Q' in coeffs:
        if np.array(coeffs['Q']).ndim>1:
            return -coeffs['Q'][0][0]+coeffs['u'][0][0]
        return -coeffs['Q']+coeffs['u']
    else:
        return 0
        
def readCdd(coeffs):
    """Reads out the ALP-down quark coupling value from TdAlps-based coupling dictionary coeffs"""
    if 'D' in coeffs:
        if np.array(coeffs['D']).ndim>1:
            return -coeffs['D'][0][0]+coeffs['d'][0][0]
        return -coeffs['D']+coeffs['d']
    elif 'Q' in coeffs:
        if np.array(coeffs['Q']).ndim>1:
            return -coeffs['Q'][0][0]+coeffs['d'][0][0]
        return -coeffs['Q']+coeffs['d']
    else:
        return 0
        
def readCcc(coeffs):
    """Reads out the ALP-charm quark coupling value from TdAlps-based coupling dictionary coeffs"""
    if 'U' in coeffs:
        if np.array(coeffs['U']).ndim>1 and len(coeffs['U'][0])>1:
            return -coeffs['U'][1][1]+coeffs['u'][1][1]
    elif 'Q' in coeffs:
        if np.array(coeffs['Q']).ndim>1 and len(coeffs['Q'][0])>1:
            return -coeffs['Q'][1][1]+coeffs['u'][1][1]
    return 0
        
def readCss(coeffs):
    """Reads out the ALP-strange quark coupling value from TdAlps-based coupling dictionary coeffs"""
    if 'D' in coeffs:
        if np.array(coeffs['D']).ndim>1 and len(coeffs['D'][0])>1:
            return -coeffs['D'][1][1]+coeffs['d'][1][1]
    elif 'Q' in coeffs:
        if np.array(coeffs['Q']).ndim>1 and len(coeffs['Q'][0])>1:
            return -coeffs['Q'][1][1]+coeffs['d'][1][1]
    return 0
            
def readCtt(coeffs):
    """Reads out the ALP-top quark coupling value from TdAlps-based coupling dictionary coeffs"""
    if 'U' in coeffs:
        if np.array(coeffs['U']).ndim>1 and len(coeffs['U'][0])>2:
            return -coeffs['U'][2][2]+coeffs['u'][2][2]
    elif 'Q' in coeffs:
        if np.array(coeffs['Q']).ndim>1 and len(coeffs['Q'][0])>2:
            return -coeffs['Q'][2][2]+coeffs['u'][2][2]
    return 0
            
def readCbb(coeffs):
    """Reads out the ALP-bottom quark coupling value from TdAlps-based coupling dictionary coeffs"""
    if 'D' in coeffs:
        if np.array(coeffs['D']).ndim>1 and len(coeffs['D'][0])>2:
            return -coeffs['D'][2][2]+coeffs['d'][2][2]
    elif 'Q' in coeffs:
        if np.array(coeffs['Q']).ndim>1 and len(coeffs['Q'][0])>2:
            return -coeffs['Q'][2][2]+coeffs['d'][2][2]
    return 0

def readCGG(coeffs):
    """Reads out the ALP-gluon coupling value from TdAlps-based coupling dictionary coeffs"""
    return coeffs['GG']

def readCgg(coeffs):
    """Reads out the ALP-photon coupling value from TdAlps-based coupling dictionary coeffs"""
    if 'gamgam' in coeffs:
        return coeffs['gamgam']
    return 0

def readCee(coeffs):
    """Reads out the ALP-electron coupling value from TdAlps-based coupling dictionary coeffs"""
    if 'E' in coeffs:
        if np.array(coeffs['E']).ndim>1:
            return -coeffs['E'][0][0]+coeffs['e'][0][0]
        return -coeffs['E']+coeffs['e']
    elif 'Q' in coeffs:
        if np.array(coeffs['L']).ndim>1:
            return -coeffs['L'][0][0]+coeffs['e'][0][0]
        return -coeffs['L']+coeffs['e']
    return 0

def readCmumu(coeffs):
    """Reads out the ALP-muon coupling value from TdAlps-based coupling dictionary coeffs"""
    if 'E' in coeffs:
        if np.array(coeffs['E']).ndim>1 and len(coeffs['E'][0])>1:
            return -coeffs['E'][1][1]+coeffs['e'][1][1]
        return -coeffs['E']+coeffs['e']
    elif 'L' in coeffs:
        if np.array(coeffs['L']).ndim>1 and len(coeffs['L'][0])>1:
            return -coeffs['L'][1][1]+coeffs['e'][1][1]
        return -coeffs['L']+coeffs['e']
    return 0

def readCtautau(coeffs):
    """Reads out the ALP-tauon coupling value from TdAlps-based coupling dictionary coeffs"""
    if 'E' in coeffs:
        if np.array(coeffs['E']).ndim>1 and len(coeffs['E'][0])>2:
            return -coeffs['E'][2][2]+coeffs['e'][2][2]
        return -coeffs['E']+coeffs['e']
    elif 'L' in coeffs:
        if np.array(coeffs['L']).ndim>1 and len(coeffs['L'][0])>2:
            return -coeffs['L'][2][2]+coeffs['e'][2][2]
        return -coeffs['L']+coeffs['e']
    return 0

def readAlphaEM(coeffs):
    """Reads out the electromagnetic coupling value from TdAlps-based coupling dictionary coeffs"""
    return coeffs['aEM']

def readAlphaS(coeffs):
    """Reads out the strong coupling value from TdAlps-based coupling dictionary coeffs"""
    return coeffs['a3']
