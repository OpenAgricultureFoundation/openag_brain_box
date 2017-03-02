#!/bin/bash

# Install LifePO4wered
echo *** Installing LiFePO4wered ***
cd ~/
git clone https://github.com/xorbit/LiFePO4wered-Pi.git
cd ~/LiFePO4wered-Pi
./build.py
sudo ./INSTALL.sh
echo *** Configure LiFePO4wered ***
lifepo4wered-cli set auto_boot 1
