@echo off
cd /d "%~dp0"
"%~dp0venv\Scripts\python.exe" -m uvicorn app.main:app --host 127.0.0.1 --port 8001 >> "%~dp0uvicorn.log" 2>&1
