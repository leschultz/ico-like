'''
Plot all thermodynamic variables as a function of time for equillibration and
data gathering portions.
'''

from matplotlib import pyplot as pl
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

    # Gather thermodynamic data
    cols, df = system_parse(os.path.join(path, 'system.txt'))
    df = pd.DataFrame(df, columns=cols)
    df['Time'] = df['TimeStep']*param['timestep']  # Time in [ps]

    # Equilibrium data
    dfeq = df[df['TimeStep'] <= param['eqhold']]

    # Settled data
    dfset = df[df['TimeStep'] > param['eqhold']]

    # Create folder for plots thermodynamic data
    plotdir = os.path.join(*[path, 'plots', 'thermodynamic'])
    if not os.path.exists(plotdir):
        os.makedirs(plotdir)

    # Start plotting thermodynamic data vs time
    xeq = dfeq['Time'].values
    xset = dfset['Time'].values
    for col in df.columns:

        # Skip time values
        if ('TimeStep' == col) or ('Time' == col):
            continue

        yeq = dfeq[col].values
        yset = dfset[col].values

        splitcol = col.split('_')[-1]

        # Equilibrium plot
        figeq, axeq = pl.subplots()

        axeq.plot(xeq, yeq, label='Equilibrium', marker='.', linestyle='none')
        axeq.legend()
        axeq.grid()

        axeq.set_ylabel(splitcol+' in '+param['units']+' units')
        axeq.set_xlabel('Time [ps]')

        figeq.tight_layout()
        pl.savefig(os.path.join(plotdir, 'equilibrium_'+splitcol))
        pl.close('all')

        # Settled plot
        figset, axset = pl.subplots()

        axset.plot(xset, yset, label='Data Gathering', marker='.', linestyle='none')
        axset.legend()
        axset.grid()

        axset.set_ylabel(splitcol+' in '+param['units']+' units')
        axset.set_xlabel('Time [ps]')

        figset.tight_layout()
        pl.savefig(os.path.join(plotdir, 'data_gathering_'+splitcol))
        pl.close('all')

    # Create folder for plots viscosity
    plotdir = os.path.join(*[path, 'plots', 'viscosity'])
    if not os.path.exists(plotdir):
        os.makedirs(plotdir)

    # Plot Viscosity vs time
    cols, df = system_parse(os.path.join(path, 'visc.txt'))
    df = pd.DataFrame(df, columns=cols)
    df['Time'] = df['TimeStep']*param['timestep']  # Time in [ps]

    fig, ax = pl.subplots()

    ax.plot(
            df['Time']-min(df['Time']),
            df['v_visc'],
            marker='.',
            linestyle='none'
            )

    ax.grid()

    ax.set_ylabel(r'Shear Viscosity $[Pa \cdot s]$')
    ax.set_xlabel('Time [ps]')

    fig.tight_layout()
    pl.savefig(os.path.join(plotdir, 'viscosity'))
    pl.close('all')

    newcount += 1
