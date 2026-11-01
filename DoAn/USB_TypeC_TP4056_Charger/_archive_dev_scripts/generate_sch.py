import sys, uuid, math

def get_uuid(): return str(uuid.uuid4())

SCH_TEMPLATE = """(kicad_sch
	(version 20240108)
	(generator "eeschema")
	(generator_version "10.0")
	(uuid "{sch_uuid}")
	(paper "A4")
	(title_block
		(title "USB Type-C TP4056 Charger with Protection")
		(date "2026-09-01")
		(rev "1.0")
		(company "Lê Ngọc Tường - MSSV: 23207124 - 23DTV_CLC3 - HK3 2025-2026")
	)
	(lib_symbols
		(symbol "charger:TP4056"
			(pin_names (offset 1.016))
			(exclude_from_sim no) (in_bom yes) (on_board yes)
			(property "Reference" "U" (at -5.08 8.89 0) (effects (font (size 1.27 1.27)) (justify left)))
			(property "Value" "TP4056" (at -5.08 6.35 0) (effects (font (size 1.27 1.27)) (justify left)))
			(property "Footprint" "charger:SOIC-8-1EP_3.9x4.9mm_P1.27mm_EP2.29x3.0mm" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(symbol "TP4056_0_1"
				(rectangle (start -7.62 5.08) (end 7.62 -7.62) (stroke (width 0.254) (type default)) (fill (type background)))
			)
			(symbol "TP4056_1_1"
				(pin input line (at -10.16 2.54 0) (length 2.54) (name "TEMP" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
				(pin input line (at -10.16 0 0) (length 2.54) (name "PROG" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
				(pin power_in line (at 0 -10.16 90) (length 2.54) (name "GND" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
				(pin power_in line (at -10.16 -2.54 0) (length 2.54) (name "VCC" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.27 1.27)))))
				(pin power_out line (at 10.16 2.54 180) (length 2.54) (name "BAT" (effects (font (size 1.27 1.27)))) (number "5" (effects (font (size 1.27 1.27)))))
				(pin open_collector line (at 10.16 0 180) (length 2.54) (name "~{{STDBY}}" (effects (font (size 1.27 1.27)))) (number "6" (effects (font (size 1.27 1.27)))))
				(pin open_collector line (at 10.16 -2.54 180) (length 2.54) (name "~{{CHRG}}" (effects (font (size 1.27 1.27)))) (number "7" (effects (font (size 1.27 1.27)))))
				(pin input line (at -10.16 -5.08 0) (length 2.54) (name "CE" (effects (font (size 1.27 1.27)))) (number "8" (effects (font (size 1.27 1.27)))))
				(pin power_in line (at 2.54 -10.16 90) (length 2.54) (name "EP" (effects (font (size 1.27 1.27)))) (number "9" (effects (font (size 1.27 1.27)))))
			)
		)
		(symbol "charger:DW01A"
			(pin_names (offset 1.016))
			(exclude_from_sim no) (in_bom yes) (on_board yes)
			(property "Reference" "U" (at -5.08 6.35 0) (effects (font (size 1.27 1.27)) (justify left)))
			(property "Value" "DW01A" (at -5.08 3.81 0) (effects (font (size 1.27 1.27)) (justify left)))
			(property "Footprint" "charger:SOT-23-6" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(symbol "DW01A_0_1"
				(rectangle (start -7.62 3.81) (end 7.62 -6.35) (stroke (width 0.254) (type default)) (fill (type background)))
			)
			(symbol "DW01A_1_1"
				(pin open_collector line (at 10.16 1.27 180) (length 2.54) (name "OD" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
				(pin input line (at -10.16 -3.81 0) (length 2.54) (name "CS" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
				(pin open_collector line (at 10.16 -1.27 180) (length 2.54) (name "OC" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
				(pin input line (at 10.16 -3.81 180) (length 2.54) (name "TD" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.27 1.27)))))
				(pin power_in line (at 0 -8.89 90) (length 2.54) (name "VCC" (effects (font (size 1.27 1.27)))) (number "5" (effects (font (size 1.27 1.27)))))
				(pin power_in line (at 0 6.35 270) (length 2.54) (name "GND" (effects (font (size 1.27 1.27)))) (number "6" (effects (font (size 1.27 1.27)))))
			)
		)
		(symbol "charger:FS8205A"
			(pin_names (offset 1.016))
			(exclude_from_sim no) (in_bom yes) (on_board yes)
			(property "Reference" "Q" (at -5.08 7.62 0) (effects (font (size 1.27 1.27)) (justify left)))
			(property "Value" "FS8205A" (at -5.08 5.08 0) (effects (font (size 1.27 1.27)) (justify left)))
			(property "Footprint" "charger:TSSOP-8_4.4x3mm_P0.65mm" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(symbol "FS8205A_0_1"
				(rectangle (start -5.08 3.81) (end 5.08 -6.35) (stroke (width 0.254) (type default)) (fill (type background)))
			)
			(symbol "FS8205A_1_1"
				(pin passive line (at -7.62 1.27 0) (length 2.54) (name "D12" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 7.62 -3.81 180) (length 2.54) (name "S1" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 7.62 -1.27 180) (length 2.54) (name "S2" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
				(pin input line (at -7.62 -3.81 0) (length 2.54) (name "G2" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.27 1.27)))))
				(pin input line (at -7.62 -1.27 0) (length 2.54) (name "G1" (effects (font (size 1.27 1.27)))) (number "5" (effects (font (size 1.27 1.27)))))
				(pin passive line (at -7.62 1.27 0) (length 2.54) (name "D12" (effects (font (size 1.27 1.27)))) (number "6" (effects (font (size 1.27 1.27)))))
				(pin passive line (at -7.62 1.27 0) (length 2.54) (name "D12" (effects (font (size 1.27 1.27)))) (number "7" (effects (font (size 1.27 1.27)))))
				(pin passive line (at -7.62 1.27 0) (length 2.54) (name "D12" (effects (font (size 1.27 1.27)))) (number "8" (effects (font (size 1.27 1.27)))))
			)
		)
		(symbol "charger:USB_C_Receptacle"
			(pin_names (offset 1.016))
			(exclude_from_sim no) (in_bom yes) (on_board yes)
			(property "Reference" "J" (at -5.08 8.89 0) (effects (font (size 1.27 1.27)) (justify left)))
			(property "Value" "USB_C" (at -5.08 6.35 0) (effects (font (size 1.27 1.27)) (justify left)))
			(property "Footprint" "charger:USB_C_Receptacle_HRO_TYPE-C-31-M-12" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(symbol "USB_C_Receptacle_0_1"
				(rectangle (start -7.62 5.08) (end 7.62 -12.7) (stroke (width 0.254) (type default)) (fill (type background)))
			)
			(symbol "USB_C_Receptacle_1_1"
				(pin passive line (at -10.16 2.54 0) (length 2.54) (name "GND" (effects (font (size 1.27 1.27)))) (number "A1" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 10.16 2.54 180) (length 2.54) (name "VBUS" (effects (font (size 1.27 1.27)))) (number "A4" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 10.16 0 180) (length 2.54) (name "CC1" (effects (font (size 1.27 1.27)))) (number "A5" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 10.16 -2.54 180) (length 2.54) (name "D+" (effects (font (size 1.27 1.27)))) (number "A6" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 10.16 -5.08 180) (length 2.54) (name "D-" (effects (font (size 1.27 1.27)))) (number "A7" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 10.16 -7.62 180) (length 2.54) (name "VBUS" (effects (font (size 1.27 1.27)))) (number "A9" (effects (font (size 1.27 1.27)))))
				(pin passive line (at -10.16 -7.62 0) (length 2.54) (name "GND" (effects (font (size 1.27 1.27)))) (number "A12" (effects (font (size 1.27 1.27)))))
				(pin passive line (at -10.16 0 0) (length 2.54) (name "GND" (effects (font (size 1.27 1.27)))) (number "B1" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 10.16 -10.16 180) (length 2.54) (name "VBUS" (effects (font (size 1.27 1.27)))) (number "B4" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 10.16 -12.7 180) (length 2.54) (name "CC2" (effects (font (size 1.27 1.27)))) (number "B5" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 10.16 -15.24 180) (length 2.54) (name "D+" (effects (font (size 1.27 1.27)))) (number "B6" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 10.16 -17.78 180) (length 2.54) (name "D-" (effects (font (size 1.27 1.27)))) (number "B7" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 10.16 -20.32 180) (length 2.54) (name "VBUS" (effects (font (size 1.27 1.27)))) (number "B9" (effects (font (size 1.27 1.27)))))
				(pin passive line (at -10.16 -10.16 0) (length 2.54) (name "GND" (effects (font (size 1.27 1.27)))) (number "B12" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 0 -15.24 90) (length 2.54) (name "SHIELD" (effects (font (size 1.27 1.27)))) (number "S1" (effects (font (size 1.27 1.27)))))
			)
		)
		(symbol "Device:C"
			(pin_numbers (hide yes)) (pin_names (offset 0.254)) (exclude_from_sim no) (in_bom yes) (on_board yes)
			(property "Reference" "C" (at 0.635 2.54 0) (effects (font (size 1.27 1.27)) (justify left)))
			(property "Value" "C" (at 0.635 -2.54 0) (effects (font (size 1.27 1.27)) (justify left)))
			(property "Footprint" "Capacitor_SMD:C_0805_2012Metric" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(symbol "C_0_1"
				(polyline (pts (xy -2.032 0.762) (xy 2.032 0.762)) (stroke (width 0.508) (type default)) (fill (type none)))
				(polyline (pts (xy -2.032 -0.762) (xy 2.032 -0.762)) (stroke (width 0.508) (type default)) (fill (type none)))
			)
			(symbol "C_1_1"
				(pin passive line (at 0 3.81 270) (length 2.794) (name "~" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 0 -3.81 90) (length 2.794) (name "~" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
			)
		)
		(symbol "Device:R_US"
			(pin_numbers (hide yes)) (pin_names (offset 0)) (exclude_from_sim no) (in_bom yes) (on_board yes)
			(property "Reference" "R" (at 2.54 0 90) (effects (font (size 1.27 1.27))))
			(property "Value" "R_US" (at -2.54 0 90) (effects (font (size 1.27 1.27))))
			(property "Footprint" "Resistor_SMD:R_0805_2012Metric" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(symbol "R_US_0_1"
				(polyline (pts (xy -1.27 0) (xy -0.889 0.762) (xy -0.254 -0.762) (xy 0.381 0.762) (xy 1.016 -0.762) (xy 1.27 0)) (stroke (width 0) (type default)) (fill (type none)))
			)
			(symbol "R_US_1_1"
				(pin passive line (at -3.81 0 0) (length 2.54) (name "~" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 3.81 0 180) (length 2.54) (name "~" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
			)
		)
		(symbol "Device:LED"
			(pin_numbers (hide yes)) (pin_names (hide yes) (offset 1.016)) (exclude_from_sim no) (in_bom yes) (on_board yes)
			(property "Reference" "D" (at 0 2.54 0) (effects (font (size 1.27 1.27))))
			(property "Value" "LED" (at 0 -2.54 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "LED_SMD:LED_0805_2012Metric" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(symbol "LED_0_1"
				(polyline (pts (xy -3.048 -0.762) (xy -4.572 -2.286) (xy -3.81 -2.286) (xy -4.572 -2.286) (xy -4.572 -1.524)) (stroke (width 0) (type default)) (fill (type none)))
				(polyline (pts (xy -1.778 -0.762) (xy -3.302 -2.286) (xy -2.54 -2.286) (xy -3.302 -2.286) (xy -3.302 -1.524)) (stroke (width 0) (type default)) (fill (type none)))
				(polyline (pts (xy -1.27 0) (xy 1.27 0)) (stroke (width 0) (type default)) (fill (type none)))
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
			(property "Reference" "J" (at 0 2.54 0) (effects (font (size 1.27 1.27))))
			(property "Value" "Conn_01x02" (at 0 -5.08 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "charger:JST_PH_B2B-PH-SM4-TB" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(symbol "Conn_01x02_1_1"
				(rectangle (start -1.27 1.27) (end 1.27 -3.81) (stroke (width 0.254) (type default)) (fill (type background)))
				(pin passive line (at -5.08 0 0) (length 3.81) (name "Pin_1" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
				(pin passive line (at -5.08 -2.54 0) (length 3.81) (name "Pin_2" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
			)
		)
		(symbol "power:GND"
			(power) (pin_names (offset 0)) (exclude_from_sim yes) (in_bom no) (on_board yes)
			(property "Reference" "#PWR" (at 0 -6.35 0) (hide yes) (effects (font (size 1.27 1.27))))
			(property "Value" "GND" (at 0 -3.81 0) (effects (font (size 1.27 1.27))))
			(symbol "GND_0_1"
				(polyline (pts (xy 0 0) (xy 0 -1.27) (xy 1.27 -1.27) (xy 0 -2.54) (xy -1.27 -1.27) (xy 0 -1.27)) (stroke (width 0) (type default)) (fill (type none)))
			)
			(symbol "GND_1_1"
				(pin power_in line (at 0 0 270) (length 0) (name "GND" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
			)
		)
		(symbol "power:+5V"
			(power) (pin_names (offset 0)) (exclude_from_sim yes) (in_bom no) (on_board yes)
			(property "Reference" "#PWR" (at 0 3.81 0) (hide yes) (effects (font (size 1.27 1.27))))
			(property "Value" "+5V" (at 0 3.81 0) (effects (font (size 1.27 1.27))))
			(symbol "+5V_0_1"
				(polyline (pts (xy -0.762 1.27) (xy 0 2.54) (xy 0.762 1.27)) (stroke (width 0) (type default)) (fill (type none)))
				(polyline (pts (xy 0 0) (xy 0 2.54)) (stroke (width 0) (type default)) (fill (type none)))
			)
			(symbol "+5V_1_1"
				(pin power_in line (at 0 0 90) (length 0) (name "+5V" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
			)
		)
		(symbol "power:PWR_FLAG"
			(power) (pin_numbers (hide yes)) (pin_names (offset 0) (hide yes)) (exclude_from_sim yes) (in_bom no) (on_board yes)
			(property "Reference" "#FLG" (at 0 1.905 0) (hide yes) (effects (font (size 1.27 1.27))))
			(property "Value" "PWR_FLAG" (at 0 3.81 0) (effects (font (size 1.27 1.27))))
			(symbol "PWR_FLAG_0_0"
				(polyline (pts (xy 0 0) (xy 0 1.27) (xy -1.016 1.905) (xy 0 2.54) (xy 1.016 1.905) (xy 0 1.27)) (stroke (width 0) (type default)) (fill (type none)))
			)
			(symbol "PWR_FLAG_1_1"
				(pin power_out line (at 0 0 90) (length 0) (name "pwr" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
			)
		)
	)
"""

def p(name, lib, ref, val, x, y, rot=0, fp=""):
    return f"""	(symbol (lib_id "{lib}") (at {x} {y} {rot}) (unit 1)
		(in_bom yes) (on_board yes) (dnp no) (uuid "{get_uuid()}")
		(property "Reference" "{ref}" (at {x-5.08} {y-5.08} 0) (effects (font (size 1.27 1.27))))
		(property "Value" "{val}" (at {x-5.08} {y-2.54} 0) (effects (font (size 1.27 1.27))))
		(property "Footprint" "{fp}" (at {x} {y} 0) (effects (font (size 1.27 1.27)) (hide yes)))
	)"""

def w(x1, y1, x2, y2):
    return f"""	(wire (pts (xy {x1} {y1}) (xy {x2} {y2})) (stroke (width 0) (type default) (color 0 0 0 0)) (uuid "{get_uuid()}"))"""

def no_conn(x, y):
    return f"""	(no_connect (at {x} {y}) (uuid "{get_uuid()}"))"""

def pwr(val, x, y, rot=0):
    return f"""	(symbol (lib_id "power:{val}") (at {x} {y} {rot}) (unit 1)
		(in_bom no) (on_board yes) (dnp no) (uuid "{get_uuid()}")
		(property "Reference" "#PWR" (at {x} {y} 0) (effects (font (size 1.27 1.27)) (hide yes)))
		(property "Value" "{val}" (at {x} {y-2.54} 0) (effects (font (size 1.27 1.27))))
		(property "Footprint" "" (at {x} {y} 0) (effects (font (size 1.27 1.27)) (hide yes)))
	)"""

def global_label(name, x, y, rot=0, shape="input"):
    return f"""	(global_label "{name}" (shape {shape}) (at {x} {y} {rot}) (fields_autoplaced yes)
		(effects (font (size 1.27 1.27)) (justify right)) (uuid "{get_uuid()}")
	)"""


out = SCH_TEMPLATE.format(sch_uuid=get_uuid())

jx, jy = 50.8, 101.6
out += p("J1", "charger:USB_C_Receptacle", "J1", "USB_C", jx, jy, 0, "charger:USB_C_Receptacle_HRO_TYPE-C-31-M-12") + "\n"

# GND: A1(-10.16, 2.54), A12(-10.16, -7.62), B1(-10.16, 0), B12(-10.16, -10.16), S1(0, -15.24)
out += w(jx-10.16, jy-2.54, jx-15.24, jy-2.54) + "\n"
out += pwr("GND", jx-15.24, jy-2.54) + "\n"

out += w(jx-10.16, jy+7.62, jx-15.24, jy+7.62) + "\n"
out += pwr("GND", jx-15.24, jy+7.62) + "\n"

out += w(jx-10.16, jy, jx-15.24, jy) + "\n"
out += pwr("GND", jx-15.24, jy) + "\n"

out += w(jx-10.16, jy+10.16, jx-15.24, jy+10.16) + "\n"
out += pwr("GND", jx-15.24, jy+10.16) + "\n"

out += w(jx, jy+15.24, jx, jy+20.32) + "\n"
out += pwr("GND", jx, jy+20.32) + "\n"

# VBUS: A4(10.16, 2.54), A9(10.16, -7.62), B4(10.16, -10.16), B9(10.16, -20.32)
out += global_label("VBUS", jx+10.16, jy-2.54, 0) + "\n"
out += global_label("VBUS", jx+10.16, jy+7.62, 0) + "\n"
out += global_label("VBUS", jx+10.16, jy+10.16, 0) + "\n"
out += global_label("VBUS", jx+10.16, jy+20.32, 0) + "\n"

# CC1/CC2: A5(10.16, 0), B5(10.16, -12.7)
out += w(jx+10.16, jy, jx+20.32, jy) + "\n"
out += p("R1", "Device:R_US", "R1", "5.1k", jx+24.13, jy, 270, "Resistor_SMD:R_0805_2012Metric") + "\n"
out += w(jx+27.94, jy, jx+33.02, jy) + "\n"
out += pwr("GND", jx+33.02, jy) + "\n"

out += w(jx+10.16, jy+12.7, jx+20.32, jy+12.7) + "\n"
out += p("R2", "Device:R_US", "R2", "5.1k", jx+24.13, jy+12.7, 270, "Resistor_SMD:R_0805_2012Metric") + "\n"
out += w(jx+27.94, jy+12.7, jx+33.02, jy+12.7) + "\n"
out += pwr("GND", jx+33.02, jy+12.7) + "\n"

out += no_conn(jx+10.16, jy+2.54) + "\n"
out += no_conn(jx+10.16, jy+5.08) + "\n"
out += no_conn(jx+10.16, jy+15.24) + "\n"
out += no_conn(jx+10.16, jy+17.78) + "\n"

# TP4056
ux, uy = 132.08, 101.6
out += p("U1", "charger:TP4056", "U1", "TP4056", ux, uy, 0, "charger:SOIC-8-1EP_3.9x4.9mm_P1.27mm_EP2.29x3.0mm") + "\n"
out += global_label("VBUS", ux-10.16, uy+2.54, 180) + "\n"
out += global_label("VBUS", ux-10.16, uy+5.08, 180) + "\n"

out += w(ux-10.16, uy-2.54, ux-15.24, uy-2.54) + "\n"
out += pwr("GND", ux-15.24, uy-2.54) + "\n"

out += w(ux-10.16, uy, ux-15.24, uy) + "\n"
out += p("R3", "Device:R_US", "R3", "1.2k", ux-19.05, uy, 270, "Resistor_SMD:R_0805_2012Metric") + "\n"
out += w(ux-22.86, uy, ux-25.4, uy) + "\n"
out += pwr("GND", ux-25.4, uy) + "\n"

out += pwr("GND", ux, uy+10.16) + "\n"
out += pwr("GND", ux-2.54, uy+10.16) + "\n"

out += global_label("BAT_OUT", ux+10.16, uy-2.54, 0) + "\n"
out += global_label("STDBY", ux+10.16, uy, 0) + "\n"
out += global_label("CHRG", ux+10.16, uy+2.54, 0) + "\n"

# Decoupling Caps
out += global_label("VBUS", 111.76, 60.96, 180) + "\n"
out += w(111.76, 60.96, 116.84, 60.96) + "\n"
out += w(116.84, 60.96, 116.84, 66.04) + "\n"
out += p("C1", "Device:C", "C1", "10uF", 116.84, 69.85, 0, "Capacitor_SMD:C_0805_2012Metric") + "\n"
out += w(116.84, 73.66, 116.84, 76.2) + "\n"
out += pwr("GND", 116.84, 76.2) + "\n"

out += w(116.84, 60.96, 127.0, 60.96) + "\n"
out += w(127.0, 60.96, 127.0, 66.04) + "\n"
out += p("C2", "Device:C", "C2", "100nF", 127.0, 69.85, 0, "Capacitor_SMD:C_0805_2012Metric") + "\n"
out += w(127.0, 73.66, 127.0, 76.2) + "\n"
out += pwr("GND", 127.0, 76.2) + "\n"

# LEDs
out += global_label("VBUS", 152.4, 60.96, 180) + "\n"
out += w(152.4, 60.96, 157.48, 60.96) + "\n"
out += w(157.48, 60.96, 157.48, 66.04) + "\n"
out += p("R4", "Device:R_US", "R4", "1k", 157.48, 69.85, 90, "Resistor_SMD:R_0805_2012Metric") + "\n"
out += w(157.48, 73.66, 157.48, 76.2) + "\n"
out += p("D1", "Device:LED", "D1", "RED", 157.48, 80.01, 270, "LED_SMD:LED_0805_2012Metric") + "\n"
out += w(157.48, 83.82, 157.48, 86.36) + "\n"
out += global_label("CHRG", 157.48, 86.36, 270) + "\n"

out += w(157.48, 60.96, 167.64, 60.96) + "\n"
out += w(167.64, 60.96, 167.64, 66.04) + "\n"
out += p("R5", "Device:R_US", "R5", "1k", 167.64, 69.85, 90, "Resistor_SMD:R_0805_2012Metric") + "\n"
out += w(167.64, 73.66, 167.64, 76.2) + "\n"
out += p("D2", "Device:LED", "D2", "GREEN", 167.64, 80.01, 270, "LED_SMD:LED_0805_2012Metric") + "\n"
out += w(167.64, 83.82, 167.64, 86.36) + "\n"
out += global_label("STDBY", 167.64, 86.36, 270) + "\n"

# Protection Circuit
dwx, dwy = 182.88, 132.08
out += p("U2", "charger:DW01A", "U2", "DW01A", dwx, dwy, 0, "charger:SOT-23-6") + "\n"
out += global_label("DW_OD", dwx+10.16, dwy-1.27, 0) + "\n"
out += global_label("DW_OC", dwx+10.16, dwy+1.27, 0) + "\n"

out += w(dwx, dwy-8.89, dwx, dwy-15.24) + "\n"
out += p("R6", "Device:R_US", "R6", "100", dwx, dwy-19.05, 90, "Resistor_SMD:R_0805_2012Metric") + "\n"
out += w(dwx, dwy-22.86, dwx, dwy-25.4) + "\n"
out += global_label("BAT_OUT", dwx, dwy-25.4, 270) + "\n"

out += w(dwx, dwy-15.24, dwx+10.16, dwy-15.24) + "\n"
out += w(dwx+10.16, dwy-15.24, dwx+10.16, dwy-10.16) + "\n"
out += p("C4", "Device:C", "C4", "100nF", dwx+10.16, dwy-6.35, 0, "Capacitor_SMD:C_0805_2012Metric") + "\n"
out += w(dwx+10.16, dwy-2.54, dwx+10.16, dwy+10.16) + "\n"
out += pwr("GND", dwx+10.16, dwy+10.16) + "\n"

out += w(dwx, dwy+6.35, dwx, dwy+15.24) + "\n"
out += global_label("BAT_MINUS", dwx, dwy+15.24, 90) + "\n"

out += w(dwx-10.16, dwy-3.81, dwx-15.24, dwy-3.81) + "\n"
out += p("R7", "Device:R_US", "R7", "1k", dwx-19.05, dwy-3.81, 270, "Resistor_SMD:R_0805_2012Metric") + "\n"
out += w(dwx-22.86, dwy-3.81, dwx-25.4, dwy-3.81) + "\n"
out += pwr("GND", dwx-25.4, dwy-3.81) + "\n"
out += no_conn(dwx+10.16, dwy-3.81) + "\n"

fsx, fsy = 233.68, 132.08
out += p("Q1", "charger:FS8205A", "Q1", "FS8205A", fsx, fsy, 0, "charger:TSSOP-8_4.4x3mm_P0.65mm") + "\n"
out += global_label("DW_OD", fsx-7.62, fsy-3.81, 180) + "\n"
out += global_label("DW_OC", fsx-7.62, fsy-1.27, 180) + "\n"

out += w(fsx+7.62, fsy-3.81, fsx+15.24, fsy-3.81) + "\n"
out += pwr("GND", fsx+15.24, fsy-3.81) + "\n"

out += w(fsx+7.62, fsy-1.27, fsx+15.24, fsy-1.27) + "\n"
out += global_label("BAT_MINUS", fsx+15.24, fsy-1.27, 0) + "\n"
out += no_conn(fsx-7.62, fsy+1.27) + "\n"

# Battery Connector
bx, by = 264.16, 132.08
out += p("J2", "Connector_Generic:Conn_01x02", "J2", "BATT", bx, by, 0, "charger:JST_PH_B2B-PH-SM4-TB") + "\n"
out += w(bx-5.08, by, bx-15.24, by) + "\n"
out += global_label("BAT_OUT", bx-15.24, by, 180) + "\n"

out += w(bx-5.08, by+2.54, bx-15.24, by+2.54) + "\n"
out += global_label("BAT_MINUS", bx-15.24, by+2.54, 180) + "\n"

# BAT_OUT decouple
out += global_label("BAT_OUT", 182.88, 60.96, 180) + "\n"
out += w(182.88, 60.96, 187.96, 60.96) + "\n"
out += w(187.96, 60.96, 187.96, 66.04) + "\n"
out += p("C3", "Device:C", "C3", "10uF", 187.96, 69.85, 0, "Capacitor_SMD:C_0805_2012Metric") + "\n"
out += w(187.96, 73.66, 187.96, 76.2) + "\n"
out += pwr("GND", 187.96, 76.2) + "\n"

# PWR_FLAGs
out += w(121.92, 40.64, 121.92, 45.72) + "\n"
out += global_label("VBUS", 121.92, 40.64, 270) + "\n"
out += pwr("PWR_FLAG", 121.92, 45.72) + "\n"

out += w(132.08, 40.64, 132.08, 45.72) + "\n"
out += pwr("GND", 132.08, 40.64) + "\n"
out += pwr("PWR_FLAG", 132.08, 45.72) + "\n"

out += w(142.24, 40.64, 142.24, 45.72) + "\n"
out += global_label("BAT_OUT", 142.24, 40.64, 270) + "\n"
out += pwr("PWR_FLAG", 142.24, 45.72) + "\n"

out += w(152.4, 40.64, 152.4, 45.72) + "\n"
out += global_label("BAT_MINUS", 152.4, 40.64, 270) + "\n"
out += pwr("PWR_FLAG", 152.4, 45.72) + "\n"

out += ")"

with open("/mnt/Windows/HK3-25-26/KhoaHe_PCB/DoAn/USB_TypeC_TP4056_Charger/USB_TypeC_TP4056_Charger.kicad_sch", "w") as f:
    f.write(out)

print("Generated.")
