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

# Board Outline: 17.5 mm x 28.0 mm (W x H)
# Center X = 8.75 mm
CX = 8.75
fps = {}

# 1. J1: USB-C connector at top edge
# Centered at CX, rotated 180 deg so receptacle opening faces TOP (Y=0)
# Mounting shield tabs are at top, signal pins are further down inside the board
fps["J1"] = add_fp("J1", "USB-C", FP_LIB, "USB_C_Receptacle_HRO_TYPE-C-31-M-12", CX, 3.8, 180)

# 2. CC1 & CC2 Pull-down resistors (5.1k 0805)
fps["R1"] = add_fp("R1", "5.1k", SMD_R[0], SMD_R[1], 4.2, 7.8, 0)
fps["R2"] = add_fp("R2", "5.1k", SMD_R[0], SMD_R[1], 13.3, 7.8, 0)

# 3. Input Capacitors C1 (10uF) & C2 (100nF)
fps["C1"] = add_fp("C1", "10uF", SMD_C[0], SMD_C[1], 2.2, 10.8, 90)
fps["C2"] = add_fp("C2", "100nF", SMD_C[0], SMD_C[1], 2.2, 13.5, 90)

# 4. Status LEDs (CHRG / FULL) & Current Limiting Resistors on Top Right
fps["R4"] = add_fp("R4", "1k", SMD_R[0], SMD_R[1], 15.3, 10.8, 90)
fps["D1"] = add_fp("D1", "RED", SMD_LED[0], SMD_LED[1], 15.3, 13.0, 90)

fps["R5"] = add_fp("R5", "1k", SMD_R[0], SMD_R[1], 15.3, 15.5, 90)
fps["D2"] = add_fp("D2", "GREEN", SMD_LED[0], SMD_LED[1], 15.3, 17.7, 90)

# 5. U1: TP4056 IC at the exact center
fps["U1"] = add_fp("U1", "TP4056", FP_LIB, "SOIC-8-1EP_3.9x4.9mm_P1.27mm_EP2.29x3.0mm", CX, 13.2, 0)

# 6. RPROG (R3, 1.2k) next to TP4056 Pin 2
fps["R3"] = add_fp("R3", "1.2k", SMD_R[0], SMD_R[1], 2.2, 16.5, 90)

# 7. Output Filter Capacitor C3 (10uF)
fps["C3"] = add_fp("C3", "10uF", SMD_C[0], SMD_C[1], CX, 18.2, 0)

# 8. Protection Section: DW01A (U2) + FS8205A (Q1)
fps["U2"] = add_fp("U2", "DW01A", FP_LIB, "SOT-23-6", 4.2, 21.8, 0)
fps["R6"] = add_fp("R6", "100", SMD_R[0], SMD_R[1], 2.2, 20.0, 90)
fps["C4"] = add_fp("C4", "100nF", SMD_C[0], SMD_C[1], 2.2, 23.0, 90)
fps["R7"] = add_fp("R7", "1k", SMD_R[0], SMD_R[1], 4.2, 24.8, 0)

# FS8205A Dual N-MOSFET (Q1)
fps["Q1"] = add_fp("Q1", "FS8205A", FP_LIB, "TSSOP-8_4.4x3mm_P0.65mm", 12.5, 22.0, 0)

# 9. J2: Battery Connector at bottom edge
fps["J2"] = add_fp("J2", "BATT", FP_LIB, "JST_PH_B2B-PH-SM4-TB", CX, 26.2, 0)

# Net assignments
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
# 1. VBUS Track from J1 pins to C1, C2 and U1 Pin 4/8
add_track("VBUS", pcbnew.F_Cu, W_PWR, CX-0.75, 7.8, 2.2, 10.8-0.95)
add_track("VBUS", pcbnew.F_Cu, W_PWR, 2.2, 10.8-0.95, 2.2, 13.5-0.95)
add_track("VBUS", pcbnew.F_Cu, W_PWR, 2.2, 13.5-0.95, CX-2.7, 13.2+1.905)
# Cross to Pin 8
add_track("VBUS", pcbnew.B_Cu, W_PWR, CX-2.7, 13.2+1.905, CX+2.7, 13.2-1.905)
add_via("VBUS", CX-2.7, 13.2+1.905)
add_via("VBUS", CX+2.7, 13.2-1.905)

# VBUS to R4, R5
add_track("VBUS", pcbnew.F_Cu, W_SIG, CX+0.75, 7.8, 15.3, 10.8-0.95)
add_track("VBUS", pcbnew.F_Cu, W_SIG, 15.3, 10.8-0.95, 15.3, 15.5-0.95)

# 2. CC1 & CC2 Pull-downs
add_track("CC1", pcbnew.F_Cu, W_SIG, CX-2.25, 7.8, 4.2-0.95, 7.8)
add_track("CC2", pcbnew.F_Cu, W_SIG, CX+2.25, 7.8, 13.3+0.95, 7.8)

# 3. PROG R3 -> U1 Pin 2
add_track("PROG", pcbnew.F_Cu, W_SIG, CX-2.7, 13.2-0.635, 2.2, 16.5-0.95)

# 4. LED traces
add_track("NET_R4_D1", pcbnew.F_Cu, W_SIG, 15.3, 10.8+0.95, 15.3, 13.0-0.95)
add_track("CHRG", pcbnew.F_Cu, W_SIG, 15.3, 13.0+0.95, CX+2.7, 13.2-0.635)

add_track("NET_R5_D2", pcbnew.F_Cu, W_SIG, 15.3, 15.5+0.95, 15.3, 17.7-0.95)
add_track("STDBY", pcbnew.F_Cu, W_SIG, 15.3, 17.7+0.95, CX+2.7, 13.2+0.635)

# 5. BAT_OUT
add_track("BAT_OUT", pcbnew.F_Cu, W_BAT, CX+2.7, 13.2+1.905, CX+0.95, 18.2)
add_track("BAT_OUT", pcbnew.F_Cu, W_BAT, CX+0.95, 18.2, CX-1.0, 26.2)
add_track("BAT_OUT", pcbnew.F_Cu, W_SIG, CX-0.95, 18.2, 2.2, 20.0-0.95)

# 6. DW01A Protection
add_track("DW_VCC", pcbnew.F_Cu, W_SIG, 2.2, 20.0+0.95, 4.2+1.3, 21.8)
add_track("DW_VCC", pcbnew.F_Cu, W_SIG, 2.2, 20.0+0.95, 2.2, 23.0-0.95)
add_track("DW_OD", pcbnew.F_Cu, W_SIG, 4.2-1.3, 21.8-0.95, 12.5-2.8, 22.0+0.975)
add_track("DW_OC", pcbnew.F_Cu, W_SIG, 4.2-1.3, 21.8+0.95, 12.5+2.8, 22.0+0.975)
add_track("DW_CS", pcbnew.F_Cu, W_SIG, 4.2-1.3, 21.8, 4.2-0.95, 24.8)

# 7. BAT_MINUS
add_track("BAT_MINUS", pcbnew.F_Cu, W_BAT, 4.2+0.95, 24.8, 12.5-2.8, 22.0+0.325)
add_track("BAT_MINUS", pcbnew.F_Cu, W_BAT, 12.5-2.8, 22.0+0.325, CX+1.0, 26.2)

# 8. FS8205A GND & Drain
add_track("GND", pcbnew.F_Cu, W_BAT, 12.5-2.8, 22.0-0.325, CX, 22.0)
add_via("GND", CX, 22.0)

add_track("DW_D12", pcbnew.F_Cu, W_BAT, 12.5-2.8, 22.0-0.975, 12.5+2.8, 22.0-0.975)
add_track("DW_D12", pcbnew.F_Cu, W_BAT, 12.5+2.8, 22.0-0.975, 12.5+2.8, 22.0+0.325)

# Copper Pour Zones
def add_copper_zone(layer):
    poly = pcbnew.SHAPE_LINE_CHAIN()
    poly.Append(pcbnew.VECTOR2I(pcbnew.FromMM(0.2), pcbnew.FromMM(0.2)))
    poly.Append(pcbnew.VECTOR2I(pcbnew.FromMM(17.3), pcbnew.FromMM(0.2)))
    poly.Append(pcbnew.VECTOR2I(pcbnew.FromMM(17.3), pcbnew.FromMM(27.8)))
    poly.Append(pcbnew.VECTOR2I(pcbnew.FromMM(0.2), pcbnew.FromMM(27.8)))
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
pts = [(0,0), (17.5,0), (17.5,28.0), (0,28.0), (0,0)]
for i in range(4):
    seg = pcbnew.PCB_SHAPE(board)
    seg.SetShape(pcbnew.SHAPE_T_SEGMENT)
    seg.SetLayer(pcbnew.Edge_Cuts)
    seg.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(pts[i][0]), pcbnew.FromMM(pts[i][1])))
    seg.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(pts[i+1][0]), pcbnew.FromMM(pts[i+1][1])))
    seg.SetWidth(pcbnew.FromMM(0.15))
    board.Add(seg)

# Clean Silkscreen
def add_silk_text(text, x, y, layer=pcbnew.F_SilkS, size=0.8, thickness=0.15):
    txt = pcbnew.PCB_TEXT(board)
    txt.SetText(text)
    txt.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y)))
    txt.SetLayer(layer)
    txt.SetTextSize(pcbnew.VECTOR2I(pcbnew.FromMM(size), pcbnew.FromMM(size)))
    txt.SetTextThickness(pcbnew.FromMM(thickness))
    board.Add(txt)

add_silk_text("TP4056 1A", CX, 8.8, size=0.7)
add_silk_text("CHRG", 15.3, 11.9, size=0.55)
add_silk_text("FULL", 15.3, 16.6, size=0.55)
add_silk_text("B+", 6.2, 26.2, size=0.8)
add_silk_text("B-", 11.3, 26.2, size=0.8)

add_silk_text("LNT 23207124", CX, 14.0, pcbnew.B_SilkS, size=1.0)

pcbnew.SaveBoard("/mnt/Windows/HK3-25-26/KhoaHe_PCB/DoAn/USB_TypeC_TP4056_Charger/USB_TypeC_TP4056_Charger.kicad_pcb", board)
print("PCB V4 Generated!")
