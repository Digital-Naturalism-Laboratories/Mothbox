import os
ROOT_FOLDER = r'E:\Panama'

def find_folders_with_json(root_folder):
  """
  Finds folders that contain at least one *.json file.

  Args:
    root_folder: The root folder to search.
  """

  for root, dirs, files in os.walk(root_folder):
    if any(file.endswith('.json') and file not in ['metadata.json', 'samples.json'] for file in files):
         print(root)

# Replace '/path/to/your/folder' with the actual path to your root folder
find_folders_with_json(ROOT_FOLDER)