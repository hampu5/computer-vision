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


def kmeans(points: list, centroids: list, iterations: int):
    k = len(centroids)
    dim = len(centroids[0])

    clusters = []
    for centroid in centroids:
        clusters.append([centroid, []])

    def assign_points():
        for i, centroid in enumerate(clusters):
            clusters[i][1] = []
            # print(clusters[i])
        
        for point in points:
            summed_squares = []
            for centroid, cluster in clusters:
                # Summed Square Difference of the coordinate components
                summed_square = 0
                for point_coord, centroid_coord in zip(point, centroid):
                    summed_square += (point_coord - centroid_coord)**2
                summed_squares.append(summed_square)
            
            # Find the index for the cluster center closest to the point
            min_ss = np.inf
            index = 0
            for i, ss in enumerate(summed_squares):
                if ss < min_ss:
                    min_ss = ss
                    index = i
            clusters[index][1].append(point)

        return clusters
        
    def calculate_centroids():
        for cluster in clusters:
            size = len(cluster[1])

            # Set all cluster centers to 0
            cluster[0] = []
            for i in range(dim):
                cluster[0].append(0)

            # Compute new cluster centers from the
            # points assigned to each cluster
            for point in cluster[1]:
                for i in range(dim):
                    cluster[0][i] += point[i] / size
    
    i = 0
    while i < iterations:
        assign_points()
        calculate_centroids()
        i += 1
    
    return clusters

# clusters = kmeans([x1, x2, x3, x4, x5, x6, x7, x8, x9, x10], [m1, m2], 2)

# print(clusters)