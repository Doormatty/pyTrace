import json
from typing import List, Dict, Any, Optional, Union

from JsonSerializable import JsonSerializable
from Point import Point3D
from Primitives import Sphere, Plane, Cube, Cuboid, Cylinder, Toroid
from RGB import RGB
from Vector import Vector3D
from Material import Material
from Camera import Camera


# Import Terrain inside methods to avoid circular imports


class Scene(JsonSerializable):
    """A scene containing 3D objects for ray tracing with JSON import/export capability."""

    def __init__(self, name: str = "Untitled Scene", objects: Optional[List] = None,
                 camera: Optional[Camera] = None,
                 camera_position: Optional[Point3D] = None,
                 camera_direction: Optional[Union[Vector3D, Point3D]] = None,
                 field_of_view: float = 90.0,
                 background_color: Optional[RGB] = None,
                 ambient_intensity: float = 0.0,
                 ambient_color: Optional[RGB] = None):
        """Initialize a scene with a name, objects, and camera/rendering parameters."""
        self.name = name
        self.objects = objects if objects else []

        # Camera setup - support both new Camera object and legacy parameters
        if camera is not None:
            self.camera = camera
        else:
            # Create camera from legacy parameters for backward compatibility
            position = camera_position if camera_position else Point3D(0, 0, 150)
            direction = camera_direction if camera_direction else Vector3D(0, 0, -1)
            self.camera = Camera(position, direction, field_of_view)

        self.background_color = background_color if background_color else RGB(0, 0, 0)

        # Validate and set ambient lighting parameters
        if ambient_intensity < 0:
            raise ValueError("Ambient intensity cannot be negative")
        self.ambient_intensity = ambient_intensity
        self.ambient_color = ambient_color if ambient_color else RGB(1.0, 1.0, 1.0)  # Default to white

    # Properties for backward compatibility with legacy camera parameters
    @property
    def camera_position(self) -> Point3D:
        """Get camera position for backward compatibility."""
        return self.camera.position

    @camera_position.setter
    def camera_position(self, position: Point3D) -> None:
        """Set camera position for backward compatibility."""
        self.camera.set_position(position)

    @property
    def camera_direction(self) -> Vector3D:
        """Get camera direction for backward compatibility."""
        return self.camera.direction

    @camera_direction.setter
    def camera_direction(self, direction: Vector3D) -> None:
        """Set camera direction for backward compatibility."""
        self.camera.set_direction(direction)

    @property
    def field_of_view(self) -> float:
        """Get field of view for backward compatibility."""
        return self.camera.field_of_view

    @field_of_view.setter
    def field_of_view(self, fov: float) -> None:
        """Set field of view for backward compatibility."""
        self.camera.field_of_view = fov
        # Invalidate coordinate system cache since FOV affects viewport calculations
        self.camera._coordinate_system_valid = False

    def add_object(self, obj) -> None:
        """Add an object to the scene."""
        self.objects.append(obj)

    def remove_object(self, index: int) -> None:
        """Remove an object from the scene by index."""
        if 0 <= index < len(self.objects):
            del self.objects[index]

    def clear(self) -> None:
        """Remove all objects from the scene."""
        self.objects.clear()

    def export_to_json(self, filepath: str) -> None:
        """Export the scene to a JSON file."""
        with open(filepath, 'w') as f:
            json.dump(self.to_json(), f, indent=2)

    @classmethod
    def import_from_json(cls, filepath: str) -> 'Scene':
        """Import a scene from a JSON file."""
        with open(filepath, 'r') as f:
            scene_data = json.load(f)
        return cls.from_json(scene_data)

        return scene

    def __len__(self):
        """Return the number of objects in the scene."""
        return len(self.objects)

    def __getitem__(self, index):
        """Get an object by index."""
        return self.objects[index]

    def __iter__(self):
        """Iterate through all objects in the scene."""
        return iter(self.objects)

    def to_json(self) -> Dict[str, Any]:
        """Convert scene to JSON-serializable dictionary."""
        result = {
            "name": self.name,
            "objects": [obj.to_json() for obj in self.objects if isinstance(obj, JsonSerializable)],
            "camera": self.camera.to_json(),
            # Include legacy camera parameters for backward compatibility
            "camera_position": self.camera.position.to_json(),
            "camera_direction": self.camera.direction.to_json(),
            "field_of_view": self.camera.field_of_view,
            "background_color": self.background_color.to_json(),
            "ambient_intensity": self.ambient_intensity,
            "ambient_color": self.ambient_color.to_json()
        }

        return result

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> 'Scene':
        """Create a Scene instance from JSON data."""
        name = data.get("name", "Imported Scene")

        # Handle both new Camera format and legacy format for backward compatibility
        camera = None
        if "camera" in data:
            # New format with Camera object
            camera = Camera.from_json(data["camera"])
        else:
            # Legacy format with separate camera parameters
            camera_position = Point3D.from_json(data.get("camera_position", {"x": 0, "y": 0, "z": 0}))
            camera_direction = Vector3D.from_json(data.get("camera_direction", {"x": 0, "y": 0, "z": -1}))
            field_of_view = data.get("field_of_view", 90.0)
            camera = Camera(camera_position, camera_direction, field_of_view)

        background_color = RGB.from_json(data.get("background_color", {"r": 0, "g": 0, "b": 0}))

        # Extract ambient lighting parameters
        ambient_intensity = data.get("ambient_intensity", 0.0)
        ambient_color = RGB.from_json(data.get("ambient_color", {"r": 1.0, "g": 1.0, "b": 1.0}))

        scene = cls(name=name,
                    camera=camera,
                    background_color=background_color,
                    ambient_intensity=ambient_intensity,
                    ambient_color=ambient_color)

        # Import Terrain here to avoid circular imports
        from Terrain import Terrain

        # Mapping of object types to their classes
        object_types = {
            "sphere": Sphere,
            "plane": Plane,
            "cube": Cube,
            "cuboid": Cuboid,
            "cylinder": Cylinder,
            "toroid": Toroid,
            "terrain": Terrain
        }

        for obj_data in data.get("objects", []):
            obj_type = obj_data.get("type")

            # Get the appropriate class for this object type
            if obj_type in object_types:
                object_class = object_types[obj_type]
                # Use the class's from_json method to create the object
                obj = object_class.from_json(obj_data)
                scene.add_object(obj)

        return scene

    def __repr__(self):
        return f"Scene(name='{self.name}', objects={len(self.objects)})"
