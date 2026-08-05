import re, base64, urllib.request

with open('fonts.css', encoding='utf-8') as f:
    css = f.read()
with open('fraunces_fixed.css', encoding='utf-8') as f:
    css += '\n' + f.read()

blocks = re.findall(r'/\*\s*([\w-]+)\s*\*/\s*(@font-face\s*\{[^}]*\})', css)

# Pick only the "latin" (default arabic for urdu font) subset per family/weight/style
wanted = {
    ('Fraunces', 'italic', '500'): 'latin',
    ('Fraunces', 'normal', '700'): 'latin',
    ('Work Sans', 'normal', '400'): 'latin',
    ('Work Sans', 'normal', '500'): 'latin',
    ('Work Sans', 'normal', '600'): 'latin',
    ('Work Sans', 'normal', '700'): 'latin',
    ('Noto Nastaliq Urdu', 'normal', '700'): 'arabic',
}

out_faces = []
picked = set()
for subset, block in blocks:
    fam = re.search(r"font-family:\s*'([^']+)'", block).group(1)
    style = re.search(r"font-style:\s*(\w+)", block).group(1)
    weight = re.search(r"font-weight:\s*(\d+)", block).group(1)
    key = (fam, style, weight)
    if key in wanted and wanted[key] == subset and key not in picked:
        url = re.search(r"url\((https://[^)]+)\)", block).group(1)
        print(f"Downloading {fam} {style} {weight} [{subset}] ...")
        req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'})
        data = urllib.request.urlopen(req, timeout=30).read()
        b64 = base64.b64encode(data).decode('ascii')
        out_faces.append(f"""@font-face {{
  font-family: '{fam}';
  font-style: {style};
  font-weight: {weight};
  font-display: swap;
  src: url(data:font/woff2;base64,{b64}) format('woff2');
}}""")
        picked.add(key)
        print(f"  -> {len(data)} bytes, base64 {len(b64)} chars")

print(f"\nTotal faces embedded: {len(picked)} / {len(wanted)}")
missing = set(wanted) - picked
if missing:
    print("MISSING:", missing)

with open('embedded-fonts.css', 'w', encoding='utf-8') as f:
    f.write('\n\n'.join(out_faces))

total_size = sum(len(x) for x in out_faces)
print(f"embedded-fonts.css size: {total_size/1024:.1f} KB")
