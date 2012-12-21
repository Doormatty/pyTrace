'''
Created on Apr 15, 2012

@author: matt
'''

import colorama
from RGB import RGB
from Point import Point3D
from Vector import Vector3D
from Normal import Normal
from Material import Material
from Primitives import *
from Ray import Ray
import math

colorama.init()

def test(string, function):
    if function:
        print colorama.Fore.GREEN + string + ": Pass" + colorama.Style.RESET_ALL
    else:
        print colorama.Fore.BLACK + colorama.Back.RED + string + ": FAIL" + colorama.Style.RESET_ALL

def testheader(string):
    print colorama.Fore.WHITE + "----=====" + colorama.Back.BLUE + string + colorama.Back.BLACK + "=====----" + colorama.Style.RESET_ALL

def TestSuite():
    
    testheader('RGB Tests')
    a = RGB(0.1, 0.1, 0.1)
    b = RGB(0.2, 0.3, 0.4)
    c = RGB(0.99, 0.0, 0.99)
    d = RGB(0.0, 0.99, 0.99)
    test("Basic RGB Addition", a + b == RGB(0.3, 0.4, 0.5))
    test("Basic RGB Subtraction", b - a == RGB(0.1, 0.2, 0.3))
    test("Equality Testing", a == a)
    test("Inequality Testing", a != b)
    test("Upper-bound RGB Clamping", a + c == RGB(1.0, 0.1, 1.0))
    test("Lower-bound RGB Clamping", a - d == RGB(0.1, 0.0, 0.0))
    
    
    testheader('3D Vector Tests') 
    u = Vector3D(10, 20, 30)
    v = Vector3D(0, 0, 1)
    test("Vector/Vector Addition", u + v == Vector3D(10, 20, 31))
    test("Vector/Vector Subtraction", u - v == Vector3D(10, 20, 29))
    test("Vector/Real Multiplication", 2 * u == u * 2 == Vector3D(20, 40, 60))
    test("Vector/Real Division", u / 2 == Vector3D(5, 10, 15))
    test("Vector/Real Division by Zero", u / 0 == False)
    test("Equality Testing", v == v)
    test("Inequality Testing", v != u)
    test("Vector Length", u.length() == math.sqrt(u.x * u.x + u.y * u.y + u.z * u.z))
    test("Vector Dot Product", Vector3D(-1, 2, -3) * Vector3D(1, -2, 3) == -14)
    test("Vector Cross Product", Vector3D(-1, 2, -3) ^ Vector3D(1, -2, 3) == Vector3D(0, 0, 0))
    test("Vector Cross Product #2", Vector3D(1, 2, 1) ^ Vector3D(0, -1, 2) == Vector3D(5, -2, -1))
    
    testheader('3D Point Tests')
    u = Vector3D(10, 20, 30)
    a = Point3D(-1, 2, -3)
    b = Point3D(1, -2, 3)
    c = 0.0
    test("Point/Vector Addition", a + u == Point3D(9, 22, 27))
    test("Point/Vector Subtraction", a - u == Point3D(-11, -18, -33))
    test("Point/Point Subtraction", a - b == Vector3D(-2, 4, -6))
    test("Equality Testing", a == a)
    test("Inequality Testing", a != b)
    
    testheader('Ray/Primitive Intersection Tests')
    tMat = Material(RGB(0, 0, 0))
    a = Sphere(Point3D(0, 0, 0), 50, tMat)
    b = Plane(Point3D(0, 0, 0), Normal(0, 1, 0), tMat)
    aRay = Ray(Point3D(100, 0, 100), Vector3D(0, 0, -1)) # Should not intersect Sphere or Plane
    bRay = Ray(Point3D(5, 5, 100), Vector3D(0, 0, -1)) # Should intersect Sphere only
    cRay = Ray(Point3D(0, 100, 0), Vector3D(0, -1, 0)) # Should intersect Sphere and Plane
    dRay = Ray(Point3D(100, 100, 100), Vector3D(0, -1, 0)) # Should intersect Plane only
    
    test("Ray/Sphere Intersection #1", a.hit(bRay) != False)
    test("Ray/Sphere Intersection #2", a.hit(cRay) != False)
    test("Ray/Sphere Miss #1", a.hit(aRay) == False)
    test("Ray/Sphere Miss #2", a.hit(dRay) == False)
    test("Ray/Plane Intersection #1", b.hit(cRay) != False)
    test("Ray/Plane Intersection #1", b.hit(dRay) != False)
    test("Ray/Plane Miss #1", b.hit(aRay) == False)
    test("Ray/Plane Miss #2", b.hit(bRay) == False)
    
    return
