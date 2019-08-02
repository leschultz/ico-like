'''
Store generic fuctions.
'''

from shutil import copyfile
from os.path import join
import os


def copier(source, name, destination):
    '''
    Search for all possible files to copy.

    inputs:
        source = the parent directory of all files
        name = the generic name for files to be copied
        destination = path to save copy of files

    outputs:
        A collection of data files
    '''

    # Get absolute paths
    source = os.path.abspath(source)
    destination = os.path.abspath(destination)

    # Gather common ancestor
    ancestor = os.path.commonprefix([source, destination])

    # Count all mathching paths
    count = 1
    paths = []
    for item in os.walk(source):

        if name not in item[2]:
            continue

        paths.append(os.path.abspath(item[0]))

        count += 1

    count = str(count)

    # Copy files
    newcount = 1
    for path in paths:

        dump = join(destination, path.replace(ancestor, ''))
        if not os.path.exists(dump):
            os.makedirs(dump)

        copyfile(join(path, name), join(dump, name))

        print('Copying '+'('+str(newcount)+'/'+count+'): '+path)

        newcount += 1
