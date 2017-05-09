from data_logger import DataLogger
import time
import logging
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('main.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

if __name__ == '__main__':
    log_variables = ["air_temperature", "humidity", "co2", "water_temperature"]
    data_logger = DataLogger(log_variables)

    while True:
        data_logger.run()
        time.sleep(1)
