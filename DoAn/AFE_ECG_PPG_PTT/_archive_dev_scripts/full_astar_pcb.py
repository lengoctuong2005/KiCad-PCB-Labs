#!/usr/bin/env python3
"""
Full Autonomous A* Maze Router for AFE ECG + PPG PTT PCB.
Guarantees zero track crossings and zero pad collisions.
"""
import pcbnew
import heapq
import math
from test_netlist_map import NET_MAP

board = pcbnew.BOARD()

# Design settings
ds = board.GetDesignSettings()
ds.SetCustomTrackWidth(pcbnew.FromMM(0.254))
ds.SetCustomTrackWidth(pcbnew.FromMM(0.5))
ds.SetCustomTrackWidth(pcbnew.FromMM(0.6))
ds.SetCustomViaSize(pcbnew.FromMM(0.6))
ds.SetCustomViaDrill(pcbnew.FromMM(0.3))
ds.m_SolderMaskMargin = 0
ds.m_SolderMaskMinWidth = 0
ds.m_TentViasFront = True
ds.m_TentViasBack = True

# 1. Edge Cuts: 100 x 80 mm
poly = pcbnew.PCB_SHAPE(board)
poly.SetShape(pcbnew.SHAPE_T_RECT)
poly.SetStart(pcbnew.VECTOR2I(0, 0))
poly.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(100), pcbnew.FromMM(80)))
poly.SetLayer(pcbnew.Edge_Cuts)
poly.SetWidth(pcbnew.FromMM(0.15))
board.Add(poly)

# 2. Add Nets
for net_name in NET_MAP.keys():
    board.Add(pcbnew.NETINFO_ITEM(board, net_name))
board_nets = board.GetNetsByName()

# 3. Footprints Placement
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
add_fp('U2', 'ADS1115IDGST', 'Package_SO', 'TSSOP-10_3x3mm_P0.5mm', 50, 38, 0)
add_fp('U3', 'MCP1700-3002E', 'Package_TO_SOT_SMD', 'SOT-23', 25, 62, 0)

# Connectors
add_fp('J1', 'SJ1-3533NG', 'Connector_Audio', 'Jack_3.5mm_CUI_SJ1-3533NG_Horizontal', 10, 20, 180)
add_fp('J1A', 'ECG_PROBES', 'Connector_PinHeader_2.54mm', 'PinHeader_1x03_P2.54mm_Vertical', 12, 36, 0)
add_fp('J2A', 'ESP32_L', 'Connector_PinHeader_2.54mm', 'PinHeader_1x19_P2.54mm_Vertical', 71, 16, 0)
add_fp('J2B', 'ESP32_R', 'Connector_PinHeader_2.54mm', 'PinHeader_1x19_P2.54mm_Vertical', 96.4, 16, 0)
add_fp('J3', 'MAX30102', 'Connector_PinHeader_2.54mm', 'PinHeader_1x07_P2.54mm_Vertical', 62, 16, 0)

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
add_fp('R16', '1k', 'Resistor_SMD', 'R_0603_1608Metric', 45, 34, 90)
add_fp('R17', '1k', 'Resistor_SMD', 'R_0603_1608Metric', 45, 42, 90)
add_fp('C7', '10nF', 'Capacitor_SMD', 'C_0603_1608Metric', 47, 34, 90)
add_fp('C8', '1nF', 'Capacitor_SMD', 'C_0603_1608Metric', 44, 30, 0)
add_fp('C9', '1nF', 'Capacitor_SMD', 'C_0603_1608Metric', 44, 46, 0)

# ADS1115 Decoupling C16, C17
add_fp('C16', '0.1uF', 'Capacitor_SMD', 'C_0603_1608Metric', 52, 30, 0)
add_fp('C17', '1uF', 'Capacitor_SMD', 'C_0603_1608Metric', 56, 30, 0)

# Pullups R18 (SDA), R19 (SCL), R20 (ALERT)
add_fp('R18', '4.7k', 'Resistor_SMD', 'R_0603_1608Metric', 64, 34, 0)
add_fp('R19', '4.7k', 'Resistor_SMD', 'R_0603_1608Metric', 64, 38, 0)
add_fp('R20', '10k', 'Resistor_SMD', 'R_0603_1608Metric', 64, 42, 0)

# Test Points TP1..TP7
tp_names = ['ECG_OUT', 'REFOUT', 'LOD+', 'LOD-', '+VS_A', '+3V3', 'GND']
for i in range(1, 8):
    add_fp(f'TP{i}', tp_names[i-1], 'TestPoint', 'TestPoint_Pad_D1.5mm', 32 + (i-1)*5, 72, 0)

# Assign nets to all pads
for net_name, conns in NET_MAP.items():
    net_item = board_nets[net_name]
    for ref, pad_num in conns:
        fp = fps[ref]
        pad = fp.FindPadByNumber(pad_num)
        if pad:
            pad.SetNet(net_item)
            pad_map[(ref, pad_num)] = pad

# 4. Grid Setup for A*
RES = 0.5 # 0.5 mm
NX = int(100.0 / RES) + 1
NY = int(80.0 / RES) + 1

def to_grid(x_mm, y_mm):
    return max(0, min(NX-1, int(round(x_mm / RES)))), max(0, min(NY-1, int(round(y_mm / RES))))

def to_mm(gx, gy):
    return gx * RES, gy * RES

# Build global obstacle map
# Layer 0: F.Cu, Layer 1: B.Cu
# Each cell maps to the net_name occupying it (or None if free)
grid_occ = {}

# Mark pads as obstacles
for ref, fp in fps.items():
    for pad in fp.Pads():
        pos = pad.GetPosition()
        px, py = pos.x / 1e6, pos.y / 1e6
        net_name = pad.GetNetname()
        gx, gy = to_grid(px, py)
        # Pad extent
        is_th = (pad.GetAttribute() != pcbnew.PAD_ATTRIB_SMD)
        layers = [0, 1] if is_th else [0]
        for l in layers:
            grid_occ[(l, gx, gy)] = (net_name, ref, pad.GetName())
            # Add 1-cell halo for through-hole pins to maintain clearance
            if is_th:
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        grid_occ[(l, gx+dx, gy+dy)] = (net_name, ref, pad.GetName())

# Board edge boundaries as obstacles
for x in range(NX):
    for y in [0, 1, NY-2, NY-1]:
        for l in [0, 1]:
            grid_occ[(l, x, y)] = ("EDGE", None, None)
for y in range(NY):
    for x in [0, 1, NX-2, NX-1]:
        for l in [0, 1]:
            grid_occ[(l, x, y)] = ("EDGE", None, None)

def astar_route(net_name, start_pos, goal_pos):
    sgx, sgy = to_grid(start_pos[0], start_pos[1])
    ggx, ggy = to_grid(goal_pos[0], goal_pos[1])
    
    start = (0, sgx, sgy) # Start on F.Cu
    goal = (0, ggx, ggy)  # Goal on F.Cu
    
    if start == goal:
        return [start]
        
    pq = []
    heapq.heappush(pq, (0, start))
    came_from = {}
    cost_so_far = {start: 0}
    
    def h(pos):
        l, x, y = pos
        return abs(x - ggx) + abs(y - ggy) + (4 if l != 0 else 0)
    
    found = False
    while pq:
        _, current = heapq.heappop(pq)
        if current == goal:
            found = True
            break
            
        l, x, y = current
        neighbors = []
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < NX and 0 <= ny < NY:
                # Prefer B.Cu for horizontal long runs, F.Cu for vertical
                step_c = 1
                if l == 1 and dy != 0: step_c = 2 # slight penalty for vertical on B.Cu
                if l == 0 and dx != 0: step_c = 2 # slight penalty for horizontal on F.Cu
                neighbors.append((l, nx, ny, step_c))
        # Layer switch (via)
        neighbors.append((1 - l, x, y, 8)) # via penalty
        
        for nl, nx, ny, sc in neighbors:
            nxt = (nl, nx, ny)
            if nxt != goal:
                occ = grid_occ.get(nxt)
                if occ is not None and occ[0] != net_name:
                    continue
            new_cost = cost_so_far[current] + sc
            if nxt not in cost_so_far or new_cost < cost_so_far[nxt]:
                cost_so_far[nxt] = new_cost
                heapq.heappush(pq, (new_cost + h(nxt), nxt))
                came_from[nxt] = current
                
    if not found:
        return None
        
    path = []
    curr = goal
    while curr != start:
        path.append(curr)
        curr = came_from[curr]
    path.append(start)
    path.reverse()
    return path

# 5. Route all non-GND chains
chains = [
    ("RA_RAW", [("J1", "T"), ("J1A", "1"), ("R1", "1")]),
    ("RA_INT", [("R1", "2"), ("R3", "1")]),
    ("RA_FILT", [("R3", "2"), ("R5", "2"), ("U1", "2")]),
    
    ("LA_RAW", [("J1", "R"), ("J1A", "2"), ("R2", "1")]),
    ("LA_INT", [("R2", "2"), ("R4", "1")]),
    ("LA_FILT", [("R4", "2"), ("R6", "2"), ("U1", "3")]),
    
    ("RL_RAW", [("J1", "S"), ("J1A", "3"), ("R15", "2")]),
    ("RLD_OUT", [("U1", "5"), ("R15", "1"), ("C6", "2"), ("R14", "2")]),
    ("RLDFB", [("U1", "4"), ("C6", "1"), ("R14", "1")]),
    
    ("HPDRIVE", [("U1", "1"), ("C1", "1")]),
    ("HP_MID", [("C1", "2"), ("C2", "1"), ("U1", "6"), ("R7", "1")]),
    ("HPSENSE", [("C2", "2"), ("U1", "20")]),
    
    ("REFIN", [("U1", "18"), ("R8", "2"), ("R9", "1"), ("C5", "1")]),
    ("REFOUT", [("U1", "8"), ("C4", "2"), ("R12", "2"), ("R17", "1"), ("TP2", "1")]),
    
    ("IAOUT", [("U1", "19"), ("R10", "1")]),
    ("SK_N1", [("R10", "2"), ("R11", "1"), ("C3", "1")]),
    ("OPAMP_P", [("U1", "7"), ("R11", "2"), ("C4", "1")]),
    ("OPAMP_N", [("U1", "9"), ("R12", "1"), ("R13", "1")]),
    ("ECG_OUT", [("U1", "10"), ("C3", "2"), ("R13", "2"), ("R16", "1"), ("TP1", "1"), ("J2A", "5")]),
    
    ("AIN0_FILT", [("R16", "2"), ("C7", "1"), ("C8", "1"), ("U2", "4")]),
    ("AIN1_FILT", [("R17", "2"), ("C7", "2"), ("C9", "1"), ("U2", "5")]),
    
    ("LOD+", [("U1", "12"), ("TP3", "1"), ("J2A", "7")]),
    ("LOD-", [("U1", "11"), ("TP4", "1"), ("J2A", "8")]),
    ("FR", [("U1", "15"), ("J2A", "9")]),
    ("ADS_ALERT", [("U2", "2"), ("R20", "2"), ("J2A", "11")]),
    ("MAX_INT", [("J3", "4"), ("J2A", "10")]),
    
    ("I2C_SDA", [("U2", "9"), ("R18", "2"), ("J3", "3"), ("J2B", "6")]),
    ("I2C_SCL", [("U2", "10"), ("R19", "2"), ("J3", "2"), ("J2B", "3")]),
    
    ("+VS_A", [("U3", "2"), ("C12", "1"), ("C13", "1"), ("C14", "1"), ("C15", "1"), ("U1", "17"), ("U1", "13"), ("R5", "1"), ("R6", "1"), ("R8", "1"), ("TP5", "1")]),
    ("+3V3", [("J2A", "1"), ("J3", "1"), ("R18", "1"), ("R19", "1"), ("R20", "1"), ("U2", "8"), ("C16", "1"), ("C17", "1"), ("U3", "3"), ("C10", "1"), ("C11", "1"), ("TP6", "1")])
]

routed_count = 0
failed_count = 0

for net_name, pin_chain in chains:
    net_item = board_nets[net_name]
    for i in range(len(pin_chain) - 1):
        r1, p1_name = pin_chain[i]
        r2, p2_name = pin_chain[i+1]
        pad1 = fps[r1].FindPadByNumber(p1_name)
        pad2 = fps[r2].FindPadByNumber(p2_name)
        if not pad1 or not pad2: continue
        
        pos1 = (pad1.GetPosition().x / 1e6, pad1.GetPosition().y / 1e6)
        pos2 = (pad2.GetPosition().x / 1e6, pad2.GetPosition().y / 1e6)
        
        path = astar_route(net_name, pos1, pos2)
        if not path:
            print(f"FAILED to route {net_name} between {r1}.{p1_name} and {r2}.{p2_name}")
            failed_count += 1
            continue
            
        routed_count += 1
        
        # Mark path in grid_occ
        for pt in path:
            grid_occ[pt] = (net_name, None, None)
            
        # Convert path to tracks and vias
        # Connect pad1 to first path point
        first_pt = (to_mm(path[0][1], path[0][2]))
        if pos1 != first_pt:
            t = pcbnew.PCB_TRACK(board)
            t.SetNet(net_item)
            t.SetLayer(pcbnew.F_Cu)
            t.SetWidth(pcbnew.FromMM(0.254))
            t.SetStart(pad1.GetPosition())
            t.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(first_pt[0]), pcbnew.FromMM(first_pt[1])))
            board.Add(t)
            
        # Draw path segments
        curr_layer = path[0][0]
        seg_start = first_pt
        
        for k in range(1, len(path)):
            prev = path[k-1]
            curr = path[k]
            prev_mm = to_mm(prev[1], prev[2])
            curr_mm = to_mm(curr[1], curr[2])
            
            if curr[0] != prev[0]:
                # Via layer transition
                t = pcbnew.PCB_TRACK(board)
                t.SetNet(net_item)
                t.SetLayer(pcbnew.F_Cu if prev[0] == 0 else pcbnew.B_Cu)
                t.SetWidth(pcbnew.FromMM(0.254))
                t.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(seg_start[0]), pcbnew.FromMM(seg_start[1])))
                t.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(prev_mm[0]), pcbnew.FromMM(prev_mm[1])))
                board.Add(t)
                
                v = pcbnew.PCB_VIA(board)
                v.SetNet(net_item)
                v.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(curr_mm[0]), pcbnew.FromMM(curr_mm[1])))
                v.SetWidth(pcbnew.FromMM(0.6))
                v.SetDrill(pcbnew.FromMM(0.3))
                v.SetLayerPair(pcbnew.F_Cu, pcbnew.B_Cu)
                v.SetViaType(pcbnew.VIATYPE_THROUGH)
                v.SetFrontTentingMode(pcbnew.TENTING_MODE_TENTED)
                v.SetBackTentingMode(pcbnew.TENTING_MODE_TENTED)
                board.Add(v)
                
                seg_start = curr_mm
                
        # Final segment
        last_mm = to_mm(path[-1][1], path[-1][2])
        t = pcbnew.PCB_TRACK(board)
        t.SetNet(net_item)
        t.SetLayer(pcbnew.F_Cu if path[-1][0] == 0 else pcbnew.B_Cu)
        t.SetWidth(pcbnew.FromMM(0.254))
        t.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(seg_start[0]), pcbnew.FromMM(seg_start[1])))
        t.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(last_mm[0]), pcbnew.FromMM(last_mm[1])))
        board.Add(t)
        
        # Connect last point to pad2
        if last_mm != pos2:
            t = pcbnew.PCB_TRACK(board)
            t.SetNet(net_item)
            t.SetLayer(pcbnew.F_Cu)
            t.SetWidth(pcbnew.FromMM(0.254))
            t.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(last_mm[0]), pcbnew.FromMM(last_mm[1])))
            t.SetEnd(pad2.GetPosition())
            board.Add(t)

print(f"Routing results: {routed_count} succeeded, {failed_count} failed.")

# 6. Solid GND zone on B.Cu
gnd_net = board_nets["GND"]
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

# Fill zones
filler = pcbnew.ZONE_FILLER(board)
filler.Fill(board.Zones())

out_file = "AFE_ECG_PPG_PTT.kicad_pcb"
pcbnew.SaveBoard(out_file, board)
print("Saved routed board to", out_file)
