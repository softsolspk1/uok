import os

# Read current index.html
with open('site/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Exact current color strings to replace
current_light = """--bg:#FFFFFF; --bg-elevated:#F8F9FA; --bg-inverse:#005230; --bg-inverse-2:#003D24;
  --text:#111827; --text-soft:#4B5563; --text-faint:#6B7280;
  --text-inverse:#FFFFFF; --text-inverse-soft:#D1FAE5;
  --accent:#059669; --accent-hover:#047857; --accent-2:#F59E0B; --accent-2-soft:#FCD34D;
  --border:#E5E7EB; --border-inverse:rgba(255,255,255,.2);
  --focus-ring:#10B981;--on-accent:#FFFFFF;"""

current_dark = """--bg:#0F172A; --bg-elevated:#1E293B; --bg-inverse:#003D24; --bg-inverse-2:#002918;
  --text:#F8FAFC; --text-soft:#94A3B8; --text-faint:#64748B;
  --text-inverse:#F8FAFC; --text-inverse-soft:#94A3B8;
  --accent:#10B981; --accent-hover:#34D399; --accent-2:#FBBF24; --accent-2-soft:#FDE68A;
  --border:#334155; --border-inverse:rgba(255,255,255,.1);
  --focus-ring:#34D399;--on-accent:#000000;"""

def create_variation(filename, light_palette, dark_palette):
    new_content = content.replace(current_light, light_palette)
    new_content = new_content.replace(current_dark, dark_palette)
    
    if new_content == content:
        print(f"Warning: Strings not found for {filename}. No changes made.")
    else:
        with open(f'site/{filename}', 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Created {filename} successfully.")

# Palette 4 (index5.html): Sunset / Vibrant Orange & Pink
sunset_light = """--bg:#FFFFFF; --bg-elevated:#FFF7ED; --bg-inverse:#7C2D12; --bg-inverse-2:#431407;
  --text:#1F2937; --text-soft:#4B5563; --text-faint:#9CA3AF;
  --text-inverse:#FFFFFF; --text-inverse-soft:#FFEDD5;
  --accent:#F97316; --accent-hover:#EA580C; --accent-2:#EC4899; --accent-2-soft:#F472B6;
  --border:#FED7AA; --border-inverse:rgba(255,255,255,.2);
  --focus-ring:#F97316;--on-accent:#FFFFFF;"""

sunset_dark = """--bg:#0F0505; --bg-elevated:#1A0808; --bg-inverse:#431407; --bg-inverse-2:#260902;
  --text:#FFF7ED; --text-soft:#FDBA74; --text-faint:#FB923C;
  --text-inverse:#FFF7ED; --text-inverse-soft:#FDBA74;
  --accent:#F97316; --accent-hover:#FB923C; --accent-2:#EC4899; --accent-2-soft:#F472B6;
  --border:#431407; --border-inverse:rgba(255,255,255,.1);
  --focus-ring:#FB923C;--on-accent:#000000;"""

# Palette 5 (index6.html): Neon / Magenta & Cyan
neon_light = """--bg:#FFFFFF; --bg-elevated:#FDF4FF; --bg-inverse:#831843; --bg-inverse-2:#4C0519;
  --text:#111827; --text-soft:#4B5563; --text-faint:#6B7280;
  --text-inverse:#FFFFFF; --text-inverse-soft:#FCE7F3;
  --accent:#DB2777; --accent-hover:#BE185D; --accent-2:#06B6D4; --accent-2-soft:#22D3EE;
  --border:#FBCFE8; --border-inverse:rgba(255,255,255,.2);
  --focus-ring:#DB2777;--on-accent:#FFFFFF;"""

neon_dark = """--bg:#09040D; --bg-elevated:#15091D; --bg-inverse:#4C0519; --bg-inverse-2:#2B030E;
  --text:#FDF4FF; --text-soft:#FBCFE8; --text-faint:#F9A8D4;
  --text-inverse:#FDF4FF; --text-inverse-soft:#FBCFE8;
  --accent:#EC4899; --accent-hover:#F472B6; --accent-2:#06B6D4; --accent-2-soft:#22D3EE;
  --border:#831843; --border-inverse:rgba(255,255,255,.1);
  --focus-ring:#F472B6;--on-accent:#000000;"""

create_variation('index5.html', sunset_light, sunset_dark)
create_variation('index6.html', neon_light, neon_dark)
