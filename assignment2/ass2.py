import cv2 as cv
import numpy as np

img = cv.imread('bird.jpg')
img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

def kernel_avg(kernel):
    a = kernel[0][0]
    b = kernel[0][1]
    c = kernel[0][2]
    d = kernel[1][0]
    e = kernel[1][1]
    f = kernel[1][2]
    g = kernel[2][0]
    h = kernel[2][1]
    i = kernel[2][2]
    avg = np.int_(a/9+b/9+c/9+d/9+e/9+f/9+g/9+h/9+i/9)
    return avg

def kernel_vec_avg(kernel):
    a = kernel[0]
    b = kernel[1]
    c = kernel[2]
    avg = np.int_(a/3+b/3+c/3)
    return avg

def filter_blur_slow(img):
    rows, cols = img.shape
    out_img = np.zeros((rows - 2, cols - 2), np.uint8)
    i = 0
    while i < rows - 2:
        j = 0
        while j < cols - 2:
            kernel = [
                [img[i, j], img[i+1, j], img[i+2, j]],
                [img[i, j+1], img[i+1, j+1], img[i+2, j+1]],
                [img[i, j+2], img[i+1, j+2], img[i+2, j+2]]
            ]
            out_img[i, j] = kernel_avg(kernel)
            j = j + 1
        i = i + 1
    return out_img

def filter_blur_fast_2step(img):
    rows, cols = img.shape

    out_col = np.zeros((rows - 2, cols), np.uint8)
    i = 0
    while i < rows - 2:
        j = 0
        while j < cols - 2:
            kernel_col = [img[i, j], img[i + 1, j], img[i + 2, j]]
            out_col[i, j] = kernel_vec_avg(kernel_col)
            j = j + 1
        i = i + 1

    rows, cols = out_col.shape
    # cv.imshow('Convolution with Column', out_col)

    out_row = np.zeros((rows, cols - 2), np.uint8)
    i = 0
    while i < rows - 2:
        j = 0
        while j < cols - 2:
            kernel_row = [out_col[i, j], out_col[i, j + 1], out_col[i, j + 2]]
            out_row[i, j] = kernel_vec_avg(kernel_row)
            j = j + 1
        i = i + 1

    return out_row

# out_img = filter_blur_slow(img)
out_img = filter_blur_fast_2step(img)


# cv.imshow('Original', img)
# cv.imshow('Blurred', out_img)
# cv.waitKey(0)
