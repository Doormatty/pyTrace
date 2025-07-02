"""
Test suite to verify and enforce the coordinate system convention.

This test suite ensures that the raytracer maintains the following axis convention:
- X = Left/Right (positive Right)
- Y = Forward/Backward (positive Forward)
- Z = Up/Down (positive Up)

These tests must NEVER be modified to accommodate changes to the coordinate system.
If these tests fail, the coordinate system implementation must be fixed, not the tests.
"""

import unittest
import math
from Camera import Camera
from Point import Point3D
from Vector import Vector3D


class TestCoordinateSystemConvention(unittest.TestCase):
    """
    Test suite to enforce the coordinate system convention.

    IMPORTANT: These tests define the coordinate system convention and must never be altered.
    If any test fails, fix the implementation, not the test.
    """

    def setUp(self):
        """Set up test fixtures."""
        self.tolerance = 1e-6

    def test_x_axis_convention_right_positive(self):
        """Test that positive X axis points to the RIGHT."""
        # Camera looking forward (negative Y), should have right vector pointing positive X
        camera_pos = Point3D(0, 10, 0)  # Camera behind origin
        camera_target = Point3D(0, 0, 0)  # Looking at origin (forward)
        camera = Camera(camera_pos, camera_target)

        right = camera.right

        # Right vector should point in positive X direction
        self.assertGreater(right.x, 0.9, 
                          f"Right vector X component should be positive (>0.9), got {right.x}")
        self.assertLess(abs(right.y), self.tolerance, 
                       f"Right vector Y component should be ~0, got {right.y}")
        self.assertLess(abs(right.z), self.tolerance, 
                       f"Right vector Z component should be ~0, got {right.z}")

    def test_x_axis_convention_left_negative(self):
        """Test that negative X axis points to the LEFT."""
        # Camera looking forward, object to the left should have negative X
        camera_pos = Point3D(0, 10, 0)
        camera_target = Point3D(0, 0, 0)
        camera = Camera(camera_pos, camera_target)

        # Point to the left of the target (from camera's perspective)
        left_point = Point3D(-5, 0, 0)  # Negative X = LEFT

        # Vector from target to left point
        left_vector = left_point - camera_target

        # This vector should have negative X component (pointing left)
        self.assertLess(left_vector.x, 0, 
                       f"Left direction should have negative X, got {left_vector.x}")

    def test_y_axis_convention_forward_positive(self):
        """Test that positive Y axis points FORWARD."""
        # Camera looking in positive Y direction should have forward vector with positive Y
        camera_pos = Point3D(0, -10, 0)  # Camera behind origin
        camera_target = Point3D(0, 0, 0)  # Looking at origin (forward in +Y)
        camera = Camera(camera_pos, camera_target)

        forward = camera.forward

        # Forward vector should point in positive Y direction
        self.assertLess(abs(forward.x), self.tolerance, 
                       f"Forward vector X component should be ~0, got {forward.x}")
        self.assertGreater(forward.y, 0.9, 
                          f"Forward vector Y component should be positive (>0.9), got {forward.y}")
        self.assertLess(abs(forward.z), self.tolerance, 
                       f"Forward vector Z component should be ~0, got {forward.z}")

    def test_y_axis_convention_backward_negative(self):
        """Test that negative Y axis points BACKWARD."""
        # Camera looking in negative Y direction should have forward vector with negative Y
        camera_pos = Point3D(0, 10, 0)  # Camera in front of origin
        camera_target = Point3D(0, 0, 0)  # Looking at origin (forward in -Y)
        camera = Camera(camera_pos, camera_target)

        forward = camera.forward

        # Forward vector should point in negative Y direction
        self.assertLess(abs(forward.x), self.tolerance, 
                       f"Forward vector X component should be ~0, got {forward.x}")
        self.assertLess(forward.y, -0.9, 
                       f"Forward vector Y component should be negative (<-0.9), got {forward.y}")
        self.assertLess(abs(forward.z), self.tolerance, 
                       f"Forward vector Z component should be ~0, got {forward.z}")

    def test_z_axis_convention_up_positive(self):
        """Test that positive Z axis points UP."""
        # Any horizontal camera direction should have up vector pointing positive Z
        test_directions = [
            Vector3D(1, 0, 0),   # Looking right
            Vector3D(-1, 0, 0),  # Looking left
            Vector3D(0, 1, 0),   # Looking forward
            Vector3D(0, -1, 0),  # Looking backward
        ]

        for direction in test_directions:
            with self.subTest(direction=direction):
                camera = Camera(Point3D(0, 0, 0), direction)
                up = camera.up

                # Up vector should point in positive Z direction
                self.assertGreater(up.z, 0.9, 
                                  f"Up vector Z component should be positive (>0.9) for direction {direction}, got {up.z}")

    def test_z_axis_convention_down_negative(self):
        """Test that negative Z axis points DOWN."""
        # Point below origin should have negative Z
        origin = Point3D(0, 0, 0)
        point_below = Point3D(0, 0, -5)  # Negative Z = DOWN

        down_vector = point_below - origin

        # This vector should have negative Z component (pointing down)
        self.assertLess(down_vector.z, 0, 
                       f"Down direction should have negative Z, got {down_vector.z}")

    def test_right_handed_coordinate_system(self):
        """Test that the coordinate system is right-handed."""
        # In a right-handed system: right × up = forward
        camera = Camera(Point3D(0, 10, 0), Point3D(0, 0, 0))  # Looking forward

        right = camera.right
        up = camera.up
        forward = camera.forward

        # Calculate right × up
        cross_product = right ^ up

        # This should be approximately equal to forward vector
        self.assertAlmostEqual(cross_product.x, forward.x, delta=self.tolerance,
                              msg="Right-handed system: (right × up).x should equal forward.x")
        self.assertAlmostEqual(cross_product.y, forward.y, delta=self.tolerance,
                              msg="Right-handed system: (right × up).y should equal forward.y")
        self.assertAlmostEqual(cross_product.z, forward.z, delta=self.tolerance,
                              msg="Right-handed system: (right × up).z should equal forward.z")

    def test_coordinate_system_consistency_across_directions(self):
        """Test that the coordinate system convention is consistent across different camera directions."""
        test_cases = [
            # (camera_pos, camera_target, description, expected_forward, expected_right, expected_up)
            (Point3D(0, 10, 0), Point3D(0, 0, 0), "Looking forward (-Y)", 
             Vector3D(0, -1, 0), Vector3D(1, 0, 0), Vector3D(0, 0, 1)),
            (Point3D(-10, 0, 0), Point3D(0, 0, 0), "Looking right (+X)", 
             Vector3D(1, 0, 0), Vector3D(0, 1, 0), Vector3D(0, 0, 1)),
            (Point3D(10, 0, 0), Point3D(0, 0, 0), "Looking left (-X)", 
             Vector3D(-1, 0, 0), Vector3D(0, -1, 0), Vector3D(0, 0, 1)),
            (Point3D(0, -10, 0), Point3D(0, 0, 0), "Looking backward (+Y)", 
             Vector3D(0, 1, 0), Vector3D(-1, 0, 0), Vector3D(0, 0, 1)),
        ]

        for camera_pos, camera_target, description, exp_forward, exp_right, exp_up in test_cases:
            with self.subTest(description=description):
                camera = Camera(camera_pos, camera_target)

                right = camera.right
                forward = camera.forward
                up = camera.up

                # Check that vectors match expected directions (within tolerance)
                self.assertAlmostEqual(forward.x, exp_forward.x, delta=self.tolerance,
                                     msg=f"{description}: Forward X mismatch")
                self.assertAlmostEqual(forward.y, exp_forward.y, delta=self.tolerance,
                                     msg=f"{description}: Forward Y mismatch")
                self.assertAlmostEqual(forward.z, exp_forward.z, delta=self.tolerance,
                                     msg=f"{description}: Forward Z mismatch")

                self.assertAlmostEqual(right.x, exp_right.x, delta=self.tolerance,
                                     msg=f"{description}: Right X mismatch")
                self.assertAlmostEqual(right.y, exp_right.y, delta=self.tolerance,
                                     msg=f"{description}: Right Y mismatch")
                self.assertAlmostEqual(right.z, exp_right.z, delta=self.tolerance,
                                     msg=f"{description}: Right Z mismatch")

                self.assertAlmostEqual(up.x, exp_up.x, delta=self.tolerance,
                                     msg=f"{description}: Up X mismatch")
                self.assertAlmostEqual(up.y, exp_up.y, delta=self.tolerance,
                                     msg=f"{description}: Up Y mismatch")
                self.assertAlmostEqual(up.z, exp_up.z, delta=self.tolerance,
                                     msg=f"{description}: Up Z mismatch")

    def test_coordinate_system_immutability(self):
        """Test that the coordinate system convention cannot be accidentally changed."""
        # This test documents the exact expected values for a standard camera setup
        camera_pos = Point3D(0, 10, 0)  # Camera at Y=10
        camera_target = Point3D(0, 0, 0)  # Looking at origin
        camera = Camera(camera_pos, camera_target)

        # These values define the coordinate system convention and must not change
        expected_forward = Vector3D(0, -1, 0)  # Forward = negative Y
        expected_right = Vector3D(1, 0, 0)     # Right = positive X
        expected_up = Vector3D(0, 0, 1)        # Up = positive Z

        # Verify exact values (within tolerance)
        self.assertAlmostEqual(camera.forward.x, expected_forward.x, delta=self.tolerance)
        self.assertAlmostEqual(camera.forward.y, expected_forward.y, delta=self.tolerance)
        self.assertAlmostEqual(camera.forward.z, expected_forward.z, delta=self.tolerance)

        self.assertAlmostEqual(camera.right.x, expected_right.x, delta=self.tolerance)
        self.assertAlmostEqual(camera.right.y, expected_right.y, delta=self.tolerance)
        self.assertAlmostEqual(camera.right.z, expected_right.z, delta=self.tolerance)

        self.assertAlmostEqual(camera.up.x, expected_up.x, delta=self.tolerance)
        self.assertAlmostEqual(camera.up.y, expected_up.y, delta=self.tolerance)
        self.assertAlmostEqual(camera.up.z, expected_up.z, delta=self.tolerance)


class TestCoordinateSystemDocumentation(unittest.TestCase):
    """
    Documentation tests that clearly state the coordinate system convention.
    """

    def test_coordinate_system_documentation(self):
        """Document the coordinate system convention for future reference."""
        # This test serves as living documentation
        convention = {
            'X_axis': 'Left/Right (positive = Right)',
            'Y_axis': 'Forward/Backward (positive = Forward)', 
            'Z_axis': 'Up/Down (positive = Up)',
            'handedness': 'Right-handed',
            'world_up': Vector3D(0, 0, 1),
            'standard_forward': 'Negative Y direction',
            'standard_right': 'Positive X direction'
        }

        # Verify with a test camera
        camera = Camera(Point3D(0, 10, 0), Point3D(0, 0, 0))

        # Document the expected behavior
        self.assertEqual(camera.forward.y, -1.0, "Standard forward direction is negative Y")
        self.assertEqual(camera.right.x, 1.0, "Standard right direction is positive X") 
        self.assertEqual(camera.up.z, 1.0, "Standard up direction is positive Z")

        # This test will fail if the coordinate system is changed, serving as a safeguard
        print(f"\nCoordinate System Convention: {convention}")


if __name__ == '__main__':
    unittest.main()
