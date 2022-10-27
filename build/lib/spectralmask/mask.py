import numpy as np
import os
from astropy.io import fits
from scipy.interpolate import interp1d
from scipy.optimize import curve_fit
from scipy.stats import norm
import pandas as pd

class Mask():
    
    def __init__(self, wv, spec, mask):
        """ Mask class
        
            reads in mask from csv file

            Args:
                wv (array-like)  : spectrum wavelength values
                spec (array-like): spectrum flux values
                mask (string)    : path + file name for mask

            Returns:
                None

            """
        self.wv = wv
        self.spec = spec
        self.mask = pd.read_csv(mask)
            
    def interpolate_wv(self, offset=0):
        """ interpolate_wv
            
            interpolates spectrum and mask over all wavelength values
            
            Args:
                self (object): Mask object
                offset (float): velocity offset for mask in cm/s
                
            Returns:
                array-like: set of all wavelength values for spectrum and mask
                array-like: spectrum interpolated over all wavelengths
                array-like: mask interpolated over all wavelengths
                                
            """
        interp_spec = interp1d(self.wv,self.spec, fill_value="extrapolate")
        
        mask_wvs = np.concatenate((self.mask['min_lambda'], self.mask['max_lambda']))
        mask_wvs = mask_wvs * (offset/2.99792e10 + 1)
        mask_vals = np.concatenate((self.mask['weight'],np.zeros(len(self.mask))))
        interp_mask = interp1d(mask_wvs,mask_vals,kind='previous',fill_value="extrapolate")
        
        mask_wvs = np.setxor1d(self.mask['min_lambda'],self.mask['max_lambda'])
        spec_wvs = self.wv
        all_wvs = np.setxor1d(mask_wvs,spec_wvs)
        
        spec_zero_edges = interp_spec(all_wvs)
        below = np.where(all_wvs < np.min(self.wv))[0]
        above = np.where(all_wvs > np.max(self.wv))[0]
        spec_zero_edges[below] = 0
        spec_zero_edges[above] = 0
        
        mask_zero_edges = interp_mask(all_wvs)
        below = np.where(all_wvs < np.min(mask_wvs))
        above = np.where(all_wvs > np.max(mask_wvs))
        mask_zero_edges[below] = 0
        mask_zero_edges[above] = 0
        
        return all_wvs, spec_zero_edges, mask_zero_edges
            
    def XC(self, offset=0):
        """ XC
            
            calculates cross-correlation
            
            Args:
                self (object) : Mask object
                offset (float): velocity offset for mask in cm/s
                
            Returns:
                float: value of cross-correlation function between mask and spectrum
                
            """
        all_wvs, spec, mask = self.interpolate_wv(offset)
        pixel_widths = np.append(all_wvs[1:]-all_wvs[:-1],[0])
        masked_spectrum = spec*mask*pixel_widths
        return np.sum(masked_spectrum)
    
    def CCF(self,min_offset=-1e7,max_offset=1e7,resolution=201):
        """ CCF
            calculates cross-correlation function
            
            Args:
                self (object)     : Mask object
                min_offset (float): minimum offset velocity for CCF evaluation in cm/s 
                max_offset (float): maximum offset velocity for CCF evaluation in cm/s
                resolution (int)  : number of offset velocity values to evaluate
            
            Returns:
                array-like: offset velocity array
                array-like: CCF value array
                
            """
        offset_vals = np.linspace(min_offset,max_offset,resolution)
        CCF_vals = [self.XC(i) for i in offset_vals]
        return offset_vals, CCF_vals
    