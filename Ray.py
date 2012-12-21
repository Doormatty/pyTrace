'''
Created on Apr 15, 2012

@author: matt
'''

from Point import Point3D
from Vector import Vector3D

class Ray:
    o = Point3D()
    d = Vector3D()
    
    def __init__(self, origin = Point3D(0, 0, 0), dest = Vector3D(0, 0, 0)):
        self.o = origin
        self.d = dest
    
    def __str__(self):
        return "Ray - Origin:" + str(self.o) + " Destination:" + str(self.d)
    
