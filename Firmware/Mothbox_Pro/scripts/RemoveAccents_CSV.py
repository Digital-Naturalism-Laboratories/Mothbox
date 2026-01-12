import csv
import unicodedata

# Global variable for the input path
INPUT_PATH = "/home/pi/Desktop/Mothbox/wordlist.csv"  # Replace <Your_Input_Path> with the path to your CSV file


def remove_accents(input_str):
    """
    Removes accent marks from a string and returns the normalized version.
    """
    normalized = unicodedata.normalize('NFKD', input_str)
    return ''.join(c for c in normalized if not unicodedata.combining(c))


def normalize_csv(input_path):
    """
    Reads a CSV file, identifies words with nonstandard characters,
    and outputs a normalized version of the file.

    Args:
        input_path (str): Path to the input CSV file.
    """
    try:
        output_path = input_path.replace('.csv', '_normalized.csv')

        with open(input_path, mode='r', encoding='utf-8') as infile:
            with open(output_path, mode='w', encoding='utf-8', newline='') as outfile:
                reader = csv.reader(infile)
                writer = csv.writer(outfile)

                # Process each row
                for row in reader:
                    normalized_row = [remove_accents(cell) for cell in row]
                    writer.writerow(normalized_row)

        print(f"Normalization completed. Output saved to: {output_path}")

    except FileNotFoundError:
        print(f"Error: The file at path '{input_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    """
    Main function to start the normalization process.
    """
    if not INPUT_PATH.endswith('.csv'):
        print("Error: INPUT_PATH must point to a CSV file.")
        return

    print(f"Starting normalization for file: {INPUT_PATH}")
    normalize_csv(INPUT_PATH)


if __name__ == "__main__":
    main()