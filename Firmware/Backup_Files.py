#!/usr/bin/python

"""
Backupper Script
This script is for folks collecting lots of data automatically that needs to get backed up at certain intervals
for instance saving a bunch of files to a folder, but then automatically copying them to larger external devices
This script first defines paths for the desktop, photos folder, and backup folder name. Then, it defines functions to:

    Get the storage information (total and available space) of a path.
    Find the sizes of all external devices in terms of total storage capacity (not available because this will change)
    Rank them in order  of their total storage capacity
    Check if the first option has space available to copy the new files
      if not, choose the next option in terms of total storage
    Copy all the files from the internal storage to the external storage
    Move the files from the directory of "fresh" files to the internal "backedup" folder
    if the internal storage gets too small, delete the internal "backedup" folder
Finally, the script checks if the photos folder exists and then finds the largest external storage. It compares the total space and available space on both the desktop and the external storage to determine if the external storage has enough space for the backup. If so, it creates a backup folder on the external storage and copies the photos. Otherwise, it informs the user about insufficient space.

Note:
    This script assumes the user running the script has read and write permissions to the desktop and any external storage devices.
    You might need to adjust the user name in desktop_path depending on your Raspberry Pi setup.
"""
import os
import subprocess
import shutil
import psutil
from pathlib import Path
from datetime import datetime
import sys

# Define paths
desktop_path = Path(
    "/home/pi/Desktop/Mothbox"
)  # Assuming user is "pi" on your Raspberry Pi
photos_folder = desktop_path / "photos"
logs_folder = desktop_path / "logs"
backedup_photos_folder = desktop_path / "photos_backedup"

backup_folder_name = "photos_backup"
internal_storage_minimum = 5 # This is Gigabytes, below 4 on a raspberry pi 4, can make weird OS problems

print("----------------- STARTING BACKUP FILES-------------------")
now = datetime.now()
formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")  # Adjust the format as needed

print(f"Current time: {formatted_time}")

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
        # Check if the mount point is actually mounted
        if is_mounted(path):
            if path.is_dir():
                total_size, available_size = get_storage_info(path)
                print(path)
                print(available_size)
                if available_size > largest_size:
                    largest_storage = path
                    largest_size = available_size
            """
      if total_size > largest_size:
        largest_storage = path
        largest_size = total_size
      """
    print("Largest Storage: " + str(largest_storage))
    print(largest_size)
    return largest_storage

def is_mounted(path):
  """
  Checks if the given path is currently mounted.
  Args:
      path: The path to check for mount status.

  Returns:
      True if the path is mounted, False otherwise.
  """
  # Use psutil library to check mounted devices
  partitions = psutil.disk_partitions()
  for partition in partitions:
    if partition.mountpoint == str(path):
      return True
  return False

def rsync_photos_to_backup(source_dir, dest_dir):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    #if you don't want as many slow print commands, turn off verbose mode
    rsync_cmd = ["rsync", "-avz", str(source_dir) + "/", dest_dir]
    # Call rsync using subprocess
    try:
        process = subprocess.run(rsync_cmd, check=True)
    except subprocess.CalledProcessError as err:
        raise RuntimeError(f"Oh no! Mothbox couldn't backup your files!") from err

def rsync_copy_and_delete_files(source_dir, dest_dir):
    """
    This function uses rsync to copy files from source_dir to dest_dir and then deletes the originals from source_dir if successful.
    Args:
      source_dir: The source directory containing the files to copy.
      dest_dir: The destination directory to copy the files to.

    Raises:
      subprocess.CalledProcessError: If the rsync command fails.
    """
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # Build the rsync command with options for recursive copy, delete on source, and verbose output    
    rsync_cmd = ["rsync", "-avz", str(source_dir) + "/", dest_dir]

    # Call rsync using subprocess
    process = subprocess.run(rsync_cmd, check=True)

    # If successful, iterate through copied files and delete them individually
    if process.returncode == 0:
        for root, _, files in os.walk(source_dir):
            for filename in files:
                source_file = os.path.join(root, filename)
                dest_file = os.path.join(dest_dir, filename)
                # Check if the file was successfully copied (exists in destination)
                if os.path.isfile(dest_file):
                    try:
                        os.remove(source_file)
                        #print(f"Deleted: {source_file}")
                    except OSError as e:
                        print(f"Error deleting {source_file}: {e}")

    return process.returncode
def move_folder_contents(source_folder, destination_folder):
  """
  Moves the entire contents of a folder to a new folder, overwriting existing files.
  Args:
      source_folder (str): Path to the source folder.
      destination_folder (str): Path to the destination folder.
  """
  print("moving folder contents")
  for filename in os.listdir(source_folder):
    source_path = os.path.join(source_folder, filename)
    destination_path = os.path.join(destination_folder, filename)

    if os.path.isfile(source_path):
      # Move the file, overwrite if exists
      shutil.move(source_path, destination_path)
    elif os.path.isdir(source_path):
      # Create destination directory if it doesn't exist
      os.makedirs(destination_path, exist_ok=True)
      os.chmod(destination_path, 0o777)
      # Recursively move contents of subfolders
      move_folder_contents(source_path, destination_path)
    else:
      print(f"Skipping unknown item: {filename}")

def move_photos_to_backup(source_folder, target_folder):
  """
  Copies all files and subfolders from the source folder to the target folder recursively,
  handling existing dated folders and copying their contents.
  Args:
      source_folder: The path to the source folder.
      target_folder: The path to the target folder.
  """
  if not os.path.exists(target_folder):
    os.makedirs(target_folder)
  os.chmod(target_folder, 0o777)  # mode=0o777 for read write for all users
  # Move all contents (files and subfolders)
  try:
    shutil.move(source_folder, target_folder)
    print("Contents moved successfully!")
    
    #recreate the empty photos folder
    if not os.path.exists(source_folder):
        os.makedirs(source_folder)
    os.chmod(source_folder, 0o777)
  except OSError as e:
    print("Error moving contents:", e)
  
def copy_photos_to_backup(source_folder, target_folder):
  """
  Copies all files and subfolders from the source folder to the target folder recursively,
  handling existing dated folders and copying their contents.
  Args:
      source_folder: The path to the source folder.
      target_folder: The path to the target folder.
  """
  if not os.path.exists(target_folder):
    os.makedirs(target_folder)
  os.chmod(target_folder, 0o777)  # mode=0o777 for read write for all users

  for item in os.listdir(source_folder):
    source_path = os.path.join(source_folder, item)
    target_path = os.path.join(target_folder, item)

    if os.path.isfile(source_path):
      shutil.copy2(source_path, target_path)  # Copy files
      os.chmod(target_path, 0o777)  # Set permissions for copied files
    else:
      # Handle existing dated folders
      if not os.path.exists(target_path):
        shutil.copytree(source_path, target_path)  # Copy subdirectory if not exists
      else:
        # Copy contents of existing subdirectory
        for inner_item in os.listdir(source_path):
          inner_source_path = os.path.join(source_path, inner_item)
          inner_target_path = os.path.join(target_path, inner_item)
          if os.path.isfile(inner_source_path):
            shutil.copy2(inner_source_path, inner_target_path)
            os.chmod(inner_target_path, 0o777)  # Set permissions for copied files

def verify_copy(source_folder, destination_folder):
  """
  Compares the contents of a source folder and its subdirectories with the destination folder to verify successful copy.
  Args:
      source_folder: The path to the source folder.
      destination_folder: The path to the destination folder.
  Returns:
      A list of any differences found between the source and destination folders.
  """
  source_path = Path(source_folder)
  dest_path = Path(destination_folder)
  differences = []

  # Check if source folder exists
  if not source_path.exists():
    differences.append(f"Error: Source folder '{source_folder}' does not exist.")
    return differences

  # Compare files and subdirectories recursively
  for root, dirs, files in os.walk(source_path):
    rel_path = os.path.relpath(root, source_path)
    dest_dir = os.path.join(dest_path, rel_path)

    # Check if corresponding directory exists in destination
    if not os.path.exists(dest_dir):
      differences.append(f"Missing directory in destination: {dest_dir}")
      continue

    # Compare files within the directory
    for filename in files:
      source_file = os.path.join(root, filename)
      dest_file = os.path.join(dest_dir, filename)

      # Check if file exists in destination
      if not os.path.isfile(dest_file):
        differences.append(f"Missing file in destination: {dest_file}")
  return differences

def delete_folder_contents(folder_path):
  """
  Deletes all contents (files and subdirectories) from a folder.
  Args:
      folder_path: The path to the folder to be emptied.
  """
  for root, dirs, files in os.walk(folder_path, topdown=False):
    for filename in files:
      file_path = os.path.join(root, filename)
      os.remove(file_path)
    for dir in dirs:
      dir_path = os.path.join(root, dir)
      os.rmdir(dir_path)

def delete_original_photos(source_folder):
    """
    Deletes all files from the source folder.
    Args:
        source_folder: The path to the source folder.
    """
    print("trying to delete fresh")
    for filename in os.listdir(source_folder):
        file_path = os.path.join(source_folder, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except OSError as e:
            print(f"Error deleting file {file_path}: {e}")
            
def get_dir_size(dir_path):
  """
  Calculates the total size of a directory and its subdirectories.
  Args:
      dir_path: The path to the directory.
  Returns:
      The total size of the directory in bytes.
  """
  total_size = 0
  for dirpath, dirnames, filenames in os.walk(dir_path):
    for filename in filenames:
      file_path = os.path.join(dirpath, filename)
      if not os.path.islink(file_path):  # Skip symbolic links (optional)
        total_size += os.path.getsize(file_path)
  return total_size

def backup_and_delete(source_folder, destination_folder):
  """
  Back up files and delete them
  Args:
      source_folder: path to the original location
      destination_folder: path to backup location
  """
  # Ensure source and destination folders exist
  if not os.path.exists(source_folder):
      print(f"Source folder '{source_folder}' does not exist.")
      return
  if not os.path.exists(destination_folder):
      os.makedirs(destination_folder)
      print(f"Created destination folder '{destination_folder}'.")
  try:
      # Copy the contents of the source folder to the destination folder
      for item in os.listdir(source_folder):
          src_path = os.path.join(source_folder, item)
          dest_path = os.path.join(destination_folder, item)
          if os.path.isdir(src_path):
              shutil.copytree(src_path, dest_path)
          else:
              shutil.copy2(src_path, dest_path)
      print(f"All contents of '{source_folder}' successfully copied to '{destination_folder}'.")
      # Verify the copy
      src_items = set(os.listdir(source_folder))
      dest_items = set(os.listdir(destination_folder))
      if not src_items.issubset(dest_items):
          print("Error: Not all items were copied successfully.")
          return
      # Delete the contents of the source folder
      for item in os.listdir(source_folder):
          src_path = os.path.join(source_folder, item)
          if os.path.isdir(src_path):
              shutil.rmtree(src_path)
          else:
              os.remove(src_path)
      print(f"All contents of '{source_folder}' have been deleted.")
  except Exception as e:
      print(f"An error occurred: {e}")



if __name__ == "__main__":
    # Check if "photos" folder exists
    if not os.path.exists(photos_folder):
        print("Photos folder not found, exiting.")
        exit(1)
    # Get total and available space on desktop and external storage
    desktop_total, desktop_available = get_storage_info(desktop_path)
    print("Desktop Total    Storage: \t" + str(desktop_total))
    print("Desktop Available Storage: \t" + str(desktop_available))

    """
  Finds storage capacity of all external drives and ranks them by size.
  """
    disks = {}  # Dictionary to store disk name and capacity
    # Check potential mount points for external drives (adjust based on your system)
    for mount_point in os.listdir("/media/pi"):
        path = Path(f"/media/pi/{mount_point}")
        if path.is_dir() and is_mounted(path):
            total_size, available_size = get_storage_info(path)
            disks[path] = total_size, available_size

    # Sort disks by capacity (descending)
    # Check if any disks were found before sorting and printing
    print("~~~sorting disks~~~~~~")
    if disks:
        sorted_disks = sorted(disks.items(), key=lambda item: item[1][0], reverse=True)
        print("External Drives (Ranked by Total Size - Descending):")
        for disk_name, capacity in sorted_disks:
            print(
                f"{disk_name}: total size {capacity[0]} GB - available size {capacity[1]} GB"
            )
    else:
        print("No external drives found.")
        print(
            "stuff never worked out with this backup, your files are not properly backedup"
        )

        exit(1)
    print("~~~sorted~~~~~~")
    thingsworkedok = False
    # this is the loop where we make stuff happen
    # iterate through the disks, starting with the largest
    # see if it has enough available space, if not, choose the next largest
    for disk_name, capacity in sorted_disks:
        print("chosen Disk: "+str(disk_name))
        total_available, external_available = capacity
        print("total available \t"+str(total_available)) 
        # Check if external storage has more available space than desktop
        dir_path = photos_folder
        total_size_bytes = get_dir_size(dir_path)
        print("total needed \t\t"+str(total_size_bytes))
        if external_available > total_size_bytes:
            # Create backup folder on external storage
            external_backup_folder = disk_name / backup_folder_name
            print("doing the backup...")
            #using the non-rsync way for now because rsync was giving errors
            
            copy_photos_to_backup(photos_folder, external_backup_folder)
            print(f"Photos successfully copied to external backup folder: {external_backup_folder}")            


            external_logs_folder = disk_name / "logs"
            copy_photos_to_backup(logs_folder,external_logs_folder)
            print(f"Logs successfully copied to external backup folder: {external_backup_folder}")            

            differences = verify_copy(photos_folder, external_backup_folder)
            if differences:
              print("Differences found:")
              for difference in differences:
                print(difference)
            else:
              print("Copy verification successful! No differences found.")
              print("moving original files to backedup_photos_folder")
              move_folder_contents(photos_folder, backedup_photos_folder)
              print(f"Photos successfully copied to internal backup folder: {backedup_photos_folder}")
            thingsworkedok=True
            if(thingsworkedok):
                # After we backed up, we can check on our internal storage and see if we need to clean up
                # Check if internal storage has less than X GB left
                x = internal_storage_minimum
                if desktop_available < x * 1024**3:  # x GB in bytes
                    delete_folder_contents(backedup_photos_folder)
                    print(
                        "Original photos deleted after being backed up due to low internal storage."
                    )
                else:
                    print(
                        "More than "
                        + str(x)
                        + "GB remain so original files are also kept in internal storage after backing up to external storage"
                    )
                print("we have finished backing up! yay!")
                break
        else:
            print("This External storage doesn't have enough space for backup.\n Trying next available storage if there is one ")
    if thingsworkedok == False:
        print("stuff never worked out with this backup, your files are not properly backedup")
    else:
        print("stuff worked out BACKUP COMPLETE")
    print("end")
quit()