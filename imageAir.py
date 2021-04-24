# read image from file

import numpy as np
import cv2

# TODO add image as argument
inputImage = "test.jpg"
airyDiskSize = (36, 36)

# Note: cv2 works in BGR channel order
baseImage = cv2.imread(inputImage)

print(np.shape(baseImage))

# take each channel of base image and create airy disk images

baseRedChannel = baseImage[:,:,0]
print(baseRedChannel)
firstBluePixel = baseImage.item(0,0,0)

# mean = (1,)
#
# cov = [[1, 0], [0, 1]]
#
# x = np.random.multivariate_normal(mean, cov, airyDiskSize)

# Initializing value of x-axis and y-axis
# in the range -1 to 1
x, y = np.meshgrid(np.linspace(-1,1,36), np.linspace(-1,1,36))
dst = np.sqrt(x*x+y*y)

# Intializing sigma and muu
sigma = 1
muu = 0.000

# Calculating Gaussian array
gauss = np.exp(-( (dst-muu)**2 / ( 2.0 * sigma**2 ) ) )

# print("2D Gaussian array :\n")
# print(gauss)
#
# print(firstBluePixel)

# normalise pixel brightness value
firstAiryDisk = gauss * firstBluePixel

# TODO: create airy disk image from all pixels

# print(firstAiryDisk)
#
# print(np.shape(firstAiryDisk))

# normalise befoew imshow. Don't know why...
# possibly because this is a 2D matrix, normally image is X x Y x B/G/R (3 channels)
cv2.imshow('image',firstAiryDisk/255)
cv2.waitKey(0)

cv2.imshow('image',baseRedChannel)
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
