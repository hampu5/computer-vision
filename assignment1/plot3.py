import matplotlib.pyplot as plt
import numpy as np

focal_length = np.arange(1, 4)

x = 1
y = 1
z = np.arange(1, 11)

def get_distances_z(point1, point2, z, focal_length):
    distance = []
    for z_val in z:
        ipoint1 = np.array([focal_length * point1[0] / z_val, focal_length * point1[1] / z_val])
        ipoint2 = np.array([focal_length * point2[0] / z_val, focal_length * point2[1] / z_val])
        distance.append(np.linalg.norm(ipoint1 - ipoint2))
    return distance

def get_distances_fl(point1, point2, z, focal_length):
    distance = []
    for fl_val in focal_length:
        ipoint1 = np.array([fl_val * point1[0] / z, fl_val * point1[1] / z])
        ipoint2 = np.array([fl_val * point2[0] / z, fl_val * point2[1] / z])
        distance.append(np.linalg.norm(ipoint1 - ipoint2))
    return distance

distances_z = get_distances_z([x, y], [x - 2, y], z, 1)
distances_fl = get_distances_fl([x, y], [x - 2, y], 1, focal_length)

plt.rcParams['figure.figsize'] = (8, 4)

fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
# fig.subplots_adjust(hspace=0.7)

ax1.plot(z, distances_z)
ax1.set_xlabel('depth (z_value)')
ax1.set_ylabel('distance between points')

ax2.plot(focal_length, distances_fl)
ax2.set_xlabel('focal length')

plt.suptitle('Distance between points as function of depth and focal length')
plt.show()