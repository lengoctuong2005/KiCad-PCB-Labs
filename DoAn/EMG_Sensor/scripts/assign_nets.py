import pcbnew

board = pcbnew.LoadBoard('DoAn/EMG_Sensor/EMG_Sensor.kicad_pcb')

pad_net_map = {
    # Connectors
    ('J1', '1'): 'VCC',
    ('J1', '2'): 'GND',
    ('J2', '1'): 'IN_PLUS_RAW',
    ('J2', '2'): 'IN_MINUS_RAW',
    ('J2', '3'): 'VREF',
    ('J3', '1'): 'VCC',
    ('J3', '2'): 'GND',
    ('J3', '3'): 'RAW_EMG',
    ('J3', '4'): 'ENV_EMG',
    # ICs
    ('U1', '1'): 'RG1',
    ('U1', '2'): 'IN_MINUS_FILT',
    ('U1', '3'): 'IN_PLUS_FILT',
    ('U1', '4'): 'GND',
    ('U1', '5'): 'VREF',
    ('U1', '6'): 'VOUT_IA',
    ('U1', '7'): 'VCC',
    ('U1', '8'): 'RG2',
    ('U2', '1'): 'VREF',
    ('U2', '2'): 'VREF',
    ('U2', '3'): 'VMID',
    ('U2', '4'): 'VCC',
    ('U2', '5'): 'LPF_IN',
    ('U2', '6'): 'LPF_FB',
    ('U2', '7'): 'RAW_EMG',
    ('U2', '8'): 'RECT_OUT',
    ('U2', '9'): 'RECT_IN',
    ('U2', '10'): 'VREF',
    ('U2', '11'): 'GND',
    ('U2', '12'): 'VREF',
    ('U2', '13'): 'ENV_IN',
    ('U2', '14'): 'ENV_EMG',
    # Diodes
    ('D1', '1'): 'NET_D1_R1',
    ('D1', '2'): 'VCC',
    ('D2', '1'): 'RECT_OUT',
    ('D2', '2'): 'RECT_IN',
    ('D3', '1'): 'RECT_HALF',
    ('D3', '2'): 'RECT_OUT',
    ('D4', '1'): 'GND',
    ('D4', '2'): 'NET_D4_R19',
    # Resistors
    ('R1', '1'): 'NET_D1_R1',
    ('R1', '2'): 'GND',
    ('R2', '1'): 'VCC',
    ('R2', '2'): 'VMID',
    ('R3', '1'): 'VMID',
    ('R3', '2'): 'GND',
    ('R4', '1'): 'IN_PLUS_RAW',
    ('R4', '2'): 'IN_PLUS_FILT',
    ('R5', '1'): 'IN_MINUS_RAW',
    ('R5', '2'): 'IN_MINUS_FILT',
    ('R6', '1'): 'IN_PLUS_FILT',
    ('R6', '2'): 'VREF',
    ('R7', '1'): 'IN_MINUS_FILT',
    ('R7', '2'): 'VREF',
    ('R8', '1'): 'RG1',
    ('R8', '2'): 'RG2',
    ('R9', '1'): 'HPF_OUT',
    ('R9', '2'): 'VREF',
    ('R10', '1'): 'HPF_OUT',
    ('R10', '2'): 'LPF_NODE',
    ('R11', '1'): 'LPF_NODE',
    ('R11', '2'): 'LPF_IN',
    ('R12', '1'): 'LPF_FB',
    ('R12', '2'): 'VREF',
    ('R13', '1'): 'LPF_FB',
    ('R13', '2'): 'RAW_EMG',
    ('R14', '1'): 'RAW_EMG',
    ('R14', '2'): 'RECT_IN',
    ('R15', '1'): 'RECT_IN',
    ('R15', '2'): 'RECT_HALF',
    ('R16', '1'): 'RECT_HALF',
    ('R16', '2'): 'ENV_IN',
    ('R17', '1'): 'RAW_EMG',
    ('R17', '2'): 'ENV_IN',
    ('R18', '1'): 'ENV_IN',
    ('R18', '2'): 'ENV_EMG',
    ('R19', '1'): 'ENV_EMG',
    ('R19', '2'): 'NET_D4_R19',
    # Capacitors
    ('C1', '1'): 'VCC',
    ('C1', '2'): 'GND',
    ('C2', '1'): 'VCC',
    ('C2', '2'): 'GND',
    ('C3', '1'): 'VMID',
    ('C3', '2'): 'GND',
    ('C4', '1'): 'VMID',
    ('C4', '2'): 'GND',
    ('C5', '1'): 'IN_PLUS_FILT',
    ('C5', '2'): 'IN_MINUS_FILT',
    ('C6', '1'): 'IN_PLUS_FILT',
    ('C6', '2'): 'GND',
    ('C7', '1'): 'IN_MINUS_FILT',
    ('C7', '2'): 'GND',
    ('C8', '1'): 'VCC',
    ('C8', '2'): 'GND',
    ('C9', '1'): 'VOUT_IA',
    ('C9', '2'): 'HPF_OUT',
    ('C10', '1'): 'LPF_NODE',
    ('C10', '2'): 'RAW_EMG',
    ('C11', '1'): 'LPF_IN',
    ('C11', '2'): 'VREF',
    ('C12', '1'): 'ENV_IN',
    ('C12', '2'): 'ENV_EMG',
    ('C13', '1'): 'VCC',
    ('C13', '2'): 'GND',
}

# Ensure all needed nets exist
all_nets = set(pad_net_map.values())
for netname in all_nets:
    if not board.FindNet(netname):
        net = pcbnew.NETINFO_ITEM(board, netname)
        board.Add(net)

assigned = 0
for (ref, pin), netname in pad_net_map.items():
    fp = board.FindFootprintByReference(ref)
    if not fp:
        print(f"Warning: footprint {ref} not found!")
        continue
    pad = fp.FindPadByNumber(pin)
    if not pad:
        print(f"Warning: pad {ref}.{pin} not found!")
        continue
    pad.SetNet(board.FindNet(netname))
    assigned += 1

# Mounting holes are connected to GND
for i in range(1, 5):
    h = board.FindFootprintByReference(f'H{i}')
    if h:
        p = h.FindPadByNumber('1')
        if p: p.SetNet(board.FindNet('GND'))

pcbnew.SaveBoard('DoAn/EMG_Sensor/EMG_Sensor.kicad_pcb', board)
print(f"Assigned nets to {assigned} pads successfully!")
