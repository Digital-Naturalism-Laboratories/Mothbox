import cv2
import numpy as np
import os

def visualize_all_images(image_folder, output_size=(640, 640)):
    """Visualizes all images in a folder as a single collage.

    Args:
        image_folder: The path to the folder containing the images.
        output_size: The desired size of the output image (tuple).

    Returns:
        The created collage image.
    """

    # Get a list of image files
    image_files = [f for f in os.listdir(image_folder) if f.endswith('.jpg') or f.endswith('.png')]

    # Calculate grid dimensions
    num_images = len(image_files)
    num_rows = int(np.ceil(np.sqrt(num_images)))
    num_cols = int(np.ceil(num_images / num_rows))

    # Calculate cell dimensions
    cell_width = output_size[1] // num_cols
    cell_height = output_size[0] // num_rows

    # Create output image
    output_image = np.zeros(output_size + (3,), dtype=np.uint8)
    print(f"Output image shape: {output_image.shape}")
    # Iterate over images and place them in the grid
    for i, image_file in enumerate(image_files):
        image_path = os.path.join(image_folder, image_file)
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

# Example usage
image_folder = r"C:\Users\andre\Desktop\x-anylabeling-matting"
output_image = visualize_all_images(image_folder)

# Display or save the output image
cv2.imshow("Image Collage", output_image)
cv2.waitKey(0)
cv2.destroyAllWindows()