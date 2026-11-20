import json, uuid

BASE = 'DoAn/ECG_PPG_System/ECG_PPG_System_clean_base.kicad_pcb'
OUT  = 'DoAn/ECG_PPG_System/ECG_PPG_System.kicad_pcb'

def uid(): return str(uuid.uuid4())
f = lambda v: f'{v:.4f}'

def seg(net, layer, w, x1, y1, x2, y2):
    if abs(x1 - x2) < 1e-4 and abs(y1 - y2) < 1e-4: return ''
    return (f'\t(segment\n\t\t(start {f(x1)} {f(y1)})\n\t\t(end {f(x2)} {f(y2)})\n'
            f'\t\t(width {f(w)})\n\t\t(layer "{layer}")\n\t\t(net "{net}")\n'
            f'\t\t(uuid "{uid()}")\n\t)\n')

def via(net, x, y, size=0.6, drill=0.3):
    return (f'\t(via\n\t\t(at {f(x)} {f(y)})\n\t\t(size {f(size)})\n\t\t(drill {f(drill)})\n'
            f'\t\t(layers "F.Cu" "B.Cu")\n\t\t(net "{net}")\n'
            f'\t\t(uuid "{uid()}")\n\t)\n')

def zone(net, layer, pts):
    ptxt = '\n\t\t\t\t' + ' '.join(f'(xy {f(x)} {f(y)})' for x, y in pts)
    return (f'\t(zone\n\t\t(net "{net}")\n\t\t(layer "{layer}")\n\t\t(uuid "{uid()}")\n'
            f'\t\t(hatch edge 0.508)\n\t\t(connect_pads yes\n\t\t\t(clearance 0.2)\n\t\t)\n'
            f'\t\t(min_thickness 0.2)\n\t\t(filled_areas_thickness no)\n'
            f'\t\t(fill yes\n\t\t\t(thermal_gap 0.2)\n\t\t\t(thermal_bridge_width 0.35)\n\t\t\t(island_removal_mode 0)\n\t\t)\n'
            f'\t\t(polygon\n\t\t\t(pts{ptxt}\n\t\t\t)\n\t\t)\n\t)\n')

s = open(BASE).read()
pos_list = [i for i in (s.find('\n\t(segment\n'), s.find('\n\t(via\n'), s.find('\n\t(zone\n')) if i >= 0]
CUT = min(pos_list) if pos_list else s.rfind(')')
head = s[:CUT]

FC, BC = 'F.Cu', 'B.Cu'
SW = 0.25
PW = 0.35

routes = []
vias = []

def add_line(net, layer, w, pts):
    for p1, p2 in zip(pts, pts[1:]):
        routes.append((net, layer, w, p1[0], p1[1], p2[0], p2[1]))

def add_via(net, x, y):
    vias.append((net, round(x, 2), round(y, 2)))

# 1. RA_RAW: J2.1 (4.0, 11.0) to R4.1 (7.68, 11.5)
add_line('RA_RAW', FC, SW, [(4.0, 11.0), (5.5, 11.0), (5.5, 11.5), (7.68, 11.5)])

# 2. LA_RAW: J2.2 (4.0, 13.54) to R5.1 (7.68, 15.5)
add_line('LA_RAW', FC, SW, [(4.0, 13.54), (5.5, 13.54), (5.5, 15.5), (7.68, 15.5)])

# 3. RL_DRL: J2.3 (4.0, 16.08) to R12.2 (10.5, 22.82)
add_line('RL_DRL', FC, SW, [(4.0, 16.08), (6.0, 16.08), (6.0, 22.82), (10.5, 22.82)])

# 4. RA_FILT: R4.2 (9.32, 11.5), C5.1 (11.5, 14.28), C6.1 (11.5, 10.28), R6.1 (13.68, 9.5), R9.1 (13.18, 25.0), U1.2 (17.53, 17.37)
add_line('RA_FILT', FC, SW, [(9.32, 11.5), (10.2, 11.5), (10.2, 10.28), (11.5, 10.28), (11.5, 9.5), (13.68, 9.5)])
add_line('RA_FILT', FC, SW, [(10.2, 11.5), (10.2, 14.28), (11.5, 14.28)])
add_line('RA_FILT', FC, SW, [(10.2, 14.28), (10.2, 17.37), (17.53, 17.37)])
add_via('RA_FILT', 10.2, 17.37)
add_line('RA_FILT', BC, SW, [(10.2, 17.37), (10.2, 25.0), (13.18, 25.0)])
add_via('RA_FILT', 13.18, 25.0)

# 5. LA_FILT: R5.2 (9.32, 15.5), C5.2 (11.5, 12.72), C7.1 (11.5, 18.28), R7.1 (13.68, 13.5), R10.1 (17.18, 25.0), U1.3 (17.53, 18.64)
add_line('LA_FILT', FC, SW, [(9.32, 15.5), (11.5, 15.5), (11.5, 18.28)])
add_line('LA_FILT', FC, SW, [(9.32, 15.5), (9.32, 13.5), (13.68, 13.5)])
add_via('LA_FILT', 9.32, 13.5)
add_line('LA_FILT', BC, SW, [(9.32, 13.5), (9.32, 12.72), (11.5, 12.72)])
add_via('LA_FILT', 11.5, 12.72)
add_line('LA_FILT', FC, SW, [(11.5, 18.28), (15.5, 18.28), (15.5, 18.64), (17.53, 18.64)])
add_via('LA_FILT', 15.5, 18.28)
add_line('LA_FILT', BC, SW, [(15.5, 18.28), (15.5, 25.0), (17.18, 25.0)])
add_via('LA_FILT', 17.18, 25.0)

# 6. RG1 & RG2: U1.1 (17.53, 16.10), R8.1 (19.18, 11.5), U1.8 (22.48, 16.10), R8.2 (20.82, 11.5)
add_line('RG1', FC, SW, [(17.53, 16.10), (16.5, 16.10), (16.5, 11.5), (19.18, 11.5)])
add_line('RG2', FC, SW, [(22.48, 16.10), (22.48, 13.5), (20.82, 13.5), (20.82, 11.5)])

# 7. ECG_IA_OUT: U1.6 (22.48, 18.64) to C10.1 (26.68, 16.5)
add_line('ECG_IA_OUT', FC, SW, [(22.48, 18.64), (24.5, 18.64), (24.5, 16.5), (26.68, 16.5)])

# 8. DRL_CM: R9.2 (14.82, 25.0), R10.2 (18.82, 25.0), R11.1 (19.68, 23.0), C9.1 (23.68, 23.0), U2.5 (35.52, 19.27)
add_line('DRL_CM', FC, SW, [(14.82, 25.0), (18.82, 25.0), (18.82, 23.0), (19.68, 23.0), (23.68, 23.0)])
add_via('DRL_CM', 23.68, 23.0)
add_line('DRL_CM', BC, SW, [(23.68, 23.0), (33.0, 23.0), (33.0, 19.27), (35.52, 19.27)])

# 9. DRL_OUT: U2.7 (35.52, 21.81), R11.2 (21.32, 23.0), C9.2 (25.32, 23.0), R12.1 (10.5, 21.18)
add_line('DRL_OUT', FC, SW, [(10.5, 21.18), (12.0, 21.18), (12.0, 23.0), (21.32, 23.0)])
add_line('DRL_OUT', FC, SW, [(21.32, 23.0), (22.5, 23.0), (22.5, 21.81), (25.32, 21.81), (25.32, 23.0)])
add_via('DRL_OUT', 25.32, 23.0)
add_line('DRL_OUT', BC, SW, [(25.32, 23.0), (34.0, 23.0), (34.0, 21.81), (35.52, 21.81)])

# 10. ECG_HPF_OUT: C10.2 (28.32, 16.5) to R13.1 (27.5, 20.82) and R14.1 (30.18, 16.5)
add_line('ECG_HPF_OUT', FC, SW, [(28.32, 16.5), (30.18, 16.5)])
add_line('ECG_HPF_OUT', FC, SW, [(28.32, 16.5), (28.32, 20.82), (27.5, 20.82)])

# 11. ECG_LPF_NODE: R14.2 (31.82, 16.5), C12.1 (31.0, 13.28), R15.1 (33.18, 26.0), C11.1 (37.23, 26.0)
add_line('ECG_LPF_NODE', FC, SW, [(31.82, 16.5), (31.0, 16.5), (31.0, 13.28)])
add_line('ECG_LPF_NODE', FC, SW, [(31.82, 16.5), (31.82, 24.5), (33.18, 24.5), (33.18, 26.0)])
add_line('ECG_LPF_NODE', FC, SW, [(33.18, 24.5), (37.23, 24.5), (37.23, 26.0)])

# 12. ECG_LPF_IN: R15.2 (34.82, 26.0) to U2.10 (40.48, 19.27)
add_line('ECG_LPF_IN', FC, SW, [(34.82, 26.0), (36.0, 26.0), (36.0, 19.27), (40.48, 19.27)])

# 13. ECG_FB: U2.9 (40.48, 20.54), R16.1 (34.0, 28.68), R17.1 (37.18, 29.5)
add_line('ECG_FB', FC, SW, [(34.0, 28.68), (35.5, 28.68), (35.5, 29.5), (37.18, 29.5)])
add_via('ECG_FB', 37.18, 29.5)
add_line('ECG_FB', BC, SW, [(37.18, 29.5), (37.18, 20.54), (40.48, 20.54)])
add_via('ECG_FB', 40.48, 20.54)

# 14. ECG_OUT: U2.8 (40.48, 21.81), C11.2 (38.77, 26.0), R17.2 (38.83, 29.5), J4.3 (66.5, 17.08)
add_line('ECG_OUT', FC, SW, [(38.77, 26.0), (38.77, 27.5), (38.83, 27.5), (38.83, 29.5)])
add_via('ECG_OUT', 38.83, 29.5)
add_line('ECG_OUT', BC, SW, [(38.83, 29.5), (42.5, 29.5), (42.5, 21.81), (40.48, 21.81)])
add_via('ECG_OUT', 40.48, 21.81)
add_line('ECG_OUT', BC, SW, [(42.5, 29.5), (42.5, 33.5), (64.5, 33.5), (64.5, 17.08), (66.5, 17.08)])

# 15. LED_DRV: J3.2 (4.0, 24.54) to R19.2 (9.32, 31.0)
add_line('LED_DRV', FC, SW, [(4.0, 24.54), (7.0, 24.54), (7.0, 31.0), (9.32, 31.0)])

# 16. PD_ANODE: J3.3 (4.0, 27.08), R18.1 (12.68, 31.0), C14.1 (16.68, 31.0), U2.12 (40.48, 16.73)
add_line('PD_ANODE', FC, SW, [(4.0, 27.08), (11.0, 27.08), (11.0, 31.0), (12.68, 31.0), (16.68, 31.0)])
add_via('PD_ANODE', 16.68, 31.0)
add_line('PD_ANODE', BC, SW, [(16.68, 31.0), (16.68, 35.0), (41.0, 35.0), (41.0, 16.73), (40.48, 16.73)])
add_via('PD_ANODE', 40.48, 16.73)

# 17. PPG_TIA_OUT: U2.14 (40.48, 14.19), R18.2 (14.32, 31.0), C14.2 (18.32, 31.0), C15.1 (44.18, 23.0)
add_line('PPG_TIA_OUT', FC, SW, [(14.32, 31.0), (18.32, 31.0)])
add_via('PPG_TIA_OUT', 18.32, 31.0)
add_line('PPG_TIA_OUT', BC, SW, [(18.32, 31.0), (18.32, 33.0), (43.0, 33.0), (43.0, 14.19), (40.48, 14.19)])
add_via('PPG_TIA_OUT', 40.48, 14.19)
add_line('PPG_TIA_OUT', FC, SW, [(40.48, 14.19), (42.5, 14.19), (42.5, 23.0), (44.18, 23.0)])

# 18. PPG_HPF_OUT: C15.2 (45.82, 23.0) to R20.1 (48.18, 23.0) and R21.1 (44.18, 27.0)
add_line('PPG_HPF_OUT', FC, SW, [(45.82, 23.0), (48.18, 23.0)])
add_line('PPG_HPF_OUT', FC, SW, [(45.82, 23.0), (45.82, 25.5), (44.18, 25.5), (44.18, 27.0)])

# 19. PPG_LPF_NODE: R21.2 (45.82, 27.0), R22.1 (48.18, 27.0), C16.1 (44.18, 31.0)
add_line('PPG_LPF_NODE', FC, SW, [(45.82, 27.0), (45.82, 29.5), (44.18, 29.5), (44.18, 31.0)])
add_via('PPG_LPF_NODE', 45.82, 27.0)
add_line('PPG_LPF_NODE', BC, SW, [(45.82, 27.0), (45.82, 25.0), (48.18, 25.0), (48.18, 27.0)])
add_via('PPG_LPF_NODE', 48.18, 27.0)

# 20. PPG_LPF_IN: R22.2 (49.82, 27.0), C17.1 (48.23, 31.0), U3.3 (53.52, 18.64)
add_line('PPG_LPF_IN', FC, SW, [(49.82, 27.0), (48.23, 27.0), (48.23, 31.0)])
add_line('PPG_LPF_IN', FC, SW, [(49.82, 27.0), (51.5, 27.0), (51.5, 18.64), (53.52, 18.64)])

# 21. PPG_FB: U3.2 (53.52, 17.37), R23.1 (44.18, 35.0), R24.1 (48.18, 35.0)
add_line('PPG_FB', FC, SW, [(44.18, 35.0), (48.18, 35.0)])
add_via('PPG_FB', 48.18, 35.0)
add_line('PPG_FB', BC, SW, [(48.18, 35.0), (52.5, 35.0), (52.5, 17.37), (53.52, 17.37)])
add_via('PPG_FB', 53.52, 17.37)

# 22. PPG_OUT: U3.1 (53.52, 16.10), C16.2 (45.82, 31.0), R24.2 (49.82, 35.0), U3.5 (58.48, 19.90), J4.4 (66.5, 19.62)
add_line('PPG_OUT', FC, SW, [(45.82, 31.0), (49.82, 31.0), (49.82, 35.0)])
add_via('PPG_OUT', 49.82, 35.0)
add_line('PPG_OUT', BC, SW, [(49.82, 35.0), (55.0, 35.0), (55.0, 16.10), (53.52, 16.10)])
add_via('PPG_OUT', 53.52, 16.10)
add_line('PPG_OUT', FC, SW, [(58.48, 19.90), (62.0, 19.90), (62.0, 19.62), (66.5, 19.62)])
add_via('PPG_OUT', 58.48, 19.90)
add_line('PPG_OUT', BC, SW, [(58.48, 19.90), (58.48, 16.10), (55.0, 16.10)])

# 23. VREF_THR: U3.6 (58.48, 18.64) to R25.2 (53.82, 4.0) and R26.1 (56.18, 4.0)
add_line('VREF_THR', FC, SW, [(53.82, 4.0), (56.18, 4.0)])
add_via('VREF_THR', 56.18, 4.0)
add_line('VREF_THR', BC, SW, [(56.18, 4.0), (57.0, 4.0), (57.0, 18.64), (58.48, 18.64)])
add_via('VREF_THR', 58.48, 18.64)

# 24. PULSE_TRIG: U3.7 (58.48, 17.37) to R27.1 (59.18, 10.5) and J4.5 (66.5, 22.16)
add_line('PULSE_TRIG', FC, SW, [(58.48, 17.37), (59.18, 17.37), (59.18, 10.5)])
add_line('PULSE_TRIG', FC, SW, [(59.18, 17.37), (64.0, 17.37), (64.0, 22.16), (66.5, 22.16)])

# 25. LEDs
add_line('NET_D1_R3', FC, SW, [(16.44, 4.0), (20.32, 4.0)])
add_line('NET_D2_R27', FC, SW, [(60.82, 10.5), (62.0, 10.5), (62.0, 5.06)])

# 26. VMID: R1.2 (36.82, 4.0), R2.1 (38.68, 4.0), C3.1 (42.05, 4.0), C4.1 (45.73, 4.0), U2.3 (35.52, 16.73)
add_line('VMID', FC, SW, [(36.82, 4.0), (38.68, 4.0), (42.05, 4.0), (45.73, 4.0)])
add_line('VMID', FC, SW, [(36.82, 4.0), (36.82, 16.73), (35.52, 16.73)])

# 27. VREF (Clean dedicated distribution on B.Cu):
add_via('VREF', 35.52, 14.19)
add_via('VREF', 35.52, 15.46)
add_line('VREF', BC, PW, [(35.52, 14.19), (34.0, 14.19), (34.0, 38.0)])
add_line('VREF', BC, PW, [(35.52, 15.46), (34.0, 15.46)])
# U2.6 (35.52, 20.54)
add_line('VREF', BC, SW, [(34.0, 20.54), (35.52, 20.54)])
add_via('VREF', 35.52, 20.54)
# U2.13 (40.48, 15.46)
add_line('VREF', BC, SW, [(34.0, 15.46), (40.48, 15.46)])
add_via('VREF', 40.48, 15.46)
# Bottom VREF spine on B.Cu at Y = 38.0:
add_line('VREF', BC, PW, [(15.32, 38.0), (63.0, 38.0)])
# Tap to J4.6 (66.5, 24.70):
add_line('VREF', BC, SW, [(63.0, 38.0), (63.0, 24.70), (66.5, 24.70)])
# Tap to R16.2 (34.0, 30.32):
add_line('VREF', BC, SW, [(34.0, 30.32), (34.0, 38.0)])
add_via('VREF', 34.0, 30.32)
# Tap to R23.2 (45.82, 35.0):
add_line('VREF', BC, SW, [(45.82, 35.0), (45.82, 38.0)])
add_via('VREF', 45.82, 35.0)
# Tap to C17.2 (49.77, 31.0):
add_line('VREF', BC, SW, [(49.77, 31.0), (49.77, 38.0)])
add_via('VREF', 49.77, 31.0)
# Tap to R25.1 (52.18, 4.0) & R20.2 (49.82, 23.0):
add_via('VREF', 52.18, 4.0)
add_line('VREF', BC, SW, [(52.18, 4.0), (52.18, 23.0), (49.82, 23.0)])
add_via('VREF', 49.82, 23.0)
add_line('VREF', BC, SW, [(52.18, 23.0), (52.18, 38.0)])
# Left side taps: R6.2 (15.32, 9.5), R7.2 (15.32, 13.5), U1.5 (22.48, 19.90), R13.2 (27.5, 19.18), C12.2 (31.0, 11.68)
add_line('VREF', FC, SW, [(15.32, 9.5), (15.32, 13.5)])
add_via('VREF', 15.32, 13.5)
add_line('VREF', BC, PW, [(15.32, 13.5), (15.32, 38.0)])
add_line('VREF', BC, SW, [(15.32, 19.90), (22.48, 19.90)])
add_via('VREF', 22.48, 19.90)
add_line('VREF', BC, SW, [(27.5, 19.18), (27.5, 38.0)])
add_via('VREF', 27.5, 19.18)
add_line('VREF', BC, SW, [(31.0, 11.68), (31.0, 38.0)])
add_via('VREF', 31.0, 11.68)

# 28. VCC (Clean top margin distribution on B.Cu):
add_line('VCC', BC, PW, [(7.0, 1.8), (64.0, 1.8)])
add_via('VCC', 30.0, 4.0)
add_line('VCC', BC, PW, [(30.0, 4.0), (30.0, 1.8)])
for vx in (7.45, 11.18, 18.68, 35.18):
    add_via('VCC', vx, 4.0)
    add_line('VCC', BC, PW, [(vx, 4.0), (vx, 1.8)])
# U1.7 & C8.1
add_via('VCC', 23.0, 11.68)
add_line('VCC', BC, PW, [(23.0, 11.68), (23.0, 1.8)])
add_line('VCC', FC, PW, [(23.0, 11.68), (23.0, 17.37), (22.48, 17.37)])
# U2.4 & C13.1
add_via('VCC', 37.18, 10.5)
add_line('VCC', BC, PW, [(37.18, 10.5), (37.18, 1.8)])
add_line('VCC', BC, PW, [(37.18, 10.5), (37.18, 18.0), (35.52, 18.0)])
add_via('VCC', 35.52, 18.0)
# U3.8 & C18.1
add_via('VCC', 55.18, 10.5)
add_line('VCC', BC, PW, [(55.18, 10.5), (55.18, 1.8)])
add_line('VCC', FC, PW, [(55.18, 10.5), (58.48, 10.5), (58.48, 16.10)])
# J4.1
add_line('VCC', BC, PW, [(64.0, 1.8), (64.0, 12.0), (66.5, 12.0)])
# J3.1 & R19.1
add_via('VCC', 7.68, 31.0)
add_line('VCC', BC, PW, [(7.0, 1.8), (2.0, 1.8), (2.0, 31.0), (7.68, 31.0)])
add_line('VCC', BC, PW, [(2.0, 22.0), (4.0, 22.0)])

# Assemble board file
r_out = []
for net, layer, w, x1, y1, x2, y2 in routes:
    r_out.append(seg(net, layer, w, x1, y1, x2, y2))

seen = set()
for net, vx, vy in vias:
    k = (net, vx, vy)
    if k not in seen:
        seen.add(k)
        r_out.append(via(net, vx, vy))

bp = [(0.5, 0.5), (69.5, 0.5), (69.5, 39.5), (0.5, 39.5)]
r_out.append(zone('GND', 'F.Cu', bp))
r_out.append(zone('GND', 'B.Cu', bp))

open(OUT, 'w').write(head + ''.join(r_out) + ')\n')
print(f"Built master clean board with {len(routes)} tracks, {len(seen)} vias!")
