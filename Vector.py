from Normal import Normal
import math


class Vector3D:
    def __init__(self, x=0, y=0, z=0):
        try:
            (self.x, self.y, self.z) = x
        except TypeError:
            self.x = x
            self.y = y
            self.z = z

    # ^ - Cross Product
    def __xor__(self, vector):
        return Vector3D(x=(self.y * vector.z) - (self.z * vector.y),
                        y=(self.z * vector.x) - (self.x * vector.z),
                        z=(self.x * vector.y) - (self.y * vector.x))

    def __add__(self, vector):
        return Vector3D(x=vector.x + self.x, y=vector.y + self.y, z=vector.z + self.z)

    def __sub__(self, vector):
        return Vector3D(x=self.x - vector.x, y=self.y - vector.y, z=self.z - vector.z)

    # % - Dot Product
    def __mod__(self, vector):
        return self.x * vector.x + self.y * vector.y + self.z * vector.z

    def __mul__(self, other):
        if isinstance(other, (Vector3D, Normal)):
            return self.x * other.x + self.y * other.y + self.z * other.z
        return Vector3D(self.x * other, self.y * other, self.z * other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if other == 0:
            return False
        return Vector3D(self.x / other, self.y / other, self.z / other)

    def normalize(self):
        length = self.length
        return Vector3D(self.x / length, self.y / length, self.z / length)

    def __eq__(self, vector):
        return (self.x == vector.x) and (self.y == vector.y) and (self.z == vector.z)

    @property
    def length(self):
        return math.sqrt((self.x * self.x) + (self.y * self.y) + (self.z * self.z))

    def __repr__(self):
        return f"Vector3D(x={self.x}, y={self.y}, z={self.z})"
