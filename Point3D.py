'''
Created on Apr 15, 2012

@author: matt
'''

from Vector import Vector3D
class point3D:
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
            t = point3D()
            t.x = self.x + Other.x
            t.y = self.y + Other.y
            t.z = self.z + Other.z
            return t
        
        if isinstance(Other, point3D):
            #print 'Adding a point to a point to get a Vector3D.'
            t = Vector3D()
            t.x = self.x + Other.x
            t.y = self.y + Other.y
            t.z = self.z + Other.z
            return t
        
        t = point3D()
        t.x = self.x + Other
        t.y = self.y + Other
        t.z = self.z + Other
        return t
        
        
        
    
    def __sub__(self, Other):         
        if isinstance(Other, Vector3D):
            #print 'Subtracting a Vector3D from a point to get a point.'
            t = point3D()
        elif isinstance(Other, point3D):
            #print 'Subtracting a point from a point to get a Vector3D.'
            t = Vector3D()
        t.x = self.x - Other.x
        t.y = self.y - Other.y
        t.z = self.z - Other.z
        return t
                 
