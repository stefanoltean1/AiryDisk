# read image from file

import numpy as np
import cv2

# TODO add arguments
# Configuration parameters
inputImage = "test.jpg"
pixelsPerOutputDisk = 64  # array size for one airy disk
disksPerInputPixel = 16  # meaning a pixel will be represented by 32x32 airyDisks

# Note: cv2 works in BGR channel order
baseImage = cv2.imread(inputImage)

print(np.shape(baseImage))

# take each channel of base image and create airy disk images

blueBaseChannel, greenBaseChannel, redBaseChannel = cv2.split(baseImage)

# mean = (1,)
#
# cov = [[1, 0], [0, 1]]
#
# x = np.random.multivariate_normal(mean, cov, airyDiskSize)

# TODO: create function for gaussian
# Initializing value of x-axis and y-axis
# in the range -1 to 1
x, y = np.meshgrid(np.linspace(-1, 1, pixelsPerOutputDisk),
                   np.linspace(-1, 1, pixelsPerOutputDisk))
dst = np.sqrt(x * x + y * y)

# Intializing sigma and muu
sigma = 1
muu = 0.000

# Calculating Gaussian array
gauss = np.exp(-((dst - muu)**2 / (2.0 * sigma**2)))


# create airyDisk area from one pixel value
def pixelToAiryDisks(pixelBrightness, gaussian, disksPerInputPixel):
    airyDisk = pixelBrightness * gaussian
    airyDiskPixelEquivalent = np.tile(airyDisk,
                                      [disksPerInputPixel, disksPerInputPixel])
    return airyDiskPixelEquivalent


# create airyDisk replacement for every pixel in channel
def airyDisksChannel(colorChannel, outputAiryChannel, gaussian,
                     disksPerInputPixel, pixelsPerOutputDisk):
    for rowIndex, row in enumerate(colorChannel):
        for columnIndex, brightnessValue in enumerate(row):
            outputRowIndex = rowIndex * outputScaleFactor
            outputColumnIndex = columnIndex * outputScaleFactor
            outputAiryChannel[outputRowIndex:outputRowIndex +
                              outputScaleFactor,
                              outputColumnIndex:outputColumnIndex +
                              outputScaleFactor] = pixelToAiryDisks(
                                  brightnessValue, gaussian,
                                  disksPerInputPixel)

    return outputAiryChannel


row, col = blueBaseChannel.shape
outputScaleFactor = disksPerInputPixel * pixelsPerOutputDisk
outputImage = np.ndarray((3, row * outputScaleFactor, col * outputScaleFactor),
                         dtype=np.uint8)

outputImageBlue, outputImageGreen, outputImageRed = outputImage

outputImageBlue = airyDisksChannel(blueBaseChannel, outputImageBlue, gauss,
                                   disksPerInputPixel, pixelsPerOutputDisk)

outputImage = np.dstack([outputImageBlue, outputImageGreen, outputImageRed])

cv2.imshow('image', outputImage)
cv2.imwrite('output.jpg', outputImage)
cv2.waitKey(0)

cv2.imshow('image', blueBaseChannel)
cv2.waitKey(0)

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
