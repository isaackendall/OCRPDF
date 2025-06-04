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