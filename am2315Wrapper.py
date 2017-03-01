# am2315Wrapper.py by ThreeSixes (https://github.com/ThreeSixes/py-am2315)
# This was originally part of the OpenWeatherStn project (https://github.com/ThreeSixes/OpenWeatherStn)

###########
# Imports #
###########

import traceback
from am2315 import am2315

#######################
# Main execution body #
#######################

class am2315Wrapper():
    def __init__(self, am2315Addr = 0x5c, i2cBusID = 1):
        """
        am2315Wrapper is a class wrapper class for the I2C-connected AOSONG AM2315 driver. The constructor for this class accepts two optional argements:
        
        am3215Addr: I2C address of the sensor, but will default to 0x5c if it's not specified. This defaults to 0x5c.
        i2cBusID: Bus ID number that the sensor is attached to. This defaults to 1 (the default bus ID on newer Raspberry Pis.)
        """
        
        # Set up AM2315 object.
        self.__am2315 = am2315(am2315Addr, i2cBusID)
    
    def getTempHumid(self):
        """
        Get wrapped temperature in degrees C, and relative hmidity in %rH as a dictioanry.
        """
        
        # Set up return value.
        retVal = {}
        
        # Grab readings.
        readings = self.__am2315.getTempHumid()
        
        # Add them to the dictionary.
        retVal.update({'temperature': readings[0], 'humidity': readings[1]})
        
        # Return it all.
        return retVal
