import os
import random
import subprocess
from operator import itemgetter
from PIL import Image

def create_video(folder_path, output_filename, fps=10, sort_by_size=False, sort_by_width=True):
  """
  Creates a video from all JPG images in a folder, shuffling them first.

  Args:
      folder_path: Path to the folder containing the JPG images.
      output_filename: Name of the output video file (e.g., "output.mp4").
      fps: Frames per second for the video (default: 10).
  """

  # Get all JPG image paths
  image_paths = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(".jpg")]

  # Shuffle the image paths randomly
  #random.shuffle(image_paths)

  # Optionally sort images by size
  if sort_by_size:
    image_sizes = [(path, os.stat(path).st_size) for path in image_paths]
    image_paths = [path for path, _ in sorted(image_sizes, key=itemgetter(1))]
    image_paths = list(reversed(image_paths))  # Reverse the sorted or unsorted list

  if sort_by_width:
      def get_width(path):
          # Open the image to get its width
          from PIL import Image
          img = Image.open(path)
          return img.width  # Return only the width

      # Sort image paths by width using a custom key function
      image_paths = sorted(image_paths, key=get_width)
      image_paths = list(reversed(image_paths))  # Reverse the sorted or unsorted list

  '''
  # Find the largest image size
  max_width, max_height = 0, 0
  for f in os.listdir(folder_path):
    if f.endswith(".jpg"):
      image_path = os.path.join(folder_path, f)
      img = Image.open(image_path)
      max_width = max(max_width, img.width)
      max_height = max(max_height, img.height)
  '''

  # Create a temporary file listing the images
  with open("image_list.txt", "w") as f:
    f.writelines(f"file '{path}'\n" for path in image_paths)
    #f.writelines(f"'file '{path}'\n'" for path in image_paths)
  # Build the ffmpeg command
  duration_per_image=4
  bitrate="200M"
  crf = "8"
  max_width=1920
  max_height=1080
  #
  #command = ["ffmpeg", "-f", "concat", "-safe", "0", "-i", "image_list.txt", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-framerate", str(fps), output_filename]
  #command = ["ffmpeg", "-f", "concat", "-safe", "0", "-i", "image_list.txt", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-framerate", str(fps), output_filename, "-loglevel", "error","-t", str(duration_per_image), "-s", f"{max_width}x{max_height}","-b:v", bitrate,]

  #lossless png  
  #command = ["ffmpeg", "-f", "concat", "-safe", "0", "-i", "image_list.txt", "-c:v", "png", "-pix_fmt", "yuv420p", "-framerate", str(fps), output_filename, "-loglevel", "error","-t", str(duration_per_image),"-b:v", bitrate,]
  command = ["ffmpeg", "-f", "concat", "-safe", "0", "-i", "image_list.txt", "-c:v", "png", "-pix_fmt", "yuv420p", "-framerate", str(fps), output_filename, "-loglevel", "error","-t", str(duration_per_image),"-b:v", bitrate, "-s", f"{max_width}x{max_height}"]
  
  #crf 
  #command = ["ffmpeg", "-f", "concat", "-safe", "0", "-i", "image_list.txt", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-framerate", str(fps), output_filename, "-loglevel", "error","-t", str(duration_per_image),"-crf", str(crf),]

  # Execute the ffmpeg command
  subprocess.run(command, check=True)

  # Clean up the temporary file
  os.remove("image_list.txt")

# Example usage
folder_path = "detected_and_cropped_images"
#output_filename = "shuffled_images.mp4"
#output_filename = "time_ordered_images.mp4"
output_filename = "width_ordered_images.mp4"

create_video(folder_path, output_filename, 10, False)