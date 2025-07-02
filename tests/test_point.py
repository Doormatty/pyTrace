import pytest
import math
from Point import Point3D
from Vector import Vector3D


class TestPoint3D:
    """Comprehensive tests for the Point3D class."""

    def test_init_default(self):
        """Test Point3D initialization with default values."""
        point = Point3D()
        assert point.x == 0
        assert point.y == 0
        assert point.z == 0

    def test_init_individual_values(self):
        """Test Point3D initialization with individual values."""
        point = Point3D(1, 2, 3)
        assert point.x == 1
        assert point.y == 2
        assert point.z == 3

    def test_init_from_iterable(self):
        """Test Point3D initialization from iterable."""
        point = Point3D([4, 5, 6])
        assert point.x == 4
        assert point.y == 5
        assert point.z == 6

    def test_init_from_tuple(self):
        """Test Point3D initialization from tuple."""
        point = Point3D((7, 8, 9))
        assert point.x == 7
        assert point.y == 8
        assert point.z == 9

    def test_init_negative_values(self):
        """Test Point3D initialization with negative values."""
        point = Point3D(-1, -2, -3)
        assert point.x == -1
        assert point.y == -2
        assert point.z == -3

    def test_init_float_values(self):
        """Test Point3D initialization with float values."""
        point = Point3D(1.5, 2.7, 3.14)
        assert point.x == 1.5
        assert point.y == 2.7
        assert point.z == 3.14

    def test_init_distance_cache(self):
        """Test Point3D initialization creates empty distance cache."""
        point = Point3D(1, 2, 3)
        assert hasattr(point, '_distance_cache')
        assert point._distance_cache == {}

    def test_add_vector(self):
        """Test point + vector = point."""
        point = Point3D(1, 2, 3)
        vector = Vector3D(4, 5, 6)
        result = point + vector
        assert isinstance(result, Point3D)
        assert result.x == 5
        assert result.y == 7
        assert result.z == 9

    def test_add_point(self):
        """Test point + point = vector."""
        point1 = Point3D(1, 2, 3)
        point2 = Point3D(4, 5, 6)
        result = point1 + point2
        assert isinstance(result, Vector3D)
        assert result.x == 5
        assert result.y == 7
        assert result.z == 9

    def test_add_scalar(self):
        """Test point + scalar = point."""
        point = Point3D(1, 2, 3)
        result = point + 5
        assert isinstance(result, Point3D)
        assert result.x == 6
        assert result.y == 7
        assert result.z == 8

    def test_add_zero_vector(self):
        """Test point + zero vector = same point."""
        point = Point3D(1, 2, 3)
        zero_vector = Vector3D(0, 0, 0)
        result = point + zero_vector
        assert result.x == 1
        assert result.y == 2
        assert result.z == 3

    def test_subtract_vector(self):
        """Test point - vector = point."""
        point = Point3D(5, 7, 9)
        vector = Vector3D(1, 2, 3)
        result = point - vector
        assert isinstance(result, Point3D)
        assert result.x == 4
        assert result.y == 5
        assert result.z == 6

    def test_subtract_point(self):
        """Test point - point = vector."""
        point1 = Point3D(5, 7, 9)
        point2 = Point3D(1, 2, 3)
        result = point1 - point2
        assert isinstance(result, Vector3D)
        assert result.x == 4
        assert result.y == 5
        assert result.z == 6

    def test_subtract_scalar(self):
        """Test point - scalar = point."""
        point = Point3D(5, 7, 9)
        result = point - 2
        assert isinstance(result, Point3D)
        assert result.x == 3
        assert result.y == 5
        assert result.z == 7

    def test_subtract_same_point(self):
        """Test point - same point = zero vector."""
        point = Point3D(1, 2, 3)
        result = point - point
        assert isinstance(result, Vector3D)
        assert result.x == 0
        assert result.y == 0
        assert result.z == 0

    def test_rsub_vector(self):
        """Test vector - point = point (right subtraction)."""
        point = Point3D(1, 2, 3)
        vector = Vector3D(5, 7, 9)
        result = point.__rsub__(vector)
        assert isinstance(result, Point3D)
        assert result.x == 4
        assert result.y == 5
        assert result.z == 6

    def test_rsub_scalar(self):
        """Test scalar - point = point (right subtraction)."""
        point = Point3D(1, 2, 3)
        result = point.__rsub__(5)
        assert isinstance(result, Point3D)
        assert result.x == 4
        assert result.y == 3
        assert result.z == 2

    def test_rsub_point(self):
        """Test point - point = vector (right subtraction)."""
        point1 = Point3D(1, 2, 3)
        point2 = Point3D(5, 7, 9)
        result = point1.__rsub__(point2)
        assert isinstance(result, Vector3D)
        assert result.x == 4
        assert result.y == 5
        assert result.z == 6

    def test_multiplication_scalar(self):
        """Test point * scalar = point."""
        point = Point3D(1, 2, 3)
        result = point * 2
        assert isinstance(result, Point3D)
        assert result.x == 2
        assert result.y == 4
        assert result.z == 6

    def test_multiplication_zero(self):
        """Test point * 0 = origin."""
        point = Point3D(1, 2, 3)
        result = point * 0
        assert result.x == 0
        assert result.y == 0
        assert result.z == 0

    def test_multiplication_negative(self):
        """Test point * negative scalar."""
        point = Point3D(1, 2, 3)
        result = point * -2
        assert result.x == -2
        assert result.y == -4
        assert result.z == -6

    def test_multiplication_float(self):
        """Test point * float scalar."""
        point = Point3D(2, 4, 6)
        result = point * 0.5
        assert result.x == 1
        assert result.y == 2
        assert result.z == 3

    def test_right_multiplication(self):
        """Test scalar * point = point."""
        point = Point3D(1, 2, 3)
        result = point.__rmul__(3)
        assert isinstance(result, Point3D)
        assert result.x == 3
        assert result.y == 6
        assert result.z == 9

    def test_distance_squared_basic(self):
        """Test distance_squared calculation."""
        point1 = Point3D(0, 0, 0)
        point2 = Point3D(3, 4, 0)
        dist_sq = point1.distance_squared(point2)
        assert dist_sq == 25  # 3^2 + 4^2 + 0^2 = 9 + 16 + 0 = 25

    def test_distance_squared_same_point(self):
        """Test distance_squared to same point."""
        point = Point3D(1, 2, 3)
        dist_sq = point.distance_squared(point)
        assert dist_sq == 0

    def test_distance_squared_negative_coordinates(self):
        """Test distance_squared with negative coordinates."""
        point1 = Point3D(-1, -2, -3)
        point2 = Point3D(1, 2, 3)
        dist_sq = point1.distance_squared(point2)
        # Expected: (1-(-1))^2 + (2-(-2))^2 + (3-(-3))^2 = 4 + 16 + 36 = 56
        assert dist_sq == 56

    def test_distance_squared_float_coordinates(self):
        """Test distance_squared with float coordinates."""
        point1 = Point3D(1.5, 2.5, 3.5)
        point2 = Point3D(4.5, 6.5, 7.5)
        dist_sq = point1.distance_squared(point2)
        # Expected: (4.5-1.5)^2 + (6.5-2.5)^2 + (7.5-3.5)^2 = 9 + 16 + 16 = 41
        assert dist_sq == 41

    def test_distance_basic(self):
        """Test distance calculation."""
        point1 = Point3D(0, 0, 0)
        point2 = Point3D(3, 4, 0)
        dist = point1.distance(point2)
        assert dist == 5.0  # sqrt(25) = 5

    def test_distance_same_point(self):
        """Test distance to same point."""
        point = Point3D(1, 2, 3)
        dist = point.distance(point)
        assert dist == 0.0

    def test_distance_caching(self):
        """Test distance calculation caching."""
        point1 = Point3D(0, 0, 0)
        point2 = Point3D(3, 4, 0)

        # First calculation should cache the result
        dist1 = point1.distance(point2)

        # Second calculation should use cached result
        dist2 = point1.distance(point2)

        assert dist1 == dist2 == 5.0

        # Check that the result is cached
        point2_id = id(point2)
        assert point2_id in point1._distance_cache
        assert point1._distance_cache[point2_id] == 5.0

    def test_distance_cache_limit(self):
        """Test distance cache size limit."""
        point = Point3D(0, 0, 0)

        # Create many points to exceed cache limit
        points = [Point3D(i, 0, 0) for i in range(150)]

        # Calculate distances to all points
        for p in points:
            point.distance(p)

        # Cache should be cleared when limit is exceeded
        assert len(point._distance_cache) <= 100

    def test_distance_symmetry(self):
        """Test distance calculation symmetry."""
        point1 = Point3D(1, 2, 3)
        point2 = Point3D(4, 6, 8)

        dist1 = point1.distance(point2)
        dist2 = point2.distance(point1)

        assert dist1 == dist2

    def test_distance_3d_pythagorean(self):
        """Test distance calculation with 3D Pythagorean theorem."""
        point1 = Point3D(0, 0, 0)
        point2 = Point3D(1, 2, 2)
        dist = point1.distance(point2)
        expected = math.sqrt(1 + 4 + 4)  # sqrt(9) = 3
        assert abs(dist - expected) < 0.001

    def test_equality_same_values(self):
        """Test point equality with same values."""
        point1 = Point3D(1, 2, 3)
        point2 = Point3D(1, 2, 3)
        assert point1 == point2

    def test_equality_different_values(self):
        """Test point inequality with different values."""
        point1 = Point3D(1, 2, 3)
        point2 = Point3D(1, 2, 4)
        assert point1 != point2

    def test_equality_float_precision(self):
        """Test point equality with float precision."""
        point1 = Point3D(1.0, 2.0, 3.0)
        point2 = Point3D(1.0, 2.0, 3.0)
        assert point1 == point2

    def test_repr(self):
        """Test string representation."""
        point = Point3D(1, 2, 3)
        repr_str = repr(point)
        assert "Point3D" in repr_str
        assert "x=1" in repr_str
        assert "y=2" in repr_str
        assert "z=3" in repr_str

    def test_json_inheritance(self):
        """Test JSON methods are inherited from Coord3D."""
        point = Point3D(1.5, 2.5, 3.5)
        json_data = point.to_json()
        expected = {"x": 1.5, "y": 2.5, "z": 3.5}
        assert json_data == expected

    def test_json_roundtrip(self):
        """Test JSON serialization and deserialization roundtrip."""
        original = Point3D(1.25, 2.75, 3.125)
        json_data = original.to_json()
        restored = Point3D.from_json(json_data)
        assert original == restored

    def test_origin_point(self):
        """Test origin point properties."""
        origin = Point3D(0, 0, 0)
        assert origin.x == 0
        assert origin.y == 0
        assert origin.z == 0

        # Distance from origin to itself should be 0
        assert origin.distance(origin) == 0
        assert origin.distance_squared(origin) == 0

    def test_point_vector_operations_chain(self):
        """Test chaining point and vector operations."""
        point = Point3D(1, 2, 3)
        vector1 = Vector3D(2, 3, 4)
        vector2 = Vector3D(1, 1, 1)

        # point + vector - vector should equal original point
        result = point + vector1 - vector1
        assert result == point

        # (point + vector) * 2 - point should equal point + vector
        # Mathematically: (P + V) * 2 - P = 2P + 2V - P = P + 2V
        result2 = (point + vector2) * 2 - point
        expected = point + (vector2 * 2)  # P + 2V
        assert result2.x == expected.x
        assert result2.y == expected.y
        assert result2.z == expected.z

    def test_midpoint_calculation(self):
        """Test midpoint calculation using point operations."""
        point1 = Point3D(0, 0, 0)
        point2 = Point3D(4, 6, 8)

        # Midpoint = (point1 + point2) / 2, but since point + point = vector,
        # we need to use: point1 + (point2 - point1) * 0.5
        midpoint_vector = (point2 - point1) * 0.5
        midpoint = point1 + midpoint_vector

        assert midpoint.x == 2
        assert midpoint.y == 3
        assert midpoint.z == 4

    def test_translation_operations(self):
        """Test point translation operations."""
        point = Point3D(1, 2, 3)
        translation = Vector3D(5, -2, 7)

        # Translate point
        translated = point + translation
        assert translated.x == 6
        assert translated.y == 0
        assert translated.z == 10

        # Translate back
        back = translated - translation
        assert back == point

    def test_edge_case_very_small_coordinates(self):
        """Test with very small coordinate values."""
        point1 = Point3D(1e-10, 1e-10, 1e-10)
        point2 = Point3D(2e-10, 2e-10, 2e-10)

        dist_sq = point1.distance_squared(point2)
        expected_dist_sq = 3 * (1e-10)**2  # 3 * 1e-20 = 3e-20
        assert abs(dist_sq - expected_dist_sq) < 1e-25

        dist = point1.distance(point2)
        expected_dist = math.sqrt(3e-20)
        assert abs(dist - expected_dist) < 1e-15

    def test_edge_case_very_large_coordinates(self):
        """Test with very large coordinate values."""
        point1 = Point3D(1e10, 1e10, 1e10)
        point2 = Point3D(2e10, 2e10, 2e10)

        dist_sq = point1.distance_squared(point2)
        expected_dist_sq = 3 * (1e10)**2  # 3 * 1e20 = 3e20
        assert abs(dist_sq - expected_dist_sq) < 1e15

        dist = point1.distance(point2)
        expected_dist = math.sqrt(3e20)
        assert abs(dist - expected_dist) < 1e5

    def test_cache_independence(self):
        """Test that different points have independent caches."""
        point1 = Point3D(0, 0, 0)
        point2 = Point3D(1, 1, 1)
        point3 = Point3D(2, 2, 2)

        # Calculate distances
        point1.distance(point3)
        point2.distance(point3)

        # Caches should be independent
        assert len(point1._distance_cache) == 1
        assert len(point2._distance_cache) == 1
        assert id(point3) in point1._distance_cache
        assert id(point3) in point2._distance_cache
