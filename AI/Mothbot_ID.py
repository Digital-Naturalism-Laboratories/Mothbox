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

import cv2.version
import polars as pl
import os
import sys
import json
import argparse
import re
import tempfile

import io
from pathlib import Path
import numpy as np
from PIL import Image
from PIL import ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = (
    True  # makes ok for use images that are messed up slightly
)

import cv2
import torch
import json
import PIL.Image
import polars as pl
import numpy as np
from bioclip import TreeOfLifeClassifier, Rank, CustomLabelsClassifier
from bioclip.predict import create_classification_dict

# ~~~~Variables to Change~~~~~~~
INPUT_PATH = r"/Volumes/Mothbox C/Deployments/Indonesia/Les_WilanForestEdge_EfectoMinla_2025-07-01"

SPECIES_LIST = r"SpeciesList_CountryIndonesia_TaxaInsecta.csv"  # downloaded from GBIF for example just insects in panama: https://www.gbif.org/occurrence/taxonomy?country=PA&taxon_key=212

""" KINGDOM = 0
    PHYLUM = 1
    CLASS = 2
    ORDER = 3
    FAMILY = 4
    GENUS = 5
    SPECIES = 6"""

TAXONOMIC_RANK_FILTER_num = 3 #!!! change this number to change the taxonomic rank we filter with. IE filter to order with "3" or filter to genus with "5"
ID_HUMANDETECTIONS = True
ID_BOTDETECTIONS = True
# you can See if a json file has an existing ID by looking at "description": "ID_BioCLIP"
OVERWRITE_EXISTING_IDs = True #True

# ~~~~Other Global Variables~~~~~~~

TAXA_COLS = ["kingdom", "phylum", "class", "order", "family", "genus", "species"]
TAXONOMIC_RANK_FILTER = Rank.ORDER
TOL_TAXONOMIC_RANK = "species"  # Change this to "species" to target just the species in your CSV # Note i think this is actually just always needs to be set for SPECIES for this exampple
DOMAIN = "Eukarya"  # basically our "creature" tag? figure we will never see a prokaryote on the mothbox # Also i think GBIF has a "Biota" category that is a fancier version of "creature" or "life"
taxa_path = SPECIES_LIST

# Paths to save filtered list of embeddings/labels
image_embeddings_path = INPUT_PATH + "/image_embeddings.npy"
embedding_labels_path = INPUT_PATH + "/embedding_labels.json"


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data-path",
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
        "--taxa-csv",
        default=SPECIES_LIST,
        help="CSV with taxonomic labels to use for CustomClassifier (default: {SPECIES_LIST})",
    )
    parser.add_argument(
        "--taxa-cols",
        default=TAXA_COLS,
        help=f"taxonomic columns in taxa CSV to load (default: {TAXA_COLS})",
    )
    parser.add_argument(
        "--device",
        required=False,
        choices=["cpu", "cuda"],
        help="device on which to run pybioblip ('cpu' or 'cuda', default: 'cpu')",
    )

    return parser.parse_args()


def load_taxon_keys(taxa_path, taxa_cols, taxon_rank="order", flag_det_errors=True):
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
      flag_det_errors: Boolean. Whether to flag holes and smudges blanks (adds "hole" and "circle" and "background" and "blank" to taxon_keys). Default: True.

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
            if pred in ["hole", "circle", "background", "wall", "floor", "blank", "sky"]:
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
                if (
                    shape["description"] != ""
                ):  # detect if there's been an identification (if so it would say something like IDbyBIOCLIP)
                    pre_ided = True
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


def get_path_from_img_temp(im):
    # im = Image.open(matching_pairs_img_json_detections[0][0])

    with io.BytesIO() as output:
        im.save(output, format="JPEG")
        output.seek(0)
        with tempfile.NamedTemporaryFile(suffix=".jpg") as temp:
            temp.write(output.read())
            temp.seek(0)
            thepath = Path(temp.name)

    print(thepath)


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
        shape["label"] = str(TAXONOMIC_RANK_FILTER).replace("Rank.", "") + "_" + pred
        shape["score"] = conf
        shape["description"] = (
            "ID_BioCLIP"  # Put what Robot did the ID, put "" for human / ground_truth
        )

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


def ID_matched_img_json_pairs(
    hu_matched_img_json_pairs,bot_matched_img_json_pairs, taxa_path, taxa_cols, taxon_rank, device, flag_the_det_errors
):
    # load up the Pybioclip stuff
    taxon_keys_list = load_taxon_keys(
        taxa_path=taxa_path,
        taxa_cols=taxa_cols,
        taxon_rank=taxon_rank.lower(),
        flag_det_errors=flag_the_det_errors,
    )
    target_values = taxon_keys_list
    print(
        #f"We are predicting from the following {len(taxon_keys_list)} taxon keys: {taxon_keys_list}"
    )

    print("Loading TOL classifier")
    classifier = TreeOfLifeClassifier()
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
    custom_labels = ["hole", "circle", "background", "wall", "floor", "blank", "sky"]
    clc = CustomLabelsClassifier(custom_labels)
    for i, label in enumerate(custom_labels):
        txt_feature_ary.append(clc.txt_embeddings[:, i])
        new_txt_names.append([[label, label, label, label, label, "", label], label])

    classifier.txt_names = new_txt_names
    classifier.txt_embeddings = torch.stack(txt_feature_ary, dim=1)
    print("TOL: Updated number of labels:", len(classifier.txt_names))
    print("TOL: Updated image embeddings shape:", classifier.txt_embeddings.shape)

    #Process Human Detections
    print("processing Human Detections.........")
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

                    #Use thumbnails now, so don't need to crop every image fresh
                    """image = Image.open(image_path)
                    cv_image = np.array(image)

                    cv_image_cropped = warp_rotation(cv_image, coordinates)

                    # pil_image = Image.fromarray(cv_image_cropped)
                    pil_image = Image.fromarray(
                        cv_image_cropped[:, :, ::-1]
                    )  # numpy images are inverted

                    pred, conf, winningdict = get_bioclip_prediction_PILimg(
                        pil_image, classifier
                    )
                    """
                    patchfullpath=os.path.dirname(image_path)+"/"+ thepatch_list[idx]
                    patchPIL=Image.open(patchfullpath)
                    pred, conf, winningdict = get_bioclip_prediction_imgpath(patchPIL,classifier)

                    # next we can make a copy of the detection json with IDs / or figure out how to ADD the IDs
                    update_json_labels_and_scores(json_path, idx, pred, conf, winningdict)

    #Process BOT Detections
    print("processing BOT Detections.........")

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
                    #Use thumbnails now, so don't need to crop every image fresh
                    """image = Image.open(image_path)
                    cv_image = np.array(image)

                    cv_image_cropped = warp_rotation(cv_image, coordinates)

                    # pil_image = Image.fromarray(cv_image_cropped)
                    pil_image = Image.fromarray(
                        cv_image_cropped[:, :, ::-1]
                    )  # numpy images are inverted

                    pred, conf, winningdict = get_bioclip_prediction_PILimg(
                        pil_image, classifier
                    )
                    """
                    patchfullpath=os.path.dirname(image_path)+"/"+ thepatch_list[idx]
                    patchPIL=Image.open(patchfullpath)
                    pred, conf, winningdict = get_bioclip_prediction_imgpath(patchPIL,classifier)



                    # next we can make a copy of the detection json with IDs / or figure out how to ADD the IDs
                    update_json_labels_and_scores(json_path, idx, pred, conf, winningdict)



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
    # Find all the dated folders that our data lives in
    print("Looking in this folder for MothboxData: " + args.data_path)
    date_folders = find_date_folders(args.data_path)
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
    if(len(hu_matched_img_json_pairs)>0):
        print(hu_matched_img_json_pairs[0])
  
    print(
        "Found ",
        str(len(bot_matched_img_json_pairs))
        + " pairs of images and BOT detection data to try to ID",
    )
    # Example Pair
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
        device="cuda",
    )

    print("Finished Automatic Identification")
