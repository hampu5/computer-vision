import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

point1a = [2, 2]
point2a = [3, 1.15]
point3a = [6, 0]

numberArr = []
for i in range(50):
    numberArr.append(i)

theta = np.array(numberArr)
theta = theta * 2 * np.pi / theta.size

def getDistance(point, theta):
    return point[0] * np.cos(theta) + point[1] * np.sin(theta)

# Plot the points
plt.plot(point1a[0], point1a[1], marker='o')
plt.plot(point2a[0], point2a[1], marker='o')
plt.plot(point3a[0], point3a[1], marker='o')

distance1a = getDistance(point1a, theta)
distance2a = getDistance(point2a, theta)
distance3a = getDistance(point3a, theta)

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
        outR = min + diff / 2
        outTheta = i * 2 * np.pi / theta.size

crossPoint = [outTheta, outR]



# Plot the sine curves
plt.plot(theta, distance1a)
plt.plot(theta, distance2a)
plt.plot(theta, distance3a)

x = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

def getY(point, x):
    return point[1] / np.sin(point[0]) - x * (np.cos(point[0]) / np.sin(point[0]))

# Plot the line
plt.plot(x, getY(crossPoint, x))

plt.show()