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

# Import the function from json_to_csv_converter.py
from Mothbot_ConvertDatasettoCSV import json_to_csv

INPUT_PATH = r"C:\Users\andre\Desktop\Canopy Tower\Gamboa_RDCTopminus1level_CalmoBarbo_2024-11-14\2024-11-14"
METADATA_PATH=r'C:\Users\andre\Documents\GitHub\Mothbox\AI\Mothbox_Main_Metadata_Field_Sheet_Example.csv'
UTC_OFFSET= -5 #Panama is -5, change for different locations

TAXA_LIST_PATH = r"C:\Users\andre\Documents\GitHub\Mothbox\AI\SpeciesList_CountryPanama_TaxaInsecta.csv" # downloaded from GBIF for example just insects in panama: https://www.gbif.org/occurrence/taxonomy?country=PA&taxon_key=212

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


def find_csv_match(input_path, metadata_path):
    """
    Finds a matching row in the CSV metadata file based on parsed components from the input path.

    Args:
        input_path (str): Path to the folder containing the data.
        metadata_path (str): Path to the CSV metadata file.

    Returns:
        dict: A dictionary containing the matching row, or an empty dict if no match is found.
    """
    # Parse the parent folder's name
    parent_folder = os.path.basename(os.path.dirname(input_path))
    
    # Split the parent folder into parts
    parts = parent_folder.split("_")
    if len(parts) != 4:
        raise ValueError("The input path does not contain the expected 4 parts in the parent folder's name.")

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

def create_sample(image_path, labels, image_height, image_width, metadata, detection_creator):
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
    unwanted_values = {"hole", "circle", "background", "wall", "floor", "blank"}
    if any(value in unwanted_values for value in filtered_dict.values()):
        taxonomic_list = ["Error"]
    else:
        # Format the filtered dictionary
        taxonomic_list = [f"{key.upper()}_{value}" for key, value in filtered_dict.items()]

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

  for image_path, json_path in hu_pairs:
    full_image_path = image_path
    labels, image_height, image_width, notmetadata, detection_creator = load_anylabeling_data(json_path)
    sample = create_sample(full_image_path, labels, image_height, image_width, metadata, detection_creator )
    samples.append(sample)

  for image_path, json_path in bot_pairs:
    full_image_path = image_path
    labels, image_height, image_width, notmetadata, detection_creator = load_anylabeling_data(json_path)
    sample = create_sample(full_image_path, labels, image_height, image_width, metadata, detection_creator )
    samples.append(sample)

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

