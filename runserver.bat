@echo off
cd /d D:\desarrollos\propios\Net\env\Scripts & activate.bat & cd /d D:\desarrollos\propios\Net & python manage.py runserver & timeout /t 3 /nobreak & start "chrome.exe" http://localhost:8000