import pytest
from Coord3D import Coord3D


class TestCoord3D:
    """Comprehensive tests for the Coord3D base class."""

    def test_to_json_basic(self):
        """Test JSON serialization with basic coordinates."""
        # Create a simple subclass for testing
        class TestCoord(Coord3D):
            def __init__(self, x=0, y=0, z=0):
                self.x = x
                self.y = y
                self.z = z
        
        coord = TestCoord(1.5, 2.7, 3.14)
        json_data = coord.to_json()
        
        expected = {"x": 1.5, "y": 2.7, "z": 3.14}
        assert json_data == expected

    def test_to_json_zero_coordinates(self):
        """Test JSON serialization with zero coordinates."""
        class TestCoord(Coord3D):
            def __init__(self, x=0, y=0, z=0):
                self.x = x
                self.y = y
                self.z = z
        
        coord = TestCoord(0, 0, 0)
        json_data = coord.to_json()
        
        expected = {"x": 0, "y": 0, "z": 0}
        assert json_data == expected

    def test_to_json_negative_coordinates(self):
        """Test JSON serialization with negative coordinates."""
        class TestCoord(Coord3D):
            def __init__(self, x=0, y=0, z=0):
                self.x = x
                self.y = y
                self.z = z
        
        coord = TestCoord(-1.5, -2.7, -3.14)
        json_data = coord.to_json()
        
        expected = {"x": -1.5, "y": -2.7, "z": -3.14}
        assert json_data == expected

    def test_to_json_integer_coordinates(self):
        """Test JSON serialization with integer coordinates."""
        class TestCoord(Coord3D):
            def __init__(self, x=0, y=0, z=0):
                self.x = x
                self.y = y
                self.z = z
        
        coord = TestCoord(1, 2, 3)
        json_data = coord.to_json()
        
        expected = {"x": 1, "y": 2, "z": 3}
        assert json_data == expected

    def test_to_json_large_coordinates(self):
        """Test JSON serialization with large coordinates."""
        class TestCoord(Coord3D):
            def __init__(self, x=0, y=0, z=0):
                self.x = x
                self.y = y
                self.z = z
        
        coord = TestCoord(1e6, 2e6, 3e6)
        json_data = coord.to_json()
        
        expected = {"x": 1e6, "y": 2e6, "z": 3e6}
        assert json_data == expected

    def test_to_json_small_coordinates(self):
        """Test JSON serialization with very small coordinates."""
        class TestCoord(Coord3D):
            def __init__(self, x=0, y=0, z=0):
                self.x = x
                self.y = y
                self.z = z
        
        coord = TestCoord(1e-6, 2e-6, 3e-6)
        json_data = coord.to_json()
        
        expected = {"x": 1e-6, "y": 2e-6, "z": 3e-6}
        assert json_data == expected

    def test_from_json_basic(self):
        """Test JSON deserialization with basic data."""
        class TestCoord(Coord3D):
            def __init__(self, x=0, y=0, z=0):
                self.x = x
                self.y = y
                self.z = z
        
        json_data = {"x": 1.5, "y": 2.7, "z": 3.14}
        coord = TestCoord.from_json(json_data)
        
        assert coord.x == 1.5
        assert coord.y == 2.7
        assert coord.z == 3.14

    def test_from_json_partial_data(self):
        """Test JSON deserialization with partial data (using defaults)."""
        class TestCoord(Coord3D):
            def __init__(self, x=0, y=0, z=0):
                self.x = x
                self.y = y
                self.z = z
        
        json_data = {"x": 5.0}
        coord = TestCoord.from_json(json_data)
        
        assert coord.x == 5.0
        assert coord.y == 0.0  # Default value
        assert coord.z == 0.0  # Default value

    def test_from_json_empty_data(self):
        """Test JSON deserialization with empty data."""
        class TestCoord(Coord3D):
            def __init__(self, x=0, y=0, z=0):
                self.x = x
                self.y = y
                self.z = z
        
        json_data = {}
        coord = TestCoord.from_json(json_data)
        
        assert coord.x == 0.0
        assert coord.y == 0.0
        assert coord.z == 0.0

    def test_from_json_missing_coordinates(self):
        """Test JSON deserialization with missing coordinates."""
        class TestCoord(Coord3D):
            def __init__(self, x=0, y=0, z=0):
                self.x = x
                self.y = y
                self.z = z
        
        # Missing y coordinate
        json_data = {"x": 1.0, "z": 3.0}
        coord = TestCoord.from_json(json_data)
        
        assert coord.x == 1.0
        assert coord.y == 0.0  # Default
        assert coord.z == 3.0

    def test_from_json_negative_coordinates(self):
        """Test JSON deserialization with negative coordinates."""
        class TestCoord(Coord3D):
            def __init__(self, x=0, y=0, z=0):
                self.x = x
                self.y = y
                self.z = z
        
        json_data = {"x": -1.5, "y": -2.7, "z": -3.14}
        coord = TestCoord.from_json(json_data)
        
        assert coord.x == -1.5
        assert coord.y == -2.7
        assert coord.z == -3.14

    def test_from_json_zero_coordinates(self):
        """Test JSON deserialization with zero coordinates."""
        class TestCoord(Coord3D):
            def __init__(self, x=0, y=0, z=0):
                self.x = x
                self.y = y
                self.z = z
        
        json_data = {"x": 0, "y": 0, "z": 0}
        coord = TestCoord.from_json(json_data)
        
        assert coord.x == 0
        assert coord.y == 0
        assert coord.z == 0

    def test_from_json_integer_coordinates(self):
        """Test JSON deserialization with integer coordinates."""
        class TestCoord(Coord3D):
            def __init__(self, x=0, y=0, z=0):
                self.x = x
                self.y = y
                self.z = z
        
        json_data = {"x": 1, "y": 2, "z": 3}
        coord = TestCoord.from_json(json_data)
        
        assert coord.x == 1
        assert coord.y == 2
        assert coord.z == 3

    def test_from_json_float_coordinates(self):
        """Test JSON deserialization with float coordinates."""
        class TestCoord(Coord3D):
            def __init__(self, x=0, y=0, z=0):
                self.x = x
                self.y = y
                self.z = z
        
        json_data = {"x": 1.1, "y": 2.2, "z": 3.3}
        coord = TestCoord.from_json(json_data)
        
        assert coord.x == 1.1
        assert coord.y == 2.2
        assert coord.z == 3.3

    def test_from_json_large_coordinates(self):
        """Test JSON deserialization with large coordinates."""
        class TestCoord(Coord3D):
            def __init__(self, x=0, y=0, z=0):
                self.x = x
                self.y = y
                self.z = z
        
        json_data = {"x": 1e10, "y": 2e10, "z": 3e10}
        coord = TestCoord.from_json(json_data)
        
        assert coord.x == 1e10
        assert coord.y == 2e10
        assert coord.z == 3e10

    def test_from_json_small_coordinates(self):
        """Test JSON deserialization with very small coordinates."""
        class TestCoord(Coord3D):
            def __init__(self, x=0, y=0, z=0):
                self.x = x
                self.y = y
                self.z = z
        
        json_data = {"x": 1e-10, "y": 2e-10, "z": 3e-10}
        coord = TestCoord.from_json(json_data)
        
        assert coord.x == 1e-10
        assert coord.y == 2e-10
        assert coord.z == 3e-10

    def test_json_roundtrip(self):
        """Test JSON serialization and deserialization roundtrip."""
        class TestCoord(Coord3D):
            def __init__(self, x=0, y=0, z=0):
                self.x = x
                self.y = y
                self.z = z
            
            def __eq__(self, other):
                return (self.x == other.x and 
                       self.y == other.y and 
                       self.z == other.z)
        
        original = TestCoord(1.25, 2.75, 3.125)
        json_data = original.to_json()
        restored = TestCoord.from_json(json_data)
        
        assert original == restored

    def test_json_roundtrip_edge_values(self):
        """Test JSON roundtrip with edge values."""
        class TestCoord(Coord3D):
            def __init__(self, x=0, y=0, z=0):
                self.x = x
                self.y = y
                self.z = z
            
            def __eq__(self, other):
                return (self.x == other.x and 
                       self.y == other.y and 
                       self.z == other.z)
        
        test_values = [
            (0, 0, 0),
            (-1, -1, -1),
            (1e10, 1e10, 1e10),
            (1e-10, 1e-10, 1e-10),
            (3.14159, 2.71828, 1.41421)
        ]
        
        for x, y, z in test_values:
            original = TestCoord(x, y, z)
            json_data = original.to_json()
            restored = TestCoord.from_json(json_data)
            assert original == restored

    def test_from_json_invalid_data_types(self):
        """Test JSON deserialization with invalid data types."""
        class TestCoord(Coord3D):
            def __init__(self, x=0, y=0, z=0):
                self.x = x
                self.y = y
                self.z = z
        
        # Test with string values (should use defaults)
        json_data = {"x": "invalid", "y": "also_invalid", "z": "still_invalid"}
        coord = TestCoord.from_json(json_data)
        
        # Should use default values when conversion fails
        assert coord.x == 0.0
        assert coord.y == 0.0
        assert coord.z == 0.0

    def test_from_json_none_values(self):
        """Test JSON deserialization with None values."""
        class TestCoord(Coord3D):
            def __init__(self, x=0, y=0, z=0):
                self.x = x
                self.y = y
                self.z = z
        
        json_data = {"x": None, "y": None, "z": None}
        coord = TestCoord.from_json(json_data)
        
        # Should use default values for None
        assert coord.x == 0.0
        assert coord.y == 0.0
        assert coord.z == 0.0

    def test_from_json_mixed_valid_invalid(self):
        """Test JSON deserialization with mix of valid and invalid data."""
        class TestCoord(Coord3D):
            def __init__(self, x=0, y=0, z=0):
                self.x = x
                self.y = y
                self.z = z
        
        json_data = {"x": 5.0, "y": "invalid", "z": 10.0}
        coord = TestCoord.from_json(json_data)
        
        assert coord.x == 5.0
        assert coord.y == 0.0  # Default for invalid
        assert coord.z == 10.0

    def test_inheritance_with_point3d(self):
        """Test that Point3D properly inherits from Coord3D."""
        from Point import Point3D
        
        point = Point3D(1, 2, 3)
        
        # Should have inherited to_json method
        json_data = point.to_json()
        assert json_data == {"x": 1, "y": 2, "z": 3}
        
        # Should have inherited from_json method
        restored = Point3D.from_json(json_data)
        assert restored == point

    def test_inheritance_with_vector3d(self):
        """Test that Vector3D properly inherits from Coord3D."""
        from Vector import Vector3D
        
        vector = Vector3D(1, 2, 3)
        
        # Should have inherited to_json method
        json_data = vector.to_json()
        assert json_data == {"x": 1, "y": 2, "z": 3}
        
        # Should have inherited from_json method
        restored = Vector3D.from_json(json_data)
        assert restored == vector

    def test_type_annotations(self):
        """Test that type annotations are properly defined."""
        # Check that the class has the expected type annotations
        assert hasattr(Coord3D, '__annotations__')
        annotations = Coord3D.__annotations__
        
        # Should have annotations for x, y, z
        assert 'x' in annotations
        assert 'y' in annotations
        assert 'z' in annotations
        
        # Check that they're annotated as float
        assert annotations['x'] == float
        assert annotations['y'] == float
        assert annotations['z'] == float

    def test_json_serializable_inheritance(self):
        """Test that Coord3D properly inherits from JsonSerializable."""
        from JsonSerializable import JsonSerializable
        
        # Coord3D should be a subclass of JsonSerializable
        assert issubclass(Coord3D, JsonSerializable)

    def test_abstract_base_class_behavior(self):
        """Test that Coord3D behaves as an abstract base class."""
        # Coord3D should be instantiable but is meant to be subclassed
        # This test ensures the basic structure is correct
        
        class ConcreteCoord(Coord3D):
            def __init__(self, x=0, y=0, z=0):
                self.x = x
                self.y = y
                self.z = z
        
        coord = ConcreteCoord(1, 2, 3)
        assert coord.x == 1
        assert coord.y == 2
        assert coord.z == 3
        
        # Should have inherited methods
        assert hasattr(coord, 'to_json')
        assert hasattr(coord, 'from_json')

    def test_json_method_return_types(self):
        """Test that JSON methods return correct types."""
        class TestCoord(Coord3D):
            def __init__(self, x=0, y=0, z=0):
                self.x = x
                self.y = y
                self.z = z
        
        coord = TestCoord(1.5, 2.5, 3.5)
        
        # to_json should return a dictionary
        json_data = coord.to_json()
        assert isinstance(json_data, dict)
        assert len(json_data) == 3
        assert all(key in json_data for key in ['x', 'y', 'z'])
        
        # from_json should return an instance of the class
        restored = TestCoord.from_json(json_data)
        assert isinstance(restored, TestCoord)

    def test_coordinate_precision(self):
        """Test that coordinate precision is maintained through JSON operations."""
        class TestCoord(Coord3D):
            def __init__(self, x=0, y=0, z=0):
                self.x = x
                self.y = y
                self.z = z
        
        # Test with high precision values
        precise_values = [
            3.141592653589793,
            2.718281828459045,
            1.4142135623730951
        ]
        
        coord = TestCoord(*precise_values)
        json_data = coord.to_json()
        restored = TestCoord.from_json(json_data)
        
        # Precision should be maintained
        assert coord.x == restored.x
        assert coord.y == restored.y
        assert coord.z == restored.z

    def test_edge_case_extreme_values(self):
        """Test with extreme coordinate values."""
        class TestCoord(Coord3D):
            def __init__(self, x=0, y=0, z=0):
                self.x = x
                self.y = y
                self.z = z
        
        # Test with very large and very small values
        extreme_coord = TestCoord(1e308, -1e308, 1e-308)
        json_data = extreme_coord.to_json()
        restored = TestCoord.from_json(json_data)
        
        assert extreme_coord.x == restored.x
        assert extreme_coord.y == restored.y
        assert extreme_coord.z == restored.z