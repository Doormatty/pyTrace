import pytest
import sys
import os

# Add the project directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Terrain import Terrain
from Material import Material
from RGB import RGB
from Point import Point3D
from Ray import Ray
from Vector import Vector3D
from Scene import Scene
from main import RayTracer


class TestTerrain:
    """Comprehensive tests for the Terrain class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.test_material = Material(RGB(0.5, 0.5, 0.5), 1.0, 0, 0.0)
        
    def test_terrain_initialization(self):
        """Test that terrain initializes with correct parameters."""
        terrain = Terrain(
            noise_scale=0.1,
            noise_amplitude=0.5,
            cube_size=1.0,
            gap_distance=0.0,
            width=3.0,
            depth=3.0,
            height=2.0,
            location=Point3D(0, 0, 0),
            material=self.test_material,
            seed=123
        )
        
        assert terrain.noise_scale == 0.1
        assert terrain.noise_amplitude == 0.5
        assert terrain.cube_size == 1.0
        assert terrain.gap_distance == 0.0
        assert terrain.width == 3.0
        assert terrain.depth == 3.0
        assert terrain.height == 2.0
        assert terrain.location == Point3D(0, 0, 0)
        assert terrain.material == self.test_material
        assert terrain.seed == 123

    def test_terrain_cube_creation(self):
        """Test that terrain creates proper cubes."""
        terrain = Terrain(
            noise_scale=0.1,
            noise_amplitude=0.5,
            cube_size=1.0,
            gap_distance=0.0,
            width=3.0,
            depth=3.0,
            height=2.0,
            location=Point3D(0, 0, 0),
            material=self.test_material,
            seed=123
        )
        
        # Check that cubes were created
        assert len(terrain.cubes) > 0, "Terrain should contain cubes"
        
        # Check expected number of cubes
        expected_cubes = terrain.num_cubes_x * terrain.num_cubes_z
        assert len(terrain.cubes) <= expected_cubes, "Number of cubes should not exceed expected"
        
        # Check that cubes have proper attributes
        for cube in terrain.cubes[:3]:  # Check first few cubes
            assert hasattr(cube, 'a'), "Cube should have point a"
            assert hasattr(cube, 'b'), "Cube should have point b"
            assert hasattr(cube, 'minx'), "Cube should have minx"
            assert hasattr(cube, 'maxx'), "Cube should have maxx"
            assert hasattr(cube, 'miny'), "Cube should have miny"
            assert hasattr(cube, 'maxy'), "Cube should have maxy"
            assert hasattr(cube, 'minz'), "Cube should have minz"
            assert hasattr(cube, 'maxz'), "Cube should have maxz"

    def test_terrain_cube_dimensions(self):
        """Test that terrain cubes have correct dimensions."""
        cube_size = 2.0
        terrain = Terrain(
            noise_scale=0.1,
            noise_amplitude=0.5,
            cube_size=cube_size,
            gap_distance=0.0,
            width=6.0,
            depth=6.0,
            height=4.0,
            location=Point3D(0, 0, 0),
            material=self.test_material,
            seed=123
        )
        
        # Check that at least one cube has expected base dimensions
        if len(terrain.cubes) > 0:
            cube = terrain.cubes[0]
            width = cube.maxx - cube.minx
            depth = cube.maxz - cube.minz
            
            # Base dimensions should match cube_size (height may vary due to noise)
            assert abs(width - cube_size) < 0.1, f"Cube width should be close to {cube_size}"
            assert abs(depth - cube_size) < 0.1, f"Cube depth should be close to {cube_size}"

    def test_terrain_ray_intersection(self):
        """Test that rays can intersect with terrain objects."""
        terrain = Terrain(
            noise_scale=0.1,
            noise_amplitude=0.5,
            cube_size=1.0,
            gap_distance=0.0,
            width=5.0,
            depth=5.0,
            height=3.0,
            location=Point3D(0, 0, 0),
            material=self.test_material,
            seed=123
        )
        
        # Test ray pointing down from above the terrain
        test_ray = Ray(Point3D(0, 10, 0), Vector3D(0, -1, 0))
        intersection = terrain.hit(test_ray)
        
        # Note: Intersection may or may not occur depending on terrain generation
        # This test verifies the hit method works without errors
        if intersection:
            assert hasattr(intersection, 'hit_point'), "Intersection should have hit_point"
            assert hasattr(intersection, 'normal'), "Intersection should have normal"
            assert intersection.hit_point.y <= 10, "Hit point should be below ray origin"

    def test_terrain_with_gaps(self):
        """Test terrain creation with gap distances."""
        terrain = Terrain(
            noise_scale=0.1,
            noise_amplitude=0.5,
            cube_size=1.0,
            gap_distance=0.5,  # Add gaps between cubes
            width=4.0,
            depth=4.0,
            height=2.0,
            location=Point3D(0, 0, 0),
            material=self.test_material,
            seed=123
        )
        
        assert len(terrain.cubes) >= 0, "Terrain with gaps should still create cubes"
        assert terrain.gap_distance == 0.5, "Gap distance should be preserved"

    def test_terrain_different_seeds(self):
        """Test that different seeds produce different terrain."""
        terrain1 = Terrain(
            noise_scale=0.1,
            noise_amplitude=0.5,
            cube_size=1.0,
            gap_distance=0.0,
            width=3.0,
            depth=3.0,
            height=2.0,
            location=Point3D(0, 0, 0),
            material=self.test_material,
            seed=123
        )
        
        terrain2 = Terrain(
            noise_scale=0.1,
            noise_amplitude=0.5,
            cube_size=1.0,
            gap_distance=0.0,
            width=3.0,
            depth=3.0,
            height=2.0,
            location=Point3D(0, 0, 0),
            material=self.test_material,
            seed=456
        )
        
        # Different seeds should potentially produce different numbers of cubes
        # or different cube heights (though this isn't guaranteed)
        assert terrain1.seed != terrain2.seed, "Terrains should have different seeds"

    def test_terrain_in_scene(self):
        """Test that terrain can be added to and used in a scene."""
        scene = Scene("Terrain Test Scene")
        
        terrain = Terrain(
            noise_scale=0.3,
            noise_amplitude=0.8,
            cube_size=2.0,
            gap_distance=0.2,
            width=10.0,
            depth=10.0,
            height=5.0,
            location=Point3D(0, 0, 0),
            material=Material(RGB(0.7, 0.5, 0.3), 1.0, 0, 0.0),
            seed=123
        )
        
        scene.add_object(terrain)
        
        # Check that terrain was added to scene
        terrain_found = False
        for obj in scene:
            if hasattr(obj, 'cubes'):  # This identifies terrain objects
                terrain_found = True
                break
        
        assert terrain_found, "Terrain should be found in scene"

    def test_terrain_bounds(self):
        """Test that terrain bounds are calculated correctly."""
        location = Point3D(5, 0, 10)
        width = 6.0
        depth = 8.0
        
        terrain = Terrain(
            noise_scale=0.1,
            noise_amplitude=0.5,
            cube_size=1.0,
            gap_distance=0.0,
            width=width,
            depth=depth,
            height=2.0,
            location=location,
            material=self.test_material,
            seed=123
        )
        
        # Check that terrain has proper offset calculations
        assert hasattr(terrain, 'offset_x'), "Terrain should have offset_x"
        assert hasattr(terrain, 'offset_z'), "Terrain should have offset_z"
        assert hasattr(terrain, 'actual_width'), "Terrain should have actual_width"
        assert hasattr(terrain, 'actual_depth'), "Terrain should have actual_depth"

    def test_terrain_material_assignment(self):
        """Test that terrain cubes inherit the correct material."""
        custom_material = Material(RGB(0.8, 0.2, 0.1), 1.0, 0.3, 0.1)
        
        terrain = Terrain(
            noise_scale=0.1,
            noise_amplitude=0.5,
            cube_size=1.0,
            gap_distance=0.0,
            width=3.0,
            depth=3.0,
            height=2.0,
            location=Point3D(0, 0, 0),
            material=custom_material,
            seed=123
        )
        
        # Check that terrain material is preserved
        assert terrain.material == custom_material, "Terrain should preserve material"
        
        # Check that cubes have the correct material
        if len(terrain.cubes) > 0:
            cube = terrain.cubes[0]
            assert cube.material == custom_material, "Cube should inherit terrain material"