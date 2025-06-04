import os
import csv

# =============================================
# INPUT YOUR PATHS HERE (you can use single \ or /, they will be normalized)
FOLDER_PATH = r"E:\Panama\Gamboa_MayJayYard_FondoGorila_2025-05-19\2025-05-20"  # Replace with your folder path
CSV_FILE_PATH = r"E:\Panama\Gamboa_MayJayYard_FondoGorila_2025-05-19\2025-05-20\Bri\2025-05-20_Bri_exportdate_2025-05-27.csv"  # Replace with your CSV file path
# =============================================

def normalize_path(path):
    """Convert all path separators to double backslashes for Windows"""
    return path.replace('\\', '\\\\')

def count_jpg_files(folder_path):
    count = 0
    normalized_path = normalize_path(folder_path)
    for root, dirs, files in os.walk(normalized_path):
        # Skip the 'patches' directory
        if 'patches' in dirs:
            dirs.remove('patches')
        for file in files:
            if file.lower().endswith('.jpg'):
                count += 1
    return count

def count_non_empty_kingdom_rows(csv_file_path):
    count = 0
    normalized_path = normalize_path(csv_file_path)
    with open(normalized_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Check if 'kingdom' column exists and has text (non-empty string)
            if 'kingdom' in row and row['kingdom'].strip():
                count += 1
    return count

def calculate_average(folder_path, csv_file_path):
    try:
        jpg_count = count_jpg_files(folder_path)
        kingdom_count = count_non_empty_kingdom_rows(csv_file_path)
        
        if jpg_count == 0:
            print("Warning: No JPG files found in the folder (excluding 'patches' directory).")
            return None
        
        average = kingdom_count / jpg_count
        return average
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    # Normalize the paths and calculate the average
    average = calculate_average(FOLDER_PATH, CSV_FILE_PATH)
    
    if average is not None:
        print(f"\nNumber of JPG files (excluding 'patches'): {count_jpg_files(FOLDER_PATH)}")
        print(f"Number of non-empty 'kingdom' rows: {count_non_empty_kingdom_rows(CSV_FILE_PATH)}")
        print(f"\nThe average is: {average:.2f}")    