import json
import math
from collections import defaultdict

def chamfer_routes(routes, vias):
    via_set = {(round(v[1], 3), round(v[2], 3)) for v in vias}

    # Group segments by (net, layer, width)
    groups = defaultdict(list)
    for r in routes:
        net, layer, w, x1, y1, x2, y2 = r
        p1 = (round(x1, 3), round(y1, 3))
        p2 = (round(x2, 3), round(y2, 3))
        if p1 != p2:
            groups[(net, layer, w)].append((p1, p2))

    new_routes = []

    for (net, layer, w), segs in groups.items():
        # Build adjacency graph
        adj = defaultdict(list)
        for idx, (p1, p2) in enumerate(segs):
            adj[p1].append((p2, idx))
            adj[p2].append((p1, idx))

        # Decompose into simple paths
        used_edges = set()
        paths = []

        # Start from endpoints (degree != 2)
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
                    # Find edge index
                    for n, e in adj[curr]:
                        if n == next_nbr and e not in used_edges:
                            used_edges.add(e)
                            break
                    path.append(next_nbr)
                    curr = next_nbr
                paths.append(path)

        # Handle remaining cycles if any
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

        # Now chamfer each path
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

                # Check if p_curr is at a via
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

                # If ~90 degree turn (cos_theta near 0)
                if abs(cos_theta) < 0.15:
                    d = min(0.35, L1 / 2.1, L2 / 2.1)
                    if d >= 0.1:
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

if __name__ == '__main__':
    with open('/tmp/emg_routes_flawless.json', 'r') as f:
        data = json.load(f)

    routes = data['routes']
    vias = data['vias']

    chamfered = chamfer_routes(routes, vias)
    print(f"Original segments: {len(routes)}, Chamfered segments: {len(chamfered)}")

    out_data = {
        'routes': chamfered,
        'vias': vias,
        'fails': data.get('fails', [])
    }
    with open('/tmp/emg_routes_chamfered.json', 'w') as f:
        json.dump(out_data, f, indent=2)
    print("Saved /tmp/emg_routes_chamfered.json")
