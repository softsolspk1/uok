# University of Karachi — Flagship Homepage (new design)

A standalone, framework-free redesign benchmarked against Oxford, Stanford, Princeton,
Imperial and Harvard. Everything is self-contained in this folder.

## Preview locally
Open `index.html` directly in a browser, or serve the folder:

```
# from inside newdesign/
python -m http.server 8000
# then visit http://localhost:8000/
```

## Pages
- `index.html` — the homepage.
- `student-dashboard.html` — Student Portal (static demo UI, sample data).
- `faculty-dashboard.html` — Faculty Portal (static demo UI, sample data).

## Design system
- Colour: deep navy-indigo `#0e1e3a` (primary) + antique brass gold `#c19a3f`
  (accent) on ivory/parchment and charcoal neutrals. No institutional green.
- Type: Fraunces (serif display) + Inter (sans UI/body), both self-hosted in `fonts/`.

## What's real vs placeholder
- **Real, verified facts** (from `../pages_text/*` and uok.edu.pk): est. 1951 by Act of
  Parliament, 1,279-acre campus, 8 faculties, 53+ departments, 20 research institutes,
  700+ faculty, 41,000+ students, 360,000+ library volumes, 145+ affiliated colleges,
  ICCBS/HEJ Research Institute of Chemistry (a centre of the Third World Academy of
  Sciences), Dr. Mahmud Husain Library + Quaid-i-Azam collection, named historic scholars.
- **Placeholders (clearly labelled):** homepage News/Events cards are CMS content
  templates (no fabricated headlines/dates); the two dashboards use illustrative sample
  student/faculty data and are marked with a "Demonstration interface" ribbon.
- No rankings, current office-holder names, or named testimonials were invented.

## Assets
Real UoK brand assets (logo, favicon, archival campus photos) copied from the repo into
`assets/`. Photos are lower-resolution archival images, used full-bleed with navy
gradient/duotone overlays by design.
