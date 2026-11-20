import pcbnew, math

def mm(v): return int(round(v * 1e6))

board = pcbnew.BOARD()

# Set design settings
ds = board.GetDesignSettings()
ds.m_TrackMinWidth = mm(0.20)
ds.m_ViasMinSize = mm(0.60)
ds.m_ViasMinDrill = mm(0.30)

BW, BH = 50.0, 30.0
outline_pts = [(0, 0), (BW, 0), (BW, BH), (0, BH), (0, 0)]
for (x1, y1), (x2, y2) in zip(outline_pts, outline_pts[1:]):
    seg = pcbnew.PCB_SHAPE(board)
    seg.SetShape(pcbnew.SHAPE_T_SEGMENT)
    seg.SetStart(pcbnew.VECTOR2I(mm(x1), mm(y1)))
    seg.SetEnd(pcbnew.VECTOR2I(mm(x2), mm(y2)))
    seg.SetWidth(mm(0.15))
    seg.SetLayer(pcbnew.Edge_Cuts)
    board.Add(seg)

# Define Nets
net_names = [
    'GND', 'VCC', 'VMID', 'VREF',
    'IN_PLUS_RAW', 'IN_MINUS_RAW', 'BODY_REF',
    'IN_PLUS_FILT', 'IN_MINUS_FILT',
    'RG1', 'RG2', 'VOUT_IA',
    'HPF_OUT', 'LPF_NODE', 'LPF_IN', 'LPF_FB', 'RAW_EMG',
    'RECT_IN', 'RECT_OUT', 'RECT_HALF',
    'ENV_IN', 'ENV_EMG',
    'NET_D1_R1', 'NET_D4_R19'
]

nets = {}
for name in net_names:
    net = pcbnew.NETINFO_ITEM(board, name)
    board.Add(net)
    nets[name] = board.FindNet(name)

# Helper function to place footprint
def place_fp(lib, name, ref, val, x, y, angle=0):
    fp = pcbnew.FootprintLoad(f'/usr/share/kicad/footprints/{lib}.pretty', name)
    if not fp:
        raise ValueError(f"Could not load footprint {lib}:{name}")
    fp.SetReference(ref)
    fp.SetValue(val)
    fp.SetPosition(pcbnew.VECTOR2I(mm(x), mm(y)))
    fp.SetOrientation(pcbnew.EDA_ANGLE(angle, pcbnew.DEGREES_T))
    board.Add(fp)
    return fp

# 1. ICs
place_fp('Package_SO', 'SOIC-8_3.9x4.9mm_P1.27mm', 'U1', 'AD623ARZ', 17.5, 14.0, 90)
place_fp('Package_SO', 'SOIC-14_3.9x8.7mm_P1.27mm', 'U2', 'MCP6004-E/SL', 35.0, 15.0, 90)

# 2. Connectors
place_fp('Connector_PinHeader_2.54mm', 'PinHeader_1x02_P2.54mm_Vertical', 'J1', 'Power_In', 6.0, 5.0, 90)
place_fp('Connector_PinHeader_2.54mm', 'PinHeader_1x03_P2.54mm_Vertical', 'J2', 'Electrodes_In', 5.0, 15.0, 0)
place_fp('Connector_PinHeader_2.54mm', 'PinHeader_1x04_P2.54mm_Vertical', 'J3', 'EMG_Out', 46.5, 15.0, 0)

# 3. Diodes
place_fp('LED_SMD', 'LED_0805_2012Metric', 'D1', 'Green_PWR', 16.0, 5.0, 0)
place_fp('Diode_SMD', 'D_SOD-123', 'D2', '1N4148W', 40.5, 20.0, 90)
place_fp('Diode_SMD', 'D_SOD-123', 'D3', '1N4148W', 43.0, 20.0, 90)
place_fp('LED_SMD', 'LED_0805_2012Metric', 'D4', 'Red_ACT', 44.0, 5.0, 0)

# 4. Resistors (0603)
resistors = [
    ('R1', '1k', 19.0, 5.0, 0),
    ('R2', '100k', 22.5, 5.0, 0),
    ('R3', '100k', 25.5, 5.0, 0),
    ('R4', '1k', 8.5, 12.5, 0),
    ('R5', '1k', 8.5, 15.0, 0),
    ('R6', '10M', 13.0, 10.5, 90),
    ('R7', '10M', 13.0, 17.0, 90),
    ('R8', '1k', 17.5, 9.5, 0),
    ('R9', '8.2k', 24.5, 11.5, 90),
    ('R10', '22k', 26.5, 14.64, 0),
    ('R11', '22k', 29.5, 14.64, 0),
    ('R12', '10k', 28.0, 20.5, 0),
    ('R13', '91k', 31.0, 20.5, 0),
    ('R14', '10k', 38.0, 22.5, 0),
    ('R15', '10k', 41.5, 23.5, 0),
    ('R16', '20k', 41.0, 16.5, 0),
    ('R17', '10k', 41.0, 14.0, 0),
    ('R18', '100k', 41.0, 11.5, 0),
    ('R19', '1k', 41.0, 5.0, 0),
]
for ref, val, x, y, angle in resistors:
    place_fp('Resistor_SMD', 'R_0603_1608Metric', ref, val, x, y, angle)

# 5. Capacitors (0603 & 0805)
capacitors = [
    ('C1', '10uF', 'Capacitor_SMD', 'C_0805_2012Metric', 10.0, 5.0, 0),
    ('C2', '100nF', 'Capacitor_SMD', 'C_0603_1608Metric', 13.0, 5.0, 0),
    ('C3', '10uF', 'Capacitor_SMD', 'C_0805_2012Metric', 28.5, 5.0, 0),
    ('C4', '100nF', 'Capacitor_SMD', 'C_0603_1608Metric', 31.5, 5.0, 0),
    ('C5', '100pF', 'Capacitor_SMD', 'C_0603_1608Metric', 11.0, 13.75, 90),
    ('C6', '47pF', 'Capacitor_SMD', 'C_0603_1608Metric', 11.0, 10.5, 90),
    ('C7', '47pF', 'Capacitor_SMD', 'C_0603_1608Metric', 11.0, 17.0, 90),
    ('C8', '100nF', 'Capacitor_SMD', 'C_0603_1608Metric', 20.5, 10.5, 90),
    ('C9', '1uF', 'Capacitor_SMD', 'C_0603_1608Metric', 23.0, 14.64, 0),
    ('C10', '15nF', 'Capacitor_SMD', 'C_0603_1608Metric', 28.0, 17.5, 0),
    ('C11', '6.8nF', 'Capacitor_SMD', 'C_0603_1608Metric', 31.0, 11.5, 90),
    ('C12', '330nF', 'Capacitor_SMD', 'C_0603_1608Metric', 41.0, 9.0, 0),
    ('C13', '100nF', 'Capacitor_SMD', 'C_0603_1608Metric', 35.0, 8.5, 0),
]
for ref, val, lib, fp_name, x, y, angle in capacitors:
    place_fp(lib, fp_name, ref, val, x, y, angle)

# 6. Mounting Holes (M2.5 plated / through-hole)
for i, (hx, hy) in enumerate([(3.0, 3.0), (47.0, 3.0), (3.0, 27.0), (47.0, 27.0)], 1):
    place_fp('MountingHole', 'MountingHole_2.2mm_M2_Pad', f'H{i}', 'MountingHole_M2', hx, hy, 0)

pcbnew.SaveBoard('DoAn/EMG_Sensor/EMG_Sensor.kicad_pcb', board)
print("Board with 41 components + 4 mounting holes created and saved!")
