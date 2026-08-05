import json

with open('../fonts/embedded-fonts.css', encoding='utf-8') as f:
    font_faces = f.read()
with open('../assets/data_uris.json', encoding='utf-8') as f:
    data = json.load(f)

jobs = [
    ('faculties_template.html', 'faculties.html', []),
    ('research_template.html', 'research.html', []),
    ('library_template.html', 'library.html', ['hero_chem']),
    ('administration_template.html', 'administration.html', []),
    ('examinations_template.html', 'examinations.html', []),
    ('alumni_template.html', 'alumni.html', []),
    ('journals_template.html', 'journals.html', []),
    ('contact_template.html', 'contact.html', []),
]

for src, dst, extra_images in jobs:
    with open(src, encoding='utf-8') as f:
        html = f.read()
    html = html.replace('__FONT_FACES__', font_faces)
    html = html.replace('__LOGO__', data['logo'])
    for img_key in extra_images:
        html = html.replace(f'__{img_key.upper()}__', data[img_key])
    with open(dst, 'w', encoding='utf-8') as f:
        f.write(html)
    remaining = html.count('__')
    print(f"{dst}: {len(html)/1024:.1f} KB, leftover placeholders: {remaining}")
