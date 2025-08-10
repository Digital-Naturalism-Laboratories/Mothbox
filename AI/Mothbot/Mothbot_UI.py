import gradio as gr
import subprocess
import sys
import os

# -------------------------------
# 🔧 Global default values
# -------------------------------
DEFAULT_SCRIPT = "Mothbot_Detect.py"

INPUT_PATH = r"C:\Users\andre\Desktop\MB_Test_Zone\Indonesia_Les_WilanTopTree_HopeCobo_2025-06-25\2025-06-26"
YOLO_MODEL = r"..\trained_models\yolo11m_4500_imgsz1600_b1_2024-01-18\weights\yolo11m_4500_imgsz1600_b1_2024-01-18.pt"
IMGSZ = 1600

# -------------------------------
# 🚀 Function to run selected script
# -------------------------------
def run_script(script_file_picker, script_path_text,
               input_file_picker, input_path_text,
               yolo_model_picker, yolo_model_text,
               imgsz,
               gen_bot_det, overwrite_bot, gen_thumbnails):

    try:
        # Decide script path
        script_path = script_file_picker if script_file_picker else script_path_text

        # Input folder
        input_path = os.path.dirname(input_file_picker) if input_file_picker else input_path_text

        # YOLO model
        yolo_model_path = yolo_model_picker if yolo_model_picker else yolo_model_text

        # Build the command
        cmd = [
            sys.executable,
            script_path,
            "--input_path", input_path,
            "--yolo_model", yolo_model_path,
            "--imgsz", str(imgsz)
        ]

        # Add boolean flags only if they are True
        cmd.extend(["--gen_bot_det_evenif_human_exists", str(gen_bot_det)])

        cmd.extend(["--overwrite_prev_bot_detections", str(overwrite_bot)])
        cmd.extend(["--gen_thumbnails", str(gen_thumbnails)])


        # Run the command and capture output
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            return f"❌ Script exited with errors:\n{result.stderr}"
        return f"✅ Script ran successfully:\n{result.stdout}"

    except Exception as e:
        return f"❌ Exception occurred:\n{str(e)}"


# -------------------------------
# 🎛️ Gradio UI
# -------------------------------
with gr.Blocks() as demo:
    gr.Markdown("## 🤖 Mothbot Detection Script Runner")

    # Script selection
    gr.Markdown("### 📝 Python Script")
    with gr.Row():
        script_file_picker = gr.File(
            label="Select Python script",
            file_types=[".py"],
            type="filepath"
        )
        script_path_text = gr.Textbox(
            label="Or enter script path manually",
            value=DEFAULT_SCRIPT
        )

    # Input folder
    gr.Markdown("### 📁 Input Folder")
    with gr.Row():
        input_file_picker = gr.File(
            label="Select any file inside input folder",
            file_types=[".jpg", ".png", ".txt", ".csv"],
            type="filepath"
        )
        input_path_text = gr.Textbox(
            label="Or enter input folder path manually",
            value=INPUT_PATH
        )

    # YOLO model
    gr.Markdown("### 🧠 YOLO Model")
    with gr.Row():
        yolo_model_picker = gr.File(
            label="Select YOLO .pt file",
            file_types=[".pt"],
            type="filepath"
        )
        yolo_model_text = gr.Textbox(
            label="Or enter YOLO model path manually",
            value=YOLO_MODEL
        )

    # Image size
    imgsz = gr.Number(label="🖼️ Image Size", value=IMGSZ)

    # Boolean flags
    gr.Markdown("### ⚙️ Detection Options")
    gen_bot_det = gr.Checkbox(label="Generate Bot Detection Even if Human Exists", value=True)
    overwrite_bot = gr.Checkbox(label="Overwrite Previous Bot Detections", value=False)
    gen_thumbnails = gr.Checkbox(label="Generate Thumbnails", value=True)

    # Run + Output
    run_button = gr.Button("🚀 Run Script")
    output = gr.Textbox(label="📜 Script Output", lines=20)

    run_button.click(
        fn=run_script,
        inputs=[
            script_file_picker, script_path_text,
            input_file_picker, input_path_text,
            yolo_model_picker, yolo_model_text,
            imgsz,
            gen_bot_det, overwrite_bot, gen_thumbnails
        ],
        outputs=output
    )

# 🖥️ Launch Gradio and auto-open in browser
if __name__ == "__main__":
    demo.launch(inbrowser=True)
