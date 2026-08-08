@echo off
git pull
python copy_images.py
cd site
python assemble_all.py
cd ..
git add .
git commit -m "Update Vercel site templates with admin photos"
git push
