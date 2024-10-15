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

from bioclip import CustomLabelsClassifier
import polars as pl
import os
import sys
import json
import argparse
#import uuid

TAXA_COLS = ["kingdom", "phylum", "class", "order", "family", "genus", "species"]
INPUT_PATH = r"C:\Users\andre\Desktop\Mothbox data\PEA_PeaPorch_AdeptTurca_2024-09-01"  # raw string


def parse_args():
  parser = argparse.ArgumentParser()
  parser.add_argument("--data-path", required = False, help = "path to images for classification (ex: datasets/test_images/data)")
  parser.add_argument("--rank", default = "order", help = "rank to which to classify; must be column in --taxa-csv (default: order)")
  parser.add_argument("--flag-holes", default = True, action = argparse.BooleanOptionalAction, help = "whether to flag holes and smudges (default: --flag-holes)")
  parser.add_argument("--taxa-csv", default = "taxa.csv", help = "CSV with taxonomic labels to use for CustomClassifier (default: taxa.csv)")
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


if __name__ == "__main__":
  
  """
  First the script takes in a INPUT_PATH

  Then, (to simplify its searching) it looks through all the folders for folders that are just a single "night"
  and follow the date format YYYY-MM-DD for their structure

  in each of these folders, it looks to see if there are any
  
  """
  
  
  
  
  
  args = parse_args()
  get_labels(data_path = r"D:\Mothbox Photos to Backup\Totumas_Lamp_Liftalce_2024-09-03\2024-09-03\detected_and_cropped_images",
             taxon_rank = args.rank,
             flag_holes = args.flag_holes,
             taxa_path = args.taxa_csv,
             taxa_cols = args.taxa_cols,
             device = "cpu")

'''
classifier = CustomLabelsClassifier(["insect", "hole"])
predictions = classifier.predict("example_moth.jpg")
for prediction in predictions:
   print(prediction["classification"], prediction["score"])
'''
