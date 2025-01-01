import cv2
import os
import random
import numpy as np

# Global variables
TRANS_IMAGES_DIR = r"C:\Users\andre\Desktop\x-anylabeling-matting\onlybig"  # Directory with transparent insect images
MAX_IMAGES = 3 

def load_random_images(dir_path, max_images):
  """
  Loads a random selection of images from the given directory.

  Args:
    dir_path: Path to the directory containing images.
    max_images: Maximum number of images to load.

  Returns:
    A list of image paths.
  """
  image_paths = [os.path.join(dir_path, f) for f in os.listdir(dir_path) if f.endswith(('.png', '.jpg', '.jpeg'))]
  return random.sample(image_paths, min(max_images, len(image_paths)))

def create_growing_outline(image_path, color):
  """
  Creates an expanding outline effect for the given image.

  Args:
    image_path: Path to the image file.
    color: Color for the outline (in BGR format).

  Returns:
    A NumPy array representing the image with the outline effect.
  """
  img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED) 
  alpha_channel = img[:, :, 3]  # Extract alpha channel
  
  # Create a copy of the alpha channel for outline
  outline_mask = alpha_channel.copy() 

  # Convert alpha channel to binary (white for non-transparent, black for transparent)
  _, outline_mask = cv2.threshold(outline_mask, 1, 255, cv2.THRESH_BINARY) 

  # Apply dilation to grow the outline
  kernel = np.ones((5, 5), np.uint8)  # Adjust kernel size for outline thickness
  dilated_mask = cv2.dilate(outline_mask, kernel, iterations=10)  # Adjust iterations for outline growth

  # Create a color mask for the outline
  color_mask = np.zeros_like(img)
  color_mask[:, :, :3] = color 
  color_mask[:, :, 3] = dilated_mask 

  # Combine original image with the colored outline
  result = cv2.addWeighted(img, 1, color_mask, 0.5, 0) 
  #return result
  return color_mask

def display_images(images):
  """
  Displays a list of images.

  Args:
    images: A list of NumPy arrays representing images.
  """
  for i, img in enumerate(images):
    cv2.imshow(f"Image {i+1}", img)
  cv2.waitKey(0)
  cv2.destroyAllWindows()

if __name__ == "__main__":
  # Load random images
  image_paths = load_random_images(TRANS_IMAGES_DIR, MAX_IMAGES)

  # Create a list to store images with outlines
  images_with_outlines = []

  # Create outlines for each image
  for path in image_paths:
    random_color = (random.randint(150, 255), random.randint(150, 255), random.randint(150, 255))  # Pastel color
    outline_image = create_growing_outline(path, random_color)
    images_with_outlines.append(outline_image)

  # Display the images with outlines
  display_images(images_with_outlines)