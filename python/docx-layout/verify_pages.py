# -*- coding: utf-8 -*-
"""检查渲染出的每一页：内容卡片是否落在页边距内（有无被裁切）。"""
import os
import sys
from PIL import Image

d = sys.argv[1]
dpi = 100.0
LEFT, RIGHT = 1.25, 8.27 - 1.25      # 内容区左右（英寸）
TOP, BOTTOM = 1.00, 11.69 - 1.00     # 内容区上下

files = sorted(f for f in os.listdir(d) if f.startswith('page-') and f.endswith('.png'))
print(f'pages: {len(files)}')
for f in files:
    im = Image.open(os.path.join(d, f)).convert('L')
    w, h = im.size
    px = im.load()
    xs, ys = [], []
    for y in range(0, h, 2):
        for x in range(0, w, 2):
            if px[x, y] < 200:
                xs.append(x); ys.append(y)
    if not xs:
        print(f'  {f}: blank')
        continue
    x0, x1 = min(xs) / dpi, max(xs) / dpi
    y0, y1 = min(ys) / dpi, max(ys) / dpi
    over_x = 'CLIP-X' if x1 > RIGHT + 0.05 else 'ok'
    over_y = 'CLIP-Y' if y1 > BOTTOM + 0.05 else 'ok'
    print(f'  {f}: x {x0:5.2f}-{x1:5.2f}in  y {y0:5.2f}-{y1:5.2f}in  '
          f'(内容区 x {LEFT}-{RIGHT}, y {TOP}-{BOTTOM})  {over_x} {over_y}')
