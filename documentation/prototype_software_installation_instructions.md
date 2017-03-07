# Prototype Software Installation Instructions

## Install Raspbian Jessie to External SSD
Follow this tutorial to get Raspbian Jessie to boot from the external SSD: http://www.berryterminal.com/doku.php/berryboot

## Minimize Task Bar in Raspi desktop GUI
1. Right click on taskbar
2. Pannel settings
3. Advanced tab
4. Check the box for minimize panel when not in use
5. Set pixel count to 0

## Edit Raspi-config
Edit raspi settings
```
sudo raspi-config
```
Change the password to whatever you want

Select Advanced Options and enable SSH / I2C.

It is recommended to ssh in from an external machine now.

To get the ip of the rpi
```
ifconfig
```

Clone repo
```
cd ~/
git clone https://github.com/OpenAgInitiative/openag_brain_box.git
```

Make install script executable
```
cd ~/openag_brain_box
chmod +x install.sh
```

Run install script
```
./install.sh
```

## Finish setting up w1thermsensor for ds18b20
Edit boot config file
```
sudo nano /boot/config.txt
```
Add to end of file
```
dtoverlay=w1-gpio
```
Restart the pi
```
sudo reboot
```
Verify sensor can be seen (Note: need to have a sensor conntected)
```
w1thermsensor ls
```
Should see something that looks like:
```
HWID: 0000068b7f41 Type: DS18B20
```

Source: http://raspberrypi.stackexchange.com/questions/26623/ds18b20-not-listed-in-sys-bus-w1-devices

## Finish setting libftdi for atlas sensors
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
Should see something like this:
```
FTDI:FT230X Basic UART:DO009P10
```
Source: https://github.com/AtlasScientific/Raspberry-Pi-sample-code

## Setup capturing images every 60 seconds
Make image capture script executable
```
chmod +x ~/openag_brain_box/get_img.sh
```
Open crontab config
```
crontab -e
```
Add line
```
* * * * * /home/pi/openag_brain_box/get_img.sh
```

## Add GUI to start automatically on startup
Modify the lxde autostart config file:
```
nano /home/pi/.config/lxsession/LXDE-pi/autostart
```

Add line
```
@python /home/pi/openag_brain_box/run_gui.py
```

## Add sensor polling to start automatically on startup
Modify the rc.local file
```
sudo nano /etc/rc.local
```
Add line **BEFORE "exit 0"**:
```
python3 /home/pi/openag_brain_box/poll_sensors.py
```

## Install LiFePO4wered
Clone Repo
```
git clone https://github.com/xorbit/LiFePO4wered-Pi.git
```
Build the code
```
cd LiFePO4wered-Pi/
./build.py
```
Install the code
```
sudo ./INSTALL.sh
```
Reboot
```
sudo reboot
```
Source: https://github.com/xorbit/LiFePO4wered-Pi
