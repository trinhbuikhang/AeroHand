"""
AeroHand - Gesture Mouse Control Application

Ứng dụng điều khiển chuột bằng cử chỉ tay sử dụng webcam
Tác giả: AeroHand Team
Phiên bản: 1.0.0
"""

import cv2
import numpy as np
import time
import logging
import sys
import argparse
from typing import Optional

# Import các module tự định nghĩa
from modules.camera_manager import CameraManager
from modules.hand_tracking import HandTracker
from utils.mouse_control import MouseController
from utils.gesture import GestureRecognizer
from config.settings import (
    WINDOW_NAME, FONT_SCALE, FONT_THICKNESS, 
    TEXT_COLOR, ERROR_COLOR, GESTURE_COLOR,
    DEBUG_MODE, SHOW_DEBUG_INFO, SHOW_LANDMARKS, SHOW_GESTURE_INFO
)

class AeroHandApp:
    """Class chính của ứng dụng AeroHand"""
    
    def __init__(self, camera_ip: Optional[str] = None, display_scale: float = 1.0):
        """Khởi tạo ứng dụng"""
        self.setup_logging()
        self.logger = logging.getLogger(__name__)
        
        # Camera configuration
        self.camera_ip = camera_ip
        self.is_network_camera = camera_ip is not None
        self.display_scale = display_scale  # Tỉ lệ thu nhỏ cửa sổ hiển thị
        
        # Khởi tạo các components
        self.camera_manager = CameraManager()
        self.hand_tracker = HandTracker()
        self.mouse_controller = MouseController()
        self.gesture_recognizer = GestureRecognizer()
        
        # Trạng thái ứng dụng
        self.is_running = False
        self.fps_counter = 0
        self.fps_start_time = time.time()
        self.current_fps = 0
          # Thông tin hiển thị
        self.status_text = "Initializing..."
        self.gesture_text = "No hand detected"
        
        # Debug info
        self.debug_info = {
            'landmarks_count': 0,
            'pinch_distance': 0.0,
            'fist_confidence': 0.0,
            'gesture_buffer': [],
            'click_cooldown': 0.0,
            'hand_confidence': 0.0
        }
    
    def setup_logging(self):
        """Cấu hình logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(sys.stdout),
                logging.FileHandler('aerohand.log', encoding='utf-8')
            ]
        )
    
    def initialize(self) -> bool:
        """
        Khởi tạo các thành phần của ứng dụng
        
        Returns:
            bool: True nếu khởi tạo thành công
        """
        self.logger.info("Đang khởi tạo AeroHand...")
        
        if self.is_network_camera:
            # Sử dụng network camera
            self.logger.info(f"Connecting to network camera: {self.camera_ip}")
            self.status_text = f"Connecting to network camera: {self.camera_ip}"
            
            # Test connection trước
            if not CameraManager.test_network_connection(self.camera_ip, 8080, 5):
                self.logger.error(f"Cannot connect to camera server: {self.camera_ip}:8080")
                self.status_text = f"Camera server not reachable: {self.camera_ip}"
                return False
            
            # Khởi tạo network camera
            if not self.camera_manager.initialize_camera(self.camera_ip):
                self.logger.error("Cannot initialize network camera")
                self.status_text = "Network camera initialization failed"
                return False
                
            self.status_text = f"Connected to network camera: {self.camera_ip}"
        else:
            # Sử dụng local camera
            if not CameraManager.check_camera_availability():
                self.logger.error("Không tìm thấy local webcam hoặc webcam không khả dụng")
                self.status_text = "Local camera not available"
                return False
            
            # Khởi tạo local camera
            if not self.camera_manager.initialize_camera("local"):
                self.logger.error("Không thể khởi tạo local camera")
                self.status_text = "Local camera initialization failed"
                return False
                
            self.status_text = "Local camera ready"
        
        self.logger.info("AeroHand đã được khởi tạo thành công")
        self.status_text += " - Show your hand to the camera"
        return True
    
    def run(self):
        """Chạy ứng dụng chính"""
        if not self.initialize():
            self.show_error_message()
            return
        
        self.logger.info("Bắt đầu chạy AeroHand")
        self.is_running = True
        
        try:
            while self.is_running:
                # Đọc frame từ camera
                ret, frame = self.camera_manager.read_frame()
                if not ret or frame is None:
                    self.logger.warning("Không thể đọc frame từ camera")
                    continue
                
                # Xử lý frame
                processed_frame = self.process_frame(frame)
                
                # Thu nhỏ cửa sổ hiển thị nếu cần
                if self.display_scale != 1.0:
                    height, width = processed_frame.shape[:2]
                    new_width = int(width * self.display_scale)
                    new_height = int(height * self.display_scale)
                    processed_frame = cv2.resize(processed_frame, (new_width, new_height))
                
                # Hiển thị frame
                cv2.imshow(WINDOW_NAME, processed_frame)
                
                # Xử lý sự kiện bàn phím
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q') or key == 27:  # 'q' hoặc ESC để thoát
                    break
                elif key == ord('r'):  # 'r' để reset
                    self.reset_application()
                elif key == ord('h'):  # 'h' để hiển thị help
                    self.show_help()
                
                # Tính FPS
                self.calculate_fps()
                
        except KeyboardInterrupt:
            self.logger.info("Người dùng dừng ứng dụng")
        except Exception as e:
            self.logger.error(f"Lỗi không mong muốn: {e}")
        finally:
            self.cleanup()
    
    def process_frame(self, frame):
        """
        Xử lý frame từ webcam
        
        Args:
            frame: Frame từ webcam
            
        Returns:
            Frame đã được xử lý
        """
        try:
            # Lấy kích thước frame
            height, width = frame.shape[:2]
            
            # Phát hiện tay
            processed_frame, results = self.hand_tracker.detect_hands(frame)
            
            if self.hand_tracker.is_hand_detected(results):
                # Lấy landmarks của tay đầu tiên
                landmarks = self.hand_tracker.get_landmarks(results, 0)
                
                if landmarks:
                    # Nhận diện gesture
                    gesture = self.gesture_recognizer.process_gesture(landmarks)
                    
                    # Lấy vị trí ngón trỏ để điều khiển chuột
                    pointer_pos = self.gesture_recognizer.get_pointer_position(landmarks)
                    
                    if pointer_pos:
                        # Chuyển đổi tọa độ normalized sang pixel
                        pixel_x = int(pointer_pos[0] * width)
                        pixel_y = int(pointer_pos[1] * height)
                        
                        # Di chuyển chuột
                        self.mouse_controller.move_cursor(pixel_x, pixel_y, width, height)
                        
                        # Vẽ điểm ngón trỏ
                        cv2.circle(processed_frame, (pixel_x, pixel_y), 10, GESTURE_COLOR, -1)
                        cv2.circle(processed_frame, (pixel_x, pixel_y), 15, GESTURE_COLOR, 2)
                    
                    # Xử lý các gesture click
                    if gesture == "left_click":
                        self.mouse_controller.left_click()
                        self.gesture_text = "LEFT CLICK"
                    elif gesture == "right_click":
                        self.mouse_controller.right_click()
                        self.gesture_text = "RIGHT CLICK"
                    elif gesture in ["left_click_cooldown", "right_click_cooldown"]:
                        self.gesture_text = "COOLDOWN"
                    else:
                        self.gesture_text = "MOVING"
                    
                    self.status_text = "Hand detected - Controlling mouse"
                else:
                    self.gesture_text = "Hand detected - No landmarks"
                    self.status_text = "Processing hand data..."
            else:
                self.gesture_text = "No hand detected"
                self.status_text = "Show your hand to the camera"
            
            # Vẽ UI lên frame
            self.draw_ui(processed_frame)
            
            return processed_frame
            
        except Exception as e:
            self.logger.error(f"Lỗi khi xử lý frame: {e}")
            self.gesture_text = "Processing error"
            self.status_text = f"Error: {str(e)}"
            self.draw_ui(frame)
            return frame
    
    def draw_ui(self, frame):
        """
        Vẽ giao diện người dùng lên frame
        
        Args:
            frame: Frame để vẽ lên
        """
        try:
            height, width = frame.shape[:2]
            
            # Vẽ background cho text
            overlay = frame.copy()
            cv2.rectangle(overlay, (0, 0), (width, 120), (0, 0, 0), -1)
            cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
            
            # Vẽ tiêu đề
            cv2.putText(frame, "AeroHand - Gesture Mouse Control", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                       FONT_SCALE, TEXT_COLOR, FONT_THICKNESS)
            
            # Vẽ trạng thái
            cv2.putText(frame, f"Status: {self.status_text}", 
                       (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 
                       0.7, TEXT_COLOR, 1)
            
            # Vẽ gesture hiện tại
            gesture_color = GESTURE_COLOR if "CLICK" in self.gesture_text else TEXT_COLOR
            cv2.putText(frame, f"Gesture: {self.gesture_text}", 
                       (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 
                       0.7, gesture_color, 2)
            
            # Vẽ FPS
            cv2.putText(frame, f"FPS: {self.current_fps:.1f}", 
                       (width - 100, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                       0.6, TEXT_COLOR, 1)
            
            # Vẽ hướng dẫn
            cv2.putText(frame, "Press 'q' to quit, 'r' to reset, 'h' for help", 
                       (10, height - 20), cv2.FONT_HERSHEY_SIMPLEX, 
                       0.5, TEXT_COLOR, 1)
            
        except Exception as e:
            self.logger.error(f"Lỗi khi vẽ UI: {e}")
    
    def calculate_fps(self):
        """Tính toán FPS"""
        self.fps_counter += 1
        if self.fps_counter >= 30:  # Cập nhật FPS mỗi 30 frames
            current_time = time.time()
            self.current_fps = self.fps_counter / (current_time - self.fps_start_time)
            self.fps_counter = 0
            self.fps_start_time = current_time
    
    def reset_application(self):
        """Reset ứng dụng"""
        self.logger.info("Đang reset ứng dụng...")
        self.gesture_recognizer.reset_cooldowns()
        self.status_text = "Application reset"
        self.gesture_text = "Ready"
    
    def show_help(self):
        """Hiển thị thông tin trợ giúp"""
        help_text = """
        AeroHand - Gesture Controls:
        
        🖱️  Index finger: Move cursor
        👆  Pinch (index + thumb): Left click  
        ✊  Fist (close all fingers): Right click
        
        Keyboard shortcuts:
        'q' or ESC: Quit application
        'r': Reset application
        'h': Show this help
        """
        self.logger.info(help_text)
        print(help_text)
    
    def show_error_message(self):
        """Hiển thị thông báo lỗi khi không thể khởi tạo"""
        error_window = "AeroHand - Error"
        error_frame = cv2.imread("error_placeholder.jpg") if cv2.imread("error_placeholder.jpg") is not None else \
                     np.zeros((400, 600, 3), dtype="uint8")
        
        cv2.putText(error_frame, "AeroHand - Error", 
                   (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, ERROR_COLOR, 2)
        cv2.putText(error_frame, self.status_text, 
                   (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, ERROR_COLOR, 1)
        cv2.putText(error_frame, "Please check your webcam connection", 
                   (50, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.6, TEXT_COLOR, 1)
        cv2.putText(error_frame, "Press any key to exit", 
                   (50, 180), cv2.FONT_HERSHEY_SIMPLEX, 0.6, TEXT_COLOR, 1)
        
        cv2.imshow(error_window, error_frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    def cleanup(self):
        """Dọn dẹp tài nguyên"""
        self.logger.info("Đang dọn dẹp tài nguyên...")
        self.is_running = False
        
        if self.camera_manager:
            self.camera_manager.release()
        
        if self.hand_tracker:
            self.hand_tracker.release()
        
        cv2.destroyAllWindows()
        self.logger.info("AeroHand đã được đóng thành công")

def main():
    """Hàm main"""
    parser = argparse.ArgumentParser(description="AeroHand - Gesture Mouse Control")
    parser.add_argument("--camera-ip", help="IP address of network camera server")
    parser.add_argument("--camera-port", type=int, default=8080, help="Port of camera server (default: 8080)")
    parser.add_argument("--display-scale", type=float, default=1.0, help="Display window scale factor (0.5 = half size, 2.0 = double size)")
    parser.add_argument("--scan-network", action="store_true", help="Scan network for camera servers")
    parser.add_argument("--demo", action="store_true", help="Run in demo mode (no mouse control)")
    
    args = parser.parse_args()
    
    # Scan network nếu được yêu cầu
    if args.scan_network:
        print("🔍 Scanning network for camera servers...")
        try:
            from network_scanner import NetworkScanner
            scanner = NetworkScanner()
            scanner.scan_network()
        except ImportError:
            print("❌ Network scanner not available")
        return
    
    # Chạy demo mode nếu được yêu cầu
    if args.demo:
        try:
            from demo import AeroHandDemo
            demo = AeroHandDemo()
            demo.run()
        except ImportError:
            print("❌ Demo mode not available")
        return
    
    print("=" * 50)
    print("🚀 Welcome to AeroHand!")
    print("   Gesture Mouse Control Application")
    print("=" * 50)
    print()
    
    if args.camera_ip:
        print(f"📹 Using network camera: {args.camera_ip}:{args.camera_port}")
        print("🔌 Make sure camera server is running on the target machine")
    else:
        print("🎥 Using local camera")
        print("🎥 Make sure your webcam is connected and working!")
    
    if args.display_scale != 1.0:
        print(f"🖼️  Display scale: {args.display_scale}x")
    
    print()
    print("📋 Instructions:")
    print("   • Point with index finger to move cursor")
    print("   • Pinch (index + thumb) for left click")
    print("   • Make a fist for right click")
    print("   • Press 'q' or ESC to quit")
    print("   • Press 'h' for help during use")
    print("=" * 50)
    
    try:
        app = AeroHandApp(args.camera_ip, args.display_scale)
        app.run()
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        logging.error(f"Fatal error in main: {e}")
    finally:
        print("\n👋 Thank you for using AeroHand!")

if __name__ == "__main__":
    main()
