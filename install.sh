#!/bin/bash

# Install Memcached
sudo pip install python-memcached
sudo pip3 install python3-memcached

# Install pylibftdi
sudo apt-get install libftdi-dev
sudo pip3 install pylibftdi

# Install quick2wire
sudo pip3 install quick2wire-api

# Install w1thermsensor
sudo apt-get install python3-w1thermsensor

# Install opencv
sudo apt-get install python-opencv

# Install fswebcam
sudo apt-get install fswebcam

# Fix incorrect mouse detection with pygame in raspbian jessie environment
# Note: not sure if this is actually necessary. running gui from local machine,
# the mouse detection is accurate. when launching gui script from remote
# machine (via ssh), the mouse tracking is off. in practice, this is a non-issue
# since the ui will always be launched at startup. however without knowing this,
# it can made development frustrating....just going to comment this out for now
# chmod +x installsdl.sh
# ./installsdl.sh
