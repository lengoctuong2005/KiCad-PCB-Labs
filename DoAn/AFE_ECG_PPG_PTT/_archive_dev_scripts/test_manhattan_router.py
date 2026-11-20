import pcbnew
from test_netlist_map import NET_MAP

board = pcbnew.BOARD()

ds = board.GetDesignSettings()
ds.SetCustomTrackWidth(pcbnew.FromMM(0.254))
ds.SetCustomViaSize(pcbnew.FromMM(0.6))
ds.SetCustomViaDrill(pcbnew.FromMM(0.3))
ds.m_SolderMaskMargin = 0
ds.m_SolderMaskMinWidth = pcbnew.FromMM(0.08)

# 1. Edge Cuts 100 x 80 mm
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

# 3. Footprints
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

# Placement - Clean floorplan with generous spacing
add_fp('H1', 'M3', 'MountingHole', 'MountingHole_3.2mm_M3_Pad', 5, 5)
add_fp('H2', 'M3', 'MountingHole', 'MountingHole_3.2mm_M3_Pad', 95, 5)
add_fp('H3', 'M3', 'MountingHole', 'MountingHole_3.2mm_M3_Pad', 5, 75)
add_fp('H4', 'M3', 'MountingHole', 'MountingHole_3.2mm_M3_Pad', 95, 75)

# ICs
add_fp('U1', 'AD8232ACPZ', 'Package_CSP', 'LFCSP-20-1EP_4x4mm_P0.5mm_EP2.5x2.5mm', 32, 38, 0)
add_fp('U2', 'ADS1115IDGST', 'Package_SO', 'TSSOP-10_3x3mm_P0.5mm', 48, 38, 0)
add_fp('U3', 'MCP1700-3002E', 'Package_TO_SOT_SMD', 'SOT-23', 25, 62, 0)

# Connectors
add_fp('J1', 'SJ1-3533NG', 'Connector_Audio', 'Jack_3.5mm_CUI_SJ1-3533NG_Horizontal', 10, 20, 180)
add_fp('J1A', 'ECG_PROBES', 'Connector_PinHeader_2.54mm', 'PinHeader_1x03_P2.54mm_Vertical', 12, 36, 0)
add_fp('J2A', 'ESP32_L', 'Connector_PinHeader_2.54mm', 'PinHeader_1x19_P2.54mm_Vertical', 72, 16, 0)
add_fp('J2B', 'ESP32_R', 'Connector_PinHeader_2.54mm', 'PinHeader_1x19_P2.54mm_Vertical', 97.4, 16, 0)
add_fp('J3', 'MAX30102', 'Connector_PinHeader_2.54mm', 'PinHeader_1x07_P2.54mm_Vertical', 60, 16, 0)

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
add_fp('R16', '1k', 'Resistor_SMD', 'R_0603_1608Metric', 44, 34, 90)
add_fp('R17', '1k', 'Resistor_SMD', 'R_0603_1608Metric', 44, 42, 90)
add_fp('C7', '10nF', 'Capacitor_SMD', 'C_0603_1608Metric', 46, 34, 90)
add_fp('C8', '1nF', 'Capacitor_SMD', 'C_0603_1608Metric', 44, 30, 0)
add_fp('C9', '1nF', 'Capacitor_SMD', 'C_0603_1608Metric', 44, 46, 0)

# ADS1115 Decoupling C16, C17
add_fp('C16', '0.1uF', 'Capacitor_SMD', 'C_0603_1608Metric', 50, 30, 0)
add_fp('C17', '1uF', 'Capacitor_SMD', 'C_0603_1608Metric', 54, 30, 0)

# Pullups R18 (SDA), R19 (SCL), R20 (ALERT)
add_fp('R18', '4.7k', 'Resistor_SMD', 'R_0603_1608Metric', 62, 34, 0)
add_fp('R19', '4.7k', 'Resistor_SMD', 'R_0603_1608Metric', 62, 38, 0)
add_fp('R20', '10k', 'Resistor_SMD', 'R_0603_1608Metric', 62, 42, 0)

# Test Points TP1..TP7
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
            pad_map[(ref, pad_num)] = pad

def get_pos(ref, pad_num):
    p = pad_map[(ref, pad_num)].GetPosition()
    return (p.x / 1e6, p.y / 1e6)

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

# Routing helper: Manhattan corridor router
def route_corridor(net_name, p1, p2, trunk_y, w_mm=0.254):
    # p1 -> via at (p1.x, trunk_y) on B.Cu -> track along trunk_y to (p2.x, trunk_y) -> via at (p2.x, trunk_y) -> p2 on F.Cu
    v1 = (p1[0], trunk_y)
    v2 = (p2[0], trunk_y)
    
    # F.Cu vertical drop to via 1
    add_track(net_name, pcbnew.F_Cu, w_mm, p1, v1)
    add_via(net_name, v1)
    
    # B.Cu horizontal trunk
    add_track(net_name, pcbnew.B_Cu, w_mm, v1, v2)
    
    # Via 2 and F.Cu vertical rise to p2
    add_via(net_name, v2)
    add_track(net_name, pcbnew.F_Cu, w_mm, v2, p2)

# Simple local F.Cu track between two points
def route_local(net_name, p1, p2, w_mm=0.254):
    if p1[0] == p2[0] or p1[1] == p2[1]:
        add_track(net_name, pcbnew.F_Cu, w_mm, p1, p2)
    else:
        mid = (p2[0], p1[1])
        add_track(net_name, pcbnew.F_Cu, w_mm, p1, mid)
        add_track(net_name, pcbnew.F_Cu, w_mm, mid, p2)

# Local intra-cluster connections (no crossings)
# 1. RA_RAW, RA_INT, RA_FILT
route_local("RA_RAW", get_pos("J1", "T"), get_pos("J1A", "1"))
route_local("RA_RAW", get_pos("J1A", "1"), get_pos("R1", "1"))
route_local("RA_INT", get_pos("R1", "2"), get_pos("R3", "1"))
route_local("RA_FILT", get_pos("R3", "2"), get_pos("R5", "2"))
route_local("RA_FILT", get_pos("R5", "2"), get_pos("U1", "2"))

# 2. LA_RAW, LA_INT, LA_FILT
route_local("LA_RAW", get_pos("J1", "R"), get_pos("J1A", "2"))
route_local("LA_RAW", get_pos("J1A", "2"), get_pos("R2", "1"))
route_local("LA_INT", get_pos("R2", "2"), get_pos("R4", "1"))
route_local("LA_FILT", get_pos("R4", "2"), get_pos("R6", "2"))
route_local("LA_FILT", get_pos("R6", "2"), get_pos("U1", "3"))

# 3. RL_RAW, RLD_OUT, RLDFB
route_local("RL_RAW", get_pos("J1", "S"), get_pos("J1A", "3"))
route_local("RL_RAW", get_pos("J1A", "3"), get_pos("R15", "2"))
route_local("RLD_OUT", get_pos("U1", "5"), get_pos("R15", "1"))
route_local("RLD_OUT", get_pos("R15", "1"), get_pos("C6", "2"))
route_local("RLD_OUT", get_pos("C6", "2"), get_pos("R14", "2"))
route_local("RLDFB", get_pos("U1", "4"), get_pos("C6", "1"))
route_local("RLDFB", get_pos("C6", "1"), get_pos("R14", "1"))

# 4. HPF
route_local("HPDRIVE", get_pos("U1", "1"), get_pos("C1", "1"))
route_local("HP_MID", get_pos("C1", "2"), get_pos("C2", "1"))
route_local("HP_MID", get_pos("C2", "1"), get_pos("U1", "6"))
route_local("HP_MID", get_pos("U1", "6"), get_pos("R7", "1"))
route_local("HPSENSE", get_pos("C2", "2"), get_pos("U1", "20"))

# 5. REFIN & REFOUT
route_local("REFIN", get_pos("R8", "2"), get_pos("R9", "1"))
route_local("REFIN", get_pos("R9", "1"), get_pos("C5", "1"))
route_local("REFIN", get_pos("R8", "2"), get_pos("U1", "18"))
route_local("REFOUT", get_pos("U1", "8"), get_pos("C4", "2"))
route_local("REFOUT", get_pos("C4", "2"), get_pos("R12", "2"))
route_local("REFOUT", get_pos("C4", "2"), get_pos("R17", "1"))
route_local("REFOUT", get_pos("R12", "2"), get_pos("TP2", "1"))

# 6. Sallen-Key LPF
route_local("IAOUT", get_pos("U1", "19"), get_pos("R10", "1"))
route_local("SK_N1", get_pos("R10", "2"), get_pos("R11", "1"))
route_local("SK_N1", get_pos("R10", "2"), get_pos("C3", "1"))
route_local("OPAMP_P", get_pos("U1", "7"), get_pos("R11", "2"))
route_local("OPAMP_P", get_pos("R11", "2"), get_pos("C4", "1"))
route_local("OPAMP_N", get_pos("U1", "9"), get_pos("R12", "1"))
route_local("OPAMP_N", get_pos("R12", "1"), get_pos("R13", "1"))
route_local("ECG_OUT", get_pos("U1", "10"), get_pos("C3", "2"))
route_local("ECG_OUT", get_pos("C3", "2"), get_pos("R13", "2"))
route_local("ECG_OUT", get_pos("R13", "2"), get_pos("R16", "1"))
route_local("ECG_OUT", get_pos("R13", "2"), get_pos("TP1", "1"))

# 7. Anti-aliasing
route_local("AIN0_FILT", get_pos("R16", "2"), get_pos("C7", "1"))
route_local("AIN0_FILT", get_pos("C7", "1"), get_pos("C8", "1"))
route_local("AIN0_FILT", get_pos("C7", "1"), get_pos("U2", "4"))
route_local("AIN1_FILT", get_pos("R17", "2"), get_pos("C7", "2"))
route_local("AIN1_FILT", get_pos("C7", "2"), get_pos("C9", "1"))
route_local("AIN1_FILT", get_pos("C7", "2"), get_pos("U2", "5"))

# 8. Digital Cross-Board Routes using Dedicated Trunk Y Corridors on B.Cu
# I2C SCL: trunk at Y = 18.0 mm
route_local("I2C_SCL", get_pos("U2", "10"), get_pos("R19", "2"))
route_local("I2C_SCL", get_pos("R19", "2"), get_pos("J3", "2"))
route_corridor("I2C_SCL", get_pos("J3", "2"), get_pos("J2B", "3"), trunk_y=18.0)

# I2C SDA: trunk at Y = 21.0 mm
route_local("I2C_SDA", get_pos("U2", "9"), get_pos("R18", "2"))
route_local("I2C_SDA", get_pos("R18", "2"), get_pos("J3", "3"))
route_corridor("I2C_SDA", get_pos("J3", "3"), get_pos("J2B", "6"), trunk_y=21.0)

# MAX INT: trunk at Y = 24.0 mm
route_corridor("MAX_INT", get_pos("J3", "4"), get_pos("J2A", "10"), trunk_y=24.0)

# ADS ALERT: trunk at Y = 41.4 mm
route_local("ADS_ALERT", get_pos("U2", "2"), get_pos("R20", "2"))
route_local("ADS_ALERT", get_pos("R20", "2"), get_pos("J2A", "11"))

# LOD+: trunk at Y = 68.0 mm
route_local("LOD+", get_pos("U1", "12"), get_pos("TP3", "1"))
route_corridor("LOD+", get_pos("TP3", "1"), get_pos("J2A", "7"), trunk_y=68.0)

# LOD-: trunk at Y = 70.0 mm
route_local("LOD-", get_pos("U1", "11"), get_pos("TP4", "1"))
route_corridor("LOD-", get_pos("TP4", "1"), get_pos("J2A", "8"), trunk_y=70.0)

# FR: trunk at Y = 72.0 mm
route_corridor("FR", get_pos("U1", "15"), get_pos("J2A", "9"), trunk_y=72.0)

# ECG_OUT to J2A.5: trunk at Y = 66.0 mm
route_corridor("ECG_OUT", get_pos("TP1", "1"), get_pos("J2A", "5"), trunk_y=66.0)

# Power Rails
# +VS_A
route_local("+VS_A", get_pos("U3", "2"), get_pos("C12", "1"), 0.5)
route_local("+VS_A", get_pos("C12", "1"), get_pos("C13", "1"), 0.5)
route_local("+VS_A", get_pos("C12", "1"), get_pos("C14", "1"), 0.5)
route_local("+VS_A", get_pos("C14", "1"), get_pos("C15", "1"), 0.5)
route_local("+VS_A", get_pos("C14", "1"), get_pos("U1", "17"), 0.5)
route_local("+VS_A", get_pos("U1", "17"), get_pos("U1", "13"), 0.3)
route_local("+VS_A", get_pos("U1", "17"), get_pos("R8", "1"), 0.3)
route_local("+VS_A", get_pos("R8", "1"), get_pos("R5", "1"), 0.3)
route_local("+VS_A", get_pos("R5", "1"), get_pos("R6", "1"), 0.3)
route_local("+VS_A", get_pos("U3", "2"), get_pos("TP5", "1"), 0.3)

# +3V3
route_local("+3V3", get_pos("J2A", "1"), get_pos("J3", "1"), 0.6)
route_local("+3V3", get_pos("J3", "1"), get_pos("R18", "1"), 0.4)
route_local("+3V3", get_pos("R18", "1"), get_pos("R19", "1"), 0.4)
route_local("+3V3", get_pos("R19", "1"), get_pos("R20", "1"), 0.4)
route_local("+3V3", get_pos("R18", "1"), get_pos("U2", "8"), 0.4)
route_local("+3V3", get_pos("U2", "8"), get_pos("C16", "1"), 0.4)
route_local("+3V3", get_pos("C16", "1"), get_pos("C17", "1"), 0.4)
route_corridor("+3V3", get_pos("C16", "1"), get_pos("U3", "3"), trunk_y=14.0, w_mm=0.6)
route_local("+3V3", get_pos("U3", "3"), get_pos("C10", "1"), 0.5)
route_local("+3V3", get_pos("C10", "1"), get_pos("C11", "1"), 0.5)
route_local("+3V3", get_pos("U3", "3"), get_pos("TP6", "1"), 0.3)

# Ground Vias for all SMD GND pads to B.Cu GND plane
gnd_net = board_nets["GND"]
for ref, pad_num in NET_MAP["GND"]:
    pad = fps[ref].FindPadByNumber(pad_num)
    if pad and pad.GetAttribute() == pcbnew.PAD_ATTRIB_SMD:
        p = pad.GetPosition()
        # Drop via 1.2mm away in open direction
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

filler = pcbnew.ZONE_FILLER(board)
filler.Fill(board.Zones())

out_file = "AFE_ECG_PPG_PTT.kicad_pcb"
pcbnew.SaveBoard(out_file, board)
print("Saved routed board to", out_file)
