import matplotlib.pyplot as plt
import numpy as np
import math

width_smartphone = 1
width_camera = 2

focal_length = 0.5

x1 = -1
x2 = 1
y = 1
z = 2

def get_image_point(x, y, z_var, focal_length):
    image_point = [focal_length * x / z_var, focal_length * y / z_var]
    return image_point

point1 = get_image_point(x1, y, z, focal_length)
point2 = get_image_point(x2, y, 4, focal_length)

plt.plot(point1[0], point1[1], marker='o', label='x1 (-1, 1, 2)')
plt.plot(point2[0], point2[1], marker='o', label='x2 (1, 1, 4)')
plt.xlim(-1, 1)
plt.ylim(-1, 1)
plt.xlabel('x-axis')
plt.ylabel('y-axis')
plt.title('Projection of world-space points to image-space, focal lengt = 1')
plt.legend()
plt.show()