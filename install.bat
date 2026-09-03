@echo off
echo ========================================
echo  Personal AI Assistant - Install
echo ========================================

echo.
echo [1/3] Creating Python virtual environment...
cd backend
if not exist venv (
  python -m venv venv
)
call venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt
cd ..

echo.
echo [2/3] Installing frontend dependencies...
cd frontend
call npm install
cd ..

echo.
echo [3/3] Installing Electron dependencies...
cd electron
call npm install
cd ..

if not exist .env (
  copy .env.example .env
  echo.
  echo Created .env – please edit it and add your OPENAI_API_KEY
)

echo.
echo Done! Edit .env then run start.bat
pause
