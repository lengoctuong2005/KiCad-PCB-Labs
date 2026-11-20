import subprocess
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

project = Path(__file__).resolve().parents[1]
schematic = project / "AFE_ECG_PPG_PTT.kicad_sch"
with tempfile.TemporaryDirectory(prefix="afe-analog-") as directory:
    netlist = Path(directory) / "schematic.xml"
    subprocess.run(
        ["kicad-cli", "sch", "export", "netlist", "--format", "kicadxml", "-o", str(netlist), str(schematic)],
        check=True,
    )
    root = ET.parse(netlist).getroot()

nets = {
    net.attrib["name"]: {(node.attrib["ref"], node.attrib["pin"]) for node in net.findall("node")}
    for net in root.findall("./nets/net")
}
components = {component.attrib["ref"]: component for component in root.findall("./components/comp")}
values = {
    "R1": "360k", "R2": "360k", "R3": "360k", "R4": "10M", "R5": "10M",
    "R6": "10M", "R8": "10M", "R11": "1M", "R12": "1M", "R13": "100k",
    "R14": "1M", "R18": "1.4M", "R19": "10k", "C1": "0.33u", "C2": "0.33u",
    "C3": "1n", "C5": "1.5n", "C6": "10n", "U3": "MCP1700-2802E",
}
for ref, value in values.items():
    assert components[ref].findtext("value") == value, (ref, components[ref].findtext("value"))
for ref in ("R18", "R19"):
    assert components[ref].findtext("footprint") == "Resistor_SMD:R_0603_1608Metric", ref

expected = {
    "HPDRIVE": {("U1", "1"), ("C1", "1")},
    "HPSENSE": {("U1", "20"), ("C1", "2"), ("R6", "1")},
    "HP_MID": {("R6", "2"), ("R8", "1"), ("R18", "1")},
    "SW_NODE": {("U1", "6"), ("C2", "1"), ("R18", "2")},
    "IAOUT": {("U1", "19"), ("R8", "2"), ("R11", "1")},
    "OPAMP_N": {("U1", "9"), ("R13", "2"), ("R14", "1")},
    "RA_IN": {("J1", "T"), ("R1", "1"), ("R4", "2")},
    "LA_IN": {("J1", "R"), ("R2", "1"), ("R5", "2")},
    "RA_P": {("R1", "2"), ("U1", "2")},
    "LA_P": {("R2", "2"), ("U1", "3")},
    "RL_E": {("J1", "S"), ("R3", "1")},
    "RLDFB": {("U1", "4"), ("C3", "1")},
    "RLD_E": {("U1", "5"), ("R3", "2"), ("C3", "2")},
    "SK_N1": {("R11", "2"), ("R12", "1"), ("C5", "1")},
    "OPAMP_P": {("U1", "7"), ("R12", "2"), ("C6", "1")},
}
for name, pins in expected.items():
    assert nets[name] == pins, (name, nets[name], pins)
for name, pins in {
    "REFOUT": {("U1", "8"), ("C2", "2"), ("C6", "2"), ("R13", "1")},
    "AD_OUT": {("U1", "10"), ("C5", "2"), ("R14", "2")},
    "+VS_A": {("U1", "13"), ("U1", "15"), ("U1", "17"), ("R4", "1"), ("R5", "1"), ("U3", "2")},
    "GND": {("U1", "14"), ("U1", "16"), ("U1", "21")},
    "+3V3": {("R19", "1"), ("U2", "8"), ("U3", "3")},
    "ALERT": {("R19", "2"), ("U2", "2"), ("J2", "11")},
}.items():
    assert pins <= nets[name], (name, nets[name], pins)

j2_9 = [name for name, pins in nets.items() if ("J2", "9") in pins]
assert len(j2_9) == 1 and nets[j2_9[0]] == {("J2", "9")}, j2_9
assert j2_9[0].startswith("unconnected-"), j2_9
assert "FR_PIN" not in nets
assert '(no_connect (at 233.67999999999998 68.58)' in schematic.read_text()
alert_pin = root.find("./libparts/libpart[@lib='afe'][@part='ADS1115']/pins/pin[@num='2']")
assert alert_pin is not None and alert_pin.attrib["type"] == "open_collector", alert_pin.attrib if alert_pin is not None else None
print("PASS: analog component values, connectivity, ALERT pull-up, and J2.9 no-connect")
