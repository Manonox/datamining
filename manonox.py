from math import sqrt


class Point:
    def __init__(self, **kwargs) -> None:
        super(Point, self).__setattr__("properties", kwargs)
    
    @staticmethod
    def generate(func, count = None, **kwargs):
        if count is None:
            init_kwargs = {}
            for property, arguments in kwargs.items():
                init_kwargs[property] = func(*arguments)
            return Point(**init_kwargs)
        
        return [Point.generate(func, **kwargs) for _ in range(count)]

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
        s = 0
        for property, value in self.properties.items():
            diff = value - other.properties.get(property, 0)
            match method:
                case "euclid":
                    s += diff ** 2
                case "manhattan":
                    s += abs(diff)
        
        match method:
            case "euclid":
                return sqrt(s)
            case "manhattan":
                return s
