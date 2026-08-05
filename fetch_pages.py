import urllib.request
import re
import os
import html as htmlmod

BASE = "https://uok.edu.pk"

pages = {
    "about": "/welcome-address.php",
    "history": "/our-history.php",
    "admissions": "/admissions/index.php",
    "faculties": "/faculties/index.php",
    "dept_sample_cs": "/faculties/computerscience/index.php",
    "library": "/library/index.php",
    "administration": "/administration/index.php",
    "vc": "/administration/vc.php",
    "registrar": "/administration/registrar.php",
    "examination": "/ann_results/index.php",
    "semester_fee": "/semesterfees/instructions.php",
    "alumni": "/alumni/index.php",
    "journals": "/Journal/index.php",
    "research_institutes": "/research_institutes/index.php",
    "news": "/news.php",
    "contacts": "/contacts.php",
    "sitemap_page": "/sitemap.php",
    "downloads": "/downloads/index.php",
    "policies": "/policies/index.php",
    "convocation": "/conv/index.php",
    "foreign_students": "/fsa/index.php",
    "pg_admissions": "/admissions/pg-index.php",
}

os.makedirs("pages_raw", exist_ok=True)
os.makedirs("pages_text", exist_ok=True)

def strip_html(raw):
    # remove scripts/styles
    raw = re.sub(r'<script.*?</script>', '', raw, flags=re.DOTALL|re.IGNORECASE)
    raw = re.sub(r'<style.*?</style>', '', raw, flags=re.DOTALL|re.IGNORECASE)
    # remove comments
    raw = re.sub(r'<!--.*?-->', '', raw, flags=re.DOTALL)
    # convert block tags to newlines
    raw = re.sub(r'<(br|/p|/div|/li|/tr|/h[1-6])\s*/?>', '\n', raw, flags=re.IGNORECASE)
    # strip remaining tags
    text = re.sub(r'<[^>]+>', ' ', raw)
    text = htmlmod.unescape(text)
    # collapse whitespace
    lines = [re.sub(r'[ \t]+', ' ', l).strip() for l in text.split('\n')]
    lines = [l for l in lines if l]
    return '\n'.join(lines)

results = {}
for name, path in pages.items():
    url = BASE + path
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=20) as resp:
            raw = resp.read().decode('utf-8', errors='ignore')
        with open(f'pages_raw/{name}.html', 'w', encoding='utf-8') as f:
            f.write(raw)
        text = strip_html(raw)
        with open(f'pages_text/{name}.txt', 'w', encoding='utf-8') as f:
            f.write(f"URL: {url}\n\n{text}")
        results[name] = f"OK ({len(text)} chars)"
    except Exception as e:
        results[name] = f"ERROR: {e}"

for k, v in results.items():
    print(f"{k}: {v}")
