from typing import List, Dict, Any, Optional, Tuple, TYPE_CHECKING
import math

from JsonSerializable import JsonSerializable
from Material import Material
from Point import Point3D
from RGB import RGB
from Vector import Vector3D
from Primitives import Cube
from Noise import Noise

# Use TYPE_CHECKING to avoid circular imports
if TYPE_CHECKING:
    from Scene import Scene


class Terrain(JsonSerializable):
    """
    A terrain object that creates a voxel version of a 2D noise map using cube objects.

    The terrain is created by sampling a 2D noise map and creating cubes with heights
    proportional to the noise values. The cubes are positioned with specified gaps.
    """

    def __init__(self,
                 noise_scale: float = 0.1,
                 noise_amplitude: float = 1.0,
                 cube_size: float = 1.0,
                 gap_distance: float = 0.0,
                 width: float = 10.0,
                 depth: float = 10.0,
                 height: float = 5.0,
                 location: Point3D = None,
                 material: Material = None,
                 seed: Optional[int] = None):
        """
        Initialize a terrain object.

        Args:
            noise_scale: Scale factor for the noise (smaller = more zoomed out)
            noise_amplitude: Maximum height multiplier for the noise values
            cube_size: Size of each cube (single side)
            gap_distance: Gap between adjacent cubes
            width: Total width of the terrain (X axis)
            depth: Total depth of the terrain (Z axis)
            height: Maximum height of the terrain (Y axis)
            location: Center point of the bottom face of the terrain
            material: Material for the cubes (if None, a default material is used)
            seed: Optional seed for the noise generator
        """
        self.noise_scale = noise_scale
        self.noise_amplitude = noise_amplitude
        self.cube_size = cube_size
        self.gap_distance = gap_distance
        self.width = width
        self.depth = depth
        self.height = height
        self.location = location if location else Point3D(0, 0, 0)
        self.material = material if material else Material()
        self.seed = seed

        # Initialize noise generator
        self.noise = Noise(seed=self.seed)

        # Calculate derived values
        self.step_size = self.cube_size + self.gap_distance
        self.num_cubes_x = math.floor(self.width / self.step_size)
        self.num_cubes_z = math.floor(self.depth / self.step_size)

        # Adjust width and depth to match actual number of cubes
        self.actual_width = self.num_cubes_x * self.step_size
        self.actual_depth = self.num_cubes_z * self.step_size

        # Calculate offset to center the terrain at the specified location
        self.offset_x = self.location.x - (self.actual_width / 2)
        self.offset_y = self.location.y
        self.offset_z = self.location.z - (self.actual_depth / 2)

        # Generate the cubes
        self.cubes = self._generate_cubes()

    def _generate_cubes(self) -> List[Cube]:
        """
        Generate the cubes for the terrain based on the noise map.

        Returns:
            A list of Cube objects positioned according to the noise map.
        """
        cubes = []

        for x_idx in range(self.num_cubes_x):
            for z_idx in range(self.num_cubes_z):
                # Calculate the world position for this cube
                x_pos = self.offset_x + (x_idx * self.step_size)
                z_pos = self.offset_z + (z_idx * self.step_size)

                # Sample the noise map at this position
                # We use x_idx and z_idx for noise sampling to ensure consistent spacing
                noise_value = self.noise.noise3d(x_idx, 0, z_idx, scale=self.noise_scale)

                # Calculate the height of this cube based on the noise value
                cube_height = noise_value * self.noise_amplitude * self.height

                # Ensure minimum height
                cube_height = max(self.cube_size, cube_height)

                # Calculate the y position (bottom of the cube)
                y_pos = self.offset_y

                # Create the cube
                cube = self._create_cube(x_pos, y_pos, z_pos, cube_height)
                cubes.append(cube)

        return cubes

    def _create_cube(self, x: float, y: float, z: float, height: float) -> Cube:
        """
        Create a cube at the specified position with the given height.

        Args:
            x: X position of the bottom-left-front corner
            y: Y position of the bottom-left-front corner
            z: Z position of the bottom-left-front corner
            height: Height of the cube

        Returns:
            A Cube object positioned at the specified location.
        """
        # Calculate the three corner points of the cube
        a = Point3D(x, y, z)
        b = Point3D(x + self.cube_size, y + height, z)
        c = Point3D(x, y, z + self.cube_size)

        # Create the cube with the specified material
        return Cube(a, b, c, self.material)

    def add_to_scene(self, scene: 'Scene') -> None:
        """
        Add all cubes in this terrain to the specified scene.

        Args:
            scene: The scene to add the cubes to
        """
        for cube in self.cubes:
            scene.add_object(cube)

    def to_json(self) -> Dict[str, Any]:
        """Convert terrain to JSON-serializable dictionary."""
        return {
            "type": "terrain",
            "noise_scale": self.noise_scale,
            "noise_amplitude": self.noise_amplitude,
            "cube_size": self.cube_size,
            "gap_distance": self.gap_distance,
            "width": self.width,
            "depth": self.depth,
            "height": self.height,
            "location": self.location.to_json(),
            "material": self.material.to_json(),
            "seed": self.seed
        }

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> 'Terrain':
        """Create a Terrain instance from JSON data."""
        return cls(
            noise_scale=data.get("noise_scale", 0.1),
            noise_amplitude=data.get("noise_amplitude", 1.0),
            cube_size=data.get("cube_size", 1.0),
            gap_distance=data.get("gap_distance", 0.0),
            width=data.get("width", 10.0),
            depth=data.get("depth", 10.0),
            height=data.get("height", 5.0),
            location=Point3D.from_json(data.get("location", {})),
            material=Material.from_json(data.get("material", {})),
            seed=data.get("seed")
        )
