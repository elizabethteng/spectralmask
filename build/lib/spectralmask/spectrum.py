import numpy as np
import os
from astropy.io import fits
from scipy.interpolate import interp1d
from scipy.optimize import curve_fit
from scipy.stats import norm
import pandas as pd

class Spectrum():
    
    def __init__(self, path, name):
        """ Spectrum class
        
            Reads in continuum-normalized spectrum from filepath

            Args:
                path (string): directory
                name (string): file name for spectrum fits file

            Returns:
                None

            """
        self.path = path
        self.name = name
        self.spec = fits.getdata(path+name)
        
    def make_wv(self,berv=True):
        """ make_wv
            
            creates wavelength array and optionally adjusts for BERV
        
            Args:
                self (object) : Spectrum object
                berv (boolean): if true, adjusts values for BERV
                
            Returns: 
                array-like: wavelength values
        
            """
        crval1 = fits.getval(filename=self.path+self.name, keyword="CRVAL1")
        cdelt1 = fits.getval(filename=self.path+self.name, keyword="CDELT1")
        naxis1 = fits.getval(filename=self.path+self.name, keyword="NAXIS1")
        
        wv = np.linspace(crval1,crval1+cdelt1*(naxis1-1),naxis1)
        
        if berv==True:
            berv = fits.getval(filename=self.path+self.name, keyword="BERV")
            berv_wv = wv * (berv/2.99792e5 + 1)
            return berv_wv
        else:
            return wv
        
    def interpolate_nan(self, wv):
        """ interpolate_nan
        
            interpolates over NaN values

            Args: 
                self (object)  : Spectrum object
                wv (array-like): wavelengths of spectrum points

            Returns:
                array-like: spectrum interpolated to correct NaNs

            """
        finite = np.where(np.isfinite(self.spec))
        lin_interp = interp1d(wv[finite],self.spec[finite], fill_value="extrapolate")
        spec = lin_interp(wv)
        return spec