import pcbnew as p

path = '/home/tuong/HK3_Semester/KhoaHe_PCB/DoAn/AFE_ECG_PPG_PTT/outputs/narrow_20261113/AFE_ECG_PPG_PTT.kicad_pcb'
board = p.LoadBoard(path)
changes = {
    ('SCL', (59.27, 19.81), (58.0, 18.54)): ((56.27, 19.81), (55.0, 18.54)),
    ('SCL', (95.13, 19.81), (59.27, 19.81)): ((87.13, 19.81), (56.27, 19.81)),
    ('SCL', (96.4, 21.08), (95.13, 19.81)): ((88.4, 21.08), (87.13, 19.81)),
    ('SDA', (59.27, 22.35), (58.0, 21.08)): ((56.27, 22.35), (55.0, 21.08)),
    ('SDA', (90.05, 22.35), (59.27, 22.35)): ((82.05, 22.35), (56.27, 22.35)),
    ('SDA', (96.4, 28.7), (90.05, 22.35)): ((88.4, 28.7), (82.05, 22.35)),
}
for track in board.GetTracks():
    if track.GetClass() != 'PCB_TRACK' or track.GetLayer() != p.F_Cu:
        continue
    start, end = track.GetStart(), track.GetEnd()
    key = (track.GetNetname(), (round(p.ToMM(start.x), 2), round(p.ToMM(start.y), 2)), (round(p.ToMM(end.x), 2), round(p.ToMM(end.y), 2)))
    if key in changes:
        new_start, new_end = changes.pop(key)
        track.SetStart(p.VECTOR2I(p.FromMM(new_start[0]), p.FromMM(new_start[1])))
        track.SetEnd(p.VECTOR2I(p.FromMM(new_end[0]), p.FromMM(new_end[1])))
        print(key, '->', new_start, new_end)
if changes:
    raise RuntimeError(f'Unmatched tracks: {changes}')
p.SaveBoard(path, board)
