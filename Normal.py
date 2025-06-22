import math


class Normal:
    """ Surface normal representation.
    A normal is a unit vector perpendicular to a surface.
    """

    def __init__(self, x=0, y=0, z=0):
        """Initialize a normal vector.

        Args:
            x, y, z: Components of the normal vector, or an iterable of 3 components
        """
        try:
            # Try to unpack if x is an iterable
            (self.x, self.y, self.z) = x
        except TypeError:
            self.x = float(x)
            self.y = float(y)
            self.z = float(z)

        # Normalize the vector
        self._normalize()

    def _normalize(self):
        """Normalize this vector to unit length."""
        length = math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
        if length > 0:  # Avoid division by zero
            self.x /= length
            self.y /= length
            self.z /= length

    def __mul__(self, other):
        """Dot product with another normal or vector."""
        return (self.x * other.x) + (self.y * other.y) + (self.z * other.z)

    def __rmul__(self, scalar):
        """Scalar multiplication (right side)."""
        return Normal(self.x * scalar, self.y * scalar, self.z * scalar)

    def __repr__(self):
        return f"Normal(x={self.x:.4f}, y={self.y:.4f}, z={self.z:.4f})"
