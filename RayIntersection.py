class RayIntersection:
    """Represents an intersection between a ray and a scene object."""

    def __init__(self, obj, normal, hit_point):
        """
        Initialize a ray intersection.

        Args:
            obj: The object that was hit
            normal: Surface normal at the hit point (Vector3D)
            hit_point: The point of intersection (Point3D)
        """
        self.object = obj
        self.normal = normal
        self.hit_point = hit_point

    def __repr__(self):
        return f"RayIntersection(object={self.object}, normal={self.normal}, hit_point={self.hit_point})"
