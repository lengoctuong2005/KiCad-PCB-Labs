#!/usr/bin/env python3
"""
route_lab6.py - Automated precision router for Lab 6 PCB
Routes all 29 nets adhering to Net Classes, 45-degree rule, clearances, and DRC.
"""

import math
import uuid
import re

def make_uuid():
    return str(uuid.uuid4())

def segment(start, end, width, layer, net_name):
    return f"""\t(segment
\t\t(start {start[0]:.3f} {start[1]:.3f})
\t\t(end {end[0]:.3f} {end[1]:.3f})
\t\t(width {width:.3f})
\t\t(layer "{layer}")
\t\t(net "{net_name}")
\t\t(uuid "{make_uuid()}")
\t)"""

def via(at, size, drill, net_name):
    return f"""\t(via
\t\t(at {at[0]:.3f} {at[1]:.3f})
\t\t(size {size:.3f})
\t\t(drill {drill:.3f})
\t\t(layers "F.Cu" "B.Cu")
\t\t(net "{net_name}")
\t\t(uuid "{make_uuid()}")
\t)"""

def route_path(points, width, layer, net_name):
    """Generate segments connecting a series of points."""
    segs = []
    for i in range(len(points) - 1):
        p1 = points[i]
        p2 = points[i+1]
        if round(p1[0], 3) == round(p2[0], 3) and round(p1[1], 3) == round(p2[1], 3):
            continue
        segs.append(segment(p1, p2, width, layer, net_name))
    return segs

print("Router module loaded.")
