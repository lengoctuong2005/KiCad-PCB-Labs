import json, uuid

BASE = 'DoAn/ECG_PPG_System/ECG_PPG_System_clean_base.kicad_pcb'
OUT  = 'DoAn/ECG_PPG_System/ECG_PPG_System.kicad_pcb'

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
            f'\t\t(hatch edge 0.508)\n\t\t(connect_pads yes\n\t\t\t(clearance 0.2)\n\t\t)\n'
            f'\t\t(min_thickness 0.2)\n\t\t(filled_areas_thickness no)\n'
            f'\t\t(fill yes\n\t\t\t(thermal_gap 0.2)\n\t\t\t(thermal_bridge_width 0.35)\n\t\t\t(island_removal_mode 0)\n\t\t)\n'
            f'\t\t(polygon\n\t\t\t(pts{ptxt}\n\t\t\t)\n\t\t)\n\t)\n')

s = open(BASE).read()
pos_list = [i for i in (s.find('\n\t(segment\n'), s.find('\n\t(via\n'), s.find('\n\t(zone\n')) if i >= 0]
CUT = min(pos_list) if pos_list else s.rfind(')')
head = s[:CUT]

d = json.load(open('/tmp/ecg_fast_flawless.json'))
routes = d['routes']
vias = d['vias']
LAYERS = {0: 'F.Cu', 1: 'B.Cu'}

clean_routes = []
for r_item in routes:
    net, L, w, x1, y1, x2, y2 = r_item
    layer_name = LAYERS[L] if isinstance(L, int) else L

    # Filter 1: VREF near C4 (Y <= 5.5, X >= 44.0)
    if net == 'VREF' and layer_name == 'F.Cu' and min(y1, y2) <= 5.5 and max(x1, x2) >= 44.0:
        continue
    # Filter 2: VCC near J3.4
    if net == 'VCC' and layer_name == 'F.Cu' and min(x1, x2) <= 6.5 and max(y1, y2) >= 27.0:
        continue
    # Filter 3: VREF near U2.7
    if net == 'VREF' and layer_name == 'F.Cu' and abs(x1 - 35.52) < 1.0 and min(y1, y2) >= 20.0 and max(y1, y2) <= 22.0:
        continue
    # Filter 4: ECG_FB going south near U2.8
    if net == 'ECG_FB' and layer_name == 'F.Cu' and abs(x1 - 40.48) < 1.0 and max(y1, y2) >= 21.0:
        continue

    clean_routes.append([net, layer_name, w, x1, y1, x2, y2])

# Add SOIC stubs for pins exiting to B.Cu (except U2.8 and U2.9 which are handled separately):
pads = json.load(open('/tmp/ecg_pads_clean_base.json'))['pads']
for p in pads:
    if p['ref'].startswith('U') and not (p['ref'] == 'U2' and p['num'] in ('8', '9')):
        dx = -1.6 if int(p['num']) <= (4 if p['ref'] in ('U1','U3') else 7) else 1.6
        ex_x = round(p['x'] + dx, 2)
        py = round(p['y'], 2)
        touches_bcu = False
        for net, layer, w, x1, y1, x2, y2 in clean_routes:
            if layer == 'B.Cu' and net == p['net']:
                if (abs(x1 - ex_x) < 0.25 and abs(y1 - py) < 0.25) or (abs(x2 - ex_x) < 0.25 and abs(y2 - py) < 0.25):
                    touches_bcu = True; break
        if touches_bcu:
            clean_routes.append([p['net'], 'F.Cu', 0.25, p['x'], p['y'], ex_x, py])
            vias.append([p['net'], ex_x, py])

# Clean orthogonal routing for U2.8 (ECG_OUT) and U2.9 (ECG_FB):
# U2.8 (40.48, 21.81): drops via at pad and runs on B.Cu down to (40.48, 26.0) then to C11.2 (38.77, 26.0)
vias.append(['ECG_OUT', 40.48, 21.81])
clean_routes.append(['ECG_OUT', 'B.Cu', 0.25, 40.48, 21.81, 40.48, 26.00])
clean_routes.append(['ECG_OUT', 'B.Cu', 0.25, 40.48, 26.00, 38.77, 26.00])
vias.append(['ECG_OUT', 38.77, 26.00])

# U2.9 (40.48, 20.54): runs on F.Cu up to Y = 19.5, then drops via to B.Cu and runs to R17.1 (37.18, 29.50)
clean_routes.append(['ECG_FB', 'F.Cu', 0.25, 40.48, 20.54, 40.48, 19.50])
vias.append(['ECG_FB', 40.48, 19.50])
clean_routes.append(['ECG_FB', 'B.Cu', 0.25, 40.48, 19.50, 37.18, 19.50])
clean_routes.append(['ECG_FB', 'B.Cu', 0.25, 37.18, 19.50, 37.18, 29.50])
vias.append(['ECG_FB', 37.18, 29.50])

# Snap U2.4 (VCC):
clean_routes.append(['VCC', 'F.Cu', 0.25, 36.04, 18.00, 35.52, 18.00])

# Snap R23.2 (VREF):
clean_routes.append(['VREF', 'F.Cu', 0.25, 48.05, 35.00, 45.82, 35.00])

# Snap U2.6 (VREF):
vias.append(['VREF', 35.52, 20.54])
clean_routes.append(['VREF', 'B.Cu', 0.25, 35.52, 20.54, 34.00, 20.54])

# Connector pin extensions:
clean_routes.append(['LED_DRV', 'F.Cu', 0.25, 4.80, 25.20, 4.00, 24.54])
clean_routes.append(['PD_ANODE', 'B.Cu', 0.25, 4.80, 27.80, 4.00, 27.08])
clean_routes.append(['PULSE_TRIG', 'F.Cu', 0.25, 65.80, 21.40, 66.50, 22.16])
clean_routes.append(['ECG_OUT', 'B.Cu', 0.25, 65.80, 17.80, 66.50, 17.08])
clean_routes.append(['PPG_OUT', 'B.Cu', 0.25, 65.80, 19.80, 66.50, 19.62])

r = []
for r_item in clean_routes:
    net, layer_name, w, x1, y1, x2, y2 = r_item
    r.append(seg(net, layer_name, w, x1, y1, x2, y2))

seen_vias = set()
for net, x, y in vias:
    k = (net, round(x, 2), round(y, 2))
    if k not in seen_vias:
        seen_vias.add(k)
        r.append(via(net, x, y))

# GND stitching vias distributed in open ground areas
# Clear of VCC (Y <= 4.0) and VREF/ECG_OUT (Y >= 33.0)
safe_gnd = [
    (3.0, 7.0), (67.0, 7.0), (3.0, 33.0), (67.0, 33.0),
    (25.0, 8.0), (45.0, 8.0),
    (12.0, 18.0), (22.0, 18.0), (32.0, 18.0), (50.0, 18.0)
]
for gx, gy in safe_gnd:
    k = ('GND', round(gx, 2), round(gy, 2))
    if k not in seen_vias:
        seen_vias.add(k)
        r.append(via('GND', gx, gy))

bp = [(0.5, 0.5), (69.5, 0.5), (69.5, 39.5), (0.5, 39.5)]
r.append(zone('GND', 'F.Cu', bp))
r.append(zone('GND', 'B.Cu', bp))

open(OUT, 'w').write(head + ''.join(r) + ')\n')
print(f"Applied final flawless board: {len(r)} items!")
