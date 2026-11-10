"""Mock-up of the screen states drawn by firmware/climate.yaml (SVG).

Matches the two-tile run page: Wi-Fi status, side-by-side temp/humidity
icons, IP, and display-on cue. Setup page still shows the SoftAP QR.

Needs segno for the QR matrix:  pip install segno
Regenerate: python3 render_screens.py
"""
from pathlib import Path

import segno

SSID = "Climate Setup"
PASSWORD = "setup1234"
EXAMPLE_SSID = "IOT"
EXAMPLE_IP = "192.170.32.111"
INK = "#e8f1f4"
MUTED = "#93a7af"
BG = "#0f1a20"
BEZEL = "#2f3a40"
BEZEL_EDGE = "#4a5b64"
TEAL = "rgb(100,210,180)"
ORANGE = "rgb(255,170,60)"
BLUE = "rgb(90,180,255)"
GREY = "rgb(90,90,90)"
DIV = "rgb(50,58,64)"
FONT = "DejaVu Sans, sans-serif"

SCREEN = 240
BEZEL_PAD = 14
PANEL = SCREEN + 2 * BEZEL_PAD
GAP = 36
MARGIN = 30
TOP = 26
CAPTION_H = 70
W = 2 * MARGIN + 2 * PANEL + GAP
H = TOP + PANEL + CAPTION_H


def text(x, y, s, size, fill, weight="400", anchor="start"):
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{FONT}" '
            f'font-size="{size}" font-weight="{weight}" fill="{fill}">{s}</text>')


def qr_modules(ox, oy, scale):
    qr = segno.make(f"WIFI:S:{SSID};T:WPA;P:{PASSWORD};;", error="L", micro=False,
                    boost_error=False)
    cells = []
    for r, row in enumerate(qr.matrix):
        for c, dark in enumerate(row):
            if dark:
                cells.append(f"M{ox + c * scale} {oy + r * scale}h{scale}v{scale}h-{scale}z")
    return f'<path d="{"".join(cells)}" fill="#000"/>', len(qr.matrix)


def icon_wifi(x, y, fill=TEAL):
    return (
        f'<g fill="none" stroke="{fill}" stroke-width="3" stroke-linecap="round">'
        f'<path d="M{x+4} {y+18} a12 12 0 0 1 24 0"/>'
        f'<path d="M{x+9} {y+18} a7 7 0 0 1 14 0"/>'
        f'<circle cx="{x+16}" cy="{y+20}" r="2.5" fill="{fill}" stroke="none"/>'
        f'</g>'
    )


def icon_thermo(x, y, fill=ORANGE):
    return (
        f'<g fill="none" stroke="{fill}" stroke-width="3" stroke-linecap="round">'
        f'<rect x="{x+14}" y="{y+2}" width="10" height="18" rx="5"/>'
        f'<circle cx="{x+19}" cy="{y+28}" r="10" fill="{fill}" stroke="{fill}"/>'
        f'</g>'
    )


def icon_drop(x, y, fill=BLUE):
    return (
        f'<path d="M{x+19} {y+2} C{x+19} {y+2} {x+4} {y+20} {x+4} {y+26} '
        f'a15 15 0 0 0 30 0 C{x+34} {y+20} {x+19} {y+2} {x+19} {y+2}Z" fill="{fill}"/>'
    )


def icon_ip(x, y, fill=MUTED):
    return (
        f'<g fill="none" stroke="{fill}" stroke-width="2.5">'
        f'<rect x="{x+4}" y="{y+8}" width="24" height="14" rx="3"/>'
        f'<path d="M{x+10} {y+22} h12 M{x+16} {y+22} v4"/>'
        f'</g>'
    )


def icon_monitor(x, y, fill=TEAL):
    return (
        f'<g fill="none" stroke="{fill}" stroke-width="2.5">'
        f'<rect x="{x+2}" y="{y+4}" width="28" height="18" rx="3"/>'
        f'<path d="M{x+10} {y+26} h12 M{x+16} {y+22} v4"/>'
        f'</g>'
    )


def setup_screen(ox, oy):
    scale = 5
    _, n = qr_modules(0, 0, scale)
    size = n * scale
    qx = ox + 120 - size // 2
    qy = oy + 120 - size // 2
    path, _ = qr_modules(qx, qy, scale)
    return [
        text(ox + 120, oy + 22, "Scan to set up", 18, "#fff", anchor="middle"),
        f'<rect x="{qx - 6}" y="{qy - 6}" width="{size + 12}" height="{size + 12}" fill="#fff"/>',
        path,
        text(ox + 120, oy + 229, SSID, 18, "#fff", anchor="middle"),
    ]


def run_screen(ox, oy, temp, hum, t_fill, h_fill):
    return [
        icon_wifi(ox + 8, oy + 4),
        text(ox + 46, oy + 24, EXAMPLE_SSID, 18, "#fff"),
        text(ox + 228, oy + 22, "-26dBm", 14, MUTED, anchor="end"),
        f'<rect x="{ox+12}" y="{oy+42}" width="216" height="1" fill="{DIV}"/>',
        f'<rect x="{ox+120}" y="{oy+52}" width="1" height="118" fill="{DIV}"/>',
        icon_thermo(ox + 41, oy + 56),
        text(ox + 60, oy + 136, temp, 32, t_fill, "500", anchor="middle"),
        text(ox + 60, oy + 164, "°C", 14, MUTED, anchor="middle"),
        icon_drop(ox + 161, oy + 56),
        text(ox + 180, oy + 136, hum, 32, h_fill, "500", anchor="middle"),
        text(ox + 180, oy + 164, "%", 14, MUTED, anchor="middle"),
        f'<rect x="{ox+12}" y="{oy+180}" width="216" height="1" fill="{DIV}"/>',
        icon_ip(ox + 8, oy + 192),
        text(ox + 46, oy + 214, EXAMPLE_IP, 16, MUTED),
        icon_monitor(ox + 204, oy + 192),
    ]


screens = [
    ("Setup page", "No saved Wi-Fi — SoftAP QR", setup_screen),
    ("Run page", "Wi-Fi, temp | humidity tiles, IP, Display on",
     lambda ox, oy: run_screen(ox, oy, "23.4", "58", ORANGE, BLUE)),
]

parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" '
    f'height="{H}" role="img" aria-label="TFT screens: setup QR and two-tile run page '
    f'with Wi-Fi, temperature, humidity, IP, and Display switch cue">',
    f'<rect width="{W}" height="{H}" fill="{BG}"/>',
]
for i, (title, sub, draw) in enumerate(screens):
    x = MARGIN + i * (PANEL + GAP)
    ox, oy = x + BEZEL_PAD, TOP + BEZEL_PAD
    parts.append(f'<rect x="{x}" y="{TOP}" width="{PANEL}" height="{PANEL}" rx="16" fill="{BEZEL}" stroke="{BEZEL_EDGE}" stroke-width="1.5"/>')
    parts.append(f'<rect x="{ox}" y="{oy}" width="{SCREEN}" height="{SCREEN}" rx="3" fill="#000"/>')
    parts.append(f'<clipPath id="s{i}"><rect x="{ox}" y="{oy}" width="{SCREEN}" height="{SCREEN}"/></clipPath>')
    parts.append(f'<g clip-path="url(#s{i})">' + "".join(draw(ox, oy)) + "</g>")
    cx = x + PANEL / 2
    parts.append(text(cx, TOP + PANEL + 30, title, 17, INK, "700", anchor="middle"))
    parts.append(text(cx, TOP + PANEL + 52, sub, 13, MUTED, anchor="middle"))
parts.append("</svg>")

out = Path(__file__).with_name("screens.svg")
out.write_text("\n".join(parts) + "\n", encoding="utf-8")
print(f"wrote {out} ({W}x{H})")
