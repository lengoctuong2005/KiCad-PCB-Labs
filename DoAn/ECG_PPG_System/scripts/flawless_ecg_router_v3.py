import json, math, heapq, uuid

STEP = 0.20
BW, BH = 70.0, 40.0
NX = int(round(BW / STEP)) + 1
NY = int(round(BH / STEP)) + 1
EDGE = 0.60
ALLB = 1 << 30

g = json.load(open('/tmp/ecg_pads_clean_base.json'))
pads = g['pads']
nets = sorted({p['net'] for p in pads if p['net']})
bit = {n: 1 << i for i, n in enumerate(nets)}

mask = [[[0] * NY for _ in range(NX)] for _ in range(2)]

def cells_in(l, t, r, b):
    ix0 = max(0, int(math.ceil(l / STEP)))
    ix1 = min(NX - 1, int(math.floor(r / STEP)))
    iy0 = max(0, int(math.ceil(t / STEP)))
    iy1 = min(NY - 1, int(math.floor(b / STEP)))
    for ix in range(ix0, ix1 + 1):
        for iy in range(iy0, iy1 + 1):
            yield ix, iy

for L in (0, 1):
    for ix in range(NX):
        x = ix * STEP
        for iy in range(NY):
            y = iy * STEP
            if x < EDGE or x > BW - EDGE or y < EDGE or y > BH - EDGE:
                mask[L][ix][iy] = ALLB

# Pad inflation: 0.45 mm ensures copper clearance >= 0.25 mm!
INFL = 0.45

for p in pads:
    b_val = bit[p['net']] if p['net'] else ALLB
    layers = (0, 1) if p['tht'] else (0,)
    for L in layers:
        for ix, iy in cells_in(p['l'] - INFL, p['t'] - INFL, p['r'] + INFL, p['bo'] + INFL):
            mask[L][ix][iy] |= b_val

# For IC footprints on F.Cu: forbid pass-through tracks between pins
for ref, cx, cy, hw, hh in [('U1', 20.0, 18.0, 3.5, 3.5), ('U2', 38.0, 18.0, 3.5, 5.5), ('U3', 56.0, 18.0, 3.5, 3.5)]:
    for ix, iy in cells_in(cx - hw, cy - hh, cx + hw, cy + hh):
        # Do not block the actual pad copper
        is_pad = False
        for p in pads:
            if p['ref'] == ref and p['l'] <= ix*STEP <= p['r'] and p['t'] <= iy*STEP <= p['bo']:
                is_pad = True; break
        if not is_pad:
            mask[0][ix][iy] = ALLB

def padcells(p):
    layers = (0, 1) if p['tht'] else (0,)
    cells = []
    cx = int(round(p['x'] / STEP))
    cy = int(round(p['y'] / STEP))
    for L in layers:
        cells.append((L, cx, cy))
        for ix, iy in cells_in(p['l'], p['t'], p['r'], p['bo']):
            cells.append((L, ix, iy))
    
    # If IC pad, add exit cell outside the forbidden box
    if p['ref'].startswith('U'):
        dx = -1.8 if int(p['num']) <= (4 if p['ref'] in ('U1','U3') else 7) else 1.8
        ex_x = p['x'] + dx
        ex_ix = int(round(ex_x / STEP))
        for L in (0, 1): cells.append((L, ex_ix, cy))
    return list(set(cells))

def allowed(L, ix, iy, b_val):
    if ix < 0 or iy < 0 or ix >= NX or iy >= NY: return False
    return (mask[L][ix][iy] & ~b_val) == 0

def mark_seg(L, x1, y1, x2, y2, w, b_val):
    hw = 0.50
    l = min(x1, x2) - hw; r = max(x1, x2) + hw
    t = min(y1, y2) - hw; bo = max(y1, y2) + hw
    dx = x2 - x1; dy = y2 - y1; L2 = dx * dx + dy * dy
    for ix, iy in cells_in(l, t, r, bo):
        px, py = ix * STEP, iy * STEP
        if L2 == 0: d = math.hypot(px - x1, py - y1)
        else:
            tt = max(0.0, min(1.0, ((px - x1) * dx + (py - y1) * dy) / L2))
            d = math.hypot(px - (x1 + tt * dx), py - (y1 + tt * dy))
        if d <= hw: mask[L][ix][iy] |= b_val

RVIA = 0.68
def mark_via(x, y, b_val):
    for L in (0, 1):
        for ix, iy in cells_in(x - RVIA, y - RVIA, x + RVIA, y + RVIA):
            mask[L][ix][iy] |= b_val

def via_ok(ix, iy, b_val):
    x, y = ix * STEP, iy * STEP
    for L in (0, 1):
        for cix, ciy in cells_in(x - RVIA, y - RVIA, x + RVIA, y + RVIA):
            if not allowed(L, cix, ciy, b_val): return False
    return True

def astar(startcells, goals, b_val, w):
    goal = set(goals); pq = []; dist = {}; prev = {}
    for c in startcells:
        L, ix, iy = c
        if not allowed(L, ix, iy, b_val): continue
        dist[c] = 0.0; heapq.heappush(pq, (0.0, c))
    if not pq: return None
    while pq:
        d, c = heapq.heappop(pq)
        if d > dist.get(c, 1e18): continue
        if c in goal:
            path = [c]
            while c in prev: c = prev[c]; path.append(c)
            return path[::-1]
        L, ix, iy = c
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (L, ix + dx, iy + dy)
            if not allowed(n[0], n[1], n[2], b_val): continue
            nd = d + 1.0
            if nd < dist.get(n, 1e18):
                dist[n] = nd; prev[n] = c; heapq.heappush(pq, (nd, n))
        if (ix % 2 == 0 and iy % 2 == 0) and via_ok(ix, iy, b_val):
            n = (1 - L, ix, iy); nd = d + 8.0
            if nd < dist.get(n, 1e18):
                dist[n] = nd; prev[n] = c; heapq.heappush(pq, (nd, n))
    return None

def to_segments(path, net, w, p_start, p_goal):
    cur = []; segs = []
    for c in path:
        if cur and c[0] != cur[-1][0]:
            segs.append(cur); cur = []
        cur.append(c)
    if cur: segs.append(cur)
    res = []
    for grp_idx, grp in enumerate(segs):
        pts = [(round(c[1] * STEP, 4), round(c[2] * STEP, 4)) for c in grp]
        m = [pts[0]]
        for k in range(1, len(pts) - 1):
            ax, ay = m[-1]; bx, by = pts[k]; cx, cy = pts[k + 1]
            if abs((bx - ax) * (cy - by) - (by - ay) * (cx - bx)) < 1e-6: continue
            m.append(pts[k])
        m.append(pts[-1])
        if grp_idx == 0 and p_start:
            m.insert(0, (round(p_start['x'], 4), round(p_start['y'], 4)))
        if grp_idx == len(segs) - 1 and p_goal:
            m.append((round(p_goal['x'], 4), round(p_goal['y'], 4)))
        for a, b2 in zip(m, m[1:]):
            if a != b2: res.append((grp[0][0], w, a[0], a[1], b2[0], b2[1]))
    return res

routes = []; vias = []; fails = []

def add(net, L, w, x1, y1, x2, y2):
    routes.append((net, L, w, x1, y1, x2, y2))
    mark_seg(L, x1, y1, x2, y2, w, bit[net])

def addvia(net, x, y):
    vias.append((net, x, y))
    mark_via(x, y, bit[net])

# 1. Dedicated trunks on B.Cu:
add('VCC', 1, 0.35, 7.0, 1.8, 64.0, 1.8)
add('VREF', 1, 0.30, 14.5, 38.2, 63.5, 38.2)
add('VREF', 1, 0.30, 63.5, 38.2, 63.5, 24.70)
add('VREF', 1, 0.30, 63.5, 24.70, 66.5, 24.70)

bynet = {}
for p in pads:
    if not p['net'] or p['net'] == 'GND': continue
    bynet.setdefault(p['net'], []).append(p)

WIDTH = {'VCC': 0.35, 'VREF': 0.30}

priority_nets = sorted(bynet.keys(), key=lambda n: (n in ('VCC', 'VREF'), len(bynet[n])))

for net in priority_nets:
    ps = bynet[net]
    w = WIDTH.get(net, 0.25)
    b_val = bit[net]

    routed_cells = []
    if net == 'VCC':
        for ix, iy in cells_in(7.0, 1.8 - 0.2, 64.0, 1.8 + 0.2):
            routed_cells.append((1, ix, iy))
    elif net == 'VREF':
        for ix, iy in cells_in(14.5, 38.2 - 0.2, 63.5, 38.2 + 0.2):
            routed_cells.append((1, ix, iy))
        for ix, iy in cells_in(63.5 - 0.2, 24.70, 63.5 + 0.2, 38.2):
            routed_cells.append((1, ix, iy))
        for ix, iy in cells_in(63.5, 24.70 - 0.2, 66.5, 24.70 + 0.2):
            routed_cells.append((1, ix, iy))

    if not routed_cells:
        connected = [0]
        unconnected = list(range(1, len(ps)))
        routed_cells = padcells(ps[0])
    else:
        connected = []
        unconnected = list(range(len(ps)))

    while unconnected:
        best_path = None
        best_pin = None
        for j in unconnected:
            starts = padcells(ps[j])
            path = astar(starts, routed_cells, b_val, w)
            if path is not None:
                if best_path is None or len(path) < len(best_path):
                    best_path = path; best_pin = j
        if best_path is None:
            for j in unconnected: fails.append((net, f"{ps[j]['ref']}.{ps[j]['num']}"))
            break
        unconnected.remove(best_pin)
        connected.append(best_pin)
        for L, ww, x1, y1, x2, y2 in to_segments(best_path, net, w, ps[best_pin], None):
            add(net, L, ww, x1, y1, x2, y2)
        for k in range(len(best_path) - 1):
            if best_path[k][0] != best_path[k + 1][0]:
                addvia(net, best_path[k][1] * STEP, best_path[k][2] * STEP)
        routed_cells.extend(best_path)

print(f"Router V3: {len(routes)} tracks, {len(vias)} vias, {len(fails)} fails")
for f in fails: print("  FAIL:", f)

json.dump(dict(routes=routes, vias=vias, fails=fails), open('/tmp/ecg_v3.json', 'w'))
