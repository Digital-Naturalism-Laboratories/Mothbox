import subprocess
import os
import time


script_path = r"C:\Users\andre\Documents\GitHub\Mothbox\AI\visualization_scripts\rembg_folder.py"  # Update this with your actual script path
input_paths = [
    r"F:\Panama\Hoya_408m_calmoBarbo_2025-01-26\2025-01-27\patches",
    r"F:\Panama\Hoya_310m_flatHapuku_2025-01-26\2025-01-27\patches",
    r"F:\Panama\Hoya_408m_calmoBarbo_2025-01-26\2025-01-27\patches",
    r"F:\Panama\Hoya_505m_prizeCrab_2025-01-26\2025-01-27\patches",
    r"F:\Panama\Hoya_606m_grisMejua_2025-01-26\2025-01-27\patches",
    r"F:\Panama\Hoya_714m_remoteAhulla_2025-01-26\2025-01-27\patches",
    r"F:\Panama\Hoya_812m_liftAlce_2025-01-26\2025-01-27\patches",
    r"F:\Panama\Hoya_916m_layerMomoto_2025-01-26\2025-01-27\patches",
    r"F:\Panama\Hoya_1004m_accionSauro_2025-01-26\2025-01-27\patches",
    r"F:\Panama\Hoya_1300m_alertTollo_2025-01-26\2025-01-27\patches",
    r"F:\Panama\Hoya_1110m_cuervoCinife_2025-01-26\2025-01-27\patches",
    r"F:\Panama\Hoya_1416m_fondoGorila_2025-01-27\2025-01-27\patches",
    r"F:\Panama\Hoya_1508m_waveUrta_2025-01-27\2025-01-27\patches",
    r"F:\Panama\Hoya_1534m_wingedHapuku_2025-01-27\2025-01-27\patches"
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
