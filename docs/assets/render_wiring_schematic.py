"""Schematic wiring diagram (SVG) for the Wire / Validate pages.

ESP32-S3 N16R8 → SHT40 (I2C) + ST7789 (SPI). BL on GPIO21 matches climate.yaml.

Dark background so it reads well in both the light and dark docs themes.
Regenerate: python3 render_wiring_schematic.py
"""

INK = "#e8f1f4"
MUTED = "#93a7af"
BG = "#0f1a20"

RED = "#c0392b"      # 3V3
BLK = "#9aa5ab"      # GND (light grey so it shows on the dark background)
C_SCL_I = "#1f8a70"  # I2C SCL
C_SDA_I = "#2e86de"  # I2C SDA
C_SCK = "#e67e22"    # SPI SCK
C_MOSI = "#8e44ad"   # SPI MOSI
C_CS = "#16a085"     # SPI CS
C_DC = "#d81b60"     # SPI DC
C_RES = "#f1c40f"    # SPI RST
C_BL = "#7f8c8d"     # backlight PWM

FONT = "DejaVu Sans, sans-serif"

W, H = 1180, 760
S3_X, S3_W = 70, 250
MOD_X, MOD_W = 820, 250
ROW_H = 34
TOP = 150

s3_pins = ["3V3", "GND", "GPIO8", "GPIO18", "GPIO11", "GPIO12",
           "GPIO10", "GPIO9", "GPIO7", "GPIO21"]
sht_pins = ["VIN", "GND", "SCL", "SDA"]
# 240×240 module: VCC GND SCL/SCK SDA RST DC CS BL
tft_pins = ["VCC", "GND", "SCL", "SDA", "RST", "DC", "CS", "BL"]

nets = [
    ("3V3", "sht", "VIN", RED),
    ("GND", "sht", "GND", BLK),
    ("GPIO18", "sht", "SCL", C_SCL_I),
    ("GPIO8", "sht", "SDA", C_SDA_I),
    ("3V3", "tft", "VCC", RED),
    ("GND", "tft", "GND", BLK),
    ("GPIO12", "tft", "SCL", C_SCK),
    ("GPIO11", "tft", "SDA", C_MOSI),
    ("GPIO7", "tft", "RST", C_RES),
    ("GPIO9", "tft", "DC", C_DC),
    ("GPIO10", "tft", "CS", C_CS),
    ("GPIO21", "tft", "BL", C_BL),
]

legend = [
    (RED, "3V3"), (BLK, "GND"),
    (C_SCL_I, "I2C SCL"), (C_SDA_I, "I2C SDA"),
    (C_SCK, "SPI SCK"), (C_MOSI, "SPI MOSI"), (C_CS, "SPI CS"),
    (C_DC, "SPI DC"), (C_RES, "SPI RST"), (C_BL, "BL PWM"),
]


def block(x, y, w, pins, title, accent):
    h = ROW_H * len(pins) + 46
    out = [f'<rect x="{x+4}" y="{y+5}" width="{w}" height="{h}" rx="12" fill="#091217"/>',
           f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="#16262e" '
           f'stroke="{accent}" stroke-width="3"/>',
           f'<rect x="{x}" y="{y}" width="{w}" height="34" rx="12" fill="{accent}"/>',
           f'<rect x="{x}" y="{y+18}" width="{w}" height="16" fill="{accent}"/>',
           f'<text x="{x+w/2}" y="{y+24}" text-anchor="middle" font-family="{FONT}" '
           f'font-size="19" font-weight="700" fill="#ffffff">{title}</text>']
    pin_y = {}
    for i, p in enumerate(pins):
        py = y + 46 + i * ROW_H + ROW_H / 2
        pin_y[p] = py
    return "".join(out), pin_y, h


svg_parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" '
    f'height="{H}" role="img" aria-label="Schematic wiring: ESP32-S3 to SHT40 '
    f'(I2C) and ST7789 (SPI), with 3V3 and GND nets">',
    f'<rect width="{W}" height="{H}" fill="{BG}"/>',
    f'<text x="48" y="54" font-family="{FONT}" font-size="30" font-weight="700" '
    f'fill="{INK}">Wiring, pad to pad</text>',
    f'<text x="50" y="86" font-family="{FONT}" font-size="16" fill="{MUTED}">'
    f'One colour per net. Trace each wire end to end. '
    f'Do not join TFT SDA to SHT40 SDA.</text>',
]

lx, ly = 50, 108
for col, lab in legend:
    svg_parts.append(f'<rect x="{lx}" y="{ly}" width="26" height="6" rx="3" fill="{col}"/>')
    svg_parts.append(f'<text x="{lx+32}" y="{ly+8}" font-family="{FONT}" '
                     f'font-size="14" fill="{INK}">{lab}</text>')
    lx += 32 + len(lab) * 8 + 18

s3_svg, s3y, s3h = block(S3_X, TOP, S3_W, s3_pins, "ESP32-S3 (N16R8)", "#4a6078")
sht_svg, shty, shth = block(MOD_X, TOP, MOD_W, sht_pins, "SHT40", C_SCL_I)
tft_top = TOP + shth + 36
tft_svg, tfty, tfth = block(MOD_X, tft_top, MOD_W, tft_pins, "ST7789 240×240", C_SCK)

for src, dst, dpin, col in nets:
    sy = s3y[src]
    dy = shty[dpin] if dst == "sht" else tfty[dpin]
    sx = S3_X + S3_W
    dx = MOD_X
    midx = (sx + dx) / 2
    svg_parts.append(
        f'<path d="M {sx} {sy} C {midx} {sy}, {midx} {dy}, {dx} {dy}" '
        f'fill="none" stroke="{col}" stroke-width="3.5" opacity="0.9"/>')
    svg_parts.append(f'<circle cx="{sx}" cy="{sy}" r="5" fill="{col}"/>')
    svg_parts.append(f'<circle cx="{dx}" cy="{dy}" r="5" fill="{col}"/>')

svg_parts += [s3_svg, sht_svg, tft_svg]

for p, py in s3y.items():
    svg_parts.append(f'<text x="{S3_X+S3_W-14}" y="{py+5}" text-anchor="end" '
                     f'font-family="{FONT}" font-size="16" fill="{INK}">{p}</text>')
for p, py in shty.items():
    svg_parts.append(f'<text x="{MOD_X+14}" y="{py+5}" font-family="{FONT}" '
                     f'font-size="16" fill="{INK}">{p}</text>')
for p, py in tfty.items():
    svg_parts.append(f'<text x="{MOD_X+14}" y="{py+5}" font-family="{FONT}" '
                     f'font-size="16" fill="{INK}">{p}</text>')

svg_parts.append(f'<text x="50" y="{H-24}" font-family="{FONT}" font-size="15" '
                 f'fill="{MUTED}">ST7789 240\u00d7240 \u00b7 '
                 f'TFT supply VCC \u00b7 clock SCL or SCK \u00b7 '
                 f'SHT40 power VIN / VCC / VN \u00b7 '
                 f'S3 underside silk is mirrored vs top.</text>')
svg_parts.append("</svg>")

with open("wiring-schematic.svg", "w") as f:
    f.write("\n".join(svg_parts))
print("ok -> wiring-schematic.svg")
