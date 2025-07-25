#!/usr/bin/env python3

import os
import json
import fiftyone as fo
import fiftyone.utils.image as foui

from hashlib import md5
from pathlib import Path
import numpy as np
from fiftyone.utils.patches import extract_patch
from PIL import Image
import fiftyone.core.labels as fol
import csv
from datetime import datetime
import re

import piexif
#import naturtag
#from naturtag import tag_images
#import exiv2
import subprocess
import threading


import platform
#platform.system() # ' ' 'Linux'

# Import the function from json_to_csv_converter.py
from Mothbot_ConvertDatasettoCSV import json_to_csv

<<<<<<< Updated upstream
INPUT_PATH = r"/Volumes/Mothbox C/Deployments/Indonesia/Indonesia_Les_WilanFirstHilltree_cuervoCinife_2025-06-25/2025-06-25"
METADATA_PATH=r'/Users/brianna/Desktop/Auto Calculations - Mothbox Main Metadata field sheet (Bilingue) (Responses) - Form responses 1.csv'
UTC_OFFSET= 8 #Panama is -5, change for different locations

TAXA_LIST_PATH = r"SpeciesList_CountryIndonesia_TaxaInsecta.csv" #ce/taxonomy?country=PA&taxon_key=212
=======
INPUT_PATH = r"F:\MothboxData_Hubert\data\Panama\Azuero_EcoVenaoAZ018_calmoBarbo_2025-04-11\2025-04-11\ID_HS_OrderLevel"
METADATA_PATH = r'F:\MothboxData_Hubert\mothbox_metadata.csv'
UTC_OFFSET= -5 #Panama is -5, change for different locations

TAXA_LIST_PATH = r"c:\Users\Hubert\Desktop\Biodiversity Monitoring\MothBox\Mothbox Github\Mothbox\AI\SpeciesList_CountryPanama_TaxaInsecta.csv" # downloaded from GBIF for example just insects in panama: https://www.gbif.org/occurrence/taxonomy?country=PA&taxon_key=212
>>>>>>> Stashed changes

SKIP_EXISTING_THUMBNAIL_PATCHES=True  # If false, this will redo the 

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def find_image_json_pairs(input_dir):
  """Finds pairs of image and JSON files with the same name in a given directory.

  Args:
    input_dir: The directory to search for files.

  Returns:
    A list of tuples, where each tuple contains the paths to the image and JSON files.
  """

  image_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.jpg') or f.lower().endswith('.png')]
  json_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.json')]

  pairs = []
  for image_file in image_files:
    json_file = image_file[:-4] + '.json'
    if json_file in json_files:
      pairs.append((os.path.join(input_dir, image_file), os.path.join(input_dir, json_file)))

  return pairs


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
    df = pl.read_csv(taxa_path, separator='\t')
    target_values = set(
        pl.Series(df.select(taxon_rank).drop_nulls())
        .str.to_lowercase()
        .unique()
        .to_list()
    )
    print("Found", len(target_values), taxon_rank, "values: ")
    #print(target_values)

    return target_values





def find_csv_match(input_path, metadata_path):
    """
    Finds a matching row in the CSV metadata file based on parsed components from the input path.

    Args:
        input_path (str): Path to the folder containing the data.
        metadata_path (str): Path to the CSV metadata file.

    Returns:
        dict: A dictionary containing the matching row, or an empty dict if no match is found.
    """
    parent_folder = os.path.basename(os.path.dirname(input_path))
    parts = parent_folder.split("_")
    if len(parts) == 4:
        pass  # Use all parts, no action needed
    elif len(parts) == 5:  # Handle more than four parts (e.g., five or six)
        parts = parts[1:]  # Discard the first part and keep the rest
    else:  # Fewer than four parts case remains unchanged in your original logic
        raise ValueError("The input path does not contain the expected minimum of 4 parts.")
    # Assign the parts to their respective semantic names and normalize them
    area, point, mothbox, deployment_date = [part.strip().lower() for part in parts]
    print("looking for metadata for:")
    print(area+"_"+point+"_"+mothbox+"_"+deployment_date)

    # Read the CSV file and search for a matching row
    with open(metadata_path, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            # Normalize CSV values
            row_area = row.get("area", "").strip().lower()
            row_point = row.get("point", "").strip().lower()
            row_mothbox = row.get("mothbox", "").strip().lower()
            row_deployment_date = row.get("deployment.date", "").strip()

            # Convert deployment date format from DD/MM/YYYY to YYYY-MM-DD
            try:
                formatted_date = datetime.strptime(row_deployment_date, "%d/%m/%Y").strftime("%Y-%m-%d")
            except ValueError:
                continue

            # Check if all components match
            if (row_area == area and
                row_point == point and
                row_mothbox == mothbox and
                formatted_date == deployment_date):
                print("found metadata!")
                return row

    # Return an empty dictionary if no match is found
    print("No metadata found")
    return {}



def load_anylabeling_data(json_path): #TODO load METADATA STRAIGHT FROM CSV - METADATA_PATH - Maybe metadata gets loaded into its own 51 thing via the WHOLe dataset?
  
  """Loads data from an AnyLabeling JSON file.

  Args:
    json_path: The path to the JSON file.

  Returns:
    A dictionary containing the loaded data.
  """

  with open(json_path, 'r') as f:
    data = json.load(f)

  image_height = data['imageHeight']
  image_width = data['imageWidth']
  creator=""
  if(data['version'].startswith("Mothbot")):
     detectionBy= data['version']
  else:
     detectionBy="HumanDetection"
  
  # Extract relevant data from the detection labels
  labels = data['shapes']
  
  # Step 2: Initialize an empty dictionary to store metadata
  #Skip metadata for now
  metadata = {}


  
  return labels, image_height, image_width, metadata, detectionBy


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



def write_taxonomy_with_exiv2_cli(image_path, taxonomic_list):
    """
    Writes iNaturalist-readable taxonomy tags to an image using the exiv2 CLI.
    """
    tags = []
    for entry in taxonomic_list:
        if "_" in entry:
            level, value = entry.split("_", 1)
            tag = f"taxonomy:{level.lower()}={value}"
            # Add tag to both dc:subject and MicrosoftPhoto LastKeywordXMP
            tags.append(f"-M\"set Xmp.dc.subject {tag}\"")
            tags.append(f"-M\"set Xmp.MicrosoftPhoto.LastKeywordXMP {tag}\"")

    # Combine the command
    command = ["exiv2"] + tags + [image_path]

    try:
        result = subprocess.run(" ".join(command), shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Tags written to {image_path}")
        else:
            print(f"❌ exiv2 failed:\n{result.stderr}")
    except FileNotFoundError:
        print("❌ exiv2 CLI tool not found. Make sure it's installed and in your system PATH.")


def add_taxonomy_subject_and_tags_exiv2(image_path, output_path, taxonomic_list):
    """
    Adds taxonomy information to a photo's EXIF/XMP data using exiv2,
    targeting fields iNaturalist is known to recognize.

    Args:
        image_path (str): Path to the input image file.
        output_path (str): Path where the modified image will be saved.
        taxonomic_list (list): A list of taxonomy strings like "Kingdom_Animalia".
    """
    # Step 1: Build semicolon-separated taxonomy string for XMP/IPTC Keywords/Subject
    subject_keywords = []
    for item in taxonomic_list:
        if "_" in item:
            level, value = item.split("_", 1)
            # iNaturalist often just looks for the raw scientific name in keywords,
            # but including the "taxonomy:level=" format is good for general use.
            # Let's add both for good measure, or just the value.
            # For iNaturalist, a simple list of names (e.g., "Homo sapiens; Chordata")
            # in Subject/Keywords is often sufficient.
            subject_keywords.append(value.replace("_", " ")) # Space for readability
            subject_keywords.append(f"taxonomy:{level.lower()}={value.replace('_', ' ')}")

    # Make sure we have unique values and join them
    unique_subject_keywords = sorted(list(set(subject_keywords)))
    keywords_str = ";".join(unique_subject_keywords)

    # For the XMP dc:title, iNaturalist often picks the most specific taxon
    # or the full scientific name (Genus species) if available.
    # Let's try to get the species if present, otherwise the lowest rank.
    dc_title = ""
    species_found = False
    for item in reversed(taxonomic_list): # Iterate in reverse to get most specific
        if "Species_" in item:
            dc_title = item.split("Species_", 1)[1].replace("_", " ")
            species_found = True
            break
        elif "_" in item and not dc_title: # If no species, take the lowest rank
            dc_title = item.split("_", 1)[1].replace("_", " ")
    
    if not dc_title and taxonomic_list: # Fallback if no specific rank found
        dc_title = taxonomic_list[-1].split("_", 1)[1].replace("_", " ")

    # Step 2: Open image with exiv2
    try:
        image = exiv2.ImageFactory.open(image_path)
        image.readMetadata()

        # Get existing metadata if any
        exif_data = image.exifData()
        iptc_data = image.iptcData()
        xmp_data = image.xmpData()

        # Step 3: Set EXIF/XMP/IPTC tags
        # iNaturalist specifically mentions looking at Subject tags (which map to XMP/IPTC Keywords)
        # and dc:title (XMP Title). UserComment is also checked.

        # XMP Subject (often used for keywords/tags)
        # exiv2 treats XMP arrays as lists directly
        # First, clear existing Subject array if we're replacing
        if 'Xmp.dc.subject' in xmp_data:
            del xmp_data['Xmp.dc.subject']
        # Add new subjects (keywords)
        for keyword in unique_subject_keywords:
            xmp_data.add('Xmp.dc.subject', keyword)
        print(f"Set Xmp.dc.subject: {unique_subject_keywords}")

        # IPTC Keywords (also often used for tags, syncs with XMP Subject)
        # IPTC keywords are typically multi-string.
        # Clear existing keywords if we're replacing
        if 'Iptc.Application2.Keywords' in iptc_data:
            del iptc_data['Iptc.Application2.Keywords']
        for keyword in unique_subject_keywords:
            iptc_data.add('Iptc.Application2.Keywords', keyword)
        print(f"Set Iptc.Application2.Keywords: {unique_subject_keywords}")


        # XMP dc:title (Title of the image, iNaturalist can parse this for taxon)
        if dc_title:
            xmp_data['Xmp.dc.title'] = dc_title
            print(f"Set Xmp.dc.title: {dc_title}")

        # UserComment (EXIF, more general notes)
        # exiv2 handles encoding for UserComment. Just provide the string.
        # The ASCII\x00\x00\x00 prefix is often managed by the library.
        exif_data['Exif.Photo.UserComment'] = taxonomy_str
        print(f"Set Exif.Photo.UserComment: {taxonomy_str}")

        # --- Ensure common EXIF tags are present (optional, but good practice) ---
        # iNaturalist often checks for DateTimeOriginal for observation date.
        # If it's missing, add current timestamp.
        if 'Exif.Photo.DateTimeOriginal' not in exif_data:
            now = datetime.datetime.now().strftime("%Y:%m:%d %H:%M:%S")
            exif_data['Exif.Photo.DateTimeOriginal'] = now
            print(f"Added Exif.Photo.DateTimeOriginal: {now}")
        
        # Ensure Exif.Image.DateTime (also a creation date field)
        if 'Exif.Image.DateTime' not in exif_data:
            now = datetime.datetime.now().strftime("%Y:%m:%d %H:%M:%S")
            exif_data['Exif.Image.DateTime'] = now
            print(f"Added Exif.Image.DateTime: {now}")

        # Step 4: Write metadata back to the image
        image.setExifData(exif_data)
        image.setIptcData(iptc_data)
        image.setXmpData(xmp_data)
        image.writeMetadata(output_path)
        print(f"Metadata written to: {output_path}")

    except exiv2.Exiv2Error as e:
        print(f"Exiv2 error: {e}")
    except FileNotFoundError:
        print(f"Error: Image not found at {image_path}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def add_taxonomy_subject_and_tags(image_path, output_path, taxonomic_list):
    # Step 1: Build semicolon-separated taxonomy string
    exif_subject = []
    for item in taxonomic_list:
        if "_" in item:
            level, value = item.split("_", 1)
            tag = f"taxonomy:{level.lower()}={value}"
            exif_subject.append(tag)
    
    taxonomy_str = ";".join(exif_subject)  # For all EXIF fields
    # taxonomy_str=taxonomy_str+";nothing"
    # Step 2: Load image and EXIF
    img = Image.open(image_path)
    exif_bytes = img.info.get("exif")
    if exif_bytes:
        exif_dict = piexif.load(exif_bytes)
    else:
        exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "thumbnail": None}

    # Step 3: Encode XP fields in UTF-16LE with null terminator
    def encode_xp(value):
        return value.encode("utf-16le") + b'\x00\x00'

    encoded_taxonomy = encode_xp(taxonomy_str)

    # Step 4: Write to XPSubject and XPKeywords
    exif_dict["0th"][piexif.ImageIFD.XPSubject] = encoded_taxonomy
    exif_dict["0th"][piexif.ImageIFD.XPKeywords] = encoded_taxonomy

    # Optional: still set UserComment (as plain UTF-8)
    user_comment_bytes = b"ASCII\x00\x00\x00" + taxonomy_str.encode("utf-8")
    exif_dict["Exif"][piexif.ExifIFD.UserComment] = user_comment_bytes

    # Step 5: Save the updated image
    exif_bytes = piexif.dump(exif_dict)
    img.save(output_path, exif=exif_bytes)
    print(f"Saved taxonomy (semicolon-separated) to Subject and Tags: {output_path}")






def write_taxonomy_with_naturtag_old(image_path, taxonomic_list, include_common_names=False):
    """
    Writes taxonomy tags into image EXIF/XMP metadata using naturtag.

    - image_path: path to the JPEG to tag
    - taxonomic_list: list like ['KINGDOM_Animalia', 'PHYLUM_Arthropoda', ...]
    - include_common_names: whether to add any common-name tags (usually False)
    """
    # Build structured taxonomy keywords
    keywords = []
    for entry in taxonomic_list:
        if "_" in entry:
            level, val = entry.split("_", 1)
            keywords.append(f"taxonomy:{level.lower()}={val}")

    # Call tag_images correctly, passing keywords to the proper parameter
    tag_images(
        image_path,
        keywords=keywords,               # custom taxonomy tags
        common_names=include_common_names,
        create_xmp=True                  # ensures XMP metadata is embedded
    )
    print(f"✅ Taxonomy tags written using naturtag to: {image_path}")


def write_taxonomy_with_naturtag(image_path, taxonomic_list, include_common_names=False):
    # Construct taxonomy keywords
    keywords = []
    for entry in taxonomic_list:
        if "_" in entry:
            level, val = entry.split("_", 1)
            keywords.append(f"taxonomy:{level.lower()}={val}")

    # Wrap call to catch warnings or recover
    try:
        tag_images(
            image_path,
            keywords=keywords,
            common_names=include_common_names,
            create_xmp=True  # ensures proper XMP embedding
        )
        print(f"✅ Successfully tagged: {image_path}")
    except Exception as e:
        print(f"❗ naturtag failed with error:\n{e}")
        print("➡️ Attempting fallback: writing only EXIF tags via piexif")

        # Fallback: write EXIF XP fields only
        import piexif
        from PIL import Image

        def encode_xp(val):
            return val.encode("utf-16le") + b'\x00\x00'

        taxonomy_str = ";".join(keywords)
        img = Image.open(image_path)
        exif_bytes = img.info.get("exif")
        exif_dict = piexif.load(exif_bytes) if exif_bytes else {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "thumbnail": None}

        exif_dict["0th"][piexif.ImageIFD.XPSubject] = encode_xp(taxonomy_str)
        exif_dict["0th"][piexif.ImageIFD.XPKeywords] = encode_xp(taxonomy_str)
        img.save(image_path, exif=piexif.dump(exif_dict))
        print("✅ Fallback EXIF tags written")


class ExifToolSession:
    exifPath="exiftool" #mac or linux
    if(platform.system()=='Windows'):
        exifPath="exiftool-13.32_64/exiftool"
    def __init__(self, exiftool_path=exifPath): 
        self.process = subprocess.Popen(
            [exiftool_path, "-stay_open", "True", "-@", "-"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1  # line-buffered
        )

        # Start a background thread to drain stderr
        self.stderr_output = []
        self.stderr_thread = threading.Thread(target=self._drain_stderr, daemon=True)
        self.stderr_thread.start()

    def _drain_stderr(self):
        for line in self.process.stderr:
            self.stderr_output.append(line.strip())

    def add_taxonomy_with_exiftool(self, full_patch_path, taxonomic_list):
        args = []

        # 1. Format taxonomy tags
        for entry in taxonomic_list:
            if "_" in entry:
                level, value = entry.split("_", 1)
                tag = f"taxonomy:{level.lower()}={value}"
                args.append(f"-XMP-dc:Subject+={tag}")
                args.append(f"-XMP-MicrosoftPhoto:LastKeywordXMP+={tag}")

        # 2. Extract datetime from filename
        filename = Path(full_patch_path).name
        match = re.search(r"_(\d{4})_(\d{2})_(\d{2})__?(\d{2})_(\d{2})_(\d{2})", filename)
        if match:
            y, m, d, h, mi, s = match.groups()
            datetime_str = f"{y}:{m}:{d} {h}:{mi}:{s}"
            args.append(f"-DateTimeOriginal={datetime_str}")
            args.append(f"-CreateDate={datetime_str}")
            args.append(f"-ModifyDate={datetime_str}")
        else:
            print(f"⚠️ No datetime found in filename: {filename}")

        # 3. Finalize arguments
        args.extend([
            "-overwrite_original",
            "-fast2",
            str(full_patch_path),
            "-execute\n"
        ])

        # 4. Send to ExifTool
        self.process.stdin.write("\n".join(args))
        self.process.stdin.flush()

        # 5. Drain stdout
        output_lines = []
        while True:
            line = self.process.stdout.readline()
            if not line:
                break
            if line.strip() == "{ready}":
                break
            output_lines.append(line.strip())

        if output_lines:
            print(f"✅  ExifTool output for {full_patch_path}:")
            for line in output_lines:
                print("  ", line)

    def close(self):
        self.process.stdin.write("-stay_open\nFalse\n")
        self.process.stdin.flush()
        self.process.wait()

def create_sample(image_path, labels, image_height, image_width, metadata, detection_creator, tagger):
  """Creates a FiftyOne sample using the 51 python interface

  Args:
    image_path: The path to the image file.
    labels: A list of labels from the AnyLabeling JSON file.
    image_height: The height of the image.
    image_width: The width of the image.

  Returns:
    A FiftyOne JSON sample.
  """

  sample = fo.Sample(
      filepath= image_path,
  )
  
  sample["uploaded"]=metadata.get("uploaded","")
  sample["sd"]=metadata.get("sd.card","")
  sample["mothbox"]=metadata.get("mothbox","")
  sample["software"]=str(metadata.get("software",""))
  sample["sheet"]=metadata.get("sheet","")
  sample["country"]=metadata.get("country","")
  sample["area"]=metadata.get("area","")
  sample["punto"]=metadata.get("point","") #point is maybe a special key name in 51
  
  
  latitude=metadata.get("latitude","")
  longitude=metadata.get("longitude","")
  geolocation = fo.GeoLocation(latitude=latitude, longitude=longitude)
  sample["location"]=geolocation
  sample["longitude"]=longitude
  sample["latitude"]=latitude
  therawgroundheight=metadata.get("height (placement above ground)","")
  sample["ground_height"]= extract_number(therawgroundheight)

  sample["deployment_name"]=metadata.get("deployment.name","")
  sample["deployment_date"]=metadata.get("deployment.date","")
  sample["collect_date"]=metadata.get("collect.date","")
  sample["data_storage_location"]=metadata.get("data.storage.location","")
  sample["crew"]=metadata.get("crew","")
  sample["notes"]=metadata.get("notes","")
  sample["program"]=metadata.get("program","")
  sample["habitat"]=metadata.get("habitat","")
  sample["attractor"]=metadata.get("attractor","")
  sample["attractor_location"]=metadata.get("attractor_location","")

  sample["detection_By"]=detection_creator

  detections_list=[]

  for label in labels:
    direction = label['direction']
    label_name = label['label']
    score = label['score']
    points = label['points']
    shape_type = label['shape_type']
    ID_by = "IDby_"+label['description']
    the_patch_path= label['patch_path']

    desired_keys = ['kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species']


    # Filter the dictionary to include only desired keys
    filtered_dict = {key: value for key, value in label.items() if key in desired_keys}

    # Check for unwanted values
    unwanted_values = {"hole", "circle", "background", "wall", "floor", "blank", "sky"}
    if any(value in unwanted_values for value in filtered_dict.values()):
        taxonomic_list = ["Error"]
    else:
        # Format the filtered dictionary
        taxonomic_list = [f"{key.upper()}_{value}" for key, value in filtered_dict.items()]

    print("adding taxon info to exif "+str(taxonomic_list))
    full_patch_path=Path(INPUT_PATH+"/"+the_patch_path) #should work on mac or windows
    #add_taxonomy_subject_and_tags(full_patch_path, full_patch_path, taxonomic_list)
    #write_taxonomy_with_naturtag(full_patch_path, full_patch_path, taxonomic_list)
    #write_taxonomy_with_naturtag(full_patch_path, taxonomic_list)
    #print(naturtag.metadata.image_metadata.ImageMetadata(image_path=r"c:\Users\andre\Desktop\Dinacon Stuff\test\cuervoCinife_2025_06_30__04_53_06_HDR0_0_Mothbot_yolo11m_4500_imgsz1600_b1_2024-01-18.pt.jpg"))
    #add_taxonomy_subject_and_tags_exiv2(full_patch_path, full_patch_path, taxonomic_list)
    #write_taxonomy_with_exiv2_cli(str(full_patch_path), taxonomic_list)
    tagger.add_taxonomy_with_exiftool(str(full_patch_path), taxonomic_list) #this works but is super slow beacause it opens exif tool every time
    #tagger.add_taxonomy_with_exiftool(full_patch_path, taxonomic_list)
    
    taxonomic_list.append(ID_by)

    if shape_type == 'rotation': #Todo - these should be handled as a polygon in 51, because they only have regular rects they call "Detections" but we have rotated rects (that should be stored as polylines via polyline.fromrotatedboundingbox https://docs.voxel51.com/user_guide/using_datasets.html#rotated-bounding-boxes)
      top, left, width, height = handle_rotation_annotation(points)
      
      #print( top, left, width, height)
      #print("The script will pause now. Press Enter to continue.")
      #input()
      
      # Normalize bounding box coordinates
      top /= image_height
      left /= image_width
      width /= image_width
      height /= image_height
      # Create a FiftyOne detection
      
      detection=fol.Detection(
        tags=taxonomic_list,
        label="creature",
        bounding_box=[left, top, width, height],
        #attributes={},
        #ID_by=ID_by,
        confidence=score,
        shape=shape_type,
        rot_direction=direction,
        patch_path=the_patch_path

      )

      detections_list.append(detection)
    elif shape_type == 'polygon':
      # Handle polygon annotations (adjust as needed)
      None
  #print("num detections")
  #print(len(detections_list))
  sample["creature_detections"] = fol.Detections(detections=detections_list) #TODO - give this an appropriate name

  return sample

def generate_patch_dataset(dataset, output_dir=INPUT_PATH+"/patches", target_size=(1024, -1)):
    """
    Generates thumbnails for images in a FiftyOne dataset, skipping existing ones.

    Args:
        dataset: The FiftyOne dataset.
        output_dir: The directory to save the thumbnails.
        target_size: The target size for the thumbnails (width, height).

    Returns:
        None
    """
    patch_folder_path=Path(INPUT_PATH+"/patches")
    patch_folder_path.mkdir(parents=True, exist_ok=True)

    
    samples_to_process = []
    patch_samples = []

    for sample in dataset.iter_samples(progress=True):
        filename = os.path.basename(sample.filepath) #this is just the basename that it stores!
        sample_fullpath=INPUT_PATH+"/"+filename

        print(sample.filename)


        #print(sample)
        detections= sample.creature_detections.detections
        detector=sample.detection_By
        detnum=0

        for detection in detections:
            patchfullpath=INPUT_PATH+"/"+detection.patch_path
            inferred_patchfilename=filename.split('.')[0] + "_" + str(detnum) +"_"+detector+ "." +filename.split('.')[1]
            inferred_patchfullpath = Path(patch_folder_path) / f'{inferred_patchfilename}' 
            #export_image(patch, patch_path,filename, detnum)

            # Extract coordinates
            xmin, ymin, xmax, ymax = detection.bounding_box

            # Calculate width and height
            p_width = xmax - xmin
            p_height = ymax - ymin
            
            patch_sample = fo.Sample(
                #filepath_fullimage= sample.filepath, 
                filepath_fullimage=sample_fullpath,
                filepath = str(patchfullpath),
                tags= detection.tags,
                label="detection",
                location=sample.location,
                longitude=sample.longitude,
                latitude=sample.latitude,
                bounding_box=detection.bounding_box,
                patch_width=p_width,
                patch_height=p_height,
                #attributes={},
                #ID_by=detection.ID_by,
                confidence=detection.confidence,
                shape=detection.shape,
                direction=detection.rot_direction,
                #direction = sample.direction,
                #label_name = label['label']
                
                uploaded=sample.uploaded,

                mothbox=sample.mothbox,
                sd=sample.sd, #Dots might be bad in key name
                software=sample.software,
                sheet=sample.sheet,
                country=sample.country,
                area=sample.area,
                punto=sample.punto, #point is maybe a special key name in 51
                ground_height=sample.ground_height,
                deployment_name = sample.deployment_name,
                deployment_date = sample.deployment_date,
                collect_date = sample.collect_date,
                data_storage_location = sample.data_storage_location,
                crew=sample.crew,
                notes=sample.notes,
                program=sample.program,
                habitat=sample.habitat,
                attractor=sample.attractor,
                attractor_location=sample.attractor_location,

                detection_By=sample.detection_By

            )

            #add GPS info to the thumbnail patch
            print("adding GPS to "+patchfullpath)
            add_gps_exif(patchfullpath, patchfullpath,float(sample.latitude), float(sample.longitude))




            patch_samples.append(patch_sample)
            detnum=detnum+1

        #sample.save()

        
    
    patch_ds = fo.Dataset()
    patch_ds.add_samples(patch_samples)

    patch_ds.app_config['media_fields'] = ['filepath', 'filepath_fullimage']
    patch_ds.app_config['grid_media_field'] = 'filepath'
    patch_ds.app_config['modal_media_field'] = 'filepath'
    patch_ds.save()

    dataset.save()
    return patch_ds



def deg_to_dms_rational(deg_float):
    """Convert decimal degrees to degrees, minutes, seconds in rational format"""
    deg = int(deg_float)
    min_float = abs(deg_float - deg) * 60
    minute = int(min_float)
    sec_float = (min_float - minute) * 60
    sec = int(sec_float * 10000)

    return ((abs(deg), 1), (minute, 1), (sec, 10000))

def add_gps_exif(input_path, output_path, lat, lng, altitude=None):
    # Load image
    img = Image.open(input_path)

    # Try to load existing EXIF data, or start fresh
    exif_bytes = img.info.get("exif")
    if exif_bytes:
        exif_dict = piexif.load(exif_bytes)
    else:
        exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "thumbnail": None}

    # Check if GPS data already exists
    gps_existing = exif_dict.get("GPS", {})
    if gps_existing.get(piexif.GPSIFD.GPSLatitude) and gps_existing.get(piexif.GPSIFD.GPSLongitude):
        print("GPS data already exists. No changes made.")
        return
    
    # Create GPS IFD
    gps_ifd = {
        piexif.GPSIFD.GPSLatitudeRef: 'N' if lat >= 0 else 'S',
        piexif.GPSIFD.GPSLatitude: deg_to_dms_rational(lat),
        piexif.GPSIFD.GPSLongitudeRef: 'E' if lng >= 0 else 'W',
        piexif.GPSIFD.GPSLongitude: deg_to_dms_rational(lng),
    }

    if altitude is not None:
        gps_ifd[piexif.GPSIFD.GPSAltitudeRef] = 0 if altitude >= 0 else 1
        gps_ifd[piexif.GPSIFD.GPSAltitude] = (int(abs(altitude * 100)), 100)

    # Inject GPS into EXIF
    exif_dict['GPS'] = gps_ifd
    exif_bytes = piexif.dump(exif_dict)

    # Save the image with new EXIF
    img.save(output_path, exif=exif_bytes)
    print(f"Saved image with GPS data: {output_path}")

def generate_patch_thumbnails_orig(dataset, output_dir=INPUT_PATH+"/patches", target_size=(1024, -1)):
    """
    Generates thumbnails for images in a FiftyOne dataset, skipping existing ones.

    Args:
        dataset: The FiftyOne dataset.
        output_dir: The directory to save the thumbnails.
        target_size: The target size for the thumbnails (width, height).

    Returns:
        None
    """
    patch_folder_path=Path(INPUT_PATH+"/patches")
    patch_folder_path.mkdir(parents=True, exist_ok=True)

    
    samples_to_process = []
    patch_samples = []

    for sample in dataset.iter_samples(progress=True):
        filename = os.path.basename(sample.filepath) #this is just the basename that it stores!
        sample_fullpath=INPUT_PATH+"/"+filename
        #thumbnail_path = f"{output_dir}/{filename}"
        #sample["thumbnail_path"]=thumbnail_path
        patch_path = INPUT_PATH+"/patches"
        print(sample.filename)


        #print(sample)
        detections= sample.creature_detections.detections
        detector=sample.detection_By
        #detector=detector.replace('.pt','')
        #print(detections)
        #print(len(detections))
        #print(dataset.get_field_schema())
        #input("Press Enter to continue...")
        detnum=0

        for detection in detections:
            patchfilename=filename.split('.')[0] + "_" + str(detnum) +"_"+detector+ "." +filename.split('.')[1]
            patchfullpath = Path(patch_folder_path) / f'{patchfilename}' 
            #export_image(patch, patch_path,filename, detnum)


            if not os.path.exists(patchfullpath) and SKIP_EXISTING_THUMBNAIL_PATCHES==False: #skip thumbs already generated unless we specifically target to overwrite them each time
                  # Load the image using PIL and convert it to a NumPy array
              img = Image.open(sample_fullpath)
              
              # Convert the image to a NumPy array for patch extraction
              img_array = np.array(img)
              
              # Extract the patch using your custom function
              patch_array = extract_patch(img_array, detection=detection)
              
              # Convert the extracted patch back to a PIL Image
              patch_image = Image.fromarray(patch_array)
              
              # Save the thumbnail
              patch_image.save(patchfullpath)


            # Extract coordinates
            xmin, ymin, xmax, ymax = detection.bounding_box

            # Calculate width and height
            p_width = xmax - xmin
            p_height = ymax - ymin
            
            patch_sample = fo.Sample(
                #filepath_fullimage= sample.filepath, 
                filepath_fullimage=sample_fullpath,
                filepath = str(patchfullpath),
                tags= detection.tags,
                label="detection",
                location=sample.location,
                longitude=sample.longitude,
                latitude=sample.latitude,
                bounding_box=detection.bounding_box,
                patch_width=p_width,
                patch_height=p_height,
                #attributes={},
                #ID_by=detection.ID_by,
                confidence=detection.confidence,
                shape=detection.shape,
                direction=detection.direction,
                #direction = sample.direction,
                #label_name = label['label']
                
                uploaded=sample.uploaded,

                mothbox=sample.mothbox,
                sd=sample.sd, #Dots might be bad in key name
                software=sample.software,
                sheet=sample.sheet,
                country=sample.country,
                area=sample.area,
                punto=sample.punto, #point is maybe a special key name in 51
                ground_height=sample.ground_height,
                deployment_name = sample.deployment_name,
                deployment_date = sample.deployment_date,
                collect_date = sample.collect_date,
                data_storage_location = sample.data_storage_location,
                crew=sample.crew,
                notes=sample.notes,
                program=sample.program,
                habitat=sample.habitat,
                attractor=sample.attractor,
                attractor_location=sample.attractor_location,

                detection_By=sample.detection_By

            )
            patch_samples.append(patch_sample)
            detnum=detnum+1

        #sample.save()

        
    
    patch_ds = fo.Dataset()
    patch_ds.add_samples(patch_samples)

    patch_ds.app_config['media_fields'] = ['filepath', 'filepath_fullimage']
    patch_ds.app_config['grid_media_field'] = 'filepath'
    patch_ds.app_config['modal_media_field'] = 'filepath'
    patch_ds.save()

    dataset.save()
    return patch_ds



if __name__ == "__main__":
  ### START
  #pairs = find_image_json_pairs(INPUT_PATH)
  hu_pairs, bot_pairs = find_detection_matches(INPUT_PATH)

  samples=[]
  # Iterate through human pairs and load data
  metadata= find_csv_match(INPUT_PATH, METADATA_PATH)

  tagger = ExifToolSession()


  for image_path, json_path in hu_pairs:
    full_image_path = image_path
    labels, image_height, image_width, notmetadata, detection_creator = load_anylabeling_data(json_path)
    sample = create_sample(full_image_path, labels, image_height, image_width, metadata, detection_creator, tagger)
    samples.append(sample)

  for image_path, json_path in bot_pairs:
    full_image_path = image_path
    labels, image_height, image_width, notmetadata, detection_creator = load_anylabeling_data(json_path)
    sample = create_sample(full_image_path, labels, image_height, image_width, metadata, detection_creator, tagger )
    samples.append(sample)

  tagger.close()
  # Create dataset
  dataset = fo.Dataset()

  dataset.add_samples(samples)


  # Generate some thumbnail images
  thepatch_dataset = generate_patch_dataset(dataset)


  # Customize the sidebar configuration
  # Get the default sidebar groups for the dataset
  sidebar_groups = fo.DatasetAppConfig.default_sidebar_groups(thepatch_dataset)

  # Collapse the `tags`, `metadata`, and `primitives` sections by default
  sidebar_groups[0].expanded = True  # tags
  sidebar_groups[1].expanded = False  # metadata
  sidebar_groups[2].expanded = False  # labels

  sidebar_groups[3].expanded = False  # primitives



  # Apply the sidebar groups configuration to the app config
  thepatch_dataset.app_config.sidebar_groups = sidebar_groups

  # Save the updated app config
  thepatch_dataset.compute_metadata()
  thepatch_dataset.save()

  # Export the dataset without saving the image data (It gets saved as "sample.json" and "metadata.json" in the inputpath folder)
  thepatch_dataset.export(
      export_dir=INPUT_PATH,
      dataset_type=fo.types.FiftyOneDataset,
      export_media=False  # This ensures only labels and metadata are saved
  )

  # Let's automatically generate the CSV now too, just to be nice
  json_to_csv(INPUT_PATH, UTC_OFFSET, TAXA_LIST_PATH)

  print(thepatch_dataset)
  # Sort the dataset by patch_width in ascending order
  sorted_dataset = thepatch_dataset.sort_by("patch_width",True)

  # Launch the FiftyOne App with the sorted view
  session = fo.launch_app(sorted_dataset)
  print(f"{bcolors.OKGREEN}The app is running, open your browser to use{bcolors.ENDC}")
  print(f"{bcolors.WARNING} or press CTRL+C to kill app{bcolors.ENDC}")


  session.wait(-1)

