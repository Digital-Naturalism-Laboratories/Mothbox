import os
import shutil
import torch
import numpy as np
from PIL import Image
from tqdm import tqdm
import torchvision.transforms as T
import hdbscan

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
    clusterer = hdbscan.HDBSCAN(min_cluster_size=5, metric="euclidean")
    labels = clusterer.fit_predict(embeddings)
    return labels

# --------------------------
# 4. Save results
# --------------------------
def save_clusters(image_folder, filenames, labels, output_folder="clusters"):
    os.makedirs(output_folder, exist_ok=True)
    for fname, label in zip(filenames, labels):
        cluster_dir = os.path.join(output_folder, f"cluster_{label}")
        os.makedirs(cluster_dir, exist_ok=True)
        src = os.path.join(image_folder, fname)
        dst = os.path.join(cluster_dir, fname)
        shutil.copy(src, dst)
    print(f"✅ Saved clustered images in '{output_folder}/'")

# --------------------------
# 5. Main
# --------------------------
if __name__ == "__main__":
    input_folder = r"C:\Users\andre\Desktop\MB_Test_Zone\Indonesia_Les_WilanTopTree_HopeCobo_2025-06-25\2025-06-26\patches"  # 🔹 change this to your folder path
    output_folder = r"C:\Users\andre\Desktop\MB_Test_Zone\Indonesia_Les_WilanTopTree_HopeCobo_2025-06-25\2025-06-26\patches\clusters"

    embeddings, filenames = extract_embeddings(input_folder)
    labels = cluster_embeddings(embeddings)
    save_clusters(input_folder, filenames, labels, output_folder)
