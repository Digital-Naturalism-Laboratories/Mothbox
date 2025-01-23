import subprocess
import os

script_path = r"C:\Users\andre\Documents\GitHub\Mothbox\AI\Mothbot_Detect.py"  # Update this with your actual script path
input_paths = [
    r"F:\Panama\Boquete_fincaelvelo_accionsauro_2024-09-23\2024-09-23",
    r"F:\Panama\Boquete_fincaelvelo_AmpleBonobo_2024-09-18\2024-09-17",
    r"F:\Panama\Boquete_fincaelvelo_AmpleBonobo_2024-09-18\2024-09-18",
    r"F:\Panama\Boquete_fincaelvelo_AmpleBonobo_2024-09-18\2024-09-19",
    r"F:\Panama\Boquete_fincaelvelo_AmpleBonobo_2024-09-18\2024-09-20",
    r"F:\Panama\Boquete_fincaelvelo_AmpleBonobo_2024-09-18\2024-09-21"
]

YOLO_MODEL=r"C:\Users\andre\Documents\GitHub\Mothbox\AI\trained_models\yolo11m_4500_imgsz1600_b1_2024-01-18\weights\best.pt"
IMGSZ=1600# Should be same imgsz as used in training for best results!
i=0
for input_path in input_paths:
    print("starting to process: "+input_path)
    subprocess.run([
        "python", script_path,
        "--input_path", input_path,
        "--yolo_model", YOLO_MODEL,
        "--imgsz", str(IMGSZ)
    ], check=True)

    i=i+1
    print("processed "+str(i)+" folders.")
    print("just finished processing "+input_path)