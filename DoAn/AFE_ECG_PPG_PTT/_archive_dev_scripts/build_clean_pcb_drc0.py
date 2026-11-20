#!/usr/bin/env python3
"""
Full Autonomous KiCad PCB Builder for AFE ECG + PPG PTT.
Enforces JLCPCB 2-Layer DFM rules.
Aims for 0 unconnected nets and minimal/zero DRC violations.
"""
import pcbnew
from test_netlist_map import NET_MAP

board = pcbnew.BOARD()

# Set up design settings according to JLCPCB capabilities
ds = board.GetDesignSettings()
ds.SetCustomTrackWidth(pcbnew.FromMM(0.254))
ds.SetCustomTrackWidth(pcbnew.FromMM(0.5))
ds.SetCustomTrackWidth(pcbnew.FromMM(0.6))
ds.SetCustomViaSize(pcbnew.FromMM(0.6))
ds.SetCustomViaDrill(pcbnew.FromMM(0.3))
ds.m_SolderMaskMargin = 0
ds.m_SolderMaskMinWidth = 0

# 1. Edge Cuts: 100 mm x 80 mm
poly = pcbnew.PCB_SHAPE(board)
poly.SetShape(pcbnew.SHAPE_T_RECT)
poly.SetStart(pcbnew.VECTOR2I(0, 0))
poly.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(100), pcbnew.FromMM(80)))
poly.SetLayer(pcbnew.Edge_Cuts)
poly.SetWidth(pcbnew.FromMM(0.15))
board.Add(poly)

# 2. Nets
for net_name in NET_MAP.keys():
    board.Add(pcbnew.NETINFO_ITEM(board, net_name))
board_nets = board.GetNetsByName()

# 3. Footprints Placement
fps = {}
pad_map = {}
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

# Mounting holes (M3 at 4 corners, offset 5mm)
add_fp('H1', 'M3', 'MountingHole', 'MountingHole_3.2mm_M3_Pad', 5, 5)
add_fp('H2', 'M3', 'MountingHole', 'MountingHole_3.2mm_M3_Pad', 95, 5)
add_fp('H3', 'M3', 'MountingHole', 'MountingHole_3.2mm_M3_Pad', 5, 75)
add_fp('H4', 'M3', 'MountingHole', 'MountingHole_3.2mm_M3_Pad', 95, 75)

# ICs
add_fp('U1', 'AD8232ACPZ', 'Package_CSP', 'LFCSP-20-1EP_4x4mm_P0.5mm_EP2.5x2.5mm', 32, 38, 0)
add_fp('U2', 'ADS1115IDGST', 'Package_SO', 'TSSOP-10_3x3mm_P0.5mm', 50, 38, 0)
add_fp('U3', 'MCP1700-3002E', 'Package_TO_SOT_SMD', 'SOT-23', 25, 62, 0)

# Connectors
add_fp('J1', 'SJ1-3533NG', 'Connector_Audio', 'Jack_3.5mm_CUI_SJ1-3533NG_Horizontal', 10, 20, 180)
add_fp('J1A', 'ECG_PROBES', 'Connector_PinHeader_2.54mm', 'PinHeader_1x03_P2.54mm_Vertical', 12, 36, 0)
add_fp('J2A', 'ESP32_L', 'Connector_PinHeader_2.54mm', 'PinHeader_1x19_P2.54mm_Vertical', 71, 16, 0)
add_fp('J2B', 'ESP32_R', 'Connector_PinHeader_2.54mm', 'PinHeader_1x19_P2.54mm_Vertical', 96.4, 16, 0)
add_fp('J3', 'MAX30102', 'Connector_PinHeader_2.54mm', 'PinHeader_1x07_P2.54mm_Vertical', 62, 16, 0)

# Input series resistors R1, R2, R3, R4
add_fp('R1', '180k', 'Resistor_SMD', 'R_0603_1608Metric', 18, 22, 0)
add_fp('R3', '180k', 'Resistor_SMD', 'R_0603_1608Metric', 23, 22, 0)
add_fp('R2', '180k', 'Resistor_SMD', 'R_0603_1608Metric', 18, 26, 0)
add_fp('R4', '180k', 'Resistor_SMD', 'R_0603_1608Metric', 23, 26, 0)

# Lead-off pullups R5, R6 (10M to +VS_A)
add_fp('R5', '10M', 'Resistor_SMD', 'R_0603_1608Metric', 23, 30, 90)
add_fp('R6', '10M', 'Resistor_SMD', 'R_0603_1608Metric', 23, 34, 90)

# RLD components C6 (1nF), R14 (1M), R15 (360k)
add_fp('C6', '1nF', 'Capacitor_SMD', 'C_0603_1608Metric', 20, 42, 0)
add_fp('R14', '1M', 'Resistor_SMD', 'R_0603_1608Metric', 20, 45, 0)
add_fp('R15', '360k', 'Resistor_SMD', 'R_0603_1608Metric', 16, 42, 90)

# HPF components C1, C2 (0.33uF), R7 (10M)
add_fp('C1', '0.33uF', 'Capacitor_SMD', 'C_0603_1608Metric', 26, 48, 0)
add_fp('C2', '0.33uF', 'Capacitor_SMD', 'C_0603_1608Metric', 30, 48, 0)
add_fp('R7', '10M', 'Resistor_SMD', 'R_0603_1608Metric', 28, 52, 90)

# Sallen-Key LPF components R10, R11, R12, R13, C3, C4
add_fp('R10', '100k', 'Resistor_SMD', 'R_0603_1608Metric', 36, 48, 0)
add_fp('R11', '100k', 'Resistor_SMD', 'R_0603_1608Metric', 40, 48, 0)
add_fp('C3', '22nF', 'Capacitor_SMD', 'C_0603_1608Metric', 36, 52, 0)
add_fp('C4', '10nF', 'Capacitor_SMD', 'C_0603_1608Metric', 40, 52, 0)
add_fp('R12', '100k', 'Resistor_SMD', 'R_0603_1608Metric', 36, 56, 0)
add_fp('R13', '1M', 'Resistor_SMD', 'R_0603_1608Metric', 40, 56, 0)

# REFIN divider R8, R9, C5
add_fp('R8', '10M', 'Resistor_SMD', 'R_0603_1608Metric', 32, 26, 0)
add_fp('R9', '10M', 'Resistor_SMD', 'R_0603_1608Metric', 36, 26, 0)
add_fp('C5', '0.1uF', 'Capacitor_SMD', 'C_0603_1608Metric', 40, 26, 0)

# AD8232 Decoupling C14 (0.1uF), C15 (1uF)
add_fp('C14', '0.1uF', 'Capacitor_SMD', 'C_0603_1608Metric', 30, 31, 0)
add_fp('C15', '1uF', 'Capacitor_SMD', 'C_0603_1608Metric', 34, 31, 0)

# LDO Decoupling C10, C11 (VIN), C12, C13 (VOUT)
add_fp('C10', '1uF', 'Capacitor_SMD', 'C_0603_1608Metric', 20, 60, 0)
add_fp('C11', '0.1uF', 'Capacitor_SMD', 'C_0603_1608Metric', 20, 64, 0)
add_fp('C12', '1uF', 'Capacitor_SMD', 'C_0603_1608Metric', 28, 60, 0)
add_fp('C13', '0.1uF', 'Capacitor_SMD', 'C_0603_1608Metric', 28, 64, 0)

# ADS1115 Anti-aliasing R16, R17, C7, C8, C9
add_fp('R16', '1k', 'Resistor_SMD', 'R_0603_1608Metric', 45, 34, 90)
add_fp('R17', '1k', 'Resistor_SMD', 'R_0603_1608Metric', 45, 42, 90)
add_fp('C7', '10nF', 'Capacitor_SMD', 'C_0603_1608Metric', 47, 34, 90)
add_fp('C8', '1nF', 'Capacitor_SMD', 'C_0603_1608Metric', 44, 30, 0)
add_fp('C9', '1nF', 'Capacitor_SMD', 'C_0603_1608Metric', 44, 46, 0)

# ADS1115 Decoupling C16, C17
add_fp('C16', '0.1uF', 'Capacitor_SMD', 'C_0603_1608Metric', 52, 30, 0)
add_fp('C17', '1uF', 'Capacitor_SMD', 'C_0603_1608Metric', 56, 30, 0)

# Pullups R18 (SDA), R19 (SCL), R20 (ALERT)
add_fp('R18', '4.7k', 'Resistor_SMD', 'R_0603_1608Metric', 64, 34, 0)
add_fp('R19', '4.7k', 'Resistor_SMD', 'R_0603_1608Metric', 64, 38, 0)
add_fp('R20', '10k', 'Resistor_SMD', 'R_0603_1608Metric', 64, 42, 0)

# Test Points TP1..TP7
tp_names = ['ECG_OUT', 'REFOUT', 'LOD+', 'LOD-', '+VS_A', '+3V3', 'GND']
for i in range(1, 8):
    add_fp(f'TP{i}', tp_names[i-1], 'TestPoint', 'TestPoint_Pad_D1.5mm', 32 + (i-1)*5, 72, 0)

# Assign nets to all pads
for net_name, conns in NET_MAP.items():
    net_item = board_nets[net_name]
    for ref, pad_num in conns:
        fp = fps[ref]
        pad = fp.FindPadByNumber(pad_num)
        if pad:
            pad.SetNet(net_item)
            pad_map[(ref, pad_num)] = pad

def get_pos(ref, pad_num):
    p = pad_map[(ref, pad_num)].GetPosition()
    return (p.x / 1e6, p.y / 1e6)

def get_escape_pos(ref, pad_num, dist=0.6):
    px, py = get_pos(ref, pad_num)
    if ref == 'U1':
        num = int(pad_num) if pad_num.isdigit() else 0
        if 1 <= num <= 5: return (px - dist, py)
        elif 6 <= num <= 10: return (px, py + dist)
        elif 11 <= num <= 15: return (px + dist, py)
        elif 16 <= num <= 20: return (px, py - dist)
    elif ref == 'U2':
        num = int(pad_num) if pad_num.isdigit() else 0
        if 1 <= num <= 5: return (px - dist, py)
        elif 6 <= num <= 10: return (px + dist, py)
    elif ref == 'U3':
        if pad_num in ['1', '2']: return (px, py + dist)
        else: return (px, py - dist)
    return (px, py)

def add_track(net_name, layer, w_mm, p1, p2):
    t = pcbnew.PCB_TRACK(board)
    t.SetNet(board_nets[net_name])
    t.SetLayer(layer)
    t.SetWidth(pcbnew.FromMM(w_mm))
    t.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(p1[0]), pcbnew.FromMM(p1[1])))
    t.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(p2[0]), pcbnew.FromMM(p2[1])))
    board.Add(t)

def add_via(net_name, pos):
    v = pcbnew.PCB_VIA(board)
    v.SetNet(board_nets[net_name])
    v.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(pos[0]), pcbnew.FromMM(pos[1])))
    v.SetWidth(pcbnew.FromMM(0.6))
    v.SetDrill(pcbnew.FromMM(0.3))
    v.SetLayerPair(pcbnew.F_Cu, pcbnew.B_Cu)
    v.SetViaType(pcbnew.VIATYPE_THROUGH)
    board.Add(v)

def route_fcu_escape(net_name, ref1, p1_name, ref2, p2_name, w_mm=0.254):
    p1 = get_pos(ref1, p1_name)
    e1 = get_escape_pos(ref1, p1_name)
    p2 = get_pos(ref2, p2_name)
    e2 = get_escape_pos(ref2, p2_name)
    
    # Track from pad 1 to escape 1
    if p1 != e1: add_track(net_name, pcbnew.F_Cu, w_mm, p1, e1)
    
    # Path between e1 and e2
    if e1[0] == e2[0] or e1[1] == e2[1]:
        add_track(net_name, pcbnew.F_Cu, w_mm, e1, e2)
    else:
        mid = (e2[0], e1[1])
        add_track(net_name, pcbnew.F_Cu, w_mm, e1, mid)
        add_track(net_name, pcbnew.F_Cu, w_mm, mid, e2)
        
    # Track from escape 2 to pad 2
    if e2 != p2: add_track(net_name, pcbnew.F_Cu, w_mm, e2, p2)

def route_corridor_escape(net_name, ref1, p1_name, ref2, p2_name, trunk_y, w_mm=0.254):
    p1 = get_pos(ref1, p1_name)
    e1 = get_escape_pos(ref1, p1_name)
    p2 = get_pos(ref2, p2_name)
    e2 = get_escape_pos(ref2, p2_name)
    
    # Pad 1 to escape 1 on F.Cu
    if p1 != e1: add_track(net_name, pcbnew.F_Cu, w_mm, p1, e1)
    add_via(net_name, e1)
    
    # B.Cu routing from e1 -> (e1[0], trunk_y) -> (e2[0], trunk_y) -> e2
    v1 = (e1[0], trunk_y)
    v2 = (e2[0], trunk_y)
    if e1 != v1: add_track(net_name, pcbnew.B_Cu, w_mm, e1, v1)
    if v1 != v2: add_track(net_name, pcbnew.B_Cu, w_mm, v1, v2)
    if v2 != e2: add_track(net_name, pcbnew.B_Cu, w_mm, v2, e2)
    
    add_via(net_name, e2)
    if e2 != p2: add_track(net_name, pcbnew.F_Cu, w_mm, e2, p2)

# Route all intra-cluster analog chains
# 1. RA
route_fcu_escape("RA_RAW", "J1", "T", "J1A", "1")
route_fcu_escape("RA_RAW", "J1A", "1", "R1", "1")
route_fcu_escape("RA_INT", "R1", "2", "R3", "1")
route_fcu_escape("RA_FILT", "R3", "2", "R5", "2")
route_fcu_escape("RA_FILT", "R5", "2", "U1", "2")

# 2. LA
route_fcu_escape("LA_RAW", "J1", "R", "J1A", "2")
route_fcu_escape("LA_RAW", "J1A", "2", "R2", "1")
route_fcu_escape("LA_INT", "R2", "2", "R4", "1")
route_fcu_escape("LA_FILT", "R4", "2", "R6", "2")
route_fcu_escape("LA_FILT", "R6", "2", "U1", "3")

# 3. RL
route_fcu_escape("RL_RAW", "J1", "S", "J1A", "3")
route_fcu_escape("RL_RAW", "J1A", "3", "R15", "2")
route_fcu_escape("RLD_OUT", "U1", "5", "R15", "1")
route_fcu_escape("RLD_OUT", "R15", "1", "C6", "2")
route_fcu_escape("RLD_OUT", "C6", "2", "R14", "2")
route_fcu_escape("RLDFB", "U1", "4", "C6", "1")
route_fcu_escape("RLDFB", "C6", "1", "R14", "1")

# 4. HPF
route_fcu_escape("HPDRIVE", "U1", "1", "C1", "1")
route_fcu_escape("HP_MID", "C1", "2", "C2", "1")
route_fcu_escape("HP_MID", "C2", "1", "U1", "6")
route_fcu_escape("HP_MID", "U1", "6", "R7", "1")
route_fcu_escape("HPSENSE", "C2", "2", "U1", "20")

# 5. REFIN & REFOUT
route_fcu_escape("REFIN", "R8", "2", "R9", "1")
route_fcu_escape("REFIN", "R9", "1", "C5", "1")
route_fcu_escape("REFIN", "R8", "2", "U1", "18")
route_fcu_escape("REFOUT", "U1", "8", "C4", "2")
route_fcu_escape("REFOUT", "C4", "2", "R12", "2")
route_fcu_escape("REFOUT", "C4", "2", "R17", "1")
route_fcu_escape("REFOUT", "R12", "2", "TP2", "1")

# 6. Sallen-Key LPF
route_fcu_escape("IAOUT", "U1", "19", "R10", "1")
route_fcu_escape("SK_N1", "R10", "2", "R11", "1")
route_fcu_escape("SK_N1", "R10", "2", "C3", "1")
route_fcu_escape("OPAMP_P", "U1", "7", "R11", "2")
route_fcu_escape("OPAMP_P", "R11", "2", "C4", "1")
route_fcu_escape("OPAMP_N", "U1", "9", "R12", "1")
route_fcu_escape("OPAMP_N", "R12", "1", "R13", "1")
route_fcu_escape("ECG_OUT", "U1", "10", "C3", "2")
route_fcu_escape("ECG_OUT", "C3", "2", "R13", "2")
route_fcu_escape("ECG_OUT", "R13", "2", "R16", "1")
route_fcu_escape("ECG_OUT", "R13", "2", "TP1", "1")

# 7. Anti-aliasing
route_fcu_escape("AIN0_FILT", "R16", "2", "C7", "1")
route_fcu_escape("AIN0_FILT", "C7", "1", "C8", "1")
route_fcu_escape("AIN0_FILT", "C7", "1", "U2", "4")
route_fcu_escape("AIN1_FILT", "R17", "2", "C7", "2")
route_fcu_escape("AIN1_FILT", "C7", "2", "C9", "1")
route_fcu_escape("AIN1_FILT", "C7", "2", "U2", "5")

# 8. Digital Cross-Board Routes using Dedicated Trunk Y Corridors on B.Cu
route_fcu_escape("I2C_SCL", "U2", "10", "R19", "2")
route_fcu_escape("I2C_SCL", "R19", "2", "J3", "2")
route_corridor_escape("I2C_SCL", "J3", "2", "J2B", "3", trunk_y=18.0)

route_fcu_escape("I2C_SDA", "U2", "9", "R18", "2")
route_fcu_escape("I2C_SDA", "R18", "2", "J3", "3")
route_corridor_escape("I2C_SDA", "J3", "3", "J2B", "6", trunk_y=21.0)

route_corridor_escape("MAX_INT", "J3", "4", "J2A", "10", trunk_y=24.0)

route_fcu_escape("ADS_ALERT", "U2", "2", "R20", "2")
route_fcu_escape("ADS_ALERT", "R20", "2", "J2A", "11")

route_fcu_escape("LOD+", "U1", "12", "TP3", "1")
route_corridor_escape("LOD+", "TP3", "1", "J2A", "7", trunk_y=68.0)

route_fcu_escape("LOD-", "U1", "11", "TP4", "1")
route_corridor_escape("LOD-", "TP4", "1", "J2A", "8", trunk_y=70.0)

route_corridor_escape("FR", "U1", "15", "J2A", "9", trunk_y=72.0)
route_corridor_escape("ECG_OUT", "TP1", "1", "J2A", "5", trunk_y=66.0)

# Power Rails
route_fcu_escape("+VS_A", "U3", "2", "C12", "1", 0.5)
route_fcu_escape("+VS_A", "C12", "1", "C13", "1", 0.5)
route_fcu_escape("+VS_A", "C12", "1", "C14", "1", 0.5)
route_fcu_escape("+VS_A", "C14", "1", "C15", "1", 0.5)
route_fcu_escape("+VS_A", "C14", "1", "U1", "17", 0.5)
route_fcu_escape("+VS_A", "U1", "17", "U1", "13", 0.3)
route_fcu_escape("+VS_A", "U1", "17", "R8", "1", 0.3)
route_fcu_escape("+VS_A", "R8", "1", "R5", "1", 0.3)
route_fcu_escape("+VS_A", "R5", "1", "R6", "1", 0.3)
route_fcu_escape("+VS_A", "U3", "2", "TP5", "1", 0.3)

route_fcu_escape("+3V3", "J2A", "1", "J3", "1", 0.6)
route_fcu_escape("+3V3", "J3", "1", "R18", "1", 0.4)
route_fcu_escape("+3V3", "R18", "1", "R19", "1", 0.4)
route_fcu_escape("+3V3", "R19", "1", "R20", "1", 0.4)
route_fcu_escape("+3V3", "R18", "1", "U2", "8", 0.4)
route_fcu_escape("+3V3", "U2", "8", "C16", "1", 0.4)
route_fcu_escape("+3V3", "C16", "1", "C17", "1", 0.4)
route_corridor_escape("+3V3", "C16", "1", "U3", "3", trunk_y=14.0, w_mm=0.6)
route_fcu_escape("+3V3", "U3", "3", "C10", "1", 0.5)
route_fcu_escape("+3V3", "C10", "1", "C11", "1", 0.5)
route_fcu_escape("+3V3", "U3", "3", "TP6", "1", 0.3)

# Ground Vias for all SMD GND pads to B.Cu GND plane
gnd_net = board_nets["GND"]
for ref, pad_num in NET_MAP["GND"]:
    pad = fps[ref].FindPadByNumber(pad_num)
    if pad and pad.GetAttribute() == pcbnew.PAD_ATTRIB_SMD:
        p = pad.GetPosition()
        via_pos = pcbnew.VECTOR2I(p.x, p.y + pcbnew.FromMM(1.2))
        v = pcbnew.PCB_VIA(board)
        v.SetNet(gnd_net)
        v.SetPosition(via_pos)
        v.SetWidth(pcbnew.FromMM(0.6))
        v.SetDrill(pcbnew.FromMM(0.3))
        v.SetLayerPair(pcbnew.F_Cu, pcbnew.B_Cu)
        v.SetViaType(pcbnew.VIATYPE_THROUGH)
        board.Add(v)
        add_track("GND", pcbnew.F_Cu, 0.254, (p.x/1e6, p.y/1e6), (via_pos.x/1e6, via_pos.y/1e6))

# Solid GND zone on B.Cu
poly_zone = pcbnew.SHAPE_LINE_CHAIN()
poly_zone.Append(pcbnew.VECTOR2I(pcbnew.FromMM(1), pcbnew.FromMM(1)))
poly_zone.Append(pcbnew.VECTOR2I(pcbnew.FromMM(99), pcbnew.FromMM(1)))
poly_zone.Append(pcbnew.VECTOR2I(pcbnew.FromMM(99), pcbnew.FromMM(79)))
poly_zone.Append(pcbnew.VECTOR2I(pcbnew.FromMM(1), pcbnew.FromMM(79)))
poly_zone.SetClosed(True)

zone = pcbnew.ZONE(board)
zone.SetNet(gnd_net)
zone.SetLayer(pcbnew.B_Cu)
zone.AddPolygon(poly_zone)
zone.SetPadConnection(pcbnew.ZONE_CONNECTION_THERMAL)
zone.SetThermalReliefSpokeWidth(pcbnew.FromMM(0.3))
zone.SetThermalReliefGap(pcbnew.FromMM(0.25))
zone.SetMinThickness(pcbnew.FromMM(0.2))
board.Add(zone)

add_track("GND", pcbnew.B_Cu, 0.5, get_pos("J3", "7"), get_pos("J2A", "14"))
filler = pcbnew.ZONE_FILLER(board)
filler.Fill(board.Zones())

out_file = "AFE_ECG_PPG_PTT.kicad_pcb"
pcbnew.SaveBoard(out_file, board)
print("Saved routed board to", out_file)
