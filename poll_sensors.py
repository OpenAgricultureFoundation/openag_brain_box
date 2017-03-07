import time
import memcache
from mhz16 import MHZ16
from am2315 import AM2315
from atlas_ph import AtlasPh
from atlas_ec import AtlasEc
from ds18b20 import DS18B20
from grove_o2 import GroveO2

# TODO: test this code on actual device
# TODO: add ros transmissions
# TODO: bring image acquisition into python, prevent simultaneous r/w
# TODO: add tests

if __name__ == '__main__':
    memcache_shared = memcache.Client(['127.0.0.1:11211'], debug=0)
    mhz16_1 = MHZ16(pseudo=True)
    am2315_1 = AM2315(pseudo=True)
    atlas_ph_1 = AtlasPh('DO009P10', pseudo=True)
    atlas_ec_1 = AtlasEc('DJ00RV6G', pseudo=True)
    ds18b20_1 = DS18B20(pseudo=True)
    grove_o2_1 = GroveO2(pseudo=True)

    while True:
        mhz16_1.poll()
        mhz16_1.transmitToConsole()

        am2315_1.poll()
        am2315_1.transmitToConsole()

        atlas_ph_1.poll()
        atlas_ph_1.transmitToConsole()

        atlas_ec_1.poll()
        atlas_ec_1.transmitToConsole()

        ds18b20_1.poll()
        ds18b20_1.transmitToConsole()

        grove_o2_1.poll()
        grove_o2_1.transmitToConsole()

        time.sleep(1)
