import os
import glob
import re

light_colors_old_pattern = r"--bg:#EDE6D2;.*?--on-accent:#FFFFFF;"
light_colors_new = """--bg:#FFFFFF; --bg-elevated:#F8F9FA; --bg-inverse:#005230; --bg-inverse-2:#003D24;
  --text:#111827; --text-soft:#4B5563; --text-faint:#6B7280;
  --text-inverse:#FFFFFF; --text-inverse-soft:#D1FAE5;
  --accent:#059669; --accent-hover:#047857; --accent-2:#F59E0B; --accent-2-soft:#FCD34D;
  --border:#E5E7EB; --border-inverse:rgba(255,255,255,.2);
  --focus-ring:#10B981;--on-accent:#FFFFFF;"""

dark_colors_old_pattern = r"--bg:#10160D;.*?--on-accent:#0B1009;"
dark_colors_new = """--bg:#0F172A; --bg-elevated:#1E293B; --bg-inverse:#003D24; --bg-inverse-2:#002918;
  --text:#F8FAFC; --text-soft:#94A3B8; --text-faint:#64748B;
  --text-inverse:#F8FAFC; --text-inverse-soft:#94A3B8;
  --accent:#10B981; --accent-hover:#34D399; --accent-2:#FBBF24; --accent-2-soft:#FDE68A;
  --border:#334155; --border-inverse:rgba(255,255,255,.1);
  --focus-ring:#34D399;--on-accent:#000000;"""

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Non-greedy match to replace exactly the color variable blocks
    new_content = re.sub(light_colors_old_pattern, light_colors_new, content, flags=re.DOTALL)
    new_content = re.sub(dark_colors_old_pattern, dark_colors_new, new_content, flags=re.DOTALL)
    
    if content != new_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filepath}")

if __name__ == "__main__":
    count = 0
    for filepath in glob.glob('site/*.html'):
        process_file(filepath)
        count += 1
    print(f"Processed {count} HTML files in site directory.")
