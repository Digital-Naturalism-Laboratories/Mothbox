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

# Import the function from json_to_csv_converter.py
from Mothbot_ConvertDatasettoCSV import json_to_csv

INPUT_PATH = r'F:\Panama\Gamboa_RDCbottom_comerLicaon_2024-11-14\2024-11-15'
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

def load_anylabeling_data(json_path):
  """Loads data from an AnyLabeling JSON file.

  Args:
    json_path: The path to the JSON file.

  Returns:
    A dictionary containing the loaded data.
  """

  with open(json_path, 'r') as f:
    data = json.load(f)

  image_path = data['imagePath']

  image_height = data['imageHeight']
  image_width = data['imageWidth']
  creator=""
  if(data['version'].startswith("Mothbot")):
     detectionBy= data['version']
     creator=detectionBy
  else:
     detectionBy="HumanDetection"
     creator=detectionBy
  
  # Extract relevant data from the detection labels
  labels = data['shapes']
  

  # Step 1: Create the metadata path
  base_name, ext = os.path.splitext(json_path)
  metadata_path = f"{base_name}_metadata{ext}"

  # Step 2: Initialize an empty dictionary to store metadata
  metadata = {}

  # Step 3: Check if the metadata file exists
  if not os.path.exists(metadata_path):
      print(f"Metadata file not found: {metadata_path}")
      return     image_path, labels, image_height, image_width, metadata, creator

  #if it does exist, do this...
  try:
      # Step 4: Open and parse the metadata JSON file
      with open(metadata_path, 'r') as file:
          data = json.load(file)
      
      # Step 5: Check if 'metadata' field exists and is a list
      if 'metadata' in data and isinstance(data['metadata'], list):
          # Step 6: Loop through the list and update the dictionary
          for item in data['metadata']:
              if isinstance(item, dict):
                  metadata.update(item)
  except Exception as e:
      print(f"Error reading metadata file: {e}")
      #return metadata #return empty metadata

  


  
  return image_path, labels, image_height, image_width, metadata, detectionBy


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



def create_sample(image_path, labels, image_height, image_width, metadata,ds, creator):
  """Creates a FiftyOne sample using the 51 python interface

  Args:
    image_path: The path to the image file.
    labels: A list of labels from the AnyLabeling JSON file.
    image_height: The height of the image.
    image_width: The width of the image.

  Returns:
    A FiftyOne JSON sample.
  """


  #print(metadata)

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
  sample["ground_height"]=metadata.get("height (placement above ground)","")
  
  sample["deployment_name"]=metadata.get("deployment.name","")
  sample["deployment_date"]=metadata.get("deployment.date","")
  sample["collect_date"]=metadata.get("collect.date","")
  sample["data_storage_location"]=metadata.get("data.storage.location","")
  sample["crew"]=metadata.get("crew","")
  sample["notes"]=metadata.get("notes","")
  sample["program"]=metadata.get("program","")
  sample["habitat"]=metadata.get("habitat","")
  sample["detection_By"]=creator

  detections_list=[]

  for label in labels:
    direction = label['direction']
    label_name = label['label']
    score = label['score']
    points = label['points']
    shape_type = label['shape_type']
    ID_by = "IDby_"+label['description']

    desired_keys = ['kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species']


    # Filter the dictionary to include only desired keys
    filtered_dict = {key: value for key, value in label.items() if key in desired_keys}

    # Check for unwanted values
    unwanted_values = {"circle", "hole", "error"}
    if any(value in unwanted_values for value in filtered_dict.values()):
        taxonomic_list = ["Error"]
    else:
        # Format the filtered dictionary
        taxonomic_list = [f"{key.upper()}_{value}" for key, value in filtered_dict.items()]

    taxonomic_list.append(ID_by)
    #print(taxonomic_list)
    #input()
    if shape_type == 'rotation':
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
        direction=direction

      )

      #sample["ground_truth"]["detections"].append(detection)
      detections_list.append(detection)
    elif shape_type == 'polygon':
      # Handle polygon annotations (adjust as needed)
      None
  #print("num detections")
  #print(len(detections_list))
  sample["ground_truth"] = fol.Detections(detections=detections_list)

  return sample


def generate_patch_thumbnails(dataset, output_dir=INPUT_PATH+"/thumbnails", target_size=(1024, -1)):
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
        detections= sample.ground_truth.detections
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
                filepath_fullimage= sample.filepath, 
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
  pairs = find_image_json_pairs(INPUT_PATH)


  dataset = fo.Dataset()
  samples=[]
  # Iterate through pairs and load data
  for image_path, json_path in pairs:
    image_path, labels, image_height, image_width, metadata, creator = load_anylabeling_data(json_path)
    sample = create_sample(image_path, labels, image_height, image_width, metadata, dataset, creator )
    samples.append(sample)
    #sample = create_fiftyone_json(image_path, labels, image_height, image_width, metadata)
    #data["samples"].append(sample)

  # Create dataset
  #dataset = fo.Dataset("my-detection-dataset")
  dataset = fo.Dataset()

  dataset.add_samples(samples)


  # Generate some thumbnail images
  #print(dataset.samples)
  #input("Press Enter to continue...")
  thepatch_dataset = generate_patch_thumbnails(dataset)


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
  sorted_dataset = thepatch_dataset.sort_by("patch_width")

  # Launch the FiftyOne App with the sorted view
  session = fo.launch_app(sorted_dataset)
  print(f"{bcolors.OKGREEN}The app is running, open your browser to use{bcolors.ENDC}")
  print(f"{bcolors.WARNING} or press CTRL+C to kill app{bcolors.ENDC}")


  session.wait(-1)

