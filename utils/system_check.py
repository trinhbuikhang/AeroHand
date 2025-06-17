"""
System Compatibility Check for AeroHand
Kiểm tra khả năng tương thích hệ thống cho AeroHand
"""

import cv2
import sys
import platform
import socket
import subprocess
from typing import List, Tuple, Dict

def check_python_version() -> Tuple[bool, str]:
    """Kiểm tra phiên bản Python"""
    version = sys.version_info
    required_major, required_minor = 3, 7
    
    if version.major >= required_major and version.minor >= required_minor:
        return True, f"Python {version.major}.{version.minor}.{version.micro}"
    else:
        return False, f"Python {version.major}.{version.minor}.{version.micro} (Yêu cầu Python 3.7+)"

def check_opencv() -> Tuple[bool, str]:
    """Kiểm tra OpenCV"""
    try:
        version = cv2.__version__
        return True, f"OpenCV {version}"
    except Exception as e:
        return False, f"OpenCV error: {str(e)}"

def check_available_cameras() -> List[int]:
    """Kiểm tra camera có sẵn"""
    available_cameras = []
    
    # Thử từ camera index 0 đến 10
    for i in range(10):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            # Thử đọc frame để chắc chắn camera hoạt động
            ret, frame = cap.read()
            if ret and frame is not None:
                available_cameras.append(i)
        cap.release()
    
    return available_cameras

def check_network_connectivity() -> Tuple[bool, str]:
    """Kiểm tra kết nối mạng"""
    try:
        # Thử kết nối tới Google DNS
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True, "Network connection available"
    except OSError:
        return False, "No network connection"

def get_system_info() -> Dict[str, str]:
    """Lấy thông tin hệ thống"""
    return {
        "OS": platform.system(),
        "OS Version": platform.version(),
        "Architecture": platform.architecture()[0],
        "Processor": platform.processor(),
        "Machine": platform.machine()
    }

def check_dependencies() -> Dict[str, Tuple[bool, str]]:
    """Kiểm tra các dependency cần thiết"""
    dependencies = {
        "mediapipe": "mediapipe",
        "numpy": "numpy", 
        "pyautogui": "pyautogui",
        "pillow": "PIL",
        "requests": "requests"
    }
    
    results = {}
    for name, import_name in dependencies.items():
        try:
            __import__(import_name)
            results[name] = (True, "Installed")
        except ImportError:
            results[name] = (False, "Not installed")
    
    return results

def main():
    """Chạy kiểm tra hệ thống"""
    print("=" * 60)
    print("🔍 AeroHand System Compatibility Check")
    print("=" * 60)
    
    # Kiểm tra Python version
    python_ok, python_info = check_python_version()
    status = "✅" if python_ok else "❌"
    print(f"{status} Python Version: {python_info}")
    
    # Kiểm tra OpenCV
    cv_ok, cv_info = check_opencv()
    status = "✅" if cv_ok else "❌"
    print(f"{status} OpenCV: {cv_info}")
    
    # Kiểm tra dependencies
    print("\n📦 Dependencies:")
    deps = check_dependencies()
    all_deps_ok = True
    for name, (ok, info) in deps.items():
        status = "✅" if ok else "❌"
        print(f"  {status} {name}: {info}")
        if not ok:
            all_deps_ok = False
    
    # Kiểm tra camera
    print("\n📹 Camera Detection:")
    cameras = check_available_cameras()
    if cameras:
        print(f"✅ Found {len(cameras)} camera(s): {cameras}")
        for cam_id in cameras:
            print(f"  📷 Camera {cam_id}: Available")
    else:
        print("❌ No cameras detected")
        print("  💡 Tips:")
        print("     - Check if webcam is connected")
        print("     - Try closing other applications using camera")
        print("     - Use network camera if local camera not available")
    
    # Kiểm tra network
    print("\n🌐 Network:")
    net_ok, net_info = check_network_connectivity()
    status = "✅" if net_ok else "❌"
    print(f"{status} {net_info}")
    
    # Thông tin hệ thống
    print("\n💻 System Information:")
    sys_info = get_system_info()
    for key, value in sys_info.items():
        print(f"  {key}: {value}")
    
    # Tổng kết
    print("\n" + "=" * 60)
    overall_ok = python_ok and cv_ok and all_deps_ok
    
    if overall_ok:
        if cameras:
            print("🎉 System is fully compatible with AeroHand!")
            print("   You can run the application with local camera.")
        else:
            print("⚠️  System is compatible but no local camera detected.")
            print("   You can still use network camera feature.")
    else:
        print("❌ System compatibility issues detected.")
        print("   Please install missing dependencies:")
        print("   Run: pip install -r requirements.txt")
    
    print("=" * 60)
    
    return overall_ok and len(cameras) > 0

if __name__ == "__main__":
    main()
    input("\nPress Enter to exit...")
