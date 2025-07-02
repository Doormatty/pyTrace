class RayIntersection:
    """Represents an intersection between a ray and a scene object."""

    def __init__(self, obj, normal, hit_point, distance=None, material=None):
        """
        Initialize a ray intersection.

        Args:
            obj: The object that was hit
            normal: Surface normal at the hit point (Vector3D)
            hit_point: The point of intersection (Point3D)
            distance: Distance from ray origin to hit point (float)
            material: Optional material override for this intersection
        """
        self.object = obj
        self.normal = normal
        self.hit_point = hit_point
        self.distance = distance
        self.material = material  # Optional material override

    def __repr__(self):
        return f"RayIntersection(object={self.object}, normal={self.normal}, hit_point={self.hit_point})"
