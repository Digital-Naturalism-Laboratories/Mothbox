import subprocess
import os
import time
#from bioclip import  Rank

script_path = r"c:/Users/andre/Documents/GitHub/Mothbox/AI/Mothbot/Mothbot_InsertMetadata.py"  # Update this with your actual script path

#you can insert a list of deployments, the ID script will automatically find the date folders!
input_paths = [
    r"g:\Shared drives\Mothbox Management\Testing\ExampleDataset\Les_BeachPalm_hopeCobo_2025-06-20",
    r"g:\Shared drives\Mothbox Management\Testing\ExampleDataset\AzueroSuperD_OriaNursery_Nursery_dobleParina_2025-02-05",
    r"g:\Shared drives\Mothbox Management\Testing\ExampleDataset\AzueroSuperD_OriaNursery_Nursery_prizecrab_2025-02-05",
    r"g:\Shared drives\Mothbox Management\Testing\ExampleDataset\AzueroSuperD_OriaNursery_Nursery_wingedHapuku_2025-02-05",
    r"g:\Shared drives\Mothbox Management\Testing\ExampleDataset\Indonesia_Les_BeachPalm_grupoKite_2025-06-23",
    r"g:\Shared drives\Mothbox Management\Testing\ExampleDataset\Indonesia_Les_WilanTopTree_HopeCobo_2025-06-25",
]



METADATA_PATH = r'..\Mothbox_Main_Metadata_Field_Sheet_Example - Form responses 1.csv'


ID_HUMANDETECTIONS = True
ID_BOTDETECTIONS = True

i=0


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

total_paths=len(input_paths)
print("starting batch processing of IDs from this many inputs: "+str(total_paths))

start_time_overall = time.time()
for input_path in input_paths:
    print("starting to process: "+input_path)
    subprocess.run([
        "python", script_path,
        "--input_path", input_path,
        "--metadata", METADATA_PATH,
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
