"""
DBSCAN(DB, distFunc, eps, minPts) {
   C=0                                                  /* Счётчик кластеров */
   for each point P in database DB {
      if label(P) ≠ undefined then continue               /* Точка была просмотрена во внутреннем цикле */
      Neighbors N=RangeQuery(DB, distFunc, P, eps)      /* Находим соседей */
      if|N|< minPts then {                              /* Проверка плотности */
         label(P)=Noise                                 /* Помечаем как шум */
         continue
      }
      C=C + 1                                           /* следующая метка кластера */
      label(P)=C                                        /* Помечаем начальную точку */
      Seed set S=N \ {P}                                /* Соседи для расширения */
      for each point Q in S {                             /* Обрабатываем каждую зачаточную точку */
         if label(Q)=Noise then label(Q)=C            /* Заменяем метку Шум на Край */
         if label(Q) ≠ undefined then continue            /* Была просмотрена */
         label(Q)=C                                     /* Помечаем соседа */
         Neighbors N=RangeQuery(DB, distFunc, Q, eps)   /* Находим соседей */
         if|N|≥ minPts then {                           /* Проверяем плотность */
            S=S ∪ N                                     /* Добавляем соседей в набор зачаточных точек */
         }
      }
   }
}
"""


import random
from math import sqrt


def __dbscan_range_query(points, point, eps, distance_func_type = "euclid"):
    other_distance_func = lambda other : point.distance(other, distance_func_type)
    distance_filter_func = lambda other : (other_distance_func(other) < eps)# and (other != point)
    result = list(filter(distance_filter_func, points))
    return result

def dbscan(points, eps, distance_func_type = "euclid"):
    labels = {}
    LABEL_NOISE = -1
    
    cluster_index = 0
    for point_index, point in enumerate(points):
        point_label = labels.get(point)
        if point_label != None:
            continue
        neighbors = __dbscan_range_query(points, point, eps, distance_func_type)
        if len(neighbors) == 0:
            labels[point] = LABEL_NOISE
            continue
        cluster_index = cluster_index + 1
        labels[point] = cluster_index
        neighbors_open = set(filter(lambda other : point != other, neighbors))
        
        while len(neighbors_open) > 0:
            neighbor_point = neighbors_open.pop()
            neighbor_point_label = labels.get(neighbor_point)
            if neighbor_point_label == LABEL_NOISE:
                labels[neighbor_point] = cluster_index
            if neighbor_point_label != None:
                continue
            labels[neighbor_point] = cluster_index
            new_neighbors = __dbscan_range_query(points, neighbor_point, eps, distance_func_type)
            if len(new_neighbors) > 0:
                neighbors_open = neighbors_open.union(set(new_neighbors))
    return labels

if __name__ == "__main__":
    from manonox import Point
    from matplotlib import pyplot as plt
    
    points = []
    points.extend(Point.generate(random.normalvariate, 100, x=[0, 0.5], y=[0, 0.5]))
    points.extend(Point.generate(random.normalvariate, 100, x=[3, 0.5], y=[2, 0.5]))
    points.extend(Point.generate(random.normalvariate, 50, x=[-1.5, 0.15], y=[-1.5, 0.15]))
    
    labels = dbscan(points, 0.5)
    plt.scatter("x", "y", c="c", s=5, data={
        "x": [point.x for point, label in labels.items()],
        "y": [point.y for point, label in labels.items()],
        "c": [label for point, label in labels.items()],
    })
    
    plt.show()