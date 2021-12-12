import cv2 as cv
import numpy as np

img0 = cv.imread('im0-400.jpg', cv.IMREAD_GRAYSCALE)
img1 = cv.imread('im1-400.jpg', cv.IMREAD_GRAYSCALE)

def err_abs(diff):
    return np.abs(diff)

def err_ssd(diff):
    return diff**2 / 255

def compute_window(img0, img1, i, j, shift, error_function):
    window_size = 5
    
    mat_row = []
    start_index = -int(np.floor(window_size / 2))
    row = start_index
    while row < window_size + start_index:
        mat_col = []
        col = 0
        while col < window_size + start_index:
            if i+row < 0 or i+row >= 274 or j+col < 0 or j+col >= 400 or j+shift+col < 0 or j+shift+col >= 400:
                calculation = 0
            else:
                calculation = error_function(img0[i + row, j + shift + col] - img1[i + row, j + col])
            mat_col.append(calculation)
            col += 1
        mat_row.append(mat_col)
        row += 1
    
    diff = np.sum(mat_row) / (window_size**2)
    return diff

def plane_sweep3(img0, img1, error_function):
    rows, cols = img0.shape
    diff_img = np.full((rows, cols), 255, np.float32)
    out_img = np.zeros((rows, cols), np.float32)
    img0 = np.array(img0, np.float32)
    img1 = np.array(img1, np.float32)

    block_size = 30
    for shift in range(0, cols, 5):
        if shift > block_size:
            break
        for i, rows in enumerate(diff_img):
            for j, elem in enumerate(rows):
                if j + shift >= cols:
                    break
                diff = compute_window(img0, img1, i, j, shift, error_function)
                if diff < elem:
                    diff_img[i, j] = diff
                    out_img[i, j] = shift / block_size
    
    return out_img

img_abs = plane_sweep3(img0, img1, err_abs)
img_ssd = plane_sweep3(img0, img1, err_ssd)

cv.imshow("Disparity image (abs)", img_abs)
cv.imshow("Disparity image (ssd)", img_ssd)

cv.waitKey(0)