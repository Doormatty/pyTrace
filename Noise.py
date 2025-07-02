import math
import random


class Noise:
    """A class for generating 3D Perlin-like noise."""

    def __init__(self, seed=None):
        """Initialize the noise generator with an optional seed."""
        if seed is not None:
            random.seed(seed)

        # Create a permutation table
        self.perm = list(range(256))
        random.shuffle(self.perm)
        self.perm += self.perm  # Duplicate to avoid overflow

    def noise3d(self, x, y, z, scale=1.0):
        """
        Generate 3D noise at the given coordinates.
        
        Args:
            x, y, z: Coordinates to sample noise at
            scale: Scale factor for the noise (smaller = more zoomed out)
            
        Returns:
            A value between 0 and 1
        """
        # Scale the coordinates
        x *= scale
        y *= scale
        z *= scale

        # Get grid cell coordinates and cache floor values
        x_floor = math.floor(x)
        y_floor = math.floor(y)
        z_floor = math.floor(z)

        X = int(x_floor) & 255
        Y = int(y_floor) & 255
        Z = int(z_floor) & 255

        # Get relative position within the cell
        x -= x_floor
        y -= y_floor
        z -= z_floor

        # Compute fade curves
        u = self._fade(x)
        v = self._fade(y)
        w = self._fade(z)

        # Cache permutation table lookups
        perm = self.perm  # Local reference to avoid attribute lookup

        # coordinates of the 8 cube corners
        a = perm[X] + Y
        aa = perm[a] + Z
        ab = perm[a + 1] + Z
        b = perm[X + 1] + Y
        ba = perm[b] + Z
        bb = perm[b + 1] + Z

        # Pre-compute gradient values
        g1 = self._grad(perm[aa], x, y, z)
        g2 = self._grad(perm[ba], x - 1, y, z)
        g3 = self._grad(perm[ab], x, y - 1, z)
        g4 = self._grad(perm[bb], x - 1, y - 1, z)
        g5 = self._grad(perm[aa + 1], x, y, z - 1)
        g6 = self._grad(perm[ba + 1], x - 1, y, z - 1)
        g7 = self._grad(perm[ab + 1], x, y - 1, z - 1)
        g8 = self._grad(perm[bb + 1], x - 1, y - 1, z - 1)

        # First level of linear interpolations
        lerp1 = self._lerp(u, g1, g2)
        lerp2 = self._lerp(u, g3, g4)
        lerp3 = self._lerp(u, g5, g6)
        lerp4 = self._lerp(u, g7, g8)

        # Second level of linear interpolations
        lerp5 = self._lerp(v, lerp1, lerp2)
        lerp6 = self._lerp(v, lerp3, lerp4)

        # Final interpolation
        result = self._lerp(w, lerp5, lerp6)

        # Convert from -1..1 to 0..1
        return (result + 1) / 2

    @staticmethod
    def _fade(t):
        """Fade function for smooth interpolation."""
        return t * t * t * (t * (t * 6 - 15) + 10)

    @staticmethod
    def _lerp(t, a, b):
        """Linear interpolation between a and b by t."""
        return a + t * (b - a)

    @staticmethod
    def _grad(hash, x, y, z):
        """Calculate the dot product for gradient noise."""
        h = hash & 15
        u = x if h < 8 else y
        v = y if h < 4 else (x if h == 12 or h == 14 else z)
        return (u if (h & 1) == 0 else -u) + (v if (h & 2) == 0 else -v)
