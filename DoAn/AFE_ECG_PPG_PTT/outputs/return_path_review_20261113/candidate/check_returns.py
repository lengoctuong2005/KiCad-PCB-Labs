import math
from pathlib import Path
import pcbnew as p

root = Path(__file__).resolve().parent
board = p.LoadBoard(str(root / 'AFE_ECG_PPG_PTT.kicad_pcb'))
baseline = p.LoadBoard(str(root.parent / 'baseline' / 'AFE_ECG_PPG_PTT.kicad_pcb'))
positions = [(40.55, 32.0), (44.6, 32.175), (14.7, 64.0)]
mm = p.ToMM
xy = lambda point: (round(mm(point.x), 4), round(mm(point.y), 4))
old_vias = [t for t in baseline.GetTracks() if isinstance(t, p.PCB_VIA)]
new_vias = [t for t in board.GetTracks() if isinstance(t, p.PCB_VIA)]
assert len(new_vias) == len(old_vias) + 3
connectivity = board.GetConnectivity()
for pos in positions:
    vias = [v for v in new_vias if xy(v.GetPosition()) == pos]
    assert len(vias) == 1
    via = vias[0]
    assert via.GetNetname() == 'GND' and abs(mm(via.GetWidth(p.F_Cu)) - 0.6) < 1e-5 and abs(mm(via.GetDrillValue()) - 0.3) < 1e-5
    assert connectivity.IsConnectedOnLayer(via, p.F_Cu) and connectivity.IsConnectedOnLayer(via, p.B_Cu)
    print('GND via', pos, 'connected on both layers')
for ref, num in [('U1', '16'), ('C11', '2'), ('C4', '2'), ('C10', '2')]:
    pad = next(d for f in board.GetFootprints() if f.GetReference() == ref for d in f.Pads() if d.GetNumber() == num)
    via = min((v for v in new_vias if v.GetNetname() == 'GND'), key=lambda v: math.dist(xy(v.GetPosition()), xy(pad.GetPosition())))
    print(ref + '.' + num, 'nearest GND via', xy(via.GetPosition()), 'center distance mm', round(math.dist(xy(via.GetPosition()), xy(pad.GetPosition())), 3))
for ref in (f.GetReference() for f in baseline.GetFootprints()):
    before = baseline.FindFootprintByReference(ref)
    after = board.FindFootprintByReference(ref)
    assert before.GetPosition() == after.GetPosition() and before.GetOrientationDegrees() == after.GetOrientationDegrees()
tracks = [t for t in board.GetTracks() if t.GetClass() == 'PCB_TRACK' and t.GetNetname() == '+3V3' and {xy(t.GetStart()), xy(t.GetEnd())} == {(63.0, 16.0), (58.0, 16.0)}]
assert len(tracks) == 1 and abs(mm(tracks[0].GetWidth()) - 0.5) < 1e-5
print('PASS: footprints unchanged; 3V3 segment 0.5 mm')
