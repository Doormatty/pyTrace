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
                 gap_distance: float = 1.0,
                 width: float = 10.0,
                 depth: float = 10.0,
                 height: float = 5.0,
                 reflectivity: float = 0.0,
                 opacity: float = 1.0,
                 luma: float = 0.0,
                 location: Point3D = None,
                 material: Material = None,
                 seed: Optional[int] = None,
                 normal: Vector3D = None):
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
            material: Material for the cubes (if None, each cube gets a position-based color)
            seed: Optional seed for the noise generator
            normal: Normal vector for the terrain (if None, defaults to Vector3D(0, 0, 1) pointing straight up)
        """
        self.noise_scale = noise_scale
        self.noise_amplitude = noise_amplitude
        self.cube_size = cube_size
        self.gap_distance = gap_distance
        self.width = width
        self.depth = depth
        self.height = height
        self.location = location if location else Point3D(0, 0, 0)
        self.material = material
        self.luma = luma
        self.reflectivity = reflectivity
        self.opacity = opacity
        self.use_position_based_colors = material is None
        self.seed = seed
        self.normal = normal if normal else Vector3D(0, 0, 1)

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

        # Create coordinate system based on normal vector
        self._setup_coordinate_system()

        # Generate the cubes
        self.cubes = self._generate_cubes()

    def _setup_coordinate_system(self):
        """
        Set up a local coordinate system based on the terrain normal vector.
        This creates transformation vectors to orient the terrain according to its normal.
        """
        # Normalize the normal vector
        self.normal_normalized = self.normal.normalize()

        # Create a local coordinate system where:
        # - normal_normalized is the "up" direction (height direction)
        # - u_axis is the "right" direction (width direction, maps to X in world)
        # - v_axis is the "forward" direction (depth direction, maps to Z in world)

        # For gaps to appear in Z direction, we want v_axis to align with Z
        # Choose an arbitrary vector that's not parallel to the normal
        # We'll prefer Z axis for depth direction when possible
        if abs(self.normal_normalized.z) > 0.9:
            # Normal is close to Z axis, use X axis for cross product
            arbitrary = Vector3D(1, 0, 0)
        else:
            # Use Z axis for depth direction
            arbitrary = Vector3D(0, 0, 1)

        # Create orthogonal basis vectors using cross products
        self.u_axis = (arbitrary ^ self.normal_normalized).normalize()  # Right direction (X)
        self.v_axis = (self.normal_normalized ^ self.u_axis).normalize()  # Forward direction (Z)

        # Store the up direction (height direction)
        self.up_axis = self.normal_normalized

    def _transform_point(self, local_x: float, local_y: float, local_z: float) -> Point3D:
        """
        Transform a point from local terrain coordinates to world coordinates.

        Args:
            local_x: X coordinate in local terrain space (width direction)
            local_y: Y coordinate in local terrain space (height direction) 
            local_z: Z coordinate in local terrain space (depth direction)

        Returns:
            Point3D in world coordinates
        """
        # Transform from local coordinates to world coordinates
        world_offset = (self.u_axis * local_x + 
                       self.up_axis * local_y + 
                       self.v_axis * local_z)

        return Point3D(
            self.location.x + world_offset.x,
            self.location.y + world_offset.y,
            self.location.z + world_offset.z
        )

    def _generate_cubes(self) -> List[Cube]:
        """
        Generate the cubes for the terrain based on the noise map.

        Returns:
            A list of Cube objects positioned according to the noise map.
        """
        cubes = []

        for x_idx in range(self.num_cubes_x):
            for z_idx in range(self.num_cubes_z):
                # Calculate the local position for this cube (in terrain coordinate system)
                local_x = self.offset_x + (x_idx * self.step_size)
                local_z = self.offset_z + (z_idx * self.step_size)

                # Sample the noise map at this position
                # We use x_idx and z_idx for noise sampling to ensure consistent spacing
                noise_value = self.noise.noise3d(x_idx, 0, z_idx, scale=self.noise_scale)

                # Calculate the height of this cube based on the noise value
                cube_height = noise_value * self.noise_amplitude * self.height

                # Ensure minimum height
                cube_height = max(self.cube_size, cube_height)

                # Local Y position starts at 0 (terrain base level)
                local_y = 0

                # Create the cubes using local coordinates (returns a list of stacked cubes)
                column_cubes = self._create_cube(local_x, local_y, local_z, cube_height, x_idx, z_idx)
                cubes.extend(column_cubes)

        return cubes

    def _create_cube(self, local_x: float, local_y: float, local_z: float, height: float, x_idx: int, z_idx: int) -> List[Cube]:
        """
        Create cubes at the specified position with the given height.
        Instead of creating one tall cube, this creates individual cube units stacked with gaps.

        Args:
            local_x: X position in local terrain coordinates (width direction)
            local_y: Y position in local terrain coordinates (base level)
            local_z: Z position in local terrain coordinates (depth direction)
            height: Total height of the column in the normal direction
            x_idx: X index in the terrain grid
            z_idx: Z index in the terrain grid

        Returns:
            A list of Cube objects positioned at the specified location in world coordinates.
        """
        cubes = []

        # Calculate how many individual cubes can fit in the given height
        # Each cube takes cube_size space plus gap_distance (except the last one doesn't need gap after it)
        cube_step = self.cube_size + self.gap_distance
        num_cubes_vertical = max(1, int(height / cube_step))

        # Create individual cubes stacked vertically
        for y_idx in range(num_cubes_vertical):
            # Calculate the Y position for this cube
            cube_local_y = local_y + (y_idx * cube_step)

            # Transform local coordinates to world coordinates
            # Bottom corner of the cube
            a_world = self._transform_point(local_x, cube_local_y, local_z)

            # Top corner of the cube (extends cube_size in all directions)
            b_world = self._transform_point(local_x + self.cube_size, cube_local_y + self.cube_size, local_z + self.cube_size)

            # Determine the material to use
            if self.use_position_based_colors:
                # Generate position-based color: X=R, Y=G, Z=B (0 to 1.0 across terrain)
                # Normalize X coordinate (0 to 1.0 across terrain width)
                red = x_idx / max(1, self.num_cubes_x - 1) if self.num_cubes_x > 1 else 0.0

                # Normalize Y coordinate (0 to 1.0 across terrain height)
                # Use the cube's vertical position relative to the maximum possible height
                green = min(1.0, (cube_local_y + self.cube_size) / (self.noise_amplitude * self.height))

                # Normalize Z coordinate (0 to 1.0 across terrain depth)
                blue = z_idx / max(1, self.num_cubes_z - 1) if self.num_cubes_z > 1 else 0.0

                # Create material with position-based color
                cube_material = Material(RGB(red, green, blue), luma=self.luma, reflect=self.reflectivity, opacity=self.opacity)
            else:
                # Use the provided material
                cube_material = self.material

            # Create the cube with the determined material using world coordinates
            cube = Cube(a_world, b_world, cube_material)
            cubes.append(cube)

        return cubes

    def hit(self, ray):
        """
        Test for ray intersection with the terrain.

        This method tests the ray against all cubes in the terrain
        and returns the closest intersection.

        Args:
            ray: The ray to test for intersection

        Returns:
            RayIntersection object if hit, None if no intersection
        """
        closest_hit = None
        closest_distance = float('inf')

        # Test ray against all cubes in the terrain
        for cube in self.cubes:
            intersection = cube.hit(ray)
            if intersection:
                # Calculate distance to intersection point
                distance = ray.origin.distance_squared(intersection.hit_point)
                if distance < closest_distance:
                    closest_distance = distance
                    closest_hit = intersection

        return closest_hit

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
            "seed": self.seed,
            "normal": self.normal.to_json()
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
            seed=data.get("seed"),
            normal=Vector3D.from_json(data.get("normal", {})) if "normal" in data else None
        )
