# ----------------------------------------------------------------------------
#
# TITLE - ChiSquare_Gaussian.py
# PROJECT - 
#
# ----------------------------------------------------------------------------

### Docstrings and metadata:
'''Determine the Chi-Square value for the Gaussian distribution given a fixed 
way of dividing each image.
'''
__author__ = "James Lane"

### Imports
import numpy as np
import sys, os, pdb, glob
from matplotlib import pyplot as plt
from scipy.special import factorial
from scipy.stats import chi2,norm

# Project specific
sys.path.append('../../src/')
import ast2050.lab1

# ----------------------------------------------------------------------------

def divisors(intgr):
	""" Return all divisors of an integer, except 1 and the number itself.
	"""
	divisors = []
	for i in range(1,intgr+1):
		if(intgr%i==0):
			divisors.append(i)
	return divisors[1:-1]
#def

# ----------------------------------------------------------------------------

# Select the image to use
image_list = glob.glob('./XRayImages/image*')[:20]
n_images = len(image_list)

# Get the dark
master_dark = np.load('./masterDark.npy')
master_dark_crop = master_dark[:900,:900]

# Select the number of ways to divide up the image
use_divisors = np.array( divisors(900)[3:-10] )
n_divisors = len(use_divisors)

# Store the p-values
p_values = np.zeros( ( n_divisors, n_images ) )
p_values[:,:] = np.nan # Set a null value

# Loop over each image
for i in range( n_images ):
    
    # Get the image
    data = ast2050.lab1.read_tiff(image_list[i]).astype(float)
    data_crop = data[:900,:900]
    
    # Loop over the divisors for the image
    for j, div in enumerate( use_divisors ):
        
        n_samps = div**2
        n_counts = np.zeros( n_samps )
        splitImage = ast2050.lab1.divideImage(data_crop, xcrop=0, ycrop=0, xnum=div, ynum=div)
        splitDark = ast2050.lab1.divideImage(master_dark_crop, xcrop=0, ycrop=0, xnum=div, ynum=div)
                
        # Loop over the splits and determine the number of counts in each
        for k, split in enumerate(splitImage):
            spe_data, _ = ast2050.lab1.detect_counts(split, dark=splitDark[k])
            n_counts[k] = len(spe_data)
        ###k
        
        # Now make the array for evaluating the Chi Square statistic.
        n_samps = div**2
        max_counts = np.max(n_counts)
        mean_counts = np.mean(n_counts)
        std_counts = np.std(n_counts)
        
        # Determine where the minimum and maximum trailing bins begin. Define 
        # them such that they will contain each ~1/20 of events
        min_trailing_bin = norm.ppf(0.05, loc=mean_counts, scale=std_counts)
        max_trailing_bin = norm.ppf(0.95, loc=mean_counts, scale=std_counts)
        
        # n_gaussian_bins = max( [8,max_trailing_bin-min_trailing_bin] )
        n_gaussian_bins = 10
        if ( max_trailing_bin - min_trailing_bin ) < 10:
            n_gaussian_bins = max_trailing_bin-min_trailing_bin+2
        
        # Split up the space between the minimum and maximum trailing bins 
        # into 8 equally sized bins, making 10 bins total
        bin_edges = np.linspace( min_trailing_bin, max_trailing_bin, num=n_gaussian_bins-1)
        binned_counts = np.empty( len(bin_edges)+1 )
        
        # Determine the probability in each bin
        pcdf = norm.cdf(bin_edges, loc=mean_counts, scale=std_counts)
        binned_gaussian = np.append( pcdf[0], np.append(np.diff(pcdf), 1-pcdf[-1] ) ) * n_samps
        
        # Determine the counts in each bin
        for k in range( len(bin_edges) ):
            if k == 0:
                binned_counts[k] = len( np.where( n_counts <= bin_edges[k] )[0] )
            else:
                binned_counts[k] = len( np.where( (n_counts <= bin_edges[k]) & 
                                                  (n_counts > bin_edges[k-1]) )[0] )
                if k == len(bin_edges)-1:
                    binned_counts[k+1] = len( np.where( n_counts > bin_edges[k] )[0] )
        ###k
        
        # Calculate the Chi Square statistic and the number of degrees of freedom
        chisquare = np.sum( np.divide( np.square( binned_counts - binned_gaussian ), 
                                       binned_gaussian) ) 
        # Number of data classes - number of variables (just mean) - 1
        dof = ( len( bin_edges ) + 1 ) - 2 
        
        # Calculate the p-value, 1-CDF of the Chi Square function
        p_value = 1-chi2.cdf(chisquare,dof)
        p_values[j,i] = p_value 
        
    ###j
    print('Done '+str(i+1)+' of '+str(n_images))
###i

mean_p_value = np.zeros( n_divisors )
mean_p_value[:] = np.nan
std_p_value = np.zeros( n_divisors )
std_p_value[:] = np.nan

for i in range( n_divisors ):
    # Ensure the standard deviation and mean will be meaningful
    if len( np.where( np.isnan( p_values[i,:] ) )[0] ) >= n_images-1: continue
    mean_p_value[i] = np.nanmean( p_values[i,:] )
    std_p_value[i] = np.nanstd( p_values[i,:] )
###i

where_nonan_p = np.where( np.isnan( mean_p_value ) == False )[0]
plot_p_mean = mean_p_value[ where_nonan_p ]
plot_p_std = std_p_value[ where_nonan_p ]
plot_divisors = use_divisors[ where_nonan_p ]
plot_npix = (900/np.array(plot_divisors))**2

fig = plt.figure()
ax = fig.add_subplot(111)
ax.errorbar( np.log10( plot_npix ), plot_p_mean, yerr=plot_p_std, fmt='o', 
            markeredgecolor='Black', markerfacecolor='Black', markersize=5, 
            ecolor='Black', capsize=2.0)
ax.set_ylim(-0.1,1.2)
ax.set_xlabel('log( pixels per sub-image )')
ax.set_ylabel(r'p-value')
ax.axhline(0.0, linestyle='dotted', color='Black', linewidth=1.0)
ax.axhline(1.0, linestyle='dotted', color='Black', linewidth=1.0)

plt.savefig('Gaussian_ChiSquare.pdf')

#