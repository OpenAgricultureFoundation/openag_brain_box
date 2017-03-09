import sys
import pygame
import pygame.camera
from pygame.locals import*
import time
import json
import memcache
import cv2
import numpy as np
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas ##
#from matplotlib.figure import Figure ##

# import matplotlib.pyplot
# import Image
#
# import pandas as pd

# from bokeh.plotting import figure, show, output_file
# from bokeh.palettes import brewer
# from bokeh.resources import CDN
# from bokeh.embed import file_html
# from bokeh.objects import PreviewSaveTool

import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


class GUI:
    def __init__(self):
        try:
            pygame.init()
            pygame.camera.init()
            pygame.mouse.set_visible(False)
            self.screen = pygame.display.set_mode((800,480),pygame.NOFRAME)
            self.cam_list = pygame.camera.list_cameras()
            self.webcam = pygame.camera.Camera(self.cam_list[0],(32,24))
            self.webcam.start()
            logger.info('Initialized pygame display')
        except:
            logger.warning('Unable to initialize pygame display')
        try:
            self.shared = memcache.Client(['127.0.0.1:11211'], debug=0)
            logger.info('Initialized memcache client')
        except:
            logger.warning('Unable to initialize memcache client')

        self.canny = False
        self.ph = '6.5'
        self.ec = '3.2'
        self.water_temp = '20.1'
        self.air_temp = '21.1'
        self.humidity = '38'
        self.co2 = '410'
        self.o2 = '17.1'
        # self.figure = matplotlib.pyplot.figure()
        # self.plot = self.figure.add_subplot(111)
        self.runSeabornEx()


    def convertFigureToSurface(self, fig):
        fig.canvas.draw()
        buf = fig.canvas.tostring_rgb()
        ncols, nrows = fig.canvas.get_width_height()
        array = np.fromstring(buf, dtype=np.uint8).reshape(nrows, ncols, 3)
        array = np.fliplr(array)
        array = np.rot90(array)
        surface = pygame.surfarray.make_surface(array)
        pygame.transform.scale(surface,(800,480))
        return surface

    def runMatplotEx(self):
        x = np.arange (0, 100, 0.1)
        y = np.sin(x)/x
        self.plot.plot(x, y)
        array = self.convertFigureToRGB(self.figure)
        array = np.fliplr(array)
        array = np.rot90(array)
        surface = pygame.surfarray.make_surface(array)
        surface = pygame.transform.scale(surface,(800,480))
        self.screen.blit(surface,(0,0))

    def runSeabornEx(self):
        self.fig, self.ax = plt.subplots()
        # sns.set(style="darkgrid")
        self.gammas = sns.load_dataset("gammas")
        sns.tsplot(data=self.gammas, time="timepoint", unit="subject",
                   condition="ROI", value="BOLD signal", ax=self.ax)

        self.surface = self.convertFigureToSurface(self.fig)
        self.screen.blit(self.surface,(0,0))

    def run(self):
        # self.blitVideoStream()
        # self.receiveSensorValuesFromMemcache()
        # self.blitSensorValues()
        # self.runMatplotEx()
        # self.runSeabornEx()
        pygame.display.update()
        self.handleEvents()

    def blitVideoStream(self):
        imagen = self.webcam.get_image()
        imagen = pygame.transform.scale(imagen,(800,480))
        if self.canny:
            imagen = self.computeCanny(imagen)

        self.screen.blit(imagen,(0,0))

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
        white = [255,255,255]
        black = [0,0,0]
        light_blue = [142,255,255]
        dark_blue = [47,114,255]

        # 3 cards unequal
        # pygame.draw.rect(self.screen, other_color, (0,0,314,77))
        # pygame.draw.rect(self.screen, air_color, (0,83,314,197))
        # pygame.draw.rect(self.screen, water_color, (0,286,314,197))

        # 3 cards equal
        # pygame.draw.rect(self.screen, other_color, (0,0,314,157))
        # pygame.draw.rect(self.screen, air_color, (0,163,314,157))
        # pygame.draw.rect(self.screen, water_color, (0,326,314,157))

        # One sensor card per
        self.createSensorCard(0, 'Air Temp: {}C'.format(self.air_temp), white, black)
        self.createSensorCard(1, 'Humidity: {} %'.format(self.humidity), light_blue, black)
        self.createSensorCard(2, 'CO2: {} ppm'.format(self.co2), white, black)
        self.createSensorCard(3, 'O2: {} %'.format(self.o2), light_blue, black)
        self.createSensorCard(4, 'Water Temp: {} C'.format(self.water_temp), white, black)
        self.createSensorCard(5, 'pH: {}'.format(self.ph), light_blue, black)
        self.createSensorCard(6, 'EC: {} ms/cm'.format(self.ec), white, black)

    def createSensorCard(self, pos, msg, box_color=None, text_color=None):
        width = 316
        height = 64
        spacing = 6
        box_colors = [[255,255,255], [0,0,0]]
        text_colors = [[0,0,0], [255,255,255]]
        x = 0
        y = (height + spacing) * pos
        font_style = 'freesans.ttf'
        font_size = 30

        if box_color is None:
            box_color = box_colors[pos%2]
        if text_color is None:
            text_color = text_colors[pos%2]

        pygame.draw.rect(self.screen, box_color, (x,y,width,height))
        font = pygame.font.SysFont(font_style, font_size)
        text_surf, text_rect = self.textObjects(msg, font, text_color)
        text_rect.center = ( (x+(width/2)), (y+(height/2)) )
        self.screen.blit(text_surf, text_rect)

    def textObjects(self, text, font, color):
        text_surface = font.render(text, True, color)
        return text_surface, text_surface.get_rect()

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE) :
                self.webcam.stop()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                x,y = pygame.mouse.get_pos()
                logger.info('{}, {}'.format(x,y))
                if 320<x<800:
                    if self.canny:
                        self.canny = False
                    else:
                        self.canny = True

    def computeCanny(self, surface):
        array = pygame.surfarray.pixels3d(surface)
        # print(array.shape)
        array = cv2.cvtColor(array, cv2.COLOR_BGR2GRAY)
        array = cv2.GaussianBlur(array, (5, 5), 0)
        array = cv2.Canny(array, 30, 150)
        return pygame.surfarray.make_surface(array)
