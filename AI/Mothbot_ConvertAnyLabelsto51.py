import os
import json





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

  # Extract relevant data
  image_path = data['imagePath']
  labels = data['shapes']
  image_height = data['imageHeight']
  image_width = data['imageWidth']

  return image_path, labels, image_height, image_width


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



def create_fiftyone_json(image_path, labels, image_height, image_width):
  """Creates a FiftyOne JSON sample manually.

  Args:
    image_path: The path to the image file.
    labels: A list of labels from the AnyLabeling JSON file.
    image_height: The height of the image.
    image_width: The width of the image.

  Returns:
    A FiftyOne JSON sample.
  """

  sample = {
      "_id": len(data["samples"]) + 1,
      "filepath": image_path,
      "tags": [],
      "_media_type": "image",
      #"_dataset_id": 1,  # Replace with your desired dataset ID
      "ground_truth": {
          "_cls": "Detections",
          "detections": []
      }
  }

  for label in labels:
    direction = label['direction']
    label_name = label['label']
    score = label['score']
    points = label['points']
    shape_type = label['shape_type']

    if shape_type == 'rotation':
      top, left, width, height = handle_rotation_annotation(points)
      # Normalize bounding box coordinates
      top /= image_height
      left /= image_width
      width /= image_width
      height /= image_height
            # Create a FiftyOne detection
      detection = {
          #"_id": len(sample["ground_truth"]["detections"]) + 1,
          "_cls": "Detection",
          "attributes": {},
          "tags": [label_name],
          "label": "boringlabel",
          "bounding_box": [
              top,
              left,
              width,
              height
          ]
      }
      sample["ground_truth"]["detections"].append(detection)

    elif shape_type == 'polygon':
      # Handle polygon annotations (adjust as needed)
      None

  return sample





# Replace 'your_input_directory' with the actual path to your input directory
INPUT_PATH = 'F:/Panama/PEA_PeaPorch_AdeptTurca_2024-09-01/2024-09-01'
pairs = find_image_json_pairs(INPUT_PATH)

# Create an initial FiftyOne JSON structure
data = {
    "samples": []
}


# Iterate through pairs and load data
for image_path, json_path in pairs:
  image_path, labels, image_height, image_width = load_anylabeling_data(json_path)
  sample = create_fiftyone_json(image_path, labels, image_height, image_width)
  data["samples"].append(sample)

# Save the final FiftyOne JSON
with open(INPUT_PATH+"/"+"samples.json", "w") as f:
    json.dump(data, f, indent=4)
    print("finish")