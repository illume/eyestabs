import pygame
import sys

from glob import glob

files = glob("*.tga")


surf = pygame.Surface((10000,10000))

print "surf!"
sys.stdout.flush()

y = 0
x = 0
for f in files:
    print f
    sys.stdout.flush()

    s = pygame.image.load(f)

    if x + s.get_width() > surf.get_width():
        x = 0
        y += s.get_height()

    surf.blit(s, (x,y))



pygame.image.save(surf, "bigstrip.jpg")

