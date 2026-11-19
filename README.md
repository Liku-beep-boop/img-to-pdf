# IMG2PDF

Desktop app to convert images into PDF files, with a dark "HUD" style interface.

Convierte imágenes a PDF desde una interfaz de escritorio con estilo HUD oscuro.

## Features

- Select images with a file dialog or **drag & drop** them into the window
- Image preview with options to **reorder** and **remove** files before converting
- Two modes:
  - Merge all images into **a single PDF**
  - Create **one PDF per image**
- Page sizes: **A4, Letter, Legal** or a **custom size** in millimeters
- Images are scaled to fit the page keeping their aspect ratio, and centered
- Custom output file name

## Tech stack

- Python 3
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) for the UI
- [tkinterdnd2](https://github.com/Eliav2/tkinterdnd2) for drag & drop
- [Pillow](https://python-pillow.org/) for image processing and PDF generation

## Getting started

```bash
git clone https://github.com/Liku-beep-boop/img-to-pdf.git
cd img-to-pdf
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux / macOS
pip install -r requirements.txt
python img2pdf_app.py
```

## Usage

1. Click **SELECCIONAR ARCHIVOS** or drag images into the drop area.
2. Reorder or remove images in the preview.
3. Choose the page size and the conversion mode.
4. (Optional) Type the output file name.
5. Click convert and choose the destination folder.
