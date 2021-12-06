import cv2 as cv
import numpy as np

x0 = [0, 0]
x1 = [0, 3]
x2 = [5, 3]
x3 = [5, 0]

xp0 = [1, 1]
xp1 = [3, 3]
xp2 = [6, 3]
xp3 = [5, 2]

old_points = [x0, x1, x2, x3]
new_points = [xp0, xp1, xp2, xp3]

def get_pair_in_a(old_point, new_point):
    out_matrix = np.array([
        [-old_points[0], -old_points[1], -1, 0, 0, 0, old_point[0]*new_point[0], old_point[0]*new_point[1], new_point[0]],

    ])

def get_a(old_points, new_points):


a = get_a(old_points, new_points)

d, u, vt = cv.SVDecomp(a)

v = np.transpose(vt)

solution = v[0] # equivalent of last column