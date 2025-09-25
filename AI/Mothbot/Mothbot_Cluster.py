#!/usr/bin/env python3

"""
Mothbot_Cluster

This script tries to group all the detections in a night perceptually and then temporally

It takes a path to a nightly folder containing already detected creatures


Usage:
  python Mothbox_ID.py

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
ImageFile.LOAD_TRUNCATED_IMAGES = (
    True  # makes ok for use images that are messed up slightly
)
import torch
import json
#import PIL.Image
import warnings
warnings.filterwarnings("ignore", message="xFormers is not available*")
warnings.filterwarnings("ignore", message="'force_all_finite' was renamed")
import io #put these 3 lines here so radio can read stuff without breaking
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")


# ~~~~Variables to Change~~~~~~~

INPUT_PATH = (
   r"E:\MothboxData_Hubert\Projects\Donald's data\Australia\20220111-Australia-Battery-TimeDelay-Subset\2022-27-12"  # raw string
)

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





# Maybe this?
def Cluster_matched_img_json_pairs(
    hu_matched_img_json_pairs,bot_matched_img_json_pairs,  device):

    #Process Human Detections
    print("processing Human Detections.........")
    patch_paths_hu = []  # define this once before your loop
    json_paths_hu = []
    idx_paths_hu = []

    if(ID_HUMANDETECTIONS):
        # Next process each pair and generate temporary files for the ROI of each detection in each image
        # Iterate through image-JSON pairs
        index = 0
        numofpairs = len(hu_matched_img_json_pairs)
        for pair in hu_matched_img_json_pairs:

            # Load JSON file and extract rotated rectangle coordinates for each detection
            image_path, json_path = pair[:2]  # Always extract the first two elements

            coordinates_of_detections_list, was_pre_ided_list,thepatch_list = (
                get_rotated_rect_raw_coordinates(json_path)
            )
            index = index + 1
            print(
                str(index)
                + "/"
                + str(numofpairs)
                + "  | "
                + str(len(coordinates_of_detections_list)),
                "HUMAN detections in " + json_path,
            )
            if coordinates_of_detections_list:
                for idx, coordinates in enumerate(coordinates_of_detections_list):
                    #add path to list of patches for perceptual processing
                    patchfullpath=os.path.dirname(image_path)+"/"+ thepatch_list[idx]

                    patch_paths_hu.append(patchfullpath)
                    json_paths_hu.append(json_path)
                    idx_paths_hu.append(idx)


    #Process BOT Detections
    print("processing BOT Detections.........")
    patch_paths_bots = []  # define this once before your loop
    json_paths_bots = []
    idx_paths_bots = []
    if(ID_BOTDETECTIONS):
        # Next process each pair and generate temporary files for the ROI of each detection in each image
        # Iterate through image-JSON pairs
        index = 0
        numofpairs = len(bot_matched_img_json_pairs)
        for pair in bot_matched_img_json_pairs:

            # Load JSON file and extract rotated rectangle coordinates for each detection
            image_path, json_path = pair[:2]  # Always extract the first two elements

            coordinates_of_detections_list, was_pre_ided_list,thepatch_list  = (
                get_rotated_rect_raw_coordinates(json_path)
            )
            index = index + 1
            print(
                str(index)
                + "/"
                + str(numofpairs)
                + "  | "
                + str(len(coordinates_of_detections_list)),
                "BOT detections in " + json_path,
            )
            if coordinates_of_detections_list:
                for idx, coordinates in enumerate(coordinates_of_detections_list):
                    patchfullpath=os.path.dirname(image_path)+"/"+ thepatch_list[idx]

                    #add path to list of patches for later perceptual processing
                    patch_paths_bots.append(patchfullpath)
                    json_paths_bots.append(json_path)
                    idx_paths_bots.append(idx)

    # ~~~~~~~~~~~~~ PERCEPTUAL PROCESSING ~~~~~~~~~~~~~~~~~~~~~~~~
    #process perceptual similarities for bot and hu detections

    #Hu detections first
    if(len(patch_paths_hu)>0):
        embeddings = extract_embeddings(patch_paths_hu)
        labels = cluster_embeddings(embeddings)
        #save_clusters(input_folder, filenames, labels, output_folder)
        labels=temporal_subclusters(patch_paths_hu, json_paths_hu, idx_paths_hu, labels)
        write_cluster_to_json(patch_paths_hu, json_paths_hu, idx_paths_hu, labels)
    
    #bot detections first
    if(len(patch_paths_bots)>0):
        embeddings = extract_embeddings(patch_paths_bots)
        labels = cluster_embeddings(embeddings)
        labels=temporal_subclusters(patch_paths_bots, json_paths_bots, idx_paths_bots, labels)
        write_cluster_to_json(patch_paths_bots, json_paths_bots, idx_paths_bots, labels)


if __name__ == "__main__":

    """
    First the script takes in a INPUT_PATH

    Then, (to simplify its searching) it looks through all the folders for folders that are just a single "night"
    and follow the date format YYYY-MM-DD for their structure

    in each of these folders, it looks to see if there are any .json

    """
    print("Starting script to cluster detections into meaningful groups")
    args = parse_args()
    ID_BOTDETECTIONS=bool(int(args.ID_Bot))
    ID_HUMANDETECTIONS=bool(int(args.ID_Hum))
    INPUT_PATH= args.input_path

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
    print("Looking in this folder for MothboxData: " + INPUT_PATH)
    date_folders = find_date_folders(INPUT_PATH)
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
        + " pairs of images and HUMAN detection data to try to ID",
    )
    # Example Pair
    print("example human detection and json pair:")
    if(len(hu_matched_img_json_pairs)>0):
        print(hu_matched_img_json_pairs[0])
  
    print(
        "Found ",
        str(len(bot_matched_img_json_pairs))
        + " pairs of images and BOT detection data to try to ID",
    )
    # Example Pair
    print("example human detection and json pair:")
    if(len(bot_matched_img_json_pairs)>0):
        print(bot_matched_img_json_pairs[0])


    # ~~~~~~~~~~~~~~~~ Processing Data ~~~~~~~~~~~~~~~~~~~~~~~~~~


    # Now that we have our data to be processed in a big list, it's time to load up the Pybioclip stuff
    Cluster_matched_img_json_pairs(
        hu_matched_img_json_pairs,
        bot_matched_img_json_pairs,
        device=DEVICE,
    )

    print("Finished Automatic Clustering")
