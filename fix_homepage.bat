@echo off
git restore homepage.html
python apply_changes.py
git add .
git commit -m "Apply Beige Theme, History Section and Favicon"
git push
