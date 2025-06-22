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
        
        # Get grid cell coordinates
        X = int(math.floor(x)) & 255
        Y = int(math.floor(y)) & 255
        Z = int(math.floor(z)) & 255
        
        # Get relative position within the cell
        x -= math.floor(x)
        y -= math.floor(y)
        z -= math.floor(z)
        
        # Compute fade curves
        u = self._fade(x)
        v = self._fade(y)
        w = self._fade(z)
        
        # Hash coordinates of the 8 cube corners
        A = self.perm[X] + Y
        AA = self.perm[A] + Z
        AB = self.perm[A + 1] + Z
        B = self.perm[X + 1] + Y
        BA = self.perm[B] + Z
        BB = self.perm[B + 1] + Z
        
        # Blend the eight corners based on distance
        result = self._lerp(w, 
            self._lerp(v, 
                self._lerp(u, 
                    self._grad(self.perm[AA], x, y, z),
                    self._grad(self.perm[BA], x-1, y, z)
                ),
                self._lerp(u, 
                    self._grad(self.perm[AB], x, y-1, z),
                    self._grad(self.perm[BB], x-1, y-1, z)
                )
            ),
            self._lerp(v, 
                self._lerp(u, 
                    self._grad(self.perm[AA+1], x, y, z-1),
                    self._grad(self.perm[BA+1], x-1, y, z-1)
                ),
                self._lerp(u, 
                    self._grad(self.perm[AB+1], x, y-1, z-1),
                    self._grad(self.perm[BB+1], x-1, y-1, z-1)
                )
            )
        )
        
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