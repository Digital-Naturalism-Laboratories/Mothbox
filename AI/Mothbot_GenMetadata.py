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

# Define a global variable for the default path
METADATA_PATH=r"F:\mothbox_metadata_2024-10-14.csv"
IMAGE_DATA_PATH=r"F:\Panama"


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
  
def convert_dates(df):
  """Converts dates in the 'deployment.date' column to YYYY-MM-DD format, handling various formats."""
  try:
    # Attempt conversion using pandas' built-in to_datetime with various format attempts
    for format in ['%d/%m/%Y', '%m/%d/%Y', '%Y-%m-%d']:  # Add more formats if needed
      try:
        df["deployment.date"] = pd.to_datetime(df["deployment.date"], format=format)
        break  # Stop iterating formats if successful
      except (pd.errors.ParserError, ValueError):
        pass  # Ignore parsing errors for this format, try the next one

    # Fallback using dateutil.parser for potentially ambiguous formats
    df["deployment.date"] = df["deployment.date"].apply(lambda x: parse(x).strftime("%Y-%m-%d") if pd.isna(x) else x)

    # Ensure all values are now strings in YYYY-MM-DD format
    df["deployment.date"] = df["deployment.date"].astype(str)
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
            str(metadata_row["mothbox"].lower()) == str(subfolder["mothbox"].lower()) and
            metadata_row["deployment.date"] == subfolder["date"]
        ):
            matches.append(subfolder["path"])
    return matches


# Get user input for paths
csv_path = get_csv_path()
image_data_path = get_image_data_path()

# Read the metadata
metadata = read_metadata(csv_path)

# Preprocess subfolders
preprocessed_subfolders = preprocess_subfolders(image_data_path)


if metadata is not None:
    metadata = convert_dates(metadata)  # Convert Dates to YYYY-MM-DD format  #Convert on a copy to avoid modifying original data
    for index, row in metadata.iterrows():
        matches = find_matching_subfolders(row, preprocessed_subfolders)
        print(f"Row {index + 1}: "+str(row["area"]) +str(row["point"]) + str(row["mothbox"]) +str(row["deployment.date"])  +"   \n Potential matches:")
        print(matches)
else:
    print("No metadata loaded.")

print("finished")
    