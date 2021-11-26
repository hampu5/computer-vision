#harris detector = f = det(H) - alpha * trace(H)

import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from sklearn import preprocessing as pp

img = cv.imread('pic1_small.jpg')
img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

cv.imshow('Original', img)

rows, cols = img.shape

img_gradient_x = cv.Sobel(img, cv.CV_64F, 0, 1)
img_gradient_x = np.absolute(img_gradient_x)
img_gradient_x = np.uint8(img_gradient_x)
img_gradient_y = cv.Sobel(img, cv.CV_64F, 1, 0)
img_gradient_y = np.absolute(img_gradient_y)
img_gradient_y = np.uint8(img_gradient_y)
# img_gradient = cv.Sobel(img, cv.CV_64F, 1, 1)
cv.imshow('Gradient x-axis', img_gradient_x)
cv.imshow('Gradient y-axis', img_gradient_y)
# cv.imshow('Gradient', img_gradient)



# Actual size is 2 * window_size + 1
window_size = 4

out_img = np.zeros((rows, cols), np.uint8)
img_r = np.zeros((rows, cols), np.float64)
# out_img = np.zeros((rows, cols), np.float64)
i = 0 + window_size
while i < rows - window_size:
    j = 0 + window_size
    while j < cols - window_size:
        # frame = np.array([])
        a = 0
        b = 0
        c = 0
        # for x in range(-window_size, window_size + 1):
        #     for y in range(-window_size, window_size + 1):
        #         grad_x = int(img_gradient_x[i + x, j + y]) / 100 # /40
        #         grad_y = int(img_gradient_y[i + x, j + y]) / 100 # /40

        #         a += grad_x**2
        #         b += grad_y**2
        #         c += grad_x * grad_y
        #         # if c > 255: print(c)
        
        grad_x = float(img_gradient_x[i, j]) # / 100 # /40
        grad_y = float(img_gradient_y[i, j]) # / 100 # /40

        h = np.array([
            [grad_x**2, grad_x*grad_y],
            [grad_y*grad_x, grad_y**2]
        ])


        # lambda_max = 0.5 * (a + c + np.sqrt(4 * b**2 + (a-c)**2))
        # lambda_min = 0.5 * (a + c - np.sqrt(4 * b**2 + (a-c)**2))
        
        # r = lambda_max*lambda_min - 0.05 * (lambda_max + lambda_min)**2
        
        h_det = h[0, 0]*h[0, 1] - h[1, 0]*h[1, 1]  # np.linalg.det(h)
        h_trace = h[0, 0] + h[1, 1] # np.trace(h)

        r = h_det - 0.05 * h_trace**2
        
        img_r[i, j] = r
        # if np.abs(r) > 400000000:
        #     img_r[i, j] = 255
        #     # print(r)
        
        
        
        
        j = j + 1
    i = i + 1

max_r = np.amax(img_r)
print(max_r)

img_norm = 255 * img_r / max_r
img_markers = np.array(img)
for i in range(rows):
    for j in range(cols):
        if img_norm[i, j] > 200:
            cv.circle(img_markers, center=(j, i), radius=3, color=(255, 0, 0), thickness=1)

cv.imshow('Detected features', img_markers)

img_harris = cv.cornerHarris(img, 9, 3, 0.05) # Probably between 0 and 1

max_harr = np.amax(img_harris)
# max_harr = (max_harr + 1) / 2
print(max_harr)

img_norm_harr = 255 * img_harris / max_harr
for i in range(rows):
    for j in range(cols):
        if img_norm_harr[i, j] > 200:
            cv.circle(img, center=(j, i), radius=3, color=(255, 0, 0), thickness=1)

# img[img_harris > 0.01 * img_harris.max()] = 255
cv.imshow("OpenCV's Harris detector", img)

cv.waitKey(0)







# def kernel_blur_vec(frame):
#     return frame[0]/3 + frame[1]/3 + frame[2]/3

# # Use them Opposite if gradient in y-axis
# def kernel_sobel_col_x(frame):
#     result = frame[0] + frame[1]*2 + frame[2] # 1 2 1
#     # if result > 255: result = 255
#     # if result < 0: result = 0
#     result = result / 2
#     return result

# def kernel_sobel_row_x(frame):
#     result = frame[0] - frame[2] # +1 0 -1
#     # if result > 255: result = 255
#     # if result < 0: result = 0
#     return (result + 255) / 2

# def separable_filter(img, kernel1, kernel2):
#     rows, cols = img.shape

#     out_col = np.zeros((rows, cols), np.uint8)
#     i = 0
#     while i < rows - 2:
#         j = 0
#         while j < cols:
#             frame_col = np.array([img[i, j], img[i + 1, j], img[i + 2, j]])
#             value = kernel1(frame_col)
#             out_col[i+1, j] = value
#             j = j + 1
#         i = i + 1

#     rows, cols = out_col.shape
#     # cv.imshow('Convolution with Column-kernel', out_col)

#     out_row = np.zeros((rows, cols), np.uint8)
#     i = 0
#     while i < rows:
#         j = 0
#         while j < cols - 2:
#             frame_row = [out_col[i, j], out_col[i, j + 1], out_col[i, j + 2]]
#             value = kernel2(frame_row)
#             out_row[i, j+1] = value
#             j = j + 1
#         i = i + 1

#     out_row

#     return out_row

# # Smoothen image
# img_smooth = separable_filter(img, kernel_blur_vec, kernel_blur_vec)
# cv.imshow('Smooth', img_smooth)

# # Create gradients in x direction
# img_sobel_x = separable_filter(img_smooth, kernel_sobel_col_x, kernel_sobel_row_x)
# cv.imshow('Gradient x-direction', img_sobel_x)

# # Create gradients in y direction
# img_sobel_y = separable_filter(img_smooth, kernel_sobel_row_x, kernel_sobel_col_x)
# cv.imshow('Gradient y-direction', img_sobel_y)
