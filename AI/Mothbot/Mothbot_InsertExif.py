#!/usr/bin/env python3
import os
import json
from pathlib import Path
from PIL import Image
from datetime import datetime
import re
import piexif
import subprocess
import threading
import argparse
import platform
import io #put these 3 lines here so radio can read stuff without breaking
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

#TODO: make work for entire deployment
INPUT_PATH = r"G:\Shared drives\Mothbox Management\Testing\ExampleDataset\Les_BeachPalm_hopeCobo_2025-06-20\2025-06-21"

#you probably always want these below as true
ID_HUMANDETECTIONS = True
ID_BOTDETECTIONS = True

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input_path",
        required=False,
        default=INPUT_PATH,
        help="path to images for classification (ex: datasets/test_images/data)",
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



def load_anylabeling_data(json_path, image_path, tagger): 
  
  """Loads data from an AnyLabeling JSON file.

  Args:

  """

  with open(json_path, 'r') as f:
    data = json.load(f)
  
  long= data['longitude']
  lat = data['latitude']

  # Extract relevant data from the detection labels
  detections = data['shapes']

  nightfolder =os.path.dirname(image_path)

  for label in detections:


    direction = label['direction']
    label_name = label['label']
    theclusterID= label['clusterID']
    score = label['score']
    points = label['points']
    shape_type = label['shape_type']
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

    full_patch_path=Path(nightfolder+"/"+the_patch_path) #should work on mac or windows

    print("adding taxonomy with Exiftool...(can take a couple seconds)")

    print("adding GPS to "+str(full_patch_path))
    add_gps_exif(full_patch_path, full_patch_path,float(lat), float(long))

    tagger.add_taxonomy_with_exiftool(str(full_patch_path), taxonomic_list) 
    print("✅ exif data written into patch file" +str(full_patch_path))


  
  return

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
            print(f" Tags written to {image_path}") # cannot do ✅
        else:
            print(f" exiv2 failed:\n{result.stderr}") #cannot do ❌
    except FileNotFoundError:
        print(" exiv2 CLI tool not found. Make sure it's installed and in your system PATH.") #cannot do ❌


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
    print(f" Taxonomy tags written using naturtag to: {image_path}")


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
        print(f" Successfully tagged: {image_path}")
    except Exception as e:
        print(f" naturtag failed with error:\n{e}")
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
        print("Fallback EXIF tags written")


class ExifToolSession:
    exifPath="exiftool" #mac or linux
    if(platform.system()=='Windows'):
        exifPath="../exiftool-13.32_64/exiftool"
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
            #print(f"  ExifTool output for {full_patch_path}:")
            for line in output_lines:
                None
                #print("  ", line)

    def close(self):
        self.process.stdin.write("-stay_open\nFalse\n")
        self.process.stdin.flush()
        self.process.wait()


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
        #filename = os.path.basename(sample.filepath) #this is just the basename that it stores!
        #sample_fullpath=INPUT_PATH+"/"+filename

        #print(sample.filename)


        #print(sample)
        detections= sample.creature_detections.detections
        detnum=0

        for detection in detections:
            patchfullpath=INPUT_PATH+"/"+detection.patch_path
            #inferred_patchfilename=filename.split('.')[0] + "_" + str(detnum) +"_"+detector+ "." +filename.split('.')[1]
            #inferred_patchfullpath = Path(patch_folder_path) / f'{inferred_patchfilename}' 

            #add GPS info to the thumbnail patch
            print("adding GPS to "+patchfullpath)
            add_gps_exif(patchfullpath, patchfullpath,float(sample.latitude), float(sample.longitude))




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

def connect_metadata_matched_img_json_pairs(
    hu_matched_img_json_pairs,bot_matched_img_json_pairs, exiftagger):

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

            load_anylabeling_data(json_path, image_path, exiftagger)

    print("processing BOT Detections.........")
    if(ID_BOTDETECTIONS):
        # Next process each pair and generate temporary files for the ROI of each detection in each image
        # Iterate through image-JSON pairs
        index = 0
        numofpairs = len(bot_matched_img_json_pairs)
        for pair in bot_matched_img_json_pairs:
            # Load JSON file and 
            image_path, json_path = pair[:2]  # Always extract the first two elements

            load_anylabeling_data(json_path, image_path, exiftagger)


if __name__ == "__main__":
  ### START
  print("adding exif info to the patches")

  """
  First the script takes in a INPUT_PATH

  Then, (to simplify its searching) it looks through all the folders for folders that are just a single "night"
  and follow the date format YYYY-MM-DD for their structure

  in each of these folders, it looks to see if there are any .json

  """
  print("Starting script to  add metadata to raw iamges")
  args = parse_args()

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
      + " pairs of images and HUMAN detection data insert exif",
  )
  # Example Pair
  print("example human detection and json pair:")
  if(len(hu_matched_img_json_pairs)>0):
      print(hu_matched_img_json_pairs[0])

  print(
      "Found ",
      str(len(bot_matched_img_json_pairs))
      + " pairs of images and BOT detection data to insert exif",
  )
  # Example Pair
  print("example human detection and json pair:")
  if(len(bot_matched_img_json_pairs)>0):
      print(bot_matched_img_json_pairs[0])


  # ~~~~~~~~~~~~~~~~ Processing Data ~~~~~~~~~~~~~~~~~~~~~~~~~~
  
  tagger = ExifToolSession()
  # Now that we have our data to be processed in a big list, it's time to load up the Pybioclip stuff
  connect_metadata_matched_img_json_pairs(
      hu_matched_img_json_pairs,
      bot_matched_img_json_pairs,
      exiftagger=tagger
  )

  tagger.close()

  print("Finished Attaching exif info")


  

