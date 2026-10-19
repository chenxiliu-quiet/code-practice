# -*- coding: utf-8 -*-
"""量一量渲染出来的页面上，图片块到底占多大（英寸）。"""
import sys
from PIL import Image

path = sys.argv[1]
dpi = float(sys.argv[2]) if len(sys.argv) > 2 else 100.0
img = Image.open(path).convert('L')
w, h = img.size
px = img.load()

row_ink = []
for y in range(h):
    ink = 0
    for x in range(0, w, 2):
        if px[x, y] < 200:
            ink += 1
    row_ink.append(ink)

bands = []
start = None
for y in range(h):
    on = row_ink[y] > 2
    if on and start is None:
        start = y
    if not on and start is not None:
        if y - start > 3:
            bands.append((start, y - 1))
        start = None
if start is not None:
    bands.append((start, h - 1))

print(f"{path}  {w}x{h}px  ({dpi:.0f}dpi)")
for (y0, y1) in bands:
    xs = [x for x in range(w) for yy in range(y0, y1 + 1, 2) if px[x, yy] < 200]
    x0, x1 = (min(xs), max(xs)) if xs else (0, 0)
    print(f"  band y {y0:4d}-{y1:4d} ({ (y1-y0+1)/dpi:5.2f}in tall)  x {x0:4d}-{x1:4d} ({(x1-x0+1)/dpi:5.2f}in wide)")
