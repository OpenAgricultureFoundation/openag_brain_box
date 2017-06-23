# Brain Box V2 Spec
This will be a custom PCB based off the beaglebone with an optional solder-in microcontroller for creating the option of standalone control and can be intefaced with via i2c.

## Priorities
- Flexibility & performance are high priority
- Cost is lower priority but obviously lower cost is better

## Interoperability
- Let the same brain be used for the PFC2 / Fermentabot / Food Server

## Sensors
- Support for (used currently): 1-wire (1), i2c (4), serial (1), analog (0), and digital (1) sensors 
     - What it is sensing, Part Name, Communication Protocol, Physical Connection
     - Temperature/Humidity, AM2315, I2C, Molex connector 
     - CO2, MHZ16, UART, Molex connector push in wire
     - pH, Atlas pH sensor, I2C, soldered to the PCB
     - EC, Atlas EC sensor, I2C, soldered to the PCB
     - H20 Temp, DS18B29, 1-Wire, Molex connector
     - H20 Level, LLE102000, Digital, Molex connector 
     - Light Intesity, TSL2561, I2C, soldered to PCB and Molex connector 
- Five extra ports for future sensors corresponding with logical pin selection on the Beagle Bone, and secondary microprocessor  


## Actuators
- Relays for AC or >5A DC. 10A relays likely sufficient. (12 Total)
     - Airflow
     - Aerator
     - H20 Pump
     - Nutrient Pump
     - C02 Solenoid
     - Humidifier
     - Dehumidifier
     - pH Pump +
     - pH Pump -
     - 3 Additional relays for future use
 -  Relay circuits will include the following:
     - Fuses in line with the main load
     - Catch Diode or TVS 
     - Logical level control
     - Optoisolation    
- Transistors for <5A 12VDC at minimum (ideally support higher current and any device <40VDC) (5 total)
     - Air Heater
     - H20 Heater
     - Grow Lights
     - 2 Additional transistors for future use

## Power Systems
- 12VDC Input line with power conditioning to include:
     - Minimum 470uF bulk capacitance
     - .1uF bypass capacitors by key components
     - Main replaceable or resettable Fuse
     - 5VDC Regulator (need to spec. current)
     - Transient protection TVS on input
     - Best noise reduction practices and isolation from analog components


## Dimensions
-Max 8" x 6"

## Other
- Conformal coating for occasional H20 contact
- Status LEDs for each major system
- Probe points for easy debugging
- Internal diagnostic test
- SD card for internal data logging

## Bonus Features
- Power sensing of each system
