"""
Code for interfacing with Atlas Scientific ec sensor connected to usb adaptor board
"""
from atlas_device import AtlasDevice
import logging, time
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class AtlasEc:
    """
    Class that represents an Atlas Scientific ec sensor instance and provides functions
    for interfacing with the sensor.
    """

    def __init__(self, device_id, pseudo=False):
        logger.debug('Initializing sensor')
        self.device_id = device_id # TODO: auto detect ids, i wonder if atlas
        # circuit ids have a consistent pattern to differentiate between ph & ec
        self.pseudo = pseudo
        self.sensor_is_connected = False
        self.ec = None
        self.connect()

    def connect(self):
        if self.pseudo:
            logger.info('Connected to pseudo sensor')
            return
        try:
            self.device = AtlasDevice(self.device_id)
            self.device.send_cmd('C,0') # turn off continuous mode
            time.sleep(1)
            self.device.flush()
            self.sensor_is_connected = True
            logger.info('Connected to sensor')
        except:
            if self.sensor_is_connected:
                logger.warning('Unable to connect to sensor')
                self.sensor_is_connected = False


    def poll(self):
        if self.pseudo:
            self.ec = 2.2
            return
        if self.sensor_is_connected:
            try:
                self.device.send_cmd("R")
                lines = self.device.read_lines()
                for i in range(len(lines)):
                    if lines[i] != u'*OK\r':
                        floats = [float(x) for x in lines[i].split(',')]
                        self.ec = floats[0] / 1000 # ms/cm
            except:
                self.ec = None
                self.sensor_is_connected = False
        else:
            self.connect()

    def transmitToConsole(self):
        if self.ec is not None:
            print('AtlasEc EC: ', self.ec, 'ms/cm')

    def transmitToMemcache(self, memcache_shared, id='ec'):
        if self.ec is not None:
            memcache_shared.set(id, '{0:.1f}'.format(self.ec))
