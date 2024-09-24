import cv2
import numpy as np
import os

import random
import time
import unicodedata
num_rows=0
num_cols=0

cell_width=0
cell_height=0


IMAGE_FOLDER = r"C:\Users\andre\Desktop\x-anylabeling-matting"


OUTPUT_SIZE=(1080, 1080) # height then width
SUBSAMPLE_SIZE=64 
UPDATE_INTERVAL=1

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
    #print(f"Output image shape: {output_image.shape}")
    # Iterate over images and place them in the grid
    for i, image_file in enumerate(image_files):
        random_image_file = random.choice(image_files)

        #image_path = os.path.join(IMAGE_FOLDER, image_file)
        image_path = os.path.join(IMAGE_FOLDER, random_image_file)

        #random_image = cv2.imread(np.fromfile(os.path.join(image_folder, normalized_filename),dtype=np.uint8))

        f = open(image_path, "rb")  # have to do this silly stuff where we open it because imread cannot read paths with accents!
        b = f.read()
        f.close()

        b = np.frombuffer(b, dtype=np.uint8)
        image = cv2.imdecode(b, cv2.IMREAD_COLOR)
        #image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

        # Check if the image was loaded successfully
        if image is None:
            #print(f"Error loading image: {image_path}")
            continue  # Skip to the next image

        # Resize image to fit the cell
        resized_image = cv2.resize(image, (cell_width, cell_height))

        
        #print(f"resized image shape: {resized_image.shape}")


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

        #print(x_start)
        #print(cell_width)
        if abs(resized_image.shape[0] - cell_height) <= tolerance and abs(resized_image.shape[1] - cell_width) <= tolerance:
        # Paste the resized image
                # Place resized image in the output image
            output_image[y_start:y_start + cell_height, x_start:x_start + cell_width] = resized_image
            #print(i)
        else:
            print(f"Image {image_file} dimensions mismatch: {resized_image.shape} vs. {(cell_height, cell_width)}")


    return output_image


def create_dynamic_collage(image_folder, output_size=(1080, 1920), subsample_size=100, update_interval=30,video_filename="collage.mp4"):
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
    image_files = [f for f in os.listdir(image_folder) if f.endswith('.jpg') or f.endswith('.png')]

    # Create initial collage
    collage = visualize_all_images(image_files, output_size, subsample_size)

    # Create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(video_filename, cv2.VideoWriter_fourcc('m','p','4','v'),30.0, (output_size[1],output_size[0]))  # 30 FPS



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

        f = open(os.path.join(image_folder, random_image_file), "rb")
        b = f.read()
        f.close()

        b = np.frombuffer(b, dtype=np.uint8)
        random_image = cv2.imdecode(b, cv2.IMREAD_COLOR);



        #normalized_filename = unicodedata.normalize('NFKD', random_image_file).encode('utf-8', 'ignore').decode('utf-8')
        #random_image = cv2.imread(os.path.join(image_folder, normalized_filename), cv2.IMREAD_UNCHANGED)
       #np.fromfile(os.path.join("data/chapter_1/capd_yard_signs", filename).replace('\\','/'), dtype=np.uint8
        # Resize image to fit the cell
        resized_image = cv2.resize(random_image, (cell_width, cell_height))

        # Replace the cell with a random image
        collage[y_start:y_start + cell_height, x_start:x_start + cell_width] = resized_image

        # Write the frame to the video
        video_writer.write(collage)


        # Create the window in fullscreen mode
        cv2.namedWindow("Dynamic Collage", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("Dynamic Collage", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)


        # Display the updated collage
        cv2.imshow("Dynamic Collage", collage)

        # Wait for the update interval
        if cv2.waitKey(update_interval) == 27:
            break
    # Release the video writer and destroy windows
    video_writer.release()
    cv2.destroyAllWindows()
# Example usage
#output_image = visualize_all_images(image_folder)

create_dynamic_collage(IMAGE_FOLDER, OUTPUT_SIZE, SUBSAMPLE_SIZE, UPDATE_INTERVAL)

# Display or save the output image
#cv2.imshow("Image Collage", output_image)
#cv2.waitKey(0)
#cv2.destroyAllWindows()