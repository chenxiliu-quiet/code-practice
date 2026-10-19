# -*- coding: utf-8 -*-
"""在源图和渲染页里都找到 image2.png 那个"粗黑边框 console 框"，用它的宽度反推图片实际显示宽度。"""
from PIL import Image
import sys


def find_box(path, thresh=120, min_run=40):
    im = Image.open(path).convert('L')
    px = im.load()
    w, h = im.size
    rows = []
    for y in range(h):
        run = 0
        best = 0
        for x in range(w):
            if px[x, y] < thresh:
                run += 1
                best = max(best, run)
            else:
                run = 0
        if best > min_run:
            rows.append((y, best))
    if not rows:
        return None
    return rows


src = 'media/image2.png'
im = Image.open(src).convert('L')
px = im.load()
w, h = im.size
# 边框行：整行大量黑像素
rows = [y for y in range(h) if sum(1 for x in range(w) if px[x, y] < 120) > w * 0.3]
cols = [x for x in range(w) if sum(1 for y in range(h) if px[x, y] < 120) > h * 0.15]
print(f'source {src}: {w}x{h}px  box rows {rows[0]}-{rows[-1]}  cols {cols[0]}-{cols[-1]}'
      f'  -> box {cols[-1]-cols[0]+1}x{rows[-1]-rows[0]+1}px')

for page in sys.argv[1:]:
    im2 = Image.open(page).convert('L')
    px2 = im2.load()
    w2, h2 = im2.size
    r2 = [y for y in range(h2) if sum(1 for x in range(w2) if px2[x, y] < 120) > 200]
    c2 = [x for x in range(w2) if sum(1 for y in range(h2) if px2[x, y] < 120) > 40]
    if not r2 or not c2:
        print(f'{page}: box not found')
        continue
    bw, bh = c2[-1] - c2[0] + 1, r2[-1] - r2[0] + 1
    scale = bw / (cols[-1] - cols[0] + 1)
    print(f'{page}: box {bw}x{bh}px  x {c2[0]}-{c2[-1]}  y {r2[0]}-{r2[-1]}'
          f'  -> 图片显示宽度 ≈ {w*scale/100:.2f}in, 高度 ≈ {h*scale/100:.2f}in')
