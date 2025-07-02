import pytest
import math
from Vector import Vector3D
from Normal import Normal


class TestVector3D:
    """Comprehensive tests for the Vector3D class."""

    def test_init_default(self):
        """Test Vector3D initialization with default values."""
        vec = Vector3D()
        assert vec.x == 0
        assert vec.y == 0
        assert vec.z == 0

    def test_init_individual_values(self):
        """Test Vector3D initialization with individual values."""
        vec = Vector3D(1, 2, 3)
        assert vec.x == 1
        assert vec.y == 2
        assert vec.z == 3

    def test_init_from_iterable(self):
        """Test Vector3D initialization from iterable."""
        vec = Vector3D([4, 5, 6])
        assert vec.x == 4
        assert vec.y == 5
        assert vec.z == 6

    def test_init_from_tuple(self):
        """Test Vector3D initialization from tuple."""
        vec = Vector3D((7, 8, 9))
        assert vec.x == 7
        assert vec.y == 8
        assert vec.z == 9

    def test_init_negative_values(self):
        """Test Vector3D initialization with negative values."""
        vec = Vector3D(-1, -2, -3)
        assert vec.x == -1
        assert vec.y == -2
        assert vec.z == -3

    def test_init_float_values(self):
        """Test Vector3D initialization with float values."""
        vec = Vector3D(1.5, 2.7, 3.14)
        assert vec.x == 1.5
        assert vec.y == 2.7
        assert vec.z == 3.14

    def test_addition(self):
        """Test vector addition."""
        vec1 = Vector3D(1, 2, 3)
        vec2 = Vector3D(4, 5, 6)
        result = vec1 + vec2
        assert result.x == 5
        assert result.y == 7
        assert result.z == 9

    def test_addition_with_zero_vector(self):
        """Test vector addition with zero vector."""
        vec1 = Vector3D(1, 2, 3)
        vec2 = Vector3D(0, 0, 0)
        result = vec1 + vec2
        assert result.x == 1
        assert result.y == 2
        assert result.z == 3

    def test_addition_negative_values(self):
        """Test vector addition with negative values."""
        vec1 = Vector3D(1, -2, 3)
        vec2 = Vector3D(-4, 5, -6)
        result = vec1 + vec2
        assert result.x == -3
        assert result.y == 3
        assert result.z == -3

    def test_subtraction(self):
        """Test vector subtraction."""
        vec1 = Vector3D(5, 7, 9)
        vec2 = Vector3D(1, 2, 3)
        result = vec1 - vec2
        assert result.x == 4
        assert result.y == 5
        assert result.z == 6

    def test_subtraction_same_vector(self):
        """Test vector subtraction with same vector."""
        vec = Vector3D(1, 2, 3)
        result = vec - vec
        assert result.x == 0
        assert result.y == 0
        assert result.z == 0

    def test_subtraction_negative_result(self):
        """Test vector subtraction resulting in negative values."""
        vec1 = Vector3D(1, 2, 3)
        vec2 = Vector3D(4, 5, 6)
        result = vec1 - vec2
        assert result.x == -3
        assert result.y == -3
        assert result.z == -3

    def test_cross_product_basic(self):
        """Test cross product operation."""
        vec1 = Vector3D(1, 0, 0)
        vec2 = Vector3D(0, 1, 0)
        result = vec1 ^ vec2
        assert result.x == 0
        assert result.y == 0
        assert result.z == 1

    def test_cross_product_parallel_vectors(self):
        """Test cross product of parallel vectors."""
        vec1 = Vector3D(1, 2, 3)
        vec2 = Vector3D(2, 4, 6)  # Parallel to vec1
        result = vec1 ^ vec2
        assert result.x == 0
        assert result.y == 0
        assert result.z == 0

    def test_cross_product_anticommutative(self):
        """Test cross product anticommutative property."""
        vec1 = Vector3D(1, 2, 3)
        vec2 = Vector3D(4, 5, 6)
        result1 = vec1 ^ vec2
        result2 = vec2 ^ vec1
        assert result1.x == -result2.x
        assert result1.y == -result2.y
        assert result1.z == -result2.z

    def test_cross_product_complex(self):
        """Test cross product with complex vectors."""
        vec1 = Vector3D(2, 3, 4)
        vec2 = Vector3D(5, 6, 7)
        result = vec1 ^ vec2
        # Expected: (3*7 - 4*6, 4*5 - 2*7, 2*6 - 3*5) = (-3, 6, -3)
        assert result.x == -3
        assert result.y == 6
        assert result.z == -3

    def test_dot_product_basic(self):
        """Test dot product operation using * operator."""
        vec1 = Vector3D(1, 2, 3)
        vec2 = Vector3D(4, 5, 6)
        result = vec1 * vec2
        # Expected: 1*4 + 2*5 + 3*6 = 4 + 10 + 18 = 32
        assert result == 32

    def test_dot_product_with_normal(self):
        """Test dot product with Normal object."""
        vec = Vector3D(1, 2, 3)
        normal = Normal(1, 0, 0)
        result = vec * normal
        assert result == 1

    def test_dot_product_orthogonal_vectors(self):
        """Test dot product of orthogonal vectors."""
        vec1 = Vector3D(1, 0, 0)
        vec2 = Vector3D(0, 1, 0)
        result = vec1 * vec2
        assert result == 0

    def test_dot_product_mod_operator(self):
        """Test dot product using % operator."""
        vec1 = Vector3D(2, 3, 4)
        vec2 = Vector3D(1, 2, 3)
        result = vec1 % vec2
        # Expected: 2*1 + 3*2 + 4*3 = 2 + 6 + 12 = 20
        assert result == 20

    def test_scalar_multiplication(self):
        """Test scalar multiplication."""
        vec = Vector3D(1, 2, 3)
        result = vec * 2
        assert result.x == 2
        assert result.y == 4
        assert result.z == 6

    def test_scalar_multiplication_zero(self):
        """Test scalar multiplication by zero."""
        vec = Vector3D(1, 2, 3)
        result = vec * 0
        assert result.x == 0
        assert result.y == 0
        assert result.z == 0

    def test_scalar_multiplication_negative(self):
        """Test scalar multiplication by negative value."""
        vec = Vector3D(1, 2, 3)
        result = vec * -2
        assert result.x == -2
        assert result.y == -4
        assert result.z == -6

    def test_scalar_multiplication_float(self):
        """Test scalar multiplication by float."""
        vec = Vector3D(2, 4, 6)
        result = vec * 0.5
        assert result.x == 1
        assert result.y == 2
        assert result.z == 3

    def test_right_scalar_multiplication(self):
        """Test right scalar multiplication."""
        vec = Vector3D(1, 2, 3)
        result = 3 * vec
        assert result.x == 3
        assert result.y == 6
        assert result.z == 9

    def test_division(self):
        """Test vector division by scalar."""
        vec = Vector3D(6, 8, 10)
        result = vec / 2
        assert result.x == 3
        assert result.y == 4
        assert result.z == 5

    def test_division_by_zero(self):
        """Test vector division by zero."""
        vec = Vector3D(1, 2, 3)
        result = vec / 0
        assert result == False

    def test_division_float(self):
        """Test vector division by float."""
        vec = Vector3D(1, 2, 3)
        result = vec / 2.0
        assert result.x == 0.5
        assert result.y == 1.0
        assert result.z == 1.5

    def test_equality_same_values(self):
        """Test vector equality with same values."""
        vec1 = Vector3D(1, 2, 3)
        vec2 = Vector3D(1, 2, 3)
        assert vec1 == vec2

    def test_equality_different_values(self):
        """Test vector inequality with different values."""
        vec1 = Vector3D(1, 2, 3)
        vec2 = Vector3D(1, 2, 4)
        assert vec1 != vec2

    def test_equality_float_precision(self):
        """Test vector equality with float precision."""
        vec1 = Vector3D(1.0, 2.0, 3.0)
        vec2 = Vector3D(1.0, 2.0, 3.0)
        assert vec1 == vec2

    def test_length_squared_property(self):
        """Test length_squared property."""
        vec = Vector3D(3, 4, 0)
        assert vec.length_squared == 25  # 3^2 + 4^2 + 0^2 = 9 + 16 + 0 = 25

    def test_length_squared_caching(self):
        """Test length_squared property caching."""
        vec = Vector3D(1, 2, 3)
        # First access should calculate
        length_sq1 = vec.length_squared
        # Second access should use cached value
        length_sq2 = vec.length_squared
        assert length_sq1 == length_sq2
        assert length_sq1 == 14  # 1^2 + 2^2 + 3^2 = 1 + 4 + 9 = 14

    def test_length_property(self):
        """Test length property."""
        vec = Vector3D(3, 4, 0)
        assert vec.length == 5.0  # sqrt(3^2 + 4^2 + 0^2) = sqrt(25) = 5

    def test_length_caching(self):
        """Test length property caching."""
        vec = Vector3D(1, 2, 2)
        # First access should calculate
        length1 = vec.length
        # Second access should use cached value
        length2 = vec.length
        assert length1 == length2
        assert abs(length1 - 3.0) < 0.001  # sqrt(1 + 4 + 4) = sqrt(9) = 3

    def test_normalize(self):
        """Test vector normalization."""
        vec = Vector3D(3, 4, 0)
        normalized = vec.normalize()
        assert abs(normalized.x - 0.6) < 0.001  # 3/5
        assert abs(normalized.y - 0.8) < 0.001  # 4/5
        assert abs(normalized.z - 0.0) < 0.001  # 0/5
        assert abs(normalized.length - 1.0) < 0.001

    def test_normalize_unit_vector(self):
        """Test normalization of unit vector."""
        vec = Vector3D(1, 0, 0)
        normalized = vec.normalize()
        assert abs(normalized.x - 1.0) < 0.001
        assert abs(normalized.y - 0.0) < 0.001
        assert abs(normalized.z - 0.0) < 0.001

    def test_normalize_complex_vector(self):
        """Test normalization of complex vector."""
        vec = Vector3D(1, 2, 2)
        normalized = vec.normalize()
        expected_length = math.sqrt(9)  # sqrt(1 + 4 + 4)
        assert abs(normalized.x - 1/expected_length) < 0.001
        assert abs(normalized.y - 2/expected_length) < 0.001
        assert abs(normalized.z - 2/expected_length) < 0.001
        assert abs(normalized.length - 1.0) < 0.001

    def test_repr(self):
        """Test string representation."""
        vec = Vector3D(1, 2, 3)
        repr_str = repr(vec)
        assert "Vector3D" in repr_str
        assert "x=1" in repr_str
        assert "y=2" in repr_str
        assert "z=3" in repr_str

    def test_json_inheritance(self):
        """Test JSON methods are inherited from Coord3D."""
        vec = Vector3D(1.5, 2.5, 3.5)
        json_data = vec.to_json()
        expected = {"x": 1.5, "y": 2.5, "z": 3.5}
        assert json_data == expected

    def test_json_roundtrip(self):
        """Test JSON serialization and deserialization roundtrip."""
        original = Vector3D(1.25, 2.75, 3.125)
        json_data = original.to_json()
        restored = Vector3D.from_json(json_data)
        assert original == restored

    def test_zero_vector_properties(self):
        """Test properties of zero vector."""
        zero_vec = Vector3D(0, 0, 0)
        assert zero_vec.length == 0.0
        assert zero_vec.length_squared == 0.0

    def test_normalize_zero_vector(self):
        """Test normalization of zero vector (should not cause divide by zero)."""
        zero_vec = Vector3D(0, 0, 0)
        normalized = zero_vec.normalize()
        # Zero vector normalization should return zero vector
        assert normalized.x == 0.0
        assert normalized.y == 0.0
        assert normalized.z == 0.0
        assert normalized.length == 0.0

    def test_unit_vectors(self):
        """Test standard unit vectors."""
        i = Vector3D(1, 0, 0)
        j = Vector3D(0, 1, 0)
        k = Vector3D(0, 0, 1)

        assert i.length == 1.0
        assert j.length == 1.0
        assert k.length == 1.0

        # Test cross products
        assert (i ^ j) == k
        assert (j ^ k) == i
        assert (k ^ i) == j

    def test_vector_operations_chain(self):
        """Test chaining multiple vector operations."""
        vec1 = Vector3D(1, 2, 3)
        vec2 = Vector3D(2, 1, 0)
        vec3 = Vector3D(1, 1, 1)

        result = (vec1 + vec2) * 2 - vec3
        # (3, 3, 3) * 2 - (1, 1, 1) = (6, 6, 6) - (1, 1, 1) = (5, 5, 5)
        assert result.x == 5
        assert result.y == 5
        assert result.z == 5

    def test_edge_case_very_small_vector(self):
        """Test with very small vector components."""
        vec = Vector3D(1e-10, 1e-10, 1e-10)
        assert vec.length_squared == 3e-20
        assert abs(vec.length - math.sqrt(3e-20)) < 1e-15

    def test_edge_case_very_large_vector(self):
        """Test with very large vector components."""
        vec = Vector3D(1e10, 1e10, 1e10)
        assert vec.length_squared == 3e20
        assert abs(vec.length - math.sqrt(3e20)) < 1e5
