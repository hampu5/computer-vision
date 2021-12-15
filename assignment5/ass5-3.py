import numpy as np
import cv2 as cv
import kmeans as km

img = cv.imread('pic2_small.jpg')

row, col, color = img.shape

# Creating an extended image with x and y parameters as well
img_extended = np.zeros((row, col, 5))
for x in range(row):
    for y in range(col):
        img_extended[x, y, 0] = img[x, y, 0]
        img_extended[x, y, 1] = img[x, y, 1]
        img_extended[x, y, 2] = img[x, y, 2]
        img_extended[x, y, 3] = x
        img_extended[x, y, 4] = y

# Reshaping before putting into kmeans()
img_extended = np.reshape(img_extended, (-1, 5))
img = np.reshape(img, (-1, 5))

clusters = km.kmeans(img_extended, [[20, 15 , 8, 350, 200], [200, 70, 50, 60, 230], [200, 200, 200, 350, 350]], 10)

# out_img = np.reshape(img_extended, (row, col, color))
img = np.reshape(img, (row, col, color))

# From clusters, add points to the correct pixel places using their x and y parameters
for cluster in clusters:
    print(cluster[0])
    for point in cluster[1]:
        c = [cluster[0][0], cluster[0][1], cluster[0][2]]
        img[int(point[3]), int(point[4])] = c


cv.imshow('Image', img)
cv.waitKey(0)