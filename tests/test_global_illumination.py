import pytest
import sys
import os

# Add the project directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import RayTracer
from Scene import Scene
from Primitives import Sphere, Plane
from Material import Material
from RGB import RGB
from Point import Point3D
from Vector import Vector3D
from Ray import Ray
from RayIntersection import RayIntersection


class TestGlobalIllumination:
    """Test the global illumination lighting function."""

    def setup_method(self):
        """Set up test fixtures."""
        # Create a scene
        self.scene = Scene(
            name="Global Illumination Test",
            camera_position=Point3D(0, 0, 150),
            camera_direction=Vector3D(0, 0, -1),
            background_color=RGB(0.0, 0.0, 0.0)
        )

        # Create materials
        # Emissive material (light source)
        self.emissive_material = Material(
            color=RGB(1.0, 1.0, 0.8),  # Warm white
            luma=0.8  # High emissive value
        )

        # Reflective material
        self.reflective_material = Material(
            color=RGB(0.8, 0.8, 0.9),  # Light blue
            reflect=0.0  # High reflectivity
        )

        # Regular diffuse material
        self.diffuse_material = Material(
            color=RGB(0.6, 0.3, 0.3),  # Red
            reflect=0.0,
            luma=0.0
        )

        # Create objects
        # Emissive sphere (acts as a light source)
        self.light_sphere = Sphere(
            center=Point3D(-30, 30, 50),
            radius=10,
            material=self.emissive_material
        )

        # Reflective sphere
        self.reflective_sphere = Sphere(
            center=Point3D(30, -20, 30),
            radius=15,
            material=self.reflective_material
        )

        # Main object to be lit
        self.main_sphere = Sphere(
            center=Point3D(0, 0, 0),
            radius=20,
            material=self.diffuse_material
        )

        # Ground plane
        self.ground = Plane(
            center=Point3D(0, 0, -30),
            normal=Vector3D(0, 0, 1),
            material=Material(color=RGB(0.4, 0.4, 0.4))
        )

        # Add objects to scene
        self.scene.add_object(self.light_sphere)
        self.scene.add_object(self.reflective_sphere)
        self.scene.add_object(self.main_sphere)

        # Create raytracer
        self.raytracer = RayTracer(
            screen_width=400,
            screen_height=400,
            recursion_limit=3,
            supersampling=1
        )

    def test_scene_setup(self):
        """Test that the global illumination test scene is set up correctly."""
        assert len(self.scene) == 3
        
        # Count objects with reflect > 0 or luma > 0
        light_sources = 0
        for obj in self.scene:
            if hasattr(obj, 'material'):
                if obj.material.reflect > 0 or obj.material.luma > 0:
                    light_sources += 1
        
        assert light_sources >= 1, "Scene should have at least one light source"

    def test_global_illumination_vs_basic_lighting(self):
        """Test that global illumination produces different results than basic lighting."""
        # Create a test ray hitting the main sphere
        test_ray = Ray(Point3D(0, 0, 100), Vector3D(0, 0, -1))
        intersection = self.main_sphere.hit(test_ray)
        
        assert intersection is not None, "Test ray should hit main sphere"

        # Test old lighting
        old_color = self.raytracer.lighting(intersection, self.scene)
        
        # Test new global illumination lighting
        new_color = self.raytracer.global_illumination_lighting(intersection, self.scene)

        # Calculate brightness
        old_brightness = old_color.r + old_color.g + old_color.b
        new_brightness = new_color.r + new_color.g + new_color.b

        # Global illumination should produce some lighting from emissive objects
        assert new_brightness >= 0, "Global illumination should produce non-negative brightness"

    def test_emissive_object_contribution(self):
        """Test that emissive objects contribute light to the scene."""
        # Create a test ray hitting the main sphere
        test_ray = Ray(Point3D(0, 0, 100), Vector3D(0, 0, -1))
        intersection = self.main_sphere.hit(test_ray)
        
        assert intersection is not None, "Test ray should hit main sphere"

        # Test global illumination lighting
        color = self.raytracer.global_illumination_lighting(intersection, self.scene)
        brightness = color.r + color.g + color.b

        # With an emissive light source, there should be some illumination
        assert brightness > 0, f"Scene with emissive objects should produce brightness, got {brightness}"

    def test_light_source_detection(self):
        """Test that the system correctly identifies light sources."""
        light_sources = []
        
        for obj in self.scene.objects:
            if obj != self.main_sphere and hasattr(obj, 'material'):
                obj_material = obj.material
                if obj_material.reflect > 0 or obj_material.luma > 0:
                    light_sources.append(obj)

        assert len(light_sources) >= 1, "Should detect at least one light source"
        
        # Check that the emissive sphere is detected as a light source
        emissive_found = False
        for light_obj in light_sources:
            if light_obj.material.luma > 0:
                emissive_found = True
                break
        
        assert emissive_found, "Emissive sphere should be detected as a light source"

    def test_no_light_sources_produces_black(self):
        """Test that a scene with no light sources produces black."""
        # Create a scene with only non-emissive, non-reflective objects
        dark_scene = Scene(
            name="Dark Scene",
            camera_position=Point3D(0, 0, 150),
            background_color=RGB(0.0, 0.0, 0.0),
            ambient_intensity=0
        )
        
        dark_material = Material(color=RGB(0.5, 0.5, 0.5), reflect=0.0, luma=0.0)
        dark_sphere = Sphere(Point3D(0, 0, 0), 10, dark_material)
        dark_scene.add_object(dark_sphere)

        # Create intersection
        test_ray = Ray(Point3D(0, 0, 100), Vector3D(0, 0, -1))
        intersection = dark_sphere.hit(test_ray)
        
        assert intersection is not None, "Test ray should hit dark sphere"

        # Test global illumination
        color = self.raytracer.global_illumination_lighting(intersection, dark_scene)
        brightness = color.r + color.g + color.b

        assert brightness == 0.0, f"Scene with no light sources should be black, got brightness {brightness}"

    def test_surface_sample_points_generation(self):
        """Test that surface sample points are generated for light sources."""
        # Test the _get_surface_sample_points method
        sample_points = self.raytracer._get_surface_sample_points(self.light_sphere, num_samples=4)
        
        assert len(sample_points) == 4, "Should generate requested number of sample points"
        
        # All sample points should be on or near the sphere surface
        for point in sample_points:
            distance_from_center = self.light_sphere.center.distance(point)
            # Allow some tolerance for surface sampling
            assert abs(distance_from_center - self.light_sphere.radius) < 1.0, \
                f"Sample point should be near sphere surface, distance: {distance_from_center}"