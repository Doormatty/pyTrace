class RGB:
    def __init__(self, r=0.0, g=0.0, b=0.0):
        self.r = self._clamp(r)
        self.g = self._clamp(g)
        self.b = self._clamp(b)

    @staticmethod
    def _clamp(value):
        if value > 1.0:
            return 1.0
        elif value < 0.0:
            return 0.0
        else:
            return value

    def __add__(self, other):
        return RGB(other.r + self.r, other.g + self.g, other.b + self.b)

    def __sub__(self, other):
        return RGB(self.r - other.r, self.g - other.g, self.b - other.b)

    def __mul__(self, num):
        return RGB(num * self.r, num * self.g, num * self.b)

    def finalcolor(self):
        return int(self.r * 255), int(self.g * 255), int(self.b * 255)

    def __eq__(self, other):
        return (round(self.r, 5) == round(other.r, 5)) and \
               (round(self.g, 5) == round(other.g, 5)) and \
               (round(self.b, 5) == round(other.b, 5))

    def __repr__(self):
        return f"RGB(r={self.r}, g={self.g}, b={self.b})"
