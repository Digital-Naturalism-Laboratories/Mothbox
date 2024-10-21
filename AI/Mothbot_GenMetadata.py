#!/usr/bin/env python3

"""
This script processes metadata collected from the field and pairs it to the raw image data.



Usage:
  python Mothbox_GenMetadata.py

Arguments:
  -h, --help    Show this help message and exit

Example:
  python process_metadata.py --input_file my_metadata.csv
"""

import os
import pandas as pd
import re
from datetime import datetime
from dateutil.parser import parse  # Import for flexible date parsing
import json


# Define a global variable for the default path
METADATA_PATH=r"C:\Users\andre\Desktop\Mothbox data\Mothbox data - metadata_2024-10-20.csv"
IMAGE_DATA_PATH=r"C:\Users\andre\Desktop\Mothbox data"

def convert_row_to_json(row, csv_headers):
  """Converts a CSV row to json metadata, dynamically adding annotations based on specified fields."""
  json_data = {
      #"image_id": 1,  # Replace with a unique image ID
      #"width": 800,  # Replace with actual image width
      #"height": 600,  # Replace with actual image height
      "metadata": []
  }

  for field_name, field_value in row.items():
    # Check if the value is NaN or None
    if pd.isnull(field_value):
      field_value = ""  # Replace NaN or None with an empty string
      #continue  # Skip NaN or None values

    json_data["metadata"].append({
        field_name: field_value,  # Replace with a unique annotation ID
    })

  return json_data


def find_date_folders(directory):
    """
    Recursively searches through a directory and its subdirectories for folders
    with names in the YYYY-MM-DD format.

    Args:
      directory: The directory to search.

    Returns:
      A list of paths to the found folders.
    """

    date_regex = r"^\d{4}-\d{2}-\d{2}$"
    folders = []

    for root, dirs, files in os.walk(directory):
        for dir_name in dirs:
            if re.match(date_regex, dir_name):
                folders.append(os.path.join(root, dir_name))

    return folders

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

    for root, dirs, files in os.walk(directory):
        for dir_name in dirs:
            if re.match(date_regex, dir_name):
                folders.append(os.path.join(root, dir_name))

    return folders




def get_csv_path():
  """Prompts user for CSV path and returns it. Falls back to default path if empty."""
  while True:
    csv_path = input("Enter the path to the CSV file (or press Enter to use default): ")
    if csv_path:
      return csv_path
    else:
      print(f"Using default path: {METADATA_PATH}")
      return METADATA_PATH

def get_image_data_path():
    """Prompts user for image data path and returns it. Falls back to default path if empty."""
    while True:
        image_data_path = input("Enter the path to the image data (or press Enter to use default): ")
        if image_data_path:
            return image_data_path
        else:
            print(f"Using default path: {IMAGE_DATA_PATH}")
            return IMAGE_DATA_PATH

def read_metadata(csv_path):
  """Reads the metadata CSV and returns a pandas DataFrame."""
  #import pandas as pd

  try:
    df = pd.read_csv(csv_path)
    return df
  except FileNotFoundError:
    print(f"Error: File not found at {csv_path}")
    return None
  
def normalize_date(date):
    parts = date.split('/')
    if len(parts) == 3:  # MM/DD/YYYY format
        month = parts[0].zfill(2)
        day = parts[1].zfill(2)
        year = parts[2]
        return f"{month}/{day}/{year}"
    elif len(parts) == 1:  # YYYY-MM-DD format
        parts = date.split('-')
        if len(parts) == 3:
            return f"{parts[0]}-{parts[1].zfill(2)}-{parts[2].zfill(2)}"
    return date  # Return as-is if not in recognized format

def convert_dates_in_dataframe(df):
    def convert_date(date):
        normalized_date = normalize_date(date)
        
        try:
            parsed_date = datetime.strptime(normalized_date, "%m/%d/%Y")
        except ValueError:
            try:
                parsed_date = datetime.strptime(normalized_date, "%Y-%m-%d")
            except ValueError:
                print(f"Unrecognized date format: {date}")
                return None
        
        return parsed_date.strftime("%Y-%m-%d")
    
    # Apply the conversion to the "deployment.date" column
    df['deployment.date'] = df['deployment.date'].apply(convert_date)
    return df

def normalize_date_gpt(date):
    parts = date.split('/')
    if len(parts) == 3:  # MM/DD/YYYY format
        month = parts[0].zfill(2)
        day = parts[1].zfill(2)
        year = parts[2]
        return f"{month}/{day}/{year}"
    elif len(parts) == 1:  # YYYY-MM-DD format
        parts = date.split('-')
        if len(parts) == 3:
            return f"{parts[0]}-{parts[1].zfill(2)}-{parts[2].zfill(2)}"
    return date  # Return as-is if not in recognized format

def convert_dates_GPT(date_list):
    converted_dates = []
    
    for date in date_list:
        normalized_date = normalize_date(date)
        
        try:
            parsed_date = datetime.datetime.strptime(normalized_date, "%m/%d/%Y")
        except ValueError:
            try:
                parsed_date = datetime.datetime.strptime(normalized_date, "%Y-%m-%d")
            except ValueError:
                print(f"Unrecognized date format: {date}")
                continue
        
        converted_dates.append(parsed_date.strftime("%Y-%m-%d"))
    
    return converted_dates


def convert_dates_OLD(df):
  """Converts dates in the 'deployment.date' column to YYYY-MM-DD format, handling various formats."""
  try:
    # Attempt direct conversion to datetime
    df["deployment.date"] = pd.to_datetime(df["deployment.date"])

    # Ensure all values are now strings in YYYY-MM-DD format
    df["deployment.date"] = df["deployment.date"].dt.strftime("%Y-%m-%d")

  except (pd.errors.ParserError, ValueError):
    # If direct conversion fails, try previous methods
    for format in ['%d/%m/%Y', '%m/%d/%Y', '%Y-%m-%d', '%Y/%m/%d']:
      try:
        df["deployment.date"] = df["deployment.date"].apply(lambda x: datetime.datetime.strptime(x, format))
      except (ValueError, TypeError):
        pass  # Ignore parsing errors for this format, try the next one

    # Fallback using datetime.datetime.strptime with infer_datetime_format=True
    df["deployment.date"] = df["deployment.date"].apply(lambda x: datetime.datetime.strptime(x, "%Y-%m-%d") if pd.notnull(x) else pd.NaT)

    # Ensure all values are now strings in YYYY-MM-DD format
    df["deployment.date"] = df["deployment.date"].apply(lambda x: x.strftime("%Y-%m-%d") if pd.notnull(x) else pd.NaT)

  except Exception as e:
    print(f"Error converting dates: {e}")  # Handle exceptions more specifically if needed

  return df

def preprocess_subfolders(image_data_path):
    """Preprocesses subfolders, ensuring they follow the naming convention and extracts dates."""
    subfolders = []
    for root, dirs, files in os.walk(image_data_path):
        for dir in dirs:
            # Check if the folder name matches the expected pattern
            match = re.match(r"(\w+)_(\w+)_(\w+)_(\w+)-(\w+)-(\w+)", dir)
            if match:
                area, point, mothbox, yyyy,mm,dd = match.groups()
                subfolders.append({
                    "area": area,
                    "point": point,
                    "mothbox": mothbox,
                    "path": os.path.join(root, dir),
                    "date": ""+str(yyyy)+"-"+str(mm)+"-"+str(dd)
                })
                #print(area, point, mothbox, ""+str(yyyy)+"-"+str(mm)+"-"+str(dd))
    return subfolders


def find_matching_subfolders(metadata_row, preprocessed_subfolders):
    """Finds matching subfolders using preprocessed data and checks deployment date."""
    matches = []
    for subfolder in preprocessed_subfolders:
         
        if (
            metadata_row["area"].lower() == subfolder["area"].lower() and
            metadata_row["point"].lower() == subfolder["point"].lower() and
            str(metadata_row["mothbox"].lower()).replace(" ", "") == str(subfolder["mothbox"].lower()) and
            metadata_row["deployment.date"] == subfolder["date"]
        ):
            matches.append(subfolder["path"])
    return matches

def scan_for_images_inallfoldersandsubfolders(folder_path):
  """Scans subfolders for JPEG files and returns a list of file paths."""
  jpeg_files = []
  for root, dirs, files in os.walk(folder_path):
    for file in files:
      if file.endswith(".jpg"):
        jpeg_files.append(os.path.join(root, file))
  return jpeg_files

def scan_for_images(folder_path):
  """Scans the specified folder for JPEG files and returns a list of file paths."""
  jpeg_files = []
  for file in os.listdir(folder_path):
    if file.endswith(".jpg"):
      jpeg_files.append(os.path.join(folder_path, file))
  return jpeg_files


# Get user input for paths
csv_path = get_csv_path()
image_data_path = get_image_data_path()

# Read the metadata
metadata = read_metadata(csv_path)

# Get CSV headers
csv_headers = metadata.columns.tolist()
print(csv_headers)
# Preprocess subfolders
preprocessed_subfolders = preprocess_subfolders(image_data_path)


if metadata is not None:
    metadata = convert_dates_in_dataframe(metadata)  # Convert Dates to YYYY-MM-DD format  #Convert on a copy to avoid modifying original data
    noMatches=[]
    for index, row in metadata.iterrows():
        matches = find_matching_subfolders(row, preprocessed_subfolders)
        print(f"Row {index + 1}: "+str(row["area"]) +str(row["point"]) + str(row["mothbox"]) +str(row["deployment.date"])  +"   \n Potential matches:")
        print(matches)

        if(len(matches)>0):
            date_folders = find_date_folders(matches[0]) #we only want to find images in the Date Folders
            
            for folder in date_folders:
               
              jpeg_files=scan_for_images(folder) #scan the first folder
              #print(len(jpeg_files))
              # ... iterate through JPEG files
              for jpeg_file in jpeg_files:
                  # Create COCO metadata
                  json_data = convert_row_to_json(row, csv_headers)

                  # Write metadata to a JSON file
                  #print(jpeg_file)
                  metadata_filename = os.path.splitext(jpeg_file)[0] + "_metadata.json"
                  with open(metadata_filename, "w") as f:
                      json.dump(json_data, f, indent=4)
        else:
           rowname=str(row["area"]) +str(row["point"]) + str(row["mothbox"]) +str(row["deployment.date"])
           noMatches.append(rowname)
    print("Could not find ",len(noMatches), "matches for these: \n")
    for missing in noMatches:
        print(missing)
else:
    print("No metadata loaded.")

print("finished")
    