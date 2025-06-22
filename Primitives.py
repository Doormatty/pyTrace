from __future__ import annotations

import math
from typing import Union, Dict, Any

from JsonSerializable import JsonSerializable
from Material import Material
from Point import Point3D
from Vector import Vector3D
from RayIntersection import RayIntersection


class Plane(JsonSerializable):
    """A plane primitive for ray tracing."""
    center: Point3D
    normal: Vector3D
    material: Material

    # Small constant to avoid self-intersection due to floating point errors
    EPSILON = 0.001

    def __init__(self, center, normal=None, material=None) -> None:
        self.center = center
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
            return RayIntersection(self, self.normal, intersection_point)

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


class Sphere(JsonSerializable):
    """A sphere primitive for ray tracing."""
    center: Point3D
    radius: Union[float, int]
    material: Material

    # Small constant to avoid self-intersection due to floating point errors
    EPSILON = 0.01

    def __init__(self, center, radius, material=None):
        self.center = center
        self.radius = radius if radius else 1.0
        self.material = material if material else Material()

    def hit(self, ray) -> Union[bool, RayIntersection]:
        """Calculate intersection between a ray and this sphere.
        Returns RayIntersection if hit, False otherwise.
        """
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

        # Calculate nearest hit point - use inverse of denominator to avoid division
        sqrt_discriminant = math.sqrt(discriminant)
        inv_denom = 0.5 / a
        t = (-b - sqrt_discriminant) * inv_denom

        # Check if intersection is in front of ray origin
        if t > self.EPSILON:
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

            return RayIntersection(self, normal, intersection_point)

        return False

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
    """A cube primitive for ray tracing, defined by three corner points."""

    EPSILON = 0.001

    def __init__(self, a=None, b=None, c=None, material=None) -> None:
        """Initialize a cube from three corner points and material."""
        self.a = a if a else Point3D()
        self.b = b if b else Point3D()
        self.c = c if c else Point3D()
        self.material = material if material else Material()

        # Calculate the 8th vertex from the given three corners
        self.tpoint = Point3D(self.a.x, self.b.y, self.c.z)

        # Define the six faces of the cube
        self.faces = [
            # Each face is defined by (point1, point2, midpoint, normal)
            (self.a, self.b, self.a - (self.a.distance(self.b) / 2), Vector3D(0, 0, -1)),
            (self.b, self.tpoint, self.b - (self.b.distance(self.tpoint) / 2), Vector3D(0, 1, 0)),
            (self.a, self.c, self.a - (self.a.distance(self.c) / 2), Vector3D(0, -1, 0)),
            (self.a, self.tpoint, self.a - (self.a.distance(self.tpoint) / 2), Vector3D(1, 0, 0)),
            (self.b, self.c, self.b - (self.b.distance(self.c) / 2), Vector3D(-1, 0, 0)),
            (self.c, self.tpoint, self.c - (self.c.distance(self.tpoint) / 2), Vector3D(0, 0, 1)),
        ]

        # Calculate cube bounds
        self.maxx = max(self.a.x, self.b.x, self.c.x)
        self.minx = min(self.a.x, self.b.x, self.c.x)
        self.maxy = max(self.a.y, self.b.y, self.c.y)
        self.miny = min(self.a.y, self.b.y, self.c.y)
        self.maxz = max(self.a.z, self.b.z, self.c.z)
        self.minz = min(self.a.z, self.b.z, self.c.z)

    def hit(self, ray) -> Union[bool, RayIntersection]:
        """Calculate intersection between a ray and this cube.
        Returns RayIntersection if hit, False otherwise.
        """
        hits = []

        for vertex1, vertex2, midpoint, normal in self.faces:
            # Calculate denominator (dot product of ray direction and face normal)
            denominator = ray.dest * normal

            # Skip if ray is parallel to face
            if abs(denominator) < self.EPSILON:
                continue

            # Calculate distance to plane intersection
            t = ((midpoint - ray.origin) * normal) / denominator

            # Skip if intersection is behind ray origin
            if t < self.EPSILON:
                continue

            # Calculate the intersection point
            hit_point = ray.origin + (t * ray.dest)

            # Check if point is within cube bounds
            if (self.minx <= hit_point.x <= self.maxx and
                    self.miny <= hit_point.y <= self.maxy and
                    self.minz <= hit_point.z <= self.maxz):
                hits.append((hit_point, normal))

        # Need at least one hit to return a valid intersection
        if not hits:
            return False

        # Sort hits by distance and return closest one
        hits.sort(key=lambda h: ray.origin.distance(h[0]))
        return RayIntersection(self, hits[0][1], hits[0][0])

    def __repr__(self):
        return f"Cube(a={self.a}, b={self.b}, c={self.c})"

    def to_json(self) -> Dict[str, Any]:
        """Convert cube to JSON-serializable dictionary."""
        return {
            "type": "cube",
            "a": self.a.to_json(),
            "b": self.b.to_json(),
            "c": self.c.to_json(),
            "material": self.material.to_json()
        }

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> 'Cube':
        """Create a Cube instance from JSON data."""
        return cls(
            a=Point3D.from_json(data.get("a", {})),
            b=Point3D.from_json(data.get("b", {})),
            c=Point3D.from_json(data.get("c", {})),
            material=Material.from_json(data.get("material", {}))
        )

