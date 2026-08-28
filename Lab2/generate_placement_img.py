import re
import subprocess
import fitz
from PIL import Image

def process():
    sch_path = r'C:\HK3-25-26\KhoaHe_PCB\Lab2\Project_KiCad\Lab_2.kicad_sch'
    with open(sch_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Filter out wire and junction blocks
    out_lines = []
    skip = False
    brace_depth = 0
    for line in lines:
        stripped = line.strip()
        if (stripped.startswith('(wire') or stripped.startswith('(junction')) and not skip:
            skip = True
            brace_depth = line.count('(') - line.count(')')
            continue
        if skip:
            brace_depth += line.count('(') - line.count(')')
            if brace_depth <= 0:
                skip = False
            continue
        out_lines.append(line)
        
    placement_sch = r'C:\HK3-25-26\KhoaHe_PCB\Lab2\Project_KiCad\Lab_2_placement.kicad_sch'
    with open(placement_sch, 'w', encoding='utf-8') as f:
        f.writelines(out_lines)
    print("Placement sch created")

    # Export to pdf via kicad-cli
    kicad_cli = r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe"
    pdf_out = r"C:\HK3-25-26\KhoaHe_PCB\Lab2\Pic\Lab_2_placement.pdf"
    cmd = [kicad_cli, "sch", "export", "pdf", "-o", pdf_out, placement_sch]
    subprocess.run(cmd, check=True)
    print("PDF exported")

    # Convert to image
    doc = fitz.open(pdf_out)
    pix = doc[0].get_pixmap(dpi=300)
    img_path = r"C:\HK3-25-26\KhoaHe_PCB\Lab2\Pic\Lab_2_placement_full.png"
    pix.save(img_path)
    print("PNG saved")

    # Crop
    img = Image.open(img_path).convert('RGB')
    crop_box = (500, 750, 2900, 2150)
    cropped = img.crop(crop_box)
    cropped.save(r"C:\HK3-25-26\KhoaHe_PCB\Lab2\Pic\components_placement_clean.png")
    print("Cropped clean components placement image saved!")

if __name__ == '__main__':
    process()
