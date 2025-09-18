import sys
import os
import re
import gradio as gr
#import subprocess
import sys
#import shlex
import tkinter as tk
from tkinter import filedialog
from multiprocessing import Process, Queue

NIGHTLY_REGEX = re.compile(r"^20\d{2}-\d{2}-\d{2}$")


TAXA_COLS = ["kingdom", "phylum", "class", "order", "family", "genus", "species"]




# A function that runs in a separate process to handle the folder dialog
def show_folder_dialog(queue):
    """
    Function to run in a separate process to safely open the folder dialog.
    """
    try:
        root = tk.Tk()
        root.withdraw()
        folder_path = filedialog.askdirectory()
        root.destroy()
        queue.put(folder_path)
    except Exception as e:
        queue.put(None)

# A function that runs in a separate process to handle the file dialog
def show_file_dialog(queue):
    """
    Function to run in a separate process to safely open the file dialog.
    """
    try:
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename()
        root.destroy()
        queue.put(file_path)
    except Exception as e:
        queue.put(None)

# Main function for the Gradio interface to get the folder path
def get_folder_path():
    """
    This function spawns a new process to handle the folder dialog
    and waits for the result.
    """
    queue = Queue()
    p = Process(target=show_folder_dialog, args=(queue,))
    p.start()
    p.join()
    folder_path = queue.get()

    if folder_path:
        print(f"Selected folder: {folder_path}")
        return folder_path
    else:
        print ("No folder selected or an error occurred.")
        return None

# Main function for the Gradio interface to get the file path
def get_file_path():
    """
    This function spawns a new process to handle the file dialog
    and waits for the result.
    """
    queue = Queue()
    p = Process(target=show_file_dialog, args=(queue,))
    p.start()
    p.join()
    file_path = queue.get()

    if file_path:
        return f"Selected file: {file_path}"
    else:
        return "No file selected or an error occurred."









def get_index(selected_word):
    return TAXA_COLS.index(selected_word)


def dataset_update_radio_options(selected_folders):
    # Ensure we hand Radio a list of strings
    choices = [str(x) for x in selected_folders] if isinstance(selected_folders, list) else []
    # Return a generic update (works across Gradio versions)
    return gr.update(choices=choices, value=None)  # or value=choices[0] to auto-select first

def dataset_use_selected_folder(folder):
    return f"{folder}" if folder else "No folder selected."

def run_detection(selected_folders, yolo_model, imsz, overwrite_bot):
    import subprocess
    #print("OVERWRITE DET")
    #print(overwrite_bot)
    if not selected_folders:
        yield "No nightly folders selected.\n"
        return

    output_log = ""

    for folder in selected_folders:
        output_log += f"---🕵🏾‍♀️ Running detection for {folder} ---\n"
        yield output_log

        cmd = [
            sys.executable,
            "Mothbot_Detect.py",
            "--input_path", folder,
            "--yolo_model", yolo_model,
            "--imgsz", str(imsz),
            #"--gen_bot_det_evenif_human_exists", str(gen_bot),
            "--overwrite_prev_bot_detections", str(int(overwrite_bot)),
        ]
        #needed to add some stuff here to catch weird char encoding errors thrown by YOLO
        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,  # line-buffered
                encoding="utf-8",      # force utf-8 decoding
                errors="replace"       # or "ignore" to drop bad bytes
            )

            # Read output line by line until process finishes
            while True:
                line = process.stdout.readline()
                if not line and process.poll() is not None:
                    break  # process ended
                if line:
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




def run_ID(selected_folders, species_list, chosenrank, IDHum,IDBot, overwrite_bot):
    import subprocess
    
    if not selected_folders:
        yield "No nightly folders selected.\n"
        return

    output_log = ""

    for folder in selected_folders:
        output_log += f"---🔍 Running IDENTIFICATION for {folder} ---\n"
        yield output_log

        cmd = [
            sys.executable,
            "Mothbot_ID.py",
            "--input_path", folder,
            "--taxa_csv", species_list,
            "--rank", str(chosenrank),
            "--ID_Hum", str(int(IDHum)),
            "--ID_Bot", str(int(IDBot)),
            "--overwrite_prev_bot_ID",str(int(overwrite_bot))
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
                output_log += f"\n❌ Identification for {folder} exited with error code {process.returncode}\n"
            else:
                output_log += f"✅ Identification completed for {folder}\n"

            yield output_log

        except Exception as e:
            output_log += f"\n❌ Exception while processing {folder}: {str(e)}\n"
            yield output_log
    output_log += f"------ ID processing finished ------"


def run_Dataset(selected_folder, species_list, metadata, Utcoffset):
    import subprocess
    
    if not selected_folder:
        yield "No nightly folder selected.\n"
        return

    output_log = ""
    folder=selected_folder
    output_log += f"---📋 Creating Dataset for {folder} ---\n"
    yield output_log

    cmd = [
        sys.executable,
        "Mothbot_CreateDataset.py",
        "--input_path", folder,
        "--taxa_csv", species_list,
        "--metadata", str(metadata),
        "--utcoff", str(int(Utcoffset)),

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
            output_log += f"\n❌ Create dataset for {folder} exited with error code {process.returncode}\n"
        else:
            output_log += f"✅ Create Dataset completed for {folder}\n"

        yield output_log

    except Exception as e:
        output_log += f"\n❌ Exception while Create Dataset processing {folder}: {str(e)}\n"
        yield output_log
    output_log += f"------ CreateDataset processing finished ------"
    yield output_log



def run_CSV(selected_folders, species_list, Utcoffset):
    import subprocess
    
    if not selected_folders:
        yield "No nightly folders selected.\n"
        return

    output_log = ""


    converted_folders = []  # List to store paths of folders with samples.json

    for folder in selected_folders:
        output_log += f"---🔍 Generating CSVs for Datasets in {folder} ---\n"
        yield output_log

        for root, _, files in os.walk(folder):
            if "samples.json" in files:
                output_log += f"Found 'samples.json' in {root}\n"  # Log the location
                converted_folders.append(root)  # Add to the list
                #break  # Stop searching once found

    if converted_folders:
        print("Executing commands on the following folders:")
        for folder in converted_folders:
            cmd = [
                sys.executable,
                "Mothbot_ConvertDatasettoCSV.py",
                "--input_path", folder,
                "--taxa_csv", species_list,
                "--utcoff", str(int(Utcoffset)),
            ]
            print(f"Executing command: {cmd}") # Debugging


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
                    output_log += f"\n❌ CSV for {folder} exited with error code {process.returncode}\n"
                else:
                    output_log += f"✅ CSV completed for {folder}\n"

                yield output_log

            except Exception as e:
                output_log += f"\n❌ Exception while processing {folder}: {str(e)}\n"
                yield output_log
    output_log += f"------ CSV processing finished ------"
    yield output_log

# DON't use this anymore, doesnt work on 75% of computers
def select_folder_old():
    """Open a native folder picker and return the selected folder path (or None)."""
    print(sys.platform)
    if sys.platform == "win32":
        tk = Tk()
        tk.withdraw()
        folder_selected = filedialog.askdirectory()
        tk.destroy()
    else:
        try:
            import webview
            _WINDOW = webview.create_window("Select Folder", hidden=True)
            datafolder_result = _WINDOW.create_file_dialog(webview.FOLDER_DIALOG)
            folder_selected = datafolder_result[0] if datafolder_result else None
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
    folder = get_folder_path()
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

with gr.Blocks(title="Mothbot") as demo:
    # ~~~~~~~~ DEPLOYMENT TAB ~~~~~~~~~~~~~~~~~~~
    with gr.Tab("Deployments"):
        gr.Markdown("### Pick a main folder of Deployments to process: ")
        
        with gr.Row():
            status = gr.Textbox(label="Status", lines=3, interactive=False)
            pick_btn = gr.Button("Pick Deployment Folder")
        
        mapping_state = gr.State({})
        toggle_label_state = gr.State("Select All")

        gr.Markdown("### Nightly Folders to be Processed:")
        
        with gr.Row():
            folder_choices = gr.CheckboxGroup(label="Nightly Folders", choices=[], value=[], interactive=True)
            with gr.Column():
                toggle_all_btn = gr.Button("Select All")
                #confirm_btn = gr.Button("Confirm Selected")  # You can keep this if you still want manual confirm

        selected_paths = gr.JSON(label="Confirmed Nightly Folders to be Processed")

        pick_btn.click(
            fn=pick_and_list,
            outputs=[status, folder_choices, mapping_state, toggle_label_state]
        )

        toggle_all_btn.click(
            fn=toggle_select_all,
            inputs=[folder_choices, mapping_state, toggle_label_state],
            outputs=[folder_choices, toggle_label_state]
        )

        toggle_label_state.change(
            lambda lbl: gr.update(value=lbl),
            inputs=toggle_label_state,
            outputs=toggle_all_btn
        )

        #Update JSON automatically on checkbox changes
        folder_choices.change(
            fn=confirm_selection,  # Same function you used before
            inputs=[folder_choices, mapping_state],
            outputs=selected_paths
        )




    #~~~~~~~~~~~~ DETECTION TAB ~~~~~~~~~~~~~~~~~~~~~~
    with gr.Tab("Detect"):
        gr.Markdown("### Detection Settings")

        selected_from_deployments = gr.JSON(label="Nightly Folders", value=[])
        with gr.Row():
            # YOLO model selection
            yolo_model_path = gr.Textbox(
                value=r"../trained_models/yolo11m_4500_imgsz1600_b1_2024-01-18/weights/yolo11m_4500_imgsz1600_b1_2024-01-18.pt",
                label="YOLO Model Path",
                scale=1
            )
            yolo_model_file = gr.File(label="Choose a YOLO .pt file", file_types=[".pt"], height=120, type="filepath")

            def update_yolo_path(file_obj):
                if file_obj is not None:
                    return file_obj.name
                return gr.update()

            yolo_model_file.change(update_yolo_path, inputs=yolo_model_file, outputs=yolo_model_path)
            with gr.Column():
                imgsz = gr.Number(label="🖼️ Image Size", value=1600)

                ''' # Not sure when we use this?
                GEN_BOT_DET_EVENIF_HUMAN_EXISTS = gr.Checkbox(
                    value=True, label="GEN_BOT_DET_EVENIF_HUMAN_EXISTS"
                )
                '''
                OVERWRITE_PREV_BOT_DETECTIONS = gr.Checkbox(
                    value=False, label="OVERWRITE_PREV_BOT_DETECTIONS"
                )

        # Keep Detect tab synced with Deployments
        selected_paths.change(lambda val: gr.update(value=val), inputs=selected_paths, outputs=selected_from_deployments)

        # Run detection button
        DET_run_btn = gr.Button("Run Detection", variant="primary")

        DET_output_box = gr.Textbox(label="Detection Output", lines=20)

        DET_run_btn.click(
            fn=run_detection,
            inputs=[
                selected_paths,
                yolo_model_path,
                imgsz,
                OVERWRITE_PREV_BOT_DETECTIONS
            ],
            outputs=DET_output_box
        )
    #~~~~~~~~~~~~ IDENTIFICATION TAB ~~~~~~~~~~~~~~~~~~~~~~

    with gr.Tab("ID"):
        selected_from_deployments = gr.JSON(label="Nightly Folders", value=[])

        with gr.Row():
            # Species selection
            species_path = gr.Textbox(
                #default path
                value=r"../SpeciesList_CountryIndonesia_TaxaInsecta.csv",
                label="Species List CSV"
            )
            species_csv_file = gr.File(label="Choose a Species List CSV File", file_types=[".csv"], height=120, type="filepath")

            def update_species_path(file_obj):
                if file_obj is not None:
                    return file_obj.name
                return gr.update()
            species_csv_file.change(update_species_path, inputs=species_csv_file, outputs=species_path)

        with gr.Row():
            with gr.Column():
                gr.Markdown("### Select how deep you want to try to automatically Identify:")
                radio = gr.Radio(TAXA_COLS, label="Select one", type="value", value="order")
                taxa_output = gr.Number(label="Index",value=TAXA_COLS.index("order"))
                radio.change(get_index, inputs=radio, outputs=taxa_output)
    
            with gr.Column():
                ID_HUMANDETECTIONS = gr.Checkbox(
                    value=True, label="Identify Human Detections"
                )
                ID_BOTDETECTIONS = gr.Checkbox(
                    value=True, label="Identify Human Detections"
                )
                OVERWRITE_PREV_BOT_IDENTIFICATIONS = gr.Checkbox(
                    value=False, label="OVERWRITE_PREV_BOT_IDENTIFICATIONS"
                )

        # Keep ID tab synced with Deployments
        selected_paths.change(lambda val: gr.update(value=val), inputs=selected_paths, outputs=selected_from_deployments)

        # Run ID button
        ID_run_btn = gr.Button("Run Identification", variant="primary")

        ID_output_box = gr.Textbox(label="Identification Output", lines=20)

        ID_run_btn.click(
            fn=run_ID,
            inputs=[
                selected_paths,
                species_path,
                taxa_output,
                ID_HUMANDETECTIONS,
                ID_BOTDETECTIONS,
                OVERWRITE_PREV_BOT_IDENTIFICATIONS
            ],
            outputs=ID_output_box
        )

    #~~~~~~~~~~~~ Create Dataset TAB ~~~~~~~~~~~~~~~~~~~~~~
    with gr.Tab("Create Dataset"):
        selected_from_deployments = gr.JSON(label="Nightly Folders", value=[])

        with gr.Row():
            # Metadata selection
            metadata_path = gr.Textbox(
                #default path
                value=r"../Mothbox_Main_Metadata_Field_Sheet_Example - Form responses 1.csv",
                label="Metadata CSV"
            )
            metadata_csv_file = gr.File(label="Choose a Metadata CSV File", file_types=[".csv"], height=120, type="filepath")

            def update_metadata_path(file_obj):
                if file_obj is not None:
                    return file_obj.name
                return gr.update()

            metadata_csv_file.change(update_metadata_path, inputs=metadata_csv_file, outputs=metadata_path)
        with gr.Row():
            # Species selection
            species_path = gr.Textbox(
                #default path
                value=r"../SpeciesList_CountryIndonesia_TaxaInsecta.csv",
                label="Species List CSV"
            )
            species_csv_file = gr.File(label="Choose a Species List CSV File", file_types=[".csv"], height=120, type="filepath")

            def update_species_path(file_obj):
                if file_obj is not None:
                    return file_obj.name
                return gr.update()
            species_csv_file.change(update_species_path, inputs=species_csv_file, outputs=species_path)

        UTCoff = gr.Number(label="🕙 UTC Offset:", value=-5)
       

        # Keep Dataset tab synced with Deployments
        selected_paths.change(lambda val: gr.update(value=val), inputs=selected_paths, outputs=selected_from_deployments)

        #Choose which folder to dataset
        single_folder_choice = gr.Radio(label="Select One Folder", choices=[], interactive=True)
        
        datafolder_result = gr.Textbox(label="Result")
        
        # Whenever the JSON changes, update the Radio choices
        selected_from_deployments.change(
            fn=dataset_update_radio_options,
            inputs=selected_from_deployments,
            outputs=single_folder_choice
        )
        
        # When user selects a folder, pass it to a function
        single_folder_choice.change(
            fn=dataset_use_selected_folder,
            inputs=single_folder_choice,
            outputs=datafolder_result
        )


        # Run Create Dataset button
        Dataset_run_btn = gr.Button("Create Dataset", variant="primary")

        Dataset_output_box = gr.Textbox(label="Dataset Creation Output", lines=20)

        Dataset_run_btn.click(
            fn=run_Dataset,
            inputs=[
                datafolder_result,
                species_path,
                metadata_path,
                UTCoff,
            ],
            outputs=Dataset_output_box
        )

    #~~~~~~~~~~~~ Create CSV TAB ~~~~~~~~~~~~~~~~~~~~~~
    with gr.Tab("Generate CSV"):
        selected_from_deployments = gr.JSON(label="Nightly Folders", value=[])

        with gr.Row():
            # Metadata selection
            metadata_path = gr.Textbox(
                #default path
                value=r"../Mothbox_Main_Metadata_Field_Sheet_Example - Form responses 1.csv",
                label="Metadata CSV"
            )
            metadata_csv_file = gr.File(label="Choose a Metadata CSV File", file_types=[".csv"], height=120, type="filepath")

            def update_metadata_path(file_obj):
                if file_obj is not None:
                    return file_obj.name
                return gr.update()

            metadata_csv_file.change(update_metadata_path, inputs=metadata_csv_file, outputs=metadata_path)
        with gr.Row():
            # Species selection
            species_path = gr.Textbox(
                #default path
                value=r"../SpeciesList_CountryIndonesia_TaxaInsecta.csv",
                label="Species List CSV"
            )
            species_csv_file = gr.File(label="Choose a Species List CSV File", file_types=[".csv"], height=120, type="filepath")

            def update_species_path(file_obj):
                if file_obj is not None:
                    return file_obj.name
                return gr.update()
            species_csv_file.change(update_species_path, inputs=species_csv_file, outputs=species_path)

        UTCoff = gr.Number(label="🕙 UTC Offset:", value=-5)
       

        # Keep Dataset tab synced with Deployments
        selected_paths.change(lambda val: gr.update(value=val), inputs=selected_paths, outputs=selected_from_deployments)


        # Run CSV button
        CSV_run_btn = gr.Button("Generate CSV ", variant="primary")

        CSV_output_box = gr.Textbox(label="CSV Creation Output", lines=20)

        CSV_run_btn.click(
            fn=run_CSV,
            inputs=[
                selected_paths,
                species_path,
                UTCoff,
            ],
            outputs=CSV_output_box
        )
if __name__ == "__main__":
    demo.launch(inbrowser=True, favicon_path='favicon.png')
