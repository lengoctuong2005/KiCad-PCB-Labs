import pcbnew
import math

board = pcbnew.BOARD()

# Add nets
nets = {
    "GND": pcbnew.NETINFO_ITEM(board, "GND"),
    "VBUS": pcbnew.NETINFO_ITEM(board, "VBUS"),
    "BAT_OUT": pcbnew.NETINFO_ITEM(board, "BAT_OUT"),
    "BAT_MINUS": pcbnew.NETINFO_ITEM(board, "BAT_MINUS"),
    "CC1": pcbnew.NETINFO_ITEM(board, "CC1"),
    "CC2": pcbnew.NETINFO_ITEM(board, "CC2"),
    "CHRG": pcbnew.NETINFO_ITEM(board, "CHRG"),
    "STDBY": pcbnew.NETINFO_ITEM(board, "STDBY"),
    "PROG": pcbnew.NETINFO_ITEM(board, "PROG"),
    "DW_VCC": pcbnew.NETINFO_ITEM(board, "DW_VCC"),
    "DW_CS": pcbnew.NETINFO_ITEM(board, "DW_CS"),
    "DW_OD": pcbnew.NETINFO_ITEM(board, "DW_OD"),
    "DW_OC": pcbnew.NETINFO_ITEM(board, "DW_OC")
}

for name, net in nets.items():
    board.Add(net)

def add_fp(ref, val, lib, fp_name, x, y, rot, side):
    fp = pcbnew.FootprintLoad(lib, fp_name)
    fp.SetReference(ref)
    fp.SetValue(val)
    fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y)))
    fp.SetOrientation(pcbnew.EDA_ANGLE(rot, pcbnew.DEGREES_T))
    if side == "B":
        fp.Flip(fp.GetPosition(), False)
    board.Add(fp)
    return fp

FP_LIB = "/mnt/Windows/HK3-25-26/KhoaHe_PCB/DoAn/USB_TypeC_TP4056_Charger/libs/charger.pretty"
SMD_C = "/usr/share/kicad/footprints/Capacitor_SMD.pretty", "C_0805_2012Metric"
SMD_R = "/usr/share/kicad/footprints/Resistor_SMD.pretty", "R_0805_2012Metric"
SMD_LED = "/usr/share/kicad/footprints/LED_SMD.pretty", "LED_0805_2012Metric"

fps = {}
fps["J1"] = add_fp("J1", "USB-C", FP_LIB, "USB_C_Receptacle_HRO_TYPE-C-31-M-12", 12.5, 5, 0, "T")
fps["C1"] = add_fp("C1", "10uF", SMD_C[0], SMD_C[1], 5, 12, 90, "T")
fps["C2"] = add_fp("C2", "100nF", SMD_C[0], SMD_C[1], 8, 12, 90, "T")
fps["R1"] = add_fp("R1", "5.1k", SMD_R[0], SMD_R[1], 15, 12, 90, "T")
fps["R2"] = add_fp("R2", "5.1k", SMD_R[0], SMD_R[1], 18, 12, 90, "T")

fps["U1"] = add_fp("U1", "TP4056", FP_LIB, "SOIC-8-1EP_3.9x4.9mm_P1.27mm_EP2.29x3.0mm", 12.5, 20, 0, "T")
fps["R3"] = add_fp("R3", "1.2k", SMD_R[0], SMD_R[1], 4, 18, 0, "T")
fps["R4"] = add_fp("R4", "1k", SMD_R[0], SMD_R[1], 18, 18, 90, "T")
fps["R5"] = add_fp("R5", "1k", SMD_R[0], SMD_R[1], 21, 18, 90, "T")
fps["D1"] = add_fp("D1", "RED", SMD_LED[0], SMD_LED[1], 18, 22, 90, "T")
fps["D2"] = add_fp("D2", "GREEN", SMD_LED[0], SMD_LED[1], 21, 22, 90, "T")

fps["C3"] = add_fp("C3", "10uF", SMD_C[0], SMD_C[1], 12.5, 27, 90, "T")

fps["U2"] = add_fp("U2", "DW01A", FP_LIB, "SOT-23-6", 7, 34, 0, "T")
fps["R6"] = add_fp("R6", "100", SMD_R[0], SMD_R[1], 4, 34, 90, "T")
fps["C4"] = add_fp("C4", "100nF", SMD_C[0], SMD_C[1], 4, 38, 90, "T")
fps["R7"] = add_fp("R7", "1k", SMD_R[0], SMD_R[1], 10, 38, 90, "T")

fps["Q1"] = add_fp("Q1", "FS8205A", FP_LIB, "TSSOP-8_4.4x3mm_P0.65mm", 18, 36, 0, "T")

fps["J2"] = add_fp("J2", "BATT", FP_LIB, "JST_PH_B2B-PH-SM4-TB", 12.5, 45, 0, "T")

assigns = {
    "J1": {"A1":"GND","A4":"VBUS","A5":"CC1","A9":"VBUS","A12":"GND","B1":"GND","B4":"VBUS","B5":"CC2","B9":"VBUS","B12":"GND", "S1":"GND"},
    "C1": {"1":"VBUS", "2":"GND"},
    "C2": {"1":"VBUS", "2":"GND"},
    "R1": {"1":"CC1", "2":"GND"},
    "R2": {"1":"CC2", "2":"GND"},
    "U1": {"1":"GND", "2":"PROG", "3":"GND", "4":"VBUS", "8":"VBUS", "5":"BAT_OUT", "6":"STDBY", "7":"CHRG", "9":"GND"},
    "R3": {"1":"PROG", "2":"GND"},
    "C3": {"1":"BAT_OUT", "2":"GND"},
    "U2": {"1":"DW_OD", "2":"DW_CS", "3":"DW_OC", "4":"", "5":"DW_VCC", "6":"GND"},
    "R6": {"1":"BAT_OUT", "2":"DW_VCC"},
    "C4": {"1":"DW_VCC", "2":"GND"},
    "R7": {"1":"DW_CS", "2":"BAT_MINUS"},
    "J2": {"1":"BAT_OUT", "2":"BAT_MINUS"}
}

board.Add(pcbnew.NETINFO_ITEM(board, "NET_R4_D1"))
board.Add(pcbnew.NETINFO_ITEM(board, "NET_R5_D2"))
board.Add(pcbnew.NETINFO_ITEM(board, "DW_D12"))

assigns["R4"] = {"1": "VBUS", "2": "NET_R4_D1"}
assigns["D1"] = {"1": "CHRG", "2": "NET_R4_D1"}
assigns["R5"] = {"1": "VBUS", "2": "NET_R5_D2"}
assigns["D2"] = {"1": "STDBY", "2": "NET_R5_D2"}
assigns["Q1"] = {"1":"DW_D12", "6":"DW_D12", "7":"DW_D12", "8":"DW_D12", "2":"GND", "3":"BAT_MINUS", "4":"DW_OD", "5":"DW_OC"}

nets = board.GetNetsByName()
for ref, asgn in assigns.items():
    fp = fps[ref]
    for pad in fp.Pads():
        pname = pad.GetName()
        if pname in asgn and asgn[pname]:
            netname = asgn[pname]
            net = nets[netname]
            pad.SetNet(net)

# Edge Cuts
pts = [(0,0), (25,0), (25,50), (0,50), (0,0)]
for i in range(4):
    seg = pcbnew.PCB_SHAPE(board)
    seg.SetShape(pcbnew.SHAPE_T_SEGMENT)
    seg.SetLayer(pcbnew.Edge_Cuts)
    seg.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(pts[i][0]), pcbnew.FromMM(pts[i][1])))
    seg.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(pts[i+1][0]), pcbnew.FromMM(pts[i+1][1])))
    seg.SetWidth(pcbnew.FromMM(0.1))
    board.Add(seg)

pcbnew.SaveBoard("/mnt/Windows/HK3-25-26/KhoaHe_PCB/DoAn/USB_TypeC_TP4056_Charger/USB_TypeC_TP4056_Charger.kicad_pcb", board)
print("PCB generated!")
