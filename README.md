# spectral-mask

Software project for Northwestern University ASTRON 441 Astronomical Techniques Fall 2022

original coding assignment from ASTRON 421 Observational Astrophysics class, Spring 2022

you will analyze the spectra of a nearby star, and ultimately conclude that there is a planet orbiting that star. You will also measure the mass of that planet! The spectra were obtained with the [ELODIE spectrograph](https://en.wikipedia.org/wiki/ELODIE_spectrograph), which provides high resolution measurements of the spectrum (enabling us to precisely locate the positions of the absorption lines).

you are given data in an uncorrected form, and then you measure the RV using an absorption spectrum "mask" – this is precisely how such measurements are made with the HARPS spectrograph, which is a successor to ELODIE.


## Radial Velocities

One of the great benefits of obtaining spectroscopic observations is that it allows us to measure the velocity of the absorbing gas (often this is gas in a star's atmophere) relative to the line of sight. These measurements can have important physical consequences, such as allowing us to infer the mass of two stars orbiting in a binary (see lecture). 

The "simple" way to measure a [radial velocity](https://en.wikipedia.org/wiki/Radial_velocity) is to identify some emission/absorption line in a spectrum and compare its observed wavelength to the wavelength measured "at rest" in a lab on earth. With that measurement in hand, the [Doppler equation](https://en.wikipedia.org/wiki/Doppler_effect) dictates how to convert the change in wavelength to a velocity.

Using a single line can be limited however, if, for example, the spectrum is low signal to noise or there are multiple processes contributing to the line profile. 

One can use "all the information" present in a spectrum to estimate the redshift/Doppler shift via a [cross correlation](https://en.wikipedia.org/wiki/Cross-correlation) with a template spectrum (see also the lecture notes). The (discrete) cross-correlation is the sum of the observed spectrum multiplied by the template. 
$$CC = \sum f(m) g(m - n)$$

where the sum is over all pixels $m$, $f$ is the spectrum, and $g$ is the shifted template (in practice we will use interpolation to place the doppler shifted template onto the same wavelength grid as the primary observations).

The cross-correlation function (CCF) is the value of the cross-correlation at different velocity shifts for the template. The peak of the CCF corresponds to your estimate for the RV of the observation.

## Precise RV measurements (graduates)

You can download continuum normalized spectra from [my solutions](https://nuwildcat-my.sharepoint.com/:u:/g/personal/aam3503_ads_northwestern_edu/EcRLxrxJVhlHm0zvwwTHxnoB67g9ZBY3VVAWQsn_RtNbBA?e=dArEOo). Once you unpack that tarball, you will also notice the file `G2_mask.csv` – which is the mask used to estimate the CCF.

The spectra for the grad students have *only* been continuum normalized. `NaN` has not been removed, and the motion of the Earth relative to the solar system barycenter has not been corrected. 

The procedure to measure the CCF is largely the same, except that instead of a template we have a mask. The mask file consists of three columns. The first column defines the "left" or "blue" edge of a mask region, the second column defines the "right" or "red" edge of a mask region, and the third column defines the mask value. 

In order to calculate the XC (and eventually the CCF), we must "interpolate" the mask onto the wavelength grid of the observed spectrum. This interpolation is not a simple call to numpy (as it is in the undergrad problem). 

To determine the value of the mask in each pixel of the ELODIE spectrum, we must calculate the fractional coverage of the mask with the givel pixel, and then multiply that fraction by the mask value. 

I will demonstrate what this means with a few examples: 

1. The mask starts at 4358.66 Ang and ends at 4358.89 Ang and has a value of 0.7. The pixel starts at 4358.7 Ang and ends at 4358.75 Ang. >>> The pixel mask has a value of 0.7. 

2. The mask starts at 5422.12 Ang and ends at 5422.96 Ang and has a value of 0.3. The pixel starts at 5422.10 Ang and ends at 5422.15 Ang. >>> The pixel mask has a value of 0.3 * (5422.15 - 5422.12)/(5422.15 - 5422.10) = 0.18.

3. One mask ends at 6452.3 and the next mask starts at 6452.9 Ang. The pixel starts at 6452.45 Ang and ends at 6452.50 Ang. >>> The pixel mask has a value of 0. 