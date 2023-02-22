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


def RunRotateMatchRun(HC,high_scale,low_scale,loops):
    # print("The SM parameters at mu=mZ")
    # print(tools.array2dictSM(params.smCouplings_ordered))
    sol = solve_ivp(HighRunning.smRGE, [p['mZ'], high_scale], params.smCouplings_ordered, args=[loops])
    smpHigh = sol.y[:, -1]
   
    HC.update(tools.array2dictSM(smpHigh))
    # print(HC['a3'])
    HCa = tools.dict2array(HC)
    # print(" \n \n \n")
    # print("The SM parameters at mu=Lambda")
    # print(tools.array2dictSM(smpHigh))
    if low_scale>p['mZ']:
        sol2 = solve_ivp(HighRunning.High_RGE_array, [high_scale,low_scale], HCa, args=[loops])
        # LC = tools.array2dict(sol2.y[:, -1])
        return tools.array2dict(sol2.y[:, -1])
    else :
        sol2 = solve_ivp(HighRunning.High_RGE_array, [high_scale, p['mZ']], HCa, args=[loops])
        LC = tools.array2dict(sol2.y[:, -1])
        LCrot = basisrotation.brot(LC)
        LK = matching.matching(LCrot, p['mZ'])  # after matching and basisrotations at mZ
        LKa = tools.dict2array8(LK)
        if low_scale>=p['mb']:
            sol3 = solve_ivp(LowRunning.Low_RGE_array8, [p['mZ'], low_scale], LKa, args=[loops,8])
            return tools.array2dict8(sol3.y[:, -1])
        else :
            sol3 = solve_ivp(LowRunning.Low_RGE_array8, [p['mZ'], p['mb']], LKa, args=[loops,8])
            LR8 = tools.array2dict8(sol3.y[:, -1])
            if low_scale>=p['mtau']:
                LR8['D']=LR8['D'][0:-1,0:-1]
                LR8['d']=LR8['d'][0:-1,0:-1]
                sol4 = solve_ivp(LowRunning.Low_RGE_array7, [p['mb'], low_scale], tools.dict2array7(LR8), args=[loops,7])
                return tools.array2dict7(sol4.y[:, -1])
            else :
                LR8['D']=LR8['D'][0:-1,0:-1]
                LR8['d']=LR8['d'][0:-1,0:-1]
                sol4 = solve_ivp(LowRunning.Low_RGE_array7, [p['mb'], p['mtau']], tools.dict2array7(LR8), args=[loops,7])
                LR7 = tools.array2dict7(sol4.y[:, -1])
                if low_scale>=p['mc']:
                    LR7['E']=LR7['E'][0:-1,0:-1]
                    LR7['e']=LR7['e'][0:-1,0:-1]
                    sol5 = solve_ivp(LowRunning.Low_RGE_array6, [p['mtau'], low_scale], tools.dict2array6(LR7), args=[loops,6])
                    return tools.array2dict6(sol5.y[:, -1])
                else :
                    LR7['E']=LR7['E'][0:-1,0:-1]
                    LR7['e']=LR7['e'][0:-1,0:-1]
                    sol5 = solve_ivp(LowRunning.Low_RGE_array6, [p['mtau'], p['mc']], tools.dict2array6(LR7), args=[loops,6])
                    LR6 = tools.array2dict6(sol5.y[:, -1])
                    if low_scale>=1.0:  ###QCD confinement scale
                        LR6['U']=LR6['U'][0:-1,0:-1]
                        LR6['u']=LR6['u'][0:-1,0:-1]
                        sol6 = solve_ivp(LowRunning.Low_RGE_array5, [p['mc'], low_scale], tools.dict2array5(LR6), args=[loops,5])
                        return tools.array2dict5(sol6.y[:, -1])
                    else:
                        print("no valid value for the low scale chosen. Has do be higher than the QCD confinement scale!")
                        print('Returning the value of the coefficients at 1GeV')
                        LR6['U']=LR6['U'][0:-1,0:-1]
                        LR6['u']=LR6['u'][0:-1,0:-1]
                        sol6 = solve_ivp(LowRunning.Low_RGE_array5, [p['mc'], 1], tools.dict2array5(LR6), args=[loops,5])
                        return tools.array2dict5(sol6.y[:, -1])

        # print(LR)



























