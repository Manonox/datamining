from math import sqrt
from copy import deepcopy


class Point:
    def __init__(self, **kwargs) -> None:
        super(Point, self).__setattr__("properties", deepcopy(kwargs))
        super(Point, self).__setattr__("meta", {})
    
    @staticmethod
    def generate(func, count = None, **kwargs):
        if count is None:
            init_kwargs = {}
            for property, arguments in kwargs.items():
                init_kwargs[property] = func(*arguments)
            return Point(**init_kwargs)
        
        return [Point.generate(func, **kwargs) for _ in range(count)]

    @staticmethod
    def centroid(points):
        count = len(points)
        if count == 0:
            return None
        properties = points[0].properties
        averages = {}
        for property in properties:
            averages[property] = sum([getattr(point, property) for point in points]) / count
        return Point(**averages)

    def add_meta(self, key, value):
        self.meta[key] = value
    
    def get_meta(self, key):
        return self.meta[key]

    def __getattr__(self, __name: str):
        return self.properties.get(__name, 0)

    def __setattr__(self, __name: str, __value) -> None:
        self.properties[__name] = __value

    def __iterate_properties_operation(self, other, func):
        init_kwargs = {}
        for property, value in self.properties.items():
            other_value = other.properties.get(property, 0)
            init_kwargs[property] = func(value, other_value)
        return Point(**init_kwargs)

    def __add__(self, other):
        return self.__iterate_properties_operation(other, lambda a, b : a + b)
    def __sub__(self, other):
        return self.__iterate_properties_operation(other, lambda a, b : a - b)
    def __mul__(self, other):
        return self.__iterate_properties_operation(other, lambda a, b : a * b)
    def __div__(self, other):
        return self.__iterate_properties_operation(other, lambda a, b : a / b)

    def distance(self, other, method = "euclid"):
        process_func = None
        out_func = None
        match method:
            case "euclid":
                process_func = lambda x : x ** 2
                out_func = lambda x : sqrt(x)
            case "manhattan":
                process_func = lambda x : abs(x)
                out_func = lambda x : x
            case "euclid_squared":
                process_func = lambda x : x ** 2
                out_func = lambda x : x
        return out_func(sum([
            process_func(value - other.properties.get(property, 0))
            for property, value in self.properties.items()
        ]))

    def copy(self):
        new = Point(self.properties)
        new.meta = deepcopy(self.meta)
        return new 
