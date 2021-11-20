import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

point1a = [2, 2]
point2a = [3, 1.15] #[5, 3]
point3a = [6, 0]

# Create theta values
theta = np.arange(0, 2 * np.pi, 2 * np.pi / 50)
print(theta)

def getDistance(point, theta):
    return point[0] * np.cos(theta) + point[1] * np.sin(theta)

distance2a = getDistance(point2a, theta)
distance1a = getDistance(point1a, theta)
distance3a = getDistance(point3a, theta)

# Get the point where the curves intersect
diffCross = 100
outTheta = 0
outR = 0
for i in range(10):
    min = np.min([distance1a[i], distance2a[i], distance3a[i]])
    max = np.max([distance1a[i], distance2a[i], distance3a[i]])
    diff = max - min
    if diff < diffCross and min > 0:
        print(diff)
        diffCross = diff
        outTheta = i * 2 * np.pi / theta.size
        outR = min + diff / 2

crossPoint = [outTheta, outR]

x = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

def getY(point, x):
    return point[1] / np.sin(point[0]) - x * (np.cos(point[0]) / np.sin(point[0]))

# Plotting
fig, ax1 = plt.subplots()
plt.title('Sines in Hough space (color) and points/line in image space (black)')
ax1.set_ylabel('r (Hough space)')
ax1.set_xlabel('\u03B8 (Hough space) - x (image space)')
ax2 = ax1.twinx()
ax2.set_ylim(-4, 8)
ax2.set_xlim(0, 6.2)
ax2.set_ylabel('y (image space)')

# Plot the points in image space
ax2.plot(point1a[0], point1a[1], marker='o', color='black')
ax2.plot(point2a[0], point2a[1], marker='o', color='black')
ax2.plot(point3a[0], point3a[1], marker='o', color='black')

# Plot the sine curves in Hough space
ax1.plot(theta, distance1a)
ax1.plot(theta, distance2a)
ax1.plot(theta, distance3a)

# Plot the line in image space
ax2.plot(x, getY(crossPoint, x), color='black')

plt.show()