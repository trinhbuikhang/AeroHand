@echo off
chcp 65001 >nul
title AeroHand Management Tool
color 0A

:MAIN_MENU
cls
echo.
echo ══════════════════════════════════════════════════════════════
echo  🚁 AeroHand - Gesture Mouse Control Management Tool
echo ══════════════════════════════════════════════════════════════
echo.
echo  Choose an option / Chọn một tùy chọn:
echo.
echo  1. 🚀 Launch AeroHand (GUI Launcher)
echo  2. 🎮 Run AeroHand (Direct)
echo  3. 🎬 Demo Mode (Safe Testing)
echo  4. 🔍 System Compatibility Check
echo  5. 📡 Camera Server (for Network Camera)
echo  6. 🌐 Scan Network for Cameras
echo  7. 🧪 Test Components
echo  8. 📦 Install/Update Dependencies
echo  9. 📖 Help & Documentation
echo  0. ❌ Exit
echo.
echo ══════════════════════════════════════════════════════════════
set /p choice="Enter your choice (0-9): "

if "%choice%"=="1" goto LAUNCHER
if "%choice%"=="2" goto RUN_DIRECT
if "%choice%"=="3" goto DEMO
if "%choice%"=="4" goto SYSTEM_CHECK
if "%choice%"=="5" goto CAMERA_SERVER
if "%choice%"=="6" goto SCAN_NETWORK
if "%choice%"=="7" goto TEST_COMPONENTS
if "%choice%"=="8" goto INSTALL_DEPS
if "%choice%"=="9" goto HELP
if "%choice%"=="0" goto EXIT

echo Invalid choice. Please try again.
timeout /t 2 >nul
goto MAIN_MENU

:LAUNCHER
echo.
echo 🚀 Starting GUI Launcher...
python launcher.py
pause
goto MAIN_MENU

:RUN_DIRECT
echo.
echo 🎮 Starting AeroHand directly...
echo.
echo Options:
echo 1. Local Camera
echo 2. Network Camera
echo 3. Demo Mode
echo 4. Scan Network First
echo.
set /p run_choice="Choose option (1-4): "

if "%run_choice%"=="1" (
    python main.py
) else if "%run_choice%"=="2" (
    set /p camera_ip="Enter camera IP address: "
    python main.py --camera-ip %camera_ip%
) else if "%run_choice%"=="3" (
    python main.py --demo
) else if "%run_choice%"=="4" (
    python main.py --scan-network
) else (
    echo Invalid option
)
pause
goto MAIN_MENU

:DEMO
echo.
echo 🎬 Starting Demo Mode...
echo This mode is safe for testing - no mouse control
python demo.py
pause
goto MAIN_MENU

:SYSTEM_CHECK
echo.
echo 🔍 Running System Compatibility Check...
python utils/system_check.py
goto MAIN_MENU

:CAMERA_SERVER
echo.
echo 📡 Starting Camera Server...
echo This will start a server to share your camera over network
echo Press Ctrl+C to stop the server
echo.
python camera_server.py
pause
goto MAIN_MENU

:SCAN_NETWORK
echo.
echo 🌐 Scanning network for camera servers...
python network_scanner.py
pause
goto MAIN_MENU

:TEST_COMPONENTS
echo.
echo 🧪 Testing All Components...
python test_components.py
goto MAIN_MENU

:INSTALL_DEPS
echo.
echo 📦 Installing/Updating Dependencies...
echo.
echo Upgrading pip...
python -m pip install --upgrade pip
echo.
echo Installing requirements...
pip install -r requirements.txt
echo.
echo Installation complete!
pause
goto MAIN_MENU

:HELP
cls
echo.
echo ══════════════════════════════════════════════════════════════
echo  📖 AeroHand Help & Documentation
echo ══════════════════════════════════════════════════════════════
echo.
echo  📄 Available Documentation:
echo.
echo  • README.md - Main documentation
echo  • TECHNICAL.md - Technical details
echo  • TROUBLESHOOTING.md - Problem solving guide
echo.
echo  🚀 Quick Start:
echo  1. Run System Check first (option 4)
echo  2. If local camera works: Use GUI Launcher (option 1)
echo  3. If no local camera: Use Camera Server on another device
echo  4. For testing: Use Demo Mode (option 3)
echo.
echo  🔧 Troubleshooting:
echo  • No camera detected? Try Network Camera
echo  • Performance issues? Check TROUBLESHOOTING.md
echo  • Installation problems? Run option 8
echo.
echo  📱 Network Camera Setup:
echo  1. Install AeroHand on device with camera
echo  2. Run Camera Server (option 5) on that device
echo  3. Note the IP address shown
echo  4. Use that IP in Network Camera option
echo.
echo ══════════════════════════════════════════════════════════════
echo.
set /p help_choice="Open documentation? (y/n): "
if /i "%help_choice%"=="y" (
    start README.md
    start TECHNICAL.md
    start TROUBLESHOOTING.md
)
goto MAIN_MENU

:EXIT
echo.
echo Thank you for using AeroHand! 👋
echo Cảm ơn bạn đã sử dụng AeroHand!
timeout /t 2 >nul
exit /b 0
