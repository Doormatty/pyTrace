import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Scene import Scene
from Primitives import Sphere, Plane, Cube
from Material import Material
from RGB import RGB
from Point import Point3D
from Vector import Vector3D

def main():
    # Create a new scene
    scene = Scene("Export Example Scene")

    # Add some objects
    scene.add_object(Sphere(
        Point3D(0, 0, 0),
        50,
        Material(RGB(1.0, 0.0, 0.0), reflect=0.5)  # Red reflective sphere
    ))

    scene.add_object(Plane(
        Point3D(0, 100, 0),
        Vector3D(0, -1, 0),
        Material(RGB(0.2, 0.2, 0.2), reflect=0.1)  # Gray floor plane
    ))

    scene.add_object(Cube(
        Point3D(-50, -50, -50),
        Point3D(50, 50, 50),
        Material(RGB(0.0, 0.0, 1.0))  # Blue cube
    ))

    # Export the scene to a JSON file
    scene.export_to_json("example_scene.json")
    print(f"Scene exported to example_scene.json")

if __name__ == "__main__":
    main()
