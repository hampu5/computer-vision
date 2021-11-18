import cv2 as cv
import numpy as np

img = cv.imread('bird.jpg')
img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)


def kernel_avg(frame):
    kernel = np.array([
        [1, 1, 1],
        [1, 1, 1],
        [1, 1, 1]
    ])
    kernel = kernel * 1/9

    result = np.sum(np.multiply(frame, kernel))
    return result

def filter_blur_slow(img):
    rows, cols = img.shape
    out_img = np.zeros((rows - 2, cols - 2), np.uint8)
    i = 0
    while i < rows - 2:
        j = 0
        while j < cols - 2:
            frame = np.array([
                [img[i, j], img[i, j+1], img[i, j+2]],
                [img[i+1, j], img[i+1, j+1], img[i+1, j+2]],
                [img[i+2, j], img[i+2, j+1], img[i+2, j+2]]
            ])
            out_img[i, j] = kernel_avg(frame)
            j = j + 1
        i = i + 1
    return out_img


def kernel_blur_vec(frame):
    kernel = np.array([1, 1, 1])
    kernel = kernel * 1/3

    result = np.sum(np.multiply(frame, kernel))
    return result

def kernel_sharp_vec(frame):
    kernel = np.array([1, 1, 1])
    kernel = kernel * 1/3

    result = np.sum(np.multiply(frame, kernel))
    return frame[1] + 0.7 * (frame[1] - result)

def separable_filter(img, kernel):
    rows, cols = img.shape

    out_col = np.zeros((rows - 2, cols), np.uint8)
    i = 0
    while i < rows - 2:
        j = 0
        while j < cols:
            kernel_col = np.array([img[i, j], img[i + 1, j], img[i + 2, j]])
            out_col[i, j] = kernel(kernel_col)
            j = j + 1
        i = i + 1

    rows, cols = out_col.shape
    # cv.imshow('Convolution with Column', out_col)

    out_row = np.zeros((rows, cols - 2), np.uint8)
    i = 0
    while i < rows:
        j = 0
        while j < cols - 2:
            kernel_row = [out_col[i, j], out_col[i, j + 1], out_col[i, j + 2]]
            out_row[i, j] = kernel(kernel_row)
            j = j + 1
        i = i + 1

    return out_row


# out_img = filter_blur_slow(img)
out_img = separable_filter(img, kernel_sharp_vec)


cv.imshow('Original', img)
cv.imshow('Blurred', out_img)
cv.waitKey(0)
