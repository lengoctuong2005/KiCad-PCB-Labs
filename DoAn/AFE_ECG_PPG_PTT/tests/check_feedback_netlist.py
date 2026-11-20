import subprocess
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

project = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix="afe-feedback-") as directory:
    netlist = Path(directory) / "schematic.xml"
    subprocess.run(
        ["kicad-cli", "sch", "export", "netlist", "--format", "kicadxml", "-o", str(netlist), str(project / "AFE_ECG_PPG_PTT.kicad_sch")],
        check=True,
    )
    root = ET.parse(netlist).getroot()
    nets = {
        net.attrib["name"]: {(node.attrib["ref"], node.attrib["pin"]) for node in net.findall("node")}
        for net in root.findall("./nets/net")
    }
    values = {component.attrib["ref"]: component.findtext("value") for component in root.findall("./components/comp")}
    assert nets["OPAMP_N"] == {("U1", "9"), ("R13", "2"), ("R14", "1")}, nets["OPAMP_N"]
    assert {("U1", "8"), ("R13", "1")} <= nets["REFOUT"]
    assert {("U1", "10"), ("R14", "2")} <= nets["AD_OUT"]
    assert not nets["REFOUT"] & nets["OPAMP_N"]
    assert values["R13"] == "100k" and values["R14"] == "1M"
print("PASS: actual schematic netlist has negative feedback, gain-setting resistors and isolated REFOUT")
