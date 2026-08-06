import os
import glob
import re

new_nav_html = '''<nav class="primary-nav" id="primary-nav">
  <div class="nav-item">
    <a href="https://uok-demo.vercel.app/">Home</a>
  </div>
  <div class="nav-item">
    <a href="index.html#about">About <span class="nav-arrow">&#9662;</span></a>
    <div class="dropdown">
      <a href="index.html#about">About the University</a>
      <a href="administration.html">Administration</a>
    </div>
  </div>
  <div class="nav-item">
    <a href="faculties.html">Academics <span class="nav-arrow">&#9662;</span></a>
    <div class="dropdown">
      <a href="faculties.html">Faculties & Departments</a>
      <a href="examinations.html">Examinations</a>
      <a href="journals.html">Journals</a>
    </div>
  </div>
  <div class="nav-item">
    <a href="admissions.html">Admissions <span class="nav-arrow">&#9662;</span></a>
    <div class="dropdown">
      <a href="admissions.html">Admissions Info</a>
      <a href="prospectus.html">Prospectus</a>
      <a href="student-portal.html">Student Portal</a>
    </div>
  </div>
  <div class="nav-item">
    <a href="research.html">Research <span class="nav-arrow">&#9662;</span></a>
    <div class="dropdown">
      <a href="research.html">Research & Institutes</a>
    </div>
  </div>
  <div class="nav-item">
    <a href="library.html">Library</a>
  </div>
  <div class="nav-item">
    <a href="index.html#news">News</a>
  </div>
  <div class="nav-item">
    <a href="contact.html">Contact <span class="nav-arrow">&#9662;</span></a>
    <div class="dropdown">
      <a href="contact.html">Contact Us</a>
      <a href="alumni.html">Alumni</a>
    </div>
  </div>
</nav>'''

new_css_html = '''
.nav-item { position: relative; }
.nav-item > a { display: flex; align-items: center; gap: 4px; }
.nav-arrow { font-size: 0.7em; opacity: 0.7; transition: transform 0.2s; }
.dropdown { position: absolute; top: 100%; left: 0; background: var(--bg-elevated); min-width: 220px; box-shadow: var(--shadow); border: 1px solid var(--border); border-radius: 6px; padding: 0.5rem 0; opacity: 0; visibility: hidden; transform: translateY(10px); transition: all 0.2s ease; z-index: 100; display: flex; flex-direction: column; }
.nav-item:hover .dropdown { opacity: 1; visibility: visible; transform: translateY(0); }
.nav-item:hover .nav-arrow { transform: rotate(180deg); }
nav.primary-nav .dropdown a { padding: 0.6rem 1.2rem; font-size: 0.9rem; color: var(--text-soft); font-weight: 500; width: 100%; border-bottom: none; }
nav.primary-nav .dropdown a::after { display: none; }
nav.primary-nav .dropdown a:hover { background: var(--bg); color: var(--accent); transform: none; }
@media (max-width: 980px) {
  .dropdown { position: static; box-shadow: none; border: none; padding: 0; min-width: 100%; opacity: 1; visibility: visible; transform: none; display: none; margin-top: 0.5rem; margin-left: 1rem; border-left: 2px solid var(--border); border-radius: 0; }
  .nav-item:hover .dropdown { display: flex; }
  .nav-item { width: 100%; }
}
'''

new_css_py = new_css_html.replace('{', '{{').replace('}', '}}')

def update_files():
    files = glob.glob('site/*.html') + glob.glob('site/*.py')
    
    updated_count = 0
    for path in files:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content
        
        # 1. Replace nav
        nav_pattern = r'<nav class="primary-nav" id="primary-nav">.*?</nav>'
        content = re.sub(nav_pattern, new_nav_html, content, flags=re.DOTALL)
        
        # 2. Add CSS
        if '.dropdown' not in content:
            if path.endswith('.py'):
                content = content.replace('</style>', new_css_py + '</style>')
            else:
                content = content.replace('</style>', new_css_html + '</style>')
            
        if content != original_content:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            updated_count += 1
            print(f"Updated {path}")

    print(f"Update complete. Modified {updated_count} files.")

if __name__ == "__main__":
    update_files()
