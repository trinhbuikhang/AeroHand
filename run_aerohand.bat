@echo off
echo =========================================
echo         AeroHand - Starting...
echo =========================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please run install.bat first or install Python 3.8+
    pause
    exit /b 1
)

echo Starting AeroHand Gesture Mouse Control...
echo.
echo Instructions:
echo - Point with index finger to move cursor
echo - Pinch (index + thumb) for left click  
echo - Make a fist for right click
echo - Press 'q' or ESC to quit
echo.

python main.py

echo.
echo AeroHand has been closed.
pause
