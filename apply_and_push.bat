@echo off
echo Running update_menus_bulk.py to apply the simple ICCBS link in uok-stadum...
cd "uok-stadum"
python update_menus_bulk.py
cd ..

echo.
echo Committing and pushing changes to git to trigger Vercel...
git add .
git commit -m "feat: Replace nested ICCBS submenu with simple ICCBS direct link in Research menu"
git push
echo.
echo Done! Please check Vercel for the deployment.
pause
