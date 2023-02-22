import math
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import numpy as np
import sys
# import params
from params import p
from collections import OrderedDict
import tools

if not (sys.version_info.major == 3):
    print("This script was written for Python3.")
    print("For a correct functioning of divisions in Python2 put")
    print("from __future__ import division")
    print("at the beginning of your script!")


# TODO: Eingabe der Matrix,
# TODO: joint RGE schreiben

def High_RGE(mu, HC, loop_order):
    """This defines the RGE of the axion + SM Lagrangian in the high-energy theory""" 
    a1 = HC['a1']
    a2 = HC['a2']
    a3 = HC['a3']
    yt = HC['yt']
    yb = HC['yb']
    ytau = HC['ytau']
    Lambda = HC['Lambda']
    #yt = 1 #
    #a3, etc. all der input aus dem standard Model running
    # weiterer Input wie cgg, cbb, cww

    # Achtung ctt läuft!!!, Achtung: Zählung der Matrixelemente ab 0
    ctt = HC['u'][2][2] - HC['Q'][2][2]
    cggt1 = HC['GG']
    cbbt1 = HC['BB']
    cwwt1 = HC['WW']

    cggt2 = 0.5 * np.trace((HC['u'] + HC['d'] - 2 * HC['Q']))
    cbbt2 = np.trace(((4/3) * HC['u'] + (1/3) * HC['d'] - (1/6) * HC['Q'] + HC['e'] - 0.5 * HC['L']))
    cwwt2 = - 0.5 * np.trace((3 * HC['Q'] + HC['L']))


    I3 = np.identity(3)
    # di3 = np.array([[0., 0., 1.], [0., 0., 1.], [0.,0.,1.]]) #this only appears in the part where i=j and therefore it has to be diag([0,0,1])
    di3 = np.diag([0,0,1])
    # dj3 = np.array([[1, 0, 0], [1, 0, 0], [1,0,0]]) brauchen wir hier eigentlich nicht
   # di3j3 = np.array([[0, 0, 1], [0, 0, 1], [1,1,0]]) same here
    di3dj3cQ = np.array([[0.,0.,HC['Q'][0][2] ], [0.,0.,HC['Q'][1][2] ],[HC['Q'][2][0],HC['Q'][2][1],0.]])
    di3dj3cu = np.array([[0., 0., HC['u'][0][2] ], [0., 0., HC['u'][1][2] ], [HC['u'][2][0], HC['u'][2][1], 0.]])
    beta = OrderedDict()

    beta['Q'] = np.array([[0.,0.,0.],[0.,0.,0.],[0.,0.,0.]])
    beta['u'] = np.array([[0.,0.,0.],[0.,0.,0.],[0.,0.,0.]])
    beta['d'] = np.array([[0.,0.,0.],[0.,0.,0.],[0.,0.,0.]])
    beta['L'] = np.array([[0.,0.,0.],[0.,0.,0.],[0.,0.,0.]])
    beta['e'] = np.array([[0.,0.,0.],[0.,0.,0.],[0.,0.,0.]])
    beta['GG'] = 0
    beta['WW'] = 0
    beta['BB'] = 0

    #see eq. 5
    bu = -1
    bd = be = 1
    bQ = bL = 0


    if loop_order >= 1:
        beta['d'] += I3 * (- 3 * yt ** 2 / (8 * p['PI'] ** 2) * bd * ctt ) + I3 * (a3 **2/(p['PI'] **2) * cggt1 + a1 **2/(12 * p['PI'] **2) * cbbt1)
        beta['L'] += I3 * (- 3 * yt ** 2 / (8 * p['PI'] ** 2) * bL * ctt ) + I3 * ( - 9*a2**2/(16 * p['PI'] **2) * cwwt1 - 3 * a1 **2/(16 * p['PI'] **2) * cbbt1)
        beta['e'] += I3 * (- 3 * yt ** 2 / (8 * p['PI'] ** 2) * be * ctt ) + I3 * ( 3 * a1 **2/(4 * p['PI'] **2) * cbbt1)
        beta['u'] += ( yt ** 2 / (8 * p['PI'] ** 2) * ((di3 -       3 * bu*I3) * ctt)) + yt**2 / (16 * p['PI']**2) * di3dj3cu + I3 * (   a3 **2 /(p['PI'] **2) * cggt1 + a1 ** 2 / (3 * p['PI'] ** 2) * cbbt1)
        beta['Q'] += (-yt ** 2 / (8 * p['PI'] ** 2) * ((di3 / 2 +   3 * bQ*I3) * ctt)) + yt**2 / (32 * p['PI']**2) * di3dj3cQ + I3 * ( - a3 **2 /(p['PI'] **2) * cggt1 - 9  * a2 **2/(16 * p['PI'] **2) * cwwt1 - a1 ** 2 / (48 * p['PI'] ** 2) * cbbt1)




    if loop_order >= 2:
        beta['d'] += I3 * (a3 **2/(p['PI'] **2) * cggt2 + a1 **2/(12 * p['PI'] **2) * cbbt2)
        beta['L'] += I3 * ( - 9*a2**2/(16 * p['PI'] **2) * cwwt2 - 3 * a1 **2/(16 * p['PI'] **2) * cbbt2)
        beta['e'] += I3 * ( 3 * a1 **2/(4 * p['PI'] **2) * cbbt2)
        beta['u'] += I3 * ( a3 **2 /(p['PI'] **2) * cggt2 + a1 ** 2 / (3 * p['PI'] ** 2) * cbbt2)
        beta['Q'] += I3 * ( - a3 **2 /(p['PI'] **2) * cggt2 - 9  * a2 **2/(16 * p['PI'] **2) * cwwt2 - a1 ** 2 / (48 * p['PI'] ** 2) * cbbt2)

    beta['d']=beta['d']/mu
    beta['L']=beta['L']/mu
    beta['e']=beta['e']/mu
    beta['u']=beta['u']/mu
    beta['Q']=beta['Q']/mu

    beta['a1'],beta['a2'],beta['a3'],beta['yt'],beta['yb'],beta['ytau'],beta['Lambda']=smRGE(mu,[a1, a2, a3, yt, yb, ytau, Lambda],loop_order)

    return beta

def High_RGE_array(mu, HCa, loop_order):
    HCd=tools.array2dict(HCa)
    beta=High_RGE(mu, HCd, loop_order)
    return tools.dict2array(beta)


def smRGE(mu, smc, loop_order):
    """ This defines the RGE of the SM couplings above the weak scale.
    The formulas are 1-loop and taken from 1307.3536.
    The definition of alpha_1 differs by 5/3 and this is corrected for here.
    Gauge couplings are translated to g from alpha and then back."""
    a1, a2, a3, yt, yb, ytau, Lambda = smc
    g1 = np.sqrt(5 / 3 * a1 * (4 * p['PI']))
    g2 = np.sqrt(a2 * (4 * p['PI']))
    g3 = np.sqrt(a3 * (4 * p['PI']))

    beta1 = 0
    beta2 = 0
    beta3 = 0
    betat = 0
    betab = 0
    betatau = 0
    betal = 0

    if loop_order >= 1:
        beta1 += g1 ** 4 / (4 * p['PI']) ** 2 * 41 / 10
        beta2 += g2 ** 4 / (4 * p['PI']) ** 2 * (-19 / 6)
        beta3 += g3 ** 4 / (4 * p['PI']) ** 2 * (-7)
        betat += yt ** 2 / (4 * p['PI']) ** 2 * (
                    9 / 2 * yt ** 2 - 8 * g3 ** 2 - 9 / 4 * g2 ** 2 - 17 / 20 * g1 ** 2 + 3 / 2 * yb ** 2 + ytau ** 2)
        betab += yb ** 2 / (4 * p['PI']) ** 2 * (
                    3 / 2 * yt ** 2 + 9 / 2 * yb ** 2 + ytau ** 2 - 8 * g3 ** 2 - 9 / 4 * g2 ** 2 - 1 / 4 * g1 ** 2)
        betatau += ytau ** 2 / (4 * p['PI']) ** 2 * (
                    3 * yt ** 2 + 3 * yb ** 2 + 5 / 2 * ytau ** 2 - 9 / 4 * (g2 ** 2 + g1 ** 2))
        betal += 1 / (4 * p['PI']) ** 2 * (Lambda * (
                    12 * Lambda + 6 * yt ** 2 + 6 * yb ** 2 + 2 * ytau ** 2 - 9 / 2 * g2 ** 2 - 9 / 10 * g1 ** 2) - 3 * yt ** 4 - 3 * yb ** 4 - ytau ** 4 + 9 / 16 * g2 ** 4 + 27 / 400 * g1 ** 4 + 9 / 40 * g1 ** 2 * g2 ** 2)
    if loop_order >= 2:
        beta1 += g1 ** 4 / (4 * p['PI']) ** 4 * (
                    44 / 5 * g3 ** 2 + 27 / 10 * g2 ** 2 + 199 / 50 * g1 ** 2 - 17 / 10 * yt ** 2 - (
                        yb ** 2 + 3 * ytau ** 2) / 2)
        beta2 += g2 ** 4 / (4 * p['PI']) ** 4 * (12 * g3 ** 2 + 35 / 6 * g2 ** 2 + 9 / 10 * g1 ** 2 - 3 / 2 * yt ** 2 - (
                    3 * yb ** 2 + ytau ** 2) / 2)
        beta3 += g3 ** 4 / (4 * p['PI']) ** 4 * (
                    -26 * g3 ** 2 + 9 / 2 * g2 ** 2 + 11 / 10 * g1 ** 2 - 2 * yt ** 2 - 2 * yb ** 2)
        betat += yt ** 2 / (4 * p['PI']) ** 4 * (yt ** 2 * (
                    -12 * yt ** 2 - 12 * Lambda + 36 * g3 ** 2 + 225 / 16 * g2 ** 2 + 393 / 80 * g1 ** 2 - 11 / 4 * yb ** 2 - 9 / 4 * ytau ** 2) + 6 * Lambda ** 2 - 108 * g3 ** 4 - 23 / 4 * g2 ** 4 - 1187 / 600 * g1 ** 4 + 9 * g3 ** 2 * g2 ** 2 + 19 / 15 * g3 ** 2 * g1 ** 2 - 9 / 20 * g1 ** 2 * g2 ** 2 + yb ** 2 * (
                                                        -yb ** 2 / 4 + 5 / 4 * ytau ** 2 + 4 * g3 ** 2 + 99 / 16 * g2 ** 2 + 7 / 80 * g1 ** 2) + ytau ** 2 * (
                                                        -9 / 4 * ytau ** 2 + 15 / 8 * (g2 ** 2 + g1 ** 2)))
        betab += yb ** 2 / (4 * p['PI']) ** 4 * (yt ** 2 * (
                    -1 / 4 * yt ** 2 - 11 / 4 * yb ** 2 + 5 / 4 * ytau ** 2 + 4 * g3 ** 2 + 99 / 16 * g2 ** 2 + 91 / 80 * g1 ** 2) + yb ** 2 * (
                                                        -12 * yb ** 2 - 9 / 4 * ytau ** 2 - 12 * Lambda + 36 * g3 ** 2 + 225 / 16 * g2 ** 2 + 237 / 80 * g1 ** 2) + ytau ** 2 * (
                                                        -9 / 4 * ytau ** 2 + 15 / 8 * (
                                                            g2 ** 2 + g1 ** 2)) + 6 * Lambda ** 2 - 108 * g3 ** 4 - 23 / 4 * g2 ** 4 - 127 / 600 * g1 ** 4 + 9 * g3 ** 2 * g2 ** 2 + 31 / 15 * g3 ** 2 * g1 ** 2 - 27 / 20 * g1 ** 2 * g2 ** 2)
        betatau += ytau ** 2 / (4 * p['PI']) ** 4 * (yt ** 2 * (
                    -27 / 4 * yt ** 2 + 3 / 2 * yb ** 2 - 27 / 4 * ytau ** 2 + 20 * g3 ** 2 + 45 / 8 * g2 ** 2 + 17 / 8 * g1 ** 2) + yb ** 2 * (
                                                            -27 / 4 * yb ** 2 - 27 / 4 * ytau ** 2 + 20 * g3 ** 2 + 45 / 8 * g2 ** 2 + 5 / 8 * g1 ** 2) + ytau ** 2 * (
                                                            -3 * ytau ** 2 - 12 * Lambda + 165 / 16 * g2 ** 2 + 537 / 80 * g1 ** 2) + 6 * Lambda ** 2 - 23 / 4 * g2 ** 4 + 1371 / 200 * g1 ** 4 + 27 / 20 * g1 ** 2 * g2 ** 2)
        betal += 1 / (4 * p['PI']) ** 4 * (Lambda ** 2 * (
                    -156 * Lambda - 72 * yt ** 2 + 54 * g2 ** 2 + 54 / 5 * g1 ** 2 - 72 * yb ** 2 - 24 * ytau ** 2) + Lambda * yt ** 2 * (
                                                  -3 / 2 * yt ** 2 + 40 * g3 ** 2 + 45 / 4 * g2 ** 2 + 17 / 4 * g1 ** 2 - 21 * yb ** 2) + Lambda * (
                                                  -73 / 16 * g2 ** 4 + 1887 / 400 * g1 ** 4 + 117 / 40 * g1 ** 2 * g2 ** 2) + yt ** 4 * (
                                                  15 * yt ** 2 - 16 * g3 ** 2 - 4 / 5 * g1 ** 2 - 3 * yb ** 2) + yt ** 2 * (
                                                  -9 / 8 * g2 ** 4 - 171 / 200 * g1 ** 4 + 63 / 20 * g1 ** 2 * g2 ** 2) + 305 / 32 * g2 ** 6 - 3411 / 4000 * g1 ** 6 - 289 / 160 * g2 ** 4 * g1 ** 2 - 1677 / 800 * g1 ** 4 * g2 ** 2 + Lambda * yb ** 2 * (
                                                  -3 / 2 * yb ** 2 + 40 * g3 ** 2 + (
                                                      45 * g2 ** 2 + 5 * g1 ** 2) / 4) + Lambda * ytau ** 2 * (
                                                  -ytau ** 2 / 2 + 15 * (g2 ** 2 + g1 ** 2) / 4) + yb ** 4 * (
                                                  -3 * yt ** 2 + 15 * yb ** 2 - 16 * g3 ** 2 + 2 * g1 ** 2 / 5) + yb ** 2 * (
                                                  -9 / 8 * g2 ** 4 + 9 / 40 * g1 ** 4 + 27 / 20 * g1 ** 2 * g2 ** 2) + ytau ** 4 * (
                                                  5 * ytau ** 2 - 6 / 5 * g1 ** 2) + ytau ** 2 * (
                                                  -3 / 8 * (g2 ** 4 + 3 * g1 ** 4) + 33 / 20 * g1 ** 2 * g2 ** 2))
    if loop_order >= 3:
        beta1 += g1 ** 4 / (4 * p['PI']) ** 6 * (yt ** 2 * (
                    189 / 16 * yt ** 2 - 29 / 5 * g3 ** 2 - 471 / 32 * g2 ** 2 - 2827 / 800 * g1 ** 2) + Lambda * (
                                                        -9 / 5 * Lambda + 9 / 10 * g2 ** 2 + 27 / 50 * g1 ** 2) + 297 / 5 * g3 ** 4 + 789 / 64 * g2 ** 4 - 388613 / 24000 * g1 ** 4 - 3 / 5 * g3 ** 2 * g2 ** 2 - 137 / 75 * g3 ** 2 * g1 ** 2 + 123 / 160 * g2 ** 2 * g1 ** 2)
        beta2 += g2 ** 4 / (4 * p['PI']) ** 6 * (
                    yt ** 2 * (147 / 16 * yt ** 2 - 7 * g3 ** 2 - 729 / 32 * g2 ** 2 - 593 / 160 * g1 ** 2) + Lambda * (
                        -3 * Lambda + 3 / 2 * g2 ** 2 + 3 / 10 * g1 ** 2) + 81 * g3 ** 4 + 324953 / 1728 * g2 ** 4 - 5597 / 1600 * g1 ** 4 + 39 * g3 ** 2 * g2 ** 2 - 1 / 5 * g1 ** 2 * g3 ** 2 + 873 / 160 * g2 ** 2 * g1 ** 2)
        beta3 += g3 ** 4 / (4 * p['PI']) ** 6 * (yt ** 2 * (
                    15 * yt ** 2 - 40 * g3 ** 2 - 93 / 8 * g2 ** 2 - 101 / 40 * g1 ** 2) + 65 / 2 * g3 ** 4 + 109 / 8 * g2 ** 4 - 523 / 120 * g1 ** 4 + 21 * g3 ** 2 * g2 ** 2 + 77 / 15 * g3 ** 2 * g1 ** 2 - 3 / 40 * g2 ** 2 * g1 ** 2)
        betat += yt ** 2 / (4 * p['PI']) ** 6 * (yt ** 4 * (
                    58.6028 * yt ** 2 + 198 * Lambda - 157 * g3 ** 2 - 1593 / 16 * g2 ** 2 - 2437 / 80 * g1 ** 2) + Lambda * yt ** 2 * (
                                                        15 / 4 * Lambda + 16 * g3 ** 2 - 135 / 2 * g2 ** 2 - 127 / 10 * g1 ** 2) + yt ** 2 * (
                                                        363.764 * g3 ** 4 + 16.990 * g2 ** 4 - 24.422 * g1 ** 4 + 48.370 * g3 ** 2 * g2 ** 2 + 18.074 * g3 ** 2 * g1 ** 2 + 34.829 * g2 ** 2 * g1 ** 2) + Lambda ** 2 * (
                                                        -36 * Lambda + 45 * g2 ** 2 + 9 * g1 ** 2) + Lambda * (
                                                        -171 / 16 * g2 ** 4 - 1089 / 400 * g1 ** 4 + 117 / 40 * g1 ** 2 * g2 ** 2) - 619.35 * g3 ** 6 + 169.829 * g2 ** 6 + 16.099 * g1 ** 6 + 73.654 * g3 ** 4 * g2 ** 2 - 15.096 * g3 ** 4 * g1 ** 2 - 21.072 * g3 ** 2 * g2 ** 4 - 22.319 * g3 ** 2 * g1 ** 4 - 321 / 20 * g3 ** 2 * g2 ** 2 * g1 ** 2 - 4.743 * g2 ** 4 * g1 ** 2 - 4.442 * g2 ** 2 * g1 ** 4)
        betab += 0
        betatau += 0
        betal += 1 / (4 * p['PI']) ** 6 * (Lambda ** 3 * (
                    6011.35 * Lambda + 873 * yt ** 2 - 387.452 * g2 ** 2 - 77.490 * g1 ** 2) + Lambda ** 2 * yt ** 2 * (
                                                  1768.26 * yt ** 2 + 160.77 * g3 ** 2 - 359.539 * g2 ** 2 - 63.869 * g1 ** 2) + Lambda ** 2 * (
                                                  -790.28 * g2 ** 4 - 185.532 * g1 ** 4 - 316.64 * g2 ** 2 * g1 ** 2) + Lambda * yt ** 4 * (
                                                  -223.382 * yt ** 2 - 662.866 * g3 ** 2 - 5.470 * g2 ** 2 - 21.015 * g1 ** 2) + Lambda * yt ** 2 * (
                                                  356.968 * g3 ** 4 - 319.664 * g2 ** 4 - 74.8599 * g1 ** 4 + 15.1443 * g3 ** 2 * g2 ** 2 + 17.454 * g3 ** 2 * g1 ** 2 + 5.615 * g2 ** 2 * g1 ** 2) + Lambda * g2 ** 4 * (
                                                  -57.144 * g3 ** 2 + 865.483 * g2 ** 2 + 79.638 * g1 ** 2) + Lambda * g1 ** 4 * (
                                                  -8.381 * g3 ** 2 + 61.753 * g2 ** 2 + 28.168 * g1 ** 2) + yt ** 6 * (
                                                  -243.149 * yt ** 2 + 250.494 * g3 ** 2 + 74.138 * g2 ** 2 + 33.930 * g1 ** 2) + yt ** 4 * (
                                                  -50.201 * g3 ** 4 + 15.884 * g2 ** 4 + 15.948 * g1 ** 4 + 13.349 * g3 ** 2 * g2 ** 2 + 17.570 * g3 ** 2 * g1 ** 2 - 70.356 * g2 ** 2 * g1 ** 2) + yt ** 2 * g3 ** 2 * (
                                                  16.464 * g2 ** 4 + 1.016 * g1 ** 4 + 11.386 * g2 ** 2 * g1 ** 2) + yt ** 2 * g2 ** 4 * (
                                                  62.500 * g2 ** 2 + 13.041 * g1 ** 2) + yt ** 2 * g1 ** 4 * (
                                                  10.627 * g2 ** 2 + 11.117 * g1 ** 2) + g3 ** 2 * (
                                                  7.356 * g2 ** 6 + 0.663 * g1 ** 6 + 1.507 * g2 ** 4 * g1 ** 2 + 1.105 * g2 ** 2 * g1 ** 4) - 114.091 * g2 ** 8 - 1.508 * g1 ** 8 - 37.889 * g2 ** 6 * g1 ** 2 + 6.500 * g2 ** 4 * g1 ** 4 - 1.543 * g2 ** 2 * g1 ** 6)

    smp = [2. / mu * beta1 / (4 * p['PI']) * 3 / 5, 2. / mu * beta2 / (4 * p['PI']), 2. / mu * beta3 / (4 * p['PI']), 1. / (mu * yt) * betat,
           1. / (mu * yb) * betab, 1. / (mu * ytau) * betatau, 2. / mu * betal]

    return smp









    
