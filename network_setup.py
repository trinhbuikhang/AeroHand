"""
AeroHand Network Setup Guide
Hướng dẫn cài đặt AeroHand với network camera
"""

import os
import sys
import subprocess

def print_banner():
    print("=" * 70)
    print("🌐 AeroHand Network Camera Setup")
    print("=" * 70)
    print()

def print_separator():
    print("-" * 70)

def install_dependencies():
    """Cài đặt dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def show_server_setup():
    """Hiển thị hướng dẫn setup server"""
    print_separator()
    print("🖥️  CAMERA SERVER SETUP (Máy có camera)")
    print_separator()
    print()
    print("1. Chạy trên máy có camera:")
    print("   python camera_server.py")
    print()
    print("2. Hoặc chạy với options:")
    print("   python camera_server.py --camera 0 --port 8080")
    print()
    print("3. Test camera trước khi chạy:")
    print("   python camera_server.py --test")
    print()
    print("📝 Lưu ý:")
    print("   • Camera server sẽ chạy trên port 8080")
    print("   • Cho phép firewall nếu được yêu cầu")
    print("   • Ghi nhớ IP address được hiển thị")
    print()

def show_client_setup():
    """Hiển thị hướng dẫn setup client"""
    print_separator()
    print("💻 AEROHAND CLIENT SETUP (Máy chạy AeroHand)")
    print_separator()
    print()
    print("1. Scan mạng để tìm camera servers:")
    print("   python network_scanner.py")
    print()
    print("2. Test kết nối đến camera server:")
    print("   python network_scanner.py --ip 192.168.14.123")
    print()
    print("3. Chạy AeroHand với network camera:")
    print("   python main.py --camera-ip 192.168.14.123")
    print()
    print("4. Hoặc chạy GUI launcher:")
    print("   python launcher.py")
    print()
    print("📝 Lưu ý:")
    print("   • Thay 192.168.14.123 bằng IP thực tế của camera server")
    print("   • Đảm bảo cả hai máy đều trong cùng mạng")
    print("   • Camera server phải chạy trước")
    print()

def show_quick_start():
    """Hiển thị hướng dẫn quick start"""
    print_separator()
    print("🚀 QUICK START GUIDE")
    print_separator()
    print()
    print("👉 Để sử dụng camera từ máy 192.168.14.123:")
    print()
    print("📋 Trên máy có camera (192.168.14.123):")
    print("   1. Tải AeroHand project")
    print("   2. Chạy: python camera_server.py")
    print("   3. Cho phép firewall nếu được hỏi")
    print("   4. Ghi nhớ IP address được hiển thị")
    print()
    print("📋 Trên máy chạy AeroHand (máy hiện tại):")
    print("   1. Chạy: python network_scanner.py")
    print("   2. Kiểm tra xem có tìm thấy camera server không")
    print("   3. Chạy: python main.py --camera-ip 192.168.14.123")
    print()
    print("🎯 Hoặc sử dụng GUI:")
    print("   python launcher.py")
    print("   → Chọn Network Camera")
    print("   → Nhập IP: 192.168.14.123")
    print()

def show_troubleshooting():
    """Hiển thị hướng dẫn troubleshooting"""
    print_separator()
    print("🔧 TROUBLESHOOTING")
    print_separator()
    print()
    print("❌ Không tìm thấy camera server:")
    print("   • Kiểm tra camera server đã chạy chưa")
    print("   • Kiểm tra firewall/antivirus")
    print("   • Thử ping IP address")
    print("   • Kiểm tra port 8080 có bị block không")
    print()
    print("❌ Kết nối bị từ chối:")
    print("   • Kiểm tra IP address có đúng không")
    print("   • Kiểm tra cả hai máy cùng mạng")
    print("   • Restart camera server")
    print()
    print("❌ Hình ảnh bị lag:")
    print("   • Kiểm tra băng thông mạng")
    print("   • Giảm độ phân giải camera")
    print("   • Sử dụng kết nối ethernet thay vì WiFi")
    print()

def show_advanced_options():
    """Hiển thị các tùy chọn nâng cao"""
    print_separator()
    print("⚙️  ADVANCED OPTIONS")
    print_separator()
    print()
    print("🔧 Camera Server Options:")
    print("   python camera_server.py --camera 0 --port 8080")
    print("   python camera_server.py --help")
    print()
    print("🔧 Network Scanner Options:")
    print("   python network_scanner.py --network 192.168.1 --port 8080")
    print("   python network_scanner.py --quick")
    print("   python network_scanner.py --help")
    print()
    print("🔧 AeroHand Options:")
    print("   python main.py --camera-ip 192.168.14.123 --camera-port 8080")
    print("   python main.py --scan-network")
    print("   python main.py --demo")
    print("   python main.py --help")
    print()

def main():
    print_banner()
    
    print("🎯 Tình huống của bạn:")
    print("   • Máy hiện tại: Không có camera")
    print("   • Máy có camera: 192.168.14.123")
    print("   • Mục tiêu: Sử dụng camera từ xa để chạy AeroHand")
    print()
    
    # Kiểm tra dependencies
    if not os.path.exists("requirements.txt"):
        print("❌ requirements.txt not found!")
        return
    
    # Tùy chọn cài đặt
    install_deps = input("📦 Install dependencies? (y/n): ").lower().strip()
    if install_deps in ['y', 'yes']:
        if not install_dependencies():
            return
    
    show_server_setup()
    show_client_setup()
    show_quick_start()
    show_troubleshooting()
    show_advanced_options()
    
    print_separator()
    print("🎉 Setup complete!")
    print("📖 Refer to the instructions above to get started")
    print("🆘 If you need help, check the troubleshooting section")
    print("=" * 70)

if __name__ == "__main__":
    main()
