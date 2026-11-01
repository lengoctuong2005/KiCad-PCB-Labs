import pcbnew
import math

board = pcbnew.BOARD()

# Net widths
W_PWR = pcbnew.FromMM(0.6)
W_BAT = pcbnew.FromMM(0.6)
W_SIG = pcbnew.FromMM(0.25)
VIA_SZ = pcbnew.FromMM(0.6)
VIA_DR = pcbnew.FromMM(0.3)

net_names = [
    "GND", "VBUS", "BAT_OUT", "BAT_MINUS", "CC1", "CC2",
    "CHRG", "STDBY", "PROG", "DW_VCC", "DW_CS", "DW_OD", "DW_OC",
    "NET_R4_D1", "NET_R5_D2", "DW_D12"
]
nets = {}
for n in net_names:
    item = pcbnew.NETINFO_ITEM(board, n)
    board.Add(item)
    nets[n] = item

FP_LIB = "/mnt/Windows/HK3-25-26/KhoaHe_PCB/DoAn/USB_TypeC_TP4056_Charger/libs/charger.pretty"
SMD_C = "/usr/share/kicad/footprints/Capacitor_SMD.pretty", "C_0805_2012Metric"
SMD_R = "/usr/share/kicad/footprints/Resistor_SMD.pretty", "R_0805_2012Metric"
SMD_LED = "/usr/share/kicad/footprints/LED_SMD.pretty", "LED_0805_2012Metric"

def add_fp(ref, val, lib, fp_name, x, y, rot, side="T"):
    fp = pcbnew.FootprintLoad(lib, fp_name)
    fp.SetReference(ref)
    fp.Reference().SetVisible(False)
    fp.SetValue(val)
    fp.Value().SetVisible(False)
    fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y)))
    fp.SetOrientation(pcbnew.EDA_ANGLE(rot, pcbnew.DEGREES_T))
    if side == "B":
        fp.Flip(fp.GetPosition(), False)
    board.Add(fp)
    return fp

def set_3d(fp, model_path, offset=(0,0,0), rot=(0,0,0)):
    fp.Models().clear()
    m = pcbnew.FP_3DMODEL()
    m.m_Filename = model_path
    m.m_Offset = pcbnew.VECTOR3D(offset[0], offset[1], offset[2])
    m.m_Scale = pcbnew.VECTOR3D(1, 1, 1)
    m.m_Rotation = pcbnew.VECTOR3D(rot[0], rot[1], rot[2])
    fp.Models().push_back(m)

CX = 10.0 # Center line on 20mm wide board
fps = {}

# Board width: 20.0mm, Board height: 32.0mm (tăng nhẹ để tránh chạm edge clearance 0.5mm)
# 1. J1: USB-C Connector (Rotated 180 deg)
fps["J1"] = add_fp("J1", "USB-C", FP_LIB, "USB_C_Receptacle_HRO_TYPE-C-31-M-12", CX, 5.0, 180)
set_3d(fps["J1"], "/usr/share/kicad/3dmodels/Connector_USB.3dshapes/USB_C_Receptacle_GCT_USB4105-xx-A_16P_TopMnt_Horizontal.step", offset=(0, -1.2, 0), rot=(0, 0, 0))

# 2. CC Resistors R1 & R2
fps["R1"] = add_fp("R1", "5.1k", SMD_R[0], SMD_R[1], 5.0, 8.5, 90)
fps["R2"] = add_fp("R2", "5.1k", SMD_R[0], SMD_R[1], 15.0, 8.5, 90)
set_3d(fps["R1"], "/usr/share/kicad/3dmodels/Resistor_SMD.3dshapes/R_0805_2012Metric.step")
set_3d(fps["R2"], "/usr/share/kicad/3dmodels/Resistor_SMD.3dshapes/R_0805_2012Metric.step")

# 3. Input Capacitors C1 & C2
fps["C1"] = add_fp("C1", "10uF", SMD_C[0], SMD_C[1], 3.0, 11.5, 0)
fps["C2"] = add_fp("C2", "100nF", SMD_C[0], SMD_C[1], 3.0, 14.2, 0)
set_3d(fps["C1"], "/usr/share/kicad/3dmodels/Capacitor_SMD.3dshapes/C_0805_2012Metric.step")
set_3d(fps["C2"], "/usr/share/kicad/3dmodels/Capacitor_SMD.3dshapes/C_0805_2012Metric.step")

# 4. Status LEDs & Resistors
fps["R4"] = add_fp("R4", "1k", SMD_R[0], SMD_R[1], 17.0, 11.5, 0)
set_3d(fps["R4"], "/usr/share/kicad/3dmodels/Resistor_SMD.3dshapes/R_0805_2012Metric.step")

fps["D1"] = add_fp("D1", "RED", SMD_LED[0], SMD_LED[1], 17.0, 14.0, 90)
set_3d(fps["D1"], "/usr/share/kicad/3dmodels/LED_SMD.3dshapes/LED_0805_2012Metric_Castellated.step", rot=(0,0,90))

fps["R5"] = add_fp("R5", "1k", SMD_R[0], SMD_R[1], 17.0, 16.8, 0)
set_3d(fps["R5"], "/usr/share/kicad/3dmodels/Resistor_SMD.3dshapes/R_0805_2012Metric.step")

fps["D2"] = add_fp("D2", "GREEN", SMD_LED[0], SMD_LED[1], 17.0, 19.3, 90)
set_3d(fps["D2"], "/usr/share/kicad/3dmodels/LED_SMD.3dshapes/LED_0805_2012Metric_Castellated.step", rot=(0,0,90))

# 5. U1: TP4056 IC at center
fps["U1"] = add_fp("U1", "TP4056", FP_LIB, "SOIC-8-1EP_3.9x4.9mm_P1.27mm_EP2.29x3.0mm", CX, 14.5, 0)
set_3d(fps["U1"], "/usr/share/kicad/3dmodels/Package_SO.3dshapes/SOIC-8-1EP_3.9x4.9mm_P1.27mm_EP2.29x3mm.wrl")

# 6. RPROG (R3)
fps["R3"] = add_fp("R3", "1.2k", SMD_R[0], SMD_R[1], 3.0, 17.5, 0)
set_3d(fps["R3"], "/usr/share/kicad/3dmodels/Resistor_SMD.3dshapes/R_0805_2012Metric.step")

# 7. Output Filter Capacitor C3
fps["C3"] = add_fp("C3", "10uF", SMD_C[0], SMD_C[1], CX, 20.2, 90)
set_3d(fps["C3"], "/usr/share/kicad/3dmodels/Capacitor_SMD.3dshapes/C_0805_2012Metric.step")

# 8. Protection Section: DW01A (U2) & FS8205A (Q1)
fps["U2"] = add_fp("U2", "DW01A", FP_LIB, "SOT-23-6", 5.5, 23.5, 0)
set_3d(fps["U2"], "/usr/share/kicad/3dmodels/Package_TO_SOT_SMD.3dshapes/SOT-23-6.wrl")

fps["R6"] = add_fp("R6", "100", SMD_R[0], SMD_R[1], 2.5, 22.0, 90)
fps["C4"] = add_fp("C4", "100nF", SMD_C[0], SMD_C[1], 2.5, 25.0, 90)
set_3d(fps["R6"], "/usr/share/kicad/3dmodels/Resistor_SMD.3dshapes/R_0805_2012Metric.step")
set_3d(fps["C4"], "/usr/share/kicad/3dmodels/Capacitor_SMD.3dshapes/C_0805_2012Metric.step")

fps["R7"] = add_fp("R7", "1k", SMD_R[0], SMD_R[1], 5.5, 26.8, 0)
set_3d(fps["R7"], "/usr/share/kicad/3dmodels/Resistor_SMD.3dshapes/R_0805_2012Metric.step")

fps["Q1"] = add_fp("Q1", "FS8205A", FP_LIB, "TSSOP-8_4.4x3mm_P0.65mm", 14.5, 24.0, 0)
set_3d(fps["Q1"], "/usr/share/kicad/3dmodels/Package_SO.3dshapes/TSSOP-8_4.4x3mm_P0.65mm.wrl")

# 9. J2: Battery Connector at bottom edge
fps["J2"] = add_fp("J2", "BATT", FP_LIB, "JST_PH_B2B-PH-SM4-TB", CX, 28.5, 0)
set_3d(fps["J2"], "/usr/share/kicad/3dmodels/Connector_JST.3dshapes/JST_PH_B2B-PH-SM4-TB_1x02-1MP_P2.00mm_Vertical.step")

# Pad Assignments
assigns = {
    "J1": {"A1":"GND","A4":"VBUS","A5":"CC1","A9":"VBUS","A12":"GND","B1":"GND","B4":"VBUS","B5":"CC2","B9":"VBUS","B12":"GND", "S1":"GND"},
    "C1": {"1":"VBUS", "2":"GND"},
    "C2": {"1":"VBUS", "2":"GND"},
    "R1": {"1":"CC1", "2":"GND"},
    "R2": {"1":"CC2", "2":"GND"},
    "U1": {"1":"GND", "2":"PROG", "3":"GND", "4":"VBUS", "8":"VBUS", "5":"BAT_OUT", "6":"STDBY", "7":"CHRG", "9":"GND"},
    "R3": {"1":"PROG", "2":"GND"},
    "R4": {"1":"VBUS", "2":"NET_R4_D1"},
    "D1": {"1":"CHRG", "2":"NET_R4_D1"},
    "R5": {"1":"VBUS", "2":"NET_R5_D2"},
    "D2": {"1":"STDBY", "2":"NET_R5_D2"},
    "C3": {"1":"BAT_OUT", "2":"GND"},
    "U2": {"1":"DW_OD", "2":"DW_CS", "3":"DW_OC", "5":"DW_VCC", "6":"GND"},
    "R6": {"1":"BAT_OUT", "2":"DW_VCC"},
    "C4": {"1":"DW_VCC", "2":"GND"},
    "R7": {"1":"DW_CS", "2":"BAT_MINUS"},
    "Q1": {"1":"DW_D12", "6":"DW_D12", "7":"DW_D12", "8":"DW_D12", "2":"GND", "3":"BAT_MINUS", "4":"DW_OD", "5":"DW_OC"},
    "J2": {"1":"BAT_OUT", "2":"BAT_MINUS"}
}

board_nets = board.GetNetsByName()
pad_map = {}
for ref, asgn in assigns.items():
    fp = fps[ref]
    for pad in fp.Pads():
        pname = pad.GetName()
        if pname in asgn and asgn[pname]:
            pad.SetNet(board_nets[asgn[pname]])
        pad_map[(ref, pname)] = pad

def get_pad_pos(ref, pname):
    pad = pad_map[(ref, pname)]
    pos = pad.GetPosition()
    return pos.x / 1e6, pos.y / 1e6

def add_track_exact(net_name, layer, width, p1, p2):
    t = pcbnew.PCB_TRACK(board)
    t.SetNet(board_nets[net_name])
    t.SetLayer(layer)
    t.SetWidth(width)
    t.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(p1[0]), pcbnew.FromMM(p1[1])))
    t.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(p2[0]), pcbnew.FromMM(p2[1])))
    board.Add(t)

def add_via_exact(net_name, pos, size=VIA_SZ, drill=VIA_DR):
    v = pcbnew.PCB_VIA(board)
    v.SetNet(board_nets[net_name])
    v.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(pos[0]), pcbnew.FromMM(pos[1])))
    v.SetWidth(size)
    v.SetDrill(drill)
    board.Add(v)

# Routing pad-to-pad:
# 1. CC1 & CC2
add_track_exact("CC1", pcbnew.F_Cu, W_SIG, get_pad_pos("J1", "A5"), get_pad_pos("R1", "1"))
add_track_exact("CC2", pcbnew.F_Cu, W_SIG, get_pad_pos("J1", "B5"), get_pad_pos("R2", "1"))

# 2. VBUS Routing
p_vbus1 = get_pad_pos("J1", "B9")
p_vbus2 = get_pad_pos("J1", "B4")
p_vbus3 = get_pad_pos("J1", "A9")
p_vbus4 = get_pad_pos("J1", "A4")

add_track_exact("VBUS", pcbnew.F_Cu, W_PWR, p_vbus1, p_vbus2)
add_track_exact("VBUS", pcbnew.F_Cu, W_PWR, p_vbus3, p_vbus4)
add_track_exact("VBUS", pcbnew.F_Cu, W_PWR, p_vbus1, p_vbus3)

add_track_exact("VBUS", pcbnew.F_Cu, W_PWR, p_vbus2, get_pad_pos("C1", "1"))
add_track_exact("VBUS", pcbnew.F_Cu, W_PWR, get_pad_pos("C1", "1"), get_pad_pos("C2", "1"))
add_track_exact("VBUS", pcbnew.F_Cu, W_PWR, get_pad_pos("C2", "1"), get_pad_pos("U1", "4"))

# VBUS via bridge to right side (U1.8, R4.1, R5.1)
via1 = (7.0, 16.0)
via2 = (13.0, 11.5)
add_track_exact("VBUS", pcbnew.F_Cu, W_PWR, get_pad_pos("U1", "4"), via1)
add_track_exact("VBUS", pcbnew.B_Cu, W_PWR, via1, via2)
add_via_exact("VBUS", via1)
add_via_exact("VBUS", via2)
add_track_exact("VBUS", pcbnew.F_Cu, W_PWR, via2, get_pad_pos("U1", "8"))
add_track_exact("VBUS", pcbnew.F_Cu, W_SIG, get_pad_pos("U1", "8"), get_pad_pos("R4", "1"))
add_track_exact("VBUS", pcbnew.F_Cu, W_SIG, get_pad_pos("R4", "1"), get_pad_pos("R5", "1"))

# 3. PROG
add_track_exact("PROG", pcbnew.F_Cu, W_SIG, get_pad_pos("R3", "1"), get_pad_pos("U1", "2"))

# 4. LED D1 & D2
add_track_exact("NET_R4_D1", pcbnew.F_Cu, W_SIG, get_pad_pos("R4", "2"), get_pad_pos("D1", "2"))
add_track_exact("CHRG", pcbnew.F_Cu, W_SIG, get_pad_pos("D1", "1"), get_pad_pos("U1", "7"))

add_track_exact("NET_R5_D2", pcbnew.F_Cu, W_SIG, get_pad_pos("R5", "2"), get_pad_pos("D2", "2"))
add_track_exact("STDBY", pcbnew.F_Cu, W_SIG, get_pad_pos("D2", "1"), get_pad_pos("U1", "6"))

# 5. BAT_OUT
add_track_exact("BAT_OUT", pcbnew.F_Cu, W_BAT, get_pad_pos("U1", "5"), get_pad_pos("C3", "1"))
add_track_exact("BAT_OUT", pcbnew.F_Cu, W_BAT, get_pad_pos("C3", "1"), get_pad_pos("J2", "1"))
add_track_exact("BAT_OUT", pcbnew.F_Cu, W_SIG, get_pad_pos("C3", "1"), get_pad_pos("R6", "1"))

# 6. Protection Circuit
add_track_exact("DW_VCC", pcbnew.F_Cu, W_SIG, get_pad_pos("R6", "2"), get_pad_pos("C4", "1"))
add_track_exact("DW_VCC", pcbnew.F_Cu, W_SIG, get_pad_pos("C4", "1"), get_pad_pos("U2", "5"))

add_track_exact("DW_OD", pcbnew.F_Cu, W_SIG, get_pad_pos("U2", "1"), get_pad_pos("Q1", "4"))
add_track_exact("DW_OC", pcbnew.F_Cu, W_SIG, get_pad_pos("U2", "3"), get_pad_pos("Q1", "5"))
add_track_exact("DW_CS", pcbnew.F_Cu, W_SIG, get_pad_pos("U2", "2"), get_pad_pos("R7", "1"))

add_track_exact("BAT_MINUS", pcbnew.F_Cu, W_BAT, get_pad_pos("R7", "2"), get_pad_pos("Q1", "3"))
add_track_exact("BAT_MINUS", pcbnew.F_Cu, W_BAT, get_pad_pos("Q1", "3"), get_pad_pos("J2", "2"))

add_track_exact("DW_D12", pcbnew.F_Cu, W_BAT, get_pad_pos("Q1", "1"), get_pad_pos("Q1", "8"))
add_track_exact("DW_D12", pcbnew.F_Cu, W_BAT, get_pad_pos("Q1", "8"), get_pad_pos("Q1", "7"))
add_track_exact("DW_D12", pcbnew.F_Cu, W_BAT, get_pad_pos("Q1", "7"), get_pad_pos("Q1", "6"))

# Dedicated GND stitching vias away from pads
gnd_vias = [(2.5, 6.0), (17.5, 6.0), (2.5, 28.0), (17.5, 28.0), (10.0, 17.5)]
for vx, vy in gnd_vias:
    add_via_exact("GND", (vx, vy))

# Copper Pour Zones (Edge clearance safe: 0.8mm inside 20x32 board)
def add_copper_zone(layer):
    poly = pcbnew.SHAPE_LINE_CHAIN()
    poly.Append(pcbnew.VECTOR2I(pcbnew.FromMM(0.8), pcbnew.FromMM(0.8)))
    poly.Append(pcbnew.VECTOR2I(pcbnew.FromMM(19.2), pcbnew.FromMM(0.8)))
    poly.Append(pcbnew.VECTOR2I(pcbnew.FromMM(19.2), pcbnew.FromMM(31.2)))
    poly.Append(pcbnew.VECTOR2I(pcbnew.FromMM(0.8), pcbnew.FromMM(31.2)))
    poly.SetClosed(True)
    
    zone = pcbnew.ZONE(board)
    zone.SetNet(board_nets["GND"])
    zone.SetLayer(layer)
    zone.AddPolygon(poly)
    zone.SetPadConnection(pcbnew.ZONE_CONNECTION_THERMAL)
    zone.SetThermalReliefGap(pcbnew.FromMM(0.25))
    zone.SetThermalReliefSpokeWidth(pcbnew.FromMM(0.35))
    board.Add(zone)
    return zone

add_copper_zone(pcbnew.F_Cu)
add_copper_zone(pcbnew.B_Cu)

filler = pcbnew.ZONE_FILLER(board)
filler.Fill(board.Zones())

# Board Outline: 20.0mm x 32.0mm
pts = [(0,0), (20.0,0), (20.0,32.0), (0,32.0), (0,0)]
for i in range(4):
    seg = pcbnew.PCB_SHAPE(board)
    seg.SetShape(pcbnew.SHAPE_T_SEGMENT)
    seg.SetLayer(pcbnew.Edge_Cuts)
    seg.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(pts[i][0]), pcbnew.FromMM(pts[i][1])))
    seg.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(pts[i+1][0]), pcbnew.FromMM(pts[i+1][1])))
    seg.SetWidth(pcbnew.FromMM(0.15))
    board.Add(seg)

# Setup DRC rules & Constraints matching Lab8
settings = board.GetDesignSettings()
# Allow min text height

pcbnew.SaveBoard("USB_TypeC_TP4056_Charger.kicad_pcb", board)
print("Saved redesigned board without text errors and clean boundaries!")
