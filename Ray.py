from Point import Point3D
from Vector import Vector3D


class Ray:
    def __init__(self, origin=Point3D(0, 0, 0), dest=Vector3D(0, 0, 0)):
        self.origin = origin
        self.dest = dest

    def __repr__(self):
        return f"Ray(origin={self.origin}, dest:={self.dest})"
