from __future__ import annotations

import math
from typing import Union, Dict, Any

from JsonSerializable import JsonSerializable
from Material import Material
from Normal import Normal
from Point import Point3D
from RGB import RGB
from RayIntersection import RayIntersection
from Vector import Vector3D


class Plane(JsonSerializable):
    """A plane primitive for ray tracing."""
    center: Point3D
    normal: Vector3D
    material: Material

    # Small constant to avoid self-intersection due to floating point errors
    EPSILON = 0.001

    def __init__(self, center=None, normal=None, material=None) -> None:
        self.center = center if center else Point3D(0, 0, 0)
        self.normal = normal if normal else Vector3D(0, 1, 0)  # Default normal is up
        self.material = material if material else Material()

    def hit(self, ray) -> Union[bool, RayIntersection]:
        """Calculate intersection between a ray and this plane.
        Returns RayIntersection if hit, False otherwise.
        """
        # Calculate denominator: dot product of ray direction and plane normal
        denominator = ray.dest * self.normal

        # Ray is parallel to plane if denominator is zero
        if abs(denominator) < self.EPSILON:
            return False

        # Calculate distance along ray to intersection
        t = ((self.center - ray.origin) * self.normal) / denominator

        # Check if intersection is in front of ray origin
        if t > self.EPSILON:
            # Calculate the intersection point
            intersection_point = ray.origin + (t * ray.dest)
            return RayIntersection(self, self.normal, intersection_point, t)

        return False

    def __repr__(self):
        return f"Plane(x={self.center.x}, y={self.center.y}, z={self.center.z})"

    def to_json(self) -> Dict[str, Any]:

        """Convert plane to JSON-serializable dictionary."""

        return {
            "type": "plane",
            "center": self.center.to_json(),
            "normal": self.normal.to_json(),
            "material": self.material.to_json()
        }

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> 'Plane':

        """Create a Plane instance from JSON data."""

        return cls(
            center=Point3D.from_json(data.get("center", {})),
            normal=Vector3D.from_json(data.get("normal", {})),
            material=Material.from_json(data.get("material", {}))
        )


class CheckerPlane(Plane):
    """A checkerboard plane primitive for ray tracing."""

    def __init__(self, center=None, normal=None, material1=None, material2=None, square_size=10):
        """
        Initialize a checkerboard plane.

        Args:
            center: Center point of the plane (Point3D)
            normal: Normal vector of the plane (Vector3D)
            material1: First material for the checkerboard pattern (Material)
            material2: Second material for the checkerboard pattern (Material)
            square_size: Size of each square in the checkerboard pattern (float)
        """
        self.center = center if center else Point3D(0, 0, 0)
        self.normal = normal if normal else Normal(0, 0, 1)
        # Initialize with the first material as the base material
        self.material1 = material1 if material1 else Material(RGB(0.8, 0.8, 0.8), 1.0, 0.0, 0.0)
        self.material2 = material2 if material2 else Material(RGB(0.2, 0.2, 0.2), 1.0, 0.0, 0.0)
        super().__init__(self.center, self.normal, self.material1)

        self.square_size = square_size if square_size > 0 else 1.0

        # Calculate two orthogonal vectors in the plane for UV mapping
        # If normal is close to (0,1,0), use (1,0,0) as reference
        if abs(self.normal.y) > 0.9:
            reference = Vector3D(1, 0, 0)
        else:
            reference = Vector3D(0, 1, 0)

        # Create orthogonal basis vectors in the plane
        # Convert normal to Vector3D for cross product operations
        normal_vec = Vector3D(self.normal.x, self.normal.y, self.normal.z)
        self.u_axis = (normal_vec ^ reference).normalize()
        self.v_axis = (normal_vec ^ self.u_axis).normalize()

    def hit(self, ray) -> Union[bool, RayIntersection]:
        """Calculate intersection and determine checkerboard material (double-sided)."""
        # Calculate denominator: dot product of ray direction and plane normal
        denominator = ray.dest * self.normal

        # Ray is parallel to plane if denominator is zero
        if abs(denominator) < self.EPSILON:
            return False

        # Calculate distance along ray to intersection
        t = ((self.center - ray.origin) * self.normal) / denominator

        # Check if intersection is in front of ray origin
        if t > self.EPSILON:
            # Calculate the intersection point
            intersection_point = ray.origin + (t * ray.dest)

            # Determine the correct normal direction
            # If denominator is negative, ray is coming from behind the plane
            if denominator < 0:
                # Ray coming from behind - use original normal
                intersection_normal = self.normal
            else:
                # Ray coming from front - flip normal to face the ray
                intersection_normal = Vector3D(-self.normal.x, -self.normal.y, -self.normal.z)

            # Calculate UV coordinates for the checkerboard pattern
            # Use world coordinates to ensure consistent pattern regardless of viewing direction
            # Vector from plane center to intersection point
            hit_vector = intersection_point - self.center

            # Use a coordinate system that's independent of normal direction
            # For consistent checkerboard pattern, use absolute world coordinates
            # projected onto the plane using a fixed coordinate system

            # Create a consistent coordinate system based on world axes
            # This ensures the pattern is the same regardless of viewing direction
            if abs(self.normal.z) > 0.9:
                # Plane is mostly horizontal (normal close to Z axis)
                # Use X and Y coordinates for the pattern
                u = hit_vector.x
                v = hit_vector.y
            elif abs(self.normal.y) > 0.9:
                # Plane is mostly vertical (normal close to Y axis)
                # Use X and Z coordinates for the pattern
                u = hit_vector.x
                v = hit_vector.z
            else:
                # Plane is mostly vertical (normal close to X axis)
                # Use Y and Z coordinates for the pattern
                u = hit_vector.y
                v = hit_vector.z

            # Determine which square we're in
            # Use floor division to ensure consistent pattern regardless of side
            u_square = int(math.floor(u / self.square_size))
            v_square = int(math.floor(v / self.square_size))

            # Checkerboard pattern: alternate materials based on square coordinates
            pattern_value = (u_square + v_square) % 2
            if pattern_value == 0:
                current_material = self.material1
            else:
                current_material = self.material2

            # Return intersection with the appropriate material and normal
            return RayIntersection(self, intersection_normal, intersection_point, t, current_material)

        return False

    def __repr__(self):
        return f"CheckerPlane(x={self.center.x}, y={self.center.y}, z={self.center.z}, square_size={self.square_size})"

    def to_json(self) -> Dict[str, Any]:
        """Convert checkerplane to JSON-serializable dictionary."""
        return {
            "type": "checkerplane",
            "center": self.center.to_json(),
            "normal": self.normal.to_json(),
            "material1": self.material1.to_json(),
            "material2": self.material2.to_json(),
            "square_size": self.square_size
        }

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> 'CheckerPlane':
        """Create a CheckerPlane instance from JSON data."""
        return cls(
            center=Point3D.from_json(data.get("center", {})),
            normal=Vector3D.from_json(data.get("normal", {})),
            material1=Material.from_json(data.get("material1", {})),
            material2=Material.from_json(data.get("material2", {})),
            square_size=data.get("square_size", 1.0)
        )


class Sphere(JsonSerializable):
    """A sphere primitive for ray tracing."""
    center: Point3D
    radius: Union[float, int]
    material: Material

    # Small constant to avoid self-intersection due to floating point errors
    EPSILON = 0.01

    def __init__(self, center, radius, material=None):
        self.center = center
        self.radius = radius if radius is not None else 1.0
        self.material = material if material else Material()

    def hit(self, ray) -> Union[bool, RayIntersection]:
        """Calculate intersection between a ray and this sphere.
        Returns RayIntersection if hit, False otherwise.
        """
        # Handle edge case: zero or negative radius
        if self.radius <= 0:
            return False

        # Vector from ray origin to sphere center
        oc = ray.origin - self.center

        # Quadratic formula coefficients: at² + bt + c = 0
        # Optimize: ray.dest * ray.dest is often 1.0 if ray direction is normalized
        a = ray.dest * ray.dest  # Dot product of ray direction with itself
        b = 2.0 * oc * ray.dest  # 2 * dot product of oc and ray direction
        c = oc * oc - (self.radius * self.radius)  # dot(oc, oc) - radius²

        # Calculate discriminant
        discriminant = b * b - 4.0 * a * c

        # No intersection if discriminant is negative
        if discriminant < 0.0:
            return False

        # Calculate both intersection points
        sqrt_discriminant = math.sqrt(discriminant)
        inv_denom = 0.5 / a
        t1 = (-b - sqrt_discriminant) * inv_denom  # Nearest intersection
        t2 = (-b + sqrt_discriminant) * inv_denom  # Farther intersection

        # Choose the appropriate intersection point
        t = None
        if t1 > self.EPSILON:
            t = t1  # Use nearest intersection if it's in front
        elif t2 > self.EPSILON:
            t = t2  # Use farther intersection if nearest is behind (ray from inside)
        else:
            return False  # Both intersections are behind the ray origin

        # Calculate intersection point
        # Reuse t * ray.dest calculation to avoid creating temporary objects
        t_times_dest = Vector3D(
            t * ray.dest.x,
            t * ray.dest.y,
            t * ray.dest.z
        )
        intersection_point = Point3D(
            ray.origin.x + t_times_dest.x,
            ray.origin.y + t_times_dest.y,
            ray.origin.z + t_times_dest.z
        )

        # Calculate surface normal at intersection point
        # Precompute inverse radius to avoid division
        inv_radius = 1.0 / self.radius
        normal = Vector3D(
            (intersection_point.x - self.center.x) * inv_radius,
            (intersection_point.y - self.center.y) * inv_radius,
            (intersection_point.z - self.center.z) * inv_radius
        )

        return RayIntersection(self, normal, intersection_point, t)

    def __repr__(self):
        return f"Sphere(x={self.center.x}, y={self.center.y}, z={self.center.z}, radius={self.radius})"

    def to_json(self) -> Dict[str, Any]:
        """Convert sphere to JSON-serializable dictionary."""
        return {
            "type": "sphere",
            "center": self.center.to_json(),
            "radius": self.radius,
            "material": self.material.to_json()
        }

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> 'Sphere':
        """Create a Sphere instance from JSON data."""
        return cls(
            center=Point3D.from_json(data.get("center", {})),
            radius=data.get("radius", 1.0),
            material=Material.from_json(data.get("material", {}))
        )


class Cube(JsonSerializable):
    """A cube primitive for ray tracing, defined by two opposite corner points or center point and distance."""

    EPSILON = 0.001

    def __init__(self, a=None, b=None, material=None, center=None, distance=None) -> None:
        """Initialize a cube from two opposite corner points OR center point and distance.

        Two initialization modes:
        1. Two corner points: Cube(a=Point3D, b=Point3D, material=Material)
        2. Center and distance: Cube(center=Point3D, distance=float, material=Material)

        Args:
            a: First corner point (for two-corner mode)
            b: Opposite corner point (for two-corner mode)
            material: Material for the cube
            center: Center point of the cube (for center-distance mode)
            distance: Distance from center to face (for center-distance mode)
        """
        self.material = material if material else Material()

        # Check which initialization mode to use
        if center is not None and distance is not None:
            # Center-distance mode
            self.center = center
            self.distance = distance

            # Calculate corner points from center and distance
            self.a = Point3D(center.x - distance, center.y - distance, center.z - distance)
            self.b = Point3D(center.x + distance, center.y + distance, center.z + distance)
        else:
            # Two-corner mode (default)
            self.a = a if a else Point3D(-1, -1, -1)
            self.b = b if b else Point3D(1, 1, 1)

            # Calculate center and distance for consistency
            self.center = Point3D(
                (self.a.x + self.b.x) / 2,
                (self.a.y + self.b.y) / 2,
                (self.a.z + self.b.z) / 2
            )
            self.distance = max(
                abs(self.b.x - self.a.x) / 2,
                abs(self.b.y - self.a.y) / 2,
                abs(self.b.z - self.a.z) / 2
            )

        # Calculate cube bounds from a and b (opposite corners)
        self.minx = min(self.a.x, self.b.x)
        self.maxx = max(self.a.x, self.b.x)
        self.miny = min(self.a.y, self.b.y)
        self.maxy = max(self.a.y, self.b.y)
        self.minz = min(self.a.z, self.b.z)
        self.maxz = max(self.a.z, self.b.z)

    def hit(self, ray) -> Union[bool, RayIntersection]:
        """Calculate intersection between a ray and this cube using AABB intersection.
        Returns RayIntersection if hit, False otherwise.
        """
        # Handle degenerate cube (all dimensions are zero)
        if (self.maxx - self.minx <= 0 or 
            self.maxy - self.miny <= 0 or 
            self.maxz - self.minz <= 0):
            return False

        # Calculate intersection with each pair of parallel planes
        # X planes
        if abs(ray.dest.x) < self.EPSILON:
            # Ray is parallel to X planes
            if ray.origin.x < self.minx or ray.origin.x > self.maxx:
                return False
            t_min_x = float('-inf')
            t_max_x = float('inf')
        else:
            t1 = (self.minx - ray.origin.x) / ray.dest.x
            t2 = (self.maxx - ray.origin.x) / ray.dest.x
            t_min_x = min(t1, t2)
            t_max_x = max(t1, t2)

        # Y planes
        if abs(ray.dest.y) < self.EPSILON:
            # Ray is parallel to Y planes
            if ray.origin.y < self.miny or ray.origin.y > self.maxy:
                return False
            t_min_y = float('-inf')
            t_max_y = float('inf')
        else:
            t1 = (self.miny - ray.origin.y) / ray.dest.y
            t2 = (self.maxy - ray.origin.y) / ray.dest.y
            t_min_y = min(t1, t2)
            t_max_y = max(t1, t2)

        # Z planes
        if abs(ray.dest.z) < self.EPSILON:
            # Ray is parallel to Z planes
            if ray.origin.z < self.minz or ray.origin.z > self.maxz:
                return False
            t_min_z = float('-inf')
            t_max_z = float('inf')
        else:
            t1 = (self.minz - ray.origin.z) / ray.dest.z
            t2 = (self.maxz - ray.origin.z) / ray.dest.z
            t_min_z = min(t1, t2)
            t_max_z = max(t1, t2)

        # Find the intersection of all three slabs
        t_min = max(t_min_x, t_min_y, t_min_z)
        t_max = min(t_max_x, t_max_y, t_max_z)

        # No intersection if t_min > t_max or if intersection is behind ray origin
        if t_min > t_max or t_max < self.EPSILON:
            return False

        # Choose the appropriate intersection point
        t = t_min if t_min > self.EPSILON else t_max
        if t < self.EPSILON:
            return False

        # Calculate intersection point
        hit_point = Point3D(
            ray.origin.x + t * ray.dest.x,
            ray.origin.y + t * ray.dest.y,
            ray.origin.z + t * ray.dest.z
        )

        # Calculate normal based on which face was hit
        normal = Vector3D(0, 0, 0)

        # Determine which face was hit by checking which coordinate is at the boundary
        if abs(hit_point.x - self.minx) < self.EPSILON:
            normal = Vector3D(-1, 0, 0)  # Left face
        elif abs(hit_point.x - self.maxx) < self.EPSILON:
            normal = Vector3D(1, 0, 0)   # Right face
        elif abs(hit_point.y - self.miny) < self.EPSILON:
            normal = Vector3D(0, -1, 0)  # Bottom face
        elif abs(hit_point.y - self.maxy) < self.EPSILON:
            normal = Vector3D(0, 1, 0)   # Top face
        elif abs(hit_point.z - self.minz) < self.EPSILON:
            normal = Vector3D(0, 0, -1)  # Front face
        elif abs(hit_point.z - self.maxz) < self.EPSILON:
            normal = Vector3D(0, 0, 1)   # Back face

        return RayIntersection(self, normal, hit_point, t)

    def __repr__(self):
        return f"Cube(a={self.a}, b={self.b})"

    def to_json(self) -> Dict[str, Any]:
        """Convert cube to JSON-serializable dictionary."""
        return {
            "type": "cube",
            "a": self.a.to_json(),
            "b": self.b.to_json(),
            "center": self.center.to_json(),
            "distance": self.distance,
            "material": self.material.to_json()
        }

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> 'Cube':
        """Create a Cube instance from JSON data."""
        # Support both old format (a, b) and new format (center, distance)
        if "center" in data and "distance" in data:
            return cls(
                center=Point3D.from_json(data.get("center", {})),
                distance=data.get("distance", 1.0),
                material=Material.from_json(data.get("material", {}))
            )
        else:
            # Legacy format with a, b (and possibly c which we ignore)
            return cls(
                a=Point3D.from_json(data.get("a", {})),
                b=Point3D.from_json(data.get("b", {})),
                material=Material.from_json(data.get("material", {}))
            )


class Cuboid(JsonSerializable):
    """A cuboid (rectangular box) primitive for ray tracing with different dimensions for each axis."""

    EPSILON = 0.001

    def __init__(self, center=None, width=None, height=None, depth=None, material=None):
        """Initialize a cuboid from center point and dimensions.

        Args:
            center: Center point of the cuboid (Point3D)
            width: Width along X-axis (float)
            height: Height along Y-axis (float) 
            depth: Depth along Z-axis (float)
            material: Material of the cuboid (Material)
        """
        self.center = center if center else Point3D(0, 0, 0)
        self.width = width if width is not None and width > 0 else 1.0
        self.height = height if height is not None and height > 0 else 1.0
        self.depth = depth if depth is not None and depth > 0 else 1.0
        self.material = material if material else Material()

        # Calculate bounds
        half_width = self.width / 2.0
        half_height = self.height / 2.0
        half_depth = self.depth / 2.0

        self.minx = self.center.x - half_width
        self.maxx = self.center.x + half_width
        self.miny = self.center.y - half_height
        self.maxy = self.center.y + half_height
        self.minz = self.center.z - half_depth
        self.maxz = self.center.z + half_depth

    def hit(self, ray) -> Union[bool, RayIntersection]:
        """Calculate intersection between a ray and this cuboid using AABB intersection.
        Returns RayIntersection if hit, False otherwise.
        """
        # Handle degenerate cuboid
        if (self.width <= 0 or self.height <= 0 or self.depth <= 0):
            return False

        # Calculate intersection with each pair of parallel planes
        # X planes
        if abs(ray.dest.x) < self.EPSILON:
            if ray.origin.x < self.minx or ray.origin.x > self.maxx:
                return False
            t_min_x = float('-inf')
            t_max_x = float('inf')
        else:
            t1 = (self.minx - ray.origin.x) / ray.dest.x
            t2 = (self.maxx - ray.origin.x) / ray.dest.x
            t_min_x = min(t1, t2)
            t_max_x = max(t1, t2)

        # Y planes
        if abs(ray.dest.y) < self.EPSILON:
            if ray.origin.y < self.miny or ray.origin.y > self.maxy:
                return False
            t_min_y = float('-inf')
            t_max_y = float('inf')
        else:
            t1 = (self.miny - ray.origin.y) / ray.dest.y
            t2 = (self.maxy - ray.origin.y) / ray.dest.y
            t_min_y = min(t1, t2)
            t_max_y = max(t1, t2)

        # Z planes
        if abs(ray.dest.z) < self.EPSILON:
            if ray.origin.z < self.minz or ray.origin.z > self.maxz:
                return False
            t_min_z = float('-inf')
            t_max_z = float('inf')
        else:
            t1 = (self.minz - ray.origin.z) / ray.dest.z
            t2 = (self.maxz - ray.origin.z) / ray.dest.z
            t_min_z = min(t1, t2)
            t_max_z = max(t1, t2)

        # Find the intersection of all three slabs
        t_min = max(t_min_x, t_min_y, t_min_z)
        t_max = min(t_max_x, t_max_y, t_max_z)

        # No intersection if t_min > t_max or if intersection is behind ray origin
        if t_min > t_max or t_max < self.EPSILON:
            return False

        # Choose the appropriate intersection point
        t = t_min if t_min > self.EPSILON else t_max
        if t < self.EPSILON:
            return False

        # Calculate intersection point
        hit_point = Point3D(
            ray.origin.x + t * ray.dest.x,
            ray.origin.y + t * ray.dest.y,
            ray.origin.z + t * ray.dest.z
        )

        # Calculate normal based on which face was hit
        normal = Vector3D(0, 0, 0)

        # Determine which face was hit by checking which coordinate is at the boundary
        if abs(hit_point.x - self.minx) < self.EPSILON:
            normal = Vector3D(-1, 0, 0)  # Left face
        elif abs(hit_point.x - self.maxx) < self.EPSILON:
            normal = Vector3D(1, 0, 0)   # Right face
        elif abs(hit_point.y - self.miny) < self.EPSILON:
            normal = Vector3D(0, -1, 0)  # Bottom face
        elif abs(hit_point.y - self.maxy) < self.EPSILON:
            normal = Vector3D(0, 1, 0)   # Top face
        elif abs(hit_point.z - self.minz) < self.EPSILON:
            normal = Vector3D(0, 0, -1)  # Front face
        elif abs(hit_point.z - self.maxz) < self.EPSILON:
            normal = Vector3D(0, 0, 1)   # Back face

        return RayIntersection(self, normal, hit_point, t)

    def __repr__(self):
        return f"Cuboid(center={self.center}, width={self.width}, height={self.height}, depth={self.depth})"

    def to_json(self) -> Dict[str, Any]:
        """Convert cuboid to JSON-serializable dictionary."""
        return {
            "type": "cuboid",
            "center": self.center.to_json(),
            "width": self.width,
            "height": self.height,
            "depth": self.depth,
            "material": self.material.to_json()
        }

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> 'Cuboid':
        """Create a Cuboid instance from JSON data."""
        return cls(
            center=Point3D.from_json(data.get("center", {})),
            width=data.get("width", 1.0),
            height=data.get("height", 1.0),
            depth=data.get("depth", 1.0),
            material=Material.from_json(data.get("material", {}))
        )


class Cylinder(JsonSerializable):
    """A cylinder primitive for ray tracing."""

    EPSILON = 0.001

    def __init__(self, center=None, radius=None, height=None, material=None):
        """Initialize a cylinder.

        Args:
            center: Center point of the cylinder base (Point3D)
            radius: Radius of the cylinder (float)
            height: Height of the cylinder along Y-axis (float)
            material: Material of the cylinder (Material)
        """
        self.center = center if center else Point3D(0, 0, 0)
        self.radius = radius if radius is not None and radius > 0 else 1.0
        self.height = height if height is not None and height > 0 else 2.0
        self.material = material if material else Material()

        # Calculate Y bounds
        self.min_y = self.center.y
        self.max_y = self.center.y + self.height

    def hit(self, ray) -> Union[bool, RayIntersection]:
        """Calculate intersection between a ray and this cylinder.
        Returns RayIntersection if hit, False otherwise.
        """
        if self.radius <= 0 or self.height <= 0:
            return False

        # Transform ray to cylinder's local coordinate system
        # Cylinder is aligned along Y-axis with base at center
        oc = Vector3D(
            ray.origin.x - self.center.x,
            ray.origin.y - self.center.y,
            ray.origin.z - self.center.z
        )

        # Quadratic equation for infinite cylinder (ignoring Y bounds for now)
        # We solve for intersection with infinite cylinder in XZ plane
        a = ray.dest.x * ray.dest.x + ray.dest.z * ray.dest.z
        b = 2.0 * (oc.x * ray.dest.x + oc.z * ray.dest.z)
        c = oc.x * oc.x + oc.z * oc.z - self.radius * self.radius

        # Check if ray is parallel to cylinder axis
        if abs(a) < self.EPSILON:
            # Ray is parallel to Y-axis, check if it's inside cylinder
            if c > self.EPSILON:
                return False  # Ray misses cylinder
            # Ray is inside cylinder, check Y bounds
            if abs(ray.dest.y) < self.EPSILON:
                return False  # Ray is parallel to cylinder and inside

            # Find intersection with top/bottom caps
            t_bottom = (self.min_y - ray.origin.y) / ray.dest.y
            t_top = (self.max_y - ray.origin.y) / ray.dest.y

            t = None
            if t_bottom > self.EPSILON:
                t = t_bottom
                normal = Vector3D(0, -1, 0)  # Bottom cap normal
            elif t_top > self.EPSILON:
                t = t_top
                normal = Vector3D(0, 1, 0)   # Top cap normal
            else:
                return False

            hit_point = Point3D(
                ray.origin.x + t * ray.dest.x,
                ray.origin.y + t * ray.dest.y,
                ray.origin.z + t * ray.dest.z
            )

            return RayIntersection(self, normal, hit_point, t)

        # Solve quadratic equation
        discriminant = b * b - 4.0 * a * c
        if discriminant < 0:
            return False

        sqrt_discriminant = math.sqrt(discriminant)
        inv_denom = 0.5 / a
        t1 = (-b - sqrt_discriminant) * inv_denom
        t2 = (-b + sqrt_discriminant) * inv_denom

        # Check both intersection points
        candidates = []

        for t in [t1, t2]:
            if t > self.EPSILON:
                # Calculate intersection point
                hit_y = ray.origin.y + t * ray.dest.y

                # Check if intersection is within cylinder height
                if self.min_y <= hit_y <= self.max_y:
                    hit_point = Point3D(
                        ray.origin.x + t * ray.dest.x,
                        hit_y,
                        ray.origin.z + t * ray.dest.z
                    )

                    # Calculate normal (pointing outward from cylinder axis)
                    normal = Vector3D(
                        (hit_point.x - self.center.x) / self.radius,
                        0,
                        (hit_point.z - self.center.z) / self.radius
                    )

                    candidates.append((t, hit_point, normal))

        # Also check intersection with top and bottom caps
        if abs(ray.dest.y) > self.EPSILON:
            # Bottom cap
            t_bottom = (self.min_y - ray.origin.y) / ray.dest.y
            if t_bottom > self.EPSILON:
                hit_x = ray.origin.x + t_bottom * ray.dest.x
                hit_z = ray.origin.z + t_bottom * ray.dest.z
                dist_sq = (hit_x - self.center.x) ** 2 + (hit_z - self.center.z) ** 2
                if dist_sq <= self.radius * self.radius:
                    hit_point = Point3D(hit_x, self.min_y, hit_z)
                    normal = Vector3D(0, -1, 0)
                    candidates.append((t_bottom, hit_point, normal))

            # Top cap
            t_top = (self.max_y - ray.origin.y) / ray.dest.y
            if t_top > self.EPSILON:
                hit_x = ray.origin.x + t_top * ray.dest.x
                hit_z = ray.origin.z + t_top * ray.dest.z
                dist_sq = (hit_x - self.center.x) ** 2 + (hit_z - self.center.z) ** 2
                if dist_sq <= self.radius * self.radius:
                    hit_point = Point3D(hit_x, self.max_y, hit_z)
                    normal = Vector3D(0, 1, 0)
                    candidates.append((t_top, hit_point, normal))

        # Return the closest valid intersection
        if candidates:
            t, hit_point, normal = min(candidates, key=lambda x: x[0])
            return RayIntersection(self, normal, hit_point, t)

        return False

    def __repr__(self):
        return f"Cylinder(center={self.center}, radius={self.radius}, height={self.height})"

    def to_json(self) -> Dict[str, Any]:
        """Convert cylinder to JSON-serializable dictionary."""
        return {
            "type": "cylinder",
            "center": self.center.to_json(),
            "radius": self.radius,
            "height": self.height,
            "material": self.material.to_json()
        }

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> 'Cylinder':
        """Create a Cylinder instance from JSON data."""
        return cls(
            center=Point3D.from_json(data.get("center", {})),
            radius=data.get("radius", 1.0),
            height=data.get("height", 2.0),
            material=Material.from_json(data.get("material", {}))
        )


class Toroid(JsonSerializable):
    """A toroid (donut shape) primitive for ray tracing."""

    EPSILON = 0.001

    def __init__(self, center=None, major_radius=None, minor_radius=None, material=None):
        """Initialize a toroid.

        Args:
            center: Center point of the toroid (Point3D)
            major_radius: Major radius (distance from center to tube center) (float)
            minor_radius: Minor radius (tube radius) (float)
            material: Material of the toroid (Material)
        """
        self.center = center if center else Point3D(0, 0, 0)
        self.major_radius = major_radius if major_radius is not None and major_radius > 0 else 2.0
        self.minor_radius = minor_radius if minor_radius is not None and minor_radius > 0 else 0.5
        self.material = material if material else Material()

        # Ensure major_radius > minor_radius for a valid toroid
        if self.major_radius <= self.minor_radius:
            self.major_radius = self.minor_radius + 1.0

    def hit(self, ray) -> Union[bool, RayIntersection]:
        """Calculate intersection between a ray and this toroid.
        Returns RayIntersection if hit, False otherwise.

        This uses the quartic equation method for ray-torus intersection.
        """
        if self.major_radius <= 0 or self.minor_radius <= 0:
            return False

        # Transform ray to toroid's local coordinate system
        oc = Vector3D(
            ray.origin.x - self.center.x,
            ray.origin.y - self.center.y,
            ray.origin.z - self.center.z
        )

        # Toroid equation: (sqrt(x² + z²) - R)² + y² = r²
        # Where R = major_radius, r = minor_radius
        R = self.major_radius
        r = self.minor_radius

        # Ray equation: P = O + t*D
        # Substitute into torus equation to get quartic equation in t

        # Precompute some values
        ox, oy, oz = oc.x, oc.y, oc.z
        dx, dy, dz = ray.dest.x, ray.dest.y, ray.dest.z

        # Coefficients for the quartic equation at⁴ + bt³ + ct² + dt + e = 0
        sum_d_sqr = dx*dx + dy*dy + dz*dz
        e_dot_d = ox*dx + oy*dy + oz*dz
        sum_e_sqr = ox*ox + oy*oy + oz*oz

        # More precomputed values
        R_sqr = R * R
        r_sqr = r * r

        # Quartic coefficients
        a = sum_d_sqr * sum_d_sqr
        b = 4.0 * sum_d_sqr * e_dot_d
        c = 2.0 * sum_d_sqr * (sum_e_sqr - r_sqr - R_sqr) + 4.0 * e_dot_d * e_dot_d + 4.0 * R_sqr * dy * dy
        d = 4.0 * e_dot_d * (sum_e_sqr - r_sqr - R_sqr) + 8.0 * R_sqr * oy * dy
        e = (sum_e_sqr - r_sqr - R_sqr) * (sum_e_sqr - r_sqr - R_sqr) - 4.0 * R_sqr * (r_sqr - oy * oy)

        # Solve quartic equation (simplified approach - we'll use a numerical method)
        # For simplicity, we'll use a more direct approach with multiple attempts

        # Try to find roots using a simplified method
        # This is a simplified version - in practice, you'd want a more robust quartic solver
        candidates = []

        # Sample multiple t values and look for sign changes (root finding)
        # This is not the most efficient method but works for basic cases
        max_t = 100.0
        step = 0.1
        prev_val = None
        prev_t = 0

        for i in range(int(max_t / step)):
            t = i * step + self.EPSILON

            # Evaluate quartic at t
            val = a * t**4 + b * t**3 + c * t**2 + d * t + e

            if prev_val is not None and prev_val * val < 0:
                # Sign change detected, refine the root
                t_root = self._refine_root(a, b, c, d, e, prev_t, t)
                if t_root > self.EPSILON:
                    candidates.append(t_root)

            prev_val = val
            prev_t = t

        # Check candidates and find the closest valid intersection
        valid_intersections = []

        for t in candidates:
            if t > self.EPSILON:
                # Calculate intersection point
                hit_point = Point3D(
                    ray.origin.x + t * ray.dest.x,
                    ray.origin.y + t * ray.dest.y,
                    ray.origin.z + t * ray.dest.z
                )

                # Calculate normal at intersection point
                normal = self._calculate_toroid_normal(hit_point)
                if normal:
                    valid_intersections.append((t, hit_point, normal))

        if valid_intersections:
            t, hit_point, normal = min(valid_intersections, key=lambda x: x[0])
            return RayIntersection(self, normal, hit_point, t)

        return False

    def _refine_root(self, a, b, c, d, e, t1, t2, max_iterations=10):
        """Refine root using bisection method."""
        for _ in range(max_iterations):
            t_mid = (t1 + t2) / 2.0
            val_mid = a * t_mid**4 + b * t_mid**3 + c * t_mid**2 + d * t_mid + e
            val1 = a * t1**4 + b * t1**3 + c * t1**2 + d * t1 + e

            if abs(val_mid) < self.EPSILON:
                return t_mid

            if val1 * val_mid < 0:
                t2 = t_mid
            else:
                t1 = t_mid

        return (t1 + t2) / 2.0

    def _calculate_toroid_normal(self, point):
        """Calculate normal vector at a point on the toroid surface."""
        # Transform point to local coordinates
        px = point.x - self.center.x
        py = point.y - self.center.y
        pz = point.z - self.center.z

        # Calculate normal using toroid geometry
        # Distance from Y-axis in XZ plane
        rho = math.sqrt(px*px + pz*pz)

        if rho < self.EPSILON:
            return None  # Degenerate case

        # Normal calculation for torus
        # The normal points away from the tube center
        factor = 1.0 - self.major_radius / rho

        nx = factor * px
        ny = py
        nz = factor * pz

        # Normalize
        length = math.sqrt(nx*nx + ny*ny + nz*nz)
        if length < self.EPSILON:
            return None

        return Vector3D(nx/length, ny/length, nz/length)

    def __repr__(self):
        return f"Toroid(center={self.center}, major_radius={self.major_radius}, minor_radius={self.minor_radius})"

    def to_json(self) -> Dict[str, Any]:
        """Convert toroid to JSON-serializable dictionary."""
        return {
            "type": "toroid",
            "center": self.center.to_json(),
            "major_radius": self.major_radius,
            "minor_radius": self.minor_radius,
            "material": self.material.to_json()
        }

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> 'Toroid':
        """Create a Toroid instance from JSON data."""
        return cls(
            center=Point3D.from_json(data.get("center", {})),
            major_radius=data.get("major_radius", 2.0),
            minor_radius=data.get("minor_radius", 0.5),
            material=Material.from_json(data.get("material", {}))
        )
