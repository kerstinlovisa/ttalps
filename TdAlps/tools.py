import math
import matplotlib.pyplot as plt
import numpy as np
import sys
from collections import OrderedDict

coeffs = ['Q','u','d','L','e','GG','WW','BB','a1','a2','a3','yt','yb','ytau','Lambda']
coeffs8 = ['U','u','D','d','E','e','nu','GG','gamgam','aEM','a3']
coeffs7 = ['U','u','D','d','E','e','nu','GG','gamgam','aEM','a3']
coeffs6 = ['U','u','D','d','E','e','nu','GG','gamgam','aEM','a3']
coeffs5 = ['U','u','D','d','E','e','nu','GG','gamgam','aEM','a3']
coeffs4 = ['U','u','D','d','E','e','nu','GG','gamgam','aEM','a3']
coeffs3 = ['U','u','D','d','E','e','nu','GG','gamgam','aEM','a3']
coeffs2 = ['U','u','E','e','nu','GG','gamgam','aEM','a3']
coeffs1 = ['E','e','nu','GG','gamgam','aEM','a3']
coeffs0 = ['nu','GG','gamgam','aEM','a3']
coeffsSM = ['a1','a2','a3','yt','yb','ytau','Lambda']

coeffMat = {
    'Q' : 'M',
    'u' : 'M',
    'd' : 'M',
    'L' : 'M',
    'e' : 'M',
    'GG' : 'S',
    'WW' : 'S',
    'BB' : 'S',
    'a1' : 'S',
    'a2' : 'S',
    'a3' : 'S',
    'yt' : 'S',
    'yb' : 'S',
    'ytau' : 'S',
    'Lambda' : 'S'
}

coeffMat8 = {
    'U' : 'M2',
    'u' : 'M2',
    'D' : 'M',
    'd' : 'M',
    'E' : 'M',
    'e' : 'M',
    'nu' : 'M',
    'GG' : 'S',
    'gamgam' : 'S',
    'aEM' : 'S',
    'a3' : 'S'
}
coeffMat7 = {
    'U' : 'M2',
    'u' : 'M2',
    'D' : 'M2',
    'd' : 'M2',
    'E' : 'M',
    'e' : 'M',
    'nu' : 'M',
    'GG' : 'S',
    'gamgam' : 'S',
    'aEM' : 'S',
    'a3' : 'S'
}
coeffMat6 = {
    'U' : 'M2',
    'u' : 'M2',
    'D' : 'M2',
    'd' : 'M2',
    'E' : 'M2',
    'e' : 'M2',
    'nu' : 'M',
    'GG' : 'S',
    'gamgam' : 'S',
    'aEM' : 'S',
    'a3' : 'S'
}

coeffMat5 = {
    'U' : 'S',
    'u' : 'S',
    'D' : 'M2',
    'd' : 'M2',
    'E' : 'M2',
    'e' : 'M2',
    'nu' : 'M',
    'GG' : 'S',
    'gamgam' : 'S',
    'aEM' : 'S',
    'a3' : 'S'
}


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

def dict2array(D):
    return np.hstack([np.asarray(D[c]).ravel() for c in coeffs])


def array2dict8(A):
    D = OrderedDict()
    i=0
    for c in coeffs8:
        mat = coeffMat8[c]
        if mat == 'S':
            j = i+1
            D[c] = A[i]
        if mat == 'M':
            j = i + 9 
            D[c] = A[i:j].reshape((3,3))
        if mat == 'M2':
            j = i + 4 
            D[c] = A[i:j].reshape((2,2))
        i = j
    return D

def dict2array8(D):
    return np.hstack([np.asarray(D[c]).ravel() for c in coeffs8])

def array2dict7(A):
    D = OrderedDict()
    i=0
    for c in coeffs7:
        mat = coeffMat7[c]
        if mat == 'S':
            j = i+1
            D[c] = A[i]
        if mat == 'M':
            j = i + 9 
            D[c] = A[i:j].reshape((3,3))
        if mat == 'M2':
            j = i + 4 
            D[c] = A[i:j].reshape((2,2))
        i = j
    return D

def dict2array7(D):
    return np.hstack([np.asarray(D[c]).ravel() for c in coeffs7])


def array2dict6(A):
    D = OrderedDict()
    i=0
    for c in coeffs6:
        mat = coeffMat6[c]
        if mat == 'S':
            j = i+1
            D[c] = A[i]
        if mat == 'M':
            j = i + 9 
            D[c] = A[i:j].reshape((3,3))
        if mat == 'M2':
            j = i + 4 
            D[c] = A[i:j].reshape((2,2))
        i = j
    return D

def dict2array6(D):
    return np.hstack([np.asarray(D[c]).ravel() for c in coeffs6])

def array2dict5(A):
    D = OrderedDict()
    i=0
    for c in coeffs5:
        mat = coeffMat5[c]
        if mat == 'S':
            j = i+1
            D[c] = A[i]
        if mat == 'M':
            j = i + 9 
            D[c] = A[i:j].reshape((3,3))
        if mat == 'M2':
            j = i + 4 
            D[c] = A[i:j].reshape((2,2))
        i = j
    return D

def dict2array5(D):
    return np.hstack([np.asarray(D[c]).ravel() for c in coeffs5])





def array2dictSM(A):
    D = OrderedDict()
    i=0
    for c in coeffsSM:
        j = i+1
        D[c] = A[i]
        i = j
    return D

def dict2arraySM(D):
    return np.hstack([np.asarray(D[c]).ravel() for c in coeffsSM])








