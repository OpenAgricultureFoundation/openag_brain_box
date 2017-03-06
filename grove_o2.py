"""
This module consists of code for interacting with a Grove O2 sensor.
"""

import serial

class GroveO2:
    """
    Class that represents a Grove O2 sensor instance and provides functions
    for interfacing with the sensor.
    """

    def __init__(self, analog_port=0, serial_port='/dev/serial/by-id/usb-Numato_Systems_Pvt._Ltd._Numato_Lab_8_Channel_USB_GPIO_Module-if00', pseudo=False):
        self.analog_port = analog_port
        self.serial_port = serial_port
        self.pseudo = pseudo
        self.o2 = None
        self.sensor_is_connected = True

        self.connect()

    def connect(self):
        if self.pseudo:
            print('Connected to pseudo Grove O2 sensor')
            return
        try:
            self.serial = serial.Serial(self.serial_port, 19200, timeout=1)
            if not self.sensor_is_connected:
                self.sensor_is_connected = True
                print('Connected to Grove O2 sensor')
        except:
            if self.sensor_is_connected:
                self.sensor_is_connected = False
                print('Unable to connect to Grove O2 sensor')

    def poll(self):
        if self.pseudo:
            self.o2 = 19.3
            return
        if self.sensor_is_connected:
            try:
                self.serial.write(('adc read {}\r'.format(self.analog_port)).encode())
                response = port.read(25)
                voltage = float(response[10:-3]) * 5 / 1024
                o2 = voltage * 0.21 / 2.0 * 100 # percent
            except:
                self.o2 = None
                self.sensor_is_connected = False
        else:
            self.connect()

    def transmitToConsole(self, id='O2'):
        if self.o2 is not None:
            print(id, ': ', self.o2, '%')

    def transmitToMemcache(self, memcache_shared, id='o2'):
        if self.o2 is not None:
            memcache_shared.set(id, '{0:.0f}'.format(self.o2))
