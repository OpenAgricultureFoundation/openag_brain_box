import sys
import time
import pygame
import pygame.camera
from pygame.locals import *

pygame.init()
pygame.camera.init()
cam = pygame.camera.Camera("/dev/video0",(640,480))
cam.start()

screen = pygame.display.set_mode((640,480))

while 1:
        image = cam.get_image()
        data = pygame.image.tostring(image,"RGB")
        img = pygame.image.fromstring(data,(640,480),"RGB")
        screen.blit(img,(0,0))
        pygame.display.update()
