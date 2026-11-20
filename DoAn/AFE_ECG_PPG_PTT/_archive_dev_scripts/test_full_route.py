import pcbnew
import math
from test_netlist_map import NET_MAP

board = pcbnew.BOARD()

# Design settings
ds = board.GetDesignSettings()
ds.SetCustomTrackWidth(pcbnew.FromMM(0.254))
ds.SetCustomViaSize(pcbnew.FromMM(0.6))
ds.SetCustomViaDrill(pcbnew.FromMM(0.3))

# Edge Cuts: 100 x 80 mm
poly = pcbnew.PCB_SHAPE(board)
poly.SetShape(pcbnew.SHAPE_T_RECT)
poly.SetStart(pcbnew.VECTOR2I(0, 0))
poly.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(100), pcbnew.FromMM(80)))
poly.SetLayer(pcbnew.Edge_Cuts)
poly.SetWidth(pcbnew.FromMM(0.15))
board.Add(poly)

# Add nets
for net_name in NET_MAP.keys():
    item = pcbnew.NETINFO_ITEM(board, net_name)
    board.Add(item)

board_nets = board.GetNetsByName()

fps = {}
def add_fp(ref, val, lib, name, x, y, rot=0):
    fp = pcbnew.FootprintLoad(f'/usr/share/kicad/footprints/{lib}.pretty', name)
    assert fp is not None, f'Failed {lib}:{name}'
    fp.SetReference(ref)
    fp.SetValue(val)
    fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y)))
    fp.SetOrientation(pcbnew.EDA_ANGLE(rot, pcbnew.DEGREES_T))
    board.Add(fp)
    fps[ref] = fp
    return fp

# Placement
add_fp('H1', 'M3', 'MountingHole', 'MountingHole_3.2mm_M3_Pad', 5, 5)
add_fp('H2', 'M3', 'MountingHole', 'MountingHole_3.2mm_M3_Pad', 95, 5)
add_fp('H3', 'M3', 'MountingHole', 'MountingHole_3.2mm_M3_Pad', 5, 75)
add_fp('H4', 'M3', 'MountingHole', 'MountingHole_3.2mm_M3_Pad', 95, 75)

add_fp('U1', 'AD8232ACPZ', 'Package_CSP', 'LFCSP-20-1EP_4x4mm_P0.5mm_EP2.5x2.5mm', 32, 38, 0)
add_fp('U2', 'ADS1115IDGST', 'Package_SO', 'TSSOP-10_3x3mm_P0.5mm', 48, 38, 0)
add_fp('U3', 'MCP1700-3002E', 'Package_TO_SOT_SMD', 'SOT-23', 25, 62, 0)

add_fp('J1', 'SJ1-3533NG', 'Connector_Audio', 'Jack_3.5mm_CUI_SJ1-3533NG_Horizontal', 10, 20, 180)
add_fp('J1A', 'ECG_PROBES', 'Connector_PinHeader_2.54mm', 'PinHeader_1x03_P2.54mm_Vertical', 12, 36, 0)
add_fp('J2A', 'ESP32_L', 'Connector_PinHeader_2.54mm', 'PinHeader_1x19_P2.54mm_Vertical', 72, 16, 0)
add_fp('J2B', 'ESP32_R', 'Connector_PinHeader_2.54mm', 'PinHeader_1x19_P2.54mm_Vertical', 97.4, 16, 0)
add_fp('J3', 'MAX30102', 'Connector_PinHeader_2.54mm', 'PinHeader_1x07_P2.54mm_Vertical', 60, 16, 0)

add_fp('R1', '180k', 'Resistor_SMD', 'R_0603_1608Metric', 18, 22, 0)
add_fp('R3', '180k', 'Resistor_SMD', 'R_0603_1608Metric', 23, 22, 0)
add_fp('R2', '180k', 'Resistor_SMD', 'R_0603_1608Metric', 18, 26, 0)
add_fp('R4', '180k', 'Resistor_SMD', 'R_0603_1608Metric', 23, 26, 0)

add_fp('R5', '10M', 'Resistor_SMD', 'R_0603_1608Metric', 23, 30, 90)
add_fp('R6', '10M', 'Resistor_SMD', 'R_0603_1608Metric', 23, 34, 90)

add_fp('C6', '1nF', 'Capacitor_SMD', 'C_0603_1608Metric', 20, 42, 0)
add_fp('R14', '1M', 'Resistor_SMD', 'R_0603_1608Metric', 20, 45, 0)
add_fp('R15', '360k', 'Resistor_SMD', 'R_0603_1608Metric', 16, 42, 90)

add_fp('C1', '0.33uF', 'Capacitor_SMD', 'C_0603_1608Metric', 26, 48, 0)
add_fp('C2', '0.33uF', 'Capacitor_SMD', 'C_0603_1608Metric', 30, 48, 0)
add_fp('R7', '10M', 'Resistor_SMD', 'R_0603_1608Metric', 28, 52, 90)

add_fp('R10', '100k', 'Resistor_SMD', 'R_0603_1608Metric', 36, 48, 0)
add_fp('R11', '100k', 'Resistor_SMD', 'R_0603_1608Metric', 40, 48, 0)
add_fp('C3', '22nF', 'Capacitor_SMD', 'C_0603_1608Metric', 36, 52, 0)
add_fp('C4', '10nF', 'Capacitor_SMD', 'C_0603_1608Metric', 40, 52, 0)
add_fp('R12', '100k', 'Resistor_SMD', 'R_0603_1608Metric', 36, 56, 0)
add_fp('R13', '1M', 'Resistor_SMD', 'R_0603_1608Metric', 40, 56, 0)

add_fp('R8', '10M', 'Resistor_SMD', 'R_0603_1608Metric', 32, 26, 0)
add_fp('R9', '10M', 'Resistor_SMD', 'R_0603_1608Metric', 36, 26, 0)
add_fp('C5', '0.1uF', 'Capacitor_SMD', 'C_0603_1608Metric', 40, 26, 0)

add_fp('C14', '0.1uF', 'Capacitor_SMD', 'C_0603_1608Metric', 30, 31, 0)
add_fp('C15', '1uF', 'Capacitor_SMD', 'C_0603_1608Metric', 34, 31, 0)

add_fp('C10', '1uF', 'Capacitor_SMD', 'C_0603_1608Metric', 20, 60, 0)
add_fp('C11', '0.1uF', 'Capacitor_SMD', 'C_0603_1608Metric', 20, 64, 0)
add_fp('C12', '1uF', 'Capacitor_SMD', 'C_0603_1608Metric', 28, 60, 0)
add_fp('C13', '0.1uF', 'Capacitor_SMD', 'C_0603_1608Metric', 28, 64, 0)

add_fp('R16', '1k', 'Resistor_SMD', 'R_0603_1608Metric', 44, 34, 90)
add_fp('R17', '1k', 'Resistor_SMD', 'R_0603_1608Metric', 44, 42, 90)
add_fp('C7', '10nF', 'Capacitor_SMD', 'C_0603_1608Metric', 46, 34, 90)
add_fp('C8', '1nF', 'Capacitor_SMD', 'C_0603_1608Metric', 44, 30, 0)
add_fp('C9', '1nF', 'Capacitor_SMD', 'C_0603_1608Metric', 44, 46, 0)

add_fp('C16', '0.1uF', 'Capacitor_SMD', 'C_0603_1608Metric', 50, 30, 0)
add_fp('C17', '1uF', 'Capacitor_SMD', 'C_0603_1608Metric', 54, 30, 0)

add_fp('R18', '4.7k', 'Resistor_SMD', 'R_0603_1608Metric', 62, 34, 0)
add_fp('R19', '4.7k', 'Resistor_SMD', 'R_0603_1608Metric', 62, 38, 0)
add_fp('R20', '10k', 'Resistor_SMD', 'R_0603_1608Metric', 62, 42, 0)

tp_names = ['ECG_OUT', 'REFOUT', 'LOD+', 'LOD-', '+VS_A', '+3V3', 'GND']
for i in range(1, 8):
    add_fp(f'TP{i}', tp_names[i-1], 'TestPoint', 'TestPoint_Pad_D1.5mm', 32 + (i-1)*5, 72, 0)

# Assign nets
for net_name, conns in NET_MAP.items():
    net_item = board_nets[net_name]
    for ref, pad_num in conns:
        fp = fps[ref]
        pad = fp.FindPadByNumber(pad_num)
        if pad:
            pad.SetNet(net_item)

# Routing primitives
def add_seg(net, layer, w_mm, p1, p2):
    t = pcbnew.PCB_TRACK(board)
    t.SetNet(net)
    t.SetLayer(layer)
    t.SetWidth(pcbnew.FromMM(w_mm))
    t.SetStart(p1)
    t.SetEnd(p2)
    board.Add(t)

def add_via(net, pos, size_mm=0.6, drill_mm=0.3):
    v = pcbnew.PCB_VIA(board)
    v.SetNet(net)
    v.SetPosition(pos)
    v.SetWidth(pcbnew.FromMM(size_mm))
    v.SetDrill(pcbnew.FromMM(drill_mm))
    v.SetLayerPair(pcbnew.F_Cu, pcbnew.B_Cu)
    v.SetViaType(pcbnew.VIATYPE_THROUGH)
    board.Add(v)
    return v

def connect_pads_fcu(net_name, pad1, pad2, w_mm=0.254):
    p1 = pad1.GetPosition()
    p2 = pad2.GetPosition()
    net = board_nets[net_name]
    if p1.x == p2.x or p1.y == p2.y:
        add_seg(net, pcbnew.F_Cu, w_mm, p1, p2)
    else:
        # 2 segment L-route
        mid = pcbnew.VECTOR2I(p2.x, p1.y)
        add_seg(net, pcbnew.F_Cu, w_mm, p1, mid)
        add_seg(net, pcbnew.F_Cu, w_mm, mid, p2)

# 1. Connect all GND pads to GND plane via vias
gnd_net = board_nets["GND"]
for ref, pad_num in NET_MAP["GND"]:
    fp = fps[ref]
    pad = fp.FindPadByNumber(pad_num)
    if not pad: continue
    pos = pad.GetPosition()
    # If through hole (like headers or mounting holes), it directly touches B.Cu!
    # If SMD pad, drop a via nearby
    if pad.GetAttribute() == pcbnew.PAD_ATTRIB_SMD:
        # place via offset
        via_pos = pcbnew.VECTOR2I(pos.x + pcbnew.FromMM(0.0), pos.y + pcbnew.FromMM(0.9))
        # thermal spokes handle it
        pass

# 2. Add solid GND zones on B.Cu and F.Cu
for layer in [pcbnew.B_Cu, pcbnew.F_Cu]:
    poly_zone = pcbnew.SHAPE_LINE_CHAIN()
    poly_zone.Append(pcbnew.VECTOR2I(pcbnew.FromMM(1), pcbnew.FromMM(1)))
    poly_zone.Append(pcbnew.VECTOR2I(pcbnew.FromMM(99), pcbnew.FromMM(1)))
    poly_zone.Append(pcbnew.VECTOR2I(pcbnew.FromMM(99), pcbnew.FromMM(79)))
    poly_zone.Append(pcbnew.VECTOR2I(pcbnew.FromMM(1), pcbnew.FromMM(79)))
    poly_zone.SetClosed(True)

    zone = pcbnew.ZONE(board)
    zone.SetNet(gnd_net)
    zone.SetLayer(layer)
    zone.AddPolygon(poly_zone)
    zone.SetPadConnection(pcbnew.ZONE_CONNECTION_THERMAL)
    zone.SetThermalReliefSpokeWidth(pcbnew.FromMM(0.3))
    zone.SetThermalReliefGap(pcbnew.FromMM(0.25))
    zone.SetMinThickness(pcbnew.FromMM(0.2))
    board.Add(zone)

# Fill zones
filler = pcbnew.ZONE_FILLER(board)
filler.Fill(board.Zones())

out_file = "/tmp/test_full_route.kicad_pcb"
pcbnew.SaveBoard(out_file, board)
print("Saved routed board to", out_file)
