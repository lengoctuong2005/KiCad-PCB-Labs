import pcbnew
from test_netlist_map import NET_MAP

board = pcbnew.BOARD()

ds = board.GetDesignSettings()
ds.SetCustomTrackWidth(pcbnew.FromMM(0.20))
ds.SetCustomTrackWidth(pcbnew.FromMM(0.254))
ds.SetCustomTrackWidth(pcbnew.FromMM(0.5))
ds.SetCustomViaSize(pcbnew.FromMM(0.6))
ds.SetCustomViaDrill(pcbnew.FromMM(0.3))
ds.m_SolderMaskMargin = 0
ds.m_SolderMaskMinWidth = 0
ds.m_TentViasFront = True
ds.m_TentViasBack = True

# Edge Cuts: 100 x 80 mm
poly = pcbnew.PCB_SHAPE(board)
poly.SetShape(pcbnew.SHAPE_T_RECT)
poly.SetStart(pcbnew.VECTOR2I(0, 0))
poly.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(100), pcbnew.FromMM(80)))
poly.SetLayer(pcbnew.Edge_Cuts)
poly.SetWidth(pcbnew.FromMM(0.15))
board.Add(poly)

# Nets
for net_name in NET_MAP.keys():
    board.Add(pcbnew.NETINFO_ITEM(board, net_name))
board_nets = board.GetNetsByName()

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

# Mounting holes
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

# Resistors & Caps
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

# Oriented vertically (rot=90) so power & ground run parallel
add_fp('C14', '0.1uF', 'Capacitor_SMD', 'C_0603_1608Metric', 30, 31, 90)
add_fp('C15', '1uF', 'Capacitor_SMD', 'C_0603_1608Metric', 34, 31, 90)

add_fp('C10', '1uF', 'Capacitor_SMD', 'C_0603_1608Metric', 20, 60, 90)
add_fp('C11', '0.1uF', 'Capacitor_SMD', 'C_0603_1608Metric', 20, 64, 90)
add_fp('C12', '1uF', 'Capacitor_SMD', 'C_0603_1608Metric', 28, 60, 90)
add_fp('C13', '0.1uF', 'Capacitor_SMD', 'C_0603_1608Metric', 28, 64, 90)

add_fp('R16', '1k', 'Resistor_SMD', 'R_0603_1608Metric', 45, 34, 90)
add_fp('R17', '1k', 'Resistor_SMD', 'R_0603_1608Metric', 45, 42, 90)
add_fp('C7', '10nF', 'Capacitor_SMD', 'C_0603_1608Metric', 47, 34, 90)
add_fp('C8', '1nF', 'Capacitor_SMD', 'C_0603_1608Metric', 44, 30, 90)
add_fp('C9', '1nF', 'Capacitor_SMD', 'C_0603_1608Metric', 44, 46, 90)

add_fp('C16', '0.1uF', 'Capacitor_SMD', 'C_0603_1608Metric', 52, 30, 90)
add_fp('C17', '1uF', 'Capacitor_SMD', 'C_0603_1608Metric', 56, 30, 90)

add_fp('R18', '4.7k', 'Resistor_SMD', 'R_0603_1608Metric', 64, 34, 0)
add_fp('R19', '4.7k', 'Resistor_SMD', 'R_0603_1608Metric', 64, 38, 0)
add_fp('R20', '10k', 'Resistor_SMD', 'R_0603_1608Metric', 64, 42, 0)

tp_names = ['ECG_OUT', 'REFOUT', 'LOD+', 'LOD-', '+VS_A', '+3V3', 'GND']
for i in range(1, 8):
    add_fp(f'TP{i}', tp_names[i-1], 'TestPoint', 'TestPoint_Pad_D1.5mm', 32 + (i-1)*5, 72, 0)

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
    v.SetFrontTentingMode(pcbnew.TENTING_MODE_TENTED)
    v.SetBackTentingMode(pcbnew.TENTING_MODE_TENTED)
    board.Add(v)
    return v

# Ground Vias
gnd_net = board_nets["GND"]
gnd_vias = set()
def gnd_drop(ref, pad_num, dx_mm=0.0, dy_mm=1.2):
    pad = fps[ref].FindPadByNumber(pad_num)
    if not pad: return
    p = pad.GetPosition()
    vx = round((p.x / 1e6) + dx_mm, 2)
    vy = round((p.y / 1e6) + dy_mm, 2)
    if (vx, vy) in gnd_vias: return
    gnd_vias.add((vx, vy))
    add_via("GND", (vx, vy))
    add_track("GND", pcbnew.F_Cu, 0.254, (p.x/1e6, p.y/1e6), (vx, vy))

gnd_drop("U1", "21", 0.0, 0.0)
gnd_drop("U1", "14", -1.2, 0.0)
gnd_drop("U1", "16", 0.0, -1.2)
gnd_drop("U2", "1", -1.2, 0.0)
gnd_drop("U2", "3", -1.2, 0.0)
gnd_drop("U2", "6", 1.2, 0.0)
gnd_drop("U2", "7", 1.2, 0.0)
gnd_drop("U3", "1", -1.2, 0.0)
gnd_drop("R7", "2", 0.0, 1.2)
gnd_drop("R9", "2", 1.2, 0.0)
gnd_drop("C5", "2", 1.2, 0.0)
gnd_drop("C8", "2", 0.0, -1.2)
gnd_drop("C9", "2", 0.0, 1.2)
gnd_drop("C10", "2", 0.0, 1.2)
gnd_drop("C11", "2", 0.0, 1.2)
gnd_drop("C12", "2", 0.0, 1.2)
gnd_drop("C13", "2", 0.0, 1.2)
gnd_drop("C14", "2", 0.0, 1.2)
gnd_drop("C15", "2", 0.0, 1.2)
gnd_drop("C16", "2", 0.0, 1.2)
gnd_drop("C17", "2", 0.0, 1.2)
gnd_drop("TP7", "1", 0.0, -1.5)

# Direct local routes on F.Cu
def route_direct(net, p1, p2, w=0.20):
    add_track(net, pcbnew.F_Cu, w, p1, p2)

route_direct("RA_RAW", get_pos("J1", "T"), get_pos("J1A", "1"))
route_direct("RA_RAW", get_pos("J1A", "1"), get_pos("R1", "1"))
route_direct("RA_INT", get_pos("R1", "2"), get_pos("R3", "1"))
route_direct("RA_FILT", get_pos("R3", "2"), get_pos("R5", "2"))
route_direct("RA_FILT", get_pos("R5", "2"), get_pos("U1", "2"))

route_direct("LA_RAW", get_pos("J1", "R"), get_pos("J1A", "2"))
route_direct("LA_RAW", get_pos("J1A", "2"), get_pos("R2", "1"))
route_direct("LA_INT", get_pos("R2", "2"), get_pos("R4", "1"))
route_direct("LA_FILT", get_pos("R4", "2"), get_pos("R6", "2"))
route_direct("LA_FILT", get_pos("R6", "2"), get_pos("U1", "3"))

route_direct("RL_RAW", get_pos("J1", "S"), get_pos("J1A", "3"))
route_direct("RL_RAW", get_pos("J1A", "3"), get_pos("R15", "2"))
route_direct("RLD_OUT", get_pos("R15", "1"), get_pos("C6", "2"))
route_direct("RLD_OUT", get_pos("C6", "2"), get_pos("R14", "2"))
route_direct("RLD_OUT", get_pos("C6", "2"), get_pos("U1", "5"))

route_direct("RLDFB", get_pos("U1", "4"), get_pos("C6", "1"))
route_direct("RLDFB", get_pos("C6", "1"), get_pos("R14", "1"))

route_direct("HPDRIVE", get_pos("U1", "1"), get_pos("C1", "1"))
route_direct("HP_MID", get_pos("C1", "2"), get_pos("C2", "1"))
route_direct("HP_MID", get_pos("C2", "1"), get_pos("U1", "6"))
route_direct("HP_MID", get_pos("C2", "1"), get_pos("R7", "1"))
route_direct("HPSENSE", get_pos("C2", "2"), get_pos("U1", "20"))

route_direct("REFIN", get_pos("R8", "2"), get_pos("R9", "1"))
route_direct("REFIN", get_pos("R9", "1"), get_pos("C5", "1"))
route_direct("REFIN", get_pos("R8", "2"), get_pos("U1", "18"))

route_direct("REFOUT", get_pos("U1", "8"), get_pos("C4", "2"))
route_direct("REFOUT", get_pos("C4", "2"), get_pos("R12", "2"))
route_direct("REFOUT", get_pos("C4", "2"), get_pos("R17", "1"))
route_direct("REFOUT", get_pos("R12", "2"), get_pos("TP2", "1"))

route_direct("IAOUT", get_pos("U1", "19"), get_pos("R10", "1"))
route_direct("SK_N1", get_pos("R10", "2"), get_pos("R11", "1"))
route_direct("SK_N1", get_pos("R10", "2"), get_pos("C3", "1"))
route_direct("OPAMP_P", get_pos("U1", "7"), get_pos("R11", "2"))
route_direct("OPAMP_P", get_pos("R11", "2"), get_pos("C4", "1"))
route_direct("OPAMP_N", get_pos("U1", "9"), get_pos("R12", "1"))
route_direct("OPAMP_N", get_pos("R12", "1"), get_pos("R13", "1"))

route_direct("ECG_OUT", get_pos("U1", "10"), get_pos("C3", "2"))
route_direct("ECG_OUT", get_pos("C3", "2"), get_pos("R13", "2"))
route_direct("ECG_OUT", get_pos("R13", "2"), get_pos("R16", "1"))
route_direct("ECG_OUT", get_pos("R13", "2"), get_pos("TP1", "1"))

route_direct("AIN0_FILT", get_pos("R16", "2"), get_pos("C7", "1"))
route_direct("AIN0_FILT", get_pos("C7", "1"), get_pos("C8", "1"))
route_direct("AIN0_FILT", get_pos("C7", "1"), get_pos("U2", "4"))

route_direct("AIN1_FILT", get_pos("R17", "2"), get_pos("C7", "2"))
route_direct("AIN1_FILT", get_pos("C7", "2"), get_pos("C9", "1"))
route_direct("AIN1_FILT", get_pos("C7", "2"), get_pos("U2", "5"))

route_direct("I2C_SDA", get_pos("U2", "9"), get_pos("R18", "2"))
route_direct("I2C_SDA", get_pos("R18", "2"), get_pos("J3", "3"))
route_direct("I2C_SCL", get_pos("U2", "10"), get_pos("R19", "2"))
route_direct("I2C_SCL", get_pos("R19", "2"), get_pos("J3", "2"))
route_direct("ADS_ALERT", get_pos("U2", "2"), get_pos("R20", "2"))
route_direct("ADS_ALERT", get_pos("R20", "2"), get_pos("J2A", "11"))
route_direct("MAX_INT", get_pos("J3", "4"), get_pos("J2A", "10"))

# +VS_A Local Route
route_direct("+VS_A", get_pos("U3", "2"), get_pos("C12", "1"), 0.5)
route_direct("+VS_A", get_pos("C12", "1"), get_pos("C13", "1"), 0.5)
route_direct("+VS_A", get_pos("C12", "1"), get_pos("C14", "1"), 0.5)
route_direct("+VS_A", get_pos("C14", "1"), get_pos("C15", "1"), 0.5)
route_direct("+VS_A", get_pos("C14", "1"), get_pos("U1", "17"), 0.5)
route_direct("+VS_A", get_pos("U1", "17"), get_pos("U1", "13"), 0.3)
route_direct("+VS_A", get_pos("U1", "17"), get_pos("R8", "1"), 0.3)
route_direct("+VS_A", get_pos("R8", "1"), get_pos("R5", "1"), 0.3)
route_direct("+VS_A", get_pos("R5", "1"), get_pos("R6", "1"), 0.3)
route_direct("+VS_A", get_pos("U3", "2"), get_pos("TP5", "1"), 0.3)

# +3V3 Local Route
route_direct("+3V3", get_pos("J2A", "1"), get_pos("J3", "1"), 0.6)
route_direct("+3V3", get_pos("J3", "1"), get_pos("R18", "1"), 0.4)
route_direct("+3V3", get_pos("R18", "1"), get_pos("R19", "1"), 0.4)
route_direct("+3V3", get_pos("R19", "1"), get_pos("R20", "1"), 0.4)
route_direct("+3V3", get_pos("R18", "1"), get_pos("U2", "8"), 0.4)
route_direct("+3V3", get_pos("U2", "8"), get_pos("C16", "1"), 0.4)
route_direct("+3V3", get_pos("C16", "1"), get_pos("C17", "1"), 0.4)

# Pure B.Cu Highway Router (no F.Cu crossing!)
def route_pure_bcu_highway(net_name, p_src, p_dst, trunk_y, w=0.254):
    v1 = (p_src[0] + 1.2, trunk_y)
    v2 = (p_dst[0] - 1.2, trunk_y)
    
    # Via at v1
    add_track(net_name, pcbnew.F_Cu, w, p_src, v1)
    add_via(net_name, v1)
    
    # B.Cu segment
    add_track(net_name, pcbnew.B_Cu, w, v1, v2)
    
    # Via at v2
    add_via(net_name, v2)
    add_track(net_name, pcbnew.F_Cu, w, v2, p_dst)

route_pure_bcu_highway("I2C_SCL", get_pos("J3", "2"), get_pos("J2B", "3"), trunk_y=18.5)
route_pure_bcu_highway("I2C_SDA", get_pos("J3", "3"), get_pos("J2B", "6"), trunk_y=21.5)
route_pure_bcu_highway("ECG_OUT", get_pos("TP1", "1"), get_pos("J2A", "5"), trunk_y=66.0)

route_direct("LOD+", get_pos("U1", "12"), get_pos("TP3", "1"))
route_pure_bcu_highway("LOD+", get_pos("TP3", "1"), get_pos("J2A", "7"), trunk_y=68.5)

route_direct("LOD-", get_pos("U1", "11"), get_pos("TP4", "1"))
route_pure_bcu_highway("LOD-", get_pos("TP4", "1"), get_pos("J2A", "8"), trunk_y=70.5)

route_pure_bcu_highway("FR", get_pos("U1", "15"), get_pos("J2A", "9"), trunk_y=72.5)

# +3V3 from C17 down to U3: route entirely on B.Cu around the edge
v_3v3_src = (get_pos("C17", "1")[0] + 1.5, 30.0)
add_track("+3V3", pcbnew.F_Cu, 0.5, get_pos("C17", "1"), v_3v3_src)
add_via("+3V3", v_3v3_src)

v_3v3_dst = (24.0, 60.0)
add_via("+3V3", v_3v3_dst)
add_track("+3V3", pcbnew.F_Cu, 0.5, v_3v3_dst, get_pos("U3", "3"))

# On B.Cu: go around left/top boundary cleanly
add_track("+3V3", pcbnew.B_Cu, 0.5, v_3v3_src, (v_3v3_src[0], 12.0))
add_track("+3V3", pcbnew.B_Cu, 0.5, (v_3v3_src[0], 12.0), (14.0, 12.0))
add_track("+3V3", pcbnew.B_Cu, 0.5, (14.0, 12.0), (14.0, 60.0))
add_track("+3V3", pcbnew.B_Cu, 0.5, (14.0, 60.0), v_3v3_dst)

route_direct("+3V3", get_pos("U3", "3"), get_pos("C10", "1"), 0.5)
route_direct("+3V3", get_pos("C10", "1"), get_pos("C11", "1"), 0.5)
route_direct("+3V3", get_pos("U3", "3"), get_pos("TP6", "1"), 0.3)

# Solid Ground Plane on B.Cu
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
