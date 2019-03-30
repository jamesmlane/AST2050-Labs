# ----------------------------------------------------------------------------
#
# TITLE -
# AUTHOR - James Lane
# PROJECT -
# CONTENTS:
#
# ----------------------------------------------------------------------------

### Docstrings and metadata:
'''

'''
__author__ = "James Lane"

### Imports

## Basic
import numpy as np
import sys, os, pdb
# import copy
# import glob
# import subprocess

## Plotting
from matplotlib import pyplot as plt
# from matplotlib.backends.backend_pdf import PdfPages
# from matplotlib import colors
# from matplotlib import cm
# import aplpy

sys.path.append('../src/')
import ast2050.lab3 as lab3

# ----------------------------------------------------------------------------

gal_lon = np.linspace( 0, 360, num=20 )
gal_lon = np.array([170,180,190,200,210,220,230])

gal_alt, gal_az = lab3.calculate_galactic_longitude_altaz(gal_lon, 
'2019-3-28 18:45:00' )

where_high_alt = np.where( gal_alt > 10 )[0]

for i in range( len(gal_az) ):
    print('Azimuth:')
    print(gal_az[i])
    print('Altitude')
    print(gal_alt[i])
    print('Longitude:')
    print(gal_lon[i])
    print('\n\n')

# print('Azimuth')
# print(gal_az[where_high_alt])
# print('Altitude')
# print(gal_alt[where_high_alt])
# 
# pdb.set_trace()

# ----------------------------------------------------------------------------
