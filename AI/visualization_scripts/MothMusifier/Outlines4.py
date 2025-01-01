import cv2
import numpy as np
import random

def get_random_pastel_color():
  """
  Generates a random pastel color in BGR format.
  """
  pastel_range = 0  # Adjust for pastel intensity
  r = random.randint(pastel_range, 255)
  g = random.randint(pastel_range, 255)
  b = random.randint(pastel_range, 255)
  return b, g, r



def overlay_image_with_alpha_np(background_img, overlay_img):
  """
  Overlays an image (overlay) with transparency onto a background image.

  Args:
    background_img: Numpy array of the background image (shape: H x W x 4, 
                      where 4 channels are R, G, B, A).
    overlay_img: Numpy array of the overlay image (shape: H x W x 4, 
                      where 4 channels are R, G, B, A).

  Returns:
    The resulting blended image as a NumPy array.
  """

  # Ensure images have the same dimensions
  if background_img.shape != overlay_img.shape:
    raise ValueError("Images must have the same dimensions.")

  # Extract alpha channels
  overlay_alpha = overlay_img[:, :, 3] / 255.0  # Normalize to 0-1
  background_alpha = background_img[:, :, 3] / 255.0

  # Create masks
  overlay_mask = overlay_alpha[:, :, np.newaxis]  # Create a 3-channel mask
  background_mask = 1.0 - overlay_alpha[:, :, np.newaxis] 

  # Create masked images
  masked_overlay = overlay_img[:, :, :3] * overlay_mask
  masked_background = background_img[:, :, :3] * background_mask

  # Combine masked images
  blended_img = masked_background + masked_overlay

  # Combine alpha channels
  blended_alpha = np.maximum(overlay_alpha, background_alpha)  # Use maximum alpha

  # Combine RGB and alpha channels
  blended_img = np.concatenate((blended_img, blended_alpha[:, :, np.newaxis]), axis=-1)

  return blended_img



def overlay_color_with_mask(background_img, mask_img, color):
  """
  Overlays a chosen color onto the background image within the shape of the mask.

  Args:
    background_img: Numpy array of the background image (H x W x C).
    mask_img: Numpy array of the mask image (H x W).
    color: Tuple of (B, G, R) values for the overlay color.

  Returns:
    Numpy array of the resulting image.
  """

  # Ensure images have the same dimensions
  if background_img.shape != mask_img.shape:
    #print(background_img.shape)
    #print(mask_img.shape)
      # Create a 3-channel mask
    mask_rgb = cv2.cvtColor(mask_img, cv2.COLOR_GRAY2BGR) 
    mask_rgb = mask_rgb / 255.0  # Normalize to 0-1
    #raise ValueError("Background and mask images must have the same dimensions.")
  else:
     mask_rgb=mask_img



  # Create a colored overlay
  color_overlay = np.full(background_img.shape, color, dtype=np.uint8) 

  # Apply the mask to the colored overlay
  masked_overlay = color_overlay * mask_rgb
  #cv2.imshow("masked overlay ", masked_overlay.astype(np.uint8)) 

  # Create an inverted mask for the background
  background_mask = 1.0 - mask_rgb

  # Apply the inverted mask to the background
  masked_background = background_img * background_mask

  #cv2.imshow("masked background ", masked_background.astype(np.uint8)) 


  # Combine the masked images
  result_img = masked_background + masked_overlay

  return result_img
def animate_alpha_overlay(image_path, max_iterations=30, delay=5):
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
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)) 
        shrinkkernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)) 

        # Initialize iteration counter
        iterations = 20
        old_dilated_alpha=thresholded_alpha

        # Create a 3-channel image from dilated alpha
        old_dilated_alpha = cv2.cvtColor(old_dilated_alpha, cv2.COLOR_GRAY2BGR) 
        non_dilated=old_dilated_alpha
        old_dilated_alpha=image[:, :, :3]
        i=0 
        while True:

            # Get a random pastel color
            pastel_color = get_random_pastel_color()

            # Dilate the alpha channel
            dilated_alpha=old_dilated_alpha
            dilated_alpha = cv2.dilate(old_dilated_alpha, kernel, iterations=2)
            dilated_alpha = cv2.blur(dilated_alpha,(25,25))
            dilated_alpha = cv2.erode(dilated_alpha, kernel, iterations=2)

            dilated_alpha = cv2.filter2D(dilated_alpha,-100, shrinkkernel)



            cv2.imshow("Dilated_alpha ", dilated_alpha.astype(np.uint8)) 

            # Create a mask for the dilated area
            dilated_mask = dilated_alpha.copy() / 255.0
            mask = non_dilated.copy() / 255.0
            


            # Create a colored background
            colored_background = np.zeros_like(old_dilated_alpha)
            # Create an array of pastel_color with the same shape as the masked region
            pastel_color_array = np.full(dilated_mask.shape, pastel_color) 
            colored_background[mask > 0] = pastel_color_array[mask > 0] 
            #dilated_alpha[mask > 0] = pastel_color_array[mask > 0] 

            #cv2.imshow("Thresholded_alpha ", thresholded_alpha.astype(np.uint8)) 

            dilated_alpha=overlay_color_with_mask(dilated_alpha,thresholded_alpha, pastel_color)

            #dilated_alpha=overlay_image_with_alpha_np(dilated_alpha,colored_background)
            #dilated_alpha=cv2.addWeighted(dilated_alpha, .9, colored_background, .1, 0)
            cv2.imshow("Dilated with overlay ", dilated_alpha.astype(np.uint8)) 
            #input()
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
            print(old_dilated_alpha.shape)

            # Reset if maximum iterations reached
            i+=1
            if i > max_iterations:
                i=0
                old_dilated_alpha=image[:, :, :3]

    except Exception as e:
        print(f"Error: {e}")
        cv2.destroyAllWindows()


if __name__ == "__main__":
    image_path = r"C:\Users\andre\Desktop\x-anylabeling-matting\onlybig\wrong_2024_09_03__23_07_19_HDR0_crop_3.png"  # Replace with the actual path
    animate_alpha_overlay(image_path)



