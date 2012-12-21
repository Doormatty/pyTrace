'''
Created on Apr 15, 2012

@author: matt
'''
import math
from Vector import Vector3D
class Point3D:
    x = 0
    y = 0
    z = 0
    def __init__(self, xx = 0, yy = 0, zz = 0):
        if type(xx) == type(()):
            self.x = xx[0]
            self.y = xx[1]
            self.z = xx[2]
        else:
            self.x = xx
            self.y = yy
            self.z = zz
            
        
    def __add__(self, Other):
        if isinstance(Other, Vector3D):
            #print 'Adding a Vector3D to a point to get a point.'
            t = Point3D()
            t.x = self.x + Other.x
            t.y = self.y + Other.y
            t.z = self.z + Other.z
            return t
        
        if isinstance(Other, Point3D):
            #print 'Adding a point to a point to get a Vector3D.'
            t = Vector3D()
            t.x = self.x + Other.x
            t.y = self.y + Other.y
            t.z = self.z + Other.z
            return t
        
        t = Point3D()
        t.x = self.x + Other
        t.y = self.y + Other
        t.z = self.z + Other
        return t
         
    def __sub__(self, Other):         
        if isinstance(Other, Vector3D):
            #print 'Subtracting a Vector3D from a point to get a point.'
            t = Point3D()
        elif isinstance(Other, int) or isinstance(Other, float):
            t = Point3D()
            t.x = self.x - Other
            t.y = self.y - Other
            t.z = self.z - Other
            return t
        elif isinstance(Other, Point3D):
            #print 'Subtracting a point from a point to get a Vector3D.'
            t = Vector3D()
        t.x = self.x - Other.x
        t.y = self.y - Other.y
        t.z = self.z - Other.z
        return t
    
    def distance(self, point):
        return int(math.sqrt((self.x - point.x) ** 2 + (self.y - point.y) ** 2 + (self.z - point.z) ** 2))
    
    def __str__(self):
        return "Point3D - X:" + str(self.x) + " Y:" + str(self.y) + " Z:" + str(self.z)
    
    def __eq__(self, oPoint3D):
        return (self.x == oPoint3D.x) and (self.y == oPoint3D.y) and (self.z == oPoint3D.z)
