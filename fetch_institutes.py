import urllib.request
import re
import os
import html as htmlmod

BASE = "https://uok.edu.pk/research_institutes"

institutes = {
    "cdfst": "/cdfst/index.php",
    "asce": "/asce/index.php",
    "cmg": "/cmg/index.php",
    "cews": "/cews/index.php",
    "chwb": "/chwb/index.php",
    "confucius": "/confucius/index.php",
    "kibge": "/kibge/index.php",
    "ies": "/ies/index.php",
    "ims": "/ims/index.php",
    "isst": "/isst/index.php",
    "nnrc": "/nnrc/index.php",
    "psc": "/psc/index.php",
    "smbbc": "/smbbc/index.php",
    "sympdc": "/sympdc/index.php",
}

RAW_DIR = "inst_pages_raw"
TEXT_DIR = "inst_pages_text"
os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(TEXT_DIR, exist_ok=True)

def strip_html(raw):
    raw = re.sub(r'<script.*?</script>', '', raw, flags=re.DOTALL|re.IGNORECASE)
    raw = re.sub(r'<style.*?</style>', '', raw, flags=re.DOTALL|re.IGNORECASE)
    raw = re.sub(r'<!--.*?-->', '', raw, flags=re.DOTALL)
    raw = re.sub(r'<(br|/p|/div|/li|/tr|/h[1-6])\s*/?>', '\n', raw, flags=re.IGNORECASE)
    text = re.sub(r'<[^>]+>', ' ', raw)
    text = htmlmod.unescape(text)
    lines = [re.sub(r'[ \t]+', ' ', l).strip() for l in text.split('\n')]
    lines = [l for l in lines if l]
    return '\n'.join(lines)

results = {}
for name, path in institutes.items():
    url = BASE + path
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=20) as resp:
            raw = resp.read().decode('utf-8', errors='ignore')
        with open(f'{RAW_DIR}/{name}.html', 'w', encoding='utf-8') as f:
            f.write(raw)
        text = strip_html(raw)
        with open(f'{TEXT_DIR}/{name}.txt', 'w', encoding='utf-8') as f:
            f.write(f"URL: {url}\n\n{text}")
        results[name] = f"OK ({len(text)} chars)"
    except Exception as e:
        results[name] = f"ERROR: {e}"

for k, v in results.items():
    print(f"{k}: {v}")
