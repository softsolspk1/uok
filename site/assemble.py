import json

with open('template.html', encoding='utf-8') as f:
    html = f.read()

with open('../fonts/embedded-fonts.css', encoding='utf-8') as f:
    font_faces = f.read()

with open('../assets/data_uris.json', encoding='utf-8') as f:
    data = json.load(f)

html = html.replace('__FONT_FACES__', font_faces)
html = html.replace('__LOGO__', data['logo'])
html = html.replace('__HERO_UBIT__', data['hero_ubit'])
html = html.replace('__HERO_CHEM__', data['hero_chem'])
html = html.replace('__HERO_DPA__', data['hero_dpa'])

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Assembled index.html: {len(html)/1024:.1f} KB")
