from typing import Protocol, Dict, Any, TypeVar, Type, runtime_checkable

T = TypeVar('T', bound='JsonSerializable')

@runtime_checkable
class JsonSerializable(Protocol):
    """Protocol for objects that can be serialized to and from JSON."""

    def to_json(self) -> Dict[str, Any]:
        """Convert object to a JSON-serializable dictionary."""
        ...

    @classmethod
    def from_json(cls: Type[T], data: Dict[str, Any]) -> T:
        """Create an instance from JSON data."""
        ...
