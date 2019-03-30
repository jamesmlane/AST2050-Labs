# ----------------------------------------------------------------------------
#
# TITLE - galactic_plane_power.py
# AUTHOR - James Lane
#
# ----------------------------------------------------------------------------

### Docstrings and metadata:
'''Calculate the power and frequency for all galactic plane pointings and 
backgrounds
'''
__author__ = "James Lane"

### Imports

## Basic
import numpy as np
import sys, os, pdb, time

## Plotting
from matplotlib import pyplot as plt

sys.path.append('../../src/')
import ast2050.lab3 as lab3

# ----------------------------------------------------------------------------

# Keywords
chunk_size = int(1E6)
sample_rate = 20.E6
lof = 1.42E9

dir = '../Data/March26/'
# filenames = [   'sun1',
#                 'sun2',
#                 'sun3']

filenames = [   'sun_H1',
                'sun_H2',
                'sun_H3',
                'sun_off1.dat',
                'sun_off2.dat']

n_files = len(filenames)

# ----------------------------------------------------------------------------

chunk_size = int(1E6)

for i in range( n_files ):
     
    data = lab3.read_airspy_data(dir+filenames[i]+'.dat')
    t1 = time.time()
    freq, power = lab3.calculate_power(data, chunk_size=chunk_size, 
                                        sample_rate=sample_rate, lof=lof)
    t2 = time.time()
    print(str(t2-t1)+' sec')
    output = np.array([freq,power])
    np.save('./data_place/'+filenames[i]+'_power_freqs.npy', output)
###i


