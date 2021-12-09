import cv2 as cv
import numpy as np
import hsolver as hs
import ransac as r


img0 = cv.imread('book0.jpg', cv.IMREAD_GRAYSCALE)
img1 = cv.imread('book1.jpg', cv.IMREAD_GRAYSCALE)

rows, cols = img0.shape

# # Use OpenCV's implementation of Harris corner detection
# img0_fd = cv.cornerHarris(img0, 3, 3, 0.06)
# img1_fd = cv.cornerHarris(img1, 3, 3, 0.06)

# for i in range(rows):
#     for j in range(cols):
#         if img0_fd[i, j] > 0.0003:
#             cv.circle(img0, center=(j, i), radius=9, color=(255, 0, 0), thickness=1)
#         if img1_fd[i, j] > 0.0003:
#             cv.circle(img1, center=(j, i), radius=9, color=(255, 0, 0), thickness=1)

# cv.imshow("First image (img0)", img0)
# cv.imshow("Second image (img1)", img1)

# Chosen by hand (Did not find RANSAC)
fd0 = [[484, 16], [544, 25], [465, 86], [540, 68], [763, 88], [464, 310], [722, 261]]
fd1 = [[143, 39], [216, 40], [141, 115], [221, 83], [448, 72], [197, 351], [451, 239]]

H = hs.get_homography(fd0, fd1)

img0_warp = cv.warpPerspective(img0, H, (cols, rows))

def perspective_transformation(input, transformation_matrix):
    height, width = input.shape
    
    img_out = np.zeros((rows, cols), np.uint8)

    for i in range(width):
        for j in range(height):
            new_point = np.matmul(transformation_matrix, [i, j, 1])
            # print(new_point)
            x = int(np.around(new_point[1] / new_point[2]))
            y = int(np.around(new_point[0] / new_point[2]))

            if x >= 0 and x < height and y >= 0 and y < width:
                # print(i)
                img_out[x, y] = input[j, i]
    
    return img_out

img0_tr = perspective_transformation(img0, H)

cv.imshow("First image (img0)", img0)
cv.imshow("Second image (img1)", img1)
cv.imshow("Transformed with OpenCV", img0_warp)
cv.imshow("Transformed with my own function", img0_tr)

cv.waitKey(0)