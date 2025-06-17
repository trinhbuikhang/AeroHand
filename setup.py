"""
Setup script for AeroHand
Kiểm tra và cài đặt dependencies
"""

import subprocess
import sys
import os

def check_python_version():
    """Kiểm tra phiên bản Python"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 trở lên là bắt buộc!")
        print(f"   Phiên bản hiện tại: {sys.version}")
        return False
    print(f"✅ Python {sys.version.split()[0]} - OK")
    return True

def install_package(package):
    """Cài đặt package"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError:
        return False

def check_and_install_dependencies():
    """Kiểm tra và cài đặt dependencies"""
    dependencies = [
        "opencv-python==4.8.1.78",
        "mediapipe==0.10.7", 
        "pyautogui==0.9.54",
        "numpy==1.24.3",
        "pillow==10.0.1"
    ]
    
    print("\n📦 Checking and installing dependencies...")
    
    for dep in dependencies:
        print(f"   Installing {dep}...")
        if install_package(dep):
            print(f"   ✅ {dep} - Installed successfully")
        else:
            print(f"   ❌ {dep} - Installation failed")
            return False
    
    return True

def check_camera():
    """Kiểm tra webcam"""
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            ret, _ = cap.read()
            cap.release()
            if ret:
                print("✅ Webcam - OK")
                return True
            else:
                print("⚠️  Webcam found but cannot read frames")
                return False
        else:
            print("❌ Webcam not found or inaccessible")
            return False
    except ImportError:
        print("⚠️  Cannot check webcam (OpenCV not installed)")
        return False

def main():
    """Hàm main"""
    print("=" * 50)
    print("🚀 AeroHand Setup Script")
    print("=" * 50)
    
    # Kiểm tra Python version
    if not check_python_version():
        input("Press Enter to exit...")
        return
    
    # Cài đặt dependencies
    if not check_and_install_dependencies():
        print("\n❌ Failed to install dependencies!")
        input("Press Enter to exit...")
        return
    
    # Kiểm tra camera
    print("\n📹 Checking webcam...")
    check_camera()
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed!")
    print("=" * 50)
    print("\nYou can now run AeroHand:")
    print("   • Double-click run_aerohand.bat")
    print("   • Or run: python main.py")
    print("\nEnjoy using AeroHand! 🎯")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
