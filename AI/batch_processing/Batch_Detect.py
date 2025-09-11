import subprocess
import os
import time


script_path = r"c:/Users/andre/Documents/GitHub/Mothbox/AI/Mothbot/Mothbot_Detect.py"  # Update this with your actual script path
nightly_deployment_input_paths = [
    r"g:\Shared drives\Mothbox Management\Testing\ExampleDataset\Les_BeachPalm_hopeCobo_2025-06-20",
    r"g:\Shared drives\Mothbox Management\Testing\ExampleDataset\AzueroSuperD_OriaNursery_Nursery_dobleParina_2025-02-05",
    r"g:\Shared drives\Mothbox Management\Testing\ExampleDataset\AzueroSuperD_OriaNursery_Nursery_prizecrab_2025-02-05",
    r"g:\Shared drives\Mothbox Management\Testing\ExampleDataset\AzueroSuperD_OriaNursery_Nursery_wingedHapuku_2025-02-05",
    r"g:\Shared drives\Mothbox Management\Testing\ExampleDataset\Indonesia_Les_BeachPalm_grupoKite_2025-06-23",
    r"g:\Shared drives\Mothbox Management\Testing\ExampleDataset\Indonesia_Les_WilanTopTree_HopeCobo_2025-06-25",
]

YOLO_MODEL=r"../trained_models/yolo11m_4500_imgsz1600_b1_2024-01-18/weights/yolo11m_4500_imgsz1600_b1_2024-01-18.pt"
IMGSZ=1600# Should be same imgsz as used in training for best results!

GEN_BOT_DET_EVENIF_HUMAN_EXISTS=True #if we encounter a human detection, but still want a parallel bot detection, make this true
OVERWRITE_PREV_BOT_DETECTIONS=False #if true, if there are previous machine detections, it will overwrite those machine detections with our current ones. This script should NEVER overwrite a human detection

#You should always leave Gen_Thumbnails as true. It will intelligently detect if a thumbnail exists and skip it if need be.
GEN_THUMBNAILS=True



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



start_time_overall = time.time()

for input_path in nightly_deployment_input_paths:
    print("starting to process: "+input_path)
    subprocess.run([
        "python", script_path,
        "--input_path", input_path,
        "--yolo_model", YOLO_MODEL,
        "--imgsz", str(IMGSZ)
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
