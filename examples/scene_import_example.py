import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Scene import Scene

def main():
    # Import a scene from a JSON file
    try:
        scene = Scene.import_from_json("example_scene.json")
        print(f"Scene '{scene.name}' imported with {len(scene)} objects")

        # Print information about all objects in the scene
        for i, obj in enumerate(scene):
            print(f"Object {i}: {obj}")

        # You could render the scene here using the RayTracer
        # from main import RayTracer
        # raytracer = RayTracer()
        # raytracer.render(scene)

    except FileNotFoundError:
        print("Error: example_scene.json not found. Run scene_export_example.py first.")
    except Exception as e:
        print(f"Error importing scene: {e}")

if __name__ == "__main__":
    main()
