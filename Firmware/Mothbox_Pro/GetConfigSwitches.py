import smbus2
import time
import subprocess

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
    "U1":     (0x22, "P0_7"), # Switch Setting Mode
    
    "h1":     (0x21, "P0_7"), # 
    "h2":     (0x21, "P0_6"), # 
    "h3":     (0x21, "P0_5"), # 
    "h4":     (0x21, "P0_4"), # 
    "h5":     (0x21, "P0_3"), # 
    "h6":     (0x21, "P0_2"), # 
    "h7":     (0x21, "P0_1"), # 
    "h8":     (0x21, "P0_0"), # 
    
    "h9":     (0x21, "P1_7"), # 
    "h10":     (0x21, "P1_6"), # 
    "h11":     (0x21, "P1_5"), # 
    "h12":     (0x21, "P1_4"), # 
    "h13":     (0x21, "P1_3"), # 
    "h14":     (0x21, "P1_0"), # 
    "h15":     (0x21, "P1_1"), # 
    "h16":     (0x21, "P1_2"), # 

    "h17":     (0x20, "P0_6"), # 
    "h18":     (0x20, "P0_5"), # 
    "h19":     (0x20, "P0_4"), # 
    "h20":     (0x20, "P0_3"), # 
    "h21":     (0x20, "P0_2"), # 
    "h22":     (0x20, "P0_1"), # 
    "h23":     (0x20, "P0_0"), # 
    "h00":     (0x20, "P0_7"), # 

    "d0":     (0x20, "P1_7"), # su
    "d1":     (0x20, "P1_6"), # mo
    "d2":     (0x20, "P1_5"), # tu
    "d3":     (0x20, "P1_4"), # we
    "d4":     (0x20, "P1_3"), # th
    "d5":     (0x20, "P1_2"), # fr
    "d6":     (0x20, "P1_1"), # sa


    "A1":     (0x20, "P0_5"), # A1
    "A2":     (0x20, "P0_4"), # A2
    "A3":     (0x20, "P0_3"), # A3
    "EXT":     (0x20, "P0_2"), # EXT
    "HI":     (0x20, "P0_1"), # HI



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

def set_SwitchesinControls(filepath, switch, state):
    with open(filepath, "r") as file:
        lines = file.readlines()

    with open(filepath, "w") as file:
        for line in lines:
            #print(line)
            if line.startswith(switch+"="):
                file.write(switch+"=" + str(state) + "\n")  
                #print("set next switch "+switch +" state in controls " + str(state))
            else:
                file.write(line)  # Keep other lines unchanged


def run_script(script_path, show_output=True):
    """
    Run a Python script and optionally display its output.
    """
    try:
        result = subprocess.run(
            ["python3", script_path],
            capture_output=True,
            text=True,
            check=True
        )
        if show_output:
            output = result.stdout.strip()
            if output:
                print(output)
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_path}: {e.stderr.strip() if e.stderr else 'Unknown error'}")



# --- Main Program ---

def main():
    run_script("/home/pi/Desktop/Mothbox/scripts/3v3SensorsOn.py", show_output=False)
    time.sleep(.1)
    all_switch_states = read_all_switches()
    '''
    print("\n--- Switch States ---")
    for addr, pins in all_switch_states.items():
        print(f"PCA9555 @ {hex(addr)}:")
        for name, state in pins.items():
            print(f"  {name}: {state}")
        print("-" * 30)
    '''
    # Example usage of descriptive lookup:
    print("\n--- Config Switch - Descriptive Name Lookups ---")
    for desc_name in DESCRIPTIVE_NAMES:
        value = get_switch_state(desc_name)
        #print(f"{desc_name}: {value}")
        set_SwitchesinControls("/boot/firmware/mothbox_custom/system/controls.txt",desc_name,value)
    time.sleep(.1)            
    run_script("/home/pi/Desktop/Mothbox/scripts/3v3SensorsOff.py", show_output=False)

if __name__ == "__main__":
    main()
