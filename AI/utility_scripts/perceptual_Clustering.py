import os
import torch
import numpy as np
from PIL import Image
from tqdm import tqdm
import torchvision.transforms as T
import hdbscan
import piexif

# --------------------------
# 1. Load DINOv2 model
# --------------------------
device = "cuda" if torch.cuda.is_available() else "cpu"
model = torch.hub.load("facebookresearch/dinov2", "dinov2_vits14").to(device)
model.eval()

# Image preprocessing
transform = T.Compose([
    T.Resize(256),
    T.CenterCrop(224),
    T.ToTensor(),
    T.Normalize(mean=(0.5, 0.5, 0.5), std=(0.5, 0.5, 0.5))
])

# --------------------------
# 2. Extract embeddings
# --------------------------
def get_embedding(img_path):
    img = Image.open(img_path).convert("RGB")
    img_tensor = transform(img).unsqueeze(0).to(device)
    with torch.no_grad():
        feat = model(img_tensor)  # shape [1, 384]
    return feat.cpu().numpy().squeeze()

def extract_embeddings(image_folder):
    embeddings, filenames = [], []
    for fname in tqdm(os.listdir(image_folder), desc="Extracting embeddings"):
        if not fname.lower().endswith((".jpg", ".jpeg", ".png")):
            continue
        path = os.path.join(image_folder, fname)
        try:
            feat = get_embedding(path)
            embeddings.append(feat)
            filenames.append(fname)
        except Exception as e:
            print(f"⚠️ Skipping {fname}: {e}")
    return np.array(embeddings), filenames

# --------------------------
# 3. Cluster with HDBSCAN
# --------------------------
def cluster_embeddings(embeddings):
    clusterer = hdbscan.HDBSCAN(
        min_cluster_size=3,          # smaller clusters allowed
        min_samples=1,               # fewer items marked as noise
        cluster_selection_epsilon=0.05,  # expand clusters slightly
        metric="euclidean"
    )
    labels = clusterer.fit_predict(embeddings)
    return labels

# --------------------------
# 4. Write Description metadata
# --------------------------
def write_cluster_to_description(image_folder, filenames, labels):
    for fname, label in zip(filenames, labels):
        path = os.path.join(image_folder, fname)
        try:
            # Load existing EXIF
            exif_dict = piexif.load(path)

            # Windows Explorer "Description" → EXIF ImageDescription (0x010E)
            description = f"Cluster {label}"
            exif_dict["0th"][piexif.ImageIFD.ImageDescription] = description.encode("utf-8")

            # Save EXIF back to file
            exif_bytes = piexif.dump(exif_dict)
            piexif.insert(exif_bytes, path)

        except Exception as e:
            print(f"⚠️ Could not update {fname}: {e}")
    print("✅ Cluster IDs written into 'Description' field (visible in Explorer).")


# --------------------------
# 4. Rename files with cluster prefix (safe overwrite)
# --------------------------
def prefix_cluster_to_filename(image_folder, filenames, labels, copy_instead=False):
    """
    Prefix cluster labels to filenames instead of writing metadata.
    If a file already has a Cluster prefix, it will be replaced (not duplicated).

    Args:
        image_folder (str): Folder containing the images.
        filenames (list[str]): List of filenames in the cluster.
        labels (list[int]): Corresponding cluster labels.
        copy_instead (bool): If True, makes copies instead of renaming originals.
    """
    cluster_pattern = re.compile(r"^Cluster\d+_")  # matches "Cluster123_"

    for fname, label in zip(filenames, labels):
        old_path = os.path.join(image_folder, fname)

        # Split into name + extension
        name, ext = os.path.splitext(fname)

        # Remove old Cluster prefix if present
        clean_name = cluster_pattern.sub("", name)

        # Build new name with correct cluster prefix
        new_name = f"Cluster{label}_{clean_name}{ext}"
        new_path = os.path.join(image_folder, new_name)

        try:
            if copy_instead:
                shutil.copy2(old_path, new_path)
            else:
                os.rename(old_path, new_path)
        except Exception as e:
            print(f"⚠️ Could not rename {fname}: {e}")

    action = "copied" if copy_instead else "renamed"
    print(f"✅ Files successfully {action} with cluster prefixes.")

# --------------------------
# 5. Main
# --------------------------
if __name__ == "__main__":
    input_folder = r"D:\x-anylabeling-matting\onlybig"  # 🔹 change this to your folder path
    #output_folder = r"C:\Users\andre\Desktop\MB_Test_Zone\Indonesia_Les_WilanTopTree_HopeCobo_2025-06-25\2025-06-26\patches\clusters"

    embeddings, filenames = extract_embeddings(input_folder)
    labels = cluster_embeddings(embeddings)
    #save_clusters(input_folder, filenames, labels, output_folder)
    #write_cluster_to_description(input_folder, filenames, labels) #doesn't work with pngs
    prefix_cluster_to_filename(input_folder, filenames, labels)

