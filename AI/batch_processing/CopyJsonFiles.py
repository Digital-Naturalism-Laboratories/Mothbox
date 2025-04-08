import os
import shutil

def copy_json_files(input_path, output_path):
    # Use os.walk to traverse all subdirectories recursively
    for root, dirs, files in os.walk(input_path):
        # Check each file and directory
        for item in files:
            if item.endswith('.json'):
                json_file = os.path.join(root, item)
                print(item)
                # Create the output directory if it doesn't exist
                output_dir = os.path.join(output_path, os.path.relpath(root, input_path))
                os.makedirs(output_dir, exist_ok=True)

                # Copy the JSON file to the new path
                shutil.copy2(json_file, output_dir)

# Replace these paths with your actual paths
input_path = r"E:\Panama"
output_path = r"E:\Panama_JSON"
print("startingCopy")
copy_json_files(input_path, output_path)
print("copied all those files to: "+output_path)
