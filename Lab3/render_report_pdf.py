import markdown
import sys
import os

def render_md_to_html(md_file, html_file):
    with open(md_file, 'r', encoding='utf-8') as f:
        text = f.read()

    # Bỏ YAML frontmatter nếu có
    if text.startswith('---'):
        parts = text.split('---', 2)
        if len(parts) >= 3:
            text = parts[2]

    html = markdown.markdown(text, extensions=['tables', 'fenced_code'])

    # Wrap in basic html
    full_html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<title>Báo cáo Lab</title>
</head>
<body>
{html}
</body>
</html>"""

    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(full_html)
    print(f"Generated {html_file}")

if __name__ == '__main__':
    md_path = sys.argv[1]
    html_path = md_path.replace('.md', '.html')
    render_md_to_html(md_path, html_path)
