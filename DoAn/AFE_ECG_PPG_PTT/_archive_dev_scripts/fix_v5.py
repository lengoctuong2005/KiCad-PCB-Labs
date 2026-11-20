import uuid, json, re
from pathlib import Path
from datetime import datetime

ROOT = Path("DoAn/AFE_ECG_PPG_PTT")
HW = ROOT/"hardware"
LIB = ROOT/"libs"
for d in [HW, LIB, ROOT/"docs", ROOT/"output/gerber"]:
    d.mkdir(parents=True, exist_ok=True)

def U(): return str(uuid.uuid4())
DATE = datetime.now().strftime("%Y-%m-%d")

lib_src = (LIB/"afe.kicad_sym").read_text()

def extract_symbols(src):
    blocks = []
    i = 0
    marker = '(symbol "afe:'
    while True:
        start = src.find(marker, i)
        if start < 0: break
        depth = 0
        j = start
        while j < len(src):
            if src[j] == '(': depth += 1
            elif src[j] == ')':
                depth -= 1
                if depth == 0:
                    blocks.append(src[start:j+1])
                    i = j+1
                    break
            j += 1
        else:
            break
    return blocks

blocks = extract_symbols(lib_src)
std = r'''  (symbol "Device:R" (pin_numbers hide) (pin_names (offset 0)) (in_bom yes) (on_board yes)
    (property "Reference" "R" (at 2.032 0 90) (effects (font (size 1.27 1.27))))
    (property "Value" "R" (at 0 0 90) (effects (font (size 1.27 1.27))))
    (property "Footprint" "" (at -1.778 0 90) (effects (font (size 1.27 1.27)) hide))
    (property "Datasheet" "~" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
    (symbol "R_0_1" (rectangle (start -1.016 -2.54) (end 1.016 2.54) (stroke (width 0.254) (type default)) (fill (type none))))
    (symbol "R_1_1" (pin passive line (at 0 3.81 270) (length 1.27) (name "~" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27))))) (pin passive line (at 0 -3.81 90) (length 1.27) (name "~" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))))
  (symbol "Device:C" (pin_numbers hide) (pin_names (offset 0.254)) (in_bom yes) (on_board yes)
    (property "Reference" "C" (at 0.635 2.54 0) (effects (font (size 1.27 1.27))))
    (property "Value" "C" (at 0.635 -2.54 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "" (at 0.9652 -3.81 0) (effects (font (size 1.27 1.27)) hide))
    (property "Datasheet" "~" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
    (symbol "C_0_1" (polyline (pts (xy -2.032 -0.762) (xy 2.032 -0.762)) (stroke (width 0.508) (type default)) (fill (type none))) (polyline (pts (xy -2.032 0.762) (xy 2.032 0.762)) (stroke (width 0.508) (type default)) (fill (type none))))
    (symbol "C_1_1" (pin passive line (at 0 3.81 270) (length 2.794) (name "~" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27))))) (pin passive line (at 0 -3.81 90) (length 2.794) (name "~" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))))
  (symbol "power:GND" (power) (pin_names (offset 0)) (in_bom no) (on_board yes)
    (property "Reference" "#PWR" (at 0 -6.35 0) (effects (font (size 1.27 1.27)) hide))
    (property "Value" "GND" (at 0 -3.81 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
    (property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
    (symbol "GND_0_1" (polyline (pts (xy 0 0) (xy 0 -1.27) (xy 1.27 -1.27) (xy 0 -2.54) (xy -1.27 -1.27) (xy 0 -1.27)) (stroke (width 0) (type default)) (fill (type none))))
    (symbol "GND_1_1" (pin power_in line (at 0 0 270) (length 0) (name "GND" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))))
  (symbol "power:+3V3" (power) (pin_names (offset 0)) (in_bom no) (on_board yes)
    (property "Reference" "#PWR" (at 0 -3.81 0) (effects (font (size 1.27 1.27)) hide))
    (property "Value" "+3V3" (at 0 3.556 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
    (property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
    (symbol "+3V3_0_1" (polyline (pts (xy -0.762 1.27) (xy 0 2.54)) (stroke (width 0) (type default)) (fill (type none))) (polyline (pts (xy 0 0) (xy 0 2.54)) (stroke (width 0) (type default)) (fill (type none))) (polyline (pts (xy 0 2.54) (xy 0.762 1.27)) (stroke (width 0) (type default)) (fill (type none))))
    (symbol "+3V3_1_1" (pin power_in line (at 0 0 90) (length 0) (name "+3V3" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))))
  (symbol "power:PWR_FLAG" (power) (pin_names (offset 0)) (in_bom no) (on_board yes)
    (property "Reference" "#FLG" (at 0 1.905 0) (effects (font (size 1.27 1.27)) hide))
    (property "Value" "PWR_FLAG" (at 0 3.81 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
    (property "Datasheet" "~" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
    (symbol "PWR_FLAG_0_0" (pin power_out line (at 0 0 90) (length 0) (name "pwr" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27))))))
    (symbol "PWR_FLAG_0_1" (polyline (pts (xy 0 0) (xy 0 1.27) (xy -1.016 1.905) (xy 0 2.54) (xy 1.016 1.905) (xy 0 1.27)) (stroke (width 0) (type default)) (fill (type none)))))'''

fixed_blocks = []
for b in blocks:
    b = re.sub(r'\(name "([^"]+)"\)(?! \(effects)', r'(name "\1" (effects (font (size 1.27 1.27))))', b)
    b = re.sub(r'\(number "([^"]+)"\)(?! \(effects)', r'(number "\1" (effects (font (size 1.27 1.27))))', b)
    fixed_blocks.append('  ' + b)

S = [f'(kicad_sch (version 20231120) (generator "dsh_afe_v5") (generator_version "5.0")',
     f'  (uuid {U()})', '  (paper "A3")',
     f'  (title_block (title "AFE ECG + PPG PTT") (date "{DATE}") (rev "E") (company "DoAn KhoaHe PCB") (comment 1 "Verify AD8232 Fig.66 values; measure ESP32/MAX30102 before fab") (comment 2 "Battery/power bank only when electrodes attached"))',
     '  (lib_symbols', std] + fixed_blocks + ['  )']

def place(lib, ref, val, x, y, fp=''):
    uid = U()
    S.append(f'  (symbol (lib_id "{lib}") (at {x} {y} 0) (unit 1) (in_bom yes) (on_board yes) (dnp no) (uuid {uid})')
    S.append(f'    (property "Reference" "{ref}" (at {x+2} {y-2} 0) (effects (font (size 1.27 1.27))))')
    S.append(f'    (property "Value" "{val}" (at {x+2} {y+2} 0) (effects (font (size 1.27 1.27))))')
    S.append(f'    (property "Footprint" "{fp}" (at {x} {y} 0) (effects (font (size 1.27 1.27)) hide))')
    S.append(f'    (property "Datasheet" "~" (at {x} {y} 0) (effects (font (size 1.27 1.27)) hide))')
    S.append(f'    (instances (project "AFE_ECG_PPG_PTT" (path "/00000000-0000-0000-0000-000000000000" (reference "{ref}") (unit 1))))))')

def label(name, x, y, shape='input'):
    S.append(f'  (global_label "{name}" (shape {shape}) (at {x} {y} 0) (fields_autoplaced yes) (effects (font (size 1.27 1.27)) (justify left)) (uuid {U()}) (property "Intersheetrefs" "${{INTERSHEET_REFS}}" (at {x} {y} 0) (effects (font (size 1.27 1.27)) hide)))')

place('afe:AD8232','U1','AD8232ACPZ',120,100,'Package_CSP:LFCSP-20-1EP_4x4mm_P0.5mm_EP2.6x2.6mm')
place('afe:ADS1115','U2','ADS1115IDGST',220,100,'Package_SO:TSSOP-10_3x3mm_P0.5mm')
place('afe:MCP1700_3V0','U3','MCP1700_3V0',80,40,'Package_TO_SOT_SMD:SOT-23')
place('afe:ESP32_DEVKIT_38P','J2','ESP32_38P_MEASURE',330,120,'Connector_PinSocket_2.54mm:PinSocket_2x19_P2.54mm_Vertical')
place('afe:MAX30102_MODULE','J3','MAX30102_VERIFY',330,45,'Connector_PinSocket_2.54mm:PinSocket_1x07_P2.54mm_Vertical')
place('afe:ECG_ELECTRODE','J1','ECG_RA_LA_RL',35,100,'Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical')

passives = [('R1','180k','Resistor_SMD:R_0603_1608Metric'),('R2','180k','Resistor_SMD:R_0603_1608Metric'),
('R3','10M','Resistor_SMD:R_0603_1608Metric'),('R4','10M','Resistor_SMD:R_0603_1608Metric'),
('R5','360k','Resistor_SMD:R_0603_1608Metric'),('R6','10M','Resistor_SMD:R_0603_1608Metric'),
('R7','10M','Resistor_SMD:R_0603_1608Metric'),('R11','82k','Resistor_SMD:R_0603_1608Metric'),
('R12','82k','Resistor_SMD:R_0603_1608Metric'),('R13','1M','Resistor_SMD:R_0603_1608Metric'),
('R14','100k','Resistor_SMD:R_0603_1608Metric'),('R15','1k','Resistor_SMD:R_0603_1608Metric'),
('R16','1k','Resistor_SMD:R_0603_1608Metric'),('R17','4.7k','Resistor_SMD:R_0603_1608Metric'),
('R18','4.7k','Resistor_SMD:R_0603_1608Metric'),
('C1','0.33uF','Capacitor_SMD:C_0603_1608Metric'),('C2','0.33uF','Capacitor_SMD:C_0603_1608Metric'),
('C3','1nF','Capacitor_SMD:C_0603_1608Metric'),('C4','0.1uF','Capacitor_SMD:C_0603_1608Metric'),
('C7','100nF','Capacitor_SMD:C_0603_1608Metric'),('C8','22nF','Capacitor_SMD:C_0603_1608Metric'),
('C9','0.1uF','Capacitor_SMD:C_0603_1608Metric'),('C10','1uF','Capacitor_SMD:C_0603_1608Metric'),
('C11','0.1uF','Capacitor_SMD:C_0603_1608Metric'),('C12','1uF','Capacitor_SMD:C_0603_1608Metric'),
('C13','1uF','Capacitor_SMD:C_0603_1608Metric'),('C14','10nF','Capacitor_SMD:C_0603_1608Metric'),
('C15','10nF','Capacitor_SMD:C_0603_1608Metric')]
for i,(ref,val,fp) in enumerate(passives):
    x = 50 + (i%10)*14; y = 160 + (i//10)*12
    place('Device:R' if ref.startswith('R') else 'Device:C', ref, val, x, y, fp)

nets = [('+3V3','power_out'),('AVDD','power_out'),('GND','input'),('ECG_IN_P','passive'),('ECG_IN_N','passive'),
        ('ECG_RL','output'),('OUT_ECG','output'),('REFOUT','output'),('I2C_SDA','bidirectional'),('I2C_SCL','bidirectional'),
        ('ADS_ALERT_IO27','output'),('MAX30102_INT','output'),('LOD_POS_IO32','output'),('LOD_NEG_IO33','output'),
        ('FR_GPIO25','input'),('OUT_BACKUP_IO34','output'),('AIN2_NC','passive'),('AIN3_NC','passive')]
for i,(n,sh) in enumerate(nets):
    x = 20 + (i%6)*65; y = 215 + (i//6)*8
    label(n, x, y, sh)

S.append('  (sheet_instances (path "/" (page "1")))')
S.append(')')
(HW/"AFE_ECG_PPG_PTT.kicad_sch").write_text("\n".join(S), encoding="utf-8")
print('blocks', len(blocks), 'lines', len(S))
