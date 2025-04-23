# mothbox_front

Design a mainboard for the MothBox

# TODO
Todo list mostly built off the [list of upcoming features for the Mothbox](https://digital-naturalism-laboratories.github.io/Mothbox/docs/about/upcoming/).

## Circuit Designs

### Photo LEDs (Point person Moritz)
These are the white, distributed LEDs that evenly light up the target area for even photography.

- place 12V UV-light / visible light attractor LED boards
- design white light <--> PI interface
- design led drivers: single constant current driver for UV and Flashlight, Relays to switch between both options, part: LDH-25-350
- place white LEDs and drivers

### Attractor LEDs (Point person Moritz)
- Design circuitry to toggle high power output to the attractor LED ports

### Power Regulation
Ideally this PCB should be able to accept a range of power. A [common power regulator that costs around $15](https://www.amazon.com/dp/B0B6VK8BPN?ref=ppx_yo2ov_dt_b_fed_asin_title&th=1) takes *9-36v* and regulates this to an even 12V at 5amps. It would be nice if we could build this into the board, though it could optionally be purchased as is and the board just made to use 12V.

- Design regulator circuit
- design connector (ideally standard barrel jack connector, or pair of + and - plugs)

### Power Management
- Integrated power monitoring (e.g. integrate something like the Adafruit 4226 INA260)
- Display Charge State

### Physical Programming Interface
The scientists often have a hard time programming features of the Mothbox. If possible, as many of these variables a user needs to set should be available as some kind of physical switch or toggle. 

![d25e1bb2-e423-492f-94e9-bb884e0817fa](https://github.com/user-attachments/assets/e90bf354-2e8e-4ae5-8092-2fc40de9ab7f)

Ideally these switches should be "soft switches" that just change a state on a pin the Pi can read and the internal software can perform the necessary functions. There are likely too many variables to route each pin to a different GPIO pin on the Pi, so a multiplexer is likely warranted to combine these inputs into just a couple GPIO pins for the Pi to read.

- Multiplexer to route the pin states
- Programming Pins
    - Mothbox Schedule
        - Days of week to run
        - Hours to start
        - Duration for each capture sequence (optional)
    - Mothbox State
        - Toggle Armed/ Disarmed
    - Attractor LED TYPE
        - Switch between UV, Visible, or Both
        - Possibly more granular (UV, Blue, Green, White)
    - Attractor LED Power Usage
        - Max Power
        - Medium Power
        - Minimum Power
    - External vs Internal Attractor
        - Toggle between using the internal attractor lights, External port, or both!



### Status indication and feedback
Some sort of low energy method to display this array of possible states, so that in the field one does not have to VNC into the device to know what it is up to. This could be a simple RGB led with color codes that blinks maybe once every couple seconds or something.
- Armed/Disarmed state
- “Is scheduled to run today/within the next 2 hours” indicator
- Copying files
- taking photos
- idle
- sleep / dormant
- error

### Bonus Features
#### GPS
GPS is great primarily because it can give us automatic time syncronization!
Secondarily it is great because it can give us location (but we generally mark GPS and the mothboxes don't move much)
- place GPS antenna / GPS board (mounting holes)
- Or, one could just [buy a GPS hat](https://www.adafruit.com/product/2324)

#### Power Microcontroller
- Integrate low power microcontroller that can fully shut off and wake up the Pi

## Physical Designs and Connections
- place connectors for attractor LED boards
- Place connectors for camera
- Place connectors for 1/4 in bolts that hold the PCB in place in the box (partially done with Andy's latest DXF)

# DONE
- decide on preferred power bank: PB120B1, https://talentcell.com/lithium-ion-battery/24v/pb240b2.html
    - 12V output: 9V-12.6V / 6 A max (direct connection to batteries)
    - 5V, 2.4A

- location and fixation of the power bank

# Order
- Arducam 64 MP
- RPi 5
- Talent Cell battery PB120B1


# Already ordered
- PLANO box

# Wishlist of functionality








