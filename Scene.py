import json
from typing import List, Dict, Any, Optional, Type, cast

from JsonSerializable import JsonSerializable
from Material import Material
from Point import Point3D
from RGB import RGB
from Vector import Vector3D
from Primitives import Sphere, Plane, Cube
# Import Terrain inside methods to avoid circular imports


class Scene(JsonSerializable):
    """A scene containing 3D objects for ray tracing with JSON import/export capability."""

    def __init__(self, name: str = "Untitled Scene", objects: Optional[List] = None):
        """Initialize a scene with a name and optional list of objects."""
        self.name = name
        self.objects = objects if objects else []

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
        return {
            "name": self.name,
            "objects": [obj.to_json() for obj in self.objects if isinstance(obj, JsonSerializable)]
        }

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> 'Scene':
        """Create a Scene instance from JSON data."""
        name = data.get("name", "Imported Scene")
        scene = cls(name=name)

        # Import Terrain here to avoid circular imports
        from Terrain import Terrain

        # Mapping of object types to their classes
        object_types = {
            "sphere": Sphere,
            "plane": Plane,
            "cube": Cube,
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
