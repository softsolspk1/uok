# Source Material for UoK Website Revamp

Gathered from the live site (https://uok.edu.pk/) and `uok.docx` on 2026-08-05.

## 1. Research brief (`uok.docx` → `uok_content.txt`)
A 24-page consultancy-style "Digital Transformation Blueprint" proposing an enterprise Digital University Platform: unified SSO (KU-ID), digital fee payments, RAG/AI chatbot, research portal integrations (ORCID/Scopus/Crossref), WCAG 2.2 AA accessibility, a proposed "Karachi Design System," a Next.js/Node/Strapi/Keycloak tech stack, and a 4-phase 24-month rollout. It also benchmarks UoK against Harvard, MIT, Stanford, Oxford, NUS, KAUST, LUMS, and NUST. This is aspirational/strategic — not a literal description of the current site.

## 2. Brand assets (`assets/`)
- `logo.png` — official wordmark + crescent/book crest, transparent PNG (239×66)
- `favicon.ico`
- `banner-nab.jpg`, `banner-elib.jpg`, `banner-chem.jpg`, `banner-dpa.jpg`, `banner-fst.jpg`, `banner-ubit.jpg` — real campus/building photos used as homepage slider banners (924×296 native use, higher-res originals)
- `color-scheme.md` — full palette extracted from the live CSS, primary brand green `#447e36`

## 3. Site structure & content (`pages_text/`, `homepage.html`, `sitemap.xml`)
Plain-text extracts of the homepage plus one representative page per major section:
- `about.txt`, `history.txt` — institutional background (est. 1951, 1,279-acre campus)
- `admissions.txt`, `pg_admissions.txt`, `foreign_students.txt` — admissions pathways
- `faculties.txt`, `dept_sample_cs.txt` — 8 faculties / 65 department links (sample: Computer Science / UBIT)
- `library.txt` — Dr. Mahmud Hussain Library + digital library
- `administration.txt`, `vc.php`→`vc.txt`, `registrar.txt` — governance/leadership pages
- `examination.txt`, `semester_fee.txt` — exams & fee voucher process
- `alumni.txt`, `journals.txt`, `research_institutes.txt` — alumni, journals, research centers
- `news.txt`, `downloads.txt`, `policies.txt`, `convocation.txt`, `contacts.txt`, `sitemap_page.txt`

Full navigation tree (all top-nav + dropdown items with URLs) captured in `homepage.html` — used to derive the current information architecture.

`sitemap.xml` (2011-era, 1,345 URLs) kept for reference if a fuller crawl is needed later — many entries are likely stale/dead.

## Not yet pulled (available on request)
The remaining ~1,320 individual department/notice/sub-pages were intentionally skipped per scope decision (core structure + samples, not a full mirror) — real content migration for those would happen via CMS import during actual build-out, not hand-copied text.
