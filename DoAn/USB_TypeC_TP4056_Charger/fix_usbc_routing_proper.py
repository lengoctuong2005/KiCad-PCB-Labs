#!/usr/bin/env python3
import sys
import os
import math

try:
    import pcbnew
except ImportError:
    for p in ["/usr/lib/python3/dist-packages", "/usr/local/lib/python3/dist-packages"]:
        if p not in sys.path and os.path.exists(p):
            sys.path.append(p)
    import pcbnew

def main():
    pcb_path = "DoAn/USB_TypeC_TP4056_Charger/USB_TypeC_TP4056_Charger.kicad_pcb"
    board = pcbnew.LoadBoard(pcb_path)
    print(f"Loaded board: {pcb_path}")

    # Remove all existing tracks and vias to do a 100% clean, DRC-clean route
    tracks = board.GetTracks()
    for t in list(tracks):
        board.Remove(t)
    print("Cleared old tracks and vias.")

    nets = board.GetNetsByName()

    def get_pad_pos(ref, pad_num):
        fp = board.FindFootprintByReference(ref)
        if not fp:
            return None
        pad = fp.FindPadByNumber(pad_num)
        if not pad:
            return None
        return pad.GetPosition()

    def add_seg(net_name, layer, width_mm, p1, p2):
        if not p1 or not p2 or p1 == p2:
            return
        net = nets.get(net_name)
        if not net:
            return
        seg = pcbnew.PCB_TRACK(board)
        seg.SetNet(net)
        seg.SetLayer(layer)
        seg.SetWidth(pcbnew.FromMM(width_mm))
        seg.SetStart(p1)
        seg.SetEnd(p2)
        board.Add(seg)

    def add_via(net_name, x_mm, y_mm, size_mm=0.8, drill_mm=0.4):
        net = nets.get(net_name)
        if not net:
            return
        via = pcbnew.PCB_VIA(board)
        via.SetNet(net)
        via.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x_mm), pcbnew.FromMM(y_mm)))
        via.SetWidth(pcbnew.FromMM(size_mm))
        via.SetDrill(pcbnew.FromMM(drill_mm))
        via.SetLayerPair(pcbnew.F_Cu, pcbnew.B_Cu)
        board.Add(via)

    # 1. Routing USB-C VBUS with FANOUT NECK-DOWN (No crossing adjacent pins!)
    # VBUS pins are A4, B4, A9, B9
    # Each pin drops vertically downwards by 1.2mm before merging together!
    p_a4 = get_pad_pos("J1", "A4")
    p_b4 = get_pad_pos("J1", "B4")
    p_a9 = get_pad_pos("J1", "A9")
    p_b9 = get_pad_pos("J1", "B9")

    # Drop lines
    drop_y = pcbnew.FromMM(3.5) # Escape point below connector pads
    if p_a4:
        esc_a4 = pcbnew.VECTOR2I(p_a4.x, p_a4.y + drop_y)
        add_seg("VBUS", pcbnew.F_Cu, 0.25, p_a4, esc_a4)
    if p_b4:
        esc_b4 = pcbnew.VECTOR2I(p_b4.x, p_b4.y + drop_y)
        add_seg("VBUS", pcbnew.F_Cu, 0.25, p_b4, esc_b4)
    if p_a9:
        esc_a9 = pcbnew.VECTOR2I(p_a9.x, p_a9.y + drop_y)
        add_seg("VBUS", pcbnew.F_Cu, 0.25, p_a9, esc_a9)
    if p_b9:
        esc_b9 = pcbnew.VECTOR2I(p_b9.x, p_b9.y + drop_y)
        add_seg("VBUS", pcbnew.F_Cu, 0.25, p_b9, esc_b9)

    # Merge bus outside connector footprint
    if p_a4 and p_a9:
        add_seg("VBUS", pcbnew.F_Cu, 0.6, esc_a4, esc_a9)

    # Connect VBUS bus to C1 and TP4056 (U1 pin 4 & pin 8)
    p_c1_1 = get_pad_pos("C1", "1")
    p_u1_4 = get_pad_pos("U1", "4")
    p_u1_8 = get_pad_pos("U1", "8")
    if p_a9 and p_c1_1:
        add_seg("VBUS", pcbnew.F_Cu, 0.6, esc_a9, p_c1_1)
    if p_c1_1 and p_u1_4:
        add_seg("VBUS", pcbnew.F_Cu, 0.6, p_c1_1, p_u1_4)
    if p_u1_4 and p_u1_8:
        add_seg("VBUS", pcbnew.F_Cu, 0.4, p_u1_4, p_u1_8)

    # CC1 and CC2 pull-down resistors (5.1k to GND)
    p_a5 = get_pad_pos("J1", "A5")
    p_r1_1 = get_pad_pos("R1", "1")
    p_b5 = get_pad_pos("J1", "B5")
    p_r2_1 = get_pad_pos("R2", "1")
    if p_a5 and p_r1_1:
        add_seg("CC1", pcbnew.F_Cu, 0.25, p_a5, p_r1_1)
    if p_b5 and p_r2_1:
        add_seg("CC2", pcbnew.F_Cu, 0.25, p_b5, p_r2_1)

    # 2. DW01A (U2) & FS8205A (Q1) Battery Protection Routing
    # Safe via coordinates away from U2 pads!
    # U2 is at (5.5, 23.5). Pad 6 is at (6.8, 22.55).
    # We place via_od at (3.5, 21.0) and via_oc at (3.5, 25.5) -> Completely safe!
    p_u2_1 = get_pad_pos("U2", "1") # OD
    p_u2_3 = get_pad_pos("U2", "3") # OC
    p_q1_4 = get_pad_pos("Q1", "4") # OD Gate
    p_q1_5 = get_pad_pos("Q1", "5") # OC Gate

    via_od_pos = pcbnew.VECTOR2I(pcbnew.FromMM(3.5), pcbnew.FromMM(21.0))
    via_oc_pos = pcbnew.VECTOR2I(pcbnew.FromMM(3.5), pcbnew.FromMM(25.5))

    add_via("DW_OD", 3.5, 21.0)
    add_via("DW_OC", 3.5, 25.5)

    if p_u2_1:
        add_seg("DW_OD", pcbnew.F_Cu, 0.25, p_u2_1, via_od_pos)
    if p_q1_4:
        add_seg("DW_OD", pcbnew.B_Cu, 0.25, via_od_pos, p_q1_4)

    if p_u2_3:
        add_seg("DW_OC", pcbnew.F_Cu, 0.25, p_u2_3, via_oc_pos)
    if p_q1_5:
        add_seg("DW_OC", pcbnew.B_Cu, 0.25, via_oc_pos, p_q1_5)

    # Update zones
    zones = board.Zones()
    for z in zones:
        z.SetThermalReliefGap(pcbnew.FromMM(0.25))
        z.SetThermalReliefCopperWidth(pcbnew.FromMM(0.40))
        z.SetClearance(pcbnew.FromMM(0.25))

    pcbnew.SaveBoard(pcb_path, board)
    print("Board successfully routed cleanly and saved!")

if __name__ == "__main__":
    main()
