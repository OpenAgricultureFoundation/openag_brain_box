# am2315 class by ThreeSixes (https://github.com/ThreeSixes/py-am2315)
# This was originally part of the OpenWeatherStn project (https://github.com/ThreeSixes/OpenWeatherStn)

###########
# Imports #
###########

import time
import quick2wire.i2c as qI2c

################
# am2315 class #
################

class am2315:
    """
    am2315 is a class that supports communication with an I2C-connected AOSONG AM2315 encased temperature and humidity sensor. The constructor for this class accepts one argement:
    
    am3215Addr: I2C address of the sensor, but will default to 0x5c if it's not specified. This defaults to 0x5c.
    i2cBusID: Bus ID number that the sensor is attached to. This defaults to 1 (the default bus ID on newer Raspberry Pis.)
    """

    # The config variables are based on the AM2315 datasheet
    def __init__(self, am2315Addr = 0x5c, i2cBusID = 1):
        # Set up I2C libraries
        self.__i2c = qI2c
        self.__i2cMaster = qI2c.I2CMaster(1)
        
        # Set global address var
        self.__addr = am2315Addr
        
        # AM2315 Registers
        self.regRhMSB = 0x00
        self.regRhLSB = 0x01
        self.regTmpMSB = 0x02
        self.regTmpLSB = 0x03
        self.regModelHi = 0x08
        self.regModelLo = 0x09
        self.regVersion = 0x0a
        self.regIDA = 0x0b
        self.regIDB = 0x0c
        self.regIDD = 0x0d
        self.regIDE = 0x0e
        self.regStat = 0x0f
        self.regUsrAMSB = 0x10
        self.regUsrALSB = 0x11
        self.regUsrBMSB = 0x12
        self.regUsrBLSB = 0x13
        
        # Commands
        self.cmdReadReg = 0x03
    
    def __getSigned(self, unsigned):
        """
        __getSigned(number)
        
        Converts the temp reading from the AM2315 to a signed int. 
        """
        
        signednum = 0
        
        # If we have the negative temp bit set
        if (unsigned & 0x8000) == 0x8000:
            # Clear the negative sign bit, and make the number negative.
           signednum = 0 - (unsigned & 0x7fff)
        else:
            signednum = unsigned
        
        # Return the unsigned int.
        return signednum
        
    def getTempHumid(self):
        """
        getTempHumid()
        
        Get the temperature and humidity from the sensor. Returns an array with two integers - temp. [0] and humidity [1]
        """
        
        # Track temperature data.
        tempRaw = 0
        humidRaw = 0
        
        # Raw temperature and humidity data.
        rawTH = 0
        
        # Return value
        retVal = []
        
        # Loop sentinel values
        failCount = 0
        notDone = True
        
        # Commands to get data temp and humidity data from AM2315
        thCmd = bytearray([0x00,0x04])
        
        # If we have failed more than twice to read the data, or have finished getting data break the loop.
        while ((failCount < 2) and notDone):
            
            try:
                # Request data from the sensor, using a reference to the command bytes.
                self.__i2cMaster.transaction(self.__i2c.writing_bytes(self.__addr, self.cmdReadReg, *thCmd))
                
                # Wait for the sensor to supply data to read.
                time.sleep(0.1)
                
                # Now read 8 bytes from the AM2315.
                rawTH = self.__i2cMaster.transaction(self.__i2c.reading(self.__addr, 8))
                
                # Break the string we want out of the array the transaction returns.
                rawTH = bytearray(rawTH[0])
                
                # Confirm the command worked by checking the response for the command we executed
                # and the number of bytes we asked for.
                if (rawTH[0] == self.cmdReadReg) and (rawTH[1] == 0x04):
                    
                    # We're done. flag the loop to exit so we can interpret the data sent back to us.
                    notDone = False
            
            # We usually fail to read data 50% of the time because the sensor goes to sleep, so try twice.
            except IOError:
                if failCount > 1:
                    raise IOError("am2315 IO Error: failed to read from sensor.")
                else:
                    failCount = failCount + 1
        
        # And the MSB and LSB for each value together to yield our raw values.
        humidRaw = (rawTH[2] << 8) | rawTH[3]
        
        # Get signed int from AND'd temperature bytes.
        tempRaw = self.__getSigned((rawTH[4] << 8) | rawTH[5])
        
        # The return data is sacled up by 10x, so compensate.
        retVal.append(tempRaw / 10.0)
        retVal.append(humidRaw / 10.0)
        
        return retVal
