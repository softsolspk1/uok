import base64, json

files = {
    "logo": ("logo.png", "image/png"),
    "hero_ubit": ("hero-ubit.jpg", "image/jpeg"),
    "hero_chem": ("hero-chem.jpg", "image/jpeg"),
    "hero_dpa": ("hero-dpa.jpg", "image/jpeg"),
}

out = {}
for key, (fname, mime) in files.items():
    with open(fname, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode("ascii")
    out[key] = f"data:{mime};base64,{b64}"
    print(key, fname, len(data)/1024, "KB ->", len(b64), "chars")

with open("data_uris.json", "w") as f:
    json.dump(out, f)
