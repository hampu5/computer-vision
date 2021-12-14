import cv2 as cv
import numpy as np

img0_raw = cv.imread('obj0.jpg')
img1_raw = cv.imread('obj1.jpg')

img0 = cv.cvtColor(img0_raw, cv.COLOR_BGR2GRAY)
img1 = cv.cvtColor(img1_raw, cv.COLOR_BGR2GRAY)

img0_features = cv.goodFeaturesToTrack(
    img0,
    maxCorners=100,
    qualityLevel=0.3,
    minDistance=7,
    mask=None,
    blockSize=7)

img1_features, status, err = cv.calcOpticalFlowPyrLK(
    img0,
    img1,
    img0_features,
    0,
    winSize=(15, 15),
    maxLevel=2,
    criteria=(cv.TERM_CRITERIA_COUNT, 30, 0.01)) # cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 5, 0.01))

img0_points = img0_features[status == 1]
img1_points = img1_features[status == 1]

mask = np.zeros_like(img0_raw)

color = (200, 200, 200)

for i, (img0_p, img1_p) in enumerate(zip(img0_points, img1_points)):
    x0, y0 = img0_p.ravel()
    x1, y1 = img1_p.ravel()
    mask = cv.line(mask, (int(x1), int(y1)), (int(x0), int(y0)), color, 1)
    mask = cv.circle(mask, (int(x1), int(y1)), 5, color, 1)

out_img = cv.addWeighted(img0_raw, 0.3, img1_raw, 0.5, 1)
out_img = cv.subtract(out_img, mask)

cv.imshow("Lucas-Kanade Optical Flow", out_img)

cv.waitKey(0)