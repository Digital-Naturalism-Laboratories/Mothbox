import torch
from ultralytics import YOLO
import yaml
import tempfile
import os

if __name__ == '__main__':
    print('Available devices:', torch.cuda.device_count())
    print('Current CUDA device:', torch.cuda.current_device())
    if torch.cuda.is_available():
        print(f"GPU: {torch.cuda.get_device_name(0)} is available.")
        torch.cuda.set_device(0)
    else:
        print("No GPU available. Training will run on CPU.")

    # Define dataset configuration directly in Python
    dataset_config = {
        'path': r'C:\Users\andre\Desktop\mothbox_dataset_3000_2025-01-13',  # Dataset root directory
        'train': 'images/train',  # Train images (relative to 'path')
        'val': 'images/val',      # Validation images (relative to 'path')
        'test': 'images/test',    # Test images (relative to 'path')
        'nc': 1,                  # Number of classes
        'names': {0: 'creature'}  # Class names
    }

    # Create a temporary YAML file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.yaml') as temp_yaml:
        yaml.dump(dataset_config, temp_yaml)
        yaml_path = temp_yaml.name

    print(f"Temporary YAML file created at: {yaml_path}")

    try:
        # Load a model
        model = YOLO('yolo11m-obb.yaml').to('cuda')  # Build a new model from YAML
        print(model.device)
        print("Now starting training...")

        # Train the model
        results = model.train(
            data=yaml_path,  # Pass the temporary YAML file path
            epochs=100,
            imgsz=1408,
            batch=2,
            device='cuda'
        )
    finally:
        # Clean up the temporary file
        os.remove(yaml_path)
        print(f"Temporary YAML file {yaml_path} deleted.")