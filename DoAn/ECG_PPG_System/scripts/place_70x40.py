import pcbnew, math

def mm(v): return int(round(v * 1e6))

board = pcbnew.BOARD()

ds = board.GetDesignSettings()
ds.m_TrackMinWidth = mm(0.20)
ds.m_ViasMinSize = mm(0.60)
ds.m_ViasMinDrill = mm(0.30)

BW, BH = 70.0, 40.0
outline_pts = [(0, 0), (BW, 0), (BW, BH), (0, BH), (0, 0)]
for (x1, y1), (x2, y2) in zip(outline_pts, outline_pts[1:]):
    seg = pcbnew.PCB_SHAPE(board)
    seg.SetShape(pcbnew.SHAPE_T_SEGMENT)
    seg.SetStart(pcbnew.VECTOR2I(mm(x1), mm(y1)))
    seg.SetEnd(pcbnew.VECTOR2I(mm(x2), mm(y2)))
    seg.SetWidth(mm(0.15))
    seg.SetLayer(pcbnew.Edge_Cuts)
    board.Add(seg)

def place_fp(lib, name, ref, val, x, y, angle=0):
    fp = pcbnew.FootprintLoad(f'/usr/share/kicad/footprints/{lib}.pretty', name)
    fp.SetReference(ref)
    fp.SetValue(val)
    fp.SetPosition(pcbnew.VECTOR2I(mm(x), mm(y)))
    fp.SetOrientation(pcbnew.EDA_ANGLE(angle, pcbnew.DEGREES_T))
    fp.Reference().SetLayer(pcbnew.F_Fab)
    fp.Value().SetLayer(pcbnew.F_Fab)
    for g in fp.GraphicalItems():
        if g.GetLayerName() == 'F.SilkS' and g.GetShapeStr() == 'rect':
            g.SetLayer(pcbnew.F_Fab)
    board.Add(fp)
    return fp

# 1. ICs (Spaced out horizontally: X = 20.0, 38.0, 56.0, Y = 18.0)
place_fp('Package_SO', 'SOIC-8_3.9x4.9mm_P1.27mm', 'U1', 'AD623ARZ', 20.0, 18.0, 0)
place_fp('Package_SO', 'SOIC-14_3.9x8.7mm_P1.27mm', 'U2', 'MCP6004-E/SL', 38.0, 18.0, 0)
place_fp('Package_SO', 'SOIC-8_3.9x4.9mm_P1.27mm', 'U3', 'MCP6002-E/SN', 56.0, 18.0, 0)

# 2. Connectors
place_fp('Connector_PinHeader_2.54mm', 'PinHeader_1x02_P2.54mm_Vertical', 'J1', 'Power_In', 30.0, 4.0, 90)
place_fp('Connector_PinHeader_2.54mm', 'PinHeader_1x03_P2.54mm_Vertical', 'J2', 'ECG_Leads', 4.0, 11.0, 0)
place_fp('Connector_PinHeader_2.54mm', 'PinHeader_1x04_P2.54mm_Vertical', 'J3', 'PPG_Sensor', 4.0, 22.0, 0)
place_fp('Connector_PinHeader_2.54mm', 'PinHeader_1x06_P2.54mm_Vertical', 'J4', 'System_Out', 66.5, 12.0, 0)

# 3. Mounting Holes M2 (hide silk text)
for i, (hx, hy) in enumerate([(2.8, 2.8), (67.2, 2.8), (2.8, 37.2), (67.2, 37.2)], 1):
    h = place_fp('MountingHole', 'MountingHole_2.2mm_M2_Pad', f'H{i}', 'M2', hx, hy, 0)
    h.Reference().SetVisible(False)
    h.Value().SetVisible(False)

# 4. Power & Virtual Ground (Top row: X: 8 to 50, Y: 4.5)
place_fp('Capacitor_SMD', 'C_0805_2012Metric', 'C1', '10uF', 8.5, 4.0, 0)
place_fp('Capacitor_SMD', 'C_0603_1608Metric', 'C2', '100nF', 12.0, 4.0, 0)
place_fp('LED_SMD', 'LED_0805_2012Metric', 'D1', 'Green_PWR', 15.5, 4.0, 0)
place_fp('Resistor_SMD', 'R_0603_1608Metric', 'R3', '1k', 19.5, 4.0, 0)

place_fp('Resistor_SMD', 'R_0603_1608Metric', 'R1', '100k', 36.0, 4.0, 0)
place_fp('Resistor_SMD', 'R_0603_1608Metric', 'R2', '100k', 39.5, 4.0, 0)
place_fp('Capacitor_SMD', 'C_0805_2012Metric', 'C3', '10uF', 43.0, 4.0, 0)
place_fp('Capacitor_SMD', 'C_0603_1608Metric', 'C4', '100nF', 46.5, 4.0, 0)

# 5. ECG Input Filter (X: 8 to 15, Y: 9 to 18)
place_fp('Resistor_SMD', 'R_0603_1608Metric', 'R4', '1k', 8.5, 11.5, 0)
place_fp('Resistor_SMD', 'R_0603_1608Metric', 'R5', '1k', 8.5, 15.5, 0)
place_fp('Capacitor_SMD', 'C_0603_1608Metric', 'C5', '100pF', 11.5, 13.5, 90)
place_fp('Capacitor_SMD', 'C_0603_1608Metric', 'C6', '47pF', 11.5, 9.5, 90)
place_fp('Capacitor_SMD', 'C_0603_1608Metric', 'C7', '47pF', 11.5, 17.5, 90)
place_fp('Resistor_SMD', 'R_0603_1608Metric', 'R6', '10M', 14.5, 9.5, 90)
place_fp('Resistor_SMD', 'R_0603_1608Metric', 'R7', '10M', 14.5, 17.5, 90)

# U1 Gain & Decoupling
place_fp('Resistor_SMD', 'R_0603_1608Metric', 'R8', '1k', 20.0, 11.5, 0)
place_fp('Capacitor_SMD', 'C_0603_1608Metric', 'C8', '100nF', 23.0, 12.5, 90)

# 6. DRL Circuit (Below U1, Y: 22 to 27)
place_fp('Resistor_SMD', 'R_0603_1608Metric', 'R9', '100k', 14.5, 22.0, 90)
place_fp('Resistor_SMD', 'R_0603_1608Metric', 'R10', '100k', 17.5, 22.0, 90)
place_fp('Resistor_SMD', 'R_0603_1608Metric', 'R11', '1M', 20.5, 23.0, 0)
place_fp('Capacitor_SMD', 'C_0603_1608Metric', 'C9', '1nF', 24.5, 23.0, 0)
place_fp('Resistor_SMD', 'R_0603_1608Metric', 'R12', '390k', 10.5, 22.0, 90)

# 7. ECG Filter (Between U1 & U2, X: 26 to 34)
place_fp('Capacitor_SMD', 'C_0603_1608Metric', 'C10', '1uF', 27.5, 16.5, 0)
place_fp('Resistor_SMD', 'R_0603_1608Metric', 'R13', '330k', 27.5, 20.0, 90)
place_fp('Resistor_SMD', 'R_0603_1608Metric', 'R14', '39k', 31.0, 16.5, 0)
place_fp('Capacitor_SMD', 'C_0603_1608Metric', 'C12', '47nF', 31.0, 12.5, 90)

# R15, C11, R16, R17 (Below U2, Y: 25 to 30)
place_fp('Resistor_SMD', 'R_0603_1608Metric', 'R15', '39k', 34.0, 26.0, 0)
place_fp('Capacitor_SMD', 'C_0603_1608Metric', 'C11', '100nF', 38.0, 26.0, 0)
place_fp('Resistor_SMD', 'R_0603_1608Metric', 'R16', '10k', 34.0, 29.5, 0)
place_fp('Resistor_SMD', 'R_0603_1608Metric', 'R17', '91k', 38.0, 29.5, 0)
place_fp('Capacitor_SMD', 'C_0603_1608Metric', 'C13', '100nF', 38.0, 10.5, 0)

# 8. PPG TIA (Bottom left, X: 8 to 22, Y: 30 to 35)
place_fp('Resistor_SMD', 'R_0603_1608Metric', 'R19', '220R', 8.5, 31.0, 0)
place_fp('Resistor_SMD', 'R_0603_1608Metric', 'R18', '1M', 13.5, 31.0, 0)
place_fp('Capacitor_SMD', 'C_0603_1608Metric', 'C14', '22pF', 17.5, 31.0, 0)

# 9. PPG Filter (Between U2 and U3, X: 44 to 52)
place_fp('Capacitor_SMD', 'C_0603_1608Metric', 'C15', '1uF', 45.0, 23.0, 0)
place_fp('Resistor_SMD', 'R_0603_1608Metric', 'R20', '330k', 49.0, 23.0, 0)
place_fp('Resistor_SMD', 'R_0603_1608Metric', 'R21', '15k', 45.0, 27.0, 0)
place_fp('Resistor_SMD', 'R_0603_1608Metric', 'R22', '15k', 49.0, 27.0, 0)
place_fp('Capacitor_SMD', 'C_0603_1608Metric', 'C16', '1uF', 45.0, 31.0, 0)
place_fp('Capacitor_SMD', 'C_0603_1608Metric', 'C17', '470nF', 49.0, 31.0, 0)
place_fp('Resistor_SMD', 'R_0603_1608Metric', 'R23', '1k', 45.0, 35.0, 0)
place_fp('Resistor_SMD', 'R_0603_1608Metric', 'R24', '47k', 49.0, 35.0, 0)

# 10. Heartbeat Pulse Detector & LED (Right side, X: 54 to 62, Y: 4 to 12)
place_fp('Resistor_SMD', 'R_0603_1608Metric', 'R25', '100k', 53.0, 4.0, 0)
place_fp('Resistor_SMD', 'R_0603_1608Metric', 'R26', '10k', 57.0, 4.0, 0)
place_fp('Capacitor_SMD', 'C_0603_1608Metric', 'C18', '100nF', 56.0, 10.5, 0)
place_fp('Resistor_SMD', 'R_0603_1608Metric', 'R27', '1k', 60.0, 10.5, 0)
place_fp('LED_SMD', 'LED_0805_2012Metric', 'D2', 'Red_PULSE', 62.0, 6.0, 90)

pcbnew.SaveBoard('DoAn/ECG_PPG_System/ECG_PPG_System.kicad_pcb', board)
print("Saved 70.0 x 40.0 mm board layout!")
