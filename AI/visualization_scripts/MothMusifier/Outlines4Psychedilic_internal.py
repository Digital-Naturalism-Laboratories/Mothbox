import cv2
import numpy as np
import random

def get_random_pastel_color():
  """
  Generates a random pastel color in BGR format.
  """
  pastel_range = 150  # Adjust for pastel intensity
  r = random.randint(pastel_range, 255)
  g = random.randint(pastel_range, 255)
  b = random.randint(pastel_range, 255)
  return b, g, r

def animate_alpha_overlay(image_path, max_iterations=120, delay=50):
    """
    Reads a PNG image with transparency, extracts the alpha channel, 
    animates the dilation, overlays the original image on top 
    of the dilated alpha channel with random pastel colors.

    Args:
        image_path: Path to the PNG image file.
        max_iterations: Maximum number of dilation iterations.
        delay: Delay between frames in milliseconds.
    """

    try:
        # Read the image with alpha channel
        image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

        # Extract the alpha channel
        alpha_channel = image[:, :, 3]

        # Threshold the alpha channel
        _, thresholded_alpha = cv2.threshold(alpha_channel, 127, 255, cv2.THRESH_BINARY)

        # Define a kernel for dilation
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)) 

        # Initialize iteration counter
        iterations = 5
        old_dilated_alpha=thresholded_alpha

        # Create a 3-channel image from dilated alpha
        old_dilated_alpha = cv2.cvtColor(old_dilated_alpha, cv2.COLOR_GRAY2BGR) 
        non_dilated=old_dilated_alpha
        while True:

            # Get a random pastel color
            pastel_color = get_random_pastel_color()

            # Dilate the alpha channel
            dilated_alpha = cv2.dilate(old_dilated_alpha, kernel, iterations=iterations)
            dilated_alpha = cv2.blur(dilated_alpha,(10,10))



            # Create a mask for the dilated area
            dilated_mask = dilated_alpha.copy() / 255.0
            mask = non_dilated.copy() / 255.0
            


            # Create a colored background
            colored_background = np.zeros_like(old_dilated_alpha)
            # Create an array of pastel_color with the same shape as the masked region
            pastel_color_array = np.full(dilated_mask.shape, pastel_color) 
            colored_background[mask > 0] = pastel_color_array[mask > 0] 

            dilated_alpha=dilated_alpha+colored_background
            
            cv2.imshow("Dilated ", dilated_alpha.astype(np.uint8)) 

            #colored_background=cv2.dilate(colored_background,kernel, iterations=iterations)
            # Extract only the color channels from the original image
            image_rgb = image[:, :, :3] 

            # Apply the mask to the original image
            masked_image = image_rgb * mask 

            # Combine the colored background and the masked image
            blended_image = dilated_alpha + masked_image

            # Display the blended image
            cv2.imshow("Animated Overlay", blended_image.astype(np.uint8)) 
            cv2.waitKey(delay)

            # Increment iteration counter
            #iterations += 1
            old_dilated_alpha=dilated_alpha
            # Reset if maximum iterations reached
            if iterations > max_iterations:
                iterations = 0

    except Exception as e:
        print(f"Error: {e}")
        cv2.destroyAllWindows()


if __name__ == "__main__":
    image_path = r"C:\Users\andre\Desktop\x-anylabeling-matting\onlybig\wrong_2024_09_03__23_07_19_HDR0_crop_3.png"  # Replace with the actual path
    animate_alpha_overlay(image_path)



