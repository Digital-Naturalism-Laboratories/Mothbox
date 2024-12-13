'''This script is here to remove common accents in non-english languages

'''


import os
import unicodedata

# Global variable for the input path
INPUT_PATH = r"D:\Panama"  # Replace <Your_Input_Path> with the path to your folder

def remove_accents(input_str):
    """
    Removes accent marks from a string and returns the normalized version.
    """
    normalized = unicodedata.normalize('NFKD', input_str)
    return ''.join(c for c in normalized if not unicodedata.combining(c))

def rename_files_and_folders(base_path):
    """
    Recursively renames files and folders to remove accent marks.

    Args:
        base_path (str): The path to start the recursive renaming.
    """
    total_subfolders = 0
    processed_subfolders = 0

    # Count total subfolders
    for _, dirs, _ in os.walk(base_path):
        total_subfolders += len(dirs)

    print(f"Total subfolders found: {total_subfolders}")

    for root, dirs, files in os.walk(base_path, topdown=False):
        # Rename files
        for filename in files:
            old_path = os.path.join(root, filename)
            new_filename = remove_accents(filename)
            new_path = os.path.join(root, new_filename)
            if old_path != new_path:
                os.rename(old_path, new_path)

        # Rename directories
        for dirname in dirs:
            old_dir_path = os.path.join(root, dirname)
            new_dirname = remove_accents(dirname)
            new_dir_path = os.path.join(root, new_dirname)
            if old_dir_path != new_dir_path:
                os.rename(old_dir_path, new_dir_path)

            processed_subfolders += 1
            print(f"Processed {processed_subfolders}/{total_subfolders} subfolders.", end='\r')

def main():
    """
    Main function to start the renaming process.
    """
    if not os.path.exists(INPUT_PATH):
        print(f"The path '{INPUT_PATH}' does not exist.")
        return

    print(f"Starting the renaming process in: {INPUT_PATH}")
    rename_files_and_folders(INPUT_PATH)
    print("\nRenaming process completed.")

if __name__ == "__main__":
    main()