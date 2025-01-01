from __future__ import print_function
import cv2 as cv
import numpy as np
import argparse
 
#src = None
src = r"C:\Users\andre\Desktop\x-anylabeling-matting\onlybig\wrong_2024_09_03__23_07_19_HDR0_crop_3.png"  # Replace with the actual path

erosion_size = 0
max_elem = 2
max_kernel_size = 221
title_trackbar_element_shape = 'Element:\n 0: Rect \n 1: Cross \n 2: Ellipse'
title_trackbar_kernel_size = 'Kernel size:\n 2n +1'
title_erosion_window = 'Erosion Demo'
title_dilation_window = 'Dilation Demo'
 
 
 
def main(image):
    global src
    # Read the image with alpha channel
    image_path=r"C:\Users\andre\Desktop\x-anylabeling-matting\onlybig\wrong_2024_09_03__23_07_19_HDR0_crop_3.png"

    src = cv.imread(image_path, cv.IMREAD_UNCHANGED)

    # Extract the alpha channel
    #src = src[:, :, 3] 


    if src is None:
        print('Could not open or find the image: ', image)
        exit(0)
 
    cv.namedWindow(title_erosion_window)
    cv.createTrackbar(title_trackbar_element_shape, title_erosion_window, 0, max_elem, erosion)
    cv.createTrackbar(title_trackbar_kernel_size, title_erosion_window, 0, max_kernel_size, erosion)
 
    cv.namedWindow(title_dilation_window)
    cv.createTrackbar(title_trackbar_element_shape, title_dilation_window, 0, max_elem, dilatation)
    cv.createTrackbar(title_trackbar_kernel_size, title_dilation_window, 0, max_kernel_size, dilatation)
 
    erosion(0)
    dilatation(0)
    cv.waitKey()
 
 
# optional mapping of values with morphological shapes
def morph_shape(val):
    if val == 0:
        return cv.MORPH_RECT
    elif val == 1:
        return cv.MORPH_CROSS
    elif val == 2:
        return cv.MORPH_ELLIPSE
 
 
 
def erosion(val):
    erosion_size = cv.getTrackbarPos(title_trackbar_kernel_size, title_erosion_window)
    erosion_shape = morph_shape(cv.getTrackbarPos(title_trackbar_element_shape, title_erosion_window))
 
    
    element = cv.getStructuringElement(erosion_shape, (2 * erosion_size + 1, 2 * erosion_size + 1),
                                       (erosion_size, erosion_size))
    
    erosion_dst = cv.erode(src, element)
    cv.imshow(title_erosion_window, erosion_dst)
 
 
 
 
def dilatation(val):
    dilatation_size = cv.getTrackbarPos(title_trackbar_kernel_size, title_dilation_window)
    dilation_shape = morph_shape(cv.getTrackbarPos(title_trackbar_element_shape, title_dilation_window))
 
    element = cv.getStructuringElement(dilation_shape, (2 * dilatation_size + 1, 2 * dilatation_size + 1),
                                       (dilatation_size, dilatation_size))
    
    # Extract the alpha channel
    #alpha_channel = src[:, :, 3] 
    dilatation_dst = cv.dilate(src, element)
    cv.imshow(title_dilation_window, dilatation_dst)
 
 
 
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Code for Eroding and Dilating tutorial.')
    parser.add_argument('--input', help='Path to input image.', default= r"C:\Users\andre\Pictures\test_color_dilate.png")
    args = parser.parse_args()
 
    main(args.input)