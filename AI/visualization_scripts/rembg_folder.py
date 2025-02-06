import os
import cv2
from rembg import remove
from PIL import Image
import argparse

INPUT_PATH=r"F:\Panama\Hoya_1204m_lightPotoro_2025-01-26\2025-01-27\patches"


#command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--input_path", default=INPUT_PATH, required=False)
args = parser.parse_args()

INPUT_PATH=args.input_path


def remove_backgrounds_from_folder(input_folder, output_folder):
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Supported image extensions
    valid_extensions = (".jpg", ".jpeg", ".png")
    # Step 1: Get all filenames with valid extensions to calculate total files
    valid_files = [filename for filename in os.listdir(input_folder) if filename.lower().endswith(valid_extensions)]
    total_files = len(valid_files)

    if total_files == 0:
        print("No files found with valid extensions.")
    else:
        count_processed = 0
        # Step 2: Process each file and display the percentage
        for filename in valid_files:
            count_processed += 1
            percentage = (count_processed / total_files) * 100
            rounded_percentage = round(percentage, 2)
            print(f"({rounded_percentage:.2f}%)... Processing {filename}")

            # Existing code to create paths and process the file
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, os.path.splitext(filename)[0] + "_no_bg.png")
    
            try:
                # Open the image with PIL
                with open(input_path, "rb") as img_file:
                    input_image = img_file.read()
                    output_image = remove(input_image)  # Remove background
                
                # Save output image
                with open(output_path, "wb") as out_file:
                    out_file.write(output_image)
                #print(f"Saved: {output_path}")
            except Exception as e:
                print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    #input_folder = input("Enter path to input folder: ").strip()
    input_folder=INPUT_PATH
    output_folder = input_folder+"/rembg"#input("Enter path to output folder: ").strip()
    
    remove_backgrounds_from_folder(input_folder, output_folder)
    print("Background removal complete!")
