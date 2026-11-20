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
            f'\t\t(min_thickness 0.2)\n\t\t(fill yes\n\t\t\t(thermal_gap 0.2)\n\t\t\t(thermal_bridge_width 0.35)\n\t\t\t(island_removal_mode 2)\n\t\t)\n'
            f'\t\t(polygon\n\t\t\t(pts{ptxt}\n\t\t\t)\n\t\t)\n\t)\n')

s = open(BASE).read()
pos_list = [i for i in (s.find('\n\t(segment\n'), s.find('\n\t(via\n'), s.find('\n\t(zone\n')) if i >= 0]
CUT = min(pos_list) if pos_list else s.rfind(')')
head = s[:CUT]

d = json.load(open('/tmp/ecg_flawless_autorouter.json'))
routes = d['routes']
vias = d['vias']
LAYERS = {0: 'F.Cu', 1: 'B.Cu'}

clean_routes = []
for r_item in routes:
    net, L, w, x1, y1, x2, y2 = r_item
    layer_name = LAYERS[L] if isinstance(L, int) else L

    if net == 'ECG_FB':
        continue
    if net == 'ECG_OUT' and max(x1, x2) <= 45.0:
        continue
    if net == 'VREF' and layer_name == 'F.Cu' and min(y1, y2) <= 6.0:
        continue
    if net == 'VREF' and layer_name == 'F.Cu' and max(y1, y2) >= 34.0 and min(x1, x2) >= 45.0:
        continue
    if net == 'VREF' and layer_name == 'B.Cu' and abs(y1 - 38.2) < 0.1 and abs(y2 - 38.2) < 0.1:
        continue

    # Filter out dangling stubs:
    if net == 'VREF':
        if abs(x1 - 49.2) < 0.6 and abs(y1 - 31.8) < 0.6: continue
        if abs(x1 - 33.6) < 0.6 and abs(y1 - 29.0) < 0.6: continue
        if abs(x1 - 39.8) < 0.6 and abs(y1 - 11.4) < 0.6: continue
        if abs(x1 - 39.0) < 0.6 and abs(y1 - 11.4) < 0.6: continue

    clean_routes.append([net, layer_name, w, x1, y1, x2, y2])

clean_vias = []
for v in vias:
    net, vx, vy = v
    if net == 'ECG_OUT':
        continue
    if net == 'VREF' and (abs(vx - 45.6) < 0.5 or abs(vx - 33.2) < 0.5):
        continue
    if net == 'RA_FILT' and abs(vx - 10.2) < 0.5:
        continue
    clean_vias.append(v)

# 1. Clean ECG_FB net:
clean_vias.append(['ECG_FB', 40.48, 20.54])
clean_routes.append(['ECG_FB', 'F.Cu', 0.25, 40.48, 20.54, 40.48, 20.54])
clean_routes.append(['ECG_FB', 'B.Cu', 0.25, 40.48, 20.54, 42.50, 20.54])
clean_routes.append(['ECG_FB', 'B.Cu', 0.25, 42.50, 20.54, 42.50, 30.33])
clean_routes.append(['ECG_FB', 'B.Cu', 0.25, 42.50, 30.33, 37.18, 30.33])
clean_routes.append(['ECG_FB', 'B.Cu', 0.25, 37.18, 30.33, 37.18, 29.50])
clean_vias.append(['ECG_FB', 37.18, 29.50])
clean_routes.append(['ECG_FB', 'F.Cu', 0.25, 37.18, 29.50, 37.18, 29.50])
clean_routes.append(['ECG_FB', 'B.Cu', 0.25, 37.18, 30.33, 34.00, 30.33])
clean_vias.append(['ECG_FB', 34.00, 30.33])
clean_routes.append(['ECG_FB', 'F.Cu', 0.25, 34.00, 30.33, 34.00, 30.33])

# 2. Clean ECG_OUT net:
clean_vias.append(['ECG_OUT', 40.48, 21.81])
clean_routes.append(['ECG_OUT', 'F.Cu', 0.25, 40.48, 21.81, 40.48, 21.81])
clean_routes.append(['ECG_OUT', 'B.Cu', 0.25, 40.48, 21.81, 38.77, 21.81])
clean_routes.append(['ECG_OUT', 'B.Cu', 0.25, 38.77, 21.81, 38.77, 26.00])
clean_vias.append(['ECG_OUT', 38.77, 26.00])
clean_routes.append(['ECG_OUT', 'F.Cu', 0.25, 38.77, 26.00, 38.77, 26.00])
clean_routes.append(['ECG_OUT', 'B.Cu', 0.25, 38.77, 26.00, 38.83, 29.50])
clean_vias.append(['ECG_OUT', 38.83, 29.50])
clean_routes.append(['ECG_OUT', 'F.Cu', 0.25, 38.83, 29.50, 38.83, 29.50])
clean_routes.append(['ECG_OUT', 'B.Cu', 0.25, 38.77, 21.81, 38.77, 17.80])
clean_routes.append(['ECG_OUT', 'B.Cu', 0.25, 38.77, 17.80, 37.80, 17.80])

# 3. Clean VREF connections:
clean_routes.append(['VREF', 'F.Cu', 0.25, 49.83, 23.00, 49.83, 23.00])
clean_vias.append(['VREF', 49.83, 23.00])
clean_routes.append(['VREF', 'B.Cu', 0.25, 49.83, 23.00, 49.77, 31.00])
clean_vias.append(['VREF', 49.77, 31.00])
clean_routes.append(['VREF', 'F.Cu', 0.25, 49.77, 31.00, 49.77, 31.00])

clean_routes.append(['VREF', 'B.Cu', 0.25, 49.77, 31.00, 52.50, 31.00])
clean_routes.append(['VREF', 'B.Cu', 0.25, 52.50, 31.00, 52.50, 38.20])

clean_routes.append(['VREF', 'F.Cu', 0.25, 45.82, 35.00, 45.82, 35.00])
clean_vias.append(['VREF', 45.82, 35.00])
clean_routes.append(['VREF', 'B.Cu', 0.25, 45.82, 35.00, 45.82, 38.20])

clean_routes.append(['VREF', 'F.Cu', 0.25, 52.17, 4.00, 52.17, 4.80])
clean_vias.append(['VREF', 52.17, 4.80])
clean_routes.append(['VREF', 'B.Cu', 0.25, 52.17, 4.80, 52.17, 12.00])
clean_routes.append(['VREF', 'B.Cu', 0.25, 52.17, 12.00, 40.48, 12.00])
clean_routes.append(['VREF', 'B.Cu', 0.25, 40.48, 12.00, 40.48, 15.46])
clean_vias.append(['VREF', 40.48, 15.46])

# Connect the 5.8mm track at (33.2, 29.0) directly to R16.2 (34.00, 28.68) and to VREF trunk at Y = 38.20 via X = 32.50:
clean_vias.append(['VREF', 33.20, 23.20])
clean_routes.append(['VREF', 'B.Cu', 0.25, 33.20, 29.00, 34.00, 28.68])
clean_routes.append(['VREF', 'F.Cu', 0.25, 34.00, 28.68, 34.00, 28.68])
clean_vias.append(['VREF', 34.00, 28.68])
clean_routes.append(['VREF', 'B.Cu', 0.25, 34.00, 28.68, 32.50, 28.68])
clean_routes.append(['VREF', 'B.Cu', 0.25, 32.50, 28.68, 32.50, 38.20])

# VREF continuous trunk on B.Cu:
clean_routes.append(['VREF', 'B.Cu', 0.30, 32.50, 38.20, 63.50, 38.20])
clean_routes.append(['VREF', 'B.Cu', 0.30, 63.50, 38.20, 63.50, 24.70])
clean_routes.append(['VREF', 'B.Cu', 0.30, 63.50, 24.70, 66.50, 24.70])

# 4. Snap connector pin extensions:
clean_routes.append(['LED_DRV', 'F.Cu', 0.25, 4.80, 25.20, 4.00, 24.54])
clean_routes.append(['PD_ANODE', 'B.Cu', 0.25, 4.80, 27.80, 4.00, 27.08])
clean_routes.append(['PULSE_TRIG', 'F.Cu', 0.25, 65.80, 21.40, 66.50, 22.16])
clean_routes.append(['ECG_OUT', 'B.Cu', 0.25, 65.80, 17.80, 66.50, 17.08])
clean_routes.append(['PPG_OUT', 'B.Cu', 0.25, 65.80, 19.80, 66.50, 19.62])

# 5. Connect ground regions to solid B.Cu ground plane:
clean_routes.append(['GND', 'F.Cu', 0.25, 17.52, 19.91, 19.00, 19.91])
clean_vias.append(['GND', 19.00, 19.91])

clean_routes.append(['GND', 'F.Cu', 0.25, 38.77, 10.50, 38.77, 9.00])
clean_vias.append(['GND', 38.77, 9.00])

clean_routes.append(['GND', 'F.Cu', 0.25, 53.52, 19.91, 52.00, 19.91])
clean_vias.append(['GND', 52.00, 19.91])

clean_vias.append(['GND', 35.00, 24.00])
clean_vias.append(['GND', 29.50, 18.00])
clean_vias.append(['GND', 11.00, 16.50])

r = []
for r_item in clean_routes:
    net, layer_name, w, x1, y1, x2, y2 = r_item
    r.append(seg(net, layer_name, w, x1, y1, x2, y2))

seen_vias = set()
for net, x, y in clean_vias:
    k = (net, round(x, 2), round(y, 2))
    if k not in seen_vias:
        seen_vias.add(k)
        r.append(via(net, x, y))

# Solid ground planes on BOTH F.Cu and B.Cu with island_removal_mode 2!
bp = [(0.5, 0.5), (69.5, 0.5), (69.5, 39.5), (0.5, 39.5)]
r.append(zone('GND', 'F.Cu', bp))
r.append(zone('GND', 'B.Cu', bp))

open(OUT, 'w').write(head + ''.join(r) + ')\n')
print(f"Applied final triumph board: {len(r)} items!")
