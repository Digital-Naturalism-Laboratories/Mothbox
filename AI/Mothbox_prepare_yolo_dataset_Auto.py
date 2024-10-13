#Mothbox Pre-training Data Collector and Preparer


import os
import random
import shutil
import datetime

# Global variable for the starting folder path
STARTING_FOLDER = r"E:\Panama"
NUM_TO_PROCESS=10

def find_matching_pairs(folder_path):
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
          matching_pairs.extend(find_matching_pairs(root))
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
    label_path,image_path=pair

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
    label_filename = os.path.basename(label_path)
    # Copy image and label using shutil.copy
    shutil.copy(image_path, os.path.join(output_image_folder, image_filename))
    shutil.copy(label_path, os.path.join(output_label_folder, label_filename))

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



'''folders_with_json = find_folders_with_json(STARTING_FOLDER)

# Now you have a list of folders with JSON files:
for folder in folders_with_json:
  # Do something with each folder, e.g., scan for specific JSON files
  print("Folders that Have JSON/Anylabelling in them ",folder)
'''


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
output_folder=  STARTING_FOLDER+"/mothbox_dataset_"+str(NUM_TO_PROCESS)+"_"+current_date

# Create output folders (ensure parents exist)
os.makedirs(os.path.join(output_folder, "images/train"), exist_ok=True)
os.makedirs(os.path.join(output_folder, "images/test"), exist_ok=True)
os.makedirs(os.path.join(output_folder, "images/val"), exist_ok=True)
os.makedirs(os.path.join(output_folder, "labels/train"), exist_ok=True)
os.makedirs(os.path.join(output_folder, "labels/test"), exist_ok=True)
os.makedirs(os.path.join(output_folder, "labels/val"), exist_ok=True)

prepare_yolo_data(matching_pairs,NUM_TO_PROCESS, output_folder)





