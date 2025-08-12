import sys
import os
import re
import gradio as gr

NIGHTLY_REGEX = re.compile(r"^20\d{2}-\d{2}-\d{2}$")

#This is hacked from the nice folks at Birdnet Analyzer who made this workaround so you can choose a folder with a Gradio interface (which is weirdly hard to do!)
def select_folder():
    """Open a native folder picker and return the selected folder path (or None)."""
    if sys.platform == "win32":
        from tkinter import Tk, filedialog
        tk = Tk()
        tk.withdraw()
        folder_selected = filedialog.askdirectory()
        tk.destroy()
    else:
        # fallback for non-Windows (pywebview may be available in your env)
        try:
            import webview
            _WINDOW = webview.create_window("Select Folder", hidden=True)
            result = _WINDOW.create_file_dialog(webview.FOLDER_DIALOG)
            folder_selected = result[0] if result else None
        except Exception:
            folder_selected = None
    return folder_selected or None

def find_nightly_folders_recursive(directory):
    """Recursively find folders named like YYYY-MM-DD anywhere under `directory`."""
    matches = []
    # include directory itself if it's a match
    if NIGHTLY_REGEX.match(os.path.basename(directory)):
        matches.append(os.path.abspath(directory))
    for root, dirs, _ in os.walk(directory):
        for d in dirs:
            if NIGHTLY_REGEX.match(d):
                matches.append(os.path.join(root, d))
    return sorted(matches)

def pick_and_list():
    """
    Handler for the "Pick Main Folder" button.
    Returns: (status_text, CheckboxGroup update, mapping dict)
    """
    folder = select_folder()
    if not folder:
        return "No folder selected.", gr.update(choices=[], value=[]), {}

    matches = find_nightly_folders_recursive(folder)
    if not matches:
        return f"Selected folder: {folder}\nNo nightly subfolders found.", gr.update(choices=[], value=[]), {}

    # Build short unique labels for UI, mapping labels -> full paths
    labels = []
    mapping = {}
    for p in matches:
        label = os.path.basename(os.path.dirname(p)) + "/" + os.path.basename(p)  # parent/date
        base = label
        i = 1
        while label in mapping:  # ensure uniqueness
            label = f"{base} ({i})"
            i += 1
        labels.append(label)
        mapping[label] = os.path.abspath(p)

    status = f"Selected folder: {folder}\nFound {len(labels)} nightly folders."
    # Set choices but leave value alone (we set value=[] once here to clear any previous selection)
    return status, gr.update(choices=labels, value=[]), mapping

def select_all(mapping):
    """Select every label currently in mapping (used by Select All button)."""
    if not mapping:
        return gr.update(value=[])
    return gr.update(value=list(mapping.keys()))

def deselect_all():
    """Clear selection."""
    return gr.update(value=[])

def confirm_selection(selected_labels, mapping):
    """Return the full paths for the selected labels."""
    if not selected_labels:
        return []
    return [mapping[label] for label in selected_labels if label in mapping]

# --- Gradio UI ---
with gr.Blocks() as demo:
    gr.Markdown("### Pick a main folder and select nightly subfolders (YYYY-MM-DD)\n\n"
                "Pick a folder → app recursively finds nightly folders → select any subset → Confirm to get full paths.")

    pick_btn = gr.Button("Pick Main Folder (native dialog)")
    status = gr.Textbox(label="Status", lines=3, interactive=False)

    # CheckboxGroup will show short labels; mapping_state stores label->fullpath dict
    mapping_state = gr.State({})

    # interactive=True makes the group clickable by the user
    folder_choices = gr.CheckboxGroup(label="Nightly Folders", choices=[], value=[], interactive=True)

    with gr.Row():
        select_all_btn = gr.Button("Select All")
        deselect_all_btn = gr.Button("Deselect All")
        confirm_btn = gr.Button("Confirm Selected")

    selected_paths = gr.JSON(label="Confirmed Nightly Full Paths")

    # Wire events
    # When user picks folder -> populate checkbox choices and mapping_state
    pick_btn.click(fn=pick_and_list, outputs=[status, folder_choices, mapping_state])

    # Select All / Deselect All use the mapping_state to know the available labels
    select_all_btn.click(fn=select_all, inputs=mapping_state, outputs=folder_choices)
    deselect_all_btn.click(fn=deselect_all, outputs=folder_choices)

    # Confirm returns the real full paths for the selected labels
    confirm_btn.click(fn=confirm_selection, inputs=[folder_choices, mapping_state], outputs=selected_paths)

demo.launch(inbrowser=True)
