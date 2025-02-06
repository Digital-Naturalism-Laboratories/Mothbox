import subprocess
import os
import time


script_path = r"C:\Users\andre\Documents\GitHub\Mothbox\AI\visualization_scripts\rembg_folder.py"  # Update this with your actual script path
input_paths = [
    r"F:\Panama\Hoya_163m_unrulyArao_2025-01-26\2025-01-27\patches",
    r"F:\Panama\Hoya_168m_doubleParina_2025-01-26\2025-01-27\patches",
    r"F:\Panama\Hoya_277m_adeptTurca_2025-01-26\2025-01-27\patches",
 

]


def time_it(func):
    """A decorator to time the execution of a function.

    Args:
        func: The function to be timed.

    Returns:
        A wrapper function that executes the given function and prints the execution time.
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()  # Record the start time
        result = func(*args, **kwargs) # Execute the function
        end_time = time.time()  # Record the end time
        execution_time = end_time - start_time # Calculate the elapsed time
        print(f"Function '{func.__name__}' took {execution_time:.4f} seconds to execute.")
        return result # Return the original function's result

    return wrapper



start_time_overall = time.time()
i=0
for input_path in input_paths:
    print("starting to process: "+input_path)
    subprocess.run([
        "python", script_path,
        "--input_path", input_path,
    ], check=True)

    i=i+1
    print("processed "+str(i)+" folders.")
    print("just finished processing "+input_path)

end_time_overall = time.time()
total_execution_time = end_time_overall - start_time_overall

hours = int(total_execution_time // 3600)
minutes = int((total_execution_time % 3600) // 60)
seconds = total_execution_time % 60

print(f"Overall script execution took {hours:02d}:{minutes:02d}:{seconds:.4f} (HH:MM:SS.SSSS)")
