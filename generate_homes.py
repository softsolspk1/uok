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

# Palette 1 (index2.html): Ocean/Academic Blue
blue_light = """--bg:#FFFFFF; --bg-elevated:#F1F5F9; --bg-inverse:#0F172A; --bg-inverse-2:#1E293B;
  --text:#0F172A; --text-soft:#475569; --text-faint:#64748B;
  --text-inverse:#F8FAFC; --text-inverse-soft:#CBD5E1;
  --accent:#2563EB; --accent-hover:#1D4ED8; --accent-2:#D97706; --accent-2-soft:#F59E0B;
  --border:#E2E8F0; --border-inverse:rgba(255,255,255,.15);
  --focus-ring:#3B82F6;--on-accent:#FFFFFF;"""

blue_dark = """--bg:#020617; --bg-elevated:#0F172A; --bg-inverse:#1E293B; --bg-inverse-2:#334155;
  --text:#F8FAFC; --text-soft:#94A3B8; --text-faint:#64748B;
  --text-inverse:#F8FAFC; --text-inverse-soft:#94A3B8;
  --accent:#3B82F6; --accent-hover:#60A5FA; --accent-2:#F59E0B; --accent-2-soft:#FCD34D;
  --border:#1E293B; --border-inverse:rgba(255,255,255,.1);
  --focus-ring:#60A5FA;--on-accent:#FFFFFF;"""

# Palette 2 (index3.html): Crimson & Slate
red_light = """--bg:#FAFAFA; --bg-elevated:#FFFFFF; --bg-inverse:#450A0A; --bg-inverse-2:#2C0606;
  --text:#171717; --text-soft:#525252; --text-faint:#737373;
  --text-inverse:#FFFFFF; --text-inverse-soft:#FECACA;
  --accent:#991B1B; --accent-hover:#7F1D1D; --accent-2:#0F172A; --accent-2-soft:#334155;
  --border:#E5E5E5; --border-inverse:rgba(255,255,255,.15);
  --focus-ring:#DC2626;--on-accent:#FFFFFF;"""

red_dark = """--bg:#0A0A0A; --bg-elevated:#171717; --bg-inverse:#2C0606; --bg-inverse-2:#1A0404;
  --text:#FAFAFA; --text-soft:#A3A3A3; --text-faint:#737373;
  --text-inverse:#FAFAFA; --text-inverse-soft:#D4D4D4;
  --accent:#DC2626; --accent-hover:#EF4444; --accent-2:#E5E5E5; --accent-2-soft:#A3A3A3;
  --border:#262626; --border-inverse:rgba(255,255,255,.1);
  --focus-ring:#EF4444;--on-accent:#FFFFFF;"""

# Palette 3 (index4.html): Deep Purple / Modern Tech
purple_light = """--bg:#FFFFFF; --bg-elevated:#F5F3FF; --bg-inverse:#2E1065; --bg-inverse-2:#1C0A3F;
  --text:#111827; --text-soft:#4B5563; --text-faint:#6B7280;
  --text-inverse:#FFFFFF; --text-inverse-soft:#DDD6FE;
  --accent:#6D28D9; --accent-hover:#5B21B6; --accent-2:#059669; --accent-2-soft:#10B981;
  --border:#E5E7EB; --border-inverse:rgba(255,255,255,.15);
  --focus-ring:#8B5CF6;--on-accent:#FFFFFF;"""

purple_dark = """--bg:#030712; --bg-elevated:#111827; --bg-inverse:#1C0A3F; --bg-inverse-2:#0F0524;
  --text:#F9FAFB; --text-soft:#9CA3AF; --text-faint:#6B7280;
  --text-inverse:#F9FAFB; --text-inverse-soft:#9CA3AF;
  --accent:#8B5CF6; --accent-hover:#A78BFA; --accent-2:#10B981; --accent-2-soft:#34D399;
  --border:#1F2937; --border-inverse:rgba(255,255,255,.1);
  --focus-ring:#A78BFA;--on-accent:#FFFFFF;"""


create_variation('index2.html', blue_light, blue_dark)
create_variation('index3.html', red_light, red_dark)
create_variation('index4.html', purple_light, purple_dark)
