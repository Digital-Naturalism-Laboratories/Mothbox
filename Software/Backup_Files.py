'''
Backupper Script
This script is for folks collecting lots of data automatically that needs to get backed up at certain intervals

for instance saving a bunch of files to a folder, but then automatically copying them to larger external devices

This script first defines paths for the desktop, photos folder, and backup folder name. Then, it defines functions to:

    Get the storage information (total and available space) of a path.
    Find the largest external storage device connected.
    Copy all files from one folder to another while preserving file metadata.

Finally, the script checks if the photos folder exists and then finds the largest external storage. It compares the total space and available space on both the desktop and the external storage to determine if the external storage has enough space for the backup. If so, it creates a backup folder on the external storage and copies the photos. Otherwise, it informs the user about insufficient space.

Note:

    This script assumes the user running the script has read and write permissions to the desktop and any external storage devices.
    You might need to adjust the user name in desktop_path depending on your Raspberry Pi setup.


'''

import os
import shutil
from pathlib import Path

# Define paths
desktop_path = Path("/home/pi/Desktop/Mothbox")  # Assuming user is "pi" on your Raspberry Pi
photos_folder = desktop_path / "photos"
backup_folder_name = "photos_backup"

def get_storage_info(path):
  """
  Gets the total and available storage space of a path.

  Args:
      path: The path to the storage device.

  Returns:
      A tuple containing the total and available storage in bytes.
  """
  try:
    stat = os.statvfs(path)
    return stat.f_blocks * stat.f_bsize, stat.f_bavail * stat.f_bsize
  except OSError:
    return 0, 0  # Handle non-existent or inaccessible storages

def find_largest_external_storage():
  """
  Finds the largest external storage device connected to the Raspberry Pi.

  Returns:
      The path to the largest storage device or None if none is found.
  """
  largest_storage = None
  largest_size = 0
  
  for mount_point in os.listdir("/media/pi"):
    path = Path(f"/media/pi/{mount_point}")
    if path.is_dir():
      total_size, available_size = get_storage_info(path)
      print(path)
      print(available_size)
      if available_size > largest_size:
          largest_storage=path
          largest_size = available_size
      '''
      if total_size > largest_size:
        largest_storage = path
        largest_size = total_size
      '''
  print("Largest Storage: "+str(largest_storage))
  print(largest_size)
  return largest_storage

def copy_photos_to_backup(source_folder, target_folder):
  """
  Copies all files from the source folder to the target folder.

  Args:
      source_folder: The path to the source folder.
      target_folder: The path to the target folder.
  """
  if not os.path.exists(target_folder):
    os.makedirs(target_folder)
  for filename in os.listdir(source_folder):
    source_path = os.path.join(source_folder, filename)
    target_path = os.path.join(target_folder, filename)
    shutil.copy2(source_path, target_path)  # Preserves file metadata
    
def delete_original_photos(source_folder):
  """
  Deletes all files from the source folder.

  Args:
      source_folder: The path to the source folder.
  """
  for filename in os.listdir(source_folder):
    file_path = os.path.join(source_folder, filename)
    try:
      if os.path.isfile(file_path):
        os.remove(file_path)
    except OSError as e:
      print(f"Error deleting file {file_path}: {e}")  


if __name__ == "__main__":
  # Check if "photos" folder exists
  if not os.path.exists(photos_folder):
    print("Photos folder not found, exiting.")
    exit(1)

  # Find largest external storage
  largest_storage = find_largest_external_storage()

  if not largest_storage:
    print("No external storage found with enough space, exiting.")
    exit(1)

  # Get total and available space on desktop and external storage
  desktop_total, desktop_available = get_storage_info(desktop_path)
  external_total,external_available = get_storage_info(largest_storage)
  print("Desktop Total    Storage: \t"+str(desktop_total))
  print("Desktop Available Storage: \t"+str(desktop_available))
  print("External Total Storage: \t"+str(external_total))
  print("External Available Storage: \t"+str(external_available))

  # Check if external storage has more available space than desktop
  if external_available > sum(os.path.getsize(f) for f in photos_folder.iterdir() if f.is_file()):
    # Create backup folder on external storage
    backup_folder = largest_storage / backup_folder_name
    copy_photos_to_backup(photos_folder, backup_folder)
    print(f"Photos successfully copied to backup folder: {backup_folder}")
    
    # Check if internal storage has less than 4 GB left
    if desktop_available < 4 * 1024**3:  # 4 GB in bytes
      delete_original_photos(photos_folder)
      print("Original photos deleted after being backed up due to low internal storage.")
    else:
        print("More than 4GB remain so original files are kept in desktop after backing up")
  else:
    print("External storage doesn't have enough space for backup.")
