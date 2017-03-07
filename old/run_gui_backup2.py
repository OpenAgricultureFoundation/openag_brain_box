import sys
import pygame
import pygame.camera
from pygame.locals import*
import time
import json
import memcache
import cv2
import numpy as np

def computeCanny(surface):
    array = pygame.surfarray.pixels3d(surface)
    array = cv2.cvtColor(array, cv2.COLOR_BGR2GRAY)
    array = cv2.GaussianBlur(array, (5, 5), 0)
    array = cv2.Canny(array, 30, 150)
    return pygame.surfarray.make_surface(array)

shared = memcache.Client(['127.0.0.1:11211'], debug=0)

canny = False

pygame.init()
pygame.camera.init()

#create fullscreen display 640x480
screen = pygame.display.set_mode((800,480),0)
pygame.mouse.set_visible(False)

#find, open and start low-res camera
cam_list = pygame.camera.list_cameras()
webcam = pygame.camera.Camera(cam_list[0],(32,24))
webcam.start()

myfont = pygame.font.SysFont("monospace", 20)

ph = '6.5'
ec = '3.2'
water_temp = '20.1'
air_temp = '21.1'
humidity = '38'
co2 = '410'
o2 = '17.1'

while True:
    #grab image, scale and blit to screen
    imagen = webcam.get_image()
    imagen = pygame.transform.scale(imagen,(480,480))

    if canny:
        imagen = computeCanny(imagen)

    screen.blit(imagen,(320,0))


    # get sensor values
    val = shared.get('ph')
    if val is not None:
        ph=val

    val = shared.get('ec')
    if val is not None:
        ec=val

    val = shared.get('water_temp')
    if val is not None:
        water_temp=val

    val = shared.get('air_temp')
    if val is not None:
        air_temp=val

    val = shared.get('humidity')
    if val is not None:
        humidity=val

    val = shared.get('co2')
    if val is not None:
        co2=val

    val = shared.get('o2')
    if val is not None:
        o2=val

    air_temp_string = "air temp: " + air_temp + " C"
    air_temp_label = myfont.render(air_temp_string, 1, (255, 255, 255))

    humidity_string = "humidity: " + humidity + " %"
    humidity_label = myfont.render(humidity_string, 1, (255, 255, 255))

    co2_string = "co2: " + co2 + " ppm"
    co2_label = myfont.render(co2_string, 1, (255, 255, 255))

    o2_string = "o2: " + o2 + " %"
    o2_label = myfont.render(o2_string, 1, (255, 255, 255))

    water_temp_string = "water temp: " + water_temp + " C"
    water_temp_label = myfont.render(water_temp_string, 1, (255, 255, 255))

    ph_string = "pH: " + ph + " ph"
    ph_label = myfont.render(ph_string, 1, (255, 255, 255))

    ec_string = "ec: " + ec + " ms/cm"
    ec_label = myfont.render(ec_string, 1, (255, 255, 255))

    screen.blit(air_temp_label, (50, 50))
    screen.blit(humidity_label, (50, 100))
    screen.blit(co2_label, (50, 150))
    screen.blit(o2_label, (50, 200))
    screen.blit(water_temp_label, (50, 250))
    screen.blit(ph_label, (50, 300))
    screen.blit(ec_label, (50, 350))

    #draw all updates to display
    pygame.display.update()

    # check for quit events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            webcam.stop()
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONUP:
            x,y = pygame.mouse.get_pos()
            if 320<x<800:
                if canny:
                    canny = False
                else:
                    canny = True
