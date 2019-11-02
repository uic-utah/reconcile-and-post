@echo off
echo activating python environment
call "C:\Program Files\ArcGIS\Pro\bin\Python\Scripts\propy.bat" -m rnp --action=reconcile
call "C:\Program Files\ArcGIS\Pro\bin\Python\Scripts\propy.bat" -m rnp --action=delete

pause
