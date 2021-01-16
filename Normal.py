class Normal:
    def __init__(self, x=0, y=0, z=0):
        try:
            (self.x, self.y, self.z) = x
        except TypeError:
            self.x = x
            self.y = y
            self.z = z

    def __mul__(self, norm):
        return (self.x * norm.x) + (self.y * norm.y) + (self.z * norm.z)

    def __repr__(self):
        return f"Normal(x={self.x}, y={self.y}, z={self.z})"
