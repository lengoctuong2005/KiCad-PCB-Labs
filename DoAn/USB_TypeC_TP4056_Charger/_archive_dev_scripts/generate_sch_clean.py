import uuid

def uid(): return str(uuid.uuid4())

# Symbol definitions
# Standard KiCad 8 / 10 s-expression schematic format
sch = f"""(kicad_sch
	(version 20240108)
	(generator "eeschema")
	(generator_version "10.0")
	(uuid "{uid()}")
	(paper "A4")
	(title_block
		(title "USB Type-C TP4056 Li-ion Charger with Battery Protection")
		(date "2026-09-08")
		(rev "2.0")
		(company "Lê Ngọc Tường - MSSV: 23207124 - 23DTV_CLC3 - HK3 2025-2026")
	)
	(lib_symbols
		(symbol "charger:TP4056"
			(pin_names (offset 1.016))
			(exclude_from_sim no) (in_bom yes) (on_board yes)
			(property "Reference" "U" (at -5.08 10.16 0) (effects (font (size 1.27 1.27)) (justify left)))
			(property "Value" "TP4056" (at -5.08 7.62 0) (effects (font (size 1.27 1.27)) (justify left)))
			(property "Footprint" "charger:SOIC-8-1EP_3.9x4.9mm_P1.27mm_EP2.29x3.0mm" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(symbol "TP4056_0_1"
				(rectangle (start -7.62 6.35) (end 7.62 -8.89) (stroke (width 0.254) (type default)) (fill (type background)))
			)
			(symbol "TP4056_1_1"
				(pin input line (at -10.16 3.81 0) (length 2.54) (name "TEMP" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
				(pin input line (at -10.16 1.27 0) (length 2.54) (name "PROG" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
				(pin power_in line (at 0 -11.43 90) (length 2.54) (name "GND" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
				(pin power_in line (at -10.16 -1.27 0) (length 2.54) (name "VCC" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.27 1.27)))))
				(pin power_out line (at 10.16 3.81 180) (length 2.54) (name "BAT" (effects (font (size 1.27 1.27)))) (number "5" (effects (font (size 1.27 1.27)))))
				(pin open_collector line (at 10.16 1.27 180) (length 2.54) (name "~{{STDBY}}" (effects (font (size 1.27 1.27)))) (number "6" (effects (font (size 1.27 1.27)))))
				(pin open_collector line (at 10.16 -1.27 180) (length 2.54) (name "~{{CHRG}}" (effects (font (size 1.27 1.27)))) (number "7" (effects (font (size 1.27 1.27)))))
				(pin input line (at -10.16 -3.81 0) (length 2.54) (name "CE" (effects (font (size 1.27 1.27)))) (number "8" (effects (font (size 1.27 1.27)))))
				(pin power_in line (at 2.54 -11.43 90) (length 2.54) (name "EP" (effects (font (size 1.27 1.27)))) (number "9" (effects (font (size 1.27 1.27)))))
			)
		)
		(symbol "charger:DW01A"
			(pin_names (offset 1.016))
			(exclude_from_sim no) (in_bom yes) (on_board yes)
			(property "Reference" "U" (at -5.08 7.62 0) (effects (font (size 1.27 1.27)) (justify left)))
			(property "Value" "DW01A" (at -5.08 5.08 0) (effects (font (size 1.27 1.27)) (justify left)))
			(property "Footprint" "charger:SOT-23-6" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(symbol "DW01A_0_1"
				(rectangle (start -7.62 3.81) (end 7.62 -6.35) (stroke (width 0.254) (type default)) (fill (type background)))
			)
			(symbol "DW01A_1_1"
				(pin output line (at 10.16 1.27 180) (length 2.54) (name "OD" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
				(pin input line (at -10.16 -3.81 0) (length 2.54) (name "CS" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
				(pin output line (at 10.16 -1.27 180) (length 2.54) (name "OC" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
				(pin input line (at 10.16 -3.81 180) (length 2.54) (name "TD" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.27 1.27)))))
				(pin power_in line (at 0 6.35 270) (length 2.54) (name "VCC" (effects (font (size 1.27 1.27)))) (number "5" (effects (font (size 1.27 1.27)))))
				(pin power_in line (at 0 -8.89 90) (length 2.54) (name "GND" (effects (font (size 1.27 1.27)))) (number "6" (effects (font (size 1.27 1.27)))))
			)
		)
		(symbol "charger:FS8205A"
			(pin_names (offset 1.016))
			(exclude_from_sim no) (in_bom yes) (on_board yes)
			(property "Reference" "Q" (at -5.08 7.62 0) (effects (font (size 1.27 1.27)) (justify left)))
			(property "Value" "FS8205A" (at -5.08 5.08 0) (effects (font (size 1.27 1.27)) (justify left)))
			(property "Footprint" "charger:TSSOP-8_4.4x3mm_P0.65mm" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(symbol "FS8205A_0_1"
				(rectangle (start -6.35 6.35) (end 6.35 -6.35) (stroke (width 0.254) (type default)) (fill (type background)))
			)
			(symbol "FS8205A_1_1"
				(pin passive line (at -8.89 3.81 0) (length 2.54) (name "D12" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 8.89 -3.81 180) (length 2.54) (name "S1" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 8.89 -1.27 180) (length 2.54) (name "S2" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
				(pin input line (at -8.89 -3.81 0) (length 2.54) (name "G2" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.27 1.27)))))
				(pin input line (at -8.89 -1.27 0) (length 2.54) (name "G1" (effects (font (size 1.27 1.27)))) (number "5" (effects (font (size 1.27 1.27)))))
				(pin passive line (at -8.89 1.27 0) (length 2.54) (name "D12" (effects (font (size 1.27 1.27)))) (number "6" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 8.89 1.27 180) (length 2.54) (name "D12" (effects (font (size 1.27 1.27)))) (number "7" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 8.89 3.81 180) (length 2.54) (name "D12" (effects (font (size 1.27 1.27)))) (number "8" (effects (font (size 1.27 1.27)))))
			)
		)
		(symbol "charger:USB_C_Receptacle"
			(pin_names (offset 1.016))
			(exclude_from_sim no) (in_bom yes) (on_board yes)
			(property "Reference" "J" (at -5.08 12.7 0) (effects (font (size 1.27 1.27)) (justify left)))
			(property "Value" "USB_C" (at -5.08 10.16 0) (effects (font (size 1.27 1.27)) (justify left)))
			(property "Footprint" "charger:USB_C_Receptacle_HRO_TYPE-C-31-M-12" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(symbol "USB_C_Receptacle_0_1"
				(rectangle (start -7.62 8.89) (end 7.62 -11.43) (stroke (width 0.254) (type default)) (fill (type background)))
			)
			(symbol "USB_C_Receptacle_1_1"
				(pin power_out line (at -10.16 6.35 0) (length 2.54) (name "GND" (effects (font (size 1.27 1.27)))) (number "A1" (effects (font (size 1.27 1.27)))))
				(pin power_out line (at 10.16 6.35 180) (length 2.54) (name "VBUS" (effects (font (size 1.27 1.27)))) (number "A4" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 10.16 3.81 180) (length 2.54) (name "CC1" (effects (font (size 1.27 1.27)))) (number "A5" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 10.16 1.27 180) (length 2.54) (name "D+" (effects (font (size 1.27 1.27)))) (number "A6" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 10.16 -1.27 180) (length 2.54) (name "D-" (effects (font (size 1.27 1.27)))) (number "A7" (effects (font (size 1.27 1.27)))))
				(pin power_out line (at 10.16 -3.81 180) (length 2.54) (name "VBUS" (effects (font (size 1.27 1.27)))) (number "A9" (effects (font (size 1.27 1.27)))))
				(pin power_out line (at -10.16 3.81 0) (length 2.54) (name "GND" (effects (font (size 1.27 1.27)))) (number "A12" (effects (font (size 1.27 1.27)))))
				(pin power_out line (at -10.16 1.27 0) (length 2.54) (name "GND" (effects (font (size 1.27 1.27)))) (number "B1" (effects (font (size 1.27 1.27)))))
				(pin power_out line (at 10.16 -6.35 180) (length 2.54) (name "VBUS" (effects (font (size 1.27 1.27)))) (number "B4" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 10.16 -8.89 180) (length 2.54) (name "CC2" (effects (font (size 1.27 1.27)))) (number "B5" (effects (font (size 1.27 1.27)))))
				(pin passive line (at -10.16 -1.27 0) (length 2.54) (name "D+" (effects (font (size 1.27 1.27)))) (number "B6" (effects (font (size 1.27 1.27)))))
				(pin passive line (at -10.16 -3.81 0) (length 2.54) (name "D-" (effects (font (size 1.27 1.27)))) (number "B7" (effects (font (size 1.27 1.27)))))
				(pin power_out line (at 10.16 -11.43 180) (length 2.54) (name "VBUS" (effects (font (size 1.27 1.27)))) (number "B9" (effects (font (size 1.27 1.27)))))
				(pin power_out line (at -10.16 -6.35 0) (length 2.54) (name "GND" (effects (font (size 1.27 1.27)))) (number "B12" (effects (font (size 1.27 1.27)))))
				(pin passive line (at -10.16 -8.89 0) (length 2.54) (name "SHIELD" (effects (font (size 1.27 1.27)))) (number "S1" (effects (font (size 1.27 1.27)))))
			)
		)
		(symbol "Device:C"
			(pin_numbers (hide yes)) (pin_names (offset 0.254)) (exclude_from_sim no) (in_bom yes) (on_board yes)
			(property "Reference" "C" (at 1.27 1.27 0) (effects (font (size 1.27 1.27)) (justify left)))
			(property "Value" "C" (at 1.27 -1.27 0) (effects (font (size 1.27 1.27)) (justify left)))
			(property "Footprint" "Capacitor_SMD:C_0805_2012Metric" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(symbol "C_0_1"
				(polyline (pts (xy -2.032 0.762) (xy 2.032 0.762)) (stroke (width 0.508) (type default)) (fill (type none)))
				(polyline (pts (xy -2.032 -0.762) (xy 2.032 -0.762)) (stroke (width 0.508) (type default)) (fill (type none)))
			)
			(symbol "C_1_1"
				(pin passive line (at 0 3.81 270) (length 3.048) (name "~" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 0 -3.81 90) (length 3.048) (name "~" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
			)
		)
		(symbol "Device:R"
			(pin_numbers (hide yes)) (pin_names (offset 0)) (exclude_from_sim no) (in_bom yes) (on_board yes)
			(property "Reference" "R" (at 2.032 0 90) (effects (font (size 1.27 1.27))))
			(property "Value" "R" (at -2.032 0 90) (effects (font (size 1.27 1.27))))
			(property "Footprint" "Resistor_SMD:R_0805_2012Metric" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(symbol "R_0_1"
				(rectangle (start -1.016 2.54) (end 1.016 -2.54) (stroke (width 0.254) (type default)) (fill (type none)))
			)
			(symbol "R_1_1"
				(pin passive line (at 0 3.81 270) (length 1.27) (name "~" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 0 -3.81 90) (length 1.27) (name "~" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
			)
		)
		(symbol "Device:LED"
			(pin_numbers (hide yes)) (pin_names (hide yes) (offset 1.016)) (exclude_from_sim no) (in_bom yes) (on_board yes)
			(property "Reference" "D" (at 1.27 2.54 0) (effects (font (size 1.27 1.27)) (justify left)))
			(property "Value" "LED" (at 1.27 -2.54 0) (effects (font (size 1.27 1.27)) (justify left)))
			(property "Footprint" "LED_SMD:LED_0805_2012Metric" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(symbol "LED_0_1"
				(polyline (pts (xy -1.27 -1.27) (xy -1.27 1.27)) (stroke (width 0.254) (type default)) (fill (type none)))
				(polyline (pts (xy 1.27 -1.27) (xy 1.27 1.27) (xy -1.27 0) (xy 1.27 -1.27)) (stroke (width 0.254) (type default)) (fill (type none)))
			)
			(symbol "LED_1_1"
				(pin passive line (at -3.81 0 0) (length 2.54) (name "K" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 3.81 0 180) (length 2.54) (name "A" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
			)
		)
		(symbol "Connector_Generic:Conn_01x02"
			(pin_names (offset 1.016) (hide yes)) (exclude_from_sim no) (in_bom yes) (on_board yes)
			(property "Reference" "J" (at 0 3.81 0) (effects (font (size 1.27 1.27))))
			(property "Value" "Conn_01x02" (at 0 -6.35 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "charger:JST_PH_B2B-PH-SM4-TB" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(symbol "Conn_01x02_0_1"
				(rectangle (start -1.27 2.54) (end 1.27 -5.08) (stroke (width 0.254) (type default)) (fill (type background)))
			)
			(symbol "Conn_01x02_1_1"
				(pin passive line (at -5.08 0 0) (length 3.81) (name "Pin_1" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
				(pin passive line (at -5.08 -2.54 0) (length 3.81) (name "Pin_2" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
			)
		)
		(symbol "power:GND"
			(power) (pin_names (offset 0)) (exclude_from_sim yes) (in_bom no) (on_board yes)
			(property "Reference" "#PWR" (at 0 -3.81 0) (hide yes) (effects (font (size 1.27 1.27))))
			(property "Value" "GND" (at 0 -2.54 0) (effects (font (size 1.27 1.27))))
			(symbol "GND_0_1"
				(polyline (pts (xy 0 0) (xy 0 -1.27) (xy 1.27 -1.27) (xy 0 -2.54) (xy -1.27 -1.27) (xy 0 -1.27)) (stroke (width 0) (type default)) (fill (type none)))
			)
			(symbol "GND_1_1"
				(pin power_in line (at 0 0 270) (length 0) (name "GND" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
			)
		)
	)
"""

def sym(lib_id, ref, val, x, y, rot=0, fp=""):
    return f"""	(symbol (lib_id "{lib_id}") (at {x} {y} {rot}) (unit 1)
		(in_bom yes) (on_board yes) (dnp no) (uuid "{uid()}")
		(property "Reference" "{ref}" (at {x} {y-6.35} 0) (effects (font (size 1.27 1.27))))
		(property "Value" "{val}" (at {x} {y+6.35} 0) (effects (font (size 1.27 1.27))))
		(property "Footprint" "{fp}" (at {x} {y} 0) (effects (font (size 1.27 1.27)) (hide yes)))
	)"""

def gnd(x, y):
    return f"""	(symbol (lib_id "power:GND") (at {x} {y} 0) (unit 1)
		(in_bom no) (on_board yes) (dnp no) (uuid "{uid()}")
		(property "Reference" "#PWR" (at {x} {y} 0) (effects (font (size 1.27 1.27)) (hide yes)))
		(property "Value" "GND" (at {x} {y-2.54} 0) (effects (font (size 1.27 1.27))))
		(property "Footprint" "" (at {x} {y} 0) (effects (font (size 1.27 1.27)) (hide yes)))
	)"""

def wire(x1, y1, x2, y2):
    return f"""	(wire (pts (xy {x1} {y1}) (xy {x2} {y2})) (stroke (width 0) (type default) (color 0 0 0 0)) (uuid "{uid()}"))"""

def label(text, x, y, rot=0):
    return f"""	(label "{text}" (at {x} {y} {rot}) (fields_autoplaced yes)
		(effects (font (size 1.27 1.27)) (justify left bottom)) (uuid "{uid()}")
	)"""

def nc(x, y):
    return f"""	(no_connect (at {x} {y}) (uuid "{uid()}"))"""

body = ""

# 1. USB-C Receptacle J1 at (40.64, 80.0)
jx, jy = 40.64, 80.01
body += sym("charger:USB_C_Receptacle", "J1", "USB_C", jx, jy, 0, "charger:USB_C_Receptacle_HRO_TYPE-C-31-M-12") + "\n"

# GND pins of J1: A1(-10.16, 6.35), A12(-10.16, 3.81), B1(-10.16, 1.27), B12(-10.16, -6.35), S1(-10.16, -8.89)
for dy in [6.35, 3.81, 1.27, -6.35, -8.89]:
    body += wire(jx-10.16, jy+dy, jx-15.24, jy+dy) + "\n"
    body += gnd(jx-15.24, jy+dy) + "\n"

# D+, D- unconnected: B6(-10.16, -1.27), B7(-10.16, -3.81), A6(10.16, 1.27), A7(10.16, -1.27)
body += nc(jx-10.16, jy-1.27) + "\n"
body += nc(jx-10.16, jy-3.81) + "\n"
body += nc(jx+10.16, jy+1.27) + "\n"
body += nc(jx+10.16, jy-1.27) + "\n"

# VBUS pins: A4(10.16, 6.35), A9(10.16, -3.81), B4(10.16, -6.35), B9(10.16, -11.43)
for dy in [6.35, -3.81, -6.35, -11.43]:
    body += wire(jx+10.16, jy+dy, jx+15.24, jy+dy) + "\n"
    body += label("VBUS", jx+15.24, jy+dy, 0) + "\n"

# CC1: A5(10.16, 3.81), CC2: B5(10.16, -8.89)
# R1 at (66.04, 83.82)
body += wire(jx+10.16, jy+3.81, 66.04, jy+3.81) + "\n"
body += label("CC1", 55.88, jy+3.81, 0) + "\n"
body += sym("Device:R", "R1", "5.1k", 66.04, jy+3.81+3.81, 0, "Resistor_SMD:R_0805_2012Metric") + "\n"
body += gnd(66.04, jy+3.81+7.62) + "\n"

# R2 at (66.04, 71.12)
body += wire(jx+10.16, jy-8.89, 66.04, jy-8.89) + "\n"
body += label("CC2", 55.88, jy-8.89, 0) + "\n"
body += sym("Device:R", "R2", "5.1k", 66.04, jy-8.89+3.81, 0, "Resistor_SMD:R_0805_2012Metric") + "\n"
body += gnd(66.04, jy-8.89+7.62) + "\n"

# 2. Input Decoupling C1, C2
# C1 at (83.82, 80.0)
body += label("VBUS", 83.82, 80.0-3.81, 90) + "\n"
body += sym("Device:C", "C1", "10uF", 83.82, 80.0, 0, "Capacitor_SMD:C_0805_2012Metric") + "\n"
body += gnd(83.82, 80.0+3.81) + "\n"

# C2 at (93.98, 80.0)
body += label("VBUS", 93.98, 80.0-3.81, 90) + "\n"
body += sym("Device:C", "C2", "100nF", 93.98, 80.0, 0, "Capacitor_SMD:C_0805_2012Metric") + "\n"
body += gnd(93.98, 80.0+3.81) + "\n"

# 3. TP4056 U1 at (130.0, 80.0)
ux, uy = 130.0, 80.0
body += sym("charger:TP4056", "U1", "TP4056", ux, uy, 0, "charger:SOIC-8-1EP_3.9x4.9mm_P1.27mm_EP2.29x3.0mm") + "\n"
# Pin 1 TEMP(at -10.16, 3.81): tied to GND
body += wire(ux-10.16, uy+3.81, ux-15.24, uy+3.81) + "\n"
body += gnd(ux-15.24, uy+3.81) + "\n"

# Pin 2 PROG(at -10.16, 1.27): to R3
body += wire(ux-10.16, uy+1.27, ux-20.32, uy+1.27) + "\n"
body += sym("Device:R", "R3", "1.2k", ux-20.32, uy+1.27+3.81, 0, "Resistor_SMD:R_0805_2012Metric") + "\n"
body += gnd(ux-20.32, uy+1.27+7.62) + "\n"
body += label("PROG", ux-15.24, uy+1.27, 0) + "\n"

# Pin 3 GND(at 0, -11.43), Pin 9 EP(at 2.54, -11.43)
body += gnd(ux, uy-11.43) + "\n"
body += gnd(ux+2.54, uy-11.43) + "\n"

# Pin 4 VCC(at -10.16, -1.27), Pin 8 CE(at -10.16, -3.81): to VBUS
body += wire(ux-10.16, uy-1.27, ux-15.24, uy-1.27) + "\n"
body += label("VBUS", ux-15.24, uy-1.27, 180) + "\n"
body += wire(ux-10.16, uy-3.81, ux-15.24, uy-3.81) + "\n"
body += label("VBUS", ux-15.24, uy-3.81, 180) + "\n"

# Pin 5 BAT(at 10.16, 3.81): to BAT_OUT
body += wire(ux+10.16, uy+3.81, ux+15.24, uy+3.81) + "\n"
body += label("BAT_OUT", ux+15.24, uy+3.81, 0) + "\n"

# Pin 6 ~STDBY(at 10.16, 1.27): to STDBY
body += wire(ux+10.16, uy+1.27, ux+15.24, uy+1.27) + "\n"
body += label("STDBY", ux+15.24, uy+1.27, 0) + "\n"

# Pin 7 ~CHRG(at 10.16, -1.27): to CHRG
body += wire(ux+10.16, uy-1.27, ux+15.24, uy-1.27) + "\n"
body += label("CHRG", ux+15.24, uy-1.27, 0) + "\n"

# 4. Status LEDs & Pull-ups
# D1 (RED) CHRG LED at (165.0, 65.0)
body += label("VBUS", 165.0, 65.0-7.62, 90) + "\n"
body += sym("Device:R", "R4", "1k", 165.0, 65.0-3.81, 0, "Resistor_SMD:R_0805_2012Metric") + "\n"
body += wire(165.0, 65.0, 165.0, 65.0+3.81) + "\n"
body += label("NET_R4_D1", 165.0, 65.0, 0) + "\n"
# LED D1 rotated 90 so Pin 2 (A) is at top (y=65.0+3.81) and Pin 1 (K) is at bottom
# Actually LED in lib: A is at 3.81, K is at -3.81.
# If rot=270: A is at y=-3.81 (top), K is at y=+3.81 (bottom).
body += sym("Device:LED", "D1", "RED", 165.0, 65.0+7.62, 270, "LED_SMD:LED_0805_2012Metric") + "\n"
body += wire(165.0, 65.0+11.43, 165.0, 65.0+13.97) + "\n"
body += label("CHRG", 165.0, 65.0+13.97, 270) + "\n"

# D2 (GREEN) STDBY LED at (180.0, 65.0)
body += label("VBUS", 180.0, 65.0-7.62, 90) + "\n"
body += sym("Device:R", "R5", "1k", 180.0, 65.0-3.81, 0, "Resistor_SMD:R_0805_2012Metric") + "\n"
body += wire(180.0, 65.0, 180.0, 65.0+3.81) + "\n"
body += label("NET_R5_D2", 180.0, 65.0, 0) + "\n"
body += sym("Device:LED", "D2", "GREEN", 180.0, 65.0+7.62, 270, "LED_SMD:LED_0805_2012Metric") + "\n"
body += wire(180.0, 65.0+11.43, 180.0, 65.0+13.97) + "\n"
body += label("STDBY", 180.0, 65.0+13.97, 270) + "\n"

# Output Capacitor C3 at (165.0, 95.0)
body += label("BAT_OUT", 165.0, 95.0-3.81, 90) + "\n"
body += sym("Device:C", "C3", "10uF", 165.0, 95.0, 0, "Capacitor_SMD:C_0805_2012Metric") + "\n"
body += gnd(165.0, 95.0+3.81) + "\n"

# 5. DW01A Protection IC U2 at (205.0, 95.0)
dwx, dwy = 205.0, 95.0
body += sym("charger:DW01A", "U2", "DW01A", dwx, dwy, 0, "charger:SOT-23-6") + "\n"

# Pin 5 VCC (at 0, 6.35): connected through R6 (100 ohm) to BAT_OUT, decoupled by C4
body += wire(dwx, dwy+6.35, dwx, dwy+10.16) + "\n"
body += label("DW_VCC", dwx, dwy+10.16, 0) + "\n"

# R6 & C4 network at (195.0, 115.0)
body += label("BAT_OUT", 195.0, 115.0-3.81, 90) + "\n"
body += sym("Device:R", "R6", "100", 195.0, 115.0, 0, "Resistor_SMD:R_0805_2012Metric") + "\n"
body += wire(195.0, 115.0+3.81, 195.0, 115.0+6.35) + "\n"
body += label("DW_VCC", 195.0, 115.0+6.35, 0) + "\n"

# C4
body += label("DW_VCC", 205.0, 115.0-3.81, 90) + "\n"
body += sym("Device:C", "C4", "100nF", 205.0, 115.0, 0, "Capacitor_SMD:C_0805_2012Metric") + "\n"
body += gnd(205.0, 115.0+3.81) + "\n"

# Pin 6 GND (at 0, -8.89)
body += gnd(dwx, dwy-8.89) + "\n"

# Pin 2 CS (at -10.16, -3.81): connected via R7 (1k) to BAT_MINUS
body += wire(dwx-10.16, dwy-3.81, dwx-15.24, dwy-3.81) + "\n"
body += label("DW_CS", dwx-15.24, dwy-3.81, 180) + "\n"

body += label("DW_CS", 180.0, 115.0-3.81, 90) + "\n"
body += sym("Device:R", "R7", "1k", 180.0, 115.0, 0, "Resistor_SMD:R_0805_2012Metric") + "\n"
body += wire(180.0, 115.0+3.81, 180.0, 115.0+6.35) + "\n"
body += label("BAT_MINUS", 180.0, 115.0+6.35, 0) + "\n"

# Pin 1 OD (at 10.16, 1.27)
body += wire(dwx+10.16, dwy+1.27, dwx+15.24, dwy+1.27) + "\n"
body += label("DW_OD", dwx+15.24, dwy+1.27, 0) + "\n"

# Pin 3 OC (at 10.16, -1.27)
body += wire(dwx+10.16, dwy-1.27, dwx+15.24, dwy-1.27) + "\n"
body += label("DW_OC", dwx+15.24, dwy-1.27, 0) + "\n"

# Pin 4 TD (at 10.16, -3.81)
body += nc(dwx+10.16, dwy-3.81) + "\n"

# 6. FS8205A Dual N-MOSFET Q1 at (240.0, 95.0)
qx, qy = 240.0, 95.0
body += sym("charger:FS8205A", "Q1", "FS8205A", qx, qy, 0, "charger:TSSOP-8_4.4x3mm_P0.65mm") + "\n"
# Pin 5 G1 (at -8.89, -1.27): to DW_OC
body += wire(qx-8.89, qy-1.27, qx-13.97, qy-1.27) + "\n"
body += label("DW_OC", qx-13.97, qy-1.27, 180) + "\n"

# Pin 4 G2 (at -8.89, -3.81): to DW_OD
body += wire(qx-8.89, qy-3.81, qx-13.97, qy-3.81) + "\n"
body += label("DW_OD", qx-13.97, qy-3.81, 180) + "\n"

# Pin 2 S1 (at 8.89, -3.81): to GND (Board Ground)
body += wire(qx+8.89, qy-3.81, qx+13.97, qy-3.81) + "\n"
body += gnd(qx+13.97, qy-3.81) + "\n"

# Pin 3 S2 (at 8.89, -1.27): to BAT_MINUS (Battery Negative)
body += wire(qx+8.89, qy-1.27, qx+13.97, qy-1.27) + "\n"
body += label("BAT_MINUS", qx+13.97, qy-1.27, 0) + "\n"

# Pins 1, 6, 7, 8 D12 (Common Drain node):
# Pin 1 (at -8.89, 3.81), Pin 6 (at -8.89, 1.27), Pin 7 (at 8.89, 1.27), Pin 8 (at 8.89, 3.81)
body += wire(qx-8.89, qy+3.81, qx-8.89, qy+1.27) + "\n"
body += wire(qx-8.89, qy+1.27, qx-13.97, qy+1.27) + "\n"
body += label("DW_D12", qx-13.97, qy+1.27, 180) + "\n"

body += wire(qx+8.89, qy+3.81, qx+8.89, qy+1.27) + "\n"
body += wire(qx+8.89, qy+1.27, qx+13.97, qy+1.27) + "\n"
body += label("DW_D12", qx+13.97, qy+1.27, 0) + "\n"

# 7. Battery Output Connector J2 at (270.0, 95.0)
body += sym("Connector_Generic:Conn_01x02", "J2", "BATT", 270.0, 95.0, 0, "charger:JST_PH_B2B-PH-SM4-TB") + "\n"
# Pin 1 (at -5.08, 0): to BAT_OUT
body += wire(270.0-5.08, 95.0, 270.0-10.16, 95.0) + "\n"
body += label("BAT_OUT", 270.0-10.16, 95.0, 180) + "\n"

# Pin 2 (at -5.08, -2.54): to BAT_MINUS
body += wire(270.0-5.08, 95.0-2.54, 270.0-10.16, 95.0-2.54) + "\n"
body += label("BAT_MINUS", 270.0-10.16, 95.0-2.54, 180) + "\n"

sch += body + ")\n"

with open("USB_TypeC_TP4056_Charger.kicad_sch", "w") as f:
    f.write(sch)

print("Generated clean schematic successfully!")
