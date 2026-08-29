"""Generate a scannable QR SVG for the DENR Biodiversity FB page.
White modules on a transparent background, sized to sit on the dark navy footer.
Rounded dot modules + rounded finder eyes. Error correction H.
Run manually: py -3 tools/gen_qr.py  ->  assets/qr/denr-fb-qr.svg

NOTE: this is an INVERTED QR (light modules on dark). It reads on most modern
phone cameras but is less universally reliable than dark-on-light."""
import os
import segno

URL = "https://www.facebook.com/denr.biodiversity/"
OUT = "assets/qr/denr-fb-qr.svg"
FG = "#FFFFFF"      # module colour (white)
BG = "#12233F"      # footer navy, used to carve the finder-eye gaps

qr = segno.make(URL, error="h")
matrix = [[bool(c) for c in row] for row in qr.matrix]
n = len(matrix)
M = 10                      # units per module
B = 4                       # quiet-zone modules
size = (n + 2 * B) * M


def in_finder(r, c):
    return ((r < 7 and c < 7) or
            (r < 7 and c >= n - 7) or
            (r >= n - 7 and c < 7))


parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" '
    f'shape-rendering="geometricPrecision" role="img" '
    f'aria-label="QR code linking to the DENR Biodiversity Facebook page">',
    f'<g fill="{FG}">',
]

for r in range(n):
    for c in range(n):
        if not matrix[r][c] or in_finder(r, c):
            continue
        cx = (c + B) * M + M / 2
        cy = (r + B) * M + M / 2
        parts.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{M*0.42:.1f}"/>')

parts.append('</g>')


def finder(r0, c0):
    x = (c0 + B) * M
    y = (r0 + B) * M
    outer = 7 * M
    parts.append(f'<rect x="{x}" y="{y}" width="{outer}" height="{outer}" rx="{M*2.4}" fill="{FG}"/>')
    parts.append(f'<rect x="{x+M}" y="{y+M}" width="{5*M}" height="{5*M}" rx="{M*1.7}" fill="{BG}"/>')
    parts.append(f'<rect x="{x+2*M}" y="{y+2*M}" width="{3*M}" height="{3*M}" rx="{M*1.1}" fill="{FG}"/>')


finder(0, 0)
finder(0, n - 7)
finder(n - 7, 0)
parts.append('</svg>')

os.makedirs("assets/qr", exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    f.write("".join(parts))
print("wrote", OUT, "modules", n, "viewBox", size)
