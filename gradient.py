from audioop import minmax

from PIL import Image
import math
import colorsys
from perlin_noise import PerlinNoise



class GetColorFrom2DNoise():
    def __init__(self, _octaves, _seed) -> None:
        self.noise = PerlinNoise(octaves=_octaves, seed=_seed)
        self.xRes = 10
        self.yRes = 10
        self.zRes = 10
        self.offSetX = 0.
        self.offSetY = 0.
    def setRes(self, x, y, z):
        self.xRes = x
        self.yRes = y
        self.zRes = z
    
    def addOffset(self, x, y):
        self.offSetX = x
        self.offSetY = y

    def getGrad(self, x, y):
        return self.noise([(x/self.xRes) + self.offSetX, (y/self.yRes) + self.offSetY])
    
    def getColorRGB(self, x, y, hughOffset):  
        grad = self.getGrad(x, y)
        grad += 0.5
        grad *= 0.5
        grad += hughOffset
        
        if(grad < 0.):
            grad = 0.
        elif(grad > 1.):
            grad = 1.
        
        color = colorsys.hsv_to_rgb(grad, 1., 1.)
        return color
    
    def makeImage(self):
        res = 256
        img = Image.new("RGB", (res, res), color=(0,0,0))
        noise = PerlinNoise(octaves=1, seed=1)
        xpix, ypix = res, res
        im = []

        for x in range(xpix):
            for y in range(ypix):
                grad = noise([x/xpix, y/ypix])
                grad *= 255
                newCol = (int(grad), int(grad), int(grad))
                img.putpixel((x, y),newCol)

        img.save("radial.png")

#gen = GetColorFrom2DNoise(4, 10)
#gen.makeImage()


        

        


