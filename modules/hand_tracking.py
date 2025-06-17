"""
Hand Tracking Module
Module nhận diện và theo dõi bàn tay sử dụng MediaPipe
"""

import cv2
import mediapipe as mp
import numpy as np
import logging
from typing import List, Optional, Tuple, Dict, Any
from config.settings import (
    DETECTION_CONFIDENCE, 
    TRACKING_CONFIDENCE, 
    MAX_HANDS
)

class HandTracker:
    """Class để nhận diện và theo dõi bàn tay"""
    
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        # Khởi tạo MediaPipe Hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=MAX_HANDS,
            min_detection_confidence=DETECTION_CONFIDENCE,
            min_tracking_confidence=TRACKING_CONFIDENCE
        )
        
        self.logger = logging.getLogger(__name__)
        
        # Định nghĩa các landmark IDs quan trọng
        self.LANDMARK_IDS = {
            'WRIST': 0,
            'THUMB_TIP': 4,
            'THUMB_IP': 3,
            'THUMB_MCP': 2,
            'INDEX_FINGER_TIP': 8,
            'INDEX_FINGER_DIP': 7,
            'INDEX_FINGER_PIP': 6,
            'INDEX_FINGER_MCP': 5,
            'MIDDLE_FINGER_TIP': 12,
            'MIDDLE_FINGER_DIP': 11,
            'MIDDLE_FINGER_PIP': 10,
            'MIDDLE_FINGER_MCP': 9,
            'RING_FINGER_TIP': 16,
            'RING_FINGER_DIP': 15,
            'RING_FINGER_PIP': 14,
            'RING_FINGER_MCP': 13,
            'PINKY_TIP': 20,
            'PINKY_DIP': 19,
            'PINKY_PIP': 18,
            'PINKY_MCP': 17
        }
    
    def detect_hands(self, frame: np.ndarray) -> Tuple[np.ndarray, Optional[Any]]:
        """
        Phát hiện bàn tay trong frame
        
        Args:
            frame: Frame đầu vào từ webcam
            
        Returns:
            Tuple[np.ndarray, Optional[Any]]: (processed_frame, hands_results)
        """
        try:
            # Convert BGR to RGB (MediaPipe yêu cầu RGB)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Xử lý frame để phát hiện tay
            results = self.hands.process(rgb_frame)
            
            # Vẽ landmarks lên frame nếu phát hiện được tay
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    self.mp_drawing.draw_landmarks(
                        frame,
                        hand_landmarks,
                        self.mp_hands.HAND_CONNECTIONS,
                        self.mp_drawing_styles.get_default_hand_landmarks_style(),
                        self.mp_drawing_styles.get_default_hand_connections_style()
                    )
            
            return frame, results
            
        except Exception as e:
            self.logger.error(f"Lỗi khi phát hiện tay: {e}")
            return frame, None
    
    def get_landmarks(self, results: Any, hand_index: int = 0) -> Optional[List[Tuple[float, float]]]:
        """
        Lấy tọa độ các landmarks của bàn tay
        
        Args:
            results: Kết quả từ MediaPipe
            hand_index: Index của bàn tay (0 cho tay đầu tiên)
            
        Returns:
            Optional[List[Tuple[float, float]]]: Danh sách tọa độ landmarks hoặc None
        """
        if not results.multi_hand_landmarks or hand_index >= len(results.multi_hand_landmarks):
            return None
        
        try:
            hand_landmarks = results.multi_hand_landmarks[hand_index]
            landmarks = []
            
            for landmark in hand_landmarks.landmark:
                landmarks.append((landmark.x, landmark.y))
            
            return landmarks
            
        except Exception as e:
            self.logger.error(f"Lỗi khi lấy landmarks: {e}")
            return None
    
    def get_finger_tip_positions(self, landmarks: List[Tuple[float, float]], 
                                image_width: int, image_height: int) -> Dict[str, Tuple[int, int]]:
        """
        Lấy vị trí đầu ngón tay trong tọa độ pixel
        
        Args:
            landmarks: Danh sách landmarks
            image_width: Chiều rộng của hình ảnh
            image_height: Chiều cao của hình ảnh
            
        Returns:
            Dict[str, Tuple[int, int]]: Dictionary chứa vị trí đầu các ngón tay
        """
        finger_tips = {}
        
        try:
            # Lấy tọa độ các đầu ngón tay
            tip_ids = {
                'thumb': self.LANDMARK_IDS['THUMB_TIP'],
                'index': self.LANDMARK_IDS['INDEX_FINGER_TIP'],
                'middle': self.LANDMARK_IDS['MIDDLE_FINGER_TIP'],
                'ring': self.LANDMARK_IDS['RING_FINGER_TIP'],
                'pinky': self.LANDMARK_IDS['PINKY_TIP']
            }
            
            for finger, tip_id in tip_ids.items():
                if tip_id < len(landmarks):
                    x = int(landmarks[tip_id][0] * image_width)
                    y = int(landmarks[tip_id][1] * image_height)
                    finger_tips[finger] = (x, y)
            
            return finger_tips
            
        except Exception as e:
            self.logger.error(f"Lỗi khi lấy vị trí đầu ngón tay: {e}")
            return {}
    
    def get_landmark_position(self, landmarks: List[Tuple[float, float]], 
                             landmark_id: int, image_width: int, image_height: int) -> Optional[Tuple[int, int]]:
        """
        Lấy vị trí pixel của một landmark cụ thể
        
        Args:
            landmarks: Danh sách landmarks
            landmark_id: ID của landmark
            image_width: Chiều rộng hình ảnh
            image_height: Chiều cao hình ảnh
            
        Returns:
            Optional[Tuple[int, int]]: Tọa độ pixel hoặc None
        """
        try:
            if landmark_id < len(landmarks):
                x = int(landmarks[landmark_id][0] * image_width)
                y = int(landmarks[landmark_id][1] * image_height)
                return (x, y)
            return None
        except Exception as e:
            self.logger.error(f"Lỗi khi lấy vị trí landmark: {e}")
            return None
    
    def calculate_distance(self, point1: Tuple[float, float], point2: Tuple[float, float]) -> float:
        """
        Tính khoảng cách Euclidean giữa hai điểm
        
        Args:
            point1: Điểm thứ nhất (x, y)
            point2: Điểm thứ hai (x, y)
            
        Returns:
            float: Khoảng cách
        """
        try:
            return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
        except Exception as e:
            self.logger.error(f"Lỗi khi tính khoảng cách: {e}")
            return float('inf')
    
    def is_hand_detected(self, results: Any) -> bool:
        """
        Kiểm tra có phát hiện được tay không
        
        Args:
            results: Kết quả từ MediaPipe
            
        Returns:
            bool: True nếu phát hiện được tay
        """
        return results is not None and results.multi_hand_landmarks is not None
    
    def release(self):
        """Giải phóng tài nguyên"""
        if self.hands:
            self.hands.close()
            self.logger.info("Hand tracker released")
