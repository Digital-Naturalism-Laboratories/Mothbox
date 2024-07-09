import cv2
from ultralytics import YOLO
import numpy as np
import os

def crop_rect(img, rect):
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


if __name__ == '__main__':

    # Load the model
    model = YOLO("runs/obb/train23/weights/best.pt")
    input_path = "predictme"
    output_path = "predictme_crops"
    img_list = os.listdir(input_path)
    i=1
    for file in img_list:
        filename = os.path.splitext(file)[0]
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

