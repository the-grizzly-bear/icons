"""Recenter + recolor persona icons to the white (c8) palette variant, using
the unified face01..face39 set (no old/new prefix)."""

from pathlib import Path
from PIL import Image, ImageChops

FACES_DIR = Path("/home/user/projects/icons/faces_full")
OUT_DIR = Path("/home/user/projects/bots-v1/icons")

MAPPING = {
    "analyst": "face10_c8",      # Athena
    "skeptic": "face06_c8",      # Marcus
    "philosopher": "face20_c8",  # Sophia
    "confused": "face05_c8",     # Helena
    "cynic": "face11_c8",        # Diogenes
    "maverick": "face24_c8",     # Heraclitus
    "scribe": "face02_c8",       # Lydia
    "synthesis": "face07_c8",    # Sage
}

THRESHOLD = 24


def recenter(img: Image.Image) -> Image.Image:
    rgb = img.convert("RGB")
    w, h = rgb.size
    bg = rgb.getpixel((0, 0))
    bg_layer = Image.new("RGB", (w, h), bg)
    diff = ImageChops.difference(rgb, bg_layer)
    r, g, b = diff.split()
    mx = ImageChops.lighter(ImageChops.lighter(r, g), b)
    mask = mx.point(lambda p: 255 if p > THRESHOLD else 0)
    bbox = mask.getbbox()
    if not bbox:
        return img

    content_cx = (bbox[0] + bbox[2]) / 2
    content_cy = (bbox[1] + bbox[3]) / 2
    canvas_cx, canvas_cy = w / 2, h / 2
    dx = round(canvas_cx - content_cx)
    dy = round(canvas_cy - content_cy)

    out = Image.new("RGBA", (w, h), bg + (255,))
    out.paste(img, (dx, dy))
    return out


def main():
    OUT_DIR.mkdir(exist_ok=True)
    for key, tile in MAPPING.items():
        src = FACES_DIR / f"{tile}.png"
        img = Image.open(src).convert("RGBA")
        centered = recenter(img)
        dest = OUT_DIR / f"{key}.png"
        centered.save(dest)
        print(f"{key}: {tile} -> {dest}")


if __name__ == "__main__":
    main()
