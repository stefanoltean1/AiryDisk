# read image from file

import numpy as np
import cv2
from AiryLib import *


def main():

    # TODO add arguments
    # Configuration parameters
    inputImage = "test.jpg"
    pixelsPerAiryDisk = 8  # array size for one airy disk

    # the 3 R,G,B "airy disk"/"PSF" “wavelengths” in um/micron (default being 0.455, 0.520 and 0.625 respectively)
    # wavelengths in um
    blueWavelength_um = 0.625
    greenWavelength_um = 0.455
    redWavelength_um = 0.520

    # camera properties
    # assume image captured by camera is same size as aperture
    fStopValue = 1.5  #unitless
    focalLength_mm = 30  #mm
    apertureDiameter_mm = focalLength_mm / fStopValue  #mm

    # airy disk diameters in um
    blueAiryDiskDiameter_um = 2.44 * blueWavelength_um * fStopValue
    greenAiryDiskDiameter_um = 2.44 * greenWavelength_um * fStopValue
    redAiryDiskDiameter_um = 2.44 * redWavelength_um * fStopValue

    print('Disk diameter values (BGR):', blueAiryDiskDiameter_um,
          greenAiryDiskDiameter_um, redAiryDiskDiameter_um)

    # outputImage properties
    outPutImageSize = 500  #10000x10000 pixels
    outputPixelSize_mm = apertureDiameter_mm / outPutImageSize
    outputPixelSize_um = outputPixelSize_mm * 1000

    print('Output pixel size:', outputPixelSize_um)

    # Airy Disk pixel size
    blueAiryDisksNumber = int(blueAiryDiskDiameter_um / outputPixelSize_um)
    if blueAiryDisksNumber < 1:
        blueAiryDisksNumber = 1
    greenAiryDisksNumber = int(greenAiryDiskDiameter_um / outputPixelSize_um)
    if greenAiryDisksNumber < 1:
        greenAiryDisksNumber = 1
    redAiryDisksNumber = int(redAiryDiskDiameter_um / outputPixelSize_um)
    if redAiryDisksNumber < 1:
        redAiryDisksNumber = 1

    # Note: cv2 works in BGR channel order
    baseImage = cv2.imread(inputImage)

    print(np.shape(baseImage))

    # take each channel of base image and create airy disk images
    blueBaseChannel, greenBaseChannel, redBaseChannel = cv2.split(baseImage)

    # original image size
    row, col = blueBaseChannel.shape

    # Gaussian distribution to simulate Airy Disk
    gaussian = genAiryDiskGaussian(pixelsPerAiryDisk)

    # use outputScaleFactor to create a large image to fill with airy disks
    # use the max pixel size
    outputScaleFactor = pixelsPerAiryDisk * max(
        blueAiryDisksNumber, greenAiryDisksNumber, redAiryDisksNumber)

    # array for output image -- all channels
    # TODO: investigate memory optimization to work with larger parameters/images
    # TODO: investigate batch processing (store data on harddrive)
    outputImage = np.ndarray(
        (3, row * outputScaleFactor, col * outputScaleFactor), dtype=np.uint8)

    # split output array into channels
    blueOutputImage, greenOutputImage, redOutputImage = outputImage

    # add Airy disks to each channel
    # scale factor used to resize image based on the size of Airy Disk for each
    # wavelength
    print('Processing Blue')
    blueScaleFactor = blueAiryDisksNumber * pixelsPerAiryDisk
    blueDimOutput = (col * blueScaleFactor, row * blueScaleFactor)
    blueOutputImage = cv2.resize(blueOutputImage, blueDimOutput)
    blueOutputImage = airyDisksChannel(blueBaseChannel, blueOutputImage,
                                       gaussian, blueAiryDisksNumber,
                                       pixelsPerAiryDisk, blueScaleFactor)

    print('Processing Green')
    greenScaleFactor = greenAiryDisksNumber * pixelsPerAiryDisk
    greenDimOutput = (col * greenScaleFactor, row * greenScaleFactor)
    greenOutputImage = cv2.resize(greenOutputImage, greenDimOutput)
    greenOutputImage = airyDisksChannel(greenBaseChannel, greenOutputImage,
                                        gaussian, greenAiryDisksNumber,
                                        pixelsPerAiryDisk, greenScaleFactor)

    print('Processing Red')
    redScaleFactor = redAiryDisksNumber * pixelsPerAiryDisk
    redDimOutput = (col * redScaleFactor, row * redScaleFactor)
    redOutputImage = cv2.resize(redOutputImage, redDimOutput)
    redOutputImage = airyDisksChannel(redBaseChannel, redOutputImage, gaussian,
                                      redAiryDisksNumber, pixelsPerAiryDisk,
                                      redScaleFactor)

    # resize all output images to minimum size before stacking them
    minScaleFactor = min(blueScaleFactor, greenScaleFactor, redScaleFactor)
    finalImageSize = (col * minScaleFactor, row * minScaleFactor)
    blueOutputImage = cv2.resize(blueOutputImage, finalImageSize)
    greenOutputImage = cv2.resize(greenOutputImage, finalImageSize)
    redOutputImage = cv2.resize(redOutputImage, finalImageSize)

    # merge channels to new Airy image
    outputImage = np.dstack(
        [blueOutputImage, greenOutputImage, redOutputImage])

    # output result
    cv2.imwrite('output.jpg', outputImage)


if __name__ == "__main__":
    # TODO: add commant line parameters
    main()
