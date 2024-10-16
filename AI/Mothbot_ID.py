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

from bioclip import CustomLabelsClassifier, Rank
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

import cv2

#import uuid
INPUT_PATH = r"F:\Panama\PEA_PeaPorch_AdeptTurca_2024-09-01"  # raw string
SPECIES_LIST = r"C:\Users\andre\Documents\GitHub\Mothbox\AI\SpeciesList_CountryPanama_TaxaInsecta.csv"

TAXA_COLS = ["kingdom", "phylum", "class", "order", "family", "genus", "species"]

TAXONOMIC_RANK ="order"

def parse_args():
  parser = argparse.ArgumentParser()
  parser.add_argument("--data-path", required = False, default=INPUT_PATH, help = "path to images for classification (ex: datasets/test_images/data)")
  parser.add_argument("--rank", default = TAXONOMIC_RANK, help = "rank to which to classify; must be column in --taxa-csv (default: {TAXONOMIC_RANK})")
  parser.add_argument("--flag-holes", default = True, action = argparse.BooleanOptionalAction, help = "whether to flag holes and smudges (default: --flag-holes)")
  parser.add_argument("--taxa-csv", default = SPECIES_LIST, help = "CSV with taxonomic labels to use for CustomClassifier (default: {SPECIES_LIST})")
  parser.add_argument("--taxa-cols", default = TAXA_COLS, help = f"taxonomic columns in taxa CSV to load (default: {TAXA_COLS})")
  parser.add_argument("--device", required = False, choices = ["cpu", "cuda"], help = "device on which to run pybioblip ('cpu' or 'cuda', default: 'cpu')")
  
  return parser.parse_args()


def load_taxon_keys(taxa_path, taxa_cols, taxon_rank = "order", flag_holes = True):
  '''
  Loads taxon keys from a tab-delimited CSV file into a list.

  Args:
    taxa_path: String. Path to the taxa CSV file.
    taxa_cols: List of strings. Taxonomic columns in taxa CSV to load (default: ["kingdom", "phylum", "class", "order", "family", "genus", "species"]).
    taxon_rank: String. Taxonomic rank to which to classify images (must be present as column in the taxa csv at file_path). Default: "order".
    flag_holes: Boolean. Whether to flag holes and smudges (adds "hole" and "circle" to taxon_keys). Default: True.

  Returns:
    taxon_keys: List. A list of taxon keys to feed to the CustomClassifier for bioCLIP classification.
  '''
  df = pl.read_csv(taxa_path, low_memory = False).select(taxa_cols).filter(pl.col(taxon_rank).is_not_null())
  taxon_keys = pl.Series(df.select(pl.col(taxon_rank)).unique()).to_list()
  
  if flag_holes:
    taxon_keys.append("circle")
    taxon_keys.append("hole")
  
  return taxon_keys


def process_files_in_directory(data_path, classifier, taxon_rank = "order"):
    '''
    Processes files within a specified subdirectory.

    Args:
    data_path: String. The path to the directory containing files.
    classifier: CustomLabelsClassifier object from TAXA_KEYS_CSV.
    taxon_rank: String. Taxonomic rank to which to classify images (must be present as column in the taxa csv at file_path). Default: "order".
    '''

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
        i=1
        for file in img_list:
            filename = os.path.splitext(file)[0]
            #print(filename)
            data = os.path.join(data_path, file)
            print(f"\n img # {str(i)} out of {str(len(img_list))}")
            i=i+1
            
            # Run inference
            results = classifier.predict(data)
            classifier.predict_classifications_from_list() #def predict_classifications_from_list(img: Union[PIL.Image.Image, str], cls_ary: List[str], device: Union[str, torch.device] = 'cpu') -> dict[str, float]:
            sorted_results = sorted(results, key=lambda x: x["score"], reverse=True)
            # Get the highest scoring result
            winner = sorted_results[0]
            pred = winner['classification']

            # Print the winner
            print(filename+f"  This is the winner: {pred} with a score of {winner['score']}")
            key = f"data/{file}"
            if pred in ["hole", "circle"]:
              predictions[key] = f"abiotic_{pred}"
            else:
              predictions[key] = taxon_rank + "_" + pred
    return predictions


def create_json(predictions, json_path):
  """
  Creates a JSON file with the specified structure, containing image filepaths and tags.

  Args:
    predictions: Dictionary with image filepaths as keys and prediction at given rank as values.
    json_path: String. Path to image directory (they must be in a 'data' folder at the lowest level for V51);
        JSON for V51 must be saved in directory containing the data directory.

  Returns:
    None
  """
  samples = []
  #dataset_id = str(uuid.uuid4()) #test and see if it accepts a UUID later! 
  i=0
  for filepath in predictions.keys():
    # revist structure of JSON for V51
    i=i+1
    sample = {
      "_id": i,
      "filepath": filepath,
      "tags": [predictions[filepath]],
      "_media_type": "image",
      "_dataset_id": "2"
    }
    samples.append(sample)

  data = {"samples": samples}
  with open(json_path, "w") as f:
    json.dump(data, f, indent=2)


def get_labels(data_path, taxon_rank = "order", flag_holes = True, taxa_path = "taxa.csv", taxa_cols = TAXA_COLS, device = "cpu"):
  '''
  Generates the list of taxa to predict, loads the CustomLabelsClassifier with that list, then gets the predictions and generates a JSON for V51 interface.
  
  Args:
    data_path: String. The path to the directory containing files.
    taxon_rank: String. Taxonomic rank to which to classify images (must be present as column in the taxa csv at file_path). Default: "order".
    flag_holes: Boolean. Whether to flag holes and smudges (adds "hole" and "circle" to taxon_keys). Default: True.
    taxa_path: String. Path to the taxa CSV file.
    taxa_cols: List of strings. Taxonomic columns in taxa CSV to load (default: ["kingdom", "phylum", "class", "order", "family", "genus", "species"]).
    device: String. Device on which to run pybioclip ('cpu' or 'cuda'). Default: 'cpu'.
  '''
  if "/data" in data_path:
    json_path = f"{data_path.split(sep = '/data')[0]}/samples.json"
  else:
    json_path = os.path.join(data_path, "..", "samples.json")
  taxon_keys_list = load_taxon_keys(taxa_path = taxa_path, taxa_cols = taxa_cols, taxon_rank = taxon_rank.lower(), flag_holes = flag_holes)
  print(f"We are predicting from the following {len(taxon_keys_list)} taxon keys: {taxon_keys_list}")

  print("Loading CustomLabelsClassifier...")
  classifier = CustomLabelsClassifier(taxon_keys_list, device = device)
  predictions = process_files_in_directory(data_path, classifier)
  
  create_json(predictions, json_path)


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

def find_matching_pairs(folder_path):
  """Finds matching pairs of .jpg and .json files in a given folder.

  Args:
    folder_path: The path to the folder to search.

  Returns:
    A list of tuples, where each tuple contains the paths to a matching .jpg and .json file.
  """

  jpg_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.jpg')]
  json_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.json')]

  pairs = []
  for jpg_file in jpg_files:
    json_file = jpg_file.replace('.jpg', '.json')
    if json_file in json_files:
      pairs.append((jpg_file, json_file))

  return pairs




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



def crop_rect(img, rect, interpolation=cv2.INTER_LINEAR): # cv2.INTER_LANCZOS4  cv2.INTER_LINEAR cv2.INTER_CUBIC
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
    print("shape of cnt: {}".format(points.shape))
    rect = cv2.minAreaRect(points)
    print("rect: {}".format(rect))

    # the order of the box points: bottom left, top left, top right,
    # bottom right
    box = cv2.boxPoints(rect)
    box = np.int0(box)

    print("bounding box: {}".format(box))
    cv2.drawContours(img, [box], 0, (0, 0, 255), 2)

    # get width and height of the detected rectangle
    width = int(rect[1][0])
    height = int(rect[1][1])

    src_pts = box.astype("float32")
    # coordinate of the points in box points after the rectangle has been
    # straightened
    dst_pts = np.array([[0, height-1],
                        [0, 0],
                        [width-1, 0],
                        [width-1, height-1]], dtype="float32")

    # the perspective transformation matrix
    M = cv2.getPerspectiveTransform(src_pts, dst_pts)

    # directly warp the rotated rectangle to get the straightened rectangle
    warped = cv2.warpPerspective(img, M, (width, height))
    return warped

def get_rotated_rect_coordinates(json_file):
  """Reads rotated rectangle coordinates from a JSON file and returns them."""
  with open(json_file, 'r') as f:
    data = json.load(f)
    coordinates_list = []
    for shape in data['shapes']:
      if shape['shape_type'] == 'rotation':
        points = shape['points']
        x, y, w, h, angle = extract_rectangle_coordinates(points)
        coordinates_list.append((x, y, w, h, angle))
    return coordinates_list
  

def get_rotated_rect_raw_coordinates(json_file):
  """Reads rotated rectangle coordinates from a JSON file and returns them."""
  with open(json_file, 'r') as f:
    data = json.load(f)
    coordinates_list = []
    for shape in data['shapes']:
      if shape['shape_type'] == 'rotation':
        points = shape['points']
        #x, y, w, h, angle = extract_rectangle_coordinates(points)
        coordinates_list.append(points)
    return coordinates_list
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
    #cnt = np.array(points)
    cnt=np.array([[int(x), int(y)] for x, y in points])
    print("shape of cnt: {}".format(cnt.shape))
    rect = cv2.minAreaRect(cnt)
    print("rect: {}".format(rect))

    # the order of the box points: bottom left, top left, top right,
    # bottom right
    box = cv2.boxPoints(rect)
    box = np.int0(box)

    print("bounding box: {}".format(box))
    #cv2.drawContours(img, [box], 0, (0, 0, 255), 2)

    # get width and height of the detected rectangle
    width = int(rect[1][0])
    height = int(rect[1][1])

    src_pts = box.astype("float32")
    # coordinate of the points in box points after the rectangle has been
    # straightened
    dst_pts = np.array([[0, height-1],
                        [0, 0],
                        [width-1, 0],
                        [width-1, height-1]], dtype="float32")

    # the perspective transformation matrix
    M = cv2.getPerspectiveTransform(src_pts, dst_pts)

    # directly warp the rotated rectangle to get the straightened rectangle
    warped = cv2.warpPerspective(img, M, (width, height))
    return warped

def get_path_from_img_temp(im):
    #im = Image.open(matching_pairs_img_json_detections[0][0])

    with io.BytesIO() as output:
        im.save(output, format='JPEG')
        output.seek(0)
        with tempfile.NamedTemporaryFile(suffix='.jpg') as temp:
            temp.write(output.read())
            temp.seek(0)
            thepath = Path(temp.name)

    print(thepath)


def get_bioclip_prediction(img_path, classifier):
   
  # Run inference
  results = classifier.predict(img_path)
  classifier.predict_classifications_from_list() #def predict_classifications_from_list(img: Union[PIL.Image.Image, str], cls_ary: List[str], device: Union[str, torch.device] = 'cpu') -> dict[str, float]:
  sorted_results = sorted(results, key=lambda x: x["score"], reverse=True)
  # Get the highest scoring result
  winner = sorted_results[0]
  pred = winner['classification']

  # Print the winner
  print(f"  This is the winner: {pred} with a score of {winner['score']}")
  return pred


def process_matched_img_json_pairs(matched_img_json_pairs, taxa_path,taxa_cols,taxon_rank,device, flag_holes):
  #load up the Pybioclip stuff
  taxon_keys_list = load_taxon_keys(taxa_path = taxa_path, taxa_cols = taxa_cols, taxon_rank = taxon_rank.lower(), flag_holes = flag_holes)
  print(f"We are predicting from the following {len(taxon_keys_list)} taxon keys: {taxon_keys_list}")

  print("Loading CustomLabelsClassifier...")
  classifier = CustomLabelsClassifier(taxon_keys_list, device = device)

  # Next process each pair and generate temporary files for the ROI of each detection in each image
  # Iterate through image-JSON pairs
  for image_path, json_path in matching_pairs_img_json_detections:
    # Load JSON file and extract rotated rectangle coordinates for each detection
    
    #coordinates_of_detections_list = get_rotated_rect_coordinates(json_path)
    coordinates_of_detections_list = get_rotated_rect_raw_coordinates(json_path)
    print(len(coordinates_of_detections_list)," detections in "+json_path)
    if coordinates_of_detections_list:
      for coordinates in coordinates_of_detections_list:
        print(coordinates)

        image = Image.open(image_path)
        cv_image = np.array(image)
        cv_image = cv_image[:, :, ::-1]  # Reverse the channels (BGR to RGB)

        cv_image_cropped = warp_rotation(cv_image,coordinates)

        #pil_image = Image.fromarray(cv_image_cropped)
        pil_image = Image.fromarray(cv_image_cropped[:, :, ::-1] )

        #crop_path=get_path_from_img_temp(pil_image)
        # create a PIL image array
        images = [pil_image]

        img_features = classifier.create_image_features(images)
        for probs in classifier.create_probabilities(img_features, classifier.txt_features):
            topk = probs.topk(k=5)
            for i, prob in zip(topk.indices, topk.values):
                print(classifier.classes[i], prob.item())
        """#From John at Bioclip
        # create a PIL image array
        pil_image_ar=[pil_image]
        img_features = classifier.create_image_features(pil_image_ar)
        idx = 0
        for probs in classifier.create_probabilities(img_features, classifier.txt_features):
            name = f"image{idx}"
            for pred in classifier.format_species_probs(None, probs, k=5):
                print(pred['species'], pred['common_name'], pred['score'])
            idx += 1"""
        

        """ #Temp directory style
        # Define a temporary directory with write permissions (adjust as needed)
        temp_dir = os.path.join(os.environ['TEMP'], 'my_temp_dir')
        os.makedirs(temp_dir, exist_ok=True)  # Create the directory if it doesn't exist
        temp_dir=INPUT_PATH
        with tempfile.NamedTemporaryFile(suffix='.jpg', dir=temp_dir, delete=False) as temp:
            pil_image.save(temp, format='JPEG')
            #temp.write(output.read())
            temp.seek(0)
            thepath = Path(temp.name)          
            crop_path=thepath
            
            print(crop_path)

            # Run inference
            results = classifier.predict(r""+str(crop_path))
            #classifier.predict_classifications_from_list() #def predict_classifications_from_list(img: Union[PIL.Image.Image, str], cls_ary: List[str], device: Union[str, torch.device] = 'cpu') -> dict[str, float]:
            sorted_results = sorted(results, key=lambda x: x["score"], reverse=True)
            print(sorted_results)
            # Get the highest scoring result
            winner = sorted_results[0]
            pred = winner['classification']

            # Print the winner
            print(f"  This is the winner: {pred} with a score of {winner['score']}")

          """

        #prediction = get_bioclip_prediction(crop_path, classifier) 
        
        #print(prediction)
        # Display the cropped image using OpenCV
        cv2.imshow("Cropped Image", cv_image_cropped)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        # Manually delete the temporary file
        #os.remove(crop_path)
  # Then feed this list of ROIs to pybioclip




if __name__ == "__main__":
  
  """
  First the script takes in a INPUT_PATH

  Then, (to simplify its searching) it looks through all the folders for folders that are just a single "night"
  and follow the date format YYYY-MM-DD for their structure

  in each of these folders, it looks to see if there are any .json
  
  """

  
  args = parse_args()

  #Find all the dated folders that our data lives in
  print("Looking in this folder for MothboxData: "+ args.data_path)
  date_folders = find_date_folders(args.data_path)
  print("Found ",str(len(date_folders))+" dated folders potentially full of mothbox data")

  # Look in each dated folder for .json detection files and the matching .jpgs
  matching_pairs_img_json_detections=[]

  for folder in date_folders:
    list_of_pairs=find_matching_pairs(folder)
    matching_pairs_img_json_detections=update_main_list(matching_pairs_img_json_detections, list_of_pairs)

  print("Found ",str(len(matching_pairs_img_json_detections))+" pairs of images and detection data to try to ID")
  #Example Pair
  print(matching_pairs_img_json_detections[0])

  # Now that we have our data to be processed in a big list, it's time to load up the Pybioclip stuff
  process_matched_img_json_pairs(matching_pairs_img_json_detections, taxon_rank = args.rank,
             flag_holes = args.flag_holes,
             taxa_path = args.taxa_csv,
             taxa_cols = args.taxa_cols,
             device = "cuda")



  








"""
  get_labels(data_path=args.data_path,
             taxon_rank = args.rank,
             flag_holes = args.flag_holes,
             taxa_path = args.taxa_csv,
             taxa_cols = args.taxa_cols,
             device = "cuda")

"""


'''
classifier = CustomLabelsClassifier(["insect", "hole"])
predictions = classifier.predict("example_moth.jpg")
for prediction in predictions:
   print(prediction["classification"], prediction["score"])
'''
