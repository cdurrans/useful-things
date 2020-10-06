import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2
import os
from PIL import Image


def binarize_image(img_path, target_path, threshold):
    """Binarize an image."""
    image_file = Image.open(img_path)
    image = image_file.convert('L')  # convert image to monochrome
    image = numpy.array(image)
    image = binarize_array(image, threshold)
    imsave(target_path, image)


def binarize_array(numpy_array, threshold=200):
    """Binarize a numpy array."""
    for i in range(len(numpy_array)):
        for j in range(len(numpy_array[0])):
            if numpy_array[i][j] > threshold:
                numpy_array[i][j] = 255
            else:
                numpy_array[i][j] = 0
    return numpy_array


def hist(img, axis):
    histogram = np.sum(img, axis=axis)
    return histogram


def getIndicesForTopValuesEveryX(histData, everyX, expectedSections=None):
    """
    Input: given numpy array 
    Process: Find top values for every xth number within an expected number of sections
    output: indices of top values
    """
    if expectedSections == None:
        expectedSections = int(histData.shape[0]/everyX)
    top_nums = []
    for x in range(expectedSections):
        startValue = x*everyX
        results = np.argsort(histData[startValue:(x+1)*everyX])[-1:]
        results += startValue
        top_nums.append(results[0])
    return top_nums


def returnSection(img,sectionIndices,sectionWanted,buffer,verticalOrHorizontal):
    startIndx = sectionIndices[0+sectionWanted]-buffer
    try:
        endIndx = sectionIndices[sectionWanted+1]-buffer
    except IndexError:
        endIndx = len(img)-1
    if verticalOrHorizontal.lower() == 'vertical':
        sectionSeperated = img[:,startIndx:endIndx]
    elif verticalOrHorizontal.lower() == 'horizontal':
        sectionSeperated = img[startIndx:endIndx,:]
    else:
        print("Please enter either vertical or horizontal for verticalOrHorizontal")
        raise ValueError
    return sectionSeperated
    

def movingAverageHistData(data,rangeToSmooth):
    dataCopy = data.copy()
    for x in range(len(dataCopy)):
        try:
            dataCopy[x] = dataCopy[x-rangeToSmooth:x+rangeToSmooth+1].mean()
        except Exception as ex:
            print(ex)
    return dataCopy


def findMiddleOfZeroSections(imgHist):
    lenImage = len(imgHist)
    increaseAmt = 1
    indx = 0
    avgZone = []
    avgZoneCalc = []
    while indx < lenImage:
        if imgHist[indx] == 0:
            avgZoneCalc.append(indx)
            if increaseAmt < 5:
                increaseAmt += 1
        else:
            if avgZoneCalc:
                avgZone.append(int(np.array(avgZoneCalc).mean()))
            avgZoneCalc = []
            increaseAmt = 1
        indx += increaseAmt
    return avgZone


img = mpimg.imread('C:/users/cdurrans/Downloads/BARRY KEVIN DAHLIN - People - 2018-02-28 (1)-0.jpg')
grayImage = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
(thresh, blackAndWhiteImage) = cv2.threshold(grayImage, 127, 255, cv2.THRESH_BINARY)

blackAndWhiteImage[blackAndWhiteImage > 200] = 1
blackAndWhiteImage[blackAndWhiteImage == 0] = 2
blackAndWhiteImage[blackAndWhiteImage == 1] = 0

plt.imshow(blackAndWhiteImage)
plt.show()

histData = hist(blackAndWhiteImage, 0)

sections = getIndicesForTopValuesEveryX(histData, 700)

sectionSep = returnSection(blackAndWhiteImage,sections,2,15,'vertical')
plt.imshow(sectionSep)
plt.show()

smoothed = sectionSep.copy()

histSmoothed = hist(smoothed,1)

smoothTest = movingAverage(histSmoothed,8)
plt.plot(smoothTest)
plt.show()

avgZoneSm = findMiddleOfZeroSections(smoothTest)
print(avgZoneSm)
plt.plot(smoothTest)
plt.show()

for x in range(len(avgZoneSm)):
    secx = returnSection(smoothed,avgZoneSm,x,0,'horizontal')
    plt.imshow(secx)
    plt.show()

for x in range(len(avgZoneSm)):
    secx = returnSection(grayImage,avgZoneSm,x,0,'horizontal')
    plt.imshow(secx)
    plt.show()





