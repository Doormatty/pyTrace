from __future__ import annotations
import math
from Vector import Vector3D
from typing import Optional, Union, Iterable


class Point3D:
    x: Union[float, Iterable[float]]
    y: Optional[float]
    z: Optional[float]

    def __init__(self, x=0, y=0, z=0) -> None:
        try:
            (self.x, self.y, self.z) = x
        except TypeError:
            self.x = x
            self.y = y
            self.z = z

    def __add__(self, other) -> Union[Point3D, Vector3D]:
        if isinstance(other, Vector3D):
            return Point3D(x=self.x + other.x, y=self.y + other.y, z=self.z + other.z)
        if isinstance(other, Point3D):
            return Vector3D(x=self.x + other.x, y=self.y + other.y, z=self.z + other.z)
        return Point3D(x=self.x + other, y=self.y + other, z=self.z + other)

    def __sub__(self, other) -> Union[Point3D, Vector3D]:
        if isinstance(other, Vector3D):
            return Point3D(x=self.x - other.x, y=self.y - other.y, z=self.z - other.z)
        elif isinstance(other, (int, float)):
            return Point3D(x=self.x - other, y=self.y - other, z=self.z - other)
        elif isinstance(other, Point3D):
            return Vector3D(x=self.x - other.x, y=self.y - other.y, z=self.z - other.z)

    def __rsub__(self, other) -> Union[Point3D, Vector3D]:
        if isinstance(other, Vector3D):
            return Point3D(x=other.x - self.x, y=other.y - self.y, z=other.z - self.z)
        elif isinstance(other, (int, float)):
            return Point3D(x=other - self.x, y=other - self.y, z=other - self.z)
        elif isinstance(other, Point3D):
            return Vector3D(x=other.x - self.x, y=other.y - self.y, z=other.z - self.z)

    def __mul__(self, other) -> Point3D:
        return Point3D(x=self.x * other, y=self.y * other, z=self.z * other)

    def __rmul__(self, other) -> Point3D:
        return Point3D(x=self.x * other, y=self.y * other, z=self.z * other)

    def distance(self, point) -> float:
        return math.sqrt((self.x - point.x) ** 2 + (self.y - point.y) ** 2 + (self.z - point.z) ** 2)

    def __repr__(self) -> str:
        return f"Point3D(x={self.x}, y={self.y}, z={self.z})"

    def __eq__(self, other) -> bool:
        return (self.x == other.x) and (self.y == other.y) and (self.z == other.z)
