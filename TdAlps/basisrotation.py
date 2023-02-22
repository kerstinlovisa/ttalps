import math
from typing import Dict

from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import numpy as np
import sys
# import params
from params import p
from ckmutil import ckm
from collections import OrderedDict

if not (sys.version_info.major == 3):
    print("This script was written for Python3.")
    print("For a correct functioning of divisions in Python2 put")
    print("from __future__ import division")
    print("at the beginning of your script!")

# PI = math.pi

# p = {}
# p['Vus'] = 0.2243
# p['Vub'] = 3.62e-3
# p['Vcb'] = 4.221e-2
# p['delta'] = 1.27

V = ckm.ckm_tree(p["Vus"], p["Vub"], p["Vcb"], p["delta"])  # V as np array


def brot(HC):


    WK = OrderedDict()

    WK['U'] = HC['Q']
    WK['E'] = HC['L']
    WK['nu'] = HC['L']
    WK['u'] = HC['u']
    WK['d'] = HC['d']
    WK['e'] = HC['e']
    WK['D'] = V.conj().T @ HC['Q'] @ V
    WK['gamgam'] = HC['WW'] + HC['BB']
    WK['gamz'] = (1 - p['sW2']) * HC['WW'] - p['sW2'] * HC['BB']
    WK['GG'] = HC['GG']
    WK['ZZ'] = (1 - p['sW2'])**2 * HC['WW'] + p['sW2']**2 * HC['BB']
    WK['WW'] = HC['WW']
    WK['a1'] = HC['a1']
    WK['a2'] = HC['a2']
    WK['a3'] = HC['a3']
    WK['yt'] = HC['yt']
    WK['yb'] = HC['yb']
    WK['ytau'] = HC['ytau']
    WK['Lambda'] = HC['Lambda']


    return WK
