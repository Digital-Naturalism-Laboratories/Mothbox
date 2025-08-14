import sys
import os
import re
import gradio as gr
import subprocess
import sys
import shlex

NIGHTLY_REGEX = re.compile(r"^20\d{2}-\d{2}-\d{2}$")

def run_detection(selected_folders, yolo_model, imsz, gen_bot, overwrite_bot):
    import subprocess

    if not selected_folders:
        yield "No nightly folders selected.\n"
        return

    output_log = ""

    for folder in selected_folders:
        output_log += f"--- Running detection for {folder} ---\n"
        yield output_log

        cmd = [
            sys.executable,
            "Mothbot_Detect.py",
            "--input_path", folder,
            "--yolo_model", yolo_model,
            "--imgsz", str(imsz),
            "--gen_bot_det_evenif_human_exists", str(gen_bot),
            "--overwrite_prev_bot_detections", str(overwrite_bot),
        ]

        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )

            for line in iter(process.stdout.readline, ''):
                cleaned_line = line.replace('\r', '')
                output_log += cleaned_line
                yield output_log

            process.stdout.close()
            process.wait()

            if process.returncode != 0:
                output_log += f"\n❌ Detection for {folder} exited with error code {process.returncode}\n"
            else:
                output_log += f"✅ Detection completed for {folder}\n"

            yield output_log

        except Exception as e:
            output_log += f"\n❌ Exception while processing {folder}: {str(e)}\n"
            yield output_log




def select_folder():
    """Open a native folder picker and return the selected folder path (or None)."""
    if sys.platform == "win32":
        from tkinter import Tk, filedialog
        tk = Tk()
        tk.withdraw()
        folder_selected = filedialog.askdirectory()
        tk.destroy()
    else:
        try:
            import webview
            _WINDOW = webview.create_window("Select Folder", hidden=True)
            result = _WINDOW.create_file_dialog(webview.FOLDER_DIALOG)
            folder_selected = result[0] if result else None
        except Exception:
            folder_selected = None
    return folder_selected or None

def find_nightly_folders_recursive(directory):
    matches = []
    if NIGHTLY_REGEX.match(os.path.basename(directory)):
        matches.append(os.path.abspath(directory))
    for root, dirs, _ in os.walk(directory):
        for d in dirs:
            if NIGHTLY_REGEX.match(d):
                matches.append(os.path.join(root, d))
    return sorted(matches)

def pick_and_list():
    folder = select_folder()
    if not folder:
        return "No folder selected.", gr.update(choices=[], value=[]), {}, "Select All"

    matches = find_nightly_folders_recursive(folder)
    if not matches:
        return f"Selected folder: {folder}\nNo nightly subfolders found.", gr.update(choices=[], value=[]), {}, "Select All"

    labels = []
    mapping = {}
    for p in matches:
        label = os.path.basename(os.path.dirname(p)) + "/" + os.path.basename(p)
        base = label
        i = 1
        while label in mapping:
            label = f"{base} ({i})"
            i += 1
        labels.append(label)
        mapping[label] = os.path.abspath(p)

    status = f"Selected folder: {folder}\nFound {len(labels)} nightly folders."
    return status, gr.update(choices=labels, value=[]), mapping, "Select All"

def toggle_select_all(current_values, mapping, button_label):
    """Toggles between selecting all and deselecting all."""
    if button_label == "Select All":
        return gr.update(value=list(mapping.keys())), "Deselect All"
    else:
        return gr.update(value=[]), "Select All"

def confirm_selection(selected_labels, mapping):
    if not selected_labels:
        return []
    return [mapping[label] for label in selected_labels if label in mapping]


# ----- UI STUFF --------------

with gr.Blocks() as demo:
    with gr.Tab("Deployments"):
        gr.Markdown("### Pick a main folder of Deployments to process: ")
        
        with gr.Row():
            status = gr.Textbox(label="Status", lines=3, interactive=False)
            pick_btn = gr.Button("Pick Main Folder (native dialog)")
        
        mapping_state = gr.State({})
        toggle_label_state = gr.State("Select All")

        gr.Markdown("### Nightly Folders to be Processed:")


        with gr.Row():
            folder_choices = gr.CheckboxGroup(label="Nightly Folders", choices=[], value=[], interactive=True)
            with gr.Column():
                toggle_all_btn = gr.Button("Select All")
                confirm_btn = gr.Button("Confirm Selected")

        selected_paths = gr.JSON(label="Confirmed Nightly Folders to be Processed")

        pick_btn.click(fn=pick_and_list, outputs=[status, folder_choices, mapping_state, toggle_label_state])
        toggle_all_btn.click(fn=toggle_select_all,
                             inputs=[folder_choices, mapping_state, toggle_label_state],
                             outputs=[folder_choices, toggle_label_state])
        toggle_label_state.change(lambda lbl: gr.update(value=lbl), inputs=toggle_label_state, outputs=toggle_all_btn)
        confirm_btn.click(fn=confirm_selection, inputs=[folder_choices, mapping_state], outputs=selected_paths)

    with gr.Tab("Detect"):
        gr.Markdown("### Detection Settings")

        selected_from_deployments = gr.JSON(label="Nightly Folders", value=[])
        with gr.Row():
            # YOLO model selection
            yolo_model_path = gr.Textbox(
                value=r"../AI/trained_models/yolo11m_4500_imgsz1600_b1_2024-01-18/weights/yolo11m_4500_imgsz1600_b1_2024-01-18.pt",
                label="YOLO Model Path"
            )
            yolo_model_file = gr.File(label="Choose a YOLO .pt file", file_types=[".pt"], type="filepath")

            def update_yolo_path(file_obj):
                if file_obj is not None:
                    return file_obj.name
                return gr.update()

            yolo_model_file.change(update_yolo_path, inputs=yolo_model_file, outputs=yolo_model_path)
            with gr.Column():
                imgsz = gr.Number(label="🖼️ Image Size", value=1600)

                GEN_BOT_DET_EVENIF_HUMAN_EXISTS = gr.Checkbox(
                    value=True, label="GEN_BOT_DET_EVENIF_HUMAN_EXISTS"
                )
                OVERWRITE_PREV_BOT_DETECTIONS = gr.Checkbox(
                    value=False, label="OVERWRITE_PREV_BOT_DETECTIONS"
                )

        # Keep Detect tab synced with Deployments
        selected_paths.change(lambda val: gr.update(value=val), inputs=selected_paths, outputs=selected_from_deployments)

        # Run detection button
        run_btn = gr.Button("Run Detection", variant="primary")

        output_box = gr.Textbox(label="Detection Output", lines=20)

        run_btn.click(
            fn=run_detection,
            inputs=[
                selected_paths,
                yolo_model_path,
                imgsz,
                GEN_BOT_DET_EVENIF_HUMAN_EXISTS,
                OVERWRITE_PREV_BOT_DETECTIONS
            ],
            outputs=output_box
        )

    with gr.Tab("ID"):
        gr.Markdown("### ID tab placeholder")

    with gr.Tab("Create Dataset"):
        gr.Markdown("### Create Dataset tab placeholder")

    with gr.Tab("Create CSV"):
        gr.Markdown("### Create CSV tab placeholder")

demo.launch(inbrowser=True)
