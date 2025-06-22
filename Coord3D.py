from typing import Dict, Any, TypeVar, Type
from JsonSerializable import JsonSerializable

T = TypeVar('T', bound='Coord3D')

class Coord3D(JsonSerializable):
    """Base class for 3D coordinates (points, vectors, normals)."""
    
    x: float
    y: float
    z: float
    
    def to_json(self) -> Dict[str, float]:
        """Convert 3D coordinate to JSON-serializable dictionary."""
        return {
            "x": self.x,
            "y": self.y,
            "z": self.z
        }
    
    @classmethod
    def from_json(cls: Type[T], data: Dict[str, Any]) -> T:
        """Create a 3D coordinate instance from JSON data."""
        return cls(
            x=data.get("x", 0.0),
            y=data.get("y", 0.0),
            z=data.get("z", 0.0)
        )