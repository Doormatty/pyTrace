from __future__ import annotations
from Normal import Normal
from typing import Optional, Union, Iterable, Dict, Any
import math
from Coord3D import Coord3D


class Vector3D(Coord3D):
    x: Union[float, Iterable[float]]
    y: Optional[float]
    z: Optional[float]
    _length_squared: Optional[float] = None
    _length: Optional[float] = None

    def __init__(self, x=0, y=0, z=0) -> None:
        try:
            (self.x, self.y, self.z) = x
        except TypeError:
            self.x = x
            self.y = y
            self.z = z

    # ^ - Cross Product
    def __xor__(self, vector) -> Vector3D:
        return Vector3D(x=(self.y * vector.z) - (self.z * vector.y),
                        y=(self.z * vector.x) - (self.x * vector.z),
                        z=(self.x * vector.y) - (self.y * vector.x))

    def __add__(self, vector) -> Vector3D:
        return Vector3D(x=vector.x + self.x, y=vector.y + self.y, z=vector.z + self.z)

    def __sub__(self, vector) -> Vector3D:
        return Vector3D(x=self.x - vector.x, y=self.y - vector.y, z=self.z - vector.z)

    # % - Dot Product
    def __mod__(self, vector) -> float:
        return self.x * vector.x + self.y * vector.y + self.z * vector.z

    def __mul__(self, other) -> Union[float, Vector3D]:
        if isinstance(other, (Vector3D, Normal)):
            return self.x * other.x + self.y * other.y + self.z * other.z
        return Vector3D(self.x * other, self.y * other, self.z * other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other) -> Vector3D:
        if other == 0:
            return False
        inv_other = 1.0 / other  # Calculate division once
        return Vector3D(self.x * inv_other, self.y * inv_other, self.z * inv_other)

    def normalize(self) -> Vector3D:
        if self._length is None:
            self._length = self.length
        inv_length = 1.0 / self._length  # Calculate division once
        return Vector3D(self.x * inv_length, self.y * inv_length, self.z * inv_length)

    def __eq__(self, vector) -> bool:
        return (self.x == vector.x) and (self.y == vector.y) and (self.z == vector.z)

    @property
    def length_squared(self) -> float:
        if self._length_squared is None:
            self._length_squared = (self.x * self.x) + (self.y * self.y) + (self.z * self.z)
        return self._length_squared

    @property
    def length(self) -> float:
        if self._length is None:
            self._length = math.sqrt(self.length_squared)
        return self._length

    def __repr__(self) -> str:
        return f"Vector3D(x={self.x}, y={self.y}, z={self.z})"

    # to_json and from_json methods are inherited from Coord3D
