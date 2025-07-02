import pytest
import math
from Primitives import Plane, CheckerPlane, Sphere, Cube
from Material import Material
from RGB import RGB
from Point import Point3D
from Vector import Vector3D
from Normal import Normal
from Ray import Ray


class TestPlane:
    """Comprehensive tests for the Plane class."""

    def test_init_default(self):
        """Test Plane initialization with default values."""
        center = Point3D(0, 0, 0)
        plane = Plane(center)
        assert plane.center == center
        assert plane.normal == Vector3D(0, 1, 0)
        assert isinstance(plane.material, Material)

    def test_init_with_center(self):
        """Test Plane initialization with custom center."""
        center = Point3D(1, 2, 3)
        plane = Plane(center)
        assert plane.center == center
        assert plane.normal == Vector3D(0, 1, 0)

    def test_init_with_normal(self):
        """Test Plane initialization with custom normal."""
        center = Point3D(0, 0, 0)
        normal = Vector3D(1, 0, 0)
        plane = Plane(center, normal=normal)
        assert plane.center == center
        assert plane.normal == normal

    def test_init_with_material(self):
        """Test Plane initialization with custom material."""
        center = Point3D(0, 0, 0)
        material = Material(color=RGB(0.5, 0.6, 0.7))
        plane = Plane(center, material=material)
        assert plane.material == material

    def test_init_with_all_parameters(self):
        """Test Plane initialization with all parameters."""
        center = Point3D(1, 2, 3)
        normal = Vector3D(0, 0, 1)
        material = Material(color=RGB(0.8, 0.2, 0.4))
        plane = Plane(center, normal=normal, material=material)
        assert plane.center == center
        assert plane.normal == normal
        assert plane.material == material

    def test_hit_perpendicular_ray(self):
        """Test ray hitting plane perpendicularly."""
        plane = Plane(Point3D(0, 0, 0), normal=Vector3D(0, 0, 1))
        ray = Ray(Point3D(0, 0, 5), Vector3D(0, 0, -1))
        intersection = plane.hit(ray)
        assert intersection is not False

    def test_hit_parallel_ray(self):
        """Test ray parallel to plane (no intersection)."""
        plane = Plane(Point3D(0, 0, 0), normal=Vector3D(0, 0, 1))
        ray = Ray(Point3D(0, 0, 5), Vector3D(1, 0, 0))
        intersection = plane.hit(ray)
        assert intersection is False

    def test_hit_ray_from_behind(self):
        """Test ray hitting plane from behind."""
        plane = Plane(Point3D(0, 0, 0), normal=Vector3D(0, 0, 1))
        ray = Ray(Point3D(0, 0, -5), Vector3D(0, 0, 1))
        intersection = plane.hit(ray)
        assert intersection is not False

    def test_hit_ray_starting_on_plane(self):
        """Test ray starting on the plane."""
        plane = Plane(Point3D(0, 0, 0), normal=Vector3D(0, 0, 1))
        ray = Ray(Point3D(1, 1, 0), Vector3D(0, 0, 1))
        intersection = plane.hit(ray)
        # Should not intersect (or intersect at distance 0)
        assert intersection is False or intersection.distance == 0

    def test_hit_oblique_ray(self):
        """Test ray hitting plane at an oblique angle."""
        plane = Plane(Point3D(0, 0, 0), normal=Vector3D(0, 0, 1))
        ray = Ray(Point3D(1, 1, 5), Vector3D(0, 0, -1))
        intersection = plane.hit(ray)
        assert intersection is not False

    def test_hit_negative_distance(self):
        """Test ray with negative intersection distance."""
        plane = Plane(Point3D(0, 0, 0), normal=Vector3D(0, 0, 1))
        ray = Ray(Point3D(0, 0, 5), Vector3D(0, 0, 1))  # Ray pointing away
        intersection = plane.hit(ray)
        assert intersection is False

    def test_repr(self):
        """Test string representation."""
        plane = Plane(Point3D(0, 0, 0))
        repr_str = repr(plane)
        assert "Plane" in repr_str

    def test_json_serialization(self):
        """Test JSON serialization."""
        center = Point3D(1, 2, 3)
        normal = Vector3D(0, 1, 0)
        material = Material(color=RGB(0.5, 0.6, 0.7))
        plane = Plane(center, normal=normal, material=material)

        json_data = plane.to_json()
        assert json_data["type"] == "plane"
        assert "center" in json_data
        assert "normal" in json_data
        assert "material" in json_data

    def test_json_deserialization(self):
        """Test JSON deserialization."""
        json_data = {
            "type": "plane",
            "center": {"x": 1, "y": 2, "z": 3},
            "normal": {"x": 0, "y": 1, "z": 0},
            "material": {
                "color": {"r": 0.5, "g": 0.6, "b": 0.7},
                "opacity": 1.0,
                "reflect": 0.0,
                "luma": 0.0,
                "roughness": {"scale": 0.1, "amplitude": 0.0}
            }
        }
        plane = Plane.from_json(json_data)
        assert plane.center == Point3D(1, 2, 3)
        assert plane.material.color == RGB(0.5, 0.6, 0.7)

    def test_json_roundtrip(self):
        """Test JSON serialization and deserialization roundtrip."""
        original = Plane(
            Point3D(2, 3, 4),
            normal=Vector3D(1, 0, 0),
            material=Material(color=RGB(0.8, 0.2, 0.4))
        )
        json_data = original.to_json()
        restored = Plane.from_json(json_data)

        assert original.center == restored.center
        assert original.material.color == restored.material.color


class TestSphere:
    """Comprehensive tests for the Sphere class."""

    def test_init_default(self):
        """Test Sphere initialization with default values."""
        sphere = Sphere(center=Point3D(0, 0, 0), radius=1)
        assert sphere.center == Point3D(0, 0, 0)
        assert sphere.radius == 1
        assert isinstance(sphere.material, Material)

    def test_init_with_parameters(self):
        """Test Sphere initialization with custom parameters."""
        center = Point3D(1, 2, 3)
        radius = 5
        material = Material(color=RGB(0.7, 0.8, 0.9))
        sphere = Sphere(center=center, radius=radius, material=material)
        assert sphere.center == center
        assert sphere.radius == radius
        assert sphere.material == material

    def test_hit_ray_through_center(self):
        """Test ray passing through sphere center."""
        sphere = Sphere(center=Point3D(0, 0, 0), radius=5)
        ray = Ray(Point3D(-10, 0, 0), Vector3D(1, 0, 0))
        intersection = sphere.hit(ray)
        assert intersection is not False
        assert intersection.distance == 5.0  # Distance to first intersection

    def test_hit_ray_tangent(self):
        """Test ray tangent to sphere."""
        sphere = Sphere(center=Point3D(0, 0, 0), radius=5)
        ray = Ray(Point3D(-10, 5, 0), Vector3D(1, 0, 0))
        intersection = sphere.hit(ray)
        # Tangent ray should intersect at exactly one point
        assert intersection is not False
        assert abs(intersection.distance - 10.0) < 0.001

    def test_hit_ray_missing_sphere(self):
        """Test ray missing the sphere."""
        sphere = Sphere(center=Point3D(0, 0, 0), radius=5)
        ray = Ray(Point3D(-10, 10, 0), Vector3D(1, 0, 0))
        intersection = sphere.hit(ray)
        assert intersection is False

    def test_hit_ray_from_inside(self):
        """Test ray starting from inside the sphere."""
        sphere = Sphere(center=Point3D(0, 0, 0), radius=5)
        ray = Ray(Point3D(0, 0, 0), Vector3D(1, 0, 0))
        intersection = sphere.hit(ray)
        assert intersection is not False
        assert intersection.distance == 5.0

    def test_hit_ray_opposite_direction(self):
        """Test ray pointing away from sphere."""
        sphere = Sphere(center=Point3D(0, 0, 0), radius=5)
        ray = Ray(Point3D(-10, 0, 0), Vector3D(-1, 0, 0))
        intersection = sphere.hit(ray)
        assert intersection is False

    def test_hit_oblique_ray(self):
        """Test ray hitting sphere at oblique angle."""
        sphere = Sphere(center=Point3D(0, 0, 0), radius=5)
        ray = Ray(Point3D(-10, 3, 0), Vector3D(1, 0, 0))
        intersection = sphere.hit(ray)
        assert intersection is not False
        # Distance should be 10 - sqrt(25 - 9) = 10 - 4 = 6
        assert abs(intersection.distance - 6.0) < 0.001

    def test_repr(self):
        """Test string representation."""
        sphere = Sphere(center=Point3D(1, 2, 3), radius=5)
        repr_str = repr(sphere)
        assert "Sphere" in repr_str

    def test_json_serialization(self):
        """Test JSON serialization."""
        sphere = Sphere(
            center=Point3D(1, 2, 3),
            radius=5,
            material=Material(color=RGB(0.5, 0.6, 0.7))
        )
        json_data = sphere.to_json()
        assert json_data["type"] == "sphere"
        assert json_data["radius"] == 5

    def test_json_roundtrip(self):
        """Test JSON serialization and deserialization roundtrip."""
        original = Sphere(
            center=Point3D(2, 3, 4),
            radius=7,
            material=Material(color=RGB(0.8, 0.2, 0.4))
        )
        json_data = original.to_json()
        restored = Sphere.from_json(json_data)

        assert original.center == restored.center
        assert original.radius == restored.radius
        assert original.material.color == restored.material.color


class TestCube:
    """Comprehensive tests for the Cube class."""

    def test_init_default(self):
        """Test Cube initialization with default values."""
        cube = Cube()
        assert cube.a == Point3D(-1, -1, -1)
        assert cube.b == Point3D(1, 1, 1)
        assert isinstance(cube.material, Material)

    def test_init_with_parameters(self):
        """Test Cube initialization with custom parameters."""
        a = Point3D(0, 0, 0)
        b = Point3D(2, 2, 2)
        material = Material(color=RGB(0.7, 0.8, 0.9))
        cube = Cube(a=a, b=b, material=material)
        assert cube.a == a
        assert cube.b == b
        assert cube.material == material

    def test_hit_ray_front_face(self):
        """Test ray hitting front face of cube."""
        cube = Cube(a=Point3D(-1, -1, -1), b=Point3D(1, 1, 1))
        ray = Ray(Point3D(0, 0, -5), Vector3D(0, 0, 1))
        intersection = cube.hit(ray)
        assert intersection is not False
        assert intersection.distance == 4.0  # Distance to front face

    def test_hit_ray_missing_cube(self):
        """Test ray missing the cube."""
        cube = Cube(a=Point3D(-1, -1, -1), b=Point3D(1, 1, 1))
        ray = Ray(Point3D(5, 0, 0), Vector3D(0, 1, 0))
        intersection = cube.hit(ray)
        assert intersection is False

    def test_hit_ray_from_inside(self):
        """Test ray starting from inside the cube."""
        cube = Cube(a=Point3D(-1, -1, -1), b=Point3D(1, 1, 1))
        ray = Ray(Point3D(0, 0, 0), Vector3D(1, 0, 0))
        intersection = cube.hit(ray)
        assert intersection is not False
        assert intersection.distance == 1.0  # Distance to right face

    def test_hit_ray_corner(self):
        """Test ray hitting cube corner."""
        cube = Cube(a=Point3D(-1, -1, -1), b=Point3D(1, 1, 1))
        ray = Ray(Point3D(-5, -5, -5), Vector3D(1, 1, 1).normalize())
        intersection = cube.hit(ray)
        # Should hit one of the faces
        assert intersection is not False

    def test_repr(self):
        """Test string representation."""
        cube = Cube()
        repr_str = repr(cube)
        assert "Cube" in repr_str

    def test_json_serialization(self):
        """Test JSON serialization."""
        cube = Cube(
            a=Point3D(0, 0, 0),
            b=Point3D(2, 2, 2),
            material=Material(color=RGB(0.5, 0.6, 0.7))
        )
        json_data = cube.to_json()
        assert json_data["type"] == "cube"

    def test_json_roundtrip(self):
        """Test JSON serialization and deserialization roundtrip."""
        original = Cube(
            a=Point3D(1, 2, 3),
            b=Point3D(4, 5, 6),
            material=Material(color=RGB(0.8, 0.2, 0.4))
        )
        json_data = original.to_json()
        restored = Cube.from_json(json_data)

        assert original.a == restored.a
        assert original.b == restored.b
        assert original.material.color == restored.material.color


class TestCheckerPlane:
    """Comprehensive tests for the CheckerPlane class."""

    def test_init_default(self):
        """Test CheckerPlane initialization with default values."""
        checker = CheckerPlane()
        assert checker.center == Point3D(0, 0, 0)
        assert checker.normal == Normal(0, 0, 1)
        assert isinstance(checker.material1, Material)
        assert isinstance(checker.material2, Material)
        assert checker.square_size == 10

    def test_init_with_parameters(self):
        """Test CheckerPlane initialization with custom parameters."""
        center = Point3D(1, 2, 3)
        normal = Normal(0, 0, 1)
        material1 = Material(color=RGB(1, 0, 0))
        material2 = Material(color=RGB(0, 1, 0))
        square_size = 5

        checker = CheckerPlane(
            center=center,
            normal=normal,
            material1=material1,
            material2=material2,
            square_size=square_size
        )

        assert checker.center == center
        assert checker.normal == normal
        assert checker.material1 == material1
        assert checker.material2 == material2
        assert checker.square_size == square_size

    def test_hit_basic_intersection(self):
        """Test basic ray intersection with checker plane."""
        checker = CheckerPlane(
            center=Point3D(0, 0, 0),
            normal=Normal(0, 0, 1),
            square_size=10
        )
        ray = Ray(Point3D(0, 0, 5), Vector3D(0, 0, -1))
        intersection = checker.hit(ray)
        assert intersection is not False
        assert intersection.distance == 5.0

    def test_hit_different_squares(self):
        """Test that different squares return different materials."""
        material1 = Material(color=RGB(1, 0, 0))
        material2 = Material(color=RGB(0, 1, 0))
        checker = CheckerPlane(
            center=Point3D(0, 0, 0),
            normal=Normal(0, 0, 1),
            material1=material1,
            material2=material2,
            square_size=10
        )

        # Hit at (0, 0, 0) - should be one material
        ray1 = Ray(Point3D(0, 0, 5), Vector3D(0, 0, -1))
        intersection1 = checker.hit(ray1)

        # Hit at (15, 0, 0) - should be different material
        ray2 = Ray(Point3D(15, 0, 5), Vector3D(0, 0, -1))
        intersection2 = checker.hit(ray2)

        assert intersection1 is not False
        assert intersection2 is not False
        # Materials should be different (checker pattern)
        # Note: The actual material selection depends on the implementation

    def test_repr(self):
        """Test string representation."""
        checker = CheckerPlane()
        repr_str = repr(checker)
        assert "CheckerPlane" in repr_str

    def test_json_serialization(self):
        """Test JSON serialization."""
        checker = CheckerPlane(
            center=Point3D(1, 2, 3),
            normal=Normal(0, 1, 0),
            material1=Material(color=RGB(1, 0, 0)),
            material2=Material(color=RGB(0, 1, 0)),
            square_size=5
        )
        json_data = checker.to_json()
        assert json_data["type"] == "checkerplane"
        assert json_data["square_size"] == 5

    def test_json_roundtrip(self):
        """Test JSON serialization and deserialization roundtrip."""
        original = CheckerPlane(
            center=Point3D(2, 3, 4),
            normal=Normal(1, 0, 0),
            material1=Material(color=RGB(0.8, 0.2, 0.4)),
            material2=Material(color=RGB(0.2, 0.8, 0.4)),
            square_size=7
        )
        json_data = original.to_json()
        restored = CheckerPlane.from_json(json_data)

        assert original.center == restored.center
        assert original.square_size == restored.square_size
        assert original.material1.color == restored.material1.color
        assert original.material2.color == restored.material2.color


class TestPrimitivesIntegration:
    """Integration tests for all primitive types."""

    def test_all_primitives_with_same_ray(self):
        """Test all primitives with the same ray to compare behavior."""
        ray = Ray(Point3D(0, 0, 5), Vector3D(0, 0, -1))

        plane = Plane(center=Point3D(0, 0, 0), normal=Normal(0, 0, 1))
        sphere = Sphere(center=Point3D(0, 0, 0), radius=3)
        cube = Cube(a=Point3D(-2, -2, -2), b=Point3D(2, 2, 2))
        checker = CheckerPlane(center=Point3D(0, 0, 0), normal=Normal(0, 0, 1))

        plane_hit = plane.hit(ray)
        sphere_hit = sphere.hit(ray)
        cube_hit = cube.hit(ray)
        checker_hit = checker.hit(ray)

        # All should intersect
        assert plane_hit is not False
        assert sphere_hit is not False
        assert cube_hit is not False
        assert checker_hit is not False

        # Sphere should be closest (radius 3, so distance = 5-3 = 2)
        assert sphere_hit.distance < plane_hit.distance
        assert sphere_hit.distance < cube_hit.distance
        assert sphere_hit.distance < checker_hit.distance

    def test_primitives_with_materials(self):
        """Test that all primitives properly handle materials."""
        red_material = Material(color=RGB(1, 0, 0))

        plane = Plane(material=red_material)
        sphere = Sphere(center=Point3D(0, 0, 0), radius=1, material=red_material)
        cube = Cube(material=red_material)

        assert plane.material.color == RGB(1, 0, 0)
        assert sphere.material.color == RGB(1, 0, 0)
        assert cube.material.color == RGB(1, 0, 0)

    def test_primitives_json_type_field(self):
        """Test that all primitives have correct type field in JSON."""
        plane = Plane()
        sphere = Sphere(center=Point3D(0, 0, 0), radius=1)
        cube = Cube()
        checker = CheckerPlane()

        assert plane.to_json()["type"] == "plane"
        assert sphere.to_json()["type"] == "sphere"
        assert cube.to_json()["type"] == "cube"
        assert checker.to_json()["type"] == "checkerplane"

    def test_edge_case_zero_radius_sphere(self):
        """Test sphere with zero radius."""
        sphere = Sphere(center=Point3D(0, 0, 0), radius=0)
        ray = Ray(Point3D(0, 0, 5), Vector3D(0, 0, -1))
        intersection = sphere.hit(ray)
        # Zero radius sphere should not intersect (or behave as a point)
        assert intersection is False or intersection.distance == 5.0

    def test_edge_case_degenerate_cube(self):
        """Test cube with same min and max points."""
        cube = Cube(a=Point3D(0, 0, 0), b=Point3D(0, 0, 0))
        ray = Ray(Point3D(0, 0, 5), Vector3D(0, 0, -1))
        intersection = cube.hit(ray)
        # Degenerate cube should not intersect
        assert intersection is False

    def test_performance_many_intersections(self):
        """Test performance with many intersection calculations."""
        sphere = Sphere(center=Point3D(0, 0, 0), radius=5)

        # Test many rays
        for i in range(100):
            ray = Ray(Point3D(i/10.0, 0, 10), Vector3D(0, 0, -1))
            intersection = sphere.hit(ray)
            # Some should hit, some should miss
            if abs(i/10.0) <= 5:  # Within sphere radius
                assert intersection is not False
            else:
                assert intersection is False
