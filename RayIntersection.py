class RayIntersection:
    def __init__(self, shape, normal, hit_point):
        self.object = shape
        self.normal = normal
        self.hit_point = hit_point

    def __repr__(self):
        return f"RayIntersection(shape={self.object}, normal={self.normal}, hit_point={self.hit_point})"
