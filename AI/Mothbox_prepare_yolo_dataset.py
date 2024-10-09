import os
import random
import shutil

DATA_PATH= r"D:/Databases/Database_1.8_StillMessy"

TOTAL_IMAGES=10

def prepare_yolo_data(image_folder, backgrounds_folder, train_ratio=0.5, test_ratio=0.3, val_ratio=0.2, bg_ratio=.2, total_images_Def=1000):
  """
  Prepares images and labels for YOLO training.

  Args:
    image_folder: Path to the folder containing images.
    label_folder: Path to the folder containing labels.
    output_folder: Path to the output folder (ready_to_yolo).
    train_ratio: Ratio of images for training (default: 0.5).
    test_ratio: Ratio of images for testing (default: 0.3).
    val_ratio: Ratio of images for validation (default: 0.2).
    total_images: Total number of image-label pairs to process.
  """
  # Get image list
  image_files = [f for f in os.listdir(image_folder) if f.endswith(".jpg")]
  print(len(image_files))
  # Get user input

  global TOTAL_IMAGES 
  TOTAL_IMAGES = int(input("Enter the total number of images to prepare: "))

  output_folder=  DATA_PATH+"/moths"+str(TOTAL_IMAGES)

  # Create output folders (ensure parents exist)
  os.makedirs(os.path.join(output_folder, "images/train"), exist_ok=True)
  os.makedirs(os.path.join(output_folder, "images/test"), exist_ok=True)
  os.makedirs(os.path.join(output_folder, "images/val"), exist_ok=True)
  os.makedirs(os.path.join(output_folder, "labels/train"), exist_ok=True)
  os.makedirs(os.path.join(output_folder, "labels/test"), exist_ok=True)
  os.makedirs(os.path.join(output_folder, "labels/val"), exist_ok=True)




  # Randomly select image-label pairs
  selected_images = random.sample(image_files, TOTAL_IMAGES)

  # Calculate number of images per category
  train_count = int(TOTAL_IMAGES * train_ratio)
  test_count = int(TOTAL_IMAGES * test_ratio)
  val_count = TOTAL_IMAGES - train_count - test_count

  # Process each image and label
  for i, image_file in enumerate(selected_images):
    image_path = os.path.join(image_folder, image_file)
    label_path = os.path.join(image_folder, os.path.splitext(image_file)[0] + ".txt")

    if i < train_count:
      output_image_folder = os.path.join(output_folder, "images/train")
      output_label_folder = os.path.join(output_folder, "labels/train")
    elif i < train_count + test_count:
      output_image_folder = os.path.join(output_folder, "images/test")
      output_label_folder = os.path.join(output_folder, "labels/test")
    else:
      output_image_folder = os.path.join(output_folder, "images/val")
      output_label_folder = os.path.join(output_folder, "labels/val")

    # Copy image and label using shutil.copy
    shutil.copy(image_path, os.path.join(output_image_folder, image_file))
    shutil.copy(label_path, os.path.join(output_label_folder, os.path.splitext(image_file)[0] + ".txt"))

    print(f"Copied {image_file} and corresponding label to {output_image_folder}")

  print("sprinkling backgrounds")
  # Get background images
  background_files = [f for f in os.listdir(backgrounds_folder) if f.endswith(".jpg")]
  print("num background files "+str(len(background_files)))

  if len(background_files)<1:
     print("no background files included")
  else:
    # Get number of background images to add 
    num_background_images = int(TOTAL_IMAGES * bg_ratio)
    if num_background_images>=len(background_files):
      print("adjusting for lower number of backgrounds")
      num_background_images=len(background_files)
    
    # Randomly select background images
    selected_backgrounds = random.sample(background_files, num_background_images)

    # Distribute background images proportionally to train/test/val
    train_background_count = int(num_background_images * train_ratio)
    test_background_count = int(num_background_images * test_ratio)
    val_background_count = num_background_images - train_background_count - test_background_count

    # Add background images to respective folders
    for i in range(train_background_count):
        background_image = random.choice(selected_backgrounds)
        destination = os.path.join(output_folder, "images/train", background_image)
        shutil.copy(os.path.join(backgrounds_folder, background_image), destination)
        print(f"Copied {background_image}  to {destination}")

    for i in range(test_background_count):
        background_image = random.choice(selected_backgrounds)
        shutil.copy(os.path.join(backgrounds_folder, background_image), os.path.join(output_folder, "images/test", background_image))

    for i in range(val_background_count):
        background_image = random.choice(selected_backgrounds)
        shutil.copy(os.path.join(backgrounds_folder, background_image), os.path.join(output_folder, "images/val", background_image))
  


# Prepare data

prepare_yolo_data(
  image_folder=DATA_PATH+"/labeled_images",
  backgrounds_folder=DATA_PATH+"/backgrounds",
)

print(f"Finished preparing {TOTAL_IMAGES} image-label pairs for YOLO.")
