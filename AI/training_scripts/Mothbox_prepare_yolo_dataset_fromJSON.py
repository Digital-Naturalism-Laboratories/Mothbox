#Mothbox Pre-training Data Collector and Preparer


import os
import random
import shutil
import datetime
import json

# Global variable for the starting folder path
STARTING_FOLDER = r"E:\Panama"
NUM_TO_PROCESS=10
CLASSES_PATH = r"E:\Panama\classes.txt"

#This is going to cheat a bit, and make all labels "creature", so we don't actually use "classes.txt" right now
def json_to_yolo_obb(json_path, classes_path,yolo_path_to_save):
    
    # Load class names
    with open(classes_path, 'r') as f:
        classes = [line.strip() for line in f.readlines()]

    # Load JSON data
    print(json_path)
    with open(json_path, 'r') as f:
        data = json.load(f)

    # Get image dimensions
    image_width = data['imageWidth']
    image_height = data['imageHeight']

    # Prepare output lines
    yolo_lines = []

    #Right now we are going to cheat, and if the class wasn't found in class.txt, we default to "creature" with id=0
    for shape in data['shapes']:
        label = shape['label']

        if label not in classes:
              print(f"Warning: Label '{label}' not found in classes. Default to creature. id 0.")
              label="creature"
              class_id=0
        else:
          class_id = classes.index(label)
        points = shape['points']

        # Normalize points
        normalized_points = [
            [x / image_width, y / image_height]
            for x, y in points
        ]

        # Flatten normalized points
        flat_points = [coord for point in normalized_points for coord in point]
        
        # Create YOLO line
        yolo_line = f"{class_id} " + " ".join(map(str, flat_points))
        yolo_lines.append(yolo_line)

    # Save to YOLO-OBB .txt file
    #output_path = os.path.splitext(json_path)[0] + '.txt'
    output_path=yolo_path_to_save
    with open(output_path, 'w') as f:
        f.write("\n".join(yolo_lines))

    print(f"YOLO-OBB file saved to: {output_path}")

def find_hu_json_detection_matches(folder_path):
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

    for jpg_file in jpg_files:
        # target human file
        humanD_json_file = jpg_file.replace(".jpg", ".json")
        if humanD_json_file in json_files:
            hu_detection_matches_list.append((jpg_file,humanD_json_file))

    return hu_detection_matches_list

def find_matching_pairs_img_txt(folder_path):
    """Finds pairs of .txt and .jpg/.png files with the same name in a given folder."""
    
    txt_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
    matching_pairs = []
    for txt_file in txt_files:
        base_name = txt_file[:-4]  # Remove the .txt extension
        image_files = [f for f in os.listdir(folder_path) if f.startswith(base_name) and f.endswith(('.jpg', '.png'))]
        if image_files:
            # Found a matching pair
            txt_file_path = os.path.join(folder_path, txt_file)
            image_file_path = os.path.join(folder_path, image_files[0])
            matching_pairs.append((txt_file_path, image_file_path))
    return matching_pairs

def search_folders(folder_path):
    """Recursively searches through folders and subfolders for matching pairs."""
    
    matching_pairs = []
    for root, dirs, files in os.walk(folder_path):
        if any(file.endswith('.json') and file not in ['metadata.json', 'samples.json'] for file in files):
          print("Folders with Annotation to Look in: ",root)
          matching_pairs.extend(find_hu_json_detection_matches(root))
    return matching_pairs

def prepare_yolo_data(matching_pairs, num_to_process, output_folder,  train_ratio=0.5, test_ratio=0.3, val_ratio=0.2):
  """
  Prepares images and labels for YOLO training.

  Args:
    train_ratio: Ratio of images for training (default: 0.5).
    test_ratio: Ratio of images for testing (default: 0.3).
    val_ratio: Ratio of images for validation (default: 0.2).
  """


  # Randomly select image-label pairs
  selected_pairs = random.sample(matching_pairs, num_to_process)
  # Calculate number of images per category
  train_count = int(num_to_process * train_ratio)
  test_count = int(num_to_process * test_ratio)
  val_count = num_to_process - train_count - test_count
  

  trainImage = os.path.join(output_folder, "images/train")
  trainLabel = os.path.join(output_folder, "labels/train")
  
  testImage = os.path.join(output_folder, "images/test")
  testLabel = os.path.join(output_folder, "labels/test")

  valImage = os.path.join(output_folder, "images/val")
  valLabel = os.path.join(output_folder, "labels/val")

  # Process each image and label
  for i, pair in enumerate(selected_pairs):
    image_path, label_path=pair

    if i < train_count:
      output_image_folder = trainImage
      output_label_folder = trainLabel
    elif i < train_count + test_count:
      output_image_folder = testImage
      output_label_folder = testLabel
    else:
      output_image_folder = valImage
      output_label_folder = valLabel

    # Get the image filename
    image_filename = os.path.basename(image_path)
    # Get the label filename
    label_filename = os.path.basename(label_path).replace(".json", ".txt")
    # Copy image and label using shutil.copy
    shutil.copy(image_path, os.path.join(output_image_folder, image_filename))

    #create label where it should go
    json_to_yolo_obb(label_path, CLASSES_PATH,os.path.join(output_label_folder, label_filename))

    print(f"{i+1}/{num_to_process} Copied {image_filename} and {label_filename} to {output_image_folder}")


def find_folders_with_json(root_folder):
  """
  Finds folders that contain at least one *.json file, excluding "metadata.json" and "samples.json".

  Args:
    root_folder: The root folder to search.

  Returns:
    A list of folder paths that contain at least one *.json file.
  """

  folders_with_json = []
  for root, dirs, files in os.walk(root_folder):
    if any(file.endswith('.json') and file not in ['metadata.json', 'samples.json'] for file in files):
      folders_with_json.append(root)
  return folders_with_json



#START CODE

# Find all matching pairs
matching_pairs = search_folders(STARTING_FOLDER)

# Print the number of matching pairs
print(f"Found {len(matching_pairs)} matching pairs.")

# Ask the user for the number of pairs to process
num_pairs_to_process = int(input("How many pairs do you want to process? "))
# Ensure num_pairs_to_process is within a valid range
num_pairs_to_process = max(1, min(num_pairs_to_process, len(matching_pairs)))
NUM_TO_PROCESS=num_pairs_to_process


# Get the current date in YYYY-MM-DD format
current_date = datetime.date.today().strftime('%Y-%m-%d')


# Get the directory of the STARTING_FOLDER
starting_folder_dir = os.path.dirname(STARTING_FOLDER)

# Get the directory of the parent folder
parent_folder_dir = os.path.dirname(starting_folder_dir)

# Create the output folder path
output_folder = os.path.join(parent_folder_dir, f"mothbox_dataset_{NUM_TO_PROCESS}_{current_date}")

# Create output folders (ensure parents exist)
os.makedirs(os.path.join(output_folder, "images/train"), exist_ok=True)
os.makedirs(os.path.join(output_folder, "images/test"), exist_ok=True)
os.makedirs(os.path.join(output_folder, "images/val"), exist_ok=True)
os.makedirs(os.path.join(output_folder, "labels/train"), exist_ok=True)
os.makedirs(os.path.join(output_folder, "labels/test"), exist_ok=True)
os.makedirs(os.path.join(output_folder, "labels/val"), exist_ok=True)

prepare_yolo_data(matching_pairs,NUM_TO_PROCESS, output_folder)





