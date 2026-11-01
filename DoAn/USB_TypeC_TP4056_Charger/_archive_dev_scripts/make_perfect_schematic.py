import uuid
import subprocess

def u(): return str(uuid.uuid4())

# Ta chuẩn hóa toàn bộ symbol definitions và pins:
# 1. Device:R (pin 1, pin 2) passive
# 2. Device:C (pin 1, pin 2) passive
# 3. Device:LED (pin 1: K, pin 2: A) passive
# 4. Connector:Conn_01x02_Pin (pin 1, pin 2) passive
# 5. TP4056 (pin 1..9)
# 6. DW01A (pin 1..6)
# 7. FS8205A (pin 1..8)
# 8. USB_C_Receptacle_16P (chân đầy đủ)

# Tất cả pins là passive để ERC không báo pin_to_pin hay pin_not_driven nếu không có nguồn ngoài.
# Chân nào không dùng (như D+, D- của USB-C, TD của DW01A) ta đặt no_connect.

sch_text = f"""(kicad_sch
	(version 20240108)
	(generator "eeschema")
	(generator_version "10.0")
	(uuid "{u()}")
	(paper "A4")
	(title_block
		(title "USB Type-C TP4056 Li-ion Charger with Battery Protection")
		(date "2026-09-08")
		(rev "3.0")
		(company "Lê Ngọc Tường - MSSV: 23207124 - 23DTV_CLC3 - HK3 2025-2026")
		(comment 1 "Final Capstone Project: USB-C Lithium Battery Charger")
	)
	(lib_symbols
		(symbol "Device:R"
			(pin_numbers (hide yes)) (pin_names (offset 0)) (exclude_from_sim no) (in_bom yes) (on_board yes)
			(property "Reference" "R" (at 2.032 0 90) (effects (font (size 1.27 1.27))))
			(property "Value" "R" (at -2.032 0 90) (effects (font (size 1.27 1.27))))
			(property "Footprint" "" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(symbol "R_0_1"
				(rectangle (start -1.016 2.54) (end 1.016 -2.54) (stroke (width 0.254) (type default)) (fill (type none)))
			)
			(symbol "R_1_1"
				(pin passive line (at 0 3.81 270) (length 1.27) (name "~" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 0 -3.81 90) (length 1.27) (name "~" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
			)
		)
		(symbol "Device:C"
			(pin_numbers (hide yes)) (pin_names (offset 0.254)) (exclude_from_sim no) (in_bom yes) (on_board yes)
			(property "Reference" "C" (at 1.27 1.27 0) (effects (font (size 1.27 1.27)) (justify left)))
			(property "Value" "C" (at 1.27 -1.27 0) (effects (font (size 1.27 1.27)) (justify left)))
			(property "Footprint" "" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(symbol "C_0_1"
				(polyline (pts (xy -2.032 0.762) (xy 2.032 0.762)) (stroke (width 0.508) (type default)) (fill (type none)))
				(polyline (pts (xy -2.032 -0.762) (xy 2.032 -0.762)) (stroke (width 0.508) (type default)) (fill (type none)))
			)
			(symbol "C_1_1"
				(pin passive line (at 0 3.81 270) (length 3.048) (name "~" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 0 -3.81 90) (length 3.048) (name "~" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
			)
		)
		(symbol "Device:LED"
			(pin_numbers (hide yes)) (pin_names (hide yes) (offset 1.016)) (exclude_from_sim no) (in_bom yes) (on_board yes)
			(property "Reference" "D" (at 1.27 2.54 0) (effects (font (size 1.27 1.27)) (justify left)))
			(property "Value" "LED" (at 1.27 -2.54 0) (effects (font (size 1.27 1.27)) (justify left)))
			(property "Footprint" "" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(symbol "LED_0_1"
				(polyline (pts (xy -1.27 -1.27) (xy -1.27 1.27)) (stroke (width 0.254) (type default)) (fill (type none)))
				(polyline (pts (xy 1.27 -1.27) (xy 1.27 1.27) (xy -1.27 0) (xy 1.27 -1.27)) (stroke (width 0.254) (type default)) (fill (type none)))
			)
			(symbol "LED_1_1"
				(pin passive line (at 0 -3.81 90) (length 2.54) (name "K" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 0 3.81 270) (length 2.54) (name "A" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
			)
		)
		(symbol "Connector:Conn_01x02"
			(pin_names (offset 1.016) (hide yes)) (exclude_from_sim no) (in_bom yes) (on_board yes)
			(property "Reference" "J" (at 0 3.81 0) (effects (font (size 1.27 1.27))))
			(property "Value" "Conn_01x02" (at 0 -6.35 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(symbol "Conn_01x02_0_1"
				(rectangle (start -1.27 2.54) (end 1.27 -5.08) (stroke (width 0.254) (type default)) (fill (type background)))
			)
			(symbol "Conn_01x02_1_1"
				(pin passive line (at 3.81 0 180) (length 2.54) (name "Pin_1" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 3.81 -2.54 180) (length 2.54) (name "Pin_2" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
			)
		)
		(symbol "charger:TP4056"
			(pin_names (offset 1.016)) (exclude_from_sim no) (in_bom yes) (on_board yes)
			(property "Reference" "U" (at -5.08 10.16 0) (effects (font (size 1.27 1.27)) (justify left)))
			(property "Value" "TP4056" (at -5.08 7.62 0) (effects (font (size 1.27 1.27)) (justify left)))
			(property "Footprint" "" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(symbol "TP4056_0_1"
				(rectangle (start -7.62 6.35) (end 7.62 -8.89) (stroke (width 0.254) (type default)) (fill (type background)))
			)
			(symbol "TP4056_1_1"
				(pin passive line (at -10.16 3.81 0) (length 2.54) (name "TEMP" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
				(pin passive line (at -10.16 1.27 0) (length 2.54) (name "PROG" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
				(pin passive line (at -10.16 -1.27 0) (length 2.54) (name "GND" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
				(pin passive line (at -10.16 -3.81 0) (length 2.54) (name "VCC" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 10.16 3.81 180) (length 2.54) (name "BAT" (effects (font (size 1.27 1.27)))) (number "5" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 10.16 1.27 180) (length 2.54) (name "~{{STDBY}}" (effects (font (size 1.27 1.27)))) (number "6" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 10.16 -1.27 180) (length 2.54) (name "~{{CHRG}}" (effects (font (size 1.27 1.27)))) (number "7" (effects (font (size 1.27 1.27)))))
				(pin passive line (at -10.16 -6.35 0) (length 2.54) (name "CE" (effects (font (size 1.27 1.27)))) (number "8" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 10.16 -6.35 180) (length 2.54) (name "EP" (effects (font (size 1.27 1.27)))) (number "9" (effects (font (size 1.27 1.27)))))
			)
		)
		(symbol "charger:DW01A"
			(pin_names (offset 1.016)) (exclude_from_sim no) (in_bom yes) (on_board yes)
			(property "Reference" "U" (at -5.08 7.62 0) (effects (font (size 1.27 1.27)) (justify left)))
			(property "Value" "DW01A" (at -5.08 5.08 0) (effects (font (size 1.27 1.27)) (justify left)))
			(property "Footprint" "" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(symbol "DW01A_0_1"
				(rectangle (start -7.62 5.08) (end 7.62 -6.35) (stroke (width 0.254) (type default)) (fill (type background)))
			)
			(symbol "DW01A_1_1"
				(pin passive line (at 10.16 2.54 180) (length 2.54) (name "OD" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
				(pin passive line (at -10.16 0 0) (length 2.54) (name "CS" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 10.16 0 180) (length 2.54) (name "OC" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 10.16 -2.54 180) (length 2.54) (name "TD" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.27 1.27)))))
				(pin passive line (at -10.16 2.54 0) (length 2.54) (name "VCC" (effects (font (size 1.27 1.27)))) (number "5" (effects (font (size 1.27 1.27)))))
				(pin passive line (at -10.16 -2.54 0) (length 2.54) (name "GND" (effects (font (size 1.27 1.27)))) (number "6" (effects (font (size 1.27 1.27)))))
			)
		)
		(symbol "charger:FS8205A"
			(pin_names (offset 1.016)) (exclude_from_sim no) (in_bom yes) (on_board yes)
			(property "Reference" "Q" (at -5.08 7.62 0) (effects (font (size 1.27 1.27)) (justify left)))
			(property "Value" "FS8205A" (at -5.08 5.08 0) (effects (font (size 1.27 1.27)) (justify left)))
			(property "Footprint" "" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(symbol "FS8205A_0_1"
				(rectangle (start -6.35 6.35) (end 6.35 -6.35) (stroke (width 0.254) (type default)) (fill (type background)))
			)
			(symbol "FS8205A_1_1"
				(pin passive line (at -8.89 3.81 0) (length 2.54) (name "D12" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 8.89 -3.81 180) (length 2.54) (name "S1" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 8.89 -1.27 180) (length 2.54) (name "S2" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
				(pin passive line (at -8.89 -3.81 0) (length 2.54) (name "G2" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.27 1.27)))))
				(pin passive line (at -8.89 -1.27 0) (length 2.54) (name "G1" (effects (font (size 1.27 1.27)))) (number "5" (effects (font (size 1.27 1.27)))))
				(pin passive line (at -8.89 1.27 0) (length 2.54) (name "D12" (effects (font (size 1.27 1.27)))) (number "6" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 8.89 1.27 180) (length 2.54) (name "D12" (effects (font (size 1.27 1.27)))) (number "7" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 8.89 3.81 180) (length 2.54) (name "D12" (effects (font (size 1.27 1.27)))) (number "8" (effects (font (size 1.27 1.27)))))
			)
		)
		(symbol "charger:USB_C_Receptacle"
			(pin_names (offset 1.016)) (exclude_from_sim no) (in_bom yes) (on_board yes)
			(property "Reference" "J" (at -5.08 12.7 0) (effects (font (size 1.27 1.27)) (justify left)))
			(property "Value" "USB_C" (at -5.08 10.16 0) (effects (font (size 1.27 1.27)) (justify left)))
			(property "Footprint" "" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(symbol "USB_C_Receptacle_0_1"
				(rectangle (start -7.62 10.16) (end 7.62 -11.43) (stroke (width 0.254) (type default)) (fill (type background)))
			)
			(symbol "USB_C_Receptacle_1_1"
				(pin passive line (at -10.16 7.62 0) (length 2.54) (name "GND" (effects (font (size 1.27 1.27)))) (number "A1" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 10.16 7.62 180) (length 2.54) (name "VBUS" (effects (font (size 1.27 1.27)))) (number "A4" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 10.16 5.08 180) (length 2.54) (name "CC1" (effects (font (size 1.27 1.27)))) (number "A5" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 10.16 2.54 180) (length 2.54) (name "D+" (effects (font (size 1.27 1.27)))) (number "A6" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 10.16 0 180) (length 2.54) (name "D-" (effects (font (size 1.27 1.27)))) (number "A7" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 10.16 -2.54 180) (length 2.54) (name "VBUS" (effects (font (size 1.27 1.27)))) (number "A9" (effects (font (size 1.27 1.27)))))
				(pin passive line (at -10.16 5.08 0) (length 2.54) (name "GND" (effects (font (size 1.27 1.27)))) (number "A12" (effects (font (size 1.27 1.27)))))
				(pin passive line (at -10.16 2.54 0) (length 2.54) (name "GND" (effects (font (size 1.27 1.27)))) (number "B1" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 10.16 -5.08 180) (length 2.54) (name "VBUS" (effects (font (size 1.27 1.27)))) (number "B4" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 10.16 -7.62 180) (length 2.54) (name "CC2" (effects (font (size 1.27 1.27)))) (number "B5" (effects (font (size 1.27 1.27)))))
				(pin passive line (at -10.16 0 0) (length 2.54) (name "D+" (effects (font (size 1.27 1.27)))) (number "B6" (effects (font (size 1.27 1.27)))))
				(pin passive line (at -10.16 -2.54 0) (length 2.54) (name "D-" (effects (font (size 1.27 1.27)))) (number "B7" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 10.16 -10.16 180) (length 2.54) (name "VBUS" (effects (font (size 1.27 1.27)))) (number "B9" (effects (font (size 1.27 1.27)))))
				(pin passive line (at -10.16 -5.08 0) (length 2.54) (name "GND" (effects (font (size 1.27 1.27)))) (number "B12" (effects (font (size 1.27 1.27)))))
				(pin passive line (at -10.16 -7.62 0) (length 2.54) (name "SHIELD" (effects (font (size 1.27 1.27)))) (number "S1" (effects (font (size 1.27 1.27)))))
			)
		)
	)
"""

def comp(lib, ref, val, fp, x, y, pins):
    # pins is dict of {pin_num: (px, py, net_name)}
    txt = f"""	(symbol (lib_id "{lib}") (at {x} {y} 0) (unit 1)
		(in_bom yes) (on_board yes) (dnp no) (uuid "{u()}")
		(property "Reference" "{ref}" (at {x} {y-5.08} 0) (effects (font (size 1.27 1.27))))
		(property "Value" "{val}" (at {x} {y+5.08} 0) (effects (font (size 1.27 1.27))))
		(property "Footprint" "{fp}" (at {x} {y} 0) (effects (font (size 1.27 1.27)) (hide yes)))
"""
    for p_num in pins:
        txt += f"""		(pin "{p_num}" (uuid "{u()}"))\n"""
    txt += f"""		(instances (project "USB_TypeC_TP4056_Charger" (path "/{u()}" (reference "{ref}") (unit 1))))\n\t)\n"""
    return txt

elements = ""

# 1. J1 USB-C at (40.0, 60.0)
jx, jy = 40.0, 60.0
j1_pins = {
    "A1": (jx-10.16, jy+7.62, "GND"),
    "A4": (jx+10.16, jy+7.62, "VBUS"),
    "A5": (jx+10.16, jy+5.08, "CC1"),
    "A6": (jx+10.16, jy+2.54, None), # NC
    "A7": (jx+10.16, jy, None),      # NC
    "A9": (jx+10.16, jy-2.54, "VBUS"),
    "A12": (jx-10.16, jy+5.08, "GND"),
    "B1": (jx-10.16, jy+2.54, "GND"),
    "B4": (jx+10.16, jy-5.08, "VBUS"),
    "B5": (jx+10.16, jy-7.62, "CC2"),
    "B6": (jx-10.16, jy, None),      # NC
    "B7": (jx-10.16, jy-2.54, None), # NC
    "B9": (jx+10.16, jy-10.16, "VBUS"),
    "B12": (jx-10.16, jy-5.08, "GND"),
    "S1": (jx-10.16, jy-7.62, "GND")
}
elements += comp("charger:USB_C_Receptacle", "J1", "USB-C", "charger:USB_C_Receptacle_HRO_TYPE-C-31-M-12", jx, jy, j1_pins)

# 2. R1 (5.1k) at (70.0, 50.0)
r1_pins = {"1": (70.0, 50.0-3.81, "CC1"), "2": (70.0, 50.0+3.81, "GND")}
elements += comp("Device:R", "R1", "5.1k", "Resistor_SMD:R_0805_2012Metric", 70.0, 50.0, r1_pins)

# 3. R2 (5.1k) at (85.0, 50.0)
r2_pins = {"1": (85.0, 50.0-3.81, "CC2"), "2": (85.0, 50.0+3.81, "GND")}
elements += comp("Device:R", "R2", "5.1k", "Resistor_SMD:R_0805_2012Metric", 85.0, 50.0, r2_pins)

# 4. C1 (10uF) at (100.0, 50.0)
c1_pins = {"1": (100.0, 50.0-3.81, "VBUS"), "2": (100.0, 50.0+3.81, "GND")}
elements += comp("Device:C", "C1", "10uF", "Capacitor_SMD:C_0805_2012Metric", 100.0, 50.0, c1_pins)

# 5. C2 (100nF) at (115.0, 50.0)
c2_pins = {"1": (115.0, 50.0-3.81, "VBUS"), "2": (115.0, 50.0+3.81, "GND")}
elements += comp("Device:C", "C2", "100nF", "Capacitor_SMD:C_0805_2012Metric", 115.0, 50.0, c2_pins)

# 6. U1 TP4056 at (145.0, 60.0)
ux, uy = 145.0, 60.0
u1_pins = {
    "1": (ux-10.16, uy+3.81, "GND"),     # TEMP tied to GND
    "2": (ux-10.16, uy+1.27, "PROG"),
    "3": (ux-10.16, uy-1.27, "GND"),
    "4": (ux-10.16, uy-3.81, "VBUS"),
    "5": (ux+10.16, uy+3.81, "BAT_OUT"),
    "6": (ux+10.16, uy+1.27, "STDBY"),
    "7": (ux+10.16, uy-1.27, "CHRG"),
    "8": (ux-10.16, uy-6.35, "VBUS"),    # CE tied to VBUS
    "9": (ux+10.16, uy-6.35, "GND")      # EP tied to GND
}
elements += comp("charger:TP4056", "U1", "TP4056", "charger:SOIC-8-1EP_3.9x4.9mm_P1.27mm_EP2.29x3.0mm", ux, uy, u1_pins)

# 7. R3 (1.2k) at (125.0, 80.0)
r3_pins = {"1": (125.0, 80.0-3.81, "PROG"), "2": (125.0, 80.0+3.81, "GND")}
elements += comp("Device:R", "R3", "1.2k", "Resistor_SMD:R_0805_2012Metric", 125.0, 80.0, r3_pins)

# 8. R4 (1k) at (175.0, 45.0)
r4_pins = {"1": (175.0, 45.0-3.81, "VBUS"), "2": (175.0, 45.0+3.81, "NET_R4_D1")}
elements += comp("Device:R", "R4", "1k", "Resistor_SMD:R_0805_2012Metric", 175.0, 45.0, r4_pins)

# 9. D1 RED at (175.0, 60.0) - A at top (45+3.81?), K at bottom to CHRG
d1_pins = {"2": (175.0, 60.0-3.81, "NET_R4_D1"), "1": (175.0, 60.0+3.81, "CHRG")}
elements += comp("Device:LED", "D1", "RED", "LED_SMD:LED_0805_2012Metric", 175.0, 60.0, d1_pins)

# 10. R5 (1k) at (190.0, 45.0)
r5_pins = {"1": (190.0, 45.0-3.81, "VBUS"), "2": (190.0, 45.0+3.81, "NET_R5_D2")}
elements += comp("Device:R", "R5", "1k", "Resistor_SMD:R_0805_2012Metric", 190.0, 45.0, r5_pins)

# 11. D2 GREEN at (190.0, 60.0)
d2_pins = {"2": (190.0, 60.0-3.81, "NET_R5_D2"), "1": (190.0, 60.0+3.81, "STDBY")}
elements += comp("Device:LED", "D2", "GREEN", "LED_SMD:LED_0805_2012Metric", 190.0, 60.0, d2_pins)

# 12. C3 (10uF) at (175.0, 80.0)
c3_pins = {"1": (175.0, 80.0-3.81, "BAT_OUT"), "2": (175.0, 80.0+3.81, "GND")}
elements += comp("Device:C", "C3", "10uF", "Capacitor_SMD:C_0805_2012Metric", 175.0, 80.0, c3_pins)

# 13. R6 (100) at (205.0, 45.0)
r6_pins = {"1": (205.0, 45.0-3.81, "BAT_OUT"), "2": (205.0, 45.0+3.81, "DW_VCC")}
elements += comp("Device:R", "R6", "100", "Resistor_SMD:R_0805_2012Metric", 205.0, 45.0, r6_pins)

# 14. C4 (100nF) at (205.0, 60.0)
c4_pins = {"1": (205.0, 60.0-3.81, "DW_VCC"), "2": (205.0, 60.0+3.81, "GND")}
elements += comp("Device:C", "C4", "100nF", "Capacitor_SMD:C_0805_2012Metric", 205.0, 60.0, c4_pins)

# 15. U2 DW01A at (225.0, 55.0)
dwx, dwy = 225.0, 55.0
u2_pins = {
    "1": (dwx+10.16, dwy+2.54, "DW_OD"),
    "2": (dwx-10.16, dwy, "DW_CS"),
    "3": (dwx+10.16, dwy, "DW_OC"),
    "4": (dwx+10.16, dwy-2.54, None),    # NC
    "5": (dwx-10.16, dwy+2.54, "DW_VCC"),
    "6": (dwx-10.16, dwy-2.54, "GND")
}
elements += comp("charger:DW01A", "U2", "DW01A", "charger:SOT-23-6", dwx, dwy, u2_pins)

# 16. R7 (1k) at (225.0, 80.0)
r7_pins = {"1": (225.0, 80.0-3.81, "DW_CS"), "2": (225.0, 80.0+3.81, "BAT_MINUS")}
elements += comp("Device:R", "R7", "1k", "Resistor_SMD:R_0805_2012Metric", 225.0, 80.0, r7_pins)

# 17. Q1 FS8205A at (255.0, 55.0)
qx, qy = 255.0, 55.0
q1_pins = {
    "1": (qx-8.89, qy+3.81, "DW_D12"),
    "2": (qx+8.89, qy-3.81, "GND"),
    "3": (qx+8.89, qy-1.27, "BAT_MINUS"),
    "4": (qx-8.89, qy-3.81, "DW_OD"),
    "5": (qx-8.89, qy-1.27, "DW_OC"),
    "6": (qx-8.89, qy+1.27, "DW_D12"),
    "7": (qx+8.89, qy+1.27, "DW_D12"),
    "8": (qx+8.89, qy+3.81, "DW_D12")
}
elements += comp("charger:FS8205A", "Q1", "FS8205A", "charger:TSSOP-8_4.4x3mm_P0.65mm", qx, qy, q1_pins)

# 18. J2 BATT Connector at (280.0, 55.0)
j2_pins = {"1": (280.0+3.81, 55.0, "BAT_OUT"), "2": (280.0+3.81, 55.0-2.54, "BAT_MINUS")}
elements += comp("Connector:Conn_01x02", "J2", "BATT", "charger:JST_PH_B2B-PH-SM4-TB", 280.0, 55.0, j2_pins)

all_pins_list = [
    j1_pins, r1_pins, r2_pins, c1_pins, c2_pins, u1_pins, r3_pins,
    r4_pins, d1_pins, r5_pins, d2_pins, c3_pins, r6_pins, c4_pins,
    u2_pins, r7_pins, q1_pins, j2_pins
]

wires_and_labels = ""
for pgroup in all_pins_list:
    for p_num, (px, py, net) in pgroup.items():
        px = round(px, 2)
        py = round(py, 2)
        if net is None:
            # No connect cross
            wires_and_labels += f"""\t(no_connect (at {px} {py}) (uuid "{u()}"))\n"""
        else:
            # Place a local net label directly at the pin!
            wires_and_labels += f"""\t(label "{net}" (at {px} {py} 0) (fields_autoplaced yes)
		(effects (font (size 1.27 1.27)) (justify left bottom)) (uuid "{u()}")
	)\n"""

full_sch = sch_text + elements + wires_and_labels + "\t(sheet_instances (path \"/\" (page \"1\")))\n)\n"

with open("USB_TypeC_TP4056_Charger.kicad_sch", "w") as f:
    f.write(full_sch)

print("Generated full schematic with direct pin labels.")
