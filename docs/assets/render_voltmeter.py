"""Optional voltmeter graphic (SVG) for the SHT40 power step.

An analog meter reading about 3.3 V, plus chips that say where the probes go
and what to set the dial to. The background is transparent and the chips carry
their own fill, so it reads on both the light and dark docs themes.

Regenerate: python3 render_voltmeter.py   (writes voltmeter-3v3.svg next to this file)
"""
import math
from pathlib import Path

FONT = "DejaVu Sans, sans-serif"
INK = "#1c1e20"
MUTED = "#5f6568"
BEZEL = "#2b2d2f"
BEZEL_EDGE = "#9aa5ab"
FACE = "#f4f1e8"
CHIP_EDGE = "#c5c5bf"
RED = "#c0392b"
GREEN = "#1f8a70"

W, H = 560, 260
CX, CY, R = 175, 190, 128        # needle pivot and scale radius
V_MAX = 5.0
START, SWEEP = 150, 120          # scale runs from 150 to 30 degrees
READING = 3.3


def ang(v):
    return math.radians(START - SWEEP * v / V_MAX)


def pt(v, r):
    a = ang(v)
    return CX + r * math.cos(a), CY - r * math.sin(a)


def line(p, q, width, colour=INK, cap="butt"):
    return (f'<line x1="{p[0]:.1f}" y1="{p[1]:.1f}" x2="{q[0]:.1f}" y2="{q[1]:.1f}" '
            f'stroke="{colour}" stroke-width="{width}" stroke-linecap="{cap}"/>')


def text(x, y, s, size, fill=INK, weight="400", anchor="middle"):
    return (f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" font-family="{FONT}" '
            f'font-size="{size}" font-weight="{weight}" fill="{fill}">{s}</text>')


parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
    f'role="img" aria-label="Analog voltmeter reading about 3.3 volts. Red probe to VIN, '
    f'black probe to GND, dial on DC volts.">',
    # Body and face.
    f'<rect x="15" y="15" width="320" height="238" rx="18" fill="{BEZEL}"/>',
    f'<rect x="29" y="29" width="292" height="176" rx="8" fill="{FACE}"/>',
]

# Scale arc.
x0, y0 = pt(0, R)
x1, y1 = pt(V_MAX, R)
parts.append(f'<path d="M {x0:.1f} {y0:.1f} A {R} {R} 0 0 1 {x1:.1f} {y1:.1f}" fill="none" '
             f'stroke="{INK}" stroke-width="2.5"/>')

# Ticks every 0.5 V, longer and numbered every 1 V.
for i in range(0, 11):
    v = i / 2
    major = i % 2 == 0
    parts.append(line(pt(v, R), pt(v, R - (13 if major else 7)), 2.2 if major else 1.3))
    if major:
        lx, ly = pt(v, R - 28)
        parts.append(text(lx, ly + 5, f"{int(v)}", 15, INK, "600"))

# Marker for the expected reading, just outside the arc.
parts.append(line(pt(READING, R - 14), pt(READING, R + 9), 4, GREEN, "round"))
lx, ly = pt(READING, R + 21)
parts.append(text(lx, ly + 4, "3.3", 12, GREEN, "700"))

# Unit label, clear of the needle.
parts.append(text(CX - 52, CY - 10, "V DC", 13, MUTED, "600"))

# Needle with a short tail, then the hub.
tip = pt(READING, R - 10)
tail = (CX - (tip[0] - CX) * 0.1, CY + (CY - tip[1]) * 0.1)
parts.append(line(tail, tip, 3, RED, "round"))
parts.append(f'<circle cx="{CX}" cy="{CY}" r="8" fill="{INK}"/>')
parts.append(f'<circle cx="{CX}" cy="{CY}" r="3" fill="{RED}"/>')

# Jacks on the bezel: red positive, black negative.
for jx, ring, label in ((110, RED, "+"), (240, "#111111", "\u2212")):
    parts.append(f'<circle cx="{jx}" cy="227" r="10" fill="{ring}" stroke="{BEZEL_EDGE}" stroke-width="2"/>')
    parts.append(f'<circle cx="{jx}" cy="227" r="4" fill="{BEZEL}"/>')
    parts.append(text(jx, 247, label, 14, "#ffffff", "700"))

# Chips: what to connect and what to expect.
chips = [
    ("dot", RED, "Red probe", "to VIN (the supply pin)"),
    ("dot", "#111111", "Black probe", "to GND, or the \u2212 rail"),
    ("dial", None, "Dial", "DC volts"),
    ("dot", GREEN, "Expect", "about 3.3 V"),
]
cx0, cw, ch, gap = 360, 190, 52, 10
for n, (kind, colour, title, sub) in enumerate(chips):
    cy0 = 11 + n * (ch + gap)
    parts.append(f'<rect x="{cx0}" y="{cy0}" width="{cw}" height="{ch}" rx="10" fill="{FACE}" '
                 f'stroke="{CHIP_EDGE}" stroke-width="1.5"/>')
    mx, my = cx0 + 24, cy0 + ch / 2
    if kind == "dot":
        edge = BEZEL_EDGE if colour == "#111111" else colour
        parts.append(f'<circle cx="{mx}" cy="{my}" r="9" fill="{colour}" stroke="{edge}" stroke-width="2"/>')
    else:
        # Small dial: a ring with a pointer at "DC volts".
        parts.append(f'<circle cx="{mx}" cy="{my}" r="10" fill="{BEZEL}" stroke="{BEZEL_EDGE}" stroke-width="2"/>')
        parts.append(line((mx, my), (mx + 6, my - 6), 2.5, "#ffffff", "round"))
    parts.append(text(cx0 + 44, cy0 + 22, title, 14, INK, "700", "start"))
    parts.append(text(cx0 + 44, cy0 + 41, sub, 12, MUTED, "400", "start"))

parts.append("</svg>")
out = Path(__file__).with_name("voltmeter-3v3.svg")
out.write_text("\n".join(parts) + "\n", encoding="utf-8")
print(f"wrote {out} ({W}x{H})")
