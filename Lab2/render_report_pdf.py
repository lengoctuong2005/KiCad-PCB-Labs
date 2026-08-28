import markdown
import weasyprint
import os

def build_pdf():
    md_file = r"C:\HK3-25-26\KhoaHe_PCB\Lab2\BaoCao_Lab02.md"
    pdf_out = r"C:\HK3-25-26\KhoaHe_PCB\Lab2\BaoCao_Lab02_KiCad.pdf"
    
    with open(md_file, "r", encoding="utf-8") as f:
        md_text = f.read()

    # Convert markdown to html with tables and extra extensions
    html_body = markdown.markdown(md_text, extensions=['tables', 'fenced_code', 'nl2br'])

    full_html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<title>Báo cáo Lab 02 - KiCad</title>
<style>
@page {{
    size: A4 portrait;
    margin: 15mm 18mm 18mm 18mm;
    @bottom-right {{
        content: "Trang " counter(page);
        font-family: 'Times New Roman', serif;
        font-size: 10pt;
        color: #555;
    }}
    @bottom-left {{
        content: "Báo cáo Thực hành Thiết kế Mạch in PCB - Lab 02";
        font-family: 'Times New Roman', serif;
        font-size: 10pt;
        color: #555;
    }}
}}

@page:first {{
    margin: 15mm 18mm 18mm 18mm;
    @bottom-right {{ content: none; }}
    @bottom-left {{ content: none; }}
}}

* {{
    box-sizing: border-box;
}}

body {{
    font-family: 'Times New Roman', 'Liberation Serif', serif;
    font-size: 11.5pt;
    line-height: 1.45;
    color: #1a1a1a;
    margin: 0;
    padding: 0;
    background-color: #fff;
}}

/* COVER PAGE FULL A4 (CHUẨN LAB 5) */
.cover-page {{
    border: 3px double #1e3a8a;
    border-radius: 8px;
    padding: 35px 25px;
    margin: 0;
    min-height: 258mm;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    text-align: center;
    background-color: #ffffff;
    page-break-after: always !important;
    break-after: page !important;
}}

.cover-header {{
    margin-top: 10px;
}}

.uni-name {{
    font-size: 13pt;
    font-weight: bold;
    color: #1e3a8a;
    line-height: 1.35;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}

.dept-divider {{
    width: 140px;
    height: 1.5px;
    background-color: #1e3a8a;
    margin: 10px auto 0 auto;
}}

.cover-body {{
    margin: 30px 0;
}}

.report-badge {{
    display: inline-block;
    font-size: 12pt;
    font-weight: bold;
    color: #1e3a8a;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 12px;
    border-bottom: 2px solid #b91c1c;
    padding-bottom: 4px;
}}

.report-title {{
    font-size: 18pt;
    font-weight: bold;
    color: #b91c1c;
    line-height: 1.35;
    margin: 12px 0 16px 0;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}}

.lab-name {{
    font-size: 13.5pt;
    font-weight: bold;
    color: #0f172a;
    line-height: 1.4;
    max-width: 90%;
    margin: 0 auto;
}}

.cover-student {{
    margin: 20px auto 10px auto;
    width: 88%;
    background-color: #f8fafc;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 16px 20px;
    text-align: left;
}}

.student-info {{
    width: 100%;
    border-collapse: collapse;
    font-size: 12pt;
    margin: 0;
}}

.student-info td {{
    padding: 5px 8px;
    border: none;
    color: #111;
    line-height: 1.4;
}}

.student-info td:first-child {{
    width: 28%;
    white-space: nowrap;
    color: #1e3a8a;
    font-weight: bold;
}}

.cover-footer {{
    margin-bottom: 10px;
    font-size: 11.5pt;
    font-weight: bold;
    color: #334155;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}

/* MAIN CONTENT STYLING (PAGE 2 ONWARD) */
h2:first-of-type {{
    page-break-before: always;
    break-before: page;
}}

h2 {{
    font-size: 13pt;
    color: #1e3a8a;
    border-bottom: 1.5px solid #1e3a8a;
    padding-bottom: 3px;
    margin-top: 20px;
    margin-bottom: 10px;
    text-transform: uppercase;
    page-break-after: avoid;
    break-after: avoid;
}}

h3 {{
    font-size: 11.5pt;
    color: #0f172a;
    margin-top: 14px;
    margin-bottom: 6px;
    page-break-after: avoid;
    break-after: avoid;
}}

h4 {{
    font-size: 11pt;
    color: #1e293b;
    margin-top: 12px;
    margin-bottom: 4px;
    page-break-after: avoid;
    break-after: avoid;
}}

p {{
    margin-top: 4px;
    margin-bottom: 8px;
    text-align: justify;
}}

ul, ol {{
    margin-top: 4px;
    margin-bottom: 8px;
    padding-left: 22px;
}}

li {{
    margin-bottom: 4px;
    text-align: justify;
}}

code {{
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 9.5pt;
    background-color: #f1f5f9;
    color: #0f172a;
    padding: 1px 3px;
    border-radius: 3px;
    border: 1px solid #e2e8f0;
}}

table {{
    width: 100%;
    border-collapse: collapse;
    margin: 12px 0;
    font-size: 9.5pt;
    table-layout: fixed;
    page-break-inside: auto;
}}

tr {{
    page-break-inside: avoid;
    page-break-after: auto;
}}

th, td {{
    border: 1px solid #334155;
    padding: 6px 7px;
    line-height: 1.35;
    word-wrap: break-word;
    word-break: break-word;
    overflow-wrap: break-word;
}}

th {{
    background-color: #1e3a8a;
    color: #ffffff;
    font-weight: bold;
    text-align: center;
}}

tbody tr:nth-child(even) {{
    background-color: #f8fafc;
}}

.figure-container {{
    text-align: center;
    margin: 14px 0;
    page-break-inside: avoid;
}}

.report-img {{
    max-width: 95%;
    height: auto;
    border: 1px solid #cbd5e1;
    border-radius: 4px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
}}

.figure-caption {{
    font-size: 10.5pt;
    font-style: italic;
    color: #334155;
    margin-top: 6px;
}}

hr {{
    border: none;
    border-top: 1px solid #cbd5e1;
    margin: 16px 0;
}}

pre {{
    background-color: #f8fafc;
    border: 1px solid #cbd5e1;
    border-radius: 4px;
    padding: 10px;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 8.5pt;
    line-height: 1.25;
    overflow-x: auto;
    page-break-inside: avoid;
}}
</style>
</head>
<body>
{html_body}
</body>
</html>
"""
    # Write intermediate html
    html_path = r"C:\HK3-25-26\KhoaHe_PCB\Lab2\BaoCao_Lab02.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(full_html)

    # Render to PDF using WeasyPrint
    base_url = r"C:\HK3-25-26\KhoaHe_PCB\Lab2"
    weasyprint.HTML(string=full_html, base_url=base_url).write_pdf(pdf_out)
    print("Successfully generated PDF at:", pdf_out)

if __name__ == "__main__":
    build_pdf()
