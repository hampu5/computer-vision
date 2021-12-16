import numpy as np
import cv2 as cv
import kmeans as km

img = cv.imread('pic2_small.jpg')

row, col, color = img.shape

# Creating an extended image with x and y parameters as well
# img_extended = np.zeros((row, col, color))
# for x in range(row):
#     for y in range(col):
#         img_extended[x, y, 0] = img[x, y, 0]
#         img_extended[x, y, 1] = img[x, y, 1]
#         img_extended[x, y, 2] = img[x, y, 2]
#         img_extended[x, y, 3] = x
#         img_extended[x, y, 4] = y


# Reshaping before putting into kmeans()
img = np.reshape(img, (-1, color))

centroids = [
    [20, 15 , 8],
    [200, 70, 50],
    [200, 200, 200]]

labels, centers = km.kmeans(img, centroids, 5)

# Recoloring the image from the labels, using the centers
for i, (pixel, label) in enumerate(zip(img, labels)):
    img[i] = centers[label]

# Reshaping the image again before showing
img = np.reshape(img, (row, col, color))

cv.imshow('Image', img)
cv.waitKey(0)