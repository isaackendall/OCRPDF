# PDF OCR Application

A simple GUI application for performing OCR (Optical Character Recognition) on PDF files using ocrmypdf. This application allows you to:
- Batch process multiple PDF files
- Choose output directory
- Configure OCR settings
- View detailed processing logs

## Prerequisites

- Python 3.7 or higher
- [ocrmypdf](https://ocrmypdf.readthedocs.io/) (requires Tesseract OCR)
  - **macOS**: `brew install tesseract ocrmypdf`
  - **Linux (Debian/Ubuntu)**: 
    ```bash
    sudo apt install tesseract-ocr
    pip install ocrmypdf
    ```
  - **Windows**: 
    - Install [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki)
    - `pip install ocrmypdf`
- Tkinter (usually comes with Python)
  - **Linux**: `sudo apt install python3-tk`

## Installation

1. Clone this repository:
```bash
git clone https://github.com/isaackendall/OCRPDF.git
cd OCRPDF
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

- The application requires ocrmypdf and Tesseract OCR to be installed on your system
- Processed files will be saved with "_OCR" appended to the original filename
- The log area shows detailed information about the processing status
- For large PDFs, consider increasing the maximum megapixels value if pages are being skipped

## Building an Executable

You can create a standalone executable using [PyInstaller](https://pyinstaller.org/):

1. First install PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Build the executable:
   ```bash
   pyinstaller --onefile --windowed ocr_gui.py
   ```

The resulting executable will be in the `dist/` folder. Note that users will still need to have `ocrmypdf` and Tesseract OCR installed on their system.

## Installing as a Package

You can install the application as a Python package:

```bash
# Install in development mode
pip install -e .

# Run the application
ocr-gui
```

## License

This project is open source and available under the [MIT License](LICENSE).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and feature requests, please [open an issue](https://github.com/isaackendall/OCRPDF/issues).
