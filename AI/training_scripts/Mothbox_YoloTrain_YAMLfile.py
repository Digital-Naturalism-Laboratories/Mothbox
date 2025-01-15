
import torch
from ultralytics import YOLO

if __name__ == '__main__':

    print ('Available devices ', torch.cuda.device_count())
    print ('Current cuda device ', torch.cuda.current_device())
    if torch.cuda.is_available():
        print(f"GPU: {torch.cuda.get_device_name(0)} is available.")
        torch.cuda.set_device(0)
    else:
        print("No GPU available. Training will run on CPU.")


    # Load a model
    model = YOLO('yolo11m-obb.yaml').to('cuda')  # build a new model from YAML using ORIENTED BOUNDING BOXES
    print(model.device)
    print("now start training~~~~~~~~~~~~~~~~~~~")
    # Train the model

    yamlPath= r"C:\Users\andre\Documents\GitHub\Mothbox\AI\training_scripts\mothbox_training.yaml"
    results = model.train(data=yamlPath, epochs=100, imgsz=1408, batch=2, device='cuda' ) #lowering batch size cuz GPU ran out of memory, default 16