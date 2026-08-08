import os
import shutil
import urllib.request
import json

def download_image(url, save_path):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req) as response, open(save_path, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
    except Exception as e:
        print(f"Failed to download {url}: {e}")

def main():
    brain_dir = r"C:\Users\softs\.gemini\antigravity-ide\brain\b942e4c9-3ab0-4319-9a81-a497e9a1999f"
    
    vc_img = next((f for f in os.listdir(brain_dir) if f.startswith('vc_portrait_') and f.endswith('.png')), None)
    reg_img = next((f for f in os.listdir(brain_dir) if f.startswith('registrar_portrait_') and f.endswith('.png')), None)
    student1 = next((f for f in os.listdir(brain_dir) if f.startswith('uok_students_1_') and f.endswith('.png')), None)
    student2 = next((f for f in os.listdir(brain_dir) if f.startswith('uok_students_2_') and f.endswith('.png')), None)

    # Project directories
    uok_stadum_blog = r"c:\Users\softs\Desktop\UOK Website\uok-stadum\assets\img\blog"
    uok_stadum_admin = r"c:\Users\softs\Desktop\UOK Website\uok-stadum\assets\img\admin"
    demo_3_photos = r"c:\Users\softs\Desktop\UOK Website\demo 3\New Werb\assets\photos"
    demo_3_admin = os.path.join(demo_3_photos, "admin")
    
    root_assets_admin = r"c:\Users\softs\Desktop\UOK Website\assets\photos\admin"
    
    os.makedirs(demo_3_admin, exist_ok=True)
    os.makedirs(uok_stadum_admin, exist_ok=True)
    os.makedirs(root_assets_admin, exist_ok=True)

    # 1. Overwrite foreign student thumbnails in uok-stadum
    if student1 and os.path.exists(uok_stadum_blog):
        shutil.copy(os.path.join(brain_dir, student1), os.path.join(uok_stadum_blog, "recent-post-1-1.jpg"))
        shutil.copy(os.path.join(brain_dir, student1), os.path.join(uok_stadum_blog, "recent-post-1-3.jpg"))
    if student2 and os.path.exists(uok_stadum_blog):
        shutil.copy(os.path.join(brain_dir, student2), os.path.join(uok_stadum_blog, "recent-post-1-2.jpg"))
        
    # 2. Copy admin photos
    if vc_img:
        shutil.copy(os.path.join(brain_dir, vc_img), os.path.join(demo_3_admin, "vc.png"))
        shutil.copy(os.path.join(brain_dir, vc_img), os.path.join(uok_stadum_admin, "vc.png"))
        shutil.copy(os.path.join(brain_dir, vc_img), os.path.join(root_assets_admin, "vc.png"))
    if reg_img:
        shutil.copy(os.path.join(brain_dir, reg_img), os.path.join(demo_3_admin, "registrar.png"))
        shutil.copy(os.path.join(brain_dir, reg_img), os.path.join(uok_stadum_admin, "registrar.png"))
        shutil.copy(os.path.join(brain_dir, reg_img), os.path.join(root_assets_admin, "registrar.png"))

    # Download random professional portraits for Deans from unsplash using source.unsplash
    # Because of internet issues with python, we will just use dummy avatars.
    dean_names = [
        "Samina Saeed", "Bilquees Gul", "Zahid Ali", "Muhammad Sarfaraz Ali Metlo", 
        "Zaeema Asrar Mohiuddin", "Fareeda Islam", "Muhammad Harris Shoaib", 
        "Bilquees Gul", "Samina Saeed"
    ]
    for idx, name in enumerate(dean_names):
        url = f"https://ui-avatars.com/api/?name={name.replace(' ', '+')}&size=256&background=random"
        download_image(url, os.path.join(demo_3_admin, f"dean_{idx}.png"))
        download_image(url, os.path.join(uok_stadum_admin, f"dean_{idx}.png"))
        download_image(url, os.path.join(root_assets_admin, f"dean_{idx}.png"))
        
    print("Images copied successfully!")

if __name__ == "__main__":
    main()
