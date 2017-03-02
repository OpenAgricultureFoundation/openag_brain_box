# Brain box v0.00001b

Brain box proof of concept. Hardware features a raspberry pi with 7" multipoint touch screen, high resolution camera, relay board for connecting multi-spectral leds, sensors for air temperature, humidity, co2, o2, water temperature, ph, and ec - all packed into a rugged encolsure. 

## Touchscreen interface with real-time sensor readouts & live (0.01 Hz) image
![ui_image] (photos/ui_image.jpeg)

## Touch the image, BOOM! canny edge detection overlay
![ui_canny] (photos/ui_canny.jpeg)

## Now just imagine this mess of wires...
![wires] (photos/wires.jpeg)

## ... neatly packed into this sealed box
![box] (photos/box.jpeg)

# Software Installation
From Raspbian Jessie

Run install script
```
./install.sh
```

## Fixes for DS18B20's w1thermsensor dependency
Edit boot config file
```
sudo nano /boot/config.txt
```
Add to end of file
```
dtoverlay=w1-gpio
```
Source: http://raspberrypi.stackexchange.com/questions/26623/ds18b20-not-listed-in-sys-bus-w1-devices

## Fixes for Atlas Scientific sensors
Create udev rule file
```
sudo nano /etc/udev/rules.d/99-libftdi.rules
```
Add to file:
```
SUBSYSTEMS=="usb", ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6015", GROUP="dialout", MODE="0660", SYMLINK+="FTDISerial_Converter_$attr{serial}"
```
Restart udev service
```
sudo service udev restart
```
Modify ftdi file
```
sudo nano /usr/local/lib/python3.4/dist-packages/pylibftdi/driver.py
```
At line 70, change this:
```
USB_PID_LIST = [0x6001, 0x6010, 0x6011, 0x6014]
```
To this:
```
USB_PID_LIST = [0x6001, 0x6010, 0x6011, 0x6014, 0x6015]  
```
Verify installation:
```
python3 -m pylibftdi.examples.list_devices
```
Source: https://github.com/AtlasScientific/Raspberry-Pi-sample-code







