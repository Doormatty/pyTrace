import sys
import os

# Add the parent directory to the path so we can import the modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from Scene import Scene
from Terrain import Terrain
from Material import Material
from RGB import RGB
from Point import Point3D


def main():
    """
    Example script demonstrating the Terrain class.
    
    This script creates a terrain object and adds it to a scene,
    then exports the scene to a JSON file.
    """
    # Create a scene
    scene = Scene(name="Terrain Example")
    
    # Create a material for the terrain
    terrain_material = Material(
        color=RGB(0.2, 0.8, 0.2),  # Green color
        reflect=0.1,
        roughness=(0.1, 0.5)
    )
    
    # Create a terrain object
    terrain = Terrain(
        noise_scale=0.2,           # Scale of the noise pattern
        noise_amplitude=1.0,       # Height multiplier for the noise
        cube_size=0.5,             # Size of each cube
        gap_distance=0.1,          # Gap between cubes
        width=10.0,                # Total width of the terrain
        depth=10.0,                # Total depth of the terrain
        height=5.0,                # Maximum height of the terrain
        location=Point3D(0, 0, 0), # Center of the terrain
        material=terrain_material  # Material for the cubes
    )
    
    # Add the terrain to the scene
    # Note: This adds all the individual cubes to the scene
    terrain.add_to_scene(scene)
    
    # Print information about the terrain
    print(f"Created terrain with {len(terrain.cubes)} cubes")
    print(f"Terrain dimensions: {terrain.actual_width} x {terrain.actual_depth}")
    print(f"Number of cubes: {terrain.num_cubes_x} x {terrain.num_cubes_z}")
    
    # Export the scene to a JSON file
    scene.export_to_json("terrain_example.json")
    print(f"Exported scene to terrain_example.json")
    
    # Note: To render this scene, you would need to load it in the main renderer
    print("To render this scene, use:")
    print("  python main.py --scene terrain_example.json")


if __name__ == "__main__":
    main()