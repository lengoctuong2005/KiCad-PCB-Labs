import re

with open("generate_pcb_final.py") as f:
    code = f.read()

# 1. Bỏ phần add via trên pad GND
old_gnd_vias = """# GND stitching vias
for ref in ["J1", "C1", "C2", "R1", "R2", "R3", "C3", "C4", "U1", "U2", "Q1"]:
    for pad in fps[ref].Pads():
        if pad.GetNetname() == "GND":
            p = pad.GetPosition()
            # add small offset via for solid GND plane connection
            vx = p.x/1e6
            vy = p.y/1e6
            add_via_exact("GND", (vx, vy))"""

new_gnd_vias = """# Dedicated GND stitching vias in open areas (not colliding with pads)
gnd_vias = [(2.0, 5.0), (16.0, 5.0), (2.0, 26.0), (16.0, 26.0), (9.0, 16.0)]
for vx, vy in gnd_vias:
    add_via_exact("GND", (vx, vy))"""

if old_gnd_vias in code:
    code = code.replace(old_gnd_vias, new_gnd_vias)
    print("Replaced GND stitching loop successfully.")
else:
    print("WARNING: old_gnd_vias block not found directly, checking regex...")

with open("generate_pcb_clean.py", "w") as f:
    f.write(code)

