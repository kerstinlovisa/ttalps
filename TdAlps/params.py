import numpy as np
import math
"""Here we define the relevant parameters"""
from collections import OrderedDict

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



















