import torch
print(torch.cuda.is_available())
from ultralytics import YOLO
if __name__ == '__main__':
    # Load a model
    model = YOLO("yolov8s-obb.yaml")  # build a new model from YAML using ORIENTED BOUNDING BOXES
    #model = YOLO("yolov8s.yaml")  # build a new model from YAML using regular  rectangle YOLO

    #model = YOLO("mothsn-obb.pt")  # load a pretrained model (recommended for training)

    #model = YOLO("yolov8n-obb.pt")  # load a pretrained model (recommended for training)
    #model = YOLO("yolov8n-obb.yaml").load("yolov8n.pt")  # build from YAML and transfer weights
    print("now start training~~~~~~~~~~~~~~~~~~~")
    # Train the model
    results = model.train(data="moths.yaml", epochs=100, imgsz=1024)