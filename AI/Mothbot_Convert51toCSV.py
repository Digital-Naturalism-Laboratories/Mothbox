
import json
import os
import datetime
import csv

INPUT_PATH = 'F:/Panama/PEA_PeaPorch_AdeptTurca_2024-09-01/2024-09-01'

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
        fieldnames = ["basisOfRecord","datasetID","parentEventID","eventID","occurrenceID","verbatimEventDate","eventDate","eventTime","identifiedBy","taxonID","phyllum","class","order","family","genus","species","commonName","scientificName","filepath", "mothbox","software","sheet","country", "area", "point","latitude","longitude","height","deployment_name","deployment_data","sample_time","collect_date", "data_storage_location","crew", "notes", "schedule","habitat", "image_id", "label", "bbox", "segmentation"]  # Adjust fieldnames as needed
        csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        csv_writer.writeheader()

        for sample in data["samples"]:
            row = {
                "id": sample["id"],
                "image_id": sample["image_id"],
                "label": sample["label"],
                "bbox": sample["bbox"],
                "segmentation": sample["segmentation"]
            }
            csv_writer.writerow(row)

    print(f"CSV file created: {output_file}")

# Call the function with the input path
json_to_csv(INPUT_PATH)