import os
import json
import unicodedata

INPUT_PATH = r"E:\Panama"

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

def contains_special_characters(data):
    """
    Recursively checks if any string values in a JSON-like structure contain special characters.

    Args:
        data: The JSON-like structure to check.

    Returns:
        True if any string values contain special characters, False otherwise.
    """
    if isinstance(data, dict):
        return any(contains_special_characters(value) for value in data.values())
    elif isinstance(data, list):
        return any(contains_special_characters(item) for item in data)
    elif isinstance(data, str):
        normalized = unicodedata.normalize('NFKD', data).encode('ascii', 'ignore').decode('ascii')
        return data != normalized
    else:
        return False

def normalize_json_files_in_path(input_path):
    """
    Normalizes all text in JSON files found within the given path and its subdirectories.

    Args:
        input_path: The root directory to search for JSON files.

    Prints status updates and processes all JSON files.
    """
    # Collect all JSON file paths
    json_files = []
    for root, _, files in os.walk(input_path):
        for file_name in files:
            if file_name.endswith('.json'):
                json_files.append(os.path.join(root, file_name))

    total_files = len(json_files)
    print(f"Total JSON files found: {total_files}")

    for index, json_path in enumerate(json_files):
        try:
            with open(json_path, "r", encoding="utf-8") as json_file:
                data = json.load(json_file)

            if contains_special_characters(data):
                # Normalize all string values in the JSON structure
                normalized_data = normalize_json(data)

                # Save the normalized data back to the file
                with open(json_path, "w", encoding="utf-8") as outfile:
                    json.dump(normalized_data, outfile, indent=4, ensure_ascii=False)

                print(f"Normalized: {json_path}")

        except (json.JSONDecodeError, FileNotFoundError, KeyError) as e:
            print(f"Error reading JSON file {json_path}: {e}")
        except UnicodeDecodeError as e:
            print(f"Encoding error in file {json_path}: {e}")

        # Print progress update
        progress = (index + 1) / total_files * 100
        print(f"Progress: {progress:.2f}% ({index + 1}/{total_files})")

if __name__ == "__main__":
    #INPUT_PATH = "<replace_with_your_input_path>"
    normalize_json_files_in_path(INPUT_PATH)
