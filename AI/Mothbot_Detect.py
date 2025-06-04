#!/usr/bin/env python3

import cv2
from ultralytics import YOLO
import numpy as np
import os
import re
import json
import PIL.Image
from pathlib import Path
import argparse
from PIL import Image  # For image format verification
from Mothbot_GenThumbnails import generateThumbnailPatches, generateThumbnailPatches_JSON


#~~~~Variables to Change~~~~~~~

INPUT_PATH = r"D:\Panama\Totumas_Summit_StudyCod_2024-09-21\2024-09-23"  # raw string

YOLO_MODEL = r"C:\Users\Hubert\Desktop\Biodiversity Monitoring\MothBox\Mothbox\AI\trained_models\yolo11m_4500_imgsz1600_b1_2024-01-18\weights\yolo11m_4500_imgsz1600_b1_2024-01-18.pt"

IMGSZ = 1600  # Should be same imgsz as used in training for best results!


#SKIP_PREVIOUS_GENERATED = True #If you ran a detection before, or partially ran one, and do not want to re-create these detections leave this as TRUE. 
GEN_BOT_DET_EVENIF_HUMAN_EXISTS=True #if we encounter a human detection, but still want a parallel bot detection, make this true
OVERWRITE_PREV_BOT_DETECTIONS=False #if true, if there are previous machine detections, it will overwrite those machine detections with our current ones. This script should NEVER overwrite a human detection

#You should always leave Gen_Thumbnails as true. It will intelligently detect if a thumbnail exists and skip it if need be.
GEN_THUMBNAILS=True


#command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--input_path", default=INPUT_PATH, required=False)
parser.add_argument("--yolo_model",default=YOLO_MODEL, required=False)
parser.add_argument("--imgsz", default=IMGSZ,type=int, required=False)
args = parser.parse_args()

print(f"Processing {args.input_path} with model {args.yolo_model} and image size {args.imgsz}")

#if run without new args, this will just be the same as above, but if not, we can insert new args
INPUT_PATH=args.input_path
YOLO_MODEL=args.yolo_model
IMGSZ=args.imgsz



#~~~~Other Stuff~~~~~~~


def scan_for_images(date_folder_path):
  """Scans subfolders for JPEG files and returns a list of file paths."""
  jpeg_files = []
  for date_folder in date_folders:
    for filename in os.listdir(date_folder):
        if filename.endswith(".jpg"):
            jpeg_files.append(os.path.join(date_folder, filename))
  return jpeg_files

def is_valid_image(image_path): #in case there is an occasional corrupt image
  
  """Checks if an image file is valid using Pillow (PIL Fork)."""
  try:
    Image.open(image_path).verify()
    return True
  except (IOError, SyntaxError):
    return False

def process_jpg_files(img_files, date_folder):
    """
    Processes all *.jpg files within the specified date folders, creating a .json file
    for each image with the image path, height, and width.

    Args:
      date_folders: A list of paths to the date folders.
    """
    # Load the model
    model = YOLO(YOLO_MODEL)
    # Get the model's file name (including extension)
    model_name = os.path.basename(YOLO_MODEL)
    model_name="Mothbot_"+model_name #adding Mothbot prefix in case other things come along to do different processing
    # Get total number of JPEG files
    total_img_files = len(img_files)


    patch_folder_path=Path(date_folder+"/patches")
    patch_folder_path.mkdir(parents=True, exist_ok=True)


    for idx,filename in enumerate(img_files):

        image_path = os.path.join(date_folder, filename)
        human_json_path = os.path.join(date_folder, filename[:-4] + ".json")
        bot_json_path = os.path.join(date_folder, filename[:-4] + "_botdetection.json")

        #verify if the image file is ok
        if not is_valid_image(image_path):
            print(f"Skipping corrupt image: {image_path}")
            continue

        # Calculate progress
        processed_files = idx + 1
        progress = (processed_files / total_img_files) * 100

        # Print progress
        print()
        print()
        print(f"({progress:.2f}%) Processing:  {filename} ")


        # **Check 0: Ensure the image file has more than 0 bytes**
        if not os.path.isfile(image_path) or os.path.getsize(image_path) == 0:
            print(f"Skipping {filename}: Image file is missing or empty.")
            continue

        # **Check 1: Check if JSON file exists and if it's an HUman file**
        if os.path.isfile(human_json_path):
            print(human_json_path)
            print("Earlier Human detection file exists, check to see if we should skip it")

            try:
                with open(human_json_path, 'r') as json_file:
                    json_data = json.load(json_file)
                    #print(json_data)
                    if(GEN_THUMBNAILS):
                        json_data=generateThumbnailPatches_JSON(image_path, json_data, patch_folder_path,)
                        # Save the updated JSON data back to the file
                        with open(human_json_path, 'w') as json_file_write:
                            json.dump(json_data, json_file_write, indent=4)
                    if(GEN_BOT_DET_EVENIF_HUMAN_EXISTS==False):
                        #create the thumbnails from the detections still though
                        print("skipping-will not create bot detections in parallel with human detections")
                        continue #don't go and create a machine detection json as well
            except json.JSONDecodeError:
                print(f"error with HUMAN made {filename}: Corrupted JSON file.")

        # **Check 2: Check if bot made JSON file exists and if we should skip it**
        if os.path.isfile(bot_json_path):
            print(bot_json_path)
            print("Earlier BOT detection file exists, check to see if we should skip it, ")
            try:
                with open(bot_json_path, 'r') as json_file:
                    json_data = json.load(json_file)
                    #print(json_data)

                    if(OVERWRITE_PREV_BOT_DETECTIONS==False):
                        #create the thumbnails from the detections still though
                        if(GEN_THUMBNAILS):
                            json_data=generateThumbnailPatches_JSON(image_path, json_data, patch_folder_path,)
                            # Save the updated JSON data back to the file
                            with open(bot_json_path, 'w') as json_file_write:
                                json.dump(json_data, json_file_write, indent=4)

                        print("skipping previously generated detection files that were able to be opened")
                        continue #don't go ahead and process for detections, don't overwrite any exsiting bot .json files
            except json.JSONDecodeError:
                print(f"error with {filename}: Corrupted JSON file.")

        #~~~~~~~~Continue Processing to detect creatures~~~~~~~~~~~~~
        #We have been given the go ahead to overwrite any existing detection .json files, and if human data exists, we should still create a bot file in parallel.

        # Process with Yolo to detect any creatures
        print("Predict a new image: ", image_path)
        results = model.predict(source=image_path, imgsz=IMGSZ)

        # Extract OBB coordinates and crop
        shapes=[]
        for result in results:
            #print(result.obb.conf)
            for idx, obb in enumerate(result.obb.xyxyxyxy):

                #print(result.obb)
                points = obb.cpu().numpy().reshape((-1, 1, 2)).astype(int)
                cnt = points
                rect = cv2.minAreaRect(cnt)
                #print(obb)
                confidence=result.obb.conf[idx].item()

                print("rect: {}".format(rect)+"   conf: "+str(confidence))

                box = cv2.boxPoints(rect)
                box = np.intp(box)


                center, size, angle = rect[0], rect[1], rect[2]
                points = obb.cpu().numpy().reshape((-1, 1, 2)).astype(float)

                # Convert NumPy arrays to lists
                points = points.tolist() 
                points = [item for sublist in points for item in sublist]  #flatten


                shape = {
                    "points": points,
                    "direction": angle,
                    "score": float(confidence)

                }

                # print("bounding box: {}".format(box))
                # cv2.drawContours(result.orig_img, [box], 0, (0, 0, 255), 2)

                if(GEN_THUMBNAILS):
                    thepatchpath=generateThumbnailPatches(result.orig_img, image_path, rect, idx, model_name)
                shape["patch_path"]=thepatchpath
                shapes.append(shape)

                
        image = PIL.Image.open(image_path)
        width, height = image.size

        
        # Create JSON file
        data = {
            "version": model_name,
            "flags": {},
            #"flags": {"Mothbot": True, "automated": True},
            #"creator": "Mothbot",
            "imagePath": image_path,
            "imageHeight": height,
            "imageWidth": width,
            "description": "",
            "imageData": None,
        }

        # Create a new "shapes" list if it doesn't exist
        if "shapes" not in data:
            data["shapes"] = []

        # Add each shape to the list
        for shape in shapes:
            #print(shape)
            shape_data = {
            "kie_linking": [],
            "direction": shape["direction"],
            "label": "creature",  # Replace with your desired label
            "score": shape["score"],
            "group_id": None,
            "description": "",
            "difficult": "false",
            "shape_type": "rotation",
            "flags": {},
            "attributes": {},
            "points": shape["points"],
            "patch_path":shape["patch_path"]
            }
            data["shapes"].append(shape_data)


        with open(bot_json_path, "w") as f: #save as the bot detection.json path
            json.dump(data, f, indent=4)





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


def get_input_path():
    """Prompts user for image data path and returns it. Falls back to default path if empty."""
    while True:
        input_path = input(
            "Enter the path to the image data (or press Enter to use default): "
        )
        if input_path:
            return input_path
        else:
            print(f"Using default path: {INPUT_PATH}")
            return INPUT_PATH


def get_yolo_model_path():
    """
    Prompts the user for the YOLO model path. If no path is provided, the default path is used.

    Returns:
        str: The path to the YOLO model.
    """

    while True:
        model_path = input(
            "Enter the path to the YOLO model (or press Enter for default): "
        )
        if model_path:
            if os.path.exists(model_path):
                return model_path
            else:
                print("Invalid path. Please try again.")
        else:
            return YOLO_MODEL


def crop_rect_old(img, rect):
    # get the parameter of the small rectangle
    center, size, angle = rect[0], rect[1], rect[2]
    center, size = tuple(map(int, center)), tuple(map(int, size))

    # get row and col num in img
    height, width = img.shape[0], img.shape[1]

    # calculate the rotation matrix
    M = cv2.getRotationMatrix2D(center, angle, 1)
    # rotate the original image
    img_rot = cv2.warpAffine(img, M, (width, height))

    # now rotated rectangle becomes vertical, and we crop it
    img_crop = cv2.getRectSubPix(img_rot, size, center)

    return img_crop, img_rot


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

    return img_crop, img_rot


if __name__ == "__main__":
    print("Starting Mothbot Detection Script")
    #input_path = get_input_path()
    #model_path = get_yolo_model_path()
    #YOLO_MODEL = model_path

    input_path=INPUT_PATH #Cheat UI for now
    model_path=YOLO_MODEL
    date_folders = find_date_folders(input_path)

    
    for date_folder_path in date_folders:
        print(date_folders)
        images = scan_for_images(date_folder_path)
        process_jpg_files(images, date_folder_path)

    print("Finished Running Detections!")

