import numpy as np
import copy

# x1 = np.array([0, 0.5])
# x2 = np.array([0, 0.76])
# x3 = np.array([1, 1])
# x4 = np.array([1.2, 0.4])
# x5 = np.array([1.5, 0.75])
# x6 = np.array([2.5, 1])
# x7 = np.array([3, 2])
# x8 = np.array([4, 1.5])
# x9 = np.array([4, 2.5])
# x10 = np.array([5, 2])

# m1 = np.array([1, 1.5])
# m2 = np.array([3, 1])


def kmeans(points: np.ndarray, centroids: np.ndarray, iterations: int):
    k = len(centroids)

    c = copy.deepcopy(centroids)
    c_size = np.zeros(k)

    labels = np.zeros(len(points), np.uint16)
    
    def assign_points():
        # Loop through all the points
        for p_i, point in enumerate(points):
            # Find the summed squared distances from the point
            # to the different centroids
            ssd_p_to_c = []
            for centroid in c:
                # Summed Square Difference
                ssd = np.sum(np.square(np.subtract(point, centroid)))
                ssd_p_to_c.append(ssd)
            
            # Find the index of the closest centroid
            closest_c_i = np.argmin(ssd_p_to_c)

            # Set the label for this point (p_i) to the index
            # of the closest centroid (closest_c_i)
            labels[p_i] = closest_c_i

            # Increment the size of the cluster with the closest centroid
            # by 1 (That is, count this point as member of that cluster)
            c_size[closest_c_i] += 1
        
    def calculate_centroids():
        # Set all centroids to 0
        for c_i, centroid in enumerate(c):
            c[c_i] = [0 for x in centroid]

        # Compute new cluster centroids
        for label, point in zip(labels, points):
            # Get the size of the cluster with index: label
            size = c_size[label]
            
            # Set the new centroids
            c[label] += point / size
    
    i = 0
    while i < iterations:
        assign_points()
        calculate_centroids()
        c_size = [0 for x in c_size]
        i += 1
    
    return labels, c

# labels, centers = kmeans(np.array([x1, x2, x3, x4, x5, x6, x7, x8, x9, x10]), np.array([m1, m2]), 2)

# print(centers)