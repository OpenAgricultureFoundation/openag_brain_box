from data_logger import DataLogger
import time

if __name__ == "__main__":
    log_variables = ["air_temperature", "humidity", "co2", "o2",
    "water_temperature", "ph", "ec", "heater_is_on", "humidifier_is_on"]
    data_logger = DataLogger(log_variables)

    while True:
        data_logger.run()
        time.sleep(1)
