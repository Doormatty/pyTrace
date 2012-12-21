'''
Created on Apr 15, 2012

@author: matt
'''

from Normal import Normal
import math

class Vector3D:
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
     
    # ^ - Cross Product
    def __xor__(self, Vec):
        tVec = Vector3D()
        tVec.x = (self.y * Vec.z) - (self.z * Vec.y)
        tVec.y = (self.z * Vec.x) - (self.x * Vec.z)
        tVec.z = (self.x * Vec.y) - (self.y * Vec.x)
        return tVec
        
    def __add__(self, Vec):
        tVec = Vector3D()
        tVec.x = Vec.x + self.x
        tVec.y = Vec.y + self.y
        tVec.z = Vec.z + self.z
        return tVec

    def __sub__(self, Vec):
        tVec = Vector3D()
        tVec.x = self.x - Vec.x
        tVec.y = self.y - Vec.y
        tVec.z = self.z - Vec.z
        return tVec
    
        # % - Dot Product        
    
    def __mod__(self, Vec):
        tF = 0.0
        tF += self.x * Vec.x
        tF += self.y * Vec.y
        tF += self.z * Vec.z
        return tF
    
    def __mul__(self, Other):
        if isinstance(Other, Vector3D):
            #print Vector3D/Vector3D Dot Product to get a Float'
            tF = 0.0
            tF += self.x * Other.x
            tF += self.y * Other.y
            tF += self.z * Other.z
            return tF
        if isinstance(Other, Normal):
            #print 'Multiplying a Vector3D by a surface Normal to get a double'
            tF = 0.0
            tF += self.x * Other.x
            tF += self.y * Other.y
            tF += self.z * Other.z
            return tF
        tVec = Vector3D()
        tVec.x = self.x * Other
        tVec.y = self.y * Other
        tVec.z = self.z * Other
        return tVec
    
    def __rmul__(self, Other):
        if isinstance(Other, Vector3D):
            #print Vector3D/Vector3D Dot Product to get a Float'
            tF = 0.0
            tF += self.x * Other.x
            tF += self.y * Other.y
            tF += self.z * Other.z
            return tF
        if isinstance(Other, Normal):
            #print 'Multiplying a Vector3D by a surface Normal to get a double'
            tF = 0.0
            tF += self.x * Other.x
            tF += self.y * Other.y
            tF += self.z * Other.z
            return tF
        tVec = Vector3D()
        tVec.x = self.x * Other
        tVec.y = self.y * Other
        tVec.z = self.z * Other
        return tVec
    
    def __div__(self, Other):
        if Other == 0:
            #print "Division by zero attempted!"
            return False
        tVec = Vector3D()
        tVec.x = self.x / Other
        tVec.y = self.y / Other
        tVec.z = self.z / Other
        return tVec
    
    def normalize(self):
        l = self.length()
        return Vector3D(self.x / l, self.y / l, self.z / l)

    def __eq__(self, Vec):
        if (self.x == Vec.x) and (self.y == Vec.y) and (self.z == Vec.z):
            return True
        else:
            return False
    
    def length(self):
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
    
    def __str__(self):
        return "Vector3D - X:" + str(self.x) + " Y:" + str(self.y) + " Z:" + str(self.z)
