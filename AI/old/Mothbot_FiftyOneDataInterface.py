import fiftyone as fo
import fiftyone.zoo as foz



#dataset = fo.load_dataset(...)

if __name__ == "__main__":
    # Ensures that the App processes are safely launched on Windows
    #session = fo.launch_app(dataset)
    """
    #name = "my-dataset"
    dataset_dir = "C:/Users/andre/Desktop/testExampel51"
    labels_path = "C:/Users/andre/Desktop/testExampel51/samples.json"
    data_path = "C:/Users/andre/Desktop/testExampel51"
    # Create the dataset
    dataset = fo.Dataset.from_dir(
        dataset_dir=dataset_dir,
        dataset_type=fo.types.FiftyOneImageDetectionDataset,
        labels_path=labels_path,
        data_path=data_path
        #name=name,
    )
""" 
    #dataset = foz.load_zoo_dataset("quickstart")
    #session = fo.launch_app(dataset)
    """"""
    session = fo.launch_app()
    session.wait()