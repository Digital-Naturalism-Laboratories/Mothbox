
import torch

print(torch.cuda.is_available())
from ultralytics import YOLO

if __name__ == '__main__':
    # Load a model
    model = YOLO("yolo11s-obb.yaml")  # build a new model from YAML using ORIENTED BOUNDING BOXES
    #model = YOLO("yolov8s.yaml")  # build a new model from YAML using regular  rectangle YOLO

    #model = YOLO("mothsn-obb.pt")  # load a pretrained model (recommended for training)

    #model = YOLO("yolov8n-obb.pt")  # load a pretrained model (recommended for training)
    #model = YOLO("yolov8n-obb.yaml").load("yolov8n.pt")  # build from YAML and transfer weights
    print("now start training~~~~~~~~~~~~~~~~~~~")
    # Train the model

    yamlPath= r"C:\Users\andre\Documents\GitHub\Mothbox\AI\mothbox_training.yaml"
    results = model.train(data=yamlPath, epochs=100, imgsz=1024, batch=14) #lowering batch size cuz GPU ran out of memory, default 16