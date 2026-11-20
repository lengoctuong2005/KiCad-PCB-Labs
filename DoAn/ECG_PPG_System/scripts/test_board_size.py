import json, math, heapq, uuid

def run_router(BW, BH):
    STEP = 0.20
    NX = int(round(BW / STEP)) + 1
    NY = int(round(BH / STEP)) + 1
    CLR = 0.21
    EDGE = 0.60
    ALLB = 1 << 30

    g = json.load(open('/tmp/ecg_pads.json'))
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

    INFL = 0.22
    for p in pads:
        b = bit[p['net']] if p['net'] else ALLB
        layers = (0, 1) if p['tht'] else (0,)
        for L in layers:
            for ix, iy in cells_in(p['l'] - INFL, p['t'] - INFL, p['r'] + INFL, p['bo'] + INFL):
                mask[L][ix][iy] |= b

    def padcells(p):
        layers = (0, 1) if p['tht'] else (0,)
        cells = []
        cx = int(round(p['x'] / STEP))
        cy = int(round(p['y'] / STEP))
        for L in layers:
            cells.append((L, cx, cy))
            for ix, iy in cells_in(p['l'], p['t'], p['r'], p['bo']):
                cells.append((L, ix, iy))
        return list(set(cells))

    def allowed(L, ix, iy, b):
        if ix < 0 or iy < 0 or ix >= NX or iy >= NY: return False
        return (mask[L][ix][iy] & ~b) == 0

    def mark_seg(L, x1, y1, x2, y2, w, b):
        hw = 0.38
        l = min(x1, x2) - hw; r = max(x1, x2) + hw
        t = min(y1, y2) - hw; bo = max(y1, y2) + hw
        dx = x2 - x1; dy = y2 - y1; L2 = dx * dx + dy * dy
        for ix, iy in cells_in(l, t, r, bo):
            px, py = ix * STEP, iy * STEP
            if L2 == 0: d = math.hypot(px - x1, py - y1)
            else:
                tt = max(0.0, min(1.0, ((px - x1) * dx + (py - y1) * dy) / L2))
                d = math.hypot(px - (x1 + tt * dx), py - (y1 + tt * dy))
            if d <= hw: mask[L][ix][iy] |= b

    RVIA = 0.62
    def mark_via(x, y, b):
        for L in (0, 1):
            for ix, iy in cells_in(x - RVIA, y - RVIA, x + RVIA, y + RVIA):
                mask[L][ix][iy] |= b

    def via_ok(ix, iy, b):
        x, y = ix * STEP, iy * STEP
        for L in (0, 1):
            for cix, ciy in cells_in(x - RVIA, y - RVIA, x + RVIA, y + RVIA):
                if not allowed(L, cix, ciy, b): return False
        return True

    def astar(startcells, goals, b, w):
        goal = set(goals); pq = []; dist = {}; prev = {}
        for c in startcells:
            L, ix, iy = c
            if not allowed(L, ix, iy, b): continue
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
                if not allowed(n[0], n[1], n[2], b): continue
                nd = d + 1.0
                if nd < dist.get(n, 1e18):
                    dist[n] = nd; prev[n] = c; heapq.heappush(pq, (nd, n))
            if via_ok(ix, iy, b):
                n = (1 - L, ix, iy); nd = d + 12.0
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

    bynet = {}
    for p in pads:
        if not p['net'] or p['net'] == 'GND': continue
        bynet.setdefault(p['net'], []).append(p)

    WIDTH = {'VCC': 0.35, 'VREF': 0.30}

    # Custom order: local signals first, then buses (VREF, VCC) on B.Cu
    priority_order = [
        'RG1', 'RG2', 'NET_D1_R3', 'NET_D2_R27',
        'RA_RAW', 'LA_RAW', 'RA_FILT', 'LA_FILT',
        'DRL_CM', 'DRL_OUT', 'RL_DRL',
        'ECG_IA_OUT', 'ECG_HPF_OUT', 'ECG_LPF_NODE', 'ECG_LPF_IN', 'ECG_FB', 'ECG_OUT',
        'LED_DRV', 'PD_ANODE', 'PPG_TIA_OUT', 'PPG_HPF_OUT', 'PPG_LPF_NODE', 'PPG_LPF_IN', 'PPG_FB', 'PPG_OUT',
        'VREF_THR', 'PULSE_TRIG',
        'VMID', 'VREF', 'VCC'
    ]

    for net in priority_order:
        if net not in bynet: continue
        ps = bynet[net]
        w = WIDTH.get(net, 0.25)
        b = bit[net]
        routed_cells = []

        n = len(ps); inT = [0]; out = list(range(1, n)); edges = []
        def dist_pads(i, j):
            return abs(ps[i]['l'] + ps[i]['r'] - ps[j]['l'] - ps[j]['r']) / 2 + abs(ps[i]['t'] + ps[i]['bo'] - ps[j]['t'] - ps[j]['bo']) / 2
        while out:
            best = None
            for i in inT:
                for j in out:
                    dd = dist_pads(i, j)
                    if best is None or dd < best[0]: best = (dd, i, j)
            edges.append((best[1], best[2])); inT.append(best[2]); out.remove(best[2])

        for i, j in edges:
            starts = padcells(ps[i])
            p_start = ps[i]
            if routed_cells:
                starts.extend(routed_cells)
                p_start = None
            goals = padcells(ps[j])
            path = astar(starts, goals, b, w)
            if path is None:
                fails.append((net, f"{ps[i]['ref']}.{ps[i]['num']}", f"{ps[j]['ref']}.{ps[j]['num']}"))
                continue
            for L, ww, x1, y1, x2, y2 in to_segments(path, net, w, p_start, ps[j]):
                add(net, L, ww, x1, y1, x2, y2)
            for k in range(len(path) - 1):
                if path[k][0] != path[k + 1][0]:
                    addvia(net, path[k][1] * STEP, path[k][2] * STEP)
            routed_cells.extend(path)

    print(f"BW={BW}, BH={BH}: {len(routes)} tracks, {len(vias)} vias, {len(fails)} fails")
    for f in fails: print("  FAIL:", f)
    return routes, vias, fails

run_router(60.0, 35.0)
