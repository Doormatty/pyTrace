'''
Created on Apr 15, 2012

@author: matt
'''
import math
from Vector import Vector3D


class Point3D:
    def __init__(self, x=0, y=0, z=0):
        try:
            (self.x, self.y, self.z) = x
        except TypeError:
            self.x = x
            self.y = y
            self.z = z

    def __add__(self, other):
        if isinstance(other, Vector3D):
            return Point3D(x=self.x + other.x, y=self.y + other.y, z=self.z + other.z)
        if isinstance(other, Point3D):
            return Vector3D(x=self.x + other.x, y=self.y + other.y, z=self.z + other.z)
        return Point3D(x=self.x + other, y=self.y + other, z=self.z + other)

    def __sub__(self, other):
        if isinstance(other, Vector3D):
            return Point3D(x=self.x - other.x, y=self.y - other.y, z=self.z - other.z)
        elif isinstance(other, (int, float)):
            return Point3D(x=self.x - other, y=self.y - other, z=self.z - other)
        elif isinstance(other, Point3D):
            return Vector3D(x=self.x - other.x, y=self.y - other.y, z=self.z - other.z)

    def __rsub__(self, other):
        if isinstance(other, Vector3D):
            return Point3D(x=other.x - self.x, y=other.y - self.y, z=other.z - self.z)
        elif isinstance(other, (int, float)):
            return Point3D(x=other - self.x, y=other - self.y, z=other - self.z)
        elif isinstance(other, Point3D):
            return Vector3D(x=other.x - self.x, y=other.y - self.y, z=other.z - self.z)

    def __mul__(self, other):
        return Point3D(x=self.x * other, y=self.y * other, z=self.z * other)

    def __rmul__(self, other):
        return Point3D(x=self.x * other, y=self.y * other, z=self.z * other)

    def distance(self, point):
        return int(math.sqrt((self.x - point.x) ** 2 + (self.y - point.y) ** 2 + (self.z - point.z) ** 2))
    #
    # def __str__(self):
    #     return "Point3D - X:" + str(self.x) + " Y:" + str(self.y) + " Z:" + str(self.z)

    def __repr__(self):
        return f"Point3D(x={self.x}, y={self.y}, z={self.z})"

    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y) and (self.z == other.z)
