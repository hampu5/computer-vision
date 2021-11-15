import matplotlib.pyplot as plt
import numpy as np
import math

width_smartphone = 1
width_camera = 2

focal_length = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

x1 = 1
x2 = 2
y = 1
z = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

def get_distances(point1, point2, z, focal_length):
    ipoint1 = np.array([point1[0]/(z*focal_length), point1[1]/(z*focal_length)])
    ipoint2 = np.array([point2[0]/(z*focal_length), point2[1]/(z*focal_length)])
    #distances.append(math.dist(ipoint1, ipoint2))
    print(ipoint1)
    distances = np.linalg.norm(ipoint1 - ipoint2)
    return distances

def get_distance_2d_z(point1, point2, z, focal_length):
    distance = []
    for val in z:
        ipoint1 = np.array([point1[0]/(val*focal_length), point1[1]/(val*focal_length)])
        ipoint2 = np.array([point2[0]/(val*focal_length), point2[1]/(val*focal_length)])
        distance.append(np.linalg.norm(ipoint1 - ipoint2))
    return distance

#point1 = get_image_point(x1, y, z, focal_length)
#point2 = get_image_point(x2, y, 4, focal_length)

#plt.plot(point1[0], point1[1], marker='o', label='x1 (-1, 1, 2)')
#plt.plot(point2[0], point2[1], marker='o', label='x2 (1, 1, 4)')

distances = get_distance_2d_z([x1, y], [x2, y], z, 2)

#plt.axes(projection='3d')
plt.plot(z, distances, marker='o')
# plt.xlim(-1, 1)
# plt.ylim(-1, 1)
plt.xlabel('focal length')
plt.ylabel('distance between points')
plt.title('Distance between points as function of focal length, depth = 2')
plt.legend()
plt.show()