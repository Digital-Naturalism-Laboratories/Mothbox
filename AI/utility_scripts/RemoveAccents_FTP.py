'''This script is here to remove common accents in non-english languages stored on FTP servers

'''

from ftplib import FTP
import unicodedata
import time
# FTP server details
FTP_HOST = "u407120.your-storagebox.de"
FTP_USER = "u407120"
FTP_PASS = ""
FTP_START_DIR = "/moths/Panama/Fortuna_PlotHondaAsitio5050_AccionSauro_2024-09-12"  # Path on the server to start the process

def remove_accents(input_str):
    """
    Removes accent marks from a string and returns the normalized version.
    """
    normalized = unicodedata.normalize('NFKD', input_str)
    return ''.join(c for c in normalized if not unicodedata.combining(c))

def count_folders(ftp, current_dir):
    """
    Counts the total number of folders within the given directory recursively.

    Args:
        ftp (FTP): An active FTP connection.
        current_dir (str): The directory to start counting from.

    Returns:
        int: The total number of folders.
    """
    folder_count = 0
    ftp.cwd(current_dir)
    items = ftp.nlst()

    for item in items:
        try:
            ftp.cwd(item)  # Check if it's a directory
            folder_count += 1
            folder_count += count_folders(ftp, f"{current_dir}/{item}")
            ftp.cwd("..")
        except Exception:
            # It's a file, not a directory
            continue

    return folder_count

def traverse_and_rename(ftp, current_dir, total_folders, processed_folders):
    """
    Recursively traverses and renames files and folders to remove accent marks on an FTP server.

    Args:
        ftp (FTP): An active FTP connection.
        current_dir (str): The current directory to process.
        total_folders (int): Total number of folders detected.
        processed_folders (list): A mutable list containing the count of processed folders.
    """
    ftp.cwd(current_dir)
    items = ftp.nlst()  # List items in the current directory

    for item in items:
        try:
            # Attempt to change to the item to check if it's a directory
            ftp.cwd(item)
            # It's a directory; rename and recurse
            new_name = remove_accents(item)
            if item != new_name:
                ftp.rename(item, new_name)
                item = new_name  # Update name after renaming

            # Recurse into the renamed directory
            traverse_and_rename(ftp, f"{current_dir}/{item}", total_folders, processed_folders)
            # Go back up to the current directory
            ftp.cwd("..")

            # Update and print progress
            processed_folders[0] += 1
            print(f"Processed {processed_folders[0]}/{total_folders} folders.", end='\r')
        except Exception:
            # It's a file; attempt to rename
            new_name = remove_accents(item)
            if item != new_name:
                ftp.rename(item, f"{current_dir}/{new_name}")

def reconnect_and_resume(ftp, current_dir, total_folders, processed_folders):
    """
    Reconnects to the FTP server and resumes processing at the last directory.

    Args:
        ftp (FTP): An active FTP connection.
        current_dir (str): The directory to resume processing.
        total_folders (int): Total number of folders detected.
        processed_folders (list): A mutable list containing the count of processed folders.
    """
    ftp.close()
    time.sleep(5)  # Wait before reconnecting
    ftp.connect(FTP_HOST)
    ftp.login(FTP_USER, FTP_PASS)
    ftp.cwd(current_dir)
    traverse_and_rename(ftp, current_dir, total_folders, processed_folders)

def main():
    """
    Main function to start the renaming process on an FTP server.
    """
    ftp = FTP(FTP_HOST)
    ftp.login(FTP_USER, FTP_PASS)
    ftp.set_pasv(True)  # Enable passive mode

    print(f"Connected to FTP server: {FTP_HOST}")
    print("Calculating total folders...")

    total_folders = count_folders(ftp, FTP_START_DIR)
    print(f"Total folders found: {total_folders}")

    processed_folders = [0]  # Use a mutable list to track progress

    try:
        traverse_and_rename(ftp, FTP_START_DIR, total_folders, processed_folders)
    except Exception as e:
        print(f"An error occurred: {e}")
        reconnect_and_resume(ftp, FTP_START_DIR, total_folders, processed_folders)
    finally:
        ftp.quit()

    print("\nRenaming process completed.")

if __name__ == "__main__":
    main()
