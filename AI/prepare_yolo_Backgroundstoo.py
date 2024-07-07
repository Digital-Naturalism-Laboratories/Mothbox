import os
import random
import shutil

def prepare_yolo_data(image_folder, label_folder,backgrounds_folder, output_folder, train_ratio=0.5, test_ratio=0.3, val_ratio=0.2, bg_ratio=.2, total_images=1000):
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

  # Create output folders (ensure parents exist)
  os.makedirs(os.path.join(output_folder, "images/train"), exist_ok=True)
  os.makedirs(os.path.join(output_folder, "images/test"), exist_ok=True)
  os.makedirs(os.path.join(output_folder, "images/val"), exist_ok=True)
  os.makedirs(os.path.join(output_folder, "labels/train"), exist_ok=True)
  os.makedirs(os.path.join(output_folder, "labels/test"), exist_ok=True)
  os.makedirs(os.path.join(output_folder, "labels/val"), exist_ok=True)

  # Get image list
  image_files = [f for f in os.listdir(image_folder) if f.endswith(".jpg")]

  # Randomly select image-label pairs
  selected_images = random.sample(image_files, total_images)

  # Calculate number of images per category
  train_count = int(total_images * train_ratio)
  test_count = int(total_images * test_ratio)
  val_count = total_images - train_count - test_count

  # Process each image and label
  for i, image_file in enumerate(selected_images):
    image_path = os.path.join(image_folder, image_file)
    label_path = os.path.join(label_folder, os.path.splitext(image_file)[0] + ".txt")

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

  # Get number of background images to add 
  num_background_images = int(total_images * bg_ratio)

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







# Get user input
total_images = int(input("Enter the total number of images to prepare: "))

# Prepare data
prepare_yolo_data(
  image_folder="ALLIMAGES",
  label_folder="labels",
  backgrounds_folder="backgrounds",
  output_folder="ready_to_yolo",
  total_images=total_images
)

print(f"Finished preparing {total_images} image-label pairs for YOLO.")
