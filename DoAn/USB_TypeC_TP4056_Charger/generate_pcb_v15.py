import pcbnew
import math

board = pcbnew.BOARD()

# Net widths
W_PWR = pcbnew.FromMM(0.8)
W_BAT = pcbnew.FromMM(0.8)
W_SIG = pcbnew.FromMM(0.35)
VIA_SZ = pcbnew.FromMM(0.8)
VIA_DR = pcbnew.FromMM(0.4)

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

CX = 9.0
fps = {}

# 1. J1: USB-C Connector (Rotated 180 deg)
fps["J1"] = add_fp("J1", "USB-C", FP_LIB, "USB_C_Receptacle_HRO_TYPE-C-31-M-12", CX, 4.2, 180)
set_3d(fps["J1"], "/usr/share/kicad/3dmodels/Connector_USB.3dshapes/USB_C_Receptacle_GCT_USB4105-xx-A_16P_TopMnt_Horizontal.step", offset=(0, -1.2, 0), rot=(0, 0, 0))

# 2. CC Resistors R1 & R2
fps["R1"] = add_fp("R1", "5.1k", SMD_R[0], SMD_R[1], 4.5, 7.8, 90)
fps["R2"] = add_fp("R2", "5.1k", SMD_R[0], SMD_R[1], 13.5, 7.8, 90)
set_3d(fps["R1"], "/usr/share/kicad/3dmodels/Resistor_SMD.3dshapes/R_0805_2012Metric.step")
set_3d(fps["R2"], "/usr/share/kicad/3dmodels/Resistor_SMD.3dshapes/R_0805_2012Metric.step")

# 3. Input Capacitors C1 & C2
fps["C1"] = add_fp("C1", "10uF", SMD_C[0], SMD_C[1], 2.4, 11.2, 0)
fps["C2"] = add_fp("C2", "100nF", SMD_C[0], SMD_C[1], 2.4, 13.8, 0)
set_3d(fps["C1"], "/usr/share/kicad/3dmodels/Capacitor_SMD.3dshapes/C_0805_2012Metric.step")
set_3d(fps["C2"], "/usr/share/kicad/3dmodels/Capacitor_SMD.3dshapes/C_0805_2012Metric.step")

# 4. Status LEDs & Resistors (LEDs rotated 90 deg for vertical placement)
fps["R4"] = add_fp("R4", "1k", SMD_R[0], SMD_R[1], 15.6, 11.2, 0)
set_3d(fps["R4"], "/usr/share/kicad/3dmodels/Resistor_SMD.3dshapes/R_0805_2012Metric.step")

fps["D1"] = add_fp("D1", "RED", SMD_LED[0], SMD_LED[1], 15.6, 13.6, 90)
set_3d(fps["D1"], "/usr/share/kicad/3dmodels/LED_SMD.3dshapes/LED_0805_2012Metric_Castellated.step", rot=(0,0,90))

fps["R5"] = add_fp("R5", "1k", SMD_R[0], SMD_R[1], 15.6, 16.2, 0)
set_3d(fps["R5"], "/usr/share/kicad/3dmodels/Resistor_SMD.3dshapes/R_0805_2012Metric.step")

fps["D2"] = add_fp("D2", "GREEN", SMD_LED[0], SMD_LED[1], 15.6, 18.6, 90)
set_3d(fps["D2"], "/usr/share/kicad/3dmodels/LED_SMD.3dshapes/LED_0805_2012Metric_Castellated.step", rot=(0,0,90))

# 5. U1: TP4056 IC at center
fps["U1"] = add_fp("U1", "TP4056", FP_LIB, "SOIC-8-1EP_3.9x4.9mm_P1.27mm_EP2.29x3.0mm", CX, 13.5, 0)
set_3d(fps["U1"], "/usr/share/kicad/3dmodels/Package_SO.3dshapes/SOIC-8-1EP_3.9x4.9mm_P1.27mm_EP2.29x3mm.wrl")

# 6. RPROG (R3)
fps["R3"] = add_fp("R3", "1.2k", SMD_R[0], SMD_R[1], 2.4, 16.8, 0)
set_3d(fps["R3"], "/usr/share/kicad/3dmodels/Resistor_SMD.3dshapes/R_0805_2012Metric.step")

# 7. Output Filter Capacitor C3
fps["C3"] = add_fp("C3", "10uF", SMD_C[0], SMD_C[1], CX, 18.8, 90)
set_3d(fps["C3"], "/usr/share/kicad/3dmodels/Capacitor_SMD.3dshapes/C_0805_2012Metric.step")

# 8. Protection Section: DW01A (U2) & FS8205A (Q1)
fps["U2"] = add_fp("U2", "DW01A", FP_LIB, "SOT-23-6", 5.2, 22.5, 0)
set_3d(fps["U2"], "/usr/share/kicad/3dmodels/Package_TO_SOT_SMD.3dshapes/SOT-23-6.wrl")

fps["R6"] = add_fp("R6", "100", SMD_R[0], SMD_R[1], 2.2, 21.0, 90)
fps["C4"] = add_fp("C4", "100nF", SMD_C[0], SMD_C[1], 2.2, 23.8, 90)
set_3d(fps["R6"], "/usr/share/kicad/3dmodels/Resistor_SMD.3dshapes/R_0805_2012Metric.step")
set_3d(fps["C4"], "/usr/share/kicad/3dmodels/Capacitor_SMD.3dshapes/C_0805_2012Metric.step")

fps["R7"] = add_fp("R7", "1k", SMD_R[0], SMD_R[1], 5.2, 25.4, 0)
set_3d(fps["R7"], "/usr/share/kicad/3dmodels/Resistor_SMD.3dshapes/R_0805_2012Metric.step")

fps["Q1"] = add_fp("Q1", "FS8205A", FP_LIB, "TSSOP-8_4.4x3mm_P0.65mm", 13.0, 23.0, 0)
set_3d(fps["Q1"], "/usr/share/kicad/3dmodels/Package_SO.3dshapes/TSSOP-8_4.4x3mm_P0.65mm.wrl")

# 9. J2: Battery Connector at bottom edge
fps["J2"] = add_fp("J2", "BATT", FP_LIB, "JST_PH_B2B-PH-SM4-TB", CX, 26.6, 0)
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
for ref, asgn in assigns.items():
    fp = fps[ref]
    for pad in fp.Pads():
        pname = pad.GetName()
        if pname in asgn and asgn[pname]:
            pad.SetNet(board_nets[asgn[pname]])

def add_track(net_name, layer, width, x1, y1, x2, y2):
    t = pcbnew.PCB_TRACK(board)
    t.SetNet(board_nets[net_name])
    t.SetLayer(layer)
    t.SetWidth(width)
    t.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(x1), pcbnew.FromMM(y1)))
    t.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(x2), pcbnew.FromMM(y2)))
    board.Add(t)

def add_via(net_name, x, y, size=VIA_SZ, drill=VIA_DR):
    v = pcbnew.PCB_VIA(board)
    v.SetNet(board_nets[net_name])
    v.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y)))
    v.SetWidth(size)
    v.SetDrill(drill)
    board.Add(v)

# Routing
add_track("VBUS", pcbnew.F_Cu, W_PWR, CX-0.75, 8.2, 6.5, 8.5)
add_track("VBUS", pcbnew.F_Cu, W_PWR, 6.5, 8.5, 2.2-0.95, 11.2)
add_track("VBUS", pcbnew.F_Cu, W_PWR, 2.2-0.95, 11.2, 2.2-0.95, 13.8)
add_track("VBUS", pcbnew.F_Cu, W_PWR, 2.2-0.95, 13.8, CX-2.7, 13.5+1.905)

# Cross to Pin 8
add_track("VBUS", pcbnew.B_Cu, W_PWR, CX-2.7, 13.5+1.905, CX+2.7, 13.5-1.905)
add_via("VBUS", CX-2.7, 13.5+1.905)
add_via("VBUS", CX+2.7, 13.5-1.905)

# VBUS to R4, R5
add_track("VBUS", pcbnew.F_Cu, W_SIG, CX+0.75, 8.2, 15.6-0.95, 8.5)
add_track("VBUS", pcbnew.F_Cu, W_SIG, 15.6-0.95, 8.5, 15.6-0.95, 11.2)
add_track("VBUS", pcbnew.F_Cu, W_SIG, 15.6-0.95, 11.2, 15.6-0.95, 16.2)

# CC1 & CC2 Pull-downs
add_track("CC1", pcbnew.F_Cu, W_SIG, CX+2.25, 8.2, 4.5, 7.8-0.95)
add_track("CC2", pcbnew.F_Cu, W_SIG, CX-2.25, 8.2, 13.5, 7.8-0.95)

# PROG R3 -> U1 Pin 2
add_track("PROG", pcbnew.F_Cu, W_SIG, CX-2.7, 13.5-0.635, 2.4+0.95, 16.8)

# LED traces (D1, D2 rotated 90 deg -> pin 1 at y+0.95, pin 2 at y-0.95)
add_track("NET_R4_D1", pcbnew.F_Cu, W_SIG, 15.6+0.95, 11.2, 15.6, 13.6-0.95)
add_track("CHRG", pcbnew.F_Cu, W_SIG, 15.6, 13.6+0.95, CX+2.7, 13.5-0.635)

add_track("NET_R5_D2", pcbnew.F_Cu, W_SIG, 15.6+0.95, 16.2, 15.6, 18.6-0.95)
add_track("STDBY", pcbnew.F_Cu, W_SIG, 15.6, 18.6+0.95, CX+2.7, 13.5+0.635)

# BAT_OUT
add_track("BAT_OUT", pcbnew.F_Cu, W_BAT, CX+2.7, 13.5+1.905, CX, 18.8-0.95)
add_track("BAT_OUT", pcbnew.F_Cu, W_BAT, CX, 18.8-0.95, CX-1.0, 26.6)
add_track("BAT_OUT", pcbnew.F_Cu, W_SIG, CX, 18.8-0.95, 2.2, 21.0-0.95)

# DW01A Protection
add_track("DW_VCC", pcbnew.F_Cu, W_SIG, 2.2, 21.0+0.95, 5.2+1.3, 22.5)
add_track("DW_VCC", pcbnew.F_Cu, W_SIG, 2.2, 21.0+0.95, 2.2, 23.8-0.95)
add_track("DW_OD", pcbnew.F_Cu, W_SIG, 5.2-1.3, 22.5-0.95, 13.0-2.8, 22.5+0.975)
add_track("DW_OC", pcbnew.F_Cu, W_SIG, 5.2-1.3, 22.5+0.95, 13.0+2.8, 22.5+0.975)
add_track("DW_CS", pcbnew.F_Cu, W_SIG, 5.2-1.3, 22.5, 5.2-0.95, 25.4)

# BAT_MINUS
add_track("BAT_MINUS", pcbnew.F_Cu, W_BAT, 5.2+0.95, 25.4, 13.0-2.8, 22.5+0.325)
add_track("BAT_MINUS", pcbnew.F_Cu, W_BAT, 13.0-2.8, 22.5+0.325, CX+1.0, 26.6)

# FS8205A GND & Drain
add_track("GND", pcbnew.F_Cu, W_BAT, 13.0-2.8, 22.5-0.325, CX, 22.5)
add_via("GND", CX, 22.5)

add_track("DW_D12", pcbnew.F_Cu, W_BAT, 13.0-2.8, 22.5-0.975, 13.0+2.8, 22.5-0.975)
add_track("DW_D12", pcbnew.F_Cu, W_BAT, 13.0+2.8, 22.5-0.975, 13.0+2.8, 22.5+0.325)

# Copper Pour Zones
def add_copper_zone(layer):
    poly = pcbnew.SHAPE_LINE_CHAIN()
    poly.Append(pcbnew.VECTOR2I(pcbnew.FromMM(0.2), pcbnew.FromMM(0.2)))
    poly.Append(pcbnew.VECTOR2I(pcbnew.FromMM(17.8), pcbnew.FromMM(0.2)))
    poly.Append(pcbnew.VECTOR2I(pcbnew.FromMM(17.8), pcbnew.FromMM(28.8)))
    poly.Append(pcbnew.VECTOR2I(pcbnew.FromMM(0.2), pcbnew.FromMM(28.8)))
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

# Edge Cuts
pts = [(0,0), (18.0,0), (18.0,29.0), (0,29.0), (0,0)]
for i in range(4):
    seg = pcbnew.PCB_SHAPE(board)
    seg.SetShape(pcbnew.SHAPE_T_SEGMENT)
    seg.SetLayer(pcbnew.Edge_Cuts)
    seg.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(pts[i][0]), pcbnew.FromMM(pts[i][1])))
    seg.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(pts[i+1][0]), pcbnew.FromMM(pts[i+1][1])))
    seg.SetWidth(pcbnew.FromMM(0.15))
    board.Add(seg)

# Silkscreen Helper
def add_silk_text(text, x, y, layer=pcbnew.F_SilkS, size=0.5, thickness=0.1):
    txt = pcbnew.PCB_TEXT(board)
    txt.SetText(text)
    txt.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y)))
    txt.SetLayer(layer)
    txt.SetTextSize(pcbnew.VECTOR2I(pcbnew.FromMM(size), pcbnew.FromMM(size)))
    txt.SetTextThickness(pcbnew.FromMM(thickness))
    if layer == pcbnew.B_SilkS:
        txt.SetMirrored(True)
    board.Add(txt)

# 1. Main Header
add_silk_text("TP4056 1A CHARGER", CX, 9.7, size=0.55, thickness=0.12)

# 2. CC Resistors
add_silk_text("R1", 2.2, 7.8, size=0.45)
add_silk_text("R2", 15.8, 7.8, size=0.45)

# 3. Input Capacitors
add_silk_text("C1", 2.2, 10.0, size=0.45)
add_silk_text("C2", 2.2, 12.6, size=0.45)

# 4. RPROG
add_silk_text("R3", 2.2, 15.6, size=0.45)

# 5. IC TP4056 Label
add_silk_text("U1", CX, 11.2, size=0.5, thickness=0.11)

# 6. LED Section - Clear Designators
add_silk_text("R4", 15.6, 9.8, size=0.45)
add_silk_text("D1:CHRG", 12.0, 13.6, size=0.42)

add_silk_text("R5", 15.6, 15.0, size=0.45)
add_silk_text("D2", 12.6, 18.6, size=0.42)

# 7. Output Filter Capacitor
add_silk_text("C3", CX, 17.5, size=0.45)

# 8. Protection Section
add_silk_text("R6", 2.2, 19.8, size=0.42)
add_silk_text("C4", 2.2, 24.8, size=0.42)
add_silk_text("U2", 5.2, 21.0, size=0.45)
add_silk_text("R7", 5.2, 26.6, size=0.42)
add_silk_text("Q1", 13.0, 21.2, size=0.45)

# 9. Battery Connector & Output Pads
add_silk_text("J2", CX, 25.2, size=0.45)
add_silk_text("B+", 5.8, 27.8, size=0.7, thickness=0.14)
add_silk_text("B-", 12.2, 27.8, size=0.7, thickness=0.14)

# Bottom Layer - Group Branding
add_silk_text("TP4056 USB-C CHARGER", CX, 11.0, pcbnew.B_SilkS, size=0.75, thickness=0.14)
add_silk_text("5V 1A LI-ION MODULE", CX, 15.0, pcbnew.B_SilkS, size=0.65, thickness=0.12)
add_silk_text("HCMUS - 2026", CX, 19.0, pcbnew.B_SilkS, size=0.65, thickness=0.12)

pcbnew.SaveBoard("/mnt/Windows/HK3-25-26/KhoaHe_PCB/DoAn/USB_TypeC_TP4056_Charger/USB_TypeC_TP4056_Charger.kicad_pcb", board)
print("PCB V15 Complete!")
