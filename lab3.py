import random
from manonox import Point


def _collect_clusters_from_assignments(cluster_count, assignments):
    clusters = [[] for i in range(cluster_count)]
    for point, cluster_index in assignments.items():
        clusters[cluster_index].append(point)
    return clusters

def _calculate_centroids(cluster_count, assignments):
    clusters = _collect_clusters_from_assignments(cluster_count, assignments)
    return [Point.centroid(cluster) for cluster in clusters]

def k_means(points, cluster_count):
    assignments = {}
    for point in points:
        cluster_index = random.randint(0, cluster_count - 1)
        assignments[point] = cluster_index
    
    centroids = _calculate_centroids(cluster_count, assignments)
    
    changed = True
    while changed:
        changed = False
        for point in points:
            current_assignment = assignments[point]
            new_assignment = sorted(
                enumerate(centroids),
                key=lambda centroid: point.distance(centroid[1], "euclid_squared") if centroid[1] != None else 9999999999
            )[0][0]
            
            if current_assignment != new_assignment:
                changed = True
                assignments[point] = new_assignment
        centroids = _calculate_centroids(cluster_count, assignments)
    
    return _collect_clusters_from_assignments(cluster_count, assignments), assignments, centroids



if __name__ == "__main__":
    import pandas as pd
    import math

    data = pd.read_csv('data/fastfood.csv')
    l = list(data.columns.values)
    meta = l[:2]
    properties = l[2:-1]

    points = []
    for row in data.itertuples():
        kwargs = {}
        for property in properties:
            value = getattr(row, property)
            if math.isnan(value):
                value = 0
            kwargs[property] = value
        point = Point(**kwargs)
        for meta_key in meta:
            point.add_meta(meta_key, getattr(row, meta_key))
        points.append(point)
    
    clusters, assignments, centroids = k_means(points, 20)

    for i, cluster in enumerate(clusters):
        centroid = centroids[i]
        if centroid == None:
            print(f"Cluster #{i} (0 points)")
            continue
        print(f"Cluster #{i} ({len(cluster)} points)\n\tCenter:")
        for property, value in centroid.properties.items():
            print(f"\t\t{property} = {value}")
        print("\tMembers:")
        for point in cluster:
            print(f"\t\t{point.get_meta('restaurant')}, {point.get_meta('item')}")
    
    print()
    print()
    print()

    low_fat_cluster = sorted(enumerate(clusters), key=lambda x: centroids[x[0]].cal_fat if centroids[x[0]] else 100000000)[0][1]
    print("Low fat items:")
    for point in low_fat_cluster:
        print(f"\t{point.get_meta('restaurant')}, {point.get_meta('item')}, {point.cal_fat}cal")
    
