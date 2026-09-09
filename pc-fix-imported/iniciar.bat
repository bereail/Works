@echo off
cd /d "%~dp0"
start "" http://127.0.0.1:8001/inicio
"%~dp0venv\Scripts\python.exe" -m uvicorn app.main:app --host 127.0.0.1 --port 8001
