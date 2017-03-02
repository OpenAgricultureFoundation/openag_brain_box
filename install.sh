#!/bin/bash

# Install Memcached
echo *** Installing Memcached ***
sudo pip3 install python-memcached python3-memcached

# Install pylibftdi
echo *** Installing pylibftdi ***
sudo pip3 install pylibftdi

# Install quick2wire
echo *** Installing quick2wire ***
sudo pip3 install quick2wire-api

# Install w1thermsensor
echo *** Installing w1thermsensor ***
sudo apt-get install w1thermsensor
