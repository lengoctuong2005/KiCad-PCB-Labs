import json
from PIL import Image, ImageDraw

# Precise pixel bounding boxes calibrated from KiCad courtyard + text union + pad verification
# Board: 50x50mm mapped to 1927px (32->1959) => scale 38.54 px/mm
# Computed via .check/parse_pcb.py courtyard + reference text expansion

groups = {
    'nguon': {'color': '#00B0F0', 'bbox': (51, 80, 917, 360)},       # USB1 + SW2 + C1/C6/C7
    'ldo': {'color': '#FF0000', 'bbox': (937, 80, 1514, 360)},       # U1 + C2 + C3
    'ap_am': {'color': '#7030A0', 'bbox': (1534, 80, 1938, 380)},    # U2 + C4
    'uart': {'color': '#00B050', 'bbox': (148, 534, 840, 1072)},     # U3 + C6..C9
    'ne555': {'color': '#ED7D31', 'bbox': (975, 534, 1900, 1072)},   # U5 + R7,R8,C10,C11
    'led': {'color': '#FFC000', 'bbox': (166, 1168, 1475, 1554)},    # D1..D6 + R1..R6
    # Header courtyards + pads + text union
    'j1': {'color': '#00FFFF', 'bbox': (150, 1533, 299, 1921)},       # J1
    'j3': {'color': '#00FFFF', 'bbox': (536, 1360, 684, 1943)},       # J3
    'j4': {'color': '#00FFFF', 'bbox': (844, 1610, 993, 1900)},       # J4
    'j5': {'color': '#00FFFF', 'bbox': (1036, 1492, 1278, 1958)},     # J5
    'j6': {'color': '#00FFFF', 'bbox': (1363, 1492, 1606, 1958)},     # J6
    'header2': {'color': '#00FFFF', 'bbox': (1485, 415, 1945, 630)},  # J7 6 pads + silkscreen + text
    'header3': {'color': '#00FFFF', 'bbox': (1485, 1110, 1945, 1330)}, # J8 6 pads + silkscreen + text
}

def draw_boxes(draw, group_names, line_width=6):
    for gn in group_names:
        if gn not in groups:
            continue
        g = groups[gn]
        bbox = g['bbox']
        if bbox:
            draw.rectangle(bbox, outline=g['color'], width=line_width)

def make_img(in_path, out_path, draw_groups):
    im = Image.open(in_path).convert('RGB')
    draw = ImageDraw.Draw(im)
    draw_boxes(draw, draw_groups)
    im.save(out_path)
    print(f"Saved {out_path} with {draw_groups}")

all_headers = ['j1', 'j3', 'j4', 'j5', 'j6', 'header2', 'header3']

make_img('Pic/lab5_pcb_top_raw.png', 'Pic/cau1.png', list(groups.keys()))
make_img('Pic/lab5_pcb_top_raw.png', 'Pic/cau2.png', ['ldo', 'ap_am', 'ne555'])
make_img('Pic/lab5_pcb_top_raw.png', 'Pic/cau3.png', ['nguon', 'uart'])
make_img('Pic/lab5_pcb_top_raw.png', 'Pic/cau4.png', all_headers + ['led', 'nguon'])
make_img('Pic/lab5_pcb_top_raw.png', 'Pic/cau4_connectors_perimeter.png', all_headers + ['nguon'])
make_img('Pic/lab5_pcb_top_raw.png', 'Pic/q5.png', ['nguon', 'ldo', 'ap_am', 'ne555', 'uart', 'led'] + all_headers)
make_img('Pic/lab5_pcb_top_raw.png', 'Pic/pcb_functional_blocks_annotated.png', ['nguon', 'ldo', 'ap_am', 'ne555', 'uart', 'led'] + all_headers)

# Also generate dedicated verification crops
im_raw = Image.open('Pic/lab5_pcb_top_raw.png').convert('RGB')
for name in ['header2', 'header3', 'j1', 'j3', 'j4', 'j5', 'j6']:
    bbox = groups[name]['bbox']
    pad = 20
    crop = im_raw.crop((max(0,bbox[0]-pad), max(0,bbox[1]-pad), min(1992,bbox[2]+pad), min(1992,bbox[3]+pad)))
    draw = ImageDraw.Draw(crop)
    draw.rectangle((pad, pad, pad + bbox[2]-bbox[0], pad + bbox[3]-bbox[1]), outline='#00FFFF', width=4)
    crop.save(f'/tmp/verify_{name}.png')
    print(f"verify {name} -> {bbox}")

# Also verify pads inside bbox
scale = (1959-32)/50.0
def mm_to_px(x_mm, y_mm):
    return (32 + (x_mm-25)*scale, 32 + (y_mm-90)*scale)
# J7 pads check
import math
def check_pads(fx,fy,rot, pads_local, bbox):
    rad=math.radians(rot)
    for lx,ly in pads_local:
        gx=fx+lx*math.cos(rad)-ly*math.sin(rad)
        gy=fy+lx*math.sin(rad)+ly*math.cos(rad)
        px,py=mm_to_px(gx,gy)
        inside = bbox[0] <= px <= bbox[2] and bbox[1] <= py <= bbox[3]
        print(f"pad {lx},{ly} -> {px:.1f},{py:.1f} inside={inside}")

pads = [(-1.58,3.58),(-1.58,6.12),(-1.58,8.66),(0.96,3.58),(0.96,6.12),(0.96,8.66)]
print("J7 pads inside header2:", groups['header2']['bbox'])
check_pads(64.4,102.5,90,pads, groups['header2']['bbox'])
print("J8 pads inside header3:", groups['header3']['bbox'])
check_pads(64.4,120.5,90,pads, groups['header3']['bbox'])
