import pcbnew
import math

IN = "/home/tuong/HK3_Semester/KhoaHe_PCB/DoAn/AFE_ECG_PPG_PTT/outputs/print_preflight_20261114/candidate/AFE_ECG_PPG_PTT.kicad_pcb"
OUT = IN
board = pcbnew.LoadBoard(IN)

SILK = {pcbnew.F_SilkS, pcbnew.B_SilkS}
changes = {"gr_text": [], "ref_props": [], "fp_silk_strokes": [], "moved_refs": []}

# gr_text on silk
for d in board.GetDrawings():
    if isinstance(d, pcbnew.PCB_TEXT) and d.GetLayer() in SILK:
        before = (pcbnew.ToMM(d.GetTextSize().x), pcbnew.ToMM(d.GetTextSize().y), pcbnew.ToMM(d.GetTextThickness()))
        d.SetTextSize(pcbnew.VECTOR2I(pcbnew.FromMM(1.0), pcbnew.FromMM(1.0)))
        d.SetTextThickness(pcbnew.FromMM(0.15))
        # reposition bottom warning texts to stay in board if enlarged
        txt = d.GetText()
        pos = d.GetPosition()
        y = pcbnew.ToMM(pos.y)
        if "NO HUMAN CONNECTION" in txt:
            d.SetPosition(pcbnew.VECTOR2I(pos.x, pcbnew.FromMM(68.8)))
        elif "ECG + PPG PAT" in txt:
            d.SetPosition(pcbnew.VECTOR2I(pos.x, pcbnew.FromMM(66.8)))
        afterpos = d.GetPosition()
        changes["gr_text"].append((txt, before, (1.0,1.0,0.15), (pcbnew.ToMM(pos.x),y), (pcbnew.ToMM(afterpos.x), pcbnew.ToMM(afterpos.y)), "F.SilkS" if d.GetLayer()==pcbnew.F_SilkS else "B.SilkS"))

# reference properties on footprints
for fp in board.GetFootprints():
    ref = fp.GetReference()
    f = fp.Reference()
    layer = f.GetLayer()
    if layer in SILK and f.IsVisible():
        before = (pcbnew.ToMM(f.GetTextSize().x), pcbnew.ToMM(f.GetTextSize().y), pcbnew.ToMM(f.GetTextThickness()), pcbnew.ToMM(f.GetPosition().x), pcbnew.ToMM(f.GetPosition().y))
        f.SetTextSize(pcbnew.VECTOR2I(pcbnew.FromMM(1.0), pcbnew.FromMM(1.0)))
        f.SetTextThickness(pcbnew.FromMM(0.15))
        changes["ref_props"].append((ref, before))

# fp silk strokes width >=0.15
stroke_count = 0
for fp in board.GetFootprints():
    for gi in fp.GraphicalItems():
        if gi.GetLayer() in SILK:
            # lines, rects, circles, arcs, polys have stroke
            try:
                sw = gi.GetWidth()
            except Exception:
                continue
            swmm = pcbnew.ToMM(sw)
            if swmm < 0.15:
                gi.SetWidth(pcbnew.FromMM(0.15))
                stroke_count += 1
changes["fp_silk_strokes"].append(stroke_count)

board.Save(OUT)

import json
with open('/home/tuong/HK3_Semester/KhoaHe_PCB/DoAn/AFE_ECG_PPG_PTT/outputs/print_preflight_20261114/candidate/fix_legend_pass1.json','w') as f:
    json.dump(changes,f,indent=2)
print('saved', OUT)
print('gr_text', len(changes['gr_text']), 'refs', len(changes['ref_props']), 'strokes_changed', stroke_count)
