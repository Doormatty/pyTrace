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


class TestShadows:
    """Test shadow casting in the global illumination lighting function."""

    def setup_method(self):
        """Set up test fixtures."""
        # Create a scene
        self.scene = Scene(
            name="Shadow Test",
            camera_position=Point3D(0, 0, 150),
            camera_direction=Vector3D(0, 0, -1),
            background_color=RGB(0.0, 0.0, 0.0)
        )

        # Create materials
        # Emissive material (light source)
        self.light_material = Material(
            color=RGB(1.0, 1.0, 1.0),  # White light
            luma=1.0  # Full emissive
        )

        # Occluder material (object that should cast shadow)
        self.occluder_material = Material(
            color=RGB(0.5, 0.5, 0.5),  # Gray
            reflect=0.0,
            luma=0.0
        )

        # Ground material (surface to receive shadow)
        self.ground_material = Material(
            color=RGB(0.8, 0.8, 0.8),  # Light gray
            reflect=0.0,
            luma=0.0
        )

        # Create objects
        # Light source (emissive sphere) - positioned above and to the left
        self.light_sphere = Sphere(
            center=Point3D(-30, 30, 60),  # Upper left
            radius=8,
            material=self.light_material
        )

        # Shadow caster (sphere between light and ground) - positioned to cast shadow
        self.shadow_caster = Sphere(
            center=Point3D(0, 0, 10),  # Between light and ground
            radius=12,
            material=self.occluder_material
        )

        # Ground plane (should receive shadow)
        self.ground = Plane(
            center=Point3D(0, 0, -20),
            normal=Vector3D(0, 0, 1),
            material=self.ground_material
        )

        # Add objects to scene
        self.scene.add_object(self.light_sphere)
        self.scene.add_object(self.shadow_caster)
        self.scene.add_object(self.ground)

        # Create raytracer
        self.raytracer = RayTracer(
            screen_width=400,
            screen_height=400,
            recursion_limit=3,
            supersampling=1
        )

    def test_scene_setup(self):
        """Test that the shadow test scene is set up correctly."""
        assert len(self.scene) == 3
        assert self.light_sphere.material.luma == 1.0
        assert self.shadow_caster.material.luma == 0.0
        assert self.ground.material.luma == 0.0

    def test_shadow_vs_lit_areas(self):
        """Test that shadowed areas are darker than lit areas."""
        # Point that should be in shadow (positioned where shadow should fall)
        shadow_point = Point3D(15, -15, -20)

        # Point that should be lit (not blocked by shadow caster)
        lit_point = Point3D(-15, -15, -20)

        # Create test rays hitting these points
        shadow_ray = Ray(Point3D(15, -15, 100), Vector3D(0, 0, -1))
        lit_ray = Ray(Point3D(-15, -15, 100), Vector3D(0, 0, -1))

        # Get intersections with ground
        shadow_intersection = self.ground.hit(shadow_ray)
        lit_intersection = self.ground.hit(lit_ray)

        assert shadow_intersection is not False, "Shadow ray should hit ground"
        assert lit_intersection is not False, "Lit ray should hit ground"
        assert hasattr(shadow_intersection, 'hit_point'), "Shadow intersection should have hit_point"
        assert hasattr(lit_intersection, 'hit_point'), "Lit intersection should have hit_point"

        # Test lighting at both points
        shadow_color = self.raytracer.global_illumination_lighting(shadow_intersection, self.scene)
        lit_color = self.raytracer.global_illumination_lighting(lit_intersection, self.scene)

        # Calculate brightness
        shadow_brightness = shadow_color.r + shadow_color.g + shadow_color.b
        lit_brightness = lit_color.r + lit_color.g + lit_color.b

        # Check if shadows are working (lit point should be significantly brighter)
        assert lit_brightness > shadow_brightness * 1.1, \
            f"Lit point ({lit_brightness:.3f}) should be brighter than shadow point ({shadow_brightness:.3f})"

    def test_ray_blocking_functionality(self):
        """Test the ray blocking function directly."""
        # Create ray from above the ground pointing down to hit the ground
        shadow_ray = Ray(Point3D(15, -15, 100), Vector3D(0, 0, -1))
        shadow_intersection = self.ground.hit(shadow_ray)

        assert shadow_intersection is not False, "Ray should hit ground"
        assert hasattr(shadow_intersection, 'hit_point'), "Intersection should have hit_point attribute"

        # Create ray from shadow point to light
        light_center = self.light_sphere.center
        shadow_to_light = Ray()
        shadow_to_light.origin = shadow_intersection.hit_point
        shadow_to_light.dest = (light_center - shadow_intersection.hit_point).normalize()
        distance_to_light = shadow_intersection.hit_point.distance(light_center)

        # Test if ray is blocked
        is_blocked = self.raytracer._is_ray_blocked(
            shadow_to_light, self.scene, self.light_sphere, self.ground, distance_to_light
        )

        assert is_blocked, "Ray from shadow point to light should be blocked by shadow caster"

    def test_unblocked_ray_to_light(self):
        """Test that rays from lit areas to light sources are not blocked."""
        # Create ray from above the ground pointing down to hit the ground
        lit_ray = Ray(Point3D(-15, -15, 100), Vector3D(0, 0, -1))
        lit_intersection = self.ground.hit(lit_ray)

        assert lit_intersection is not False, "Ray should hit ground"
        assert hasattr(lit_intersection, 'hit_point'), "Intersection should have hit_point attribute"

        # Create ray from lit point to light
        light_center = self.light_sphere.center
        lit_to_light = Ray()
        lit_to_light.origin = lit_intersection.hit_point
        lit_to_light.dest = (light_center - lit_intersection.hit_point).normalize()
        distance_to_light = lit_intersection.hit_point.distance(light_center)

        # Test if ray is blocked
        is_blocked = self.raytracer._is_ray_blocked(
            lit_to_light, self.scene, self.light_sphere, self.ground, distance_to_light
        )

        assert not is_blocked, "Ray from lit point to light should not be blocked"

    def test_shadow_caster_intersection(self):
        """Test that the shadow caster properly intersects rays."""
        # Create ray from above the ground pointing down to hit the ground
        shadow_ray = Ray(Point3D(15, -15, 100), Vector3D(0, 0, -1))
        shadow_intersection = self.ground.hit(shadow_ray)

        assert shadow_intersection is not False, "Ray should hit ground"
        assert hasattr(shadow_intersection, 'hit_point'), "Intersection should have hit_point attribute"

        light_center = self.light_sphere.center
        shadow_to_light = Ray()
        shadow_to_light.origin = shadow_intersection.hit_point
        shadow_to_light.dest = (light_center - shadow_intersection.hit_point).normalize()

        # Test intersection with shadow caster
        shadow_caster_intersection = self.shadow_caster.hit(shadow_to_light)

        assert shadow_caster_intersection is not False, "Ray should intersect with shadow caster"
        assert hasattr(shadow_caster_intersection, 'hit_point'), "Shadow caster intersection should have hit_point"

        # Verify intersection is between ground and light
        dist_to_intersection = shadow_to_light.origin.distance(shadow_caster_intersection.hit_point)
        distance_to_light = shadow_to_light.origin.distance(light_center)

        assert dist_to_intersection < distance_to_light, \
            "Shadow caster intersection should be closer than light source"
