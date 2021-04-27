import numpy as np
import cv2


# Print iterations progress
def printProgressBar(iteration,
                     total,
                     prefix='',
                     suffix='',
                     decimals=1,
                     length=100,
                     fill='█',
                     printEnd="\r"):
    percent = ("{0:." + str(decimals) + "f}").format(
        100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()


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
def airyDisksChannel(colorBaseChannel, outputAiryChannel, gaussian,
                     disksPerInputPixel, pixelsPerAiryDisk, scaleFactor):
    totalRows, cols = colorBaseChannel.shape
    printProgressBar(0,
                     totalRows,
                     prefix='Progress:',
                     suffix='Complete',
                     length=50)
    for rowIndex, row in enumerate(colorBaseChannel):
        for columnIndex, brightnessValue in enumerate(row):
            outputRowIndex = rowIndex * scaleFactor
            outputColumnIndex = columnIndex * scaleFactor
            outputAiryChannel[outputRowIndex:outputRowIndex + scaleFactor,
                              outputColumnIndex:outputColumnIndex +
                              scaleFactor] = pixelToAiryDisks(
                                  brightnessValue, gaussian,
                                  disksPerInputPixel)
            printProgressBar(rowIndex + 1,
                             totalRows,
                             prefix='Progress:',
                             suffix='Complete',
                             length=50)
    print('\n')
    return outputAiryChannel
