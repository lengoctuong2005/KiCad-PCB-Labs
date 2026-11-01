import uuid
import subprocess

def u(): return str(uuid.uuid4())

# Toàn bộ tọa độ linh kiện và pin sẽ được đặt chuẩn trên lưới 2.54mm (100 mil)
# Grid: 2.54 mm.
# Y_world = Y_sym - Y_local.

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
			(property "Reference" "R" (at 2.54 0 90) (effects (font (size 1.27 1.27))))
			(property "Value" "R" (at -2.54 0 90) (effects (font (size 1.27 1.27))))
			(property "Footprint" "" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(symbol "R_0_1"
				(rectangle (start -1.27 2.54) (end 1.27 -2.54) (stroke (width 0.254) (type default)) (fill (type none)))
			)
			(symbol "R_1_1"
				(pin passive line (at 0 5.08 270) (length 2.54) (name "~" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 0 -5.08 90) (length 2.54) (name "~" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
			)
		)
		(symbol "Device:C"
			(pin_numbers (hide yes)) (pin_names (offset 0.254)) (exclude_from_sim no) (in_bom yes) (on_board yes)
			(property "Reference" "C" (at 2.54 1.27 0) (effects (font (size 1.27 1.27)) (justify left)))
			(property "Value" "C" (at 2.54 -1.27 0) (effects (font (size 1.27 1.27)) (justify left)))
			(property "Footprint" "" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(symbol "C_0_1"
				(polyline (pts (xy -2.54 0.762) (xy 2.54 0.762)) (stroke (width 0.508) (type default)) (fill (type none)))
				(polyline (pts (xy -2.54 -0.762) (xy 2.54 -0.762)) (stroke (width 0.508) (type default)) (fill (type none)))
			)
			(symbol "C_1_1"
				(pin passive line (at 0 5.08 270) (length 4.318) (name "~" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 0 -5.08 90) (length 4.318) (name "~" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
			)
		)
		(symbol "Device:LED"
			(pin_numbers (hide yes)) (pin_names (hide yes) (offset 1.016)) (exclude_from_sim no) (in_bom yes) (on_board yes)
			(property "Reference" "D" (at 2.54 2.54 0) (effects (font (size 1.27 1.27)) (justify left)))
			(property "Value" "LED" (at 2.54 -2.54 0) (effects (font (size 1.27 1.27)) (justify left)))
			(property "Footprint" "" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(symbol "LED_0_1"
				(polyline (pts (xy -1.27 -1.27) (xy -1.27 1.27)) (stroke (width 0.254) (type default)) (fill (type none)))
				(polyline (pts (xy 1.27 -1.27) (xy 1.27 1.27) (xy -1.27 0) (xy 1.27 -1.27)) (stroke (width 0.254) (type default)) (fill (type none)))
			)
			(symbol "LED_1_1"
				(pin passive line (at 0 -5.08 90) (length 3.81) (name "K" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 0 5.08 270) (length 3.81) (name "A" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
			)
		)
		(symbol "Connector_Generic:Conn_01x02"
			(pin_names (offset 1.016) (hide yes)) (exclude_from_sim no) (in_bom yes) (on_board yes)
			(property "Reference" "J" (at 0 5.08 0) (effects (font (size 1.27 1.27))))
			(property "Value" "Conn_01x02" (at 0 -7.62 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(symbol "Conn_01x02_0_1"
				(rectangle (start -2.54 2.54) (end 2.54 -5.08) (stroke (width 0.254) (type default)) (fill (type background)))
			)
			(symbol "Conn_01x02_1_1"
				(pin passive line (at 5.08 0 180) (length 2.54) (name "Pin_1" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 5.08 -2.54 180) (length 2.54) (name "Pin_2" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
			)
		)
		(symbol "charger:TP4056"
			(pin_names (offset 1.016)) (exclude_from_sim no) (in_bom yes) (on_board yes)
			(property "Reference" "U" (at -5.08 12.7 0) (effects (font (size 1.27 1.27)) (justify left)))
			(property "Value" "TP4056" (at -5.08 10.16 0) (effects (font (size 1.27 1.27)) (justify left)))
			(property "Footprint" "" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(symbol "TP4056_0_1"
				(rectangle (start -7.62 7.62) (end 7.62 -10.16) (stroke (width 0.254) (type default)) (fill (type background)))
			)
			(symbol "TP4056_1_1"
				(pin passive line (at -10.16 5.08 0) (length 2.54) (name "TEMP" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
				(pin passive line (at -10.16 2.54 0) (length 2.54) (name "PROG" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
				(pin passive line (at -10.16 0 0) (length 2.54) (name "GND" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
				(pin passive line (at -10.16 -2.54 0) (length 2.54) (name "VCC" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.27 1.27)))))
				(pin passive line (at -10.16 -5.08 0) (length 2.54) (name "CE" (effects (font (size 1.27 1.27)))) (number "8" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 10.16 5.08 180) (length 2.54) (name "BAT" (effects (font (size 1.27 1.27)))) (number "5" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 10.16 2.54 180) (length 2.54) (name "~{{STDBY}}" (effects (font (size 1.27 1.27)))) (number "6" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 10.16 0 180) (length 2.54) (name "~{{CHRG}}" (effects (font (size 1.27 1.27)))) (number "7" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 10.16 -5.08 180) (length 2.54) (name "EP" (effects (font (size 1.27 1.27)))) (number "9" (effects (font (size 1.27 1.27)))))
			)
		)
		(symbol "charger:DW01A"
			(pin_names (offset 1.016)) (exclude_from_sim no) (in_bom yes) (on_board yes)
			(property "Reference" "U" (at -5.08 7.62 0) (effects (font (size 1.27 1.27)) (justify left)))
			(property "Value" "DW01A" (at -5.08 5.08 0) (effects (font (size 1.27 1.27)) (justify left)))
			(property "Footprint" "" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(symbol "DW01A_0_1"
				(rectangle (start -7.62 5.08) (end 7.62 -5.08) (stroke (width 0.254) (type default)) (fill (type background)))
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
			(property "Reference" "Q" (at -5.08 10.16 0) (effects (font (size 1.27 1.27)) (justify left)))
			(property "Value" "FS8205A" (at -5.08 7.62 0) (effects (font (size 1.27 1.27)) (justify left)))
			(property "Footprint" "" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(symbol "FS8205A_0_1"
				(rectangle (start -7.62 7.62) (end 7.62 -7.62) (stroke (width 0.254) (type default)) (fill (type background)))
			)
			(symbol "FS8205A_1_1"
				(pin passive line (at -10.16 5.08 0) (length 2.54) (name "D12" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
				(pin passive line (at -10.16 2.54 0) (length 2.54) (name "D12" (effects (font (size 1.27 1.27)))) (number "6" (effects (font (size 1.27 1.27)))))
				(pin passive line (at -10.16 0 0) (length 2.54) (name "G1" (effects (font (size 1.27 1.27)))) (number "5" (effects (font (size 1.27 1.27)))))
				(pin passive line (at -10.16 -2.54 0) (length 2.54) (name "G2" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 10.16 5.08 180) (length 2.54) (name "D12" (effects (font (size 1.27 1.27)))) (number "8" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 10.16 2.54 180) (length 2.54) (name "D12" (effects (font (size 1.27 1.27)))) (number "7" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 10.16 0 180) (length 2.54) (name "S2" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 10.16 -2.54 180) (length 2.54) (name "S1" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
			)
		)
		(symbol "charger:USB_C_Receptacle"
			(pin_names (offset 1.016)) (exclude_from_sim no) (in_bom yes) (on_board yes)
			(property "Reference" "J" (at -5.08 15.24 0) (effects (font (size 1.27 1.27)) (justify left)))
			(property "Value" "USB_C" (at -5.08 12.7 0) (effects (font (size 1.27 1.27)) (justify left)))
			(property "Footprint" "" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(symbol "USB_C_Receptacle_0_1"
				(rectangle (start -7.62 12.7) (end 7.62 -12.7) (stroke (width 0.254) (type default)) (fill (type background)))
			)
			(symbol "USB_C_Receptacle_1_1"
				(pin passive line (at -10.16 10.16 0) (length 2.54) (name "GND" (effects (font (size 1.27 1.27)))) (number "A1" (effects (font (size 1.27 1.27)))))
				(pin passive line (at -10.16 7.62 0) (length 2.54) (name "GND" (effects (font (size 1.27 1.27)))) (number "A12" (effects (font (size 1.27 1.27)))))
				(pin passive line (at -10.16 5.08 0) (length 2.54) (name "GND" (effects (font (size 1.27 1.27)))) (number "B1" (effects (font (size 1.27 1.27)))))
				(pin passive line (at -10.16 2.54 0) (length 2.54) (name "GND" (effects (font (size 1.27 1.27)))) (number "B12" (effects (font (size 1.27 1.27)))))
				(pin passive line (at -10.16 0 0) (length 2.54) (name "SHIELD" (effects (font (size 1.27 1.27)))) (number "S1" (effects (font (size 1.27 1.27)))))
				(pin passive line (at -10.16 -2.54 0) (length 2.54) (name "D+" (effects (font (size 1.27 1.27)))) (number "B6" (effects (font (size 1.27 1.27)))))
				(pin passive line (at -10.16 -5.08 0) (length 2.54) (name "D-" (effects (font (size 1.27 1.27)))) (number "B7" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 10.16 10.16 180) (length 2.54) (name "VBUS" (effects (font (size 1.27 1.27)))) (number "A4" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 10.16 7.62 180) (length 2.54) (name "VBUS" (effects (font (size 1.27 1.27)))) (number "A9" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 10.16 5.08 180) (length 2.54) (name "VBUS" (effects (font (size 1.27 1.27)))) (number "B4" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 10.16 2.54 180) (length 2.54) (name "VBUS" (effects (font (size 1.27 1.27)))) (number "B9" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 10.16 0 180) (length 2.54) (name "CC1" (effects (font (size 1.27 1.27)))) (number "A5" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 10.16 -2.54 180) (length 2.54) (name "CC2" (effects (font (size 1.27 1.27)))) (number "B5" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 10.16 -5.08 180) (length 2.54) (name "D+" (effects (font (size 1.27 1.27)))) (number "A6" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 10.16 -7.62 180) (length 2.54) (name "D-" (effects (font (size 1.27 1.27)))) (number "A7" (effects (font (size 1.27 1.27)))))
			)
		)
	)
"""

components_dict = {
    "J1": ("charger:USB_C_Receptacle", "USB-C", "charger:USB_C_Receptacle_HRO_TYPE-C-31-M-12", 40.64, 60.96, {
        "A1": (-10.16, 10.16, "GND"),
        "A12": (-10.16, 7.62, "GND"),
        "B1": (-10.16, 5.08, "GND"),
        "B12": (-10.16, 2.54, "GND"),
        "S1": (-10.16, 0.0, "GND"),
        "B6": (-10.16, -2.54, None),
        "B7": (-10.16, -5.08, None),
        "A4": (10.16, 10.16, "VBUS"),
        "A9": (10.16, 7.62, "VBUS"),
        "B4": (10.16, 5.08, "VBUS"),
        "B9": (10.16, 2.54, "VBUS"),
        "A5": (10.16, 0.0, "CC1"),
        "B5": (10.16, -2.54, "CC2"),
        "A6": (10.16, -5.08, None),
        "A7": (10.16, -7.62, None)
    }),
    "R1": ("Device:R", "5.1k", "Resistor_SMD:R_0805_2012Metric", 71.12, 50.8, {
        "1": (0.0, 5.08, "CC1"),
        "2": (0.0, -5.08, "GND")
    }),
    "R2": ("Device:R", "5.1k", "Resistor_SMD:R_0805_2012Metric", 86.36, 50.8, {
        "1": (0.0, 5.08, "CC2"),
        "2": (0.0, -5.08, "GND")
    }),
    "C1": ("Device:C", "10uF", "Capacitor_SMD:C_0805_2012Metric", 101.6, 50.8, {
        "1": (0.0, 5.08, "VBUS"),
        "2": (0.0, -5.08, "GND")
    }),
    "C2": ("Device:C", "100nF", "Capacitor_SMD:C_0805_2012Metric", 116.84, 50.8, {
        "1": (0.0, 5.08, "VBUS"),
        "2": (0.0, -5.08, "GND")
    }),
    "U1": ("charger:TP4056", "TP4056", "charger:SOIC-8-1EP_3.9x4.9mm_P1.27mm_EP2.29x3.0mm", 147.32, 60.96, {
        "1": (-10.16, 5.08, "GND"),
        "2": (-10.16, 2.54, "PROG"),
        "3": (-10.16, 0.0, "GND"),
        "4": (-10.16, -2.54, "VBUS"),
        "8": (-10.16, -5.08, "VBUS"),
        "5": (10.16, 5.08, "BAT_OUT"),
        "6": (10.16, 2.54, "STDBY"),
        "7": (10.16, 0.0, "CHRG"),
        "9": (10.16, -5.08, "GND")
    }),
    "R3": ("Device:R", "1.2k", "Resistor_SMD:R_0805_2012Metric", 127.0, 81.28, {
        "1": (0.0, 5.08, "PROG"),
        "2": (0.0, -5.08, "GND")
    }),
    "R4": ("Device:R", "1k", "Resistor_SMD:R_0805_2012Metric", 177.8, 45.72, {
        "1": (0.0, 5.08, "VBUS"),
        "2": (0.0, -5.08, "NET_R4_D1")
    }),
    "D1": ("Device:LED", "RED", "LED_SMD:LED_0805_2012Metric", 177.8, 60.96, {
        "2": (0.0, 5.08, "NET_R4_D1"),
        "1": (0.0, -5.08, "CHRG")
    }),
    "R5": ("Device:R", "1k", "Resistor_SMD:R_0805_2012Metric", 193.04, 45.72, {
        "1": (0.0, 5.08, "VBUS"),
        "2": (0.0, -5.08, "NET_R5_D2")
    }),
    "D2": ("Device:LED", "GREEN", "LED_SMD:LED_0805_2012Metric", 193.04, 60.96, {
        "2": (0.0, 5.08, "NET_R5_D2"),
        "1": (0.0, -5.08, "STDBY")
    }),
    "C3": ("Device:C", "10uF", "Capacitor_SMD:C_0805_2012Metric", 177.8, 81.28, {
        "1": (0.0, 5.08, "BAT_OUT"),
        "2": (0.0, -5.08, "GND")
    }),
    "R6": ("Device:R", "100", "Resistor_SMD:R_0805_2012Metric", 208.28, 45.72, {
        "1": (0.0, 5.08, "BAT_OUT"),
        "2": (0.0, -5.08, "DW_VCC")
    }),
    "C4": ("Device:C", "100nF", "Capacitor_SMD:C_0805_2012Metric", 208.28, 60.96, {
        "1": (0.0, 5.08, "DW_VCC"),
        "2": (0.0, -5.08, "GND")
    }),
    "U2": ("charger:DW01A", "DW01A", "charger:SOT-23-6", 228.6, 55.88, {
        "5": (-10.16, 2.54, "DW_VCC"),
        "2": (-10.16, 0.0, "DW_CS"),
        "6": (-10.16, -2.54, "GND"),
        "1": (10.16, 2.54, "DW_OD"),
        "3": (10.16, 0.0, "DW_OC"),
        "4": (10.16, -2.54, None)
    }),
    "R7": ("Device:R", "1k", "Resistor_SMD:R_0805_2012Metric", 228.6, 81.28, {
        "1": (0.0, 5.08, "DW_CS"),
        "2": (0.0, -5.08, "BAT_MINUS")
    }),
    "Q1": ("charger:FS8205A", "FS8205A", "charger:TSSOP-8_4.4x3mm_P0.65mm", 259.08, 55.88, {
        "1": (-10.16, 5.08, "DW_D12"),
        "6": (-10.16, 2.54, "DW_D12"),
        "5": (-10.16, 0.0, "DW_OC"),
        "4": (-10.16, -2.54, "DW_OD"),
        "8": (10.16, 5.08, "DW_D12"),
        "7": (10.16, 2.54, "DW_D12"),
        "3": (10.16, 0.0, "BAT_MINUS"),
        "2": (10.16, -2.54, "GND")
    }),
    "J2": ("Connector_Generic:Conn_01x02", "BATT", "charger:JST_PH_B2B-PH-SM4-TB", 284.48, 55.88, {
        "1": (5.08, 0.0, "BAT_OUT"),
        "2": (5.08, -2.54, "BAT_MINUS")
    })
}

body = ""
wires_labels = ""

for ref, (lib, val, fp, sx, sy, pins) in components_dict.items():
    body += f"""	(symbol (lib_id "{lib}") (at {sx} {sy} 0) (unit 1)
		(in_bom yes) (on_board yes) (dnp no) (uuid "{u()}")
		(property "Reference" "{ref}" (at {sx} {sy-6.35} 0) (effects (font (size 1.27 1.27))))
		(property "Value" "{val}" (at {sx} {sy+6.35} 0) (effects (font (size 1.27 1.27))))
		(property "Footprint" "{fp}" (at {sx} {sy} 0) (effects (font (size 1.27 1.27)) (hide yes)))
"""
    for p_num in pins:
        body += f"""		(pin "{p_num}" (uuid "{u()}"))\n"""
    body += f"""		(instances (project "USB_TypeC_TP4056_Charger" (path "/{u()}" (reference "{ref}") (unit 1))))\n\t)\n"""

    for p_num, (lx, ly, net) in pins.items():
        # EXACT World coordinate:
        wx = round(sx + lx, 2)
        wy = round(sy - ly, 2)
        if net is None:
            wires_labels += f"""\t(no_connect (at {wx} {wy}) (uuid "{u()}"))\n"""
        else:
            wires_labels += f"""\t(label "{net}" (at {wx} {wy} 0) (fields_autoplaced yes)
		(effects (font (size 1.27 1.27)) (justify left bottom)) (uuid "{u()}")
	)\n"""

full_sch = sch_text + body + wires_labels + "\t(sheet_instances (path \"/\" (page \"1\")))\n)\n"

with open("USB_TypeC_TP4056_Charger.kicad_sch", "w") as f:
    f.write(full_sch)

print("Saved clean schematic v2!")
