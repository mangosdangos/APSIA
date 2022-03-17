git pull
git stage map/map.png
if %ERRORLEVEL% neq 0 exit %ERRORLEVEL%
git commit -m "Updated map."
if %ERRORLEVEL% neq 0 exit %ERRORLEVEL%
git push