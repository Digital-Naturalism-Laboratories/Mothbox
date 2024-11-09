
import json
import os
import datetime
import csv



INPUT_PATH = r'C:\Users\andre\Desktop\Mothbox data\PEA_PeaPorch_AdeptTurca_2024-09-01\2024-09-01'

def json_to_csv(input_path):
    # Get the last folder name from the input path
    folder_name = os.path.basename(input_path)

    # Get the current date in YYYY-MM-DD format
    current_date = datetime.date.today().strftime('%Y-%m-%d')

    # Create the output CSV file name
    output_file = f"{folder_name}_{current_date}.csv"

    # Append "samples.json" to the input path to get the correct file path
    json_file_path = os.path.join(input_path, "samples.json")

    try:
        with open(json_file_path, "r") as f:
            data = json.load(f)
        print("Found fiftyone dataset's json path")
    except FileNotFoundError:
        print("Could not find fiftyone dataset's json path, maybe try a different folder?")
        return

    with open(output_file, "w", newline="") as csvfile:
        fieldnames = ["basisOfRecord","datasetID","parentEventID","eventID","occurrenceID","verbatimEventDate","eventDate","eventTime","identifiedBy","taxonID","phylum","class","order","family","genus","species","commonName","scientificName","filepath", "mothbox","software","sheet","country", "area", "point","latitude","longitude","height","deployment_name","deployment_data","sample_time","collect_date", "data_storage_location","crew", "notes", "schedule","habitat", "image_id", "label", "bbox", "segmentation"]  # Adjust fieldnames as needed
        csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        csv_writer.writeheader()

        for sample in data["samples"]:
            for gtruth in sample["ground_truth"]: #will need to do this for all ground truth and all predictions

                for detection in gtruth[0]:
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
                    for tag in detection[0]:
                        # Check for prefixes
                        if tag.startswith("identifiedBy"):
                            identified_by = tag[len("identifiedBy"):].strip()
                        elif tag.startswith("taxonID"):
                            taxon_id = tag[len("taxonID"):].strip()
                        elif tag.startswith("phylum"):
                            phylum = tag[len("phylum"):].strip()
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

                    row = {
                        #"label_type":"ground_truth", 
                        "filepath":sample["filepath"],
                        #"id": sample["_id"],
                        #"image_id": sample["image_id"],
                        
                        #"basisOfRecord": sample["basisOfRecord"],
                        "datasetID":sample["_dataset_id"],
                        #"parentEventID":sample[""],
                        #"eventID":sample[""],
                        #"occurrenceID":sample[""],
                        #"verbatimEventDate":sample[""],
                        #"eventDate":sample[""],
                        #"eventTime":sample[""],

                        "mothbox":sample["mothbox"],
                        "software":sample["software"],
                        "sheet":sample["sheet"],
                        "country":sample["country"],
                        "area":sample["area"], 
                        "point":sample["punto"],
                        #"latitude":sample[""],
                        #"longitude":sample[""],
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
json_to_csv(INPUT_PATH)