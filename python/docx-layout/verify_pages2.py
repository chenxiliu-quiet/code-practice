# -*- coding: utf-8 -*-
"""检查渲染页：只用深色像素（真内容）判断是否越界/被裁切。"""
import os
import sys
from PIL import Image

d = sys.argv[1]
thresh = int(sys.argv[2]) if len(sys.argv) > 2 else 150
dpi = 100.0
LEFT, RIGHT = 1.25, 8.27 - 1.25
TOP, BOTTOM = 1.00, 11.69 - 1.00

files = sorted(f for f in os.listdir(d) if f.startswith('page-') and f.endswith('.png'))
print(f'pages: {len(files)}   (thresh<{thresh})')
for f in files:
    im = Image.open(os.path.join(d, f)).convert('L')
    w, h = im.size
    px = im.load()
    xs, ys, n = [], [], 0
    for y in range(h):
        for x in range(w):
            if px[x, y] < thresh:
                xs.append(x); ys.append(y); n += 1
    if not xs:
        print(f'  {f}: blank')
        continue
    x0, x1 = min(xs) / dpi, max(xs) / dpi
    y0, y1 = min(ys) / dpi, max(ys) / dpi
    flag = []
    if x1 > RIGHT + 0.05: flag.append('CLIP-X')
    if y1 > BOTTOM + 0.05: flag.append('CLIP-Y')
    if x0 < LEFT - 0.05: flag.append('LEFT')
    print(f'  {f}: x {x0:5.2f}-{x1:5.2f}  y {y0:5.2f}-{y1:5.2f}  dark={n:6d}  '
          f'{" ".join(flag) if flag else "OK"}')
