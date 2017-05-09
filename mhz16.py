"""
This module consists of code for interacting with a MHZ16 CO2 sensor.
"""

import NDIR
import time
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('main.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class MHZ16:
    """
    Class that represents a MHZ16 CO2 sensor instance and provides functions
    for interfacing with the sensor.
    """

    def __init__(self, i2c_addr=0x4D, pseudo=False):
        logger.debug('Initializing sensor')
        self.i2c_addr = i2c_addr
        self.pseudo = pseudo
        self.sensor_is_connected = False
        self.co2 = None
        self.connect()

    def connect(self):
        logger.debug('Trying to connect to sensor')

        if self.pseudo:
            logger.info('Connected as a pseudo sensor')
            return
        try:
            self.sensor = NDIR.Sensor(0x4D)
            self.sensor.begin()
            self.sensor_is_connected = True
            logger.info('Connected to sensor')
        except:
            self.sensor_is_connected = False
            logger.warning('Unable to connect to sensor')

    def poll(self):
        if self.pseudo:
            self.co2 = 415
            return

        if self.sensor_is_connected:
            try:
                self.sensor.measure()
                self.co2 = self.sensor.ppm
            except:
                self.co2 = None
                self.sensor_is_connected = False
        else:
            self.connect()

    def transmitToConsole(self, id='CO2'):
        if self.co2 is not None:
            print(id, ': ', self.co2, 'ppm')

    def transmitToMemcache(self, memcache_shared, id='co2'):
        if self.co2 is not None:
            logger.debug("Transmitting value to memcache: '{}': '{}'".format(id, self.co2))
            memcache_shared.set(id, "{0:.0f}".format(self.co2))
