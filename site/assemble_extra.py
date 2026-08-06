import json

with open('../fonts/embedded-fonts.css', encoding='utf-8') as f:
    font_faces = f.read()
with open('../assets/data_uris.json', encoding='utf-8') as f:
    data = json.load(f)

jobs = [
    ('prospectus_template.html', 'prospectus.html'),
    ('student_portal_template.html', 'student-portal.html'),
]

for src, dst in jobs:
    with open(src, encoding='utf-8') as f:
        html = f.read()
    html = html.replace('__FONT_FACES__', font_faces).replace('__LOGO__', data['logo'])
    with open(dst, 'w', encoding='utf-8') as f:
        f.write(html)
    remaining = html.count('__')
    print(f"{dst}: {len(html)/1024:.1f} KB, leftover placeholders: {remaining}")
