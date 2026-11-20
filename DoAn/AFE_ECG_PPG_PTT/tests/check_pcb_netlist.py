import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

import pcbnew

project = Path(__file__).resolve().parents[1]
board_path = Path(sys.argv[1]) if len(sys.argv) > 1 else project / "AFE_ECG_PPG_PTT.kicad_pcb"
with tempfile.TemporaryDirectory(prefix="afe-parity-") as directory:
    netlist = Path(directory) / "schematic.xml"
    subprocess.run(
        ["kicad-cli", "sch", "export", "netlist", "--format", "kicadxml", "-o", str(netlist), str(project / "AFE_ECG_PPG_PTT.kicad_sch")],
        check=True,
    )
    root = ET.parse(netlist).getroot()
components = {item.attrib["ref"]: item for item in root.findall("./components/comp")}
expected_nodes = {
    (node.attrib["ref"], node.attrib["pin"]): net.attrib["name"]
    for net in root.findall("./nets/net")
    for node in net.findall("node")
}
board = pcbnew.LoadBoard(str(board_path))
footprints = list(board.GetFootprints())
actual = {fp.GetReference(): fp for fp in footprints}
assert len(actual) == len(footprints), "Duplicate footprint references"
assert set(actual) == set(components), {"missing": sorted(set(components) - set(actual)), "extra": sorted(set(actual) - set(components))}
for ref, component in components.items():
    fp = actual[ref]
    assert fp.GetValue() == component.findtext("value"), (ref, "value", fp.GetValue())
    identity = fp.GetFPID()
    name = f"{identity.GetLibNickname()}:{identity.GetLibItemName()}"
    assert name == component.findtext("footprint"), (ref, "footprint", name)
    symbol_id = (component.findtext("tstamps") or "").strip()
    assert symbol_id, (ref, "missing schematic symbol identity")
    assert fp.GetPath().AsString().rstrip("/").endswith("/" + symbol_id), (ref, "symbol path", fp.GetPath().AsString())
    for pad in fp.Pads():
        key = (ref, pad.GetNumber())
        expected = expected_nodes.get(key, "")
        assert pad.GetNetname() == expected, (key, "pad net", pad.GetNetname(), expected)
for (ref, pin), expected in expected_nodes.items():
    pads = [p for p in actual[ref].Pads() if p.GetNumber() == pin]
    assert pads and all(p.GetNetname() == expected for p in pads), (ref, pin, expected)
assert board.GetCopperLayerCount() == 2
bounds = board.GetBoardEdgesBoundingBox()
assert pcbnew.ToMM(bounds.GetWidth()) <= 100.2
assert pcbnew.ToMM(bounds.GetHeight()) <= 100.2
print(f"PASS: {len(actual)} footprints, {len(expected_nodes)} schematic nodes, values, footprint IDs, symbol paths and two-layer outline")
