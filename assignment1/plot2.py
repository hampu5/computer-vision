import matplotlib.pyplot as plt
import numpy as np
import math

focal_length = 1

x = 1
y = 1
z = 1

world_point1 = [x, y, z]
world_point2 = [x - 2, y, z]
world_point2_z = [x - 2, y, z + 1]

def get_image_point(point, focal_length):
    image_point = [focal_length * point[0] / point[2], focal_length * point[1] / point[2]]
    return image_point

image_point1 = get_image_point(world_point1, focal_length)
image_point2 = get_image_point(world_point2, focal_length)
image_point2_z = get_image_point(world_point2_z, focal_length)
image_point1_f = get_image_point(world_point1, focal_length - 0.5)
image_point2_z_f = get_image_point(world_point2_z, focal_length - 0.5)

plt.rcParams['figure.figsize'] = (9, 3)
plt.rcParams['legend.loc'] = 'lower left'

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, sharey=True)
fig.subplots_adjust(bottom=0.2)

ax1.plot(image_point1[0], image_point1[1], marker='o', label=f'WrldPt1 {world_point1}')
ax1.plot(image_point2[0], image_point2[1], marker='o', label=f'WrldPt2 {world_point2}')
ax1.plot(0, 0, marker='+', color='black')
ax1.set_title('Focal length = 1')
ax1.set_xlim(-1.5, 1.5)
ax1.set_ylim(-1.5, 1.5)
ax1.set_xlabel('x-axis (image space)')
ax1.set_ylabel('y-axis (image space)')
ax1.legend()

ax2.plot(image_point1[0], image_point1[1], marker='o', label=f'WrldPt1 {world_point1}')
ax2.plot(image_point2_z[0], image_point2_z[1], marker='o', label=f'WrldPt2 {world_point2_z}')
ax2.plot(0, 0, marker='+', color='black')
ax2.set_title('Focal length = 1')
ax2.set_xlim(-1.5, 1.5)
ax2.set_ylim(-1.5, 1.5)
ax2.set_xlabel('x-axis (image space)')
ax2.legend()

ax3.plot(image_point1_f[0], image_point1_f[1], marker='o', label=f'WrldPt1 {world_point1}')
ax3.plot(image_point2_z_f[0], image_point2_z_f[1], marker='o', label=f'WrldPt2 {world_point2_z}')
ax3.plot(0, 0, marker='+', color='black')
ax3.set_title('Focal length = 0.5')
ax3.set_xlim(-1.5, 1.5)
ax3.set_ylim(-1.5, 1.5)
ax3.set_xlabel('x-axis (image space)')
ax3.legend()

plt.show()