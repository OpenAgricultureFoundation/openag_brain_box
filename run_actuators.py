from actuators import Actuators
import time

if __name__ == '__main__':
    actuators = Actuators()
    time.sleep(10) # wait 10 seconds for everything else to start up

    while True:
        actuators.run()
        time.sleep(1)
