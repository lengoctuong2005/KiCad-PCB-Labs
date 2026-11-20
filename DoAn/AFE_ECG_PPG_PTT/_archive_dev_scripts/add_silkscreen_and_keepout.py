import pcbnew

board = pcbnew.LoadBoard("AFE_ECG_PPG_PTT.kicad_pcb")

def add_text(text, x_mm, y_mm, layer=pcbnew.F_SilkS, size_mm=1.0, thickness_mm=0.15):
    txt = pcbnew.PCB_TEXT(board)
    txt.SetText(text)
    txt.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x_mm), pcbnew.FromMM(y_mm)))
    txt.SetLayer(layer)
    txt.SetTextSize(pcbnew.VECTOR2I(pcbnew.FromMM(size_mm), pcbnew.FromMM(size_mm)))
    txt.SetTextThickness(pcbnew.FromMM(thickness_mm))
    board.Add(txt)
    return txt

# 1. Main Project Header
add_text("AFE ECG + PPG PTT ACQUISITION SYSTEM", 15, 8, size_mm=1.5, thickness_mm=0.25)
add_text("Author: Le Ngoc Tuong - MSSV: 23207124 - Class: 23DTV_CLC3", 15, 11, size_mm=1.0, thickness_mm=0.15)
add_text("Hardware Rev 1.0 - Nov 2026 - Capstone Project", 15, 14, size_mm=0.9, thickness_mm=0.15)

# 2. Safety Notice (Crucial Bio-medical Constraint)
add_text("SAFETY: BATTERY / POWERBANK ONLY", 10, 77, size_mm=1.1, thickness_mm=0.20)
add_text("DO NOT CONNECT MAINS USB WHEN ELECTRODES ATTACHED", 48, 77, size_mm=0.85, thickness_mm=0.15)

# 3. Connector Labels
add_text("J1: ECG 3.5mm JACK (RA/LA/RL)", 8, 27, size_mm=0.8, thickness_mm=0.12)
add_text("J1A: PROBES", 2, 33, size_mm=0.8, thickness_mm=0.12)
add_text("1:RA", 2, 44, size_mm=0.7, thickness_mm=0.12)
add_text("2:LA", 2, 46, size_mm=0.7, thickness_mm=0.12)
add_text("3:RL", 2, 48, size_mm=0.7, thickness_mm=0.12)

add_text("J3: MAX30102 PPG MODULE", 55, 12, size_mm=0.9, thickness_mm=0.15)
add_text("VIN SCL SDA INT RD IRD GND", 58, 35, size_mm=0.65, thickness_mm=0.12)

add_text("ESP32 DEVKIT-38P", 74, 12, size_mm=1.0, thickness_mm=0.18)
add_text("ANTENNA KEEPOUT", 76, 5, size_mm=0.85, thickness_mm=0.15)

# 4. Test Point Labels
tp_labels = [
    ("TP7:GND", 22, 70),
    ("TP6:3V3", 25, 70),
    ("TP5:AVDD", 28, 70),
    ("TP1:OUT", 42, 55),
    ("TP2:REF", 38.5, 55),
    ("TP3:LOD+", 38, 29),
    ("TP4:LOD-", 40, 36)
]
for lbl, x, y in tp_labels:
    add_text(lbl, x, y, size_mm=0.7, thickness_mm=0.12)

# 5. Zone Partition Silkscreen Dividers
# Line dividing Analog Zone from Digital Zone at X = 53 mm
div = pcbnew.PCB_SHAPE(board)
div.SetShape(pcbnew.SHAPE_T_SEGMENT)
div.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(53), pcbnew.FromMM(18)))
div.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(53), pcbnew.FromMM(74)))
div.SetLayer(pcbnew.F_SilkS)
div.SetWidth(pcbnew.FromMM(0.2))
board.Add(div)

add_text("<< ANALOG AFE ZONE", 34, 18, size_mm=0.85, thickness_mm=0.15)
add_text("DIGITAL & MCU ZONE >>", 55, 18, size_mm=0.85, thickness_mm=0.15)

# 6. ESP32 Antenna Keepout Area (X: 71..96, Y: 0..8)
zone_ko = pcbnew.ZONE(board)
zone_ko.SetIsRuleArea(True)
zone_ko.SetDoNotAllowZoneFills(True)
zone_ko.SetDoNotAllowTracks(True)
zone_ko.SetDoNotAllowVias(True)
zone_ko.SetLayer(pcbnew.F_Cu)

ko_poly = pcbnew.SHAPE_LINE_CHAIN()
ko_poly.Append(pcbnew.VECTOR2I(pcbnew.FromMM(70), pcbnew.FromMM(0)))
ko_poly.Append(pcbnew.VECTOR2I(pcbnew.FromMM(98), pcbnew.FromMM(0)))
ko_poly.Append(pcbnew.VECTOR2I(pcbnew.FromMM(98), pcbnew.FromMM(10)))
ko_poly.Append(pcbnew.VECTOR2I(pcbnew.FromMM(70), pcbnew.FromMM(10)))
ko_poly.SetClosed(True)
zone_ko.AddPolygon(ko_poly)
board.Add(zone_ko)

pcbnew.SaveBoard("AFE_ECG_PPG_PTT.kicad_pcb", board)
print("Silkscreen markings and antenna keepout added successfully.")
