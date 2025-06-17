"""
Network Camera Module
Module để kết nối với camera qua mạng (IP camera hoặc camera streaming)
"""

import cv2
import requests
import numpy as np
import logging
import socket
import threading
import time
from typing import Tuple, Optional, Union
from config.settings import CAMERA_WIDTH, CAMERA_HEIGHT, FPS

class NetworkCameraManager:
    """Quản lý camera qua mạng"""
    
    def __init__(self):
        self.cap = None
        self.is_opened = False
        self.logger = logging.getLogger(__name__)
        self.stream_url = None
        self.connection_type = None
        
        # Streaming server info
        self.server_running = False
        self.server_thread = None
        
    def connect_to_ip_camera(self, ip_address: str, port: int = 8080, 
                           username: str = None, password: str = None,
                           stream_path: str = "/video") -> bool:
        """
        Kết nối đến IP camera hoặc camera streaming
        
        Args:
            ip_address: Địa chỉ IP của camera
            port: Port của camera stream
            username: Username (nếu có authentication)
            password: Password (nếu có authentication)
            stream_path: Đường dẫn stream (thường là /video hoặc /mjpeg)
            
        Returns:
            bool: True nếu kết nối thành công
        """
        try:
            # Tạo URL stream
            if username and password:
                self.stream_url = f"http://{username}:{password}@{ip_address}:{port}{stream_path}"
            else:
                self.stream_url = f"http://{ip_address}:{port}{stream_path}"
            
            self.logger.info(f"Đang kết nối đến camera: {ip_address}:{port}")
            
            # Thử kết nối
            self.cap = cv2.VideoCapture(self.stream_url)
            
            if not self.cap.isOpened():
                self.logger.error(f"Không thể kết nối đến camera: {self.stream_url}")
                return False
            
            # Test đọc frame
            ret, frame = self.cap.read()
            if not ret:
                self.logger.error("Không thể đọc frame từ camera")
                self.cap.release()
                return False
            
            self.connection_type = "ip_camera"
            self.is_opened = True
            self.logger.info(f"Kết nối thành công đến IP camera: {ip_address}:{port}")
            return True
            
        except Exception as e:
            self.logger.error(f"Lỗi khi kết nối IP camera: {e}")
            return False
    
    def connect_to_mjpeg_stream(self, stream_url: str) -> bool:
        """
        Kết nối đến MJPEG stream
        
        Args:
            stream_url: URL của MJPEG stream
            
        Returns:
            bool: True nếu kết nối thành công
        """
        try:
            self.stream_url = stream_url
            self.logger.info(f"Đang kết nối đến MJPEG stream: {stream_url}")
            
            self.cap = cv2.VideoCapture(stream_url)
            
            if not self.cap.isOpened():
                self.logger.error(f"Không thể kết nối đến MJPEG stream: {stream_url}")
                return False
            
            # Test frame
            ret, frame = self.cap.read()
            if not ret:
                self.logger.error("Không thể đọc frame từ MJPEG stream")
                self.cap.release()
                return False
            
            self.connection_type = "mjpeg_stream"
            self.is_opened = True
            self.logger.info(f"Kết nối thành công đến MJPEG stream")
            return True
            
        except Exception as e:
            self.logger.error(f"Lỗi khi kết nối MJPEG stream: {e}")
            return False
    
    def read_frame(self) -> Tuple[bool, Optional[np.ndarray]]:
        """
        Đọc frame từ network camera
        
        Returns:
            Tuple[bool, Optional[np.ndarray]]: (success, frame)
        """
        if not self.is_opened or self.cap is None:
            return False, None
        
        try:
            ret, frame = self.cap.read()
            if ret and frame is not None:
                # Flip frame để có hiệu ứng gương
                frame = cv2.flip(frame, 1)
                
                # Resize nếu cần
                if frame.shape[1] != CAMERA_WIDTH or frame.shape[0] != CAMERA_HEIGHT:
                    frame = cv2.resize(frame, (CAMERA_WIDTH, CAMERA_HEIGHT))
                
            return ret, frame
        except Exception as e:
            self.logger.error(f"Lỗi khi đọc frame từ network camera: {e}")
            return False, None
    
    def get_frame_dimensions(self) -> Tuple[int, int]:
        """
        Lấy kích thước frame
        
        Returns:
            Tuple[int, int]: (width, height)
        """
        if not self.is_opened or self.cap is None:
            return CAMERA_WIDTH, CAMERA_HEIGHT
        
        return CAMERA_WIDTH, CAMERA_HEIGHT
    
    def release(self):
        """Giải phóng tài nguyên"""
        if self.cap is not None:
            self.cap.release()
            self.is_opened = False
            self.logger.info("Network camera released")
    
    def is_available(self) -> bool:
        """
        Kiểm tra camera có sẵn sàng không
        
        Returns:
            bool: True nếu camera sẵn sàng
        """
        return self.is_opened and self.cap is not None
    
    @staticmethod
    def test_connection(ip_address: str, port: int = 8080, timeout: int = 5) -> bool:
        """
        Test kết nối đến IP address và port
        
        Args:
            ip_address: Địa chỉ IP cần test
            port: Port cần test
            timeout: Timeout (giây)
            
        Returns:
            bool: True nếu có thể kết nối
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((ip_address, port))
            sock.close()
            return result == 0
        except Exception:
            return False
    
    @staticmethod
    def scan_network_cameras(network_prefix: str = "192.168.14", 
                           port: int = 8080, 
                           timeout: int = 1) -> list:
        """
        Quét mạng để tìm camera
        
        Args:
            network_prefix: Prefix mạng (vd: "192.168.14")
            port: Port để scan
            timeout: Timeout cho mỗi IP
            
        Returns:
            list: Danh sách IP có camera
        """
        available_cameras = []
        
        def check_ip(ip):
            if NetworkCameraManager.test_connection(ip, port, timeout):
                available_cameras.append(ip)
        
        threads = []
        for i in range(1, 255):
            ip = f"{network_prefix}.{i}"
            thread = threading.Thread(target=check_ip, args=(ip,))
            thread.daemon = True
            thread.start()
            threads.append(thread)
        
        # Đợi tất cả threads hoàn thành
        for thread in threads:
            thread.join()
        
        return available_cameras

class CameraServer:
    """
    Server để stream camera từ máy có camera
    Chạy trên máy có camera để stream cho máy khác
    """
    
    def __init__(self, camera_index: int = 0, port: int = 8080):
        self.camera_index = camera_index
        self.port = port
        self.logger = logging.getLogger(__name__)
        self.cap = None
        self.server_running = False
        
    def start_server(self):
        """Khởi động camera server"""
        try:
            from flask import Flask, Response
            import io
            
            app = Flask(__name__)
            
            # Khởi tạo camera
            self.cap = cv2.VideoCapture(self.camera_index)
            if not self.cap.isOpened():
                self.logger.error(f"Không thể mở camera {self.camera_index}")
                return False
            
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
            self.cap.set(cv2.CAP_PROP_FPS, FPS)
            
            def generate_frames():
                while self.server_running:
                    ret, frame = self.cap.read()
                    if not ret:
                        break
                    
                    # Encode frame thành JPEG
                    _, buffer = cv2.imencode('.jpg', frame, 
                                           [cv2.IMWRITE_JPEG_QUALITY, 90])
                    frame_bytes = buffer.tobytes()
                    
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            
            @app.route('/video')
            def video_feed():
                return Response(generate_frames(),
                              mimetype='multipart/x-mixed-replace; boundary=frame')
            
            @app.route('/status')
            def status():
                return {'status': 'running', 'camera_index': self.camera_index}
            
            self.server_running = True
            self.logger.info(f"Camera server starting on port {self.port}")
            
            # Chạy Flask server
            app.run(host='0.0.0.0', port=self.port, debug=False, threaded=True)
            
        except ImportError:
            self.logger.error("Flask không được cài đặt. Chạy: pip install flask")
            return False
        except Exception as e:
            self.logger.error(f"Lỗi khi khởi động camera server: {e}")
            return False
    
    def stop_server(self):
        """Dừng camera server"""
        self.server_running = False
        if self.cap:
            self.cap.release()
        self.logger.info("Camera server stopped")
