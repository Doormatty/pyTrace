'''
Created on Apr 18, 2012

@author: matt
'''

from Normal import Normal
from Point import Point3D
from Primitives import Shape

class RayIntersection:
    
    object = Shape()
    normal = Normal()
    hit_point = Point3D()
    
    def __init__(self, shape, normal, hit_point):
        self.object = shape
        self.normal = normal
        self.hit_point = hit_point
    
    def __str__(self):
        return str(self.object) + " " + str(self.normal) + " " + str(self.hit_point)
