import unittest
import math
from Point import Point3D
from Vector import Vector3D
from Camera import Camera, CameraConfig
from Scene import Scene
from main import RayTracer
from Primitives import Sphere
from Material import Material
from RGB import RGB


class TestCameraIntegration(unittest.TestCase):
    """Integration tests for the robust camera system."""

    def setUp(self):
        """Set up test fixtures."""
        self.tracer = RayTracer(screen_width=100, screen_height=100, recursion_limit=5)

    def test_scene_camera_integration(self):
        """Test that Scene properly integrates with Camera class."""
        # Test new Camera object constructor
        camera = Camera(Point3D(0, 0, 10), Vector3D(0, 0, -1), 60.0)
        scene = Scene("Test Scene", camera=camera)

        self.assertIs(scene.camera, camera)
        self.assertEqual(scene.camera_position, Point3D(0, 0, 10))
        self.assertEqual(scene.camera_direction, Vector3D(0, 0, -1))
        self.assertEqual(scene.field_of_view, 60.0)

    def test_scene_legacy_parameters(self):
        """Test that Scene still works with legacy camera parameters."""
        scene = Scene(
            "Legacy Scene",
            camera_position=Point3D(5, 5, 5),
            camera_direction=Vector3D(1, 0, -1),
            field_of_view=45.0
        )

        self.assertEqual(scene.camera_position, Point3D(5, 5, 5))
        self.assertEqual(scene.camera_direction, Vector3D(1, 0, -1).normalize())
        self.assertEqual(scene.field_of_view, 45.0)
        self.assertIsInstance(scene.camera, Camera)

    def test_scene_property_setters(self):
        """Test that Scene property setters work correctly."""
        scene = Scene("Test Scene")

        # Test position setter
        new_position = Point3D(10, 20, 30)
        scene.camera_position = new_position
        self.assertEqual(scene.camera.position, new_position)
        self.assertEqual(scene.camera_position, new_position)

        # Test direction setter
        new_direction = Vector3D(1, 1, -1)
        scene.camera_direction = new_direction
        self.assertEqual(scene.camera.direction, new_direction.normalize())
        self.assertEqual(scene.camera_direction, new_direction.normalize())

        # Test field of view setter
        scene.field_of_view = 120.0
        self.assertEqual(scene.camera.field_of_view, 120.0)
        self.assertEqual(scene.field_of_view, 120.0)

    def test_raytracer_camera_integration(self):
        """Test that RayTracer properly uses the Camera class."""
        scene = Scene(
            "Test Scene",
            camera_position=Point3D(0, 0, 10),
            camera_direction=Vector3D(0, 0, -1),
            field_of_view=90.0
        )

        # Add a simple object to trace
        sphere = Sphere(Point3D(0, 0, 0), 5, Material(RGB(1.0, 0, 0), 1.0, 0, 0.0))
        scene.add_object(sphere)

        # Test that scene parameters are calculated correctly
        viewport_z, viewport_height, viewport_width, pixel_size_x, pixel_size_y = \
            self.tracer._calculate_scene_parameters(scene)

        # For 90-degree FOV, viewport_z should be 1.0
        self.assertAlmostEqual(viewport_z, 1.0, places=5)

        # Test ray generation through the tracer
        from Ray import Ray
        ray = Ray(Point3D(0, 0, 0), Vector3D(0, 0, -1))

        # This should not raise an exception
        self.tracer._setup_ray_for_pixel(ray, 50, 50, 100, 100, pixel_size_x, pixel_size_y, viewport_z, scene)

        # Ray should be properly set up
        self.assertEqual(ray.origin, scene.camera_position)
        self.assertIsNotNone(ray.dest)

    def test_camera_roll_prevention_integration(self):
        """Test that camera maintains level horizons in the integrated system."""
        test_directions = [
            Vector3D(1, 0, -1),      # Tilted right
            Vector3D(-1, 0, -1),     # Tilted left
            Vector3D(0, 1, -1),      # Tilted up
            Vector3D(0, -1, -1),     # Tilted down
        ]

        scenes = []
        for i, direction in enumerate(test_directions):
            scene = Scene(
                f"Test Scene {i}",
                camera_position=Point3D(0, 0, 10),
                camera_direction=direction,
                field_of_view=60.0
            )
            scenes.append(scene)

        # Test that all cameras maintain level horizons
        for i, scene in enumerate(scenes):
            with self.subTest(direction=test_directions[i]):
                camera = scene.camera

                # The right vector should be horizontal (no Z component)
                self.assertAlmostEqual(camera.right.z, 0.0, delta=CameraConfig.NUMERICAL_TOLERANCE,
                                     msg=f"Right vector should be horizontal for direction {test_directions[i]}")

                # The up vector should have a positive Z component (pointing generally upward)
                self.assertGreater(camera.up.z, 0.0,
                                 msg=f"Up vector should point generally upward for direction {test_directions[i]}")

                # The coordinate system should be orthonormal
                tolerance = CameraConfig.NUMERICAL_TOLERANCE
                self.assertAlmostEqual(camera.forward % camera.right, 0, delta=tolerance)
                self.assertAlmostEqual(camera.forward % camera.up, 0, delta=tolerance)
                self.assertAlmostEqual(camera.right % camera.up, 0, delta=tolerance)

    def test_extreme_camera_directions(self):
        """Test camera system with extreme directions."""
        extreme_directions = [
            Vector3D(1, 0, 0),       # Looking along positive X
            Vector3D(-1, 0, 0),      # Looking along negative X
            Vector3D(0, 1, 0),       # Looking along positive Y
            Vector3D(0, -1, 0),      # Looking along negative Y
            Vector3D(0, 0, 1),       # Looking along positive Z
            Vector3D(0, 0, -1),      # Looking along negative Z
            Vector3D(0.999, 0, 0.001),  # Nearly parallel to X
            Vector3D(0.001, 0, 0.999),  # Nearly parallel to Z
        ]

        for direction in extreme_directions:
            with self.subTest(direction=direction):
                # Should not raise an exception
                scene = Scene(
                    "Extreme Test",
                    camera_position=Point3D(0, 0, 0),
                    camera_direction=direction,
                    field_of_view=90.0
                )

                # Camera should be valid
                self.assertIsNotNone(scene.camera.forward)
                self.assertIsNotNone(scene.camera.right)
                self.assertIsNotNone(scene.camera.up)

                # Coordinate system should be orthonormal
                tolerance = CameraConfig.NUMERICAL_TOLERANCE
                self.assertAlmostEqual(scene.camera.forward % scene.camera.right, 0, delta=tolerance)
                self.assertAlmostEqual(scene.camera.forward % scene.camera.up, 0, delta=tolerance)
                self.assertAlmostEqual(scene.camera.right % scene.camera.up, 0, delta=tolerance)

                # Ray generation should work
                ray = scene.camera.generate_ray_for_pixel(50, 50, 100, 100)
                self.assertIsNotNone(ray.origin)
                self.assertIsNotNone(ray.dest)

    def test_json_serialization_integration(self):
        """Test that JSON serialization works with the integrated camera system."""
        # Create a scene with camera
        original_scene = Scene(
            "JSON Test Scene",
            camera_position=Point3D(1, 2, 3),
            camera_direction=Vector3D(0.5, 0.5, -0.7),
            field_of_view=75.0,
            ambient_intensity=0.3
        )

        # Add an object
        sphere = Sphere(Point3D(0, 0, 0), 5, Material(RGB(1.0, 0, 0), 1.0, 0, 0.0))
        original_scene.add_object(sphere)

        # Serialize to JSON
        json_data = original_scene.to_json()

        # Deserialize from JSON
        restored_scene = Scene.from_json(json_data)

        # Check that camera is properly restored
        self.assertEqual(restored_scene.camera_position, original_scene.camera_position)
        self.assertEqual(restored_scene.camera_direction, original_scene.camera_direction)
        self.assertEqual(restored_scene.field_of_view, original_scene.field_of_view)

        # Check that coordinate systems are equivalent
        tolerance = CameraConfig.NUMERICAL_TOLERANCE
        original_forward = original_scene.camera.forward
        restored_forward = restored_scene.camera.forward
        self.assertAlmostEqual((original_forward - restored_forward).length, 0, delta=tolerance)

    def test_camera_modification_robustness(self):
        """Test that camera modifications don't break the system."""
        scene = Scene("Modification Test")

        # Start with default camera
        original_direction = scene.camera_direction

        # Modify camera multiple times
        modifications = [
            Vector3D(1, 0, -1),
            Vector3D(-1, 1, -1),
            Vector3D(0, -1, -1),
            Vector3D(1, 1, 1),
            Vector3D(-1, -1, -1),
        ]

        for direction in modifications:
            scene.camera_direction = direction

            # Camera should remain valid after each modification
            self.assertIsNotNone(scene.camera.forward)
            self.assertIsNotNone(scene.camera.right)
            self.assertIsNotNone(scene.camera.up)

            # Coordinate system should remain orthonormal
            tolerance = CameraConfig.NUMERICAL_TOLERANCE
            self.assertAlmostEqual(scene.camera.forward % scene.camera.right, 0, delta=tolerance)
            self.assertAlmostEqual(scene.camera.forward % scene.camera.up, 0, delta=tolerance)
            self.assertAlmostEqual(scene.camera.right % scene.camera.up, 0, delta=tolerance)

            # Ray generation should still work
            ray = scene.camera.generate_ray_for_pixel(25, 75, 100, 100)
            self.assertIsNotNone(ray.origin)
            self.assertIsNotNone(ray.dest)

    def test_field_of_view_edge_cases(self):
        """Test camera system with extreme field of view values."""
        fov_values = [1.0, 15.0, 45.0, 90.0, 120.0, 150.0, 179.0]

        for fov in fov_values:
            with self.subTest(fov=fov):
                scene = Scene(
                    f"FOV Test {fov}",
                    camera_position=Point3D(0, 0, 10),
                    camera_direction=Vector3D(0, 0, -1),
                    field_of_view=fov
                )

                # Camera should be valid
                self.assertEqual(scene.field_of_view, fov)

                # Viewport parameters should be calculated correctly
                viewport_z, viewport_height, viewport_width, pixel_size_x, pixel_size_y = \
                    scene.camera.calculate_viewport_parameters(100, 100)

                # All parameters should be positive and finite
                self.assertGreater(viewport_z, 0)
                self.assertGreater(viewport_height, 0)
                self.assertGreater(viewport_width, 0)
                self.assertGreater(pixel_size_x, 0)
                self.assertGreater(pixel_size_y, 0)

                self.assertTrue(math.isfinite(viewport_z))
                self.assertTrue(math.isfinite(viewport_height))
                self.assertTrue(math.isfinite(viewport_width))

    def test_stress_test_rapid_changes(self):
        """Stress test the camera system with rapid changes."""
        scene = Scene("Stress Test")

        # Rapidly change camera parameters
        for i in range(100):
            angle = i * 0.1
            direction = Vector3D(
                math.sin(angle),
                math.cos(angle * 0.7),
                -math.cos(angle)
            )

            position = Point3D(
                math.sin(angle * 1.3) * 10,
                math.cos(angle * 0.9) * 10,
                math.sin(angle * 1.7) * 10 + 20
            )

            fov = 30 + 60 * (math.sin(angle * 2) + 1) / 2  # FOV between 30 and 90

            # Apply changes
            scene.camera_direction = direction
            scene.camera_position = position
            scene.field_of_view = fov

            # System should remain stable
            self.assertIsNotNone(scene.camera.forward)
            self.assertIsNotNone(scene.camera.right)
            self.assertIsNotNone(scene.camera.up)

            # Generate a ray to ensure everything still works
            ray = scene.camera.generate_ray_for_pixel(50, 50, 100, 100)
            self.assertIsNotNone(ray.origin)
            self.assertIsNotNone(ray.dest)


if __name__ == '__main__':
    unittest.main()
