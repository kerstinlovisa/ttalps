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

# p['PI'] = math.p['PI']
I3 = np.identity(3)
I2 = np.identity(2)

Qu=2/3
Qe=-1
Qd=-1/3
Qnu=0

# beta3 = 0
# betaem = 0
# aEM = params.aEM

def Low_RGE(mu, MK, loop_order, n_charged_fermions):
    #QCD beta func taken from 1604.08082

    beta = OrderedDict()

    beta['U']=np.array([[0.+0j,0.+0j],[0.+0j,0.+0j]])
    beta['u']=np.array([[0.+0j,0.+0j],[0.+0j,0.+0j]])
    beta['D']=np.array([[0.+0j,0.+0j,0.+0j],[0.+0j,0.+0j,0.+0j],[0.+0j,0.+0j,0.+0j]])
    beta['d']=np.array([[0.+0j,0.+0j,0.+0j],[0.+0j,0.+0j,0.+0j],[0.+0j,0.+0j,0.+0j]])
    beta['E']=np.array([[0.+0j,0.+0j,0.+0j],[0.+0j,0.+0j,0.+0j],[0.+0j,0.+0j,0.+0j]])
    beta['e']=np.array([[0.+0j,0.+0j,0.+0j],[0.+0j,0.+0j,0.+0j],[0.+0j,0.+0j,0.+0j]])
    beta['nu']=np.array([[0.+0j,0.+0j,0.+0j],[0.+0j,0.+0j,0.+0j],[0.+0j,0.+0j,0.+0j]])
    beta['GG']=0+0j
    beta['gamgam']=0+0j
    beta['aEM']=0+0j
    beta['a3']=0+0j

    nC=3 #number of colours

    #default values for n_charged_fermions = 8
    nCf=5 # number of fermions with colour charge
    nu=2 #number of dynamical up-type quarks
    nd=3 #number of dynamical down-type quarks
    ne=3 #number of dynamical charged leptons

    Ie=I3 #identity for charged leptons
    Iu=I2 #identity for up-type quarks
    Id=I3 #identity for down-type quarks

    # cggloop=1./2.*(np.trace(MK['u']-MK['U'])+np.trace(MK['d']-MK['D']))
    # cgamgamloop=(nC*Qu**2*np.trace(MK['u']-MK['U'])+nC*Qd**2*np.trace(MK['d']-MK['D'])+Qe**2*np.trace(MK['e']-MK['E']))
    # print(MK['aEM'])
    if n_charged_fermions<7.5:
        nCf=4
        nd=2
        Id=I2
        beta['D']=np.array([[0.+0j,0.+0j],[0.+0j,0.+0j]])
        beta['d']=np.array([[0.+0j,0.+0j],[0.+0j,0.+0j]])
    if n_charged_fermions<6.5:
        ne=2
        Ie=I2
        beta['E']=np.array([[0.+0j,0.+0j],[0.+0j,0.+0j]])
        beta['e']=np.array([[0.+0j,0.+0j],[0.+0j,0.+0j]])

    if n_charged_fermions<5.5:
        nCf=3
        nu=1
        Iu=1
        beta['U']=0.+0j
        beta['u']=0.+0j
        cggloop=1./2.*((MK['u']-MK['U'])+np.trace(MK['d']-MK['D']))
        cgamgamloop=(nC*Qu**2*(MK['u']-MK['U'])+nC*Qd**2*np.trace(MK['d']-MK['D'])+Qe**2*np.trace(MK['e']-MK['E']))
    else:
        cggloop=1./2.*(np.trace(MK['u']-MK['U'])+np.trace(MK['d']-MK['D']))
        cgamgamloop=(nC*Qu**2*np.trace(MK['u']-MK['U'])+nC*Qd**2*np.trace(MK['d']-MK['D'])+Qe**2*np.trace(MK['e']-MK['E']))

    if loop_order >= 1:
        beta['e'] +=  Ie * 3 * (MK['aEM'])**2/ (4 * p['PI']**2) * MK['gamgam']
        beta['E'] += -Ie * 3 * (MK['aEM']) ** 2 / (4 * p['PI'] ** 2) * MK['gamgam'] 
        beta['u'] +=  Iu * (MK['a3'] ** 2 / p['PI'] ** 2 * MK['GG'] + 3 * (MK['aEM']) ** 2 / (4 * p['PI'] ** 2) * Qu ** 2 * MK['gamgam'])
        beta['U'] += -Iu * (MK['a3'] ** 2 / p['PI'] ** 2 * MK['GG'] + 3 * (MK['aEM']) ** 2 / (4 * p['PI'] ** 2) * Qu ** 2 * MK['gamgam']) 
        beta['d'] +=  Id * (MK['a3'] ** 2 / p['PI'] ** 2 * MK['GG'] + 3 * (MK['aEM']) ** 2 / (4 * p['PI'] ** 2) * Qd ** 2 * MK['gamgam']) 
        beta['D'] += -Id * (MK['a3'] ** 2 / p['PI'] ** 2 * MK['GG'] + 3 * (MK['aEM']) ** 2 / (4 * p['PI'] ** 2) * Qd ** 2 * MK['gamgam'])
        beta['a3'] +=  - MK['a3']**2  / (2 * p['PI']) * (11 - 2/3*nCf)
        beta['aEM'] +=   MK['aEM']**2 / (2 * p['PI']) * 4/3*(nu*nC*Qu**2+nd*nC*Qd**2+ne*Qe**2)

    if loop_order >= 2:

        beta['e'] +=  Ie * 3 * (MK['aEM']) ** 2 / (4 * p['PI'] ** 2) * cgamgamloop
        beta['E'] += -Ie * 3 * (MK['aEM']) ** 2 / (4 * p['PI'] ** 2) * cgamgamloop
        beta['u'] +=  Iu * (MK['a3'] ** 2 / p['PI'] ** 2 * cggloop + 3 * (MK['aEM']) ** 2 / (4 * p['PI'] ** 2) * Qu ** 2 * cgamgamloop)
        beta['U'] += -Iu * (MK['a3'] ** 2 / p['PI'] ** 2 * cggloop + 3 * (MK['aEM']) ** 2 / (4 * p['PI'] ** 2) * Qu ** 2 * cgamgamloop)
        beta['d'] +=  Id * (MK['a3'] ** 2 / p['PI'] ** 2 * cggloop + 3 * (MK['aEM']) ** 2 / (4 * p['PI'] ** 2) * Qd ** 2 * cgamgamloop)
        beta['D'] += -Id * (MK['a3'] ** 2 / p['PI'] ** 2 * cggloop + 3 * (MK['aEM']) ** 2 / (4 * p['PI'] ** 2) * Qd ** 2 * cgamgamloop)
        beta['a3'] += - 2*(MK['a3'])**3 / (4 * p['PI'])**2 * (102 - 38 / 3 * nCf) #check this expression
        beta['aEM'] += 0

    beta['U']=beta['U']/mu
    beta['u']=beta['u']/mu
    beta['D']=beta['D']/mu
    beta['d']=beta['d']/mu
    beta['E']=beta['E']/mu
    beta['e']=beta['e']/mu
    beta['nu']=beta['nu']/mu
    beta['aEM']=beta['aEM']/mu
    beta['a3']=beta['a3']/mu

    return beta

def Low_RGE_array8(mu, MKa, loop_order,n_charged_fermions):
    MKd=tools.array2dict8(MKa)
    beta=Low_RGE(mu, MKd, loop_order,n_charged_fermions)
    return tools.dict2array8(beta)

def Low_RGE_array7(mu, MKa, loop_order,n_charged_fermions):
    MKd=tools.array2dict7(MKa)
    beta=Low_RGE(mu, MKd, loop_order,n_charged_fermions)
    return tools.dict2array7(beta)

def Low_RGE_array6(mu, MKa, loop_order,n_charged_fermions):
    MKd=tools.array2dict6(MKa)
    beta=Low_RGE(mu, MKd, loop_order,n_charged_fermions)
    return tools.dict2array6(beta)

def Low_RGE_array5(mu, MKa, loop_order,n_charged_fermions):
    MKd=tools.array2dict5(MKa)
    beta=Low_RGE(mu, MKd, loop_order,n_charged_fermions)
    return tools.dict2array5(beta)

    