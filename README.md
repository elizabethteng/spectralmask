# spectralmask

This package was created to aid in measuring radial velocities from stellar spectra by comparing observed spectra to masks based on fiducial absorption spectra. 

## Radial Velocities

The "simple" way to measure a radial velocity is to compare the wavelength of an observed spectral line to the wavelength measured in a laboratory setting. With that measurement in hand, the Doppler equation dictates how to convert the difference in wavelength to a velocity. Using a single line can be limited if, for example, the spectrum is low signal to noise or there are multiple processes contributing to the line profile. 

One can use "all the information" present in a spectrum to estimate the redshift/Doppler shift via a cross-correlation with a template spectrum. The (discrete) cross-correlation is the sum of the observed spectrum multiplied by the template. 
$$CC = \sum f(m) g(m - n)$$

where the sum is over all pixels $m$, $f$ is the spectrum, and $g$ is the shifted template (in practice we use interpolation to place the Doppler-shifted template onto the same wavelength grid as the primary observations).

The cross-correlation function (CCF) is the value of the cross-correlation at different velocity shifts for the template. The peak of the CCF corresponds to your estimate for the RV of the observation.

## Measuring Radial Velocities using spectralmask

The example spectra included in this package were obtained with the ELODIE spectrograph and are continuum normalized (but not corrected for NaNs or the motion of the Solar system barycenter). The file `G2_mask.csv` provided is a spectral mask that can be used to estimate the cross-correlation function. 

The procedure to measure the cross-correlation function is largely the same, except that instead of a template we have a mask. The mask file consists of three columns. The first column defines the "left" or "blue" edge of a mask region, the second column defines the "right" or "red" edge of a mask region, and the third column defines the mask value. 

In order to calculate the XC (and eventually the CCF), we must "interpolate" the mask onto the wavelength grid of the observed spectrum. This interpolation is not a simple call to numpy (as it is in the undergrad problem). 

To determine the value of the mask in each pixel of the ELODIE spectrum, we must calculate the fractional coverage of the mask with the givel pixel, and then multiply that fraction by the mask value. 

*Software project for Northwestern University ASTRON 441 Astronomical Techniques Fall 2022*

*original coding assignment from ASTRON 421 Observational Astrophysics class, Spring 2022*
