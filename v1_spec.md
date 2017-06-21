# Brain Box V1.0 Spec
This will be a custom PCB based off the beaglebone with an optional solder-in microcontroller for creating the option of standalone control and can be intefaced with via i2c.
We still need to think through the mechanical design for preventing fowling of components / water damage / etc.

## Priorities
- Flexibility & performance are high priority
- Cost is lower priority but obviously lower cost is better

## Interoperability
- Let the same brain be used for the PFC2 / Fermentabot / Food Server

## Sensors
- Support for 1-wire, i2c, serial, analog, and digital sensors
- Extra ports for future sensors

## Actuators
- Relays for AC or >5A DC. 10A relays likely sufficient
- Transistors for <5A 12VDC at minimum (ideally support higher current and any device <40VDC)
- Quantity is TBD but more is generally better that can fit within a reasonable footprint (maybe spec dimension by what could easily swap out into the PFCV2 space but not a hard constraint)

## Power Sensing
- Reporting on all power usage would be great to start optimizing recipes for energy but not requirement for v1

## Other
- Lots of LEDS for status
- Probe points for easy debugging
