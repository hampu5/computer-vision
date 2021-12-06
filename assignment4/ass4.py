import cv2 as cv
import numpy as np


# [x'] ~ [wx']   [a b c][x]   [ax + by + c]
# [y'] = [wy'] = [d e f][y] = [dx + ey + f]   =>
# [ 1]   [ w ]   [g h i][1]   [gx + hy + i]
#
# wx' = ax + by + c
# wy' = dx + ey + f   =>
#  w  = gx + hy + i
#
# (gx + hy + i)x' = ax + by + c
# (gx + hy + i)y' = dx + ey + f   =>
#
# gxx' + hyx' + ix' -ax -by -c = 0
# gxy' + hyy' + iy' -dx -ey -f = 0   =>
#
#               A                h     0
# [-x -y -1  0  0  0 xx' yx' x'][a]   [0]   One pair in A for
# [ 0  0  0 -x -y -1 xy' yy' y'][b] = [0]   each point we track
# [ .  .  .  .  .  .  .   .  . ][c]   [.]
# [ .  .  .  .  .  .  .   .  . ][d]   [.]
# [ .  .  .  .  .  .  .   .  . ][e]   [.]
#                               [f]
#                               [g]
#                               [h]
#                               [i]


x0 = [0, 0]
x1 = [0, 3]
x2 = [5, 3]
x3 = [5, 0]

_x0 = [1, 1]
_x1 = [3, 3]
_x2 = [6, 3]
_x3 = [5, 2]

old_points = [x0, x1, x2, x3]
new_points = [_x0, _x1, _x2, _x3]


def get_pair_in_a(old_point, new_point):
    return np.array([
        [-old_point[0], -old_point[1], -1, 0, 0, 0, old_point[0]*new_point[0], old_point[1]*new_point[0], new_point[0]],
        [0, 0, 0, -old_point[0], -old_point[1], -1, old_point[0]*new_point[1], old_point[1]*new_point[1], new_point[1]]
    ])

def get_a(old_points, new_points):
    out_A = []
    for old_point, new_point in zip(old_points, new_points):
        pair = get_pair_in_a(old_point, new_point)
        out_A.append(pair[0])
        out_A.append(pair[1])
    return out_A


A = get_a(old_points, new_points)

U, D, VT = np.linalg.svd(A)

V = np.transpose(VT)

solution = V[-1] # last column in V

print(solution)