import sys
import pygame
import pygame.camera
from pygame.locals import*
import time
import json
import memcache
import cv2
import numpy as np

class GUI:
    def __init__(self):
        pygame.init()
        pygame.camera.init()
        pygame.mouse.set_visible(False)

        self.shared = memcache.Client(['127.0.0.1:11211'], debug=0)
        self.canny = False
        self.screen = pygame.display.set_mode((800,480),0)
        self.cam_list = pygame.camera.list_cameras()
        self.webcam = pygame.camera.Camera(self.cam_list[0],(32,24))
        self.webcam.start()
        self.myfont = pygame.font.SysFont("monospace", 20)
        self.ph = '6.5'
        self.ec = '3.2'
        self.water_temp = '20.1'
        self.air_temp = '21.1'
        self.humidity = '38'
        self.co2 = '410'
        self.o2 = '17.1'

    def run(self):
        self.blitVideoStream()
        self.receiveSensorValuesFromMemcache()
        self.blitSensorValues()
        pygame.display.update()
        self.handleEvents()

    def blitVideoStream(self):
        imagen = self.webcam.get_image()
        imagen = pygame.transform.scale(imagen,(480,480))
        if self.canny:
            imagen = self.computeCanny(imagen)
        self.screen.blit(imagen,(320,0))

    def receiveSensorValuesFromMemcache(self):
        val = self.shared.get('ph')
        if val is not None:
            self.ph=val

        val = self.shared.get('ec')
        if val is not None:
            self.ec=val

        val = self.shared.get('water_temperature')
        if val is not None:
            self.water_temp=val

        val = self.shared.get('air_temperature')
        if val is not None:
            self.air_temp=val

        val = self.shared.get('humidity')
        if val is not None:
            self.humidity=val

        val = self.shared.get('co2')
        if val is not None:
            self.co2=val

        val = self.shared.get('o2')
        if val is not None:
            self.o2=val

    def blitSensorValues(self):
        air_temp_string = "air temp: " + self.air_temp + " C"
        air_temp_label = self.myfont.render(air_temp_string, 1, (255, 255, 255))

        humidity_string = "humidity: " + self.humidity + " %"
        humidity_label = self.myfont.render(humidity_string, 1, (255, 255, 255))

        co2_string = "co2: " + self.co2 + " ppm"
        co2_label = self.myfont.render(co2_string, 1, (255, 255, 255))

        o2_string = "o2: " + self.o2 + " %"
        o2_label = self.myfont.render(o2_string, 1, (255, 255, 255))

        water_temp_string = "water temp: " + self.water_temp + " C"
        water_temp_label = self.myfont.render(water_temp_string, 1, (255, 255, 255))

        ph_string = "pH: " + self.ph + " ph"
        ph_label = self.myfont.render(ph_string, 1, (255, 255, 255))

        ec_string = "ec: " + self.ec + " ms/cm"
        ec_label = self.myfont.render(ec_string, 1, (255, 255, 255))

        self.screen.blit(air_temp_label, (50, 50))
        self.screen.blit(humidity_label, (50, 100))
        self.screen.blit(co2_label, (50, 150))
        self.screen.blit(o2_label, (50, 200))
        self.screen.blit(water_temp_label, (50, 250))
        self.screen.blit(ph_label, (50, 300))
        self.screen.blit(ec_label, (50, 350))

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.webcam.stop()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                x,y = pygame.mouse.get_pos()
                if 320<x<800:
                    if self.canny:
                        self.canny = False
                    else:
                        self.canny = True

    def computeCanny(self, surface):
        array = pygame.surfarray.pixels3d(surface)
        array = cv2.cvtColor(array, cv2.COLOR_BGR2GRAY)
        array = cv2.GaussianBlur(array, (5, 5), 0)
        array = cv2.Canny(array, 30, 150)
        return pygame.surfarray.make_surface(array)
