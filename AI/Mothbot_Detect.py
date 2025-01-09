#!/usr/bin/env python3

import cv2
from ultralytics import YOLO
import numpy as np
import os
import re
import json
import PIL.Image
from pathlib import Path

from Mothbot_GenThumbnails import generateThumbnailPatches, generateThumbnailPatches_JSON


#~~~~Variables to Change~~~~~~~

INPUT_PATH = r"D:\Panama\Boquete_Houseside_CuatroTopo _2025-01-03\2025-01-03"  # raw string

YOLO_MODEL = r"C:\Users\andre\Documents\GitHub\Mothbox\AI\trained_models\best_3000Images_batch2_1408px.pt"

IMGSZ = 1408  # Should be same imgsz as used in training for best results!

GEN_THUMBNAILS=True

#SKIP_PREVIOUS_GENERATED = True #If you ran a detection before, or partially ran one, and do not want to re-create these detections leave this as TRUE. 
GEN_BOT_DET_EVENIF_HUMAN_EXISTS=True #if we encounter a human detection, but still want a parallel bot detection, make this true
OVERWRITE_PREV_BOT_DETECTIONS=False #if true, if there are previous machine detections, it will overwrite those machine detections with our current ones. This script should NEVER overwrite a human detection

#~~~~Other Stuff~~~~~~~


def scan_for_images(date_folder_path):
  """Scans subfolders for JPEG files and returns a list of file paths."""
  jpeg_files = []
  for date_folder in date_folders:
    for filename in os.listdir(date_folder):
        if filename.endswith(".jpg"):
            jpeg_files.append(os.path.join(date_folder, filename))
  return jpeg_files


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


        # Calculate progress
        processed_files = idx + 1
        progress = (processed_files / total_img_files) * 100

        # Print progress
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
                        generateThumbnailPatches_JSON(image_path, json_data, patch_folder_path,)
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
                            generateThumbnailPatches_JSON(image_path, json_data, patch_folder_path,)

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

                shapes.append(shape)
                # print("bounding box: {}".format(box))
                # cv2.drawContours(result.orig_img, [box], 0, (0, 0, 255), 2)

                if(GEN_THUMBNAILS):
                    generateThumbnailPatches(result.orig_img, image_path, rect, idx, model_name)

                
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
            "points": shape["points"]
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

