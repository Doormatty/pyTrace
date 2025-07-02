import pytest
import math
from RGB import RGB


class TestRGB:
    """Comprehensive tests for the RGB class."""

    def test_init_default(self):
        """Test RGB initialization with default values."""
        rgb = RGB()
        assert rgb.r == 0.0
        assert rgb.g == 0.0
        assert rgb.b == 0.0

    def test_init_float_values(self):
        """Test RGB initialization with float values in [0.0, 1.0] range."""
        rgb = RGB(0.5, 0.7, 0.9)
        assert rgb.r == 0.5
        assert rgb.g == 0.7
        assert rgb.b == 0.9

    def test_init_255_range_values(self):
        """Test RGB initialization with values in [0, 255] range."""
        rgb = RGB(128, 192, 255)
        assert abs(rgb.r - 128/255.0) < 0.001
        assert abs(rgb.g - 192/255.0) < 0.001
        assert abs(rgb.b - 255/255.0) < 0.001

    def test_init_mixed_values(self):
        """Test RGB initialization with mixed range values."""
        rgb = RGB(0.5, 128, 1.0)
        assert rgb.r == 0.5
        assert abs(rgb.g - 128/255.0) < 0.001
        assert rgb.b == 1.0

    def test_init_clamping_high(self):
        """Test RGB initialization converts values above 1.0 from 255 range."""
        rgb = RGB(1.5, 2.0, 10.0)
        assert abs(rgb.r - 1.5/255.0) < 0.001
        assert abs(rgb.g - 2.0/255.0) < 0.001
        assert abs(rgb.b - 10.0/255.0) < 0.001

    def test_init_clamping_low(self):
        """Test RGB initialization clamps values below 0.0."""
        rgb = RGB(-0.5, -1.0, -10.0)
        assert rgb.r == 0.0
        assert rgb.g == 0.0
        assert rgb.b == 0.0

    def test_clamp_method(self):
        """Test the _clamp static method."""
        assert RGB._clamp(0.5) == 0.5
        assert RGB._clamp(1.5) == 1.0
        assert RGB._clamp(-0.5) == 0.0
        assert RGB._clamp(0.0) == 0.0
        assert RGB._clamp(1.0) == 1.0

    def test_addition(self):
        """Test RGB addition operation."""
        rgb1 = RGB(0.3, 0.4, 0.5)
        rgb2 = RGB(0.2, 0.3, 0.1)
        result = rgb1 + rgb2
        assert result.r == 0.5
        assert result.g == 0.7
        assert result.b == 0.6

    def test_addition_with_clamping(self):
        """Test RGB addition with clamping."""
        rgb1 = RGB(0.8, 0.9, 0.7)
        rgb2 = RGB(0.5, 0.6, 0.8)
        result = rgb1 + rgb2
        assert result.r == 1.0  # Clamped
        assert result.g == 1.0  # Clamped
        assert result.b == 1.0  # Clamped

    def test_subtraction(self):
        """Test RGB subtraction operation."""
        rgb1 = RGB(0.8, 0.7, 0.6)
        rgb2 = RGB(0.3, 0.2, 0.1)
        result = rgb1 - rgb2
        assert result.r == 0.5
        assert result.g == 0.5
        assert result.b == 0.5

    def test_subtraction_with_clamping(self):
        """Test RGB subtraction with clamping."""
        rgb1 = RGB(0.2, 0.1, 0.3)
        rgb2 = RGB(0.5, 0.4, 0.8)
        result = rgb1 - rgb2
        assert result.r == 0.0  # Clamped
        assert result.g == 0.0  # Clamped
        assert result.b == 0.0  # Clamped

    def test_multiplication_scalar(self):
        """Test RGB multiplication by scalar."""
        rgb = RGB(0.4, 0.6, 0.8)
        result = rgb * 2
        assert result.r == 0.8
        assert result.g == 1.0  # Clamped
        assert result.b == 1.0  # Clamped

    def test_right_multiplication_scalar(self):
        """Test RGB right multiplication by scalar."""
        rgb = RGB(0.4, 0.6, 0.8)
        result = 2 * rgb
        assert result.r == 0.8
        assert result.g == 1.0  # Clamped
        assert result.b == 1.0  # Clamped

    def test_multiplication_zero(self):
        """Test RGB multiplication by zero."""
        rgb = RGB(0.5, 0.7, 0.9)
        result = rgb * 0
        assert result.r == 0.0
        assert result.g == 0.0
        assert result.b == 0.0

    def test_multiplication_negative(self):
        """Test RGB multiplication by negative scalar."""
        rgb = RGB(0.5, 0.7, 0.9)
        result = rgb * -1
        assert result.r == 0.0  # Clamped
        assert result.g == 0.0  # Clamped
        assert result.b == 0.0  # Clamped

    def test_equality_same_values(self):
        """Test RGB equality with same values."""
        rgb1 = RGB(0.5, 0.6, 0.7)
        rgb2 = RGB(0.5, 0.6, 0.7)
        assert rgb1 == rgb2

    def test_equality_different_values(self):
        """Test RGB inequality with different values."""
        rgb1 = RGB(0.5, 0.6, 0.7)
        rgb2 = RGB(0.5, 0.6, 0.8)
        assert rgb1 != rgb2

    def test_equality_epsilon_tolerance(self):
        """Test RGB equality with epsilon tolerance."""
        rgb1 = RGB(0.5, 0.6, 0.7)
        rgb2 = RGB(0.500001, 0.600001, 0.700001)
        assert rgb1 == rgb2  # Should be equal within epsilon

    def test_equality_beyond_epsilon(self):
        """Test RGB inequality beyond epsilon tolerance."""
        rgb1 = RGB(0.5, 0.6, 0.7)
        rgb2 = RGB(0.51, 0.6, 0.7)
        assert rgb1 != rgb2  # Should not be equal beyond epsilon

    def test_equality_with_non_rgb(self):
        """Test RGB equality with non-RGB object."""
        rgb = RGB(0.5, 0.6, 0.7)
        assert rgb != "not an RGB"
        assert rgb != 42
        assert rgb != None

    def test_finalcolor_conversion(self):
        """Test finalcolor method for pygame color format."""
        rgb = RGB(0.0, 0.5, 1.0)
        result = rgb.finalcolor()
        assert result == (0, 127, 255)

    def test_finalcolor_edge_cases(self):
        """Test finalcolor method with edge cases."""
        rgb_black = RGB(0.0, 0.0, 0.0)
        assert rgb_black.finalcolor() == (0, 0, 0)

        rgb_white = RGB(1.0, 1.0, 1.0)
        assert rgb_white.finalcolor() == (255, 255, 255)

    def test_to_json(self):
        """Test JSON serialization."""
        rgb = RGB(0.3, 0.6, 0.9)
        json_data = rgb.to_json()
        expected = {"r": 0.3, "g": 0.6, "b": 0.9}
        assert json_data == expected

    def test_from_json_complete_data(self):
        """Test JSON deserialization with complete data."""
        json_data = {"r": 0.4, "g": 0.7, "b": 0.2}
        rgb = RGB.from_json(json_data)
        assert rgb.r == 0.4
        assert rgb.g == 0.7
        assert rgb.b == 0.2

    def test_from_json_partial_data(self):
        """Test JSON deserialization with partial data."""
        json_data = {"r": 0.8}
        rgb = RGB.from_json(json_data)
        assert rgb.r == 0.8
        assert rgb.g == 0.1  # Default value
        assert rgb.b == 0.1  # Default value

    def test_from_json_empty_data(self):
        """Test JSON deserialization with empty data."""
        json_data = {}
        rgb = RGB.from_json(json_data)
        assert rgb.r == 0.1  # Default value
        assert rgb.g == 0.1  # Default value
        assert rgb.b == 0.1  # Default value

    def test_from_json_invalid_data(self):
        """Test JSON deserialization with invalid data."""
        json_data = {"r": "invalid", "g": None, "b": []}
        rgb = RGB.from_json(json_data)
        # Should use defaults when data is invalid
        assert rgb.r == 0.1
        assert rgb.g == 0.1
        assert rgb.b == 0.1

    def test_repr(self):
        """Test string representation."""
        rgb = RGB(0.123, 0.456, 0.789)
        repr_str = repr(rgb)
        assert "RGB" in repr_str
        assert "0.12" in repr_str  # Rounded to 2 decimal places
        assert "0.46" in repr_str
        assert "0.79" in repr_str

    def test_json_roundtrip(self):
        """Test JSON serialization and deserialization roundtrip."""
        original = RGB(0.25, 0.75, 0.5)
        json_data = original.to_json()
        restored = RGB.from_json(json_data)
        assert original == restored

    def test_color_operations_chain(self):
        """Test chaining multiple color operations."""
        rgb1 = RGB(0.2, 0.3, 0.4)
        rgb2 = RGB(0.1, 0.2, 0.1)
        rgb3 = RGB(0.3, 0.1, 0.2)

        result = (rgb1 + rgb2) * 2 - rgb3
        # (0.3, 0.5, 0.5) * 2 = (0.6, 1.0, 1.0) - (0.3, 0.1, 0.2) = (0.3, 0.9, 0.8)
        assert abs(result.r - 0.3) < 0.001
        assert abs(result.g - 0.9) < 0.001
        assert abs(result.b - 0.8) < 0.001

    def test_edge_case_very_small_values(self):
        """Test with very small values."""
        rgb = RGB(1e-10, 1e-10, 1e-10)
        assert abs(rgb.r - 1e-10) < 1e-15  # Should preserve small values
        assert abs(rgb.g - 1e-10) < 1e-15
        assert abs(rgb.b - 1e-10) < 1e-15

    def test_edge_case_very_large_values(self):
        """Test with very large values."""
        rgb = RGB(1e10, 1e10, 1e10)
        assert rgb.r == 1.0  # Should be clamped to 1
        assert rgb.g == 1.0
        assert rgb.b == 1.0
