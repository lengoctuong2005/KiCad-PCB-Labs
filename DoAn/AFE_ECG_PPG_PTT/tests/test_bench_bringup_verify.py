#!/usr/bin/env python3
import csv
import json
import os
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import unittest
import zipfile
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TOOL_PATH = PROJECT_ROOT / 'tools' / 'bench_bringup_verify.py'
sys.path.insert(0, str(PROJECT_ROOT / 'tools'))
import bench_bringup_verify as bbv


BUYABLE_REFS = [
    'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11',
    'J1', 'J2', 'J3',
    'R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R8', 'R9', 'R10', 'R11', 'R12',
    'R13', 'R14', 'R15', 'R16', 'R17', 'R18', 'R19',
    'U1', 'U2', 'U3',
]
DNP_REFS = ['H1', 'H2', 'H3', 'H4', 'TP1', 'TP2', 'TP3', 'TP4', 'TP5', 'TP6', 'TP7']


def extract_json_from_cli(stdout_text):
    idx = stdout_text.find('{')
    if idx < 0:
        raise AssertionError(f'No JSON found in output: {stdout_text!r}')
    return json.loads(stdout_text[idx:])


def build_valid_preflight_fixture(root_dir):
    root = Path(root_dir)
    (root / 'AFE_ECG_PPG_PTT.kicad_sch').write_text('(kicad_sch)\n', encoding='utf-8')
    (root / 'AFE_ECG_PPG_PTT.kicad_pcb').write_text('(kicad_pcb)\n', encoding='utf-8')

    preflight = root / 'outputs' / 'print_preflight_20261114'
    gerbers = preflight / 'gerbers'
    gerbers.mkdir(parents=True, exist_ok=True)

    via_coords = [(10.0 + (i % 10) * 2.0, 20.0 + (i // 10) * 2.0) for i in range(38)]
    pth_lines = ['M48', 'FMAT,2', 'METRIC', 'T1C0.300', 'T2C1.000', 'T3C3.200', '%', 'G90', 'G05', 'T1']
    for vx, vy in via_coords:
        pth_lines.append(f'X{vx:.3f}Y-{vy:.3f}')
    pth_lines.append('T2')
    for i in range(45):
        pth_lines.append(f'X{60.0 + (i % 2) * 5.0:.3f}Y-{15.0 + (i // 2) * 2.54:.3f}')
    pth_lines.append('T3')
    for hx, hy in [(5.0, 5.0), (5.0, 65.0), (54.0, 6.0), (54.0, 65.0)]:
        pth_lines.append(f'X{hx:.1f}Y-{hy:.1f}')
    pth_lines.extend([
        'T2',
        'X13.5Y-5.55G85X14.5Y-5.55',
        'X15.5Y-7.95G85X16.5Y-7.95',
        'X15.5Y-13.45G85X16.5Y-13.45',
        'M30',
    ])
    (gerbers / 'AFE_ECG_PPG_PTT-PTH.drl').write_text('\n'.join(pth_lines) + '\n', encoding='utf-8')
    (gerbers / 'AFE_ECG_PPG_PTT-NPTH.drl').write_text(
        'M48\nFMAT,2\nMETRIC\n%\nG90\nG05\nM30\n', encoding='utf-8'
    )

    paste_lines = [
        '%FSLAX46Y46*%',
        '%MOMM*%',
        '%ADD13RoundRect,0.250000X-0.275000X-0.275000X0.275000X-0.275000X0.275000X0.275000X-0.275000X0.275000X0*%',
        '%ADD14RoundRect,0.062500X-0.375000X-0.062500X0.375000X-0.062500X0.375000X0.062500X-0.375000X0.062500X0*%',
        'D13*',
        '%TO.C,U1*%',
        'X37350000Y-35350000D03*',
        'X37350000Y-36650000D03*',
        'X38650000Y-35350000D03*',
        'X38650000Y-36650000D03*',
        'D14*',
        'X36062500Y-35000000D03*',
        '%TD*%',
        'M02*',
    ]
    (gerbers / 'AFE_ECG_PPG_PTT-F_Paste.gtp').write_text('\n'.join(paste_lines) + '\n', encoding='utf-8')

    mask_lines = [
        '%FSLAX46Y46*%',
        '%MOMM*%',
        'G36*',
        'X50000000Y-50000000D02*',
        'G01*',
        'X51000000Y-50000000D01*',
        'X51000000Y-51000000D01*',
        'X50000000Y-51000000D01*',
        'X50000000Y-50000000D01*',
        'G37*',
        'M02*',
    ]
    (gerbers / 'AFE_ECG_PPG_PTT-F_Mask.gts').write_text('\n'.join(mask_lines) + '\n', encoding='utf-8')
    (gerbers / 'AFE_ECG_PPG_PTT-B_Mask.gbs').write_text('\n'.join(mask_lines) + '\n', encoding='utf-8')

    for name in [
        'AFE_ECG_PPG_PTT-F_Cu.gtl',
        'AFE_ECG_PPG_PTT-B_Cu.gbl',
        'AFE_ECG_PPG_PTT-F_Silkscreen.gto',
        'AFE_ECG_PPG_PTT-B_Silkscreen.gbo',
        'AFE_ECG_PPG_PTT-B_Paste.gbp',
        'AFE_ECG_PPG_PTT-Edge_Cuts.gm1',
    ]:
        (gerbers / name).write_text('G04 fixture*\nM02*\n', encoding='utf-8')

    zip_path = preflight / 'GERBER_ONLY_92x70_NOT_CAM_APPROVED.zip'
    with zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
        for member in sorted(bbv.EXPECTED_ZIP_MEMBERS):
            zf.write(gerbers / member, arcname=member)

    bom_path = preflight / 'BOM.csv'
    with bom_path.open('w', encoding='utf-8', newline='') as handle:
        writer = csv.writer(handle)
        writer.writerow(['Reference', 'Value', 'Footprint', 'MPN', 'LCSC', 'Quantity'])
        for idx, ref in enumerate(BUYABLE_REFS, start=1):
            writer.writerow([ref, 'VAL', 'FP', f'MPN-{ref}', f'C{10000 + idx}', '1'])
        for ref in DNP_REFS:
            writer.writerow([ref, 'DNP_ITEM', 'FP', 'PCB_INTEGRATED', 'DNP', '1'])

    (preflight / 'Interactive_Soldering_Guide.html').write_text(
        '<!doctype html><html><body><svg width="92" height="70"></svg></body></html>\n',
        encoding='utf-8',
    )
    (preflight / 'Assembly_1to1.pdf').write_bytes(b'%PDF-1.4\n%%EOF\n')
    (preflight / 'drc.json').write_text(
        json.dumps({'violations': [], 'unconnected_items': [], 'schematic_parity': [], 'ignored_checks': []}),
        encoding='utf-8',
    )

    fw_dir = root / 'firmware' / 'esp32_ptt_streamer'
    (fw_dir / 'build' / 'bootloader').mkdir(parents=True, exist_ok=True)
    (fw_dir / 'build' / 'partition_table').mkdir(parents=True, exist_ok=True)
    (fw_dir / 'main').mkdir(parents=True, exist_ok=True)
    (fw_dir / 'build' / 'esp32_ptt_streamer.bin').write_bytes(b'\x00' * 64)
    (fw_dir / 'build' / 'bootloader' / 'bootloader.bin').write_bytes(b'\x00' * 64)
    (fw_dir / 'build' / 'partition_table' / 'partition-table.bin').write_bytes(b'\x00' * 64)
    main_bytes = b'void app_main(void) {}\n'
    (fw_dir / 'main.c').write_bytes(main_bytes)
    (fw_dir / 'main' / 'main.c').write_bytes(main_bytes)

    tools_dir = root / 'tools'
    (tools_dir / 'esp32_bench_diag').mkdir(parents=True, exist_ok=True)
    flash_sh = tools_dir / 'flash_esp32.sh'
    flash_sh.write_text(chr(35) + '!/usr/bin/env bash\nexit 0\n', encoding='utf-8')
    os.chmod(flash_sh, 0o755)
    (tools_dir / 'esp32_bench_diag' / 'esp32_bench_diag.ino').write_text('void setup() {}\nvoid loop() {}\n', encoding='utf-8')

    (root / 'software').mkdir(parents=True, exist_ok=True)
    shutil.copy2(PROJECT_ROOT / 'software' / 'ptt_live_analyzer.py', root / 'software' / 'ptt_live_analyzer.py')
    return root


class BenchBringupVerifyTests(unittest.TestCase):
    def test_self_test_cli(self):
        proc = subprocess.run(
            [sys.executable, str(TOOL_PATH), '--self-test'],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr + proc.stdout)
        self.assertIn('SELF-TEST SUMMARY', proc.stdout)
        data = extract_json_from_cli(proc.stdout)
        self.assertTrue(data['passed'])
        self.assertEqual(data['verified_cases'], 9)
        self.assertEqual(data['total_cases'], 9)

    def test_csv_check_cli_pass_and_fail(self):
        with tempfile.TemporaryDirectory(prefix='csv-check-test-') as tmpdir:
            good_csv = Path(tmpdir) / 'good.csv'
            good_csv.write_text('\n'.join(bbv.generate_synthetic_csv_lines()) + '\n', encoding='ascii')
            proc_ok = subprocess.run(
                [sys.executable, str(TOOL_PATH), '--csv-check', str(good_csv)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(proc_ok.returncode, 0, proc_ok.stdout + proc_ok.stderr)
            self.assertIn('TELEMETRY AUDIT (csv-check): PASS', proc_ok.stdout)
            report_ok = extract_json_from_cli(proc_ok.stdout)
            self.assertTrue(report_ok['passed'])
            self.assertEqual(report_ok['metrics']['self_test_lines'], 4)
            self.assertEqual(report_ok['metrics']['i2c_error_count'], 0)

            bad_csv = Path(tmpdir) / 'bad.csv'
            bad_lines = bbv.generate_synthetic_csv_lines(inject_i2c_error=True, inject_lod=True)
            bad_csv.write_text('\n'.join(bad_lines) + '\n', encoding='ascii')
            proc_bad = subprocess.run(
                [sys.executable, str(TOOL_PATH), '--csv-check', str(bad_csv), '--json'],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(proc_bad.returncode, 1)
            report_bad = json.loads(proc_bad.stdout)
            self.assertFalse(report_bad['passed'])
            self.assertFalse(report_bad['checks']['i2c_error_zero'])
            self.assertFalse(report_bad['checks']['lod_clear'])

            proc_missing = subprocess.run(
                [sys.executable, str(TOOL_PATH), '--csv-check', str(Path(tmpdir) / 'missing.csv'), '--json'],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(proc_missing.returncode, 1)

    def test_udp_check_cli_loopback(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as probe:
            probe.bind(('127.0.0.1', 0))
            port = probe.getsockname()[1]

        lines = [
            line
            for line in bbv.generate_synthetic_csv_lines(duration_s=0.3)
            if not line.startswith('[SELF-TEST]') and not line.startswith('seq,')
        ]
        target_hex = f'0100007F:{port:04X}'
        proc = subprocess.Popen(
            [sys.executable, str(TOOL_PATH), '--udp-check', '--bind', '127.0.0.1', '--port', str(port), '--duration', '1.2', '--json'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        try:
            wait_deadline = time.monotonic() + 5.0
            bound = False
            while time.monotonic() < wait_deadline:
                udp_table = Path('/proc/net/udp').read_text(encoding='ascii')
                if target_hex in udp_table:
                    bound = True
                    break
                time.sleep(0.02)
            self.assertTrue(bound, f'UDP listener did not bind to {target_hex}')
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as tx:
                for idx, line in enumerate(lines):
                    tx.sendto((line + '\n').encode('ascii'), ('127.0.0.1', port))
                    if idx % 20 == 19:
                        time.sleep(0.002)
            stdout, stderr = proc.communicate(timeout=10)
        finally:
            if proc.poll() is None:
                proc.kill()
                proc.wait()
        self.assertEqual(proc.returncode, 0, stdout + stderr)
        data = json.loads(stdout)
        self.assertEqual(data['mode'], 'udp-check')
        self.assertTrue(data['passed'])
        self.assertEqual(data['metrics']['packets_total'], len(lines))

    def test_preflight_temp_fixture_10_of_10_pass(self):
        with tempfile.TemporaryDirectory(prefix='preflight-pass-') as tmpdir:
            root = build_valid_preflight_fixture(tmpdir)
            proc = subprocess.run(
                [sys.executable, str(TOOL_PATH), '--preflight', '--project-dir', str(root)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            self.assertIn('PREFLIGHT SUMMARY (10/10 PASS)', proc.stdout)
            data = extract_json_from_cli(proc.stdout)
            self.assertTrue(data['passed'])
            self.assertEqual(data['passed_count'], 10)
            self.assertEqual(data['total_gates'], 10)
            self.assertTrue(all(g['passed'] for g in data['gates']))

    def test_preflight_temp_fixture_negative_gates(self):
        with tempfile.TemporaryDirectory(prefix='preflight-neg-') as tmpdir:
            root = build_valid_preflight_fixture(tmpdir)
            preflight = root / 'outputs' / 'print_preflight_20261114'
            gerbers = preflight / 'gerbers'

            (preflight / 'Interactive_Soldering_Guide.html').unlink()
            res8 = bbv.run_preflight(root)
            self.assertFalse(res8['passed'])
            self.assertFalse(res8['gates'][7]['passed'])

            (preflight / 'Interactive_Soldering_Guide.html').write_text('<html><svg></svg></html>', encoding='utf-8')
            (preflight / 'drc.json').write_text(
                json.dumps({'violations': [{'type': 'clearance'}], 'unconnected_items': [], 'schematic_parity': []}),
                encoding='utf-8',
            )
            res9 = bbv.run_preflight(root)
            self.assertFalse(res9['gates'][8]['passed'])
            (preflight / 'drc.json').write_text(
                json.dumps({'violations': [], 'unconnected_items': [], 'schematic_parity': [], 'ignored_checks': []}),
                encoding='utf-8',
            )

            with (preflight / 'BOM.csv').open('r', encoding='utf-8') as handle:
                bom_rows = list(csv.reader(handle))
            bom_rows[1][4] = ''
            with (preflight / 'BOM.csv').open('w', encoding='utf-8', newline='') as handle:
                csv.writer(handle).writerows(bom_rows)
            res5 = bbv.run_preflight(root)
            self.assertFalse(res5['gates'][4]['passed'])
            bom_rows[1][4] = 'C10001'
            with (preflight / 'BOM.csv').open('w', encoding='utf-8', newline='') as handle:
                csv.writer(handle).writerows(bom_rows)

            fmask = gerbers / 'AFE_ECG_PPG_PTT-F_Mask.gts'
            orig_mask = fmask.read_text(encoding='utf-8')
            exposed_mask = orig_mask.replace(
                'M02*',
                'G36*\nX9500000Y-19500000D02*\nG01*\nX10500000Y-19500000D01*\nX10500000Y-20500000D01*\nX9500000Y-20500000D01*\nX9500000Y-19500000D01*\nG37*\nM02*',
            )
            fmask.write_text(exposed_mask, encoding='utf-8')
            res4 = bbv.run_preflight(root)
            self.assertFalse(res4['gates'][3]['passed'])
            fmask.write_text(orig_mask, encoding='utf-8')

            (root / 'firmware' / 'esp32_ptt_streamer' / 'main.c').write_bytes(b'modified\n')
            res6 = bbv.run_preflight(root)
            self.assertFalse(res6['gates'][5]['passed'])

    def test_preflight_live_repo_clean_behavior(self):
        proc = subprocess.run(
            [sys.executable, str(TOOL_PATH), '--preflight', '--project-dir', str(PROJECT_ROOT)],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertIn(proc.returncode, (0, 1), proc.stderr + proc.stdout)
        self.assertIn('PREFLIGHT SUMMARY', proc.stdout)
        data = extract_json_from_cli(proc.stdout)
        self.assertEqual(data['total_gates'], 10)
        gates_by_id = {g['id']: g for g in data['gates']}
        for core_gate in (1, 2, 3, 4, 6, 7, 9, 10):
            self.assertTrue(gates_by_id[core_gate]['passed'], f'Core gate {core_gate} failed: {gates_by_id[core_gate]}')
        if proc.returncode == 0:
            self.assertEqual(data['passed_count'], 10)
            self.assertTrue(data['passed'])

    def test_owned_files_have_no_comments(self):
        triple_dq = '"' * 3
        triple_sq = "'" * 3
        hash_bang = chr(35) + '!'
        py_sh_kconfig = [
            PROJECT_ROOT / 'firmware' / 'esp32_ptt_streamer' / 'main' / 'Kconfig.projbuild',
            PROJECT_ROOT / 'tools' / 'flash_esp32.sh',
            PROJECT_ROOT / 'tools' / 'bench_bringup_verify.py',
            PROJECT_ROOT / 'tests' / 'test_bench_bringup_verify.py',
        ]
        for path in py_sh_kconfig:
            lines = path.read_text(encoding='utf-8').splitlines()
            for lineno, line in enumerate(lines, start=1):
                if lineno == 1 and line.startswith(hash_bang):
                    continue
                self.assertNotIn(chr(35), line, f'{path}:{lineno} contains hash char')
                self.assertNotIn(triple_dq, line, f'{path}:{lineno} contains triple double quotes')
                self.assertNotIn(triple_sq, line, f'{path}:{lineno} contains triple single quotes')

        c_ino = [
            PROJECT_ROOT / 'firmware' / 'esp32_ptt_streamer' / 'main' / 'esp32_ptt_streamer.h',
            PROJECT_ROOT / 'firmware' / 'esp32_ptt_streamer' / 'tests' / 'test_ptt_firmware_logic.c',
            PROJECT_ROOT / 'tools' / 'esp32_bench_diag' / 'esp32_bench_diag.ino',
        ]
        for path in c_ino:
            text = path.read_text(encoding='utf-8')
            self.assertNotIn('//', text, f'{path} contains //')
            self.assertNotIn('/*', text, f'{path} contains /*')


if __name__ == '__main__':
    unittest.main(verbosity=2)
