"""
Test script for AeroHand components
Kiểm tra tất cả components có hoạt động không
"""

import sys
import os

def test_imports():
    """Test import các modules"""
    print("🧪 Testing imports...")
    
    try:
        import cv2
        print("✅ OpenCV imported successfully")
    except ImportError as e:
        print(f"❌ OpenCV import failed: {e}")
        return False
    
    try:
        import mediapipe as mp
        print("✅ MediaPipe imported successfully")
    except ImportError as e:
        print(f"❌ MediaPipe import failed: {e}")
        return False
    
    try:
        import pyautogui
        print("✅ PyAutoGUI imported successfully")
    except ImportError as e:
        print(f"❌ PyAutoGUI import failed: {e}")
        return False
    
    try:
        import numpy as np
        print("✅ NumPy imported successfully")
    except ImportError as e:
        print(f"❌ NumPy import failed: {e}")
        return False
    
    return True

def test_camera():
    """Test webcam"""
    print("\n📹 Testing webcam...")
    
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("❌ Cannot open webcam")
            return False
        
        ret, frame = cap.read()
        if not ret:
            print("❌ Cannot read from webcam")
            cap.release()
            return False
        
        height, width = frame.shape[:2]
        print(f"✅ Webcam working - Resolution: {width}x{height}")
        
        cap.release()
        return True
        
    except Exception as e:
        print(f"❌ Webcam test failed: {e}")
        return False

def test_mediapipe():
    """Test MediaPipe hand detection"""
    print("\n🖐️ Testing MediaPipe hand detection...")
    
    try:
        import mediapipe as mp
        
        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands(
            static_image_mode=True,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        
        print("✅ MediaPipe hands initialized successfully")
        hands.close()
        return True
        
    except Exception as e:
        print(f"❌ MediaPipe test failed: {e}")
        return False

def test_mouse_control():
    """Test mouse control"""
    print("\n🖱️ Testing mouse control...")
    
    try:
        import pyautogui
        
        # Get screen size
        screen_width, screen_height = pyautogui.size()
        print(f"✅ Screen size: {screen_width}x{screen_height}")
        
        # Get current mouse position
        x, y = pyautogui.position()
        print(f"✅ Current mouse position: ({x}, {y})")
        
        # Test moving mouse (small movement)
        pyautogui.move(5, 5)
        pyautogui.move(-5, -5)
        print("✅ Mouse movement test successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Mouse control test failed: {e}")
        return False

def test_project_structure():
    """Test project structure"""
    print("\n📁 Testing project structure...")
    
    required_files = [
        "main.py",
        "requirements.txt",
        "README.md",
        "config/settings.py",
        "modules/hand_tracking.py",
        "modules/camera_manager.py",
        "utils/gesture.py",
        "utils/mouse_control.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    else:
        print("✅ All required files present")
        return True

def main():
    """Main test function"""
    print("=" * 60)
    print("🚀 AeroHand Component Test")
    print("=" * 60)
    
    all_tests_passed = True
    
    # Test project structure
    if not test_project_structure():
        all_tests_passed = False
    
    # Test imports
    if not test_imports():
        all_tests_passed = False
        print("\n❌ Cannot proceed with other tests due to import failures")
        print("   Please run 'pip install -r requirements.txt' first")
    else:
        # Test camera
        if not test_camera():
            all_tests_passed = False
        
        # Test MediaPipe
        if not test_mediapipe():
            all_tests_passed = False
        
        # Test mouse control
        if not test_mouse_control():
            all_tests_passed = False
    
    print("\n" + "=" * 60)
    if all_tests_passed:
        print("🎉 All tests passed! AeroHand is ready to use.")
        print("   Run 'python main.py' to start the application")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        print("   Try running 'python setup.py' to fix dependencies")
    print("=" * 60)
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
