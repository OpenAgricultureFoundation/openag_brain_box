import time
import datetime
import os
import memcache
import logging
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('main.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class DataLogger:
    def __init__(self, log_variables):
        self.shared = memcache.Client(['127.0.0.1:11211'], debug=0)
        self.log_variables = log_variables

    def run(self):
        for variable in self.log_variables:
            value = self.shared.get(variable)
            if value is not None:
                self.logToCsv(variable, value, 0.01)

    def logToCsv(self, variable, value, variance):
        value = float(value)
        date = str(datetime.date.today())
        file_name = "data/{}/{}-{}.csv".format(variable, date, variable)

        new_file = False
        if not os.path.exists(os.path.dirname(file_name)):
            try:
                os.makedirs(os.path.dirname(file_name))
                new_file = True
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        with open(file_name, "a+") as log_file: # append to file
            # Create new file if does not exist
            if new_file:
                logger.info("Creating new log file: {}".format(file_name))
                log_file.write("time,{}\n".format(variable)) # add csv headers
                log_file.write("{},{}\n".format(time.time(), value))

            else:
                # Get previously logged value
                lines = log_file.readlines()
                split_line = lines[-1].split(',')
                previous_value = float(split_line[1].strip())

                # Only log new values
                if abs(value) > (previous_value) * (1 + variance) or  abs(value) < (previous_value) * (1 - variance):
                    logger.info("Logging: {},{} to file: {}".format(time.time(), value, file_name))
                    log_file.write("{},{}\n".format(time.time(), value))
                else:
                    logger.debug("Not logging to file: {}, Value = {}, Previous Value = {}".format(file_name, value, previous_value))

            log_file.close()
