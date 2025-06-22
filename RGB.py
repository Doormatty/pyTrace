from typing import Dict

from JsonSerializable import JsonSerializable


class RGB(JsonSerializable):
    """RGB color representation with values in range [0.0, 1.0]."""

    def __init__(self, r=0.0, g=0.0, b=0.0):
        """
        Initialize an RGB color.

        Values are automatically clamped to the range [0.0, 1.0].
        Input values can be in range [0.0, 1.0] or [0, 255].
        """
        # Detect if values are likely in [0, 255] range and convert to [0.0, 1.0]
        if isinstance(r, (int, float)) and r > 1.0:
            r = r / 255.0
        if isinstance(g, (int, float)) and g > 1.0:
            g = g / 255.0
        if isinstance(b, (int, float)) and b > 1.0:
            b = b / 255.0

        self.r = self._clamp(r)
        self.g = self._clamp(g)
        self.b = self._clamp(b)

    @staticmethod
    def _clamp(value):
        """Clamp value to range [0.0, 1.0]."""
        return max(0.0, min(1.0, value))

    def __add__(self, other):
        """Add two colors, clamping the result."""
        return RGB(self.r + other.r, self.g + other.g, self.b + other.b)

    def __sub__(self, other):
        """Subtract two colors, clamping the result."""
        return RGB(self.r - other.r, self.g - other.g, self.b - other.b)

    def __mul__(self, num):
        """Multiply color by a scalar, clamping the result."""
        return RGB(num * self.r, num * self.g, num * self.b)

    def __rmul__(self, num):
        """Multiply color by a scalar (right multiplication)."""
        return self.__mul__(num)

    def finalcolor(self):
        """Convert to pygame color format (tuple of integers in range [0, 255])."""
        return int(self.r * 255), int(self.g * 255), int(self.b * 255)

    def __eq__(self, other):
        """Check if two colors are equal (within a small epsilon)."""
        if not isinstance(other, RGB):
            return False

        EPSILON = 0.00001
        return (abs(self.r - other.r) < EPSILON and
                abs(self.g - other.g) < EPSILON and
                abs(self.b - other.b) < EPSILON)

    def to_json(self) -> Dict[str, float]:
        """Convert RGB color to JSON-serializable dictionary."""
        return {
            "r": self.r,
            "g": self.g,
            "b": self.b
        }

    @classmethod
    def from_json(cls, data: Dict[str, float]) -> 'RGB':
        """Create an RGB instance from JSON data."""
        return cls(
            r=data.get("r", 0.1),
            g=data.get("g", 0.1),
            b=data.get("b", 0.1)
        )

    def __repr__(self):
        return f"RGB(r={self.r:.2f}, g={self.g:.2f}, b={self.b:.2f})"
