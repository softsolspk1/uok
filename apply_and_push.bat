@echo off
echo Running Python script to add ICCBS link to the Research header menu...
python add_iccs_menu.py
echo.
echo Committing and pushing changes to git to trigger Vercel...
git add .
git commit -m "feat: add ICCBS link to Research header menu across all pages"
git push
echo.
echo Done! Please check Vercel for the deployment.
pause
