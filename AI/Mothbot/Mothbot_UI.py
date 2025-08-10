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
# 🚀 Run function
# -------------------------------
def run_script(script_file_picker, script_path_text,
               input_file_picker, input_path_text,
               yolo_model_picker, yolo_model_text,
               imgsz,
               gen_bot_det, overwrite_bot, gen_thumbnails):
    import subprocess

    script_path = script_file_picker if script_file_picker else script_path_text
    input_path = os.path.dirname(input_file_picker) if input_file_picker else input_path_text
    yolo_model_path = yolo_model_picker if yolo_model_picker else yolo_model_text

    cmd = [
        sys.executable,
        script_path,
        "--input_path", input_path,
        "--yolo_model", yolo_model_path,
        "--imgsz", str(imgsz),
        "--gen_bot_det_evenif_human_exists", str(gen_bot_det),
        "--overwrite_prev_bot_detections", str(overwrite_bot),
        "--gen_thumbnails", str(gen_thumbnails)
    ]

    try:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        output_log = ""

        for line in iter(process.stdout.readline, ''):
            cleaned_line = line.replace('\r', '')
            output_log += cleaned_line
            yield output_log

        process.stdout.close()
        process.wait()

        if process.returncode != 0:
            output_log += f"\n❌ Script exited with error code {process.returncode}"
        else:
            output_log += "\n✅ Script completed successfully."

        yield output_log

    except Exception as e:
        yield f"\n❌ Exception: {str(e)}"


# -------------------------------
# Compact Gradio UI
# -------------------------------
with gr.Blocks() as demo:
    gr.Markdown("## 🦋🤖 Mothbot UI")

    with gr.Row():
        with gr.Column():
            input_file_picker = gr.File(label="📁 Pick file in input folder", file_types=[".jpg", ".png", ".txt", ".csv"], type="filepath")
            input_path_text = gr.Textbox(label="Or type input folder path", value=INPUT_PATH)

        with gr.Column():
            yolo_model_picker = gr.File(label="📄 Pick YOLO model (.pt)", file_types=[".pt"], type="filepath")
            yolo_model_text = gr.Textbox(label="Or type YOLO model path", value=YOLO_MODEL)

    with gr.Row():
        imgsz = gr.Number(label="🖼️ Image Size", value=IMGSZ)
        run_button = gr.Button("🚀 Run Script")

    with gr.Accordion("Advanced Options", open=False):
        with gr.Row():
            script_file_picker = gr.File(label="Select script", file_types=[".py"], type="filepath")
            script_path_text = gr.Textbox(label="Or type script path", value=DEFAULT_SCRIPT)

        gr.Markdown("### ⚙️ Detection Flags")
        with gr.Row():
            gen_bot_det = gr.Checkbox(label="Generate Bot Detection Even if Human Exists", value=True)
            overwrite_bot = gr.Checkbox(label="Overwrite Previous Bot Detections", value=False)
            gen_thumbnails = gr.Checkbox(label="Generate Thumbnails", value=True)

    output_textbox = gr.Textbox(label="📜 Script Output", lines=10, interactive=False)
    #output_textbox = gr.Textbox(label="📜 Script Output", lines=18, interactive=False, show_copy_button=True, max_lines=1000)

    run_button.click(
        fn=run_script,
        inputs=[
            script_file_picker, script_path_text,
            input_file_picker, input_path_text,
            yolo_model_picker, yolo_model_text,
            imgsz,
            gen_bot_det, overwrite_bot, gen_thumbnails
        ],
        outputs=output_textbox,
    )

# 🖥️ Launch and auto-open
if __name__ == "__main__":
    demo.launch(inbrowser=True)
