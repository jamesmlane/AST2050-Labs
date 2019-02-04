# ----------------------------------------------------------------------------
#
# TITLE - background_subtraction.py
# PROJECT - AST 2050
#
# ----------------------------------------------------------------------------

### Docstrings and metadata:
'''Perform background subtraction on each image of the X-ray source using the 
corresponding flat.
'''
__author__ = "James Lane"

### Imports

## Basic
import numpy as np
import sys, os, pdb, glob

## Plotting
from matplotlib import pyplot as plt

## Project-specific import
sys.path.append('../../src/')
import ast2050.lab1 as lab1

# ----------------------------------------------------------------------------

# Filenames
file_dir = 'MasterDark/'
filenames = glob.glob(file_dir+'*.tiff')

# ----------------------------------------------------------------------------

# First read in all the images


for i in range( len(dark_file_names) ):
    
    # Make the background subtracted image
    dark_image = lab1.read_tiff( dark_file_names[i] )
    data_image = lab1.read_tiff( data_file_names[i] )
    
    print('flat: '+dark_file_names[i]+' and data:'+data_file_names[i])

###i


# Make a figure
fig = plt.figure()
ax = fig.add_subplot(111)
ax.imshow(img_median)
fig.savefig(data_file_names[i][:-6]+'_bsub'+str(i+1)+'.pdf')

