from Primitives import Shape
from Normal import Normal
from Point import Point3D


class Intersection:

    def __init__(self, shape, normal, hit_point):
        self.object = shape
        self.normal = normal
        self.hit_point = hit_point
