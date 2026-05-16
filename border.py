from PIL import Image
from PIL import ImageFilter
from PIL import ImageOps
from pathlib import Path

# ============================================
# SETTINGS
# ============================================

INPUT_DIR = "input"
OUTPUT_DIR = "output"

EXPORT_HEIGHT = 1920
BORDER_PERCENT = 0.01

BACKGROUND_COLOR = (255, 255, 255)

JPEG_QUALITY = 95

SUPPORTED_EXTENSIONS = [
    ".jpg",
    ".jpeg",
    ".png",
    ".tif",
    ".tiff"
]

ENABLE_SHARPENING = True
ENABLE_SHARPENING_LANDSCAPE = True


SHARPEN_RADIUS = 0.8
SHARPEN_PERCENT = 80
SHARPEN_THRESHOLD = 2

def apply_sharpening(img):

    if ENABLE_SHARPENING:

        return img.filter(
            ImageFilter.UnsharpMask(
                radius=SHARPEN_RADIUS,
                percent=SHARPEN_PERCENT,
                threshold=SHARPEN_THRESHOLD
            )
        )

    return 

SHARPEN_RADIUS_LANDSCAPE = 0.4
SHARPEN_PERCENT_LANDSCAPE = 40
SHARPEN_THRESHOLD_LANDSCAPE = 1

def apply_sharpening_landscape(img):

    if ENABLE_SHARPENING_LANDSCAPE:

        return img.filter(
            ImageFilter.UnsharpMask(
                radius=SHARPEN_RADIUS_LANDSCAPE,
                percent=SHARPEN_PERCENT_LANDSCAPE,
                threshold=SHARPEN_THRESHOLD_LANDSCAPE
            )
        )

    return img

# ============================================

Path(OUTPUT_DIR).mkdir(exist_ok=True)


def crop_to_aspect(img, target_ratio):
    """
    Crop image to target aspect ratio.
    target_ratio = width / height
    """

    w, h = img.size
    current_ratio = w / h

    if current_ratio > target_ratio:
        # too wide
        new_w = int(h * target_ratio)
        left = (w - new_w) // 2

        return img.crop((left, 0, left + new_w, h))

    else:
        # too tall
        new_h = int(w / target_ratio)
        top = (h - new_h) // 2

        return img.crop((0, top, w, top + new_h))


# ============================================
# PORTRAIT MODE 1
# Full 2:3 image inside 3:4 canvas
# ============================================

def process_portrait_mode_1(img):

    canvas_w = int(EXPORT_HEIGHT * 3 / 4)
    canvas_h = EXPORT_HEIGHT

    canvas = Image.new("RGB", (canvas_w, canvas_h), BACKGROUND_COLOR)

    border = int(canvas_w * BORDER_PERCENT)

    available_w = canvas_w - 2 * border
    available_h = canvas_h - 2 * border

    img_copy = img.copy()

    img_copy.thumbnail((available_w, available_h), Image.LANCZOS)

    img_copy = apply_sharpening(img_copy)

    x = (canvas_w - img_copy.width) // 2
    y = (canvas_h - img_copy.height) // 2

    canvas.paste(img_copy, (x, y))

    return canvas


# ============================================
# PORTRAIT MODE 2
# Crop to 3:4 then add border
# ============================================

def process_portrait_mode_2(img):

    img_copy = img.copy()

    img_copy = crop_to_aspect(img_copy, 3 / 4)

    canvas_w = int(EXPORT_HEIGHT * 3 / 4)
    canvas_h = EXPORT_HEIGHT

    border = int(canvas_w * BORDER_PERCENT)

    target_w = canvas_w - 2 * border
    target_h = canvas_h - 2 * border

    img_copy = img_copy.resize((target_w, target_h), Image.LANCZOS)

    img_copy = apply_sharpening(img_copy)

    canvas = Image.new("RGB", (canvas_w, canvas_h), BACKGROUND_COLOR)

    canvas.paste(img_copy, (border, border))

    return canvas


# ============================================
# LANDSCAPE MODE
# ============================================

def process_landscape(img):
    """
    Preserve ANY landscape aspect ratio.
    Add even white borders.
    """

    # Instagram-friendly portrait canvas
    # Gives elegant bordered landscape presentation

    canvas_w = 1440
    canvas_h = 960

    border = int(canvas_w * BORDER_PERCENT)

    available_w = canvas_w - (1.5 * border)
    available_h = canvas_h - (1.5 * border)

    img_copy = img.copy()

    # Preserve aspect ratio automatically
    img_copy.thumbnail((available_w, available_h), Image.LANCZOS)

    img_copy = apply_sharpening_landscape(img_copy)

    canvas = Image.new(
        "RGB",
        (canvas_w, canvas_h),
        BACKGROUND_COLOR
    )

    x = (canvas_w - img_copy.width) // 2
    y = (canvas_h - img_copy.height) // 2

    canvas.paste(img_copy, (x, y))

    return canvas


# ============================================
# MAIN LOOP
# ============================================

for filepath in Path(INPUT_DIR).iterdir():

    if filepath.suffix.lower() not in SUPPORTED_EXTENSIONS:
        continue

    print(f"\nProcessing: {filepath.name}")

    img = Image.open(filepath)

    # Apply EXIF orientation automatically
    img = ImageOps.exif_transpose(img)

    img = Image.open(filepath)

    # Fix EXIF orientation
    img = ImageOps.exif_transpose(img)

    # Convert to RGB for JPEG export
    img = img.convert("RGB")

    w, h = img.size

    portrait = h > w

    # ========================================
    # PORTRAIT IMAGES
    # ========================================

    if portrait:

        # ----- MODE 1 -----
        result_1 = process_portrait_mode_1(img)

        output_1 = (
            Path(OUTPUT_DIR)
            / f"{filepath.stem}_portrait_full.jpg"
        )

        result_1.save(
            output_1,
            quality=JPEG_QUALITY,
            subsampling=0
        )

        print(f"Saved: {output_1.name}")

        # ----- MODE 2 -----
        result_2 = process_portrait_mode_2(img)

        output_2 = (
            Path(OUTPUT_DIR)
            / f"{filepath.stem}_portrait_crop.jpg"
        )

        result_2.save(
            output_2,
            quality=JPEG_QUALITY,
            subsampling=0
        )

        print(f"Saved: {output_2.name}")

    # ========================================
    # LANDSCAPE IMAGES
    # ========================================

    else:

        result = process_landscape(img)

        output_path = (
            Path(OUTPUT_DIR)
            / f"{filepath.stem}_landscape.jpg"
        )

        result.save(
            output_path,
            quality=JPEG_QUALITY,
            subsampling=0
        )

        print(f"Saved: {output_path.name}")

print("\nDone.")