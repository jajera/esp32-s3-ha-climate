"""Build the Open Graph (social preview) images, 1200x630 PNG.

  docs/assets/og-image.png     default card (overview and anything unmatched)
  docs/assets/og/<name>.png    one card per tutorial section

overrides/main.html picks the card from the page URL. Every card has big type
that survives being shrunk to a link-preview thumbnail, and a visual that
matches the section. The cards that quote the firmware are checked against
firmware/climate.yaml, and the script stops if a quoted line has drifted.

Needs cairosvg and Pillow:  pip install cairosvg pillow
Regenerate: python3 render_og_image.py
"""
import re
from pathlib import Path

import cairosvg
from PIL import ImageFont

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
FIRMWARE = REPO / "firmware" / "climate.yaml"
SCREENS = ROOT / "screens.svg"
SCHEMATIC = ROOT / "wiring-schematic.svg"
BRANDS = REPO / "overrides" / ".icons" / "brands"
OUT_DIR = ROOT / "og"

W, H = 1200, 630
BG = "#0f1a20"
INK = "#e8f1f4"
MUTED = "#93a7af"
ACCENT = "#64d2b4"
PANEL = "#0b1519"
PANEL_EDGE = "#2a434d"
FONT = "DejaVu Sans, sans-serif"
MONO = "DejaVu Sans Mono, monospace"

MARGIN = 64
LEFT_MAX_W = 500                      # widest the title may be
AREA_X, AREA_W = 628, W - MARGIN - 628  # where the visual lives
AREA_Y, AREA_H = 70, 440

_SITE = re.search(r'site_url\s*=\s*"https?://([^/"]+)', (REPO / "zensical.toml").read_text())
URL = _SITE.group(1) if _SITE else "esp32-s3-ha-climate.johna.kiwi"

_FW = FIRMWARE.read_text(encoding="utf-8")

# ---------------------------------------------------------------- text helpers

_FONT_FILES = {
    ("sans", False): "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ("sans", True): "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ("mono", False): "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
}


def text_width(s, size, bold=False, mono=False):
    path = _FONT_FILES.get(("mono", False) if mono else ("sans", bold))
    if path and Path(path).exists():
        return ImageFont.truetype(path, size).getlength(s)
    return len(s) * size * (0.6 if mono else 0.7 if bold else 0.6)


def fit(lines, max_w, start, floor, bold=False, mono=False):
    size = start
    while size > floor and max(text_width(l, size, bold, mono) for l in lines) > max_w:
        size -= 1
    return size


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def require_in_firmware(lines):
    """Stop if a line quoted on a card is no longer in the firmware."""
    for line in lines:
        if line.strip() and line.strip() != "…" and line not in _FW:
            raise SystemExit(f"firmware/climate.yaml no longer contains: {line!r}")


# ------------------------------------------------------------------ shared art

def background():
    return f'''<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#101d24"/><stop offset="1" stop-color="#0b1318"/>
  </linearGradient>
  <radialGradient id="glowA" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="#64d2b4" stop-opacity="0.22"/>
    <stop offset="1" stop-color="#64d2b4" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="glowB" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="#5ab4ff" stop-opacity="0.16"/>
    <stop offset="1" stop-color="#5ab4ff" stop-opacity="0"/>
  </radialGradient>
</defs>
<rect width="{W}" height="{H}" fill="url(#bg)"/>
<circle cx="1090" cy="30" r="470" fill="url(#glowA)"/>
<circle cx="60" cy="650" r="430" fill="url(#glowB)"/>'''


def brand_mark(name, x, y, size):
    """Inline a brand SVG from overrides/.icons/brands/ at the given size."""
    src = (BRANDS / f"{name}.svg").read_text(encoding="utf-8")
    head = re.match(r"\s*(?:<\?xml[^>]*>\s*)?<svg[^>]*>", src)
    body = src[head.end():].rsplit("</svg>", 1)[0]
    return (f'<svg x="{x}" y="{y}" width="{size}" height="{size}" '
            f'viewBox="0 0 240 240" fill="none">{body}</svg>')


def footer():
    y, size = 538, 38
    x = MARGIN
    parts = []
    for name, label in (("esphome", "ESPHome"), ("home-assistant", "Home Assistant")):
        parts.append(brand_mark(name, x, y, size))
        parts.append(f'<text x="{x + size + 12}" y="{y + 27}" font-family="{FONT}" '
                     f'font-size="22" fill="{MUTED}">{label}</text>')
        x += size + 12 + text_width(label, 22) + 30
    parts.append(f'<text x="{W - MARGIN}" y="{y + 27}" text-anchor="end" font-family="{FONT}" '
                 f'font-size="23" fill="{MUTED}">{URL}</text>')
    return "".join(parts)


def left_column(eyebrow, brand, title, sub):
    parts = []
    # Eyebrow pill, with the site name next to it on section cards.
    spacing = 2
    pw = text_width(eyebrow, 20, True) + spacing * len(eyebrow) + 36
    parts.append(f'<rect x="{MARGIN}" y="58" width="{pw:.0f}" height="42" rx="21" '
                 f'fill="{ACCENT}" fill-opacity="0.14" stroke="{ACCENT}" stroke-opacity="0.55"/>')
    parts.append(f'<text x="{MARGIN + 18}" y="86" font-family="{FONT}" font-size="20" '
                 f'font-weight="700" letter-spacing="{spacing}" fill="{ACCENT}">{eyebrow}</text>')
    if brand:
        parts.append(f'<text x="{MARGIN + pw + 18:.0f}" y="86" font-family="{FONT}" '
                     f'font-size="22" fill="{MUTED}">{brand}</text>')
    # Title.
    size = fit(title, LEFT_MAX_W, 88, 54, bold=True)
    line_h = round(size * 1.14)
    y = 190 + size * 0.2
    for line in title:
        parts.append(f'<text x="{MARGIN}" y="{y:.0f}" font-family="{FONT}" font-size="{size}" '
                     f'font-weight="700" fill="{INK}">{esc(line)}</text>')
        y += line_h
    # Subtitle.
    y += 12
    for line in sub:
        parts.append(f'<text x="{MARGIN}" y="{y:.0f}" font-family="{FONT}" font-size="30" '
                     f'fill="{MUTED}">{esc(line)}</text>')
        y += 42
    return "".join(parts)


# --------------------------------------------------------------------- visuals

def _centered(w, h, max_w=AREA_W, max_h=AREA_H):
    scale = min(max_w / w, max_h / h)
    sw, sh = w * scale, h * scale
    return AREA_X + (AREA_W - sw) / 2, AREA_Y + (AREA_H - sh) / 2, sw, sh


def v_screens(view):
    """Crop of screens.svg: 'both' panels or just the 'run' page."""
    s = SCREENS.read_text(encoding="utf-8")
    s = re.sub(r'<rect width="\d+" height="\d+" fill="#[0-9a-fA-F]+"/>', "", s, count=1)
    inner = s[s.index(">") + 1:s.rindex("</svg>")]
    vx, vy, vw, vh = {"both": (30, 26, 572, 268), "run": (334, 26, 268, 268)}[view]
    x, y, w, h = _centered(vw, vh)
    return (f'<svg x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
            f'viewBox="{vx} {vy} {vw} {vh}"><clipPath id="og-crop">'
            f'<rect x="{vx}" y="{vy}" width="{vw}" height="{vh}"/></clipPath>'
            f'<g clip-path="url(#og-crop)">{inner}</g></svg>')


def _check_pins():
    for _, n, _, pattern in PINS:
        if not re.search(pattern, _FW):
            raise SystemExit(f"firmware/climate.yaml no longer has GPIO{n} for this signal")


def _block(x, y, w, h, title, sub, accent):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="#16262e" '
            f'stroke="{accent}" stroke-width="3"/>'
            f'<path d="M{x} {y + 44} V{y + 14} a14 14 0 0 1 14 -14 H{x + w - 14} '
            f'a14 14 0 0 1 14 14 V{y + 44} Z" fill="{accent}"/>'
            f'<text x="{x + w / 2}" y="{y + 30}" text-anchor="middle" font-family="{FONT}" '
            f'font-size="23" font-weight="700" fill="#ffffff">{title}</text>'
            f'<text x="{x + w / 2}" y="{y + h - 18}" text-anchor="middle" font-family="{FONT}" '
            f'font-size="19" fill="{MUTED}">{sub}</text>')


def v_wiring():
    """Simplified wiring: ESP32-S3 to the SHT40 (I2C) and the display (SPI)."""
    _check_pins()
    by_label = {label: colour for label, _, colour, _ in PINS}
    red, grey = "#c0392b", "#9aa5ab"
    x0, x1 = AREA_X, AREA_X + AREA_W
    esp = (x0, 130, 150, 300)
    sht = (x1 - 170, 80, 170, 140)
    tft = (x1 - 170, 270, 170, 230)
    sht_wires = [red, grey, by_label["I2C SDA"], by_label["I2C SCL"]]
    tft_wires = [red, grey, by_label["SPI clock"], by_label["SPI MOSI"], by_label["Display RES"],
                 by_label["Display DC"], by_label["Display CS"], by_label["Backlight"]]
    n = len(sht_wires) + len(tft_wires)
    sx = esp[0] + esp[2]
    top, span = esp[1] + 64, esp[3] - 64 - 22
    out = []
    ends = ([(sht[0], sht[1] + 62 + i * 22) for i in range(len(sht_wires))]
            + [(tft[0], tft[1] + 62 + j * 22) for j in range(len(tft_wires))])
    for k, ((ex, ey), colour) in enumerate(zip(ends, sht_wires + tft_wires)):
        sy = top + k * span / (n - 1)
        mx = (sx + ex) / 2
        out.append(f'<path d="M{sx} {sy:.1f} C{mx} {sy:.1f} {mx} {ey} {ex} {ey}" fill="none" '
                   f'stroke="{colour}" stroke-width="3.5"/>'
                   f'<circle cx="{sx}" cy="{sy:.1f}" r="4.5" fill="{colour}"/>'
                   f'<circle cx="{ex}" cy="{ey}" r="4.5" fill="{colour}"/>')
    blocks = (_block(*esp, "ESP32-S3", "N16R8", "#4a6078")
              + _block(*sht, "SHT40", "I2C · 0x44", "#1f8a70")
              + _block(*tft, "ST7789", "SPI · 240×240", "#e67e22"))
    return "".join(out) + blocks


def v_schematic():
    s = SCHEMATIC.read_text(encoding="utf-8")
    s = re.sub(r'<rect width="\d+" height="\d+" fill="#[0-9a-fA-F]+"/>', "", s, count=1)
    inner = s[s.index(">") + 1:s.rindex("</svg>")]
    vx, vy, vw, vh = 50, 140, 1040, 560      # the two blocks and their wires only
    x, y, w, h = _centered(vw, vh)
    return (f'<svg x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
            f'viewBox="{vx} {vy} {vw} {vh}"><clipPath id="og-crop">'
            f'<rect x="{vx}" y="{vy}" width="{vw}" height="{vh}"/></clipPath>'
            f'<g clip-path="url(#og-crop)">{inner}</g></svg>')


def _window(h, title):
    """A rounded panel with a title bar; returns (svg, x, y, w) for content."""
    x, w = AREA_X, AREA_W
    y = AREA_Y + (AREA_H - h) / 2
    svg = (f'<rect x="{x}" y="{y:.0f}" width="{w}" height="{h}" rx="18" fill="{PANEL}" '
           f'stroke="{PANEL_EDGE}" stroke-width="2"/>'
           f'<circle cx="{x + 28}" cy="{y + 30:.0f}" r="7" fill="#ff5f56"/>'
           f'<circle cx="{x + 52}" cy="{y + 30:.0f}" r="7" fill="#ffbd2e"/>'
           f'<circle cx="{x + 76}" cy="{y + 30:.0f}" r="7" fill="#27c93f"/>'
           f'<text x="{x + w - 24}" y="{y + 37:.0f}" text-anchor="end" font-family="{MONO}" '
           f'font-size="18" fill="{MUTED}">{esc(title)}</text>'
           f'<rect x="{x}" y="{y + 58:.0f}" width="{w}" height="2" fill="{PANEL_EDGE}"/>')
    return svg, x, y


_KEY = "#7aa2f7"
_VAL = "#9ece6a"


def _yaml_line(line, size, x, y):
    m = re.match(r"^(\s*)(- )?([A-Za-z_][\w]*)(:)(.*)$", line)
    char = text_width("M", size, mono=True)
    if not m:
        fill = MUTED if line.strip() == "…" else INK
        return (f'<text x="{x}" y="{y}" xml:space="preserve" font-family="{MONO}" '
                f'font-size="{size}" fill="{fill}">{esc(line)}</text>')
    indent, dash, key, colon, rest = m.groups()
    parts = [f'<tspan fill="{INK}">{esc(indent)}{esc(dash or "")}</tspan>',
             f'<tspan fill="{_KEY}">{esc(key)}</tspan>',
             f'<tspan fill="{INK}">{colon}</tspan>',
             f'<tspan fill="{_VAL}">{esc(rest)}</tspan>']
    return (f'<text x="{x}" y="{y}" xml:space="preserve" font-family="{MONO}" '
            f'font-size="{size}">{"".join(parts)}</text>')


def v_yaml(lines, filename):
    require_in_firmware(lines)
    size = fit(lines, AREA_W - 56, 25, 17, mono=True)
    line_h = round(size * 1.5)
    h = 60 + 28 + line_h * len(lines) + 12
    svg, x, y = _window(h, filename)
    ty = y + 60 + 28 + size
    for line in lines:
        svg += _yaml_line(line, size, x + 28, f"{ty:.0f}")
        ty += line_h
    return svg


def v_terminal(lines, title="bash"):
    """lines: (kind, text) with kind in cmd / info / ok / plain."""
    texts = [t for _, t in lines]
    size = fit(texts, AREA_W - 56, 23, 16, mono=True)
    line_h = round(size * 1.85)
    h = 60 + 40 + line_h * len(lines) + 22
    svg, x, y = _window(h, title)
    ty = y + 60 + 40 + size
    for kind, t in lines:
        if kind == "cmd":
            body = f'<tspan fill="{ACCENT}">$</tspan><tspan fill="{INK}">{esc(t[1:])}</tspan>'
        elif kind == "ok":
            body = f'<tspan fill="{_VAL}" font-weight="700">{esc(t)}</tspan>'
        elif kind == "info":
            body = f'<tspan fill="{ACCENT}">INFO</tspan><tspan fill="{MUTED}">{esc(t[4:])}</tspan>'
        else:
            body = f'<tspan fill="{MUTED}">{esc(t)}</tspan>'
        svg += (f'<text x="{x + 28}" y="{ty:.0f}" xml:space="preserve" font-family="{MONO}" '
                f'font-size="{size}">{body}</text>')
        ty += line_h
    return svg


# Signal, GPIO, colour (same colours as the wiring schematic) and the firmware
# pattern that proves the pin number. The wiring card draws these.
PINS = [
    ("I2C SDA", 8, "#2e86de", r"sda:\s*GPIO8\b"),
    ("I2C SCL", 18, "#1f8a70", r"scl:\s*GPIO18\b"),
    ("SPI clock", 12, "#e67e22", r"clk_pin:\s*GPIO12\b"),
    ("SPI MOSI", 11, "#8e44ad", r"mosi_pin:\s*GPIO11\b"),
    ("Display CS", 10, "#16a085", r"cs_pin:\s*GPIO10\b"),
    ("Display DC", 9, "#d81b60", r"dc_pin:\s*GPIO9\b"),
    ("Display RES", 7, "#f1c40f", r"reset_pin:\s*GPIO7\b"),
    ("Backlight", 21, "#7f8c8d", r"pin:\s*GPIO21\b"),
]


# ----------------------------------------------------------------------- cards

WIFI_LINES = ["wifi:", "  ap:", "    ssid: ${ap_ssid}", "    password: ${ap_password}",
              "  …", "captive_portal:", "improv_ble:", "improv_serial:"]

CARDS = {
    "default": dict(
        out=ROOT / "og-image.png", eyebrow="TUTORIAL", brand=None,
        title=["ESP32-S3", "HA climate"],
        sub=["Temperature and humidity", "in Home Assistant, set up", "by scanning a QR code."],
        visual=lambda: v_screens("both"),
        alt="ESP32-S3 HA climate: the setup QR page and the readings page on the TFT"),
    "walkthrough": dict(
        out=OUT_DIR / "walkthrough.png", eyebrow="STEP 1 OF 5", brand="ESP32-S3 HA climate",
        title=["Walk through", "the code"],
        sub=["One ESPHome YAML file,", "explained block by block."],
        visual=lambda: v_yaml(WIFI_LINES, "climate.yaml"),
        alt="Walk through the code: the wifi setup block from climate.yaml"),
    "build": dict(
        out=OUT_DIR / "build.png", eyebrow="STEP 2 OF 5", brand="ESP32-S3 HA climate",
        title=["Build the", "image"],
        sub=["Install ESPHome and compile", "the firmware on Ubuntu."],
        visual=lambda: v_terminal([
            ("cmd", "$ esphome compile \\"),
            ("plain", "    firmware/climate.yaml"),
            ("info", "INFO Creating factory.bin..."),
            ("info", "INFO Created: …/firmware.factory.bin"),
            ("ok", "INFO Successfully compiled program."),
        ], "esphome")),
    "wire": dict(
        out=OUT_DIR / "wire.png", eyebrow="STEP 3 OF 5", brand="ESP32-S3 HA climate",
        title=["Wire and", "validate"],
        sub=["SHT40 and ST7789 on a", "breadboard, one checkpoint", "at a time."],
        visual=v_wiring,
        alt="Wire and validate: the ESP32-S3 wired to the SHT40 and the display"),
    "flash": dict(
        out=OUT_DIR / "flash.png", eyebrow="STEP 4 OF 5", brand="ESP32-S3 HA climate",
        title=["Flash the", "ESP32"],
        sub=["Upload over USB and", "watch it boot."],
        visual=lambda: v_terminal([
            ("cmd", "$ esphome upload \\"),
            ("plain", "    firmware/climate.yaml \\"),
            ("plain", "    --device /dev/ttyACM0"),
            ("ok", "INFO Successfully uploaded program."),
        ], "esphome")),
    "configure": dict(
        out=OUT_DIR / "configure.png", eyebrow="STEP 5 OF 5", brand="ESP32-S3 HA climate",
        title=["Configure", "and test"],
        sub=["Join Wi-Fi, add it to", "Home Assistant, test", "the factory reset."],
        visual=lambda: v_screens("run"),
        alt="Configure and test: the readings page on the TFT"),
}


def render(name, card):
    title = card["title"]
    label = card.get("alt") or f'{" ".join(title)}: ESP32-S3 HA climate tutorial'
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img"
     aria-label="{esc(label)}">
{background()}
{left_column(card["eyebrow"], card["brand"], title, card["sub"])}
{card["visual"]()}
{footer()}
</svg>
'''
    out = card["out"]
    out.parent.mkdir(parents=True, exist_ok=True)
    if name == "default":
        out.with_suffix(".svg").write_text(svg, encoding="utf-8")
    cairosvg.svg2png(bytestring=svg.encode("utf-8"), write_to=str(out),
                     output_width=W, output_height=H)
    print(f"wrote {out.relative_to(REPO)} ({out.stat().st_size // 1024} KB)")


def main():
    for name, card in CARDS.items():
        render(name, card)


if __name__ == "__main__":
    main()
