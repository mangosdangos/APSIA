git pull -X ours
if %ERRORLEVEL% neq 0 goto onerror
git stage map/map.png
if %ERRORLEVEL% neq 0 goto onerror
git commit -m "Updated map."
if %ERRORLEVEL% neq 0 goto onerror
git push
exit

:onerror
pause
exit %ERRORLEVEL%