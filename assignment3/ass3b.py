import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from numpy.core.fromnumeric import amax
from sklearn import preprocessing as pp



def harris_detector(img_gradient_x, img_gradient_y):
    # Actual size is 2 * window_size + 1
    window_size = 4

    # Calculate elements of the structure tensor (H)
    h00 = 0
    h11 = 0
    h01 = 0 # and h10
    for x in range(2 * window_size + 1):
        for y in range(2 * window_size + 1):
            h00 += int(img_gradient_x[x, y])**2
            h11 += int(img_gradient_y[x, y])**2
            h01 += int(img_gradient_x[x, y])*int(img_gradient_y[x, y])

    # Create the structure tensor (H)
    h = np.array([
        [h00, h01],
        [h01, h11]
    ])
    
    # Calculate determinant(H) and trace(H)
    h_det = h[0, 0]*h[1, 1] - h[0, 1]*h[1, 0] # np.linalg.det(h)
    # print(h_det)
    h_trace = h[0, 0] + h[1, 1] # np.trace(h)

    # Calculate the Harris operator
    r = h_det - 0.05 * h_trace**2



img_raw = cv.imread('pic2_small.jpg')
img_raw = cv.cvtColor(img_raw, cv.COLOR_BGR2GRAY)

cv.imshow('Original', img_raw)

img = cv.GaussianBlur(img_raw, ksize=(3, 3), sigmaX=2, sigmaY=2)

rows, cols = img.shape

# Get the gradients in x and y
img_gradient_x = cv.Sobel(img, cv.CV_64F, 1, 0)
img_gradient_x = np.absolute(img_gradient_x)
grad_x_max = np.amax(img_gradient_x)
img_gradient_x = np.uint8(255 * img_gradient_x / grad_x_max)

img_gradient_y = cv.Sobel(img, cv.CV_64F, 0, 1)
img_gradient_y = np.absolute(img_gradient_y)
grad_y_max = np.amax(img_gradient_y)
img_gradient_y = np.uint8(255 * img_gradient_y / grad_y_max)

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
        grad_x = int(img_gradient_x[i, j]) # / 100 # /40
        grad_y = int(img_gradient_y[i, j]) # / 100 # /40
        # print(grad_x**2 * grad_y**2 - grad_x*grad_y * grad_x*grad_y)

        h00 = 0
        h11 = 0
        h01 = 0 # and h10
        for x in range(2 * window_size + 1):
            for y in range(2 * window_size + 1):
                h00 += int(img_gradient_x[x, y])**2
                h11 += int(img_gradient_y[x, y])**2
                h01 += int(img_gradient_x[x, y])*int(img_gradient_y[x, y])

        # Create the H matrix
        h = np.array([
            [h00, h01],
            [h01, h11]
        ])
        
        # Calculate determinant(H) and trace(H)
        h_det = h[0, 0]*h[1, 1] - h[0, 1]*h[1, 0] # np.linalg.det(h)
        # print(h_det)
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

