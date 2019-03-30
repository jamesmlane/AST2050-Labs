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

sys.path.append('../src/')
import ast2050.lab3 as lab3

# ----------------------------------------------------------------------------

# Keywords
chunk_size = int(1E6)
sample_rate = 20.E6
lof = 1.42E9

dir = '../Data/March21/'
filenames = [   'background_1',
                'background_2',
                'background_3',
                'background_4',
                'l_014',
                'l_095',
                'l_132',
                'l_151',
                'l_170',
                'l_180',
                'l_190',
                'l_200',
                'l_210',
                'l_220',
                'l_230']

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


