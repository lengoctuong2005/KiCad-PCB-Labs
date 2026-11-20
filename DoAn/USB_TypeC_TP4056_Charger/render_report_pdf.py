import markdown
import sys
import os
from lxml import html as LH
from lxml_html_clean import Cleaner


_CLEAN = Cleaner(scripts=True, javascript=True, comments=True, style=False,
                 links=False, meta=False, page_structure=False,
                 embedded=True, frames=True, forms=True)

def sanitize_html(fragment):
    node = LH.fragment_fromstring(fragment, create_parent='div')
    node = _CLEAN.clean_html(node)
    return (node.text or '') + ''.join(LH.tostring(c, encoding='unicode') for c in node)

def render_md_to_html(md_file, html_file):
    with open(md_file, 'r', encoding='utf-8') as f:
        text = f.read()

    # Bỏ YAML frontmatter nếu có
    if text.startswith('---'):
        parts = text.split('---', 2)
        if len(parts) >= 3:
            text = parts[2].strip()

    # Tách phần <style>...</style> nếu có ở đầu
    style_content = ""
    body_content = text
    if '<style>' in text and '</style>' in text:
        s_start = text.find('<style>')
        s_end = text.find('</style>') + len('</style>')
        style_content = text[s_start:s_end]
        body_content = text[:s_start] + text[s_end:]

    html = markdown.markdown(body_content.strip(), extensions=['tables', 'fenced_code'])
    html = sanitize_html(html)

    full_html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<title>Báo cáo Đồ Án Cuối Kỳ - USB-C TP4056 Charger</title>
{style_content}
</head>
<body>
{html}
</body>
</html>"""

    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(full_html)
    print(f"Generated {html_file}")

if __name__ == '__main__':
    md_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), 'BaoCao_DoAn.md')
    html_path = md_path.replace('.md', '.html')
    render_md_to_html(md_path, html_path)
