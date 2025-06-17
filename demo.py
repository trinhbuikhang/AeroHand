"""
AeroHand Demo Mode
Chế độ demo để test gesture detection mà không điều khiển chuột thật
"""

import cv2
import time
import logging
import sys
from modules.camera_manager import CameraManager
from modules.hand_tracking import HandTracker
from utils.gesture import GestureRecognizer
from config.settings import WINDOW_NAME, TEXT_COLOR, GESTURE_COLOR, ERROR_COLOR

class AeroHandDemo:
    """Demo mode của AeroHand chỉ hiển thị gesture detection"""
    
    def __init__(self):
        """Khởi tạo demo"""
        self.setup_logging()
        self.logger = logging.getLogger(__name__)
        
        # Components
        self.camera_manager = CameraManager()
        self.hand_tracker = HandTracker()
        self.gesture_recognizer = GestureRecognizer()
        
        # Status
        self.is_running = False
        self.fps_counter = 0
        self.fps_start_time = time.time()
        self.current_fps = 0
        
        # Display info
        self.status_text = "Demo Mode - No mouse control"
        self.gesture_text = "Show your hand to camera"
    
    def setup_logging(self):
        """Setup logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
    
    def run(self):
        """Chạy demo"""
        print("=" * 50)
        print("🎬 AeroHand Demo Mode")
        print("=" * 50)
        print("This demo shows gesture detection without mouse control")
        print("Gestures to try:")
        print("  • Point with index finger")
        print("  • Pinch index finger and thumb together")
        print("  • Make a fist with all fingers")
        print("Press 'q' or ESC to exit")
        print("=" * 50)
        
        if not self.initialize():
            print("❌ Failed to initialize camera")
            return
        
        self.is_running = True
        
        try:
            while self.is_running:
                ret, frame = self.camera_manager.read_frame()
                if not ret or frame is None:
                    continue
                
                processed_frame = self.process_frame(frame)
                cv2.imshow(f"{WINDOW_NAME} - Demo Mode", processed_frame)
                
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q') or key == 27:
                    break
                
                self.calculate_fps()
                
        except KeyboardInterrupt:
            print("\nDemo stopped by user")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.cleanup()
    
    def initialize(self) -> bool:
        """Khởi tạo components"""
        if not CameraManager.check_camera_availability():
            return False
        
        return self.camera_manager.initialize_camera()
    
    def process_frame(self, frame):
        """Xử lý frame"""
        height, width = frame.shape[:2]
        
        # Detect hands
        processed_frame, results = self.hand_tracker.detect_hands(frame)
        
        if self.hand_tracker.is_hand_detected(results):
            landmarks = self.hand_tracker.get_landmarks(results, 0)
            
            if landmarks:
                # Get gesture
                gesture = self.gesture_recognizer.process_gesture(landmarks)
                
                # Get pointer position for visualization
                pointer_pos = self.gesture_recognizer.get_pointer_position(landmarks)
                
                if pointer_pos:
                    pixel_x = int(pointer_pos[0] * width)
                    pixel_y = int(pointer_pos[1] * height)
                    
                    # Draw pointer position
                    cv2.circle(processed_frame, (pixel_x, pixel_y), 15, GESTURE_COLOR, 3)
                    cv2.circle(processed_frame, (pixel_x, pixel_y), 8, (255, 255, 255), -1)
                
                # Update gesture text
                if gesture == "left_click":
                    self.gesture_text = "🖱️ LEFT CLICK DETECTED!"
                elif gesture == "right_click":
                    self.gesture_text = "🖱️ RIGHT CLICK DETECTED!"
                elif gesture in ["left_click_cooldown", "right_click_cooldown"]:
                    self.gesture_text = "⏳ COOLDOWN..."
                else:
                    self.gesture_text = "👉 POINTING / MOVING"
                
                self.status_text = "✅ Hand detected - Tracking gestures"
            else:
                self.gesture_text = "🤔 Hand visible but no landmarks"
                self.status_text = "Processing hand data..."
        else:
            self.gesture_text = "👋 Show your hand to the camera"
            self.status_text = "🔍 Looking for hands..."
        
        self.draw_demo_ui(processed_frame)
        return processed_frame
    
    def draw_demo_ui(self, frame):
        """Vẽ UI cho demo mode"""
        height, width = frame.shape[:2]
        
        # Background overlay
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (width, 150), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.8, frame, 0.2, 0, frame)
        
        # Title
        cv2.putText(frame, "AeroHand - Demo Mode", 
                   (10, 35), cv2.FONT_HERSHEY_SIMPLEX, 1.2, TEXT_COLOR, 2)
        
        # Status
        cv2.putText(frame, f"Status: {self.status_text}", 
                   (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, TEXT_COLOR, 1)
        
        # Gesture
        gesture_color = GESTURE_COLOR if "DETECTED" in self.gesture_text else TEXT_COLOR
        cv2.putText(frame, f"Gesture: {self.gesture_text}", 
                   (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.8, gesture_color, 2)
        
        # FPS
        cv2.putText(frame, f"FPS: {self.current_fps:.1f}", 
                   (width - 120, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.7, TEXT_COLOR, 1)
        
        # Instructions
        cv2.putText(frame, "Demo Mode - Mouse control disabled", 
                   (10, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 1)
        
        # Bottom instructions
        cv2.putText(frame, "Try: Point finger | Pinch fingers | Make fist | Press 'q' to quit", 
                   (10, height - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, TEXT_COLOR, 1)
    
    def calculate_fps(self):
        """Calculate FPS"""
        self.fps_counter += 1
        if self.fps_counter >= 30:
            current_time = time.time()
            self.current_fps = self.fps_counter / (current_time - self.fps_start_time)
            self.fps_counter = 0
            self.fps_start_time = current_time
    
    def cleanup(self):
        """Cleanup resources"""
        self.is_running = False
        if self.camera_manager:
            self.camera_manager.release()
        if self.hand_tracker:
            self.hand_tracker.release()
        cv2.destroyAllWindows()
        print("Demo finished!")

def main():
    """Main function"""
    demo = AeroHandDemo()
    demo.run()

if __name__ == "__main__":
    main()
