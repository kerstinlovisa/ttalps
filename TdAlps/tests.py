import HighRunning
import LowRunning
import basisrotation
from params import p
import params
import tools
import matching
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from collections import OrderedDict
import math

PI = math.pi


def plot(loops):
    sol = solve_ivp(HighRunning.smRGE, [p['mZ'], 10e17], params.smCouplings_ordered, args=[loops], dense_output=True)
    t = np.linspace(np.log10(p['mZ']), 17, 3000)
    z = sol.sol(10 ** t)
    plt.plot(t, z.T)
    plt.title('SM RGE at ' + str(loops) + '-loop')
    plt.xlabel('log(mu)')
    plt.yscale("log")
    plt.ylim([5e-5, 1.1])
    plt.legend(['a1', 'a2', 'a3', 't2', 'b2', 'tau2', 'l'], shadow=True)
    plt.show()

def SMatScale(scale,loops):
    sol = solve_ivp(HighRunning.smRGE, [p['mZ'], scale], params.smCouplings_ordered, args=[loops], dense_output=False)
    smpHigh = sol.y[:, -1]
    print(smpHigh)
    # t = np.linspace(np.log10(p['mZ']), 17, 3000)
    # z = sol.sol(10 ** t)
    # plt.plot(t, z.T)
    # plt.title('SM RGE at ' + str(loops) + '-loop')
    # plt.xlabel('log(mu)')
    # plt.yscale("log")
    # plt.ylim([5e-5, 1.1])
    # plt.legend(['a1', 'a2', 'a3', 't2', 'b2', 'tau2', 'l'], shadow=True)
    # plt.show()


def plotALPS(loops):
    sol = solve_ivp(HighRunning.smRGE, [p['mZ'], 1e10], params.smCouplings_ordered, args=[loops])
    smpHigh = sol.y[:, -1]
    HC = {
        'Q': np.array([[0, 0, 1], [0, 0, 0], [1, 0, 1]]),
        'u': np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]]),
        'd': np.array([[0, 1, 0], [1, 0, 0], [0, 0, 0]]),
        'L': np.array([[0, 0, 0], [0, 0, 1], [0, 1, 0]]),
        'e': np.array([[0, 0, 0], [0, 0, 1], [0, 1, 0]]),
        'GG': 0,
        'WW': 0,
        'BB': 0
    }
    HC.update(tools.array2dictSM(smpHigh))
    HCa = tools.dict2array(HC)
    sol2 = solve_ivp(HighRunning.High_RGE_array, [1e10, p['mZ']], HCa, args=[loops], dense_output=True)
    print(tools.array2dict(sol2.y[:, -1]))
    t = np.linspace(p['mZ'], 1e10, 3000)
    z = sol2.sol(t)[:-7]  # we only plot the BSM coeffs.
    plt.plot(t, abs(z).T)
    plt.title('ALP RGE at ' + str(loops) + '-loop')
    plt.xlabel('log(mu)')
    plt.yscale("log")
    plt.xscale("log")
    plt.ylim([5e-5, 1.1])
    plt.show()


def RunAndRotate(loops):
    print("The SM parameters at mu=mZ")
    print(tools.array2dictSM(params.smCouplings_ordered))
    sol = solve_ivp(HighRunning.smRGE, [p['mZ'], 1e13], params.smCouplings_ordered, args=[loops])
    smpHigh = sol.y[:, -1]
    HC = OrderedDict()
    HC['Q'] = np.array([[0, 0, 1], [0, 0, 0], [1, 0, 1]])
    HC['u'] = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    HC['d'] = np.array([[0, 1, 0], [1, 0, 0], [0, 0, 0]])
    HC['L'] = np.array([[0, 0, 0], [0, 0, 1], [0, 1, 0]])
    HC['e'] = np.array([[0, 0, 0], [0, 0, 1], [0, 1, 0]])
    HC['GG'] = 0
    HC['WW'] = 0
    HC['BB'] = 0
    HC.update(tools.array2dictSM(smpHigh))
    HCa = tools.dict2array(HC)
    print(" \n \n \n")
    print("The SM parameters at mu=Lambda")
    print(tools.array2dictSM(smpHigh))
    sol2 = solve_ivp(HighRunning.High_RGE_array, [1e13, p['mZ']], HCa, args=[loops])
    LC = tools.array2dict(sol2.y[:, -1])
    LCrot = basisrotation.brot(LC)
    print(" \n \n \n")
    print('All coeffs at mu=mZ in up-basis')
    print(LC)
    print(" \n \n \n")
    print('All coeffs at mu=mZ in mass-basis')
    print(LCrot)

def RunMatchRun(loops):
    mb=4.1
    mu=p['mZ']
    HighScale=p['mZ']
    print("The SM parameters at mu=mZ")
    print(tools.array2dictSM(params.smCouplings_ordered))
    sol = solve_ivp(HighRunning.smRGE, [p['mZ'], HighScale], params.smCouplings_ordered, args=[loops])
    smpHigh = sol.y[:, -1]
    HC = OrderedDict()
    HC['Q'] = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 1]])
    HC['u'] = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    HC['d'] = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    HC['L'] = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    HC['e'] = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    HC['GG'] = 0
    HC['WW'] = 0
    HC['BB'] = 0
    HC.update(tools.array2dictSM(smpHigh))
    HCa = tools.dict2array(HC)
    print(" \n \n \n")
    print("The SM parameters at mu=Lambda")
    print(tools.array2dictSM(smpHigh))
    sol2 = solve_ivp(HighRunning.High_RGE_array, [HighScale, p['mZ']], HCa, args=[loops])
    LC = tools.array2dict(sol2.y[:, -1])
    LCrot = basisrotation.brot(LC)
    LK = matching.matching(LCrot, mu)
    LKa=tools.dict2array8(LK)
    solLow = solve_ivp(LowRunning.Low_RGE_array, [p['mZ'], mb], LKa, args=[loops,8], dense_output=True)
    print(tools.array2dict8(solLow.y[:, -1]))
    t = np.linspace(mb,p['mZ'], 3000)
    z = solLow.sol(t)[:-2]  # we only plot the BSM coeffs.
    plt.plot(t, abs(z).T)
    plt.title('ALP RGE at ' + str(loops) + '-loop')
    plt.xlabel('log(mu)')
    plt.yscale("log")
    plt.xscale("log")
    plt.ylim([5e-5, 1.1])
    plt.show()


def RunRotateMatchRun(scale,loops):
    print("The SM parameters at mu=mZ")
    print(tools.array2dictSM(params.smCouplings_ordered))
    sol = solve_ivp(HighRunning.smRGE, [p['mZ'], scale], params.smCouplings_ordered, args=[loops])
    smpHigh = sol.y[:, -1]
    HC = OrderedDict()
    HC['Q'] = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 1]])
    HC['u'] = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    HC['d'] = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    HC['L'] = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    HC['e'] = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    HC['GG'] = 0
    HC['WW'] = 0
    HC['BB'] = 0
    HC.update(tools.array2dictSM(smpHigh))
    HCa = tools.dict2array(HC)
    # print(" \n \n \n")
    # print("The SM parameters at mu=Lambda")
    # print(tools.array2dictSM(smpHigh))
    sol2 = solve_ivp(HighRunning.High_RGE_array, [scale, p['mZ']], HCa, args=[loops])
    LC = tools.array2dict(sol2.y[:, -1])
    LCrot = basisrotation.brot(LC)
    print(" \n \n \n")
    print('All coeffs at mu=mZ in up-basis')
    print(LC)
    print(" \n \n \n")
    print('All coeffs at mu=mZ in mass-basis')
    print(LCrot)
    LK = matching.matching(LCrot, p['mZ'])  # after matching and basisrotations at mZ
    LKa = tools.dict2array8(LK)
    sol3 = solve_ivp(LowRunning.Low_RGE_array, [p['mZ'], p['mb']], LKa, args=[loops,8])
    LR = tools.array2dict8(sol3.y[:, -1])
    print(LR)













