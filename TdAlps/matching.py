import math
from typing import Dict

from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import numpy as np
import sys
import params
from params import p
from ckmutil import ckm
from collections import OrderedDict


ln = np.log
I3 = np.identity(3)
I2 = np.identity(2)

T3 = np.array([[0, 0, 0], [0, 0, 0], [0,0,1]])


V = ckm.ckm_tree(p["Vus"], p["Vub"], p["Vcb"], p["delta"])  # V as np array

def matching(WK,mu):
     sW2= WK['a1']/(WK['a1']+WK['a2'])
     mt = WK['yt']*p['vh']/np.sqrt(2)
     xt = mt**2 / p['mW']**2
     d1 = - 11 / 3 #this is a scheme dependent parameter. Here chosen for DimReg.

     ctt = WK['u'][2][2] - WK['U'][2][2]


     T3U=1/2
     T3D=-1/2
     T3E=-1/2
     T3nu=1/2

     Qu=2/3
     Qe=-1
     Qd=-1/3
     Qnu=0

     MK = OrderedDict()
     MK['aEM']=1/(1/WK['a1']+1/WK['a2'])


     MK['U'] = WK['U'][0:-1,0:-1] + I2 * (3 * WK['yt']**2 / (8 * p['PI']**2) * ctt * (T3U - Qu * sW2) * ln(mu**2 / (mt**2)) + 3 * MK['aEM']**2 / (8 * p['PI']**2) * (WK['WW'] / (2 * sW2**2) * (ln(mu**2 / (p['mW']**2)) + 0.5 + d1) + 2 * WK['gamz'] / (sW2 * (1 - sW2)) * Qu * (T3U - Qu * sW2) * (ln(mu**2 / (p['mZ']**2)) + 1.5 + d1) +  WK['ZZ'] / (sW2**2 * (1 - sW2)**2) * (T3U - Qu * sW2)**2 * (ln(mu**2 / (p['mZ']**2)) + 0.5 + d1)))
     MK['E'] = WK['E'] +            I3 * (3 * WK['yt']**2 / (8 * p['PI']**2) * ctt * (T3E - Qe * sW2) * ln(mu**2 / (mt**2)) + 3 * MK['aEM']**2 / (8 * p['PI']**2) * (WK['WW'] / (2 * sW2**2) * (ln(mu**2 / (p['mW']**2)) + 0.5 + d1) + 2 * WK['gamz'] / (sW2 * (1 - sW2)) * Qe * (T3E - Qe * sW2) * (ln(mu**2 / (p['mZ']**2)) + 1.5 + d1) +  WK['ZZ'] / (sW2**2 * (1 - sW2)**2) * (T3E - Qe * sW2)**2 * (ln(mu**2 / (p['mZ']**2)) + 0.5 + d1)))
     MK['nu'] = WK['nu'] +          I3 * (3 * WK['yt']**2 / (8 * p['PI']**2) * ctt * (T3nu -Qnu* sW2) * ln(mu**2 / (mt**2)) + 3 * MK['aEM']**2 / (8 * p['PI']**2) * (WK['WW'] / (2 * sW2**2) * (ln(mu**2 / (p['mW']**2)) + 0.5 + d1) + 2 * WK['gamz'] / (sW2 * (1 - sW2)) * Qnu* (T3nu- Qnu* sW2) * (ln(mu**2 / (p['mZ']**2)) + 1.5 + d1) +  WK['ZZ'] / (sW2**2 * (1 - sW2)**2) * (T3nu- Qnu* sW2)**2 * (ln(mu**2 / (p['mZ']**2)) + 0.5 + d1)))
     MK['u'] = WK['u'][0:-1,0:-1] + I2 * (3 * WK['yt']**2 / (8 * p['PI']**2) * ctt * (-Qu) * sW2 * ln(mu**2 / (mt**2)) +      3 * MK['aEM']**2 / (8 * p['PI']**2) * (Qu)**2 * (2 * WK['gamz'] / (1 - sW2) * (ln(mu**2 / (p['mZ']**2)) + 1.5 + d1) - WK['ZZ'] / (1 - sW2)**2 * (ln(mu**2 / (p['mZ']**2)) + 0.5 + d1)))
     MK['d'] = WK['d'] +            I3 * (3 * WK['yt']**2 / (8 * p['PI']**2) * ctt * (-Qd) * sW2 * ln(mu**2 / (mt**2)) +      3 * MK['aEM']**2 / (8 * p['PI']**2) * (Qd)**2 * (2 * WK['gamz'] / (1 - sW2) * (ln(mu**2 / (p['mZ']**2)) + 1.5 + d1) - WK['ZZ'] / (1 - sW2)**2 * (ln(mu**2 / (p['mZ']**2)) + 0.5 + d1)))
     MK['e'] = WK['e'] +            I3 * (3 * WK['yt']**2 / (8 * p['PI']**2) * ctt * (-Qe) * sW2 * ln(mu**2 / (mt**2)) +      3 * MK['aEM']**2 / (8 * p['PI']**2) * (Qe)**2 * (2 * WK['gamz'] / (1 - sW2) * (ln(mu**2 / (p['mZ']**2)) + 1.5 + d1) - WK['ZZ'] / (1 - sW2)**2 * (ln(mu**2 / (p['mZ']**2)) + 0.5 + d1)))
     MK['D'] = WK['D'] +            I3 * (3 * WK['yt']**2 / (8 * p['PI']**2) * ctt * (T3D - Qd * sW2) * ln(mu**2 / (mt**2)) + 3 * MK['aEM']**2 / (8 * p['PI']**2) * (WK['WW'] / (2 * sW2**2) * (ln(mu**2 / (p['mW']**2)) + 0.5 + d1) + 2 * WK['gamz'] / (sW2 * (1 - sW2)) * Qd * (T3D - Qd * sW2) * (ln(mu**2 / (p['mZ']**2)) + 1.5 + d1) +  WK['ZZ'] / (sW2**2 * (1 - sW2)**2) * (T3D - Qd * sW2)**2 * (ln(mu**2 / (p['mZ']**2)) + 0.5 + d1)))+ WK['yt']**2 / (16 * p['PI']**2) * ((V.conj().T @ T3 @ WK['U'] @ V + V.conj().T @ WK['U'] @ T3 @ V) * (-1 / 4 * ln (mu**2 / (mt**2)) - 3 / 8 + (3 / 4) * (1 - xt + ln(xt)) / (1 - xt)**2)+ V.conj().T @  T3 @ V * WK['U'][2][2] + V.conj().T @ T3 @ V * WK['u'][2][2] * (1/2 * ln(mu**2/(mt**2)) - 1 / 4 - (3 / 2) * (1 - xt + ln(xt)) / (1 - xt)**2) - 3 * MK['aEM']/ ( 2 * p['PI'] * sW2) * WK['WW'] * V.conj().T @ T3 @ V * (1 - xt + xt * ln(xt)) / (1 - xt)**2)
     MK['gamgam'] = WK['gamgam']
     MK['GG'] = WK['GG']
     MK['a3'] = WK['a3']

     return MK
