@echo off
echo Starting Personal AI Assistant...

start "Backend" cmd /k "cd backend && call venv\Scripts\activate.bat && python run.py"
timeout /t 3 /nobreak >nul

start "Frontend" cmd /k "cd frontend && npm run dev"
timeout /t 2 /nobreak >nul

start "Electron" cmd /k "cd electron && npm start"

echo All processes launched.
echo Close the windows to stop.
pause
