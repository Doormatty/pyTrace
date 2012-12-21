import pygame, sys
from pygame.locals import *
import time

import random
import datetime
from Vector import Vector3D
from Point import Point3D
from Primitives import *
from RGB import RGB
from Material import Material
from Ray import Ray
from TestSuite import TestSuite
from RayIntersection import RayIntersection

background_color = RGB(0, 0, 0)
xres = 640
yres = 480
psize = 1
recurse = 10
Viewportz = 100

def can_see(point, object):
    cast_ray = Ray()
    cast_ray.o = point
    cast_ray.d = Vector3D(-260, -100, 0)
    cast_ray.d = cast_ray.d.normalize()
    hit = False
    for thing in World:
        intersection = thing.hit(cast_ray)
        #if it's not False, it hit something.
        if intersection != False:
            #is this the first time we've hit something?
            if hit == False:
                hit = True
                hit_distance = cast_ray.o.distance(intersection.hit_point)
                closest_object = intersection
            else:
                #check if the latest hit is closer
                if cast_ray.o.distance(intersection.hit_point) < hit_distance:
                    closest_object = intersection
                    hit_distance = cast_ray.o.distance(intersection.hit_point)
    if hit == False:
        return False
    else:
        if closest_object == object:
            return True
        else:
            return False

def lighting(intersection):     
    #How much light things get from cosine shading.
    diffuse_coefficient = 1
    shade = Vector3D(0, 0, 1) * intersection.normal
    if shade < 0:
        shade = 0
    
    point_color = intersection.object.mat.color * (diffuse_coefficient * shade)
    #point_color = object[1].color * (ambient_coefficient + diffuse_coefficient * shade) 
    if intersection.object.mat.luma > 0:
        return intersection.object.mat.color
    return point_color

def lighting2(intersection):
    if can_see(intersection.hit_point, World[3]):
        print "CAN SEE!"
        point_color = intersection.object.mat.color
        return point_color
    else:
        return RGB(0, 0, 0)
        
        
def raytrace(cast_ray, r = recurse):
    hit = False
    for thing in World:
        intersection = thing.hit(cast_ray)
        #if it's not False, it hit something.
        if intersection != False:
            #is this the first time we've hit something?
            if hit == False:
                hit = True
                hit_distance = cast_ray.o.distance(intersection.hit_point)
                closest_object = intersection
            else:
                #check if the latest hit is closer
                if cast_ray.o.distance(intersection.hit_point) < hit_distance:
                    closest_object = intersection
                    hit_distance = cast_ray.o.distance(intersection.hit_point)
    if hit == False:
        return background_color
    else:
        # At this point, closest_object[4] contains the closest item the ray intersects with.
        #Check for end of recursion
        if r == 1:
            #Now we apply lighting
            
            lit_color = lighting(closest_object)
            return RGB(1, 1, 1)
            return lit_color
        
        #Check for Reflectance
        if closest_object.object.mat.reflect > 0:
            reflect_ray = Ray()
            reflect_ray.o = closest_object.hit_point
            c1 = 0 - (closest_object.normal * cast_ray.d)
            reflect_ray.d = cast_ray.d + (2 * closest_object.normal * c1)
            reflect_ray.d = reflect_ray.d.normalize()
            reflect_color = raytrace(reflect_ray, r - 1)
            
            tcolor = lighting(closest_object)
            tcolor = tcolor + (reflect_color * closest_object.object.mat.reflect)
            return tcolor
        else:
            # The object isn't reflective.
            lit_color = lighting(closest_object)
            return lit_color
        #return closest_object[1].color
            
        

def Render():
    pygame.init()
    windowSurfaceObj = pygame.display.set_mode((xres, yres))
    pygame.display.set_caption("Matt's Ray Tracer")
    pixArr = pygame.PixelArray(windowSurfaceObj)
    tRay = Ray()
    tRay.d = Vector3D(0, 0, -1)
    #Hardcoded Viewport for now
    tRay.o.z = Viewportz
    starttime = time.time() 
    
       
    for y in range(yres):
        for event in pygame.event.get():
            if event.type == QUIT:
                filename = datetime.datetime.strftime(datetime.datetime.now(), "%H.%M.%S_%d-%b-%Y") + '.png'
                pygame.image.save(windowSurfaceObj, filename)
                pygame.quit()
                sys.exit()
        pygame.display.set_caption("Matt's Ray Tracer - Render in Progress...")
        tRay.o.y = psize * (y - 0.5 * (yres - 1))
        for x in range(xres):
            tRay.o.x = psize * (x - 0.5 * (xres - 1))
            ray_color = raytrace(tRay)
            tcolor = ray_color.finalcolor()
            pixArr[x][y] = pygame.Color(tcolor[0], tcolor[1], tcolor[2])
        pygame.display.update()
        
        
            
    del pixArr
    pygame.display.set_caption("Matt's Ray Tracer - Render Finished - Total time: " + str(time.time() - starttime) + " seconds")
    print 'Time :', time.time() - starttime 
    filename = datetime.datetime.strftime(datetime.datetime.now(), "%H.%M.%S_%d-%b-%Y") + '.png'
    pygame.image.save(windowSurfaceObj, filename)
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

#World.append(Cube(Point3D(0,0,0),Point3D(-100,100,0),Point3D(-100,0,-100),Material(RGB(.5,0,0))))


World.append(Sphere(Point3D(100, -100, 1), 95, Material(RGB(.5, 0, 0), 1.0, 0.7, 0.0)))
World.append(Sphere(Point3D(-100, -100, 1), 95, Material(RGB(0, .5, 0), 1.0, 0.7, 0.0)))
World.append(Sphere(Point3D(1, 140, 1), 95, Material(RGB(0, 0, .5), 1.0, 0.7, 0.0)))

#World.append(Sphere(Point3D(-260, -100, 0), 40, Material(RGB(1.0, 1.0, 1.0), 1.0, 0.0, 1.0)))
#World.append(Plane(Point3D(1, 90, 200), Vector3D(0, 0, -1), Material(RGB(.3, .3, .3), 1.0, 0.0, 0.0)))

#White Sphere on Right - should be merged with red sphere below
#World.append(Sphere(Point3D(180, 0, 0), 30, Material(RGB(255, 255, 255), 1.0, 0.0, 0.0)))

#Brown Sphere behind Red Sphere
#World.append(Sphere(Point3D(150, 0, -10), 30, Material(RGB(255, 255, 0), 1.0, 0.0, 0.0)))

#Red Sphere on Right
#World.append(Sphere(Point3D(150, 0, 0), 30, Material(RGB(255, 0, 0), 1.0, 0.0, 0.0)))

#Dim Red Sphere on Left
#World.append(Sphere(Point3D(-150, 0, 0), 30, Material(RGB(127, 0, 0), 1.0, 0.0, 0.0)))

#Green sphere on bottom
#World.append(Sphere(Point3D(0, 150, 0), 30, Material(RGB(0, 255, 0), 1.0, 0.0, 0.0)))

#Dim green sphere on top
#World.append(Sphere(Point3D(1, -150, 1), 30, Material(RGB(0, 127, 0), 1.0, 1.0, 0.0)))

#Bright Blue sphere on bottom right
#World.append(Sphere(Point3D(150, 150, 0), 30, Material(RGB(0, 0, 255), 1.0, 0.0, 0.0)))

#Dim Blue Sphere on top left
#World.append(Sphere(Point3D(-150, -150, 0), 30, Material(RGB(0, 0, 127), 1.0, 0.0, 0.0)))

#add a light
#World.append(Sphere(Point3D(0, 0, 0), 30, Material(RGB(255, 255, 255), 1.0, 1.0, 1.0)))

TestSuite()
Render()

