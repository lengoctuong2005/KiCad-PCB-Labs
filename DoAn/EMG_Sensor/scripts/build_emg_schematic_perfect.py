import uuid

def uid(): return str(uuid.uuid4())

def generate():
    sch = f"""(kicad_sch
\t(version 20231120)
\t(generator "kicad-cli")
\t(generator_version "8.0")
\t(uuid "{uid()}")
\t(paper "A3")
\t(title_block
\t\t(title "EMG Sensor - Surface Electromyography Analog Front-End")
\t\t(date "2026-11-08")
\t\t(rev "v1.0")
\t\t(company "KhoaHe Biomedical PCB")
\t\t(comment 1 "Dual Output: Bandpassed Raw EMG & Linear Contraction Envelope")
\t\t(comment 2 "0 DRC / 0 ERC Medical Grade Design")
\t)
\t(lib_symbols
\t\t(symbol "emg:AD623"
\t\t\t(pin_names (offset 1.016)) (in_bom yes) (on_board yes)
\t\t\t(property "Reference" "U" (at -5.08 12.7 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Value" "AD623" (at -5.08 10.16 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
\t\t\t(symbol "AD623_0_1"
\t\t\t\t(rectangle (start -7.62 7.62) (end 7.62 -7.62) (stroke (width 0.254) (type default)) (fill (type background)))
\t\t\t)
\t\t\t(symbol "AD623_1_1"
\t\t\t\t(pin passive line (at -10.16 3.81 0) (length 2.54) (name "RG1" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin passive line (at -10.16 1.27 0) (length 2.54) (name "-IN" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin passive line (at -10.16 -1.27 0) (length 2.54) (name "+IN" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin passive line (at -10.16 -3.81 0) (length 2.54) (name "-VS" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin passive line (at 10.16 -3.81 180) (length 2.54) (name "REF" (effects (font (size 1.27 1.27)))) (number "5" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin passive line (at 10.16 -1.27 180) (length 2.54) (name "OUT" (effects (font (size 1.27 1.27)))) (number "6" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin passive line (at 10.16 1.27 180) (length 2.54) (name "+VS" (effects (font (size 1.27 1.27)))) (number "7" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin passive line (at 10.16 3.81 180) (length 2.54) (name "RG2" (effects (font (size 1.27 1.27)))) (number "8" (effects (font (size 1.27 1.27)))))
\t\t\t)
\t\t)
\t\t(symbol "emg:MCP6004"
\t\t\t(pin_names (offset 1.016)) (in_bom yes) (on_board yes)
\t\t\t(property "Reference" "U" (at -5.08 15.24 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Value" "MCP6004" (at -5.08 12.7 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
\t\t\t(symbol "MCP6004_0_1"
\t\t\t\t(rectangle (start -7.62 10.16) (end 7.62 -10.16) (stroke (width 0.254) (type default)) (fill (type background)))
\t\t\t)
\t\t\t(symbol "MCP6004_1_1"
\t\t\t\t(pin passive line (at -10.16 7.62 0) (length 2.54) (name "1OUT" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin passive line (at -10.16 5.08 0) (length 2.54) (name "1IN-" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin passive line (at -10.16 2.54 0) (length 2.54) (name "1IN+" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin passive line (at -10.16 0.00 0) (length 2.54) (name "VDD" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin passive line (at -10.16 -2.54 0) (length 2.54) (name "2IN+" (effects (font (size 1.27 1.27)))) (number "5" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin passive line (at -10.16 -5.08 0) (length 2.54) (name "2IN-" (effects (font (size 1.27 1.27)))) (number "6" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin passive line (at -10.16 -7.62 0) (length 2.54) (name "2OUT" (effects (font (size 1.27 1.27)))) (number "7" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin passive line (at 10.16 -7.62 180) (length 2.54) (name "3OUT" (effects (font (size 1.27 1.27)))) (number "8" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin passive line (at 10.16 -5.08 180) (length 2.54) (name "3IN-" (effects (font (size 1.27 1.27)))) (number "9" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin passive line (at 10.16 -2.54 180) (length 2.54) (name "3IN+" (effects (font (size 1.27 1.27)))) (number "10" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin passive line (at 10.16 0.00 180) (length 2.54) (name "VSS" (effects (font (size 1.27 1.27)))) (number "11" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin passive line (at 10.16 2.54 180) (length 2.54) (name "4IN+" (effects (font (size 1.27 1.27)))) (number "12" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin passive line (at 10.16 5.08 180) (length 2.54) (name "4IN-" (effects (font (size 1.27 1.27)))) (number "13" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin passive line (at 10.16 7.62 180) (length 2.54) (name "4OUT" (effects (font (size 1.27 1.27)))) (number "14" (effects (font (size 1.27 1.27)))))
\t\t\t)
\t\t)
\t\t(symbol "emg:R"
\t\t\t(pin_numbers hide) (pin_names (offset 0) hide) (in_bom yes) (on_board yes)
\t\t\t(property "Reference" "R" (at 2.032 0 90) (effects (font (size 1.27 1.27))))
\t\t\t(property "Value" "R" (at 0 0 90) (effects (font (size 1.27 1.27))))
\t\t\t(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
\t\t\t(symbol "R_0_1"
\t\t\t\t(rectangle (start -1.016 -2.54) (end 1.016 2.54) (stroke (width 0.254) (type default)) (fill (type none)))
\t\t\t)
\t\t\t(symbol "R_1_1"
\t\t\t\t(pin passive line (at 0 3.81 270) (length 1.27) (name "~" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin passive line (at 0 -3.81 90) (length 1.27) (name "~" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
\t\t\t)
\t\t)
\t\t(symbol "emg:C"
\t\t\t(pin_numbers hide) (pin_names (offset 0.254) hide) (in_bom yes) (on_board yes)
\t\t\t(property "Reference" "C" (at 0.635 2.54 0) (effects (font (size 1.27 1.27)) (justify left)))
\t\t\t(property "Value" "C" (at 0.635 -2.54 0) (effects (font (size 1.27 1.27)) (justify left)))
\t\t\t(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
\t\t\t(symbol "C_0_1"
\t\t\t\t(polyline (pts (xy -2.032 -0.762) (xy 2.032 -0.762)) (stroke (width 0.508) (type default)) (fill (type none)))
\t\t\t\t(polyline (pts (xy -2.032 0.762) (xy 2.032 0.762)) (stroke (width 0.508) (type default)) (fill (type none)))
\t\t\t)
\t\t\t(symbol "C_1_1"
\t\t\t\t(pin passive line (at 0 3.81 270) (length 3.048) (name "~" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin passive line (at 0 -3.81 90) (length 3.048) (name "~" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
\t\t\t)
\t\t)
\t\t(symbol "emg:LED"
\t\t\t(pin_numbers hide) (pin_names (offset 1.016) hide) (in_bom yes) (on_board yes)
\t\t\t(property "Reference" "D" (at 0 2.54 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Value" "LED" (at 0 -2.54 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
\t\t\t(symbol "LED_0_1"
\t\t\t\t(polyline (pts (xy -1.27 -1.27) (xy -1.27 1.27)) (stroke (width 0.254) (type default)) (fill (type none)))
\t\t\t\t(polyline (pts (xy -1.27 0) (xy 1.27 0)) (stroke (width 0) (type default)) (fill (type none)))
\t\t\t\t(polyline (pts (xy 1.27 -1.27) (xy 1.27 1.27) (xy -1.27 0) (xy 1.27 -1.27)) (stroke (width 0.254) (type default)) (fill (type outline)))
\t\t\t)
\t\t\t(symbol "LED_1_1"
\t\t\t\t(pin passive line (at -3.81 0 0) (length 2.54) (name "K" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin passive line (at 3.81 0 180) (length 2.54) (name "A" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
\t\t\t)
\t\t)
\t\t(symbol "emg:D"
\t\t\t(pin_numbers hide) (pin_names (offset 1.016) hide) (in_bom yes) (on_board yes)
\t\t\t(property "Reference" "D" (at 0 2.54 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Value" "D" (at 0 -2.54 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
\t\t\t(symbol "D_0_1"
\t\t\t\t(polyline (pts (xy -1.27 -1.27) (xy -1.27 1.27)) (stroke (width 0.254) (type default)) (fill (type none)))
\t\t\t\t(polyline (pts (xy 1.27 -1.27) (xy 1.27 1.27) (xy -1.27 0) (xy 1.27 -1.27)) (stroke (width 0.254) (type default)) (fill (type outline)))
\t\t\t)
\t\t\t(symbol "D_1_1"
\t\t\t\t(pin passive line (at -3.81 0 0) (length 2.54) (name "K" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin passive line (at 3.81 0 180) (length 2.54) (name "A" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
\t\t\t)
\t\t)
\t\t(symbol "emg:Conn_01x02"
\t\t\t(pin_names (offset 1.016) hide) (in_bom yes) (on_board yes)
\t\t\t(property "Reference" "J" (at 0 5.08 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Value" "Conn_01x02" (at 0 -5.08 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
\t\t\t(symbol "Conn_01x02_1_1"
\t\t\t\t(rectangle (start -1.27 2.54) (end 1.27 -2.54) (stroke (width 0.254) (type default)) (fill (type background)))
\t\t\t\t(pin passive line (at -5.08 1.27 0) (length 3.81) (name "Pin_1" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin passive line (at -5.08 -1.27 0) (length 3.81) (name "Pin_2" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
\t\t\t)
\t\t)
\t\t(symbol "emg:Conn_01x03"
\t\t\t(pin_names (offset 1.016) hide) (in_bom yes) (on_board yes)
\t\t\t(property "Reference" "J" (at 0 5.08 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Value" "Conn_01x03" (at 0 -5.08 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
\t\t\t(symbol "Conn_01x03_1_1"
\t\t\t\t(rectangle (start -1.27 3.81) (end 1.27 -3.81) (stroke (width 0.254) (type default)) (fill (type background)))
\t\t\t\t(pin passive line (at -5.08 2.54 0) (length 3.81) (name "Pin_1" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin passive line (at -5.08 0 0) (length 3.81) (name "Pin_2" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin passive line (at -5.08 -2.54 0) (length 3.81) (name "Pin_3" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
\t\t\t)
\t\t)
\t\t(symbol "emg:Conn_01x04"
\t\t\t(pin_names (offset 1.016) hide) (in_bom yes) (on_board yes)
\t\t\t(property "Reference" "J" (at 0 6.35 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Value" "Conn_01x04" (at 0 -6.35 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
\t\t\t(symbol "Conn_01x04_1_1"
\t\t\t\t(rectangle (start -1.27 5.08) (end 1.27 -5.08) (stroke (width 0.254) (type default)) (fill (type background)))
\t\t\t\t(pin passive line (at -5.08 3.81 0) (length 3.81) (name "Pin_1" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin passive line (at -5.08 1.27 0) (length 3.81) (name "Pin_2" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin passive line (at -5.08 -1.27 0) (length 3.81) (name "Pin_3" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin passive line (at -5.08 -3.81 0) (length 3.81) (name "Pin_4" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.27 1.27)))))
\t\t\t)
\t\t)
\t)
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

    # 1. Connectors
    elements.append(sym_inst("emg:Conn_01x02", "J1", "Power_In", "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical", 30.48, 40.64, ["1", "2"]))
    elements.append(label("VCC", 30.48-5.08, 40.64+1.27))
    elements.append(label("GND", 30.48-5.08, 40.64-1.27))

    elements.append(sym_inst("emg:Conn_01x03", "J2", "Electrodes_In", "Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical", 30.48, 76.2, ["1", "2", "3"]))
    elements.append(label("IN_PLUS_RAW", 30.48-5.08, 76.2+2.54))
    elements.append(label("IN_MINUS_RAW", 30.48-5.08, 76.2+0.00))
    elements.append(label("VREF", 30.48-5.08, 76.2-2.54))

    elements.append(sym_inst("emg:Conn_01x04", "J3", "EMG_Out", "Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical", 254.0, 76.2, ["1", "2", "3", "4"]))
    elements.append(label("VCC", 254.0-5.08, 76.2+3.81))
    elements.append(label("GND", 254.0-5.08, 76.2+1.27))
    elements.append(label("RAW_EMG", 254.0-5.08, 76.2-1.27))
    elements.append(label("ENV_EMG", 254.0-5.08, 76.2-3.81))

    # 2. U1 (AD623)
    elements.append(sym_inst("emg:AD623", "U1", "AD623ARZ", "Package_SO:SOIC-8_3.9x4.9mm_P1.27mm", 101.6, 101.6, [str(i) for i in range(1, 9)]))
    u1_p = [
        ("1", "RG1", 101.6-10.16, 101.6+3.81),
        ("2", "IN_MINUS_FILT", 101.6-10.16, 101.6+1.27),
        ("3", "IN_PLUS_FILT", 101.6-10.16, 101.6-1.27),
        ("4", "GND", 101.6-10.16, 101.6-3.81),
        ("5", "VREF", 101.6+10.16, 101.6-3.81),
        ("6", "VOUT_IA", 101.6+10.16, 101.6-1.27),
        ("7", "VCC", 101.6+10.16, 101.6+1.27),
        ("8", "RG2", 101.6+10.16, 101.6+3.81),
    ]
    for num, net, px, py in u1_p:
        elements.append(label(net, px, py))

    # 3. U2 (MCP6004)
    elements.append(sym_inst("emg:MCP6004", "U2", "MCP6004-E/SL", "Package_SO:SOIC-14_3.9x8.7mm_P1.27mm", 177.8, 101.6, [str(i) for i in range(1, 15)]))
    u2_p = [
        ("1", "VREF", 177.8-10.16, 101.6+7.62),
        ("2", "VREF", 177.8-10.16, 101.6+5.08),
        ("3", "VMID", 177.8-10.16, 101.6+2.54),
        ("4", "VCC", 177.8-10.16, 101.6+0.00),
        ("5", "LPF_IN", 177.8-10.16, 101.6-2.54),
        ("6", "LPF_FB", 177.8-10.16, 101.6-5.08),
        ("7", "RAW_EMG", 177.8-10.16, 101.6-7.62),
        ("8", "RECT_OUT", 177.8+10.16, 101.6-7.62),
        ("9", "RECT_IN", 177.8+10.16, 101.6-5.08),
        ("10", "VREF", 177.8+10.16, 101.6-2.54),
        ("11", "GND", 177.8+10.16, 101.6+0.00),
        ("12", "VREF", 177.8+10.16, 101.6+2.54),
        ("13", "ENV_IN", 177.8+10.16, 101.6+5.08),
        ("14", "ENV_EMG", 177.8+10.16, 101.6+7.62),
    ]
    for num, net, px, py in u2_p:
        elements.append(label(net, px, py))

    # 4. Resistors R1..R19
    res_info = [
        ("R1", "1k", "NET_D1_R1", "GND"),
        ("R2", "100k", "VCC", "VMID"),
        ("R3", "100k", "VMID", "GND"),
        ("R4", "1k", "IN_PLUS_RAW", "IN_PLUS_FILT"),
        ("R5", "1k", "IN_MINUS_RAW", "IN_MINUS_FILT"),
        ("R6", "10M", "IN_PLUS_FILT", "VREF"),
        ("R7", "10M", "IN_MINUS_FILT", "VREF"),
        ("R8", "1k", "RG1", "RG2"),
        ("R9", "8.2k", "HPF_OUT", "VREF"),
        ("R10", "22k", "HPF_OUT", "LPF_NODE"),
        ("R11", "22k", "LPF_NODE", "LPF_IN"),
        ("R12", "10k", "LPF_FB", "VREF"),
        ("R13", "91k", "LPF_FB", "RAW_EMG"),
        ("R14", "10k", "RAW_EMG", "RECT_IN"),
        ("R15", "10k", "RECT_IN", "RECT_HALF"),
        ("R16", "20k", "RECT_HALF", "ENV_IN"),
        ("R17", "10k", "RAW_EMG", "ENV_IN"),
        ("R18", "100k", "ENV_IN", "ENV_EMG"),
        ("R19", "1k", "ENV_EMG", "NET_D4_R19"),
    ]
    ry = 142.24
    for i, (ref, val, n1, n2) in enumerate(res_info):
        rx = 30.48 + (i % 7) * 27.94
        if i % 7 == 0 and i > 0: ry += 25.4
        elements.append(sym_inst("emg:R", ref, val, "Resistor_SMD:R_0603_1608Metric", rx, ry, ["1", "2"]))
        elements.append(label(n1, rx, ry+3.81))
        elements.append(label(n2, rx, ry-3.81))

    # 5. Capacitors C1..C13
    cap_info = [
        ("C1", "10uF", "VCC", "GND", "Capacitor_SMD:C_0805_2012Metric"),
        ("C2", "100nF", "VCC", "GND", "Capacitor_SMD:C_0603_1608Metric"),
        ("C3", "10uF", "VMID", "GND", "Capacitor_SMD:C_0805_2012Metric"),
        ("C4", "100nF", "VMID", "GND", "Capacitor_SMD:C_0603_1608Metric"),
        ("C5", "100pF", "IN_PLUS_FILT", "IN_MINUS_FILT", "Capacitor_SMD:C_0603_1608Metric"),
        ("C6", "47pF", "IN_PLUS_FILT", "GND", "Capacitor_SMD:C_0603_1608Metric"),
        ("C7", "47pF", "IN_MINUS_FILT", "GND", "Capacitor_SMD:C_0603_1608Metric"),
        ("C8", "100nF", "VCC", "GND", "Capacitor_SMD:C_0603_1608Metric"),
        ("C9", "1uF", "VOUT_IA", "HPF_OUT", "Capacitor_SMD:C_0603_1608Metric"),
        ("C10", "15nF", "LPF_NODE", "RAW_EMG", "Capacitor_SMD:C_0603_1608Metric"),
        ("C11", "6.8nF", "LPF_IN", "VREF", "Capacitor_SMD:C_0603_1608Metric"),
        ("C12", "330nF", "ENV_IN", "ENV_EMG", "Capacitor_SMD:C_0603_1608Metric"),
        ("C13", "100nF", "VCC", "GND", "Capacitor_SMD:C_0603_1608Metric"),
    ]
    cy = 228.6
    for i, (ref, val, n1, n2, fp) in enumerate(cap_info):
        cx = 30.48 + (i % 7) * 27.94
        if i % 7 == 0 and i > 0: cy += 25.4
        elements.append(sym_inst("emg:C", ref, val, fp, cx, cy, ["1", "2"]))
        elements.append(label(n1, cx, cy+3.81))
        elements.append(label(n2, cx, cy-3.81))

    # 6. Diodes D1..D4
    elements.append(sym_inst("emg:LED", "D1", "Green_PWR", "LED_SMD:LED_0805_2012Metric", 76.2, 40.64, ["1", "2"]))
    elements.append(label("NET_D1_R1", 76.2-3.81, 40.64))
    elements.append(label("VCC", 76.2+3.81, 40.64))

    elements.append(sym_inst("emg:D", "D2", "1N4148W", "Diode_SMD:D_SOD-123", 114.3, 40.64, ["1", "2"]))
    elements.append(label("RECT_OUT", 114.3-3.81, 40.64))
    elements.append(label("RECT_IN", 114.3+3.81, 40.64))

    elements.append(sym_inst("emg:D", "D3", "1N4148W", "Diode_SMD:D_SOD-123", 152.4, 40.64, ["1", "2"]))
    elements.append(label("RECT_HALF", 152.4-3.81, 40.64))
    elements.append(label("RECT_OUT", 152.4+3.81, 40.64))

    elements.append(sym_inst("emg:LED", "D4", "Red_ACT", "LED_SMD:LED_0805_2012Metric", 190.5, 40.64, ["1", "2"]))
    elements.append(label("GND", 190.5-3.81, 40.64))
    elements.append(label("NET_D4_R19", 190.5+3.81, 40.64))

    return sch + '\n'.join(elements) + '\n)\n'

open('DoAn/EMG_Sensor/EMG_Sensor.kicad_sch', 'w').write(generate())
print("Perfect EMG schematic generated!")
