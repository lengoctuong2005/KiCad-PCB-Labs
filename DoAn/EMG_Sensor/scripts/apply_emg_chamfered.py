import re
import json
import uuid
import math
from collections import defaultdict

def chamfer_routes(routes, vias):
    via_set = {(round(v[1], 3), round(v[2], 3)) for v in vias}

    groups = defaultdict(list)
    for r in routes:
        net, layer, w, x1, y1, x2, y2 = r
        p1 = (round(x1, 3), round(y1, 3))
        p2 = (round(x2, 3), round(y2, 3))
        if p1 != p2:
            groups[(net, layer, w)].append((p1, p2))

    new_routes = []

    for (net, layer, w), segs in groups.items():
        adj = defaultdict(list)
        for idx, (p1, p2) in enumerate(segs):
            adj[p1].append((p2, idx))
            adj[p2].append((p1, idx))

        used_edges = set()
        paths = []

        start_nodes = [node for node, nbrs in adj.items() if len(nbrs) != 2]
        if not start_nodes and adj:
            start_nodes = [list(adj.keys())[0]]

        for start in start_nodes:
            for nbr, edge_idx in adj[start]:
                if edge_idx in used_edges:
                    continue
                path = [start, nbr]
                used_edges.add(edge_idx)
                curr = nbr
                while len(adj[curr]) == 2:
                    next_nodes = [n for n, e in adj[curr] if e not in used_edges]
                    if not next_nodes:
                        break
                    next_nbr = next_nodes[0]
                    for n, e in adj[curr]:
                        if n == next_nbr and e not in used_edges:
                            used_edges.add(e)
                            break
                    path.append(next_nbr)
                    curr = next_nbr
                paths.append(path)

        for idx, (p1, p2) in enumerate(segs):
            if idx not in used_edges:
                used_edges.add(idx)
                path = [p1, p2]
                curr = p2
                while len(adj[curr]) == 2:
                    next_nodes = [n for n, e in adj[curr] if e not in used_edges]
                    if not next_nodes:
                        break
                    next_nbr = next_nodes[0]
                    for n, e in adj[curr]:
                        if n == next_nbr and e not in used_edges:
                            used_edges.add(e)
                            break
                    path.append(next_nbr)
                    curr = next_nbr
                paths.append(path)

        for path in paths:
            if len(path) < 3:
                for k in range(len(path) - 1):
                    new_routes.append([net, layer, w, path[k][0], path[k][1], path[k+1][0], path[k+1][1]])
                continue

            chamfered_path = [path[0]]
            for i in range(1, len(path) - 1):
                p_prev = chamfered_path[-1]
                p_curr = path[i]
                p_next = path[i + 1]

                if p_curr in via_set:
                    chamfered_path.append(p_curr)
                    continue

                v1 = (p_curr[0] - p_prev[0], p_curr[1] - p_prev[1])
                v2 = (p_next[0] - p_curr[0], p_next[1] - p_curr[1])

                L1 = math.hypot(v1[0], v1[1])
                L2 = math.hypot(v2[0], v2[1])

                if L1 < 1e-4 or L2 < 1e-4:
                    chamfered_path.append(p_curr)
                    continue

                dot = v1[0] * v2[0] + v1[1] * v2[1]
                cos_theta = max(-1.0, min(1.0, dot / (L1 * L2)))

                if abs(cos_theta) < 0.15:
                    d = min(0.35, L1 / 2.1, L2 / 2.1)
                    if d >= 0.08:
                        c1 = (round(p_curr[0] - (v1[0] / L1) * d, 4), round(p_curr[1] - (v1[1] / L1) * d, 4))
                        c2 = (round(p_curr[0] + (v2[0] / L2) * d, 4), round(p_curr[1] + (v2[1] / L2) * d, 4))
                        chamfered_path.append(c1)
                        chamfered_path.append(c2)
                        continue

                chamfered_path.append(p_curr)

            chamfered_path.append(path[-1])

            for k in range(len(chamfered_path) - 1):
                p_a = chamfered_path[k]
                p_b = chamfered_path[k + 1]
                if p_a != p_b:
                    new_routes.append([net, layer, w, p_a[0], p_a[1], p_b[0], p_b[1]])

    return new_routes

def zone_str(net, layer, netname, pts, clearance=0.25, thermal_gap=0.25):
    u = str(uuid.uuid4())
    pts_s = "\n".join(f"        (xy {x:.4f} {y:.4f})" for x, y in pts)
    return f"""  (zone
    (net {net})
    (net_name "{netname}")
    (layer "{layer}")
    (uuid "{u}")
    (hatch edge 0.5000)
    (connect_pads yes
      (clearance {clearance:.4f})
    )
    (min_thickness 0.2000)
    (fill yes
      (thermal_gap {thermal_gap:.4f})
      (thermal_bridge_width 0.4000)
      (island_removal_mode 0)
    )
    (polygon
      (pts
{pts_s}
      )
    )
  )"""

def main():
    with open('/tmp/emg_routes_flawless.json') as f:
        data = json.load(f)

    routes = data['routes']
    vias = data['vias']

    chamfered_routes = chamfer_routes(routes, vias)
    print(f"Original segments: {len(routes)} -> Chamfered: {len(chamfered_routes)}")

    with open('DoAn/EMG_Sensor/EMG_Sensor.kicad_pcb') as f:
        txt = f.read()

    idx = txt.find('(segment')
    if idx == -1:
        idx = txt.find('(zone')
    if idx == -1:
        idx = txt.rfind(')')
    head = txt[:idx].rstrip() + '\n'

    net_map = {}
    for m in re.finditer(r'\(net\s+(\d+)\s+"([^"]+)"\)', head):
        net_map[m.group(2)] = int(m.group(1))

    gnd_net = net_map.get('GND', 1)

    lines = [head]

    for r in chamfered_routes:
        netname, L, w, x1, y1, x2, y2 = r
        net_id = net_map.get(netname, 0)
        layer_s = 'F.Cu' if L == 0 else 'B.Cu'
        u = str(uuid.uuid4())
        lines.append(f'  (segment (start {x1:.4f} {y1:.4f}) (end {x2:.4f} {y2:.4f}) (width {w:.4f}) (layer "{layer_s}") (net {net_id}) (uuid "{u}"))')

    for v in vias:
        netname, vx, vy, sz, dr = v
        net_id = net_map.get(netname, 0)
        u = str(uuid.uuid4())
        lines.append(f'  (via (at {vx:.4f} {vy:.4f}) (size {sz:.4f}) (drill {dr:.4f}) (layers "F.Cu" "B.Cu") (net {net_id}) (uuid "{u}"))')

    # Stitching GND vias
    gnd_vias = [
        (4.0, 4.0), (10.0, 4.0), (25.0, 4.0), (45.0, 4.0),
        (4.0, 26.0), (10.0, 26.0), (25.0, 26.0), (45.0, 26.0),
        (4.0, 15.0), (45.0, 15.0)
    ]
    for vx, vy in gnd_vias:
        u = str(uuid.uuid4())
        lines.append(f'  (via (at {vx:.4f} {vy:.4f}) (size 0.8000) (drill 0.4000) (layers "F.Cu" "B.Cu") (net {gnd_net}) (uuid "{u}"))')

    bp = [(0.5, 0.5), (49.5, 0.5), (49.5, 29.5), (0.5, 29.5)]
    lines.append(zone_str(gnd_net, 'F.Cu', 'GND', bp, clearance=0.25, thermal_gap=0.25))
    lines.append(zone_str(gnd_net, 'B.Cu', 'GND', bp, clearance=0.25, thermal_gap=0.25))
    lines.append(')\n')

    out_text = '\n'.join(lines)
    with open('DoAn/EMG_Sensor/EMG_Sensor.kicad_pcb', 'w') as f:
        f.write(out_text)

    print("Updated DoAn/EMG_Sensor/EMG_Sensor.kicad_pcb successfully!")

if __name__ == '__main__':
    main()
