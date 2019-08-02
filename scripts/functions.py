from ast import literal_eval
from os.path import join
import numpy as np
import random


def run_creator(
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
                vischold,
                temp,
                corlength,
                sampleinterval,
                ):
    '''
    Generate a LAMMPS input file
    '''

    # Random number used by LAMMPS
    seed = random.randint(0, 9999999)

    # The number of atoms to simulate
    natoms = str(len(elements.split(' ')))

    # The types of atoms
    types = literal_eval(types)
    count = 1
    atom_types = ''
    for i in types:
        atom_types += 'set atom '+str(i[0])+'*'+str(i[1])+' type '+str(count)+'\n'
        count += 1

    # Replace keywords within a template document
    contents = template_contents
    contents = contents.replace('#replace_elements#', elements)
    contents = contents.replace('#replace_natoms#', natoms)
    contents = contents.replace('#replace_potential#', join('..', potential))
    contents = contents.replace('#replace_potential_type#', potential_type)
    contents = contents.replace('#replace_side#', side)
    contents = contents.replace('#replace_unit_cell_type#', unit_cell_type)
    contents = contents.replace('#replace_types#', atom_types)
    contents = contents.replace('#replace_lattice_param#', lattice_param)
    contents = contents.replace('#replace_timestep#', timestep)
    contents = contents.replace('#replace_dumprate#', dump_rate)
    contents = contents.replace('#replace_eqhold#', eqhold)
    contents = contents.replace('#replace_vischold#', vischold)
    contents = contents.replace('#replace_holdtemp#', temp)
    contents = contents.replace('#replace_seed#', str(seed))
    contents = contents.replace('#replace_corlength#', corlength)
    contents = contents.replace('#replace_sampleinterval#', sampleinterval)


    return contents


def input_parse(infile):
    '''
    Parse the input file for important parameters

    inputs:
        infile = The name and path of the input file
    outputs:
        param = Dictionary containing run paramters
    '''

    with open(infile) as f:
        for line in f:

            line = line.strip().split(' ')

            if 'units' in line:
                units = line[-1]

            if 'pair_coeff' in line:
                line = [i for i in line if i != '']
                elements = line[4:]

            if ('holdtemp' in line) and ('variable' in line):
                line = [i for i in line if i != '']
                temperature = float(line[-1])

            if 'eqhold' in line:
                eqhold = int(line[-1])

            if 'vischold' in line:
                vischold = int(line[-1])

            if 'mytimestep' in line:
                timestep = float(line[-1])

    param = {
             'units': units,
             'eqhold': eqhold,
             'vischold': vischold,
             'elements': elements,
             'temperatures': temperature,
             'timestep': timestep
             }

    return param


def system_parse(sysfile):
    '''
    Parse the thermodynamic data file

    inputs:
        sysfile = The name and path of the thermodynamic data file
    outputs:
        columns = The columns for the data
        data = The data from the file
    '''

    data = []
    with open(sysfile) as f:
        line = next(f)
        for line in f:

            if '#' in line:
                values = line.strip().split(' ')
                columns = values[1:]

            else:
                values = line.strip().split(' ')
                values = list(map(literal_eval, values))
                data.append(values)

    return columns, data

def correlation(x, k):
    '''
    Calculate the autocorrelation function.

    inputs:
        x = The set of data
        k = The interval between datapoints (k-lag)
    outputs:
        c = The autocrrelation
    '''

    n = len(x)

    c = 0.0
    for i in np.arange(0, n-k):
        c += x[i+k]*x[i]

    c /= n-k

    return c
