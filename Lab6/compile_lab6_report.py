#!/usr/bin/env python3
import os
import sys
import markdown
import subprocess

lab_dir = "/mnt/Windows/HK3-25-26/KhoaHe_PCB/Lab6"
md_path = os.path.join(lab_dir, "BaoCao_Lab06.md")
html_path = os.path.join(lab_dir, "BaoCao_Lab06.html")
pdf_path = os.path.join(lab_dir, "BaoCao_Lab06_KiCad.pdf")

with open(md_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Strip frontmatter
if text.startswith('---'):
    parts = text.split('---', 2)
    if len(parts) >= 3:
        text = parts[2]

html_body = markdown.markdown(text, extensions=['tables', 'fenced_code'])

full_html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<title>Báo cáo Lab 06 - KiCad Routing</title>
</head>
<body>
{html_body}
</body>
</html>"""

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(full_html)
print(f"Generated {html_path}")

# Run puppeteer or chrome to print pdf
js_script = f"""
const path = require('path');
const puppeteer = require('/mnt/Windows/HK3-25-26/KhoaHe_PCB/Lab3/node_modules/puppeteer');

(async () => {{
  const browser = await puppeteer.launch({{
    executablePath: '/usr/bin/google-chrome',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  }});
  const page = await browser.newPage();
  const fileUrl = 'file://' + path.resolve('{html_path}');
  await page.goto(fileUrl, {{ waitUntil: 'networkidle0' }});
  await page.pdf({{
    path: path.resolve('{pdf_path}'),
    format: 'A4',
    printBackground: true,
    margin: {{ top: '0', bottom: '0', left: '0', right: '0' }}
  }});
  await browser.close();
  console.log("Generated {pdf_path}");
}})();
"""

temp_js = os.path.join(lab_dir, "temp_print.js")
with open(temp_js, 'w', encoding='utf-8') as f:
    f.write(js_script)

res = subprocess.run(["node", temp_js], capture_output=True, text=True)
print("Node output:", res.stdout)
if res.stderr:
    print("Node error:", res.stderr)

if os.path.exists(temp_js):
    os.remove(temp_js)

if os.path.exists(pdf_path):
    print("SUCCESS: PDF compiled successfully:", pdf_path)
else:
    print("ERROR: PDF was not generated.")
