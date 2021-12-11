import cv2 as cv
import numpy as np

img0 = cv.imread('im0-400.jpg', cv.IMREAD_GRAYSCALE)
img1 = cv.imread('im1-400.jpg', cv.IMREAD_GRAYSCALE)

rows, cols = img0.shape

def stereo_match(img0, img1):
    rows, cols = img0.shape
    img_d = np.zeros((rows, cols), np.uint8)
    counter = 0
    for i, row0 in enumerate(img0):
        if i > rows-3:
            break
        for j, pixel0 in enumerate(row0):
            if j > cols-3:
                break
            ssds = []
            for k, pixel1 in enumerate(img1[i]):
                if k > cols-3:
                    break
                # diff = [
                #     (img1[i, k] - img0[i, j]), (img1[i, k+1] - img0[i, j+1]), (img1[i, k+2] - img0[i, j+2]),
                #     (img1[i+1, k] - img0[i+1, j]), (img1[i+1, k+1] - img0[i+1, j+1]), (img1[i+1, k+2] - img0[i+1, j+2]),
                #     (img1[i+2, k] - img0[i+2, j]), (img1[i+2, k+1] - img0[i+2, j+1]), (img1[i+2, k+2] - img0[i+2, j+2]),
                # ]
                # ssd = np.sum(diff)
                ssds.append(pixel1-pixel0)
            min = np.amin(ssds)
            # print(counter)
            # counter += 1
            img_d[i+1, j+1] = min
    return img_d

img_d = stereo_match(img0, img1)

cv.imshow("Disparity image", img_d)

cv.waitKey(0)