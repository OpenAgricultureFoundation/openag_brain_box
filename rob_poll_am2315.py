#!/usr/bin/env python3
 
import time
from am2315 import AM2315
import logging
logging.basicConfig()
logger = logging.getLogger(__name__)
#logger.setLevel(logging.INFO)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('/tmp/main.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
 
 
if __name__ == "__main__":
    am2315_1 = AM2315()
 
    while True:
        am2315_1.poll()
        am2315_1.transmitToConsole()
        time.sleep(1)
