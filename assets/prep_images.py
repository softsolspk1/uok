from PIL import Image
import os

jobs = [
    # (src, dst, max_width, quality)
    ("banner-ubit.jpg", "hero-ubit.jpg", 1600, 72),
    ("banner-chem.jpg", "hero-chem.jpg", 1000, 70),
    ("banner-dpa.jpg", "hero-dpa.jpg", 1000, 70),
]

for src, dst, maxw, q in jobs:
    im = Image.open(src).convert("RGB")
    w, h = im.size
    if w > maxw:
        new_h = int(h * (maxw / w))
        im = im.resize((maxw, new_h), Image.LANCZOS)
    im.save(dst, "JPEG", quality=q, optimize=True)
    print(dst, im.size, os.path.getsize(dst) / 1024, "KB")
