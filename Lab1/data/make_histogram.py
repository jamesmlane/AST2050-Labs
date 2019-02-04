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

# Get the master dark
master_dark = np.load('./masterDark.npy')

# Get an array to hold the number of counts
n_counts = np.zeros(n_images)

# Loop over the images
for i in range(n_images):
    
    data = ast2050.lab1.read_tiff(image_list[i]).astype(float)
    
    spe_data, _ = ast2050.lab1.detect_counts(data, dark=master_dark)

    n_counts[i] = len(spe_data)
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter( np.arange(0,len(spe_data))+1, spe_data, )
    ax.set_ylim(90,275)
    ax.set_xlabel('Number')
    ax.set_ylabel('Counts')
    fig.savefig(image_list[i]+'.pdf')
    plt.close('all')
    
###i

fig = plt.figure()
ax = fig.add_subplot(111)


ax.plot( np.arange(0,n_images)+1, n_counts, color='Black', linewidth=0.5 )
ax.axhline( np.average(n_counts), color='Red', linestyle='dashed', linewidth=1.0 )
ax.set_xlim(1,n_images)
ax.set_xlabel('Image Number')
ax.set_ylabel('Counts')

fig.savefig('count_histogram.pdf')
plt.close('all')

# ----------------------------------------------------------------------------
