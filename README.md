# AiryDisk
Airy Disk image generator

More info in Airy Disk in photography: https://www.cambridgeincolour.com/tutorials/diffraction-photography.htm

Problem description:
Need a Windows Python script (likely using PIL and numpy) that will simulate an approximation of how an image would look if it was produced by a lens and was made up of airy disks (aka PSF - point spread functions) rather than solid square pixels. A very limited optics info is involved here (one equation and 5 basic optics terms, highlighted with quotation marks in the job post) and the simulation assumes an ideal unrealistic optical system. Due to how "airy disk" / "PSF" function looks like, a gaussian approximation may be used instead for simplicity.

There will be two main steps for the script:
1) generate an "airy disk" image for each R,G,B color channel/”wavelength”
2) populate a very high resolution image (with the resolution configurable by the user) with such "airy disks"/"PSFs" based on the pixel data of the input low-res image.


The inputs should be
1) the ”focal length” in millimeters, default being 50mm
2) ”aperture” size in millimeters (X and Y of the aperture may be different values and the resulting R,G,B "airy disk"/"PSF" images may not be radially symmetric), default being 10mm
3) the 3 R,G,B "airy disk"/"PSF" “wavelengths” in um/micron (default being 0.455, 0.520 and 0.625 respectively)
4) the input image
5) the output image resolution (default being 10,000x10,000)
6) generated "airy disk"/"PSF" images resolution (default being 128x128)
7) There should be an option (for example in the config file) to set how many PSFs should represent a single input image pixel, with the default value being a 32x32 array (X and Y for this is assumed to always be equal).

These inputs besides the input image should be read from a config file.


“Airy disk” diameter equation is: airy_disk_diameter_in_um = 2.44 * wavelength_in_um * (focal_length/aperture_diameter)

The size of the resulting image in mm is assumed to be the size of the “aperture” in mm.

Again, the aperture_diameter may not be same in X and Y and the equation may give two separate values for “aperture” size X and Y.

We are dealing with simulating light here. So each new airy disk in the list has its value added (color addition) to existing result image.

To generate accurate results, the different color channels of the input image should be processed separately as again, airy disk diameter is dependent of wavelength (color) .


We will need a progress bar and ability to pause the processing as well as to quit and save what has already been processed. Whether this is done in the command line or with a very simple GUI is up to you.

The output should be a 16bit bmp or png of each color channel as well as combined 48bit RGB image, same folder as input image.
