import pcbnew
import math

def add_track_seg(board, net, layer, width_mm, p1, p2):
    t = pcbnew.PCB_TRACK(board)
    t.SetNet(net)
    t.SetLayer(layer)
    t.SetWidth(pcbnew.FromMM(width_mm))
    t.SetStart(p1)
    t.SetEnd(p2)
    board.Add(t)
    return t

def route_two_points(board, net, layer, width_mm, p1, p2):
    # p1, p2 are VECTOR2I
    x1, y1 = p1.x, p1.y
    x2, y2 = p2.x, p2.y
    if x1 == x2 or y1 == y2:
        add_track_seg(board, net, layer, width_mm, p1, p2)
    else:
        # 45 degree or 90 degree dogleg
        mid = pcbnew.VECTOR2I(x2, y1)
        add_track_seg(board, net, layer, width_mm, p1, mid)
        add_track_seg(board, net, layer, width_mm, mid, p2)

def add_gnd_via(board, gnd_net, pad, dx_mm=0.0, dy_mm=1.0):
    pos = pad.GetPosition()
    via_pos = pcbnew.VECTOR2I(pos.x + pcbnew.FromMM(dx_mm), pos.y + pcbnew.FromMM(dy_mm))
    
    # Via
    v = pcbnew.PCB_VIA(board)
    v.SetNet(gnd_net)
    v.SetPosition(via_pos)
    v.SetWidth(pcbnew.FromMM(0.6))
    v.SetDrill(pcbnew.FromMM(0.3))
    v.SetLayerPair(pcbnew.F_Cu, pcbnew.B_Cu)
    v.SetViaType(pcbnew.VIATYPE_THROUGH)
    board.Add(v)
    
    # Track from pad to via
    add_track_seg(board, gnd_net, pcbnew.F_Cu, 0.254, pos, via_pos)
    return v

print("Router test script ready")
