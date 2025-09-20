import subprocess
import os

def get_cpu_temp():
  """
  Executes the command `vcgencmd measure_temp && cat /sys/class/thermal/thermal_zone0/temp`
  and prints the results.
  """

  try:
    # Execute the command
    #vcgencmd can fail sometimes so just that one. Returns a string that is like 74900 which means 74.9 degrees celcius
    result = subprocess.run(['cat', '/sys/class/thermal/thermal_zone0/temp'],
                           capture_output=True, text=True, check=True)

    # Print the output
    print(result.stdout)

  except subprocess.CalledProcessError as e:
    print(f"Error executing command: {e}")
    print(f"Error output: {e.stderr}")

  except Exception as e:
    print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
  get_cpu_temp()
