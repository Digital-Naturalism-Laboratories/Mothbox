import fiftyone as fo
import fiftyone.utils.data as fou

INPUT_PATH = r"C:\Users\andre\Desktop\MB_Test_Zone\Indonesia_Les_WilanTopTree_HopeCobo_2025-06-25\2025-06-26\AQMStest"


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