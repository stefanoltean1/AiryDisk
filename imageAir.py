# read image from file

import numpy as np
import cv2

# TODO add arguments
# Configuration parameters
inputImage = "test.jpg"
pixelsPerAiryDisk = 32  # array size for one airy disk
disksPerInputPixel = 4  # meaning a pixel will be represented by 32x32 airyDisks

# the 3 R,G,B "airy disk"/"PSF" “wavelengths” in um/micron (default being 0.455, 0.520 and 0.625 respectively)
# wavelengths in um
blueWavelength_um = 0.625
greenWavelength_um = 0.455
redWavelength_um = 0.520

# camera properties
# assume image captured by camera is same size as aperture
fStopValue = 18  #unitless
focalLength_mm = 55  #mm
apertureDiameter_mm = focalLength_mm / fStopValue  #mm

# airy disk diameters in um
blueAiryDiskDiameter_um = 2.44 * blueWavelength_um * fStopValue
greenAiryDiskDiameter_um = 2.44 * greenWavelength_um * fStopValue
redAiryDiskDiameter_um = 2.44 * redWavelength_um * fStopValue

print('Diks diameter values (BGR):', blueAiryDiskDiameter_um,
      greenAiryDiskDiameter_um, redAiryDiskDiameter_um)

# outputImage properties
outPutImageSize = 10000  #10000x10000 pixels
outputPixelSize_mm = apertureDiameter_mm / outPutImageSize
outputPixelSize_um = outputPixelSize_mm * 1000

print('Output pixe size:', outputPixelSize_um)

# Airy Disk pixel size
blueAiryDiskPixels = int(blueAiryDiskDiameter_um / outputPixelSize_um)
greenAiryDiskPixels = int(greenAiryDiskDiameter_um / outputPixelSize_um)
redAiryDiskPixels = int(redAiryDiskDiameter_um / outputPixelSize_um)

print(blueAiryDiskPixels, greenAiryDiskPixels, redAiryDiskPixels)

# Note: cv2 works in BGR channel order
baseImage = cv2.imread(inputImage)

print(np.shape(baseImage))

# take each channel of base image and create airy disk images

blueBaseChannel, greenBaseChannel, redBaseChannel = cv2.split(baseImage)


# generate mock Airy Disk (gaussian distribution)
def genAiryDiskGaussian(pixelsPerAiryDisk, sigma=1, mu=0.0):
    # Initializing value of x-axis and y-axis
    # in the range -1 to 1
    x, y = np.meshgrid(np.linspace(-1, 1, pixelsPerAiryDisk),
                       np.linspace(-1, 1, pixelsPerAiryDisk))
    dst = np.sqrt(x * x + y * y)

    # Calculating Gaussian array
    gauss = np.exp(-((dst - mu)**2 / (2.0 * sigma**2)))
    return gauss


# create airyDisk area from one pixel value
def pixelToAiryDisks(pixelBrightness, gaussian, disksPerInputPixel):
    airyDisk = pixelBrightness * gaussian
    airyDiskPixelEquivalent = np.tile(airyDisk,
                                      [disksPerInputPixel, disksPerInputPixel])
    return airyDiskPixelEquivalent


# create airyDisk replacement for every pixel in channel
# TODO: if AiryDiskPixels < 1 --> do nothing, just keep old pixel or add padding
def airyDisksChannel(colorBaseChannel, outputAiryChannel, gaussian,
                     disksPerInputPixel, pixelsPerAiryDisk, scaleFactor):
    print(colorBaseChannel.shape)
    print(outputAiryChannel.shape)
    for rowIndex, row in enumerate(colorBaseChannel):
        for columnIndex, brightnessValue in enumerate(row):
            outputRowIndex = rowIndex * scaleFactor
            outputColumnIndex = columnIndex * scaleFactor
            outputAiryChannel[outputRowIndex:outputRowIndex + scaleFactor,
                              outputColumnIndex:outputColumnIndex +
                              scaleFactor] = pixelToAiryDisks(
                                  brightnessValue, gaussian,
                                  disksPerInputPixel)

    return outputAiryChannel


# original image size
row, col = blueBaseChannel.shape

# use outputScaleFactor to create a large image to fill with airy disks
# use the max pixel size
outputScaleFactor = disksPerInputPixel * max(
    blueAiryDiskPixels, greenAiryDiskPixels, redAiryDiskPixels)

# array for output image -- all channels
# TODO: investigate memory optimization to work with larger parameters/images
# TODO: investigate batch processing (store data on harddrive)
outputImage = np.ndarray((3, row * outputScaleFactor, col * outputScaleFactor),
                         dtype=np.uint8)

# split output array into channels
blueOutputImage, greenOutputImage, redOutputImage = outputImage

print(blueOutputImage)

blueScaleFactor = disksPerInputPixel * blueAiryDiskPixels
blueDimOutput = (col * blueScaleFactor, row * blueScaleFactor)
blueOutputImage = cv2.resize(blueOutputImage, blueDimOutput)
# blueBaseChannel = cv2.resize(blueBaseChannel, blueDimOutput)

greenScaleFactor = disksPerInputPixel * greenAiryDiskPixels
greenDimOutput = (col * greenScaleFactor, row * greenScaleFactor)
greenOutputImage = cv2.resize(greenOutputImage, greenDimOutput)
# greenBaseChannel = cv2.resize(greenBaseChannel, greenDimOutput)

redScaleFactor = disksPerInputPixel * redAiryDiskPixels
redDimOutput = (col * redScaleFactor, row * redScaleFactor)
redOutputImage = cv2.resize(redOutputImage, redDimOutput)
# redBaseChannel = cv2.resize(redBaseChannel, redDimOutput)

print(blueDimOutput, greenDimOutput, redDimOutput)
print(blueScaleFactor, greenScaleFactor, redScaleFactor)

# add Airy disks to each channel
print('Processing Blue')
blueDiskGaussian = genAiryDiskGaussian(blueAiryDiskPixels)
blueOutputImage = airyDisksChannel(blueBaseChannel, blueOutputImage,
                                   blueDiskGaussian, disksPerInputPixel,
                                   blueAiryDiskPixels, blueScaleFactor)

print(blueOutputImage.shape)

print('Processing Green')
greenDiskGaussian = genAiryDiskGaussian(greenAiryDiskPixels)
greenOutputImage = airyDisksChannel(greenBaseChannel, greenOutputImage,
                                    greenDiskGaussian, disksPerInputPixel,
                                    greenAiryDiskPixels, greenScaleFactor)

print('Processing Red')
redDiskGaussian = genAiryDiskGaussian(redAiryDiskPixels)
redOutputImage = airyDisksChannel(redBaseChannel, redOutputImage,
                                  redDiskGaussian, disksPerInputPixel,
                                  redAiryDiskPixels, redScaleFactor)

# TODO: refactoring, colors at the beggining of variables

# resize all output images to same size before stacking them
minScaleFactor = min(blueScaleFactor, greenScaleFactor, redScaleFactor)
finalImageSize = (col * minScaleFactor, row * minScaleFactor)
blueOutputImage = cv2.resize(blueOutputImage, finalImageSize)
greenOutputImage = cv2.resize(greenOutputImage, finalImageSize)
redOutputImage = cv2.resize(redOutputImage, finalImageSize)

# merge channels to new Airy image
outputImage = np.dstack([blueOutputImage, greenOutputImage, redOutputImage])

# output result
cv2.imwrite('output.jpg', outputImage)

# pad area surrounding each pixel to "increase resolution

# create airy disk based on each pixel value for each channel ---> 32x32 size
# TODO configure airy disk size / pixel
# create airy disk image which will be 32*Xx32*Y pixels

# get pixel size of new image (default 10kx10k)

# calculate diameter of airy disk

# find out size of one pixel in new image

# reduce size of airy disk images to fit number of pixels in new image
# airy disk will be 32x32 and PSFSize = x um
# the real image si 10000x1000 and size 10 mm (or different input)
# a pixel size in real image is 10/10000
# find out how many PSF fit in one image

# and R + G + B

# Output image

# TODO add __main__
