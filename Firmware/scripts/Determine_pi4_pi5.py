import sys

# Define functions for each Raspberry Pi model
def raspberry_pi_4():
  print("Hello from Raspberry Pi 4!")
  # Add functionalities specific to Pi 4 here

def raspberry_pi_5():
  print("Hello from Raspberry Pi 5!")
  # Add functionalities specific to Pi 5 here

# Check Raspberry Pi model using CPU info
cpuinfo = open("/proc/cpuinfo", "r")
model = None  # Initialize model variable outside the loop
for line in cpuinfo:
  print(line)

  if line.startswith("Model"):
    model = line.split(":")[1].strip()
    break
cpuinfo.close()

# Execute function based on model
print(model)
if model:  # Check if model was found
  if "Pi 4" in model:  # Model identifier for Raspberry Pi 4
    raspberry_pi_4()
  elif "Pi 5" in model:  # Model identifier for Raspberry Pi 5
    raspberry_pi_5()
  else:
    print("Unknown Raspberry Pi model detected.")
else:
  print("Error: Could not read Raspberry Pi model information.")

