import csv

bom_rows = [
    ["Comment", "Designator", "Footprint", "LCSC Part Number", "Value", "Description", "Quantity"],
    # ICs
    ["AD8232ACPZ-R7", "U1", "Package_CSP:LFCSP-20-1EP_4x4mm_P0.5mm_EP2.5x2.5mm", "C95796", "AD8232ACPZ", "Single-Lead Heart Rate Monitor AFE, 1100x Gain, LFCSP-20", 1],
    ["ADS1115IDGST", "U2", "Package_SO:TSSOP-10_3x3mm_P0.5mm", "C37593", "ADS1115IDGST", "Ultra-Small 16-Bit Precision ADC, 860SPS, I2C, VSSOP-10", 1],
    ["MCP1700T-3002E/TT", "U3", "Package_TO_SOT_SMD:SOT-23", "C33527", "MCP1700-3002E", "Low Quiescent 3.0V 250mA Low-Dropout Linear Regulator, SOT-23", 1],
    # Connectors & Modules
    ["SJ1-3533NG", "J1", "Connector_Audio:Jack_3.5mm_CUI_SJ1-3533NG_Horizontal", "C51997", "SJ1-3533NG", "3.5mm Stereo Audio Jack for 3-Lead ECG Cable (RA/LA/RL)", 1],
    ["ECG_PROBES", "J1A", "Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical", "C124375", "1x03 Header", "2.54mm Pitch 1x03 Male Header for Breadboard ECG Lead Wires", 1],
    ["ESP32_L, ESP32_R", "J2A, J2B", "Connector_PinHeader_2.54mm:PinHeader_1x19_P2.54mm_Vertical", "C2897384", "1x19 Header", "2.54mm Pitch 1x19 Socket Headers for ESP32-WROOM-32 DevKit 38-Pin", 2],
    ["MAX30102_HEADER", "J3", "Connector_PinHeader_2.54mm:PinHeader_1x07_P2.54mm_Vertical", "C225430", "1x07 Header", "2.54mm Pitch 1x07 Socket Header for MAX30102 PPG Optical Sensor Module", 1],
    ["M3 Mounting Hole", "H1, H2, H3, H4", "MountingHole:MountingHole_3.2mm_M3_Pad", "Hardware", "M3_Pad", "3.2mm M3 Mechanical Mounting Holes with Isolated Ground Pad", 4],
    # Resistors
    ["180k 1%", "R1, R2, R3, R4", "Resistor_SMD:R_0603_1608Metric", "C22949", "180k", "0603 1/10W 1% Patient Protection Input Resistors (360k Total)", 4],
    ["10M 1%", "R5, R6", "Resistor_SMD:R_0603_1608Metric", "C25744", "10M", "0603 1/10W 1% DC Lead-Off Detection Pull-Up Resistors", 2],
    ["10M 1%", "R7", "Resistor_SMD:R_0603_1608Metric", "C25744", "10M", "0603 1/10W 1% High-Pass Filter Frequency Setting Resistor (0.5Hz)", 1],
    ["10M 1%", "R8, R9", "Resistor_SMD:R_0603_1608Metric", "C25744", "10M", "0603 1/10W 1% Internal Reference Divider Resistors (Mid-Supply Bias)", 2],
    ["100k 1%", "R10, R11", "Resistor_SMD:R_0603_1608Metric", "C25804", "100k", "0603 1/10W 1% Sallen-Key 2-Pole 40Hz Butterworth Low-Pass Filter Resistors", 2],
    ["100k 1%", "R12", "Resistor_SMD:R_0603_1608Metric", "C25804", "100k", "0603 1/10W 1% Op-Amp Inverting Feedback Gain Input Resistor", 1],
    ["1M 1%", "R13", "Resistor_SMD:R_0603_1608Metric", "C26087", "1M", "0603 1/10W 1% Op-Amp Inverting Feedback Gain Resistor (Gain = 11x)", 1],
    ["1M 1%", "R14", "Resistor_SMD:R_0603_1608Metric", "C26087", "1M", "0603 1/10W 1% Right Leg Drive (RLD) Loop Damping Resistor", 1],
    ["360k 1%", "R15", "Resistor_SMD:R_0603_1608Metric", "C22968", "360k", "0603 1/10W 1% Right Leg Drive (RLD) Patient Output Protection Resistor", 1],
    ["1k 1%", "R16, R17", "Resistor_SMD:R_0603_1608Metric", "C21190", "1k", "0603 1/10W 1% ADS1115 Differential Anti-Aliasing Filter Resistors", 2],
    ["4.7k 1%", "R18, R19", "Resistor_SMD:R_0603_1608Metric", "C25900", "4.7k", "0603 1/10W 1% I2C Bus Pull-Up Resistors (400kHz Fast Mode)", 2],
    ["10k 1%", "R20", "Resistor_SMD:R_0603_1608Metric", "C25804", "10k", "0603 1/10W 1% ADS1115 ALERT/RDY Open-Drain Pull-Up Resistor", 1],
    # Capacitors
    ["0.33uF 50V", "C1, C2", "Capacitor_SMD:C_0603_1608Metric", "C1619", "0.33uF", "0603 50V X7R High-Pass Filter Coupling Capacitors (fc = 0.5Hz)", 2],
    ["22nF 50V", "C3", "Capacitor_SMD:C_0603_1608Metric", "C1605", "22nF", "0603 50V X7R Sallen-Key Low-Pass Feedback Capacitor (C3 >= 2*C4 for Q=0.707)", 1],
    ["10nF 50V", "C4", "Capacitor_SMD:C_0603_1608Metric", "C1588", "10nF", "0603 50V X7R Sallen-Key Low-Pass Ground Capacitor", 1],
    ["0.1uF 50V", "C5", "Capacitor_SMD:C_0603_1608Metric", "C14663", "0.1uF", "0603 50V X7R Internal Reference Filter Capacitor (REFIN Decoupling)", 1],
    ["1nF 50V", "C6", "Capacitor_SMD:C_0603_1608Metric", "C1589", "1nF", "0603 50V X7R Right Leg Drive (RLD) Integrator Loop Stability Capacitor", 1],
    ["10nF 50V", "C7", "Capacitor_SMD:C_0603_1608Metric", "C1588", "10nF", "0603 50V X7R ADS1115 Differential Anti-Aliasing Filter Capacitor", 1],
    ["1nF 50V", "C8, C9", "Capacitor_SMD:C_0603_1608Metric", "C1589", "1nF", "0603 50V X7R ADS1115 Common-Mode Anti-Aliasing Filter Capacitors", 2],
    ["1uF 25V", "C10, C12, C15, C17", "Capacitor_SMD:C_0603_1608Metric", "C15849", "1uF", "0603 25V X7R Ceramic Decoupling Bulk Capacitors (LDO & IC Power Rails)", 4],
    ["0.1uF 50V", "C11, C13, C14, C16", "Capacitor_SMD:C_0603_1608Metric", "C14663", "0.1uF", "0603 50V X7R High-Frequency Bypass Decoupling Capacitors", 4],
    # Test Points
    ["TestPoint", "TP1, TP2, TP3, TP4, TP5, TP6, TP7", "TestPoint:TestPoint_Pad_D1.5mm", "PCB_PAD", "1.5mm Pad", "Surface Mount Test Points (OUT, REFOUT, LOD+, LOD-, +VS_A, +3V3, GND)", 7]
]

with open("outputs/BOM_AFE_ECG_PPG_PTT.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(bom_rows)

print("BOM generated successfully in outputs/BOM_AFE_ECG_PPG_PTT.csv")
