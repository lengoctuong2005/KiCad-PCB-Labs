#!/usr/bin/env python3
"""
build_complete_lab6_pcb.py - Precise non-destructive routing & NetClass builder for Lab 6
"""

import math
import uuid
import re
import json
import shutil

def make_uuid():
    return str(uuid.uuid4())

def get_net_id_map(net_names):
    net_map = {"": 0}
    for i, name in enumerate(net_names, 1):
        net_map[name] = i
    return net_map

def update_pro_file():
    pro_path = "LAB6.kicad_pro"
    with open(pro_path, "r", encoding="utf-8") as f:
        pro_data = json.load(f)
    
    classes = [
        {
            "bus_width": 12,
            "clearance": 0.2,
            "diff_pair_gap": 0.25,
            "diff_pair_via_gap": 0.25,
            "diff_pair_width": 0.2,
            "line_style": 0,
            "microvia_diameter": 0.3,
            "microvia_drill": 0.1,
            "name": "Default",
            "pcb_color": "rgba(0, 0, 0, 0.000)",
            "priority": 2147483647,
            "schematic_color": "rgba(0, 0, 0, 0.000)",
            "track_width": 0.4,
            "tuning_profile": "",
            "via_diameter": 0.8,
            "via_drill": 0.4,
            "wire_width": 6
        },
        {
            "bus_width": 12,
            "clearance": 0.25,
            "diff_pair_gap": 0.25,
            "diff_pair_via_gap": 0.25,
            "diff_pair_width": 0.2,
            "line_style": 0,
            "microvia_diameter": 0.3,
            "microvia_drill": 0.1,
            "name": "Power_Main",
            "pcb_color": "rgba(255, 0, 0, 0.800)",
            "priority": 1,
            "schematic_color": "rgba(255, 0, 0, 0.800)",
            "track_width": 0.8,
            "tuning_profile": "",
            "via_diameter": 0.8,
            "via_drill": 0.4,
            "wire_width": 6
        },
        {
            "bus_width": 12,
            "clearance": 0.2,
            "diff_pair_gap": 0.25,
            "diff_pair_via_gap": 0.25,
            "diff_pair_width": 0.3,
            "line_style": 0,
            "microvia_diameter": 0.3,
            "microvia_drill": 0.1,
            "name": "USB_Diff",
            "pcb_color": "rgba(0, 200, 0, 0.800)",
            "priority": 2,
            "schematic_color": "rgba(0, 200, 0, 0.800)",
            "track_width": 0.3,
            "tuning_profile": "",
            "via_diameter": 0.6,
            "via_drill": 0.3,
            "wire_width": 6
        },
        {
            "bus_width": 12,
            "clearance": 0.2,
            "diff_pair_gap": 0.25,
            "diff_pair_via_gap": 0.25,
            "diff_pair_width": 0.2,
            "line_style": 0,
            "microvia_diameter": 0.3,
            "microvia_drill": 0.1,
            "name": "Signal_UART",
            "pcb_color": "rgba(0, 100, 255, 0.800)",
            "priority": 3,
            "schematic_color": "rgba(0, 100, 255, 0.800)",
            "track_width": 0.3,
            "tuning_profile": "",
            "via_diameter": 0.6,
            "via_drill": 0.3,
            "wire_width": 6
        }
    ]
    
    patterns = [
        {"name": "Power_Main", "pattern": "/VDD*"},
        {"name": "Power_Main", "pattern": "GND"},
        {"name": "USB_Diff", "pattern": "/D*"},
        {"name": "Signal_UART", "pattern": "/TX"},
        {"name": "Signal_UART", "pattern": "/RX"},
        {"name": "Signal_UART", "pattern": "/1Hz"}
    ]
    
    if "net_settings" not in pro_data:
        pro_data["net_settings"] = {}
    pro_data["net_settings"]["classes"] = classes
    pro_data["net_settings"]["net_class_patterns"] = patterns
    
    for path in ["LAB6.kicad_pro", "lab6.kicad_pro"]:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(pro_data, f, indent=2)
        print(f"Updated {path} with 4 Net Classes.")

def generate_pcb():
    # Source from LAB5 clean file
    src_path = "/mnt/Windows/HK3-25-26/KhoaHe_PCB/Lab5/Project_KiCad/LAB5.kicad_pcb"
    with open(src_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract all net names from pads
    pad_nets = sorted(list(set(re.findall(r'\(net\s+\"([^\"]+)\"\)', content))))
    valid_nets = [n for n in pad_nets if n and not n.startswith("unconnected-")]
    if "GND" not in valid_nets:
        valid_nets.append("GND")
    valid_nets = sorted(valid_nets)
    
    net_id_map = get_net_id_map(valid_nets)
    
    # Build net declarations for header
    net_decl_lines = ['\t(net 0 "")']
    for nname in valid_nets:
        nid = net_id_map[nname]
        net_decl_lines.append(f'\t(net {nid} "{nname}")')
    net_decl_str = "\n".join(net_decl_lines)
    
    elements = []
    
    def add_segment(p1, p2, width, layer, nname):
        if round(p1[0], 3) == round(p2[0], 3) and round(p1[1], 3) == round(p2[1], 3):
            return
        nid = net_id_map.get(nname, 0)
        elements.append(f"""\t(segment
\t\t(start {p1[0]:.3f} {p1[1]:.3f})
\t\t(end {p2[0]:.3f} {p2[1]:.3f})
\t\t(width {width:.3f})
\t\t(layer "{layer}")
\t\t(net {nid})
\t\t(uuid "{make_uuid()}")
\t)""")

    def add_via(at, size, drill, nname):
        nid = net_id_map.get(nname, 0)
        elements.append(f"""\t(via
\t\t(at {at[0]:.3f} {at[1]:.3f})
\t\t(size {size:.3f})
\t\t(drill {drill:.3f})
\t\t(layers "F.Cu" "B.Cu")
\t\t(net {nid})
\t\t(uuid "{make_uuid()}")
\t)""")

    def add_polyline(pts, width, layer, nname):
        for i in range(len(pts)-1):
            add_segment(pts[i], pts[i+1], width, layer, nname)

    # ==================== ROUTING DEFINITIONS ====================
    # 1. USB Differential Pair (/D+, /D-)
    # USB1.2 (29.33, 98.34) -> U3.5 (34.297, 105.27)
    add_polyline([(29.33, 98.34), (29.33, 101.5), (31.0, 103.17), (31.0, 105.27), (34.297, 105.27)], 0.3, "F.Cu", "/D-")
    # USB1.3 (29.98, 98.34) -> U3.4 (34.297, 105.77)
    add_polyline([(29.98, 98.34), (29.98, 101.0), (31.6, 102.62), (31.6, 105.77), (34.297, 105.77)], 0.3, "F.Cu", "/D+")

    # 2. VDD_5V_IN (USB VBUS to C6 to SW2)
    add_polyline([(28.68, 98.34), (29.05, 98.71), (29.05, 106.0)], 0.8, "F.Cu", "/VDD_5V_IN")
    add_polyline([(28.68, 98.34), (28.68, 95.0), (37.85, 95.0)], 0.8, "F.Cu", "/VDD_5V_IN")

    # 3. CP2102 Local Connections
    add_polyline([(34.297, 104.77), (32.0, 104.77), (32.0, 110.95), (30.95, 112.0)], 0.4, "F.Cu", "Net-(U3-VDD)")
    add_polyline([(35.11, 108.082), (35.11, 110.0), (37.11, 112.0), (44.45, 112.0)], 0.4, "F.Cu", "Net-(U3-DTR)")
    add_polyline([(42.55, 112.0), (41.5, 113.05), (41.5, 133.62), (40.0, 135.12)], 0.3, "F.Cu", "/DTR")

    # 4. UART TX, RX
    add_polyline([(36.11, 108.082), (36.11, 109.5), (38.5, 111.89), (38.5, 131.08), (40.0, 132.58)], 0.3, "F.Cu", "/TX")
    add_via((40.0, 132.58), 0.8, 0.4, "/TX")
    add_polyline([(40.0, 132.58), (45.0, 132.58), (55.0, 122.58), (60.062, 122.58), (60.062, 122.0)], 0.3, "B.Cu", "/TX")

    add_polyline([(36.61, 108.082), (36.61, 109.0), (39.0, 111.39), (39.0, 129.04), (40.0, 130.04)], 0.3, "F.Cu", "/RX")
    add_via((40.0, 130.04), 0.8, 0.4, "/RX")
    add_polyline([(40.0, 130.04), (44.0, 130.04), (52.0, 122.04), (54.062, 122.04), (54.062, 122.0)], 0.3, "B.Cu", "/RX")

    # 5. LEDs and Series Resistors
    add_polyline([(31.938, 122.0), (31.938, 125.0), (31.0, 125.938), (31.0, 127.412)], 0.4, "F.Cu", "Net-(D1-A)")
    add_polyline([(37.938, 122.0), (37.938, 125.0), (37.0, 125.938), (37.0, 127.412)], 0.4, "F.Cu", "Net-(D2-A)")
    add_polyline([(42.062, 122.0), (42.062, 125.0), (43.0, 125.938), (43.0, 127.412)], 0.4, "F.Cu", "Net-(D3-K)")
    add_polyline([(49.938, 122.0), (49.938, 125.0), (49.0, 125.938), (49.0, 127.412)], 0.4, "F.Cu", "Net-(D4-A)")
    add_polyline([(55.938, 122.0), (55.938, 124.0), (57.5, 125.588), (61.0, 125.588)], 0.4, "F.Cu", "Net-(D5-A)")
    add_polyline([(61.938, 122.0), (61.938, 123.5), (59.85, 125.588), (55.0, 125.588)], 0.4, "F.Cu", "Net-(D6-A)")

    # 6. NE555 Clock Generator (U5)
    add_polyline([(55.425, 110.635), (51.0, 110.635), (49.0, 112.635), (49.0, 125.588)], 0.3, "F.Cu", "/1Hz")
    add_polyline([(49.0, 125.588), (49.0, 135.54), (48.0, 136.54)], 0.3, "F.Cu", "/1Hz")
    add_polyline([(60.575, 111.905), (65.0, 111.905), (68.405, 108.5), (73.0, 108.5)], 0.4, "F.Cu", "Net-(U5-CV)")
    add_polyline([(60.575, 109.365), (57.0, 109.365), (54.547, 106.912), (52.0, 106.912)], 0.4, "F.Cu", "Net-(U5-DC)")
    add_polyline([(52.0, 106.912), (52.0, 111.088)], 0.4, "F.Cu", "Net-(U5-DC)")
    add_polyline([(55.425, 109.365), (53.5, 109.365), (53.5, 112.912), (52.0, 112.912)], 0.4, "F.Cu", "Net-(U5-TH)")
    add_polyline([(55.425, 109.365), (58.0, 109.365), (59.27, 110.635), (60.575, 110.635)], 0.4, "F.Cu", "Net-(U5-TH)")
    add_polyline([(60.575, 110.635), (66.435, 110.635), (68.8, 113.0)], 0.4, "F.Cu", "Net-(U5-TH)")

    # 7. LM2776 Charge Pump (U2)
    add_polyline([(67.638, 95.55), (56.5, 95.55)], 0.4, "F.Cu", "Net-(U2-C1-)")
    add_polyline([(67.638, 96.5), (60.0, 96.5), (59.05, 97.45), (56.5, 97.45)], 0.4, "F.Cu", "Net-(U2-C1+)")
    add_polyline([(65.362, 97.45), (67.638, 97.45)], 0.4, "F.Cu", "Net-(U2-EN)")
    add_polyline([(65.362, 97.45), (64.0, 97.45), (62.1, 95.55), (45.5, 95.55)], 0.4, "F.Cu", "Net-(U2-EN)")
    add_via((45.5, 95.55), 0.8, 0.4, "Net-(U2-EN)")
    add_polyline([(45.5, 95.55), (45.5, 92.5), (28.0, 92.5), (28.0, 134.54), (30.0, 134.54)], 0.4, "B.Cu", "Net-(U2-EN)")

    # 8. Potentiometer Headers (P1+, P1-, P2+, P2-)
    add_polyline([(60.82, 100.92), (58.28, 100.92), (55.74, 100.92)], 0.8, "F.Cu", "/P1+")
    add_via((55.74, 100.92), 0.8, 0.4, "/P1+")
    add_polyline([(55.74, 100.92), (55.74, 134.89), (55.54, 135.09)], 0.8, "B.Cu", "/P1+")

    add_polyline([(60.82, 103.46), (58.28, 103.46), (55.74, 103.46)], 0.8, "F.Cu", "/P1-")
    add_via((55.74, 103.46), 0.8, 0.4, "/P1-")
    add_polyline([(55.74, 103.46), (53.0, 106.2), (53.0, 135.09)], 0.8, "B.Cu", "/P1-")

    add_polyline([(60.82, 118.92), (58.28, 118.92), (55.74, 118.92)], 0.8, "F.Cu", "/P2+")
    add_via((60.82, 118.92), 0.8, 0.4, "/P2+")
    add_polyline([(60.82, 118.92), (64.04, 122.14), (64.04, 135.09)], 0.8, "B.Cu", "/P2+")

    add_polyline([(60.82, 121.46), (58.28, 121.46), (55.74, 121.46)], 0.8, "F.Cu", "/P2-")
    add_via((60.82, 121.46), 0.8, 0.4, "/P2-")
    add_polyline([(60.82, 121.46), (61.5, 122.14), (61.5, 135.09)], 0.8, "B.Cu", "/P2-")

    # 9. Power Rails (/VDD_5V, /VDD_3V3, /VDD_N)
    add_polyline([(35.67, 95.0), (35.67, 97.0), (34.297, 98.373), (34.297, 104.27)], 0.8, "F.Cu", "/VDD_5V")
    add_polyline([(34.297, 104.27), (35.11, 103.457)], 0.8, "F.Cu", "/VDD_5V")
    add_polyline([(35.67, 95.0), (44.05, 95.0), (47.85, 98.8)], 0.8, "F.Cu", "/VDD_5V")
    add_polyline([(47.85, 98.8), (51.0, 98.8), (54.25, 95.55), (71.5, 95.55)], 0.8, "F.Cu", "/VDD_5V")
    add_via((71.5, 95.55), 0.8, 0.4, "/VDD_5V")
    add_polyline([(71.5, 95.55), (73.5, 95.55), (73.5, 137.63), (64.04, 137.63), (55.54, 137.63)], 0.8, "B.Cu", "/VDD_5V")
    add_polyline([(55.54, 137.63), (30.0, 137.63), (30.0, 137.08)], 0.8, "B.Cu", "/VDD_5V")
    add_via((31.0, 125.588), 0.8, 0.4, "/VDD_5V")
    add_polyline([(31.0, 125.588), (31.0, 137.63)], 0.8, "B.Cu", "/VDD_5V")
    add_via((55.0, 127.412), 0.8, 0.4, "/VDD_5V")
    add_polyline([(55.0, 127.412), (55.0, 137.63)], 0.8, "B.Cu", "/VDD_5V")
    add_via((61.0, 127.412), 0.8, 0.4, "/VDD_5V")
    add_polyline([(61.0, 127.412), (61.0, 137.63)], 0.8, "B.Cu", "/VDD_5V")
    add_polyline([(60.575, 108.095), (60.575, 106.0), (44.45, 106.0)], 0.8, "F.Cu", "/VDD_5V")
    add_polyline([(44.45, 106.0), (52.0, 106.0), (52.0, 105.088)], 0.8, "F.Cu", "/VDD_5V")
    add_polyline([(44.45, 106.0), (44.45, 98.8), (47.85, 98.8)], 0.8, "F.Cu", "/VDD_5V")
    add_polyline([(60.575, 108.095), (60.575, 106.5), (55.425, 106.5), (55.425, 111.905)], 0.8, "F.Cu", "/VDD_5V")

    add_polyline([(47.85, 96.5), (54.15, 96.5), (58.0, 96.5), (64.0, 102.5), (65.55, 102.5)], 0.8, "F.Cu", "/VDD_3V3")
    add_via((65.55, 102.5), 0.8, 0.4, "/VDD_3V3")
    add_polyline([(65.55, 102.5), (67.0, 102.5), (67.0, 132.55), (64.04, 132.55), (55.54, 132.55)], 0.8, "B.Cu", "/VDD_3V3")
    add_polyline([(55.54, 132.55), (40.0, 132.55), (40.0, 127.5)], 0.8, "B.Cu", "/VDD_3V3")
    add_polyline([(40.0, 132.55), (30.0, 132.55), (30.0, 132.0)], 0.8, "B.Cu", "/VDD_3V3")
    add_via((37.0, 125.588), 0.8, 0.4, "/VDD_3V3")
    add_polyline([(37.0, 125.588), (37.0, 132.55)], 0.8, "B.Cu", "/VDD_3V3")

    add_polyline([(65.362, 95.55), (61.5, 95.55)], 0.8, "F.Cu", "/VDD_N")
    add_via((61.5, 95.55), 0.8, 0.4, "/VDD_N")
    add_polyline([(61.5, 95.55), (61.5, 132.55), (53.0, 132.55), (43.0, 132.55), (43.0, 125.588)], 0.8, "B.Cu", "/VDD_N")

    # 10. Local Ground connections
    add_polyline([(41.85, 95.0), (43.97, 95.0), (47.85, 94.2)], 0.8, "F.Cu", "GND")
    add_polyline([(31.28, 98.34), (33.705, 98.39), (33.855, 102.19)], 0.8, "F.Cu", "GND")
    add_polyline([(26.105, 102.19), (26.255, 98.39), (28.68, 98.39)], 0.8, "F.Cu", "GND")
    add_polyline([(30.062, 122.0), (36.062, 122.0), (43.938, 122.0), (48.062, 122.0)], 0.8, "F.Cu", "GND")
    add_polyline([(61.5, 97.45), (71.5, 97.45)], 0.8, "F.Cu", "GND")
    add_polyline([(53.0, 137.63), (61.5, 137.63)], 0.8, "F.Cu", "GND")

    # Modify title block in source content
    content_mod = content.replace("Lab 05: Placement - Bo tri linh kien tren PCB", "Lab 06: Routing - Ky thuat Di day Mach in tren PCB")
    content_mod = content_mod.replace('(date "2026-08-28")', '(date "2026-08-30")')
    
    # Insert net declarations after paper
    paper_match = re.search(r'\(paper \"[^\"]+\"\)', content_mod)
    pos = paper_match.end()
    content_with_nets = content_mod[:pos] + "\n" + net_decl_str + content_mod[pos:]

    # Append routes before the last closing paren
    last_paren = content_with_nets.rfind(")")
    routes_str = "\n" + "\n".join(elements) + "\n"
    final_content = content_with_nets[:last_paren] + routes_str + content_with_nets[last_paren:]

    for target in ["LAB6.kicad_pcb", "lab6.kicad_pcb"]:
        with open(target, "w", encoding="utf-8") as f:
            f.write(final_content)
        print(f"Generated {target} with {len(elements)} routing segments/vias.")

if __name__ == "__main__":
    update_pro_file()
    generate_pcb()
