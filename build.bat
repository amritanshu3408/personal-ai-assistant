@echo off
echo Building Personal AI Assistant...

echo [1] Building frontend...
cd frontend
call npm run build
cd ..

echo [2] (Optional) PyInstaller backend...
cd backend
call venv\Scripts\activate.bat
pyinstaller pyinstaller.spec --noconfirm
cd ..

echo [3] Electron builder...
cd electron
call npm run build
cd ..

echo Build finished. Check electron\dist and backend\dist
pause
