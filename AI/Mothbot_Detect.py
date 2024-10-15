import cv2
from ultralytics import YOLO
import numpy as np
import os
import re
import json
import PIL.Image


INPUT_PATH = r"C:\Users\andre\Desktop\Mothbox data\PEA_PeaPorch_AdeptTurca_2024-09-01"  # raw string
YOLO_MODEL = r"C:\Users\andre\Documents\GitHub\Mothbox\AI\trained_models\Dataset19Mixed1230_semiC.pt"
IMGSZ = 1408  # Should be same imgsz as used in training for best results!


def process_jpg_files(date_folders):
    """
    Processes all *.jpg files within the specified date folders, creating a .json file
    for each image with the image path, height, and width.

    Args:
      date_folders: A list of paths to the date folders.
    """
    # Load the model
    model = YOLO(YOLO_MODEL)

    for date_folder in date_folders:
        for filename in os.listdir(date_folder):
            if filename.endswith(".jpg"):
                image_path = os.path.join(date_folder, filename)
                json_path = os.path.join(date_folder, filename[:-4] + ".json")

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


def process_subdirectories(input_path, out_path):
    """Processes subdirectories within the specified input path, excluding "output_path".

    Args:
    input_path: The path to the directory containing subdirectories.
    out_path: Path to the subdirectory to exclude
    """

    for subdir in os.listdir(input_path):
        subdirectory_path = os.path.join(input_path, subdir)
        if (
            os.path.isdir(subdirectory_path)
            and subdirectory_path != out_path
            and not output_folder in subdirectory_path
        ):

            print(f"Processing subdirectory: {subdirectory_path}")
            process_files_in_directory(subdirectory_path)


def process_files_in_directory(subdirectory_path):
    """Processes files within a specified subdirectory.

    Args:
    subdirectory_path: The path to the subdirectory containing files.
    """

    # Example: Print all file names in the subdirectory
    for file in os.listdir(subdirectory_path):
        file_path = os.path.join(subdirectory_path, file)
        if os.path.isfile(file_path):
            print(f"File: {file_path}")

    sub_output_folder = "detected_and_cropped_images"
    sub_output_path = subdirectory_path + "/" + output_folder
    # Create the output directory if it doesn't exist
    if not os.path.exists(sub_output_path):
        os.makedirs(sub_output_path)

    img_list = [f for f in os.listdir(subdirectory_path) if f.endswith(".jpg")]

    if not img_list:
        # No imgs were found in base level
        print("No .jpg images found in the input path: " + subdirectory_path)
    else:
        # Analyze the files
        print(f"Found {len(img_list)} .jpg images.")
        i = 1
        for file in img_list:
            filename = os.path.splitext(file)[0]
            print(filename)
            data = os.path.join(subdirectory_path, file)
            print("\n img # " + str(i) + "  out of " + str(len(img_list)))
            i = i + 1
            # Run inference
            print("Predict a new image")
            results = model.predict(source=data, imgsz=IMGSZ)

            # Extract OBB coordinates and crop
            for result in results:
                for idx, obb in enumerate(result.obb.xyxyxyxy):

                    points = obb.cpu().numpy().reshape((-1, 1, 2)).astype(int)
                    cnt = points
                    rect = cv2.minAreaRect(cnt)
                    print("rect: {}".format(rect))

                    box = cv2.boxPoints(rect)
                    box = np.intp(box)
                    # print("bounding box: {}".format(box))
                    # cv2.drawContours(result.orig_img, [box], 0, (0, 0, 255), 2)

                    # img_crop will the cropped rectangle, img_rot is the rotated image
                    img_crop, img_rot = crop_rect(result.orig_img, rect)
                    # cv2.imwrite("cropped_img.jpg", img_crop)
                    cv2.imwrite(
                        os.path.join(sub_output_path, f"{filename}_crop_{idx}.jpg"),
                        img_crop,
                    )

                    # mask = cv2.fillPoly(np.zeros_like(result.orig_img), [points], (255, 255, 255))
                    # cropped_img = cv2.bitwise_and(result.orig_img, mask)
                    # cv2.waitKey(0)


if __name__ == "__main__":
    '''
    input_path = get_input_path()
    model_path = get_yolo_model_path()

    YOLO_MODEL = model_path
    
    '''
    input_path=INPUT_PATH #Cheat UI for now

    output_folder = "detected_and_cropped_images"
    output_path = input_path + "/" + output_folder

    date_folders = find_date_folders(input_path)
    print(date_folders)

    process_jpg_files(date_folders)
    # process_files_in_directory(input_path)
    # process_subdirectories(input_path,output_path)
