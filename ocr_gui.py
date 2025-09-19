"""Tkinter-based front end for ``ocrmypdf``.

This simple GUI lets users select one or more PDF files and run OCR on them
using ``ocrmypdf``. The OCR command always includes ``--force-ocr`` to ensure
text layers are regenerated. Large images can be skipped by supplying a value
for the ``--skip-big`` option.
"""

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import subprocess
import threading
import os
import shutil
import queue


def find_ocrmypdf():
    """Return the path to ``ocrmypdf`` or ``None`` if it cannot be located."""
    ocr_path = shutil.which("ocrmypdf")
    if not ocr_path:
        messagebox.showerror(
            "Error",
            "The 'ocrmypdf' command was not found.\n"
            "Install it and ensure it is available on your PATH."
        )
        return None
    return ocr_path


class OCRApp:
    """Main application window for running ``ocrmypdf`` on selected PDFs."""

    # Constants
    DEFAULT_MAX_MEGAPIXELS = "10"
    MAX_RETRIES = 3

    def __init__(self, root):
        """Configure the UI and initialize state."""
        self.root = root
        self.root.title("OCR GUI App")

        self.ocrmypdf_path = find_ocrmypdf()
        if not self.ocrmypdf_path:
            self.root.destroy()
            return

        # Initialize parameters
        self.files = []            # List of selected PDF files
        self.output_folder = ""    # Output folder
        self.max_megapixels = tk.StringVar(value=self.DEFAULT_MAX_MEGAPIXELS)
        self.overwrite_existing = tk.BooleanVar(value=False)

        # Processing state
        self.is_processing = False
        self.total_files = 0
        self.current_file = 0
        self.should_cancel = False

        self.log_queue = queue.Queue()

        self.create_widgets()
        self.update_log()  # Start log updating loop

    def create_widgets(self):
        """Build the application widgets."""
        frame = tk.Frame(self.root)
        frame.pack(padx=10, pady=10)

        # Button to select PDF files
        tk.Button(frame, text="Select PDF Files", command=self.select_files)\
            .grid(row=0, column=0, padx=5, pady=5)
        self.files_label = tk.Label(frame, text="No files selected")
        self.files_label.grid(row=0, column=1, padx=5, pady=5)

        # Button to select output folder
        tk.Button(frame, text="Select Output Folder", command=self.select_output_folder)\
            .grid(row=1, column=0, padx=5, pady=5)
        self.output_label = tk.Label(frame, text="No output folder selected")
        self.output_label.grid(row=1, column=1, padx=5, pady=5)

        # Entry for max megapixels
        tk.Label(frame, text="Max Megapixels:").grid(row=2, column=0, padx=5, pady=5)
        tk.Entry(frame, textvariable=self.max_megapixels)\
            .grid(row=2, column=1, padx=5, pady=5)

        # Checkbox for overwriting existing files
        tk.Checkbutton(frame, text="Overwrite existing files", variable=self.overwrite_existing)\
            .grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        # Progress bar and label
        self.progress_var = tk.DoubleVar()
        self.progress_label = tk.Label(frame, text="Ready")
        self.progress_label.grid(row=4, column=0, columnspan=2, padx=5, pady=5)
        self.progress_bar = ttk.Progressbar(frame, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        # Button frame for Start and Cancel buttons
        button_frame = tk.Frame(frame)
        button_frame.grid(row=6, column=0, columnspan=2, padx=5, pady=10)

        # Action buttons
        self.start_button = tk.Button(button_frame, text="Start OCR", command=self.start_ocr)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.cancel_button = tk.Button(button_frame, text="Cancel",
                                       command=self.cancel_processing, state="disabled")
        self.cancel_button.pack(side=tk.LEFT, padx=5)

        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        self.status_bar = tk.Label(self.root, textvariable=self.status_var,
                                   bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Log output area (scrollable)
        self.log_text = scrolledtext.ScrolledText(self.root, width=60, height=20, state='disabled')
        self.log_text.pack(padx=10, pady=10)

    def select_files(self):
        """Open a dialog to choose PDF files for processing."""
        files = filedialog.askopenfilenames(
            title="Select PDF Files",
            filetypes=[("PDF Files", "*.pdf")],
        )
        if files:
            self.files = list(files)
            self.files_label.config(text=f"{len(self.files)} file(s) selected")
        else:
            self.files_label.config(text="No files selected")

    def select_output_folder(self):
        """Prompt the user for the folder to store OCR results."""
        folder = filedialog.askdirectory(title="Select Output Folder")
        if folder:
            self.output_folder = folder
            self.output_label.config(text=self.output_folder)
        else:
            self.output_label.config(text="No output folder selected")

    def log(self, message):
        """Add a message to the log queue."""
        self.log_queue.put(message)

    def update_log(self):
        """Periodically pull messages from the queue and display them."""
        try:
            while True:
                message = self.log_queue.get_nowait()
                self.log_text.config(state='normal')
                self.log_text.insert(tk.END, message + "\n")
                self.log_text.config(state='disabled')
                self.log_text.see(tk.END)
        except queue.Empty:
            pass
        self.root.after(100, self.update_log)

    def cancel_processing(self):
        """Signal the processing thread to stop."""
        if self.is_processing:
            self.should_cancel = True
            self.status_var.set("Cancelling...")
            self.log("Cancelling processing...")

    def start_ocr(self):
        """Validate input and start the OCR thread."""
        if not self.files:
            messagebox.showerror("Error", "No PDF files selected.")
            return
        if not self.output_folder:
            messagebox.showerror("Error", "No output folder selected.")
            return
        try:
            max_mp = float(self.max_megapixels.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid max megapixels value.")
            return

        self.should_cancel = False
        self.is_processing = True
        self.start_button.config(state="disabled")
        self.cancel_button.config(state="normal")
        self.status_var.set("Processing...")
        self.log("Starting OCR processing...")

        # Run OCR processing in a separate thread to keep the GUI responsive
        threading.Thread(target=self.process_files, args=(max_mp,), daemon=True).start()

    def process_files(self, max_mp):
        """Run OCR on the selected files."""
        try:
            self.total_files = len(self.files)
            for index, file in enumerate(self.files):
                if self.should_cancel:
                    self.log("Processing cancelled by user.")
                    break

                self.current_file = index + 1
                self.update_progress()

                for retry in range(self.MAX_RETRIES):
                    try:
                        base_name = os.path.splitext(os.path.basename(file))[0]
                        output_file = os.path.join(self.output_folder, f"{base_name}_OCR.pdf")

                        if os.path.exists(output_file) and not self.overwrite_existing.get():
                            self.log(f"Skipping: {output_file} already exists.")
                            break

                        self.log(f"Processing: {file}")
                        self.status_var.set(
                            f"Processing file {self.current_file} of {self.total_files}")
                        command = [
                            self.ocrmypdf_path,
                            "--force-ocr",
                            "--skip-big",
                            str(max_mp),
                            "--continue-on-soft-render-error",
                            file,
                            output_file,
                        ]
                        self.log("Running: " + " ".join(command))
                        try:
                            subprocess.run(
                                command,
                                capture_output=True,
                                text=True,
                                check=True,
                            )
                            self.log(f"Successfully processed: {file} -> {output_file}")
                            break
                        except subprocess.CalledProcessError as exc:
                            error_msg = exc.stderr.strip() or exc.stdout.strip()
                            self.log(f"Error processing {file}: {error_msg}")
                            if retry == self.MAX_RETRIES - 1:
                                messagebox.showerror(
                                    "Error",
                                    f"Failed to process {file}:\n{error_msg}",
                                )
                    except Exception as e:
                        if retry == self.MAX_RETRIES - 1:
                            self.log(f"Failed after {self.MAX_RETRIES} attempts: {file}")
                            messagebox.showerror("Error", f"Failed to process {file}:\n{str(e)}")
                            raise
                        self.log(f"Retry {retry + 1}/{self.MAX_RETRIES} for {file}")
        finally:
            self.is_processing = False
            self.should_cancel = False
            self.root.after(0, lambda: self.start_button.config(state="normal"))
            self.root.after(0, lambda: self.cancel_button.config(state="disabled"))
            self.root.after(0, lambda: self.status_var.set("Ready"))

    def update_progress(self):
        """Refresh the progress bar and label."""
        progress = (self.current_file / self.total_files) * 100
        self.progress_var.set(progress)
        self.progress_label.config(
            text=f"Processing: {self.current_file}/{self.total_files} files"
        )


def main():
    """Launch the OCR GUI application."""
    root = tk.Tk()
    OCRApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
