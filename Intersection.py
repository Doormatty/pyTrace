'''
Created on Apr 18, 2012

@author: matt
'''
from Primitives import Shape
from Normal import Normal
from Point import Point3D

class Intersection:
    object = Shape()
    normal = Normal()
    hit_point = Point3D()
    
    def __init__(self, shape, normal, hit_point):
        self.object = shape
        self.normal = normal
        self.hit_point = hit_point
        
