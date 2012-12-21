'''
Created on Apr 15, 2012

@author: matt
'''
class RGB:
    r = 0.0
    g = 0.0
    b = 0.0
    def __init__(self, rr = 0.0, gg = 0.0, bb = 0.0):
        if rr > 1.0:
            self.r = 1.0
        elif rr < 0.0:
            self.r = 0.0
        else:
            self.r = rr
        
        if gg > 1.0:
            self.g = 1.0
        elif gg < 0.0:
            self.g = 0.0
        else:
            self.g = gg
        
        if bb > 1.0:
            self.b = 1.0
        elif bb < 0.0:
            self.b = 0.0
        else:
            self.b = bb
            
    def __add__(self, oRGB):
        tRGB = RGB()
        if oRGB.r + self.r > 1.0:
            tRGB.r = 1.0
        elif oRGB.r + self.r < 0.0:
            tRGB.r = 0.0
        else:
            tRGB.r = oRGB.r + self.r
        
        if oRGB.g + self.g > 1.0:
            tRGB.g = 1.0
        elif oRGB.g + self.g < 0.0:
            tRGB.g = 0.0
        else:
            tRGB.g = oRGB.g + self.g
        
        if oRGB.b + self.b > 1.0:
            tRGB.b = 1.0
        elif oRGB.b + self.b < 0.0:
            tRGB.b = 0.0
        else:
            tRGB.b = oRGB.b + self.b
        return tRGB
    
    def __sub__(self, oRGB):
        tRGB = RGB()
        if self.r - oRGB.r > 1.0:
            tRGB.r = 1.0
        elif self.r - oRGB.r < 0.0:
            tRGB.r = 0.0
        else:
            tRGB.r = self.r - oRGB.r
        
        if self.g - oRGB.g > 1.0:
            tRGB.g = 1.0
        elif self.g - oRGB.g < 0.0:
            tRGB.g = 0.0
        else:
            tRGB.g = self.g - oRGB.g
        
        if self.b - oRGB.b > 1.0:
            tRGB.b = 1.0
        elif self.b - oRGB.b < 0.0:
            tRGB.b = 0.0
        else:
            tRGB.b = self.b - oRGB.b
        return tRGB
    
    def __mul__(self, num):
        tRGB = RGB()
        if self.r * num > 1.0:
            tRGB.r = 1.0
        elif self.r * num < 0.0:
            tRGB.r = 0.0
        else:
            tRGB.r = self.r * num
        
        if self.g * num > 1.0:
            tRGB.g = 1.0
        elif self.g * num < 0.0:
            tRGB.g = 0.0
        else:
            tRGB.g = self.g * num
        
        if self.b * num > 1.0:
            tRGB.b = 1.0
        elif self.b * num < 0.0:
            tRGB.b = 0.0
        else:
            tRGB.b = self.b * num
        return tRGB
    
    def finalcolor(self):
        tr = int(self.r * 255)
        tg = int(self.g * 255)
        tb = int(self.b * 255)
        return (tr, tg, tb)

    def __eq__(self, oRGB):
        if (round(self.r, 5) == round(oRGB.r, 5)) and (round(self.g, 5) == round(oRGB.g, 5)) and (round(self.b, 5) == round(oRGB.b, 5)):
            return True
        else:
            return False
        
    def __str__(self):
        return "RGB - R:" + str(self.r) + " G:" + str(self.g) + " B:" + str(self.b)
