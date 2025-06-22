import argparse
import datetime
import os
import random
import sys
import time

# Hide pygame welcome message
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
from pygame.locals import *

from Primitives import *
from RGB import RGB
from Ray import Ray
from Scene import Scene
from Noise import Noise
from Terrain import Terrain


class RayTracer:
    """A ray tracing renderer that can render a scene of 3D objects."""

    def __init__(self,
                 screen_width=900,
                 screen_height=900,
                 field_of_view=90,
                 viewport_z=100,
                 background_color=RGB(0, 0, 0),
                 recursion_limit=80,
                 supersampling=1):  # Added supersampling parameter
        # Store parameters
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.field_of_view = field_of_view
        self.viewport_z = viewport_z
        self.background_color = background_color
        self.recursion_limit = recursion_limit
        self.supersampling = max(1, supersampling)  # Ensure at least 1 sample per pixel

        # Initialize noise generator
        self.noise = Noise()

        # Calculate derived values
        self.aspect_ratio = self.screen_width / self.screen_height
        self.viewport_height = 2 * self.viewport_z * math.tan(math.radians(self.field_of_view / 2))
        self.viewport_width = self.viewport_height * self.aspect_ratio
        self.pixel_size_x = self.viewport_width / self.screen_width
        self.pixel_size_y = self.viewport_height / self.screen_height

    # Cache the light direction vector since it's constant
    _light_direction = Vector3D(0, 0, 1)

    def lighting(self, hit, scene):
        """Calculate lighting at the hit point using cosine shading."""
        # Get material for easier access
        material = hit.object.material

        # If the object is emissive (has luma), return its color directly
        if material.luma > 0:
            return material.color

        # Calculate diffuse component (cosine of the angle between normal and light direction)
        # Use cached light direction vector
        shade = max(0, self._light_direction * hit.normal)

        # Optimization: Create RGB directly instead of using multiplication that creates a new object
        color = material.color
        shaded_color = RGB(
            color.r * shade,
            color.g * shade,
            color.b * shade
        )

        return shaded_color

    def _calculate_reflection(self, cast_ray, closest_hit, scene, recursion_depth):
        """Calculate reflection for a ray intersection."""
        material = closest_hit.object.material

        # Calculate reflection direction using: R = V - 2(N·V)N
        dot_product = closest_hit.normal * cast_ray.dest

        # Create reflect_ray
        reflect_ray = Ray()
        reflect_ray.origin = closest_hit.hit_point

        # Avoid creating temporary objects in reflection calculation
        double_dot = 2.0 * dot_product
        reflect_dir = Vector3D(
            cast_ray.dest.x - double_dot * closest_hit.normal.x,
            cast_ray.dest.y - double_dot * closest_hit.normal.y,
            cast_ray.dest.z - double_dot * closest_hit.normal.z
        ).normalize()

        # Apply roughness if present - adds perturbation to reflection direction using 3D noise
        roughness_scale, roughness_amplitude = material.roughness
        if roughness_amplitude > 0:
            # Get hit point coordinates for noise sampling
            hit_x = closest_hit.hit_point.x
            hit_y = closest_hit.hit_point.y
            hit_z = closest_hit.hit_point.z

            # Sample 3D noise at hit point position (with slight offsets for each dimension)
            # This creates locally consistent roughness
            noise_x = self.noise.noise3d(hit_x, hit_y, hit_z, roughness_scale)
            noise_y = self.noise.noise3d(hit_x + 42.5, hit_y + 13.7, hit_z + 91.3, roughness_scale)
            noise_z = self.noise.noise3d(hit_x + 79.3, hit_y + 36.2, hit_z + 63.7, roughness_scale)

            # Convert from 0-1 range to -amplitude to +amplitude range
            random_factor = roughness_amplitude * 2.0
            random_x = (noise_x * random_factor - roughness_amplitude)
            random_y = (noise_y * random_factor - roughness_amplitude)
            random_z = (noise_z * random_factor - roughness_amplitude)

            # Avoid creating temporary Vector3D for perturbation
            reflect_dir = Vector3D(
                reflect_dir.x + random_x,
                reflect_dir.y + random_y,
                reflect_dir.z + random_z
            ).normalize()

        reflect_ray.dest = reflect_dir

        # Recursively trace the reflection ray
        reflect_color = self.raytrace(reflect_ray, scene, recursion_depth - 1)

        # Combine direct lighting with reflection
        direct_lighting = self.lighting(closest_hit, scene)
        reflect_factor = material.reflect

        return RGB(
            direct_lighting.r + (reflect_color.r * reflect_factor),
            direct_lighting.g + (reflect_color.g * reflect_factor),
            direct_lighting.b + (reflect_color.b * reflect_factor)
        )

    def _find_closest_intersection(self, cast_ray, scene):
        """Find the closest intersection between a ray and scene objects."""
        hit_distance = float('inf')
        closest_hit = None

        # Use a local variable for scene objects to avoid attribute lookup
        scene_objects = scene.objects if hasattr(scene, 'objects') else scene

        for obj in scene_objects:
            if intersection := obj.hit(cast_ray):
                # Use distance_squared to avoid square root calculation
                current_distance = cast_ray.origin.distance_squared(intersection.hit_point)
                if current_distance < hit_distance:
                    hit_distance = current_distance
                    closest_hit = intersection

        return closest_hit

    def raytrace(self, cast_ray, scene, recursion_depth=None) -> RGB:
        """Trace a ray through the scene and return the resulting color."""
        # Use default recursion depth if not specified
        if recursion_depth is None:
            recursion_depth = self.recursion_limit

        # Find the closest intersection
        closest_hit = self._find_closest_intersection(cast_ray, scene)

        # If no intersection, return background color
        if not closest_hit:
            return self.background_color

        # Base case: reached recursion limit
        if recursion_depth <= 1:
            return self.lighting(closest_hit, scene)

        # Handle reflections if the material is reflective
        material = closest_hit.object.material
        if material.reflect > 0:
            return self._calculate_reflection(cast_ray, closest_hit, scene, recursion_depth)
        else:
            # Object isn't reflective, just return direct lighting
            return self.lighting(closest_hit, scene)

    def _setup_ray_for_pixel(self, ray, x, y, width, height, pixel_size_x, pixel_size_y, viewport_z, offset_x=0.0, offset_y=0.0):
        """Set up ray for a specific pixel with optional subpixel offsets for supersampling."""
        ray.origin.x = pixel_size_x * (x - 0.5 * (width - 1) + offset_x)
        ray.origin.y = pixel_size_y * (0.5 * (height - 1) - y + offset_y)
        ray.origin.z = viewport_z
        ray.dest = Vector3D(0, 0, -1)

    def _supersample_pixel(self, ray, x, y, width, height, pixel_size_x, pixel_size_y, viewport_z, scene):
        """Take multiple samples for a single pixel and average the results."""
        # If supersampling is 1, just take a single sample at the center of the pixel
        if self.supersampling == 1:
            self._setup_ray_for_pixel(ray, x, y, width, height, pixel_size_x, pixel_size_y, viewport_z)
            return self.raytrace(ray, scene)

        # For supersampling, take multiple samples and average them
        total_r = 0.0
        total_g = 0.0
        total_b = 0.0
        samples = self.supersampling * self.supersampling  # Total number of samples

        # Calculate step size for the grid
        step = 1.0 / self.supersampling

        # Take samples in a grid pattern
        for sy in range(self.supersampling):
            for sx in range(self.supersampling):
                # Calculate offset within the pixel (from -0.5 to 0.5)
                offset_x = (sx + 0.5) * step - 0.5
                offset_y = (sy + 0.5) * step - 0.5

                # Set up ray for this sample
                self._setup_ray_for_pixel(ray, x, y, width, height, pixel_size_x, pixel_size_y, viewport_z, offset_x, offset_y)

                # Trace the ray and accumulate the color
                color = self.raytrace(ray, scene)
                total_r += color.r
                total_g += color.g
                total_b += color.b

        # Average the colors
        return RGB(total_r / samples, total_g / samples, total_b / samples)

    def render_chunk(self, scene, y_start, y_end, width, height, pixel_size_x, pixel_size_y, viewport_z):
        """Render a chunk of the scene (for parallel processing)."""
        chunk_buffer = []
        ray = Ray(Point3D(0, 0, viewport_z), Vector3D(0, 0, -1))

        # Render each pixel in the chunk
        for y in range(y_start, y_end):
            row = []
            for x in range(width):
                color = self._supersample_pixel(ray, x, y, width, height, pixel_size_x, pixel_size_y, viewport_z, scene).finalcolor()
                row.append(color)
            chunk_buffer.append(row)

        return chunk_buffer

    def render(self, scene):
        """Render the scene using ray tracing with optional multi-threading."""
        # Initialize pygame
        pygame.init()
        window = pygame.display.set_mode((self.screen_width, self.screen_height))
        pixels = pygame.PixelArray(window)
        pygame.display.set_caption("PyTrace - Rendering in Progress...")
        pygame.event.set_allowed(pygame.QUIT)

        start_time = time.time()

        # Determine if we should use multi-threading
        use_threading = False
        try:
            import multiprocessing
            # Only use threading if we have more than 1 CPU
            if multiprocessing.cpu_count() > 1:
                use_threading = True
        except (ImportError, NotImplementedError):
            # If multiprocessing is not available, fall back to single-threaded
            use_threading = False

        if use_threading:
            # Multi-threaded rendering
            try:
                import concurrent.futures

                # Determine number of threads (use CPU count - 1 to leave one CPU for system)
                num_threads = max(1, multiprocessing.cpu_count() - 1)

                # Calculate chunk size (divide image into horizontal strips)
                chunk_size = max(1, self.screen_height // num_threads)

                # Create chunks
                chunks = []
                for i in range(0, self.screen_height, chunk_size):
                    y_start = i
                    y_end = min(i + chunk_size, self.screen_height)
                    chunks.append((y_start, y_end))

                # Render chunks in parallel
                with concurrent.futures.ProcessPoolExecutor(max_workers=num_threads) as executor:
                    # Submit rendering tasks
                    futures = [
                        executor.submit(
                            self.render_chunk,
                            scene,
                            chunk[0], chunk[1],
                            self.screen_width, self.screen_height,
                            self.pixel_size_x, self.pixel_size_y, self.viewport_z
                        )
                        for chunk in chunks
                    ]

                    # Create a mapping of futures to their chunk indices
                    future_to_chunk_idx = {future: i for i, future in enumerate(futures)}

                    # Process results as they complete
                    for future in concurrent.futures.as_completed(futures):
                        # Get the correct chunk index for this future
                        chunk_idx = future_to_chunk_idx[future]
                        chunk_buffer = future.result()
                        y_start = chunks[chunk_idx][0]

                        # Copy chunk data to pixel array
                        for y_offset, row in enumerate(chunk_buffer):
                            y = y_start + y_offset
                            for x, color in enumerate(row):
                                pixels[x, y] = color

                        # Update display after each chunk
                        pygame.display.update()

                        # Check for quit events
                        self._handle_quit_events(window)

            except (ImportError, Exception) as e:
                # Fall back to single-threaded if there's any error
                print(f"Multi-threading failed: {e}. Falling back to single-threaded rendering.")
                self._render_single_threaded(scene, window, pixels)
        else:
            # Single-threaded rendering
            self._render_single_threaded(scene, window, pixels)

        # Clean up and save result
        del pixels

        # Calculate and display rendering time
        render_time = time.time() - start_time
        pygame.display.set_caption(f"PyTrace Render Complete - Time: {render_time:.2f} seconds")
        print(f'Rendering time: {render_time:.2f} seconds')

        # Wait for user to close window
        pygame.event.set_allowed((pygame.QUIT, pygame.KEYDOWN))
        self.wait_for_exit(window)

    def _render_single_threaded(self, scene, window, pixels):
        """Render the scene using a single thread."""
        # Setup primary ray for rendering
        ray = Ray(Point3D(0, 0, self.viewport_z), Vector3D(0, 0, -1))

        # Render each pixel
        for y in range(self.screen_height):
            # Check for quit events during rendering
            self._handle_quit_events(window)

            for x in range(self.screen_width):
                # Use supersampling to get the pixel color
                pixels[x, y] = self._supersample_pixel(
                    ray, x, y,
                    self.screen_width, self.screen_height,
                    self.pixel_size_x, self.pixel_size_y,
                    self.viewport_z, scene
                ).finalcolor()

            # Update display after each scanline
            pygame.display.update()

    def save_image(self, window_surface):
        """Save the rendered image with timestamp filename."""
        timestamp = datetime.datetime.strftime(datetime.datetime.now(), "%H.%M.%S_%d-%b-%Y")
        filename = f"render_{timestamp}.png"
        pygame.image.save(window_surface, filename)
        print(f"Image saved as: {filename}")

    def _handle_quit_events(self, window_surface):
        """Handle quit events and save the image if needed."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.save_image(window_surface)
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.event.post(pygame.event.Event(QUIT))

    def wait_for_exit(self, window_surface):
        """Wait for user to quit or press ESC."""
        while True:
            self._handle_quit_events(window_surface)


def create_terrain():
    scene = Scene("Terrain Scene")
    # Create a material for the terrain
    terrain_material = Material(
        color=RGB(0.2, 0.8, 0.2),  # Green color
        reflect=0.1,
        roughness=(0.1, 0.5)
    )

    # Create a terrain object
    terrain = Terrain(
        noise_scale=0.2,  # Scale of the noise pattern
        noise_amplitude=1.0,  # Height multiplier for the noise
        cube_size=10,  # Size of each cube
        gap_distance=0.1,  # Gap between cubes
        width=100.0,  # Total width of the terrain
        depth=100.0,  # Total depth of the terrain
        height=40.0,  # Maximum height of the terrain
        location=Point3D(0, 0, 0),  # Center of the terrain
        material=terrain_material  # Material for the cubes
    )

    # Add the terrain to the scene
    # Note: This adds all the individual cubes to the scene
    terrain.add_to_scene(scene)
    return scene


def create_scene():
    """Create and return the scene with all objects."""
    scene = Scene("Default Scene")

    # Red sphere on the right with reflection and high roughness
    scene.add_object(Sphere(
        Point3D(50, -50, 1),
        70,
        Material(RGB(0.5, 0, 0), 1.0, 0.7, 0.0)  # (scale, amplitude)
    ))

    # Green sphere on the left with reflection and medium roughness
    scene.add_object(Sphere(
        Point3D(-50, -50, 1),
        70,
        Material(RGB(0, 0.5, 0), 1.0, 0.7, 0.0)  # (scale, amplitude)
    ))

    # Blue sphere on the top with reflection and no roughness (smooth)
    scene.add_object(Sphere(
        Point3D(1, 50, 1),
        70,
        Material(RGB(0, 0, 0.5), 1.0, 0.7, 0.0)  # (scale, amplitude)
    ))

    # Uncomment to add more objects to the scene

    # White light source
    # scene.add_object(Sphere(
    #     Point3D(0, 0, 0), 
    #     30, 
    #     Material(RGB(1.0, 1.0, 1.0), 1.0, 0.0, 1.0, (0.1, 0.0))  # (scale, amplitude)
    # ))

    # Ground plane
    # scene.add_object(Plane(
    #     Point3D(0, 100, 0), 
    #     Vector3D(0, -1, 0), 
    #     Material(RGB(0.3, 0.3, 0.3), 1.0, 0.2, 0.0, (0.1, 0.2))  # (scale, amplitude)
    # ))

    return scene



if __name__ == "__main__":
    # Initialize random seed
    random.seed()

    # Set up argument parser
    parser = argparse.ArgumentParser(
        description='PyTrace - A Python Ray Tracer',
        epilog='''
Examples:
  python main.py                                # Run with default settings
  python main.py --width 1280 --height 720      # Render at 720p resolution
  python main.py -w 1920 -h 1080 -s 4           # Render at 1080p with 4x supersampling
  python main.py --bg-r 0.2 --bg-g 0.3 --bg-b 0.4  # Set custom background color
        '''
    )
    def positive_int(value):
        ivalue = int(value)
        if ivalue <= 0:
            raise argparse.ArgumentTypeError(f"Value must be a positive integer, got {value}")
        return ivalue

    def fov_range(value):
        fvalue = float(value)
        if fvalue <= 0 or fvalue >= 180:
            raise argparse.ArgumentTypeError(f"Field of view must be between 1 and 179 degrees, got {value}")
        return fvalue

    def positive_float(value):
        fvalue = float(value)
        if fvalue <= 0:
            raise argparse.ArgumentTypeError(f"Value must be positive, got {value}")
        return fvalue


    parser.add_argument('-w', '--width', type=positive_int, default=900, help='Screen width in pixels (default: 900)')
    parser.add_argument('-t', '--height', type=positive_int, default=900, help='Screen height in pixels (default: 900)')
    parser.add_argument('-f', '--fov', type=fov_range, default=90, help='Field of view in degrees (1-179) (default: 90)')
    parser.add_argument('-z', '--viewport-z', type=positive_float, default=100, help='Viewport Z distance (default: 100)')

    def color_component(value):
        value = float(value)
        if value < 0.0 or value > 1.0:
            raise argparse.ArgumentTypeError(f"Color component must be between 0.0 and 1.0, got {value}")
        return value


    parser.add_argument('--bg-r', type=color_component, default=0.0, help='Background color red component (0.0-1.0) (default: 0.0)')
    parser.add_argument('--bg-g', type=color_component, default=0.0, help='Background color green component (0.0-1.0) (default: 0.0)')
    parser.add_argument('--bg-b', type=color_component, default=0.0, help='Background color blue component (0.0-1.0) (default: 0.0)')
    parser.add_argument('-r', '--recursion-limit', type=positive_int, default=80, help='Maximum recursion depth for ray tracing (default: 80)')

    def supersampling_level(value):
        ivalue = positive_int(value)
        if ivalue < 1 or ivalue > 4:
            raise argparse.ArgumentTypeError(f"Supersampling level must be between 1 and 4, got {value}")
        return ivalue


    parser.add_argument('-s', '--supersampling', type=supersampling_level, default=1, help='Supersampling level for anti-aliasing (1-4) (default: 1)')

    # Parse arguments
    args = parser.parse_args()

    # Create a scene
    scene = create_scene()

    # Create background color from RGB components
    background_color = RGB(args.bg_r, args.bg_g, args.bg_b)

    # Create a raytracer with the parsed arguments
    raytracer = RayTracer(
        screen_width=args.width,
        screen_height=args.height,
        field_of_view=args.fov,
        viewport_z=args.viewport_z,
        background_color=background_color,
        recursion_limit=args.recursion_limit,
        supersampling=args.supersampling
    )

    # Render the scene
    raytracer.render(scene)
