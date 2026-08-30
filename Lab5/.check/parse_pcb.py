#!/usr/bin/env python3
"""Proper S-expression parser for KiCad PCB - extracts footprint positions + courtyard bounds."""
import json, sys, math

def tokenize(s):
    i, n = 0, len(s)
    while i < n:
        c = s[i]
        if c.isspace(): i += 1; continue
        if c == '(' or c == ')':
            yield c; i += 1; continue
        if c == '"':
            j = i + 1
            while j < n and s[j] != '"':
                if s[j] == '\\': j += 1
                j += 1
            yield ('str', s[i+1:j]); i = j + 1; continue
        j = i
        while j < n and not s[j].isspace() and s[j] not in '()"':
            j += 1
        yield ('atom', s[i:j]); i = j

def parse(tokens):
    stack = [[]]
    for t in tokens:
        if t == '(':
            new = []
            stack[-1].append(new)
            stack.append(new)
        elif t == ')':
            stack.pop()
        else:
            stack[-1].append(t[1])
    return stack[0]

def find_all(node, key, direct=False):
    out = []
    if isinstance(node, list):
        if node and node[0] == key:
            out.append(node)
        if direct:
            for ch in node:
                if isinstance(ch, list) and ch and ch[0] == key:
                    out.append(ch)
        else:
            for ch in node:
                if isinstance(ch, list):
                    out.extend(find_all(ch, key))
    return out

def get_pos(fp):
    # (at x y [rot]) is a DIRECT child of footprint
    ats = [ch for ch in fp if isinstance(ch, list) and ch and ch[0] == 'at']
    if not ats: return None
    at = ats[0]
    x, y = float(at[1]), float(at[2])
    rot = float(at[3]) if len(at) > 3 and at[3] not in ('unlocked',) else 0.0
    return x, y, rot

def footprint_bounds(fp, pos):
    x0, y0, rot = pos
    pts = []
    for item in fp:
        if not isinstance(item, list) or not item: continue
        layers = [ch for ch in item if isinstance(ch, list) and ch and ch[0] == 'layer']
        on_crtyd = any('CrtYd' in str(l[1]) for l in layers if len(l) > 1)
        if not on_crtyd: continue
        if item[0] in ('fp_rect', 'fp_line'):
            for key in ('start', 'end'):
                n = find_all(item, key, direct=True)
                if n:
                    pts.append((float(n[0][1]), float(n[0][2])))
        elif item[0] == 'fp_circle':
            ctr = find_all(item, 'center', direct=True)
            end = find_all(item, 'end', direct=True)
            if ctr and end:
                cx, cy = float(ctr[0][1]), float(ctr[0][2])
                ex, ey = float(end[0][1]), float(end[0][2])
                rad = math.hypot(ex - cx, ey - cy)
                pts.append((cx - rad, cy - rad))
                pts.append((cx + rad, cy + rad))
    if not pts:
        return None
    r = math.radians(rot)
    cosr, sinr = math.cos(r), math.sin(r)
    abspts = []
    for (px, py) in pts:
        rx = px * cosr - py * sinr
        ry = px * sinr + py * cosr
        abspts.append((rx + x0, ry + y0))
    xs = [p[0] for p in abspts]; ys = [p[1] for p in abspts]
    return (min(xs), min(ys), max(xs), max(ys))

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else 'LAB5.kicad_pcb'
    with open(path) as f:
        content = f.read()
    tree = parse(tokenize(content))
    result = {}
    for fp in find_all(tree, 'footprint'):
        if not isinstance(fp, list): continue
        ref = None
        for prop in fp:
            if isinstance(prop, list) and prop and prop[0] == 'property' and len(prop) > 2 and prop[1] == 'Reference':
                ref = prop[2]
        if not ref: continue
        pos = get_pos(fp)
        if not pos: continue
        bbox = footprint_bounds(fp, pos)
        result[ref] = {
            'center': [round(pos[0], 3), round(pos[1], 3)],
            'rot': pos[2],
            'courtyard': [round(v, 3) for v in bbox] if bbox else None
        }
    print(json.dumps(result, indent=1))

main()
