import json

# Define dummy data
info = {"description": "Dummy COCO dataset", "url": "http://your-dataset-url.com"}
licenses = [
    {"id": 1, "name": "Attribution-NonCommercial-ShareAlike License", "url": "http://creativecommons.org/licenses/by-nc-sa/2.0/"}
]
categories = [{"id": 1, "name": "cat", "supercategory": "animal"}]
images = [
    {"id": 1, "license": 1, "file_name": "dummy_image.jpg", "height": 480, "width": 640}
]
annotations = [
    {
        "id": 1,
        "image_id": 1,
        "category_id": 1,
        "bbox": [260, 177, 231, 199],  # Dummy bounding box coordinates
        "segmentation": [],  # Empty segmentation (replace with actual data)
        "keypoints": [],  # Empty keypoints (replace with actual data)
        "num_keypoints": 0,
        "score": 0.95,
        "area": 45969,
        "iscrowd": 0,
    }
]

# Create the COCO dictionary
coco = {"info": info, "licenses": licenses, "categories": categories, "images": images, "annotations": annotations}

# Write data to JSON file
with open("labels.json", "w") as outfile:
  json.dump(coco, outfile, indent=4)  # Indent for readability

print("Created labels.json file with dummy data!")