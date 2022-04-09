import math
import numpy as np
import scipy.integrate
from collections import OrderedDict
import sys
sys.path.insert(1,'/home/ruth/Documents/TdAlps-Internal') #'/home/ruth/Documents/Uni/Projects/ALPs/invisibleVSdisplacedVSprompt/Python/SebastiansCode/TdAlps-Internal'
import TdAlps
import aux

sm={
    'sw': math.sqrt(0.23121), 
    'hbar': 6.582119569*10**(-25),
    'c': 29979245800,
    'me': 0.0005109989461, 
    'mmu': 0.1056583745, 
    'mtau': 1.77686, 
    'mu': 0.00216, 
    'md': 0.00467, 
    'ms': 0.093, 
    'mc': 1.27, 
    'mb': 4.18, 
    'mt': 163.6,#172.76, 
    'mZ': 91.1876, 
    'mB+': 5.27934, 
    'mK+': 0.493677, 
    'mpi+': 0.13957039,
    'mpi0': 0.1349768,
    'fpi': 0.130,
    'tauB+': 1.638*10**(-12),
    'GF': 1.166*10**(-5),
    'alpha': 1/137,
    'Vtb': 0.999,
    'Vts': 0.0404,
    'Xt': 1.462,
    'BrBtoKnunu+': 4.5*10**(-6),
    'NBBBaBar': 471*10**6,
    'NBBBelleII': 5*10**10,
    'mp': 0.9383,
    'mn': 0.9396
}

def fz(t):
    tplus = (sm['mB+']+sm['mK+'])**2
    tminus = (sm['mB+']-sm['mK+'])**2
    tzero = tplus * (1-math.sqrt(1-tminus/tplus))
    return (math.sqrt(tplus-t) - math.sqrt(tplus-tzero))/(math.sqrt(tplus-t) + math.sqrt(tplus-tzero))

def formFactorFplusBplus(qsqr):
    tmp = 0.329
    tmp += -0.876 * (fz(qsqr) - fz(0))
    tmp += 0.006 * (fz(qsqr) - fz(0))**2
    tmp = tmp/(1-qsqr/5.325**2)
    return tmp

def formFactorFzeroBplus(qsqr):
    tmp = 0.329
    tmp += 0.195 * (fz(qsqr) - fz(0))
    tmp += -0.446 * (fz(qsqr) - fz(0))**2
    tmp = tmp/(1-qsqr/5.54**2)
    return tmp

def dGammadqsqrBtoKnunu(qsqr, alphaEM):
    return (sm['GF']**2 * (math.sqrt(sm['mB+']**4+sm['mK+']**4+qsqr**2-2*(sm['mB+']**2 * sm['mK+']**2 + sm['mK+']**2 * qsqr + qsqr * sm['mB+']**2)))**3 * abs(sm['Vtb'])**2 * abs(sm['Vts'])**2 * alphaEM**2 * sm['Xt']**2 * abs(formFactorFplusBplus(qsqr))**2)/(256 * sm['mB+']**3 * math.pi**5 * sm['sw']**4)

def GammaBtoKnunu(alphaEM):
    return scipy.integrate.quad(dGammadqsqrBtoKnunu,0,(sm['mB+']-sm['mK+'])**2,args=(alphaEM))[0]

def BrBtoKnunu(sB,alphaEM):
    qsqrmin = math.floor(10*(sB-0.00001))*0.1*sm['mB+']**2
    qsqrmax = min(math.ceil(10*(sB-0.00001))*0.1*sm['mB+']**2,(sm['mB+']-sm['mK+'])**2)
    return sm['BrBtoKnunu+'] * scipy.integrate.quad(dGammadqsqrBtoKnunu,qsqrmin,qsqrmax,args=(alphaEM))[0]/GammaBtoKnunu(alphaEM)

def B2(tau):
    return 1-(tau-1)*funcB(tau)**2

def B1(tau):
    return 1-tau*funcB(tau)**2

def funcB(tau):
    if tau>=1:
        return math.asin(1/math.sqrt(tau))
    else:
        return math.pi/2 + 1j/2 * math.log((1+math.sqrt(1-tau))/(1-math.sqrt(1-tau)))
    
def Gammaatoll(ma, cll, ml, Lambda):
    if ma <= 2 * ml:
        return 0
    gamma = ml**2 * abs(cll)**2 * math.sqrt(ma**2 - 4 * ml**2) * 2 * math.pi / (Lambda**2) 
    if gamma.imag  != 0:
        if gamma.imag/gamma.real > 10**-10:
            print("The Decay rate to leptons with mass " + str(ml) + " is complex: " + str(gamma))
    return float(gamma)

def Gammaatoqq(ma, cqq, mq, Lambda):
    if ma <= 2 * mq:
        return 0
    gamma = 3 * mq**2 * abs(cqq)**2 * math.sqrt(ma**2 - 4 * mq**2) * 2 * math.pi / (Lambda**2) 
    if gamma.imag  != 0:
        if gamma.imag/gamma.real > 10**-10:
            print("The Decay rate to quarks with mass " + str(mq) + " is complex: " + str(gamma))
    return float(gamma)

def Gammaatogamgam(ma, coeffs, Lambda):
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
    if ((r<0) or (r>1/9)):
        return 0
    integrand = lambda z: math.sqrt(1-4*r/z) * math.sqrt(1+z**2+r**2-2*r-2*z-2*z*r)
    lim_0 = 4*r
    lim_1 = (1-math.sqrt(r))**2
    integral = scipy.integrate.quad(integrand,lim_0,lim_1)
    factor = 2/(1-r)**2
    return factor*integral[0]
    
def gpm(r):
    if ((r<0) or (r>1/9)):
        return 0
    integrand = lambda z: math.sqrt(1-4*r/z) * math.sqrt(1+z**2+r**2-2*r-2*z-2*z*r) * (z-r)**2
    lim_0 = 4*r
    lim_1 = (1-math.sqrt(r))**2
    integral = scipy.integrate.quad(integrand,lim_0,lim_1)
    factor = 12/(1-r)**2
    return factor*integral[0] 

def BrBtoKaplus(ma, cbs, Lambda):
    return abs(cbs)**2 * math.pi/(4 * Lambda**2) * abs(formFactorFzeroBplus(ma**2))**2 * (sm['mB+']**2-sm['mK+']**2)**2/sm['mB+']**3 * math.sqrt(sm['mB+']**4+sm['mK+']**4+ma**4-2*(sm['mB+']**2 * sm['mK+']**2 + sm['mK+']**2 * ma**2 + ma**2 * sm['mB+']**2))/sm['hbar']*sm['tauB+']

def Gammaa(ma, ctL,ctR, Lambda):
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
    gamma = Gammaa(ma,ctL,ctR,Lambda)
    if gamma == 0:
        print("The decay width of a with ma=" + str(ma) + "GeV and cff=" + str(cff) + ", cWW="+ str(cww)+ ", cBB=" + str(cbb) + " is zero.")
        return 0
    return sm['c']*sm['hbar']/gamma

def getLSfromctt(ctL,ctR, Lambda, mu):
    with aux.HiddenPrints():
        HC = OrderedDict()
        HC['Q'] = np.array([[0,0,0],[0,0,0],[0,0,ctL]])
        HC['u'] = np.array([[0,0,0],[0,0,0],[0,0,-ctR]])
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
    if 'U' in coeffs:
        if np.array(coeffs['U']).ndim>1 and len(coeffs['U'][0])>1:
            return -coeffs['U'][1][1]+coeffs['u'][1][1]
    elif 'Q' in coeffs:
        if np.array(coeffs['Q']).ndim>1 and len(coeffs['Q'][0])>1:
            return -coeffs['Q'][1][1]+coeffs['u'][1][1]
    return 0
        
def readCss(coeffs):
    if 'D' in coeffs:
        if np.array(coeffs['D']).ndim>1 and len(coeffs['D'][0])>1:
            return -coeffs['D'][1][1]+coeffs['d'][1][1]
    elif 'Q' in coeffs:
        if np.array(coeffs['Q']).ndim>1 and len(coeffs['Q'][0])>1:
            return -coeffs['Q'][1][1]+coeffs['d'][1][1]
    return 0
            
def readCtt(coeffs):
    if 'U' in coeffs:
        if np.array(coeffs['U']).ndim>1 and len(coeffs['U'][0])>2:
            return -coeffs['U'][2][2]+coeffs['u'][2][2]
    elif 'Q' in coeffs:
        if np.array(coeffs['Q']).ndim>1 and len(coeffs['Q'][0])>2:
            return -coeffs['Q'][2][2]+coeffs['u'][2][2]
    return 0
            
def readCbb(coeffs):
    if 'D' in coeffs:
        if np.array(coeffs['D']).ndim>1 and len(coeffs['D'][0])>2:
            return -coeffs['D'][2][2]+coeffs['d'][2][2]
    elif 'Q' in coeffs:
        if np.array(coeffs['Q']).ndim>1 and len(coeffs['Q'][0])>2:
            return -coeffs['Q'][2][2]+coeffs['d'][2][2]
    return 0

def readCGG(coeffs):
    return coeffs['GG']

def readCgg(coeffs):
    if 'gamgam' in coeffs:
        return coeffs['gamgam']
    return 0

def readCee(coeffs):
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
    return coeffs['aEM']

def readAlphaS(coeffs):
    return coeffs['a3']
