import fiftyone as fo
import fiftyone.utils.data as fou

INPUT_PATH = r"D:\Panama\Hoya_1508m_waveUrta_2025-01-27\2025-01-28"

dataset_dir = INPUT_PATH

# The type of the dataset being imported
dataset_type = fo.types.FiftyOneDataset  # for example

# Import the dataset
dataset = fo.Dataset.from_dir(
    dataset_dir=dataset_dir,
    dataset_type=dataset_type,
)

session = fo.launch_app(dataset)
print("FiftyOne session launched. Press Ctrl+C to close.")
session.wait()