import json, math, heapq, uuid

# Load from pure_mst_route_v2.py
s = open('DoAn/ECG_PPG_System/scripts/pure_mst_route_v2.py').read()

# Replace the inner loop for multi-pin nets (where len(ps) > 2)
new_loop = '''    if len(ps) <= 2:
        starts = padcells(ps[0])
        goals = padcells(ps[1])
        path = astar(starts, goals, b_val, w)
        if path is None:
            fails.append((net, f"{ps[0]['ref']}.{ps[0]['num']}", f"{ps[1]['ref']}.{ps[1]['num']}"))
        else:
            for L, ww, x1, y1, x2, y2 in to_segments(path, net, w, ps[0], ps[1]):
                add(net, L, ww, x1, y1, x2, y2)
            for k in range(len(path) - 1):
                if path[k][0] != path[k + 1][0]:
                    addvia(net, path[k][1] * STEP, path[k][2] * STEP)
    else:
        # Multi-pin net (e.g. VCC, VREF, VMID, ECG_OUT, PPG_OUT):
        # Seed tree with first pin (or pre-routed trunk)
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
                        best_path = path
                        best_pin = j
            if best_path is None:
                for j in unconnected:
                    fails.append((net, f"{ps[j]['ref']}.{ps[j]['num']}"))
                break
            unconnected.remove(best_pin)
            connected.append(best_pin)
            for L, ww, x1, y1, x2, y2 in to_segments(best_path, net, w, ps[best_pin], None):
                add(net, L, ww, x1, y1, x2, y2)
            for k in range(len(best_path) - 1):
                if best_path[k][0] != best_path[k + 1][0]:
                    addvia(net, best_path[k][1] * STEP, best_path[k][2] * STEP)
            routed_cells.extend(best_path)
'''

# Find the start of the edges loop
start_idx = s.find('    n = len(ps); inT = [0]')
end_idx = s.find("print(f\"Router V2 result:")

s_new = s[:start_idx] + new_loop + s[end_idx:]
open('/tmp/test_vref_nearest.py', 'w').write(s_new)
print('Wrote /tmp/test_vref_nearest.py')
