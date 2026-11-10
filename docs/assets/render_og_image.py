"""Build docs/assets/og-image.png (1200×630) with title + TFT screen mock-up.

Uses screens.svg (same SoftAP QR + run-page layout as the overview).
Regenerate: python3 render_og_image.py
"""
from pathlib import Path

import cairosvg

ROOT = Path(__file__).resolve().parent
SCREENS = ROOT / "screens.svg"
OUT_SVG = ROOT / "og-image.svg"
OUT_PNG = ROOT / "og-image.png"

W, H = 1200, 630
BG = "#0f1a20"
INK = "#e8f1f4"
MUTED = "#93a7af"
ACCENT = "#64d2b4"

# screens.svg viewBox is 632×364 — keep on the right with clear gap from title
SW, SH = 632, 364
RIGHT_W = 560
SCALE = RIGHT_W / SW
SC_H = SH * SCALE
SC_X = W - RIGHT_W - 48
SC_Y = (H - SC_H) / 2


def main() -> None:
    screens = SCREENS.read_text(encoding="utf-8")
    # strip outer svg wrapper; keep inner markup
    start = screens.find(">") + 1
    end = screens.rfind("</svg>")
    inner = screens[start:end].strip()

    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img"
     aria-label="ESP32-S3 HA climate — SoftAP QR setup and run page on the TFT">
  <rect width="{W}" height="{H}" fill="{BG}"/>
  <circle cx="1080" cy="-40" r="220" fill="#64d2b4" fill-opacity="0.08"/>
  <circle cx="-60" cy="520" r="180" fill="#5ab4ff" fill-opacity="0.07"/>

  <g font-family="DejaVu Sans, sans-serif">
    <text x="56" y="188" font-size="40" font-weight="700" fill="{INK}">ESP32-S3</text>
    <text x="56" y="242" font-size="40" font-weight="700" fill="{INK}">HA climate</text>
    <text x="56" y="300" font-size="20" font-weight="400" fill="{MUTED}">SHT40 + ST7789 → Home Assistant</text>
    <text x="56" y="342" font-size="17" font-weight="400" fill="{ACCENT}">Scan QR · SoftAP setup · live TFT readings</text>
  </g>

  <g transform="translate({SC_X:.1f},{SC_Y:.1f}) scale({SCALE:.6f})">
    {inner}
  </g>
</svg>
'''
    OUT_SVG.write_text(svg, encoding="utf-8")
    cairosvg.svg2png(url=str(OUT_SVG), write_to=str(OUT_PNG), output_width=W, output_height=H)
    print(f"wrote {OUT_PNG} ({OUT_PNG.stat().st_size} bytes) and {OUT_SVG.name}")


if __name__ == "__main__":
    main()
