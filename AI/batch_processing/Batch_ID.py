import subprocess
import os
import time
#from bioclip import  Rank

script_path = r"c:/Users/andre/Documents/GitHub/Mothbox/AI/Mothbot/Mothbot_ID.py"  # Update this with your actual script path

#you can insert a list of deployments, the ID script will automatically find the date folders!
input_paths = [
      r"G:\Shared drives\Mothbox Management\Testing\ExampleDataset\Indonesia_Les_BeachPalm_grupoKite_2025-06-23\2025-06-22",
    r"G:\Shared drives\Mothbox Management\Testing\ExampleDataset\Indonesia_Les_BeachPalm_grupoKite_2025-06-23\2025-06-23",
    r"G:\Shared drives\Mothbox Management\Testing\ExampleDataset\Indonesia_Les_BeachPalm_grupoKite_2025-06-23\2025-06-24",
    r"G:\Shared drives\Mothbox Management\Testing\ExampleDataset\Les_BeachPalm_hopeCobo_2025-06-20\2025-06-20",
    r"G:\Shared drives\Mothbox Management\Testing\ExampleDataset\Les_BeachPalm_hopeCobo_2025-06-20\2025-06-21",


]


SPECIES_LIST = r"C:\Users\andre\Documents\GitHub\Mothbox\AI\SpeciesList_CountryIndonesia_TaxaInsecta.csv"  # downloaded from GBIF for example just insects in panama: https://www.gbif.org/occurrence/taxonomy?country=PA&taxon_key=212

""" KINGDOM = 0
    PHYLUM = 1
    CLASS = 2
    ORDER = 3
    FAMILY = 4
    GENUS = 5
    SPECIES = 6"""

TAXONOMIC_RANK_FILTER = 3

ID_HUMANDETECTIONS = True
ID_BOTDETECTIONS = True
# you can See if a json file has an existing ID by looking at "description": "ID_BioCLIP"
OVERWRITE_EXISTING_IDs = True 

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

print("starting batch processing of IDs")

start_time_overall = time.time()
#print(TAXONOMIC_RANK_FILTER)
for input_path in input_paths:
    print("starting to process: "+input_path)
    subprocess.run([
        "python", script_path,
        "--input_path", input_path,
        "--taxa_csv", SPECIES_LIST,
        "--rank", str(TAXONOMIC_RANK_FILTER)
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
