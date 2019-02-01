import numpy as np
import sys, os, pdb, glob
from matplotlib import pyplot as plt
sys.path.append('../../src/')
import ast2050.lab1
from scipy.special import factorial

# Plot a histogram for one of your sequences with a small count rate, e.g, 2-4 counts

def PoissonDist(mu, x):
	""" Returns a Poisson distriubtion.

	Parameters
	----------
	mu: float
		mean
	x: array
		array of x values to put into the Poisson distribution

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
ax.hist(n_counts, histtype='step', linewidth=2, color='k', density=True)
ax.axvline(np.mean(n_counts), color='r', linestyle='--', label=r'$\mu$ = %s' % np.mean(n_counts))
x = np.linspace(min(n_counts), max(n_counts))
ax.plot(x, PoissonDist(mean(n_counts), x), color='blue', linewidth=2, label='Poisson Distribution')
ax.legend(fancybox='True', loc='best')
ax.set_xlabel('Counts')
ax.set_ylabel('Normalized Frequency')
fig.savefig('Poisson_Distribution.pdf')




