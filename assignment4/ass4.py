import hsolver as hs


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

solution = hs.get_homography(old_points, new_points)

# The transformation matrix generates homogeneous coordinates
# If you divide by the last value (z-coordinate) you get
# reduced (normalized) homogeneous coordinates,
# that is, you get the appropriate (x', y').

print([x for x in solution]) # to get more decimals