#!/usr/bin/env python3

"""
MOTHBOT_ID
This script looks for mothbox image data and detection data, pairs them together, finds the region of interest in the image of the detection
feeds this ROI to pyBIOCLIP to try to get an ID

the pybioclip also takes in GBIF species lists


Get list of taxa from just specific region in GBIF
ex:
country = 'PA' #2 letter country code https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2 "Panama"==PA
classKey = '216' # just insects i think

Example search in GBIF
https://www.gbif.org/occurrence/taxonomy?country=PA&taxon_key=212


Usage:
  python Mothbox_ID.py

Arguments:
  -h, --help    Show this help message and exit

"""
import ssl
ssl._create_default_https_context = ssl._create_unverified_context #needed for some macs to automatically download files associated with some of the libraries 
print("Loading all the ID libraries...")
import polars as pl
import os
import sys
import json
import argparse
import re
import io
from pathlib import Path
import numpy as np
from PIL import Image
from PIL import ImageFile
import torch
from datetime import datetime
ImageFile.LOAD_TRUNCATED_IMAGES = (
    True  # makes ok for use images that are messed up slightly
)
from bioclip import TreeOfLifeClassifier, Rank, CustomLabelsClassifier
from bioclip.predict import create_classification_dict
import importlib.metadata
VERSION = "pybioclip_"+importlib.metadata.version("pybioclip")
print("ID model: "+VERSION)


# ~~~~Variables to Change~~~~~~~

INPUT_PATH = (
   r"D:\MothboxData_Hubert\data\Panama\Hoya_119m_bothDeer_2025-01-26\2025-01-26"  # raw string
)
SPECIES_LIST = r"../SpeciesList_CountryPanamaCostaRica_TaxaInsecta_doi.org10.15468dl.6nxkw6.csv"  # downloaded from GBIF for example just insects in panama: https://www.gbif.org/occurrence/taxonomy?country=PA&taxon_key=212


""" KINGDOM = 0
    PHYLUM = 1
    CLASS = 2
    ORDER = 3
    FAMILY = 4
    GENUS = 5
    SPECIES = 6"""

TAXONOMIC_RANK_FILTER_num = 3 #!!! change this number to change the taxonomic rank we filter with. IE filter to order with "3" or filter to genus with "5"

# you can See if a json file has an existing ID by looking at identifier_bot: pybioclip  
OVERWRITE_EXISTING_IDs = True #True

#you probably always want these below as true
ID_HUMANDETECTIONS = True
ID_BOTDETECTIONS = True
# ~~~~Other Global Variables~~~~~~~

TAXA_COLS = ["kingdom", "phylum", "class", "order", "family", "genus", "species"]
TAXONOMIC_RANK_FILTER = Rank.ORDER
TOL_TAXONOMIC_RANK = "species"  # Change this to "species" to target just the species in your CSV # Note i think this is actually just always needs to be set for SPECIES for this exampple
DOMAIN = "Eukarya"  # basically our "creature" tag? figure we will never see a prokaryote on the mothbox # Also i think GBIF has a "Biota" category that is a fancier version of "creature" or "life"
taxa_path = SPECIES_LIST

# Paths to save filtered list of embeddings/labels
image_embeddings_path = INPUT_PATH + "/image_embeddings.npy"
embedding_labels_path = INPUT_PATH + "/embedding_labels.json"
#print(torch.cuda.is_available())
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
DOI= ""

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input_path",
        required=False,
        default=INPUT_PATH,
        help="path to images for classification (ex: datasets/test_images/data)",
    )
    parser.add_argument(
        "--TOLrank",
        default=TOL_TAXONOMIC_RANK,
        #help="rank to which to classify; must be column in --taxa-csv (default: {TAXONOMIC_RANK})", #this always needs to just be left at species i think
    )

    parser.add_argument(
        "--rank",
        default=TAXONOMIC_RANK_FILTER_num,
        help="rank to which to classify; must be column in --taxa-csv (default: {TAXONOMIC_RANK})", 
    )
    parser.add_argument(
        "--flag-det-errors",
        default=True,
        action=argparse.BooleanOptionalAction,
        help="whether to flag detection errors like holes and smudges (default: --flag-det-errors)",
    )
    parser.add_argument(
        "--taxa_csv",
        default=SPECIES_LIST,
        help="CSV with taxonomic labels to use for CustomClassifier (default: {SPECIES_LIST})",
    )
    parser.add_argument(
        "--taxa_cols",
        default=TAXA_COLS,
        help=f"taxonomic columns in taxa CSV to load (default: {TAXA_COLS})",
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
    parser.add_argument(
        "--overwrite_prev_bot_ID",
        default=OVERWRITE_EXISTING_IDs,
        required=False,
        help="If IDs already exist, should we overwrite?",
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

def load_taxon_keys(taxa_path, taxa_cols=None, taxon_rank="order", flag_det_errors=True):
    """
    Read taxa_path (path, bytes, or file-like) robustly handling encoding issues
    and return a set of unique, lowercased values for taxon_rank.

    Returns:
        set(str): lowercased unique taxon_rank values
    """
    print(f"Reading {taxa_path!s}, extracting {taxon_rank} values.")

    # encodings to try in order (utf-8 first, then common windows/latin fallbacks)
    encodings = ("utf-8", "utf-8-sig", "utf-16", "cp1252", "latin-1")

    raw = None
    text = None

    # Accept bytes/bytearray directly
    if isinstance(taxa_path, (bytes, bytearray)):
        raw = bytes(taxa_path)

    # Accept an already-open file-like object
    elif hasattr(taxa_path, "read"):
        try:
            # try reading bytes first (some file-like objects are in binary mode)
            raw = taxa_path.read()
        except Exception:
            # if that fails, try text-mode read
            taxa_path.seek(0)
            text = taxa_path.read()

    # Otherwise treat it as a filesystem path-like
    else:
        p = Path(taxa_path)
        if not p.exists():
            raise FileNotFoundError(f"taxa_path not found: {taxa_path}")
        with open(p, "rb") as f:
            raw = f.read()

    # If we already have text (not bytes), use it
    if text is None:
        # If raw is already str (unlikely) use it
        if isinstance(raw, str):
            text = raw
        else:
            # Try the encodings in order
            decoded = None
            for enc in encodings:
                try:
                    decoded = raw.decode(enc)
                    # quick sanity check: if decoding produced something non-empty, accept it
                    if decoded is not None:
                        text = decoded
                        break
                except Exception:
                    continue
            # Last-resort: decode with replacement so we never raise UnicodeDecodeError
            if text is None:
                text = raw.decode("utf-8", errors="replace")

    # Try to load into Polars; prefer tab-separated but fall back to automatic parsing.
    try:
        df = pl.read_csv(io.StringIO(text), separator="\t")
    except Exception:
        try:
            df = pl.read_csv(io.StringIO(text))  # let polars infer delimiter
        except Exception:
            # final fallback: use pandas to parse then convert to polars
            import pandas as pd
            df_pd = pd.read_csv(io.StringIO(text), sep="\t")
            df = pl.from_pandas(df_pd)

    # If user provided a taxa_cols mapping/dictionary, prefer it for column lookup
    chosen_col = None
    if taxa_cols and isinstance(taxa_cols, dict):
        chosen_col = taxa_cols.get(taxon_rank, None)

    # If chosen_col not set or not present, do case-insensitive matching against dataframe columns
    if not chosen_col or chosen_col not in df.columns:
        cols_lower = {c.lower(): c for c in df.columns}
        if taxon_rank.lower() in cols_lower:
            chosen_col = cols_lower[taxon_rank.lower()]
        elif chosen_col and chosen_col in df.columns:
            # keep chosen_col if it exists
            pass
        else:
            raise KeyError(f"taxon_rank '{taxon_rank}' not found in file columns: {list(df.columns)}")

    # Extract unique non-null values and normalize to lowercase strings
    try:
        vals = df[chosen_col].drop_nulls().unique().to_list()
        target_values = {str(v).lower() for v in vals if v is not None and str(v).strip() != ""}
    except Exception:
        # conservative fallback: iterate rows if the vectorized route fails
        vals = []
        for rec in df.select(chosen_col).to_dicts():
            v = rec.get(chosen_col)
            if v is not None:
                vals.append(v)
        target_values = {str(v).lower() for v in vals if str(v).strip() != ""}

    print("Found", len(target_values), taxon_rank, "values.")
    return target_values

def load_taxon_keys_old(taxa_path, taxa_cols, taxon_rank="order", flag_det_errors=True):
    print("Reading", taxa_path, "extracting", taxon_rank, "values.")
    df = pl.read_csv(taxa_path, separator='\t')  # Changed separator to '\t' for tab-delimited
    target_values = set(
        pl.Series(df.select(taxon_rank).drop_nulls())
        .str.to_lowercase()
        .unique()
        .to_list()
    )
    print("Found", len(target_values), taxon_rank, "values: ")
    #print(target_values)
  
    return target_values


def load_taxon_keys_comma(taxa_path, taxa_cols, taxon_rank="order", flag_det_errors=True):
    """
    Loads taxon keys from a Comma-delimited CSV file into a list.

    Args:
      taxa_path: String. Path to the taxa CSV file.
      taxa_cols: List of strings. Taxonomic columns in taxa CSV to load (default: ["kingdom", "phylum", "class", "order", "family", "genus", "species"]).
      taxon_rank: String. Taxonomic rank to which to classify images (must be present as column in the taxa csv at file_path). Default: "order".
      flag_det_errors: Boolean. Whether to flag holes and smudges blanks (adds "hole" and "background" and "blank" to taxon_keys). Default: True.

    Returns:
      taxon_keys: List. A list of taxon keys to feed to the CustomClassifier for bioCLIP classification.
    """
    print("Reading", taxa_path, "extracting", taxon_rank, "values.")
    df = pl.read_csv(taxa_path)
    target_values = set(
        pl.Series(df.select(taxon_rank).drop_nulls())
        .str.to_lowercase()
        .unique()
        .to_list()
    )
    print("Found", len(target_values), taxon_rank, "values: ")
    #print(target_values)

    return target_values

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



def calculate_rotation_angle(points):
    """Calculates the rotation angle of the rectangle."""
    # Implement a suitable algorithm to calculate the angle based on the points
    # For example, using the slope of the first two points
    p1, p2 = points[:2]
    angle = np.arctan2(p2[1] - p1[1], p2[0] - p1[0]) * 180 / np.pi
    return angle


def rotate_image_to_vertical(image, angle):
    """Rotates an image to vertical orientation based on the given angle."""
    image = image.rotate(-angle, expand=True)
    return image

""" 
#don't use anymore
def crop_rect(
    img, rect, interpolation=cv2.INTER_LINEAR
):  # cv2.INTER_LANCZOS4  cv2.INTER_LINEAR cv2.INTER_CUBIC
    # get the parameter of the small rectangle
    center, size, angle = rect[0], rect[1], rect[2]
    center, size = tuple(map(int, center)), tuple(map(int, size))

    # get row and col num in img
    height, width = img.shape[0], img.shape[1]

    # calculate the rotation matrix
    M = cv2.getRotationMatrix2D(center, angle, 1)
    # rotate the original image
    img_rot = cv2.warpAffine(img, M, (width, height), flags=interpolation)

    # now rotated rectangle becomes vertical, and we crop it
    img_crop = cv2.getRectSubPix(img_rot, size, center)

    return img_crop, img_rot
 """

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

# not sure we use this anymore
def rotate_cropped(img, points):
    # print("shape of cnt: {}".format(points.shape))
    rect = cv2.minAreaRect(points)
    # print("rect: {}".format(rect))

    # the order of the box points: bottom left, top left, top right,
    # bottom right
    box = cv2.boxPoints(rect)
    box = np.int0(box)

    # print("bounding box: {}".format(box))
    cv2.drawContours(img, [box], 0, (0, 0, 255), 2)

    # get width and height of the detected rectangle
    width = int(rect[1][0])
    height = int(rect[1][1])

    src_pts = box.astype("float32")
    # coordinate of the points in box points after the rectangle has been
    # straightened
    dst_pts = np.array(
        [[0, height - 1], [0, 0], [width - 1, 0], [width - 1, height - 1]],
        dtype="float32",
    )

    # the perspective transformation matrix
    M = cv2.getPerspectiveTransform(src_pts, dst_pts)

    # directly warp the rotated rectangle to get the straightened rectangle
    warped = cv2.warpPerspective(img, M, (width, height))
    return warped


def get_rotated_rect_coordinates(json_file):
    """Reads rotated rectangle coordinates from a JSON file and returns them."""
    with open(json_file, "r") as f:
        data = json.load(f)
        coordinates_list = []
        for shape in data["shapes"]:
            if shape["shape_type"] == "rotation":
                points = shape["points"]
                x, y, w, h, angle = extract_rectangle_coordinates(points)
                coordinates_list.append((x, y, w, h, angle))
        return coordinates_list


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


def extract_rectangle_coordinates(points):
    """Extracts rectangle coordinates from a list of points."""
    # Assuming points are in clockwise order (adjust if needed)
    min_x = min(point[0] for point in points)
    min_y = min(point[1] for point in points)
    max_x = max(point[0] for point in points)
    max_y = max(point[1] for point in points)

    width = max_x - min_x
    height = max_y - min_y
    angle = calculate_rotation_angle(points)
    return min_x, min_y, width, height, angle


def calculate_rotation_angle(points):
    """Calculates the rotation angle of the rectangle."""
    # Implement a suitable algorithm to calculate the angle based on the points
    # For example, using the slope of the first two points
    p1, p2 = points[:2]
    angle = np.arctan2(p2[1] - p1[1], p2[0] - p1[0]) * 180 / np.pi
    return angle

#not sure we use this
def rotate_image_around_center(image, angle):
    """Rotates an image around its center by the specified angle."""
    cv_image = np.array(image)

    height, width, _ = cv_image.shape
    center = (width // 2, height // 2)
    M_translate = np.float32([[1, 0, -center[0]], [0, 1, -center[1]]])
    translated_image = cv2.warpAffine(cv_image, M_translate, (width, height))

    rotated_image = cv2.rotate(translated_image, angle=angle)

    M_translate_back = np.float32([[1, 0, center[0]], [0, 1, center[1]]])
    final_image = cv2.warpAffine(rotated_image, M_translate_back, (width, height))
    return final_image


def crop_image(image, x, y, w, h):
    """Crops an image based on the specified coordinates."""
    cropped_image = image.crop((x, y, x + w, y + h))
    return cropped_image

#not sure this is being used
def warp_rotation(img, points):
    # cnt = np.array(points)
    cnt = np.array([[int(x), int(y)] for x, y in points])
    # print("shape of cnt: {}".format(cnt.shape))
    rect = cv2.minAreaRect(cnt)
    # print("rect: {}".format(rect))

    # the order of the box points: bottom left, top left, top right,
    # bottom right
    box = cv2.boxPoints(rect)
    box = np.int0(box)

    # print("bounding box: {}".format(box))
    # cv2.drawContours(img, [box], 0, (0, 0, 255), 2)

    # get width and height of the detected rectangle
    width = int(rect[1][0])
    height = int(rect[1][1])

    src_pts = box.astype("float32")
    # coordinate of the points in box points after the rectangle has been
    # straightened
    dst_pts = np.array(
        [[0, height - 1], [0, 0], [width - 1, 0], [width - 1, height - 1]],
        dtype="float32",
    )

    # the perspective transformation matrix
    M = cv2.getPerspectiveTransform(src_pts, dst_pts)

    # directly warp the rotated rectangle to get the straightened rectangle
    warped = cv2.warpPerspective(img, M, (width, height))
    return warped



def get_bioclip_prediction(img_path, classifier):

    # Run inference
    results = classifier.predict(img_path, rank=TAXONOMIC_RANK_FILTER)
    classifier.predict_classifications_from_list()  # def predict_classifications_from_list(img: Union[PIL.Image.Image, str], cls_ary: List[str], device: Union[str, torch.device] = 'cpu') -> dict[str, float]:
    sorted_results = sorted(results, key=lambda x: x["score"], reverse=True)
    # Get the highest scoring result
    winner = sorted_results[0]
    pred = winner["classification"]

    # Print the winner
    print(f"  This is the winner: {pred} with a score of {winner['score']}")
    return pred


def get_bioclip_prediction_imgpath(img, classifier):
    # create a PIL image array
    images = [img]
    winner = ""
    winnerprob = ""

    img_embeddings = classifier.create_image_features(images)
    for probs in classifier.create_probabilities(img_embeddings, classifier.txt_embeddings):
        topk = probs.topk(k=5)
        index = 0
        for pred in classifier.format_grouped_probs(
            "", probs, rank=TAXONOMIC_RANK_FILTER, min_prob=1e-9, k=5
        ):  # TODO make it so tags get saved for all ranks, and specify deepest rank? #this shows the depth of the order it searches to
            #print(pred)
            if index == 0:
                kingdom = pred["kingdom"]
                #print(str(TAXONOMIC_RANK_FILTER.get_label()))
                winner = pred[
                    str(TAXONOMIC_RANK_FILTER.get_label())
                ]  # get the correct ID based on the deepest order we are searching
                winnerprob = pred["score"]
                winningdict = pred
            index = index + 1

    # Print the winner
    print(f"  This is the winner: {winner} with a score of {winnerprob}")
    return winner, winnerprob, winningdict



def get_bioclip_prediction_PILimg(img, classifier):
    # create a PIL image array
    images = [img]
    winner = ""
    winnerprob = ""

    img_embeddings = classifier.create_image_features(images)
    for probs in classifier.create_probabilities(img_embeddings, classifier.txt_embeddings):
        topk = probs.topk(k=5)
        index = 0
        for pred in classifier.format_grouped_probs(
            "", probs, rank=TAXONOMIC_RANK_FILTER, min_prob=1e-9, k=5
        ):  # TODO make it so tags get saved for all ranks, and specify deepest rank? #this shows the depth of the order it searches to
            #print(pred)
            if index == 0:
                kingdom = pred["kingdom"]
                #print(str(TAXONOMIC_RANK_FILTER.get_label()))
                winner = pred[
                    str(TAXONOMIC_RANK_FILTER.get_label())
                ]  # get the correct ID based on the deepest order we are searching
                winnerprob = pred["score"]
                winningdict = pred
            index = index + 1

    # Print the winner
    print(f"  This is the winner: {winner} with a score of {winnerprob}")
    return winner, winnerprob, winningdict


def update_json_labels_and_scores(json_path, index, pred, conf, winningdict):
    """Updates the "label" and "score" entries for a specific shape in a JSON file.

    Args:
        json_path: The path to the JSON file.
        index: The index of the shape to update (0-based).
        pred: The new label value.
        conf: The new score value.
    """
    # TODO add winningdict here correctly
    with open(json_path, "r") as f:
        data = json.load(f)

    if 0 <= index < len(data["shapes"]):
        shape = data["shapes"][index]
        
        # do stuff here now
        shape["identifier_bot"] = VERSION
        shape["species_list"]= DOI
        shape["timestamp_ID_bot"]=current_timestamp()
        shape["confidence_ID"] = conf



        predstring = str(pred).strip().lower()
        if predstring in ["hole", "background", "wall", "floor", "blank", "sky"]:
            shape["label"] = "ERROR_" + pred
        else:            
            shape["label"] = str(TAXONOMIC_RANK_FILTER).replace("Rank.", "") + "_" + pred

        #shape["description"] = (
        #    VERSION  # Put what Robot did the ID, put "" for human / ground_truth
        #)

        # Add taxonomic ranks only if they exist in the winningdict
        for rank in [
            "kingdom",
            "phylum",
            "class",
            "order",
            "family",
            "genus",
            "species",
        ]:
            if rank in winningdict:
                if winningdict[rank].strip().lower() in ["hole", "background", "wall", "floor", "blank", "sky"]:
                    shape[rank] = "ERROR_" + winningdict[rank]
                else:    
                    shape[rank] = winningdict[rank]

    with open(json_path, "w") as f:
        json.dump(data, f, indent=4)


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


# Patch get_txt_names to always use UTF-8
def fixed_get_txt_names(self):
    txt_names_json = self.get_cached_datafile("embeddings/txt_emb_species.json")
    with open(txt_names_json, encoding="utf-8") as fd:
        return json.load(fd)


def ID_matched_img_json_pairs(
    hu_matched_img_json_pairs,bot_matched_img_json_pairs, taxa_path, taxa_cols, taxon_rank, device, flag_the_det_errors):


    # derive cache filename
    cache_path = os.path.splitext(taxa_path)[0] + ".pt"

    if os.path.exists(cache_path):
        print(f"Loading cached embeddings from {cache_path}")
        cache = torch.load(cache_path, map_location=device)
        TreeOfLifeClassifier.get_txt_names = fixed_get_txt_names # weird patch
        classifier = TreeOfLifeClassifier(device=device)  # still need classifier structure
        classifier.txt_names = cache["txt_names"]
        classifier.txt_embeddings = cache["txt_embeddings"].to(device)
        print("TOL: Loaded number of labels:", len(classifier.txt_names))
        print("TOL: Loaded image embeddings shape:", classifier.txt_embeddings.shape)
        #return classifier

    # ----------------------
    # No cache → build fresh
    # ----------------------
    else:
        # load up the Pybioclip stuff
        taxon_keys_list = load_taxon_keys(
            taxa_path=taxa_path,
            taxa_cols=taxa_cols,
            taxon_rank=taxon_rank.lower(),
            flag_det_errors=flag_the_det_errors,
        )

        target_values = taxon_keys_list


        print("Loading TOL classifier")
        TreeOfLifeClassifier.get_txt_names = fixed_get_txt_names # weird patch to make it not give an undefined character error!  
        classifier = TreeOfLifeClassifier(device=DEVICE) #it used to crash here
        print("TOL: number of labels:", len(classifier.txt_names))
        print("TOL: image embeddings shape:", classifier.txt_embeddings.shape)

        print("Finding embeddings matching the targets.")
        found_items = []
        for i, txt_name in enumerate(classifier.txt_names):
            name_dict = create_classification_dict(txt_name, Rank.SPECIES)
            if name_dict[taxon_rank].lower() in target_values:
                found_items.append((i, txt_name))

        print("Found", len(found_items), "embeddings matching the", taxon_rank, "values")

        print("Building the image embedding tensor")
        txt_feature_ary = []
        new_txt_names = []
        for i, txt_name in found_items:
            txt_feature_ary.append(classifier.txt_embeddings[:, i])
            new_txt_names.append(txt_name)

        print("Creating embeddings for custom labels")
        custom_labels = ["hole", "background", "wall", "floor", "blank", "sky"]
        clc = CustomLabelsClassifier(custom_labels, device=DEVICE)
        for i, label in enumerate(custom_labels):
            txt_feature_ary.append(clc.txt_embeddings[:, i])
            new_txt_names.append([[label, label, label, label, label, "", label], label])

        #HERE TO FIX
        classifier.txt_names = new_txt_names
        classifier.txt_embeddings = torch.stack(txt_feature_ary, dim=1)
        print("TOL: Updated number of labels:", len(classifier.txt_names))
        print("TOL: Updated image embeddings shape:", classifier.txt_embeddings.shape)

        # ----------------------
        # Save cache
        # ----------------------
        print(f"Saving embeddings cache to {cache_path}")
        torch.save({
            "txt_names": classifier.txt_names,
            "txt_embeddings": classifier.txt_embeddings.cpu(),  # save portable CPU tensors
        }, cache_path)


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
                    # print(coordinates)
                    if was_pre_ided_list[idx] and OVERWRITE_EXISTING_IDs==False:  # skip processing if IDed
                        continue

                    patchfullpath=os.path.dirname(image_path)+"/"+ thepatch_list[idx]

                    patchPIL=Image.open(patchfullpath)
                    pred, conf, winningdict = get_bioclip_prediction_imgpath(patchPIL,classifier)

                    # next we can make a copy of the detection json with IDs / or figure out how to ADD the IDs
                    update_json_labels_and_scores(json_path, idx, pred, conf, winningdict)

                    #add path to list of patches for perceptual processing
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
                    # print(coordinates)
                    if was_pre_ided_list[idx] and OVERWRITE_EXISTING_IDs==False:  # skip processing if IDed
                        continue

                    patchfullpath=os.path.dirname(image_path)+"/"+ thepatch_list[idx]
                    


                    patchPIL=Image.open(patchfullpath)
                    pred, conf, winningdict = get_bioclip_prediction_imgpath(patchPIL,classifier)



                    # next we can make a copy of the detection json with IDs / or figure out how to ADD the IDs
                    update_json_labels_and_scores(json_path, idx, pred, conf, winningdict)

                    #add path to list of patches for later perceptual processing
                    patch_paths_bots.append(patchfullpath)
                    json_paths_bots.append(json_path)
                    idx_paths_bots.append(idx)



def extract_doi_from_csv_path(csv_path: str) -> str:
    """
    Extracts the DOI from a filename like:
      SpeciesList_..._doi.org10.15468dl.epzeza.csv
    and returns the full DOI URL.

    Works for any DOI variant formatted as "doi.org10....".
    Returns "no_doi" if no valid DOI is found.
    """
    filename = os.path.basename(csv_path)

    # Try to find the DOI chunk (everything after 'doi.org' up to .csv)
    match = re.search(r"(doi\.org[0-9A-Za-z\.\-]+)", filename)
    if not match:
        return "no_doi"

    doi_raw = match.group(1)  # e.g. "doi.org10.15468dl.epzeza"
    doi_core = doi_raw.replace("doi.org", "")  # e.g. "10.15468dl.epzeza"

    # General DOI rule: starts with "10." and has a slash somewhere
    # Fix by inserting a slash between the prefix and the rest
    m = re.match(r"(10\.\d+)(.+)", doi_core)
    if not m:
        return "no_doi"

    prefix, suffix = m.groups()
    doi_fixed = f"{prefix}/{suffix}"

    return f"https://doi.org/{doi_fixed}"

if __name__ == "__main__":

    """
    First the script takes in a INPUT_PATH

    Then, (to simplify its searching) it looks through all the folders for folders that are just a single "night"
    and follow the date format YYYY-MM-DD for their structure

    in each of these folders, it looks to see if there are any .json

    """

    args = parse_args()
    taxon_filter_num=int(args.rank)
    TAXONOMIC_RANK_FILTER = Rank(taxon_filter_num)
    OVERWRITE_EXISTING_IDs= bool(int(args.overwrite_prev_bot_ID)) #note arg parser can't do booleans, so you need this workaround!
    ID_BOTDETECTIONS=bool(int(args.ID_Bot))
    ID_HUMANDETECTIONS=bool(int(args.ID_Hum))


    # get species list DOI
    
    DOI=extract_doi_from_csv_path(args.taxa_csv)
    
    print("using species list: "+DOI)

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

    # Now that we have our data to be processed in a big list, it's time to load up the Pybioclip stuff
    ID_matched_img_json_pairs(
        hu_matched_img_json_pairs,
        bot_matched_img_json_pairs,
        taxon_rank=args.TOLrank,
        flag_the_det_errors=args.flag_det_errors,
        taxa_path=args.taxa_csv,
        taxa_cols=args.taxa_cols,
        device=DEVICE,
    )

    print("Finished Automatic Identification")
