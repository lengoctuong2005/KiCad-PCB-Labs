#!/usr/bin/env python3
"""
Generate a complete, ERC-clean KiCad schematic for AFE_ECG_PPG_PTT.
"""
import uuid

def u():
    return str(uuid.uuid4())

lines = []
lines.append('(kicad_sch (version 20240108) (generator "afe_ecg_ppg_designer") (generator_version "10.0")')
lines.append(f'  (uuid "{u()}")')
lines.append('  (paper "A3")')
lines.append('  (title_block')
lines.append('    (title "AFE ECG + PPG PTT ACQUISITION SYSTEM")')
lines.append('    (date "2026-11-08")')
lines.append('    (rev "1.0")')
lines.append('    (company "HCMUTE - CLC3")')
lines.append('    (comment 1 "Author: Le Ngoc Tuong - MSSV: 23207124")')
lines.append('    (comment 2 "AD8232 + ADS1115 16-bit + MAX30102 + ESP32 DevKit")')
lines.append('  )')

# Read existing afe.kicad_sym to embed symbols or use afe library
lines.append('  (lib_symbols')
with open('libs/afe.kicad_sym') as f:
    sym_content = f.read()
# Extract inside of (kicad_symbol_lib ... )
start = sym_content.find('(symbol ')
end = sym_content.rfind(')')
lines.append(sym_content[start:end])
lines.append('  )')

# Helper functions for placing symbols, wires, labels
symbols = []
wires = []
labels = []

def add_sym(lib_id, ref, val, fp, x, y, rot=0):
    s = f'''  (symbol (lib_id "{lib_id}") (at {x:.2f} {y:.2f} {rot}) (unit 1)
    (in_bom yes) (on_board yes) (dnp no)
    (uuid "{u()}")
    (property "Reference" "{ref}" (at {x:.2f} {y-2.54:.2f} 0) (effects (font (size 1.27 1.27))))
    (property "Value" "{val}" (at {x:.2f} {y+2.54:.2f} 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "{fp}" (at {x:.2f} {y:.2f} 0) (effects (font (size 1.27 1.27)) hide))
    (property "Datasheet" "~" (at {x:.2f} {y:.2f} 0) (effects (font (size 1.27 1.27)) hide))
  )'''
    symbols.append(s)

def add_wire(x1, y1, x2, y2):
    w = f'''  (wire (pts (xy {x1:.2f} {y1:.2f}) (xy {x2:.2f} {y2:.2f}))
    (stroke (width 0) (type solid))
    (uuid "{u()}")
  )'''
    wires.append(w)

def add_label(name, x, y, rot=0, shape="input"):
    justify = "left" if rot == 0 else ("right" if rot == 180 else "center")
    l = f'''  (global_label "{name}" (shape {shape}) (at {x:.2f} {y:.2f} {rot})
    (effects (font (size 1.27 1.27)) (justify {justify}))
    (uuid "{u()}")
  )'''
    labels.append(l)

print("Helper defined.")
