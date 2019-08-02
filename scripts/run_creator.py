'''
Create runs based on a template.
'''

from ast import literal_eval

import numpy as np
import sys
import os

from functions import *

rundir = sys.argv[1]  # Where runs are stored
runs = int(sys.argv[2])  # The number of runs to generate
template = sys.argv[3]  # Template file path
elements = sys.argv[4]  # Elements
potential = sys.argv[5]  # The potential used
potential_type = sys.argv[6]  # The type of potential
types = sys.argv[7]  # The atom id with their type
side = sys.argv[8]  # The length of the cubic simulation box
unit_cell_type = sys.argv[9]  # fcc, hcp, or bcc
lattice_param = sys.argv[10]  # The lattice parameter
timestep = sys.argv[11]  # The timestep
dump_rate = sys.argv[12]  # The rate to dump data
eqhold = sys.argv[13]  # The steps for equilibrium hold
deformhold = sys.argv[14]  # The steps for box deformation
temp = sys.argv[15]  # The simulation temperature
corlength = sys.argv[16]  # The correlation length for the autocorrelation
sampleinterval = sys.argv[17]  # The sample interval

# Open and read template
template_file = open(template)
template_contents = template_file.read()
template_file.close()

runs = np.arange(runs)
runs = ['run_'+str(i) for i in runs]

for run in runs:
    contents = run_creator(
                           template_contents,
                           elements,
                           potential,
                           potential_type,
                           types,
                           side,
                           unit_cell_type,
                           lattice_param,
                           timestep,
                           dump_rate,
                           eqhold,
                           deformhold,
                           temp,
                           corlength,
                           sampleinterval,
                           )

    # Write the input file
    path = os.path.join(rundir, run)

    if not os.path.exists(path):
        os.makedirs(path)

    file_out = open(join(path, template.split('/')[-1]), 'w')
    file_out.write(contents)
    file_out.close()
