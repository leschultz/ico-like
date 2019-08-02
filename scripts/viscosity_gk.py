'''
Use the Green-Kubo formalism to compute viscosity based on the
off diagonal components of the pressure tensor.
'''

from matplotlib import pyplot as pl
from scipy import constants
from functions import *

import pandas as pd
import numpy as np

import sys
import os

runsdir = sys.argv[1]  # The path to the run set
runin = sys.argv[2]  # The name for the input file

# Count the available runs
runs = []
count = 0
for path, subdir, files in os.walk(runsdir):

    if 'system.txt' not in files:
        continue
    if runin not in files:
        continue

    runs.append(path)
    count += 1

newcount = 1
for path in runs:

    print('Run ('+str(newcount)+'/'+str(count)+'): '+path)

    param = input_parse(os.path.join(path, runin))

    cols, df = system_parse(os.path.join(path, 'system.txt'))
    df = pd.DataFrame(df, columns=cols)
    df['Time'] = df['TimeStep']*param['timestep']  # Time in [ps]

    # Settled data
    dfset = df[df['TimeStep'] > param['eqhold']]

    time = dfset['Time'].values
    pxy = dfset['v_pxy'].values
    pxz = dfset['v_pxz'].values
    pyz = dfset['v_pyz'].values

    # Variables outside of GK integral
    vol = dfset['v_vol'].mean()
    temp = dfset['c_temp'].mean()
    k = constants.value('Boltzmann constant in eV/K')

    # Variables  within GK integral    
    time = dfset['Time'].values
    pxy = dfset['v_pxy'].values
    pxz = dfset['v_pxz'].values
    pyz = dfset['v_pyz'].values

    # Autocorrelation function
    print(np.mean([pxy[0]*i for i in pxy]))
    print(dfset)
    print(temp)
    print(k)

    k = np.arange(0, len(pxy))  # k-lag
    r = list(map(lambda lag: correlation(pxy, lag), k))

    print(r)
    pl.plot(r)
    pl.show()

    newcount += 1
