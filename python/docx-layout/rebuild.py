# -*- coding: utf-8 -*-
"""重建作业文档：一页一题。
1) 从源 docx 按顺序读出所有段落文字与图片原始尺寸；
2) 计算每题 3 张图的显示尺寸（单图上限 + 整页高度预算）；
3) 重写 PNG 的 DPI 元数据，使「图片自然尺寸」= 目标尺寸（不损失像素，
   且无论渲染器用 wp:extent 还是图片 DPI，结果一致）；
4) python-docx 重新生成：A4、同页边距、每道题从新页开始、题号黄色高亮。
"""
import os
import re
import sys
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_COLOR_INDEX
from docx.oxml.ns import qn
from PIL import Image

SRC, MEDIA, OUTDIR, DST = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
SCALE = float(sys.argv[5]) if len(sys.argv) > 5 else 1.0
POST = float(sys.argv[6]) if len(sys.argv) > 6 else 1.0   # QA 用：整体缩放最终图片尺寸

IMAGE_BUDGET_IN = 8.30 * SCALE
CAPS = [2.40 * SCALE, 5.60 * SCALE, 2.40 * SCALE]   # 题目说明 / 代码 / 运行结果
EMU_PER_IN = 914400
WP_EXTENT = qn('wp:extent')
TITLE_RE = re.compile(r'^题目\s*\d+\s*[:：]$')

# ---------- 1) 按顺序读出文字与图片 ----------
src = Document(SRC)
entries = []          # ('text', s) | ('img', cx, cy)
for p in src.paragraphs:
    t = p.text.strip()
    if t:
        entries.append(('text', t))
    for el in p._p.iter():
        if el.tag == WP_EXTENT:
            entries.append(('img', int(el.get('cx')), int(el.get('cy'))))

media_files = sorted(
    [f for f in os.listdir(MEDIA) if re.fullmatch(r'image\d+\.png', f)],
    key=lambda s: int(re.findall(r'\d+', s)[0])
)
n_img = sum(1 for e in entries if e[0] == 'img')
assert n_img == len(media_files), f'图片数不匹配 {n_img} vs {len(media_files)}'
img_iter = iter(media_files)

# ---------- 2) 计算每组图片的目标尺寸 ----------
def plan_sizes(items):
    hs = [cy / EMU_PER_IN for _, cy, _ in items]
    caps = CAPS[:len(hs)]
    capped = [min(h, c) for h, c in zip(hs, caps)]
    total = sum(capped)
    extra = IMAGE_BUDGET_IN / total if total > IMAGE_BUDGET_IN else 1.0
    out = []
    for (cx, cy, f), h, c in zip(items, hs, capped):
        h_in = (c / h) * extra * h
        w_in = h_in * (cx / cy)
        out.append((w_in, h_in, f))
    return out

planned = []
cur = []
for item in entries:
    if item[0] == 'img':
        cur.append((item[1], item[2], next(img_iter)))
    elif TITLE_RE.match(item[1]) and cur:
        planned.append(plan_sizes(cur))
        cur = []
if cur:
    planned.append(plan_sizes(cur))

# ---------- 3) 准备图片 ----------
# 显示尺寸完全由 docx 里的 wp:extent 决定（Word 按它渲染），
# 所以这里保留截图的原始像素，只做复制，保证清晰度不损失。
import shutil
os.makedirs(OUTDIR, exist_ok=True)


def prepare(infile, w_in, h_in, idx):
    dst = os.path.join(OUTDIR, f'p{idx:02d}_{infile}')
    shutil.copyfile(os.path.join(MEDIA, infile), dst)
    return dst


# ---------- 4) 生成新文档 ----------
out = Document()
st = out.styles['Normal']
st.font.name = 'Times New Roman'
try:
    st.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
except Exception:
    pass
st.font.size = Pt(11)

sec = out.sections[0]
sec.page_width, sec.page_height = Inches(8.27), Inches(11.69)
sec.left_margin = sec.right_margin = Inches(1.25)
sec.top_margin = sec.bottom_margin = Inches(1.0)

head = out.add_paragraph()
head.alignment = WD_ALIGN_PARAGRAPH.CENTER
hr = head.add_run('example-id  Student　　第7周周三晚自习任务')
hr.bold = True
hr.font.size = Pt(14)
head.paragraph_format.space_after = Pt(10)

plan_q = list(planned)
cur_plan = None
idx = 0
for item in entries:
    if item[0] == 'text':
        text = item[1]
        p = out.add_paragraph()
        run = p.add_run(text)
        pf = p.paragraph_format
        pf.space_before, pf.space_after, pf.line_spacing = Pt(2), Pt(3), 1.0
        if TITLE_RE.match(text):
            pf.page_break_before = True
            run.bold, run.font.size = True, Pt(13)
            run.font.highlight_color = WD_COLOR_INDEX.YELLOW
        elif '程序代码' in text or '运行结果' in text:
            run.bold, run.font.size = True, Pt(11)
            run.font.highlight_color = WD_COLOR_INDEX.YELLOW
    else:
        cx, cy = item[1], item[2]
        if not cur_plan:
            cur_plan = list(plan_q.pop(0))
        w_in, h_in, fname = cur_plan.pop(0)
        w_in, h_in = w_in * POST, h_in * POST
        path = prepare(fname, w_in, h_in, idx)
        idx += 1
        p = out.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.0
        p.add_run().add_picture(path, width=Inches(w_in), height=Inches(h_in))

out.save(DST)

for i, plan in enumerate(planned):
    print(f"组{i}: " + " + ".join(f"{w:.2f}x{h:.2f}" for w, h, _ in plan) +
          f"  高合计 {sum(h for _, h, _ in plan):.2f}in")
print('saved:', os.path.basename(DST), os.path.getsize(DST), 'bytes')
