#!/usr/bin/env python3
import argparse
import csv
import importlib.util
import json
import math
import os
import re
import socket
import statistics
import subprocess
import sys
import tempfile
import time
import zipfile
from pathlib import Path


EXPECTED_ZIP_MEMBERS = {
    'AFE_ECG_PPG_PTT-F_Cu.gtl',
    'AFE_ECG_PPG_PTT-B_Cu.gbl',
    'AFE_ECG_PPG_PTT-F_Mask.gts',
    'AFE_ECG_PPG_PTT-B_Mask.gbs',
    'AFE_ECG_PPG_PTT-F_Silkscreen.gto',
    'AFE_ECG_PPG_PTT-B_Silkscreen.gbo',
    'AFE_ECG_PPG_PTT-F_Paste.gtp',
    'AFE_ECG_PPG_PTT-B_Paste.gbp',
    'AFE_ECG_PPG_PTT-Edge_Cuts.gm1',
    'AFE_ECG_PPG_PTT-PTH.drl',
    'AFE_ECG_PPG_PTT-NPTH.drl',
}

DNP_REFS = {
    'H1', 'H2', 'H3', 'H4',
    'TP1', 'TP2', 'TP3', 'TP4', 'TP5', 'TP6', 'TP7',
}


def load_analyzer_module(project_dir):
    analyzer_path = Path(project_dir) / 'software' / 'ptt_live_analyzer.py'
    if not analyzer_path.is_file():
        default_path = Path(__file__).resolve().parents[1] / 'software' / 'ptt_live_analyzer.py'
        analyzer_path = default_path
    spec = importlib.util.spec_from_file_location('ptt_live_analyzer', str(analyzer_path))
    if spec is None or spec.loader is None:
        raise ImportError(f'Unable to load analyzer module from {analyzer_path}')
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def parse_excellon_file(path):
    text = path.read_text(encoding='utf-8', errors='replace')
    has_metric = 'METRIC' in text
    has_g90 = 'G90' in text
    tools = {}
    selected = None
    features = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        tool_def = re.fullmatch(r'T(\d+)C([\d.]+)', line)
        if tool_def:
            tools[int(tool_def.group(1))] = float(tool_def.group(2))
            continue
        tool_sel = re.fullmatch(r'T(\d+)', line)
        if tool_sel:
            selected = int(tool_sel.group(1))
            continue
        coord = re.fullmatch(r'X(-?[\d.]+)Y(-?[\d.]+)(?:G85X(-?[\d.]+)Y(-?[\d.]+))?', line)
        if coord:
            diam = tools.get(selected, 0.0)
            x1 = float(coord.group(1))
            y1 = float(coord.group(2))
            is_slot = coord.group(3) is not None
            x2 = float(coord.group(3)) if is_slot else x1
            y2 = float(coord.group(4)) if is_slot else y1
            features.append({
                'tool': selected,
                'diameter_mm': diam,
                'x1': x1,
                'y1': y1,
                'x2': x2,
                'y2': y2,
                'is_slot': is_slot,
            })
    return {
        'has_metric': has_metric,
        'has_g90': has_g90,
        'tools': tools,
        'features': features,
    }


def _gerber_scale(text):
    scale = 1e-6
    fs_match = re.search(r'%FSLAX(\d)(\d)Y(\d)(\d)\*%', text)
    if fs_match:
        dec_x = int(fs_match.group(2))
        scale = 10.0 ** (-dec_x)
    if '%MOIN*%' in text:
        scale *= 25.4
    return scale


def _point_in_polygon(x, y, poly):
    inside = False
    n = len(poly)
    if n < 3:
        return False
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if ((y1 > y) != (y2 > y)):
            x_int = (x2 - x1) * (y - y1) / (y2 - y1) + x1
            if x < x_int:
                inside = not inside
    return inside


def _dist_point_to_segment(px, py, x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    l2 = dx * dx + dy * dy
    if l2 == 0.0:
        return math.hypot(px - x1, py - y1)
    t = max(0.0, min(1.0, ((px - x1) * dx + (py - y1) * dy) / l2))
    return math.hypot(px - (x1 + t * dx), py - (y1 + t * dy))


def _point_near_polygon(x, y, poly, margin_mm=0.05):
    if _point_in_polygon(x, y, poly):
        return True
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if _dist_point_to_segment(x, y, x1, y1, x2, y2) <= margin_mm:
            return True
    return False


def _parse_gerber_apertures(text):
    apertures = {}
    for line in text.splitlines():
        m_rr = re.match(r'%ADD(\d+)RoundRect,([^*]+)\*%', line.strip())
        if m_rr:
            code = int(m_rr.group(1))
            nums = [float(v) for v in m_rr.group(2).split('X')]
            r = nums[0] if nums else 0.0
            coords = nums[1:9]
            xs = coords[0::2]
            ys = coords[1::2]
            if xs and ys:
                w = (max(xs) - min(xs)) + 2.0 * r
                h = (max(ys) - min(ys)) + 2.0 * r
            else:
                w = h = 2.0 * r
            apertures[code] = ('rect', w, h)
            continue
        m_rect = re.match(r'%ADD(\d+)R,([^*]+)\*%', line.strip())
        if m_rect:
            code = int(m_rect.group(1))
            nums = [float(v) for v in m_rect.group(2).split('X')]
            w = nums[0]
            h = nums[1] if len(nums) > 1 else nums[0]
            apertures[code] = ('rect', w, h)
            continue
        m_circ = re.match(r'%ADD(\d+)C,([^*]+)\*%', line.strip())
        if m_circ:
            code = int(m_circ.group(1))
            nums = [float(v) for v in m_circ.group(2).split('X')]
            d = nums[0]
            apertures[code] = ('circle', d, d)
            continue
    return apertures


def parse_paste_u1_windows(paste_path):
    text = paste_path.read_text(encoding='utf-8', errors='replace')
    scale = _gerber_scale(text)
    apertures = _parse_gerber_apertures(text)
    current_comp = None
    current_ap = None
    in_region = False
    region_pts = []
    u1_ep_windows = 0
    u1_total_shapes = 0

    for raw in text.splitlines():
        line = raw.strip()
        m_comp = re.fullmatch(r'%TO\.C,([^*]+)\*%', line)
        if m_comp:
            current_comp = m_comp.group(1)
            continue
        if line == '%TD*%':
            current_comp = None
            continue
        m_ap = re.fullmatch(r'D(\d+)\*', line)
        if m_ap and int(m_ap.group(1)) >= 10:
            current_ap = int(m_ap.group(1))
            continue
        if line == 'G36*':
            in_region = True
            region_pts = []
            continue
        if line == 'G37*':
            if in_region and current_comp == 'U1' and region_pts:
                u1_total_shapes += 1
                xs = [p[0] for p in region_pts]
                ys = [p[1] for p in region_pts]
                w = max(xs) - min(xs)
                h = max(ys) - min(ys)
                if 0.85 <= w <= 1.30 and 0.85 <= h <= 1.30:
                    u1_ep_windows += 1
            in_region = False
            region_pts = []
            continue
        m_xy = re.fullmatch(r'X(-?\d+)Y(-?\d+)D(\d+)\*', line)
        if m_xy:
            x = int(m_xy.group(1)) * scale
            y = int(m_xy.group(2)) * scale
            d_code = int(m_xy.group(3))
            if in_region:
                region_pts.append((x, y))
            elif d_code == 3 and current_comp == 'U1':
                u1_total_shapes += 1
                ap = apertures.get(current_ap)
                if ap is not None:
                    _, w, h = ap
                    if 0.85 <= w <= 1.30 and 0.85 <= h <= 1.30:
                        u1_ep_windows += 1
    return u1_ep_windows, u1_total_shapes


def parse_mask_openings(mask_path):
    text = mask_path.read_text(encoding='utf-8', errors='replace')
    scale = _gerber_scale(text)
    apertures = _parse_gerber_apertures(text)
    polygons = []
    flashes = []
    current_ap = None
    in_region = False
    region_pts = []

    for raw in text.splitlines():
        line = raw.strip()
        m_ap = re.fullmatch(r'D(\d+)\*', line)
        if m_ap and int(m_ap.group(1)) >= 10:
            current_ap = int(m_ap.group(1))
            continue
        if line == 'G36*':
            in_region = True
            region_pts = []
            continue
        if line == 'G37*':
            if in_region and len(region_pts) >= 3:
                xs = [p[0] for p in region_pts]
                ys = [p[1] for p in region_pts]
                polygons.append((min(xs), max(xs), min(ys), max(ys), region_pts))
            in_region = False
            region_pts = []
            continue
        m_xy = re.fullmatch(r'X(-?\d+)Y(-?\d+)D(\d+)\*', line)
        if m_xy:
            x = int(m_xy.group(1)) * scale
            y = int(m_xy.group(2)) * scale
            d_code = int(m_xy.group(3))
            if in_region:
                region_pts.append((x, y))
            elif d_code == 3:
                ap = apertures.get(current_ap)
                w = ap[1] if ap is not None else 0.5
                h = ap[2] if ap is not None else 0.5
                flashes.append((x, y, w, h))
    return polygons, flashes


def count_exposed_vias(via_coords, polygons, flashes, margin_mm=0.05):
    exposed = []
    for vx, vy in via_coords:
        hit = False
        for xmin, xmax, ymin, ymax, poly in polygons:
            if xmin - margin_mm <= vx <= xmax + margin_mm and ymin - margin_mm <= vy <= ymax + margin_mm:
                if _point_near_polygon(vx, vy, poly, margin_mm=margin_mm):
                    hit = True
                    break
        if not hit:
            for fx, fy, w, h in flashes:
                if abs(vx - fx) <= (w / 2.0 + margin_mm) and abs(vy - fy) <= (h / 2.0 + margin_mm):
                    hit = True
                    break
        if hit:
            exposed.append((vx, vy))
    return exposed


def run_preflight(project_dir):
    project_dir = Path(project_dir).resolve()
    preflight_dir = project_dir / 'outputs' / 'print_preflight_20261114'
    gerbers_dir = preflight_dir / 'gerbers'
    gates = []

    def add_gate(gate_id, name, passed, detail):
        gates.append({
            'id': gate_id,
            'name': name,
            'passed': bool(passed),
            'detail': detail,
        })

    sch_path = project_dir / 'AFE_ECG_PPG_PTT.kicad_sch'
    pcb_path = project_dir / 'AFE_ECG_PPG_PTT.kicad_pcb'
    g1_ok = sch_path.is_file() and sch_path.stat().st_size > 0 and pcb_path.is_file() and pcb_path.stat().st_size > 0
    add_gate(1, 'kicad_sources', g1_ok,
             f'sch={sch_path.is_file()}, pcb={pcb_path.is_file()}')

    zip_path = preflight_dir / 'GERBER_ONLY_92x70_NOT_CAM_APPROVED.zip'
    g2_ok = False
    g2_detail = f'missing {zip_path}'
    if zip_path.is_file() and gerbers_dir.is_dir():
        try:
            with zipfile.ZipFile(zip_path, 'r') as zf:
                names = zf.namelist()
                crc_err = zf.testzip()
                exact_set = len(names) == len(EXPECTED_ZIP_MEMBERS) and set(names) == EXPECTED_ZIP_MEMBERS
                byte_matches = False
                if exact_set and crc_err is None:
                    byte_matches = all(
                        (gerbers_dir / n).is_file() and zf.read(n) == (gerbers_dir / n).read_bytes()
                        for n in names
                    )
                g2_ok = exact_set and crc_err is None and byte_matches
                g2_detail = f'members={len(names)}/11, crc_ok={crc_err is None}, bytes_match={byte_matches}'
        except (zipfile.BadZipFile, OSError) as exc:
            g2_detail = f'zip error: {exc}'
    add_gate(2, 'gerber_zip', g2_ok, g2_detail)

    pth_path = gerbers_dir / 'AFE_ECG_PPG_PTT-PTH.drl'
    npth_path = gerbers_dir / 'AFE_ECG_PPG_PTT-NPTH.drl'
    via_coords = []
    g3_ok = False
    g3_detail = 'missing drill files'
    if pth_path.is_file() and npth_path.is_file():
        pth_data = parse_excellon_file(pth_path)
        npth_data = parse_excellon_file(npth_path)
        pth_count = len(pth_data['features'])
        slot_count = sum(1 for f in pth_data['features'] if f['is_slot'])
        npth_count = len(npth_data['features'])
        via_coords = [
            (f['x1'], f['y1'])
            for f in pth_data['features']
            if not f['is_slot'] and 0.25 <= f['diameter_mm'] <= 0.35
        ]
        g3_ok = (
            pth_data['has_metric'] and pth_data['has_g90']
            and npth_data['has_metric'] and npth_data['has_g90']
            and pth_count == 90 and slot_count == 3 and npth_count == 0
            and len(via_coords) == 38
        )
        g3_detail = f'pth={pth_count}/90, slots={slot_count}/3, vias={len(via_coords)}/38, npth={npth_count}/0'
    add_gate(3, 'drill_features', g3_ok, g3_detail)

    paste_path = gerbers_dir / 'AFE_ECG_PPG_PTT-F_Paste.gtp'
    fmask_path = gerbers_dir / 'AFE_ECG_PPG_PTT-F_Mask.gts'
    bmask_path = gerbers_dir / 'AFE_ECG_PPG_PTT-B_Mask.gbs'
    g4_ok = False
    g4_detail = 'missing paste/mask gerbers or vias'
    if paste_path.is_file() and fmask_path.is_file() and bmask_path.is_file() and len(via_coords) == 38:
        u1_ep_windows, u1_shapes = parse_paste_u1_windows(paste_path)
        f_polys, f_flashes = parse_mask_openings(fmask_path)
        b_polys, b_flashes = parse_mask_openings(bmask_path)
        f_exposed = count_exposed_vias(via_coords, f_polys, f_flashes)
        b_exposed = count_exposed_vias(via_coords, b_polys, b_flashes)
        g4_ok = u1_ep_windows == 4 and len(f_exposed) == 0 and len(b_exposed) == 0
        g4_detail = (
            f'u1_ep_windows={u1_ep_windows}/4 (u1_pads={u1_shapes}), '
            f'f_tented={38 - len(f_exposed)}/38, b_tented={38 - len(b_exposed)}/38'
        )
    add_gate(4, 'paste_and_tented_vias', g4_ok, g4_detail)

    bom_path = preflight_dir / 'BOM.csv'
    g5_ok = False
    g5_detail = f'missing {bom_path}'
    if bom_path.is_file():
        try:
            with bom_path.open('r', encoding='utf-8-sig', newline='') as handle:
                reader = csv.DictReader(handle)
                cols = set(reader.fieldnames or [])
                if not {'Reference', 'MPN', 'LCSC'}.issubset(cols):
                    g5_detail = f'missing MPN/LCSC columns in {bom_path.name} (found {sorted(cols)})'
                else:
                    seen_refs = {}
                    for row in reader:
                        raw_refs = (row.get('Reference') or '').strip()
                        mpn = (row.get('MPN') or '').strip()
                        lcsc = (row.get('LCSC') or '').strip()
                        for ref in [r.strip() for r in raw_refs.split(',') if r.strip()]:
                            seen_refs[ref] = (mpn, lcsc)
                    buyable_bad = []
                    dnp_bad = []
                    buyable_count = 0
                    dnp_count = 0
                    for ref, (mpn, lcsc) in seen_refs.items():
                        if ref in DNP_REFS:
                            dnp_count += 1
                            if lcsc.upper() != 'DNP':
                                dnp_bad.append(ref)
                        else:
                            buyable_count += 1
                            if not mpn or mpn.upper() in {'DNP', 'N/A', 'NONE', 'TBD'} or not re.fullmatch(r'C\d+', lcsc):
                                buyable_bad.append(ref)
                    missing_dnp = sorted(DNP_REFS - set(seen_refs.keys()))
                    g5_ok = (
                        len(seen_refs) == 46
                        and buyable_count == 35
                        and dnp_count == 11
                        and not missing_dnp
                        and not buyable_bad
                        and not dnp_bad
                    )
                    g5_detail = (
                        f'total={len(seen_refs)}/46, buyable_ok={buyable_count - len(buyable_bad)}/35, '
                        f'dnp_ok={dnp_count - len(dnp_bad)}/11'
                    )
                    if buyable_bad:
                        g5_detail += f', bad_buyable={buyable_bad[:5]}'
                    if dnp_bad or missing_dnp:
                        g5_detail += f', bad_dnp={dnp_bad + missing_dnp}'
        except (OSError, csv.Error) as exc:
            g5_detail = f'bom read error: {exc}'
    add_gate(5, 'bom_mpn_lcsc', g5_ok, g5_detail)

    fw_dir = project_dir / 'firmware' / 'esp32_ptt_streamer'
    app_bin = fw_dir / 'build' / 'esp32_ptt_streamer.bin'
    boot_bin = fw_dir / 'build' / 'bootloader' / 'bootloader.bin'
    part_bin = fw_dir / 'build' / 'partition_table' / 'partition-table.bin'
    root_main = fw_dir / 'main.c'
    sub_main = fw_dir / 'main' / 'main.c'
    bins_ok = all(p.is_file() and p.stat().st_size > 0 for p in (app_bin, boot_bin, part_bin))
    parity_ok = root_main.is_file() and sub_main.is_file() and root_main.read_bytes() == sub_main.read_bytes()
    g6_ok = bins_ok and parity_ok
    add_gate(6, 'firmware_binaries', g6_ok,
             f'bins_ok={bins_ok}, main_c_identical={parity_ok}')

    flash_sh = project_dir / 'tools' / 'flash_esp32.sh'
    ino_file = project_dir / 'tools' / 'esp32_bench_diag' / 'esp32_bench_diag.ino'
    sh_ok = flash_sh.is_file() and flash_sh.stat().st_size > 0 and os.access(flash_sh, os.X_OK)
    ino_ok = ino_file.is_file() and ino_file.stat().st_size > 0
    g7_ok = sh_ok and ino_ok
    add_gate(7, 'bringup_tools', g7_ok,
             f'flash_esp32.sh_exec={sh_ok}, esp32_bench_diag.ino={ino_ok}')

    guide_html = preflight_dir / 'Interactive_Soldering_Guide.html'
    asm_pdf = preflight_dir / 'Assembly_1to1.pdf'
    html_ok = False
    if guide_html.is_file() and guide_html.stat().st_size > 0:
        html_head = guide_html.read_text(encoding='utf-8', errors='replace').lower()
        html_ok = '<html' in html_head or '<svg' in html_head
    pdf_ok = asm_pdf.is_file() and asm_pdf.stat().st_size > 0 and asm_pdf.read_bytes()[:5] == b'%PDF-'
    g8_ok = html_ok and pdf_ok
    add_gate(8, 'soldering_and_assembly_guides', g8_ok,
             f'Interactive_Soldering_Guide.html={html_ok}, Assembly_1to1.pdf={pdf_ok}')

    drc_path = preflight_dir / 'drc.json'
    g9_ok = False
    g9_detail = f'missing {drc_path}'
    if drc_path.is_file():
        try:
            drc_data = json.loads(drc_path.read_text(encoding='utf-8'))
            v_cnt = len(drc_data.get('violations', [None]))
            u_cnt = len(drc_data.get('unconnected_items', [None]))
            p_cnt = len(drc_data.get('schematic_parity', [None]))
            i_cnt = len(drc_data.get('ignored_checks', []))
            g9_ok = v_cnt == 0 and u_cnt == 0 and p_cnt == 0 and i_cnt == 0
            g9_detail = f'violations={v_cnt}, unconnected={u_cnt}, parity={p_cnt}, ignored={i_cnt}'
        except (OSError, ValueError, TypeError) as exc:
            g9_detail = f'drc.json error: {exc}'
    add_gate(9, 'drc_clean', g9_ok, g9_detail)

    analyzer_path = project_dir / 'software' / 'ptt_live_analyzer.py'
    g10_ok = False
    g10_detail = f'missing {analyzer_path}'
    if analyzer_path.is_file():
        try:
            proc = subprocess.run(
                [sys.executable, str(analyzer_path), '--simulate'],
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )
            if proc.returncode == 0:
                sim_data = json.loads(proc.stdout)
                beats_cnt = len(sim_data.get('beats', []))
                segs_cnt = sim_data.get('quality', {}).get('analyzed_segments', 0)
                g10_ok = sim_data.get('source') == 'synthetic' and beats_cnt >= 8 and segs_cnt >= 1
                g10_detail = f'rc=0, beats={beats_cnt}, analyzed_segments={segs_cnt}'
            else:
                g10_detail = f'rc={proc.returncode}, stderr={proc.stderr.strip()[:120]}'
        except (subprocess.SubprocessError, ValueError, OSError) as exc:
            g10_detail = f'simulation error: {exc}'
    add_gate(10, 'analyzer_simulation', g10_ok, g10_detail)

    passed_count = sum(1 for g in gates if g['passed'])
    return {
        'mode': 'preflight',
        'project_dir': str(project_dir),
        'passed': passed_count == len(gates),
        'passed_count': passed_count,
        'total_gates': len(gates),
        'gates': gates,
    }


def audit_telemetry_lines(lines, parse_packet_fn, source_label):
    packets = []
    self_test_lines = []
    malformed = 0

    for raw in lines:
        if isinstance(raw, bytes):
            try:
                line = raw.decode('ascii', errors='strict')
            except UnicodeError:
                malformed += 1
                continue
        else:
            line = raw
        stripped = line.strip()
        if not stripped or stripped.startswith('seq,'):
            continue
        if stripped.startswith('[SELF-TEST]'):
            self_test_lines.append(stripped)
            continue
        fields = stripped.split(',')
        if len(fields) != 8:
            malformed += 1
            continue
        try:
            pkt = parse_packet_fn(stripped)
        except (ValueError, UnicodeError):
            malformed += 1
            continue
        packets.append(pkt)

    prev_pkt = None
    prev_e_ts = None
    prev_p_ts = None
    e_timestamps = []
    p_timestamps = []
    ecg_values = []
    ppg_values = []
    skew_values = []

    duplicate_seq = 0
    sequence_discontinuities = 0
    nonmonotonic_ecg_ts = 0
    nonmonotonic_ppg_ts = 0
    i2c_error_count = 0
    fifo_overflow_count = 0
    queue_drop_count = 0
    fifo_burst_count = 0
    timestamp_uncertain_count = 0
    lod_active_count = 0
    lod_pos_count = 0
    lod_neg_count = 0
    saturated_ecg_count = 0
    saturated_ppg_count = 0

    for pkt in packets:
        if prev_pkt is not None:
            delta = (pkt.seq - prev_pkt.seq) % (2 ** 32)
            if delta == 0:
                duplicate_seq += 1
            elif delta != 1:
                sequence_discontinuities += 1
        prev_pkt = pkt

        if pkt.quality_flags & 0x08:
            i2c_error_count += 1
        if pkt.quality_flags & 0x10:
            fifo_overflow_count += 1
        if pkt.quality_flags & 0x20:
            queue_drop_count += 1
        if pkt.quality_flags & 0x40:
            fifo_burst_count += 1
        if pkt.quality_flags & 0x80:
            timestamp_uncertain_count += 1

        if (pkt.lead_off & 0x01) or (pkt.quality_flags & 0x01):
            lod_pos_count += 1
        if (pkt.lead_off & 0x02) or (pkt.quality_flags & 0x02):
            lod_neg_count += 1
        if pkt.lead_off != 0 or (pkt.quality_flags & 0x03) != 0:
            lod_active_count += 1

        if pkt.sample_type == 'E':
            if prev_e_ts is not None and pkt.timestamp_us <= prev_e_ts:
                nonmonotonic_ecg_ts += 1
            prev_e_ts = pkt.timestamp_us
            e_timestamps.append(pkt.timestamp_us)
            ecg_values.append(pkt.ecg_raw)
            skew_values.append(abs(pkt.sync_skew_us))
            if (pkt.quality_flags & 0x04) or abs(pkt.ecg_raw) >= 32700:
                saturated_ecg_count += 1
        else:
            if prev_p_ts is not None and pkt.timestamp_us <= prev_p_ts:
                nonmonotonic_ppg_ts += 1
            prev_p_ts = pkt.timestamp_us
            p_timestamps.append(pkt.timestamp_us)
            ppg_values.append(pkt.ppg_ir)
            if (pkt.quality_flags & 0x04) or not (100 < pkt.ppg_ir < 260000):
                saturated_ppg_count += 1

    e_span_s = (e_timestamps[-1] - e_timestamps[0]) / 1e6 if len(e_timestamps) >= 2 else 0.0
    p_span_s = (p_timestamps[-1] - p_timestamps[0]) / 1e6 if len(p_timestamps) >= 2 else 0.0
    e_rate_hz = (len(e_timestamps) - 1) / e_span_s if e_span_s > 0.0 else 0.0
    p_rate_hz = (len(p_timestamps) - 1) / p_span_s if p_span_s > 0.0 else 0.0

    e_dts = [b - a for a, b in zip(e_timestamps, e_timestamps[1:]) if b > a]
    p_dts = [b - a for a, b in zip(p_timestamps, p_timestamps[1:]) if b > a]
    e_median_hz = 1e6 / statistics.median(e_dts) if e_dts else 0.0
    p_median_hz = 1e6 / statistics.median(p_dts) if p_dts else 0.0

    checks = {
        'has_sufficient_samples': len(e_timestamps) >= 20 and len(p_timestamps) >= 20 and e_span_s > 0.0 and p_span_s > 0.0,
        'no_malformed': malformed == 0,
        'ecg_rate_near_475': 425.0 <= e_rate_hz <= 525.0,
        'ppg_rate_near_400': 360.0 <= p_rate_hz <= 440.0,
        'i2c_error_zero': i2c_error_count == 0,
        'ecg_not_saturated': len(e_timestamps) > 0 and saturated_ecg_count == 0,
        'ppg_not_saturated': len(p_timestamps) > 0 and saturated_ppg_count == 0,
        'lod_clear': lod_active_count == 0,
        'seq_monotonic': sequence_discontinuities == 0 and duplicate_seq == 0,
        'timestamps_monotonic': nonmonotonic_ecg_ts == 0 and nonmonotonic_ppg_ts == 0,
    }

    return {
        'source': source_label,
        'passed': all(checks.values()),
        'checks': checks,
        'metrics': {
            'packets_total': len(packets),
            'packets_e': len(e_timestamps),
            'packets_p': len(p_timestamps),
            'malformed': malformed,
            'e_duration_s': round(e_span_s, 4),
            'p_duration_s': round(p_span_s, 4),
            'e_rate_hz': round(e_rate_hz, 2),
            'e_median_rate_hz': round(e_median_hz, 2),
            'p_rate_hz': round(p_rate_hz, 2),
            'p_median_rate_hz': round(p_median_hz, 2),
            'i2c_error_count': i2c_error_count,
            'fifo_overflow_count': fifo_overflow_count,
            'queue_drop_count': queue_drop_count,
            'fifo_burst_count': fifo_burst_count,
            'timestamp_uncertain_count': timestamp_uncertain_count,
            'lod_active_count': lod_active_count,
            'lod_pos_count': lod_pos_count,
            'lod_neg_count': lod_neg_count,
            'saturated_ecg_count': saturated_ecg_count,
            'saturated_ppg_count': saturated_ppg_count,
            'ecg_min': min(ecg_values) if ecg_values else None,
            'ecg_max': max(ecg_values) if ecg_values else None,
            'ppg_min': min(ppg_values) if ppg_values else None,
            'ppg_max': max(ppg_values) if ppg_values else None,
            'duplicate_seq': duplicate_seq,
            'sequence_discontinuities': sequence_discontinuities,
            'nonmonotonic_ecg_timestamps': nonmonotonic_ecg_ts,
            'nonmonotonic_ppg_timestamps': nonmonotonic_ppg_ts,
            'max_abs_skew_us': max(skew_values) if skew_values else None,
            'self_test_lines': len(self_test_lines),
        },
        'self_test_banner': self_test_lines,
    }


def run_csv_check(file_path, project_dir):
    analyzer = load_analyzer_module(project_dir)
    path = Path(file_path)
    if not path.is_file():
        return {
            'mode': 'csv-check',
            'passed': False,
            'error': f'CSV file not found: {path}',
            'checks': {},
            'metrics': {},
        }
    with path.open('r', encoding='ascii', errors='strict') as handle:
        result = audit_telemetry_lines(handle, analyzer.parse_packet, str(path))
    result['mode'] = 'csv-check'
    return result


def run_udp_check(bind_addr, port, duration, project_dir):
    captured_lines = []
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((bind_addr, port))
        sock.settimeout(0.05)
        deadline = time.monotonic() + duration
        while time.monotonic() < deadline:
            try:
                data, _ = sock.recvfrom(1024)
            except socket.timeout:
                continue
            try:
                text = data.decode('ascii', errors='strict')
            except UnicodeError:
                captured_lines.append(data)
                continue
            for part in text.splitlines():
                if part.strip():
                    captured_lines.append(part)
    analyzer = load_analyzer_module(project_dir)
    result = audit_telemetry_lines(captured_lines, analyzer.parse_packet, f'udp://{bind_addr}:{port}')
    result['mode'] = 'udp-check'
    result['capture_duration_s'] = duration
    return result


def generate_synthetic_csv_lines(duration_s=2.0, e_fs=475.0, p_fs=400.0,
                                 inject_i2c_error=False, inject_sat_ecg=False,
                                 inject_sat_ppg=False, inject_lod=False,
                                 inject_bad_seq=False, inject_bad_ts=False):
    events = []
    n_e = int(round(duration_s * e_fs))
    n_p = int(round(duration_s * p_fs))
    for i in range(n_e):
        t_us = round(1_000_000 + i * (1e6 / e_fs))
        events.append((t_us, 0, i))
    for i in range(n_p):
        t_us = round(1_000_000 + i * (1e6 / p_fs))
        events.append((t_us, 1, i))
    events.sort(key=lambda item: (item[0], item[1]))

    lines = [
        '[SELF-TEST] Step 1 I2C Probe: ADS1115(0x48)=OK MAX30102(0x57)=OK PART_ID=0x15 (PASS)',
        '[SELF-TEST] Step 2 ADS1115 Config: 475SPS AIN0-AIN1 ALERT=GPIO27 cfg=0x04C0 irq_50ms=23 status=PASS',
        '[SELF-TEST] Step 3 MAX30102 Config: 400SPS SpO2/IR INT=GPIO26 irq_50ms=20 status=PASS',
        '[SELF-TEST] Step 4 LOD ADC: GPIO32=120mV(LOW) GPIO33=115mV(LOW) thresh=1400mV GPIO34=1400mV status=PASS',
        'seq,ts_us,ecg_raw,ppg_ir,lod,quality_flags,skew_us,sample_type',
    ]

    last_ppg_ts = 0
    for seq_idx, (t_us, kind, ch_idx) in enumerate(events):
        seq = seq_idx + (5 if (inject_bad_seq and seq_idx == 25) else 0)
        ts_val = (t_us - 5000) if (inject_bad_ts and seq_idx == 30) else t_us
        if kind == 0:
            t_s = (t_us - 1_000_000) / 1e6
            ecg_raw = round(10000.0 * math.sin(2.0 * math.pi * 1.2 * t_s))
            lod = 0
            flags = 0
            if inject_lod and ch_idx == 10:
                lod = 1
                flags |= 0x01
            if inject_sat_ecg and ch_idx == 15:
                ecg_raw = 32767
                flags |= 0x04
            if inject_i2c_error and ch_idx == 20:
                flags |= 0x08
            skew = 0 if last_ppg_ts == 0 else int(ts_val - last_ppg_ts)
            lines.append(f'{seq},{ts_val},{ecg_raw},0,{lod},{flags},{skew},E')
        else:
            t_s = (t_us - 1_000_000) / 1e6
            ppg_ir = round(120000.0 + 15000.0 * math.sin(2.0 * math.pi * 1.2 * t_s))
            flags = 0x80
            if inject_sat_ppg and ch_idx == 12:
                ppg_ir = 261000
                flags |= 0x04
            last_ppg_ts = ts_val
            lines.append(f'{seq},{ts_val},0,{ppg_ir},0,{flags},0,P')
    return lines


def run_self_test(project_dir):
    cases = [
        ('nominal_475_400', {}, True, None),
        ('fail_i2c_error', {'inject_i2c_error': True}, False, 'i2c_error_zero'),
        ('fail_sat_ecg', {'inject_sat_ecg': True}, False, 'ecg_not_saturated'),
        ('fail_sat_ppg', {'inject_sat_ppg': True}, False, 'ppg_not_saturated'),
        ('fail_lod_active', {'inject_lod': True}, False, 'lod_clear'),
        ('fail_bad_ecg_rate', {'e_fs': 200.0}, False, 'ecg_rate_near_475'),
        ('fail_bad_ppg_rate', {'p_fs': 200.0}, False, 'ppg_rate_near_400'),
        ('fail_bad_seq', {'inject_bad_seq': True}, False, 'seq_monotonic'),
        ('fail_bad_ts', {'inject_bad_ts': True}, False, 'timestamps_monotonic'),
    ]
    results = []
    with tempfile.TemporaryDirectory(prefix='bench-selftest-') as tmpdir:
        tmp_path = Path(tmpdir)
        for name, kwargs, expected_pass, expected_failed_check in cases:
            csv_file = tmp_path / f'{name}.csv'
            csv_file.write_text('\n'.join(generate_synthetic_csv_lines(**kwargs)) + '\n', encoding='ascii')
            audit = run_csv_check(csv_file, project_dir)
            ok = audit['passed'] == expected_pass
            if expected_failed_check is not None:
                ok = ok and (audit['checks'].get(expected_failed_check) is False)
            results.append({
                'case': name,
                'expected_pass': expected_pass,
                'actual_pass': audit['passed'],
                'expected_failed_check': expected_failed_check,
                'case_verified': ok,
                'e_rate_hz': audit['metrics'].get('e_rate_hz'),
                'p_rate_hz': audit['metrics'].get('p_rate_hz'),
            })
    all_ok = all(r['case_verified'] for r in results)
    return {
        'mode': 'self-test',
        'passed': all_ok,
        'verified_cases': sum(1 for r in results if r['case_verified']),
        'total_cases': len(results),
        'cases': results,
    }


def format_preflight_table(report):
    lines = [
        f"PREFLIGHT SUMMARY ({report['passed_count']}/{report['total_gates']} PASS) - {report['project_dir']}",
        '+----+--------------------------------+--------+------------------------------------------------------------+',
        '| ID | Gate                           | Status | Detail                                                     |',
        '+----+--------------------------------+--------+------------------------------------------------------------+',
    ]
    for g in report['gates']:
        status = 'PASS' if g['passed'] else 'FAIL'
        detail = g['detail'][:58]
        lines.append(f"| {g['id']:>2} | {g['name']:<30} | {status:<6} | {detail:<58} |")
    lines.append('+----+--------------------------------+--------+------------------------------------------------------------+')
    return '\n'.join(lines)


def format_telemetry_table(report):
    m = report.get('metrics', {})
    lines = [
        f"TELEMETRY AUDIT ({report['mode']}): {'PASS' if report['passed'] else 'FAIL'} - {report.get('source', '')}",
        '+------------------------------+--------+----------------------------------------+',
        '| Check                        | Status | Observed Value                         |',
        '+------------------------------+--------+----------------------------------------+',
    ]
    summary_map = {
        'has_sufficient_samples': f"E={m.get('packets_e', 0)}, P={m.get('packets_p', 0)}",
        'no_malformed': f"malformed={m.get('malformed', 0)}",
        'ecg_rate_near_475': f"{m.get('e_rate_hz', 0)} Hz (med {m.get('e_median_rate_hz', 0)} Hz)",
        'ppg_rate_near_400': f"{m.get('p_rate_hz', 0)} Hz (med {m.get('p_median_rate_hz', 0)} Hz)",
        'i2c_error_zero': f"i2c_err={m.get('i2c_error_count', 0)}",
        'ecg_not_saturated': f"sat={m.get('saturated_ecg_count', 0)}, [{m.get('ecg_min')}, {m.get('ecg_max')}]",
        'ppg_not_saturated': f"sat={m.get('saturated_ppg_count', 0)}, [{m.get('ppg_min')}, {m.get('ppg_max')}]",
        'lod_clear': f"lod_active={m.get('lod_active_count', 0)}",
        'seq_monotonic': f"disc={m.get('sequence_discontinuities', 0)}, dup={m.get('duplicate_seq', 0)}",
        'timestamps_monotonic': f"nonmono_e={m.get('nonmonotonic_ecg_timestamps', 0)}, nonmono_p={m.get('nonmonotonic_ppg_timestamps', 0)}",
    }
    for check_name, passed in report.get('checks', {}).items():
        status = 'PASS' if passed else 'FAIL'
        val = summary_map.get(check_name, '')[:38]
        lines.append(f"| {check_name:<28} | {status:<6} | {val:<38} |")
    lines.append('+------------------------------+--------+----------------------------------------+')
    return '\n'.join(lines)


def format_selftest_table(report):
    lines = [
        f"SELF-TEST SUMMARY ({report['verified_cases']}/{report['total_cases']} VERIFIED): {'PASS' if report['passed'] else 'FAIL'}",
        '+------------------------+----------+--------+--------------------------+',
        '| Case                   | Expected | Actual | Verified                 |',
        '+------------------------+----------+--------+--------------------------+',
    ]
    for c in report['cases']:
        exp_s = 'PASS' if c['expected_pass'] else 'FAIL'
        act_s = 'PASS' if c['actual_pass'] else 'FAIL'
        ver_s = 'PASS' if c['case_verified'] else 'FAIL'
        lines.append(f"| {c['case']:<22} | {exp_s:<8} | {act_s:<6} | {ver_s:<24} |")
    lines.append('+------------------------+----------+--------+--------------------------+')
    return '\n'.join(lines)


def main():
    default_project = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description='AFE ECG+PPG Bench Bring-Up Verification CLI')
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--preflight', action='store_true', help='Verify 10 fabrication, firmware, and tooling gates')
    mode.add_argument('--csv-check', metavar='FILE', help='Audit captured 8-field CSV telemetry file')
    mode.add_argument('--udp-check', action='store_true', help='Capture live UDP telemetry and run audit')
    mode.add_argument('--self-test', action='store_true', help='Run synthetic pass/fail telemetry verification')
    parser.add_argument('--project-dir', default=str(default_project), help='Project root directory')
    parser.add_argument('--port', type=int, default=5005, help='UDP port for --udp-check')
    parser.add_argument('--bind', default='0.0.0.0', help='UDP bind IP for --udp-check')
    parser.add_argument('--duration', type=float, default=5.0, help='UDP capture duration in seconds')
    parser.add_argument('--json', action='store_true', help='Emit JSON only without summary table')
    args = parser.parse_args()

    if not 1 <= args.port <= 65535:
        parser.error('--port must be between 1 and 65535')
    if not math.isfinite(args.duration) or args.duration <= 0:
        parser.error('--duration must be positive and finite')

    if args.preflight:
        report = run_preflight(args.project_dir)
        table = format_preflight_table(report)
    elif args.csv_check:
        report = run_csv_check(args.csv_check, args.project_dir)
        table = format_telemetry_table(report)
    elif args.udp_check:
        report = run_udp_check(args.bind, args.port, args.duration, args.project_dir)
        table = format_telemetry_table(report)
    else:
        report = run_self_test(args.project_dir)
        table = format_selftest_table(report)

    if not args.json:
        print(table)
        print()
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report.get('passed') else 1


if __name__ == '__main__':
    sys.exit(main())
