import math
import sys
from pathlib import Path

import pcbnew

project = Path(__file__).resolve().parents[1]
board = pcbnew.LoadBoard(str(Path(sys.argv[1]) if len(sys.argv) > 1 else project / 'AFE_ECG_PPG_PTT.kicad_pcb'))
footprints = {fp.GetReference(): fp for fp in board.GetFootprints()}
expected = {('U1', '16'): (39.6, 34.32), ('C4', '2'): (40.85, 32), ('C11', '2'): (44.6, 32.175), ('C10', '2'): (14.7, 64)}
tracks = list(board.GetTracks())
for (ref, pin), (x, y) in expected.items():
    pads = [pad for pad in footprints[ref].Pads() if pad.GetNumber() == pin]
    assert len(pads) == 1 and pads[0].GetNetname() == 'GND'
    pad = pads[0]
    matches = [item for item in tracks if isinstance(item, pcbnew.PCB_VIA) and abs(pcbnew.ToMM(item.GetPosition().x) - x) < 0.00001 and abs(pcbnew.ToMM(item.GetPosition().y) - y) < 0.00001]
    assert len(matches) == 1, (ref, pin, 'via')
    via = matches[0]
    assert via.GetNetname() == 'GND'
    assert via.GetWidth(pcbnew.F_Cu) == pcbnew.FromMM(0.6) and via.GetDrillValue() == pcbnew.FromMM(0.3)
    assert via.IsTented(pcbnew.F_Cu) and via.IsTented(pcbnew.B_Cu)
    point = via.GetPosition()
    center = pad.GetPosition()
    assert math.hypot(point.x - center.x, point.y - center.y) <= pcbnew.FromMM(1.3)
    connected = False
    for item in tracks:
        if isinstance(item, pcbnew.PCB_VIA) or item.GetNetname() != 'GND' or item.GetLayer() != pcbnew.F_Cu:
            continue
        start, end = item.GetStart(), item.GetEnd()
        dx, dy = end.x - start.x, end.y - start.y
        length_squared = dx * dx + dy * dy
        if not length_squared:
            continue
        fraction = max(0, min(1, ((point.x - start.x) * dx + (point.y - start.y) * dy) / length_squared))
        connected |= math.hypot(point.x - start.x - fraction * dx, point.y - start.y - fraction * dy) <= item.GetWidth() / 2
    assert connected, (ref, pin, 'front return')
supply = [item for item in tracks if not isinstance(item, pcbnew.PCB_VIA) and item.GetNetname() == '+3V3' and {tuple(item.GetStart()), tuple(item.GetEnd())} == {(pcbnew.FromMM(63), pcbnew.FromMM(16)), (pcbnew.FromMM(58), pcbnew.FromMM(16))}]
assert len(supply) == 1 and supply[0].GetWidth() == pcbnew.FromMM(0.5)
print('PASS: four tented local GND returns and 0.5 mm J2-to-J3 supply; native DRC required for plane connectivity')
