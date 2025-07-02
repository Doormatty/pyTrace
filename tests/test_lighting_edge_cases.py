import pytest
import sys
import os

# Add the project directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Scene import Scene
from Material import Material
from RGB import RGB
from Point import Point3D
from Vector import Vector3D
from Primitives import Sphere
from main import RayTracer
from RayIntersection import RayIntersection
from Normal import Normal


class TestLightingEdgeCases:
    """Test edge cases in the lighting system."""

    def setup_method(self):
        """Set up test fixtures."""
        self.ray_tracer = RayTracer(100, 100)
        self.test_sphere = Sphere(Point3D(0, 0, 0), 10, Material(RGB(0.5, 0.5, 0.5), luma=0.0))
        self.hit_point = Point3D(0, 0, 10)
        self.normal = Normal(0, 0, 1)
        self.hit = RayIntersection(self.test_sphere, self.normal, self.hit_point)

    def test_scene_with_no_ambient_lighting(self):
        """Test that a scene with no ambient lighting produces black pixels."""
        scene = Scene("No Ambient Scene", objects=[self.test_sphere], ambient_intensity=0)
        
        color = self.ray_tracer.lighting(self.hit, scene)
        brightness = color.r + color.g + color.b
        
        assert brightness == 0.0, f"Scene should be black but has brightness: {brightness}"

    def test_scene_with_zero_ambient_intensity(self):
        """Test that a scene with zero ambient intensity produces black pixels."""
        scene = Scene("Zero Ambient Scene", objects=[self.test_sphere], 
                     ambient_intensity=0, ambient_color=RGB(1.0, 1.0, 1.0))
        
        color = self.ray_tracer.lighting(self.hit, scene)
        brightness = color.r + color.g + color.b
        
        assert brightness == 0.0, f"Scene should be black but has brightness: {brightness}"

    def test_global_illumination_with_no_light_sources(self):
        """Test that global illumination with no light sources produces black pixels."""
        scene = Scene("No Light Sources", objects=[self.test_sphere], ambient_intensity=0)
        
        color = self.ray_tracer.global_illumination_lighting(self.hit, scene)
        brightness = color.r + color.g + color.b
        
        assert brightness == 0.0, f"Global illumination should be black but has brightness: {brightness}"

    def test_scene_with_ambient_lighting_produces_brightness(self):
        """Test that a scene with ambient lighting produces brightness (positive control)."""
        scene = Scene("Bright Ambient Scene", objects=[self.test_sphere], 
                     ambient_intensity=0.3, ambient_color=RGB(1.0, 1.0, 1.0))
        
        color = self.ray_tracer.lighting(self.hit, scene)
        brightness = color.r + color.g + color.b
        
        assert brightness > 0.0, f"Scene with ambient lighting should have brightness but is black"

    def test_emissive_object_returns_its_color(self):
        """Test that emissive objects return their color directly."""
        emissive_material = Material(RGB(1.0, 0.8, 0.6), luma=0.8)
        emissive_sphere = Sphere(Point3D(0, 0, 0), 10, emissive_material)
        emissive_hit = RayIntersection(emissive_sphere, self.normal, self.hit_point)
        
        scene = Scene("Emissive Test", objects=[emissive_sphere])
        color = self.ray_tracer.lighting(emissive_hit, scene)
        
        # Should match the material color since luma > 0
        expected = emissive_material.color
        assert abs(color.r - expected.r) < 0.001
        assert abs(color.g - expected.g) < 0.001
        assert abs(color.b - expected.b) < 0.001