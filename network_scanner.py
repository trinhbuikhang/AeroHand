"""
Network Camera Scanner
Script để quét mạng và tìm camera servers
"""

import socket
import threading
import time
import argparse
from modules.camera_manager import CameraManager

class NetworkScanner:
    """Class để scan network tìm camera servers"""
    
    def __init__(self, network_prefix="192.168.14", port=8080, timeout=2):
        self.network_prefix = network_prefix
        self.port = port
        self.timeout = timeout
        self.found_servers = []
        self.scan_complete = False
        
    def test_ip(self, ip):
        """Test một IP address"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            result = sock.connect_ex((ip, self.port))
            sock.close()
            
            if result == 0:
                self.found_servers.append(ip)
                print(f"📹 Found camera server at: {ip}:{self.port}")
                
        except Exception:
            pass
    
    def scan_network(self):
        """Scan toàn bộ network"""
        print("=" * 60)
        print("📡 AeroHand Network Camera Scanner")
        print("=" * 60)
        print(f"🔍 Scanning network: {self.network_prefix}.1-254")
        print(f"🔌 Port: {self.port}")
        print(f"⏱️  Timeout: {self.timeout}s per IP")
        print("=" * 60)
        print("⏳ Scanning... This may take a moment...")
        
        start_time = time.time()
        threads = []
        
        # Tạo threads để scan song song
        for i in range(1, 255):
            ip = f"{self.network_prefix}.{i}"
            thread = threading.Thread(target=self.test_ip, args=(ip,))
            thread.daemon = True
            thread.start()
            threads.append(thread)
            
            # Giới hạn số threads đồng thời
            if len(threads) >= 50:
                for t in threads:
                    t.join()
                threads = []
        
        # Đợi threads còn lại
        for thread in threads:
            thread.join()
        
        scan_time = time.time() - start_time
        self.scan_complete = True
        
        print("=" * 60)
        print(f"✅ Scan completed in {scan_time:.1f} seconds")
        
        if self.found_servers:
            print(f"🎉 Found {len(self.found_servers)} camera server(s):")
            for server in self.found_servers:
                print(f"   📹 {server}:{self.port}")
        else:
            print("❌ No camera servers found")
            print("\n💡 Tips:")
            print("   • Make sure camera server is running on the target machine")
            print("   • Check if the port 8080 is correct")
            print("   • Verify network connectivity")
            print("   • Try different network prefix if needed")
        
        print("=" * 60)
        return self.found_servers
    
    def test_specific_ip(self, ip):
        """Test một IP cụ thể"""
        print(f"🔍 Testing connection to {ip}:{self.port}...")
        
        if CameraManager.test_network_connection(ip, self.port, self.timeout):
            print(f"✅ Connection successful to {ip}:{self.port}")
            return True
        else:
            print(f"❌ Cannot connect to {ip}:{self.port}")
            return False

def main():
    parser = argparse.ArgumentParser(description="AeroHand Network Camera Scanner")
    parser.add_argument("--network", default="192.168.14", 
                       help="Network prefix to scan (default: 192.168.14)")
    parser.add_argument("--port", type=int, default=8080,
                       help="Port to scan (default: 8080)")
    parser.add_argument("--timeout", type=int, default=2,
                       help="Timeout per IP in seconds (default: 2)")
    parser.add_argument("--ip", help="Test specific IP address only")
    parser.add_argument("--quick", action="store_true",
                       help="Quick scan with shorter timeout")
    
    args = parser.parse_args()
    
    if args.quick:
        args.timeout = 1
    
    scanner = NetworkScanner(args.network, args.port, args.timeout)
    
    if args.ip:
        # Test specific IP
        scanner.test_specific_ip(args.ip)
    else:
        # Scan entire network
        found_servers = scanner.scan_network()
        
        if found_servers:
            print("\n🚀 Ready to use AeroHand with network camera!")
            print("📋 Next steps:")
            print("   1. Choose a camera server IP from the list above")
            print("   2. Run AeroHand with network camera:")
            print(f"      python main.py --camera-ip {found_servers[0]}")
            print("   3. Or use the GUI launcher and select network camera")

if __name__ == "__main__":
    main()
