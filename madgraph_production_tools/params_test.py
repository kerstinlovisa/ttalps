from collections import OrderedDict
import math
import numpy as np
import os
import sys
from scipy.integrate import solve_ivp
import tools
import HighRunning
import basisrotation
import matching
import LowRunning
import TdAlps

p = OrderedDict()

p['PI']=math.pi

"""The SM parameters at mu=mZ"""
p['mt'] 	= 172.76
p['mb'] 	= 4.18
p['mtau'] 	= 1.77686
p['mc']		= 1.28
p['mmu']	= 105.66e-3
p['ms']		= 96e-3
p['md']		= 4.7e-3
p['mu']		= 2.2e-3
p['me']		= 0.511e-3
p['sW2'] 	= 0.23122
p['mW'] 	= 80.379
p['mZ'] 	= 91.1876
p['a3'] 	= 0.1181
p['aEM'] 	= 1./127.955
p['mH'] 	= 125
p['a2'] 	= p['aEM']/p['sW2']
p['a1'] 	= p['aEM']/(1-p['sW2'])
p['vh'] 	= p['mW']/np.sqrt(p['a2']*4*p['PI'])*2
p['yt'] 	= p['mt']/p['vh']*np.sqrt(2)
p['yb'] 	= p['mb']/p['vh']*np.sqrt(2)
p['ytau'] 	= p['mtau']/p['vh']*np.sqrt(2)
p['lam'] 	= (p['mH']/p['vh'])**2/2

p['Vus'] 	= 0.2243
p['Vub'] 	= 3.62e-3
p['Vcb'] 	= 4.221e-2
p['delta'] 	= 1.27


smCouplings_ordered = [p['a1'],p['a2'],p['a3'],p['yt'],p['yb'],p['ytau'],p['lam']]

class HiddenPrints:
    """with HiddenPrints(): hides all stdout within this environment"""
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout

def array2dict(A):
    D = OrderedDict()
    i=0
    for c in coeffs:
        mat = coeffMat[c]
        if mat == 'S':
            j = i+1
            D[c] = A[i]
        else:
            j = i + 9
            D[c] = A[i:j].reshape((3,3))
        i = j
    return D


def getLSfromctt(ctL,ctR, Lambda, mu):
    """Returns low-energy coefficient dictionary from UV ALP-top couplings
    
    Interface function to the TdAlps package
    ctL - coupling of the lefthanded top-quark to the ALP in the UV
    ctR - coupling of the righthanded top-quark to the ALP in the UV
    Lambda - cutoff scale of the ALP-EFT where ctL and ctR are defines
    mu - low-energy scale to which the couplings are run
    the running is based on hep-ph: [2012.12272]"""
    with HiddenPrints():
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


def readCmumu(coeffs):
    """Reads out the ALP-muon coupling value from TdAlps-based coupling dictionary coeffs"""
    if 'E' in coeffs:
        
        if np.array(coeffs['E']).ndim>1 and len(coeffs['E'][0])>1:
            print("option 1.a")
            return -coeffs['E'][1][1]+coeffs['e'][1][1]

        print("option 1.b")
        return -coeffs['E']+coeffs['e']
    elif 'L' in coeffs:
        
        if np.array(coeffs['L']).ndim>1 and len(coeffs['L'][0])>1:
            print("option 2.a")
            return -coeffs['L'][1][1]+coeffs['e'][1][1]
        print("option 2.b")
        return -coeffs['L']+coeffs['e']

    print("option 3")
    return 0


def Gammaatoll(ma, cll, ml, Lambda):
    """decay rate of an ALP to a pair of leptons

    ma - ALP mass
    cll - coupling of ALP to leptons
    ml - mass of leptons
    Lambda - cutoff scale of the ALP-EFT
    following hep-ph: [2012.12272]"""
    if ma <= 2 * ml:
        return 0
    gamma = ml ** 2 * abs(cll) ** 2 * math.sqrt(ma ** 2 - 4 * ml ** 2) * 2 * math.pi / (Lambda ** 2)
    if gamma.imag != 0:
        if gamma.imag / gamma.real > 10 ** -10:
            print("The Decay rate to leptons with mass " + str(ml) + " is complex: " + str(gamma))
    return float(gamma)

coupling = 0.5
Lambda = 1000
alp_mass = 1

lscs = getLSfromctt(coupling, coupling, Lambda, alp_mass)

for k, v in lscs.items():
    print(f"{k}: {v}")

# print(f"{lscs=}")

cmumu = readCmumu(lscs)

print(f"{cmumu=}")

# gamma = ph.Gammaatoll(alp_mass, cmumu, p['mmu'], Lambda)


# V_41 = Vertex(name = 'V_41', particles = [ P.t__tilde__, P.t, P.ax ],
#               color = [ 'Identity(1,2)' ],
#               lorentz = [ L.FFS1, L.FFS3 ],
#               couplings = {(0,0):C.GC_82,(0,1):C.GC_85})
# GC_82 = Coupling(name = 'GC_82', value = '-(CQ3x3/fa) - complexconjugate(CQ3x3)/fa', order = {'NP':1})
# GC_85 = Coupling(name = 'GC_85', value = '-(Cu3x3/fa) - complexconjugate(Cu3x3)/fa', order = {'NP':1})