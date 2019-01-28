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
import glob
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

def single_pixel_center_difference(image,threshold=0.):
    '''single_pixel_center_difference:
    
    For each pixel subtract the 8 surrounding pixels from the central pixel.
    Return a map of the same size but with this metric calculated.
    
    Args:
        image (float array) - Input image
        threshold (float) - The threshold below which the metric will not be 
            computed
        
    Returns:
        metric (float array) - Single pixel detection metric array
    '''
    
    # Shape arrays and output array.
    lenx,leny = image.shape
    metric = np.zeros_like(image)
    
    # Determine where to look
    xs, ys = np.where( image > threshold )
    npix = len( xs )
    
    for i in range( npix ):
        
        indx = xs[i]
        indy = ys[i]
        
        # Continue if an edge pixel
        if indx == 0 or indx == (lenx-1) or indy == 0 or indy == (leny-1): 
            continue
        ##fi
        
        # Calculate the metric
        metric[indx,indy] = 2*image[indx,indy] - \
                            np.sum(image[(indx-1):(indx+2),(indy-1):(indy+2)]) 
                            
    ###i
    
    return metric
    
def masterDark(path_to_darks, ax1 = 964, ax2 = 1288):
    """ Combines darks and takes the median of each pixel to make a master dark.

    Parameters
    ----------
    path_to_darks: str
        path to where the dark .tiff files are stored
    ax1: float
        first axis of the dark array; will probably always be the same
    ax2: float
        second axis of the dark array; will probably always be the same

    Returns
    ----------
    """
    darks = glob.glob(path_to_darks+'*.tiff')
    master = np.empty((len(darks), ax1, ax2))
    for idx, dark in enumerate(darks):
        master[idx,:,:] = read_tiff(dark)
    master_dark = np.median(master, axis=0) # take the median across the pixel axis
    return master_dark

def divideImage(image, num=4):
    """ Divides an image into subimages.

    Parameters
    ----------
    image: ndarray
        array to divide into subimages
    num: int
        number of images to divide along an axis

    Returns
    ----------
    images: list
        list containing an array for each subimage
    """
    images = []
    splitX = np.split(image, num)
    splitXY = [np.split(splitX[i], num, axis=1) for i in range(num)]
    for i in splitXY:
        for j in i:
            images.append(j)
    return images





















