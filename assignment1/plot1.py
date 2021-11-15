import matplotlib.pyplot as plt
import numpy as np
import math

width_smartphone = 1
width_camera = 2

focal_length = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

def get_fov(width, focal_length):
    return_array = []
    for val in focal_length:
        return_array.append( (2 * math.atan2(width, 2 * val)) * 180 / math.pi)
    return return_array

plt.plot(focal_length, get_fov(width_smartphone, focal_length), label='Smartphone camera')
plt.plot(focal_length, get_fov(width_camera, focal_length), label='Other camera (double sensor width')
plt.xlabel('Focal length')
plt.ylabel('Field of view (fov)')
plt.title('Fov of cameras with different sensor width')
plt.legend()
plt.show()