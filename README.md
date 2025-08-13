# PDF OCR Application

A simple GUI application for performing OCR (Optical Character Recognition) on PDF files using ocrmypdf.

## Prerequisites

- Python 3.x
- [ocrmypdf](https://ocrmypdf.readthedocs.io/) (install with your package manager, e.g. `brew install ocrmypdf` on macOS)
- Tkinter (often installed with Python; on Linux install the `python3-tk` package)

## Installation

1. Clone this repository:
```bash
git clone <your-repository-url>
cd pdf-ocr-app
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On macOS/Linux
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:
```bash
python ocr_gui.py
```

2. In the GUI:
   - Click "Select PDF Files" to choose the PDF files you want to process
   - Click "Select Output Folder" to choose where to save the processed files
   - Adjust "Max Megapixels" if needed (default is 10)
   - Click "Start OCR" to begin processing

3. The progress bar will show the overall progress, and the log area will display detailed information about the processing.

## Features

- Batch processing of multiple PDF files
- Progress tracking
- Detailed logging
- Configurable maximum megapixels
- Skip existing files option

## Command options

The application invokes `ocrmypdf` with:

```
ocrmypdf --force-ocr --skip-big <max_mp> input.pdf output.pdf
```

`--force-ocr` ensures that a fresh text layer is created even if the PDF
already contains text. `--skip-big` allows you to avoid processing pages with
images larger than the specified megapixel limit.

## Notes

- The application requires ocrmypdf to be installed on your system
- Processed files will be saved with "_OCR" appended to the original filename
- The log area shows detailed information about the processing status

## Building an executable

You can create a standalone executable using [PyInstaller](https://pyinstaller.org/):

```bash
pyinstaller --onefile ocr_gui.py
```

The resulting program appears in the `dist/` folder and can be run without Python.

### Bundling `ocrmypdf`

The executable above still expects the `ocrmypdf` command to be installed on the
system. If you want the program to work on machines where `ocrmypdf` is not
already available, include the `ocrmypdf` binary during the build. First locate
its path:

```bash
which ocrmypdf
```

Then supply that path to PyInstaller using the `--add-binary` option. On
Windows use a semicolon (`;`) instead of a colon to separate the destination:

```bash
pyinstaller --onefile \
    --add-binary "/path/to/ocrmypdf:." \
    ocr_gui.py
```

Replace `/path/to/ocrmypdf` with the output of `which ocrmypdf`. The bundled
binary will be copied next to the executable so the application can find it at
runtime.

### Automatic installation

If the program cannot locate `ocrmypdf` when launched, it will prompt you to
install it using `pip`. This requires an internet connection and may take a
moment to complete.

## Installing as a package

Install the project using `pip` and run it from anywhere:

```bash
pip install .
ocr-gui
```
