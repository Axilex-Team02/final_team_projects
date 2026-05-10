@echo off
setlocal
echo ========================================================
echo AXILEX - Local Project Setup & Runner
echo ========================================================
echo.

cd /d "%~dp0"

:: 1. Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in your PATH.
    echo Please install Python from python.org
    pause
    exit /b
)

:: 2. Create Virtual Environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

:: 3. Activate and Install Requirements
echo Activating virtual environment and installing dependencies...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt

:: 4. Run Database Setup
echo Setting up database...
python database_setup.py

:: 5. Start the Server
echo.
echo ========================================================
echo SUCCESS! Starting the server now...
echo Access the site at http://127.0.0.1:5000
echo ========================================================
echo.

:: Automatically open the browser after a short delay
start http://127.0.0.1:5000/

:: Run the app
python app.py

pause
