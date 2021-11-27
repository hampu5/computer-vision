import cv2 as cv
import numpy as np


def corner_harris(img, window_size, sobel_aperture_size, k):
    out_mat = calc_covariance_matrix(img, window_size, sobel_aperture_size, k)
    assert(out_mat.dtype == np.float32)
    return out_mat


def calc_covariance_matrix(img, window_size, sobel_aperture_size, k):

    rows, cols = img.shape

    scale = np.float32((1 << ((sobel_aperture_size if sobel_aperture_size > 0 else 3) - 1)) * window_size)
    scale *= 255.0
    scale = 1.0 / scale

    assert(img.dtype == np.uint8)

    # Get the gradients in x and y
    img_gradient_x = cv.Sobel(img, cv.CV_32F, 1, 0, ksize=sobel_aperture_size, scale=scale)
    # img_gradient_x = np.absolute(img_gradient_x)
    # grad_x_max = np.amax(img_gradient_x)
    # img_gradient_x = np.uint8(255 * img_gradient_x / grad_x_max)

    img_gradient_y = cv.Sobel(img, cv.CV_32F, 0, 1, ksize=sobel_aperture_size, scale=scale)
    # img_gradient_y = np.absolute(img_gradient_y)
    # grad_y_max = np.amax(img_gradient_y)
    # img_gradient_y = np.uint8(255 * img_gradient_y / grad_y_max)
    
    covariance_matrix = np.zeros((rows, cols, 3), np.float32)

    for x in range(rows):
        for y in range(cols):
            dx = float(img_gradient_x[x, y])
            dy = float(img_gradient_y[x, y])
            
            covariance_matrix[x, y, 0] = dx*dx
            covariance_matrix[x, y, 1] = dx*dy
            covariance_matrix[x, y, 2] = dy*dy
    
    # covariance_matrix = cv.boxFilter(covariance_matrix, cv.CV_32F, (window_size, window_size))
    covariance_matrix = cv.GaussianBlur(covariance_matrix, ksize=(window_size, window_size), sigmaX=2, sigmaY=2)
    
    return calc_harris(covariance_matrix, k)


def calc_harris(covariance_matrix, k):
    rows, cols, channels = covariance_matrix.shape

    out_matrix = np.zeros((rows, cols), np.float32)

    for x in range(rows):
        for y in range(cols):
            a = covariance_matrix[x, y, 0]
            b = covariance_matrix[x, y, 1]
            c = covariance_matrix[x, y, 2]

            # Calculate determinant(H) and trace(H)
            h_det = a*c - b*b # np.linalg.det(h)
            h_trace = a + c # np.trace(h)
            r = h_det - k * h_trace * h_trace
            
            out_matrix[x, y] = r
    
    return out_matrix



img_raw = cv.imread('pic2_small.jpg')
img_raw = cv.cvtColor(img_raw, cv.COLOR_BGR2GRAY)

rows, cols = img_raw.shape

cv.imshow('Original', img_raw)


# Calculate the places where features are marked (detected)
img_r = corner_harris(img_raw, 3, 3, 0.06)
img_r = img_r * 81 # No idea why...

max_r = np.amax(img_r)
min_r = np.amin(img_r)
print(format(max_r, '.20f'))
print(format(min_r, '.20f'))

img_markers = np.array(img_raw)
for i in range(rows):
    for j in range(cols):
        if img_r[i, j] > 0.0005:
            cv.circle(img_markers, center=(j, i), radius=9, color=(255, 0, 0), thickness=1)

cv.imshow('Detected features', img_markers)


# Use OpenCV's implementation of Harris corner detection
img_harris = cv.cornerHarris(img_raw, 3, 3, 0.06)

max_harr = np.amax(img_harris)
min_harr = np.amin(img_harris)
print(format(max_harr, '.20f'))
print(format(min_harr, '.20f'))

for i in range(rows):
    for j in range(cols):
        if img_harris[i, j] > 0.0005:
            cv.circle(img_raw, center=(j, i), radius=9, color=(255, 0, 0), thickness=1)

cv.imshow("OpenCV's Harris detector", img_raw)

cv.waitKey(0)