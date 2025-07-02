import pytest
import json
import tempfile
import os
from Scene import Scene
from Primitives import Sphere, Plane, Cube
from Material import Material
from RGB import RGB
from Point import Point3D
from Vector import Vector3D


class TestScene:
    """Comprehensive tests for the Scene class."""

    def test_init_default(self):
        """Test Scene initialization with default values."""
        scene = Scene()
        assert scene.name == "Untitled Scene"
        assert scene.objects == []
        assert scene.camera_position == Point3D(0, 0, 150)
        assert scene.camera_direction == Vector3D(0, 0, -1).normalize()
        assert scene.field_of_view == 90.0
        assert scene.background_color == RGB(0, 0, 0)
        assert scene.ambient_intensity == 0.0
        assert scene.ambient_color == RGB(1.0, 1.0, 1.0)

    def test_init_with_name(self):
        """Test Scene initialization with custom name."""
        scene = Scene(name="Test Scene")
        assert scene.name == "Test Scene"
        assert scene.objects == []

    def test_init_with_objects(self):
        """Test Scene initialization with objects list."""
        sphere = Sphere(center=Point3D(0, 0, 0), radius=1)
        plane = Plane(Point3D(0, 0, 0))
        objects = [sphere, plane]
        scene = Scene(objects=objects)
        assert scene.objects == objects
        assert len(scene.objects) == 2

    def test_init_with_camera_parameters(self):
        """Test Scene initialization with custom camera parameters."""
        camera_pos = Point3D(10, 20, 30)
        camera_dir = Vector3D(1, 0, 0)
        fov = 60.0

        scene = Scene(
            camera_position=camera_pos,
            camera_direction=camera_dir,
            field_of_view=fov
        )

        assert scene.camera_position == camera_pos
        assert scene.camera_direction == camera_dir.normalize()
        assert scene.field_of_view == fov

    def test_init_with_rendering_parameters(self):
        """Test Scene initialization with custom rendering parameters."""
        bg_color = RGB(0.2, 0.3, 0.4)
        ambient_intensity = 0.3
        ambient_color = RGB(0.8, 0.9, 1.0)

        scene = Scene(
            background_color=bg_color,
            ambient_intensity=ambient_intensity,
            ambient_color=ambient_color
        )

        assert scene.background_color == bg_color
        assert scene.ambient_intensity == ambient_intensity
        assert scene.ambient_color == ambient_color

    def test_init_with_all_parameters(self):
        """Test Scene initialization with all parameters."""
        sphere = Sphere(center=Point3D(0, 0, 0), radius=1)
        objects = [sphere]

        scene = Scene(
            name="Complete Scene",
            objects=objects,
            camera_position=Point3D(5, 10, 15),
            camera_direction=Vector3D(0, 0, -1),
            field_of_view=45.0,
            background_color=RGB(0.1, 0.2, 0.3),
            ambient_intensity=0.2,
            ambient_color=RGB(0.9, 0.8, 0.7)
        )

        assert scene.name == "Complete Scene"
        assert scene.objects == objects
        assert scene.camera_position == Point3D(5, 10, 15)
        assert scene.field_of_view == 45.0
        assert scene.ambient_intensity == 0.2
        assert scene.ambient_color == RGB(0.9, 0.8, 0.7)

    def test_add_object(self):
        """Test adding objects to the scene."""
        scene = Scene()
        sphere = Sphere(center=Point3D(0, 0, 0), radius=1)

        scene.add_object(sphere)
        assert len(scene.objects) == 1
        assert scene.objects[0] == sphere

    def test_add_multiple_objects(self):
        """Test adding multiple objects to the scene."""
        scene = Scene()
        sphere = Sphere(center=Point3D(0, 0, 0), radius=1)
        plane = Plane(Point3D(0, 0, 0))
        cube = Cube()

        scene.add_object(sphere)
        scene.add_object(plane)
        scene.add_object(cube)

        assert len(scene.objects) == 3
        assert sphere in scene.objects
        assert plane in scene.objects
        assert cube in scene.objects

    def test_remove_object_valid_index(self):
        """Test removing object by valid index."""
        scene = Scene()
        sphere = Sphere(center=Point3D(0, 0, 0), radius=1)
        plane = Plane(Point3D(0, 0, 0))

        scene.add_object(sphere)
        scene.add_object(plane)

        scene.remove_object(0)
        assert len(scene.objects) == 1
        assert scene.objects[0] == plane

    def test_remove_object_invalid_index(self):
        """Test removing object by invalid index."""
        scene = Scene()
        sphere = Sphere(center=Point3D(0, 0, 0), radius=1)
        scene.add_object(sphere)

        # Try to remove with invalid indices
        scene.remove_object(-1)  # Should not crash
        scene.remove_object(5)   # Should not crash

        # Object should still be there
        assert len(scene.objects) == 1
        assert scene.objects[0] == sphere

    def test_remove_object_empty_scene(self):
        """Test removing object from empty scene."""
        scene = Scene()
        scene.remove_object(0)  # Should not crash
        assert len(scene.objects) == 0

    def test_clear(self):
        """Test clearing all objects from the scene."""
        scene = Scene()
        sphere = Sphere(center=Point3D(0, 0, 0), radius=1)
        plane = Plane(Point3D(0, 0, 0))
        cube = Cube()

        scene.add_object(sphere)
        scene.add_object(plane)
        scene.add_object(cube)

        scene.clear()
        assert len(scene.objects) == 0

    def test_clear_empty_scene(self):
        """Test clearing empty scene."""
        scene = Scene()
        scene.clear()  # Should not crash
        assert len(scene.objects) == 0

    def test_len(self):
        """Test __len__ method."""
        scene = Scene()
        assert len(scene) == 0

        scene.add_object(Sphere(center=Point3D(0, 0, 0), radius=1))
        assert len(scene) == 1

        scene.add_object(Plane(Point3D(0, 0, 0)))
        assert len(scene) == 2

    def test_getitem(self):
        """Test __getitem__ method."""
        scene = Scene()
        sphere = Sphere(center=Point3D(0, 0, 0), radius=1)
        plane = Plane(Point3D(0, 0, 0))

        scene.add_object(sphere)
        scene.add_object(plane)

        assert scene[0] == sphere
        assert scene[1] == plane

    def test_getitem_invalid_index(self):
        """Test __getitem__ with invalid index."""
        scene = Scene()
        sphere = Sphere(center=Point3D(0, 0, 0), radius=1)
        scene.add_object(sphere)

        with pytest.raises(IndexError):
            _ = scene[5]

    def test_iter(self):
        """Test __iter__ method."""
        scene = Scene()
        sphere = Sphere(center=Point3D(0, 0, 0), radius=1)
        plane = Plane(Point3D(0, 0, 0))
        cube = Cube()

        scene.add_object(sphere)
        scene.add_object(plane)
        scene.add_object(cube)

        objects = list(scene)
        assert len(objects) == 3
        assert sphere in objects
        assert plane in objects
        assert cube in objects

    def test_iter_empty_scene(self):
        """Test iteration over empty scene."""
        scene = Scene()
        objects = list(scene)
        assert objects == []

    def test_to_json(self):
        """Test JSON serialization."""
        sphere = Sphere(center=Point3D(1, 2, 3), radius=5)
        scene = Scene(
            name="Test Scene",
            objects=[sphere],
            camera_position=Point3D(0, -10, 5),
            camera_direction=Vector3D(0, 1, 0),
            field_of_view=60.0,
            background_color=RGB(0.1, 0.2, 0.3),
            ambient_intensity=0.4,
            ambient_color=RGB(0.8, 0.7, 0.6)
        )

        json_data = scene.to_json()

        assert json_data["name"] == "Test Scene"
        assert len(json_data["objects"]) == 1
        assert json_data["field_of_view"] == 60.0
        assert json_data["ambient_intensity"] == 0.4
        assert "camera_position" in json_data
        assert "camera_direction" in json_data
        assert "background_color" in json_data
        assert "ambient_color" in json_data

    def test_to_json_empty_scene(self):
        """Test JSON serialization of empty scene."""
        scene = Scene(name="Empty Scene")
        json_data = scene.to_json()

        assert json_data["name"] == "Empty Scene"
        assert json_data["objects"] == []

    def test_from_json_basic(self):
        """Test JSON deserialization with basic data."""
        json_data = {
            "name": "Imported Scene",
            "objects": [],
            "camera_position": {"x": 5, "y": 10, "z": 15},
            "camera_direction": {"x": 0, "y": 0, "z": -1},
            "field_of_view": 45.0,
            "background_color": {"r": 0.2, "g": 0.3, "b": 0.4},
            "ambient_intensity": 0.3,
            "ambient_color": {"r": 0.9, "g": 0.8, "b": 0.7}
        }

        scene = Scene.from_json(json_data)

        assert scene.name == "Imported Scene"
        assert len(scene.objects) == 0
        assert scene.camera_position == Point3D(5, 10, 15)
        assert scene.field_of_view == 45.0
        assert scene.background_color == RGB(0.2, 0.3, 0.4)
        assert scene.ambient_intensity == 0.3
        assert scene.ambient_color == RGB(0.9, 0.8, 0.7)

    def test_from_json_with_objects(self):
        """Test JSON deserialization with objects."""
        json_data = {
            "name": "Scene with Objects",
            "objects": [
                {
                    "type": "sphere",
                    "center": {"x": 0, "y": 0, "z": 0},
                    "radius": 5,
                    "material": {
                        "color": {"r": 1, "g": 0, "b": 0},
                        "opacity": 1.0,
                        "reflect": 0.0,
                        "luma": 0.0,
                        "roughness": {"scale": 0.1, "amplitude": 0.0}
                    }
                },
                {
                    "type": "plane",
                    "center": {"x": 0, "y": -5, "z": 0},
                    "normal": {"x": 0, "y": 1, "z": 0},
                    "material": {
                        "color": {"r": 0, "g": 1, "b": 0},
                        "opacity": 1.0,
                        "reflect": 0.0,
                        "luma": 0.0,
                        "roughness": {"scale": 0.1, "amplitude": 0.0}
                    }
                }
            ],
            "camera_position": {"x": 0, "y": 0, "z": 0},
            "camera_direction": {"x": 0, "y": 0, "z": -1},
            "field_of_view": 90.0,
            "background_color": {"r": 0, "g": 0, "b": 0},
            "ambient_intensity": 0.0,
            "ambient_color": {"r": 1.0, "g": 1.0, "b": 1.0}
        }

        scene = Scene.from_json(json_data)

        assert scene.name == "Scene with Objects"
        assert len(scene.objects) == 2
        assert isinstance(scene.objects[0], Sphere)
        assert isinstance(scene.objects[1], Plane)

    def test_from_json_partial_data(self):
        """Test JSON deserialization with partial data (using defaults)."""
        json_data = {
            "name": "Partial Scene"
        }

        scene = Scene.from_json(json_data)

        assert scene.name == "Partial Scene"
        assert len(scene.objects) == 0
        # Should use default values for missing fields
        assert scene.field_of_view == 90.0
        assert scene.ambient_intensity == 0.0
        assert scene.ambient_color == RGB(1.0, 1.0, 1.0)

    def test_from_json_unknown_object_type(self):
        """Test JSON deserialization with unknown object type."""
        json_data = {
            "name": "Scene with Unknown Object",
            "objects": [
                {
                    "type": "unknown_primitive",
                    "some_property": "some_value"
                },
                {
                    "type": "sphere",
                    "center": {"x": 0, "y": 0, "z": 0},
                    "radius": 3,
                    "material": {
                        "color": {"r": 1, "g": 1, "b": 1},
                        "opacity": 1.0,
                        "reflect": 0.0,
                        "luma": 0.0,
                        "roughness": {"scale": 0.1, "amplitude": 0.0}
                    }
                }
            ]
        }

        scene = Scene.from_json(json_data)

        # Should skip unknown object type and only load the sphere
        assert len(scene.objects) == 1
        assert isinstance(scene.objects[0], Sphere)

    def test_json_roundtrip(self):
        """Test JSON serialization and deserialization roundtrip."""
        sphere = Sphere(center=Point3D(1, 2, 3), radius=4)
        plane = Plane(Point3D(0, -5, 0))

        original = Scene(
            name="Roundtrip Test",
            objects=[sphere, plane],
            camera_position=Point3D(10, 20, 30),
            camera_direction=Vector3D(0, 0, -1),
            field_of_view=75.0,
            background_color=RGB(0.5, 0.6, 0.7),
            ambient_intensity=0.25,
            ambient_color=RGB(0.9, 0.8, 0.7)
        )

        json_data = original.to_json()
        restored = Scene.from_json(json_data)

        assert original.name == restored.name
        assert len(original.objects) == len(restored.objects)
        assert original.camera_position == restored.camera_position
        assert original.field_of_view == restored.field_of_view
        assert original.background_color == restored.background_color
        assert original.ambient_intensity == restored.ambient_intensity
        assert original.ambient_color == restored.ambient_color

    def test_export_to_json_file(self):
        """Test exporting scene to JSON file."""
        scene = Scene(name="File Export Test")
        sphere = Sphere(center=Point3D(0, 0, 0), radius=1)
        scene.add_object(sphere)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            filepath = f.name

        try:
            scene.export_to_json(filepath)

            # Verify file was created and contains valid JSON
            assert os.path.exists(filepath)

            with open(filepath, 'r') as f:
                loaded_data = json.load(f)

            assert loaded_data["name"] == "File Export Test"
            assert len(loaded_data["objects"]) == 1

        finally:
            # Clean up
            if os.path.exists(filepath):
                os.unlink(filepath)

    def test_import_from_json_file(self):
        """Test importing scene from JSON file."""
        # Create test data
        test_data = {
            "name": "File Import Test",
            "objects": [
                {
                    "type": "sphere",
                    "center": {"x": 0, "y": 0, "z": 0},
                    "radius": 2,
                    "material": {
                        "color": {"r": 0.5, "g": 0.5, "b": 0.5},
                        "opacity": 1.0,
                        "reflect": 0.0,
                        "luma": 0.0,
                        "roughness": {"scale": 0.1, "amplitude": 0.0}
                    }
                }
            ],
            "camera_position": {"x": 0, "y": -10, "z": 0},
            "camera_direction": {"x": 0, "y": 1, "z": 0},
            "field_of_view": 60.0,
            "background_color": {"r": 0.1, "g": 0.1, "b": 0.1},
            "ambient_intensity": 0.1,
            "ambient_color": {"r": 0.9, "g": 0.9, "b": 0.9}
        }

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(test_data, f)
            filepath = f.name

        try:
            scene = Scene.import_from_json(filepath)

            assert scene.name == "File Import Test"
            assert len(scene.objects) == 1
            assert isinstance(scene.objects[0], Sphere)
            assert scene.field_of_view == 60.0

        finally:
            # Clean up
            if os.path.exists(filepath):
                os.unlink(filepath)

    def test_repr(self):
        """Test string representation."""
        scene = Scene(name="Test Scene")
        sphere = Sphere(center=Point3D(0, 0, 0), radius=1)
        plane = Plane(Point3D(0, 0, 0))
        scene.add_object(sphere)
        scene.add_object(plane)

        repr_str = repr(scene)
        assert "Scene" in repr_str
        assert "Test Scene" in repr_str
        assert "2" in repr_str  # Number of objects

    def test_repr_empty_scene(self):
        """Test string representation of empty scene."""
        scene = Scene(name="Empty")
        repr_str = repr(scene)
        assert "Scene" in repr_str
        assert "Empty" in repr_str
        assert "0" in repr_str

    def test_scene_with_different_primitive_types(self):
        """Test scene with all different primitive types."""
        scene = Scene(name="All Primitives")

        sphere = Sphere(center=Point3D(0, 0, 0), radius=2)
        plane = Plane(Point3D(0, -5, 0))
        cube = Cube(a=Point3D(-1, -1, -1), b=Point3D(1, 1, 1))

        scene.add_object(sphere)
        scene.add_object(plane)
        scene.add_object(cube)

        assert len(scene) == 3
        assert isinstance(scene[0], Sphere)
        assert isinstance(scene[1], Plane)
        assert isinstance(scene[2], Cube)

    def test_scene_camera_direction_normalization(self):
        """Test that camera direction is automatically normalized."""
        scene = Scene(camera_direction=Vector3D(3, 4, 0))  # Length = 5

        # Should be normalized to length 1.0
        assert abs(scene.camera_direction.length - 1.0) < 0.001

    def test_edge_case_none_objects_list(self):
        """Test scene initialization with None objects list."""
        scene = Scene(objects=None)
        assert scene.objects == []

    def test_edge_case_none_camera_parameters(self):
        """Test scene initialization with None camera parameters."""
        scene = Scene(
            camera_position=None,
            camera_direction=None,
            background_color=None,
            ambient_color=None
        )

        # Should use defaults
        assert scene.camera_position == Point3D(0, 0, 150)
        assert scene.camera_direction == Vector3D(0, 0, -1).normalize()
        assert scene.background_color == RGB(0, 0, 0)
        assert scene.ambient_color == RGB(1.0, 1.0, 1.0)

    def test_scene_modification_after_creation(self):
        """Test modifying scene properties after creation."""
        scene = Scene()

        # Modify properties
        scene.name = "Modified Scene"
        scene.field_of_view = 120.0
        scene.background_color = RGB(1, 1, 1)

        assert scene.name == "Modified Scene"
        assert scene.field_of_view == 120.0
        assert scene.background_color == RGB(1, 1, 1)
