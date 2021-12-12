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
                diff = img1[i, j] - img0[i, disparity]
                if diff < min_diff:
                    min_diff = diff
                    print(diff)
                    true_disp = j - disparity # or -k
                j += 1
            out_img[i, disparity] = true_disp
            i += 1
        disparity += 1
        # print(disparity)
    out_img = out_img / np.amax(out_img)
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

img_d = plane_sweep2(img0, img1)

cv.imshow("Disparity image", img_d)

cv.waitKey(0)