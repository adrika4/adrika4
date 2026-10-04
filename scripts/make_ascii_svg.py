import cv2
import numpy as np
from PIL import Image
from rembg import remove

RAMP = " .:-=+*#%@"
COLS, FS, LH = 130, 6, 7
CW = FS * 0.6

src = Image.open("source-photo.png").convert("RGB")
alpha = np.array(remove(src))[:, :, 3] / 255.0
alpha = cv2.GaussianBlur(alpha, (0, 0), 1.5)

g = cv2.cvtColor(np.array(src), cv2.COLOR_RGB2GRAY)
g = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(8, 8)).apply(g)
g = (255 * (g / 255.0) ** 0.5).astype(np.uint8)
blur = cv2.GaussianBlur(g, (0, 0), 3)
g = np.clip(cv2.addWeighted(g, 1.7, blur, -0.7, 0), 0, 255)

subject = 75 + g * (180 / 255.0)          # lift dark blazer/hair to mid-tone
img = (subject * alpha).astype(np.uint8)  # background -> 0 (blank)

h, w = img.shape
rows = int(h / w * COLS * CW / LH)
px = Image.fromarray(img).resize((COLS, rows), Image.LANCZOS).load()
W, H = COLS * CW, rows * LH

o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.1f} {H}" width="{W:.1f}" height="{H}">']
o.append(f'<rect width="{W:.1f}" height="{H}" rx="8" fill="#0d1117"/>')
o.append('<defs>')
for y in range(rows):
    d = y * 0.06
    o.append(f'<clipPath id="c{y}"><rect x="0" y="{y*LH}" width="0" height="{LH}">'
             f'<animate attributeName="width" from="0" to="{W:.1f}" begin="{d:.2f}s" dur="0.5s" fill="freeze"/>'
             f'</rect></clipPath>')
o.append('</defs>')
for y in range(rows):
    d = y * 0.06
    line = "".join(RAMP[int(px[x, y] / 255 * (len(RAMP) - 1))] for x in range(COLS))
    o.append(f'<text x="0" y="{(y+1)*LH-1.5}" font-family="Consolas,Menlo,monospace" font-size="{FS}" '
             f'fill="#c9d1d9" xml:space="preserve" textLength="{W:.1f}" lengthAdjust="spacing" '
             f'clip-path="url(#c{y})">{line}</text>')
    o.append(f'<rect y="{y*LH}" width="{CW:.1f}" height="{LH-1}" fill="#c9d1d9" opacity="0">'
             f'<set attributeName="opacity" to="1" begin="{d:.2f}s"/>'
             f'<animate attributeName="x" from="0" to="{W:.1f}" begin="{d:.2f}s" dur="0.5s" fill="freeze"/>'
             f'<set attributeName="opacity" to="0" begin="{d+0.5:.2f}s"/></rect>')
o.append('</svg>')
open("ascii.svg", "w", encoding="utf-8").write("\n".join(o))
print("done: ascii.svg")
