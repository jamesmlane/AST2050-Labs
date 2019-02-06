# ----------------------------------------------------------------------------
#
# TITLE - DarkCurrent.py
# PROJECT - AST 2050
#
# ----------------------------------------------------------------------------

### Docstrings and metadata:
'''Examine the dark current as a function of time
'''
__author__ = "James Lane"

### Imports
import numpy as np
import sys, os, pdb, glob
from matplotlib import pyplot as plt
from scipy.special import factorial
from scipy.stats import chi2

# Project specific
sys.path.append('../../src/')
import ast2050.lab1

# ----------------------------------------------------------------------------

# Read in the images
image_list = glob.glob('./timeIncrease/*.tiff')
ast2050.lab1.sort_nicely(image_list)

# Make the times
times = np.arange(0.5,30.5,0.5)
n_times = len(times)
means = np.zeros_like(times)
means_norm = np.zeros_like(times)

# Read in the dark
master_dark = np.load('./masterDark.npy')

# Loop over the different images and plot the average as a function of time
for i in range( n_times ):
    
    data = ast2050.lab1.read_tiff(image_list[i]).astype(float)
    data_norm = np.divide( data, master_dark )
    data_norm[ np.where( np.isinf( data_norm ) ) ] = np.nan
    
    means[i] = np.mean(data)
    means_norm[i] = np.nanmean( data_norm )
    
###i

fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter( times, means, s=1, facecolor='Red', edgecolor='None')
ax.scatter( times, means_norm, s=1, facecolor='Blue', edgecolor='None')
ax.set_xlabel('Exposure Time (s)')
ax.set_ylabel('Mean Counts')

plt.show()

# ----------------------------------------------------------------------------
