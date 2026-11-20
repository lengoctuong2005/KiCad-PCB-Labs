import json, uuid

BASE = 'DoAn/ECG_PPG_System/ECG_PPG_System.kicad_pcb'
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
            f'\t\t(hatch edge 0.508)\n\t\t(connect_pads yes\n\t\t\t(clearance 0.2000)\n\t\t)\n'
            f'\t\t(min_thickness 0.2000)\n\t\t(filled_areas_thickness no)\n'
            f'\t\t(fill yes\n\t\t\t(thermal_gap 0.2000)\n\t\t\t(thermal_bridge_width 0.3500)\n\t\t)\n'
            f'\t\t(polygon\n\t\t\t(pts{ptxt}\n\t\t\t)\n\t\t)\n\t)\n')

s = open(BASE).read()
pos_list = [i for i in (s.find('\n\t(segment\n'), s.find('\n\t(via\n'), s.find('\n\t(zone\n')) if i >= 0]
CUT = min(pos_list) if pos_list else s.rfind(')')
head = s[:CUT]

d = json.load(open('/tmp/ecg_master_clean.json'))
routes = d['routes']
vias = d['vias']
LAYERS = {0: 'F.Cu', 1: 'B.Cu'}

# 1. Connect the 4 remaining pairs cleanly:
# U2.1 to U2.2 on B.Cu:
routes.append(['VREF', 0, 0.25, 35.52, 14.19, 33.80, 14.19])
vias.append(['VREF', 33.80, 14.19])
routes.append(['VREF', 1, 0.25, 33.80, 14.19, 33.80, 15.46])
vias.append(['VREF', 33.80, 15.46])
routes.append(['VREF', 0, 0.25, 33.80, 15.46, 35.52, 15.46])

# R21.2 to R22.1 on B.Cu above at Y = 25.0:
routes.append(['PPG_LPF_NODE', 0, 0.25, 45.83, 27.00, 45.83, 25.00])
vias.append(['PPG_LPF_NODE', 45.83, 25.00])
routes.append(['PPG_LPF_NODE', 1, 0.25, 45.83, 25.00, 48.17, 25.00])
vias.append(['PPG_LPF_NODE', 48.17, 25.00])
routes.append(['PPG_LPF_NODE', 0, 0.25, 48.17, 25.00, 48.17, 27.00])

# R20.2 to C17.2 on B.Cu at X = 52.0:
routes.append(['VREF', 0, 0.25, 49.83, 23.00, 52.00, 23.00])
vias.append(['VREF', 52.00, 23.00])
routes.append(['VREF', 1, 0.25, 52.00, 23.00, 52.00, 31.00])
vias.append(['VREF', 52.00, 31.00])
routes.append(['VREF', 0, 0.25, 52.00, 31.00, 49.77, 31.00])

# U2.8 to C11.2 on B.Cu at X = 42.5:
routes.append(['ECG_OUT', 0, 0.25, 40.48, 21.81, 42.50, 21.81])
vias.append(['ECG_OUT', 42.50, 21.81])
routes.append(['ECG_OUT', 1, 0.25, 42.50, 21.81, 42.50, 26.00])
routes.append(['ECG_OUT', 1, 0.25, 42.50, 26.00, 38.77, 26.00])
vias.append(['ECG_OUT', 38.77, 26.00])

# 2. Connector pin extensions:
routes.append(['LED_DRV', 0, 0.25, 4.80, 25.20, 4.00, 24.54])
routes.append(['PD_ANODE', 1, 0.25, 4.80, 27.80, 4.00, 27.08])
routes.append(['PULSE_TRIG', 0, 0.25, 65.80, 21.40, 66.50, 22.16])
routes.append(['ECG_OUT', 1, 0.25, 65.80, 17.80, 66.50, 17.08])
routes.append(['PPG_OUT', 1, 0.25, 65.80, 19.80, 66.50, 19.62])

r = []
for r_item in routes:
    net, L, w, x1, y1, x2, y2 = r_item
    layer_name = LAYERS[L] if isinstance(L, int) else L
    r.append(seg(net, layer_name, w, x1, y1, x2, y2))

seen_vias = set()
for net, x, y in vias:
    k = (net, round(x, 2), round(y, 2))
    if k not in seen_vias:
        seen_vias.add(k)
        r.append(via(net, x, y))

# GND stitching vias
safe_gnd = [
    (3.0, 7.0), (67.0, 7.0), (3.0, 33.0), (67.0, 33.0),
    (25.0, 8.0), (45.0, 8.0),
    (18.0, 33.0), (38.0, 33.0), (52.0, 33.0)
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
print(f"Applied master clean: {len(r)} items!")
