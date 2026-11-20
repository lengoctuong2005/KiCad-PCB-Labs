import pcbnew as p
from pathlib import Path

path = Path(__file__).parent / 'AFE_ECG_PPG_PTT.kicad_pcb'
board = p.LoadBoard(str(path.parent / 'baseline' / path.name))
point = lambda x, y: p.VECTOR2I(p.FromMM(x), p.FromMM(y))
for ref, pos in {'J2': (63, 16), 'J3': (55, 16), 'H2': (54, 6), 'H4': (54, 65)}.items():
    board.FindFootprintByReference(ref).SetPosition(point(*pos))
for item in board.GetDrawings():
    if item.GetLayer() == p.Edge_Cuts:
        item.SetEnd(point(92, 70))
for zone in board.Zones():
    outline = zone.Outline().COutline(0)
    for i in range(outline.PointCount()):
        v = outline.CPoint(i)
        x, y = p.ToMM(v.x), p.ToMM(v.y)
        if zone.GetIsRuleArea():
            x -= 8
        elif x == 99:
            x = 91
        outline.SetPoint(i, point(x, y))
p.SaveBoard(str(path), board)
