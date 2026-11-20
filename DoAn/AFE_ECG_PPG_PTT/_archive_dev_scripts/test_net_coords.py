import pcbnew
from test_netlist_map import NET_MAP

board = pcbnew.LoadBoard('/tmp/test_full_route.kicad_pcb')
fps = {fp.GetReference(): fp for fp in board.GetFootprints()}

print("=== NET COORDINATES TO ROUTE ===")
for net_name, conns in NET_MAP.items():
    if net_name == "GND": continue
    print(f"\nNet {net_name} ({len(conns)} pins):")
    for ref, pad_num in conns:
        fp = fps.get(ref)
        pad = fp.FindPadByNumber(pad_num) if fp else None
        if pad:
            pos = pad.GetPosition()
            print(f"  {ref:5s}.{pad_num:<2s} -> ({pos.x/1e6:6.2f}, {pos.y/1e6:6.2f}) mm")
