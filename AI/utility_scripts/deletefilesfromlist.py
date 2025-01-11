import os

# Function to delete files listed in a .txt file
def delete_files_from_list(file_list_path):
    """Deletes every file listed in the specified .txt file."""
    try:
        # Read the file list
        with open(file_list_path, 'r', encoding='utf-8') as file:
            file_paths = file.read().splitlines()

        # Track deleted and failed deletions
        deleted_files = []
        failed_files = []

        # Delete each file in the list
        for file_path in file_paths:
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    deleted_files.append(file_path)
                except Exception as e:
                    print(f"Failed to delete {file_path}: {e}")
                    failed_files.append(file_path)
            else:
                print(f"File not found: {file_path}")
                failed_files.append(file_path)

        # Print summary
        print(f"Deleted {len(deleted_files)} files.")
        print(f"Failed to delete {len(failed_files)} files.")

        if failed_files:
            print("Failed file paths:")
            for failed_file in failed_files:
                print(failed_file)

    except FileNotFoundError:
        print(f"File not found: {file_list_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Run the function
if __name__ == "__main__":
    # Replace <INSERT_PATH_TO_TXT_FILE> with the path to the .txt file containing the file list
    file_list_path = r"C:\Users\andre\Documents\GitHub\Mothbox\AI\utility_scripts\flaggedfiles.txt"
    delete_files_from_list(file_list_path)
