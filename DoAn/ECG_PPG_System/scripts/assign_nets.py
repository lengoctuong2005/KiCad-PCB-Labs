import pcbnew

board = pcbnew.LoadBoard('DoAn/ECG_PPG_System/ECG_PPG_System.kicad_pcb')

pad_net_map = {
    # Connectors
    ('J1', '1'): 'VCC', ('J1', '2'): 'GND',
    ('J2', '1'): 'RA_RAW', ('J2', '2'): 'LA_RAW', ('J2', '3'): 'RL_DRL',
    ('J3', '1'): 'VCC', ('J3', '2'): 'LED_DRV', ('J3', '3'): 'PD_ANODE', ('J3', '4'): 'GND',
    ('J4', '1'): 'VCC', ('J4', '2'): 'GND', ('J4', '3'): 'ECG_OUT', ('J4', '4'): 'PPG_OUT', ('J4', '5'): 'PULSE_TRIG', ('J4', '6'): 'VREF',
    # ICs
    ('U1', '1'): 'RG1', ('U1', '2'): 'RA_FILT', ('U1', '3'): 'LA_FILT', ('U1', '4'): 'GND',
    ('U1', '5'): 'VREF', ('U1', '6'): 'ECG_IA_OUT', ('U1', '7'): 'VCC', ('U1', '8'): 'RG2',
    ('U2', '1'): 'VREF', ('U2', '2'): 'VREF', ('U2', '3'): 'VMID', ('U2', '4'): 'VCC',
    ('U2', '5'): 'DRL_CM', ('U2', '6'): 'VREF', ('U2', '7'): 'DRL_OUT', ('U2', '8'): 'ECG_OUT',
    ('U2', '9'): 'ECG_FB', ('U2', '10'): 'ECG_LPF_IN', ('U2', '11'): 'GND', ('U2', '12'): 'PD_ANODE',
    ('U2', '13'): 'VREF', ('U2', '14'): 'PPG_TIA_OUT',
    ('U3', '1'): 'PPG_OUT', ('U3', '2'): 'PPG_FB', ('U3', '3'): 'PPG_LPF_IN', ('U3', '4'): 'GND',
    ('U3', '5'): 'PPG_OUT', ('U3', '6'): 'VREF_THR', ('U3', '7'): 'PULSE_TRIG', ('U3', '8'): 'VCC',
    # LEDs
    ('D1', '1'): 'GND', ('D1', '2'): 'NET_D1_R3',
    ('D2', '1'): 'GND', ('D2', '2'): 'NET_D2_R27',
    # Resistors
    ('R1', '1'): 'VCC', ('R1', '2'): 'VMID',
    ('R2', '1'): 'VMID', ('R2', '2'): 'GND',
    ('R3', '1'): 'VCC', ('R3', '2'): 'NET_D1_R3',
    ('R4', '1'): 'RA_RAW', ('R4', '2'): 'RA_FILT',
    ('R5', '1'): 'LA_RAW', ('R5', '2'): 'LA_FILT',
    ('R6', '1'): 'RA_FILT', ('R6', '2'): 'VREF',
    ('R7', '1'): 'LA_FILT', ('R7', '2'): 'VREF',
    ('R8', '1'): 'RG1', ('R8', '2'): 'RG2',
    ('R9', '1'): 'RA_FILT', ('R9', '2'): 'DRL_CM',
    ('R10', '1'): 'LA_FILT', ('R10', '2'): 'DRL_CM',
    ('R11', '1'): 'DRL_CM', ('R11', '2'): 'DRL_OUT',
    ('R12', '1'): 'DRL_OUT', ('R12', '2'): 'RL_DRL',
    ('R13', '1'): 'ECG_HPF_OUT', ('R13', '2'): 'VREF',
    ('R14', '1'): 'ECG_HPF_OUT', ('R14', '2'): 'ECG_LPF_NODE',
    ('R15', '1'): 'ECG_LPF_NODE', ('R15', '2'): 'ECG_LPF_IN',
    ('R16', '1'): 'ECG_FB', ('R16', '2'): 'VREF',
    ('R17', '1'): 'ECG_FB', ('R17', '2'): 'ECG_OUT',
    ('R18', '1'): 'PD_ANODE', ('R18', '2'): 'PPG_TIA_OUT',
    ('R19', '1'): 'VCC', ('R19', '2'): 'LED_DRV',
    ('R20', '1'): 'PPG_HPF_OUT', ('R20', '2'): 'VREF',
    ('R21', '1'): 'PPG_HPF_OUT', ('R21', '2'): 'PPG_LPF_NODE',
    ('R22', '1'): 'PPG_LPF_NODE', ('R22', '2'): 'PPG_LPF_IN',
    ('R23', '1'): 'PPG_FB', ('R23', '2'): 'VREF',
    ('R24', '1'): 'PPG_FB', ('R24', '2'): 'PPG_OUT',
    ('R25', '1'): 'VREF', ('R25', '2'): 'VREF_THR',
    ('R26', '1'): 'VREF_THR', ('R26', '2'): 'GND',
    ('R27', '1'): 'PULSE_TRIG', ('R27', '2'): 'NET_D2_R27',
    # Capacitors
    ('C1', '1'): 'VCC', ('C1', '2'): 'GND',
    ('C2', '1'): 'VCC', ('C2', '2'): 'GND',
    ('C3', '1'): 'VMID', ('C3', '2'): 'GND',
    ('C4', '1'): 'VMID', ('C4', '2'): 'GND',
    ('C5', '1'): 'RA_FILT', ('C5', '2'): 'LA_FILT',
    ('C6', '1'): 'RA_FILT', ('C6', '2'): 'GND',
    ('C7', '1'): 'LA_FILT', ('C7', '2'): 'GND',
    ('C8', '1'): 'VCC', ('C8', '2'): 'GND',
    ('C9', '1'): 'DRL_CM', ('C9', '2'): 'DRL_OUT',
    ('C10', '1'): 'ECG_IA_OUT', ('C10', '2'): 'ECG_HPF_OUT',
    ('C11', '1'): 'ECG_LPF_NODE', ('C11', '2'): 'ECG_OUT',
    ('C12', '1'): 'ECG_LPF_IN', ('C12', '2'): 'VREF',
    ('C13', '1'): 'VCC', ('C13', '2'): 'GND',
    ('C14', '1'): 'PD_ANODE', ('C14', '2'): 'PPG_TIA_OUT',
    ('C15', '1'): 'PPG_TIA_OUT', ('C15', '2'): 'PPG_HPF_OUT',
    ('C16', '1'): 'PPG_LPF_NODE', ('C16', '2'): 'PPG_OUT',
    ('C17', '1'): 'PPG_LPF_IN', ('C17', '2'): 'VREF',
    ('C18', '1'): 'VCC', ('C18', '2'): 'GND',
}

all_nets = set(pad_net_map.values())
for netname in all_nets:
    if not board.FindNet(netname):
        net = pcbnew.NETINFO_ITEM(board, netname)
        board.Add(net)

assigned = 0
for (ref, pin), netname in pad_net_map.items():
    fp = board.FindFootprintByReference(ref)
    if not fp:
        print(f"Warning: fp {ref} not found!")
        continue
    pad = fp.FindPadByNumber(pin)
    if not pad:
        print(f"Warning: pad {ref}.{pin} not found!")
        continue
    pad.SetNet(board.FindNet(netname))
    assigned += 1

for i in range(1, 5):
    h = board.FindFootprintByReference(f'H{i}')
    if h:
        p = h.FindPadByNumber('1')
        if p: p.SetNet(board.FindNet('GND'))

pcbnew.SaveBoard('DoAn/ECG_PPG_System/ECG_PPG_System.kicad_pcb', board)
print(f"Assigned nets to {assigned} pads successfully!")
