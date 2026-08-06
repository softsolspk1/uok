import glob
import os

css_injection = """
.brand img { transition: filter 0.3s ease; }
@media (prefers-color-scheme: dark) {
  html:not([data-theme="light"]) .brand img { filter: brightness(0) invert(1); }
}
:root[data-theme="dark"] .brand img { filter: brightness(0) invert(1); }
</style>
"""

count = 0
for filepath in glob.glob('site/*.html'):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if "filter: brightness(0) invert(1);" not in content:
        new_content = content.replace("</style>", css_injection)
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            count += 1

print(f"Fixed logo visibility in {count} files.")
