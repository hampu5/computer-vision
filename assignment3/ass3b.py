import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from sklearn import preprocessing as pp

img = cv.imread('pic2_small.jpg')
img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

cv.imshow('Original', img)

rows, cols = img.shape
print(rows)
print(cols)

# Get the gradients in x and y
img_gradient_x = cv.Sobel(img, cv.CV_64F, 1, 0)
img_gradient_x = np.absolute(img_gradient_x)
img_gradient_x = np.uint8(img_gradient_x)

img_gradient_y = cv.Sobel(img, cv.CV_64F, 0, 1)
img_gradient_y = np.absolute(img_gradient_y)
img_gradient_y = np.uint8(img_gradient_y)

cv.imshow('Gradient x-axis', img_gradient_x)
cv.imshow('Gradient y-axis', img_gradient_y)

# Actual size is 2 * window_size + 1
window_size = 4

out_img = np.zeros((rows, cols), np.uint8)
img_r = np.zeros((rows, cols), np.float64)
i = 0 + window_size
while i < rows - window_size: # Along a column
    j = 0 + window_size
    while j < cols - window_size: # Along a row
        grad_x = float(img_gradient_x[i, j]) # / 100 # /40
        grad_y = float(img_gradient_y[i, j]) # / 100 # /40

        # Create the H matrix
        h = np.array([
            [grad_x**2, grad_x*grad_y],
            [grad_y*grad_x, grad_y**2]
        ])
        
        # Calculate determinant(H) and trace(H)
        h_det = h[0, 0]*h[0, 1] - h[1, 0]*h[1, 1]  # np.linalg.det(h)
        h_trace = h[0, 0] + h[1, 1] # np.trace(h)

        # Calculate the Harris operator
        r = h_det - 0.05 * h_trace**2
        
        # Create a matrix with values from Harris operator
        img_r[i, j] = r

        j = j + 1
    i = i + 1

# Calculate the places where features are marked (detected)
max_r = np.amax(img_r)
img_norm = 255 * img_r / max_r
img_markers = np.array(img)
for i in range(rows):
    for j in range(cols):
        if img_norm[i, j] > 128:
            cv.circle(img_markers, center=(j, i), radius=3, color=(255, 0, 0), thickness=1)

cv.imshow('Detected features', img_markers)

# Use OpenCV's implementation of Harris corner detection
img_harris = cv.cornerHarris(img, 9, 3, 0.05) # Probably between 0 and 1

max_harr = np.amax(img_harris)
min_harr = np.amin(img_harris)
# max_harr = (max_harr + 1) / 2
img_norm_harr = np.uint8(255 * (img_harris + min_harr) / (max_harr + min_harr))
for i in range(rows):
    for j in range(cols):
        if img_norm_harr[i, j] > 200:
            cv.circle(img, center=(j, i), radius=3, color=(255, 0, 0), thickness=1)

cv.imshow("OpenCV's Harris detector", img)

cv.waitKey(0)