import pytest
import sys
import os

# Add the project directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import RayTracer
from Scene import Scene
from Primitives import Sphere, Cube
from Material import Material
from RGB import RGB
from Point import Point3D
from Vector import Vector3D
from Ray import Ray


class TestShadowBlocking:
    """Test shadow blocking with zero ambient illumination."""

    def setup_method(self):
        """Set up test fixtures."""
        # Create a scene with zero ambient illumination
        self.scene = Scene(
            name="Shadow Blocking Test",
            camera_position=Point3D(0, 0, 150),
            camera_direction=Vector3D(0, 0, -1),
            background_color=RGB(0.0, 0.0, 0.0),
            ambient_intensity=0.0  # Zero ambient illumination
        )

        # Create materials
        # Emissive material (luma = 1)
        self.emissive_material = Material(
            color=RGB(1.0, 1.0, 1.0),  # White light
            luma=1.0  # Maximum emissive value
        )

        # Non-emissive material (luma = 0)
        self.non_emissive_material = Material(
            color=RGB(0.5, 0.5, 0.5),  # Gray
            luma=0.0,  # No emission
            reflect=0.0  # No reflection
        )

        # Blocking cube material
        self.blocking_material = Material(
            color=RGB(0.3, 0.3, 0.3),  # Dark gray
            luma=0.0,  # No emission
            reflect=0.0  # No reflection
        )

        # Create objects
        # Emissive sphere (light source) - positioned to the left
        self.light_sphere = Sphere(
            center=Point3D(-50, 0, 0),
            radius=10,
            material=self.emissive_material
        )

        # Non-emissive sphere (target) - positioned to the right
        self.target_sphere = Sphere(
            center=Point3D(50, 0, 0),
            radius=10,
            material=self.non_emissive_material
        )

        # Blocking cube - positioned between the two spheres
        # Make it large enough to completely block light rays
        self.blocking_cube = Cube(
            a=Point3D(-15, -25, -25),  # One corner
            b=Point3D(15, 25, 25),     # Opposite corner
            material=self.blocking_material
        )

        # Add objects to scene
        self.scene.add_object(self.light_sphere)
        self.scene.add_object(self.target_sphere)
        self.scene.add_object(self.blocking_cube)

        # Create raytracer
        self.raytracer = RayTracer(
            screen_width=400,
            screen_height=400,
            recursion_limit=3,
            supersampling=1
        )

    def test_scene_setup(self):
        """Test that the shadow blocking scene is set up correctly."""
        assert len(self.scene) == 3, "Scene should have 3 objects"
        
        # Verify we have one light source (emissive object)
        light_sources = 0
        for obj in self.scene:
            if hasattr(obj, 'material') and obj.material.luma > 0:
                light_sources += 1
        
        assert light_sources == 1, "Scene should have exactly one light source"
        
        # Verify zero ambient illumination
        assert self.scene.ambient_intensity == 0.0, "Scene should have zero ambient illumination"

    def test_emissive_sphere_self_illumination(self):
        """Test that the emissive sphere illuminates itself."""
        # Create a ray hitting the emissive sphere
        test_ray = Ray(Point3D(-50, 0, 100), Vector3D(0, 0, -1))
        intersection = self.light_sphere.hit(test_ray)
        
        assert intersection is not None, "Test ray should hit emissive sphere"

        # Test global illumination lighting
        color = self.raytracer.global_illumination_lighting(intersection, self.scene)
        brightness = color.r + color.g + color.b

        # Emissive objects should return their own color directly
        assert brightness > 0, f"Emissive sphere should be bright, got brightness {brightness}"

    def test_target_sphere_blocked_by_cube(self):
        """Test that the target sphere receives no light due to the blocking cube."""
        # Create a ray hitting the target sphere from the front
        test_ray = Ray(Point3D(50, 0, 100), Vector3D(0, 0, -1))
        intersection = self.target_sphere.hit(test_ray)
        
        assert intersection is not None, "Test ray should hit target sphere"

        # Test global illumination lighting
        color = self.raytracer.global_illumination_lighting(intersection, self.scene)
        brightness = color.r + color.g + color.b

        # With zero ambient illumination and the cube blocking all light from the emissive sphere,
        # the target sphere should be completely black
        assert brightness == 0.0, f"Target sphere should be black due to blocking cube, got brightness {brightness}"

    def test_cube_blocks_direct_light_path(self):
        """Test that the cube is positioned to block the direct light path."""
        # Test a ray from the light sphere center towards the target sphere center
        light_center = self.light_sphere.center
        target_center = self.target_sphere.center
        
        # Create a ray from light to target
        direction = (target_center - light_center).normalize()
        test_ray = Ray(light_center, direction)
        
        # The ray should hit the blocking cube before reaching the target sphere
        cube_intersection = self.blocking_cube.hit(test_ray)
        target_intersection = self.target_sphere.hit(test_ray)
        
        assert cube_intersection is not False, "Ray should hit the blocking cube"
        assert target_intersection is not False, "Ray should also be able to hit target sphere if extended"
        
        # The cube intersection should be closer than the target intersection
        if cube_intersection and target_intersection:
            assert cube_intersection.distance < target_intersection.distance, \
                "Cube should block the direct path to target sphere"

    def test_no_ambient_light_produces_black_for_non_emissive(self):
        """Test that non-emissive objects in zero ambient light with blocked direct light are black."""
        # Test the blocking cube itself
        test_ray = Ray(Point3D(0, 0, 100), Vector3D(0, 0, -1))
        intersection = self.blocking_cube.hit(test_ray)
        
        assert intersection is not None, "Test ray should hit blocking cube"

        # Test global illumination lighting
        color = self.raytracer.global_illumination_lighting(intersection, self.scene)
        brightness = color.r + color.g + color.b

        # The cube should be black since it's non-emissive, non-reflective, 
        # and there's no ambient light
        assert brightness == 0.0, f"Blocking cube should be black, got brightness {brightness}"

    def test_light_sphere_material_properties(self):
        """Test that the light sphere has the correct material properties."""
        assert self.light_sphere.material.luma == 1.0, "Light sphere should have luma = 1.0"
        assert self.light_sphere.material.reflect == 0.0, "Light sphere should have no reflectivity"

    def test_target_sphere_material_properties(self):
        """Test that the target sphere has the correct material properties."""
        assert self.target_sphere.material.luma == 0.0, "Target sphere should have luma = 0.0"
        assert self.target_sphere.material.reflect == 0.0, "Target sphere should have no reflectivity"

    def test_cube_size_adequate_for_blocking(self):
        """Test that the cube is large enough to block light between the spheres."""
        # Check cube dimensions
        cube_width = self.blocking_cube.maxx - self.blocking_cube.minx
        cube_height = self.blocking_cube.maxy - self.blocking_cube.miny
        cube_depth = self.blocking_cube.maxz - self.blocking_cube.minz
        
        # Cube should be larger than the sphere diameters
        sphere_diameter = self.light_sphere.radius * 2
        
        assert cube_width > sphere_diameter, "Cube width should be larger than sphere diameter"
        assert cube_height > sphere_diameter, "Cube height should be larger than sphere diameter"
        assert cube_depth > sphere_diameter, "Cube depth should be larger than sphere diameter"