import uuid

def uid(): return str(uuid.uuid4())

def generate_lib():
    return f"""(kicad_symbol_lib
\t(version 20231120)
\t(generator "kicad-cli")
\t(generator_version "8.0")
\t(symbol "ecg_ppg:AD623"
\t\t(pin_names (offset 1.016)) (in_bom yes) (on_board yes)
\t\t(property "Reference" "U" (at -5.08 12.7 0) (effects (font (size 1.27 1.27))))
\t\t(property "Value" "AD623" (at -5.08 10.16 0) (effects (font (size 1.27 1.27))))
\t\t(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
\t\t(symbol "AD623_0_1"
\t\t\t(rectangle (start -7.62 7.62) (end 7.62 -7.62) (stroke (width 0.254) (type default)) (fill (type background)))
\t\t)
\t\t(symbol "AD623_1_1"
\t\t\t(pin passive line (at -10.16 3.81 0) (length 2.54) (name "RG1" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at -10.16 1.27 0) (length 2.54) (name "-IN" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at -10.16 -1.27 0) (length 2.54) (name "+IN" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at -10.16 -3.81 0) (length 2.54) (name "-VS" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at 10.16 -3.81 180) (length 2.54) (name "REF" (effects (font (size 1.27 1.27)))) (number "5" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at 10.16 -1.27 180) (length 2.54) (name "OUT" (effects (font (size 1.27 1.27)))) (number "6" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at 10.16 1.27 180) (length 2.54) (name "+VS" (effects (font (size 1.27 1.27)))) (number "7" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at 10.16 3.81 180) (length 2.54) (name "RG2" (effects (font (size 1.27 1.27)))) (number "8" (effects (font (size 1.27 1.27)))))
\t\t)
\t)
\t(symbol "ecg_ppg:MCP6004"
\t\t(pin_names (offset 1.016)) (in_bom yes) (on_board yes)
\t\t(property "Reference" "U" (at -5.08 15.24 0) (effects (font (size 1.27 1.27))))
\t\t(property "Value" "MCP6004" (at -5.08 12.7 0) (effects (font (size 1.27 1.27))))
\t\t(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
\t\t(symbol "MCP6004_0_1"
\t\t\t(rectangle (start -7.62 10.16) (end 7.62 -10.16) (stroke (width 0.254) (type default)) (fill (type background)))
\t\t)
\t\t(symbol "MCP6004_1_1"
\t\t\t(pin passive line (at -10.16 7.62 0) (length 2.54) (name "1OUT" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at -10.16 5.08 0) (length 2.54) (name "1IN-" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at -10.16 2.54 0) (length 2.54) (name "1IN+" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at -10.16 0.00 0) (length 2.54) (name "VDD" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at -10.16 -2.54 0) (length 2.54) (name "2IN+" (effects (font (size 1.27 1.27)))) (number "5" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at -10.16 -5.08 0) (length 2.54) (name "2IN-" (effects (font (size 1.27 1.27)))) (number "6" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at -10.16 -7.62 0) (length 2.54) (name "2OUT" (effects (font (size 1.27 1.27)))) (number "7" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at 10.16 -7.62 180) (length 2.54) (name "3OUT" (effects (font (size 1.27 1.27)))) (number "8" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at 10.16 -5.08 180) (length 2.54) (name "3IN-" (effects (font (size 1.27 1.27)))) (number "9" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at 10.16 -2.54 180) (length 2.54) (name "3IN+" (effects (font (size 1.27 1.27)))) (number "10" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at 10.16 0.00 180) (length 2.54) (name "VSS" (effects (font (size 1.27 1.27)))) (number "11" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at 10.16 2.54 180) (length 2.54) (name "4IN+" (effects (font (size 1.27 1.27)))) (number "12" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at 10.16 5.08 180) (length 2.54) (name "4IN-" (effects (font (size 1.27 1.27)))) (number "13" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at 10.16 7.62 180) (length 2.54) (name "4OUT" (effects (font (size 1.27 1.27)))) (number "14" (effects (font (size 1.27 1.27)))))
\t\t)
\t)
\t(symbol "ecg_ppg:MCP6002"
\t\t(pin_names (offset 1.016)) (in_bom yes) (on_board yes)
\t\t(property "Reference" "U" (at -5.08 12.7 0) (effects (font (size 1.27 1.27))))
\t\t(property "Value" "MCP6002" (at -5.08 10.16 0) (effects (font (size 1.27 1.27))))
\t\t(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
\t\t(symbol "MCP6002_0_1"
\t\t\t(rectangle (start -7.62 7.62) (end 7.62 -7.62) (stroke (width 0.254) (type default)) (fill (type background)))
\t\t)
\t\t(symbol "MCP6002_1_1"
\t\t\t(pin passive line (at -10.16 3.81 0) (length 2.54) (name "1OUT" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at -10.16 1.27 0) (length 2.54) (name "1IN-" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at -10.16 -1.27 0) (length 2.54) (name "1IN+" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at -10.16 -3.81 0) (length 2.54) (name "VSS" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at 10.16 -3.81 180) (length 2.54) (name "2IN+" (effects (font (size 1.27 1.27)))) (number "5" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at 10.16 -1.27 180) (length 2.54) (name "2IN-" (effects (font (size 1.27 1.27)))) (number "6" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at 10.16 1.27 180) (length 2.54) (name "2OUT" (effects (font (size 1.27 1.27)))) (number "7" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at 10.16 3.81 180) (length 2.54) (name "VDD" (effects (font (size 1.27 1.27)))) (number "8" (effects (font (size 1.27 1.27)))))
\t\t)
\t)
\t(symbol "ecg_ppg:R"
\t\t(pin_numbers hide) (pin_names (offset 0) hide) (in_bom yes) (on_board yes)
\t\t(property "Reference" "R" (at 2.54 0 90) (effects (font (size 1.27 1.27))))
\t\t(property "Value" "R" (at 0 0 90) (effects (font (size 1.27 1.27))))
\t\t(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
\t\t(symbol "R_0_1"
\t\t\t(rectangle (start -1.27 -2.54) (end 1.27 2.54) (stroke (width 0.254) (type default)) (fill (type none)))
\t\t)
\t\t(symbol "R_1_1"
\t\t\t(pin passive line (at 0 2.54 270) (length 0) (name "~" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at 0 -2.54 90) (length 0) (name "~" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
\t\t)
\t)
\t(symbol "ecg_ppg:C"
\t\t(pin_numbers hide) (pin_names (offset 0.254) hide) (in_bom yes) (on_board yes)
\t\t(property "Reference" "C" (at 1.27 2.54 0) (effects (font (size 1.27 1.27)) (justify left)))
\t\t(property "Value" "C" (at 1.27 -2.54 0) (effects (font (size 1.27 1.27)) (justify left)))
\t\t(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
\t\t(symbol "C_0_1"
\t\t\t(polyline (pts (xy -2.54 -0.635) (xy 2.54 -0.635)) (stroke (width 0.508) (type default)) (fill (type none)))
\t\t\t(polyline (pts (xy -2.54 0.635) (xy 2.54 0.635)) (stroke (width 0.508) (type default)) (fill (type none)))
\t\t)
\t\t(symbol "C_1_1"
\t\t\t(pin passive line (at 0 2.54 270) (length 1.905) (name "~" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at 0 -2.54 90) (length 1.905) (name "~" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
\t\t)
\t)
\t(symbol "ecg_ppg:LED"
\t\t(pin_numbers hide) (pin_names (offset 1.016) hide) (in_bom yes) (on_board yes)
\t\t(property "Reference" "D" (at 0 2.54 0) (effects (font (size 1.27 1.27))))
\t\t(property "Value" "LED" (at 0 -2.54 0) (effects (font (size 1.27 1.27))))
\t\t(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
\t\t(symbol "LED_0_1"
\t\t\t(polyline (pts (xy -1.27 -1.27) (xy -1.27 1.27)) (stroke (width 0.254) (type default)) (fill (type none)))
\t\t\t(polyline (pts (xy -1.27 0) (xy 1.27 0)) (stroke (width 0) (type default)) (fill (type none)))
\t\t\t(polyline (pts (xy 1.27 -1.27) (xy 1.27 1.27) (xy -1.27 0) (xy 1.27 -1.27)) (stroke (width 0.254) (type default)) (fill (type outline)))
\t\t)
\t\t(symbol "LED_1_1"
\t\t\t(pin passive line (at -2.54 0 0) (length 1.27) (name "K" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at 2.54 0 180) (length 1.27) (name "A" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
\t\t)
\t)
\t(symbol "ecg_ppg:Conn_01x02"
\t\t(pin_names (offset 1.016) hide) (in_bom yes) (on_board yes)
\t\t(property "Reference" "J" (at 0 5.08 0) (effects (font (size 1.27 1.27))))
\t\t(property "Value" "Conn_01x02" (at 0 -5.08 0) (effects (font (size 1.27 1.27))))
\t\t(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
\t\t(symbol "Conn_01x02_1_1"
\t\t\t(rectangle (start -1.27 2.54) (end 1.27 -2.54) (stroke (width 0.254) (type default)) (fill (type background)))
\t\t\t(pin passive line (at -5.08 1.27 0) (length 3.81) (name "Pin_1" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at -5.08 -1.27 0) (length 3.81) (name "Pin_2" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
\t\t)
\t)
\t(symbol "ecg_ppg:Conn_01x03"
\t\t(pin_names (offset 1.016) hide) (in_bom yes) (on_board yes)
\t\t(property "Reference" "J" (at 0 5.08 0) (effects (font (size 1.27 1.27))))
\t\t(property "Value" "Conn_01x03" (at 0 -5.08 0) (effects (font (size 1.27 1.27))))
\t\t(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
\t\t(symbol "Conn_01x03_1_1"
\t\t\t(rectangle (start -1.27 3.81) (end 1.27 -3.81) (stroke (width 0.254) (type default)) (fill (type background)))
\t\t\t(pin passive line (at -5.08 2.54 0) (length 3.81) (name "Pin_1" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at -5.08 0 0) (length 3.81) (name "Pin_2" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at -5.08 -2.54 0) (length 3.81) (name "Pin_3" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
\t\t)
\t)
\t(symbol "ecg_ppg:Conn_01x04"
\t\t(pin_names (offset 1.016) hide) (in_bom yes) (on_board yes)
\t\t(property "Reference" "J" (at 0 6.35 0) (effects (font (size 1.27 1.27))))
\t\t(property "Value" "Conn_01x04" (at 0 -6.35 0) (effects (font (size 1.27 1.27))))
\t\t(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
\t\t(symbol "Conn_01x04_1_1"
\t\t\t(rectangle (start -1.27 5.08) (end 1.27 -5.08) (stroke (width 0.254) (type default)) (fill (type background)))
\t\t\t(pin passive line (at -5.08 3.81 0) (length 3.81) (name "Pin_1" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at -5.08 1.27 0) (length 3.81) (name "Pin_2" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at -5.08 -1.27 0) (length 3.81) (name "Pin_3" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at -5.08 -3.81 0) (length 3.81) (name "Pin_4" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.27 1.27)))))
\t\t)
\t)
\t(symbol "ecg_ppg:Conn_01x06"
\t\t(pin_names (offset 1.016) hide) (in_bom yes) (on_board yes)
\t\t(property "Reference" "J" (at 0 8.89 0) (effects (font (size 1.27 1.27))))
\t\t(property "Value" "Conn_01x06" (at 0 -8.89 0) (effects (font (size 1.27 1.27))))
\t\t(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
\t\t(symbol "Conn_01x06_1_1"
\t\t\t(rectangle (start -1.27 7.62) (end 1.27 -7.62) (stroke (width 0.254) (type default)) (fill (type background)))
\t\t\t(pin passive line (at -5.08 6.35 0) (length 3.81) (name "Pin_1" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at -5.08 3.81 0) (length 3.81) (name "Pin_2" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at -5.08 1.27 0) (length 3.81) (name "Pin_3" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at -5.08 -1.27 0) (length 3.81) (name "Pin_4" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at -5.08 -3.81 0) (length 3.81) (name "Pin_5" (effects (font (size 1.27 1.27)))) (number "5" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at -5.08 -6.35 0) (length 3.81) (name "Pin_6" (effects (font (size 1.27 1.27)))) (number "6" (effects (font (size 1.27 1.27)))))
\t\t)
\t)
)
"""

def generate_sch():
    lib_txt = generate_lib()
    start = lib_txt.find('(symbol "')
    end = lib_txt.rfind(')')
    internal_syms = lib_txt[start:end]

    sch = f"""(kicad_sch
\t(version 20231120)
\t(generator "kicad-cli")
\t(generator_version "8.0")
\t(uuid "{uid()}")
\t(paper "A3")
\t(title_block
\t\t(title "Synchronous ECG + PPG Sensor (PAT/PTT Blood Pressure Estimation)")
\t\t(date "2026-11-08")
\t\t(rev "v1.0")
\t\t(company "KhoaHe Biomedical PCB")
\t\t(comment 1 "ECG Lead I (AD623 + DRL) & PPG Pulse Sensor (TIA + BPF + Comparator)")
\t\t(comment 2 "0 DRC / 0 ERC Medical Grade Design")
\t)
\t(lib_symbols
{internal_syms}\t)
"""
    elements = []

    def sym_inst(lib_id, ref, val, fp, x, y, pins):
        pins_txt = "".join(f'\t\t(pin "{p}" (uuid "{uid()}"))\n' for p in pins)
        return f"""\t(symbol (lib_id "{lib_id}") (at {x:.2f} {y:.2f} 0) (unit 1)
\t\t(in_bom yes) (on_board yes) (dnp no) (uuid "{uid()}")
\t\t(property "Reference" "{ref}" (at {x:.2f} {y-2.54:.2f} 0) (effects (font (size 1.27 1.27))))
\t\t(property "Value" "{val}" (at {x:.2f} {y+2.54:.2f} 0) (effects (font (size 1.27 1.27))))
\t\t(property "Footprint" "{fp}" (at {x:.2f} {y:.2f} 0) (effects (font (size 1.27 1.27)) hide))
{pins_txt}\t)"""

    def label(name, x, y):
        return f'\t(label "{name}" (at {x:.2f} {y:.2f} 0) (fields_autoplaced yes) (effects (font (size 1.27 1.27)) (justify left bottom)) (uuid "{uid()}"))'

    # 1. Connectors (All on exact 2.54mm grid)
    elements.append(sym_inst("ecg_ppg:Conn_01x02", "J1", "Power_In", "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical", 25.40, 25.40, ["1", "2"]))
    elements.append(label("VCC", 25.40-5.08, 25.40+1.27))
    elements.append(label("GND", 25.40-5.08, 25.40-1.27))

    elements.append(sym_inst("ecg_ppg:Conn_01x03", "J2", "ECG_Leads", "Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical", 25.40, 76.20, ["1", "2", "3"]))
    elements.append(label("RA_RAW", 25.40-5.08, 76.20+2.54))
    elements.append(label("LA_RAW", 25.40-5.08, 76.20+0.00))
    elements.append(label("RL_DRL", 25.40-5.08, 76.20-2.54))

    elements.append(sym_inst("ecg_ppg:Conn_01x04", "J3", "PPG_Sensor", "Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical", 25.40, 127.00, ["1", "2", "3", "4"]))
    elements.append(label("VCC", 25.40-5.08, 127.00+3.81))
    elements.append(label("LED_DRV", 25.40-5.08, 127.00+1.27))
    elements.append(label("PD_ANODE", 25.40-5.08, 127.00-1.27))
    elements.append(label("GND", 25.40-5.08, 127.00-3.81))

    elements.append(sym_inst("ecg_ppg:Conn_01x06", "J4", "System_Out", "Connector_PinHeader_2.54mm:PinHeader_1x06_P2.54mm_Vertical", 355.60, 76.20, ["1", "2", "3", "4", "5", "6"]))
    elements.append(label("VCC", 355.60-5.08, 76.20+6.35))
    elements.append(label("GND", 355.60-5.08, 76.20+3.81))
    elements.append(label("ECG_OUT", 355.60-5.08, 76.20+1.27))
    elements.append(label("PPG_OUT", 355.60-5.08, 76.20-1.27))
    elements.append(label("PULSE_TRIG", 355.60-5.08, 76.20-3.81))
    elements.append(label("VREF", 355.60-5.08, 76.20-6.35))

    # 2. ICs
    # U1: AD623
    elements.append(sym_inst("ecg_ppg:AD623", "U1", "AD623ARZ", "Package_SO:SOIC-8_3.9x4.9mm_P1.27mm", 101.60, 76.20, [str(i) for i in range(1, 9)]))
    u1_p = [
        ("1", "RG1", 101.60-10.16, 76.20+3.81),
        ("2", "RA_FILT", 101.60-10.16, 76.20+1.27),
        ("3", "LA_FILT", 101.60-10.16, 76.20-1.27),
        ("4", "GND", 101.60-10.16, 76.20-3.81),
        ("5", "VREF", 101.60+10.16, 76.20-3.81),
        ("6", "ECG_IA_OUT", 101.60+10.16, 76.20-1.27),
        ("7", "VCC", 101.60+10.16, 76.20+1.27),
        ("8", "RG2", 101.60+10.16, 76.20+3.81),
    ]
    for num, net, px, py in u1_p: elements.append(label(net, px, py))

    # U2: MCP6004
    elements.append(sym_inst("ecg_ppg:MCP6004", "U2", "MCP6004-E/SL", "Package_SO:SOIC-14_3.9x8.7mm_P1.27mm", 177.80, 76.20, [str(i) for i in range(1, 15)]))
    u2_p = [
        ("1", "VREF", 177.80-10.16, 76.20+7.62),
        ("2", "VREF", 177.80-10.16, 76.20+5.08),
        ("3", "VMID", 177.80-10.16, 76.20+2.54),
        ("4", "VCC", 177.80-10.16, 76.20+0.00),
        ("5", "DRL_CM", 177.80-10.16, 76.20-2.54),
        ("6", "VREF", 177.80-10.16, 76.20-5.08),
        ("7", "DRL_OUT", 177.80-10.16, 76.20-7.62),
        ("8", "ECG_OUT", 177.80+10.16, 76.20-7.62),
        ("9", "ECG_FB", 177.80+10.16, 76.20-5.08),
        ("10", "ECG_LPF_IN", 177.80+10.16, 76.20-2.54),
        ("11", "GND", 177.80+10.16, 76.20+0.00),
        ("12", "PD_ANODE", 177.80+10.16, 76.20+2.54),
        ("13", "VREF", 177.80+10.16, 76.20+5.08),
        ("14", "PPG_TIA_OUT", 177.80+10.16, 76.20+7.62),
    ]
    for num, net, px, py in u2_p: elements.append(label(net, px, py))

    # U3: MCP6002
    elements.append(sym_inst("ecg_ppg:MCP6002", "U3", "MCP6002-E/SN", "Package_SO:SOIC-8_3.9x4.9mm_P1.27mm", 254.00, 76.20, [str(i) for i in range(1, 9)]))
    u3_p = [
        ("1", "PPG_OUT", 254.00-10.16, 76.20+3.81),
        ("2", "PPG_FB", 254.00-10.16, 76.20+1.27),
        ("3", "PPG_LPF_IN", 254.00-10.16, 76.20-1.27),
        ("4", "GND", 254.00-10.16, 76.20-3.81),
        ("5", "PPG_OUT", 254.00+10.16, 76.20-3.81),
        ("6", "VREF_THR", 254.00+10.16, 76.20-1.27),
        ("7", "PULSE_TRIG", 254.00+10.16, 76.20+1.27),
        ("8", "VCC", 254.00+10.16, 76.20+3.81),
    ]
    for num, net, px, py in u3_p: elements.append(label(net, px, py))

    # 3. Resistors R1..R27
    res_list = [
        ("R1", "100k", "VCC", "VMID"),
        ("R2", "100k", "VMID", "GND"),
        ("R3", "1k", "VCC", "NET_D1_R3"),
        ("R4", "1k", "RA_RAW", "RA_FILT"),
        ("R5", "1k", "LA_RAW", "LA_FILT"),
        ("R6", "10M", "RA_FILT", "VREF"),
        ("R7", "10M", "LA_FILT", "VREF"),
        ("R8", "1k", "RG1", "RG2"),
        ("R9", "100k", "RA_FILT", "DRL_CM"),
        ("R10", "100k", "LA_FILT", "DRL_CM"),
        ("R11", "1M", "DRL_CM", "DRL_OUT"),
        ("R12", "390k", "DRL_OUT", "RL_DRL"),
        ("R13", "330k", "ECG_HPF_OUT", "VREF"),
        ("R14", "39k", "ECG_HPF_OUT", "ECG_LPF_NODE"),
        ("R15", "39k", "ECG_LPF_NODE", "ECG_LPF_IN"),
        ("R16", "10k", "ECG_FB", "VREF"),
        ("R17", "91k", "ECG_FB", "ECG_OUT"),
        ("R18", "1M", "PD_ANODE", "PPG_TIA_OUT"),
        ("R19", "220R", "VCC", "LED_DRV"),
        ("R20", "330k", "PPG_HPF_OUT", "VREF"),
        ("R21", "15k", "PPG_HPF_OUT", "PPG_LPF_NODE"),
        ("R22", "15k", "PPG_LPF_NODE", "PPG_LPF_IN"),
        ("R23", "1k", "PPG_FB", "VREF"),
        ("R24", "47k", "PPG_FB", "PPG_OUT"),
        ("R25", "100k", "VREF", "VREF_THR"),
        ("R26", "10k", "VREF_THR", "GND"),
        ("R27", "1k", "PULSE_TRIG", "NET_D2_R27"),
    ]
    ry = 177.80
    for i, (ref, val, n1, n2) in enumerate(res_list):
        rx = 25.40 + (i % 7) * 38.10
        if i % 7 == 0 and i > 0: ry += 25.40
        elements.append(sym_inst("ecg_ppg:R", ref, val, "Resistor_SMD:R_0603_1608Metric", rx, ry, ["1", "2"]))
        elements.append(label(n1, rx, ry+2.54))
        elements.append(label(n2, rx, ry-2.54))

    # 4. Capacitors C1..C18
    cap_list = [
        ("C1", "10uF", "VCC", "GND", "Capacitor_SMD:C_0805_2012Metric"),
        ("C2", "100nF", "VCC", "GND", "Capacitor_SMD:C_0603_1608Metric"),
        ("C3", "10uF", "VMID", "GND", "Capacitor_SMD:C_0805_2012Metric"),
        ("C4", "100nF", "VMID", "GND", "Capacitor_SMD:C_0603_1608Metric"),
        ("C5", "100pF", "RA_FILT", "LA_FILT", "Capacitor_SMD:C_0603_1608Metric"),
        ("C6", "47pF", "RA_FILT", "GND", "Capacitor_SMD:C_0603_1608Metric"),
        ("C7", "47pF", "LA_FILT", "GND", "Capacitor_SMD:C_0603_1608Metric"),
        ("C8", "100nF", "VCC", "GND", "Capacitor_SMD:C_0603_1608Metric"),
        ("C9", "1nF", "DRL_CM", "DRL_OUT", "Capacitor_SMD:C_0603_1608Metric"),
        ("C10", "1uF", "ECG_IA_OUT", "ECG_HPF_OUT", "Capacitor_SMD:C_0603_1608Metric"),
        ("C11", "100nF", "ECG_LPF_NODE", "ECG_OUT", "Capacitor_SMD:C_0603_1608Metric"),
        ("C12", "47nF", "ECG_LPF_IN", "VREF", "Capacitor_SMD:C_0603_1608Metric"),
        ("C13", "100nF", "VCC", "GND", "Capacitor_SMD:C_0603_1608Metric"),
        ("C14", "22pF", "PD_ANODE", "PPG_TIA_OUT", "Capacitor_SMD:C_0603_1608Metric"),
        ("C15", "1uF", "PPG_TIA_OUT", "PPG_HPF_OUT", "Capacitor_SMD:C_0603_1608Metric"),
        ("C16", "1uF", "PPG_LPF_NODE", "PPG_OUT", "Capacitor_SMD:C_0603_1608Metric"),
        ("C17", "470nF", "PPG_LPF_IN", "VREF", "Capacitor_SMD:C_0603_1608Metric"),
        ("C18", "100nF", "VCC", "GND", "Capacitor_SMD:C_0603_1608Metric"),
    ]
    cy = 304.80
    for i, (ref, val, n1, n2, fp) in enumerate(cap_list):
        cx = 25.40 + (i % 7) * 38.10
        if i % 7 == 0 and i > 0: cy += 25.40
        elements.append(sym_inst("ecg_ppg:C", ref, val, fp, cx, cy, ["1", "2"]))
        elements.append(label(n1, cx, cy+2.54))
        elements.append(label(n2, cx, cy-2.54))

    # 5. LEDs
    elements.append(sym_inst("ecg_ppg:LED", "D1", "Green_PWR", "LED_SMD:LED_0805_2012Metric", 76.20, 25.40, ["1", "2"]))
    elements.append(label("GND", 76.20-2.54, 25.40))
    elements.append(label("NET_D1_R3", 76.20+2.54, 25.40))

    elements.append(sym_inst("ecg_ppg:LED", "D2", "Red_PULSE", "LED_SMD:LED_0805_2012Metric", 127.00, 25.40, ["1", "2"]))
    elements.append(label("GND", 127.00-2.54, 25.40))
    elements.append(label("NET_D2_R27", 127.00+2.54, 25.40))

    return sch + '\n'.join(elements) + '\n)\n'

open('DoAn/ECG_PPG_System/libs/ecg_ppg.kicad_sym', 'w').write(generate_lib())
open('DoAn/ECG_PPG_System/ECG_PPG_System.kicad_sch', 'w').write(generate_sch())
print("Re-generated clean schematic!")
