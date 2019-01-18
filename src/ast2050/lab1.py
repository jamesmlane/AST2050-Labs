# ----------------------------------------------------------------------------
#
# TITLE - lab1.py
# PROJECT - AST 2050
# CONTENTS:
#
# ----------------------------------------------------------------------------

### Docstrings and metadata:
'''Functions for Lab 1 of AST 2050

Import me by including this at the beginning of the script:
sys.path.append('path/to/src/')
import ast2050.lab1
'''

### Imports

## Basic
import numpy as np
import sys, os, pdb
# import copy
# import glob
# import subprocess

# Imaging
from PIL import Image

## Plotting
from matplotlib import pyplot as plt


# ----------------------------------------------------------------------------

def read_tiff(filename):
    '''read_tiff:
    
    Read a .tiff file and return a numpy array
    
    Args:
        filename (string) - File name (with .tiff ending)
    
    Returns:
        image (float array) - Image as a numpy array
    '''
    return np.array( Image.open( filename ) )
#def

# ----------------------------------------------------------------------------

def single_pixel_center_difference(image):
    '''single_pixel_center_difference:
    
    For each pixel subtract the 8 surrounding pixels from the central pixel.
    Return a map of the same size but with this metric calculated.
    
    Args:
        image (float array) - Input image
        
    Returns:
        metric (float array) - Single pixel detection metric array
    '''
    
    # Shape arrays and output array.
    lenx, leny = image.shape
    metric = np.zeros_like(image)
    
    # Double loop over each pixel.
    for i in range( lenx ):
        for j in range( leny ):
            
            # Continue if an edge pixel
            if i==0 or i==(lenx-1) or j==0 or j==(leny-1): continue
            
            # Subtract the pixels around the point 
            metric[i,j] = 2*image[i,j] - np.sum(image[(i-1):(i+2),(j-1):(j+2)])
        ###j
    ###i
    
    return metric
    
#def