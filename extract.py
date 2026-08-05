import re
import html

with open('extracted/word/document.xml', encoding='utf-8') as f:
    content = f.read()

# Split into paragraphs
paras = re.findall(r'<w:p[ >].*?</w:p>', content, re.DOTALL)
out_lines = []
for p in paras:
    texts = re.findall(r'<w:t[^>]*>(.*?)</w:t>', p, re.DOTALL)
    line = ''.join(html.unescape(t) for t in texts)
    out_lines.append(line)

with open('uok_content.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out_lines))

print(f'{len(out_lines)} paragraphs written')
