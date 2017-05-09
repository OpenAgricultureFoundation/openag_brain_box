import RPi.GPIO as GPIO
import time
import memcache
import csv
import logging
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('/home/pi/openag_brain_box/ui/main.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class Actuators:
    def __init__(self):
        GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
        self.shared = memcache.Client(['127.0.0.1:11211'], debug=0)
        self.relay_pins = [27,22,23,24] # <-- BCM pins, corresponding header pins [13,15,16,18] and colors [org,grn,blu,gry]
        self.ph = None
        self.ec = None
        self.water_temp = None
        self.air_temp = None
        self.humidity = None
        self.co2 = None
        self.o2 = None
        self.desired_air_temp = 30
        self.temperature_lower_band = 1
        self.heater_overshoot = 0.5
        self.desired_humidity = 85
        self.humidity_lower_band = 5
        self.humidifier_overshoot = 2.5
        self.heater_is_on = False
        self.humidifier_is_on = False

        # Check for setpoints in setpoints.csv file
        with open('/home/pi/openag_brain_box/ui/setpoints.csv', mode='r') as setpoints_file:
            reader = csv.reader(setpoints_file)
            setpoints = {rows[0]:rows[1] for rows in reader}
            logger.debug(setpoints)
            try:
                self.desired_air_temp = float(setpoints["air_temperature"])
                self.desired_humidity = float(setpoints["humidity"])
                logger.info("Set air temp to {}, humidity to {}".format(self.desired_air_temp, self.desired_humidity))
            except:
                logger.warning("Unable to parse setpoints file, setpoints are set to default values")

            self.shared.set("desired_air_temperature", "{0:.1f}".format(self.desired_air_temp))
            self.shared.set("desired_humidity", "{0:.1f}".format(self.desired_humidity))

        # Initialize relays to be OFF
        for pin in self.relay_pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.HIGH)

    def run(self):
        self.receiveSensorValuesFromMemcache()

        # Control air temperature
        if self.air_temp is not None:
            if not self.heater_is_on and self.air_temp < self.desired_air_temp - self.temperature_lower_band:
                logger.debug('Heater turning on')
                self.heater_is_on = True
                GPIO.output(self.relay_pins[2], GPIO.LOW) # turn on heater
            if self.heater_is_on and self.air_temp >= self.desired_air_temp - self.heater_overshoot:
                logger.debug('Heater turning off')
                self.heater_is_on = False
                GPIO.output(self.relay_pins[2], GPIO.HIGH) # turn off heater
        else:
            logger.warning('Unable to acquire air_temp from memcache')
        self.shared.set("heater_is_on", "{}".format(self.heater_is_on))

        # Control humidity
        if self.humidity is not None:
            if not self.humidifier_is_on and self.humidity < self.desired_humidity - self.humidity_lower_band:
                logger.debug('Humidifier turning on')
                self.humidifier_is_on = True
                GPIO.output(self.relay_pins[3], GPIO.LOW) # turn on humidifier
            if self.humidifier_is_on and self.humidity >= self.desired_humidity - self.humidifier_overshoot:
                logger.debug('Humidifier turning off')
                self.humidifier_is_on = False
                GPIO.output(self.relay_pins[3], GPIO.HIGH) # turn off humidifier
        else:
            logger.warning('Unable to acquire humidity from memcache')
        self.shared.set("humidifier_is_on", "{}".format(self.humidifier_is_on))

    def receiveSensorValuesFromMemcache(self):
        val = self.shared.get('ph')
        if val is not None:
            self.ph=float(val)

        val = self.shared.get('ec')
        if val is not None:
            self.ec=float(val)

        val = self.shared.get('water_temperature')
        if val is not None:
            self.water_temp=float(val)

        val = self.shared.get('air_temperature')
        if val is not None:
            self.air_temp=float(val)

        val = self.shared.get('humidity')
        if val is not None:
            self.humidity=float(val)

        val = self.shared.get('co2')
        if val is not None:
            self.co2=float(val)

        val = self.shared.get('o2')
        if val is not None:
            self.o2=float(val)
