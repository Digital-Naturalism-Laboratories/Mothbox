import cv2
import numpy as np
import os

import random
import time

num_rows=0
num_cols=0

cell_width=0
cell_height=0


IMAGE_FOLDER = r"C:\Users\andre\Desktop\Mothbox data\PEA_PeaPorch_2024-09-01\2024-09-01\detected_and_cropped_images"


OUTPUT_SIZE=(1080, 1920)
SUBSAMPLE_SIZE=200 
UPDATE_INTERVAL=10

def visualize_all_images(image_files, output_size=(1080, 1920), subsample_size=300):
    """Visualizes all images in a folder as a single collage.

    Args:
        image_folder: The path to the folder containing the images.
        output_size: The desired size of the output image (tuple).

    Returns:
        The created collage image.
    """

    # Get a list of image files
    #image_files = [f for f in os.listdir(image_folder) if f.endswith('.jpg')]

    # Calculate grid dimensions
    #num_images = len(image_files)
    num_images = subsample_size
    global num_rows 
    num_rows= int(np.ceil(np.sqrt(num_images)))
    global num_cols
    num_cols = int(np.ceil(num_images / num_rows))

    # Calculate cell dimensions
    global cell_width
    global cell_height
    cell_width = output_size[1] // num_cols
    cell_height = output_size[0] // num_rows

    # Create output image
    output_image = np.zeros(output_size + (3,), dtype=np.uint8)
    print(f"Output image shape: {output_image.shape}")
    # Iterate over images and place them in the grid
    for i, image_file in enumerate(image_files):
        image_path = os.path.join(IMAGE_FOLDER, image_file)
        image = cv2.imread(image_path)

        # Check if the image was loaded successfully
        if image is None:
            print(f"Error loading image: {image_path}")
            continue  # Skip to the next image

        # Resize image to fit the cell
        resized_image = cv2.resize(image, (cell_width, cell_height))

        
        print(f"resized image shape: {resized_image.shape}")


        # Calculate position in the output image
        row = i // num_cols
        col = i % num_cols
        x_start = col * cell_width
        y_start = row * cell_height

        tolerance = 5  # Adjust tolerance as needed
        # Adjust x_start if necessary to prevent overflow
        if x_start + cell_width > output_size[1]:
            x_start = output_size[1] - cell_width

        if y_start + cell_height > output_size[0]:
            y_start = output_size[0] - cell_height

        print(x_start)
        print(cell_width)
        if abs(resized_image.shape[0] - cell_height) <= tolerance and abs(resized_image.shape[1] - cell_width) <= tolerance:
        # Paste the resized image
                # Place resized image in the output image
            output_image[y_start:y_start + cell_height, x_start:x_start + cell_width] = resized_image
            #print(i)
        else:
            print(f"Image {image_file} dimensions mismatch: {resized_image.shape} vs. {(cell_height, cell_width)}")


    return output_image


def create_dynamic_collage(image_folder, output_size=(1080, 1920), subsample_size=100, update_interval=50):
    """Creates a dynamic collage that updates with random images.

    Args:
        image_folder: The path to the folder containing the images.
        output_size: The desired size of the output image (tuple).
        subsample_size: The number of images to include in the initial collage.
        update_interval: The interval (in milliseconds) between updates.

    Returns:
        None
    """

    # Load all images
    image_files = [f for f in os.listdir(image_folder) if f.endswith('.jpg')]

    # Create initial collage
    collage = visualize_all_images(image_files, output_size, subsample_size)

    # Continuously update the collage
    while True:
        # Choose a random cell to update
        row, col = random.randint(0, num_rows - 1), random.randint(0, num_cols - 1)


        x_start = col * cell_width
        y_start = row * cell_height

        tolerance = 5  # Adjust tolerance as needed
        # Adjust x_start if necessary to prevent overflow
        if x_start + cell_width > output_size[1]:
            x_start = output_size[1] - cell_width

        if y_start + cell_height > output_size[0]:
            y_start = output_size[0] - cell_height

        random_image_file = random.choice(image_files)
        random_image = cv2.imread(os.path.join(image_folder, random_image_file))

        # Resize image to fit the cell
        resized_image = cv2.resize(random_image, (cell_width, cell_height))

        # Replace the cell with a random image
        collage[y_start:y_start + cell_height, x_start:x_start + cell_width] = resized_image

        # Display the updated collage
        cv2.imshow("Dynamic Collage", collage)

        # Wait for the update interval
        if cv2.waitKey(update_interval) == 27:
            break

# Example usage
#output_image = visualize_all_images(image_folder)

create_dynamic_collage(IMAGE_FOLDER, OUTPUT_SIZE, SUBSAMPLE_SIZE, UPDATE_INTERVAL)

# Display or save the output image
#cv2.imshow("Image Collage", output_image)
#cv2.waitKey(0)
#cv2.destroyAllWindows()