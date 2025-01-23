#Mothbox_YoloValidate

from ultralytics import YOLO
if __name__ == '__main__':

    # Load a model
    model = YOLO('yolo11m-obb.yaml').to('cuda')  # Build a new model from YAML # load an official model
    model = YOLO(r"C:\Users\andre\Documents\GitHub\Mothbox\AI\training_scripts\runs\obb\train\weights\best.pt")  # load a custom model

    # Validate the model
    metrics = model.val()  # no arguments needed, dataset and settings remembered
    metrics.box.map  # map50-95
    metrics.box.map50  # map50
    metrics.box.map75  # map75
    metrics.box.maps  # a list contains map50-95 of each category