import cv2
from ultralytics import YOLO
import numpy as np
import os

INPUT_PATH=r"E:\Panama\Totumas_Summit_StudyCod_2024-09-21\2024-09-23" #raw string
YOLO_MODEL = r"C:\Users\andre\Desktop\mothbox_dataset_3000_2024-10-10\train14_3000Images_batch2_1408px\weights\best.pt"
IMGSZ=1408 # Should be same imgsz as used in training for best results!


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

def crop_rect(img, rect, interpolation=cv2.INTER_LINEAR): # cv2.INTER_LANCZOS4  cv2.INTER_LINEAR cv2.INTER_CUBIC
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
        if os.path.isdir(subdirectory_path) and subdirectory_path != out_path and not output_folder in subdirectory_path:

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
    
    sub_output_folder="detected_and_cropped_images"
    sub_output_path = subdirectory_path+"/"+output_folder
    # Create the output directory if it doesn't exist
    if not os.path.exists(sub_output_path):
        os.makedirs(sub_output_path)


    img_list = [f for f in os.listdir(subdirectory_path) if f.endswith(".jpg")]
    
    if not img_list:
        # No imgs were found in base level
        print("No .jpg images found in the input path: "+subdirectory_path)
    else:
        # Analyze the files
        print(f"Found {len(img_list)} .jpg images.")
        i=1
        for file in img_list:
            filename = os.path.splitext(file)[0]
            print(filename)
            data = os.path.join(subdirectory_path, file)
            print("\n img # "+str(i)+"  out of "+str(len(img_list)))
            i=i+1
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
                    #cv2.drawContours(result.orig_img, [box], 0, (0, 0, 255), 2)

                    # img_crop will the cropped rectangle, img_rot is the rotated image
                    img_crop, img_rot = crop_rect(result.orig_img, rect)
                    #cv2.imwrite("cropped_img.jpg", img_crop)
                    cv2.imwrite(os.path.join(sub_output_path, f"{filename}_crop_{idx}.jpg"), img_crop)

                    #mask = cv2.fillPoly(np.zeros_like(result.orig_img), [points], (255, 255, 255))
                    #cropped_img = cv2.bitwise_and(result.orig_img, mask)
                    #cv2.waitKey(0)



if __name__ == '__main__':

    # Load the model
    model = YOLO(YOLO_MODEL)

    print(INPUT_PATH)
    #input_path = input_path.encode('utf-8').decode('mbcs')
    INPUT_PATH= os.path.normpath(INPUT_PATH)
    print(INPUT_PATH)
    output_folder="detected_and_cropped_images"
    output_path = INPUT_PATH+"/"+output_folder


    '''
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    






    #First analyze any images that may be in the base folder
    #img_list = os.listdir(input_path)
    img_list = [f for f in os.listdir(input_path) if f.endswith(".jpg")]
    
    if not img_list:
        # No imgs were found in base level
        print("No .jpg images found in the input path.")
    else:
        # Analyze the files
        print(f"Found {len(img_list)} .jpg images.")
        i=1
        for file in img_list:
            filename = os.path.splitext(file)[0]
            print(filename)
            #if(filename==output_folder)
            data = os.path.join(input_path, file)
            print("\n img # "+str(i)+"  out of "+str(len(img_list)))
            i=i+1
            # Run inference
            print("Predict a new image")
            results = model.predict(source=data, imgsz=1024)
            
            # Extract OBB coordinates and crop
            for result in results:
                for idx, obb in enumerate(result.obb.xyxyxyxy):


                    points = obb.cpu().numpy().reshape((-1, 1, 2)).astype(int)
                    cnt = points
                    rect = cv2.minAreaRect(cnt)
                    print("rect: {}".format(rect))

                    box = cv2.boxPoints(rect)
                    box = np.int0(box)
                    # print("bounding box: {}".format(box))
                    #cv2.drawContours(result.orig_img, [box], 0, (0, 0, 255), 2)

                    # img_crop will the cropped rectangle, img_rot is the rotated image
                    img_crop, img_rot = crop_rect(result.orig_img, rect)
                    #cv2.imwrite("cropped_img.jpg", img_crop)
                    cv2.imwrite(os.path.join(output_path, f"{filename}_crop_{idx}.jpg"), img_crop)

                    #mask = cv2.fillPoly(np.zeros_like(result.orig_img), [points], (255, 255, 255))
                    #cropped_img = cv2.bitwise_and(result.orig_img, mask)
                    cv2.waitKey(0)
    '''
    process_files_in_directory(INPUT_PATH)
    process_subdirectories(INPUT_PATH,output_path)
