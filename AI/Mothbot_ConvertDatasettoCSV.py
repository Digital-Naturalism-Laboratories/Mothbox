#!/usr/bin/env python3

import json
import os
import datetime
import csv
import re
from datetime import datetime, timedelta
#from unidecode import unidecode
#from pygbif import species
import unicodedata
import pandas as pd

INPUT_PATH = r'/Volumes/Mothbox C/Deployments/Indonesia/Indonesia_Les_WilanFirstHilltree_cuervoCinife_2025-06-25/2025-06-25/BriID'
UTC_OFFSET=8 #indonesiaD
# Specify the path to your taxonomy CSV file
TAXA_LIST_PATH = r"SpeciesList_CountryIndonesia_TaxaInsecta.csv"
TAXA = ['kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species']

def OLDcreate_occurrence_id(filename, latitude, longitude):
    # Step 1: Process filename
    # Remove spaces, convert to lowercase, replace irregular characters, convert "_" to "-"
    filename = unidecode(filename).lower().strip()
    
    # Remove .jpg extension and extract relevant part of the filename
    filename = filename.replace(".jpg", "")
    
    # Extract part before the 9th underscore
    parts = filename.split('_')
    if len(parts) >= 9:
        filename_part = '_'.join(parts[:8])
    else:
        filename_part = '_'.join(parts)
    filename_part = filename_part.replace("_", "-")
    
    # Step 2: Extract the number right before .jpg
    final_number = parts[-1] if parts[-1].isdigit() else "0"
    
    # Step 3: Process latitude
    # Remove non-digit characters (like "." and "-"), then take the first 5 characters
    cleaned_lat = re.sub(r'[^0-9]', '', latitude)  # Remove ".", "-"
    lat = cleaned_lat[:5]  # Take only the first 5 digits
    
    # Step 4: Process longitude
    # Remove non-digit characters (like "." and "-"), then take the first 5 characters
    cleaned_lon = re.sub(r'[^0-9]', '', longitude)  # Remove ".", "-"
    lon = cleaned_lon[:5]  # Take only the first 5 digits
    
    # Step 5: Combine into occurrenceID
    occurrence_id = f"{filename_part}-{lat}-{lon}-{final_number}"
    
    return occurrence_id

def adjust_timestamp_with_utc_offset(date_str, time_str, utc_offset):
    # Step 1: Parse the date and timestamp
    original_datetime = datetime.strptime(f"{date_str} {time_str}", "%Y_%m_%d %H_%M_%S")
    
    # Step 2: Apply the UTC offset (assuming utc_offset is in hours, e.g., +2, -5)
    adjusted_datetime = original_datetime + timedelta(hours=utc_offset)
    
    # Step 3: Format the adjusted datetime back into strings
    adjusted_date = adjusted_datetime.strftime("%Y_%m_%d")
    adjusted_time = adjusted_datetime.strftime("%H_%M_%S")
    
    return adjusted_date, adjusted_time

def format_datetime_with_utc_offset(date_str, time_str, utc_offset):
    # Step 1: Parse the adjusted date and time
    original_datetime = datetime.strptime(f"{date_str} {time_str}", "%Y_%m_%d %H_%M_%S")
    
    # Step 2: Apply the UTC offset to set to UTC time (assuming utc_offset is in hours)
    adjusted_datetime = original_datetime - timedelta(hours=utc_offset)
    
    # Step 3: Determine the sign and format the UTC offset
    offset_sign = "+" if utc_offset >= 0 else "-"
    abs_offset = abs(utc_offset)
    offset_hours = int(abs_offset)
    offset_minutes = int((abs_offset - offset_hours) * 60)
    formatted_offset = f"{offset_sign}{offset_hours:02d}{offset_minutes:02d}"
    
    # Step 4: Format the final datetime string in the desired format
    formatted_datetime = adjusted_datetime.strftime("%Y-%m-%dT%H:%M:%S")
    final_output = f"{formatted_datetime}{formatted_offset}"
    
    return final_output



def get_deepest_classification(kingdom="", phylum="",class_="", order="", family="", genus="",species=""):
    
    for rank in reversed(TAXA):
        # Handle the special case where 'class' is stored as 'class_'
        var_name = rank if rank != "class" else "class_"
        value = locals().get(var_name, "")
        if value:
            return rank, value
    return None, None


# Function to search GBIF for taxonomic details
#This works great but can be VERY slow
def get_gbif_info_online(rank, name):
    try:
        # Search GBIF by name
        search_results = species.name_lookup(q=name, rank=rank, limit=1)
        if search_results['results']:
            result = search_results['results'][0]
            taxon_id = result.get('key', None)
            scientific_name = result.get('scientificName', None)
            common_name = result.get('vernacularName', None)
            
            # Normalize names to ASCII to remove any special characters
            if scientific_name:
                scientific_name = unicodedata.normalize('NFKD', scientific_name).encode('ascii', 'ignore').decode('utf-8')
            if common_name:
                common_name = unicodedata.normalize('NFKD', common_name).encode('ascii', 'ignore').decode('utf-8')
            
            return taxon_id, scientific_name, common_name
        else:
            print(f"No GBIF results found for {rank}: {name}")
            return None, None, None
    except Exception as e:
        print(f"Error fetching GBIF data: {e}")
        return None, None, None

# Function to load the taxa lookup CSV into a pandas DataFrame
def load_taxa_lookup(taxa_list_path):
    # Load the CSV into a pandas DataFrame
    taxa_lookup_df = pd.read_csv(taxa_list_path, sep='\t')
    return taxa_lookup_df

# Function to find the deepest taxon information based on the deepest rank and value
def find_deepest_taxon_info(taxa_list, taxa_values, taxa_lookup):
    # Step 1: Determine the deepest rank and its corresponding value
    deepest_rank = None
    deepest_value = None

    # Find the deepest rank with a non-empty value
    for rank, value in zip(taxa_list, taxa_values):
        if value != "" and value is not None:
            deepest_rank = rank
            deepest_value = value

    # Check if we found a deepest rank and value
    if deepest_rank and deepest_value:
        #print(f"Deepest Rank: {deepest_rank}, Deepest Value: {deepest_value}")

        # Step 2: Filter rows in taxa_lookup where 'taxonRank' matches the deepest rank (case insensitive)
        filtered_rows = taxa_lookup[taxa_lookup['taxonRank'].str.lower() == deepest_rank.lower()]
        
        # Step 3: Find the row where the 'deepest_value' matches (case insensitive)
        matched_row = filtered_rows[filtered_rows[deepest_rank].str.lower() == deepest_value.lower()]

        # Step 4: If a match is found, return taxonKey and scientificName
        if not matched_row.empty:
            taxon_id = matched_row['taxonKey'].values[0]
            scientific_name = matched_row['scientificName'].values[0]
            return taxon_id, scientific_name
        else:
            print("No match found for the given deepest rank and value.")
            return None, None
    else:
        print(str(taxa_values)+"No valid deepest rank and value found. Probably ID'ed as an Error category, don't worry")
        return None, None
def create_uniquedatasetID(deployment_name, oid_dict):
  """
  Creates a deployment name by concatenating the given deployment_name 
  with the 'oid' value extracted from the provided dictionary.

  Args:
    deployment_name: The base name for the deployment.
    oid_dict: A dictionary containing the 'oid' key.

  Returns:
    The concatenated deployment name.
  """
  try:
    oid = oid_dict['$oid']
    return f"{deployment_name}_oid_{oid}"
  except KeyError:
    return f"{deployment_name}"  # Return original name if 'oid' key is missing
 
def json_to_csv(input_path, utc_offset,taxa_list_path):

    #preload this stuff for faster lookup
    taxa_lookup = load_taxa_lookup(taxa_list_path)

    # Get the last folder name from the input path
    folder_name = os.path.basename(input_path)
    
    # Get the parent folder name
    parent_folder = os.path.basename(os.path.dirname(input_path))

    # Get the current date in YYYY-MM-DD format
    current_date = datetime.today().strftime('%Y-%m-%d')

    # Create the output CSV file name
    output_file = f"{parent_folder}_{folder_name}_exportdate_{current_date}.csv"

    # Append "samples.json" to the input path to get the correct file path
    json_file_path = os.path.join(input_path, "samples.json")

    try:
        with open(json_file_path, "r") as f:
            data = json.load(f)
        print("Found fiftyone dataset's json path")
    except FileNotFoundError:
        print("Could not find fiftyone dataset's json path, maybe try a different folder?")
        return

    with open(input_path+"/"+output_file, "w", newline="") as csvfile:
        fieldnames = ["basisOfRecord","datasetID","parentEventID","eventID","occurrenceID","verbatimEventDate","eventDate","eventTime","UTCOFFSET","detectionBy","detection_confidence","identifiedBy","ID_confidence","kingdom","phylum","class","order","family","genus","species","taxonID","commonName","scientificName","filepath", "mothbox","software","sheet","country", "area", "point","latitude","longitude","ground_height","deployment_name","deployment_date","collect_date", "data_storage_location","crew", "notes", "schedule","habitat", "image_id", "label", "bbox", "segmentation", "attractor", "attractor_location"]  # Adjust fieldnames as needed
        csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        csv_writer.writeheader()

        for sample in data["samples"]:

            #tags are the only thing directly editable in 51
            detectionBy=""
            identified_by=""

            kingdom=""
            phylum=""
            tclass=""
            order=""
            family=""
            genus=""
            species=""
            commonName=""
            scientificName=""
            taxon_id=""
            ground_height=""
            attractor=""
            attractor_location=""



            # Regular expression pattern to extract date and timestamp
            pattern = r"_(\d{4}_\d{2}_\d{2})__(\d{2}_\d{2}_\d{2})"

            # Search for the pattern in the file path
            match = re.search(pattern, sample["filepath"])

            if match:
                date = match.group(1)
                timestamp = match.group(2)
                #print(f"Date: {date}")
                #print(f"Timestamp: {timestamp}")
            else:
                print("No date and timestamp found in the file path.")

            # Adjust date and timestamp based on the UTC offset
            #UTC_date, UTC_time = adjust_timestamp_with_utc_offset(date, timestamp, utc_offset)
            formattedUTC_dateTime = format_datetime_with_utc_offset(date, timestamp, utc_offset)

            for tag in sample["tags"]:
                # Check for prefixes
                if tag.startswith("KINGDOM"):
                    kingdom = tag[len("KINGDOM"):].strip('_')
                elif tag.startswith("PHYLUM"):
                    phylum = tag[len("PHYLUM"):].strip('_')
                elif tag.startswith("CLASS"):
                    tclass = tag[len("CLASS"):].strip('_')
                elif tag.startswith("ORDER"):
                    order = tag[len("ORDER"):].strip('_')
                elif tag.startswith("FAMILY"):
                    family = tag[len("FAMILY"):].strip('_')
                elif tag.startswith("GENUS"):
                    genus = tag[len("GENUS"):].strip('_')
                elif tag.startswith("SPECIES"):
                    species = tag[len("SPECIES"):].strip('_')
                elif tag.startswith("commonName"):
                    common_name = tag[len("commonName"):].strip('_')
                elif tag.startswith("scientificName"):
                    scientificName = tag[len("scientificName"):].strip('_')
                elif tag.startswith("IDby"):
                    identified_by = tag[len("IDby"):].strip('_')
                elif tag.startswith("ERROR"):
                    commonName="ERROR"


            if tag.startswith("taxonID"):
                taxon_id = tag[len("taxonID"):].strip('_')
            elif tag.startswith("phylum"):
                phylum = tag[len("phylum"):].strip('_')
             #fieldnames = ["basisOfRecord","datasetID","parentEventID","eventID","occurrenceID","verbatimEventDate","eventDate","eventTime","identifiedBy","taxonID","kingdom","phylum","class","order","family","genus","species","commonName","scientificName","filepath", "mothbox","software","sheet","country", "area", "point","latitude","longitude","height","deployment_name","deployment_date","sample_time","collect_date", "data_storage_location","crew", "notes", "schedule","habitat", "image_id", "label", "bbox", "segmentation"]  # Adjust fieldnames as needed
            #print("sample")


            #deepest_rank, deepest_value = get_deepest_classification(kingdom, phylum,tclass, order, family, genus,species)

            # Find the deepest available rank and its taxonomic details
            taxa_values = [kingdom, phylum, tclass, order, family, genus, species]
            taxon_id, scientificName= find_deepest_taxon_info(TAXA, taxa_values, taxa_lookup)

            uniquedatasetID=create_uniquedatasetID(sample["deployment_name"],sample["_dataset_id"])

            row = {
                "filepath":sample["filepath"],
                
                "basisOfRecord": "MachineObservation",
                "datasetID":uniquedatasetID,
                "parentEventID":sample["deployment_name"],
                "eventID":os.path.basename(sample['filepath_fullimage']),
                "occurrenceID":os.path.basename(sample["filepath"]),
                "verbatimEventDate":date+"__"+timestamp,
                "eventDate":formattedUTC_dateTime,
                "eventTime":formattedUTC_dateTime.split("T")[1],
                "UTCOFFSET":utc_offset,
                "mothbox":sample["mothbox"],
                "software":sample["software"],
                "sheet":sample["sheet"],
                "country":sample["country"],
                "area":sample["area"], 
                "point":sample["punto"],
                "latitude":sample["latitude"],
                "longitude":sample["longitude"],
                "ground_height":sample["ground_height"],
                "attractor":sample["attractor"],
                "attractor_location":sample["attractor_location"],

                "deployment_name":sample["deployment_name"],
                "deployment_date":sample["deployment_date"],
                #"sample_time":formattedUTC_dateTime,
                "collect_date":sample["collect_date"], 
                "data_storage_location":sample["data_storage_location"],
                "crew":sample["crew"], 
                "notes": "", #sample["notes"], #Disabled for now, hubert doesn't want notes for each critter sighting
                "schedule":sample["program"],
                "habitat":sample["habitat"], 

                #detection specific
                "detectionBy": sample["detection_By"],

                "identifiedBy":identified_by,

                "ID_confidence": sample["confidence"],

                "kingdom":kingdom,
                "phylum":phylum,
                "class":tclass,
                "order":order,
                "family":family,
                "genus":genus,
                "species":species,
                "commonName":commonName,
                "scientificName":scientificName,
                "taxonID":taxon_id,
               
            }
            csv_writer.writerow(row)

    print(f"CSV file created: {output_file}")

# This code will only run if this script is executed directly
if __name__ == "__main__":
    # Call the function with the input path
    json_to_csv(INPUT_PATH, UTC_OFFSET, TAXA_LIST_PATH)