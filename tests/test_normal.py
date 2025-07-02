import pytest
import math
from Normal import Normal


class TestNormal:
    """Comprehensive tests for the Normal class."""

    def test_init_default(self):
        """Test Normal initialization with default values."""
        normal = Normal()
        assert normal.x == 0.0
        assert normal.y == 0.0
        assert normal.z == 0.0

    def test_init_individual_values(self):
        """Test Normal initialization with individual values."""
        normal = Normal(3, 4, 0)
        # Should be normalized: (3, 4, 0) -> (0.6, 0.8, 0.0)
        assert abs(normal.x - 0.6) < 0.001
        assert abs(normal.y - 0.8) < 0.001
        assert abs(normal.z - 0.0) < 0.001

    def test_init_from_iterable(self):
        """Test Normal initialization from iterable."""
        normal = Normal([6, 8, 0])
        # Should be normalized: (6, 8, 0) -> (0.6, 0.8, 0.0)
        assert abs(normal.x - 0.6) < 0.001
        assert abs(normal.y - 0.8) < 0.001
        assert abs(normal.z - 0.0) < 0.001

    def test_init_from_tuple(self):
        """Test Normal initialization from tuple."""
        normal = Normal((1, 0, 0))
        # Should remain normalized: (1, 0, 0) -> (1.0, 0.0, 0.0)
        assert abs(normal.x - 1.0) < 0.001
        assert abs(normal.y - 0.0) < 0.001
        assert abs(normal.z - 0.0) < 0.001

    def test_init_unit_vector_x(self):
        """Test Normal initialization with unit vector along x-axis."""
        normal = Normal(1, 0, 0)
        assert abs(normal.x - 1.0) < 0.001
        assert abs(normal.y - 0.0) < 0.001
        assert abs(normal.z - 0.0) < 0.001

    def test_init_unit_vector_y(self):
        """Test Normal initialization with unit vector along y-axis."""
        normal = Normal(0, 1, 0)
        assert abs(normal.x - 0.0) < 0.001
        assert abs(normal.y - 1.0) < 0.001
        assert abs(normal.z - 0.0) < 0.001

    def test_init_unit_vector_z(self):
        """Test Normal initialization with unit vector along z-axis."""
        normal = Normal(0, 0, 1)
        assert abs(normal.x - 0.0) < 0.001
        assert abs(normal.y - 0.0) < 0.001
        assert abs(normal.z - 1.0) < 0.001

    def test_init_negative_values(self):
        """Test Normal initialization with negative values."""
        normal = Normal(-3, -4, 0)
        # Should be normalized: (-3, -4, 0) -> (-0.6, -0.8, 0.0)
        assert abs(normal.x - (-0.6)) < 0.001
        assert abs(normal.y - (-0.8)) < 0.001
        assert abs(normal.z - 0.0) < 0.001

    def test_init_float_values(self):
        """Test Normal initialization with float values."""
        normal = Normal(1.5, 2.0, 2.5)
        length = math.sqrt(1.5*1.5 + 2.0*2.0 + 2.5*2.5)
        expected_x = 1.5 / length
        expected_y = 2.0 / length
        expected_z = 2.5 / length
        assert abs(normal.x - expected_x) < 0.001
        assert abs(normal.y - expected_y) < 0.001
        assert abs(normal.z - expected_z) < 0.001

    def test_normalization_property(self):
        """Test that Normal vectors are always unit length."""
        test_vectors = [
            (1, 2, 3),
            (5, 0, 0),
            (0, 7, 0),
            (0, 0, 9),
            (1, 1, 1),
            (2, 2, 2),
            (-1, -1, -1),
            (3.5, 4.2, 1.8)
        ]

        for x, y, z in test_vectors:
            normal = Normal(x, y, z)
            length = math.sqrt(normal.x**2 + normal.y**2 + normal.z**2)
            assert abs(length - 1.0) < 0.001, f"Normal({x}, {y}, {z}) not unit length: {length}"

    def test_zero_vector_handling(self):
        """Test Normal initialization with zero vector."""
        normal = Normal(0, 0, 0)
        # Division by zero should be handled gracefully
        assert normal.x == 0.0
        assert normal.y == 0.0
        assert normal.z == 0.0

    def test_very_small_vector_handling(self):
        """Test Normal initialization with very small vector."""
        normal = Normal(1e-10, 1e-10, 1e-10)
        # Should still normalize properly
        length = math.sqrt(normal.x**2 + normal.y**2 + normal.z**2)
        if length > 0:  # If not exactly zero due to precision
            assert abs(length - 1.0) < 0.001

    def test_dot_product_basic(self):
        """Test dot product operation."""
        normal1 = Normal(1, 0, 0)
        normal2 = Normal(0, 1, 0)
        result = normal1 * normal2
        assert abs(result - 0.0) < 0.001  # Orthogonal vectors

    def test_dot_product_parallel(self):
        """Test dot product of parallel normals."""
        normal1 = Normal(1, 0, 0)
        normal2 = Normal(2, 0, 0)  # Will be normalized to (1, 0, 0)
        result = normal1 * normal2
        assert abs(result - 1.0) < 0.001  # Parallel unit vectors

    def test_dot_product_antiparallel(self):
        """Test dot product of antiparallel normals."""
        normal1 = Normal(1, 0, 0)
        normal2 = Normal(-1, 0, 0)
        result = normal1 * normal2
        assert abs(result - (-1.0)) < 0.001  # Antiparallel unit vectors

    def test_dot_product_45_degrees(self):
        """Test dot product at 45 degrees."""
        normal1 = Normal(1, 0, 0)
        normal2 = Normal(1, 1, 0)  # Will be normalized to (1/√2, 1/√2, 0)
        result = normal1 * normal2
        expected = 1.0 / math.sqrt(2)  # cos(45°) = 1/√2
        assert abs(result - expected) < 0.001

    def test_dot_product_with_vector(self):
        """Test dot product with vector-like object."""
        normal = Normal(1, 0, 0)

        # Create a mock vector object with x, y, z attributes
        class MockVector:
            def __init__(self, x, y, z):
                self.x = x
                self.y = y
                self.z = z

        vector = MockVector(0.5, 0.5, 0.0)
        result = normal * vector
        assert abs(result - 0.5) < 0.001

    def test_scalar_multiplication_right(self):
        """Test right scalar multiplication."""
        normal = Normal(1, 0, 0)
        result = normal.__rmul__(2)
        assert isinstance(result, Normal)
        assert abs(result.x - 1.0) < 0.001  # Should be normalized to unit vector
        assert abs(result.y - 0.0) < 0.001
        assert abs(result.z - 0.0) < 0.001

    def test_scalar_multiplication_zero(self):
        """Test scalar multiplication by zero."""
        normal = Normal(1, 2, 3)
        result = normal.__rmul__(0)
        assert result.x == 0.0
        assert result.y == 0.0
        assert result.z == 0.0

    def test_scalar_multiplication_negative(self):
        """Test scalar multiplication by negative value."""
        normal = Normal(1, 0, 0)
        result = normal.__rmul__(-1)
        assert abs(result.x - (-1.0)) < 0.001
        assert abs(result.y - 0.0) < 0.001
        assert abs(result.z - 0.0) < 0.001

    def test_scalar_multiplication_float(self):
        """Test scalar multiplication by float."""
        normal = Normal(0, 1, 0)
        result = normal.__rmul__(0.5)
        assert abs(result.x - 0.0) < 0.001
        assert abs(result.y - 1.0) < 0.001  # Should be normalized to unit vector
        assert abs(result.z - 0.0) < 0.001

    def test_repr(self):
        """Test string representation."""
        normal = Normal(3, 4, 0)
        repr_str = repr(normal)
        assert "Normal" in repr_str
        assert "x=" in repr_str
        assert "y=" in repr_str
        assert "z=" in repr_str
        # Check that values are formatted to 4 decimal places
        assert ".6000" in repr_str or "0.6000" in repr_str
        assert ".8000" in repr_str or "0.8000" in repr_str

    def test_normalization_preserves_direction(self):
        """Test that normalization preserves vector direction."""
        test_cases = [
            (2, 0, 0),    # Should become (1, 0, 0)
            (0, 3, 0),    # Should become (0, 1, 0)
            (0, 0, 4),    # Should become (0, 0, 1)
            (1, 1, 0),    # Should become (1/√2, 1/√2, 0)
            (1, 1, 1),    # Should become (1/√3, 1/√3, 1/√3)
        ]

        for x, y, z in test_cases:
            normal = Normal(x, y, z)
            original_length = math.sqrt(x*x + y*y + z*z)

            if original_length > 0:
                expected_x = x / original_length
                expected_y = y / original_length
                expected_z = z / original_length

                assert abs(normal.x - expected_x) < 0.001
                assert abs(normal.y - expected_y) < 0.001
                assert abs(normal.z - expected_z) < 0.001

    def test_common_surface_normals(self):
        """Test common surface normal vectors."""
        # Face normals for a cube
        face_normals = [
            (1, 0, 0),   # +X face
            (-1, 0, 0),  # -X face
            (0, 1, 0),   # +Y face
            (0, -1, 0),  # -Y face
            (0, 0, 1),   # +Z face
            (0, 0, -1),  # -Z face
        ]

        for x, y, z in face_normals:
            normal = Normal(x, y, z)
            assert abs(normal.x - x) < 0.001
            assert abs(normal.y - y) < 0.001
            assert abs(normal.z - z) < 0.001

    def test_diagonal_normals(self):
        """Test diagonal normal vectors."""
        # Diagonal of a cube face
        normal = Normal(1, 1, 0)
        expected = 1.0 / math.sqrt(2)
        assert abs(normal.x - expected) < 0.001
        assert abs(normal.y - expected) < 0.001
        assert abs(normal.z - 0.0) < 0.001

        # Space diagonal of a cube
        normal = Normal(1, 1, 1)
        expected = 1.0 / math.sqrt(3)
        assert abs(normal.x - expected) < 0.001
        assert abs(normal.y - expected) < 0.001
        assert abs(normal.z - expected) < 0.001

    def test_dot_product_symmetry(self):
        """Test dot product symmetry property."""
        normal1 = Normal(1, 2, 3)
        normal2 = Normal(4, 5, 6)

        result1 = normal1 * normal2
        result2 = normal2 * normal1

        assert abs(result1 - result2) < 0.001

    def test_dot_product_range(self):
        """Test that dot product is always in range [-1, 1] for unit vectors."""
        test_normals = [
            Normal(1, 0, 0),
            Normal(0, 1, 0),
            Normal(0, 0, 1),
            Normal(1, 1, 0),
            Normal(1, 1, 1),
            Normal(-1, 0, 0),
            Normal(0, -1, 0),
            Normal(0, 0, -1),
            Normal(2, 3, 4),
            Normal(-2, -3, -4),
        ]

        for normal1 in test_normals:
            for normal2 in test_normals:
                dot_product = normal1 * normal2
                assert -1.001 <= dot_product <= 1.001, f"Dot product {dot_product} out of range for {normal1} * {normal2}"

    def test_edge_case_very_large_values(self):
        """Test Normal with very large input values."""
        normal = Normal(1e10, 1e10, 1e10)
        # Should still normalize to unit length
        length = math.sqrt(normal.x**2 + normal.y**2 + normal.z**2)
        assert abs(length - 1.0) < 0.001

        # Should be equal to (1/√3, 1/√3, 1/√3)
        expected = 1.0 / math.sqrt(3)
        assert abs(normal.x - expected) < 0.001
        assert abs(normal.y - expected) < 0.001
        assert abs(normal.z - expected) < 0.001

    def test_edge_case_mixed_large_small(self):
        """Test Normal with mixed large and small values."""
        normal = Normal(1e10, 1e-10, 0)
        # Should be approximately (1, 0, 0) since 1e10 >> 1e-10
        assert abs(normal.x - 1.0) < 0.001
        assert abs(normal.y) < 0.001
        assert abs(normal.z) < 0.001

    def test_initialization_type_conversion(self):
        """Test that initialization converts values to float."""
        normal = Normal(1, 2, 3)
        assert isinstance(normal.x, float)
        assert isinstance(normal.y, float)
        assert isinstance(normal.z, float)

    def test_normal_from_cross_product_concept(self):
        """Test creating normal from cross product concept."""
        # If we had vectors (1,0,0) and (0,1,0), their cross product would be (0,0,1)
        # This should be a valid normal
        normal = Normal(0, 0, 1)
        assert abs(normal.x - 0.0) < 0.001
        assert abs(normal.y - 0.0) < 0.001
        assert abs(normal.z - 1.0) < 0.001

    def test_normal_consistency(self):
        """Test that creating Normal with same values gives consistent results."""
        for _ in range(10):  # Test multiple times to check for any randomness
            normal1 = Normal(3, 4, 5)
            normal2 = Normal(3, 4, 5)

            assert abs(normal1.x - normal2.x) < 1e-10
            assert abs(normal1.y - normal2.y) < 1e-10
            assert abs(normal1.z - normal2.z) < 1e-10
