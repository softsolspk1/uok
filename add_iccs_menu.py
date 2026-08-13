import os
import re

workspace_dir = r"c:\Users\softs\Desktop\UOK Website"

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = content
    
    # We want to ensure that inside the Research submenu, we have both:
    # 1. Research Institutes (or Overview)
    # 2. International Center for Chemical and Biological Sciences
    
    # We will target the Research submenu block to be safe.
    
    def fix_submenu(m):
        submenu_content = m.group(0)
        
        # Check if ICCBS is already there
        iccs_html = '<li><a href="https://iccs.edu/" target="_blank">International Center for Chemical and Biological Sciences</a></li>'
        
        has_iccs = 'iccs.edu' in submenu_content
        has_ri = 'Research Institutes' in submenu_content
        
        # We want to clean up and insert properly
        if not has_iccs:
            # We need to insert ICCBS
            # Let's insert it right after the 'Research Institutes' or 'Research Institutes Overview' link if it exists
            if has_ri:
                submenu_content = re.sub(
                    r'(<li[^>]*><a[^>]*href="research\.html"[^>]*>Research Institutes(?: Overview)?</a></li>)',
                    r'\1\n                  ' + iccs_html,
                    submenu_content
                )
            else:
                # Just insert at the top of the submenu
                submenu_content = re.sub(
                    r'(<ul[^>]*>)',
                    r'\1\n                  ' + iccs_html,
                    submenu_content,
                    count=1
                )
                
        if has_iccs and not has_ri:
            # It was replaced previously! We should restore 'Research Institutes' before ICCBS
            text = "Research Institutes Overview" if 'uok-stadum' in filepath.replace('\\', '/') else "Research Institutes"
            ri_html = f'<li><a href="research.html">{text}</a></li>'
            
            submenu_content = re.sub(
                r'(<li[^>]*><a[^>]*href="https://iccs\.edu/"[^>]*>International Center for Chemical and Biological Sciences</a></li>)',
                ri_html + r'\n                  \1',
                submenu_content
            )
            
        return submenu_content

    # This pattern targets the Research menu item and its immediate submenu <ul> block
    pattern = r'<li[^>]*>\s*<a[^>]*href="research\.html"[^>]*>Research</a>\s*<ul[^>]*>.*?(?=</ul>)</ul>'
    
    new_content = re.sub(pattern, fix_submenu, new_content, flags=re.DOTALL | re.IGNORECASE)

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filepath}")

for root, dirs, files in os.walk(workspace_dir):
    if '.git' in root or 'node_modules' in root:
        continue
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            try:
                process_file(filepath)
            except Exception as e:
                pass

print("Done")
