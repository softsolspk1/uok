import os
import glob

def update_files():
    # Find all html and python files in site/
    files = glob.glob('site/*.html') + glob.glob('site/*.py')
    
    updated_count = 0
    for path in files:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        if '<nav class="primary-nav" id="primary-nav">' in content and 'https://uok-demo.vercel.app/' not in content:
            # Try to insert right after the nav opening tag
            new_content = content.replace(
                '<nav class="primary-nav" id="primary-nav">',
                '<nav class="primary-nav" id="primary-nav">\n    <a href="https://uok-demo.vercel.app/">Home</a>'
            )
            
            if new_content != content:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                updated_count += 1
                print(f"Updated {path}")

    print(f"Update complete. Modified {updated_count} files.")

if __name__ == "__main__":
    update_files()
