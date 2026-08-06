import os
import glob
import re

new_js = '''  nav.querySelectorAll('a').forEach(function(a){
    a.addEventListener('click', function(e){
      var item = a.closest('.nav-item');
      if(window.innerWidth <= 980 && a.nextElementSibling && a.nextElementSibling.classList.contains('dropdown')){
        e.preventDefault();
        var wasOpen = item ? item.classList.contains('open') : false;
        document.querySelectorAll('.nav-item.open').forEach(function(i){ if(i!==item) i.classList.remove('open'); });
        if(item) item.classList.toggle('open', !wasOpen);
      } else if(window.innerWidth <= 980){
        nav.classList.remove('open');
        toggle.setAttribute('aria-expanded','false');
      }
    });
  });'''

new_js_py = new_js.replace('{', '{{').replace('}', '}}')

def fix_files():
    files = glob.glob('site/*.html') + glob.glob('site/*.py')
    updated_count = 0
    for path in files:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        orig = content
        
        # 1. Fix CSS
        content = content.replace('.nav-item:hover .dropdown { display: flex; }', '.nav-item.open .dropdown { display: flex; }')
        content = content.replace('.nav-item:hover .dropdown {{ display: flex; }}', '.nav-item.open .dropdown {{ display: flex; }}')
        
        # 2. Fix JS
        if path.endswith('.py'):
            # For python scripts which use {{ and }}
            js_pattern = r"nav\.querySelectorAll\('a'\)\.forEach\(function\(a\)\{\{a\.addEventListener\('click',function\(\)\{\{nav\.classList\.remove\('open'\);toggle\.setAttribute\('aria-expanded','false'\);\}\}\);\}\}\);"
            content = re.sub(js_pattern, new_js_py, content)
        else:
            # HTML files might have it minified or multiline
            js_pattern1 = r"nav\.querySelectorAll\('a'\)\.forEach\(function\(a\).*?\}\);\s*\}\);"
            content = re.sub(js_pattern1, new_js, content, flags=re.DOTALL)
            
            # Remove the old .nav-arrow listener if it exists in HTML files
            arrow_pattern = r"document\.querySelectorAll\('\.nav-arrow'\)\.forEach\(function\(arrow\).*?\}\);\s*\}\);"
            content = re.sub(arrow_pattern, "", content, flags=re.DOTALL)
            
        if content != orig:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            updated_count += 1
            print(f"Fixed {path}")

    print(f"Update complete. Modified {updated_count} files.")

if __name__ == "__main__":
    fix_files()
