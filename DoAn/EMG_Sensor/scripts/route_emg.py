import pcbnew, math, uuid

def mm(v): return int(round(v * 1e6))
def uid(): return str(uuid.uuid4())

board = pcbnew.LoadBoard('DoAn/EMG_Sensor/EMG_Sensor.kicad_pcb')

# Remove existing tracks and vias if any
for t in list(board.GetTracks()):
    board.Remove(t)
for z in list(board.Zones()):
    board.Remove(z)

def add_seg(netname, layer_id, w, x1, y1, x2, y2):
    t = pcbnew.PCB_TRACK(board)
    t.SetStart(pcbnew.VECTOR2I(mm(x1), mm(y1)))
    t.SetEnd(pcbnew.VECTOR2I(mm(x2), mm(y2)))
    t.SetWidth(mm(w))
    t.SetLayer(layer_id)
    t.SetNet(board.FindNet(netname))
    board.Add(t)

def add_via(netname, x, y, size=0.6, drill=0.3):
    v = pcbnew.PCB_VIA(board)
    v.SetPosition(pcbnew.VECTOR2I(mm(x), mm(y)))
    v.SetWidth(mm(size))
    v.SetDrill(mm(drill))
    v.SetNet(board.FindNet(netname))
    board.Add(v)

def route_poly(netname, layer_id, w, pts):
    for p1, p2 in zip(pts, pts[1:]):
        if abs(p1[0]-p2[0]) > 1e-4 or abs(p1[1]-p2[1]) > 1e-4:
            add_seg(netname, layer_id, w, p1[0], p1[1], p2[0], p2[1])

FC = pcbnew.F_Cu
BC = pcbnew.B_Cu
SW = 0.25  # Signal width
PW = 0.35  # Power width

# 1. IN_PLUS_RAW & IN_MINUS_RAW (J2 to R4/R5)
route_poly('IN_PLUS_RAW', FC, SW, [(4.0, 15.0), (5.5, 15.0), (5.5, 12.0), (7.17, 12.0)])
route_poly('IN_MINUS_RAW', FC, SW, [(4.0, 17.54), (5.5, 17.54), (5.5, 16.0), (7.17, 16.0)])

# 2. IN_PLUS_FILT: R4.2 (8.82, 12.0) to C5.1 (10.5, 14.78), U1.3 (15.03, 14.63), C6.1 (10.5, 9.78), R6.1 (13.0, 9.82)
route_poly('IN_PLUS_FILT', FC, SW, [(8.82, 12.0), (9.8, 12.0), (9.8, 14.78), (10.5, 14.78)])
route_poly('IN_PLUS_FILT', FC, SW, [(10.5, 14.78), (15.03, 14.63)])
route_poly('IN_PLUS_FILT', FC, SW, [(9.8, 12.0), (9.8, 9.78), (10.5, 9.78), (13.0, 9.82)])

# 3. IN_MINUS_FILT: R5.2 (8.82, 16.0) to C5.2 (10.5, 13.22), U1.2 (15.03, 13.37), C7.1 (10.5, 19.77), R7.1 (13.0, 19.82)
# Route via B.Cu bridge to avoid crossing IN_PLUS_FILT
route_poly('IN_MINUS_FILT', FC, SW, [(8.82, 16.0), (9.2, 16.0)])
add_via('IN_MINUS_FILT', 9.2, 16.0)
route_poly('IN_MINUS_FILT', BC, SW, [(9.2, 16.0), (9.2, 13.22), (10.5, 13.22)])
add_via('IN_MINUS_FILT', 10.5, 13.22)
route_poly('IN_MINUS_FILT', FC, SW, [(10.5, 13.22), (15.03, 13.37)])
route_poly('IN_MINUS_FILT', FC, SW, [(8.82, 16.0), (8.82, 19.77), (10.5, 19.77), (13.0, 19.82)])

# 4. RG1 & RG2 (U1 Gain resistor R8)
route_poly('RG1', FC, SW, [(15.03, 12.10), (15.03, 8.5), (16.68, 8.5)])
route_poly('RG2', FC, SW, [(19.98, 12.10), (19.98, 8.5), (18.32, 8.5)])

# 5. VOUT_IA (U1.6 to C9.1)
route_poly('VOUT_IA', FC, SW, [(19.98, 14.63), (22.23, 14.64)])

# 6. HPF_OUT (C9.2 to R10.1 and R9.1)
route_poly('HPF_OUT', FC, SW, [(23.77, 14.64), (25.68, 14.64)])
route_poly('HPF_OUT', FC, SW, [(23.77, 14.64), (23.77, 19.32), (23.0, 19.32)])

# 7. LPF_NODE (R10.2 to R11.1 and C10.1)
route_poly('LPF_NODE', FC, SW, [(27.32, 14.64), (28.68, 14.64)])
route_poly('LPF_NODE', FC, SW, [(27.32, 14.64), (27.23, 18.5)])

# 8. LPF_IN (R11.2 to U2.5 and C11.1)
route_poly('LPF_IN', FC, SW, [(30.32, 14.64), (31.0, 14.64), (31.0, 16.27), (32.52, 16.27)])
route_poly('LPF_IN', FC, SW, [(30.32, 14.64), (30.32, 11.78), (29.5, 11.78)])

# 9. LPF_FB (R12.1, R13.1, U2.6)
route_poly('LPF_FB', FC, SW, [(26.18, 22.0), (29.68, 22.0), (31.5, 22.0), (31.5, 17.54), (32.52, 17.54)])

# 10. RAW_EMG (U2.7 to R13.2, C10.2, R14.1, R17.1, J3.3)
route_poly('RAW_EMG', FC, SW, [(32.52, 18.81), (31.32, 22.0), (28.77, 18.5)])
route_poly('RAW_EMG', FC, SW, [(32.52, 18.81), (34.17, 23.5)])
# Cross to R17.1 (40.67, 14.0) via B.Cu
add_via('RAW_EMG', 34.5, 20.0)
route_poly('RAW_EMG', FC, SW, [(32.52, 18.81), (34.5, 20.0)])
route_poly('RAW_EMG', BC, SW, [(34.5, 20.0), (39.5, 20.0), (39.5, 14.0), (40.67, 14.0)])
add_via('RAW_EMG', 40.67, 14.0)
# To J3.3 (46.5, 20.08) via B.Cu
route_poly('RAW_EMG', BC, SW, [(39.5, 20.0), (46.5, 20.08)])

# 11. RECT_OUT (U2.8 to D2.1 and D3.2)
route_poly('RECT_OUT', FC, SW, [(37.48, 18.81), (39.0, 18.81), (39.0, 22.65), (40.0, 22.65)])
route_poly('RECT_OUT', FC, SW, [(39.0, 18.81), (43.0, 18.81), (43.0, 19.35)])

# 12. RECT_IN (U2.9 to D2.2, R14.2, R15.1)
route_poly('RECT_IN', FC, SW, [(37.48, 17.54), (40.0, 17.54), (40.0, 19.35)])
route_poly('RECT_IN', FC, SW, [(37.48, 17.54), (37.0, 17.54), (37.0, 23.5), (35.83, 23.5)])
route_poly('RECT_IN', FC, SW, [(40.0, 19.35), (40.0, 25.0), (40.67, 25.0)])

# 13. RECT_HALF (D3.1 to R15.2 and R16.1)
route_poly('RECT_HALF', FC, SW, [(43.0, 22.65), (42.33, 25.0)])
route_poly('RECT_HALF', FC, SW, [(43.0, 22.65), (43.0, 16.5), (40.67, 16.5)])

# 14. ENV_IN (U2.13 to R16.2, R17.2, R18.1, C12.1)
route_poly('ENV_IN', FC, SW, [(37.48, 12.46), (39.5, 12.46), (39.5, 11.5), (40.67, 11.5)])
route_poly('ENV_IN', FC, SW, [(39.5, 12.46), (39.5, 16.5), (42.33, 16.5)])
route_poly('ENV_IN', FC, SW, [(39.5, 12.46), (39.5, 14.0), (42.33, 14.0)])
route_poly('ENV_IN', FC, SW, [(39.5, 11.5), (39.5, 9.0), (40.73, 9.0)])

# 15. ENV_EMG (U2.14 to R18.2, C12.2, J3.4, R19.1)
route_poly('ENV_EMG', FC, SW, [(37.48, 11.19), (42.33, 11.19), (42.33, 11.5)])
route_poly('ENV_EMG', FC, SW, [(42.33, 11.19), (42.27, 9.0)])
route_poly('ENV_EMG', FC, SW, [(42.33, 11.19), (44.5, 11.19), (44.5, 22.62), (46.5, 22.62)])
# To R19.1 (13.5, 24.82) via B.Cu
add_via('ENV_EMG', 44.5, 22.62)
route_poly('ENV_EMG', BC, SW, [(44.5, 22.62), (44.5, 26.5), (13.5, 26.5), (13.5, 24.82)])
add_via('ENV_EMG', 13.5, 24.82)

# 16. LEDs (NET_D1_R1 and NET_D4_R19)
route_poly('NET_D1_R1', FC, SW, [(14.56, 4.0), (18.68, 4.0)])
route_poly('NET_D4_R19', FC, SW, [(13.5, 23.18), (17.94, 23.18), (17.94, 24.0)])

# 17. VMID (R2.2, R3.1, C3.1, C4.1 to U2.3)
route_poly('VMID', FC, SW, [(31.82, 4.0), (33.67, 4.0), (37.05, 4.0), (40.73, 4.0)])
route_poly('VMID', FC, SW, [(31.82, 4.0), (31.82, 13.73), (32.52, 13.73)])

# 18. VREF (U2.1 & U2.2 to R12.2, U2.10, U2.12, U1.5, R9.2, C11.2, R6.2, R7.2, J2.3)
route_poly('VREF', FC, SW, [(32.52, 11.19), (32.52, 12.46)])
# Drop to B.Cu bus for VREF distribution across the board
add_via('VREF', 31.0, 12.46)
route_poly('VREF', FC, SW, [(32.52, 12.46), (31.0, 12.46)])
# Distribute on B.Cu at Y = 7.0 and Y = 21.0
route_poly('VREF', BC, PW, [(31.0, 12.46), (31.0, 7.0), (4.0, 7.0), (4.0, 20.08)])
add_via('VREF', 4.0, 20.08) # J2.3
# R6.2 (13.0, 8.18) & C11.2 (29.5, 10.22)
route_poly('VREF', BC, SW, [(13.0, 7.0), (13.0, 8.18)])
add_via('VREF', 13.0, 8.18)
route_poly('VREF', BC, SW, [(29.5, 7.0), (29.5, 10.22)])
add_via('VREF', 29.5, 10.22)
# U1.5 (19.98, 15.9), R9.2 (23.0, 17.68), R7.2 (13.0, 18.18), R12.2 (27.82, 22.0), U2.10 (37.48, 16.27), U2.12 (37.48, 13.73)
route_poly('VREF', BC, PW, [(31.0, 12.46), (31.0, 16.27)])
add_via('VREF', 31.0, 16.27)
route_poly('VREF', FC, SW, [(31.0, 16.27), (27.82, 16.27), (27.82, 22.0)]) # R12.2
route_poly('VREF', FC, SW, [(27.82, 16.27), (23.0, 16.27), (23.0, 17.68)]) # R9.2
route_poly('VREF', FC, SW, [(23.0, 16.27), (19.98, 16.27), (19.98, 15.9)]) # U1.5
route_poly('VREF', BC, SW, [(31.0, 16.27), (36.5, 16.27)])
add_via('VREF', 36.5, 16.27)
route_poly('VREF', FC, SW, [(36.5, 16.27), (37.48, 16.27)]) # U2.10
route_poly('VREF', FC, SW, [(36.5, 16.27), (36.5, 13.73), (37.48, 13.73)]) # U2.12
route_poly('VREF', BC, SW, [(13.0, 7.0), (13.0, 18.18)])
add_via('VREF', 13.0, 18.18) # R7.2

# 19. VCC (Power distribution on B.Cu trunk at Y = 2.5)
route_poly('VCC', FC, PW, [(25.0, 3.5), (25.0, 2.0)])
add_via('VCC', 25.0, 2.0)
route_poly('VCC', BC, PW, [(6.0, 2.0), (46.5, 2.0)])
# Connect all VCC pins:
for vx, vy in [(7.55, 4.0), (11.22, 4.0), (16.44, 4.0), (30.18, 4.0), (34.23, 8.5)]:
    route_poly('VCC', BC, PW, [(vx, 2.0), (vx, vy)])
    add_via('VCC', vx, vy)
# U1.7 (19.98, 13.37) & C8.1 (20.0, 10.28)
route_poly('VCC', BC, PW, [(20.0, 2.0), (20.0, 10.28)])
add_via('VCC', 20.0, 10.28)
route_poly('VCC', FC, PW, [(20.0, 10.28), (19.98, 13.37)])
# U2.4 (32.52, 15.0)
route_poly('VCC', BC, PW, [(32.52, 2.0), (32.52, 15.0)])
add_via('VCC', 32.52, 15.0)
# J3.1 (46.5, 15.0)
route_poly('VCC', BC, PW, [(46.5, 2.0), (46.5, 15.0)])

# ==================== COPPER POURS (GND) ====================
def _disabled_add_zone(layer_id):
    z = board.AddArea(None, board.FindNet('GND'), layer_id, pcbnew.VECTOR2I(0, 0), pcbnew.CPolyLine.DIAGONAL_EDGE)
    pts = pcbnew.VECTOR_VECTOR2I()
    for x, y in [(mm(0.5), mm(0.5)), (mm(49.5), mm(0.5)), (mm(49.5), mm(29.5)), (mm(0.5), mm(29.5))]:
        pts.append(pcbnew.VECTOR2I(x, y))
    z.AddPolygon(pts)
    z.SetHatch(pcbnew.CPolyLine.NO_HATCH, mm(0.5), True)
    z.SetMinThickness(mm(0.20))
    z.SetThermalReliefGap(mm(0.20))
    z.SetThermalReliefCopperBridge(mm(0.35))
    z.SetClearance(mm(0.20))
    z.SetPadConnection(pcbnew.ZONE_CONNECTION_T_THERMAL)

# zones added via s-expr

# GND Stitching Vias
for sx, sy in [
    (6.0, 10.0), (6.0, 25.0),
    (16.0, 17.5), (20.0, 22.0), (25.0, 11.0), (25.0, 25.0),
    (33.0, 25.0), (36.0, 27.0), (44.0, 18.0), (44.0, 27.0),
    (14.0, 14.0), (36.0, 6.0), (22.0, 6.0)
]:
    add_via('GND', sx, sy)

pcbnew.SaveBoard('DoAn/EMG_Sensor/EMG_Sensor.kicad_pcb', board)
print("Board routing & copper pours created successfully!")
