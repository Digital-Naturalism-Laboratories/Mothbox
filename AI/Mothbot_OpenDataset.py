import fiftyone as fo
import fiftyone.utils.data as fou

INPUT_PATH = r"/Users/brianna/Desktop/Indonesia_Deployments/Les_DurianFarm_EfectoMinla_2025-07-04/2025-07-05/BriHemipteraOnly"

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