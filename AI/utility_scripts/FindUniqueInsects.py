import os
from PIL import Image
import imagehash
import shutil

def find_unique_insects(input_folder, output_folder="unique_insects", hash_size=8, threshold=5):
    """
    Process all JPGs in `input_folder`, compare visual similarity using perceptual hash,
    and copy one representative image per visually similar group to `output_folder`.
    """
    output_folder=input_folder+"/"+output_folder

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    seen_hashes = []
    copied_files = 0

    for filename in os.listdir(input_folder):
        if not filename.lower().endswith(".jpg"):
            continue

        filepath = os.path.join(input_folder, filename)
        try:
            img = Image.open(filepath).convert("RGB")
            img_hash = imagehash.phash(img, hash_size=hash_size)
        except Exception as e:
            print(f"❌ Skipping {filename}: {e}")
            continue

        # Check similarity with previously seen hashes
        is_duplicate = False
        for existing_hash in seen_hashes:
            if abs(img_hash - existing_hash) <= threshold:
                is_duplicate = True
                break

        if not is_duplicate:
            seen_hashes.append(img_hash)
            dest_path = os.path.join(output_folder, filename)
            shutil.copy(filepath, dest_path)
            copied_files += 1
            print(f"✅ Copied unique: {filename}")

    print(f"\n🎉 Done! Copied {copied_files} unique insect images to '{output_folder}'.")

# Example usage
if __name__ == "__main__":
    find_unique_insects(r"C:\Users\andre\Desktop\Dinacon Stuff\Indonesia_Les_BeachPalm_grupoKite_2025-06-25\2025-06-29\patches", threshold=15)
