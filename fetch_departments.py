import urllib.request
import re
import os
import html as htmlmod

BASE = "https://uok.edu.pk"

departments = {
    "agriculture": "/faculties/agriculture/index.php",
    "appliedchemistry": "/faculties/appliedchemistry/index.php",
    "appliedphysics": "/faculties/appliedphysics/index.php",
    "arabic": "/faculties/arabic/index.php",
    "bengali": "/faculties/bengali/index.php",
    "biochemistry": "/faculties/biochemistry/index.php",
    "biotechnology": "/faculties/biotechnology/index.php",
    "botany": "/faculties/botany/index.php",
    "businessadministration": "/faculties/businessadministration/index.php",
    "chemicalengineering": "/faculties/chemicalengineering/index.php",
    "chemistry": "/faculties/chemistry/index.php",
    "commerce": "/faculties/commerce/index.php",
    "criminology": "/faculties/criminology/index.php",
    "economics": "/faculties/economics/index.php",
    "education": "/faculties/education/index.php",
    "english": "/faculties/english/index.php",
    "foodscience": "/faculties/foodscience/index.php",
    "genetics": "/faculties/genetics/index.php",
    "geography": "/faculties/geography/index.php",
    "geology": "/faculties/geology/index.php",
    "healthphysical": "/faculties/healthphysical/index.php",
    "generalhistory": "/faculties/generalhistory/index.php",
    "internationalrelations": "/faculties/internationalrelations/index.php",
    "islamichistory": "/faculties/islamichistory/index.php",
    "islamiclearning": "/faculties/islamiclearning/index.php",
    "libraryinformationsciences": "/faculties/libraryinformationsciences/index.php",
    "masscommunication": "/faculties/masscommunication/index.php",
    "mathematics": "/faculties/mathematics/index.php",
    "microbiology": "/faculties/microbiology/index.php",
    "persian": "/faculties/persian/index.php",
    "petroleumtechnology": "/faculties/petroleumtechnology/index.php",
    "pharmaceuticalchemistry": "/faculties/pharmaceuticalchemistry/index.php",
    "pharmaceutics": "/faculties/pharmaceutics/index.php",
    "pharmacognosy": "/faculties/pharmacognosy/index.php",
    "pharmacology": "/faculties/pharmacology/index.php",
    "pharmacy": "/faculties/pharmacy/index.php",
    "pharmacypractice": "/faculties/pharmacypractice/index.php",
    "philosophy": "/faculties/philosophy/index.php",
    "physics": "/faculties/physics/index.php",
    "physiology": "/faculties/physiology/index.php",
    "politicalscience": "/faculties/politicalscience/index.php",
    "psychology": "/faculties/psychology/index.php",
    "publicadministration": "/faculties/publicadministration/index.php",
    "quranwasunnah": "/faculties/quranwasunnah/index.php",
    "researchfacility": "/faculties/researchfacility/index.php",
    "law": "/faculties/law/index.php",
    "shahlatifchair": "/faculties/shahlatifchair/index.php",
    "sindhi": "/faculties/sindhi/index.php",
    "socialwork": "/faculties/socialwork/index.php",
    "sociology": "/faculties/sociology/index.php",
    "specialeducation": "/faculties/specialeducation/index.php",
    "statistics": "/faculties/statistics/index.php",
    "teachereducation": "/faculties/teachereducation/index.php",
    "urdu": "/faculties/urdu/index.php",
    "usooluddin": "/faculties/usooluddin/index.php",
    "visualstudies": "/faculties/visualstudies/index.php",
    "zoology": "/faculties/zoology/index.php",
}

RAW_DIR = "dept_pages_raw"
TEXT_DIR = "dept_pages_text"

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
for name, path in departments.items():
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
print(f"\nDone: {len(results)} pages, {sum(1 for v in results.values() if v.startswith('OK'))} OK")
