from __future__ import annotations

import math
from typing import Optional, Union, Iterable, Dict

from Coord3D import Coord3D
from Vector import Vector3D


class Point3D(Coord3D):
    x: Union[float, Iterable[float]]
    y: Optional[float]
    z: Optional[float]
    _distance_cache: Dict[int, float] = {}

    def __init__(self, x=0, y=0, z=0) -> None:
        try:
            (self.x, self.y, self.z) = x
        except TypeError:
            self.x = x
            self.y = y
            self.z = z
        self._distance_cache = {}

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

    def distance_squared(self, point) -> float:
        """Calculate squared distance to another point (faster than distance)."""
        dx = self.x - point.x
        dy = self.y - point.y
        dz = self.z - point.z
        return dx * dx + dy * dy + dz * dz

    def distance(self, point) -> float:
        """Calculate distance to another point with caching."""
        # Use object id as cache key
        point_id = id(point)
        if point_id in self._distance_cache:
            return self._distance_cache[point_id]

        # Calculate distance
        dist = math.sqrt(self.distance_squared(point))

        # Cache the result (limit cache size to prevent memory issues)
        if len(self._distance_cache) > 100:  # Arbitrary limit
            self._distance_cache.clear()
        self._distance_cache[point_id] = dist

        return dist

    def __repr__(self) -> str:
        return f"Point3D(x={self.x}, y={self.y}, z={self.z})"

    def __eq__(self, other) -> bool:
        return (self.x == other.x) and (self.y == other.y) and (self.z == other.z)

    # to_json and from_json methods are inherited from Coord3D
