import cv2 as cv
import numpy as np
import argparse
import easygui
# Read image given by user
img_location = easygui.fileopenbox('Find the image in question.')
image = cv.imread(cv.samples.findFile(img_location))
if image is None:
    print('Could not open or find the image: ', img_location)
    exit(0)
new_image = np.zeros(image.shape, image.dtype)
alpha = 1.0 # Simple contrast control
beta = 0    # Simple brightness control
# Initialize values
print(' Basic Linear Transforms ')
print('-------------------------')
try:
    alpha = float(input('* Enter the alpha value [1.0-3.0]: '))
    beta = int(input('* Enter the beta value [0-100]: '))
except ValueError:
    print('Error, not a number')
# Do the operation new_image(i,j) = alpha*image(i,j) + beta
# Instead of these 'for' loops we could have used simply:
# new_image = cv.convertScaleAbs(image, alpha=alpha, beta=beta)
# but we wanted to show you how to access the pixels :)
for y in range(image.shape[0]):
    for x in range(image.shape[1]):
        for c in range(image.shape[2]):
            new_image[y,x,c] = np.clip(alpha*image[y,x,c] + beta, 0, 255)

# #gamma adjustment
# lookUpTable = np.empty((1,256), np.uint8)
#     for i in range(256):
#         lookUpTable[0,i] = np.clip(pow(i / 255.0, gamma) * 255.0, 0, 255)
#     res = cv.LUT(img_original, lookUpTable)

cv.imshow('Original Image', image)
cv.imshow('New Image', new_image)
# Wait until user press some key
cv.waitKey()