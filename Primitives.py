'''
Created on Apr 15, 2012

@author: matt
'''

import math
from Material import Material
# from Normal import Normal
from Point import Point3D
from Vector import Vector3D
from RGB import RGB


class Shape:
    mat = Material()
    center = Point3D()


class Plane(Shape):
    normal = Vector3D()

    def __init__(self, centerpoint=Point3D(), normal=Vector3D(0, 1, 0), material=Material()):
        self.center = centerpoint
        self.normal = normal
        self.mat = material

    def hit(self, Ray):
        t2 = Ray.d * self.normal
        if t2 == 0:  # Ray is parallel to plane'
            return False
        t = (self.center - Ray.o) * self.normal / t2
        if t > 0:
            intersection_point = Ray.o + (t * Ray.d)
            return RayIntersection(self, self.normal, intersection_point)
            # return(self, self.normal, intersection_point)
        return False

    def __str__(self):
        return "Plane - X:" + str(self.center.x) + " Y:" + str(self.center.y) + " Z:" + str(self.center.z)


class Sphere(Shape):
    def __init__(self, center, radius=1, material=Material()):
        self.center = center
        self.radius = radius
        self.mat = material
        self.kEpsilon = .1

    def hit(self, ray):
        t = 0
        tVec = ray.o - self.center
        a = ray.d * ray.d
        b = 2.0 * tVec * ray.d
        c = tVec * tVec - (self.radius * self.radius)
        disc = b * b - 4.0 * a * c
        if disc < 0.0:
            return False

        e = math.sqrt(disc)
        denom = 2.0 * a
        t = ((0 - b) - e) / denom

        if t > self.kEpsilon:
            intersection_point = ray.o + t * ray.d
            normal = Vector3D((intersection_point.x - self.center.x) / self.radius,
                              (intersection_point.y - self.center.y) / self.radius,
                              (intersection_point.z - self.center.z) / self.radius)
            return RayIntersection(self, normal, intersection_point)
        return False

    def __str__(self):
        return f"Sphere(x={self.center.x}, y={self.center.y}, z={self.center.z}, radius={self.radius})"

    def __repr__(self):
        return f"Sphere(x={self.center.x}, y={self.center.y}, z={self.center.z}, radius={self.radius})"


class Cube(Shape):
    a = Point3D()
    b = Point3D()
    c = Point3D()
    faces = []

    def __init__(self, a=Point3D(), b=Point3D(), c=Point3D(), material=Material()):
        self.a = a
        self.b = b
        self.c = c

        self.mat = material
        tpoint = Point3D(self.a.x, self.b.y, self.c.z)
        # self.faces.append(self.a,self.b,Vector3D(0,0,-1))
        # self.faces.append(self.b,tpoint,Vector3D(0,1,0))
        # self.faces.append(self.a,self.c,Vector3D(0,-1,0))
        # self.faces.append(self.a,tpoint,Vector3D(1,0,0))
        # self.faces.append(self.b,self.c,Vector3D(-1,0,0))
        # self.faces.append(self.c,tpoint,Vector3D(0,0,1))
        self.faces.append((self.a, self.b, self.a - (self.a.distance(self.b) / 2), Vector3D(0, 0, -1)))
        self.faces.append((self.b, tpoint, self.a - (self.b.distance(tpoint) / 2), Vector3D(0, 1, 0)))
        self.faces.append((self.a, self.c, self.a - (self.a.distance(self.c) / 2), Vector3D(0, -1, 0)))
        self.faces.append((self.a, tpoint, self.a - (self.a.distance(tpoint) / 2), Vector3D(1, 0, 0)))
        self.faces.append((self.b, self.c, self.a - (self.b.distance(self.c) / 2), Vector3D(-1, 0, 0)))
        self.faces.append((self.c, tpoint, self.a - (self.c.distance(tpoint) / 2), Vector3D(0, 0, 1)))

    def hit(self, Ray):
        maxx = max(self.a.x, self.b.x, self.c.x)
        minx = min(self.a.x, self.b.x, self.c.x)
        maxy = max(self.a.y, self.b.y, self.c.y)
        miny = min(self.a.y, self.b.y, self.c.y)
        maxz = max(self.a.z, self.b.z, self.c.z)
        minz = min(self.a.z, self.b.z, self.c.z)
        hits = []
        for face in self.faces:
            t2 = Ray.d * face[3]
            if t2 == 0:  # Ray is parallel to plane'
                return False
            t = (face[2] - Ray.o) * face[3] / t2
            if t > 0:
                # At this point, the ray has intersected the plane, but perhaps not within the bounds of the cube.
                hit_point = Ray.o + (t * Ray.d)
                if (hit_point.x > maxx or hit_point.x < minx) and (hit_point.y > maxy or hit_point.y < miny) and (
                        hit_point.z > maxz or hit_point.z < minz):
                    hits.append(hit_point, face[3])

        if len(hits) < 2:
            return False
        else:
            if hits[0][0].distance(Ray.o) < hits[1][0].distance(Ray.o):
                return RayIntersection(self, hits[0][1], hits[0][0])
            else:
                return RayIntersection(self, hits[1][1], hits[1][0])
        return False


from RayIntersection import RayIntersection
