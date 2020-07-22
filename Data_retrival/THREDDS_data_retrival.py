# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 15:04:43 2020

@author: Eirik Nordgård

This is a short script to retrieve data from MET Norways THREDDS 
modell- and research data. Detailed information may be found on 
https://thredds.met.no/thredds/catalog.html 
"""

#%%

import netCDF4
import numpy as np
import pandas as pd

# Read netcdf file from thredds server
# This is the lates forecast file compiled from AROME-arctic 
# Enter "data" in console to get more information 

data = netCDF4.Dataset('https://thredds.met.no/thredds/dodsC/aromearcticlatest/arome_arctic_pp_2_5km_latest.nc')                     

#Extract desired data
t2m = data.variables['air_temperature_2m'][:] #(time,height,y,x)

'''
This is fast, want to put "data" into a dataframe, or t2m
'''

#%% Alternative way to make a dataframe, not sure if this is what i want
url='https://thredds.met.no/thredds/dodsC/aromearcticlatest/arome_arctic_pp_2_5km_latest.nc'

import xarray 

ds = xarray.open_dataset(url)
df = ds.to_dataframe()