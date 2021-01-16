from RGB import RGB
from Point import Point3D
from Vector import Vector3D
from Normal import Normal
from Primitives import *
from Ray import Ray
import math


class TestRGB:
    a = RGB(0.1, 0.1, 0.1)
    b = RGB(0.2, 0.3, 0.4)
    c = RGB(0.99, 0.0, 0.99)
    d = RGB(0.0, 0.99, 0.99)

    def test_add(self):
        assert self.a + self.b == RGB(0.3, 0.4, 0.5)

    def test_subtract(self):
        assert self.b - self.a == RGB(0.1, 0.2, 0.3)

    def test_equality(self):
        assert self.a == self.a == RGB(0.1, 0.1, 0.1)

    def test_inequality(self):
        assert self.a != self.b

    def test_upperclamp(self):
        assert self.a + self.c == RGB(1.0, 0.1, 1.0)

    def test_lowerclamp(self):
        assert self.a - self.d == RGB(0.1, 0.0, 0.0)


class TestVector:
    u = Vector3D(10, 20, 30)
    v = Vector3D(0, 0, 1)

    def test_vecadd(self):
        assert self.u + self.v == Vector3D(10, 20, 31)

    def test_vecsub(self):
        assert self.u - self.v == Vector3D(10, 20, 29)
        assert self.v - self.u == Vector3D(-10, -20, -29)

    def test_vecmult(self):
        assert 2 * self.u == self.u * 2 == Vector3D(20, 40, 60)

    def test_vecdiv(self):
        assert self.u / 2 == Vector3D(5, 10, 15)
        assert self.u / 0 == False

    def test_equality(self):
        assert self.v == self.v
        assert self.v != self.u

    def test_length(self):
        assert self.u.length == math.sqrt(self.u.x * self.u.x + self.u.y * self.u.y + self.u.z * self.u.z)

    def test_dot(self):
        assert Vector3D(-1, 2, -3) * Vector3D(1, -2, 3) == -14

    def test_cross(self):
        assert Vector3D(-1, 2, -3) ^ Vector3D(1, -2, 3) == Vector3D(0, 0, 0)
        assert Vector3D(1, 2, 1) ^ Vector3D(0, -1, 2) == Vector3D(5, -2, -1)


class TestPoint:
    u = Vector3D(10, 20, 30)
    a = Point3D(-1, 2, -3)
    b = Point3D(1, -2, 3)

    def test_pointvec_add(self):
        assert self.a + self.u == Point3D(9, 22, 27)

    def test_pointvec_sub(self):
        assert self.a - self.u == Point3D(-11, -18, -33)

    def test_pointpoint_sub(self):
        assert self.a - self.b == Vector3D(-2, 4, -6)

    def test_equality(self):
        assert self.a == self.a
        assert self.a != self.b


class TestIntersection:
    tMat = Material(RGB(0, 0, 0))
    a = Sphere(Point3D(0, 0, 0), 50, tMat)
    b = Plane(Point3D(0, 0, 0), Normal(0, 1, 0), tMat)
    aRay = Ray(Point3D(100, 0, 100), Vector3D(0, 0, -1))  # Should not intersect Sphere or Plane
    bRay = Ray(Point3D(5, 5, 100), Vector3D(0, 0, -1))  # Should intersect Sphere only
    cRay = Ray(Point3D(0, 100, 0), Vector3D(0, -1, 0))  # Should intersect Sphere and Plane
    dRay = Ray(Point3D(100, 100, 100), Vector3D(0, -1, 0))  # Should intersect Plane only

    def test_ray_sphere(self):
        assert self.a.hit(self.bRay) != False
        assert self.a.hit(self.cRay) != False
        assert self.a.hit(self.aRay) == False
        assert self.a.hit(self.dRay) == False

    def test_ray_plane(self):
        assert self.b.hit(self.cRay) != False
        assert self.b.hit(self.dRay) != False
        assert self.b.hit(self.aRay) == False
        assert False == self.b.hit(self.bRay)
