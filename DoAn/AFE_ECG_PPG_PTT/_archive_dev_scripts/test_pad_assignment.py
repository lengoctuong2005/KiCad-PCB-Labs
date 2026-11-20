import pcbnew
from test_netlist_map import NET_MAP

board = pcbnew.BOARD()

# Add nets
for net_name in NET_MAP.keys():
    item = pcbnew.NETINFO_ITEM(board, net_name)
    board.Add(item)

board_nets = board.GetNetsByName()

fps = {}
def load(ref, val, lib, name, x, y, rot=0):
    fp = pcbnew.FootprintLoad(f'/usr/share/kicad/footprints/{lib}.pretty', name)
    assert fp is not None, f'Failed {lib}:{name}'
    fp.SetReference(ref)
    fp.SetValue(val)
    fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y)))
    fp.SetOrientation(pcbnew.EDA_ANGLE(rot, pcbnew.DEGREES_T))
    board.Add(fp)
    fps[ref] = fp
    return fp

# Load all 56 footprints
load('U1', 'AD8232ACPZ', 'Package_CSP', 'LFCSP-20-1EP_4x4mm_P0.5mm_EP2.5x2.5mm', 32, 38)
load('U2', 'ADS1115IDGST', 'Package_SO', 'TSSOP-10_3x3mm_P0.5mm', 48, 38)
load('U3', 'MCP1700-3002E', 'Package_TO_SOT_SMD', 'SOT-23', 24, 64)

load('J1', 'SJ1-3533NG', 'Connector_Audio', 'Jack_3.5mm_CUI_SJ1-3533NG_Horizontal', 10, 20, 180)
load('J1A', 'ECG_PROBES', 'Connector_PinHeader_2.54mm', 'PinHeader_1x03_P2.54mm_Vertical', 12, 36)
load('J2A', 'ESP32_L', 'Connector_PinHeader_2.54mm', 'PinHeader_1x19_P2.54mm_Vertical', 70, 16)
load('J2B', 'ESP32_R', 'Connector_PinHeader_2.54mm', 'PinHeader_1x19_P2.54mm_Vertical', 95.4, 16)
load('J3', 'MAX30102', 'Connector_PinHeader_2.54mm', 'PinHeader_1x07_P2.54mm_Vertical', 60, 16)

for i in range(1, 21):
    load(f'R{i}', f'R{i}', 'Resistor_SMD', 'R_0603_1608Metric', 10 + (i%5)*5, 45 + (i//5)*4)

for i in range(1, 18):
    load(f'C{i}', f'C{i}', 'Capacitor_SMD', 'C_0603_1608Metric', 10 + (i%5)*5, 60 + (i//5)*4)

for i in range(1, 8):
    load(f'TP{i}', f'TP{i}', 'TestPoint', 'TestPoint_Pad_D1.5mm', 35 + (i-1)*5, 72)

for i in range(1, 5):
    load(f'H{i}', 'M3', 'MountingHole', 'MountingHole_3.2mm_M3_Pad', 5 if i in [1,3] else 95, 5 if i in [1,2] else 75)

# Assign pads
missing_pads = []
for net_name, conns in NET_MAP.items():
    net_item = board_nets[net_name]
    for ref, pad_num in conns:
        fp = fps.get(ref)
        if not fp:
            missing_pads.append((ref, pad_num, 'Footprint missing'))
            continue
        pad = fp.FindPadByNumber(pad_num)
        if not pad:
            missing_pads.append((ref, pad_num, 'Pad missing'))
        else:
            pad.SetNet(net_item)

print(f"Assigned {len(NET_MAP)} nets. Missing pads count: {len(missing_pads)}")
if missing_pads:
    for m in missing_pads:
        print("  Missing:", m)
else:
    print("ALL 145 PADS SUCCESSFULLY ASSIGNED TO EXACT NETS!")
