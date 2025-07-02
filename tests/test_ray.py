import pytest
from Ray import Ray
from Point import Point3D
from Vector import Vector3D


class TestRay:
    """Comprehensive tests for the Ray class."""

    def test_init_default(self):
        """Test Ray initialization with default values."""
        ray = Ray()
        assert ray.origin == Point3D(0, 0, 0)
        assert ray.dest == Vector3D(0, 0, 0)

    def test_init_with_origin_only(self):
        """Test Ray initialization with origin only."""
        origin = Point3D(1, 2, 3)
        ray = Ray(origin=origin)
        assert ray.origin == origin
        assert ray.dest == Vector3D(0, 0, 0)

    def test_init_with_dest_only(self):
        """Test Ray initialization with destination only."""
        dest = Vector3D(1, 0, 0)
        ray = Ray(dest=dest)
        assert ray.origin == Point3D(0, 0, 0)
        assert ray.dest == dest

    def test_init_with_both_parameters(self):
        """Test Ray initialization with both origin and destination."""
        origin = Point3D(1, 2, 3)
        dest = Vector3D(0, 1, 0)
        ray = Ray(origin=origin, dest=dest)
        assert ray.origin == origin
        assert ray.dest == dest

    def test_init_with_positional_arguments(self):
        """Test Ray initialization with positional arguments."""
        origin = Point3D(5, 6, 7)
        dest = Vector3D(0, 0, 1)
        ray = Ray(origin, dest)
        assert ray.origin == origin
        assert ray.dest == dest

    def test_init_with_none_origin(self):
        """Test Ray initialization with None origin."""
        dest = Vector3D(1, 1, 1)
        ray = Ray(origin=None, dest=dest)
        assert ray.origin == Point3D(0, 0, 0)
        assert ray.dest == dest

    def test_init_with_none_dest(self):
        """Test Ray initialization with None destination."""
        origin = Point3D(2, 3, 4)
        ray = Ray(origin=origin, dest=None)
        assert ray.origin == origin
        assert ray.dest == Vector3D(0, 0, 0)

    def test_init_with_both_none(self):
        """Test Ray initialization with both parameters as None."""
        ray = Ray(origin=None, dest=None)
        assert ray.origin == Point3D(0, 0, 0)
        assert ray.dest == Vector3D(0, 0, 0)

    def test_repr(self):
        """Test string representation."""
        origin = Point3D(1, 2, 3)
        dest = Vector3D(0, 1, 0)
        ray = Ray(origin, dest)
        repr_str = repr(ray)
        assert "Ray" in repr_str
        assert "origin=" in repr_str
        assert "direction=" in repr_str
        assert "Point3D" in repr_str
        assert "Vector3D" in repr_str

    def test_repr_default(self):
        """Test string representation with default values."""
        ray = Ray()
        repr_str = repr(ray)
        assert "Ray" in repr_str
        assert "origin=" in repr_str
        assert "direction=" in repr_str

    def test_ray_properties_independence(self):
        """Test that ray properties are independent."""
        origin1 = Point3D(1, 0, 0)
        dest1 = Vector3D(0, 1, 0)
        ray1 = Ray(origin1, dest1)
        
        origin2 = Point3D(0, 1, 0)
        dest2 = Vector3D(1, 0, 0)
        ray2 = Ray(origin2, dest2)
        
        # Modifying one ray shouldn't affect the other
        assert ray1.origin != ray2.origin
        assert ray1.dest != ray2.dest

    def test_common_ray_directions(self):
        """Test rays with common directions."""
        origin = Point3D(0, 0, 0)
        
        # Axis-aligned rays
        ray_x = Ray(origin, Vector3D(1, 0, 0))
        ray_y = Ray(origin, Vector3D(0, 1, 0))
        ray_z = Ray(origin, Vector3D(0, 0, 1))
        
        assert ray_x.dest == Vector3D(1, 0, 0)
        assert ray_y.dest == Vector3D(0, 1, 0)
        assert ray_z.dest == Vector3D(0, 0, 1)

    def test_ray_with_negative_direction(self):
        """Test ray with negative direction vector."""
        origin = Point3D(5, 5, 5)
        dest = Vector3D(-1, -1, -1)
        ray = Ray(origin, dest)
        assert ray.origin == origin
        assert ray.dest == dest

    def test_ray_with_zero_direction(self):
        """Test ray with zero direction vector."""
        origin = Point3D(1, 2, 3)
        dest = Vector3D(0, 0, 0)
        ray = Ray(origin, dest)
        assert ray.origin == origin
        assert ray.dest == dest

    def test_ray_with_unit_direction(self):
        """Test ray with unit direction vector."""
        origin = Point3D(0, 0, 0)
        dest = Vector3D(1, 0, 0)  # Unit vector
        ray = Ray(origin, dest)
        assert ray.origin == origin
        assert ray.dest == dest
        assert ray.dest.length == 1.0

    def test_ray_with_non_unit_direction(self):
        """Test ray with non-unit direction vector."""
        origin = Point3D(0, 0, 0)
        dest = Vector3D(3, 4, 0)  # Length = 5
        ray = Ray(origin, dest)
        assert ray.origin == origin
        assert ray.dest == dest
        assert ray.dest.length == 5.0

    def test_ray_from_origin_to_point(self):
        """Test creating ray from origin to target point."""
        origin = Point3D(1, 1, 1)
        target = Point3D(4, 5, 1)
        direction = target - origin  # This creates a Vector3D
        ray = Ray(origin, direction)
        
        assert ray.origin == origin
        assert ray.dest == Vector3D(3, 4, 0)

    def test_ray_parametric_point_calculation(self):
        """Test calculating points along the ray using parametric equation."""
        origin = Point3D(1, 2, 3)
        direction = Vector3D(1, 0, 0)
        ray = Ray(origin, direction)
        
        # Point at parameter t=0 should be the origin
        point_t0 = ray.origin + ray.dest * 0
        assert point_t0 == origin
        
        # Point at parameter t=1 should be origin + direction
        point_t1 = ray.origin + ray.dest * 1
        assert point_t1 == Point3D(2, 2, 3)
        
        # Point at parameter t=2
        point_t2 = ray.origin + ray.dest * 2
        assert point_t2 == Point3D(3, 2, 3)

    def test_ray_with_float_coordinates(self):
        """Test ray with float coordinates."""
        origin = Point3D(1.5, 2.7, 3.14)
        dest = Vector3D(0.5, -0.3, 0.8)
        ray = Ray(origin, dest)
        assert ray.origin == origin
        assert ray.dest == dest

    def test_ray_with_large_coordinates(self):
        """Test ray with large coordinates."""
        origin = Point3D(1e6, 1e6, 1e6)
        dest = Vector3D(1e3, 1e3, 1e3)
        ray = Ray(origin, dest)
        assert ray.origin == origin
        assert ray.dest == dest

    def test_ray_with_small_coordinates(self):
        """Test ray with very small coordinates."""
        origin = Point3D(1e-6, 1e-6, 1e-6)
        dest = Vector3D(1e-3, 1e-3, 1e-3)
        ray = Ray(origin, dest)
        assert ray.origin == origin
        assert ray.dest == dest

    def test_multiple_rays_from_same_origin(self):
        """Test multiple rays from the same origin."""
        origin = Point3D(0, 0, 0)
        directions = [
            Vector3D(1, 0, 0),
            Vector3D(0, 1, 0),
            Vector3D(0, 0, 1),
            Vector3D(1, 1, 0),
            Vector3D(1, 1, 1),
        ]
        
        rays = [Ray(origin, direction) for direction in directions]
        
        # All rays should have the same origin
        for ray in rays:
            assert ray.origin == origin
        
        # Each ray should have its respective direction
        for ray, expected_direction in zip(rays, directions):
            assert ray.dest == expected_direction

    def test_ray_equality_concept(self):
        """Test concept of ray equality (rays are equal if origin and direction are equal)."""
        origin = Point3D(1, 2, 3)
        dest = Vector3D(0, 1, 0)
        
        ray1 = Ray(origin, dest)
        ray2 = Ray(origin, dest)
        
        # While Ray class doesn't implement __eq__, we can test component equality
        assert ray1.origin == ray2.origin
        assert ray1.dest == ray2.dest

    def test_ray_different_origins_same_direction(self):
        """Test rays with different origins but same direction."""
        dest = Vector3D(1, 0, 0)
        
        ray1 = Ray(Point3D(0, 0, 0), dest)
        ray2 = Ray(Point3D(1, 1, 1), dest)
        
        assert ray1.origin != ray2.origin
        assert ray1.dest == ray2.dest

    def test_ray_same_origin_different_directions(self):
        """Test rays with same origin but different directions."""
        origin = Point3D(5, 5, 5)
        
        ray1 = Ray(origin, Vector3D(1, 0, 0))
        ray2 = Ray(origin, Vector3D(0, 1, 0))
        
        assert ray1.origin == ray2.origin
        assert ray1.dest != ray2.dest

    def test_ray_camera_rays_concept(self):
        """Test concept of camera rays (rays from camera through pixels)."""
        camera_position = Point3D(0, -10, 0)
        
        # Rays through different "pixels"
        pixel_directions = [
            Vector3D(-1, 1, -1),  # Top-left
            Vector3D(0, 1, -1),   # Top-center
            Vector3D(1, 1, -1),   # Top-right
            Vector3D(-1, 1, 0),   # Center-left
            Vector3D(0, 1, 0),    # Center
            Vector3D(1, 1, 0),    # Center-right
        ]
        
        camera_rays = [Ray(camera_position, direction) for direction in pixel_directions]
        
        # All camera rays should originate from the camera
        for ray in camera_rays:
            assert ray.origin == camera_position

    def test_ray_reflection_concept(self):
        """Test concept of reflection rays."""
        # Incident ray hitting a surface
        incident_origin = Point3D(0, 0, 5)
        incident_direction = Vector3D(0, 0, -1)
        incident_ray = Ray(incident_origin, incident_direction)
        
        # Reflection point (where ray hits surface)
        hit_point = Point3D(0, 0, 0)
        
        # Reflected ray (simplified - just reverse Z direction)
        reflected_direction = Vector3D(0, 0, 1)
        reflected_ray = Ray(hit_point, reflected_direction)
        
        assert incident_ray.origin == incident_origin
        assert incident_ray.dest == incident_direction
        assert reflected_ray.origin == hit_point
        assert reflected_ray.dest == reflected_direction

    def test_ray_with_normalized_direction(self):
        """Test ray with normalized direction vector."""
        origin = Point3D(0, 0, 0)
        direction = Vector3D(3, 4, 0)  # Length = 5
        normalized_direction = direction.normalize()  # Should be (0.6, 0.8, 0)
        
        ray = Ray(origin, normalized_direction)
        assert ray.origin == origin
        assert abs(ray.dest.length - 1.0) < 0.001  # Should be unit length

    def test_edge_case_ray_attributes_modification(self):
        """Test that ray attributes can be modified after creation."""
        ray = Ray()
        
        # Modify origin
        new_origin = Point3D(10, 20, 30)
        ray.origin = new_origin
        assert ray.origin == new_origin
        
        # Modify destination
        new_dest = Vector3D(1, 1, 1)
        ray.dest = new_dest
        assert ray.dest == new_dest

    def test_ray_with_extreme_values(self):
        """Test ray with extreme coordinate values."""
        # Very large values
        large_origin = Point3D(1e10, 1e10, 1e10)
        large_dest = Vector3D(1e5, 1e5, 1e5)
        large_ray = Ray(large_origin, large_dest)
        assert large_ray.origin == large_origin
        assert large_ray.dest == large_dest
        
        # Very small values
        small_origin = Point3D(1e-10, 1e-10, 1e-10)
        small_dest = Vector3D(1e-5, 1e-5, 1e-5)
        small_ray = Ray(small_origin, small_dest)
        assert small_ray.origin == small_origin
        assert small_ray.dest == small_dest