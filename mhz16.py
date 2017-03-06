"""
This module consists of code for interacting with a MHZ16 CO2 sensor.
"""

# import NDIR
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MHZ16:
    """
    Class that represents a MHZ16 CO2 sensor instance and provides functions
    for interfacing with the sensor.
    """

    def __init__(self, i2c_addr=0x4D, pseudo=False):
        self.i2c_addr = i2c_addr
        self.pseudo = pseudo
        self.sensor_is_connected = True
        self.co2 = None
        self.connect()

    def connect(self):
        if self.pseudo:
            logger.info('Connected to pseudo MHZ16 CO2 sensor')
            return
        try:
            self.sensor = NDIR.Sensor(i2c_addr)
            self.sensor.begin()
            if not self.sensor_is_connected:
                self.sensor_is_connected = True
                logger.info('Connected to MHZ16 CO2 sensor')
        except:
            if self.sensor_is_connected: # Avoid saturating the logs
                 self.sensor_is_connected = False
                 logger.warning('Unable to connect to MHZ16 CO2 sensor')


    def poll(self):
        if self.pseudo:
            self.co2 = 419.8
            return
        if self.sensor_is_connected:
            try:
                sensor.measure()
                self.co2 = sensor.ppm
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
            memcache_shared.set(id, "{0:.0f}".format(self.co2))
