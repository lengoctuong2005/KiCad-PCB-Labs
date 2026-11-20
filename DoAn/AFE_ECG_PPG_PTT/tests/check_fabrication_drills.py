import math
import re
import sys
from pathlib import Path

import pcbnew

project = Path(__file__).resolve().parents[1]
folder = Path(sys.argv[1]) if len(sys.argv) > 1 else project / 'outputs/print_preflight_20261114/gerbers'
board = pcbnew.LoadBoard(str(project / 'AFE_ECG_PPG_PTT.kicad_pcb'))
expected = []
for item in board.GetTracks():
    if isinstance(item, pcbnew.PCB_VIA):
        pos = item.GetPosition()
        expected.append((True, pcbnew.ToMM(pos.x), -pcbnew.ToMM(pos.y), pcbnew.ToMM(item.GetDrillValue()), 0.0, 0.0))
for footprint in board.GetFootprints():
    for pad in footprint.Pads():
        size = pad.GetDrillSize()
        if not size.x or not size.y:
            continue
        pos = pad.GetPosition()
        dx, dy = pcbnew.ToMM(size.x), pcbnew.ToMM(size.y)
        width = min(dx, dy)
        length = abs(dx - dy)
        angle = math.radians(pad.GetOrientationDegrees() + (90 if dy > dx else 0))
        expected.append((pad.GetAttribute() != pcbnew.PAD_ATTRIB_NPTH, pcbnew.ToMM(pos.x), -pcbnew.ToMM(pos.y), width, abs(length * math.cos(angle)), abs(length * math.sin(angle))))
actual = []
for plated, name in ((True, 'PTH'), (False, 'NPTH')):
    text = (folder / f'AFE_ECG_PPG_PTT-{name}.drl').read_text()
    assert 'METRIC' in text and 'G90' in text, name
    tools = {}
    selected = None
    for line in text.splitlines():
        tool = re.fullmatch(r'T(\d+)C([\d.]+)', line)
        if tool:
            tools[int(tool[1])] = float(tool[2])
            continue
        selection = re.fullmatch(r'T(\d+)', line)
        if selection:
            selected = int(selection[1])
            continue
        coordinate = re.fullmatch(r'X(-?[\d.]+)Y(-?[\d.]+)(?:G85X(-?[\d.]+)Y(-?[\d.]+))?', line)
        if coordinate:
            assert selected in tools, line
            x, y = float(coordinate[1]), float(coordinate[2])
            end_x = float(coordinate[3]) if coordinate[3] is not None else x
            end_y = float(coordinate[4]) if coordinate[4] is not None else y
            actual.append((plated, (x + end_x) / 2, (y + end_y) / 2, tools[selected], abs(end_x - x), abs(end_y - y)))
        elif line.startswith(('X', 'Y', 'G85', 'M71', 'M72', 'INCH')):
            raise AssertionError(('unsupported Excellon command', line))
assert len(expected) == len(actual), (len(expected), len(actual))
remaining = list(actual)
for hole in expected:
    candidates = [i for i, other in enumerate(remaining) if hole[0] == other[0] and all(abs(a - b) <= 0.0011 for a, b in zip(hole[1:], other[1:]))]
    assert len(candidates) == 1, ('missing or ambiguous exported drill', hole)
    remaining.pop(candidates[0])
assert not remaining
print(f'PASS: {len(expected)} PCB holes and slots match Excellon position, diameter, slot direction and plating within 0.0011 mm')
