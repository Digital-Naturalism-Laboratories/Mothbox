#!/usr/bin/env python3

import json
import os
INPUT_PATH = r'C:\Users\andre\Desktop\FondoGorila\2024-11-17'
from pathlib import Path
import cv2
import numpy as np
import re


def crop_rect(
    img, rect, interpolation=cv2.INTER_LINEAR
):  # cv2.INTER_LANCZOS4  cv2.INTER_LINEAR cv2.INTER_CUBIC
    # get the parameter of the small rectangle
    center, size, angle = rect[0], rect[1], rect[2]
    center, size = tuple(map(int, center)), tuple(map(int, size))

    # get row and col num in img
    height, width = img.shape[0], img.shape[1]

    # calculate the rotation matrix
    M = cv2.getRotationMatrix2D(center, angle, 1)
    # rotate the original image
    img_rot = cv2.warpAffine(img, M, (width, height), flags=interpolation)

    # now rotated rectangle becomes vertical, and we crop it
    img_crop = cv2.getRectSubPix(img_rot, size, center)

    return img_crop #, img_rot




def generateThumbnailPatches_JSON(image_path, json_data, patch_folder,skip_existing=True):
    # Load the image using OpenCV
    model_name=json_data.get("version")
    if not model_name.startswith("Mothbot"):
        model_name="HumanDetection"

    # Dictionary to store loaded images
    loaded_images = {}

    # Iterate through each shape in the JSON data
    for shape_index, shape in enumerate(json_data["shapes"]):
        filename=os.path.basename(image_path)
        patchfilename=filename.split('.')[0] + "_"+str(shape_index) + "_" + model_name+"." +filename.split('.')[1]
        patchfullpath = Path(patch_folder) / patchfilename 
        if os.path.exists(patchfullpath) and skip_existing: #if the thumbnail already exists, and it's true we want to skip it, then skip it
            print("thumbnail exists, skipping")
            continue
                
        # Check if the image is already loaded
        if image_path not in loaded_images:
            loaded_images[image_path] = cv2.imread(image_path)

        image = loaded_images[image_path]
        
        # Extract the points from the shape
        points = shape["points"]

        # Convert the points to a NumPy array
        points = np.array(points, dtype=np.float32)

        # Calculate the minimum area rectangle
        rect = cv2.minAreaRect(points)

        # Send the cropped image and the shape index to the crop_rect function
        img_crop=crop_rect(image, rect)

        cv2.imwrite(
            patchfullpath,
            img_crop,
        )
    loaded_images.clear()

def generateThumbnailPatches(img,thefilepath,rectangle,detnum, modelname):

    filename=os.path.basename(thefilepath)
    directory_path = os.path.dirname(thefilepath)
    patch_folder_path=Path(directory_path+"/patches")
    patch_folder_path.mkdir(parents=True, exist_ok=True)

    patchfilename=filename.split('.')[0] + "_" + str(detnum) + "_" + model_name+"." +filename.split('.')[1]
    patchfullpath = Path(patch_folder_path) / f'{patchfilename}' 

    # img_crop will the cropped rectangle
    img_crop= crop_rect(img, rectangle)


    cv2.imwrite(
        patchfullpath,
        img_crop,
    )


def scan_for_images(date_folder_path):
  """Scans subfolders for JPEG files and returns a list of file paths."""
  jpeg_files = []
  for date_folder in date_folders:
    for filename in os.listdir(date_folder):
        if filename.endswith(".jpg"):
            jpeg_files.append(os.path.join(date_folder, filename))
  return jpeg_files

def find_date_folders(directory):
    """
    Recursively searches through a directory and its subdirectories for folders
    with names in the YYYY-MM-DD format. If the input directory itself is a "date folder",
    it will also be included in the results.

    Args:
        directory: The directory to search.

    Returns:
        A list of paths to the found folders.
    """

    date_regex = r"^\d{4}-\d{2}-\d{2}$"
    folders = []

    # Check if the input directory itself is a "date folder"
    if re.match(date_regex, os.path.basename(directory)):
        folders.append(directory)

    # Recursively search subdirectories for "date folders"
    for root, dirs, files in os.walk(directory):
        for dir_name in dirs:
            if re.match(date_regex, dir_name):
                folders.append(os.path.join(root, dir_name))

    return folders

def process_images(img_files, date_folder):
    """
   

    Args:
      
    """

    # Get total number of JPEG files
    total_img_files = len(img_files)

    patch_folder_path=Path(date_folder+"/patches")
    patch_folder_path.mkdir(parents=True, exist_ok=True)


    for idx,filename in enumerate(img_files):

        image_path = os.path.join(date_folder, filename)
        json_path = os.path.join(date_folder, filename[:-4] + ".json")

        # Calculate progress
        processed_files = idx + 1
        progress = (processed_files / total_img_files) * 100

        # Print progress
        print(f"({progress:.2f}%) Processing:  {filename} ")


        # **Check 0: Ensure the image file has more than 0 bytes**
        if not os.path.isfile(image_path) or os.path.getsize(image_path) == 0:
            print(f"Skipping {filename}: Image file is missing or empty.")
            continue

        # **Check 1: Check if JSON file exists and if it's an automated Mothbot file**
        is_ground_truth_detection = False
        if os.path.isfile(json_path):
            is_ground_truth_detection=True
            print(json_path)
            print("Json exists for this image file")

            try:
                with open(json_path, 'r') as json_file:
                    json_data = json.load(json_file)
                    #print(json_data)
                    print("creating thumbnails for img+json pair")
                    generateThumbnailPatches_JSON(image_path, json_data, patch_folder_path,)

            except json.JSONDecodeError:
                print(f"{filename}: Corrupted JSON file.")


# This code will only run if this script is executed directly
if __name__ == "__main__":

    date_folders = find_date_folders(INPUT_PATH)
    for date_folder_path in date_folders:
        print(date_folders)
        images = scan_for_images(date_folder_path)
        process_images(images, date_folder_path)
