import pcbnew, math, uuid

def mm(v): return int(round(v * 1e6))

board = pcbnew.BOARD()

# Set design settings
ds = board.GetDesignSettings()
ds.m_TrackMinWidth = mm(0.20)
ds.m_ViasMinSize = mm(0.60)
ds.m_ViasMinDrill = mm(0.30)

# Board outline: 50.0 x 30.0 mm
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

print(f"Created {len(nets)} nets!")
