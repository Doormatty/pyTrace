from __future__ import annotations

import math
from typing import Optional, Tuple, Union

from JsonSerializable import JsonSerializable
from Point import Point3D
from Ray import Ray
from Vector import Vector3D


class CameraConfig:
    """Configuration constants for camera calculations."""
    PARALLEL_THRESHOLD = 0.99
    NUMERICAL_TOLERANCE = 1e-6
    DEFAULT_WORLD_UP = Vector3D(0, 1, 0)
    DEFAULT_WORLD_RIGHT = Vector3D(1, 0, 0)
    FALLBACK_WORLD_RIGHT = Vector3D(0, 1, 0)


class Camera(JsonSerializable):
    """
    A robust camera class that handles coordinate system calculation and ray generation.

    This class encapsulates all camera-related logic and provides a mathematically
    stable approach to camera orientation that prevents unwanted camera roll.
    """

    def __init__(self, position: Point3D, direction: Union[Vector3D, Point3D], field_of_view: float = 90.0):
        """
        Initialize a camera with position, direction, and field of view.

        Args:
            position: Camera position in world space
            direction: Camera direction vector (will be normalized) or 3D point to "look at"
            field_of_view: Field of view angle in degrees (must be between 0 and 180)

        Raises:
            ValueError: If field_of_view is not in valid range (0, 180)
        """
        if not (0 < field_of_view < 180):
            raise ValueError(f"Field of view must be between 0 and 180 degrees, got {field_of_view}")

        self.position = position
        if isinstance(direction, Vector3D):
            self.set_direction(direction)
        elif isinstance(direction, Point3D):
            self.set_direction(direction - self.position)
        else:
            raise ValueError(f"Invalid direction type: {type(direction)}")

        self.field_of_view = field_of_view

        # Cache for coordinate system vectors
        self._forward: Optional[Vector3D] = None
        self._right: Optional[Vector3D] = None
        self._up: Optional[Vector3D] = None
        self._coordinate_system_valid = False

        # Calculate initial coordinate system
        self._update_coordinate_system()

    def _update_coordinate_system(self) -> None:
        """
        Calculate and cache the camera coordinate system using a mathematically stable approach.

        This method uses a "fixed world up" approach that keeps the horizon level
        by prioritizing alignment with the world up vector (0, 0, 1).
        """
        forward = self.direction

        # Define the world up direction to keep horizon level
        world_up = Vector3D(0, 0, 1)

        # If the camera direction is too close to the world up vector, use fallback
        if abs(forward % world_up) > CameraConfig.PARALLEL_THRESHOLD:
            # Camera is looking nearly straight up or down, use world right as reference
            world_right = CameraConfig.DEFAULT_WORLD_RIGHT
            # Calculate right vector
            right = forward ^ world_right
            right = right.normalize()
            # Calculate up vector to maintain orthogonality
            up = right ^ forward
            up = up.normalize()
        else:
            # Normal case: calculate right vector to be perpendicular to both forward and world up
            right = forward ^ world_up
            right = right.normalize()
            # Calculate up vector to maintain orthogonality and be as close to world up as possible
            up = right ^ forward
            up = up.normalize()

        # Cache the results
        self._forward = forward
        self._right = right
        self._up = up

        # Validate the coordinate system
        self._validate_coordinate_system()
        self._coordinate_system_valid = True

    def _validate_coordinate_system(self) -> None:
        """
        Validate that the coordinate system is orthonormal.

        Raises:
            ValueError: If the coordinate system is not orthonormal within tolerance
        """
        if not (self._forward and self._right and self._up):
            raise ValueError("Coordinate system vectors not calculated")

        tolerance = CameraConfig.NUMERICAL_TOLERANCE

        # Check orthogonality
        forward_right_dot = abs(self._forward % self._right)
        forward_up_dot = abs(self._forward % self._up)
        right_up_dot = abs(self._right % self._up)

        if forward_right_dot > tolerance:
            raise ValueError(f"Forward and right vectors not orthogonal: {forward_right_dot}")
        if forward_up_dot > tolerance:
            raise ValueError(f"Forward and up vectors not orthogonal: {forward_up_dot}")
        if right_up_dot > tolerance:
            raise ValueError(f"Right and up vectors not orthogonal: {right_up_dot}")

        # Check normalization
        forward_length = abs(self._forward.length - 1.0)
        right_length = abs(self._right.length - 1.0)
        up_length = abs(self._up.length - 1.0)

        if forward_length > tolerance:
            raise ValueError(f"Forward vector not normalized: length = {self._forward.length}")
        if right_length > tolerance:
            raise ValueError(f"Right vector not normalized: length = {self._right.length}")
        if up_length > tolerance:
            raise ValueError(f"Up vector not normalized: length = {self._up.length}")

    @property
    def forward(self) -> Vector3D:
        """Get the forward vector of the camera coordinate system."""
        if not self._coordinate_system_valid:
            self._update_coordinate_system()
        return self._forward

    @property
    def right(self) -> Vector3D:
        """Get the right vector of the camera coordinate system."""
        if not self._coordinate_system_valid:
            self._update_coordinate_system()
        return self._right

    @property
    def up(self) -> Vector3D:
        """Get the up vector of the camera coordinate system."""
        if not self._coordinate_system_valid:
            self._update_coordinate_system()
        return self._up

    def set_direction(self, direction: Vector3D) -> None:
        """
        Set a new camera direction and update the coordinate system.

        Args:
            direction: New camera direction vector (will be normalized)
        """
        self.direction = direction.normalize()
        self._coordinate_system_valid = False
        self._update_coordinate_system()

    def set_position(self, position: Point3D) -> None:
        """
        Set a new camera position.

        Args:
            position: New camera position in world space
        """
        self.position = position

    def look_at(self, target: Point3D) -> None:
        """
        Set the camera direction to look at a specific 3D point.

        The camera direction will be calculated as the normalized vector
        from the camera's current position to the target point.

        Args:
            target: The 3D point that the camera should look at
        """
        # Calculate direction vector from camera position to target
        direction_vector = target - self.position

        # Set the camera direction (set_direction will normalize it automatically)
        self.set_direction(direction_vector)

    def calculate_viewport_parameters(self, screen_width: int, screen_height: int) -> Tuple[float, float, float, float, float]:
        """
        Calculate viewport parameters for ray generation.

        Args:
            screen_width: Screen width in pixels
            screen_height: Screen height in pixels

        Returns:
            Tuple of (viewport_z, viewport_height, viewport_width, pixel_size_x, pixel_size_y)
        """
        # Calculate viewport parameters based on field of view
        aspect_ratio = screen_width / screen_height
        fov_radians = math.radians(self.field_of_view)

        # Use a fixed viewport distance and calculate height based on FOV
        viewport_z = 1.0
        viewport_height = 2.0 * math.tan(fov_radians / 2.0)
        viewport_width = viewport_height * aspect_ratio

        # Calculate pixel sizes
        pixel_size_x = viewport_width / screen_width
        pixel_size_y = viewport_height / screen_height

        return viewport_z, viewport_height, viewport_width, pixel_size_x, pixel_size_y

    def generate_ray_for_pixel(self, x: int, y: int, screen_width: int, screen_height: int,
                               offset_x: float = 0.0, offset_y: float = 0.0) -> Ray:
        """
        Generate a ray for a specific pixel with optional subpixel offsets.

        Args:
            x: Pixel x coordinate
            y: Pixel y coordinate
            screen_width: Screen width in pixels
            screen_height: Screen height in pixels
            offset_x: Subpixel offset in x direction (-0.5 to 0.5)
            offset_y: Subpixel offset in y direction (-0.5 to 0.5)

        Returns:
            Ray from camera through the specified pixel
        """
        # Calculate viewport parameters
        viewport_z, _, _, pixel_size_x, pixel_size_y = self.calculate_viewport_parameters(screen_width, screen_height)

        # Calculate pixel position in viewport coordinates
        viewport_x = pixel_size_x * (x - 0.5 * (screen_width - 1) + offset_x)
        viewport_y = pixel_size_y * (0.5 * (screen_height - 1) - y + offset_y)

        # Calculate ray direction using camera coordinate system
        # Correct coordinate mapping: screen X should map to camera right, screen Y should map to camera up
        ray_dir = self.forward * viewport_z + self.right * viewport_x + self.up * viewport_y
        ray_dir = ray_dir.normalize()

        return Ray(self.position, ray_dir)

    def to_json(self) -> dict:
        """Convert camera to JSON-serializable dictionary."""
        return {
            "type": "camera",
            "position": self.position.to_json(),
            "direction": self.direction.to_json(),
            "field_of_view": self.field_of_view
        }

    @classmethod
    def from_json(cls, data: dict) -> 'Camera':
        """Create a Camera instance from JSON data."""
        position = Point3D.from_json(data["position"])
        direction = Vector3D.from_json(data["direction"])
        field_of_view = data.get("field_of_view", 90.0)

        return cls(position, direction, field_of_view)

    def __repr__(self) -> str:
        return f"Camera(position={self.position}, direction={self.direction}, fov={self.field_of_view})"
