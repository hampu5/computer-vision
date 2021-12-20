import numpy as np
import matplotlib.pyplot as plt

# def diffuse_light(light_intensity, angle_to_normal, surface_color, k_al):
#     return light_intensity * np.cos(angle_to_normal) * surface_color * k_al

# def phong(light_intensity, diffuse_light, specular_light, shininess, surface_color):
#     k_al = 1
#     k_dl = 1
#     k_sl = 1

def specular_light(light_intensity, angle_to_reflection, surface_color, shininess, k_al):
    return light_intensity * np.cos(angle_to_reflection)**shininess * k_al

fig = plt.figure()
 
ax = plt.axes(projection ='3d')
 
x = np.linspace(0, np.pi/2, 30)
y = np.linspace(0, 1, 30)
X, Y = np.meshgrid(x, y)
zs = np.array(specular_light(1, np.ravel(X), 1, np.ravel(Y), 1))
Z = zs.reshape(Y.shape)
 
ax.plot_surface(X, Y, Z)
ax.set_title('Phong lighting as function of angle and shininess')

ax.set_xlabel('Angle (x axis)')
ax.set_ylabel('Shininess (y axis)')
ax.set_zlabel('Specular light (z axis)')

plt.show()