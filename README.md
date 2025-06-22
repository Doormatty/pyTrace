# pyTrace

A raytracer written in Python from scratch with minimal external dependencies.

## Description

pyTrace is a simple ray tracing engine that can render spheres, planes, and cubes with reflections and lighting effects. The program uses only pygame for window management and rendering the final image.

## Features

- Primitive shapes: Spheres, Planes, and Cubes
- Procedural terrain generation using noise maps
- Reflective materials
- Diffuse lighting
- Supersampling anti-aliasing
- Save rendered images automatically

## Requirements

- Python 3.x
- pygame

## Usage

Simply run the main.py file to generate a ray-traced image:

```bash
python main.py
```

The rendered image will be saved automatically with a timestamp filename.

Press ESC or close the window to exit the program after rendering.

## Customization

You can modify the scene by editing the `create_scene()` function in main.py. Uncomment some of the examples or create your own objects.

### Screen Resolution and Field of View

You can change the screen resolution by modifying `SCREEN_WIDTH` and `SCREEN_HEIGHT` constants in main.py. The renderer uses a proper perspective projection based on:

- Field of view (FOV): Controls the angular extent of the scene visible on screen (default: 60°)
- Aspect ratio: Automatically calculated from screen dimensions
- Viewport scaling: Maintains correct object sizes across different resolutions

You can adjust the `FIELD_OF_VIEW` constant to change the perspective - higher values give a wider angle view, while lower values create a more telephoto/zoomed effect.

### Supersampling Anti-Aliasing

The renderer supports supersampling anti-aliasing to reduce jagged edges and improve image quality. You can control the level of supersampling when creating the RayTracer instance:

```python
# Create a raytracer with 2x2 supersampling (4 samples per pixel)
raytracer = RayTracer(supersampling=2)

# For higher quality (9 samples per pixel)
raytracer = RayTracer(supersampling=3)

# For even higher quality (16 samples per pixel)
raytracer = RayTracer(supersampling=4)
```

The supersampling parameter controls the number of samples taken per pixel:
- `supersampling=1`: No supersampling (1 sample per pixel)
- `supersampling=2`: 4 samples per pixel (2x2 grid)
- `supersampling=3`: 9 samples per pixel (3x3 grid)
- `supersampling=4`: 16 samples per pixel (4x4 grid)

Higher values produce smoother edges but increase rendering time significantly. For a good balance between quality and performance, a value of 2 is recommended.

### Terrain Generation

The renderer supports procedural terrain generation using noise maps. The Terrain class creates a voxel terrain using cube objects based on a 2D noise map. You can customize the terrain with the following parameters:

```python
terrain = Terrain(
    noise_scale=0.2,           # Scale of the noise pattern (smaller = more zoomed out)
    noise_amplitude=1.0,       # Height multiplier for the noise values
    cube_size=0.5,             # Size of each cube (single side)
    gap_distance=0.1,          # Gap between adjacent cubes
    width=10.0,                # Total width of the terrain (X axis)
    depth=10.0,                # Total depth of the terrain (Z axis)
    height=5.0,                # Maximum height of the terrain (Y axis)
    location=Point3D(0, 0, 0), # Center point of the bottom face of the terrain
    material=terrain_material, # Material for the cubes
    seed=42                    # Optional seed for the noise generator
)

# Add the terrain to a scene
terrain.add_to_scene(scene)
```

For a complete example of terrain generation, see the `examples/terrain_example.py` script.

## Performance

The renderer is implemented in pure Python without optimization, so it can be quite slow for complex scenes. For better performance, consider reducing the screen resolution.

## License

Feel free to use and modify this code for educational purposes.

-Matt
