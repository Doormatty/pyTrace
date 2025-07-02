import pytest
from Material import Material
from RGB import RGB


class TestMaterial:
    """Comprehensive tests for the Material class."""

    def test_init_default(self):
        """Test Material initialization with default values."""
        material = Material()
        assert material.color == RGB(0.1, 0.1, 0.1)
        assert material.opacity == 1.0
        assert material.reflect == 0.0
        assert material.luma == 0.0
        assert material.roughness == (0.0, 0.0)

    def test_init_with_color(self):
        """Test Material initialization with custom color."""
        color = RGB(0.5, 0.7, 0.9)
        material = Material(color=color)
        assert material.color == color
        assert material.opacity == 1.0
        assert material.reflect == 0.0
        assert material.luma == 0.0
        assert material.roughness == (0.0, 0.0)

    def test_init_with_all_parameters(self):
        """Test Material initialization with all parameters."""
        color = RGB(0.8, 0.6, 0.4)
        material = Material(
            color=color,
            opacity=0.7,
            reflect=0.3,
            luma=0.2,
            roughness=(0.5, 0.8)
        )
        assert material.color == color
        assert material.opacity == 0.7
        assert material.reflect == 0.3
        assert material.luma == 0.2
        assert material.roughness == (0.5, 0.8)

    def test_init_opacity_clamping_high(self):
        """Test Material initialization clamps opacity above 1.0."""
        material = Material(opacity=1.5)
        assert material.opacity == 1.0

    def test_init_opacity_clamping_low(self):
        """Test Material initialization clamps opacity below 0.0."""
        material = Material(opacity=-0.5)
        assert material.opacity == 0.0

    def test_init_reflect_clamping_high(self):
        """Test Material initialization clamps reflect above 1.0."""
        material = Material(reflect=2.0)
        assert material.reflect == 1.0

    def test_init_reflect_clamping_low(self):
        """Test Material initialization clamps reflect below 0.0."""
        material = Material(reflect=-0.3)
        assert material.reflect == 0.0

    def test_init_luma_clamping_high(self):
        """Test Material initialization clamps luma above 1.0."""
        material = Material(luma=1.8)
        assert material.luma == 1.0

    def test_init_luma_clamping_low(self):
        """Test Material initialization clamps luma below 0.0."""
        material = Material(luma=-0.2)
        assert material.luma == 0.0

    def test_init_roughness_tuple(self):
        """Test Material initialization with roughness tuple."""
        material = Material(roughness=(0.3, 0.7))
        assert material.roughness == (0.3, 0.7)

    def test_init_roughness_tuple_amplitude_clamping_high(self):
        """Test Material initialization clamps roughness amplitude above 1.0."""
        material = Material(roughness=(0.2, 1.5))
        assert material.roughness == (0.2, 1.0)

    def test_init_roughness_tuple_amplitude_clamping_low(self):
        """Test Material initialization clamps roughness amplitude below 0.0."""
        material = Material(roughness=(0.2, -0.3))
        assert material.roughness == (0.2, 0.0)

    def test_init_roughness_single_value(self):
        """Test Material initialization with single roughness value (backward compatibility)."""
        material = Material(roughness=0.5)
        assert material.roughness == (0.1, 0.5)

    def test_init_roughness_single_value_clamping_high(self):
        """Test Material initialization clamps single roughness value above 1.0."""
        material = Material(roughness=1.8)
        assert material.roughness == (0.1, 1.0)

    def test_init_roughness_single_value_clamping_low(self):
        """Test Material initialization clamps single roughness value below 0.0."""
        material = Material(roughness=-0.4)
        assert material.roughness == (0.1, 0.0)

    def test_init_roughness_invalid_type(self):
        """Test Material initialization with invalid roughness type."""
        material = Material(roughness="invalid")
        assert material.roughness == (0.1, 0.0)

    def test_init_roughness_incomplete_tuple(self):
        """Test Material initialization with incomplete roughness tuple."""
        material = Material(roughness=(0.3,))
        assert material.roughness == (0.1, 0.0)

    def test_clamp_method(self):
        """Test the _clamp static method."""
        assert Material._clamp(0.5) == 0.5
        assert Material._clamp(1.5) == 1.0
        assert Material._clamp(-0.5) == 0.0
        assert Material._clamp(0.0) == 0.0
        assert Material._clamp(1.0) == 1.0

    def test_to_json_complete(self):
        """Test JSON serialization with all properties."""
        color = RGB(0.6, 0.7, 0.8)
        material = Material(
            color=color,
            opacity=0.8,
            reflect=0.4,
            luma=0.3,
            roughness=(0.2, 0.6)
        )
        json_data = material.to_json()
        expected = {
            "color": {"r": 0.6, "g": 0.7, "b": 0.8},
            "opacity": 0.8,
            "reflect": 0.4,
            "luma": 0.3,
            "roughness": {
                "scale": 0.2,
                "amplitude": 0.6
            }
        }
        assert json_data == expected

    def test_to_json_default_values(self):
        """Test JSON serialization with default values."""
        material = Material()
        json_data = material.to_json()
        expected = {
            "color": {"r": 0.1, "g": 0.1, "b": 0.1},
            "opacity": 1.0,
            "reflect": 0.0,
            "luma": 0.0,
            "roughness": {
                "scale": 0.0,
                "amplitude": 0.0
            }
        }
        assert json_data == expected

    def test_from_json_complete_data(self):
        """Test JSON deserialization with complete data."""
        json_data = {
            "color": {"r": 0.5, "g": 0.6, "b": 0.7},
            "opacity": 0.9,
            "reflect": 0.2,
            "luma": 0.1,
            "roughness": {
                "scale": 0.3,
                "amplitude": 0.4
            }
        }
        material = Material.from_json(json_data)
        assert material.color == RGB(0.5, 0.6, 0.7)
        assert material.opacity == 0.9
        assert material.reflect == 0.2
        assert material.luma == 0.1
        assert material.roughness == (0.3, 0.4)

    def test_from_json_partial_data(self):
        """Test JSON deserialization with partial data."""
        json_data = {
            "color": {"r": 0.8, "g": 0.2, "b": 0.4},
            "opacity": 0.5
        }
        material = Material.from_json(json_data)
        assert material.color == RGB(0.8, 0.2, 0.4)
        assert material.opacity == 0.5
        assert material.reflect == 0.0  # Default
        assert material.luma == 0.0  # Default
        assert material.roughness == (0.1, 0.0)  # Default

    def test_from_json_empty_data(self):
        """Test JSON deserialization with empty data."""
        json_data = {}
        material = Material.from_json(json_data)
        assert material.color == RGB(0.1, 0.1, 0.1)  # Default from RGB.from_json
        assert material.opacity == 1.0
        assert material.reflect == 0.0
        assert material.luma == 0.0
        assert material.roughness == (0.1, 0.0)

    def test_from_json_legacy_roughness_format(self):
        """Test JSON deserialization with legacy roughness format."""
        json_data = {
            "color": {"r": 0.3, "g": 0.4, "b": 0.5},
            "roughness": 0.7
        }
        material = Material.from_json(json_data)
        assert material.color == RGB(0.3, 0.4, 0.5)
        assert material.roughness == (0.1, 0.7)

    def test_from_json_legacy_roughness_zero(self):
        """Test JSON deserialization with legacy roughness format (zero value)."""
        json_data = {
            "roughness": 0
        }
        material = Material.from_json(json_data)
        assert material.roughness == (0.1, 0.0)

    def test_from_json_missing_roughness(self):
        """Test JSON deserialization with missing roughness data."""
        json_data = {
            "color": {"r": 0.1, "g": 0.2, "b": 0.3}
        }
        material = Material.from_json(json_data)
        assert material.roughness == (0.1, 0.0)

    def test_from_json_partial_roughness_data(self):
        """Test JSON deserialization with partial roughness data."""
        json_data = {
            "roughness": {
                "scale": 0.5
                # Missing amplitude
            }
        }
        material = Material.from_json(json_data)
        assert material.roughness == (0.5, 0.0)

    def test_repr(self):
        """Test string representation."""
        color = RGB(0.2, 0.4, 0.6)
        material = Material(
            color=color,
            opacity=0.8,
            reflect=0.3,
            luma=0.1,
            roughness=(0.2, 0.5)
        )
        repr_str = repr(material)
        assert "Material" in repr_str
        assert "color=" in repr_str
        assert "opacity=0.8" in repr_str
        assert "reflect=0.3" in repr_str
        assert "luma=0.1" in repr_str
        assert "roughness=(0.2, 0.5)" in repr_str

    def test_json_roundtrip(self):
        """Test JSON serialization and deserialization roundtrip."""
        original = Material(
            color=RGB(0.25, 0.75, 0.5),
            opacity=0.6,
            reflect=0.4,
            luma=0.2,
            roughness=(0.3, 0.7)
        )
        json_data = original.to_json()
        restored = Material.from_json(json_data)
        
        assert original.color == restored.color
        assert original.opacity == restored.opacity
        assert original.reflect == restored.reflect
        assert original.luma == restored.luma
        assert original.roughness == restored.roughness

    def test_material_presets(self):
        """Test creating materials with common presets."""
        # Matte material
        matte = Material(
            color=RGB(0.7, 0.7, 0.7),
            opacity=1.0,
            reflect=0.0,
            luma=0.0,
            roughness=(0.1, 0.9)
        )
        assert matte.opacity == 1.0
        assert matte.reflect == 0.0
        assert matte.roughness[1] == 0.9  # High roughness amplitude

        # Mirror material
        mirror = Material(
            color=RGB(0.9, 0.9, 0.9),
            opacity=1.0,
            reflect=1.0,
            luma=0.0,
            roughness=(0.1, 0.0)
        )
        assert mirror.reflect == 1.0
        assert mirror.roughness[1] == 0.0  # No roughness

        # Glass material
        glass = Material(
            color=RGB(0.9, 0.9, 1.0),
            opacity=0.1,
            reflect=0.8,
            luma=0.0,
            roughness=(0.1, 0.0)
        )
        assert glass.opacity == 0.1
        assert glass.reflect == 0.8

        # Emissive material
        emissive = Material(
            color=RGB(1.0, 0.8, 0.6),
            opacity=1.0,
            reflect=0.0,
            luma=1.0,
            roughness=(0.1, 0.2)
        )
        assert emissive.luma == 1.0

    def test_edge_case_extreme_values(self):
        """Test material with extreme values."""
        material = Material(
            opacity=10.0,  # Should be clamped to 1.0
            reflect=-5.0,  # Should be clamped to 0.0
            luma=2.5,      # Should be clamped to 1.0
            roughness=(100.0, -10.0)  # Amplitude should be clamped to 0.0
        )
        assert material.opacity == 1.0
        assert material.reflect == 0.0
        assert material.luma == 1.0
        assert material.roughness == (100.0, 0.0)  # Scale not clamped, amplitude clamped

    def test_edge_case_zero_values(self):
        """Test material with all zero values."""
        material = Material(
            color=RGB(0, 0, 0),
            opacity=0.0,
            reflect=0.0,
            luma=0.0,
            roughness=(0.0, 0.0)
        )
        assert material.color == RGB(0, 0, 0)
        assert material.opacity == 0.0
        assert material.reflect == 0.0
        assert material.luma == 0.0
        assert material.roughness == (0.0, 0.0)

    def test_edge_case_maximum_values(self):
        """Test material with maximum valid values."""
        material = Material(
            color=RGB(1, 1, 1),
            opacity=1.0,
            reflect=1.0,
            luma=1.0,
            roughness=(1.0, 1.0)
        )
        assert material.color == RGB(1, 1, 1)
        assert material.opacity == 1.0
        assert material.reflect == 1.0
        assert material.luma == 1.0
        assert material.roughness == (1.0, 1.0)

    def test_material_property_independence(self):
        """Test that material properties are independent."""
        material1 = Material(opacity=0.5)
        material2 = Material(reflect=0.5)
        
        # Changing one material shouldn't affect the other
        assert material1.opacity == 0.5
        assert material1.reflect == 0.0
        assert material2.opacity == 1.0
        assert material2.reflect == 0.5

    def test_color_none_handling(self):
        """Test material initialization with None color."""
        material = Material(color=None)
        assert material.color == RGB(0.1, 0.1, 0.1)

    def test_roughness_scale_not_clamped(self):
        """Test that roughness scale is not clamped (only amplitude is)."""
        material = Material(roughness=(5.0, 0.5))
        assert material.roughness == (5.0, 0.5)  # Scale can be > 1.0
        
        material2 = Material(roughness=(-2.0, 0.3))
        assert material2.roughness == (-2.0, 0.3)  # Scale can be negative

    def test_json_with_invalid_color_data(self):
        """Test JSON deserialization with invalid color data."""
        json_data = {
            "color": "invalid_color_data",
            "opacity": 0.7
        }
        material = Material.from_json(json_data)
        # Should use default color when color data is invalid
        assert material.color == RGB(0.1, 0.1, 0.1)
        assert material.opacity == 0.7