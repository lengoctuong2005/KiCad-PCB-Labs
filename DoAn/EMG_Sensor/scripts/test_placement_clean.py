import pcbnew, math

def mm(v): return int(round(v * 1e6))

board = pcbnew.BOARD()

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

def place_fp(lib, name, ref, val, x, y, angle=0):
    fp = pcbnew.FootprintLoad(f'/usr/share/kicad/footprints/{lib}.pretty', name)
    fp.SetReference(ref)
    fp.SetValue(val)
    fp.SetPosition(pcbnew.VECTOR2I(mm(x), mm(y)))
    fp.SetOrientation(pcbnew.EDA_ANGLE(angle, pcbnew.DEGREES_T))
    # Place reference silkscreen neatly above or below
    ref_txt = fp.Reference()
    ref_txt.SetPosition(pcbnew.VECTOR2I(mm(x), mm(y - 1.4 if angle==0 else y - 1.8)))
    board.Add(fp)
    return fp

# 1. ICs
place_fp('Package_SO', 'SOIC-8_3.9x4.9mm_P1.27mm', 'U1', 'AD623ARZ', 17.5, 14.0, 0)
place_fp('Package_SO', 'SOIC-14_3.9x8.7mm_P1.27mm', 'U2', 'MCP6004-E/SL', 35.0, 15.0, 0)

# Move U1 and U2 component body rect from F.SilkS to F.Fab to prevent silk_over_copper warnings!
for u in ('U1', 'U2'):
    f = board.FindFootprintByReference(u)
    for g in f.GraphicalItems():
        if g.GetLayerName() == 'F.SilkS' and g.GetShapeStr() == 'rect':
            g.SetLayer(pcbnew.F_Fab)

# 2. Connectors
place_fp('Connector_PinHeader_2.54mm', 'PinHeader_1x02_P2.54mm_Vertical', 'J1', 'Power_In', 25.0, 3.5, 90)
place_fp('Connector_PinHeader_2.54mm', 'PinHeader_1x03_P2.54mm_Vertical', 'J2', 'Electrodes_In', 4.0, 15.0, 0)
place_fp('Connector_PinHeader_2.54mm', 'PinHeader_1x04_P2.54mm_Vertical', 'J3', 'EMG_Out', 46.5, 15.0, 0)

# 3. Mounting Holes (hide silk text)
for i, (hx, hy) in enumerate([(2.8, 2.8), (47.2, 2.8), (2.8, 27.2), (47.2, 27.2)], 1):
    h = place_fp('MountingHole', 'MountingHole_2.2mm_M2_Pad', f'H{i}', 'M2', hx, hy, 0)
    h.Reference().SetVisible(False)
    h.Value().SetVisible(False)

# 4. Input Protection & Bias (Left side, X: 7 to 13, Y: 8 to 22)
place_fp('Resistor_SMD', 'R_0603_1608Metric', 'R4', '1k', 8.0, 12.0, 0)
place_fp('Resistor_SMD', 'R_0603_1608Metric', 'R5', '1k', 8.0, 16.0, 0)
place_fp('Capacitor_SMD', 'C_0603_1608Metric', 'C5', '100pF', 10.5, 14.0, 90)
place_fp('Capacitor_SMD', 'C_0603_1608Metric', 'C6', '47pF', 10.5, 9.0, 90)
place_fp('Capacitor_SMD', 'C_0603_1608Metric', 'C7', '47pF', 10.5, 19.0, 90)
place_fp('Resistor_SMD', 'R_0603_1608Metric', 'R6', '10M', 13.0, 9.0, 90)
place_fp('Resistor_SMD', 'R_0603_1608Metric', 'R7', '10M', 13.0, 19.0, 90)

# 5. U1 InAmp Gain & Decoupling
place_fp('Resistor_SMD', 'R_0603_1608Metric', 'R8', '1k', 17.5, 8.5, 0)
place_fp('Capacitor_SMD', 'C_0603_1608Metric', 'C8', '100nF', 20.0, 9.5, 90)

# 6. High-Pass Filter (DC Blocking)
place_fp('Capacitor_SMD', 'C_0603_1608Metric', 'C9', '1uF', 23.0, 14.64, 0)
place_fp('Resistor_SMD', 'R_0603_1608Metric', 'R9', '8.2k', 23.0, 18.5, 90)

# 7. Sallen-Key Low-Pass Filter
place_fp('Resistor_SMD', 'R_0603_1608Metric', 'R10', '22k', 26.5, 14.64, 0)
place_fp('Resistor_SMD', 'R_0603_1608Metric', 'R11', '22k', 29.5, 14.64, 0)
place_fp('Capacitor_SMD', 'C_0603_1608Metric', 'C10', '15nF', 28.0, 18.5, 0)
place_fp('Capacitor_SMD', 'C_0603_1608Metric', 'C11', '6.8nF', 29.5, 11.0, 90)
place_fp('Resistor_SMD', 'R_0603_1608Metric', 'R12', '10k', 27.0, 22.0, 0)
place_fp('Resistor_SMD', 'R_0603_1608Metric', 'R13', '91k', 30.5, 22.0, 0)

# 8. Precision Rectifier (U2C)
place_fp('Resistor_SMD', 'R_0603_1608Metric', 'R14', '10k', 35.0, 23.5, 0)
place_fp('Diode_SMD', 'D_SOD-123', 'D2', '1N4148W', 40.0, 21.0, 90)
place_fp('Diode_SMD', 'D_SOD-123', 'D3', '1N4148W', 43.0, 21.0, 90)
place_fp('Resistor_SMD', 'R_0603_1608Metric', 'R15', '10k', 41.5, 25.0, 0)

# 9. Envelope Integrator (U2D)
place_fp('Resistor_SMD', 'R_0603_1608Metric', 'R16', '20k', 41.5, 16.5, 0)
place_fp('Resistor_SMD', 'R_0603_1608Metric', 'R17', '10k', 41.5, 14.0, 0)
place_fp('Resistor_SMD', 'R_0603_1608Metric', 'R18', '100k', 41.5, 11.5, 0)
place_fp('Capacitor_SMD', 'C_0603_1608Metric', 'C12', '330nF', 41.5, 9.0, 0)

# 10. Rail Splitter & Virtual Ground (Top row, X: 8 to 22, Y: 4.5)
place_fp('Capacitor_SMD', 'C_0805_2012Metric', 'C1', '10uF', 8.5, 4.0, 0)
place_fp('Capacitor_SMD', 'C_0603_1608Metric', 'C2', '100nF', 12.0, 4.0, 0)
place_fp('LED_SMD', 'LED_0805_2012Metric', 'D1', 'Green_PWR', 15.5, 4.0, 0)
place_fp('Resistor_SMD', 'R_0603_1608Metric', 'R1', '1k', 19.5, 4.0, 0)

place_fp('Resistor_SMD', 'R_0603_1608Metric', 'R2', '100k', 31.0, 4.0, 0)
place_fp('Resistor_SMD', 'R_0603_1608Metric', 'R3', '100k', 34.5, 4.0, 0)
place_fp('Capacitor_SMD', 'C_0805_2012Metric', 'C3', '10uF', 38.0, 4.0, 0)
place_fp('Capacitor_SMD', 'C_0603_1608Metric', 'C4', '100nF', 41.5, 4.0, 0)

# 11. U2 Decoupling & Activity LED
place_fp('Capacitor_SMD', 'C_0603_1608Metric', 'C13', '100nF', 35.0, 8.5, 0)
place_fp('Resistor_SMD', 'R_0603_1608Metric', 'R19', '1k', 44.5, 8.5, 90)
place_fp('LED_SMD', 'LED_0805_2012Metric', 'D4', 'Red_ACT', 44.5, 5.5, 0)

pcbnew.SaveBoard('/tmp/test_clean_place.kicad_pcb', board)
print("Saved clean placement test board!")
