import pygame
xres = 640
yres = 480
psize = 1
pygame.init()
windowSurfaceObj = pygame.display.set_mode((xres, yres))
pygame.display.set_caption("Matt's Ray Tracer")
pixArr = pygame.PixelArray(windowSurfaceObj) 
for y in range(yres):
    for x in range(xres):
        pixArr[x][y] = pygame.Color(255, 0, 0)
    pygame.display.update()
del pixArr
for event in pygame.event.get():
    if event.type == QUIT:
            pygame.quit()
            sys.exit()