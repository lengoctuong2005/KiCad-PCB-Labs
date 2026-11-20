import uuid

def uid(): return str(uuid.uuid4())

def generate():
    sch_head = f"""(kicad_sch
\t(version 20231120)
\t(generator "kicad-cli")
\t(generator_version "8.0")
\t(uuid "{uid()}")
\t(paper "A4")
\t(title_block
\t\t(title "EMG Sensor - Surface Electromyography Analog Front-End")
\t\t(date "2026-11-08")
\t\t(rev "v1.0")
\t\t(company "KhoaHe Biomedical PCB")
\t\t(comment 1 "Dual Output: Bandpassed Raw EMG & Linear Contraction Envelope")
\t\t(comment 2 "0 DRC / 0 ERC Medical Grade Design")
\t)
\t(lib_symbols
\t\t(symbol "Connector_Generic:Conn_01x02"
\t\t\t(pin_names (offset 1.016) hide)
\t\t\t(in_bom yes)
\t\t\t(on_board yes)
\t\t\t(property "Reference" "J" (at 0 2.54 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Value" "Conn_01x02" (at 0 -2.54 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
\t\t\t(symbol "Conn_01x02_1_1"
\t\t\t\t(rectangle (start -1.27 2.54) (end 1.27 -2.54) (stroke (width 0.254) (type default)) (fill (type background)))
\t\t\t\t(pin passive line (at -5.08 1.27 0) (length 3.81) (name "Pin_1" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin passive line (at -5.08 -1.27 0) (length 3.81) (name "Pin_2" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
\t\t\t)
\t\t)
\t\t(symbol "Connector_Generic:Conn_01x03"
\t\t\t(pin_names (offset 1.016) hide)
\t\t\t(in_bom yes)
\t\t\t(on_board yes)
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
\t\t(symbol "Connector_Generic:Conn_01x04"
\t\t\t(pin_names (offset 1.016) hide)
\t\t\t(in_bom yes)
\t\t\t(on_board yes)
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
\t\t(symbol "Device:C"
\t\t\t(pin_numbers hide)
\t\t\t(pin_names (offset 0.254) hide)
\t\t\t(in_bom yes)
\t\t\t(on_board yes)
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
\t\t(symbol "Device:R"
\t\t\t(pin_numbers hide)
\t\t\t(pin_names (offset 0) hide)
\t\t\t(in_bom yes)
\t\t\t(on_board yes)
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
\t\t(symbol "Device:LED"
\t\t\t(pin_numbers hide)
\t\t\t(pin_names (offset 1.016) hide)
\t\t\t(in_bom yes)
\t\t\t(on_board yes)
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
\t\t(symbol "Device:D"
\t\t\t(pin_numbers hide)
\t\t\t(pin_names (offset 1.016) hide)
\t\t\t(in_bom yes)
\t\t\t(on_board yes)
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
\t\t(symbol "Amplifier_Instrumentation:AD623"
\t\t\t(in_bom yes)
\t\t\t(on_board yes)
\t\t\t(property "Reference" "U" (at 0 11.43 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Value" "AD623" (at 0 -11.43 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
\t\t\t(symbol "AD623_0_1"
\t\t\t\t(polyline (pts (xy -8.89 10.16) (xy -8.89 -10.16) (xy 8.89 0) (xy -8.89 10.16)) (stroke (width 0.254) (type default)) (fill (type background)))
\t\t\t)
\t\t\t(symbol "AD623_1_1"
\t\t\t\t(pin passive line (at -11.43 7.62 0) (length 2.54) (name "Rg" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin input line (at -11.43 2.54 0) (length 2.54) (name "-IN" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin input line (at -11.43 -2.54 0) (length 2.54) (name "+IN" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin power_in line (at 0 -12.7 90) (length 2.54) (name "-Vs" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin input line (at 0 12.7 270) (length 2.54) (name "Ref" (effects (font (size 1.27 1.27)))) (number "5" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin output line (at 11.43 0 180) (length 2.54) (name "OUT" (effects (font (size 1.27 1.27)))) (number "6" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin power_in line (at 0 12.7 270) (length 2.54) (name "+Vs" (effects (font (size 1.27 1.27)))) (number "7" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin passive line (at -11.43 -7.62 0) (length 2.54) (name "Rg" (effects (font (size 1.27 1.27)))) (number "8" (effects (font (size 1.27 1.27)))))
\t\t\t)
\t\t)
\t\t(symbol "Amplifier_Operational:MCP6004"
\t\t\t(in_bom yes)
\t\t\t(on_board yes)
\t\t\t(property "Reference" "U" (at 0 5.08 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Value" "MCP6004" (at 0 -5.08 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
\t\t\t(symbol "MCP6004_1_1"
\t\t\t\t(polyline (pts (xy -5.08 5.08) (xy -5.08 -5.08) (xy 5.08 0) (xy -5.08 5.08)) (stroke (width 0.254) (type default)) (fill (type background)))
\t\t\t\t(pin output line (at 7.62 0 180) (length 2.54) (name "~" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin input line (at -7.62 2.54 0) (length 2.54) (name "-" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin input line (at -7.62 -2.54 0) (length 2.54) (name "+" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin power_in line (at 0 7.62 270) (length 2.54) (name "V+" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin input line (at -7.62 -2.54 0) (length 2.54) (name "+" (effects (font (size 1.27 1.27)))) (number "5" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin input line (at -7.62 2.54 0) (length 2.54) (name "-" (effects (font (size 1.27 1.27)))) (number "6" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin output line (at 7.62 0 180) (length 2.54) (name "~" (effects (font (size 1.27 1.27)))) (number "7" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin output line (at 7.62 0 180) (length 2.54) (name "~" (effects (font (size 1.27 1.27)))) (number "8" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin input line (at -7.62 2.54 0) (length 2.54) (name "-" (effects (font (size 1.27 1.27)))) (number "9" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin input line (at -7.62 -2.54 0) (length 2.54) (name "+" (effects (font (size 1.27 1.27)))) (number "10" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin power_in line (at 0 -7.62 90) (length 2.54) (name "V-" (effects (font (size 1.27 1.27)))) (number "11" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin input line (at -7.62 -2.54 0) (length 2.54) (name "+" (effects (font (size 1.27 1.27)))) (number "12" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin input line (at -7.62 2.54 0) (length 2.54) (name "-" (effects (font (size 1.27 1.27)))) (number "13" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin output line (at 7.62 0 180) (length 2.54) (name "~" (effects (font (size 1.27 1.27)))) (number "14" (effects (font (size 1.27 1.27)))))
\t\t\t)
\t\t)
\t\t(symbol "power:PWR_FLAG"
\t\t\t(power)
\t\t\t(property "Reference" "#FLG" (at 0 1.905 0) (effects (font (size 1.27 1.27)) hide))
\t\t\t(property "Value" "PWR_FLAG" (at 0 3.81 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
\t\t\t(symbol "PWR_FLAG_0_0"
\t\t\t\t(polyline (pts (xy 0 0) (xy 0 1.27) (xy -1.016 1.905) (xy 0 2.54) (xy 1.016 1.905) (xy 0 1.27)) (stroke (width 0.254) (type default)) (fill (type outline)))
\t\t\t)
\t\t\t(symbol "PWR_FLAG_0_1"
\t\t\t\t(pin power_out line (at 0 0 90) (length 0) (name "~" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
\t\t\t)
\t\t)
\t)
"""
    elements = []

    def sym_inst(lib_id, ref, val, fp, x, y, pin_dict=None):
        pins_txt = ""
        if pin_dict:
            for pnum in pin_dict:
                pins_txt += f'\t\t(pin "{pnum}" (uuid "{uid()}"))\n'
        return f"""\t(symbol (lib_id "{lib_id}") (at {x} {y} 0) (unit 1)
\t\t(in_bom yes) (on_board yes) (dnp no) (uuid "{uid()}")
\t\t(property "Reference" "{ref}" (at {x} {y-2.54} 0) (effects (font (size 1.27 1.27))))
\t\t(property "Value" "{val}" (at {x} {y+2.54} 0) (effects (font (size 1.27 1.27))))
\t\t(property "Footprint" "{fp}" (at {x} {y} 0) (effects (font (size 1.27 1.27)) hide))
{pins_txt}\t)"""

    def wire(x1, y1, x2, y2):
        return f'\t(wire (pts (xy {x1} {y1}) (xy {x2} {y2})) (stroke (width 0) (type default)) (uuid "{uid()}"))'

    def label(name, x, y):
        return f'\t(label "{name}" (at {x} {y} 0) (fields_autoplaced yes) (effects (font (size 1.27 1.27)) (justify left bottom)) (uuid "{uid()}"))'

    # 1. ICs
    elements.append(sym_inst("Amplifier_Instrumentation:AD623", "U1", "AD623ARZ", "Package_SO:SOIC-8_3.9x4.9mm_P1.27mm", 100, 100, {str(i):"" for i in range(1, 9)}))
    elements.append(wire(88.57, 92.38, 80, 92.38)); elements.append(label("RG1", 80, 92.38))
    elements.append(wire(88.57, 97.46, 80, 97.46)); elements.append(label("IN_MINUS_FILT", 80, 97.46))
    elements.append(wire(88.57, 102.54, 80, 102.54)); elements.append(label("IN_PLUS_FILT", 80, 102.54))
    elements.append(wire(100, 112.7, 100, 118)); elements.append(label("GND", 100, 118))
    elements.append(wire(100, 87.3, 100, 80)); elements.append(label("VREF", 100, 80))
    elements.append(wire(111.43, 100, 120, 100)); elements.append(label("VOUT_IA", 120, 100))
    elements.append(wire(100, 87.3, 100, 87.3)); elements.append(label("VCC", 100, 87.3))
    elements.append(wire(88.57, 107.62, 80, 107.62)); elements.append(label("RG2", 80, 107.62))

    elements.append(sym_inst("Amplifier_Operational:MCP6004", "U2", "MCP6004-E/SL", "Package_SO:SOIC-14_3.9x8.7mm_P1.27mm", 180, 100, {str(i):"" for i in range(1, 15)}))
    # U2 pins:
    elements.append(wire(187.62, 100, 195, 100)); elements.append(label("VREF", 195, 100)) # Pin 1
    elements.append(wire(172.38, 97.46, 165, 97.46)); elements.append(label("VREF", 165, 97.46)) # Pin 2
    elements.append(wire(172.38, 102.54, 165, 102.54)); elements.append(label("VMID", 165, 102.54)) # Pin 3
    elements.append(wire(180, 92.38, 180, 85)); elements.append(label("VCC", 180, 85)) # Pin 4
    elements.append(wire(172.38, 102.54, 165, 102.54)); elements.append(label("LPF_IN", 165, 102.54)) # Pin 5
    elements.append(wire(172.38, 97.46, 165, 97.46)); elements.append(label("LPF_FB", 165, 97.46)) # Pin 6
    elements.append(wire(187.62, 100, 195, 100)); elements.append(label("RAW_EMG", 195, 100)) # Pin 7
    elements.append(wire(187.62, 100, 195, 100)); elements.append(label("RECT_OUT", 195, 100)) # Pin 8
    elements.append(wire(172.38, 97.46, 165, 97.46)); elements.append(label("RECT_IN", 165, 97.46)) # Pin 9
    elements.append(wire(172.38, 102.54, 165, 102.54)); elements.append(label("VREF", 165, 102.54)) # Pin 10
    elements.append(wire(180, 107.62, 180, 115)); elements.append(label("GND", 180, 115)) # Pin 11
    elements.append(wire(172.38, 102.54, 165, 102.54)); elements.append(label("VREF", 165, 102.54)) # Pin 12
    elements.append(wire(172.38, 97.46, 165, 97.46)); elements.append(label("ENV_IN", 165, 97.46)) # Pin 13
    elements.append(wire(187.62, 100, 195, 100)); elements.append(label("ENV_EMG", 195, 100)) # Pin 14

    # 2. Connectors
    elements.append(sym_inst("Connector_Generic:Conn_01x02", "J1", "Power_In", "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical", 30, 40, {"1":"","2":""}))
    elements.append(wire(24.92, 38.73, 15, 38.73)); elements.append(label("VCC", 15, 38.73))
    elements.append(wire(24.92, 41.27, 15, 41.27)); elements.append(label("GND", 15, 41.27))

    elements.append(sym_inst("Connector_Generic:Conn_01x03", "J2", "Electrodes_In", "Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical", 30, 80, {"1":"","2":"","3":""}))
    elements.append(wire(24.92, 77.46, 15, 77.46)); elements.append(label("IN_PLUS_RAW", 15, 77.46))
    elements.append(wire(24.92, 80.00, 15, 80.00)); elements.append(label("IN_MINUS_RAW", 15, 80.00))
    elements.append(wire(24.92, 82.54, 15, 82.54)); elements.append(label("VREF", 15, 82.54))

    elements.append(sym_inst("Connector_Generic:Conn_01x04", "J3", "EMG_Out", "Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical", 250, 80, {"1":"","2":"","3":"","4":""}))
    elements.append(wire(244.92, 76.19, 235, 76.19)); elements.append(label("VCC", 235, 76.19))
    elements.append(wire(244.92, 78.73, 235, 78.73)); elements.append(label("GND", 235, 78.73))
    elements.append(wire(244.92, 81.27, 235, 81.27)); elements.append(label("RAW_EMG", 235, 81.27))
    elements.append(wire(244.92, 83.81, 235, 83.81)); elements.append(label("ENV_EMG", 235, 83.81))

    # Power Flags
    elements.append(sym_inst("power:PWR_FLAG", "#FLG01", "PWR_FLAG", "", 15, 38.73, {"1":""}))
    elements.append(sym_inst("power:PWR_FLAG", "#FLG02", "PWR_FLAG", "", 15, 41.27, {"1":""}))

    # 3. Resistors R1..R19
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
    ry = 130
    for i, (ref, val, n1, n2) in enumerate(res_info):
        rx = 30 + (i % 7) * 25
        if i % 7 == 0 and i > 0: ry += 25
        elements.append(sym_inst("Device:R", ref, val, "Resistor_SMD:R_0603_1608Metric", rx, ry, {"1":"","2":""}))
        elements.append(wire(rx, ry-3.81, rx, ry-6)); elements.append(label(n1, rx, ry-6))
        elements.append(wire(rx, ry+3.81, rx, ry+6)); elements.append(label(n2, rx, ry+6))

    # 4. Capacitors C1..C13
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
    cy = 210
    for i, (ref, val, n1, n2, fp) in enumerate(cap_info):
        cx = 30 + (i % 7) * 25
        if i % 7 == 0 and i > 0: cy += 25
        elements.append(sym_inst("Device:C", ref, val, fp, cx, cy, {"1":"","2":""}))
        elements.append(wire(cx, cy-3.81, cx, cy-6)); elements.append(label(n1, cx, cy-6))
        elements.append(wire(cx, cy+3.81, cx, cy+6)); elements.append(label(n2, cx, cy+6))

    # 5. Diodes D1..D4
    elements.append(sym_inst("Device:LED", "D1", "Green_PWR", "LED_SMD:LED_0805_2012Metric", 70, 40, {"1":"","2":""}))
    elements.append(wire(70-3.81, 40, 60, 40)); elements.append(label("NET_D1_R1", 60, 40))
    elements.append(wire(70+3.81, 40, 80, 40)); elements.append(label("VCC", 80, 40))

    elements.append(sym_inst("Device:D", "D2", "1N4148W", "Diode_SMD:D_SOD-123", 110, 40, {"1":"","2":""}))
    elements.append(wire(110-3.81, 40, 100, 40)); elements.append(label("RECT_OUT", 100, 40))
    elements.append(wire(110+3.81, 40, 120, 40)); elements.append(label("RECT_IN", 120, 40))

    elements.append(sym_inst("Device:D", "D3", "1N4148W", "Diode_SMD:D_SOD-123", 150, 40, {"1":"","2":""}))
    elements.append(wire(150-3.81, 40, 140, 40)); elements.append(label("RECT_HALF", 140, 40))
    elements.append(wire(150+3.81, 40, 160, 40)); elements.append(label("RECT_OUT", 160, 40))

    elements.append(sym_inst("Device:LED", "D4", "Red_ACT", "LED_SMD:LED_0805_2012Metric", 190, 40, {"1":"","2":""}))
    elements.append(wire(190-3.81, 40, 180, 40)); elements.append(label("GND", 180, 40))
    elements.append(wire(190+3.81, 40, 200, 40)); elements.append(label("NET_D4_R19", 200, 40))

    return sch_head + "\n".join(elements) + "\n)\n"

open('DoAn/EMG_Sensor/EMG_Sensor.kicad_sch', 'w').write(generate())
print("Updated full EMG schematic!")
