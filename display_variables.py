import memcache
import time
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
    display_variables = ["desired_air_temperature", "desired_humidity",
    "air_temperature", "humidity", "co2", "o2", "water_temperature", "ph", "ec",
    "heater_is_on", "humidifier_is_on"]

    start_time = time.time() - 3570 # display vars after 30 sec operation
    variable_dict = {}
    while True:
        current_variables_file = open('/home/pi/openag_brain_box/ui/current_variables.csv', 'w')
        for variable in display_variables:
            value = shared.get(variable)
            current_variables_file.write("{}: {}\n".format(variable, value))
            variable_dict[variable] = value
        current_variables_file.close()
        time.sleep(1)

        if time.time() - start_time > 3600: # Output all current variables to log every hour
            start_time = time.time()
            logger.info("Current variables: {}".format(variable_dict))
