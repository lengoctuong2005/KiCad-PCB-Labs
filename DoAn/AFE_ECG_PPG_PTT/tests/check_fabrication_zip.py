import sys
import zipfile
from pathlib import Path

project = Path(__file__).resolve().parents[1]
folder = project / 'outputs/print_preflight_20261114'
archive = Path(sys.argv[1]) if len(sys.argv) > 1 else folder / 'GERBER_ONLY_92x70_NOT_CAM_APPROVED.zip'
gerbers = Path(sys.argv[2]) if len(sys.argv) > 2 else archive.parent / 'gerbers'
prefix = 'AFE_ECG_PPG_PTT-'
expected = {prefix + name for name in ['F_Cu.gtl', 'B_Cu.gbl', 'F_Mask.gts', 'B_Mask.gbs', 'F_Silkscreen.gto', 'B_Silkscreen.gbo', 'F_Paste.gtp', 'B_Paste.gbp', 'Edge_Cuts.gm1', 'PTH.drl', 'NPTH.drl']}
with zipfile.ZipFile(archive) as source:
    names = source.namelist()
    assert len(names) == len(expected) and set(names) == expected, names
    assert source.testzip() is None
    for name in names:
        assert source.read(name) == (gerbers / name).read_bytes(), name
print('PASS: 11 flat Gerber/drill members, CRC and exact source bytes')
