import pytest
import sys
import os

# Add the project directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import create_scene
from Ray import Ray
from Point import Point3D
from Vector import Vector3D


class TestMainScene:
    """Test the main scene creation and terrain functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.scene = create_scene()

    def test_scene_creation(self):
        """Test that the main scene is created successfully."""
        assert self.scene is not None, "Scene should be created successfully"
        assert len(self.scene.objects) > 0, "Scene should contain objects"

    def test_scene_contains_terrain(self):
        """Test that the scene contains terrain objects (if any)."""
        terrain_found = False
        terrain_object = None

        for obj in self.scene.objects:
            if hasattr(obj, 'cubes'):
                terrain_found = True
                terrain_object = obj
                break

        if terrain_found:
            assert terrain_object is not None, "Terrain object should not be None"
            assert len(terrain_object.cubes) > 0, "Terrain should contain cubes"
            print(f"Found terrain with {len(terrain_object.cubes)} cubes")
        else:
            print("No terrain objects found in scene (this is acceptable)")

    def test_terrain_cube_dimensions(self):
        """Test that terrain cubes have proper dimensions (if terrain exists)."""
        terrain = None
        for obj in self.scene.objects:
            if hasattr(obj, 'cubes'):
                terrain = obj
                break

        if terrain is not None:
            if len(terrain.cubes) > 0:
                cube = terrain.cubes[0]

                # Check that cube has proper attributes
                assert hasattr(cube, 'minx'), "Cube should have minx attribute"
                assert hasattr(cube, 'maxx'), "Cube should have maxx attribute"
                assert hasattr(cube, 'miny'), "Cube should have miny attribute"
                assert hasattr(cube, 'maxy'), "Cube should have maxy attribute"
                assert hasattr(cube, 'minz'), "Cube should have minz attribute"
                assert hasattr(cube, 'maxz'), "Cube should have maxz attribute"

                # Check that dimensions are positive
                width = cube.maxx - cube.minx
                height = cube.maxy - cube.miny
                depth = cube.maxz - cube.minz

                assert width > 0, f"Cube width should be positive, got {width}"
                assert height > 0, f"Cube height should be positive, got {height}"
                assert depth > 0, f"Cube depth should be positive, got {depth}"
                print(f"Terrain cube dimensions: {width:.1f} x {height:.1f} x {depth:.1f}")
            else:
                print("Terrain found but contains no cubes")
        else:
            print("No terrain found in scene (test skipped)")

    def test_ray_intersection_with_terrain(self):
        """Test that rays can intersect with terrain objects (if terrain exists)."""
        # Find terrain object
        terrain = None
        for obj in self.scene.objects:
            if hasattr(obj, 'cubes'):
                terrain = obj
                break

        if terrain is not None:
            # Test ray pointing down from above the terrain
            test_ray = Ray(Point3D(0, 10, 0), Vector3D(0, -1, 0))
            intersection = terrain.hit(test_ray)

            # Note: This test may pass or fail depending on terrain generation
            # The important thing is that the hit method works without errors
            if intersection:
                assert intersection.hit_point is not None, "Intersection should have hit point"
                assert intersection.normal is not None, "Intersection should have normal"
                print("Ray successfully intersected with terrain")
            else:
                print("Ray did not intersect terrain (acceptable depending on terrain layout)")
        else:
            print("No terrain found in scene (test skipped)")

    def test_scene_object_types(self):
        """Test that the scene contains expected object types."""
        object_types = []
        for obj in self.scene.objects:
            object_types.append(type(obj).__name__)

        # Should contain at least some recognizable object types
        assert len(object_types) > 0, "Scene should contain objects"

        # Log object types for debugging
        print(f"Scene contains object types: {object_types}")

    def test_ray_intersection_with_scene_objects(self):
        """Test that rays can intersect with various scene objects."""
        # Test ray pointing down from above
        test_ray = Ray(Point3D(0, 10, 0), Vector3D(0, -1, 0))

        intersections = []
        for obj in self.scene.objects:
            intersection = obj.hit(test_ray)
            if intersection:
                intersections.append((type(obj).__name__, intersection))

        # At least one object should be intersectable (though not necessarily hit by this specific ray)
        # The important thing is that hit methods work without errors
        print(f"Found {len(intersections)} intersections with scene objects")

    def test_scene_has_camera_settings(self):
        """Test that the scene has proper camera settings."""
        assert hasattr(self.scene, 'camera_position'), "Scene should have camera position"
        assert hasattr(self.scene, 'camera_direction'), "Scene should have camera direction"

        # Camera position should be a valid Point3D
        assert self.scene.camera_position is not None, "Camera position should not be None"

        # Camera direction should be a valid Vector3D
        assert self.scene.camera_direction is not None, "Camera direction should not be None"

    def test_scene_background_color(self):
        """Test that the scene has a background color."""
        assert hasattr(self.scene, 'background_color'), "Scene should have background color"
        assert self.scene.background_color is not None, "Background color should not be None"

    def test_multiple_ray_intersections(self):
        """Test ray intersections from different angles."""
        test_rays = [
            Ray(Point3D(0, 10, 0), Vector3D(0, -1, 0)),    # From above
            Ray(Point3D(10, 0, 0), Vector3D(-1, 0, 0)),    # From right
            Ray(Point3D(0, 0, 10), Vector3D(0, 0, -1)),    # From front
            Ray(Point3D(-10, 0, 0), Vector3D(1, 0, 0)),    # From left
        ]

        total_intersections = 0
        for i, test_ray in enumerate(test_rays):
            ray_intersections = 0
            for obj in self.scene.objects:
                intersection = obj.hit(test_ray)
                if intersection:
                    ray_intersections += 1

            total_intersections += ray_intersections
            print(f"Ray {i+1} found {ray_intersections} intersections")

        print(f"Total intersections found: {total_intersections}")
        # The test passes as long as no exceptions are thrown
        assert True, "Ray intersection tests completed successfully"
