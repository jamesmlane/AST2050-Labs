### Imports

## Basic
import numpy as np
import sys, os, pdb, glob

## Plotting
from matplotlib import pyplot as plt

sys.path.append('../../src/')
import ast2050.lab1

# ----------------------------------------------------------------------------

# Get a list of the images
image_list = glob.glob('./XRayImages/image*')
n_images = len(image_list)

# number of sub-images per axis
num = 4

# Get the master dark
master_dark = np.load('./masterDark.npy')

# split master dark
splitDark = ast2050.lab1.divideImage(master_dark, xcrop=12, ycrop=0, xnum=34, ynum=28)

# Get an array to hold the number of counts
#n_counts = np.zeros(n_images)

# Loop over the images
means = []
variances = []
for idx, image in enumerate(image_list):

	n_counts = []
	
	data = ast2050.lab1.read_tiff(image).astype(float)

	splitImage = ast2050.lab1.divideImage(data, xcrop=12, ycrop=0, xnum=34, ynum=28)

	for jdx, split in enumerate(splitImage):
	
		spe_data, _ = ast2050.lab1.detect_counts(split, dark=splitDark[jdx])

		n_counts.append(len(spe_data))

	#fig = plt.figure()
	#ax = fig.add_subplot(111)
	#####
	#ax.plot( np.arange(0,num*num)+1, n_counts, color='Black', linewidth=0.5 )
	#ax.axhline( np.average(n_counts), color='Red', linestyle='dashed', linewidth=1.0 )
	#ax.set_xlim(1,num*num)
	#ax.set_xlabel('Sub-Image Number')
	#ax.set_ylabel('Counts')
	#fig.savefig('subHistograms/count_histogram_%s.pdf' % idx)
	#plt.close('all')
	#####
	#ax.hist(n_counts, bins=6, histtype='step', linewidth=2, color='k')
	#ax.axvline(np.mean(n_counts), color='red', linestyle='dashed')
	#ax.set_xlabel('Count')
	#ax.set_ylabel('Frequency')
	#ax.set_title(r'$\mu = $ %s, $\sigma = $ %s' % (np.mean(n_counts), np.std(n_counts)))
	#fig.savefig('subHistograms/histogram_%s.pdf' % idx)
	#plt.close('all')
	means.append(np.mean(n_counts))
	variances.append(np.var(n_counts))

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(means, variances, '.', color='k')
ax.plot(np.linspace(min(means), max(means)), np.linspace(min(means), max(means)), color='r', linestyle='--')
ax.set_xlabel('Mean')
ax.set_ylabel('Variance')
fig.savefig('mean-vs-variance-784Images.pdf')
plt.close('all')

# ----------------------------------------------------------------------------
