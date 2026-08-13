import os
import re

workspace_dir = r"c:\Users\softs\Desktop\UOK Website"

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the header block
    header_match = re.search(r'(<header>.*?</header>)', content, re.DOTALL | re.IGNORECASE)
    if not header_match:
        return

    header_content = header_match.group(1)
    
    def replacer(m):
        li_tag = m.group(1)
        a_tag = m.group(2)
        a_tag = a_tag.replace('href="research.html"', 'href="https://iccs.edu/" target="_blank"')
        return f'{li_tag}{a_tag}International Center for Chemical and Biological Sciences</a></li>'

    new_header_content = re.sub(
        r'(<li[^>]*>)\s*(<a[^>]*href="research\.html"[^>]*>)\s*Research Institutes\s*</a>\s*</li>',
        replacer,
        header_content
    )

    if new_header_content != header_content:
        new_content = content[:header_match.start()] + new_header_content + content[header_match.end():]
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filepath}")

for root, dirs, files in os.walk(workspace_dir):
    if '.git' in root:
        continue
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            try:
                process_file(filepath)
            except Exception as e:
                print(f"Error processing {filepath}: {e}")

print("Done")
