import memcache
shared = memcache.Client(['127.0.0.1:11211'], debug=0)
import string
import pylibftdi
from pylibftdi.device import Device
from pylibftdi.driver import FtdiError
from pylibftdi import Driver
import os
import time
from am2315 import am2315
from w1thermsensor import W1ThermSensor
import NDIR


class AtlasDevice(Device):
	def __init__(self, sn):
		Device.__init__(self, mode='t', device_id=sn)


	def read_line(self, size=0):
		"""
		taken from the ftdi library and modified to 
		use the ezo line separator "\r"
		"""
		lsl = len('\r')
		line_buffer = []
		while True:
			next_char = self.read(1)
			if next_char == '' or (size > 0 and len(line_buffer) > size):
				break
			line_buffer.append(next_char)
			if (len(line_buffer) >= lsl and
					line_buffer[-lsl:] == list('\r')):
				break
		return ''.join(line_buffer)
	
	def read_lines(self):
		"""
		also taken from ftdi lib to work with modified readline function
		"""
		lines = []
		try:
			while True:
				line = self.read_line()
				if not line:
					break
					self.flush_input()
				lines.append(line)
			return lines
		
		except FtdiError:
			print("Failed to read from the sensor.")
			return ''		

	def send_cmd(self, cmd):
		"""
		Send command to the Atlas Sensor.
		Before sending, add Carriage Return at the end of the command.
		:param cmd:
		:return:
		"""
		buf = cmd + "\r"     	# add carriage return
		try:
			self.write(buf)
			return True
		except FtdiError:
			print ("Failed to send command to the sensor.")
			return False
			
			
			
def get_ftdi_device_list():
	"""
	return a list of lines, each a colon-separated
	vendor:product:serial summary of detected devices
	"""
	dev_list = []
	
	for device in Driver().list_devices():
		# list_devices returns bytes rather than strings
		dev_info = map(lambda x: x.decode('latin1'), device)
		# device must always be this triple
		vendor, product, serial = dev_info
		dev_list.append(serial)
	return dev_list


def atlasPhInit(device_id):
    #print(get_ftdi_device_list())
    dev = AtlasDevice(device_id)
    dev.send_cmd("C,0") # turn off continuous mode
    time.sleep(1)
    dev.flush()
    return dev

def atlasPhUpdate(dev):
    dev.send_cmd("R")
    lines = dev.read_lines()
    for i in range(len(lines)):
        if lines[i] != u'*OK\r':
            ph = float(lines[i])
            ph_str = "{0:.1f}".format(ph)
            shared.set('ph', ph_str)
            #print(ph_str)

def atlasEcInit(device_id):
    dev = AtlasDevice(device_id)
    dev.send_cmd("C,0") # turn off continuous mode
    time.sleep(1)
    dev.flush()
    return dev

def atlasEcUpdate(dev):
    dev.send_cmd("R")
    lines = dev.read_lines()
    for i in range(len(lines)):
        if lines[i] != u'*OK\r':
            floats = [float(x) for x in lines[i].split(',')]
            ec = floats[0] / 1000 # ms/cm
            ec_str = "{0:.1f}".format(ec)
            shared.set('ec', ec_str)
            #print(ec_str)


def am2315Init():
    sensor = am2315()
    return sensor

def am2315Update(sensor):
    data = sensor.getTempHumid()
    temp = data[0]
    temp_str = "{0:.1f}".format(temp)
    shared.set('air_temp', temp_str)
    #print(temp_str)
    hum = data[1]
    hum_str = "{0:.1f}".format(hum)
    shared.set('humidity', hum_str)
    #print(hum_str)


def ds18b20Init():
    sensor = W1ThermSensor()
    return sensor

def ds18b20Update(sensor):
    temp = sensor.get_temperature()
    temp_str = "{0:.1f}".format(temp)
    shared.set('water_temp', temp_str)
    #print(temp_str)

def mhz16Init():
    sensor = NDIR.Sensor(0x4D)
    sensor.begin()
    return sensor

def mhz16Update(sensor):
    sensor.measure()
    co2 = sensor.ppm
    co2_str = "{0:.0f}".format(co2)
    shared.set('co2', co2_str)

if __name__ == '__main__':
    atlas_ph = atlasPhInit('DO009P10')
    atlas_ec = atlasEcInit('DJ00RV6G')
    am2315 = am2315Init()
    ds18b20 = ds18b20Init()
    mhz16 = mhz16Init()    

    while 1:
        atlasPhUpdate(atlas_ph)
        atlasEcUpdate(atlas_ec)
        am2315Update(am2315)
        ds18b20Update(ds18b20)
        mhz16Update(mhz16)    
        time.sleep(1)
