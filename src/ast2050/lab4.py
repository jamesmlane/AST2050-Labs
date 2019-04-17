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

## Scipy
from scipy import optimize


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

def _gaussian_function(x,A,x0,sigma,offset):
    '''_gaussian_function
    
    Function for use fitting the spine of the data
    
    
    '''
    return A*np.exp( -np.square(x-x0)/(2*sigma**2) ) + offset
#def
    
# ----------------------------------------------------------------------------

def _linear_function(x,m,b):
    '''_linear_function
    
    Function used to fit the column gaussian means
    
    
    '''
    return m*x+b
#def

# ----------------------------------------------------------------------------

def determine_spectrum_linear_spine(data, threshold, slice_array=None):
    '''determine_spectrum_linear_spine:
    
    Determine a best-fitting linear spine for a spectrum. Examine each column 
    of pixels and find the gaussian means of each group of pixels, then fit a 
    linear form to the sample of means, weighted by the error in the mean fit.
    
    Args:
        data (2D array) - 2D image data. The index will be for rows, and the 
            second for columns. This means that data[:,N] will select the Nth 
            column
        threshold (float) - Value below which data will not be considered
        slice_array (4 element list) - An array of [min1,max1,min2,max2] for 
            slicing dimensions 1 and 2, like [min1:max1,min2:max2]
        
    Output:
        linear_params (2 element list) - 2 element list of slope and y intercept 
            of the best-fitting linear profile to the spine of the spectrum.
    
    '''
    
    assert len(slice_array) == 4
    
    # First slice n dice the array
    data = data[ slice_array[0]:slice_array[1], slice_array[2]:slice_array[3] ]
    
    # Figure out the number of columns, make the data arrays
    n_cols = data.shape[1]
    mean_sample = np.zeros( n_cols )
    mean_error_sample = np.zeros( n_cols )
    
    # First, zero out all the data which doesn't reach the threshold value
    where_data_below_thresh = np.where( data < threshold )
    data[ where_data_below_thresh ] = 0
    
    # Loop over all columns
    for i in range( n_cols ):
        
        # For each column, get the data, fit the gaussian
        col_data = data[:,i]
        row_indexes = np.arange( slice_array[0], slice_array[1], 1.0 )
        p0 = [  np.max(col_data)-np.mean(col_data),
                np.argmax(col_data)+slice_array[0],
                3,
                np.mean(col_data)
             ]
        popt, pcov = optimize.curve_fit(_gaussian_function, row_indexes, 
            col_data, p0=p0, sigma=None)
        mean_sample[i] = popt[1]
        mean_error_sample[i] = np.sqrt(pcov[1,1])
        
        if i%10 != 0: continue
        
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot( row_indexes, col_data, color='Blue' )
        ax.plot( row_indexes, _gaussian_function(row_indexes, *popt), color='Red' )
        fig.savefig('test'+str(i)+'.png', dpi=200)
        plt.close('all')
    ###i
    
    col_indexes = np.arange(slice_array[2],slice_array[3],1.0)
    
    # return mean_sample+slice_array[0], mean_error_sample, col_indexes
    
    popt,pcov = optimize.curve_fit( _linear_function, col_indexes,
        mean_sample+slice_array[0] )
    
    return popt
#def













