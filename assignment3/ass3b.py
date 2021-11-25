#harris detector = f = det(H) - alpha * trace(H)

import cv2 as cv
import numpy as np

img = cv.imread('pic1_small.jpg')
img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

rows, cols = img.shape

img_gradient_x = cv.Sobel(img, cv.CV_32F, 0, 1)
img_gradient_y = cv.Sobel(img, cv.CV_32F, 1, 0)
# cv.imshow('Gradient x-axis', img_gradient_x)
# cv.imshow('Gradient y-axis', img_gradient_y)
cv.imshow('Original', img)

# Actual size is 2 * window_size + 1
window_size = 1

out_img = np.zeros((rows, cols), np.uint8)
i = 0 + window_size
while i < rows - window_size:
    j = 0 + window_size
    while j < cols - window_size:
        frame = np.array([])
        a = 0
        b = 0
        c = 0
        for x in range(-window_size, window_size + 1):
            for y in range(-window_size, window_size + 1):
                grad_x = img_gradient_x[i + x, j + y] / 255
                grad_y = img_gradient_y[i + x, j + y] / 255
                
                a += grad_x**2
                b += grad_y**2
                c += grad_x * grad_y



        lambda_max = 0.5 * (a + c + np.sqrt(b**2 + (a-c)**2))
        lambda_min = 0.5 * (a + c - np.sqrt(b**2 + (a-c)**2))
        
        r = lambda_max*lambda_min - 0.05 * (lambda_max + lambda_min)**2
        
        if r > 20:
            out_img[i, j] = 255

        # if np.abs(r) < 50:
        #     out_img[i, j] = 0
        # elif r < 0:
        #     out_img[i, j] = 127
        # elif np.abs(r) > 50:
        #     out_img[i, j] = 255
        

        # frame = np.array([
        #     [img[i, j], img[i, j+1], img[i, j+2]],
        #     [img[i+1, j], img[i+1, j+1], img[i+1, j+2]],
        #     [img[i+2, j], img[i+2, j+1], img[i+2, j+2]]
        # ])
        # A = np.array([
        #     [img[i, j]]
        # ])
        
        j = j + 1
    i = i + 1

cv.imshow('R-values', out_img)
cv.waitKey(0)