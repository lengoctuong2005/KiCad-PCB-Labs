import sys
from pathlib import Path

import pcbnew

project = Path(__file__).resolve().parents[1]
board = pcbnew.LoadBoard(str(Path(sys.argv[1]) if len(sys.argv) > 1 else project / 'AFE_ECG_PPG_PTT.kicad_pcb'))
footprints = {fp.GetReference(): fp for fp in board.GetFootprints()}
edges = [item for item in board.GetDrawings() if item.GetLayer() == pcbnew.Edge_Cuts]
assert len(edges) == 1 and edges[0].GetShape() == pcbnew.SHAPE_T_RECT
assert edges[0].GetStart() == pcbnew.VECTOR2I(0, 0)
assert edges[0].GetEnd() == pcbnew.VECTOR2I(pcbnew.FromMM(92), pcbnew.FromMM(70))
bounds = board.GetBoardEdgesBoundingBox()
for ref, expected in {'J1': (14, 5.55), 'H1': (5, 5), 'H2': (54, 6), 'H3': (5, 65), 'H4': (54, 65), 'J2': (63, 16), 'J3': (58, 16)}.items():
    pos = footprints[ref].GetPosition()
    assert abs(pcbnew.ToMM(pos.x) - expected[0]) < 0.001, (ref, 'x')
    assert abs(pcbnew.ToMM(pos.y) - expected[1]) < 0.001, (ref, 'y')
assert abs(footprints['J1'].GetOrientationDegrees()) < 0.001
jack_label = footprints['J1'].Reference()
assert jack_label.IsVisible() and jack_label.GetLayer() == pcbnew.F_SilkS
jack_bounds = jack_label.GetBoundingBox()
assert bounds.Contains(jack_bounds.GetPosition()) and bounds.Contains(jack_bounds.GetEnd())
keepouts = [zone for zone in board.Zones() if zone.GetZoneName() == 'ANTENNA_KEEPOUT']
assert len(keepouts) == 2
assert {zone.GetLayer() for zone in keepouts} == {pcbnew.F_Cu, pcbnew.B_Cu}
for zone in keepouts:
    assert zone.GetIsRuleArea()
    assert all([zone.GetDoNotAllowTracks(), zone.GetDoNotAllowVias(), zone.GetDoNotAllowPads(), zone.GetDoNotAllowZoneFills(), zone.GetDoNotAllowFootprints()])
    polygon = zone.Outline()
    assert polygon.OutlineCount() == 1 and polygon.HoleCount(0) == 0
    outline = polygon.COutline(0)
    points = [(round(pcbnew.ToMM(outline.CPoint(i).x), 3), round(pcbnew.ToMM(outline.CPoint(i).y), 3)) for i in range(outline.PointCount())]
    expected = [(60, 0), (92, 0), (92, 12), (60, 12)]
    assert any(points == order[i:] + order[:i] for order in [expected, expected[::-1]] for i in range(4)), points
labels = [item for item in board.GetDrawings() if isinstance(item, pcbnew.PCB_TEXT) and item.GetText() == 'NO HUMAN CONNECTION / SAFETY NOT VALIDATED']
assert len(labels) == 1 and labels[0].GetLayer() == pcbnew.F_SilkS
label_bounds = labels[0].GetBoundingBox()
assert bounds.Contains(label_bounds.GetPosition()) and bounds.Contains(label_bounds.GetEnd())
print('PASS: 92 x 70 mm, edge-jack placement, mounting holes, both antenna keepouts and safety label')
