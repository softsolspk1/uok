import re, os, json, glob

TEXT_DIR = '../dept_pages_text'
OUT_DIR = '.'

FACULTY_MAP = {
    'agriculture': 'Science', 'appliedchemistry': 'Science', 'appliedphysics': 'Science',
    'biochemistry': 'Science', 'biotechnology': 'Science', 'botany': 'Science', 'chemistry': 'Science',
    'foodscience': 'Science', 'genetics': 'Science', 'geography': 'Science', 'geology': 'Science',
    'healthphysical': 'Science', 'mathematics': 'Science', 'microbiology': 'Science',
    'petroleumtechnology': 'Science', 'physics': 'Science', 'physiology': 'Science',
    'statistics': 'Science', 'zoology': 'Science',
    'chemicalengineering': 'Engineering',
    'islamiclearning': 'Islamic Studies', 'quranwasunnah': 'Islamic Studies', 'usooluddin': 'Islamic Studies',
    'law': 'Law',
    'businessadministration': 'Management & Administrative Sciences',
    'commerce': 'Management & Administrative Sciences',
    'publicadministration': 'Management & Administrative Sciences',
    'pharmaceuticalchemistry': 'Pharmacy & Pharmaceutical Sciences',
    'pharmaceutics': 'Pharmacy & Pharmaceutical Sciences',
    'pharmacology': 'Pharmacy & Pharmaceutical Sciences',
    'pharmacognosy': 'Pharmacy & Pharmaceutical Sciences',
    'pharmacypractice': 'Pharmacy & Pharmaceutical Sciences',
    'pharmacy': 'Pharmacy & Pharmaceutical Sciences',
    'education': 'Education', 'specialeducation': 'Education', 'teachereducation': 'Education',
    'arabic': 'Arts & Social Sciences', 'bengali': 'Arts & Social Sciences', 'criminology': 'Arts & Social Sciences',
    'economics': 'Arts & Social Sciences', 'english': 'Arts & Social Sciences', 'generalhistory': 'Arts & Social Sciences',
    'internationalrelations': 'Arts & Social Sciences', 'islamichistory': 'Arts & Social Sciences',
    'libraryinformationsciences': 'Arts & Social Sciences', 'masscommunication': 'Arts & Social Sciences',
    'persian': 'Arts & Social Sciences', 'philosophy': 'Arts & Social Sciences', 'politicalscience': 'Arts & Social Sciences',
    'psychology': 'Arts & Social Sciences', 'sindhi': 'Arts & Social Sciences', 'shahlatifchair': 'Arts & Social Sciences',
    'socialwork': 'Arts & Social Sciences', 'sociology': 'Arts & Social Sciences', 'urdu': 'Arts & Social Sciences',
    'visualstudies': 'Arts & Social Sciences', 'researchfacility': 'Arts & Social Sciences',
}

DISPLAY_NAME_OVERRIDES = {
    'generalhistory': 'History', 'islamichistory': 'Islamic History',
    'libraryinformationsciences': 'Library & Information Science',
    'internationalrelations': 'International Relations',
    'healthphysical': 'Health & Physical Education',
    'appliedchemistry': 'Applied Chemistry & Chemical Technology',
    'businessadministration': 'Business Administration',
    'chemicalengineering': 'Chemical Engineering', 'foodscience': 'Food Science & Technology',
    'petroleumtechnology': 'Petroleum Technology', 'publicadministration': 'Public Administration',
    'quranwasunnah': 'Quran wa Sunnah', 'islamiclearning': 'Islamic Learning', 'usooluddin': 'Usool-ud-Din',
    'shahlatifchair': 'Shah Latif Chair', 'specialeducation': 'Special Education',
    'teachereducation': 'Teacher Education', 'socialwork': 'Social Work', 'politicalscience': 'Political Science',
    'visualstudies': 'Visual Studies', 'researchfacility': 'Research Facility Centre',
    'pharmaceuticalchemistry': 'Pharmaceutical Chemistry', 'pharmacypractice': 'Pharmacy Practice',
    'businessadministration': 'Karachi University Business School', 'law': 'School of Law',
    'appliedphysics': 'Applied Physics',
}

def parse_dept(slug, raw_text):
    lines = raw_text.split('\n')

    # Prefer the real department name as printed on the page itself
    real_name = None
    for l in lines[:65]:
        m = re.match(r'^Department of (.+)$', l.strip())
        if m:
            real_name = m.group(1).strip()
            break

    # find last 'Contact' before body (end of dept sub-nav)
    contact_idxs = [i for i, l in enumerate(lines) if l.strip() == 'Contact']
    if not contact_idxs:
        return None
    start = contact_idxs[-1] + 1
    footer_idx = next((i for i in range(start, len(lines)) if lines[i].strip() == 'About Us'), len(lines))
    body_lines = [l.strip() for l in lines[start:footer_idx] if l.strip()]
    if not body_lines:
        return None

    chairman = None
    chair_pattern = re.compile(r'^(Chairman|Chairperson|Chairwoman|Chairperson/Convener|Convener|In-?charge|Head)\s*[:\-]\s*(.+)$', re.IGNORECASE)
    m = chair_pattern.match(body_lines[0])
    if m:
        chairman = m.group(2).strip()
        body_lines = body_lines[1:]

    if not body_lines:
        return None

    # established year
    est_year = None
    joined = ' '.join(body_lines[:3])
    ey = re.search(r'establish\w*\s+(?:in|since|by[^.]*?in)?\s*(?:the year\s*)?(\d{4})', joined, re.IGNORECASE)
    if ey:
        est_year = ey.group(1)

    # Build blocks: treat short lines (<45 chars, no ending period, next line longer) as subheadings
    blocks = []
    i = 0
    while i < len(body_lines):
        line = body_lines[i]
        is_heading = (len(line) < 45 and not line.endswith('.') and not line.endswith(':')
                      and i + 1 < len(body_lines) and len(body_lines[i+1]) > 60)
        if is_heading:
            blocks.append(('h', line))
        else:
            blocks.append(('p', line))
        i += 1

    return {
        'slug': slug, 'chairman': chairman, 'established': est_year, 'blocks': blocks,
        'real_name': real_name,
    }

def title_case_name(slug):
    if slug in DISPLAY_NAME_OVERRIDES:
        return DISPLAY_NAME_OVERRIDES[slug]
    return slug.replace('_', ' ').title()

def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

TEMPLATE = '''<meta charset="utf-8" />
<title>{name} — University of Karachi</title>
<style>
__FONT_FACES__
:root{{--bg:#EDE6D2; --bg-elevated:#F7F3E4; --bg-inverse:#1E4429; --bg-inverse-2:#183A22;
  --text:#1B2A1E; --text-soft:#4B5A45; --text-faint:#5E695A; --text-inverse:#F3EFDD; --text-inverse-soft:#BFD1B9;
  --accent:#3B7331; --accent-hover:#356A2C; --accent-2:#845E2F; --accent-2-soft:#C9A567;
  --border:rgba(27,42,29,.15); --border-inverse:rgba(243,239,221,.16); --focus-ring:#3B7331;--on-accent:#FFFFFF;
  --font-display:'Fraunces',Georgia,'Times New Roman',serif; --font-body:'Work Sans',system-ui,-apple-system,'Segoe UI',sans-serif;
  --font-urdu:'Noto Nastaliq Urdu',serif; --container:1240px; color-scheme: light;}}
@media (prefers-color-scheme: dark){{:root{{--bg:#10160D; --bg-elevated:#1A2416; --bg-inverse:#24361F; --bg-inverse-2:#1B2A17;
  --text:#EDE8D6; --text-soft:#A9B39C; --text-faint:#809079; --text-inverse:#F2EEDC; --text-inverse-soft:#C7D4BE;
  --accent:#72C25A; --accent-hover:#8AD473; --accent-2:#D3A968; --accent-2-soft:#BA955F;
  --border:rgba(237,232,214,.14); --border-inverse:rgba(237,232,214,.14); --focus-ring:#8AD473;--on-accent:#0B1009; color-scheme: dark;}}}}
:root[data-theme="dark"]{{--bg:#10160D; --bg-elevated:#1A2416; --bg-inverse:#24361F; --bg-inverse-2:#1B2A17;
  --text:#EDE8D6; --text-soft:#A9B39C; --text-faint:#809079; --text-inverse:#F2EEDC; --text-inverse-soft:#C7D4BE;
  --accent:#72C25A; --accent-hover:#8AD473; --accent-2:#D3A968; --accent-2-soft:#BA955F;
  --border:rgba(237,232,214,.14); --border-inverse:rgba(237,232,214,.14); --focus-ring:#8AD473;--on-accent:#0B1009; color-scheme: dark;}}
:root[data-theme="light"]{{--bg:#EDE6D2; --bg-elevated:#F7F3E4; --bg-inverse:#1E4429; --bg-inverse-2:#183A22;
  --text:#1B2A1E; --text-soft:#4B5A45; --text-faint:#5E695A; --text-inverse:#F3EFDD; --text-inverse-soft:#BFD1B9;
  --accent:#3B7331; --accent-hover:#356A2C; --accent-2:#845E2F; --accent-2-soft:#C9A567;
  --border:rgba(27,42,29,.15); --border-inverse:rgba(243,239,221,.16); --focus-ring:#3B7331;--on-accent:#FFFFFF; color-scheme: light;}}
*,*::before,*::after{{box-sizing:border-box;}} html{{scroll-behavior:smooth;}}
@media (prefers-reduced-motion: reduce){{html{{scroll-behavior:auto;}}*,*::before,*::after{{animation-duration:.001ms !important;animation-iteration-count:1 !important;transition-duration:.001ms !important;scroll-behavior:auto !important;}}}}
body{{margin:0;background:var(--bg);color:var(--text);font-family:var(--font-body);font-size:17px;line-height:1.65;-webkit-font-smoothing:antialiased;overflow-x:hidden;}}
img{{max-width:100%;display:block;}} a{{color:inherit;}}
h1,h2,h3,h4{{font-family:var(--font-display);font-weight:700;margin:0;text-wrap:balance;}}
p{{margin:0;}} button{{font-family:inherit;}} ul{{margin:0;padding:0;list-style:none;}}
:focus-visible{{outline:3px solid var(--focus-ring);outline-offset:3px;border-radius:2px;}}
.skip-link{{position:absolute;left:1rem;top:-100px;background:var(--accent);color:var(--on-accent);padding:.75rem 1.25rem;border-radius:4px;z-index:1000;transition:top .2s;font-weight:600;}}
.skip-link:focus{{top:1rem;}}
.container{{max-width:var(--container);margin-inline:auto;padding-inline:1.5rem;}} @media(min-width:640px){{.container{{padding-inline:2.5rem;}}}}
.eyebrow{{font-size:.72rem;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--accent-2);display:flex;align-items:center;gap:.6rem;}}
.eyebrow::before{{content:"";width:22px;height:2px;background:var(--accent-2);display:inline-block;}}
.section{{padding-block:5.5rem;}} @media(max-width:640px){{.section{{padding-block:3.5rem;}}}}
.band-inverse{{background:var(--bg-inverse);color:var(--text-inverse);}} .band-elevated{{background:var(--bg-elevated);}}
.btn{{display:inline-flex;align-items:center;gap:.5rem;font-weight:600;font-size:.95rem;padding:.85rem 1.5rem;border-radius:3px;border:1.5px solid transparent;cursor:pointer;text-decoration:none;transition:background .15s,color .15s,border-color .15s,transform .15s;white-space:nowrap;}}
.btn:active{{transform:translateY(1px);}} .btn-primary{{background:var(--accent);color:var(--on-accent);}} .btn-primary:hover{{background:var(--accent-hover);}}
.btn-outline{{border-color:currentColor;color:inherit;background:transparent;}} .btn-outline:hover{{background:rgba(255,255,255,.08);}}
.btn-outline.on-light{{border-color:var(--text);color:var(--text);}} .btn-outline.on-light:hover{{background:rgba(27,42,29,.06);}}
.utility-bar{{background:var(--bg-inverse-2);color:var(--text-inverse-soft);font-size:.8rem;}}
.utility-bar .container{{display:flex;align-items:center;justify-content:space-between;height:38px;gap:1rem;}}
.utility-left{{display:flex;align-items:center;gap:.5rem;font-family:var(--font-urdu);font-size:1rem;}} .utility-left .sep{{opacity:.5;font-family:var(--font-body);font-size:.8rem;}}
.utility-right{{display:flex;align-items:center;gap:1.25rem;}} .utility-right a{{text-decoration:none;color:inherit;opacity:.9;}} .utility-right a:hover{{opacity:1;text-decoration:underline;}}
.lang-toggle{{display:flex;gap:2px;font-weight:700;}} .lang-toggle button{{background:none;border:none;color:inherit;opacity:.6;cursor:pointer;padding:.2rem .35rem;font-size:.78rem;font-family:var(--font-body);}}
.lang-toggle button[aria-pressed="true"]{{opacity:1;text-decoration:underline;text-underline-offset:3px;}} @media(max-width:760px){{.utility-right .hide-sm{{display:none;}}}}
header.site-header{{position:sticky;top:0;z-index:100;background:var(--bg);border-bottom:1px solid var(--border);}}
.header-row{{display:flex;align-items:center;justify-content:space-between;gap:1.5rem;height:84px;}}
.brand{{display:flex;align-items:center;gap:.85rem;text-decoration:none;color:inherit;}} .brand img{{height:46px;width:auto;}}
.brand-word{{display:flex;flex-direction:column;line-height:1.15;}} .brand-word .name{{font-family:var(--font-display);font-weight:700;font-size:1.18rem;}}
.brand-word .tag{{font-size:.68rem;letter-spacing:.09em;text-transform:uppercase;color:var(--text-faint);}}
nav.primary-nav{{display:flex;align-items:center;gap:2.1rem;}} nav.primary-nav a{{text-decoration:none;font-weight:600;font-size:.95rem;color:var(--text);position:relative;padding-block:.3rem;}}
nav.primary-nav a::after{{content:"";position:absolute;left:0;right:0;bottom:0;height:2px;background:var(--accent);transform:scaleX(0);transform-origin:left;transition:transform .18s;}}
nav.primary-nav a:hover::after{{transform:scaleX(1);}} nav.primary-nav a[aria-current="page"]{{color:var(--accent);}} nav.primary-nav a[aria-current="page"]::after{{transform:scaleX(1);}}
.header-actions{{display:flex;align-items:center;gap:.9rem;}} .menu-toggle{{display:none;background:none;border:1px solid var(--border);border-radius:4px;padding:.5rem;cursor:pointer;color:var(--text);}}
@media(max-width:980px){{nav.primary-nav{{position:fixed;inset:84px 0 0 0;background:var(--bg);flex-direction:column;align-items:flex-start;padding:2rem 1.5rem;gap:1.4rem;transform:translateX(100%);transition:transform .25s ease;overflow-y:auto;}}
  nav.primary-nav.open{{transform:translateX(0);}} nav.primary-nav a{{font-size:1.2rem;}} .menu-toggle{{display:flex;}} .header-actions .btn-primary{{display:none;}}}}
.breadcrumb{{display:flex;align-items:center;gap:.5rem;font-size:.82rem;color:var(--text-soft);margin-bottom:1.3rem;flex-wrap:wrap;}}
.breadcrumb a{{text-decoration:none;color:inherit;opacity:.85;}} .breadcrumb a:hover{{opacity:1;text-decoration:underline;}}
.breadcrumb span.sep{{opacity:.5;}} .breadcrumb .current{{opacity:1;font-weight:600;color:var(--text);}}
.page-head{{padding-block:3.5rem 3rem;border-bottom:1px solid var(--border);}}
.page-head h1{{font-size:clamp(1.9rem,4vw,2.9rem);line-height:1.1;margin-bottom:1rem;max-width:800px;}}
.page-head .lead{{font-size:1.02rem;color:var(--text-soft);max-width:62ch;}}
.fact-strip{{border-bottom:1px solid var(--border);}} .fact-strip .container{{display:flex;flex-wrap:wrap;gap:0;}}
.fact-strip .fact{{flex:1 1 200px;padding:1.3rem 1.6rem;border-right:1px solid var(--border);display:flex;flex-direction:column;gap:.2rem;}}
.fact-strip .fact:last-child{{border-right:none;}}
.fact-strip .fact b{{font-family:var(--font-display);font-size:1.15rem;}}
.fact-strip .fact span{{font-size:.76rem;color:var(--text-faint);text-transform:uppercase;letter-spacing:.06em;}}
.prose-card{{background:var(--bg-elevated);border:1px solid var(--border);border-radius:10px;padding:clamp(1.75rem,4vw,3.25rem);box-shadow:0 1px 2px rgba(27,42,29,.05),0 12px 32px -18px rgba(27,42,29,.22);}}
.prose{{max-width:74ch;}} .prose p{{color:var(--text-soft);margin-bottom:1.1rem;font-size:1.02rem;}} .prose p:last-child{{margin-bottom:0;}}
.prose p:first-of-type{{font-family:var(--font-display);font-style:italic;font-size:1.22rem;line-height:1.55;color:var(--text);}}
.prose h3{{font-size:1.15rem;color:var(--text);margin:2rem 0 .8rem;}} .prose h3:first-child{{margin-top:0;}}
.contact-card{{background:var(--bg-elevated);border:1px solid var(--border);border-left:3px solid var(--accent);border-radius:4px;padding:1.9rem;max-width:420px;}}
.contact-card .crole{{font-size:.72rem;text-transform:uppercase;letter-spacing:.08em;color:var(--accent-2);font-weight:700;margin-bottom:.6rem;}}
.contact-card .cname{{font-family:var(--font-display);font-weight:700;font-size:1.15rem;margin-bottom:.3rem;}}
.contact-card a{{font-size:.88rem;color:var(--accent);text-decoration:none;font-weight:600;display:block;margin-top:.3rem;}}
.contact-card a:hover{{text-decoration:underline;}}
.cta-band{{display:flex;align-items:center;justify-content:space-between;gap:2rem;flex-wrap:wrap;padding:3.2rem 0;}}
.cta-band h3{{font-size:1.5rem;}} .cta-band p{{color:var(--text-inverse-soft);margin-top:.4rem;}}
footer{{padding-top:4.5rem;}} .footer-grid{{display:grid;grid-template-columns:1.4fr repeat(4,1fr);gap:2.5rem;padding-bottom:3rem;}}
.footer-col h4{{font-size:.76rem;text-transform:uppercase;letter-spacing:.09em;color:var(--accent-2-soft);margin-bottom:1.1rem;font-weight:700;}}
.footer-col ul{{display:flex;flex-direction:column;gap:.65rem;}} .footer-col a{{text-decoration:none;color:var(--text-inverse-soft);font-size:.9rem;}} .footer-col a:hover{{color:var(--text-inverse);text-decoration:underline;}}
.footer-brand{{display:flex;align-items:center;gap:.75rem;margin-bottom:1.1rem;}} .footer-brand img{{height:38px;filter:brightness(0) invert(1);opacity:.92;}}
.footer-brand span{{font-family:var(--font-display);font-weight:700;font-size:1.05rem;}}
.footer-about p{{color:var(--text-inverse-soft);font-size:.9rem;max-width:32ch;margin-bottom:1rem;}} .footer-about address{{font-style:normal;color:var(--text-inverse-soft);font-size:.85rem;line-height:1.7;}}
@media(max-width:980px){{.footer-grid{{grid-template-columns:repeat(2,1fr);}}}} @media(max-width:560px){{.footer-grid{{grid-template-columns:1fr;}}}}
.footer-bottom{{border-top:1px solid var(--border-inverse);padding-block:1.6rem;display:flex;justify-content:space-between;align-items:center;gap:1rem;flex-wrap:wrap;font-size:.8rem;color:var(--text-inverse-soft);}}
.footer-bottom .flinks{{display:flex;gap:1.3rem;flex-wrap:wrap;}} .footer-bottom a{{text-decoration:none;color:inherit;}} .footer-bottom a:hover{{text-decoration:underline;}}
.footer-bottom .dev-credit{{color:var(--text-inverse-soft);opacity:.75;font-size:.78rem;}}
.reveal{{opacity:0;transform:translateY(16px);transition:opacity .6s ease,transform .6s ease;}} .reveal.in{{opacity:1;transform:none;}}
</style>

<a href="#main" class="skip-link">Skip to main content</a>
<div class="utility-bar"><div class="container">
  <div class="utility-left"><span class="urdu">جامعہ کراچی</span><span class="sep">·</span><span>Est. 1951 &nbsp;·&nbsp; Federal Charter</span></div>
  <div class="utility-right"><div class="lang-toggle" role="group" aria-label="Language"><button type="button" aria-pressed="true">EN</button><span aria-hidden="true">/</span><button type="button" aria-pressed="false">اردو</button></div>
    <a href="#" class="hide-sm">(9221) 9926 1300-7</a><a href="contact.html">Directory</a><a href="student-portal.html">Student Portal</a></div>
</div></div>

<header class="site-header"><div class="container header-row">
  <a href="index.html" class="brand"><img src="__LOGO__" alt="University of Karachi crest" /></a>
  <nav class="primary-nav" id="primary-nav">
    <a href="https://uok-demo.vercel.app/">Home</a>
    <a href="index.html#about">About</a><a href="faculties.html" aria-current="page">Academics</a><a href="admissions.html">Admissions</a>
    <a href="research.html">Research</a><a href="library.html">Library</a><a href="contact.html">Contact</a>
  </nav>
  <div class="header-actions"><a href="admissions.html" class="btn btn-primary">Apply Now</a>
    <button class="menu-toggle" id="menu-toggle" aria-expanded="false" aria-controls="primary-nav" aria-label="Toggle navigation menu"><svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg></button>
  </div>
</div></header>

<main id="main">
  <div class="page-head"><div class="container reveal">
    <div class="breadcrumb"><a href="index.html">Home</a><span class="sep">/</span><a href="faculties.html">Faculty of {faculty}</a><span class="sep">/</span><span class="current">{name}</span></div>
    <div class="eyebrow">Faculty of {faculty}</div>
    <h1 style="margin-top:.8rem;">Department of {name}</h1>
    {lead}
  </div></div>

  {fact_strip}

  <section class="section">
    <div class="container">
      <div class="prose-card reveal">
        <div class="prose">
          {body_html}
        </div>
      </div>
    </div>
  </section>

  {contact_section}

  <section class="band-inverse"><div class="container cta-band">
    <div><h3>Interested in {name}?</h3><p>Admissions run through the standard university-wide pathway.</p></div>
    <a href="admissions.html" class="btn btn-primary">View Admissions</a>
  </div></section>
</main>

<footer class="band-inverse" id="footer"><div class="container">
  <div class="footer-grid">
    <div class="footer-col footer-about"><div class="footer-brand"><img src="__LOGO__" alt="" /><span>University of Karachi</span></div>
      <p>Pakistan&rsquo;s largest university &mdash; eight faculties, fifty-three departments, twenty research institutes.</p>
      <address>University Road, Karachi&nbsp;75270<br />Sindh, Pakistan<br />(9221) 9926 1300&ndash;7</address></div>
    <div class="footer-col"><h4>Academics</h4><ul><li><a href="faculties.html">All Faculties</a></li><li><a href="research.html">Research Institutes</a></li><li><a href="library.html">Library</a></li></ul></div>
    <div class="footer-col"><h4>Admissions</h4><ul><li><a href="admissions.html">Admissions 2026</a></li><li><a href="examinations.html">Examinations</a></li></ul></div>
    <div class="footer-col"><h4>Administration</h4><ul><li><a href="administration.html">Vice Chancellor</a></li><li><a href="administration.html">Directorates</a></li></ul></div>
    <div class="footer-col"><h4>Connect</h4><ul><li><a href="index.html">Homepage</a></li><li><a href="alumni.html">Alumni</a></li><li><a href="contact.html">Contact Us</a></li></ul></div>
  </div>
  <div class="footer-bottom"><span>&copy; 2026 University of Karachi. This site is available in English and Urdu.</span><span class="dev-credit">Developed by Softsols Pakistan</span>
    <div class="flinks"><a href="#">Accessibility</a><a href="#">Disclaimer</a><a href="#">Sitemap</a><a href="#">Credits</a></div>
  </div>
</div></footer>

<script>
(function(){{
  var toggle=document.getElementById('menu-toggle'),nav=document.getElementById('primary-nav');
  toggle.addEventListener('click',function(){{var open=nav.classList.toggle('open');toggle.setAttribute('aria-expanded',open?'true':'false');}});
  nav.querySelectorAll('a').forEach(function(a){{a.addEventListener('click',function(){{nav.classList.remove('open');toggle.setAttribute('aria-expanded','false');}});}});
  var reduceMotion=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var revealEls=document.querySelectorAll('.reveal');
  if('IntersectionObserver' in window && !reduceMotion){{
    var io=new IntersectionObserver(function(entries){{entries.forEach(function(entry){{if(entry.isIntersecting){{entry.target.classList.add('in');io.unobserve(entry.target);}}}});}},{{threshold:.1,rootMargin:'0px 0px -40px 0px'}});
    revealEls.forEach(function(el){{io.observe(el);}});
  }} else {{ revealEls.forEach(function(el){{el.classList.add('in');}}); }}
  var langBtns=document.querySelectorAll('.lang-toggle button');
  langBtns.forEach(function(btn){{btn.addEventListener('click',function(){{langBtns.forEach(function(b){{b.setAttribute('aria-pressed','false');}});btn.setAttribute('aria-pressed','true');}});}});
}})();
</script>
'''

def build_page(slug, data, faculty):
    name = data.get('real_name') or title_case_name(slug)
    body_parts = []
    for kind, text in data['blocks']:
        if kind == 'h':
            body_parts.append(f'<h3>{esc(text)}</h3>')
        else:
            body_parts.append(f'<p>{esc(text)}</p>')
    body_html = '\n        '.join(body_parts)

    first_para = next((t for k, t in data['blocks'] if k == 'p'), '')
    lead = f'<p class="lead">{esc(first_para[:220])}{"…" if len(first_para) > 220 else ""}</p>' if first_para else ''

    facts = []
    if data['established']:
        facts.append(f'<div class="fact"><b>{data["established"]}</b><span>Established</span></div>')
    facts.append(f'<div class="fact"><b>Faculty of {esc(faculty)}</b><span>Parent faculty</span></div>')
    if data['chairman']:
        facts.append(f'<div class="fact"><b>{esc(data["chairman"])}</b><span>Chairman</span></div>')
    fact_strip = f'<div class="fact-strip"><div class="container">{"".join(facts)}</div></div>' if facts else ''

    contact_section = ''
    if data['chairman']:
        contact_section = f'''<section class="section band-elevated">
    <div class="container">
      <div class="eyebrow reveal">Contact</div>
      <div class="contact-card reveal" style="margin-top:1.5rem;">
        <div class="crole">Chairman</div>
        <div class="cname">{esc(data["chairman"])}</div>
        <a href="contact.html">Find department contact &rarr;</a>
      </div>
    </div>
  </section>'''

    html = TEMPLATE.format(
        name=esc(name), faculty=esc(faculty), lead=lead, fact_strip=fact_strip,
        body_html=body_html, contact_section=contact_section,
    )
    return html

def main():
    with open('../fonts/embedded-fonts.css', encoding='utf-8') as f:
        font_faces = f.read()
    with open('../assets/data_uris.json', encoding='utf-8') as f:
        data_uris = json.load(f)

    generated = []
    skipped = []
    for path in sorted(glob.glob(f'{TEXT_DIR}/*.txt')):
        slug = os.path.splitext(os.path.basename(path))[0]
        if slug == 'computerscience':
            continue
        with open(path, encoding='utf-8') as f:
            raw = f.read()
        parsed = parse_dept(slug, raw)
        if not parsed:
            skipped.append(slug)
            continue
        faculty = FACULTY_MAP.get(slug, 'Science')
        html = build_page(slug, parsed, faculty)
        html = html.replace('__FONT_FACES__', font_faces).replace('__LOGO__', data_uris['logo'])
        outname = f'dept-{slug}.html'
        with open(outname, 'w', encoding='utf-8') as f:
            f.write(html)
        generated.append(outname)

    print(f"Generated {len(generated)} department pages")
    if skipped:
        print(f"Skipped (no parseable content): {skipped}")

if __name__ == '__main__':
    main()
