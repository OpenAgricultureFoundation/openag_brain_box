"""
Code for interfacing with Atlas Scientific ec sensor connected to usb adaptor board
"""
from atlas_device import AtlasDevice
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AtlasEc:
    """
    Class that represents an Atlas Scientific ec sensor instance and provides functions
    for interfacing with the sensor.
    """

    def __init__(self, device_id, pseudo=False):
        self.device_id = device_id # TODO: auto detect ids, i wonder if atlas
        # circuit ids have a consistent pattern to differentiate between ph & ec
        self.pseudo = pseudo
        self.sensor_is_connected = True
        self.ec = None
        self.connect()

    def connect(self):
        if self.pseudo:
            logger.info('Connected to pseudo Atlas EC sensor')
            return
        try:
            self.device = AtlasDevice(self.device_id)
            self.device.send_cmd('C,0') # turn off continuous mode
            time.sleep(1)
            dev.flush()
            logger.info('Connected to Atlas EC sensor')
        except:
            if self.sensor_is_connected:
                logger.warning('Unable to connect to Atlas EC sensor')
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

    def transmitToMemcache(self, memcache_shared, ec_id='ec'):
        if self.ec is not None:
            memcache_shared.set(id, "{0:.1f}".format(self.ec))
