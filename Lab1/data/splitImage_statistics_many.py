import numpy as np
import sys, os, pdb, glob
from matplotlib import pyplot as plt
sys.path.append('../../src/')
import ast2050.lab1

def divisors(intgr):
	""" Return all divisors of an integer, except 1 and the number itself.
	"""
	divisors = []
	for i in range(1,intgr+1):
		if(intgr%i==0):
			divisors.append(i)
	return divisors[1:-1]

image_list = glob.glob('./XRayImages/image*')
n_images = len(image_list)

master_dark = np.load('./masterDark.npy')
master_dark_crop = master_dark[:900,:900]

means = []
variances = []

for idx, image in enumerate(image_list):
	data = ast2050.lab1.read_tiff(image).astype(float)
	data_crop = data[:900,:900]
	for div in divisors(900)[:-2]:
		n_counts = []
		splitImage = ast2050.lab1.divideImage(data_crop, xcrop=0, ycrop=0, xnum=div, ynum=div)
		splitDark = ast2050.lab1.divideImage(master_dark_crop, xcrop=0, ycrop=0, xnum=div, ynum=div)
		for jdx, split in enumerate(splitImage):
			spe_data, _ = ast2050.lab1.detect_counts(split, dark=splitDark[jdx])
			n_counts.append(len(spe_data))
		means.append(np.mean(n_counts))
		variances.append(np.var(n_counts))

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(means, variances, '.', color='k')
ax.plot(np.linspace(min(means), max(means)), np.linspace(min(means), max(means)), color='r', linestyle='--')
ax.set_xlabel('Mean')
ax.set_ylabel('Variance')
ax.set_xscale('log')
ax.set_yscale('log')
fig.savefig('mean-vs-variance-many.pdf')
plt.close('all')