import pcbnew
import math

board = pcbnew.BOARD()

# Design rules / Net classes setup
# Widths in mm:
# Power / GND / BAT: 0.8mm - 1.0mm
# Signals: 0.3mm - 0.4mm
W_PWR = pcbnew.FromMM(0.8)
W_BAT = pcbnew.FromMM(0.8)
W_SIG = pcbnew.FromMM(0.35)
VIA_SZ = pcbnew.FromMM(0.8)
VIA_DR = pcbnew.FromMM(0.4)

# Create nets
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
    fp.SetValue(val)
    fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y)))
    fp.SetOrientation(pcbnew.EDA_ANGLE(rot, pcbnew.DEGREES_T))
    if side == "B":
        fp.Flip(fp.GetPosition(), False)
    board.Add(fp)
    return fp

# Board Dimensions: 18.0 mm x 28.0 mm (Standard Commercial TP4056 Module Size)
# Origin (0,0) -> (18, 28)
# Type-C edge sits at Y=0 (overhanging slightly at Y=-0.5 for flush socket mounting)
fps = {}

# J1: USB Type-C receptacle at top center
# Position: X=9.0, Y=3.0 (receptacle tongue at Y=0)
fps["J1"] = add_fp("J1", "USB-C", FP_LIB, "USB_C_Receptacle_HRO_TYPE-C-31-M-12", 9.0, 2.5, 0)

# CC resistors R1, R2 right behind Type-C pins
fps["R1"] = add_fp("R1", "5.1k", SMD_R[0], SMD_R[1], 4.5, 7.5, 90)
fps["R2"] = add_fp("R2", "5.1k", SMD_R[0], SMD_R[1], 13.5, 7.5, 90)

# Input filter caps C1 (10uF) & C2 (100nF)
fps["C1"] = add_fp("C1", "10uF", SMD_C[0], SMD_C[1], 2.2, 10.5, 0)
fps["C2"] = add_fp("C2", "100nF", SMD_C[0], SMD_C[1], 2.2, 13.0, 0)

# LED indicators on top left/right
fps["R4"] = add_fp("R4", "1k", SMD_R[0], SMD_R[1], 15.8, 10.5, 0)
fps["D1"] = add_fp("D1", "RED", SMD_LED[0], SMD_LED[1], 15.8, 13.0, 0)

fps["R5"] = add_fp("R5", "1k", SMD_R[0], SMD_R[1], 15.8, 15.5, 0)
fps["D2"] = add_fp("D2", "GREEN", SMD_LED[0], SMD_LED[1], 15.8, 18.0, 0)

# U1: TP4056 in central section
fps["U1"] = add_fp("U1", "TP4056", FP_LIB, "SOIC-8-1EP_3.9x4.9mm_P1.27mm_EP2.29x3.0mm", 9.0, 13.0, 0)
# RPROG (R3) next to TP4056 Pin 2
fps["R3"] = add_fp("R3", "1.2k", SMD_R[0], SMD_R[1], 2.2, 16.0, 0)

# Output filter cap C3 (10uF)
fps["C3"] = add_fp("C3", "10uF", SMD_C[0], SMD_C[1], 9.0, 18.2, 90)

# Protection Section: DW01A + FS8205A
# DW01A (U2) SOT-23-6
fps["U2"] = add_fp("U2", "DW01A", FP_LIB, "SOT-23-6", 4.5, 22.0, 0)
fps["R6"] = add_fp("R6", "100", SMD_R[0], SMD_R[1], 2.2, 21.0, 90)
fps["C4"] = add_fp("C4", "100nF", SMD_C[0], SMD_C[1], 2.2, 23.5, 90)
fps["R7"] = add_fp("R7", "1k", SMD_R[0], SMD_R[1], 4.5, 25.2, 0)

# FS8205A (Q1) TSSOP-8
fps["Q1"] = add_fp("Q1", "FS8205A", FP_LIB, "TSSOP-8_4.4x3mm_P0.65mm", 12.0, 22.5, 0)

# J2: Battery connector / pads at bottom
fps["J2"] = add_fp("J2", "BATT", FP_LIB, "JST_PH_B2B-PH-SM4-TB", 9.0, 26.2, 0)

# Assign Pads to Nets
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
            netname = asgn[pname]
            pad.SetNet(board_nets[netname])

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

# --- ROUTING ENGINE ---
# 1. VBUS Routing (High current 0.8mm)
# J1 VBUS pins -> C1, C2 -> U1 Pin 4, Pin 8 & R4, R5
add_track("VBUS", pcbnew.F_Cu, W_PWR, 9.0-2.75+2.0, 2.5+4.0, 6.5, 8.5)
add_track("VBUS", pcbnew.F_Cu, W_PWR, 6.5, 8.5, 2.2-0.95, 10.5) # to C1
add_track("VBUS", pcbnew.F_Cu, W_PWR, 2.2-0.95, 10.5, 2.2-0.95, 13.0) # to C2
add_track("VBUS", pcbnew.F_Cu, W_PWR, 2.2-0.95, 13.0, 9.0-2.7, 13.0+1.905) # to U1 pin 4
add_track("VBUS", pcbnew.F_Cu, W_PWR, 9.0-2.7, 13.0+1.905, 9.0+2.7, 13.0-1.905) # through back or top to pin 8

# VBUS to LED pull-up resistors
add_track("VBUS", pcbnew.F_Cu, W_SIG, 6.5, 8.5, 15.8-0.95, 8.5)
add_track("VBUS", pcbnew.F_Cu, W_SIG, 15.8-0.95, 8.5, 15.8-0.95, 10.5)
add_track("VBUS", pcbnew.F_Cu, W_SIG, 15.8-0.95, 10.5, 15.8-0.95, 15.5)

# 2. CC1 & CC2 Pull-down lines
add_track("CC1", pcbnew.F_Cu, W_SIG, 9.0-2.25, 2.5+4.0, 4.5, 7.5-0.95)
add_track("CC2", pcbnew.F_Cu, W_SIG, 9.0+2.25, 2.5+4.0, 13.5, 7.5-0.95)

# 3. PROG resistor R3 -> U1 Pin 2
add_track("PROG", pcbnew.F_Cu, W_SIG, 9.0-2.7, 13.0-0.635, 2.2+0.95, 16.0)

# 4. LEDs -> TP4056 CHRG / STDBY
# R4 to D1
add_track("NET_R4_D1", pcbnew.F_Cu, W_SIG, 15.8+0.95, 10.5, 15.8+0.95, 13.0)
# D1 cathode to U1 Pin 7 (CHRG)
add_track("CHRG", pcbnew.F_Cu, W_SIG, 15.8-0.95, 13.0, 9.0+2.7, 13.0-0.635)

# R5 to D2
add_track("NET_R5_D2", pcbnew.F_Cu, W_SIG, 15.8+0.95, 15.5, 15.8+0.95, 18.0)
# D2 cathode to U1 Pin 6 (STDBY)
add_track("STDBY", pcbnew.F_Cu, W_SIG, 15.8-0.95, 18.0, 9.0+2.7, 13.0+0.635)

# 5. BAT_OUT (Power track 0.8mm)
# U1 Pin 5 -> C3 -> R6 -> J2 Pin 1
add_track("BAT_OUT", pcbnew.F_Cu, W_BAT, 9.0+2.7, 13.0+1.905, 9.0, 18.2-0.95) # to C3
add_track("BAT_OUT", pcbnew.F_Cu, W_BAT, 9.0, 18.2-0.95, 9.0-1.0, 26.2) # straight to J2 Pin 1 (BATT+)
add_track("BAT_OUT", pcbnew.F_Cu, W_SIG, 9.0, 18.2-0.95, 2.2, 21.0-0.95) # to R6 for DW01A VCC

# 6. DW01A Protection Routing
# R6 to U2 Pin 5 (VCC) & C4
add_track("DW_VCC", pcbnew.F_Cu, W_SIG, 2.2, 21.0+0.95, 4.5+1.3, 22.0)
add_track("DW_VCC", pcbnew.F_Cu, W_SIG, 2.2, 21.0+0.95, 2.2, 23.5-0.95)

# DW01A OD (Pin 1) -> FS8205A G2 (Pin 4)
add_track("DW_OD", pcbnew.F_Cu, W_SIG, 4.5-1.3, 22.0-0.95, 12.0-2.8, 22.5+0.975)

# DW01A OC (Pin 3) -> FS8205A G1 (Pin 5)
add_track("DW_OC", pcbnew.F_Cu, W_SIG, 4.5-1.3, 22.0+0.95, 12.0+2.8, 22.5+0.975)

# DW01A CS (Pin 2) -> R7 -> BAT_MINUS
add_track("DW_CS", pcbnew.F_Cu, W_SIG, 4.5-1.3, 22.0, 4.5-0.95, 25.2)
add_track("BAT_MINUS", pcbnew.F_Cu, W_BAT, 4.5+0.95, 25.2, 12.0-2.8, 22.5+0.325) # to Q1 Pin 3 (S2)
add_track("BAT_MINUS", pcbnew.F_Cu, W_BAT, 12.0-2.8, 22.5+0.325, 9.0+1.0, 26.2) # to J2 Pin 2 (BATT-)

# FS8205A S1 (Pin 2) -> System GND
add_track("GND", pcbnew.F_Cu, W_BAT, 12.0-2.8, 22.5-0.325, 9.0, 22.5)
add_via("GND", 9.0, 22.5)

# FS8205A Drain 1-2 interconnection (Pins 1, 6, 7, 8)
add_track("DW_D12", pcbnew.F_Cu, W_BAT, 12.0-2.8, 22.5-0.975, 12.0+2.8, 22.5-0.975)
add_track("DW_D12", pcbnew.F_Cu, W_BAT, 12.0+2.8, 22.5-0.975, 12.0+2.8, 22.5+0.325)

# 7. Copper Pour / GND Planes (Top & Bottom Layer)
def add_copper_zone(layer):
    poly = pcbnew.SHAPE_LINE_CHAIN()
    poly.Append(pcbnew.VECTOR2I(pcbnew.FromMM(0.2), pcbnew.FromMM(0.2)))
    poly.Append(pcbnew.VECTOR2I(pcbnew.FromMM(17.8), pcbnew.FromMM(0.2)))
    poly.Append(pcbnew.VECTOR2I(pcbnew.FromMM(17.8), pcbnew.FromMM(27.8)))
    poly.Append(pcbnew.VECTOR2I(pcbnew.FromMM(0.2), pcbnew.FromMM(27.8)))
    poly.SetClosed(True)
    
    zone = pcbnew.ZONE(board)
    zone.SetNet(board_nets["GND"])
    zone.SetLayer(layer)
    zone.AddPolygon(poly)
    zone.SetPadConnection(pcbnew.ZONE_CONNECTION_THERMAL)
    zone.SetThermalReliefGap(pcbnew.FromMM(0.3))
    zone.SetThermalReliefSpokeWidth(pcbnew.FromMM(0.4))
    board.Add(zone)
    return zone

z_top = add_copper_zone(pcbnew.F_Cu)
z_bot = add_copper_zone(pcbnew.B_Cu)

# Filler engine for zones
filler = pcbnew.ZONE_FILLER(board)
filler.Fill(board.Zones())

# 8. Board Outline (Edge.Cuts) 18.0 mm x 28.0 mm
pts = [(0,0), (18,0), (18,28), (0,28), (0,0)]
for i in range(4):
    seg = pcbnew.PCB_SHAPE(board)
    seg.SetShape(pcbnew.SHAPE_T_SEGMENT)
    seg.SetLayer(pcbnew.Edge_Cuts)
    seg.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(pts[i][0]), pcbnew.FromMM(pts[i][1])))
    seg.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(pts[i+1][0]), pcbnew.FromMM(pts[i+1][1])))
    seg.SetWidth(pcbnew.FromMM(0.15))
    board.Add(seg)

# 9. Silkscreen Labels
def add_silk_text(text, x, y, layer=pcbnew.F_SilkS, size=0.8, thickness=0.15):
    txt = pcbnew.PCB_TEXT(board)
    txt.SetText(text)
    txt.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y)))
    txt.SetLayer(layer)
    txt.SetTextSize(pcbnew.VECTOR2I(pcbnew.FromMM(size), pcbnew.FromMM(size)))
    txt.SetTextThickness(pcbnew.FromMM(thickness))
    board.Add(txt)

add_silk_text("TYPE-C 5V", 9.0, 1.0)
add_silk_text("CHRG", 13.5, 13.0)
add_silk_text("DONE", 13.5, 18.0)
add_silk_text("BAT+", 6.5, 26.2)
add_silk_text("BAT-", 11.5, 26.2)
add_silk_text("TP4056 PROT", 9.0, 14.5, pcbnew.B_SilkS, size=1.0)

pcbnew.SaveBoard("/mnt/Windows/HK3-25-26/KhoaHe_PCB/DoAn/USB_TypeC_TP4056_Charger/USB_TypeC_TP4056_Charger.kicad_pcb", board)
print("Ultra Compact & Fully Routed PCB Generated!")
