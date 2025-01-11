import os
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

# Global variable to store the input path
INPUT_PATH = r"E:\Panama"  # Replace <INSERT_PATH_HERE> with the desired path

def check_file(file_path):
    """Check if the file contains a non-numerical version field."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # Read only the "version" field
            data = json.load(file)
            version = data.get("version")
            if version is not None and (not isinstance(version, str) or not version[0].isdigit()):
                return file_path
    except (json.JSONDecodeError, FileNotFoundError, KeyError) as e:
        print(f"Error processing file {file_path}: {e}")
    return None

def detect_false_ground_truth(input_path):
    """Detects files with a non-numerical version field in HDR0.json files."""
    flagged_files = []

    # Walk through all folders and subfolders to find HDR0.json files
    hdr0_files = [os.path.join(root, file)
                  for root, _, files in os.walk(input_path)
                  for file in files if file.endswith("HDR0.json")]

    # Print the number of HDR0.json files found
    print(f"Found {len(hdr0_files)} HDR0.json files.")

    # Process files in parallel with progress updates
    with ThreadPoolExecutor() as executor:
        future_to_file = {executor.submit(check_file, file_path): file_path for file_path in hdr0_files}
        for idx, future in enumerate(as_completed(future_to_file), start=1):
            print(f"Processed {idx}/{len(hdr0_files)} files.")
            result = future.result()
            if result:
                flagged_files.append(result)

    # Print the list of flagged files
    print("False Ground Truth files:")
    for flagged_file in flagged_files:
        print(flagged_file)

    # Save the list of flagged files to a text document
    with open("flaggedfiles.txt", "w", encoding="utf-8") as output_file:
        output_file.write("\n".join(flagged_files))
        print("Flagged files have been saved to 'flaggedfiles.txt'.")

# Run the function
if __name__ == "__main__":
    detect_false_ground_truth(INPUT_PATH)
