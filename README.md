# border.py
# border.py

A lightweight photography utility for creating elegant Instagram-ready bordered images from portrait and landscape photographs.

border.py batch-processes images from a folder, automatically detects orientation, applies configurable white borders, optionally sharpens resized images, and exports polished JPEGs optimized for Instagram posting.

Designed especially for:
- film photographers
- scanned negatives
- fine-art presentation
- minimalist Instagram aesthetics
- gallery-style framing

---

# Features

## Portrait Processing

For every portrait image, border.py automatically creates TWO outputs:

### 1. Full Portrait Mode
- Preserves the full original 2:3 composition
- Places the image on a 3:4 white canvas
- Adds elegant whitespace above/below or around the image
- No cropping

### 2. Cropped Portrait Mode
- Crops the image to 3:4
- Adds symmetric white borders
- Optimized for Instagram feed presentation

---

## Landscape Processing

- Automatically detects landscape images using aspect-ratio thresholds
- Preserves arbitrary landscape aspect ratios
- Adds centered white borders
- Supports:
  - 3:2
  - 16:9
  - panoramic crops
  - irregular aspect ratios

---

## Additional Features

- EXIF-aware auto rotation
- TIFF/TIF support
- Batch folder processing
- Optional sharpening after resize
- Configurable border thickness
- High-quality JPEG export
- Instagram-ready resolutions
- Cross-platform (Windows/macOS/Linux)

---

# Example Workflow

Input:

```text
input/
    image001.jpg
    image002.tif
```

Output:

```text
output/
    image001_portrait_full.jpg
    image001_portrait_crop.jpg
    image002_landscape.jpg
```

---

# Installation

## 1. Install Python

Download Python:

https://www.python.org/downloads/

---

## 2. Install Pillow

```bash
pip install pillow
```

---

# Usage

Place images into the `input/` folder.

Run:

```bash
python border_tool.py
```

Processed images will appear in:

```text
output/
```

---

# Supported File Types

Input:
- JPG
- JPEG
- PNG
- TIF
- TIFF

Output:
- JPG

---

# Configuration

Inside `border_tool.py`:

```python
EXPORT_HEIGHT = 1800
BORDER_PERCENT = 0.06
JPEG_QUALITY = 95
```

---

# Sharpening

border.py optionally applies sharpening AFTER resizing for improved Instagram rendering.

Example:

```python
ImageFilter.UnsharpMask(
    radius=1.2,
    percent=140,
    threshold=2
)
```

---

# EXIF Handling

border.py automatically corrects EXIF orientation metadata using:

```python
ImageOps.exif_transpose()
```

This ensures portrait images exported from phones, Lightroom, scanners, and cameras are handled correctly.

---

# Future Plans

- GUI interface
- drag-and-drop support
- live preview
- border presets
- gallery-paper tones
- watermark/signature support
- Lightroom integration
- export presets
- adaptive canvas sizing

---

# Why "border.py"?

A border.py is the mat border surrounding framed artwork or photographic prints.

This project aims to bring that same gallery-style presentation aesthetic to digital photography and Instagram posting workflows.

---

# License

MIT License

See `LICENSE` for details.
