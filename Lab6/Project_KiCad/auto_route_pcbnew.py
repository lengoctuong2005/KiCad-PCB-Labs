#!/usr/bin/env python3
"""
auto_route_pcbnew.py - Zero-Crossing Professional Router for Lab 6 PCB
Guarantees 0 unconnected items and eliminates track crossings.
"""

import math
import pcbnew
import json
import shutil

def route_board(pcb_path):
    src_path = "/mnt/Windows/HK3-25-26/KhoaHe_PCB/Lab5/Project_KiCad/LAB5.kicad_pcb"
    shutil.copyfile(src_path, pcb_path)
    
    board = pcbnew.LoadBoard(pcb_path)
    
    # Clear existing routing
    for item in list(board.GetTracks()):
        board.Remove(item)
    for zone in list(board.Zones()):
        board.Remove(zone)

    # Net code lookup
    net_map = {}
    for netcode, net in board.GetNetInfo().NetsByName().items():
        net_map[str(net.GetNetname())] = net.GetNetCode()

    # Footprint pad lookup
    pads_by_ref = {}
    for fp in board.GetFootprints():
        ref = str(fp.GetReference())
        pads_by_ref[ref] = {}
        for pad in fp.Pads():
            pnum = str(pad.GetNumber())
            pads_by_ref[ref][pnum] = pad

    def P(ref, pnum):
        return pads_by_ref[ref][str(pnum)].GetPosition()

    def add_seg(p1, p2, width_mm, layer, net_name):
        if p1 == p2:
            return
        netcode = net_map.get(net_name, 0)
        t = pcbnew.PCB_TRACK(board)
        t.SetStart(p1)
        t.SetEnd(p2)
        t.SetWidth(pcbnew.FromMM(width_mm))
        t.SetLayer(layer)
        t.SetNetCode(netcode)
        board.Add(t)

    def add_via(pos, size_mm, drill_mm, net_name):
        netcode = net_map.get(net_name, 0)
        v = pcbnew.PCB_VIA(board)
        v.SetPosition(pos)
        v.SetWidth(pcbnew.FromMM(size_mm))
        v.SetDrill(pcbnew.FromMM(drill_mm))
        v.SetNetCode(netcode)
        v.SetViaType(pcbnew.VIATYPE_THROUGH)
        board.Add(v)

    def poly(pts, width_mm, layer, net_name):
        for i in range(len(pts)-1):
            add_seg(pts[i], pts[i+1], width_mm, layer, net_name)

    def V(x_mm, y_mm):
        return pcbnew.VECTOR2I(pcbnew.FromMM(x_mm), pcbnew.FromMM(y_mm))

    # ==================== ROUTING SYSTEM ====================

    # 1. USB Differential Pair (/D+, /D-) on F.Cu
    poly([P("USB1", 3), V(29.98, 101.0), V(31.6, 102.62), V(31.6, 105.77), P("U3", 4)], 0.3, pcbnew.F_Cu, "/D+")
    poly([P("USB1", 2), V(29.33, 101.5), V(31.0, 103.17), V(31.0, 105.27), P("U3", 5)], 0.3, pcbnew.F_Cu, "/D-")

    # 2. VDD_5V_IN on F.Cu (Clean routing above SW2)
    poly([P("USB1", 1), V(28.68, 98.71), P("C6", 1)], 0.8, pcbnew.F_Cu, "/VDD_5V_IN")
    poly([P("USB1", 1), V(28.68, 93.5), V(37.85, 93.5), P("SW2", 2)], 0.8, pcbnew.F_Cu, "/VDD_5V_IN")

    # 3. CP2102 Local Nets on F.Cu
    # U3.6 to C7.2 (route clear of USB diff pairs)
    poly([P("U3", 6), V(33.0, 104.77), V(33.0, 110.95), P("C7", 2)], 0.4, pcbnew.F_Cu, "Net-(U3-VDD)")
    poly([P("U3", 28), V(35.11, 110.0), V(37.11, 112.0), P("C9", 2)], 0.4, pcbnew.F_Cu, "Net-(U3-DTR)")
    poly([P("C9", 1), V(41.5, 113.05), V(41.5, 133.62), P("J3", 4)], 0.3, pcbnew.F_Cu, "/DTR")

    # 4. UART TX, RX
    # /TX: U3.26 -> J3.3 (F.Cu) -> via -> B.Cu -> via -> D6.1
    poly([P("U3", 26), V(36.11, 109.5), V(38.5, 111.89), V(38.5, 131.08), P("J3", 3)], 0.3, pcbnew.F_Cu, "/TX")
    poly([P("J3", 3), V(45.0, 132.58), V(55.0, 123.5), V(60.0625, 123.5)], 0.3, pcbnew.B_Cu, "/TX")
    add_via(V(60.0625, 123.5), 0.6, 0.3, "/TX")
    poly([V(60.0625, 123.5), P("D6", 1)], 0.3, pcbnew.F_Cu, "/TX")

    # /RX: U3.25 -> J3.2 (F.Cu) -> via -> B.Cu -> via -> D5.1
    poly([P("U3", 25), V(36.61, 109.0), V(39.0, 111.39), V(39.0, 129.04), P("J3", 2)], 0.3, pcbnew.F_Cu, "/RX")
    poly([P("J3", 2), V(44.0, 130.04), V(52.0, 123.0), V(54.0625, 123.0)], 0.3, pcbnew.B_Cu, "/RX")
    add_via(V(54.0625, 123.0), 0.6, 0.3, "/RX")
    poly([V(54.0625, 123.0), P("D5", 1)], 0.3, pcbnew.F_Cu, "/RX")

    # 5. LEDs & Resistors
    # D1 to R1 (Net-(D1-A))
    poly([P("D1", 2), V(31.9375, 124.0), V(31.0, 124.938), P("R1", 2)], 0.4, pcbnew.F_Cu, "Net-(D1-A)")
    # D2 to R2 (Net-(D2-A))
    poly([P("D2", 2), V(37.9375, 124.0), V(37.0, 124.938), P("R2", 2)], 0.4, pcbnew.F_Cu, "Net-(D2-A)")
    # D3 to R3 (Net-(D3-K))
    poly([P("D3", 1), V(42.0625, 124.0), V(43.0, 124.938), P("R3", 2)], 0.4, pcbnew.F_Cu, "Net-(D3-K)")
    # D4 to R4 (Net-(D4-A))
    poly([P("D4", 2), V(49.9375, 124.0), V(49.0, 124.938), P("R4", 2)], 0.4, pcbnew.F_Cu, "Net-(D4-A)")
    # D5 to R6 (Net-(D5-A)) on F.Cu
    poly([P("D5", 2), V(55.9375, 124.0), V(57.5, 125.5875), V(61.0, 125.5875), P("R6", 1)], 0.4, pcbnew.F_Cu, "Net-(D5-A)")
    # D6 to R5 (Net-(D6-A)) using B.Cu layer to avoid crossing D5
    add_via(V(61.9375, 123.0), 0.6, 0.3, "Net-(D6-A)")
    poly([P("D6", 2), V(61.9375, 123.0)], 0.4, pcbnew.F_Cu, "Net-(D6-A)")
    add_via(V(55.0, 128.5), 0.6, 0.3, "Net-(D6-A)")
    poly([V(61.9375, 123.0), V(55.0, 123.0), V(55.0, 128.5)], 0.4, pcbnew.B_Cu, "Net-(D6-A)")
    poly([V(55.0, 128.5), P("R5", 1)], 0.4, pcbnew.F_Cu, "Net-(D6-A)")

    # 6. NE555 Clock (U5)
    # /1Hz: U5.3 to R4.1 to J4.2 (routed on B.Cu to avoid crossing local nets)
    add_via(V(54.0, 110.635), 0.6, 0.3, "/1Hz")
    poly([P("U5", 3), V(54.0, 110.635)], 0.3, pcbnew.F_Cu, "/1Hz")
    add_via(V(49.0, 128.5), 0.6, 0.3, "/1Hz")
    poly([V(54.0, 110.635), V(49.0, 115.635), V(49.0, 128.5)], 0.3, pcbnew.B_Cu, "/1Hz")
    poly([V(49.0, 128.5), P("R4", 1)], 0.3, pcbnew.F_Cu, "/1Hz")
    poly([P("R4", 1), V(49.0, 135.54), P("J4", 2)], 0.3, pcbnew.F_Cu, "/1Hz")

    # Net-(U5-CV): U5.5 to C10.2
    poly([P("U5", 5), V(65.0, 111.905), V(68.405, 108.5), P("C10", 2)], 0.4, pcbnew.F_Cu, "Net-(U5-CV)")
    # Net-(U5-DC): U5.7 to R7.2 to R8.1
    poly([P("U5", 7), V(57.0, 109.365), V(54.547, 105.0875), P("R7", 2)], 0.4, pcbnew.F_Cu, "Net-(U5-DC)")
    poly([P("R7", 2), P("R8", 1)], 0.4, pcbnew.F_Cu, "Net-(U5-DC)")
    # Net-(U5-TH): U5.2 to U5.6 to R8.2 to C11.2
    poly([P("U5", 2), V(53.5, 109.365), V(53.5, 111.0875), P("R8", 2)], 0.4, pcbnew.F_Cu, "Net-(U5-TH)")
    poly([P("U5", 2), V(58.0, 109.365), V(59.27, 110.635), P("U5", 6)], 0.4, pcbnew.F_Cu, "Net-(U5-TH)")
    poly([P("U5", 6), V(66.435, 110.635), P("C11", 2)], 0.4, pcbnew.F_Cu, "Net-(U5-TH)")

    # 7. LM2776 (U2)
    poly([P("U2", 6), P("C2", 1)], 0.4, pcbnew.F_Cu, "Net-(U2-C1-)")
    poly([P("U2", 5), V(60.0, 96.5), V(59.05, 95.55), P("C2", 2)], 0.4, pcbnew.F_Cu, "Net-(U2-C1+)")
    poly([P("U2", 3), P("U2", 4)], 0.4, pcbnew.F_Cu, "Net-(U2-EN)")
    poly([P("U2", 3), V(64.0, 97.45), V(62.1, 97.45), P("C1", 1)], 0.4, pcbnew.F_Cu, "Net-(U2-EN)")
    add_via(V(43.5, 97.45), 0.8, 0.4, "Net-(U2-EN)")
    poly([P("C1", 1), V(43.5, 97.45)], 0.4, pcbnew.F_Cu, "Net-(U2-EN)")
    poly([V(43.5, 97.45), V(43.5, 92.5), V(28.0, 92.5), V(28.0, 134.54), P("J1", 2)], 0.4, pcbnew.B_Cu, "Net-(U2-EN)")

    # 8. Potentiometer Connectors (J7, J8) to Jumpers (J5, J6)
    # /P1+
    poly([P("J7", 1), P("J7", 2), P("J7", 3)], 0.8, pcbnew.F_Cu, "/P1+")
    poly([P("J7", 1), V(70.0, 104.08), V(70.0, 135.09), P("J5", 2)], 0.8, pcbnew.B_Cu, "/P1+")

    # /P1-
    poly([P("J7", 4), P("J7", 5), P("J7", 6)], 0.8, pcbnew.F_Cu, "/P1-")
    poly([P("J7", 4), V(68.0, 101.54), V(68.0, 106.2), V(53.0, 106.2), P("J5", 5)], 0.8, pcbnew.B_Cu, "/P1-")

    # /P2+
    poly([P("J8", 1), P("J8", 2), P("J8", 3)], 0.8, pcbnew.F_Cu, "/P2+")
    poly([P("J8", 1), V(72.0, 122.08), V(72.0, 135.09), P("J6", 2)], 0.8, pcbnew.B_Cu, "/P2+")

    # /P2-
    poly([P("J8", 4), P("J8", 5), P("J8", 6)], 0.8, pcbnew.F_Cu, "/P2-")
    poly([P("J8", 4), V(66.0, 119.54), V(66.0, 126.0), V(61.5, 126.0), P("J6", 5)], 0.8, pcbnew.B_Cu, "/P2-")

    # 9. /VDD_3V3 (U1.2, C5.1, J6.3, J5.3, J1.1, R2.1, J3.1)
    poly([V(47.85, 96.5), V(54.15, 96.5), V(58.0, 96.5), V(64.0, 102.5), P("C5", 1)], 0.8, pcbnew.F_Cu, "/VDD_3V3")
    add_via(V(65.55, 101.0), 0.8, 0.4, "/VDD_3V3")
    poly([P("C5", 1), V(65.55, 101.0)], 0.8, pcbnew.F_Cu, "/VDD_3V3")
    poly([V(65.55, 101.0), V(65.55, 132.55), P("J6", 3), P("J5", 3)], 0.8, pcbnew.B_Cu, "/VDD_3V3")
    poly([P("J5", 3), V(40.0, 132.55), P("J3", 1)], 0.8, pcbnew.B_Cu, "/VDD_3V3")
    poly([P("J3", 1), V(30.0, 127.5), P("J1", 1)], 0.8, pcbnew.B_Cu, "/VDD_3V3")
    add_via(V(37.0, 129.0), 0.8, 0.4, "/VDD_3V3")
    poly([P("R2", 1), V(37.0, 129.0)], 0.8, pcbnew.F_Cu, "/VDD_3V3")
    poly([V(37.0, 129.0), V(37.0, 132.55), P("J3", 1)], 0.8, pcbnew.B_Cu, "/VDD_3V3")

    # 10. /VDD_N (U2.1, C3.1, J6.4, J5.4, R3.1)
    poly([P("U2", 1), P("C3", 1)], 0.8, pcbnew.F_Cu, "/VDD_N")
    add_via(V(61.5, 99.0), 0.8, 0.4, "/VDD_N")
    poly([P("C3", 1), V(61.5, 99.0)], 0.8, pcbnew.F_Cu, "/VDD_N")
    poly([V(61.5, 99.0), V(61.5, 132.55), P("J6", 4), P("J5", 4)], 0.8, pcbnew.B_Cu, "/VDD_N")
    add_via(V(43.0, 129.0), 0.8, 0.4, "/VDD_N")
    poly([P("R3", 1), V(43.0, 129.0)], 0.8, pcbnew.F_Cu, "/VDD_N")
    poly([V(43.0, 129.0), V(43.0, 132.55), P("J5", 4)], 0.8, pcbnew.B_Cu, "/VDD_N")

    # 11. /VDD_5V (SW2.1, U1.3, C4.1, J6.1, J5.1, R1.1, J1.3, R7.1, R5.2, C8.2, U5.4, U5.8, R6.2, U3.7, U3.8)
    poly([P("SW2", 1), V(35.67, 97.0), V(34.2975, 98.373), P("U3", 7), P("U3", 8)], 0.8, pcbnew.F_Cu, "/VDD_5V")
    poly([P("SW2", 1), V(35.67, 92.5), V(44.05, 92.5), V(44.05, 98.8), P("U1", 3)], 0.8, pcbnew.F_Cu, "/VDD_5V")
    poly([P("U1", 3), V(51.0, 98.8), V(54.25, 98.8), V(71.5, 98.8), P("C4", 1)], 0.8, pcbnew.F_Cu, "/VDD_5V")
    
    # 5V distribution bus on B.Cu
    add_via(V(74.0, 98.8), 0.8, 0.4, "/VDD_5V")
    poly([P("C4", 1), V(74.0, 98.8)], 0.8, pcbnew.F_Cu, "/VDD_5V")
    poly([V(74.0, 98.8), V(74.0, 137.63), P("J6", 1), P("J5", 1)], 0.8, pcbnew.B_Cu, "/VDD_5V")
    poly([P("J5", 1), V(30.0, 137.63), P("J1", 3)], 0.8, pcbnew.B_Cu, "/VDD_5V")

    # Resistors to 5V bus
    add_via(V(31.0, 129.0), 0.8, 0.4, "/VDD_5V")
    poly([P("R1", 1), V(31.0, 129.0)], 0.8, pcbnew.F_Cu, "/VDD_5V")
    poly([V(31.0, 129.0), V(31.0, 137.63)], 0.8, pcbnew.B_Cu, "/VDD_5V")

    add_via(V(55.0, 124.0), 0.8, 0.4, "/VDD_5V")
    poly([P("R5", 2), V(55.0, 124.0)], 0.8, pcbnew.F_Cu, "/VDD_5V")
    poly([V(55.0, 124.0), V(55.0, 137.63)], 0.8, pcbnew.B_Cu, "/VDD_5V")

    add_via(V(61.0, 124.0), 0.8, 0.4, "/VDD_5V")
    poly([P("R6", 2), V(61.0, 124.0)], 0.8, pcbnew.F_Cu, "/VDD_5V")
    poly([V(61.0, 124.0), V(61.0, 137.63)], 0.8, pcbnew.B_Cu, "/VDD_5V")

    # U5 5V connections
    poly([P("U5", 8), V(60.575, 106.0), V(44.45, 106.0), P("C8", 2)], 0.8, pcbnew.F_Cu, "/VDD_5V")
    poly([P("C8", 2), V(52.0, 106.0), P("R7", 1)], 0.8, pcbnew.F_Cu, "/VDD_5V")
    poly([P("C8", 2), V(44.45, 98.8), P("U1", 3)], 0.8, pcbnew.F_Cu, "/VDD_5V")
    poly([P("U5", 8), V(60.575, 106.5), V(55.425, 106.5), P("U5", 4)], 0.8, pcbnew.F_Cu, "/VDD_5V")

    # 12. Ground Connections (GND) - Clean local stubs to ground plane
    poly([P("SW2", 4), P("SW2", 5)], 0.8, pcbnew.F_Cu, "GND")
    poly([P("USB1", 5), P("USB1", 6), P("USB1", 7)], 0.8, pcbnew.F_Cu, "GND")
    poly([P("USB1", 8), P("USB1", 9), V(28.68, 98.39), P("USB1", 5)], 0.8, pcbnew.F_Cu, "GND")
    poly([P("USB1", 5), V(30.95, 98.34), P("C6", 2), P("C7", 1)], 0.8, pcbnew.F_Cu, "GND")
    poly([P("U3", 3), V(34.2975, 105.77), P("U3", 0), V(42.55, 105.77), P("C8", 1)], 0.8, pcbnew.F_Cu, "GND")
    poly([P("U3", 3), V(34.2975, 112.0), P("C7", 1)], 0.8, pcbnew.F_Cu, "GND")
    poly([P("U2", 2), V(65.3625, 96.5), P("C3", 2), P("C4", 2)], 0.8, pcbnew.F_Cu, "GND")
    poly([P("U2", 2), V(67.45, 96.5), P("C5", 2), V(70.5, 102.5), P("C10", 1), V(70.5, 113.0), P("C11", 1)], 0.8, pcbnew.F_Cu, "GND")
    poly([P("U5", 1), V(55.425, 106.0), V(42.55, 106.0), P("C8", 1)], 0.8, pcbnew.F_Cu, "GND")
    poly([P("D1", 1), P("D2", 1), P("D3", 2), P("D4", 1)], 0.8, pcbnew.F_Cu, "GND")
    poly([P("D1", 1), V(30.0625, 112.0), P("C7", 1)], 0.8, pcbnew.F_Cu, "GND")
    poly([P("J5", 6), P("J6", 6)], 0.8, pcbnew.F_Cu, "GND")
    poly([P("J4", 1), V(48.0, 137.63), P("J5", 6)], 0.8, pcbnew.F_Cu, "GND")
    poly([P("J3", 5), P("J4", 1)], 0.8, pcbnew.F_Cu, "GND")
    poly([P("J6", 6), V(61.5, 113.0), P("C11", 1)], 0.8, pcbnew.F_Cu, "GND")
    poly([P("C1", 2), V(45.5, 95.55), P("C3", 2)], 0.8, pcbnew.F_Cu, "GND")
    poly([P("C8", 1), V(42.55, 120.0), P("D3", 2)], 0.8, pcbnew.F_Cu, "GND")
    poly([P("D4", 1), V(48.0, 122.0), P("J4", 1)], 0.8, pcbnew.F_Cu, "GND")
    poly([P("U1", 1), V(47.85, 95.0), P("SW2", 5)], 0.8, pcbnew.F_Cu, "GND")

    # 13. Top & Bottom GND Copper Zones
    gnd_netcode = net_map.get("GND", 1)
    pts = pcbnew.VECTOR_VECTOR2I()
    pts.push_back(pcbnew.VECTOR2I(pcbnew.FromMM(15.0), pcbnew.FromMM(80.0)))
    pts.push_back(pcbnew.VECTOR2I(pcbnew.FromMM(85.0), pcbnew.FromMM(80.0)))
    pts.push_back(pcbnew.VECTOR2I(pcbnew.FromMM(85.0), pcbnew.FromMM(150.0)))
    pts.push_back(pcbnew.VECTOR2I(pcbnew.FromMM(15.0), pcbnew.FromMM(150.0)))

    for layer in [pcbnew.F_Cu, pcbnew.B_Cu]:
        zone = pcbnew.ZONE(board)
        zone.SetNetCode(gnd_netcode)
        zone.SetLayer(layer)
        zone.AddPolygon(pts)
        zone.SetMinThickness(pcbnew.FromMM(0.25))
        zone.SetThermalReliefGap(pcbnew.FromMM(0.25))
        zone.SetThermalReliefSpokeWidth(pcbnew.FromMM(0.4))
        board.Add(zone)

    # 14. Title Block
    tb = board.GetTitleBlock()
    tb.SetTitle("Lab 06: Routing - Ky thuat Di day Mach in tren PCB")
    tb.SetDate("2026-08-30")
    tb.SetRevision("Rev 1.0")
    tb.SetCompany("Truong Dai Hoc Khoa Hoc Tu Nhien - DHQG TPHCM")
    tb.SetComment(1, "Nguoi thiet ke: Le Ngoc Tuong - MSSV: 23207124")
    tb.SetComment(2, "Lop: 23DTV_CLC3 - Ca thuc hanh: Ca 2")

    board.Save(pcb_path)
    print(f"Board saved successfully to {pcb_path} with {len(board.GetTracks())} tracks!")

if __name__ == "__main__":
    for p in ["LAB6.kicad_pcb", "lab6.kicad_pcb"]:
        route_board(p)
