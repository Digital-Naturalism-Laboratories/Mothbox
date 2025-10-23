import smbus2
import time

# I2C setup
I2C_BUS = 1
PCA9555_ADDR = 0x20  #  base address

# Register addresses
REG_INPUT_PORT_0  = 0x00
REG_INPUT_PORT_1  = 0x01
REG_CONFIG_PORT_0 = 0x06
REG_CONFIG_PORT_1 = 0x07

# Initialize I2C bus
bus = smbus2.SMBus(I2C_BUS)

def configure_all_pins_as_inputs(add_Offset):
    """
    Set all 16 pins as inputs. PCA9535 has no internal pull-ups,
    so external pull-up resistors must be used in hardware.
    """
    bus.write_byte_data(PCA9555_ADDR + add_Offset, REG_CONFIG_PORT_0, 0xFF)
    bus.write_byte_data(PCA9555_ADDR + add_Offset, REG_CONFIG_PORT_1, 0xFF)
    time.sleep(0.1)

def verify_configuration(add_Offset):
    config0 = bus.read_byte_data(PCA9555_ADDR + add_Offset, REG_CONFIG_PORT_0)
    config1 = bus.read_byte_data(PCA9555_ADDR + add_Offset, REG_CONFIG_PORT_1)
    print(f" Config Port 0: {format(config0, '08b')} (1 = input)")
    print(f" Config Port 1: {format(config1, '08b')} (1 = input)")

    if config0 != 0xFF or config1 != 0xFF:
        print(" Not all pins set as inputs!")

def read_input_states(add_Offset):
    input0 = bus.read_byte_data(PCA9555_ADDR + add_Offset, REG_INPUT_PORT_0)
    input1 = bus.read_byte_data(PCA9555_ADDR + add_Offset, REG_INPUT_PORT_1)
    
    return format(input0, '08b'), format(input1, '08b')

def main():
    for PCA9555 in range(3):
       print(f"Configuring PCA9555 #: {PCA9555} pins as inputs...")
       configure_all_pins_as_inputs(PCA9555)
       verify_configuration(PCA9555)
       print()

    print("\n Monitoring switch states. Press Ctrl+C to stop.")

    try:
        while True:
            
          for PCA9555 in range(3):
            port0, port1 = read_input_states(PCA9555)
            print(f"PCA9555 #: {PCA9555} Port 0: (P0_7 to P0_0): {port0}  -  Port 1: (P1_7 to P1_0): {port1}")
            print("-" * 40)
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\n? Exiting.")

if __name__ == "__main__":
    main()
