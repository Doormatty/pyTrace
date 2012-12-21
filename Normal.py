'''
Created on Apr 15, 2012

@author: matt
'''
class Normal:
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
            
    def __mul__(self, Norm):
        tF = 0.0
        tF += self.x * Norm.x
        tF += self.y * Norm.y
        tF += self.z * Norm.z
        return tF
            
    def __str__(self):
        return "Normal - X:" + str(self.x) + " Y:" + str(self.y) + " Z:" + str(self.z)
