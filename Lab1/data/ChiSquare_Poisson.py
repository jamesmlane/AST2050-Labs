# ----------------------------------------------------------------------------
#
# TITLE - ChiSquare_Poisson.py
# PROJECT - 
#
# ----------------------------------------------------------------------------

### Docstrings and metadata:
'''Determine the Chi-Square value for the Poisson distribution given a fixed 
way of dividing each image.
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

def PoissonDist(mu, x):
	""" Returns a Poisson distriubtion.

	Parameters
	----------
	mu: float
		mean
	x: array
		array of interger x values to put into the Poisson distribution

	Returns
	----------
	y: array
		poission distribution
	"""
	y = ((mu**x)/factorial(x))*np.exp(-1.*mu)
	return y
#def

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
image_list = glob.glob('./XRayImages/image*')
n_images = len(image_list)

# Get the dark
master_dark = np.load('./masterDark.npy')
master_dark_crop = master_dark[:900,:900]

data = ast2050.lab1.read_tiff(image_list[3]).astype(float)
data_crop = data[:900,:900]

# Store the p-values
p_values = []

use_divisors = divisors(900)[:]

# Loop over the divisors for the image
for j, div in enumerate( use_divisors ):
    
    n_counts = []
    splitImage = ast2050.lab1.divideImage(data_crop, xcrop=0, ycrop=0, xnum=div, ynum=div)
    splitDark = ast2050.lab1.divideImage(master_dark_crop, xcrop=0, ycrop=0, xnum=div, ynum=div)
    
    # Loop over the splits
    for k, split in enumerate(splitImage):
        spe_data, _ = ast2050.lab1.detect_counts(split, dark=splitDark[k])
        n_counts.append(len(spe_data))
    ###j
    
    # Now make the array for evaluating the Chi Square statistic.
    max_counts = np.max(n_counts)
    binned_counts,_ = np.histogram(n_counts, bins=np.arange(-0.5,max_counts+1.5))
    # binned_counts = binned_counts / len(n_counts)
    bin_numbers = np.linspace(0, max_counts, max_counts+1)
    poisson_bin = PoissonDist(np.mean(n_counts), bin_numbers) * len(n_counts)
    
    # Calculate the Chi Square statistic and the number of degrees of freedom
    chisquare = np.sum( np.divide( np.square( binned_counts - poisson_bin ), poisson_bin ) ) 
    # Number of data classes - number of variables (just mean) - 1
    dof = len( binned_counts ) - 2 
    
    # Calculate the p-value, 1-CDF of the Chi Square function
    p_value = 1-chi2.cdf(chisquare,dof)
    p_values.append( p_value )
    
    # print(div)
    # print(dof)
    # print(chisquare)
    # print(p_value)
    # print('\n')
###i

# pdb.set_trace()

fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter( (900/np.array(use_divisors))**2, p_values )
ax.set_ylim(0,1)
ax.set_xlabel('Pixels per sub-image')
ax.set_ylabel(r'p-value')
plt.show()




#