import fiftyone as fo
import fiftyone.utils.data as fou

INPUT_PATH = r"E:\Panama\Gamboa_MayJayYard_FondoGorila_2025-05-19\2025-05-20\Bri"

dataset_dir = INPUT_PATH

# The type of the dataset being imported
dataset_type = fo.types.FiftyOneDataset  # for example

# Import the dataset
dataset = fo.Dataset.from_dir(
    dataset_dir=dataset_dir,
    dataset_type=dataset_type,
)
# Sort the dataset by patch_width in ascending order
sorted_dataset = dataset.sort_by("patch_width",True)

session = fo.launch_app(sorted_dataset)
print("FiftyOne session launched. Press Ctrl+C to close.")
session.wait()