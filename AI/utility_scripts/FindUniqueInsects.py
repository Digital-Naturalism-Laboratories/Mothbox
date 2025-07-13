import os
from PIL import Image
import imagehash
import shutil

folder_path=r"E:\Deployments\Indonesia\Les_BeachPalm_hopeCobo_2025-06-20\2025-06-20\patches"

def find_unique_insects(input_folder, output_folder="unique_insects", hash_size=8, threshold=5, min_resolution=(0, 0)):
    """
    Process all JPGs in `input_folder`, compare visual similarity using perceptual hash,
    and copy one representative image per visually similar group to `output_folder`.
    
    Only includes images larger than `min_size` (width, height).
    """

    output_folder=input_folder+"/"+output_folder
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    seen_hashes = []
    copied_files = 0
    min_width, min_height = min_resolution

    for filename in os.listdir(input_folder):
        if not filename.lower().endswith(".jpg"):
            continue

        filepath = os.path.join(input_folder, filename)
        try:
            img = Image.open(filepath).convert("RGB")

            # Skip small images
            if img.width < min_width or img.height < min_height:
                print(f"🚫 Skipping {filename}: too small ({img.width}x{img.height})")
                continue

            img_hash = imagehash.phash(img, hash_size=hash_size)
        except Exception as e:
            print(f"❌ Skipping {filename}: {e}")
            continue

        # Check similarity
        is_duplicate = any(abs(img_hash - h) <= threshold for h in seen_hashes)

        if not is_duplicate:
            seen_hashes.append(img_hash)
            dest_path = os.path.join(output_folder, filename)
            shutil.copy(filepath, dest_path)
            copied_files += 1
            print(f"✅ Copied unique: {filename}")

    print(f"\n🎉 Done! Copied {copied_files} unique insect images to '{output_folder}'.")
# Example usage
if __name__ == "__main__":
    find_unique_insects(
        input_folder=folder_path,
        threshold=18,
        min_resolution=(60, 60)  # e.g. skip anything smaller than 60x60
    )