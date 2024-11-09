
import json
import os
import datetime
import csv
import re
from datetime import datetime, timedelta

INPUT_PATH = r'C:\Users\andre\Desktop\Mothbox data\PEA_PeaPorch_AdeptTurca_2024-09-01\2024-09-01'
UTC_OFFSET=-5 #panama



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
    
    # Step 2: Apply the UTC offset (assuming utc_offset is in hours)
    #adjusted_datetime = original_datetime + timedelta(hours=utc_offset)
    adjusted_datetime = original_datetime # I don't think we need to adjust we just include the offset
    
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

def json_to_csv(input_path, utc_offset):
    # Get the last folder name from the input path
    folder_name = os.path.basename(input_path)

    # Get the current date in YYYY-MM-DD format
    current_date = datetime.today().strftime('%Y-%m-%d')

    # Create the output CSV file name
    output_file = f"{folder_name}_exportdate_{current_date}.csv"

    # Append "samples.json" to the input path to get the correct file path
    json_file_path = os.path.join(input_path, "samples.json")

    try:
        with open(json_file_path, "r") as f:
            data = json.load(f)
        print("Found fiftyone dataset's json path")
    except FileNotFoundError:
        print("Could not find fiftyone dataset's json path, maybe try a different folder?")
        return

    with open(INPUT_PATH+"/"+output_file, "w", newline="") as csvfile:
        fieldnames = ["basisOfRecord","datasetID","parentEventID","eventID","occurrenceID","verbatimEventDate","eventDate","eventTime","UTC_OFFSET","identifiedBy","taxonID","kingdom","phylum","class","order","family","genus","species","commonName","scientificName","filepath", "mothbox","software","sheet","country", "area", "point","latitude","longitude","height","deployment_name","deployment_data","sample_time","collect_date", "data_storage_location","crew", "notes", "schedule","habitat", "image_id", "label", "bbox", "segmentation"]  # Adjust fieldnames as needed
        csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        csv_writer.writeheader()

        for sample in data["samples"]:

            #tags are the only thing directly editable in 51
            identified_by=""
            taxon_id=""
            phylum=""
            tclass=""
            order=""
            family=""
            genus=""
            species=""
            commonName=""
            scientificName=""
            kingdom=""



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
                    kingdom = tag[len("KINGDOM"):].strip()
                elif tag.startswith("PHYLUM"):
                    phylum = tag[len("PHYLUM"):].strip()
                elif tag.startswith("tclass"):
                    tclass = tag[len("tclass"):].strip()
                elif tag.startswith("order"):
                    order = tag[len("order"):].strip()
                elif tag.startswith("family"):
                    family = tag[len("family"):].strip()
                elif tag.startswith("genus"):
                    genus = tag[len("genus"):].strip()
                elif tag.startswith("species"):
                    species = tag[len("species"):].strip()
                elif tag.startswith("commonName"):
                    common_name = tag[len("commonName"):].strip()
                elif tag.startswith("scientificName"):
                    scientific_name = tag[len("scientificName"):].strip()
                elif tag.startswith("IDby"):
                    identified_by = tag[len("IDby"):].strip()

            if tag.startswith("taxonID"):
                taxon_id = tag[len("taxonID"):].strip()
            elif tag.startswith("phylum"):
                phylum = tag[len("phylum"):].strip()
        #fieldnames = ["basisOfRecord","datasetID","parentEventID","eventID","occurrenceID","verbatimEventDate","eventDate","eventTime","identifiedBy","taxonID","kingdom","phylum","class","order","family","genus","species","commonName","scientificName","filepath", "mothbox","software","sheet","country", "area", "point","latitude","longitude","height","deployment_name","deployment_data","sample_time","collect_date", "data_storage_location","crew", "notes", "schedule","habitat", "image_id", "label", "bbox", "segmentation"]  # Adjust fieldnames as needed

            row = {
                #"label_type":"ground_truth", 
                "filepath":sample["filepath"],
                #"id": sample["_id"],
                #"image_id": sample["image_id"],
                
                "basisOfRecord": "machine_observation",
                "datasetID":sample["_dataset_id"],
                "parentEventID":"",
                "eventID":"",
                "occurrenceID":"",
                "verbatimEventDate":date+"__"+timestamp,
                "eventDate":formattedUTC_dateTime,
                "eventTime":formattedUTC_dateTime.split("T")[1],
                "UTC_OFFSET":utc_offset,
                "mothbox":sample["mothbox"],
                "software":sample["software"],
                "sheet":sample["sheet"],
                "country":sample["country"],
                "area":sample["area"], 
                "point":sample["punto"],
                "latitude":sample["latitude"],
                "longitude":sample["longitude"],
                #"height":sample["height"],
                #"deployment_name":sample[""],
                #"deployment_data":sample[""],
                #"sample_time":sample[""],
                #"collect_date":sample[""], 
                #"data_storage_location":sample[""],
                #"crew":sample[""], 
                #"notes":sample[""], 
                #"schedule":sample[""],
                #"habitat":sample[""], 

                #detection specific
                "identifiedBy":identified_by,
                "taxonID":taxon_id,
                "kingdom":kingdom,
                "phylum":phylum,
                "class":tclass,
                "order":order,
                "family":family,
                "genus":genus,
                "species":species,
                "commonName":commonName,
                "scientificName":scientificName,
                #"detection_type": detection["_cls"],
                #"points":tag["bounding_box"],
                #"detectionID":tag["_id"]

                
            }
            csv_writer.writerow(row)

    print(f"CSV file created: {output_file}")

# Call the function with the input path
json_to_csv(INPUT_PATH, UTC_OFFSET)