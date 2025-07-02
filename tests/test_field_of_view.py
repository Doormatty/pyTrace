import pytest
import math
from Scene import Scene
from Primitives import Sphere, Plane
from Material import Material
from RGB import RGB
from Point import Point3D
from Vector import Vector3D
from Ray import Ray
from main import RayTracer


class TestFieldOfView:
    """Comprehensive tests for field_of_view functionality."""

    def test_field_of_view_parameter_storage(self):
        """Test that field_of_view parameter is correctly stored in Scene."""
        # Test default value
        scene = Scene()
        assert scene.field_of_view == 90.0

        # Test custom values
        scene_narrow = Scene(field_of_view=30.0)
        assert scene_narrow.field_of_view == 30.0

        scene_wide = Scene(field_of_view=120.0)
        assert scene_wide.field_of_view == 120.0

    def test_field_of_view_viewport_calculations(self):
        """Test that field_of_view correctly affects viewport calculations."""
        raytracer = RayTracer(screen_width=600, screen_height=600)

        # Test different field_of_view values
        test_cases = [
            (30.0, "narrow"),   # Narrow field of view
            (60.0, "normal"),   # Normal field of view
            (90.0, "default"),  # Default field of view
            (120.0, "wide"),    # Wide field of view
        ]

        for fov, description in test_cases:
            scene = Scene(
                camera_position=Point3D(0, 0, 100),
                camera_direction=Vector3D(0, 0, -1),
                field_of_view=fov
            )

            viewport_z, viewport_height, viewport_width, pixel_size_x, pixel_size_y = raytracer._calculate_scene_parameters(scene)

            # Verify the mathematical relationship
            expected_viewport_height = 2 * viewport_z * math.tan(math.radians(fov / 2))
            assert abs(viewport_height - expected_viewport_height) < 1e-10, f"Viewport height calculation incorrect for {description} FOV ({fov}°)"

            # Verify aspect ratio is maintained
            expected_viewport_width = viewport_height * raytracer.aspect_ratio
            assert abs(viewport_width - expected_viewport_width) < 1e-10, f"Viewport width calculation incorrect for {description} FOV ({fov}°)"

            # Verify pixel sizes
            expected_pixel_size_x = viewport_width / raytracer.screen_width
            expected_pixel_size_y = viewport_height / raytracer.screen_height
            assert abs(pixel_size_x - expected_pixel_size_x) < 1e-10, f"Pixel size X calculation incorrect for {description} FOV ({fov}°)"
            assert abs(pixel_size_y - expected_pixel_size_y) < 1e-10, f"Pixel size Y calculation incorrect for {description} FOV ({fov}°)"

    def test_field_of_view_ordering(self):
        """Test that different field_of_view values produce expected relative viewport sizes."""
        raytracer = RayTracer(screen_width=600, screen_height=600)

        # Create scenes with different FOV values
        scene_narrow = Scene(camera_position=Point3D(0, 0, 100), field_of_view=30.0)
        scene_normal = Scene(camera_position=Point3D(0, 0, 100), field_of_view=60.0)
        scene_wide = Scene(camera_position=Point3D(0, 0, 100), field_of_view=120.0)

        # Calculate viewport parameters
        _, height_narrow, width_narrow, _, _ = raytracer._calculate_scene_parameters(scene_narrow)
        _, height_normal, width_normal, _, _ = raytracer._calculate_scene_parameters(scene_normal)
        _, height_wide, width_wide, _, _ = raytracer._calculate_scene_parameters(scene_wide)

        # Verify ordering: narrow < normal < wide
        assert height_narrow < height_normal < height_wide, "Viewport heights should increase with field_of_view"
        assert width_narrow < width_normal < width_wide, "Viewport widths should increase with field_of_view"

    def test_field_of_view_ray_generation(self):
        """Test that field_of_view affects ray generation correctly."""
        raytracer = RayTracer(screen_width=100, screen_height=100)

        # Test with narrow and wide field of view
        scene_narrow = Scene(
            camera_position=Point3D(0, 0, 100),
            camera_direction=Vector3D(0, 0, -1),
            field_of_view=30.0
        )
        scene_wide = Scene(
            camera_position=Point3D(0, 0, 100),
            camera_direction=Vector3D(0, 0, -1),
            field_of_view=120.0
        )

        # Calculate scene parameters
        viewport_z_narrow, _, _, pixel_size_x_narrow, pixel_size_y_narrow = raytracer._calculate_scene_parameters(scene_narrow)
        viewport_z_wide, _, _, pixel_size_x_wide, pixel_size_y_wide = raytracer._calculate_scene_parameters(scene_wide)

        # Create rays for corner pixels
        ray_narrow = Ray(scene_narrow.camera_position, scene_narrow.camera_direction)
        ray_wide = Ray(scene_wide.camera_position, scene_wide.camera_direction)

        # Test corner pixel (0, 0) - top-left
        raytracer._setup_ray_for_pixel(ray_narrow, 0, 0, 100, 100, pixel_size_x_narrow, pixel_size_y_narrow, viewport_z_narrow, scene_narrow)
        raytracer._setup_ray_for_pixel(ray_wide, 0, 0, 100, 100, pixel_size_x_wide, pixel_size_y_wide, viewport_z_wide, scene_wide)

        # The ray directions should be different
        assert ray_narrow.dest != ray_wide.dest, "Ray directions should differ for different field_of_view values"

        # For the same pixel position, wider FOV should have rays pointing further from center
        # Calculate angles from the forward direction
        forward = Vector3D(0, 0, -1)
        angle_narrow = math.acos(max(-1, min(1, ray_narrow.dest * forward)))
        angle_wide = math.acos(max(-1, min(1, ray_wide.dest * forward)))

        # Wide FOV should have larger angles for corner pixels
        assert angle_wide > angle_narrow, "Wide field_of_view should produce larger angles for corner pixels"

    def test_field_of_view_edge_cases(self):
        """Test field_of_view with edge case values."""
        raytracer = RayTracer(screen_width=600, screen_height=600)

        # Test very small field of view
        scene_tiny = Scene(camera_position=Point3D(0, 0, 100), field_of_view=1.0)
        viewport_z, viewport_height, viewport_width, pixel_size_x, pixel_size_y = raytracer._calculate_scene_parameters(scene_tiny)

        # Should produce very small viewport
        assert viewport_height > 0, "Viewport height should be positive for tiny FOV"
        assert viewport_width > 0, "Viewport width should be positive for tiny FOV"
        assert viewport_height < 10, "Viewport height should be very small for tiny FOV"

        # Test very large field of view
        scene_huge = Scene(camera_position=Point3D(0, 0, 100), field_of_view=179.0)
        viewport_z, viewport_height, viewport_width, pixel_size_x, pixel_size_y = raytracer._calculate_scene_parameters(scene_huge)

        # Should produce very large viewport (179° FOV produces ~229 viewport height)
        assert viewport_height > 200, "Viewport height should be very large for huge FOV"
        assert viewport_width > 200, "Viewport width should be very large for huge FOV"

    def test_field_of_view_object_visibility(self):
        """Test that field_of_view affects ray directions correctly."""
        raytracer = RayTracer(screen_width=100, screen_height=100, recursion_limit=1)

        # Create scenes with different FOV values
        scene_narrow = Scene(
            camera_position=Point3D(0, 0, 100),
            camera_direction=Vector3D(0, 0, -1),
            field_of_view=30.0,
            background_color=RGB(0, 0, 0)
        )

        scene_wide = Scene(
            camera_position=Point3D(0, 0, 100),
            camera_direction=Vector3D(0, 0, -1),
            field_of_view=120.0,
            background_color=RGB(0, 0, 0)
        )

        # Add a center sphere (should be visible in both FOV)
        center_sphere = Sphere(
            center=Point3D(0, 0, 0),
            radius=10,
            material=Material(RGB(1, 0, 0), 0, 0, 1.0)  # Red, emissive
        )

        scene_narrow.add_object(center_sphere)
        scene_wide.add_object(center_sphere)

        # Calculate scene parameters
        viewport_z_narrow, _, _, pixel_size_x_narrow, pixel_size_y_narrow = raytracer._calculate_scene_parameters(scene_narrow)
        viewport_z_wide, _, _, pixel_size_x_wide, pixel_size_y_wide = raytracer._calculate_scene_parameters(scene_wide)

        # Test center pixel - should see center sphere in both cases
        ray_center_narrow = Ray(scene_narrow.camera_position, scene_narrow.camera_direction)
        raytracer._setup_ray_for_pixel(ray_center_narrow, 50, 50, 100, 100, pixel_size_x_narrow, pixel_size_y_narrow, viewport_z_narrow, scene_narrow)
        color_center_narrow = raytracer.raytrace(ray_center_narrow, scene_narrow)

        ray_center_wide = Ray(scene_wide.camera_position, scene_wide.camera_direction)
        raytracer._setup_ray_for_pixel(ray_center_wide, 50, 50, 100, 100, pixel_size_x_wide, pixel_size_y_wide, viewport_z_wide, scene_wide)
        color_center_wide = raytracer.raytrace(ray_center_wide, scene_wide)

        # Both should see the red center sphere
        assert color_center_narrow.r > 0.5, "Narrow FOV should see center red sphere"
        assert color_center_wide.r > 0.5, "Wide FOV should see center red sphere"

        # Test that ray directions are different for edge pixels
        ray_edge_narrow = Ray(scene_narrow.camera_position, scene_narrow.camera_direction)
        raytracer._setup_ray_for_pixel(ray_edge_narrow, 90, 50, 100, 100, pixel_size_x_narrow, pixel_size_y_narrow, viewport_z_narrow, scene_narrow)

        ray_edge_wide = Ray(scene_wide.camera_position, scene_wide.camera_direction)
        raytracer._setup_ray_for_pixel(ray_edge_wide, 90, 50, 100, 100, pixel_size_x_wide, pixel_size_y_wide, viewport_z_wide, scene_wide)

        # The ray directions should be significantly different
        ray_diff = abs(ray_edge_narrow.dest.x - ray_edge_wide.dest.x) + abs(ray_edge_narrow.dest.y - ray_edge_wide.dest.y) + abs(ray_edge_narrow.dest.z - ray_edge_wide.dest.z)
        assert ray_diff > 0.5, f"Ray directions should be significantly different for different FOV values (difference: {ray_diff:.3f})"

        # Verify that wide FOV produces larger angles from center
        import math
        forward = Vector3D(0, 0, -1)
        angle_narrow = math.acos(max(-1, min(1, ray_edge_narrow.dest * forward)))
        angle_wide = math.acos(max(-1, min(1, ray_edge_wide.dest * forward)))

        assert angle_wide > angle_narrow, "Wide FOV should produce larger angles for edge pixels"

    def test_field_of_view_json_serialization(self):
        """Test that field_of_view is correctly serialized and deserialized."""
        original_scene = Scene(
            name="FOV Test Scene",
            camera_position=Point3D(10, 20, 30),
            camera_direction=Vector3D(1, 0, 0),
            field_of_view=75.0,
            background_color=RGB(0.1, 0.2, 0.3)
        )

        # Serialize to JSON
        json_data = original_scene.to_json()
        assert json_data["field_of_view"] == 75.0, "field_of_view should be correctly serialized"

        # Deserialize from JSON
        restored_scene = Scene.from_json(json_data)
        assert restored_scene.field_of_view == 75.0, "field_of_view should be correctly deserialized"
        assert restored_scene.field_of_view == original_scene.field_of_view, "Restored field_of_view should match original"

    def test_field_of_view_mathematical_precision(self):
        """Test mathematical precision of field_of_view calculations."""
        raytracer = RayTracer(screen_width=600, screen_height=600)

        # Test specific mathematical relationships
        test_cases = [
            (45.0, 1.0),      # tan(45°/2) = tan(22.5°) ≈ 0.414
            (60.0, math.sqrt(3)/3),  # tan(60°/2) = tan(30°) = 1/√3
            (90.0, 1.0),      # tan(90°/2) = tan(45°) = 1
        ]

        for fov, expected_tan_half in test_cases:
            scene = Scene(
                camera_position=Point3D(0, 0, 100),
                field_of_view=fov
            )

            viewport_z, viewport_height, _, _, _ = raytracer._calculate_scene_parameters(scene)

            # Calculate the actual tan(fov/2) from the viewport dimensions
            actual_tan_half = viewport_height / (2 * viewport_z)
            expected_tan_half_calculated = math.tan(math.radians(fov / 2))

            assert abs(actual_tan_half - expected_tan_half_calculated) < 1e-10, f"Mathematical precision error for FOV {fov}°"

    def test_field_of_view_consistency_across_camera_positions(self):
        """Test that field_of_view works consistently regardless of camera position."""
        raytracer = RayTracer(screen_width=100, screen_height=100)

        camera_positions = [
            Point3D(0, 0, 50),
            Point3D(0, 0, 100),
            Point3D(0, 0, 200),
        ]

        fov = 60.0

        for camera_pos in camera_positions:
            scene = Scene(
                camera_position=camera_pos,
                camera_direction=Vector3D(0, 0, -1),
                field_of_view=fov
            )

            viewport_z, viewport_height, _, _, _ = raytracer._calculate_scene_parameters(scene)

            # The relationship between viewport_height and viewport_z should be consistent
            # regardless of camera position
            tan_half_fov = viewport_height / (2 * viewport_z)
            expected_tan_half_fov = math.tan(math.radians(fov / 2))

            assert abs(tan_half_fov - expected_tan_half_fov) < 1e-10, f"FOV calculation inconsistent for camera position {camera_pos}"
