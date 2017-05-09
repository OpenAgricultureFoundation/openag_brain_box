import time
import memcache
from mhz16 import MHZ16
from am2315 import AM2315
from atlas_ph import AtlasPh
from atlas_ec import AtlasEc
from ds18b20 import DS18B20
from grove_o2 import GroveO2
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('main.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# TODO: add ros transmissions
# TODO: add tests

if __name__ == '__main__':
    shared = memcache.Client(['127.0.0.1:11211'], debug=0)
    mhz16_1 = MHZ16()
    am2315_1 = AM2315()
    atlas_ph_1 = AtlasPh('DO009MQN', pseudo=True)
    atlas_ec_1 = AtlasEc('DO009N86', pseudo=True)
    ds18b20_1 = DS18B20()
    grove_o2_1 = GroveO2(pseudo=True)

    while True:
        mhz16_1.poll()
        mhz16_1.transmitToMemcache(shared)

        am2315_1.poll()
        am2315_1.transmitToMemcache(shared)

        atlas_ph_1.poll()
        atlas_ph_1.transmitToMemcache(shared)

        atlas_ec_1.poll()
        atlas_ec_1.transmitToMemcache(shared)

        ds18b20_1.poll()
        ds18b20_1.transmitToMemcache(shared)

        grove_o2_1.poll()
        grove_o2_1.transmitToMemcache(shared)

        time.sleep(1)
