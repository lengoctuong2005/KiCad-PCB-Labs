import pcbnew

board = pcbnew.LoadBoard('/mnt/Windows/HK3-25-26/KhoaHe_PCB/DoAn/USB_TypeC_TP4056_Charger/USB_TypeC_TP4056_Charger.kicad_pcb')

def set_3d_model(fp, model_path, offset=(0,0,0), scale=(1,1,1), rotate=(0,0,0)):
    fp.Models().clear()
    m = pcbnew.FP_3DMODEL()
    m.m_Filename = model_path
    m.m_Offset = pcbnew.VECTOR3D(offset[0], offset[1], offset[2])
    m.m_Scale = pcbnew.VECTOR3D(scale[0], scale[1], scale[2])
    m.m_Rotation = pcbnew.VECTOR3D(rotate[0], rotate[1], rotate[2])
    fp.Models().push_back(m)

for fp in board.GetFootprints():
    ref = fp.GetReferenceAsString()
    if ref == "J1":
        set_3d_model(fp, "/usr/share/kicad/3dmodels/Connector_USB.3dshapes/USB_C_Receptacle_GCT_USB4105-xx-A_16P_TopMnt_Horizontal.step", offset=(0, 1.4, 0))
    elif ref == "U1":
        set_3d_model(fp, "/usr/share/kicad/3dmodels/Package_SO.3dshapes/SOIC-8-1EP_3.9x4.9mm_P1.27mm_EP2.29x3mm.wrl")
    elif ref == "U2":
        set_3d_model(fp, "/usr/share/kicad/3dmodels/Package_TO_SOT_SMD.3dshapes/SOT-23-6.wrl")
    elif ref == "Q1":
        set_3d_model(fp, "/usr/share/kicad/3dmodels/Package_SO.3dshapes/TSSOP-8_4.4x3mm_P0.65mm.wrl")
    elif ref == "J2":
        set_3d_model(fp, "/usr/share/kicad/3dmodels/Connector_JST.3dshapes/JST_PH_B2B-PH-SM4-TB_1x02-1MP_P2.00mm_Vertical.step")

pcbnew.SaveBoard('/mnt/Windows/HK3-25-26/KhoaHe_PCB/DoAn/USB_TypeC_TP4056_Charger/USB_TypeC_TP4056_Charger.kicad_pcb', board)
print("Updated all 3D models!")
