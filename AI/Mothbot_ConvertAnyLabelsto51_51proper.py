import os
import json
import fiftyone as fo
INPUT_PATH = r'C:/Users/andre/Desktop/Mothbox data/PEA_PeaPorch_AdeptTurca_2024-09-01/2024-09-01'




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
  
  # Extract relevant data from the detection labels
  labels = data['shapes']
  
  metadata = {}
  for item in data.get('metadata', []):   #todo, fix METAdata inserting function so only one meta data deeep (no unecessary metadata)
    if 'metadata' in item:
      for subitem in item['metadata']:
        key, value = list(subitem.items())[0]
        metadata[key] = value
    else:
      key, value = list(item.items())[0]
      metadata[key] = value

  
  
  
  
  
  return image_path, labels, image_height, image_width, metadata


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



def create_sample(image_path, labels, image_height, image_width, metadata,ds):
  """Creates a FiftyOne JSON sample manually.

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

      uploaded=metadata["uploaded"],

      mothbox=metadata["mothbox"],
      sdcard=metadata["sd.card"], #Dots might be bad in key name
      software=str(metadata["software"]),
      sheet=metadata["sheet"],
      country=metadata["country"],
      area=metadata["area"],
      punto=metadata["point"], #point is maybe a special key name in 51

  )
   
  """ 
    sample = {
      "_id": len(data["samples"]) + 1,
      "filepath": image_path,

      "uploaded":metadata["uploaded"],

      "mothbox":metadata["mothbox"],
      "sdcard":metadata["sd.card"], #Dots might be bad in key name
      "software":str(metadata["software"]),
      "sheet":metadata["sheet"],
      "country":metadata["country"],
      "area":metadata["area"],
      "punto":metadata["point"], #point is maybe a special key name in 51


      "location": {
        'point':[metadata["longitude"],metadata["latitude"]],
        'line':None,
        'tags':[metadata["area"],metadata["point"],"height_"+str(metadata["height (placement above ground)"])]
      },



      "habitat":metadata["habitat"],
      "program":metadata["program"],
      "notes":metadata["notes"],
      "crew":metadata["crew"],
      "deployment_name":metadata["deployment.name"], #warning dots like . break json keys
      "deployment_date":metadata["deployment.date"],
      "collect_date":metadata["collect.date"],
      "data_storage_location":metadata["data.storage.location"],
      "basis_of_record": "machine_observation",



      "tags": [],
      "_media_type": "image",
      #"_dataset_id": 1,  # Replace with your desired dataset ID
      "ground_truth": {
          "_cls": "Detections",
          "detections": []
      }
  }
  """
  detections=[]


  for label in labels:
    direction = label['direction']
    label_name = label['label']
    score = label['score']
    points = label['points']
    shape_type = label['shape_type']

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
      jsondetection = {
          #"_id": len(sample["ground_truth"]["detections"]) + 1,
          "_cls": "Detection",
          "attributes": {},
          "tags": [label_name],
          "label": "boringlabel",
          "bounding_box": [
              left,
              top,
              width,
              height
          ]
      }

      detection=fo.Detection(
        tags=[label_name],
        label="creature",
        bounding_box=[left, top, width, height],
        attributes={}
      )

      #sample["ground_truth"]["detections"].append(detection)
      detections.append(detection)
    elif shape_type == 'polygon':
      # Handle polygon annotations (adjust as needed)
      None

    sample["ground_truth"] = fo.Detections(detections=detections)
    return sample


def create_fiftyone_dataset(data_dir, labels_dir, metadata_field):
  """Creates a FiftyOne dataset from multiple JSON files.

  Args:
    data_dir (str): Path to the directory containing image files.
    labels_dir (str): Path to the directory containing JSON label files.
    metadata_field (str): Name of the field in the JSON files containing metadata.

  Returns:
    fiftyone.Dataset: The created FiftyOne dataset.
  """

  dataset = fo.Dataset()

  for image_filename in sorted(os.listdir(data_dir)):
    image_path = os.path.join(data_dir, image_filename)

    # Load image dimensions (adjust as needed based on your image format)
    image_height, image_width = get_image_dimensions(image_path)

    # Load labels from JSON file
    with open(os.path.join(labels_dir, os.path.splitext(image_filename)[0] + ".json"), "r") as f:
      labels = json.load(f)

    # Load metadata from JSON file
    metadata = labels[metadata_field]

    # Create a FiftyOne sample
    sample = dataset.create_sample(
      filepath=image_path,
      ground_truth=fo.Detections(detections=[])
    )

    # Add metadata fields
    for field, value in metadata.items():
      if field in ["longitude", "latitude"]:
        # Handle location data (adjust as needed)
        if not sample.exists("location"):
          sample["location"] = fo.Geolocation(point=[0, 0], line=None, tags=[])
        sample["location"][field] = value
      else:
        sample[field] = value

    for label in labels:
      direction = label['direction']
      label_name = label['label']
      score = label['score']
      points = label['points']
      shape_type = label['shape_type']
      ID_type = label['description']

      if shape_type == 'rotation':
        top, left, width, height = handle_rotation_annotation(points)

        # Normalize bounding box coordinates
        top /= image_height
        left /= image_width
        width /= image_width
        height /= image_height

        # Create a FiftyOne detection
        detection = fo.Detection(
          tags=[label_name],
          label="creature",
          bounding_box=[left, top, width, height],
          attributes={},
          label_type=ID_type
        )
        sample.ground_truth.detections.append(detection)

      elif shape_type == 'polygon':
        # Handle polygon annotations (adjust as needed)
        pass

  return dataset

def add_sample_to_dataset(dataset, image_path, labels, metadata):
  """Adds a sample to a FiftyOne dataset.

  Args:
    dataset (fiftyone.Dataset): The FiftyOne dataset.
    image_path (str): Path to the image file.
    labels (list): List of labels.
    metadata (dict): Metadata for the sample.
  """

  sample = dataset.create_sample(
    filepath=image_path,
    ground_truth=fo.Detections(detections=[])
  )

  # Add metadata fields
  for field, value in metadata.items():
    sample[field] = value

  for label in labels:
    direction = label['direction']
    label_name = label['label']
    score = label['score']
    points = label['points']
    shape_type = label['shape_type']

    # ... (handle shape types and create detections as needed)

    # Example for rotation:
    if shape_type == 'rotation':
      top, left, width, height = handle_rotation_annotation(points)

      # Normalize bounding box coordinates (adjust as needed)

      detection = fo.Detection(
        tags=[label_name],
        label="boringlabel",
        bounding_box=[left, top, width, height],
        attributes={}
      )
      sample.ground_truth.detections.append(detection)

  dataset.save()


### START
pairs = find_image_json_pairs(INPUT_PATH)


dataset = fo.Dataset()
samples=[]
# Iterate through pairs and load data
for image_path, json_path in pairs:
  image_path, labels, image_height, image_width, metadata = load_anylabeling_data(json_path)
  #TODO: #New thoughts: assume metadata was loaded in the json file, add it if it is there. # OLD THOUGHTS:Also look for a _metadata.json file. Load its data, and send to the next function too
  sample = create_sample(image_path, labels, image_height, image_width, metadata, dataset )
  samples.append(sample)
  #sample = create_fiftyone_json(image_path, labels, image_height, image_width, metadata)
  #data["samples"].append(sample)

# Create dataset
#dataset = fo.Dataset("my-detection-dataset")
dataset = fo.Dataset()

dataset.add_samples(samples)


session = fo.launch_app(dataset)
session.wait()

"""
# Save the final FiftyOne JSON
with open(INPUT_PATH+"/"+"samples.json", "w") as f:
    json.dump(data, f, indent=4)
    print("finished creating: "+INPUT_PATH+"/"+"samples.json")
"""