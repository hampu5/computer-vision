import cv2 as cv
import numpy as np
from numpy.lib.function_base import disp

img0 = cv.imread('im0-400.jpg', cv.IMREAD_GRAYSCALE)
img1 = cv.imread('im1-400.jpg', cv.IMREAD_GRAYSCALE)

rows, cols = img0.shape

def plane_sweep(img0, img1):
    rows, cols = img0.shape
    out_img = np.zeros((rows, cols), np.float32)
    disparity = 0
    while disparity < cols:
        i = 0
        while i < rows:
            j = disparity
            while j < cols:
                min_diff = np.inf
                k = 0
                while k < cols - disparity:
                    diff = img1[i, k] - img0[i, j]
                    if diff < min_diff:
                        min_diff = diff
                        true_disp = disparity
                        out_img[i, j] = true_disp
                    k += 1
                j += 1
            i += 1
        disparity += 1
        print(disparity)
    return out_img

def plane_sweep2(img0, img1):
    rows, cols = img0.shape
    out_img = np.zeros((rows, cols), np.float32)
    disparity = 0
    
    while disparity < cols:

        i = 0
        while i < rows:
            min_diff = np.inf
            true_disp = 0

            j = disparity
            while j < cols: # - disparity:
                diff = img1[i, disparity] - img0[i, j]

                if diff < min_diff:
                    min_diff = diff
                    # print(diff)
                    true_disp = j - disparity # or -k
                
                j += 1
            
            out_img[i, disparity] = true_disp
            i += 1
        
        disparity += 1
        # print(disparity)
    
    out_img = out_img / np.amax(out_img)
    return out_img

def compute_window(img0, img1, i, j, shift):
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
                calculation = np.abs(img0[i + row, j + shift + col] - img1[i + row, j + col])
            mat_col.append(calculation)
            col += 1
        mat_row.append(mat_col)
        row += 1
    
    diff = np.sum(mat_row) / (window_size**2)
    return diff
        

def plane_sweep3(img0, img1):
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
                # if j < shift:
                #     continue
                if j + shift >= cols:
                    break
                # diff = np.abs(img0[i, j + shift] - img1[i, j])
                diff = compute_window(img0, img1, i, j, shift)
                # print(diff)
                if diff < elem:
                    diff_img[i, j] = diff
                    # print(shift/block_size)
                    out_img[i, j] = shift / block_size
    
    # out_img = out_img / np.amax(out_img)
    return out_img
            


def stereo_match(img0, img1):
    rows, cols = img0.shape
    img_d = np.zeros((rows, cols), np.float32)
    counter = 0
   
    # a b c
    # d e f
    # g h i
    # Loops through the rows in img0
    for i, row0 in enumerate(img0):
        if i > rows-3:
            break
        # Loops through the elements in the rows of img0
        for j, pixel0 in enumerate(row0):
            if j > cols-3:
                break
            min = np.inf
            min_disparity = 0
            # <            j                   >
            # <        k       k               > Z = f * (B/d)
            # Loops through the elements in the rows of img1
            for k, pixel1 in enumerate(img1[i]):
                if k > cols-3:
                    break
                if k < j - 30 or k > j + 5:
                    # ssds.append(255)
                    continue
                diff = [
                    (img1[i, k] - img0[i, j])**2, (img1[i, k+1] - img0[i, j+1])**2, (img1[i, k+2] - img0[i, j+2])**2,
                    (img1[i+1, k] - img0[i+1, j])**2, (img1[i+1, k+1] - img0[i+1, j+1])**2, (img1[i+1, k+2] - img0[i+1, j+2])**2,
                    (img1[i+2, k] - img0[i+2, j])**2, (img1[i+2, k+1] - img0[i+2, j+1])**2, (img1[i+2, k+2] - img0[i+2, j+2])**2
                ]
                ssd = np.sum(diff)
                if ssd < min:
                    min = ssd
                    min_disparity = k - j
            # min = np.amin(ssds)
            # print(min)
            img_d[i+1, j+1] = np.abs(min_disparity)
        print(counter)
        counter += 1
    img_d = img_d / np.amax(img_d)
    return img_d

img_d = plane_sweep3(img0, img1)

cv.imshow("Disparity image", img_d)

cv.waitKey(0)