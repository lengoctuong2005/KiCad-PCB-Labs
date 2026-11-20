import json, uuid

BASE = 'DoAn/EMG_Sensor/EMG_Sensor.kicad_pcb'
OUT  = 'DoAn/EMG_Sensor/EMG_Sensor.kicad_pcb'

def uid(): return str(uuid.uuid4())
f = lambda v: f'{v:.4f}'

def seg(net, layer, w, x1, y1, x2, y2):
    if abs(x1 - x2) < 1e-5 and abs(y1 - y2) < 1e-5: return ''
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
            f'\t\t(hatch edge 0.508)\n\t\t(connect_pads yes\n\t\t\t(clearance 0.2000)\n\t\t)\n'
            f'\t\t(min_thickness 0.2000)\n\t\t(filled_areas_thickness no)\n'
            f'\t\t(fill yes\n\t\t\t(thermal_gap 0.2000)\n\t\t\t(thermal_bridge_width 0.3500)\n\t\t)\n'
            f'\t\t(polygon\n\t\t\t(pts{ptxt}\n\t\t\t)\n\t\t)\n\t)\n')

s = open(BASE).read()
pos_list = [i for i in (s.find('\n\t(segment\n'), s.find('\n\t(via\n'), s.find('\n\t(zone\n')) if i >= 0]
CUT = min(pos_list) if pos_list else s.rfind(')')
head = s[:CUT]

r = []
FC, BC = 'F.Cu', 'B.Cu'
SW = 0.25
PW = 0.35

# 1. IN_PLUS_RAW: J2.1 (4.0, 15.0) to R4.1 (7.18, 12.0)
r.append(seg('IN_PLUS_RAW', FC, SW, 4.0, 15.0, 5.5, 15.0))
r.append(seg('IN_PLUS_RAW', FC, SW, 5.5, 15.0, 5.5, 12.0))
r.append(seg('IN_PLUS_RAW', FC, SW, 5.5, 12.0, 7.18, 12.0))

# 2. IN_MINUS_RAW: J2.2 (4.0, 17.54) to R5.1 (7.18, 16.0)
r.append(seg('IN_MINUS_RAW', FC, SW, 4.0, 17.54, 5.5, 17.54))
r.append(seg('IN_MINUS_RAW', FC, SW, 5.5, 17.54, 5.5, 16.0))
r.append(seg('IN_MINUS_RAW', FC, SW, 5.5, 16.0, 7.18, 16.0))

# 3. IN_PLUS_FILT: R4.2 (8.82, 12.0), C5.1 (10.5, 14.78), C6.1 (10.5, 9.78), R6.1 (13.0, 9.82), U1.3 (15.03, 14.63)
r.append(seg('IN_PLUS_FILT', FC, SW, 8.82, 12.0, 9.8, 12.0))
r.append(seg('IN_PLUS_FILT', FC, SW, 9.8, 12.0, 9.8, 14.78))
r.append(seg('IN_PLUS_FILT', FC, SW, 9.8, 14.78, 10.5, 14.78))
r.append(seg('IN_PLUS_FILT', FC, SW, 10.5, 14.78, 15.03, 14.63))
r.append(seg('IN_PLUS_FILT', FC, SW, 9.8, 12.0, 9.8, 9.78))
r.append(seg('IN_PLUS_FILT', FC, SW, 9.8, 9.78, 10.5, 9.78))
r.append(seg('IN_PLUS_FILT', FC, SW, 10.5, 9.78, 13.0, 9.82))

# 4. IN_MINUS_FILT: R5.2 (8.82, 16.0), C5.2 (10.5, 13.22), C7.1 (10.5, 19.78), R7.1 (13.0, 19.82), U1.2 (15.03, 13.37)
# Use B.Cu bridge to avoid crossing IN_PLUS_FILT
r.append(seg('IN_MINUS_FILT', FC, SW, 8.82, 16.0, 9.0, 16.0))
r.append(via('IN_MINUS_FILT', 9.0, 16.0))
r.append(seg('IN_MINUS_FILT', BC, SW, 9.0, 16.0, 9.0, 13.22))
r.append(seg('IN_MINUS_FILT', BC, SW, 9.0, 13.22, 10.5, 13.22))
r.append(via('IN_MINUS_FILT', 10.5, 13.22))
r.append(seg('IN_MINUS_FILT', FC, SW, 10.5, 13.22, 15.03, 13.37))
# To C7.1 & R7.1
r.append(seg('IN_MINUS_FILT', FC, SW, 8.82, 16.0, 8.82, 19.78))
r.append(seg('IN_MINUS_FILT', FC, SW, 8.82, 19.78, 10.5, 19.78))
r.append(seg('IN_MINUS_FILT', FC, SW, 10.5, 19.78, 13.0, 19.82))

# 5. RG1 & RG2 (U1 Gain resistor R8)
r.append(seg('RG1', FC, SW, 15.03, 12.10, 15.03, 8.5))
r.append(seg('RG1', FC, SW, 15.03, 8.5, 16.68, 8.5))
r.append(seg('RG2', FC, SW, 19.98, 12.10, 19.98, 8.5))
r.append(seg('RG2', FC, SW, 19.98, 8.5, 18.32, 8.5))

# 6. VOUT_IA (U1.6 to C9.1)
r.append(seg('VOUT_IA', FC, SW, 19.98, 14.63, 22.18, 14.64))

# 7. HPF_OUT (C9.2 to R10.1 and R9.1)
r.append(seg('HPF_OUT', FC, SW, 23.82, 14.64, 25.68, 14.64))
r.append(seg('HPF_OUT', FC, SW, 23.82, 14.64, 23.82, 19.32))
r.append(seg('HPF_OUT', FC, SW, 23.82, 19.32, 23.0, 19.32))

# 8. LPF_NODE (R10.2 to R11.1 and C10.1)
r.append(seg('LPF_NODE', FC, SW, 27.32, 14.64, 28.68, 14.64))
r.append(seg('LPF_NODE', FC, SW, 27.32, 14.64, 27.18, 18.5))

# 9. LPF_IN (R11.2 to U2.5 and C11.1)
r.append(seg('LPF_IN', FC, SW, 30.32, 14.64, 31.0, 14.64))
r.append(seg('LPF_IN', FC, SW, 31.0, 14.64, 31.0, 16.27))
r.append(seg('LPF_IN', FC, SW, 31.0, 16.27, 32.52, 16.27))
r.append(seg('LPF_IN', FC, SW, 31.0, 14.64, 31.0, 11.78))
r.append(seg('LPF_IN', FC, SW, 31.0, 11.78, 29.5, 11.78))

# 10. LPF_FB (R12.1, R13.1, U2.6)
r.append(seg('LPF_FB', FC, SW, 26.18, 22.0, 29.68, 22.0))
r.append(seg('LPF_FB', FC, SW, 29.68, 22.0, 31.5, 22.0))
r.append(seg('LPF_FB', FC, SW, 31.5, 22.0, 31.5, 17.54))
r.append(seg('LPF_FB', FC, SW, 31.5, 17.54, 32.52, 17.54))

# 11. RAW_EMG (U2.7 to R13.2, C10.2, R14.1, R17.1, J3.3)
r.append(seg('RAW_EMG', FC, SW, 32.52, 18.81, 31.32, 22.0))
r.append(seg('RAW_EMG', FC, SW, 31.32, 22.0, 28.82, 18.5))
r.append(seg('RAW_EMG', FC, SW, 32.52, 18.81, 34.18, 23.5))
# Cross to R17.1 & J3.3 via B.Cu
r.append(via('RAW_EMG', 34.5, 20.0))
r.append(seg('RAW_EMG', FC, SW, 32.52, 18.81, 34.5, 20.0))
r.append(seg('RAW_EMG', BC, SW, 34.5, 20.0, 39.5, 20.0))
r.append(seg('RAW_EMG', BC, SW, 39.5, 20.0, 39.5, 14.0))
r.append(seg('RAW_EMG', BC, SW, 39.5, 14.0, 40.68, 14.0))
r.append(via('RAW_EMG', 40.68, 14.0))
# J3.3 (46.5, 20.08)
r.append(seg('RAW_EMG', BC, SW, 39.5, 20.0, 46.5, 20.08))

# 12. RECT_OUT (U2.8 to D2.1 and D3.2)
r.append(seg('RECT_OUT', FC, SW, 37.48, 18.81, 39.0, 18.81))
r.append(seg('RECT_OUT', FC, SW, 39.0, 18.81, 39.0, 22.65))
r.append(seg('RECT_OUT', FC, SW, 39.0, 22.65, 40.0, 22.65))
r.append(seg('RECT_OUT', FC, SW, 39.0, 18.81, 43.0, 18.81))
r.append(seg('RECT_OUT', FC, SW, 43.0, 18.81, 43.0, 19.35))

# 13. RECT_IN (U2.9 to D2.2, R14.2, R15.1)
r.append(seg('RECT_IN', FC, SW, 37.48, 17.54, 40.0, 17.54))
r.append(seg('RECT_IN', FC, SW, 40.0, 17.54, 40.0, 19.35))
r.append(seg('RECT_IN', FC, SW, 37.48, 17.54, 37.0, 17.54))
r.append(seg('RECT_IN', FC, SW, 37.0, 17.54, 37.0, 23.5))
r.append(seg('RECT_IN', FC, SW, 37.0, 23.5, 35.82, 23.5))
r.append(seg('RECT_IN', FC, SW, 40.0, 19.35, 40.0, 25.0))
r.append(seg('RECT_IN', FC, SW, 40.0, 25.0, 40.68, 25.0))

# 14. RECT_HALF (D3.1 to R15.2 and R16.1)
# Route entirely on F.Cu at X=42.32
r.append(seg('RECT_HALF', FC, SW, 43.0, 22.65, 42.32, 25.0))
r.append(seg('RECT_HALF', FC, SW, 43.0, 22.65, 43.0, 17.5))
r.append(seg('RECT_HALF', FC, SW, 43.0, 17.5, 40.68, 17.5))
r.append(seg('RECT_HALF', FC, SW, 40.68, 17.5, 40.68, 16.5))

# 15. ENV_IN (U2.13 to R16.2, R17.2, R18.1, C12.1)
r.append(seg('ENV_IN', FC, SW, 37.48, 12.46, 38.5, 12.46))
r.append(seg('ENV_IN', FC, SW, 38.5, 12.46, 38.5, 16.5))
r.append(seg('ENV_IN', FC, SW, 38.5, 16.5, 42.32, 16.5))
r.append(seg('ENV_IN', FC, SW, 38.5, 14.0, 42.32, 14.0))
r.append(seg('ENV_IN', FC, SW, 38.5, 12.46, 38.5, 11.5))
r.append(seg('ENV_IN', FC, SW, 38.5, 11.5, 40.68, 11.5))
r.append(seg('ENV_IN', FC, SW, 38.5, 11.5, 38.5, 9.0))
r.append(seg('ENV_IN', FC, SW, 38.5, 9.0, 40.68, 9.0))

# 16. ENV_EMG (U2.14 to R18.2, C12.2, J3.4, R19.1)
r.append(seg('ENV_EMG', FC, SW, 37.48, 11.19, 42.32, 11.19))
r.append(seg('ENV_EMG', FC, SW, 42.32, 11.19, 42.32, 11.5))
r.append(seg('ENV_EMG', FC, SW, 42.32, 11.19, 42.32, 9.0))
# J3.4 at (46.5, 22.62)
r.append(seg('ENV_EMG', FC, SW, 42.32, 11.19, 45.0, 11.19))
r.append(seg('ENV_EMG', FC, SW, 45.0, 11.19, 45.0, 22.62))
r.append(seg('ENV_EMG', FC, SW, 45.0, 22.62, 46.5, 22.62))
# Long run to R19.1 (13.5, 24.82) on B.Cu
r.append(via('ENV_EMG', 45.0, 22.62))
r.append(seg('ENV_EMG', BC, SW, 45.0, 22.62, 45.0, 26.5))
r.append(seg('ENV_EMG', BC, SW, 45.0, 26.5, 13.5, 26.5))
r.append(seg('ENV_EMG', BC, SW, 13.5, 26.5, 13.5, 24.82))
r.append(via('ENV_EMG', 13.5, 24.82))

# 17. LEDs (NET_D1_R1 and NET_D4_R19)
r.append(seg('NET_D1_R1', FC, SW, 14.56, 4.0, 18.68, 4.0))
r.append(seg('NET_D4_R19', FC, SW, 13.5, 23.18, 17.94, 23.18))
r.append(seg('NET_D4_R19', FC, SW, 17.94, 23.18, 17.94, 24.0))

# 18. VMID (R2.2, R3.1, C3.1, C4.1 to U2.3)
r.append(seg('VMID', FC, SW, 31.82, 4.0, 33.68, 4.0))
r.append(seg('VMID', FC, SW, 33.68, 4.0, 36.95, 4.0))
r.append(seg('VMID', FC, SW, 36.95, 4.0, 40.68, 4.0))
r.append(seg('VMID', FC, SW, 31.82, 4.0, 31.82, 13.73))
r.append(seg('VMID', FC, SW, 31.82, 13.73, 32.52, 13.73))

# 19. VREF (U2.1 & U2.2 to R12.2, U2.10, U2.12, U1.5, R9.2, C11.2, R6.2, R7.2, J2.3)
r.append(seg('VREF', FC, SW, 32.52, 11.19, 32.52, 12.46))
r.append(seg('VREF', FC, SW, 32.52, 12.46, 31.0, 12.46))
r.append(via('VREF', 31.0, 12.46))
# B.Cu trunk from (31.0, 12.46) to J2.3 (4.0, 20.08)
r.append(seg('VREF', BC, PW, 31.0, 12.46, 31.0, 7.0))
r.append(seg('VREF', BC, PW, 31.0, 7.0, 2.0, 7.0))
r.append(seg('VREF', BC, PW, 2.0, 7.0, 2.0, 20.08))
r.append(seg('VREF', BC, PW, 2.0, 20.08, 4.0, 20.08))
# Taps from VREF bus on B.Cu to R6.2, R7.2, C11.2:
r.append(seg('VREF', BC, SW, 13.0, 7.0, 13.0, 8.18))
r.append(via('VREF', 13.0, 8.18))
r.append(seg('VREF', BC, SW, 13.0, 7.0, 13.0, 18.18))
r.append(via('VREF', 13.0, 18.18))
r.append(seg('VREF', BC, SW, 29.5, 7.0, 29.5, 10.22))
r.append(via('VREF', 29.5, 10.22))
# Right taps on B.Cu to U2.10 and U2.12:
r.append(seg('VREF', BC, SW, 31.0, 12.46, 36.5, 12.46))
r.append(via('VREF', 36.5, 12.46))
r.append(seg('VREF', FC, SW, 36.5, 12.46, 36.5, 13.73))
r.append(seg('VREF', FC, SW, 36.5, 13.73, 37.48, 13.73)) # U2.12
r.append(seg('VREF', FC, SW, 36.5, 13.73, 36.5, 16.27))
r.append(seg('VREF', FC, SW, 36.5, 16.27, 37.48, 16.27)) # U2.10
# Taps to U1.5, R9.2, R12.2:
r.append(via('VREF', 25.0, 17.68))
r.append(seg('VREF', BC, SW, 31.0, 12.46, 31.0, 17.68))
r.append(seg('VREF', BC, SW, 31.0, 17.68, 25.0, 17.68))
r.append(seg('VREF', FC, SW, 25.0, 17.68, 23.0, 17.68)) # R9.2
r.append(seg('VREF', FC, SW, 25.0, 17.68, 25.0, 15.90))
r.append(seg('VREF', FC, SW, 25.0, 15.90, 19.98, 15.90)) # U1.5
r.append(seg('VREF', FC, SW, 25.0, 17.68, 27.82, 17.68))
r.append(seg('VREF', FC, SW, 27.82, 17.68, 27.82, 22.0)) # R12.2

# 20. VCC (Power distribution on B.Cu trunk at Y = 2.0)
r.append(seg('VCC', FC, PW, 25.0, 3.5, 25.0, 2.0))
r.append(via('VCC', 25.0, 2.0))
r.append(seg('VCC', BC, PW, 7.45, 2.0, 46.5, 2.0))
# Taps to C1.1, C2.1, D1.2, R2.1, U1.7, U2.4, J3.1:
for vx, vy in [(7.45, 4.0), (11.18, 4.0), (16.44, 4.0), (30.18, 4.0)]:
    r.append(seg('VCC', BC, PW, vx, 2.0, vx, 4.0))
    r.append(via('VCC', vx, 4.0))
# U1.7 (19.98, 13.37) & C8.1 (20.0, 10.28)
r.append(seg('VCC', BC, PW, 20.0, 2.0, 20.0, 10.28))
r.append(via('VCC', 20.0, 10.28))
r.append(seg('VCC', FC, PW, 20.0, 10.28, 21.2, 10.28))
r.append(seg('VCC', FC, PW, 21.2, 10.28, 21.2, 13.37))
r.append(seg('VCC', FC, PW, 21.2, 13.37, 19.98, 13.37))
# U2.4 (32.52, 15.00) & C13.1 (34.18, 8.5)
r.append(seg('VCC', BC, PW, 34.18, 2.0, 34.18, 8.5))
r.append(via('VCC', 34.18, 8.5))
r.append(seg('VCC', BC, PW, 32.52, 2.0, 32.52, 15.00))
r.append(via('VCC', 32.52, 15.00))
# J3.1 (46.5, 15.00)
r.append(seg('VCC', BC, PW, 46.5, 2.0, 46.5, 15.00))

# GND stitching vias
gnd_vias = [
    (5.0, 5.0), (45.0, 5.0), (5.0, 25.0), (45.0, 25.0),
    (15.0, 24.0), (20.0, 24.0), (25.0, 24.0), (30.0, 25.0),
    (15.0, 6.0), (25.0, 6.0), (35.0, 6.0), (40.0, 6.0),
    (2.8, 5.0), (47.2, 5.0), (2.8, 25.0), (47.2, 25.0)
]
for gx, gy in gnd_vias:
    r.append(via('GND', gx, gy))

bp = [(0.5, 0.5), (49.5, 0.5), (49.5, 29.5), (0.5, 29.5)]
r.append(zone('GND', 'F.Cu', bp))
r.append(zone('GND', 'B.Cu', bp))

open(OUT, 'w').write(head + ''.join(r) + ')\n')
print("Master EMG route applied successfully!")
