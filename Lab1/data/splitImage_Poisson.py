import numpy as np
import sys, os, pdb, glob
from matplotlib import pyplot as plt
sys.path.append('../../src/')
import ast2050.lab1
from scipy.special import factorial
from scipy.stats import chi

# Plot a histogram for one of your sequences with a small count rate, e.g, 2-4 counts

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

xnum = 17
ynum = 14
xcrop = 12
ycrop = 0

# just use a random image
image = './XRayImages/image00000.tiff'

master_dark = np.load('./masterDark.npy')
splitDark = ast2050.lab1.divideImage(master_dark, xcrop=xcrop, ycrop=ycrop, xnum=xnum, ynum=ynum)

n_counts = []
data = ast2050.lab1.read_tiff(image).astype(float)
splitImage = ast2050.lab1.divideImage(data, xcrop=xcrop, ycrop=ycrop, xnum=xnum, ynum=ynum)
for jdx, split in enumerate(splitImage):
	spe_data, _ = ast2050.lab1.detect_counts(split, dark=splitDark[jdx])
	n_counts.append(len(spe_data))

fig = plt.figure()
ax = fig.add_subplot(111)
ax.hist(n_counts, histtype='step', align='left', linewidth=2, color='k')
ax.plot([], [], linewidth=2, color='k', label='Data')
ax.axvline(np.mean(n_counts), color='r', linestyle='--', label=r'Mean = %s' % round(np.mean(n_counts),2) )
x = np.linspace(min(n_counts), max(n_counts), num=1000)
ax.plot(x, PoissonDist(np.mean(n_counts), x)*len(n_counts), color='blue', linewidth=2, label='Poisson Distribution')
ax.legend(fancybox='True', loc='best')
ax.set_xlabel('Counts')
ax.set_ylabel('Number')
ax.set_xlim(0,11)
fig.savefig('Poisson_Distribution.pdf')

# Bin the counts before calculating the Chi square statistic
max_counts = np.max(n_counts)
binned_counts, bin_edges = np.histogram(n_counts, bins=np.linspace(0,max_counts+1,max_counts+2)-0.5)
binned_counts = binned_counts / len(n_counts)
bin_numbers = np.linspace(0, max_counts, max_counts+1)
poisson_bin = PoissonDist(np.mean(n_counts), bin_numbers)

# Calculate the Chi Square statistic and the number of degrees of freedom
chisquare = np.sum( np.divide( np.square( binned_counts - poisson_bin ), poisson_bin ) ) 
# Number of data classes - number of variables (just mean) - 1
dof = len( np.where(binned_counts>0.0)[0] ) - 2

# Calculate the p-value, the inverse CDF of the Chi Square function
pvalue = 1-chi.cdf(chisquare,dof)

pdb.set_trace()
