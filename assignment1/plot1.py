import matplotlib.pyplot as plt
import numpy as np

width_smartphone = 1
width_camera = 2

# Numbers from 1 to 10
focal_length = np.arange(1, 10+1)

def get_fov(width, focal_length):
    return_array = []
    for val in focal_length:
        return_array.append( (2 * np.atan2(width, 2 * val)) * 180 / np.pi)
    return return_array

plt.plot(focal_length, get_fov(width_smartphone, focal_length), label='Smartphone camera')
plt.plot(focal_length, get_fov(width_camera, focal_length), label='Other camera (double sensor width')
plt.xlabel('Focal length')
plt.ylabel('Field of view (fov)')
plt.title('Fov of cameras with different sensor width')
plt.legend()
plt.show()