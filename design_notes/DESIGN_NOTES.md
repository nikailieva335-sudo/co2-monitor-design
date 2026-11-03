## Design Notes and Criteria for Wearable Development

### The Heater Implementation
#### Materials:
1. MT3608 Booster (w/ Potentiometer)
2. NPN Transisotr 2N4401
3. FIT0845 Heater Module (5W, 5V 100C)
4. NTC Thermistor 10kOhm (103FL 2441) + 4.7kOhm Resistor

Firstly, the heater module needs to be tested on a breadboard.

#### Hardware Design
To protect the nRF development kit, power supply to the heater will be supplied through an external battery instead of the controller.

The heater switching will use an NPN MOSFET controlled by GPIO

A 10kOhm NTC thermistor with a 4.7kOhm voltage divider will be used to sense temperature.

#### Control and Safety

Target heater surface temperature: 40-45C
Use PWM to regulate heater power
Measure temperature continuously wth the thermistor. The SCD41 does have a temperature sensor built in but the sensing time is too slow to recognize dangeous temperatures in a sensible manner.

Firmware should be configured to have a safety temperature limit that forces the heater to switch OFF if:

- Temperature exceeds the safety limit
- Thermistor is disconnected or short circuited
- Thermistor values are invalid
- Readings stop updating
- Temperature changes in unexpected manner

