"""
Camera Manager Module
Quản lý webcam và capture video frames
"""

import cv2
import logging
import socket
import numpy as np
from typing import Tuple, Optional
from config.settings import CAMERA_INDEX, CAMERA_WIDTH, CAMERA_HEIGHT, FPS

class NetworkCameraClient:
    """Client để kết nối đến camera server qua mạng"""
    
    def __init__(self, server_ip: str, server_port: int = 8080):
        self.server_ip = server_ip
        self.server_port = server_port
        self.socket = None
        self.connected = False
        self.logger = logging.getLogger(__name__)
        
    def connect(self) -> bool:
        """Kết nối đến camera server"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(10)  # 10 second timeout
            self.socket.connect((self.server_ip, self.server_port))
            self.connected = True
            self.logger.info(f"Đã kết nối đến camera server: {self.server_ip}:{self.server_port}")
            return True
        except Exception as e:
            self.logger.error(f"Không thể kết nối đến camera server: {e}")
            return False
    
    def read_frame(self) -> Tuple[bool, Optional[np.ndarray]]:
        """Đọc frame từ camera server"""
        if not self.connected or self.socket is None:
            return False, None
        
        try:
            # Đọc kích thước frame (4 bytes)
            size_data = b''
            while len(size_data) < 4:
                chunk = self.socket.recv(4 - len(size_data))
                if not chunk:
                    return False, None
                size_data += chunk
            
            frame_size = int.from_bytes(size_data, byteorder='big')
            
            # Đọc frame data
            frame_data = b''
            while len(frame_data) < frame_size:
                chunk = self.socket.recv(min(4096, frame_size - len(frame_data)))
                if not chunk:
                    return False, None
                frame_data += chunk
            
            # Decode frame
            frame_array = np.frombuffer(frame_data, dtype=np.uint8)
            frame = cv2.imdecode(frame_array, cv2.IMREAD_COLOR)
            
            if frame is not None:
                # Flip frame để có hiệu ứng gương (đã flip ở server rồi thì không cần)
                # frame = cv2.flip(frame, 1)
                return True, frame
            else:
                return False, None
                
        except Exception as e:
            self.logger.error(f"Lỗi đọc frame từ network camera: {e}")
            self.connected = False
            return False, None
    
    def disconnect(self):
        """Ngắt kết nối"""
        self.connected = False
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
            self.socket = None
        self.logger.info("Đã ngắt kết nối camera server")

class CameraManager:
    """Quản lý webcam và các thao tác liên quan đến camera (hỗ trợ cả local và network camera)"""
    
    def __init__(self):
        self.cap = None
        self.network_client = None
        self.is_opened = False
        self.is_network_camera = False
        self.logger = logging.getLogger(__name__)
        
    def initialize_camera(self, camera_source: str = "local") -> bool:
        """
        Khởi tạo camera (local hoặc network)
        
        Args:
            camera_source: "local" hoặc IP address của network camera
            
        Returns:
            bool: True nếu khởi tạo thành công
        """
        if camera_source == "local":
            return self._initialize_local_camera()
        else:
            return self._initialize_network_camera(camera_source)
    def _initialize_local_camera(self) -> bool:
        """Khởi tạo local camera với robust backend detection"""
        backends = [
            (cv2.CAP_DSHOW, "DirectShow"),
            (cv2.CAP_MSMF, "Microsoft Media Foundation"),
            (cv2.CAP_ANY, "Auto")
        ]
        
        for backend_id, backend_name in backends:
            try:
                self.logger.info(f"Trying camera with {backend_name} backend...")
                self.cap = cv2.VideoCapture(CAMERA_INDEX, backend_id)
                
                if not self.cap.isOpened():
                    self.logger.warning(f"Cannot open camera with {backend_name}")
                    continue
                
                # Cấu hình camera
                self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
                self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
                self.cap.set(cv2.CAP_PROP_FPS, FPS)
                
                # Test đọc frame nhiều lần để đảm bảo ổn định
                success_count = 0
                for i in range(5):
                    ret, frame = self.cap.read()
                    if ret and frame is not None:
                        success_count += 1
                
                if success_count >= 3:
                    # Kiểm tra độ phân giải thực tế
                    actual_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                    actual_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    actual_fps = int(self.cap.get(cv2.CAP_PROP_FPS))
                    
                    self.logger.info(f"Local camera initialized with {backend_name}: {actual_width}x{actual_height} @ {actual_fps}fps")
                    self.logger.info(f"Camera stability test: {success_count}/5 frames successful")
                    
                    self.is_opened = True
                    self.is_network_camera = False
                    return True
                else:
                    self.logger.warning(f"{backend_name}: Poor frame capture rate ({success_count}/5)")
                    self.cap.release()
                    
            except Exception as e:
                self.logger.error(f"Error with {backend_name} backend: {e}")
                if hasattr(self, 'cap') and self.cap is not None:
                    try:
                        self.cap.release()
                    except:
                        pass
                continue
        
        # Nếu tất cả backend thất bại, thử với camera index khác
        self.logger.info("Trying different camera indices...")
        for camera_idx in range(0, 4):
            if camera_idx == CAMERA_INDEX:
                continue  # Đã thử rồi
                
            try:
                self.logger.info(f"Trying camera index {camera_idx}...")
                self.cap = cv2.VideoCapture(camera_idx, cv2.CAP_DSHOW)
                
                if self.cap.isOpened():
                    ret, frame = self.cap.read()
                    if ret and frame is not None:
                        self.logger.info(f"Found working camera at index {camera_idx}")
                        
                        # Cấu hình camera
                        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
                        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
                        self.cap.set(cv2.CAP_PROP_FPS, FPS)
                        
                        self.is_opened = True
                        self.is_network_camera = False
                        return True
                    else:
                        self.cap.release()
                else:
                    if hasattr(self, 'cap') and self.cap is not None:
                        self.cap.release()
                        
            except Exception as e:
                self.logger.error(f"Error with camera index {camera_idx}: {e}")
                if hasattr(self, 'cap') and self.cap is not None:
                    try:
                        self.cap.release()
                    except:
                        pass
                continue
        
        self.logger.error("Failed to initialize any local camera")
        return False
    
    def _initialize_network_camera(self, server_ip: str, server_port: int = 8080) -> bool:
        """
        Khởi tạo network camera
        
        Args:
            server_ip: IP address của camera server
            server_port: Port của camera server
            
        Returns:
            bool: True nếu kết nối thành công
        """
        try:
            self.network_client = NetworkCameraClient(server_ip, server_port)
            
            if not self.network_client.connect():
                return False
            
            # Test đọc frame đầu tiên
            ret, frame = self.network_client.read_frame()
            if not ret or frame is None:
                self.logger.error("Không thể đọc frame từ network camera")
                self.network_client.disconnect()
                return False
            
            self.is_opened = True
            self.is_network_camera = True
            self.logger.info(f"Network camera initialized: {server_ip}:{server_port}")
            return True
            
        except Exception as e:
            self.logger.error(f"Lỗi khi khởi tạo network camera: {e}")
            return False
    
    def read_frame(self) -> Tuple[bool, Optional[np.ndarray]]:
        """
        Đọc frame từ camera (local hoặc network)
        
        Returns:
            Tuple[bool, Optional[np.ndarray]]: (success, frame)
        """
        if not self.is_opened:
            return False, None
        
        try:
            if self.is_network_camera and self.network_client:
                # Đọc từ network camera
                ret, frame = self.network_client.read_frame()
                if ret and frame is not None:
                    # Resize nếu cần
                    if frame.shape[1] != CAMERA_WIDTH or frame.shape[0] != CAMERA_HEIGHT:
                        frame = cv2.resize(frame, (CAMERA_WIDTH, CAMERA_HEIGHT))
                return ret, frame
            elif self.cap is not None:
                # Đọc từ local camera
                ret, frame = self.cap.read()
                if ret:
                    # Flip frame horizontally để có hiệu ứng gương
                    frame = cv2.flip(frame, 1)
                return ret, frame
            else:
                return False, None
                
        except Exception as e:
            self.logger.error(f"Lỗi khi đọc frame: {e}")
            return False, None
    
    def get_frame_dimensions(self) -> Tuple[int, int]:
        """
        Lấy kích thước frame
        
        Returns:
            Tuple[int, int]: (width, height)
        """
        return CAMERA_WIDTH, CAMERA_HEIGHT
    
    def release(self):
        """Giải phóng tài nguyên camera"""
        self.is_opened = False
        
        if self.is_network_camera and self.network_client:
            self.network_client.disconnect()
            self.network_client = None
            self.logger.info("Network camera released")
        elif self.cap is not None:
            self.cap.release()
            self.logger.info("Local camera released")
        
        self.cap = None
        self.is_network_camera = False
    
    def is_available(self) -> bool:
        """
        Kiểm tra camera có sẵn sàng không
        
        Returns:
            bool: True nếu camera sẵn sàng
        """
        if self.is_network_camera:
            return self.is_opened and self.network_client and self.network_client.connected
        else:
            return self.is_opened and self.cap is not None and self.cap.isOpened()
    
    @staticmethod
    def check_camera_availability(camera_index: int = CAMERA_INDEX) -> bool:
        """
        Kiểm tra tính khả dụng của local camera
        
        Args:
            camera_index: Index của camera cần kiểm tra
            
        Returns:
            bool: True nếu camera khả dụng
        """
        try:
            test_cap = cv2.VideoCapture(camera_index)
            if test_cap.isOpened():
                ret, _ = test_cap.read()
                test_cap.release()
                return ret
            return False
        except Exception:
            return False
    
    @staticmethod
    def test_network_connection(ip_address: str, port: int = 8080, timeout: int = 5) -> bool:
        """
        Test kết nối network đến camera server
        
        Args:
            ip_address: IP address cần test
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
    
    def get_camera_info(self) -> dict:
        """
        Lấy thông tin camera hiện tại
        
        Returns:
            dict: Thông tin camera
        """
        info = {
            "is_opened": self.is_opened,
            "is_network_camera": self.is_network_camera,
            "width": CAMERA_WIDTH,
            "height": CAMERA_HEIGHT,
            "fps": FPS
        }
        
        if self.is_network_camera and self.network_client:
            info["server_ip"] = self.network_client.server_ip
            info["server_port"] = self.network_client.server_port
            info["connected"] = self.network_client.connected
        
        return info
