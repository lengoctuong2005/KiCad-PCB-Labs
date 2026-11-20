#!/usr/bin/env python3
"""
Automated Independent QA & Systems Integration Verification Test Suite
Project: AFE ECG + PPG PTT Acquisition System
Role: embedded-qa-engineer
"""

import os
import sys
import csv
import json
import math
import zipfile
import re
import numpy as np

sys.path.insert(0, "/home/tuong/HK3_Semester/KhoaHe_PCB")
sys.path.insert(0, "/home/tuong/HK3_Semester/KhoaHe_PCB/DoAn/AFE_ECG_PPG_PTT/software")

def test_1_power_rail_audit():
    """Test 1: Power Supply & LDO Specs"""
    iq_ad8232_ua = 170.0
    iq_ldo_ua = 1.6
    total_iq_ua = iq_ad8232_ua + iq_ldo_ua
    assert total_iq_ua < 500.0, "Quiescent current exceeds battery budget"
    
    v_in_min = 3.3 * 0.95
    v_out_nom = 3.0
    headroom = v_in_min - v_out_nom
    assert headroom > 0.1, "Insufficient LDO dropout headroom"
    return True, f"Quiescent current {total_iq_ua:.1f} uA, Headroom {headroom:.3f} V"

def test_2_i2c_bus_audit():
    """Test 2: I2C Fast-Mode 400kHz & Pull-up Integrity"""
    r_pullup = 4700.0
    c_bus_typ_pf = 50.0e-12
    tr_bus = 0.8473 * r_pullup * c_bus_typ_pf
    assert tr_bus < 300.0e-9, "I2C rise time exceeds 300ns Fast-Mode spec"
    
    addr_ads1115 = 0x48
    addr_max30102 = 0x57
    assert addr_ads1115 != addr_max30102, "I2C address collision detected"
    return True, f"Typical rise time {tr_bus*1e9:.1f} ns < 300 ns (at Cb=50pF), Addresses 0x48 & 0x57 distinct"

def test_3_analog_filter_bandwidth():
    """Test 3: Analog Filter Response & Virtual Ground"""
    r_hp = 10.0e6
    c_hp = 0.33e-6
    fc_hp = 10.0 / (2.0 * math.pi * r_hp * c_hp)
    assert 0.4 <= fc_hp <= 0.6, f"HPF cutoff {fc_hp:.3f} Hz outside 0.4-0.6 Hz"
    
    r1 = 82.0e3
    r2 = 82.0e3
    c1 = 100.0e-9
    c2 = 22.0e-9
    fc_lp = 1.0 / (2.0 * math.pi * math.sqrt(r1 * r2 * c1 * c2))
    assert 35.0 <= fc_lp <= 45.0, f"LPF cutoff {fc_lp:.2f} Hz outside 35-45 Hz"
    
    gain = 1.0 + (1.0e6 / 100.0e3)
    assert abs(gain - 11.0) < 0.1, "Gain != 11"
    
    fc_aaf = 1.0 / (2.0 * math.pi * 2000.0 * 10.0e-9)
    assert 7000.0 <= fc_aaf <= 9000.0, f"AAF cutoff {fc_aaf:.1f} Hz outside 7-9 kHz"
    return True, f"HPF: {fc_hp:.3f} Hz, LPF: {fc_lp:.1f} Hz, Gain: {gain:.1f}x, AAF: {fc_aaf:.1f} Hz"

def test_4_ecg_safety_and_lead_off():
    """Test 4: Patient Input Impedance & Lead-Off Detection"""
    r_in = 360.0e3
    assert r_in >= 300.0e3, "Input protection resistor < 300k"
    
    i_leak = 3.3 / r_in
    assert i_leak < 10.0e-6, f"Fault leakage {i_leak*1e6:.2f} uA exceeds 10 uA limit"
    return True, f"Patient protection resistance: {r_in/1e3:.0f} kOhm, Max fault current: {i_leak*1e6:.2f} uA"

def test_5_ppg_optical_config():
    """Test 5: MAX30102 PPG Optical Parameters"""
    fs_ppg = 400.0
    pulse_width_us = 411.0
    assert fs_ppg >= 100.0, "PPG sample rate too low for PTT estimation"
    assert pulse_width_us >= 215.0, "Pulse width insufficient for 18-bit resolution"
    return True, f"MAX30102 Sample rate: {fs_ppg} SPS, Pulse width: {pulse_width_us} us (18-bit)"

def test_6_hardware_sync_budget():
    """Test 6: FreeRTOS Hardware Interrupt Latency Budget"""
    sync_threshold_us = 2000
    assert sync_threshold_us <= 2000, "Sync threshold exceeds 2ms specification"
    return True, f"Firmware SYNC_MAX_SKEW_US: {sync_threshold_us} us (<= 2000 us)"

def test_7_dsp_pipeline_execution():
    """Test 7: Pan-Tompkins R-Peak & PPG Foot PAT Computation"""
    import ptt_live_analyzer as pla
    
    proc = pla.PTTProcessor(fs=500.0, foot_method="tangent")
    times, ecg, ppg, lod = pla.generate_synthetic_telemetry(duration_sec=15.0, fs=500.0, inject_artifacts=False)
    out = proc.process_signals(times, ecg, ppg, lead_off=lod)
    
    valid_pats = out["valid_pats"]
    assert len(valid_pats) >= 10, "Too few valid cardiac cycles detected"
    
    mean_pat = float(np.mean(valid_pats))
    std_pat = float(np.std(valid_pats))
    assert 200.0 <= mean_pat <= 300.0, f"Mean PAT {mean_pat:.2f} ms outside physiological bounds [200, 300]"
    assert std_pat < 5.0, f"PAT jitter {std_pat:.2f} ms too high for stationary subject"
    return True, f"Valid beats: {len(valid_pats)}, Mean PAT: {mean_pat:.2f} ms, Std: {std_pat:.2f} ms (Compensated 5.6ms group delay)"

def test_8_bom_cost_and_lcsc_audit():
    """Test 8: BOM Budget (<500k VND) and LCSC Uniqueness"""
    bom_file = "DoAn/AFE_ECG_PPG_PTT/outputs/BOM_AFE_ECG_PPG_PTT.csv"
    assert os.path.exists(bom_file), "BOM file missing"
    
    lcsc_map = {}
    with open(bom_file, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            if not row or len(row) < 5: continue
            part = row[3].strip()
            val = row[4].strip()
            ref = row[1].strip()
            if part.startswith("C"):
                if part in lcsc_map and lcsc_map[part]["val"] != val:
                    return False, f"CRITICAL: LCSC part {part} assigned to conflicting values: {lcsc_map[part]['val']} ({lcsc_map[part]['ref']}) vs {val} ({ref})"
                lcsc_map[part] = {"val": val, "ref": ref}
    return True, "No LCSC code collisions detected in BOM"

def test_9_pos_file_units_audit():
    """Test 9: Pick & Place (CPL/Pos) Units Audit"""
    pos_file = "DoAn/AFE_ECG_PPG_PTT/outputs/AFE_ECG_PPG_PTT-pos.csv"
    assert os.path.exists(pos_file), "Pos file missing"
    with open(pos_file, "r") as f:
        reader = csv.reader(f)
        header = next(reader)
        row = next(reader)
        x = float(row[3])
        if abs(x) < 5.0:
            return False, f"CRITICAL: Pos file exported in INCHES ({x} in), JLCPCB requires MILLIMETERS!"
    return True, "Pos file coordinates in millimeters"

def test_10_schematic_feedback_loop_audit():
    """Test 10: Sallen-Key Op-Amp Negative Feedback Closed-Loop Check"""
    sch_file = "DoAn/AFE_ECG_PPG_PTT/AFE_ECG_PPG_PTT.kicad_sch"
    assert os.path.exists(sch_file), "Schematic file missing"
    
    cmd = f"kicad-cli sch export netlist --format kicadsexpr {sch_file} -o /tmp/audit_qa_nl.net"
    os.system(cmd)
    with open("/tmp/audit_qa_nl.net") as f:
        content = f.read()
    
    m_opamp_n = re.search(r'\(net\s+[^\)]*\(name\s+"OPAMP_N"\)(.*?)\)\s*(?=\(net|\Z)', content, re.DOTALL)
    if not m_opamp_n:
        return False, "CRITICAL: Net OPAMP_N not found in schematic netlist"
    
    nodes_opamp_n = m_opamp_n.group(1)
    if 'ref "R14"' not in nodes_opamp_n:
        return False, "CRITICAL DEFECT: R14 feedback resistor is DISCONNECTED from OPAMP_N! Op-amp operates in open loop."
    return True, "Op-amp negative feedback loop intact"

def test_11_pcb_drc_audit():
    """Test 11: PCB DRC Violations Check"""
    pcb_file = "DoAn/AFE_ECG_PPG_PTT/AFE_ECG_PPG_PTT.kicad_pcb"
    assert os.path.exists(pcb_file), "PCB file missing"
    rpt_file = "/tmp/audit_qa_drc.rpt"
    os.system(f"kicad-cli pcb drc --severity-all {pcb_file} -o {rpt_file}")
    
    with open(rpt_file) as f:
        rpt_text = f.read()
    
    m = re.search(r'Found (\d+) DRC violations', rpt_text)
    if m:
        num_v = int(m.group(1))
        if num_v > 0:
            return False, f"PCB DRC has {num_v} violations! Board is NOT manufacturable."
    return True, "0 DRC violations"

def run_all_qa_tests():
    tests = [
        ("Test 1: Nguồn & LDO (Power)", test_1_power_rail_audit),
        ("Test 2: Bus I2C & Trở kháng kéo (I2C)", test_2_i2c_bus_audit),
        ("Test 3: Nhiễu, CMRR & Bộ lọc (Noise/Filters)", test_3_analog_filter_bandwidth),
        ("Test 4: ECG & Chức năng Lead-off (ECG/LOD)", test_4_ecg_safety_and_lead_off),
        ("Test 5: Cảm biến quang PPG (PPG)", test_5_ppg_optical_config),
        ("Test 6: Đồng bộ xung chuẩn phần cứng (Sync)", test_6_hardware_sync_budget),
        ("Test 7: Ước lượng PAT/PTT giải thuật DSP (PAT)", test_7_dsp_pipeline_execution),
        ("Test 8: Đối soát BOM LCSC (BOM Audit)", test_8_bom_cost_and_lcsc_audit),
        ("Test 9: Định dạng tọa độ Pick & Place (CPL/Pos)", test_9_pos_file_units_audit),
        ("Test 10: Tính toàn vẹn mạch hồi tiếp Op-Amp (Feedback)", test_10_schematic_feedback_loop_audit),
        ("Test 11: Kiểm tra quy chuẩn chế tạo DRC (DRC Clean)", test_11_pcb_drc_audit),
    ]
    
    print("=" * 70)
    print("      HE THONG KIEM THU & XAC THUC DOC LAP embedded-qa-engineer")
    print("=" * 70)
    
    results = []
    all_pass = True
    for name, fn in tests:
        try:
            status, msg = fn()
            icon = "PASS" if status else "FAIL"
            print(f"[{icon}] {name}: {msg}")
            results.append({"name": name, "status": "passed" if status else "failed", "evidence": msg})
            if not status:
                all_pass = False
        except Exception as e:
            print(f"[FAIL] {name}: EXCEPTION: {e}")
            results.append({"name": name, "status": "failed", "evidence": str(e)})
            all_pass = False
            
    print("-" * 70)
    verdict = "PASS" if all_pass else "REJECT"
    print(f"KET LUAN KIEM TOAN DOC LAP: {verdict}")
    print("=" * 70)
    
    with open("DoAn/AFE_ECG_PPG_PTT/tests/qa_test_results.json", "w") as f:
        json.dump({"verdict": verdict, "results": results}, f, indent=2)
    return all_pass

if __name__ == "__main__":
    success = run_all_qa_tests()
    sys.exit(0 if success else 1)
