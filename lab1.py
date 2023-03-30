import random
from manonox import Point
        
        
def __normalize_row(r):
    s = sum(r)
    for i in range(len(r)):
        r[i] /= s
    return r

def __generate_fcm_matrix(point_count, cluster_count):
    return [
        __normalize_row([random.uniform(0.0, 1.0) for _ in range(cluster_count)])
        for _ in range(point_count)
    ]

def __calculate_fcm_cost(points, centroids, matrix):
    sum = 0
    for point_index, point_relations in enumerate(matrix):
        for cluster_index, relation in enumerate(point_relations):
            centroid = centroids[cluster_index]
            point = points[point_index]
            sum += relation * centroid.distance(point) # , "manhattan"
    return sum

def __get_centroids(matrix, points, fuzziness):
    cluster_count = len(matrix[0])
    properties = points[0].properties.keys()
    centroids = []
    for cluster_index in range(cluster_count):
        init_kwargs = {}
        for property in properties:
            bottom = 0
            top = 0
            for point_index, point_relations in enumerate(matrix):
                relation = point_relations[cluster_index]
                relation_with_fuzziness = pow(relation, fuzziness)
                point = points[point_index]
                bottom += relation_with_fuzziness
                top += relation_with_fuzziness * point.properties[property]
            init_kwargs[property] = top / bottom
        centroids.append(Point(**init_kwargs))
    return centroids


def fcm(points, cluster_count, fuzziness = 1.5, eps = 0.1, max_cycles = 200):
    matrix = __generate_fcm_matrix(len(points), cluster_count)
    cost_previous = 0
    cost_current = 1
    cycle_count = 0
    centroids = None
    while cycle_count < max_cycles and abs(cost_current - cost_previous) > eps:
        cost_previous = cost_current
        centroids = __get_centroids(matrix, points, fuzziness)
        for point_index, point_relations in enumerate(matrix):
            point = points[point_index]
            for cluster_index, relation in enumerate(point_relations):
                distance = point.distance(centroids[cluster_index])
                new_relation = pow(1 / distance, 2 / (fuzziness - 1))
                point_relations[cluster_index] = new_relation
            __normalize_row(point_relations)
        cost_current = __calculate_fcm_cost(points, centroids, matrix)
        cycle_count += 1
    return matrix, centroids

if __name__ == "__main__":
    from matplotlib import pyplot as plot

    points = Point.generate(random.normalvariate, 1000, x=[0, 1], y=[0, 1])
    #points = Point.generate(random.uniform, 1000, x=[0, 1], y=[0, 1])

    relation_matrix, centroids = fcm(points, 3)
    
    plot.scatter("x", "y", c="c", s=5, data={
        "x": [p.x for p in points],
        "y": [p.y for p in points],
        "c": [tuple(point_relations) for point_relations in relation_matrix],
    })

    plot.scatter("x", "y", c="#00000033", s=2000, data={
        "x": [p.x for p in centroids],
        "y": [p.y for p in centroids],
    })

    plot.show()
