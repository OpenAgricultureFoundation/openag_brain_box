import time
import csv
import memcache
from mhz16 import MHZ16
from am2315 import AM2315
from atlas_ph import AtlasPh
from atlas_ec import AtlasEc
from ds18b20 import DS18B20
from grove_o2 import GroveO2
import logging
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('/home/pi/openag_brain_box/ui/main.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


if __name__ == "__main__":
    shared = memcache.Client(['127.0.0.1:11211'], debug=0)
    mhz16_1 = MHZ16()
    am2315_1 = AM2315()

    with open('/home/pi/openag_brain_box/ui/config.csv', mode='r') as config_file:
        reader = csv.reader(config_file)
        config = {rows[0]:rows[1] for rows in reader}
        logger.debug(config)
        atlas_ph_id = None
        atlas_ec_id = None
        try:
            atlas_ph_id = config["atlas_ph_id"]
            atlas_ec_id = config["atlas_ec_id"]
            logger.debug("Atlas pH ID is: {}, Atlas EC ID is: {}".format(atlas_ph_id, atlas_ec_id))
        except:
            logger.error("Unable to parse config file")

    atlas_ph_1 = AtlasPh(atlas_ph_id)
    atlas_ec_1 = AtlasEc(atlas_ec_id)
    ds18b20_1 = DS18B20()
    grove_o2_1 = GroveO2()

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
