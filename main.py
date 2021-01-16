import pygame
import sys
import time
import random
import datetime
from pygame.locals import *
from Primitives import *
from RGB import RGB
from Material import Material
from Ray import Ray

background_color = RGB(0, 0, 0)
xres = 640
yres = 480
psize = 1
recurse_limit = 20
Viewportz = 100


def can_see(point, target):
    cast_ray = Ray()
    cast_ray.origin = point
    cast_ray.dest = Vector3D(-260, -100, 0)
    cast_ray.dest = cast_ray.dest.normalize()
    hit_distance = False
    closest_object = False
    for thing in World:
        intersection = thing.hit(cast_ray)
        if intersection:
            t_hit_distance = cast_ray.origin.distance(intersection.hit_point)
            if t_hit_distance < hit_distance:
                hit_distance = t_hit_distance
                closest_object = intersection
    if not hit_distance:
        return False
    else:
        if closest_object == target:
            return True
        else:
            return False


def lighting(hit):
    # How much light things get from cosine shading.
    diffuse_coefficient = 1
    shade = Vector3D(0, 0, 1) * hit.normal
    if shade < 0:
        shade = 0

    point_color = hit.object.material.color * (diffuse_coefficient * shade)
    # point_color = object[1].color * (ambient_coefficient + diffuse_coefficient * shade)
    if hit.object.material.luma > 0:
        return hit.object.material.color
    return point_color


def lighting2(intersection):
    if can_see(intersection.hit_point, World[3]):
        print("CAN SEE!")
        point_color = intersection.object.material.color
        return point_color
    else:
        return RGB(0, 0, 0)


def raytrace(cast_ray, r=recurse_limit) -> RGB:
    hit_distance = False
    hit = False
    for thing in World:
        intersection = thing.hit(cast_ray)
        if intersection:
            # return intersection.object.material.color  # For debugging
            t_hit_distance = cast_ray.origin.distance(intersection.hit_point)
            if t_hit_distance < hit_distance or not hit_distance:
                hit_distance = t_hit_distance
                hit = intersection
    if not hit_distance:
        return background_color
    # At this point, hit.object is the closest item that ray intersected with.
    # Check for end of recursion
    if r <= 1:
        # Now we apply lighting
        return lighting(hit)

    # Check for Reflectance
    if hit.object.material.reflect > 0:
        reflect_ray = Ray()
        reflect_ray.origin = hit.hit_point
        reflect_ray.dest = cast_ray.dest + (2 * hit.normal * (0 - (hit.normal * cast_ray.dest)))
        reflect_ray.dest = reflect_ray.dest.normalize()
        reflect_color = raytrace(reflect_ray, r - 1)
        return lighting(hit) + (reflect_color * hit.object.material.reflect)
    else:
        # The object isn't reflective.
        return lighting(hit)


def render():
    pygame.init()
    window_surface_obj = pygame.display.set_mode((xres, yres))
    pixels = pygame.PixelArray(window_surface_obj)
    pygame.display.set_caption("PyTrace - Render in Progress...")
    pygame.event.set_allowed(pygame.QUIT)
    ray = Ray()
    ray.dest = Vector3D(0, 0, -1)
    #  Hardcoded Viewport for now
    ray.origin.z = Viewportz
    starttime = time.time()

    for y in range(yres):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                filename = datetime.datetime.strftime(datetime.datetime.now(), "%H.%M.%S_%d-%b-%Y") + '.png'
                pygame.image.save(window_surface_obj, filename)
                pygame.quit()
                sys.exit()

        ray.origin.y = psize * (y - 0.5 * (yres - 1))
        for x in range(xres):
            ray.origin.x = psize * (x - 0.5 * (xres - 1))
            pixels[x, y] = raytrace(ray).finalcolor()
        pygame.display.update()

    del pixels
    pygame.display.set_caption(f"PyTrace Render Finished - Total time: {time.time() - starttime} seconds")
    print('Time :', time.time() - starttime)
    filename = datetime.datetime.strftime(datetime.datetime.now(), "%H.%M.%S_%d-%b-%Y") + '.png'
    pygame.image.save(window_surface_obj, filename)
    pygame.event.set_allowed((pygame.QUIT, pygame.KEYDOWN))
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.event.post(pygame.event.Event(QUIT))


World = []
random.seed()

# World.append(Cube(Point3D(0,0,0),Point3D(-100,100,0),Point3D(-100,0,-100),Material(RGB(.5,0,0))))


World.append(Sphere(Point3D(50, -50, 1), 95, Material(RGB(.5, 0, 0), 1.0, 0.7, 0.0)))
World.append(Sphere(Point3D(-50, -50, 1), 95, Material(RGB(0, .5, 0), 1.0, 0.7, 0.0)))
World.append(Sphere(Point3D(1, 50, 1), 95, Material(RGB(0, 0, .5), 1.0, 0.7, 0.0)))

# World.append(Sphere(Point3D(-260, -100, 0), 40, Material(RGB(1.0, 1.0, 1.0), 1.0, 0.0, 1.0)))
# World.append(Plane(Point3D(1, 90, 200), Vector3D(0, 0, -1), Material(RGB(.3, .3, .3), 1.0, 0.0, 0.0)))

# White Sphere on Right - should be merged with red sphere below
# World.append(Sphere(Point3D(180, 0, 0), 30, Material(RGB(255, 255, 255), 1.0, 0.0, 0.0)))

# Brown Sphere behind Red Sphere
# World.append(Sphere(Point3D(150, 0, -10), 30, Material(RGB(255, 255, 0), 1.0, 0.0, 0.0)))

# Red Sphere on Right
# World.append(Sphere(Point3D(150, 0, 0), 30, Material(RGB(255, 0, 0), 1.0, 0.0, 0.0)))

# Dim Red Sphere on Left
# World.append(Sphere(Point3D(-150, 0, 0), 30, Material(RGB(127, 0, 0), 1.0, 0.0, 0.0)))

# Green sphere on bottom
# World.append(Sphere(Point3D(0, 150, 0), 30, Material(RGB(0, 255, 0), 1.0, 0.0, 0.0)))

# Dim green sphere on top
# World.append(Sphere(Point3D(1, -150, 1), 30, Material(RGB(0, 127, 0), 1.0, 1.0, 0.0)))

# Bright Blue sphere on bottom right
# World.append(Sphere(Point3D(150, 150, 0), 30, Material(RGB(0, 0, 255), 1.0, 0.0, 0.0)))

# Dim Blue Sphere on top left
# World.append(Sphere(Point3D(-150, -150, 0), 30, Material(RGB(0, 0, 127), 1.0, 0.0, 0.0)))

# add a light
# World.append(Sphere(Point3D(0, 0, 0), 30, Material(RGB(255, 255, 255), 1.0, 1.0, 1.0)))

render()
