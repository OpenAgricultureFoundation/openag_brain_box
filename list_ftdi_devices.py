#!/usr/bin/python3

import pylibftdi
from pylibftdi import Driver

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


print(get_ftdi_device_list())
