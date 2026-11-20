#!/usr/bin/env python3
import argparse
import os
import xml.etree.ElementTree as ET
import pcbnew

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AFE_PRETTY = os.path.join(PROJECT_DIR, "libs", "afe.pretty")
SYS_FP = "/usr/share/kicad/footprints"

PLACEMENTS = {
    "H1": (5.0, 5.0, 0),
    "H2": (62.0, 6.0, 0),
    "H3": (5.0, 75.0, 0),
    "H4": (95.0, 75.0, 0),
    "J1": (12.0, 20.0, 0),
    "J2": (71.0, 16.0, 0),
    "J3": (58.0, 16.0, 0),
    "R1": (32, 35, 0),
    "R2": (32, 39, 0),
    "R3": (25, 30, 0),
    "R4": (26, 16, 0),
    "R5": (26, 21, 0),
    "U1": (38.0, 36.0, 0),
    "C1": (32, 31, 0),
    "R6": (32, 27, 0),
    "R8": (37, 27, 0),
    "R18": (33, 45, 0),
    "C2": (37, 45, 0),
    "C3": (28, 43, 0),
    "C7": (47, 40, 0),
    "R9": (40, 29, 0),
    "R10": (44, 29, 0),
    "C8": (58.5, 45.5, 0),
    "C9": (22, 64, 0),
    "R11": (36.0, 50.0, 0),
    "R12": (41.0, 50.0, 0),
    "C5": (36.0, 55.0, 0),
    "C6": (41.0, 55.0, 0),
    "R13": (35, 41, 0),
    "R14": (39, 41, 0),
    "R15": (46.0, 44.0, 0),
    "U3": (18.0, 64.0, 0),
    "C10": (13.0, 64.0, 0),
    "C11": (43, 33, 0),
    "U2": (53.0, 44.0, 0),
    "C4": (39, 32, 0),
    "R19": (53.0, 51.0, 0),
    "R16": (58.0, 38.0, 0),
    "R17": (58.0, 42.0, 0),
    "TP1": (47.0, 48.0, 0),
    "TP2": (47.0, 52.0, 0),
    "TP3": (44.0, 36.0, 0),
    "TP4": (44.0, 40.0, 0),
    "TP5": (23.0, 58.0, 0),
    "TP6": (18.0, 58.0, 0),
    "TP7": (13.0, 58.0, 0),
}


def fail(msg):
    raise SystemExit(msg)


def mm(v):
    return pcbnew.FromMM(v)


def get_footprint(fp_str):
    lib, name = fp_str.split(":", 1)
    base = AFE_PRETTY if lib == "afe" else os.path.join(SYS_FP, f"{lib}.pretty")
    fp = pcbnew.FootprintLoad(base, name)
    if fp is None:
        fail(f"Could not load footprint: {fp_str} from {base}")
    return fp, lib, name


def parse_netlist(path):
    tree = ET.parse(path)
    root = tree.getroot()
    design = root.find("design")
    sheet = design.find("sheet") if design is not None else None
    title = "AFE ECG + PPG PTT"
    company = "KhoaHe PCB"
    rev = "v1.0"
    date = "2026-11-12"
    if sheet is not None:
        tb = sheet.find("title_block")
        if tb is not None:
            title = tb.findtext("title") or title
            company = tb.findtext("company") or company
            rev = tb.findtext("rev") or rev
            date = tb.findtext("date") or date

    components = {}
    for comp in root.findall("./components/comp"):
        ref = comp.attrib.get("ref")
        footprint = comp.findtext("footprint") or ""
        if not ref or ref in components or ":" not in footprint:
            fail(f"Invalid component identity or footprint: {ref} {footprint}")
        if not (comp.findtext("tstamps") or "").strip():
            fail(f"Missing schematic symbol identity: {ref}")
        components[ref] = {
            "ref": ref,
            "value": comp.findtext("value") or "",
            "footprint": footprint,
            "tstamp": (comp.findtext("tstamps") or "").strip(),
        }

    nets = {}
    nodes = {}
    for net in root.findall("./nets/net"):
        name = net.attrib.get("name")
        if not name or name in nets:
            fail(f"Invalid or duplicate net: {name}")
        nets[name] = net
        for node in net.findall("node"):
            nref = node.attrib.get("ref")
            pin = node.attrib.get("pin")
            if nref not in components or not pin or (nref, pin) in nodes:
                fail(f"Invalid or duplicate node: {nref}.{pin}")
            nodes[(nref, pin)] = name
    if not components or not nets:
        fail("Empty component or net inventory")

    return {"title": title, "company": company, "rev": rev, "date": date, "components": components, "nets": nets, "nodes": nodes}


def build_board(data, export_dsn_path=None):
    board = pcbnew.BOARD()
    tb = board.GetTitleBlock()
    tb.SetTitle(data["title"])
    tb.SetCompany(data["company"])
    tb.SetRevision(data["rev"])
    tb.SetDate(data["date"])
    board.SetTitleBlock(tb)

    ds = board.GetDesignSettings()
    ds.m_TrackMinWidth = mm(0.2)
    ds.m_ViasMinSize = mm(0.6)
    ds.m_MinThroughDrill = mm(0.3)
    ds.m_CopperEdgeClearance = mm(0.5)
    ds.m_SolderMaskMargin = 0
    ds.m_SolderMaskMinWidth = 0

    edge = pcbnew.PCB_SHAPE(board)
    edge.SetShape(pcbnew.SHAPE_T_RECT)
    edge.SetStart(pcbnew.VECTOR2I(mm(0), mm(0)))
    edge.SetEnd(pcbnew.VECTOR2I(mm(100), mm(80)))
    edge.SetLayer(pcbnew.Edge_Cuts)
    edge.SetWidth(mm(0.1))
    board.Add(edge)

    for netname in sorted(data["nets"].keys()):
        board.Add(pcbnew.NETINFO_ITEM(board, netname))

    for ref in sorted(data["components"]):
        comp = data["components"][ref]
        fp, lib, name = get_footprint(comp["footprint"])
        fp.SetFPID(pcbnew.LIB_ID(lib, name))
        fp.SetReference(ref)
        fp.SetValue(comp["value"])
        if comp["tstamp"]:
            fp.SetPath(pcbnew.KIID_PATH(f"/{comp['tstamp']}"))
        fp.SetAttributes(fp.GetAttributes() & ~pcbnew.FP_EXCLUDE_FROM_BOM)

        ref_field = fp.Reference()
        ref_field.SetVisible(True)
        ref_field.SetTextSize(pcbnew.VECTOR2I(mm(0.8), mm(0.8)))
        ref_field.SetTextThickness(mm(0.12))

        val_field = fp.Value()
        val_field.SetVisible(False)

        for f in fp.GetFields():
            if f.GetName() not in ("Reference", "Value"):
                f.SetVisible(False)

        if ref not in PLACEMENTS:
            fail(f"Missing placement coordinates for {ref}")
        x, y, rot = PLACEMENTS[ref]
        fp.SetPosition(pcbnew.VECTOR2I(mm(x), mm(y)))
        fp.SetOrientation(pcbnew.EDA_ANGLE(rot, pcbnew.DEGREES_T))
        if ref == "U1":
            fp.Reference().SetPosition(pcbnew.VECTOR2I(mm(36), mm(32.5)))

        board.Add(fp)

        pad_names = {pad.GetNumber() for pad in fp.Pads()}
        missing_pins = {pin for component, pin in data["nodes"] if component == ref} - pad_names
        if missing_pins:
            fail(f"{ref}: missing footprint pads {sorted(missing_pins)}")
        for pad in fp.Pads():
            netname = data["nodes"].get((ref, pad.GetNumber()))
            if netname:
                pad.SetNet(board.FindNet(netname))

    for layer in (pcbnew.F_Cu, pcbnew.B_Cu):
        zone = pcbnew.ZONE(board)
        zone.SetLayer(layer)
        zone.SetIsRuleArea(True)
        zone.SetDoNotAllowZoneFills(True)
        zone.SetDoNotAllowTracks(True)
        zone.SetDoNotAllowVias(True)
        zone.SetDoNotAllowPads(True)
        zone.SetDoNotAllowFootprints(True)
        zone.SetZoneName("ANTENNA_KEEPOUT")
        outline = zone.Outline()
        outline.NewOutline()
        for x, y in [(68, 0), (100, 0), (100, 12), (68, 12)]:
            outline.Append(pcbnew.VECTOR2I(mm(x), mm(y)))
        board.Add(zone)

    if export_dsn_path:
        ok = pcbnew.ExportSpecctraDSN(board, export_dsn_path)
        if not ok:
            fail(f"ExportSpecctraDSN failed: {export_dsn_path}")

    return board


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("netlist_path")
    ap.add_argument("output_board_path")
    ap.add_argument("--export-dsn")
    ap.add_argument("--overwrite", action="store_true")
    args = ap.parse_args()

    if not os.path.isfile(args.netlist_path):
        fail(f"Netlist not found: {args.netlist_path}")
    if os.path.exists(args.output_board_path) and not args.overwrite:
        fail(f"Output exists, use --overwrite: {args.output_board_path}")

    for output in (args.output_board_path, args.export_dsn):
        if output and os.path.exists(output) and not args.overwrite:
            fail(f"Output exists, use --overwrite: {output}")
        if output and not os.path.isdir(os.path.dirname(os.path.abspath(output))):
            fail(f"Output directory does not exist: {output}")
    data = parse_netlist(args.netlist_path)
    board = build_board(data, export_dsn_path=args.export_dsn)
    ok = board.Save(args.output_board_path)
    if not ok:
        fail(f"Failed to save board: {args.output_board_path}")
    print(f"WROTE {args.output_board_path}")
    if args.export_dsn:
        print(f"WROTE {args.export_dsn}")


if __name__ == "__main__":
    main()
