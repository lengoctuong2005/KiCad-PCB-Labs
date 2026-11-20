import pcbnew

# Netlist definition: net_name -> list of (ref, pad_name)
NET_MAP = {
    # Power & Ground
    "GND": [
        ("U1", "14"), ("U1", "16"), ("U1", "21"), # AD8232 AC/DC, GND, EP
        ("U2", "1"), ("U2", "3"), ("U2", "6"), ("U2", "7"), # ADS1115 ADDR, GND, AIN2, AIN3
        ("U3", "1"), # MCP1700 GND
        ("J2A", "14"), ("J2B", "1"), ("J2B", "7"), # ESP32 GND
        ("J3", "7"), # MAX30102 GND
        ("R7", "2"), ("R9", "2"), # HPF pulldown, REFIN pulldown
        ("C5", "2"), ("C8", "2"), ("C9", "2"), # REFIN cap, AIN0/AIN1 filt to GND
        ("C10", "2"), ("C11", "2"), ("C12", "2"), ("C13", "2"), # LDO caps
        ("C14", "2"), ("C15", "2"), # AD8232 caps
        ("C16", "2"), ("C17", "2"), # ADS1115 caps
        ("TP7", "1"), # GND testpoint
        ("H1", "1"), ("H2", "1"), ("H3", "1"), ("H4", "1") # Mounting holes
    ],
    "+3V3": [
        ("J2A", "1"), # ESP32 3V3 out
        ("U3", "3"), # MCP1700 VIN
        ("C10", "1"), ("C11", "1"), # LDO VIN caps
        ("U2", "8"), # ADS1115 VDD
        ("C16", "1"), ("C17", "1"), # ADS1115 VDD caps
        ("J3", "1"), # MAX30102 VIN
        ("R18", "1"), ("R19", "1"), ("R20", "1"), # I2C & ALERT pullups
        ("TP6", "1") # 3V3 testpoint
    ],
    "+VS_A": [
        ("U3", "2"), # MCP1700 VOUT (3.0V)
        ("C12", "1"), ("C13", "1"), # LDO VOUT caps
        ("U1", "13"), ("U1", "17"), # AD8232 SDN, +VS
        ("C14", "1"), ("C15", "1"), # AD8232 +VS caps
        ("R5", "1"), ("R6", "1"), # Lead-off DC pullups
        ("R8", "1"), # REFIN divider pullup
        ("TP5", "1") # +VS_A testpoint
    ],
    "+5V": [
        ("J2A", "19") # ESP32 5V
    ],
    
    # Electrodes & Protection
    "RA_RAW": [("J1", "T"), ("J1A", "1"), ("R1", "1")],
    "RA_INT": [("R1", "2"), ("R3", "1")],
    "RA_FILT": [("R3", "2"), ("R5", "2"), ("U1", "2")], # U1 +IN
    
    "LA_RAW": [("J1", "R"), ("J1A", "2"), ("R2", "1")],
    "LA_INT": [("R2", "2"), ("R4", "1")],
    "LA_FILT": [("R4", "2"), ("R6", "2"), ("U1", "3")], # U1 -IN
    
    "RL_RAW": [("J1", "S"), ("J1A", "3"), ("R15", "2")],
    "RLD_OUT": [("U1", "5"), ("R15", "1"), ("C6", "2"), ("R14", "2")],
    "RLDFB": [("U1", "4"), ("C6", "1"), ("R14", "1")],
    
    # AD8232 High-Pass Filter & SW
    "HPDRIVE": [("U1", "1"), ("C1", "1")],
    "HP_MID": [("C1", "2"), ("C2", "1"), ("U1", "6"), ("R7", "1")], # U1 SW
    "HPSENSE": [("C2", "2"), ("U1", "20")],
    
    # Reference
    "REFIN": [("U1", "18"), ("R8", "2"), ("R9", "1"), ("C5", "1")],
    "REFOUT": [("U1", "8"), ("C4", "2"), ("R12", "2"), ("R17", "1"), ("TP2", "1")],
    
    # Sallen-Key Low-Pass Filter
    "IAOUT": [("U1", "19"), ("R10", "1")],
    "SK_N1": [("R10", "2"), ("R11", "1"), ("C3", "1")],
    "OPAMP_P": [("U1", "7"), ("R11", "2"), ("C4", "1")],
    "OPAMP_N": [("U1", "9"), ("R12", "1"), ("R13", "1")],
    "ECG_OUT": [
        ("U1", "10"), ("C3", "2"), ("R13", "2"),
        ("R16", "1"), ("TP1", "1"), ("J2A", "5") # ESP32 GPIO34 backup ADC
    ],
    
    # ADS1115 Anti-Aliasing Filter
    "AIN0_FILT": [("R16", "2"), ("C7", "1"), ("C8", "1"), ("U2", "4")],
    "AIN1_FILT": [("R17", "2"), ("C7", "2"), ("C9", "1"), ("U2", "5")],
    
    # Control & Digital I/O
    "LOD+": [("U1", "12"), ("J2A", "7"), ("TP3", "1")], # ESP32 GPIO32
    "LOD-": [("U1", "11"), ("J2A", "8"), ("TP4", "1")], # ESP32 GPIO33
    "FR": [("U1", "15"), ("J2A", "9")], # ESP32 GPIO25
    "ADS_ALERT": [("U2", "2"), ("R20", "2"), ("J2A", "11")], # ESP32 GPIO27
    "MAX_INT": [("J3", "4"), ("J2A", "10")], # ESP32 GPIO26
    "I2C_SDA": [("U2", "9"), ("J3", "3"), ("R18", "2"), ("J2B", "6")], # ESP32 GPIO21
    "I2C_SCL": [("U2", "10"), ("J3", "2"), ("R19", "2"), ("J2B", "3")], # ESP32 GPIO22
    
    # Auxiliary pins
    "MAX_RD": [("J3", "5")],
    "MAX_IRD": [("J3", "6")]
}

print(f"Total defined nets: {len(NET_MAP)}")
total_pins = sum(len(pins) for pins in NET_MAP.values())
print(f"Total mapped pin connections: {total_pins}")
