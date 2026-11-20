import pcbnew as p
from pathlib import Path

root = Path(__file__).resolve().parent
board = p.LoadBoard(str(root / 'AFE_ECG_PPG_PTT.kicad_pcb'))
mm = p.FromMM
point = lambda x, y: p.VECTOR2I(mm(x), mm(y))
gnd = board.FindNet('GND')
for x, y in [(40.55, 32.0), (44.6, 32.175), (14.7, 64.0)]:
    via = p.PCB_VIA(board)
    via.SetPosition(point(x, y))
    via.SetWidth(mm(0.6))
    via.SetDrill(mm(0.3))
    via.SetViaType(p.VIATYPE_THROUGH)
    via.SetLayerPair(p.F_Cu, p.B_Cu)
    via.SetNet(gnd)
    board.Add(via)
track = p.PCB_TRACK(board)
track.SetStart(point(39.775, 32.0))
track.SetEnd(point(40.55, 32.0))
track.SetLayer(p.F_Cu)
track.SetWidth(mm(0.2))
track.SetNet(gnd)
board.Add(track)
for track in board.GetTracks():
    if track.GetClass() == 'PCB_TRACK' and track.GetNetname() == '+3V3' and { (track.GetStart().x, track.GetStart().y), (track.GetEnd().x, track.GetEnd().y) } == { (mm(63), mm(16)), (mm(58), mm(16)) }:
        track.SetWidth(mm(0.5))
p.SaveBoard(str(root / 'AFE_ECG_PPG_PTT.kicad_pcb'), board)
