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

# Palette 6: Sapphire & Electric Cyan (Professional & Vibrant)
sapphire_light = """--bg:#FFFFFF; --bg-elevated:#F8FAFC; --bg-inverse:#082F49; --bg-inverse-2:#041F33;
  --text:#0F172A; --text-soft:#475569; --text-faint:#94A3B8;
  --text-inverse:#FFFFFF; --text-inverse-soft:#E0F2FE;
  --accent:#0EA5E9; --accent-hover:#0284C7; --accent-2:#F43F5E; --accent-2-soft:#FB7185;
  --border:#E2E8F0; --border-inverse:rgba(255,255,255,.15);
  --focus-ring:#38BDF8;--on-accent:#FFFFFF;"""

sapphire_dark = """--bg:#040B16; --bg-elevated:#0A192F; --bg-inverse:#082F49; --bg-inverse-2:#021120;
  --text:#F8FAFC; --text-soft:#CBD5E1; --text-faint:#94A3B8;
  --text-inverse:#F8FAFC; --text-inverse-soft:#BAE6FD;
  --accent:#38BDF8; --accent-hover:#7DD3FC; --accent-2:#FB7185; --accent-2-soft:#FDA4AF;
  --border:#0F2942; --border-inverse:rgba(255,255,255,.15);
  --focus-ring:#7DD3FC;--on-accent:#000000;"""

# Super Cool Revamp CSS Injection
css_revamp_injection = """
/* ====== SUPER COOL REVAMP CSS ====== */
:root {
  --shadow-premium: 0 20px 40px -15px rgba(0,0,0,0.08);
  --shadow-hover: 0 25px 50px -12px rgba(14, 165, 233, 0.25);
}
@media (prefers-color-scheme: dark) {
  :root {
    --shadow-premium: 0 20px 40px -15px rgba(0,0,0,0.4);
    --shadow-hover: 0 25px 50px -12px rgba(56, 189, 248, 0.35);
  }
}
:root[data-theme="dark"] {
  --shadow-premium: 0 20px 40px -15px rgba(0,0,0,0.4);
  --shadow-hover: 0 25px 50px -12px rgba(56, 189, 248, 0.35);
}

/* Glassmorphism Header */
header.site-header {
  background: rgba(255, 255, 255, 0.75) !important;
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(0,0,0,0.05) !important;
}
@media (prefers-color-scheme: dark) {
  header.site-header { 
    background: rgba(4, 11, 22, 0.8) !important; 
    border-bottom: 1px solid rgba(255,255,255,0.05) !important;
  }
}
:root[data-theme="dark"] header.site-header { 
  background: rgba(4, 11, 22, 0.8) !important; 
  border-bottom: 1px solid rgba(255,255,255,0.05) !important;
}

/* Rounded, Floating Cards */
.quick-grid { border-radius: 20px !important; overflow: hidden; box-shadow: var(--shadow-premium) !important; }
.academic-card, .research-card, .news-card {
  border-radius: 20px !important;
  box-shadow: var(--shadow-premium) !important;
  border: 1px solid var(--border) !important;
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
  background: var(--bg-elevated) !important;
}
.academic-card:hover, .research-card:hover, .news-card:hover {
  transform: translateY(-8px) scale(1.02) !important;
  box-shadow: var(--shadow-hover) !important;
  border-color: var(--accent) !important;
}

/* Vibrant Gradient Buttons */
.btn-primary {
  background: linear-gradient(135deg, var(--accent), var(--accent-hover)) !important;
  border-radius: 99px !important;
  border: none !important;
  transition: transform 0.2s, box-shadow 0.2s !important;
  box-shadow: 0 4px 15px -3px rgba(14, 165, 233, 0.4) !important;
}
.btn-primary:hover {
  transform: translateY(-2px) scale(1.05) !important;
  box-shadow: 0 12px 25px -5px rgba(14, 165, 233, 0.6) !important;
}

/* Sleeker Hero Gradient */
.hero-scrim {
  background: linear-gradient(180deg, rgba(4,11,22,0.3) 0%, rgba(4,11,22,0.7) 60%, rgba(4,11,22,1) 100%) !important;
}
</style>
"""

def create_variation(filename, light_palette, dark_palette):
    new_content = content.replace(current_light, light_palette)
    new_content = new_content.replace(current_dark, dark_palette)
    
    # Inject the revamp CSS right before </style>
    if "</style>" in new_content:
        # We replace the LAST occurrence of </style> or we just replace </style> knowing there is only one in the template logic
        new_content = new_content.replace("</style>", css_revamp_injection)
        
    if new_content == content:
        print(f"Warning: Strings not found for {filename}. No changes made.")
    else:
        with open(f'site/{filename}', 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Created {filename} successfully with revamped design.")

create_variation('index7.html', sapphire_light, sapphire_dark)
