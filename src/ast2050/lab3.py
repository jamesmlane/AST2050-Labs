# ----------------------------------------------------------------------------
#
# TITLE - lab1.py
# PROJECT - AST 2050
# CONTENTS:
#
# ----------------------------------------------------------------------------

### Docstrings and metadata:
'''Functions for Lab 3 of AST 2050

Import me by including this at the beginning of the script:
sys.path.append('path/to/src/')
import ast2050.lab1
'''

### Imports

## Basic
import numpy as np
import sys, os, pdb, re
import glob

## Plotting
from matplotlib import pyplot as plt

## Astropy
from astropy.time import Time
from astropy.coordinates import SkyCoord, EarthLocation, AltAz
from astropy import units as apu

# ----------------------------------------------------------------------------

def read_airspy_data(filename):
    '''
    read_airspy_data:
    
    Reads data recorded using the airspy. Returns a time series.
    
    Args:
        filename (string)
    
    Returns:
        data (int array)
    '''
    return np.fromfile(filename, dtype='int16') - 2**11
#def

def calculate_galactic_longitude_radec(lon):
    '''calculate_galactic_longitude_radec:
    
    Calculate the RA / Dec of a point in the plane of the galaxy.
    
    Args:
        lon (float) - galactic longitude
        
    Returns:
        (Ra,Dec)
    '''
    coord_gal = SkyCoord( l=lon*apu.deg, b=np.zeros_like(lon)*apu.deg, 
                        frame='galactic' )
    coord_icrs = coord_gal.icrs
    return (coord_icrs.ra.value,coord_icrs.dec.value)
#def

def calculate_galactic_longitude_altaz(lon, date_time_string):
    '''calculate_galactic_longitude_altaz:
    
    Calculate the Alt / Az of a point in the plane of the galaxy.
    
    Args:
        lon (float) - galactic longitude
        date_time_string (string) - A string specifying the date and time that 
            takes the form: 'YYYY-MM-DD HH:MM:SS'
        
    Returns:
        (Ra,Dec)
    '''
    coord_gal = SkyCoord( l=lon*apu.deg, b=np.zeros_like(lon)*apu.deg, 
                        frame='galactic' )
    toronto_location = EarthLocation( lon=(360-79.3832)*apu.deg, lat=43.6532*apu.deg, 
                                      height=70*apu.m )
    utoffset = -4*apu.hour # EDT
    time = Time(date_time_string) - utoffset
    coord_altaz = coord_gal.transform_to(AltAz(obstime=time, 
                                                location=toronto_location))
    return (coord_altaz.alt.value, coord_altaz.az.value)
#def

def calculate_power(data,chunk_size,sample_rate=5.0E6,lof=1.42E9):
    '''calculate_power:
    
    Take the raw data time series from the airspy and compute the 
    power spectrum
    
    Args:
        data (N-length int array)
        chunk_size (int) - The number of data points to calculate the FFT on 
            at a time
        sample_rate (float) - samples/second [5E6]
        lof (float) - local oscillator frequency in Hz [1.42 Ghz]
        
    Return:
        power (float array) - Power
        freqs (float array) - RF Frequencies
    '''
    
    # Sample length
    sample_size = len(data)
    timestep = 1/sample_rate
    
    # Array to hold stacked fft result
    fft = np.zeros(chunk_size//2+1,dtype='complex64')
    
    # Take the Fourier transform looped over the chunks
    for i in range( sample_size//chunk_size ):
        fft += np.fft.rfft(data[ i*chunk_size : (i+1)*chunk_size ]) / (chunk_size/2)
    ###i
    
    # Determine the frequencies
    freq = abs( lof - np.fft.rfftfreq(chunk_size, d=timestep) ) + sample_rate/4
    
    # Calculate the power using the periodogram. Trivial because we've only 
    # taken positive frequency data anyways.
    power = np.abs( fft )**2
    
    return freq, power
#def
