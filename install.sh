#!/bin/bash

# Install Memcached
echo *** Installing Memcached ***
sudo pip install python-memcached
sudo pip3 install python3-memcached

# Install pylibftdi
echo *** Installing pylibftdi ***
sudo pip3 install pylibftdi

# Install quick2wire
echo *** Installing quick2wire ***
sudo pip3 install quick2wire-api

# Install w1thermsensor
echo *** Installing w1thermsensor ***
sudo apt-get install w1thermsensor

# Install opencv
echo *** Installing opencv ***
sudo apt-get install python-opencv

# Install fswebcam
echo *** Installing fswebcam ***
sudo apt-get install fswebcam
