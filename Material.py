from RGB import RGB
from typing import Dict, Any
from JsonSerializable import JsonSerializable


class Material(JsonSerializable):
    """Material properties for raytracing objects."""

    def __init__(self, color=None, opacity=1.0, reflect=0.0, luma=0.0, roughness=(0.0, 0.0)):
        """
        Initialize a material with specified properties.

        Args:
            color: RGB color of the material (defaults to dark gray)
            opacity: Transparency level (1.0 = opaque, 0.0 = transparent)
            reflect: Reflectivity (0.0 = no reflection, 1.0 = perfect mirror)
            luma: Emissive property (0.0 = not emissive, 1.0 = fully emissive)
            roughness: Surface roughness as a tuple of (scale, amplitude)
                       scale: Controls the granularity of the roughness pattern (default: 0.0)
                       amplitude: Controls the strength of the roughness effect (0.0 = smooth, 1.0 = very rough)
        """
        self.color = color if color else RGB(0.1, 0.1, 0.1)
        self.opacity = self._clamp(opacity)
        self.reflect = self._clamp(reflect)
        self.luma = self._clamp(luma)

        # Handle roughness as a tuple of (scale, amplitude)
        if isinstance(roughness, tuple) and len(roughness) == 2:
            self.roughness = (roughness[0], self._clamp(roughness[1]))
        else:
            # For backward compatibility, convert single value to tuple
            self.roughness = (0.1, self._clamp(roughness) if isinstance(roughness, (int, float)) else 0.0)

    @staticmethod
    def _clamp(value):
        """Clamp value between 0.0 and 1.0"""
        return max(0.0, min(1.0, value))

    def to_json(self) -> Dict[str, Any]:
        """Convert material to JSON-serializable dictionary."""
        return {
            "color": self.color.to_json(),
            "opacity": self.opacity,
            "reflect": self.reflect,
            "luma": self.luma,
            "roughness": {
                "scale": self.roughness[0],
                "amplitude": self.roughness[1]
            }
        }

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> 'Material':
        """Create a Material instance from JSON data."""
        # Handle roughness data which can be in different formats
        roughness_data = data.get("roughness", {})
        if isinstance(roughness_data, dict):
            # New format with scale and amplitude
            roughness = (
                roughness_data.get("scale", 0.1),
                roughness_data.get("amplitude", 0.0)
            )
        else:
            # Legacy format with single value
            roughness = (0.1, float(roughness_data) if roughness_data else 0.0)

        return cls(
            color=RGB.from_json(data.get("color", {})),
            opacity=data.get("opacity", 1.0),
            reflect=data.get("reflect", 0.0),
            luma=data.get("luma", 0.0),
            roughness=roughness
        )

    def __repr__(self):
        return f"Material(color={self.color}, opacity={self.opacity}, reflect={self.reflect}, luma={self.luma}, roughness={self.roughness})"
