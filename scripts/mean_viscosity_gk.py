'''
Calculate the averages for the Green-Kubo viscosities.
'''

from matplotlib import pyplot as pl
from scipy import constants
from functools import reduce
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

data = []

newcount = 1
for path in runs:

    print('Run ('+str(newcount)+'/'+str(count)+'): '+path)

    param = input_parse(os.path.join(path, runin))

    cols, df = system_parse(os.path.join(path, 'system.txt'))
    df = pd.DataFrame(df, columns=cols)
    df['Time'] = df['TimeStep']*param['timestep']  # Time in [ps]

    # Plot Viscosity vs time
    cols, df = system_parse(os.path.join(path, 'visc.txt'))
    df = pd.DataFrame(df, columns=cols)
    df['Time'] = df['TimeStep']*param['timestep']  # Time in [ps]
    df = df[['Time', 'v_visc']]

    data.append(df)

    newcount += 1

data = reduce(lambda x, y: pd.merge(x, y, on = 'Time'), data)

time = data['Time'].values
time = time-min(time)

viscs = data.loc[:, data.columns != 'Time'].values
visc = np.mean(viscs, axis=1)
std = np.std(viscs, axis=1)
sem = std/(len(std))**0.5

# Create folder for plots viscosity
plotdir = os.path.join(*[runsdir, 'plots', 'viscosity'])
if not os.path.exists(plotdir):
    os.makedirs(plotdir)

fig, ax = pl.subplots()

ax.errorbar(
            time,
            visc,
            std,
            ecolor='r',
            marker='.',
            linestyle='none',
            label='STDEV'
            )

ax.errorbar(
            time,
            visc,
            sem,
            ecolor='y',
            marker='.',
            linestyle='none',
            label='SEM'
            )

ax.legend()
ax.grid()

ax.set_ylabel(r'Shear Viscosity $[Pa \cdot s]$')
ax.set_xlabel('Time [ps]')

fig.tight_layout()
pl.savefig(os.path.join(plotdir, 'viscosity'))
pl.close('all')
