#!/usr/bin/env python3
"""Generate PWA icons matching the Soundquest aesthetic."""
from PIL import Image, ImageDraw, ImageFilter
import math, pathlib

OUT = pathlib.Path(__file__).parent

def make(size, maskable=False):
    pad = int(size * 0.1) if maskable else 0
    inner = size - pad * 2
    canvas = Image.new("RGBA", (size, size), (7, 4, 16, 255))
    img = Image.new("RGBA", (inner, inner), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # Background gradient
    for y in range(inner):
        t = y / inner
        # Interpolate purple → pink → deep blue
        r = int(124 + (236 - 124) * t * 0.6)
        g = int(58 + (72 - 58) * t * 0.4)
        b = int(237 - (237 - 100) * t * 0.7)
        d.line([(0, y), (inner, y)], fill=(r, g, b, 255))
    # Glow blob
    blob = Image.new("RGBA", (inner, inner), (0, 0, 0, 0))
    bd = ImageDraw.Draw(blob)
    bd.ellipse(
        [int(inner * 0.55), int(inner * 0.05), int(inner * 1.15), int(inner * 0.65)],
        fill=(244, 114, 182, 220),
    )
    blob = blob.filter(ImageFilter.GaussianBlur(int(inner * 0.18)))
    img = Image.alpha_composite(img, blob)
    # Sound-wave glyph: stacked rounded bars centered
    bars = [0.55, 0.85, 0.65, 1.0, 0.7, 0.4]
    bar_w = inner * 0.07
    gap = inner * 0.045
    total_w = len(bars) * bar_w + (len(bars) - 1) * gap
    x0 = (inner - total_w) / 2
    cy = inner * 0.55
    for i, h in enumerate(bars):
        bh = inner * 0.42 * h
        x = x0 + i * (bar_w + gap)
        y_top = cy - bh / 2
        y_bot = cy + bh / 2
        d2 = ImageDraw.Draw(img)
        d2.rounded_rectangle(
            [x, y_top, x + bar_w, y_bot],
            radius=bar_w / 2,
            fill=(255, 255, 255, 240),
        )
    # Round corners (only for non-maskable)
    if not maskable:
        radius = int(inner * 0.22)
        mask = Image.new("L", (inner, inner), 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, inner, inner], radius=radius, fill=255)
        rounded = Image.new("RGBA", (inner, inner), (0, 0, 0, 0))
        rounded.paste(img, (0, 0), mask)
        img = rounded
    canvas.paste(img, (pad, pad), img)
    return canvas

for s in (192, 512):
    make(s).save(OUT / f"icon-{s}.png")
make(512, maskable=True).save(OUT / "icon-maskable-512.png")
print("icons written")
