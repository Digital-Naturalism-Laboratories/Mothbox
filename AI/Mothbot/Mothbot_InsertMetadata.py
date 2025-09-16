#!/usr/bin/env python3

"""
MOTHBOT_InsertMetadata
This script tries to put field sheet metadata into the json files associated with each raw image

Get list of taxa from just specific region in GBIF
ex:
country = 'PA' #2 letter country code https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2 "Panama"==PA
classKey = '216' # just insects i think

Example search in GBIF
https://www.gbif.org/occurrence/taxonomy?country=PA&taxon_key=212


Arguments:
  -h, --help    Show this help message and exit

"""

import ssl
ssl._create_default_https_context = ssl._create_unverified_context #needed for some macs to automatically download files associated with some of the libraries 

# import polars as pl
import os
import sys
import json
import argparse
import re
# import tempfile

# import io
# from pathlib import Path
import numpy as np
from PIL import Image
from PIL import ImageFile

#perception clustering
import torch
from tqdm import tqdm
import torchvision.transforms as T
import hdbscan

from datetime import datetime, timedelta
from collections import defaultdict
import csv



ImageFile.LOAD_TRUNCATED_IMAGES = (
    True  # makes ok for use images that are messed up slightly
)

#import cv2
import torch
import json
#import PIL.Image
import warnings
warnings.filterwarnings("ignore", message="xFormers is not available*")
warnings.filterwarnings("ignore", message="'force_all_finite' was renamed")



# ~~~~Variables to Change~~~~~~~

INPUT_PATH = (
   r"G:\Shared drives\Mothbox Management\Testing\ExampleDataset\Les_BeachPalm_hopeCobo_2025-06-20\2025-06-21"  # raw string
)

METADATA_PATH = r'..\Mothbox_Main_Metadata_Field_Sheet_Example - Form responses 1.csv'
#UTC_OFFSET= 8 # The file shou Panama is -5, Indonesia is 8 change for different locations

TAXA_LIST_PATH = r"..\SpeciesList_CountryIndonesia_TaxaInsecta.csv" # downloaded from GBIF for example just insects in panama: https://www.gbif.org/occurrence/taxonomy?country=PA&taxon_key=216


#you probably always want these below as true
ID_HUMANDETECTIONS = True
ID_BOTDETECTIONS = True

# Paths to save filtered list of embeddings/labels
image_embeddings_path = INPUT_PATH + "/image_embeddings.npy"
embedding_labels_path = INPUT_PATH + "/embedding_labels.json"

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input_path",
        required=False,
        default=INPUT_PATH,
        help="path to images for classification (ex: datasets/test_images/data)",
    )

    parser.add_argument(
        "--device",
        required=False,
        choices=["cpu", "cuda"],
        default=DEVICE,
        help="device on which to run pybioblip ('cpu' or 'cuda', default: what your comp detects)",
    )
    parser.add_argument(
        "--ID_Hum",
        required=False,
        default=ID_HUMANDETECTIONS,
        help="ID detections made by humans?",
    )
    parser.add_argument(
        "--ID_Bot",
        required=False,
        default=ID_BOTDETECTIONS,
        help="ID detections made by robots?",
    )


    return parser.parse_args()

# FUNCTIONS ~~~~~~~~~~~~~

def current_timestamp() -> str:
    """
    Returns the current timestamp in format:
    YYYY-MM-DD__HH_MM_SS_(±HHMM)
    """
    now = datetime.now().astimezone()  # local time with UTC offset
    return now.strftime("%Y-%m-%d__%H_%M_%S_(%z)")


#We don't use this function much anymore
def process_files_in_directory(data_path, classifier, taxon_rank="order"):
    """
    Processes files within a specified subdirectory.

    Args:
    data_path: String. The path to the directory containing files.
    classifier: CustomLabelsClassifier object from TAXA_KEYS_CSV.
    taxon_rank: String. Taxonomic rank to which to classify images (must be present as column in the taxa csv at file_path). Default: "order".
    """

    # Example: Print all file names in the subdirectory
    for file in os.listdir(data_path):
        file_path = os.path.join(data_path, file)
        if os.path.isfile(file_path):
            print(f"File: {file_path}")

    img_list = [f for f in os.listdir(data_path) if f.endswith(".jpg")]

    if not img_list:
        # No imgs were found in base level
        sys.exit("No .jpg images found in the data path: " + data_path)
    else:
        predictions = {}
        # Analyze the files
        print(f"Found {len(img_list)} .jpg images. \n Getting predictions...")
        i = 1
        for file in img_list:
            filename = os.path.splitext(file)[0]
            # print(filename)
            data = os.path.join(data_path, file)
            print(f"\n img # {str(i)} out of {str(len(img_list))}")
            i = i + 1

            # Run inference
            results = classifier.predict(data)
            classifier.predict_classifications_from_list()  # def predict_classifications_from_list(img: Union[PIL.Image.Image, str], cls_ary: List[str], device: Union[str, torch.device] = 'cpu') -> dict[str, float]:
            sorted_results = sorted(results, key=lambda x: x["score"], reverse=True)
            # Get the highest scoring result
            winner = sorted_results[0]
            pred = winner["classification"]

            # Print the winner
            print(
                filename
                + f"  This is the winner: {pred} with a score of {winner['score']}"
            )
            key = f"data/{file}"
            predstring = str(pred).strip().lower()
            print(predstring)
            if predstring in ["hole", "background", "wall", "floor", "blank", "sky"]:
                predictions[key] = f"abiotic_{pred}"
            else:
                predictions[key] = taxon_rank + "_" + pred
    return predictions


def find_date_folders(directory):
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


def find_detection_matches(folder_path):
    """Finds matching triplets of .jpg, botdetection.json, and potentially a humandetection .json files in a given folder.

    Args:
        folder_path: The path to the folder to search.

    Returns:
        two lists of tuples, where each tuple contains the paths to a matching .jpg, botdetection.json, 
        or matching jpg and  humandetection.json file.
    """

    # ALL jpg files in the folder
    jpg_files = [
        os.path.join(folder_path, f)
        for f in os.listdir(folder_path)
        if f.endswith(".jpg")
    ]
    # List of ALL json files in the folder
    json_files = [
        os.path.join(folder_path, f)
        for f in os.listdir(folder_path)
        if f.endswith(".json")
    ]

    hu_detection_matches_list = []
    bot_detection_matches_list = []

    for jpg_file in jpg_files:
        # target human file
        humanD_json_file = jpg_file.replace(".jpg", ".json")
        botD_json_file = jpg_file.replace(".jpg", "_botdetection.json")

        if humanD_json_file in json_files:
            hu_detection_matches_list.append((jpg_file,humanD_json_file))
        if botD_json_file in json_files:
            bot_detection_matches_list.append((jpg_file,botD_json_file))


    return hu_detection_matches_list, bot_detection_matches_list



def update_main_list(main_list, new_items):
    """Updates the main list with new items, avoiding duplicates.

    Args:
      main_list: The main list to update.
      new_items: A list of new items to add.

    Returns:
      The updated main list.
    """

    # Create a set of existing items for efficient lookup
    existing_items = set(main_list)

    # Add new items to the main list if they don't exist
    for item in new_items:
        if item not in existing_items:
            main_list.append(item)

    return main_list



def add_metadata_to_json(json_path, metadata_path):
    """Adds metadata from a separate JSON file to an existing JSON file.

    Args:
      json_path: The path to the JSON file to modify.
      metadata_path: The path to the JSON file containing the metadata to add.
    """

    with open(json_path, "r") as f:
        data = json.load(f)

    with open(metadata_path, "r") as f:
        metadata = json.load(f)

    # Check if the 'metadata' key exists in the data
    if "metadata" not in data:
        data["metadata"] = []  # Create an empty 'metadata' list if it doesn't exist

    # Add metadata to the existing 'metadata' list, avoiding duplicates
    for key, value in metadata.items():
        if not any(item.get(key) for item in data["metadata"]):
            data["metadata"].append({key: value})

    with open(json_path, "w") as f:
        json.dump(data, f, indent=4)

    print(f"Metadata added to {json_path}")


####################################
# --------------------------
# # Perceptual Processing Functions
# --------------------------
####################################

# --------------------------
# 1. Load DINOv2 model
# --------------------------
#device = "cuda" if torch.cuda.is_available() else "cpu"

model = torch.hub.load("facebookresearch/dinov2", "dinov2_vits14").to(DEVICE)
model.eval()

# Image preprocessing
transform = T.Compose([
    T.Resize(256),
    T.CenterCrop(224),
    T.ToTensor(),
    T.Normalize(mean=(0.5, 0.5, 0.5), std=(0.5, 0.5, 0.5))
])

# --------------------------
# 2. Extract embeddings
# --------------------------
def get_embedding(img_path):
    img = Image.open(img_path).convert("RGB")
    img_tensor = transform(img).unsqueeze(0).to(DEVICE)
    with torch.no_grad():
        feat = model(img_tensor)  # shape [1, 384]
    return feat.cpu().numpy().squeeze()


def extract_embeddings(image_files):
    embeddings, filenames = [], []
    for image_file in tqdm(image_files, desc="Extracting embeddings"):
        try:
            feat = get_embedding(image_file)
            embeddings.append(feat)
            filenames.append(image_file)
        except Exception as e:
            print(f"⚠️ Skipping {image_file}: {e}")
    return np.array(embeddings)

def extract_embeddings_from_folder(image_folder):
    embeddings, filenames = [], []
    for fname in tqdm(os.listdir(image_folder), desc="Extracting embeddings"):
        if not fname.lower().endswith((".jpg", ".jpeg", ".png")):
            continue
        path = os.path.join(image_folder, fname)
        try:
            feat = get_embedding(path)
            embeddings.append(feat)
            filenames.append(fname)
        except Exception as e:
            print(f"⚠️ Skipping {fname}: {e}")
    return np.array(embeddings), filenames

# --------------------------
# 3. Cluster with HDBSCAN
# --------------------------
def cluster_embeddings(embeddings):
    clusterer = hdbscan.HDBSCAN(
        min_cluster_size=3,          # smaller clusters allowed
        min_samples=1,               # fewer items marked as noise
        cluster_selection_epsilon=0.05,  # expand clusters slightly
        metric="euclidean"
    )
    labels = clusterer.fit_predict(embeddings)

    # Count clusters (ignore -1 which means "noise")
    unique_labels = set(labels)
    if -1 in unique_labels:
        unique_labels.remove(-1)
    n_clusters = len(unique_labels)

    print(f"✅ The clusterer (HDBSCAN() created {n_clusters} clusters of similar insect photos (and {np.sum(labels == -1)} noise points - ie insect photos that were unique).")

    return labels

# --------------------------
# 4. Write cluster to JSON
# --------------------------
def write_cluster_to_json(filepaths, json_paths, idxes, labels):
    for fname,json_path,i, label in zip(filepaths, json_paths,idxes, labels):
        try:
            with open(json_path, "r") as f:
                data = json.load(f)
            if 0 <= i < len(data["shapes"]):
                shape = data["shapes"][i]
                shape["clusterID"] = float(label)
                shape["timestamp_cluster"] = current_timestamp()
            with open(json_path, "w") as f:
                json.dump(data, f, indent=4)
            
        except Exception as e:
            print(f"⚠️ Could not update {fname}: {e}")
    print("✅ Cluster IDs written into 'Json' field.")




# Subcluster through TIME
def temporal_subclusters(
    patch_paths_hu, json_paths_hu, idx_paths_hu, labels, gap_minutes=1
):
    """
    Creates temporal subclusters within perceptual clusters based on timestamp proximity.

    Args:
        patch_paths_hu (list[str]): Paths to parent images
        json_paths_hu (list[str]): Paths to JSON metadata
        idx_paths_hu (list[str]): Paths to cropped insect images
        labels (list[int]): Cluster IDs for each detection (from HDBSCAN etc.)
        gap_minutes (int, optional): Maximum gap (in minutes) allowed between
                                     consecutive detections in the same temporal chain.
                                     Default = 1.

    Returns:
        list[str]: A list of new cluster IDs (like "3.1", "3.2") aligned with inputs.
    """
    # Initialize result list (default keep -1 for noise)
    new_labels = [str(l) if l != -1 else "-1" for l in labels]

    # Group indices by cluster
    cluster_to_indices = defaultdict(list)
    for idx, cl in enumerate(labels):
        if cl != -1:  # skip noise
            cluster_to_indices[cl].append(idx)

    # Regex to extract timestamp from filename
    ts_pattern = re.compile(r"(\d{4}_\d{2}_\d{2}__\d{2}_\d{2}_\d{2})")

    # Loop through each perceptual cluster
    for cluster_id, indices in cluster_to_indices.items():
        timestamps = []
        for i in indices:
            fname = os.path.basename(patch_paths_hu[i])
            match = ts_pattern.search(fname)
            if not match:
                raise ValueError(f"Could not parse timestamp from filename: {fname}")
            ts_str = match.group(1)
            ts = datetime.strptime(ts_str, "%Y_%m_%d__%H_%M_%S")
            timestamps.append((i, ts))

        # Sort detections in this cluster by time
        timestamps.sort(key=lambda x: x[1])

        # Find temporal sequences
        gap = timedelta(minutes=gap_minutes)
        seq_id = 1
        prev_time = None

        for i, ts in timestamps:
            if prev_time is None:
                # start first sequence
                new_labels[i] = f"{cluster_id}.{seq_id}"
                prev_time = ts
            else:
                if ts - prev_time <= gap:
                    # same sequence
                    new_labels[i] = f"{cluster_id}.{seq_id}"
                else:
                    # new sequence
                    seq_id += 1
                    new_labels[i] = f"{cluster_id}.{seq_id}"
                prev_time = ts

    return new_labels

# Patch get_txt_names to always use UTF-8
def fixed_get_txt_names(self):
    txt_names_json = self.get_cached_datafile("embeddings/txt_emb_species.json")
    with open(txt_names_json, encoding="utf-8") as fd:
        return json.load(fd)


def get_rotated_rect_raw_coordinates(json_file):
    """Reads rotated rectangle coordinates from a JSON file and returns them."""
    pre_ided = False  # variable to detect if this has already been IDed

    with open(json_file, "r") as f:
        data = json.load(f)
        coordinates_list = []
        pre_ided_list = []
        patch_list = []
        for shape in data["shapes"]:
            if shape["shape_type"] == "rotation":
                patch=shape["patch_path"]
                patch_list.append(patch)
                points = shape["points"]
                # x, y, w, h, angle = extract_rectangle_coordinates(points)
                coordinates_list.append(points)
                
                if "identifier_bot" in shape:
                    if shape["identifier_bot"] != "": # detect if there's been an identification (if so it would say something like pybioclip)
                        pre_ided = True
                        #print("it was previously IDed")
                pre_ided_list.append(pre_ided)

        return coordinates_list, pre_ided_list, patch_list





def extract_number(raw_height):
  """
  Extracts the numerical value from a string representing height.

  Args:
    raw_height: The string containing the height information.

  Returns:
    The numerical value of the height as a float, or None if no numerical value 
    could be extracted.
  """
  # Use regular expression to find the first floating-point or integer number
  match = re.search(r"[-+]?\d+\.?\d*|\d+", raw_height) 
  if match:
    return float(match.group(0))
  else:
    return None


def handle_rotation_annotation(points):
  """Converts an oriented bounding box to a horizontal bounding box.

  Args:
    points: A list of points representing the vertices of the oriented bounding box.

  Returns:
    A tuple containing the top, left, width, and height of the horizontal bounding box.
  """

  min_x = float('inf')
  max_x = -float('inf')
  min_y = float('inf')
  max_y = -float('inf')

  for point in points:
    x, y = point
    min_x = min(min_x, x)
    max_x = max(max_x, x)
    min_y = min(min_y, y)
    max_y = max(max_y, y)

  top = min_y
  left = min_x
  width = max_x - min_x
  height = max_y - min_y

  return top, left, width, height



#PUt everything in the JSON

def load_anylabeling_data(json_path, image_path, metadata): #TODO load METADATA STRAIGHT FROM CSV - METADATA_PATH - Maybe metadata gets loaded into its own 51 thing via the WHOLe dataset?
  
  """Loads data from an AnyLabeling JSON file.

  Args:
    json_path: The path to the JSON file.

  Returns:
    A dictionary containing the loaded data.
  """
  latitude = metadata.get("latitude", "0.00000")
  longitude = metadata.get("longitude", "0.00000")
  therawgroundheight = metadata.get("height_above_ground", "-1")

  with open(json_path, 'r') as f:
    data = json.load(f)

    data["filepath"] = image_path
    data["uploaded"] = metadata.get("uploaded", "")
    data["sd"] = metadata.get("sd_card", "")
    data["device"] = metadata.get("device", "")
    data["firmware"] = str(metadata.get("firmware", ""))
    data["sheet"] = metadata.get("sheet", "")
    data["datasetcollection"] = metadata.get("dataset", "")
    data["project"] = metadata.get("project", "")
    data["site"] = metadata.get("site", "")
    data["longitude"] = longitude
    data["latitude"] = latitude
    data["ground_height"] = extract_number(therawgroundheight)
    data["deployment_name"] = metadata.get("deployment_name", "")
    data["UTC"] = metadata.get("UTC", "0")
    data["deployment_date"] = metadata.get("deployment_date", "")
    data["collect_date"] = metadata.get("collect_date", "")
    data["data_storage_location"] = metadata.get("data_storage_location", "")
    data["crew"] = metadata.get("crew", "")
    data["notes"] = metadata.get("notes", "")
    data["schedule"] = metadata.get("schedule", "")
    data["habitat"] = metadata.get("habitat", "")
    data["attractor"] = metadata.get("attractor", "")
    data["attractor_location"] = metadata.get("attractor_location", "")

  with open(json_path, "w") as f:
      json.dump(data, f, indent=4)

  print("✅ Metadata written into 'Json' field for." +str(json_path))


  
  return





def create_sample(image_path, labels, image_height, image_width, metadata, detection_creator):# skipping exif tagger for now, tagger):
  """Creates a FiftyOne sample using the 51 python interface

  Args:


  Returns:

  """
  
  latitude = metadata.get("latitude", "0.00000")
  longitude = metadata.get("longitude", "0.00000")
  therawgroundheight = metadata.get("height_above_ground", "-1")

  sample = {
      "filepath": image_path,
      "uploaded": metadata.get("uploaded", ""),
      "sd": metadata.get("sd_card", ""),
      "device": metadata.get("device", ""),
      "firmware": str(metadata.get("firmware", "")),
      "sheet": metadata.get("sheet", ""),
      "datasetcollection": metadata.get("dataset", ""),
      "project": metadata.get("project", ""),
      "site": metadata.get("site", ""),
      "longitude": longitude,
      "latitude": latitude,
      "ground_height": extract_number(therawgroundheight),
      "deployment_name": metadata.get("deployment_name", ""),
      "UTC": metadata.get("UTC", "0"),
      "deployment_date": metadata.get("deployment_date", ""),
      "collect_date": metadata.get("collect_date", ""),
      "data_storage_location": metadata.get("data_storage_location", ""),
      "crew": metadata.get("crew", ""),
      "notes": metadata.get("notes", ""),
      "schedule": metadata.get("schedule", ""),
      "habitat": metadata.get("habitat", ""),
      "attractor": metadata.get("attractor", ""),
      "attractor_location": metadata.get("attractor_location", ""),
      "image_height": image_height,
      "image_width": image_width,
      "detection_By": str(detection_creator),
  }


  detections_list=[]

  for label in labels:
    direction = label['direction']
    label_name = label['label']
    theclusterID= label['clusterID']
    score = label['score']
    points = label['points']
    shape_type = label['shape_type']
    ID_by = "IDby_"+label['description']
    the_patch_path= label['patch_path']

    desired_keys = ['kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species']


    # Filter the dictionary to include only desired keys
    filtered_dict = {key: value for key, value in label.items() if key in desired_keys}

    # Check for unwanted values
    unwanted_values = {"error", "ERROR", "Error"}
    if any(any(u.lower() in value.lower() for u in unwanted_values) for value in filtered_dict.values()):
        taxonomic_list = ["Error"]
    else:
        # Format the filtered dictionary
        taxonomic_list = [f"{key.upper()}_{value}" for key, value in filtered_dict.items()]


    
    taxonomic_list.append(ID_by)

    if shape_type == 'rotation': #Todo - these should be handled as a polygon in 51, because they only have regular rects they call "Detections" but we have rotated rects (that should be stored as polylines via polyline.fromrotatedboundingbox https://docs.voxel51.com/user_guide/using_datasets.html#rotated-bounding-boxes)
      top, left, width, height = handle_rotation_annotation(points)
      
    
      # Normalize bounding box coordinates
      top /= image_height
      left /= image_width
      width /= image_width
      height /= image_height
      # Create a FiftyOne detection
      

      detection = {
        "tags": taxonomic_list,
        "label": "creature",
        "bounding_box": [left, top, width, height],
        # "attributes": {},   # uncomment if you want
        # "ID_by": ID_by,    # uncomment if you want
        "confidence": score,
        "shape": shape_type,
        "rot_direction": direction,
        "patch_path": the_patch_path,
        "clusterID": theclusterID,
      }

      detections_list.append(detection)
    elif shape_type == 'polygon':
      # Handle polygon annotations (adjust as needed)
      None
  #print("num detections")
  #print(len(detections_list))
  sample["creature_detections"] = fol.Detections(detections=detections_list) #TODO - give this an appropriate name

  return sample

# Maybe this?
def connect_metadata_matched_img_json_pairs(
    hu_matched_img_json_pairs,bot_matched_img_json_pairs, metadata,  device):

    #Process Human Detections
    print("processing Human Detections.........")
    if(ID_HUMANDETECTIONS):
        # Next process each pair and generate temporary files for the ROI of each detection in each image
        # Iterate through image-JSON pairs
        index = 0
        numofpairs = len(hu_matched_img_json_pairs)
        for pair in hu_matched_img_json_pairs:

            # Load JSON file
            image_path, json_path = pair[:2]  # Always extract the first two elements

            load_anylabeling_data(json_path, image_path, metadata)

    print("processing BOT Detections.........")
    if(ID_BOTDETECTIONS):
        # Next process each pair and generate temporary files for the ROI of each detection in each image
        # Iterate through image-JSON pairs
        index = 0
        numofpairs = len(bot_matched_img_json_pairs)
        for pair in bot_matched_img_json_pairs:
            # Load JSON file and 
            image_path, json_path = pair[:2]  # Always extract the first two elements

            load_anylabeling_data(json_path, image_path, metadata)


def _without_first_prefix(name: str) -> str:
    """Return the string with the first underscore-separated prefix removed.
    e.g. 'Indonesia_Les_Wilan...' -> 'Les_Wilan...'. If no underscore, returns original.
    """
    if not name:
        return name
    parts = name.split('_', 1)
    return parts[1] if len(parts) == 2 else name

def find_csv_match(input_path: str, metadata_path: str) -> dict:
    """
    Finds a row in the CSV where 'deployment.name' matches the folder name of input_path.
    Tolerates the presence/absence of the first leading prefix on either side.
    Matching is case-insensitive.
    If multiple matches are found, prints a warning and returns only the first one.

    Returns:
        dict: The first matching row as a dict, or {} if no match is found.
    """
    parent_folder = os.path.basename(os.path.dirname(input_path)).strip()
    alt_parent = _without_first_prefix(parent_folder)

    # store variants in lowercase for case-insensitive matching
    folder_variants = {parent_folder.lower(), alt_parent.lower()}

    matches = []
    print(f"scanning for metadata matches... (folder variants: {folder_variants})")

    with open(metadata_path, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            dep_name = (row.get("deployment_name") or "").strip()
            if not dep_name:
                continue

            alt_dep = _without_first_prefix(dep_name)
            dep_variants = {dep_name.lower(), alt_dep.lower()}

            # if any variant intersects, it's a match
            if folder_variants & dep_variants:
                matches.append(row)

    if not matches:
        print(f"⚠️ No match found for '{parent_folder}' (or '{alt_parent}') in {metadata_path}")
        return {}

    if len(matches) > 1:
        print(f"⚠️ Warning: Multiple matches found for '{parent_folder}', using the first one.")

    print(f"✅ Matched deployment.name = '{matches[0].get('deployment_name')}'")
    return matches[0]


if __name__ == "__main__":

    """
    First the script takes in a INPUT_PATH

    Then, (to simplify its searching) it looks through all the folders for folders that are just a single "night"
    and follow the date format YYYY-MM-DD for their structure

    in each of these folders, it looks to see if there are any .json

    """
    print("Starting script to  add metadata to raw iamges")
    args = parse_args()
    ID_BOTDETECTIONS=bool(int(args.ID_Bot))
    ID_HUMANDETECTIONS=bool(int(args.ID_Hum))


    # Check if CUDA is available
    if torch.cuda.is_available():
        print("CUDA is available!")
        print("CUDA version:", torch.version.cuda)
        print("Number of GPUs:", torch.cuda.device_count())
        print("Current device:", torch.cuda.current_device())
        print("GPU Name:", torch.cuda.get_device_name(torch.cuda.current_device()))
        DEVICE = torch.device("cuda")
    else:
        print("CUDA not available, using CPU")
        DEVICE = torch.device("cpu")


    # ~~~~~~~~~~~~~~~~ GATHERING DATA ~~~~~~~~~~~~~~~~~~~~~~~~~~

    # Find all the dated folders that our data lives in
    print("Looking in this folder for MothboxData: " + args.input_path)
    date_folders = find_date_folders(args.input_path)
    print(
        "Found ",
        str(len(date_folders)) + " dated folders potentially full of mothbox data",
    )

    # Look in each dated folder for .json detection files and the matching .jpgs
    hu_matched_img_json_pairs = []
    bot_matched_img_json_pairs = []

    for folder in date_folders:
        hu_list_of_matches, bot_list_of_matches = find_detection_matches(folder)
        hu_matched_img_json_pairs = update_main_list(
            hu_matched_img_json_pairs, hu_list_of_matches
        )
        bot_matched_img_json_pairs = update_main_list(
            bot_matched_img_json_pairs, bot_list_of_matches
        )

    print(
        "Found ",
        str(len(hu_matched_img_json_pairs))
        + " pairs of images and HUMAN detection data to insert metadata",
    )
    # Example Pair
    print("example human detection and json pair:")
    if(len(hu_matched_img_json_pairs)>0):
        print(hu_matched_img_json_pairs[0])
  
    print(
        "Found ",
        str(len(bot_matched_img_json_pairs))
        + " pairs of images and BOT detection data to insert metadata",
    )
    # Example Pair
    print("example human detection and json pair:")
    if(len(bot_matched_img_json_pairs)>0):
        print(bot_matched_img_json_pairs[0])

    metadata= find_csv_match(INPUT_PATH, METADATA_PATH)

    # ~~~~~~~~~~~~~~~~ Processing Data ~~~~~~~~~~~~~~~~~~~~~~~~~~


    # Now that we have our data to be processed in a big list, it's time to load up the Pybioclip stuff
    connect_metadata_matched_img_json_pairs(
        hu_matched_img_json_pairs,
        bot_matched_img_json_pairs,
        device=DEVICE, metadata=metadata,
    )

    print("Finished Attaching Metadata field info")
