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
import sys, os, pdb, re
import glob

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

# ----------------------------------------------------------------------------

def detect_counts(data, dark=None, threshold_metric=100., threshold_spe=100.):
    '''detect_counts:
    
    Take a data and a dark frame (optional), perform background subtraction and 
    then detect single pixel events using the single_pixel_center_difference 
    metric. 
    
    Args:
        data (float array) - Data array
        dark (float array) - Dark array. If None then data is already 
            background subtracted. [None]
        threshold_metric (float) - The threshold to consider a point for 
            calculation of the metric (saves time so you don't calculate the 
            metric on pixels with low numbers of counts) [100.]
        threshold_spe (float) - The threshold of the metric function to count 
            something as a single pixel event. [100.]
    Returns:
        spe_data (float array) - Array of single pixel event count numbers
        where_spe (float array) - Array of single pixel event locations (xs,ys)
    '''
    
    # Background subtraction
    if type(dark) != type(None):
        data -= dark
    ##fi
    
    # Calculate the metric and determine where single pixel events are.
    metric = single_pixel_center_difference(data,threshold=threshold_metric)
    where_spe = np.where(metric > threshold_spe)
    spe_data = data[where_spe]
    
    return spe_data, where_spe
# def

# ----------------------------------------------------------------------------
    
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

def divideImage(image, xcrop=0, ycrop=0, xnum=4, ynum=4):
    """ Divides an image into subimages.

    Parameters
    ----------
    image: ndarray
        array to divide into subimages
    xcrop, ycrop: int
    	value at which to crop the image, in case it won't divide evenly
    xnum, ynum: int
        number of images to divide along an axis

    Returns
    ----------
    images: list
        list containing an array for each subimage
    """
    image = image[xcrop:,ycrop:]
    images = []
    splitX = np.split(image, xnum)
    splitXY = [np.split(splitX[i], ynum, axis=1) for i in range(ynum)]
    for i in splitXY:
        for j in i:
            images.append(np.asarray(j, dtype='float'))
    return images

# ----------------------------------------------------------------------------

def sort_nicely(l):
    '''sort_nicely:

    Sort a bunch of files as a human would rather than how a dumb computer
    would
    
    Use as: 
    >> list = [things,more,things]
    >> ast2050.lab1.sort_nicely(list)
    >> # List is now sorted

    Args:
        l (str array) - array of filenames to sort

    Returns:
        s - sorted array of
    '''
    def tryint(s):
            try:
                    return int(s)
            except:
                    return s
    #def
    def alphanum_key(s):
            return [ tryint(c) for c in re.split('([0-9]+)', s) ]
    #def
    l.sort(key=alphanum_key)
#def

# ----------------------------------------------------------------------------














