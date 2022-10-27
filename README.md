# spectralmask

This package was created to aid in measuring radial velocities from stellar spectra by comparing observed spectra to masks based on fiducial absorption spectra. 

## Features
The class `Spectrum` processes .fits files containing continuum-normalized spectra. It has modules for constructing a spectrum object from the data and metadata (optionally making a Barycenter-Earth RV correction), and for interpolating over NaN values. 

The class `Mask` reads in a spectral mask from a .csv file and a spectrum in the form of wavelength and flux arrays. It has modules that interpolate the mask and spectrum over all wavelength values and calculate cross-correlation and the cross-correlation function. 

The function `gaussian_fit` fits a Gaussian curve to the cross-correlation function between the spectrum and mask to measure the difference in wavelength. 

## Cloning and Installing spectralmask
To use this package, first clone this repository:
```
git clone https://github.com/elizabethteng/spectralmask.git
```

then open the spectralmask directory and install it in your python environment:
```
pip install .
```
The dependencies should also install automatically. 

## Tutorial
The notebook `tutorial.ipynb` included in the main directory contains an explanation of the scientific basis for this package as well a brief tutorial demonstrating the basics of the code. Additional documentation exists in the docstrings of the source code. 

--

*Software project for Northwestern University ASTRON 441 Astronomical Techniques Fall 2022*

*original coding assignment from ASTRON 421 Observational Astrophysics class, Spring 2022*
