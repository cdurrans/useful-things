import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2
import os
from PIL import Image

def pltMultImg(images,titles=None):
    f, imagesPlts = plt.subplots(1, len(images), figsize=(20,10))
    for indx, im in enumerate(imagesPlts):
        if titles != None:
            assert len(images) == len(titles)
            im.title.set_text(titles[indx])
        im.imshow(images[indx])



img = mpimg.imread('test_images/test1.jpg')
img2 = mpimg.imread('test_images/test2.jpg')
img3 = mpimg.imread('test_images/test3.jpg')
pltMultImg([img,img2,img3],['1','2','3'])


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


img = mpimg.imread('C:/users/cdurrans/Downloads/BARRY KEVIN DAHLIN - People - 2018-02-28 (1)-0.jpg')
grayImage = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

(thresh, blackAndWhiteImage) = cv2.threshold(grayImage, 127, 255, cv2.THRESH_BINARY)

plt.imshow(blackAndWhiteImage)
plt.show()
blackAndWhiteImage[blackAndWhiteImage > 200] = 1
blackAndWhiteImage[blackAndWhiteImage == 0] = 2
blackAndWhiteImage[blackAndWhiteImage == 1] = 0


from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA
from sklearn.preprocessing import scale
from time import time
np.random.seed(42)

data = scale(blackAndWhiteImage)

xl = []
yl = []
for x in range(blackAndWhiteImage.shape[1]):
    for y in range(blackAndWhiteImage.shape[0]):
        if blackAndWhiteImage[y][x] == 2:
            xl.append(x)
            yl.append(y)

data = np.column_stack((xl, yl))

n_samples, n_features = data.shape
n_clusters_expected = 12


estimator = KMeans(init='k-means++', n_clusters=n_clusters_expected, n_init=10)

estimator.fit(data)

def bench_k_means(estimator, name, data):
    t0 = time()
    estimator.fit(data)
    print('%-9s\t%.2fs\t%i\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f'
          % (name, (time() - t0), estimator.inertia_,
             metrics.homogeneity_score(labels, estimator.labels_),
             metrics.completeness_score(labels, estimator.labels_),
             metrics.v_measure_score(labels, estimator.labels_),
             metrics.adjusted_rand_score(labels, estimator.labels_),
             metrics.adjusted_mutual_info_score(labels,  estimator.labels_),
             metrics.silhouette_score(data, estimator.labels_,
                                      metric='euclidean',
                                      sample_size=sample_size)))


# Step size of the mesh. Decrease to increase the quality of the VQ.
h = .2     # point in the mesh [x_min, x_max]x[y_min, y_max].

# Plot the decision boundary. For that, we will assign a color to each
x_min, x_max = data[:, 0].min() - 1, data[:, 0].max() + 1
y_min, y_max = data[:, 1].min() - 1, data[:, 1].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

# Obtain labels for each point in mesh. Use last trained model.
Z = estimator.predict(np.c_[xx.ravel(), yy.ravel()])

# Put the result into a color plot
Z = Z.reshape(xx.shape)
plt.figure(1)
plt.clf()
plt.imshow(Z, interpolation='nearest',
           extent=(xx.min(), xx.max(), yy.min(), yy.max()),
           cmap=plt.cm.Paired,
           aspect='auto', origin='lower')

plt.plot(data[:, 0], data[:, 1], 'k.', markersize=2)
# Plot the centroids as a white X
centroids = estimator.cluster_centers_
plt.scatter(centroids[:, 0], centroids[:, 1],
            marker='x', s=169, linewidths=3,
            color='w', zorder=10)
plt.title('K-means clustering on the digits dataset (PCA-reduced data)\n'
          'Centroids are marked with white cross')
plt.xlim(x_min, x_max)
plt.ylim(y_min, y_max)
plt.xticks(())
plt.yticks(())
plt.show()



