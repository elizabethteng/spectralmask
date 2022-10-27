import numpy as np
from scipy.optimize import curve_fit
from scipy.stats import norm

def gaussian_fit(x,y):
    
    def gaussian(x, mean, std, amp, offset):
        return amp * np.exp(-(x-mean)**2 / (2*std**2)) + offset
    
    best_vals, covar = curve_fit(gaussian,x,y,p0 = [0,1e6,-2e6,50])
    mean, std = best_vals[0],best_vals[1]
    
    return mean, np.abs(std)
