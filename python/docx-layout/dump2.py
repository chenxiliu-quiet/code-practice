import sys, os, json, zipfile
from docx import Document
from docx.shared import Emu
from docx.table import Table
from docx.text.paragraph import Paragraph

src = sys.argv[1]
out = sys.argv[2]
imgdir = sys.argv[3]
os.makedirs(imgdir, exist_ok=True)

doc = Document(src)
lines = []

for i, s in enumerate(doc.sections):
    lines.append(f"[section {i}] page={Emu(s.page_width).inches:.2f}x{Emu(s.page_height).inches:.2f}in "
                 f"margins L={Emu(s.left_margin).inches:.2f} R={Emu(s.right_margin).inches:.2f} "
                 f"T={Emu(s.top_margin).inches:.2f} B={Emu(s.bottom_margin).inches:.2f}")

# map rId -> media file name
part = doc.part
rid_map = {}
for rid, rel in part.rels.items():
    if "image" in rel.reltype:
        rid_map[rid] = os.path.basename(rel.target_ref)

body = doc.element.body
pi = 0
for child in body.iterchildren():
    tag = child.tag.split('}')[-1]
    if tag == 'p':
        p = Paragraph(child, doc)
        xml = child.xml
        imgs = []
        for rid, fname in rid_map.items():
            if f' r:embed="{rid}"' in xml or f'r:link="{rid}"' in xml:
                imgs.append(fname)
        # sizes of drawings in this paragraph
        sizes = []
        for ext in child.iter():
            if ext.tag.endswith('}extent'):
                cx = int(ext.get('cx')); cy = int(ext.get('cy'))
                sizes.append(f"{Emu(cx).inches:.2f}x{Emu(cy).inches:.2f}in")
        lines.append(f"P{pi:03d} text={p.text!r} style={p.style.name!r} align={p.alignment} "
                     f"imgs={imgs} sizes={sizes} pagebreak_before={p.paragraph_format.page_break_before}")
        pi += 1
    elif tag == 'tbl':
        t = Table(child, doc)
        lines.append(f"TABLE rows={len(t.rows)} cols={len(t.columns)}")

with open(out, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

# extract media
with zipfile.ZipFile(src) as z:
    names = [n for n in z.namelist() if n.startswith('word/media/') and not n.endswith('/')]
    manifest = []
    for n in names:
        data = z.read(n)
        target = os.path.join(imgdir, os.path.basename(n))
        with open(target, 'wb') as f:
            f.write(data)
        manifest.append(f"{os.path.basename(n)}  {len(data)} bytes")
print('\n'.join(sorted(manifest)))
