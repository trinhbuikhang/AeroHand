@echo off
echo =========================================
echo    AeroHand Installation Script
echo =========================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo Python found! Installing dependencies...
echo.

echo Installing required packages...
pip install -r requirements.txt

if errorlevel 1 (
    echo ERROR: Failed to install dependencies!
    echo Please check your internet connection and try again.
    pause
    exit /b 1
)

echo.
echo =========================================
echo    Installation completed successfully!
echo =========================================
echo.
echo You can now run AeroHand by double-clicking run_aerohand.bat
echo or by running: python main.py
echo.
pause
