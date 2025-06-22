from Point import Point3D
from Vector import Vector3D


class Ray:
    """A ray for ray tracing, defined by origin point and direction vector."""

    def __init__(self, origin=None, dest=None):
        self.origin = origin if origin else Point3D(0, 0, 0)
        self.dest = dest if dest else Vector3D(0, 0, 0)

    def __repr__(self):
        return f"Ray(origin={self.origin}, direction={self.dest})"
