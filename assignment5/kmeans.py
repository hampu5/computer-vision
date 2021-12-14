import numpy as np

x1 = [0, 0.5]
x2 = [0, 0.76]
x3 = [1, 1]
x4 = [1.2, 0.4]
x5 = [1.5, 0.75]
x6 = [2.5, 1]
x7 = [3, 2]
x8 = [4, 1.5]
x9 = [4, 2.5]
x10 = [5, 2]

m1 = [1, 1.5]
m2 = [3, 1]

cluster_m1 = []
cluster_m2 = []

def assign_points(points, centers):
    for point in points:
        summed_squares = []
        for center in centers:
            summed_square = 0
            for point_coord, center_coord in zip(point, center):
                summed_square += (point_coord - center_coord)**2
            summed_squares.append(summed_square)
        if summed_squares[0] > summed_squares[1]:
            cluster_m1.append(point)
            if point in cluster_m2:
                cluster_m2.remove(point)
        else:
            cluster_m2.append(point)
            if point in cluster_m1:
                cluster_m1.remove(point)

def calculate_centroids():
    m1_new = [0, 0]
    m2_new = [0, 0]
    for point in cluster_m1:
        m1_new[0] += point[0]
        m1_new[1] += point[1]
    
    for point in cluster_m2:
        m2_new[0] += point[0]
        m2_new[1] += point[1]
    
    m1[0] = m1_new[0] / len(cluster_m1)
    m1[1] = m1_new[1] / len(cluster_m1)

    m2[0] = m2_new[0] / len(cluster_m2)
    m2[1] = m2_new[1] / len(cluster_m2)

assign_points([x1, x2, x3, x4, x5, x6, x7, x8, x9, x10], [m1, m2])
calculate_centroids()

assign_points([x1, x2, x3, x4, x5, x6, x7, x8, x9, x10], [m1, m2])
calculate_centroids()

print(cluster_m1)
print(cluster_m2)