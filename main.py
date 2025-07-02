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


class RayTracer:
    """A ray tracing renderer that can render a scene of 3D objects."""

    def __init__(self,
                 screen_width=600,
                 screen_height=600,
                 recursion_limit=4,
                 supersampling=2,
                 ascii_mode=False,
                 ascii_only_mode=False,
                 downsample_factor=4):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.recursion_limit = recursion_limit
        self.supersampling = max(1, supersampling)  # Ensure at least 1 sample per pixel
        self.ascii_mode = ascii_mode
        self.ascii_only_mode = ascii_only_mode
        self.downsample_factor = downsample_factor

        # Initialize noise generator
        self.noise = Noise()

        # Calculate aspect ratio (other derived values will be calculated per scene)
        self.aspect_ratio = self.screen_width / self.screen_height

    def _calculate_scene_parameters(self, scene):
        """Calculate derived parameters from scene settings."""
        # Use the camera's viewport parameter calculation
        return scene.camera.calculate_viewport_parameters(self.screen_width, self.screen_height)

    def lighting(self, hit, scene):
        """Calculate lighting at the hit point using ambient lighting."""
        material = hit.material if hit.material else hit.object.material

        # If the object is emissive (has luma), return its color directly
        if material.luma > 0:
            return material.color

        # Check if there is ambient lighting available
        has_ambient_light = (hasattr(scene, 'ambient_intensity') and
                             scene.ambient_intensity > 0)

        # If no ambient light, return black
        if not has_ambient_light:
            return RGB(0, 0, 0)

        # Apply ambient lighting (omnidirectional, no directional component)
        ambient_color = scene.ambient_color if hasattr(scene, 'ambient_color') else RGB(1.0, 1.0, 1.0)
        ambient_contribution = material.color * ambient_color * scene.ambient_intensity

        return ambient_contribution

    def global_illumination_lighting(self, hit, scene):
        """Calculate lighting by iterating over all objects with reflect>0 or luma>0."""
        material = hit.material if hit.material else hit.object.material

        # If the object is emissive (has luma), return its color directly
        if material.luma > 0:
            return material.color

        # Check if there is ambient lighting available
        has_ambient_light = (hasattr(scene, 'ambient_intensity') and scene.ambient_intensity > 0)

        # Find all objects that can contribute light (reflect > 0 or luma > 0)
        light_sources = []

        for obj in scene.objects:
            if obj != hit.object and hasattr(obj, 'material') and obj.material is not None:
                obj_material = obj.material
                if obj_material.reflect > 0 or obj_material.luma > 0:
                    light_sources.append(obj)

        # If no light sources at all (no ambient light and no emissive/reflective objects), return black
        if not has_ambient_light and len(light_sources) == 0:
            return RGB(0, 0, 0)

        # Start with ambient lighting from scene
        if has_ambient_light:
            # Apply ambient lighting (omnidirectional, no directional component)
            ambient_color = scene.ambient_color if hasattr(scene, 'ambient_color') else RGB(1.0, 1.0, 1.0)
            ambient_contribution = material.color * ambient_color * scene.ambient_intensity * 0.3  # Scale ambient contribution
            accumulated_color = ambient_contribution
        else:
            # No ambient lighting, start with black
            accumulated_color = RGB(0, 0, 0)

        # Cast rays to each light source and accumulate lighting
        for light_obj in light_sources:
            # Get sample points on the light source surface
            sample_points = self._get_surface_sample_points(light_obj, num_samples=4)

            for sample_point in sample_points:
                # Create ray from hit point to sample point
                light_ray = Ray()
                light_ray.origin = hit.hit_point
                light_direction_to_sample = (sample_point - hit.hit_point).normalize()
                light_ray.dest = light_direction_to_sample

                # Check if the ray is blocked by other objects
                if not self._is_ray_blocked(light_ray, scene, light_obj, hit.object, hit.hit_point.distance(sample_point)):
                    # Calculate lighting contribution
                    light_intensity = max(0, light_direction_to_sample * hit.normal)

                    if light_intensity > 0:
                        # Distance falloff
                        distance = hit.hit_point.distance(sample_point)
                        falloff = 1.0 / (1.0 + distance * distance * 0.01)  # Quadratic falloff with scaling

                        # Determine light color based on object properties
                        if light_obj.material.luma > 0:
                            # Emissive object - use its color scaled by luma
                            light_color = light_obj.material.color * light_obj.material.luma
                        else:
                            # Reflective object - use a portion of its color scaled by reflectivity
                            light_color = light_obj.material.color * light_obj.material.reflect * 0.5

                        # Add contribution (multiply by material color to get proper surface color)
                        contribution = material.color * light_color * light_intensity * falloff * (1.0 / len(sample_points))
                        accumulated_color = accumulated_color + contribution

        return accumulated_color

    def _get_surface_sample_points(self, obj, num_samples=4):
        """Get sample points on the surface of an object for lighting calculations."""
        from Primitives import Sphere, Plane, Cube, CheckerPlane

        sample_points = []

        if isinstance(obj, Sphere):
            # Sample points on sphere surface
            import math
            for i in range(num_samples):
                # Simple uniform sampling on sphere
                theta = 2 * math.pi * i / num_samples
                phi = math.pi * (i + 0.5) / num_samples

                x = obj.center.x + obj.radius * math.sin(phi) * math.cos(theta)
                y = obj.center.y + obj.radius * math.sin(phi) * math.sin(theta)
                z = obj.center.z + obj.radius * math.cos(phi)

                sample_points.append(Point3D(x, y, z))

        elif isinstance(obj, (Plane, CheckerPlane)):
            # Sample points on plane surface around the plane center
            # Create two perpendicular vectors in the plane
            normal = obj.normal.normalize()

            # Find a vector perpendicular to the normal
            if abs(normal.x) < 0.9:
                tangent1 = Vector3D(1, 0, 0) ^ normal
            else:
                tangent1 = Vector3D(0, 1, 0) ^ normal
            tangent1 = tangent1.normalize()

            tangent2 = normal ^ tangent1
            tangent2 = tangent2.normalize()

            # Sample points in a small area around the plane center
            sample_size = 10.0  # Size of sampling area
            for i in range(num_samples):
                offset1 = (i % 2 - 0.5) * sample_size
                offset2 = (i // 2 - 0.5) * sample_size

                sample_point = Point3D(
                    obj.center.x + offset1 * tangent1.x + offset2 * tangent2.x,
                    obj.center.y + offset1 * tangent1.y + offset2 * tangent2.y,
                    obj.center.z + offset1 * tangent1.z + offset2 * tangent2.z
                )
                sample_points.append(sample_point)

        elif isinstance(obj, Cube):
            # Sample points on cube faces
            # For simplicity, sample the center of each face
            center_x = (obj.a.x + obj.b.x) / 2
            center_y = (obj.a.y + obj.b.y) / 2
            center_z = (obj.a.z + obj.b.z) / 2

            # Sample points on different faces
            faces = [
                Point3D(obj.a.x, center_y, center_z),  # Left face
                Point3D(obj.b.x, center_y, center_z),  # Right face
                Point3D(center_x, obj.a.y, center_z),  # Front face
                Point3D(center_x, obj.b.y, center_z),  # Back face
            ]

            sample_points.extend(faces[:min(num_samples, len(faces))])

        # If no specific sampling method, use object center as fallback
        if not sample_points:
            if hasattr(obj, 'center'):
                sample_points.append(obj.center)
            elif hasattr(obj, 'a') and hasattr(obj, 'b'):
                # Cube center
                center = Point3D((obj.a.x + obj.b.x) / 2, (obj.a.y + obj.b.y) / 2, (obj.a.z + obj.b.z) / 2)
                sample_points.append(center)

        return sample_points

    def _is_ray_blocked(self, ray, scene, target_obj, source_obj, max_distance):
        """Check if a ray is blocked by other objects before reaching the target."""
        scene_objects = scene.objects if hasattr(scene, 'objects') else scene

        for obj in scene_objects:
            if obj != target_obj and obj != source_obj:  # Don't check against target or source object
                intersection = obj.hit(ray)
                if intersection:
                    # Check if intersection is closer than target
                    distance_to_intersection = ray.origin.distance(intersection.hit_point)
                    if distance_to_intersection < max_distance - 0.01:  # Small epsilon for floating point errors
                        return True

        return False

    def _calculate_reflection(self, cast_ray, closest_hit, scene, recursion_depth):
        """Calculate reflection for a ray intersection."""
        material = closest_hit.material if closest_hit.material else closest_hit.object.material

        double_dot = (closest_hit.normal * cast_ray.dest) * 2.0

        reflect_ray = Ray()
        reflect_ray.origin = closest_hit.hit_point

        reflect_dir = Vector3D(cast_ray.dest.x - double_dot * closest_hit.normal.x,
                               cast_ray.dest.y - double_dot * closest_hit.normal.y,
                               cast_ray.dest.z - double_dot * closest_hit.normal.z).normalize()

        roughness_scale, roughness_amplitude = material.roughness
        if roughness_amplitude > 0:
            hit_x = closest_hit.hit_point.x
            hit_y = closest_hit.hit_point.y
            hit_z = closest_hit.hit_point.z

            # Sample 3D noise at hit point position (with slight offsets for each dimension)
            # This creates locally consistent roughness
            noise_x = self.noise.noise3d(hit_x, hit_y, hit_z, roughness_scale)
            noise_y = self.noise.noise3d(hit_z, hit_x, hit_y, roughness_scale)
            noise_z = self.noise.noise3d(hit_y, hit_z, hit_x, roughness_scale)

            # Convert from 0-1 range to -amplitude to +amplitude range
            random_factor = roughness_amplitude * 2.0
            random_x = (noise_x * random_factor - roughness_amplitude)
            random_y = (noise_y * random_factor - roughness_amplitude)
            random_z = (noise_z * random_factor - roughness_amplitude)
            reflect_dir = Vector3D(reflect_dir.x + random_x, reflect_dir.y + random_y, reflect_dir.z + random_z).normalize()

        reflect_ray.dest = reflect_dir

        reflect_color = self.raytrace(reflect_ray, scene, recursion_depth - 1)
        lighting_color = self.global_illumination_lighting(closest_hit, scene)
        reflection_contribution = reflect_color * material.reflect
        combined_color = lighting_color + reflection_contribution

        return combined_color

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

        # Base case: reached recursion limit (changed from <= 1 to <= 0)
        if recursion_depth <= 0:
            # When recursion limit is reached, just return basic lighting without reflections or transparency
            closest_hit = self._find_closest_intersection(cast_ray, scene)
            if not closest_hit:
                background_color = scene.background_color if hasattr(scene, 'background_color') else RGB(0, 0, 0)
                return background_color
            return self.global_illumination_lighting(closest_hit, scene)

        # Find the closest intersection
        closest_hit = self._find_closest_intersection(cast_ray, scene)

        # If no intersection, return background color from scene
        if not closest_hit:
            background_color = scene.background_color if hasattr(scene, 'background_color') else RGB(0, 0, 0)
            return background_color

        # Get material properties
        material = closest_hit.material if closest_hit.material else closest_hit.object.material

        # Handle reflections if the material is reflective
        if material.reflect > 0:
            reflection_color = self._calculate_reflection(cast_ray, closest_hit, scene, recursion_depth)

            # Handle transparency for reflective materials
            if material.opacity < 1.0:
                # Cast a ray through the object to get the background color
                through_ray = Ray()
                through_ray.origin = closest_hit.hit_point
                through_ray.dest = cast_ray.dest
                background_color = self.raytrace(through_ray, scene, recursion_depth - 1)

                # Blend reflection color with background based on opacity
                return reflection_color * material.opacity + background_color * (1.0 - material.opacity)
            else:
                return reflection_color
        else:
            # Object isn't reflective, handle lighting and transparency
            surface_color = self.global_illumination_lighting(closest_hit, scene)

            # Handle transparency/opacity
            if material.opacity < 1.0:
                # Cast a ray through the object to get the background color
                through_ray = Ray()
                through_ray.origin = closest_hit.hit_point
                through_ray.dest = cast_ray.dest
                background_color = self.raytrace(through_ray, scene, recursion_depth - 1)

                # Blend surface color with background based on opacity
                return surface_color * material.opacity + background_color * (1.0 - material.opacity)
            else:
                return surface_color

    def _setup_ray_for_pixel(self, ray, x, y, width, height, pixel_size_x, pixel_size_y, viewport_z, scene, offset_x=0.0, offset_y=0.0):
        """Set up ray for a specific pixel with optional subpixel offsets for supersampling."""
        # Use the camera's robust ray generation method
        generated_ray = scene.camera.generate_ray_for_pixel(x, y, width, height, offset_x, offset_y)

        # Copy the generated ray data to the provided ray object
        ray.origin.x = generated_ray.origin.x
        ray.origin.y = generated_ray.origin.y
        ray.origin.z = generated_ray.origin.z
        ray.dest = generated_ray.dest

    def _supersample_pixel(self, ray, x, y, width, height, pixel_size_x, pixel_size_y, viewport_z, scene):
        """Take multiple samples for a single pixel and average the results."""
        # If supersampling is 1, just take a single sample at the center of the pixel
        if self.supersampling == 1:
            self._setup_ray_for_pixel(ray, x, y, width, height, pixel_size_x, pixel_size_y, viewport_z, scene)
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
                self._setup_ray_for_pixel(ray, x, y, width, height, pixel_size_x, pixel_size_y, viewport_z, scene, offset_x, offset_y)

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
        # Initialize ray with camera position and direction (will be updated per pixel)
        ray = Ray(scene.camera_position, scene.camera_direction)

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
        # Calculate scene parameters
        viewport_z, viewport_height, viewport_width, pixel_size_x, pixel_size_y = self._calculate_scene_parameters(scene)

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
                            pixel_size_x, pixel_size_y, viewport_z
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
                self._render_single_threaded(scene, window, pixels, pixel_size_x, pixel_size_y, viewport_z)
        else:
            # Single-threaded rendering
            self._render_single_threaded(scene, window, pixels, pixel_size_x, pixel_size_y, viewport_z)

        # Clean up and save result
        del pixels

        # Calculate and display rendering time
        render_time = time.time() - start_time
        pygame.display.set_caption(f"PyTrace Render Complete - Time: {render_time:.2f} seconds")
        print(f'Rendering time: {render_time:.2f} seconds')

        # Handle ASCII output and program exit based on mode
        if self.ascii_only_mode:
            # Generate ASCII output and exit immediately
            print("\nGenerating ASCII output...")
            self.render_ascii(window, self.downsample_factor)
            # Save image before exiting
            self.save_image(window)
            pygame.quit()
            sys.exit()
        elif self.ascii_mode:
            # Generate ASCII output and wait for manual closure
            print("\nGenerating ASCII output...")
            self.render_ascii(window, self.downsample_factor)
            # Wait for user to close window
            pygame.event.set_allowed((pygame.QUIT, pygame.KEYDOWN))
            self.wait_for_exit(window)
        else:
            # No ASCII output, just wait for manual closure
            pygame.event.set_allowed((pygame.QUIT, pygame.KEYDOWN))
            self.wait_for_exit(window)

    def _render_single_threaded(self, scene, window, pixels, pixel_size_x, pixel_size_y, viewport_z):
        """Render the scene using a single thread."""
        # Setup primary ray for rendering (will be updated per pixel)
        ray = Ray(scene.camera_position, scene.camera_direction)

        # Render each pixel
        for y in range(self.screen_height):
            # Check for quit events during rendering
            self._handle_quit_events(window)

            for x in range(self.screen_width):
                # Use supersampling to get the pixel color
                pixels[x, y] = self._supersample_pixel(
                    ray, x, y,
                    self.screen_width, self.screen_height,
                    pixel_size_x, pixel_size_y,
                    viewport_z, scene
                ).finalcolor()

            # Update display after each scanline
            pygame.display.update()

    def save_image(self, window_surface):
        """Save the rendered image with timestamp filename."""
        timestamp = datetime.datetime.strftime(datetime.datetime.now(), "%H.%M.%S_%d-%b-%Y")
        filename = f"render_{timestamp}.png"
        pygame.image.save(window_surface, filename)
        print(f"Image saved as: {filename}")

    def render_ascii(self, window_surface, downsample_factor=4):
        """Render ASCII output from the current pygame surface."""
        # Get pixel data from the surface
        width, height = window_surface.get_size()
        ascii_width = width // downsample_factor
        ascii_height = height // downsample_factor

        # Color to ASCII character mapping
        color_map = {
            'black': ' ',  # Use space instead of empty string for proper formatting
            'dark_gray': '░',
            'gray': '▒',
            'light_gray': '▓',
            'white': 'W',
            'red': 'R',
            'dark_red': 'r',
            'blue': 'B',
            'dark_blue': 'b',
            'green': 'G',
            'dark_green': 'g',
            'yellow': 'Y',
            'dark_yellow': 'y',
            'purple': 'P',
            'dark_purple': 'p',
            'cyan': 'C',
            'dark_cyan': 'c',
            'orange': 'O',
            'dark_orange': 'o',
        }

        # Reference colors for mapping (RGB values 0-255)
        reference_colors = {
            'black': (0, 0, 0),
            'dark_gray': (16, 16, 16),
            'gray': (32, 32, 32),
            'light_gray': (48, 48, 48),
            'white': (255, 255, 255),
            'red': (255, 0, 0),
            'dark_red': (127, 0, 0),
            'blue': (0, 0, 255),
            'dark_blue': (0, 0, 127),
            'green': (0, 255, 0),
            'dark_green': (0, 127, 0),
            'yellow': (255, 255, 0),
            'dark_yellow': (127, 127, 0),
            'purple': (128, 0, 128),
            'dark_purple': (64, 0, 64),
            'cyan': (0, 255, 255),
            'dark_cyan': (0, 128, 128),
            'orange': (255, 165, 0),
            'dark_orange': (128, 82, 0)
        }

        def color_distance(color1, color2):
            """Calculate Euclidean distance between two RGB colors."""
            return ((color1[0] - color2[0]) ** 2 +
                    (color1[1] - color2[1]) ** 2 +
                    (color1[2] - color2[2]) ** 2) ** 0.5

        def find_nearest_color(pixel_color):
            """Find the nearest reference color and return its ASCII character."""
            min_distance = float('inf')
            nearest_color = 'black'

            for color_name, ref_color in reference_colors.items():
                distance = color_distance(pixel_color, ref_color)
                if distance < min_distance:
                    min_distance = distance
                    nearest_color = color_name

            return color_map[nearest_color]

        ascii_lines = []
        for y in range(ascii_height):
            line = ""
            for x in range(ascii_width):
                sample_x = min(x * downsample_factor + downsample_factor // 2, width - 1)
                sample_y = min(y * downsample_factor + downsample_factor // 2, height - 1)
                pixel_color = window_surface.get_at((sample_x, sample_y))[:3]
                ascii_char = find_nearest_color(pixel_color)
                line += ascii_char
            ascii_lines.append(line)
        print("\n" + "=" * 50)
        print("ASCII RENDER OUTPUT:")
        print("=" * 50)
        for line in ascii_lines:
            print(line)
        print("=" * 50)

        # Also save to file
        timestamp = datetime.datetime.strftime(datetime.datetime.now(), "%H.%M.%S_%d-%b-%Y")
        ascii_filename = f"ascii_render_{timestamp}.txt"
        with open(ascii_filename, 'w', encoding='utf-8') as f:
            f.write("ASCII RENDER OUTPUT:\n")
            f.write("=" * 50 + "\n")
            for line in ascii_lines:
                f.write(line + "\n")
            f.write("=" * 50 + "\n")

        print(f"ASCII render saved as: {ascii_filename}")

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


def create_scene():
    """Create and return the scene with all objects."""
    scene = Scene("Default Scene",
                  camera_position=Point3D(0, 0,25 ),
                  camera_direction=Point3D(0, 0, 0),
                  ambient_intensity=0.0,
                  field_of_view=90)

    scene.add_object(Sphere(Point3D(-10, 0, 5), 5, Material(RGB(1, 1, 1), 1.0, 0.00, 1.0)))

    scene.add_object(Sphere(Point3D(10, 0, 5), 5, Material(RGB(0, 1, 0), 1.0, 0.00, 0.0)))

    scene.add_object(Cuboid(center=Point3D(0, 5, 10), width=1, height=10, depth=20, material=(Material(RGB(0.0, 0.0, 1)))))

    scene.add_object(CheckerPlane(center=Point3D(0, 0, 0), normal=Normal(0, 0, 1)))

    # Red sphere on the right with reflection and high roughness
    # scene.add_object(Sphere(Point3D(50, 50, -50), 30, Material(RGB(0.5, 0, 0), 1.0, 0.01, 0.0)))

    # Green sphere on the left with reflection and medium roughness
    # scene.add_object(Sphere(Point3D(-50, 50, -50), 30, Material(RGB(0, 0.5, 0), 1.0, 0.01, 0.0)))

    # Blue sphere on the top with reflection and no roughness (smooth)
    # scene.add_object(Sphere(Point3D(1, 50, 50), 30, Material(RGB(0, 0, 0.5), 1.0, 0.01, 0.0)))

    # terrain1 = Terrain(
    #     noise_scale=0.5,
    #     noise_amplitude=0.8,
    #     cube_size=1,
    #     gap_distance=1,
    #     width=15.0,
    #     depth=15.0,
    #     height=15.0,
    #     reflectivity=0.5,
    #     opacity=1.0,
    #     location=Point3D(0, 0, 0),
    #     normal=Vector3D(0, 0, 1),
    #     seed=123
    # )
    #
    # scene.add_object(terrain1)
    return scene


if __name__ == "__main__":
    random.seed()

    # Set up argument parser
    parser = argparse.ArgumentParser(
        description='PyTrace - A Python Ray Tracer',
        epilog='''
Examples:
  python main.py                                # Run with default settings
  python main.py --width 1280 --height 720      # Render at 720p resolution
  python main.py -w 1920 -h 1080 -s 4           # Render at 1080p with 4x supersampling
  python main.py -r 100 -s 2                    # Higher recursion limit with 2x supersampling
        '''
    )


    def positive_int(value):
        ivalue = int(value)
        if ivalue <= 0:
            raise argparse.ArgumentTypeError(f"Value must be a positive integer, got {value}")
        return ivalue


    parser.add_argument('-w', '--width', type=positive_int, default=600, help='Screen width in pixels (default: 600)')
    parser.add_argument('-t', '--height', type=positive_int, default=600, help='Screen height in pixels (default: 600)')
    parser.add_argument('-r', '--recursion-limit', type=positive_int, default=5, help='Maximum recursion depth for ray tracing (default: 5)')


    def supersampling_level(value):
        ivalue = positive_int(value)
        if ivalue < 1 or ivalue > 4:
            raise argparse.ArgumentTypeError(f"Supersampling level must be between 1 and 4, got {value}")
        return ivalue


    parser.add_argument('-s', '--supersampling', type=supersampling_level, default=1, help='Supersampling level for anti-aliasing (1-4) (default: 1)')
    parser.add_argument('--ascii', action='store_true', help='Display ASCII output and wait for manual program closure')
    parser.add_argument('--ascii_only', action='store_true', help='Display ASCII output and exit immediately')
    parser.add_argument('--downsample_factor', type=positive_int, default=4, help='Downsample factor for ASCII rendering (default: 4, only used with --ascii or --ascii_only)')

    # Parse arguments
    args = parser.parse_args()

    # Create a scene
    scene = create_scene()

    # Create a raytracer with the parsed arguments
    raytracer = RayTracer(
        screen_width=args.width,
        screen_height=args.height,
        recursion_limit=args.recursion_limit,
        supersampling=args.supersampling,
        ascii_mode=args.ascii,
        ascii_only_mode=args.ascii_only,
        downsample_factor=args.downsample_factor
    )

    # Render the scene
    raytracer.render(scene)
