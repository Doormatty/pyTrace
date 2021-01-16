from __future__ import annotations
import math
from Material import Material
from typing import Optional, Union
from Point import Point3D
from Vector import Vector3D
from RGB import RGB


class Plane:
    center: Point3D
    normal: Optional[Vector3D]
    material: Optional[Material]
    ray: Vector3D

    def __init__(self, center, normal, material) -> None:
        self.center = center
        self.normal = normal if normal else Vector3D(0, 1, 0)
        self.material = material if material else Material()

    def hit(self, ray):
        t2 = ray.dest * self.normal
        if t2 == 0:  # Ray is parallel to plane
            return False
        t = (self.center - ray.origin) * self.normal / t2
        if t > 0:
            intersection_point = ray.origin + (t * ray.dest)
            return RayIntersection(self, self.normal, intersection_point)
            # return(self, self.normal, intersection_point)
        return False

    def __repr__(self):
        return f"Plane(x={self.center.x}, y={self.center.y}, z={self.center.z})"


class Sphere:
    center: Point3D
    radius: Union[float, int]
    material: Material

    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius if radius else 1
        self.material = material if material else Material()
        self.kEpsilon = .01

    def hit(self, ray) -> Union[bool, RayIntersection]:
        t_vec = ray.origin - self.center
        a = ray.dest * ray.dest
        b = 2.0 * t_vec * ray.dest
        c = t_vec * t_vec - (self.radius * self.radius)
        disc = b * b - 4.0 * a * c
        if disc < 0.0:
            return False

        e = math.sqrt(disc)
        t = ((0 - b) - e) / (2.0 * a)

        if t > self.kEpsilon:
            intersection_point = ray.origin + t * ray.dest
            normal = Vector3D((intersection_point.x - self.center.x) / self.radius,
                              (intersection_point.y - self.center.y) / self.radius,
                              (intersection_point.z - self.center.z) / self.radius)
            return RayIntersection(self, normal, intersection_point)
        return False

    def __repr__(self):
        return f"Sphere(x={self.center.x}, y={self.center.y}, z={self.center.z}, radius={self.radius})"


class Cube:
    def __init__(self, a=Point3D(), b=Point3D(), c=Point3D(), material=Material()) -> None:
        self.a = a
        self.b = b
        self.c = c
        self.material = material
        tpoint = Point3D(self.a.x, self.b.y, self.c.z)
        # self.faces.append(self.a,self.b,Vector3D(0,0,-1))
        # self.faces.append(self.b,tpoint,Vector3D(0,1,0))
        # self.faces.append(self.a,self.c,Vector3D(0,-1,0))
        # self.faces.append(self.a,tpoint,Vector3D(1,0,0))
        # self.faces.append(self.b,self.c,Vector3D(-1,0,0))
        # self.faces.append(self.c,tpoint,Vector3D(0,0,1))
        self.faces = []
        self.faces.append((self.a, self.b, self.a - (self.a.distance(self.b) / 2), Vector3D(0, 0, -1)))
        self.faces.append((self.b, tpoint, self.a - (self.b.distance(tpoint) / 2), Vector3D(0, 1, 0)))
        self.faces.append((self.a, self.c, self.a - (self.a.distance(self.c) / 2), Vector3D(0, -1, 0)))
        self.faces.append((self.a, tpoint, self.a - (self.a.distance(tpoint) / 2), Vector3D(1, 0, 0)))
        self.faces.append((self.b, self.c, self.a - (self.b.distance(self.c) / 2), Vector3D(-1, 0, 0)))
        self.faces.append((self.c, tpoint, self.a - (self.c.distance(tpoint) / 2), Vector3D(0, 0, 1)))

    def hit(self, ray):
        maxx = max(self.a.x, self.b.x, self.c.x)
        minx = min(self.a.x, self.b.x, self.c.x)
        maxy = max(self.a.y, self.b.y, self.c.y)
        miny = min(self.a.y, self.b.y, self.c.y)
        maxz = max(self.a.z, self.b.z, self.c.z)
        minz = min(self.a.z, self.b.z, self.c.z)
        hits = []
        for face in self.faces:
            t2 = ray.dest * face[3]
            if t2 == 0:  # Ray is parallel to plane'
                return False
            t = (face[2] - ray.origin) * face[3] / t2
            if t > 0:
                # At this point, the ray has intersected the plane, but perhaps not within the bounds of the cube.
                hit_point = ray.origin + (t * ray.dest)
                if (hit_point.x > maxx or hit_point.x < minx) and (hit_point.y > maxy or hit_point.y < miny) and (
                        hit_point.z > maxz or hit_point.z < minz):
                    hits.append(hit_point, face[3])

        if len(hits) < 2:
            return False

        if hits[0][0].distance(ray.origin) < hits[1][0].distance(ray.origin):
            return RayIntersection(self, hits[0][1], hits[0][0])
        else:
            return RayIntersection(self, hits[1][1], hits[1][0])


from RayIntersection import RayIntersection
