import smbus2
import time

# --- Configuration ---
I2C_BUS = 1
PCA9555_ADDRESSES = [0x20, 0x21, 0x22]  # all 3 chips

# Register addresses
REG_INPUT_PORT_0  = 0x00
REG_INPUT_PORT_1  = 0x01
REG_CONFIG_PORT_0 = 0x06
REG_CONFIG_PORT_1 = 0x07

# Initialize I2C bus
bus = smbus2.SMBus(I2C_BUS)

# --- Descriptive names mapping ---
# Example: assign human-readable names to specific (address, pin)
DESCRIPTIVE_NAMES = {
    "Active":    (0x20, "P1_0"),
    "Debug":   (0x22, "P0_0"),
    "C1":     (0x22, "P0_6"), # Party Mode

    # Add as many as you want...
}

# --- Core Functions ---

def configure_all_pins_as_inputs(addr):
    """Configure all 16 pins of the PCA9555 at this address as inputs."""
    bus.write_byte_data(addr, REG_CONFIG_PORT_0, 0xFF)
    bus.write_byte_data(addr, REG_CONFIG_PORT_1, 0xFF)
    time.sleep(0.05)

def verify_configuration(addr):
    """Optional: Verify configuration is all inputs."""
    config0 = bus.read_byte_data(addr, REG_CONFIG_PORT_0)
    config1 = bus.read_byte_data(addr, REG_CONFIG_PORT_1)
    if config0 != 0xFF or config1 != 0xFF:
        print(f"⚠️ PCA9555 @ {hex(addr)} not fully configured as inputs!")

def read_input_states(addr):
    """Read both ports and return their bit states as integers (reversed logic)."""
    input0 = bus.read_byte_data(addr, REG_INPUT_PORT_0)
    input1 = bus.read_byte_data(addr, REG_INPUT_PORT_1)

    # Reverse logic: 1→0, 0→1
    input0 = (~input0) & 0xFF
    input1 = (~input1) & 0xFF

    return input0, input1

def read_all_switches():
    """
    Reads all PCA9555 chips once and returns organized dictionary like:
    {
      0x20: {'P0_0':0, 'P0_1':1, ..., 'P1_7':0},
      0x21: {...},
      0x22: {...}
    }
    """
    all_states = {}

    for addr in PCA9555_ADDRESSES:
        configure_all_pins_as_inputs(addr)
        verify_configuration(addr)

        port0, port1 = read_input_states(addr)

        bits = {}
        for i in range(8):
            bits[f"P0_{i}"] = (port0 >> i) & 1
        for i in range(8):
            bits[f"P1_{i}"] = (port1 >> i) & 1

        all_states[addr] = bits

    return all_states

# --- New Feature: lookup by descriptive name ---

def get_switch_state(name):
    """
    Returns the current state (0 or 1) of a switch by its descriptive name.
    Example: get_switch_state("Mode Button")
    """
    if name not in DESCRIPTIVE_NAMES:
        raise ValueError(f"Unknown switch name: '{name}'")

    addr, pin_name = DESCRIPTIVE_NAMES[name]
    port0, port1 = read_input_states(addr)

    if pin_name.startswith("P0_"):
        bit = int(pin_name.split("_")[1])
        value = (port0 >> bit) & 1
    elif pin_name.startswith("P1_"):
        bit = int(pin_name.split("_")[1])
        value = (port1 >> bit) & 1
    else:
        raise ValueError(f"Invalid pin name format: '{pin_name}'")

    return value

# --- Main Program ---

def main():
    all_switch_states = read_all_switches()

    print("\n--- Switch States ---")
    for addr, pins in all_switch_states.items():
        print(f"PCA9555 @ {hex(addr)}:")
        for name, state in pins.items():
            print(f"  {name}: {state}")
        print("-" * 30)

    # Example usage of descriptive lookup:
    print("\n--- Descriptive Name Lookups ---")
    for desc_name in DESCRIPTIVE_NAMES:
        value = get_switch_state(desc_name)
        print(f"{desc_name}: {value}")

if __name__ == "__main__":
    main()
