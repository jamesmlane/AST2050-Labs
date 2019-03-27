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
    
    Reads data from the airspy. Returns a time series.
    
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

def calculate_power_bsub(data,background,sample_rate=5.0E6,lof=1.42E9):
    '''calculate_power_bsub:
    
    Take a raw data time series from the Airspy and compute the 
    power spectrum and subtract off the background.
        
    Args:
        data (N-length int array)
        background (N-length int array) [None]
        sample_rate (float) - samples/second [5E6]
        lof (float) - local oscillator frequency in Hz [1.42 Ghz]
        
    Return:
        power (float array) - Power
        freqs (float array) - RF Frequencies
    '''
    
    # Make sure data and background have the same length
    len_data = len(data)
    len_bg = len(background)
    if len_data > len_bg:
        data = data[:len_bg]
    elif len_bg > len_data:
        background = background[:len_data]
    ##ei
    
    # Take the Fourier transform and shift it
    ft_data = np.fft.fftshift( np.fft.fft( data ) )
    ft_bg = np.fft.fftshift( np.fft.fft( background ) )
    
    # Determine the frequencies
    freq = np.fft.fftshift( np.fft.fftfreq( len_data, 1/sample_rate ) )
    freq_rf = np.abs( freq_data[:int(len_data/2)] ) + lof
    
    # Calculate the power using the periodogram
    power_data = np.abs(ft_data)**2 + np.abs(ft_data[::-1])**2
    power_background = np.abs(ft_background)**2 + np.abs(ft_background[::-1])**2
    
    # Only take the power corresponding to positive frequencies.
    # Then normalize by the square of the number of data points
    power_data_rf = power_data[:int(len_data/2)] / n_data**2
    power_background_rf = power_background[:int(len_data/2)] / n_data**2
    power_data_rf_bsub = power_data_rf - power_background_rf
    
    return power_data_rf_bsub, freq_data_rf
    
#def

