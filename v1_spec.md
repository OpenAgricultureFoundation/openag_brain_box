# Brain Box V2 Spec
This will be a custom PCB based off the beaglebone with an optional solder-in microcontroller for creating the option of standalone control and can be intefaced with via i2c.

## Priorities
- Flexibility & performance are high priority
- Cost is lower priority but obviously lower cost is better

## Questions
- Should we seperate the power board from the signal board where sensors + beaglebone go on signal board and power board has its own micro to communicate via i2c to then manage all the relays and transistors? Develop signal board first, then power board.
- Should there be a power bank for easily routing 12VDC to the relays? E.g. something that is done similar to what is on [this](https://shop.controleverything.com/collections/light-dimmers/products/16-channel-12-bit-5-amp-high-current-n-channel-pwm-light-dimmer-for-iot) device

## Interoperability
- Let the same brain be used for the PFC2 / Fermentabot / Food Server

## Sensors
- Support for (used currently): 1-wire (1), i2c (5), serial (1), analog (1), and digital (1) sensors
     - What it is sensing, Part Name, Communication Protocol, Physical Connection
     - Temperature/Humidity, AM2315, I2C, Molex connector
     - CO2, MHZ16, UART, Molex connector push in wire
     - pH, Atlas pH sensor, I2C, soldered to the PCB (BNC for probe)
     - EC, Atlas EC sensor, I2C, soldered to the PCB (BNC for probe)
     - DO, Atlas DO sensor, I2C, soldered to the PCB (BNC for probe)
     - ORP, Atlas ORP sensor, I2C, soldered to the PCB (BNC for probe)
     - H20 Temp, DS18B20, 1-Wire, Molex connector
     - H20 Level, LLE102000, Digital, Molex connector
     - Light Intesity, TSL2561, I2C, soldered to PCB and Molex connector
     - Temperature/Humidity, Si7021, I2C, soldered to PCB and Molex connector [eagle files](https://www.adafruit.com/product/3251) (Rationale: community had concerns with AM2315 life expectancy)
     - O2, Grove O2, Analog, Molex connector
     - Also need to provide a 140khz signal to drive chiller. Previous solution was using [this](https://www.arduino.cc/en/Reference/Tone)
- Five extra ports for future sensors corresponding with logical pin selection on the Beagle Bone, and secondary microprocessor  


## Actuators
- Relays for AC or >5A DC. 10A relays likely sufficient. (10 Total)
     - What it is actuating, Voltage, Current, Physical Connection
     - Water Aerator Pump, 12VDC, 0.5A, Molex conn
     - Water Circulation Pump, 12VDC, 0.7A
     - H20 Pump (to refill the basin), 12VDC, 0.3A
     - C02 Solenoid, 12VDC, UKN, Molex conn
     - Humidifier, 5VDC, UKN, Molex conn
     - Air Heater Core 1, 12VDC, 12.5A, Molex conn  (Rationale: higher than 5A DC)
     - Air Heater Core 2, 12VDC, 12.5A, Molex conn
     - Chiller pump, 12VDC, UKN, Molex conn
     - Chiller fan, 12VDC, UKN, Molex conn
     - Air flush (x2 solenoids + x2 fans on common harness), 12VDC, Molex conn (x3 pos)
     - 3 Additional relays for future use
 -  Relay circuits will include the following:
     - Fuses in line with the main load
     - Catch Diode or TVS
     - Logical level control
     - Optoisolation    
- Transistors for <6A 12VDC at minimum (ideally support higher current and any device <40VDC) (11 total)
     - What it is actuating, Voltage, Current, Physical Connection
     - Red Grow Light, 12VDC, 6A, Molex conn
     - Blue Grow Light, 12VDC, 2.4A, Molex conn
     - White Grow Light, 12VDC, 2.2A, Molex conn
     - IR Grow Light, UKN, UKN, Molex conn
     - UV Grow Light, UKN, UKN, Molex conn
     - Nutrient A Pump, 12VDC, 0.3A, Molex conn (Control via FET b/c pumps likely be more accurate if running at a lower duty cycle)
     - Nurtient B Pump, 12VDC, 0.3A, Molex conn
     - pH Pump +, 12VDC, 0.3A, Molex conn
     - pH Pump -, 12VDC, 0.3A, Molex conn
     - Air Circulation Fan, 12VDC, 1.75A, Molex conn
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
- Would be nice-to-have option to connect [BBB touchscreen cape](https://www.sparkfun.com/products/12086)
