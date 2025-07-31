@echo off
start py run.py
timeout /t 5 /nobreak > nul
start http://127.0.0.1:5000
pause