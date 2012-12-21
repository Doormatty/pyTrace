'''
Created on Apr 15, 2012

@author: matt
'''

from RGB import RGB

class Material:
    color = RGB()
    opacity = 1.0
    reflect = 0.0
    luma = 0.0
    def __init__(self, color = RGB(0, 0, 0), opacity = 1.0, reflect = 0.0, luma = 0.0):
        self.color = color
        self.opacity = opacity
        self.reflect = reflect
        self.luma = luma     
    
    def __str__(self):
        return "Material - Color=" + str(self.color) + ", Opacity=" + str(self.opacity) + ", Reflectiveness=" + str(self.reflect) + " Luma=" + str(self.luma)

