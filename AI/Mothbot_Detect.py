import cv2
from ultralytics import YOLO
import numpy as np
import os
import re
import json
import PIL.Image


INPUT_PATH = r"C:\Users\andre\Desktop\Mothbox data\PEA_PeaPorch_AdeptTurca_2024-09-01\2024-09-01"  # raw string
YOLO_MODEL = r"C:\Users\andre\Documents\GitHub\Mothbox\AI\trained_models\train14_3000Images_batch2_1408px\weights\best.pt"
IMGSZ = 1408  # Should be same imgsz as used in training for best results!


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
    # Get total number of JPEG files
    total_img_files = len(img_files)

    for idx,filename in enumerate(img_files):

        image_path = os.path.join(date_folder, filename)
        json_path = os.path.join(date_folder, filename[:-4] + ".json")

        # Calculate progress
        processed_files = idx + 1
        progress = (processed_files / total_img_files) * 100

        # Print progress
        print(f"({progress:.2f}%) Processing:  {filename} ")


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

                '''
                # img_crop will the cropped rectangle, img_rot is the rotated image
                img_crop, img_rot = crop_rect(result.orig_img, rect)
                # cv2.imwrite("cropped_img.jpg", img_crop)
                cv2.imwrite(
                    os.path.join(sub_output_path, f"{filename}_crop_{idx}.jpg"),
                    img_crop,
                )
                '''
                
        image = PIL.Image.open(image_path)
        width, height = image.size

        # Create JSON file
        data = {
            "version": "2.4.3",
            "flags": {},
            "creator": "Mothbot",
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


        with open(json_path, "w") as f:
            json.dump(data, f, indent=4)





def find_date_folders(directory):
    """
    Recursively searches through a directory and its subdirectories for folders
    with names in the YYYY-MM-DD format.

    Args:
      directory: The directory to search.

    Returns:
      A list of paths to the found folders.
    """

    date_regex = r"^\d{4}-\d{2}-\d{2}$"
    folders = []

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
    input_path = get_input_path()
    model_path = get_yolo_model_path()

    YOLO_MODEL = model_path
    
    #input_path=INPUT_PATH #Cheat UI for now

    date_folders = find_date_folders(input_path)

    
    for date_folder_path in date_folders:
        print(date_folders)
        images = scan_for_images(date_folder_path)
        process_jpg_files(images, date_folder_path)

