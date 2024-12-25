"""
This script finds folders that have ground truth data
It also normalizes the data

"""
import os
import re
import json
import unicodedata

# Global input path
INPUT_PATH = r"F:\Panama"

def find_date_folders_inclusive(directory):
    """
    Recursively searches through a directory and its subdirectories for folders
    with names in the YYYY-MM-DD format.

    Args:
        directory: The directory to search.

    Returns:
        A list of paths to the found folders, including the root directory if it matches the date format.
    """
    date_regex = r"^\d{4}-\d{2}-\d{2}$"
    folders = []

    # Check if the root directory itself matches the date format
    if re.match(date_regex, os.path.basename(directory)):
        folders.append(directory)

    for root, dirs, _ in os.walk(directory):
        for dir_name in dirs:
            if re.match(date_regex, dir_name):
                folders.append(os.path.join(root, dir_name))

    return folders

def normalize_special_characters(value):
    """
    Normalizes special characters in a string by removing accents and converting to plain text.

    Args:
        value: The string to normalize.

    Returns:
        A normalized string with special characters replaced.
    """
    return unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')

def normalize_json(data):
    """
    Recursively normalizes all string values in a JSON-like structure (dict or list).

    Args:
        data: The JSON-like structure to normalize.

    Returns:
        The normalized JSON-like structure.
    """
    if isinstance(data, dict):
        return {key: normalize_json(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [normalize_json(item) for item in data]
    elif isinstance(data, str):
        return normalize_special_characters(data)
    else:
        return data

def find_ground_truth_data(input_path):
    """
    Finds and identifies ground-truth data folders.

    Args:
        input_path: The root directory to search for date folders.

    Returns:
        A list of paths containing ground-truth data.
    """
    ground_truth_folders = []
    date_folders = find_date_folders_inclusive(input_path)

    print(f"Total date folders found: {len(date_folders)}")

    json_file_regex = re.compile(r".*_\d{4}_\d{2}_\d{2}__\d{2}_\d{2}_\d{2}_HDR0\.json$")

    for index, folder in enumerate(date_folders):
        print(f"Processing folder {index + 1} of {len(date_folders)}: {folder}")
        for file_name in os.listdir(folder):
            if json_file_regex.match(file_name):
                json_path = os.path.join(folder, file_name)

                try:
                    with open(json_path, "r", encoding="utf-8") as json_file:
                        data = json.load(json_file)

                        # Normalize all string values in the JSON structure
                        #normalized_data = normalize_json(data)
                        normalized_data=data
                        # Save the normalized data back to the file
                        with open(json_path, "w", encoding="utf-8") as outfile:
                            json.dump(normalized_data, outfile, indent=4, ensure_ascii=False)

                        version = normalized_data.get("version", "")
                        if not version.startswith("Mothbot"):
                            ground_truth_folders.append(folder)
                            break  # No need to check further files in this folder

                except (json.JSONDecodeError, FileNotFoundError, KeyError) as e:
                    print(f"Error reading JSON file {json_path}: {e}")
                except UnicodeDecodeError as e:
                    print(f"Encoding error in file {json_path}: {e}")

    return ground_truth_folders

if __name__ == "__main__":
    # Find ground-truth folders and print them
    result = find_ground_truth_data(INPUT_PATH)
    print("\nGround-truth data folders:")
    for folder in result:
        print(folder)
