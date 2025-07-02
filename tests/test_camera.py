import unittest
import math
from Point import Point3D
from Vector import Vector3D
from Camera import Camera, CameraConfig


class TestCamera(unittest.TestCase):
    """Comprehensive tests for the Camera class."""

    def setUp(self):
        """Set up test fixtures."""
        self.default_position = Point3D(0, 0, 0)
        self.default_direction = Vector3D(0, 0, -1)
        self.default_fov = 90.0

    def test_camera_initialization(self):
        """Test camera initialization with various parameters."""
        camera = Camera(self.default_position, self.default_direction, self.default_fov)

        self.assertEqual(camera.position, self.default_position)
        self.assertEqual(camera.direction, self.default_direction.normalize())
        self.assertEqual(camera.field_of_view, self.default_fov)

        # Coordinate system should be calculated automatically
        self.assertIsNotNone(camera.forward)
        self.assertIsNotNone(camera.right)
        self.assertIsNotNone(camera.up)

    def test_coordinate_system_orthogonality(self):
        """Test that the coordinate system is orthonormal."""
        test_directions = [
            Vector3D(0, 0, -1),      # Standard forward
            Vector3D(1, 0, -1),      # Tilted right
            Vector3D(-1, 0, -1),     # Tilted left
            Vector3D(0, 1, -1),      # Tilted up
            Vector3D(0, -1, -1),     # Tilted down
            Vector3D(1, 1, -1),      # Tilted right and up
            Vector3D(-1, -1, -1),    # Tilted left and down
        ]

        for direction in test_directions:
            with self.subTest(direction=direction):
                camera = Camera(self.default_position, direction, self.default_fov)

                forward = camera.forward
                right = camera.right
                up = camera.up

                # Check orthogonality (dot products should be ~0)
                tolerance = CameraConfig.NUMERICAL_TOLERANCE
                self.assertAlmostEqual(forward % right, 0, delta=tolerance,
                                     msg="Forward and right vectors not orthogonal")
                self.assertAlmostEqual(forward % up, 0, delta=tolerance,
                                     msg="Forward and up vectors not orthogonal")
                self.assertAlmostEqual(right % up, 0, delta=tolerance,
                                     msg="Right and up vectors not orthogonal")

                # Check normalization (lengths should be ~1)
                self.assertAlmostEqual(forward.length, 1.0, delta=tolerance,
                                     msg="Forward vector not normalized")
                self.assertAlmostEqual(right.length, 1.0, delta=tolerance,
                                     msg="Right vector not normalized")
                self.assertAlmostEqual(up.length, 1.0, delta=tolerance,
                                     msg="Up vector not normalized")

    def test_camera_roll_consistency(self):
        """Test that camera maintains level horizons regardless of direction."""
        # Test various horizontal directions - all should have level horizons
        directions = [
            Vector3D(1, 0, -1).normalize(),   # Northeast down
            Vector3D(-1, 0, -1).normalize(),  # Northwest down
            Vector3D(0, 1, -1).normalize(),   # North down
            Vector3D(0, -1, -1).normalize(),  # South down
            Vector3D(1, 1, -1).normalize(),   # Northeast down
            Vector3D(-1, -1, -1).normalize(), # Southwest down
        ]

        world_up = Vector3D(0, 0, 1)

        for direction in directions:
            with self.subTest(direction=direction):
                camera = Camera(self.default_position, direction, self.default_fov)

                # The right vector should be horizontal (no Z component)
                self.assertAlmostEqual(camera.right.z, 0.0, delta=CameraConfig.NUMERICAL_TOLERANCE,
                                     msg=f"Right vector should be horizontal for direction {direction}")

                # The up vector should have a positive Z component (pointing generally upward)
                self.assertGreater(camera.up.z, 0.0,
                                 msg=f"Up vector should point generally upward for direction {direction}")

                # The coordinate system should be orthonormal
                self.assertAlmostEqual(camera.forward % camera.right, 0, delta=CameraConfig.NUMERICAL_TOLERANCE)
                self.assertAlmostEqual(camera.forward % camera.up, 0, delta=CameraConfig.NUMERICAL_TOLERANCE)
                self.assertAlmostEqual(camera.right % camera.up, 0, delta=CameraConfig.NUMERICAL_TOLERANCE)

    def test_edge_case_directions(self):
        """Test camera with edge case directions (nearly parallel to reference vectors)."""
        edge_cases = [
            Vector3D(1, 0, 0),       # Looking along positive X
            Vector3D(-1, 0, 0),      # Looking along negative X
            Vector3D(0, 1, 0),       # Looking along positive Y
            Vector3D(0, -1, 0),      # Looking along negative Y
            Vector3D(0, 0, 1),       # Looking along positive Z
            Vector3D(0, 0, -1),      # Looking along negative Z
            Vector3D(0.99, 0, 0.1),  # Nearly parallel to X
            Vector3D(0.1, 0, 0.99),  # Nearly parallel to Z
        ]

        for direction in edge_cases:
            with self.subTest(direction=direction):
                # Should not raise an exception
                camera = Camera(self.default_position, direction, self.default_fov)

                # Coordinate system should still be valid
                self.assertIsNotNone(camera.forward)
                self.assertIsNotNone(camera.right)
                self.assertIsNotNone(camera.up)

                # Should pass orthogonality tests
                tolerance = CameraConfig.NUMERICAL_TOLERANCE
                self.assertAlmostEqual(camera.forward % camera.right, 0, delta=tolerance)
                self.assertAlmostEqual(camera.forward % camera.up, 0, delta=tolerance)
                self.assertAlmostEqual(camera.right % camera.up, 0, delta=tolerance)

    def test_set_direction(self):
        """Test changing camera direction."""
        camera = Camera(self.default_position, self.default_direction, self.default_fov)

        original_forward = camera.forward
        original_right = camera.right
        original_up = camera.up

        # Change direction to something significantly different
        new_direction = Vector3D(1, 1, -1)
        camera.set_direction(new_direction)

        # Direction should be updated and normalized
        self.assertEqual(camera.direction, new_direction.normalize())

        # Forward vector should definitely change
        self.assertNotEqual(camera.forward, original_forward)

        # At least one of right or up should change (but not necessarily both)
        coordinate_system_changed = (
            camera.right != original_right or 
            camera.up != original_up
        )
        self.assertTrue(coordinate_system_changed, 
                       "Coordinate system should change when direction changes significantly")

        # New coordinate system should still be orthonormal
        tolerance = CameraConfig.NUMERICAL_TOLERANCE
        self.assertAlmostEqual(camera.forward % camera.right, 0, delta=tolerance)
        self.assertAlmostEqual(camera.forward % camera.up, 0, delta=tolerance)
        self.assertAlmostEqual(camera.right % camera.up, 0, delta=tolerance)

    def test_set_position(self):
        """Test changing camera position."""
        camera = Camera(self.default_position, self.default_direction, self.default_fov)

        new_position = Point3D(10, 20, 30)
        camera.set_position(new_position)

        self.assertEqual(camera.position, new_position)

        # Coordinate system should not change when position changes
        self.assertEqual(camera.direction, self.default_direction.normalize())

    def test_viewport_parameters(self):
        """Test viewport parameter calculation."""
        camera = Camera(self.default_position, self.default_direction, 90.0)

        screen_width, screen_height = 800, 600
        viewport_z, viewport_height, viewport_width, pixel_size_x, pixel_size_y = \
            camera.calculate_viewport_parameters(screen_width, screen_height)

        # For 90-degree FOV, viewport_z should be 1.0
        self.assertAlmostEqual(viewport_z, 1.0, places=5)

        # Viewport height should be 2.0
        self.assertAlmostEqual(viewport_height, 2.0, places=5)

        # Viewport width should maintain aspect ratio
        expected_width = viewport_height * (screen_width / screen_height)
        self.assertAlmostEqual(viewport_width, expected_width, places=5)

        # Pixel sizes should be correct
        self.assertAlmostEqual(pixel_size_x, viewport_width / screen_width, places=5)
        self.assertAlmostEqual(pixel_size_y, viewport_height / screen_height, places=5)

    def test_ray_generation(self):
        """Test ray generation for pixels."""
        camera = Camera(Point3D(0, 0, 10), Vector3D(0, 0, -1), 90.0)

        screen_width, screen_height = 100, 100

        # Test center pixel
        center_x, center_y = 50, 50
        ray = camera.generate_ray_for_pixel(center_x, center_y, screen_width, screen_height)

        # Ray should start at camera position
        self.assertEqual(ray.origin, camera.position)

        # Ray direction should be approximately forward for center pixel
        # (with small viewport offset due to pixel positioning)
        self.assertAlmostEqual(ray.dest.z, -1.0, delta=0.1)

        # Test corner pixel
        corner_ray = camera.generate_ray_for_pixel(0, 0, screen_width, screen_height)
        self.assertEqual(corner_ray.origin, camera.position)

        # Corner ray should have different direction than center ray
        self.assertNotEqual(corner_ray.dest, ray.dest)

    def test_ray_generation_with_offsets(self):
        """Test ray generation with subpixel offsets."""
        camera = Camera(self.default_position, self.default_direction, 90.0)

        screen_width, screen_height = 100, 100
        x, y = 50, 50

        # Generate rays with different offsets
        ray_center = camera.generate_ray_for_pixel(x, y, screen_width, screen_height, 0.0, 0.0)
        ray_offset = camera.generate_ray_for_pixel(x, y, screen_width, screen_height, 0.5, 0.5)

        # Rays should have different directions
        self.assertNotEqual(ray_center.dest, ray_offset.dest)

        # But both should start at camera position
        self.assertEqual(ray_center.origin, camera.position)
        self.assertEqual(ray_offset.origin, camera.position)

    def test_json_serialization(self):
        """Test JSON serialization and deserialization."""
        original_camera = Camera(
            Point3D(1, 2, 3),
            Vector3D(0.5, 0.5, -0.7),
            60.0
        )

        # Serialize to JSON
        json_data = original_camera.to_json()

        # Check JSON structure
        self.assertEqual(json_data["type"], "camera")
        self.assertIn("position", json_data)
        self.assertIn("direction", json_data)
        self.assertIn("field_of_view", json_data)

        # Deserialize from JSON
        restored_camera = Camera.from_json(json_data)

        # Check that restored camera matches original
        self.assertEqual(restored_camera.position, original_camera.position)
        self.assertEqual(restored_camera.direction, original_camera.direction)
        self.assertEqual(restored_camera.field_of_view, original_camera.field_of_view)

        # Coordinate systems should be equivalent
        tolerance = CameraConfig.NUMERICAL_TOLERANCE
        self.assertAlmostEqual(
            (restored_camera.forward - original_camera.forward).length, 0, delta=tolerance
        )
        self.assertAlmostEqual(
            (restored_camera.right - original_camera.right).length, 0, delta=tolerance
        )
        self.assertAlmostEqual(
            (restored_camera.up - original_camera.up).length, 0, delta=tolerance
        )

    def test_coordinate_system_caching(self):
        """Test that coordinate system is properly cached and invalidated."""
        camera = Camera(self.default_position, self.default_direction, self.default_fov)

        # Access coordinate system vectors
        forward1 = camera.forward
        right1 = camera.right
        up1 = camera.up

        # Access again - should return same objects (cached)
        forward2 = camera.forward
        right2 = camera.right
        up2 = camera.up

        self.assertIs(forward1, forward2)
        self.assertIs(right1, right2)
        self.assertIs(up1, up2)

        # Change direction - cache should be invalidated
        camera.set_direction(Vector3D(1, 0, -1))

        forward3 = camera.forward
        right3 = camera.right
        up3 = camera.up

        # Should be different objects now
        self.assertIsNot(forward1, forward3)
        self.assertIsNot(right1, right3)
        self.assertIsNot(up1, up3)

    def test_validation_errors(self):
        """Test that validation catches coordinate system errors."""
        # This test verifies that the validation system works
        # We can't easily create invalid coordinate systems through the public API
        # since the Camera class ensures they're always valid, but we can test
        # the validation logic indirectly

        camera = Camera(self.default_position, self.default_direction, self.default_fov)

        # The coordinate system should be valid
        # If validation fails, it would raise a ValueError during initialization
        self.assertIsNotNone(camera.forward)
        self.assertIsNotNone(camera.right)
        self.assertIsNotNone(camera.up)

    def test_repr(self):
        """Test string representation."""
        camera = Camera(
            Point3D(1, 2, 3),
            Vector3D(0, 0, -1),
            45.0
        )

        repr_str = repr(camera)
        self.assertIn("Camera", repr_str)
        self.assertIn("position", repr_str)
        self.assertIn("direction", repr_str)
        self.assertIn("fov", repr_str)


class TestCameraConfig(unittest.TestCase):
    """Test camera configuration constants."""

    def test_config_constants(self):
        """Test that configuration constants are reasonable."""
        self.assertGreater(CameraConfig.PARALLEL_THRESHOLD, 0.9)
        self.assertLess(CameraConfig.PARALLEL_THRESHOLD, 1.0)

        self.assertGreater(CameraConfig.NUMERICAL_TOLERANCE, 0)
        self.assertLess(CameraConfig.NUMERICAL_TOLERANCE, 0.01)

        self.assertIsInstance(CameraConfig.DEFAULT_WORLD_UP, Vector3D)
        self.assertIsInstance(CameraConfig.DEFAULT_WORLD_RIGHT, Vector3D)
        self.assertIsInstance(CameraConfig.FALLBACK_WORLD_RIGHT, Vector3D)


if __name__ == '__main__':
    unittest.main()
