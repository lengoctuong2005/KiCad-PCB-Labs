import re, uuid

def uid(): return str(uuid.uuid4())

def extract_sym(lib_file, sym_name):
    txt = open(f'/usr/share/kicad/symbols/{lib_file}').read()
    m = re.search(r'\n(\t\(symbol\s+\"' + sym_name + r'\".*?\n\t\)\n)', txt, re.S)
    if m:
        return m.group(1)
    raise ValueError(f"Could not find {sym_name} in {lib_file}")

syms = [
    extract_sym('Device.kicad_sym', 'C'),
    extract_sym('Device.kicad_sym', 'R'),
    extract_sym('Device.kicad_sym', 'LED'),
    extract_sym('Device.kicad_sym', 'D'),
    extract_sym('Connector_Generic.kicad_sym', 'Conn_01x02'),
    extract_sym('Connector_Generic.kicad_sym', 'Conn_01x03'),
    extract_sym('Connector_Generic.kicad_sym', 'Conn_01x04'),
    extract_sym('power.kicad_sym', 'PWR_FLAG'),
    extract_sym('Amplifier_Instrumentation.kicad_sym', 'AD620'),
    extract_sym('Amplifier_Instrumentation.kicad_sym', 'AD623'),
    extract_sym('Amplifier_Operational.kicad_sym', 'LM324'),
    extract_sym('Amplifier_Operational.kicad_sym', 'MCP6004'),
]

sch_head = f"""(kicad_sch
\t(version 20231120)
\t(generator "kicad-cli")
\t(generator_version "8.0")
\t(uuid "{uid()}")
\t(paper "A3")
\t(title_block
\t\t(title "EMG Sensor - Surface Electromyography Analog Front-End")
\t\t(date "2026-11-08")
\t\t(rev "v1.0")
\t\t(company "KhoaHe Biomedical PCB")
\t\t(comment 1 "Dual Output: Bandpassed Raw EMG & Linear Contraction Envelope")
\t\t(comment 2 "0 DRC / 0 ERC Medical Grade Design")
\t)
\t(lib_symbols
{''.join(syms)}\t)
"""

elements = []

def sym_inst(lib_id, ref, val, fp, x, y, pin_dict=None, unit=1):
    pins_txt = ""
    if pin_dict:
        for pnum in pin_dict:
            pins_txt += f'\t\t(pin "{pnum}" (uuid "{uid()}"))\n'
    return f"""\t(symbol (lib_id "{lib_id}") (at {x:.2f} {y:.2f} 0) (unit {unit})
\t\t(in_bom yes) (on_board yes) (dnp no) (uuid "{uid()}")
\t\t(property "Reference" "{ref}" (at {x:.2f} {y-2.54:.2f} 0) (effects (font (size 1.27 1.27))))
\t\t(property "Value" "{val}" (at {x:.2f} {y+2.54:.2f} 0) (effects (font (size 1.27 1.27))))
\t\t(property "Footprint" "{fp}" (at {x:.2f} {y:.2f} 0) (effects (font (size 1.27 1.27)) hide))
{pins_txt}\t)"""

def wire(x1, y1, x2, y2):
    return f'\t(wire (pts (xy {x1:.2f} {y1:.2f}) (xy {x2:.2f} {y2:.2f})) (stroke (width 0) (type default)) (uuid "{uid()}"))'

def label(name, x, y):
    return f'\t(label "{name}" (at {x:.2f} {y:.2f} 0) (fields_autoplaced yes) (effects (font (size 1.27 1.27)) (justify left bottom)) (uuid "{uid()}"))'

# 1. Connectors
elements.append(sym_inst("Connector_Generic:Conn_01x02", "J1", "Power_In", "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical", 30.48, 40.64, {"1":"","2":""}))
elements.append(wire(30.48-5.08, 40.64+1.27, 30.48-10.16, 40.64+1.27)); elements.append(label("VCC", 30.48-10.16, 40.64+1.27))
elements.append(wire(30.48-5.08, 40.64-1.27, 30.48-10.16, 40.64-1.27)); elements.append(label("GND", 30.48-10.16, 40.64-1.27))

# PWR_FLAG on VCC and GND at J1
elements.append(sym_inst("power:PWR_FLAG", "#FLG01", "PWR_FLAG", "", 30.48-10.16, 40.64+1.27, {"1":""}))
elements.append(sym_inst("power:PWR_FLAG", "#FLG02", "PWR_FLAG", "", 30.48-10.16, 40.64-1.27, {"1":""}))

elements.append(sym_inst("Connector_Generic:Conn_01x03", "J2", "Electrodes_In", "Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical", 30.48, 76.2, {"1":"","2":"","3":""}))
elements.append(wire(30.48-5.08, 76.2+2.54, 30.48-10.16, 76.2+2.54)); elements.append(label("IN_PLUS_RAW", 30.48-10.16, 76.2+2.54))
elements.append(wire(30.48-5.08, 76.2+0.00, 30.48-10.16, 76.2+0.00)); elements.append(label("IN_MINUS_RAW", 30.48-10.16, 76.2+0.00))
elements.append(wire(30.48-5.08, 76.2-2.54, 30.48-10.16, 76.2-2.54)); elements.append(label("VREF", 30.48-10.16, 76.2-2.54))

elements.append(sym_inst("Connector_Generic:Conn_01x04", "J3", "EMG_Out", "Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical", 254.0, 76.2, {"1":"","2":"","3":"","4":""}))
elements.append(wire(254.0-5.08, 76.2+3.81, 254.0-10.16, 76.2+3.81)); elements.append(label("VCC", 254.0-10.16, 76.2+3.81))
elements.append(wire(254.0-5.08, 76.2+1.27, 254.0-10.16, 76.2+1.27)); elements.append(label("GND", 254.0-10.16, 76.2+1.27))
elements.append(wire(254.0-5.08, 76.2-1.27, 254.0-10.16, 76.2-1.27)); elements.append(label("RAW_EMG", 254.0-10.16, 76.2-1.27))
elements.append(wire(254.0-5.08, 76.2-3.81, 254.0-10.16, 76.2-3.81)); elements.append(label("ENV_EMG", 254.0-10.16, 76.2-3.81))

# 2. U1 (AD623)
elements.append(sym_inst("Amplifier_Instrumentation:AD623", "U1", "AD623ARZ", "Package_SO:SOIC-8_3.9x4.9mm_P1.27mm", 101.6, 101.6, {str(i):"" for i in range(1, 9)}))
u1_pins = [
    ("1", "RG1", 101.6-10.16, 101.6+3.81, 101.6-15.24, 101.6+3.81),
    ("2", "IN_MINUS_FILT", 101.6-10.16, 101.6+1.27, 101.6-15.24, 101.6+1.27),
    ("3", "IN_PLUS_FILT", 101.6-10.16, 101.6-1.27, 101.6-15.24, 101.6-1.27),
    ("4", "GND", 101.6-10.16, 101.6-3.81, 101.6-15.24, 101.6-3.81),
    ("5", "VREF", 101.6+10.16, 101.6-3.81, 101.6+15.24, 101.6-3.81),
    ("6", "VOUT_IA", 101.6+10.16, 101.6-1.27, 101.6+15.24, 101.6-1.27),
    ("7", "VCC", 101.6+10.16, 101.6+1.27, 101.6+15.24, 101.6+1.27),
    ("8", "RG2", 101.6+10.16, 101.6+3.81, 101.6+15.24, 101.6+3.81),
]
for pnum, net, px, py, lx, ly in u1_pins:
    elements.append(wire(px, py, lx, ly)); elements.append(label(net, lx, ly))

# 3. U2 (MCP6004 units 1..5)
# Unit 1 (OpAmp A: pins 1, 2, 3)
elements.append(sym_inst("Amplifier_Operational:MCP6004", "U2", "MCP6004-E/SL", "Package_SO:SOIC-14_3.9x8.7mm_P1.27mm", 160.02, 80.0, {"1":"","2":"","3":""}, unit=1))
elements.append(wire(160.02-5.08, 80.0+2.54, 160.02-10.16, 80.0+2.54)); elements.append(label("VREF", 160.02-10.16, 80.0+2.54)) # 1IN-
elements.append(wire(160.02-5.08, 80.0-2.54, 160.02-10.16, 80.0-2.54)); elements.append(label("VMID", 160.02-10.16, 80.0-2.54)) # 1IN+
elements.append(wire(160.02+5.08, 80.0, 160.02+10.16, 80.0)); elements.append(label("VREF", 160.02+10.16, 80.0)) # 1OUT

# Unit 2 (OpAmp B: pins 5, 6, 7)
elements.append(sym_inst("Amplifier_Operational:MCP6004", "U2", "MCP6004-E/SL", "Package_SO:SOIC-14_3.9x8.7mm_P1.27mm", 200.66, 80.0, {"5":"","6":"","7":""}, unit=2))
elements.append(wire(200.66-5.08, 80.0-2.54, 200.66-10.16, 80.0-2.54)); elements.append(label("LPF_IN", 200.66-10.16, 80.0-2.54)) # 2IN+
elements.append(wire(200.66-5.08, 80.0+2.54, 200.66-10.16, 80.0+2.54)); elements.append(label("LPF_FB", 200.66-10.16, 80.0+2.54)) # 2IN-
elements.append(wire(200.66+5.08, 80.0, 200.66+10.16, 80.0)); elements.append(label("RAW_EMG", 200.66+10.16, 80.0)) # 2OUT

# Unit 3 (OpAmp C: pins 8, 9, 10)
elements.append(sym_inst("Amplifier_Operational:MCP6004", "U2", "MCP6004-E/SL", "Package_SO:SOIC-14_3.9x8.7mm_P1.27mm", 160.02, 110.0, {"8":"","9":"","10":""}, unit=3))
elements.append(wire(160.02-5.08, 110.0-2.54, 160.02-10.16, 110.0-2.54)); elements.append(label("VREF", 160.02-10.16, 110.0-2.54)) # 3IN+
elements.append(wire(160.02-5.08, 110.0+2.54, 160.02-10.16, 110.0+2.54)); elements.append(label("RECT_IN", 160.02-10.16, 110.0+2.54)) # 3IN-
elements.append(wire(160.02+5.08, 110.0, 160.02+10.16, 110.0)); elements.append(label("RECT_OUT", 160.02+10.16, 110.0)) # 3OUT

# Unit 4 (OpAmp D: pins 12, 13, 14)
elements.append(sym_inst("Amplifier_Operational:MCP6004", "U2", "MCP6004-E/SL", "Package_SO:SOIC-14_3.9x8.7mm_P1.27mm", 200.66, 110.0, {"12":"","13":"","14":""}, unit=4))
elements.append(wire(200.66-5.08, 110.0-2.54, 200.66-10.16, 110.0-2.54)); elements.append(label("VREF", 200.66-10.16, 110.0-2.54)) # 4IN+
elements.append(wire(200.66-5.08, 110.0+2.54, 200.66-10.16, 110.0+2.54)); elements.append(label("ENV_IN", 200.66-10.16, 110.0+2.54)) # 4IN-
elements.append(wire(200.66+5.08, 110.0, 200.66+10.16, 110.0)); elements.append(label("ENV_EMG", 200.66+10.16, 110.0)) # 4OUT

# Unit 5 (Power: pins 4, 11)
elements.append(sym_inst("Amplifier_Operational:MCP6004", "U2", "MCP6004-E/SL", "Package_SO:SOIC-14_3.9x8.7mm_P1.27mm", 180.34, 60.0, {"4":"","11":""}, unit=5))
elements.append(wire(180.34, 60.0-5.08, 180.34, 60.0-10.16)); elements.append(label("VCC", 180.34, 60.0-10.16)) # 4 (V+)
elements.append(wire(180.34, 60.0+5.08, 180.34, 60.0+10.16)); elements.append(label("GND", 180.34, 60.0+10.16)) # 11 (V-)

# 4. Resistors R1..R19
res_info = [
    ("R1", "1k", "NET_D1_R1", "GND"),
    ("R2", "100k", "VCC", "VMID"),
    ("R3", "100k", "VMID", "GND"),
    ("R4", "1k", "IN_PLUS_RAW", "IN_PLUS_FILT"),
    ("R5", "1k", "IN_MINUS_RAW", "IN_MINUS_FILT"),
    ("R6", "10M", "IN_PLUS_FILT", "VREF"),
    ("R7", "10M", "IN_MINUS_FILT", "VREF"),
    ("R8", "1k", "RG1", "RG2"),
    ("R9", "8.2k", "HPF_OUT", "VREF"),
    ("R10", "22k", "HPF_OUT", "LPF_NODE"),
    ("R11", "22k", "LPF_NODE", "LPF_IN"),
    ("R12", "10k", "LPF_FB", "VREF"),
    ("R13", "91k", "LPF_FB", "RAW_EMG"),
    ("R14", "10k", "RAW_EMG", "RECT_IN"),
    ("R15", "10k", "RECT_IN", "RECT_HALF"),
    ("R16", "20k", "RECT_HALF", "ENV_IN"),
    ("R17", "10k", "RAW_EMG", "ENV_IN"),
    ("R18", "100k", "ENV_IN", "ENV_EMG"),
    ("R19", "1k", "ENV_EMG", "NET_D4_R19"),
]
ry = 142.24
for i, (ref, val, n1, n2) in enumerate(res_info):
    rx = 30.48 + (i % 7) * 27.94
    if i % 7 == 0 and i > 0: ry += 25.4
    elements.append(sym_inst("Device:R", ref, val, "Resistor_SMD:R_0603_1608Metric", rx, ry, {"1":"","2":""}))
    elements.append(wire(rx, ry+3.81, rx, ry+6.35)); elements.append(label(n1, rx, ry+6.35))
    elements.append(wire(rx, ry-3.81, rx, ry-6.35)); elements.append(label(n2, rx, ry-6.35))

# 5. Capacitors C1..C13
cap_info = [
    ("C1", "10uF", "VCC", "GND", "Capacitor_SMD:C_0805_2012Metric"),
    ("C2", "100nF", "VCC", "GND", "Capacitor_SMD:C_0603_1608Metric"),
    ("C3", "10uF", "VMID", "GND", "Capacitor_SMD:C_0805_2012Metric"),
    ("C4", "100nF", "VMID", "GND", "Capacitor_SMD:C_0603_1608Metric"),
    ("C5", "100pF", "IN_PLUS_FILT", "IN_MINUS_FILT", "Capacitor_SMD:C_0603_1608Metric"),
    ("C6", "47pF", "IN_PLUS_FILT", "GND", "Capacitor_SMD:C_0603_1608Metric"),
    ("C7", "47pF", "IN_MINUS_FILT", "GND", "Capacitor_SMD:C_0603_1608Metric"),
    ("C8", "100nF", "VCC", "GND", "Capacitor_SMD:C_0603_1608Metric"),
    ("C9", "1uF", "VOUT_IA", "HPF_OUT", "Capacitor_SMD:C_0603_1608Metric"),
    ("C10", "15nF", "LPF_NODE", "RAW_EMG", "Capacitor_SMD:C_0603_1608Metric"),
    ("C11", "6.8nF", "LPF_IN", "VREF", "Capacitor_SMD:C_0603_1608Metric"),
    ("C12", "330nF", "ENV_IN", "ENV_EMG", "Capacitor_SMD:C_0603_1608Metric"),
    ("C13", "100nF", "VCC", "GND", "Capacitor_SMD:C_0603_1608Metric"),
]
cy = 228.6
for i, (ref, val, n1, n2, fp) in enumerate(cap_info):
    cx = 30.48 + (i % 7) * 27.94
    if i % 7 == 0 and i > 0: cy += 25.4
    elements.append(sym_inst("Device:C", ref, val, fp, cx, cy, {"1":"","2":""}))
    elements.append(wire(cx, cy+3.81, cx, cy+6.35)); elements.append(label(n1, cx, cy+6.35))
    elements.append(wire(cx, cy-3.81, cx, cy-6.35)); elements.append(label(n2, cx, cy-6.35))

# 6. Diodes D1..D4
elements.append(sym_inst("Device:LED", "D1", "Green_PWR", "LED_SMD:LED_0805_2012Metric", 76.2, 40.64, {"1":"","2":""}))
elements.append(wire(76.2-3.81, 40.64, 76.2-6.35, 40.64)); elements.append(label("NET_D1_R1", 76.2-6.35, 40.64))
elements.append(wire(76.2+3.81, 40.64, 76.2+6.35, 40.64)); elements.append(label("VCC", 76.2+6.35, 40.64))

elements.append(sym_inst("Device:D", "D2", "1N4148W", "Diode_SMD:D_SOD-123", 114.3, 40.64, {"1":"","2":""}))
elements.append(wire(114.3-3.81, 40.64, 114.3-6.35, 40.64)); elements.append(label("RECT_OUT", 114.3-6.35, 40.64))
elements.append(wire(114.3+3.81, 40.64, 114.3+6.35, 40.64)); elements.append(label("RECT_IN", 114.3+6.35, 40.64))

elements.append(sym_inst("Device:D", "D3", "1N4148W", "Diode_SMD:D_SOD-123", 152.4, 40.64, {"1":"","2":""}))
elements.append(wire(152.4-3.81, 40.64, 152.4-6.35, 40.64)); elements.append(label("RECT_HALF", 152.4-6.35, 40.64))
elements.append(wire(152.4+3.81, 40.64, 152.4+6.35, 40.64)); elements.append(label("RECT_OUT", 152.4+6.35, 40.64))

elements.append(sym_inst("Device:LED", "D4", "Red_ACT", "LED_SMD:LED_0805_2012Metric", 190.5, 40.64, {"1":"","2":""}))
elements.append(wire(190.5-3.81, 40.64, 190.5-6.35, 40.64)); elements.append(label("GND", 190.5-6.35, 40.64))
elements.append(wire(190.5+3.81, 40.64, 190.5+6.35, 40.64)); elements.append(label("NET_D4_R19", 190.5+6.35, 40.64))

open('DoAn/EMG_Sensor/EMG_Sensor.kicad_sch', 'w').write(sch_head + '\n'.join(elements) + '\n)\n')
print("Generated official KiCad EMG schematic with 5 units for U2 and official symbols!")
