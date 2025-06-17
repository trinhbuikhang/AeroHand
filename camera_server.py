"""
Camera Server - Standalone script để chạy trên máy có camera
Chạy script này trên máy có camera để stream cho máy khác
"""

import cv2
import socket
import threading
import time
import argparse
import sys

class SimpleCameraServer:
    """Simple camera server không cần Flask"""
    
    def __init__(self, camera_index=0, port=8080):
        self.camera_index = camera_index
        self.port = port
        self.running = False
        self.cap = None
        
    def get_local_ip(self):
        """Lấy IP địa phương"""
        try:
            # Kết nối đến một địa chỉ external để lấy local IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except Exception:
            return "127.0.0.1"
    
    def handle_client(self, client_socket):
        """Xử lý client connection"""
        try:
            while self.running:
                if self.cap is None:
                    break
                
                ret, frame = self.cap.read()
                if not ret:
                    continue
                
                # Encode frame thành JPEG
                _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
                
                # Gửi kích thước frame trước
                frame_size = len(buffer)
                client_socket.sendall(frame_size.to_bytes(4, byteorder='big'))
                
                # Gửi frame data
                client_socket.sendall(buffer.tobytes())
                
                time.sleep(1/30)  # 30 FPS
                
        except Exception as e:
            print(f"Client error: {e}")
        finally:
            client_socket.close()
    
    def start_server(self):
        """Khởi động server"""
        print("=" * 50)
        print("📹 AeroHand Camera Server")
        print("=" * 50)
        
        # Khởi tạo camera
        print(f"Đang khởi tạo camera {self.camera_index}...")
        self.cap = cv2.VideoCapture(self.camera_index)
        
        if not self.cap.isOpened():
            print(f"❌ Không thể mở camera {self.camera_index}")
            return False
        
        # Cấu hình camera
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        
        actual_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        actual_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        print(f"✅ Camera initialized: {actual_width}x{actual_height}")
        
        # Khởi tạo server socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            server_socket.bind(('0.0.0.0', self.port))
            server_socket.listen(5)
            
            local_ip = self.get_local_ip()
            print(f"🌐 Server đang chạy tại: {local_ip}:{self.port}")
            print(f"📡 Để kết nối từ máy khác, sử dụng IP: {local_ip}")
            print("=" * 50)
            print("Để dừng server, nhấn Ctrl+C")
            print("=" * 50)
            
            self.running = True
            
            while self.running:
                try:
                    client_socket, addr = server_socket.accept()
                    print(f"🔌 Client kết nối từ: {addr}")
                    
                    # Tạo thread cho mỗi client
                    client_thread = threading.Thread(
                        target=self.handle_client, 
                        args=(client_socket,)
                    )
                    client_thread.daemon = True
                    client_thread.start()
                    
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    print(f"Server error: {e}")
                    
        except Exception as e:
            print(f"❌ Lỗi khởi tạo server: {e}")
            return False
        finally:
            print("\n🛑 Đang dừng server...")
            self.running = False
            if self.cap:
                self.cap.release()
            server_socket.close()
            print("✅ Server đã dừng")
        
        return True

class NetworkCameraClient:
    """Client để kết nối đến camera server"""
    
    def __init__(self, server_ip, server_port=8080):
        self.server_ip = server_ip
        self.server_port = server_port
        self.socket = None
        self.connected = False
        
    def connect(self):
        """Kết nối đến server"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.server_ip, self.server_port))
            self.connected = True
            print(f"✅ Đã kết nối đến camera server: {self.server_ip}:{self.server_port}")
            return True
        except Exception as e:
            print(f"❌ Không thể kết nối đến server: {e}")
            return False
    
    def read_frame(self):
        """Đọc frame từ server"""
        if not self.connected or self.socket is None:
            return False, None
        
        try:
            # Đọc kích thước frame
            size_data = self.socket.recv(4)
            if len(size_data) != 4:
                return False, None
            
            frame_size = int.from_bytes(size_data, byteorder='big')
            
            # Đọc frame data
            frame_data = b''
            while len(frame_data) < frame_size:
                chunk = self.socket.recv(frame_size - len(frame_data))
                if not chunk:
                    return False, None
                frame_data += chunk
            
            # Decode frame
            import numpy as np
            frame_array = np.frombuffer(frame_data, dtype=np.uint8)
            frame = cv2.imdecode(frame_array, cv2.IMREAD_COLOR)
            
            if frame is not None:
                # Flip frame để có hiệu ứng gương
                frame = cv2.flip(frame, 1)
            
            return True, frame
            
        except Exception as e:
            print(f"Lỗi đọc frame: {e}")
            return False, None
    
    def disconnect(self):
        """Ngắt kết nối"""
        self.connected = False
        if self.socket:
            self.socket.close()

def main():
    parser = argparse.ArgumentParser(description="AeroHand Camera Server")
    parser.add_argument("--camera", type=int, default=0, help="Camera index (default: 0)")
    parser.add_argument("--port", type=int, default=8080, help="Server port (default: 8080)")
    parser.add_argument("--test", action="store_true", help="Test camera before starting server")
    
    args = parser.parse_args()
    
    if args.test:
        print("🧪 Testing camera...")
        cap = cv2.VideoCapture(args.camera)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                print("✅ Camera test successful")
                cv2.imshow("Camera Test", frame)
                cv2.waitKey(2000)
                cv2.destroyAllWindows()
            else:
                print("❌ Cannot read from camera")
            cap.release()
        else:
            print("❌ Cannot open camera")
        return
    
    server = SimpleCameraServer(args.camera, args.port)
    try:
        server.start_server()
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")

if __name__ == "__main__":
    main()
