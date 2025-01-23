import subprocess
import os

script_path = "path/to/your_script.py"  # Update this with your actual script path
input_paths = [
    r"C:\Path\To\Data1",
    r"C:\Path\To\Data2",
    r"C:\Path\To\Data3"
]

for input_path in input_paths:
    os.environ["INPUT_PATH"] = input_path  # Set environment variable
    os.environ["YOLO_MODEL"] = r"C:\Users\andre\Desktop\yolo11m_4500_imgsz1600_b1_2024-01-18\weights\best.pt"
    os.environ["IMGSZ"] = 1600  # Should be same imgsz as used in training for best results!

    subprocess.run(["python", script_path], check=True)
