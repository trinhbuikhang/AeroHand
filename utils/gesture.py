"""
Gesture Recognition Module
Module nhận diện các cử chỉ tay để điều khiển chuột với tính năng nâng cao
"""

import time
import logging
import numpy as np
from typing import List, Tuple, Optional, Dict
from config.settings import (
    CLICK_THRESHOLD, FIST_THRESHOLD, CLICK_COOLDOWN, 
    DOUBLE_CLICK_TIME, HOVER_TIME, PINCH_STABILITY_FRAMES
)

class GestureRecognizer:
    """Class nhận diện các cử chỉ tay với tính năng nâng cao"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Thời gian của lần click cuối cùng
        self.last_left_click_time = 0
        self.last_right_click_time = 0
        self.click_count = 0
        self.last_click_position = None
        
        # Trạng thái gesture hiện tại
        self.current_gesture = "moving"
        
        # Buffer để lưu trữ lịch sử gesture
        self.gesture_buffer = []
        self.buffer_size = 5
        
        # Pinch detection stability
        self.pinch_buffer = []
        self.pinch_buffer_size = PINCH_STABILITY_FRAMES
          # Hover detection
        self.hover_start_time = 0
        self.hover_position = None
        self.is_hovering = False
        
        # Gesture stability
        self.gesture_stability_count = 0
        self.stable_gesture_threshold = 3
    
    def detect_pinch_gesture(self, landmarks: List[Tuple[float, float]]) -> bool:
        """
        Phát hiện cử chỉ nhíp (ngón trỏ và ngón cái chạm nhau) với độ chính xác cao
        
        Args:
            landmarks: Danh sách landmarks của bàn tay
            
        Returns:
            bool: True nếu phát hiện cử chỉ nhíp
        """
        try:
            if len(landmarks) < 21:  # MediaPipe có 21 landmarks
                return False
            
            # Lấy vị trí đầu ngón trỏ (landmark 8) và đầu ngón cái (landmark 4)
            index_tip = landmarks[8]  # INDEX_FINGER_TIP
            thumb_tip = landmarks[4]  # THUMB_TIP
            
            # Lấy thêm các landmarks để kiểm tra tư thế
            index_pip = landmarks[6]  # INDEX_FINGER_PIP (khớp giữa ngón trỏ)
            thumb_ip = landmarks[3]   # THUMB_IP (khớp ngón cái)
            
            # Tính khoảng cách giữa hai đầu ngón
            tip_distance = self._calculate_distance(index_tip, thumb_tip)
            
            # Kiểm tra xem ngón trỏ có thẳng không (để tránh nhầm với nắm tay)
            index_pip_to_tip = self._calculate_distance(index_pip, index_tip)
            thumb_ip_to_tip = self._calculate_distance(thumb_ip, thumb_tip)
            
            # Ngón trỏ phải duỗi thẳng (khoảng cách từ PIP đến TIP phải đủ lớn)
            index_extended = index_pip_to_tip > 0.05
            thumb_extended = thumb_ip_to_tip > 0.03
            
            # Kiểm tra pinch chỉ khi cả hai ngón đều duỗi
            is_pinch_gesture = (tip_distance < CLICK_THRESHOLD and 
                               index_extended and thumb_extended)
            
            # Thêm vào buffer để làm mượt
            self.pinch_buffer.append(is_pinch_gesture)
            if len(self.pinch_buffer) > self.pinch_buffer_size:
                self.pinch_buffer.pop(0)
            
            # Chỉ trả về True nếu đa số các frame gần đây đều phát hiện pinch
            pinch_count = sum(self.pinch_buffer)
            stable_pinch = pinch_count >= (self.pinch_buffer_size // 2 + 1)
            
            self.logger.debug(f"Pinch - Distance: {tip_distance:.3f}, Index extended: {index_extended}, "
                            f"Thumb extended: {thumb_extended}, Stable: {stable_pinch} ({pinch_count}/{len(self.pinch_buffer)})")
            
            return stable_pinch
            
        except Exception as e:
            self.logger.error(f"Lỗi khi phát hiện cử chỉ nhíp: {e}")
            return False
    
    def detect_fist_gesture(self, landmarks: List[Tuple[float, float]]) -> bool:
        """
        Phát hiện cử chỉ nắm tay (tất cả ngón tay co lại)
        
        Args:
            landmarks: Danh sách landmarks của bàn tay
            
        Returns:
            bool: True nếu phát hiện cử chỉ nắm tay
        """
        try:
            if len(landmarks) < 21:
                return False
            
            # Landmarks của các đầu ngón tay
            finger_tips = [
                landmarks[4],   # Thumb tip
                landmarks[8],   # Index finger tip
                landmarks[12],  # Middle finger tip
                landmarks[16],  # Ring finger tip
                landmarks[20]   # Pinky tip
            ]
            
            # Landmarks của các khớp MCP (gốc ngón tay)
            finger_mcps = [
                landmarks[2],   # Thumb MCP (sử dụng landmark khác cho ngón cái)
                landmarks[5],   # Index finger MCP
                landmarks[9],   # Middle finger MCP
                landmarks[13],  # Ring finger MCP
                landmarks[17]   # Pinky MCP
            ]
            
            # Trung tâm của lòng bàn tay (landmark 0 - wrist)
            wrist = landmarks[0]
            
            # Đếm số ngón tay đang co
            closed_fingers = 0
            
            for i, (tip, mcp) in enumerate(zip(finger_tips, finger_mcps)):
                # Tính khoảng cách từ đầu ngón tay đến cổ tay
                tip_to_wrist = self._calculate_distance(tip, wrist)
                # Tính khoảng cách từ khớp MCP đến cổ tay
                mcp_to_wrist = self._calculate_distance(mcp, wrist)
                
                # Nếu đầu ngón tay gần cổ tay hơn khớp MCP, ngón tay được coi là co
                if i == 0:  # Ngón cái - xử lý đặc biệt
                    # Đối với ngón cái, kiểm tra theo trục x
                    if abs(tip[0] - mcp[0]) < 0.05:  # Ngón cái co ngang
                        closed_fingers += 1
                else:
                    # Các ngón tay khác
                    if tip_to_wrist < mcp_to_wrist * 0.9:  # 10% tolerance
                        closed_fingers += 1
            
            # Nếu ít nhất 4/5 ngón tay co lại thì coi là nắm tay
            is_fist = closed_fingers >= 4
            
            self.logger.debug(f"Closed fingers: {closed_fingers}/5, is_fist: {is_fist}")
            
            return is_fist
            
        except Exception as e:
            self.logger.error(f"Lỗi khi phát hiện cử chỉ nắm tay: {e}")
            return False
    
    def get_pointer_position(self, landmarks: List[Tuple[float, float]]) -> Optional[Tuple[float, float]]:
        """
        Lấy vị trí ngón trỏ để điều khiển con trỏ chuột
        
        Args:
            landmarks: Danh sách landmarks của bàn tay
            
        Returns:
            Optional[Tuple[float, float]]: Tọa độ ngón trỏ hoặc None
        """
        try:
            if len(landmarks) < 21:
                return None
              # Sử dụng đầu ngón trỏ (landmark 8)
            index_tip = landmarks[8]
            return index_tip
            
        except Exception as e:
            self.logger.error(f"Lỗi khi lấy vị trí ngón trỏ: {e}")
            return None
    
    def process_gesture(self, landmarks: List[Tuple[float, float]]) -> str:
        """
        Xử lý và nhận diện gesture tổng thể
        
        Args:
            landmarks: Danh sách landmarks của bàn tay
            
        Returns:
            str: Tên gesture ("moving", "left_click", "right_click")
        """
        try:
            current_time = time.time()
            gesture = "moving"  # Default gesture
            
            # Kiểm tra cử chỉ nắm tay (right click) trước
            if self.detect_fist_gesture(landmarks):
                if current_time - self.last_right_click_time > CLICK_COOLDOWN:
                    gesture = "right_click"
                    self.last_right_click_time = current_time
                    self.logger.debug("Right click detected and executed")
                else:
                    gesture = "right_click_cooldown"
                    self.logger.debug(f"Right click in cooldown: {current_time - self.last_right_click_time:.2f}s")
            
            # Kiểm tra cử chỉ nhíp (left click) - chỉ khi không phải right click
            elif self.detect_pinch_gesture(landmarks):
                if current_time - self.last_left_click_time > CLICK_COOLDOWN:
                    gesture = "left_click"
                    self.last_left_click_time = current_time
                    self.logger.debug("Left click detected and executed")
                else:
                    gesture = "left_click_cooldown"
                    self.logger.debug(f"Left click in cooldown: {current_time - self.last_left_click_time:.2f}s")
            
            # Không dùng buffer cho cooldown - trả về trực tiếp
            if "cooldown" in gesture:
                return gesture
            
            # Chỉ dùng buffer cho các gesture khác
            if gesture not in ["left_click_cooldown", "right_click_cooldown"]:
                self.gesture_buffer.append(gesture)
                if len(self.gesture_buffer) > self.buffer_size:
                    self.gesture_buffer.pop(0)
                
                # Lấy gesture phổ biến nhất trong buffer (không bao gồm cooldown)
                smoothed_gesture = self._get_most_common_gesture()
                self.current_gesture = smoothed_gesture
                return smoothed_gesture
            else:
                return gesture
            
        except Exception as e:
            self.logger.error(f"Lỗi khi xử lý gesture: {e}")
            return "moving"
    
    def _calculate_distance(self, point1: Tuple[float, float], point2: Tuple[float, float]) -> float:
        """
        Tính khoảng cách Euclidean giữa hai điểm
        
        Args:
            point1: Điểm thứ nhất (x, y)
            point2: Điểm thứ hai (x, y)
            
        Returns:
            float: Khoảng cách
        """
        return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
    
    def _get_most_common_gesture(self) -> str:
        """
        Lấy gesture phổ biến nhất trong buffer
        
        Returns:
            str: Gesture phổ biến nhất
        """
        if not self.gesture_buffer:
            return "moving"
        
        # Đếm tần suất của mỗi gesture
        gesture_counts = {}
        for gesture in self.gesture_buffer:
            gesture_counts[gesture] = gesture_counts.get(gesture, 0) + 1
        
        # Trả về gesture có tần suất cao nhất
        return max(gesture_counts, key=gesture_counts.get)
    
    def get_current_gesture(self) -> str:
        """
        Lấy gesture hiện tại
        
        Returns:
            str: Gesture hiện tại
        """
        return self.current_gesture
    
    def reset_cooldowns(self):
        """Reset thời gian cooldown của các click"""
        self.last_left_click_time = 0
        self.last_right_click_time = 0
    
    def get_gesture_info(self) -> Dict[str, any]:
        """
        Lấy thông tin chi tiết về gesture hiện tại
        
        Returns:
            Dict[str, any]: Thông tin gesture
        """
        current_time = time.time()
        return {
            'current_gesture': self.current_gesture,
            'left_click_cooldown': max(0, CLICK_COOLDOWN - (current_time - self.last_left_click_time)),
            'right_click_cooldown': max(0, CLICK_COOLDOWN - (current_time - self.last_right_click_time)),
            'buffer_size': len(self.gesture_buffer),
            'gesture_buffer': self.gesture_buffer.copy()
        }
    
    def detect_double_click(self, current_position: Tuple[float, float]) -> bool:
        """
        Phát hiện double click dựa trên thời gian và vị trí
        
        Args:
            current_position: Vị trí hiện tại của gesture
            
        Returns:
            bool: True nếu là double click
        """
        try:
            current_time = time.time()
            
            # Kiểm tra thời gian giữa các click
            if (current_time - self.last_left_click_time) <= DOUBLE_CLICK_TIME:
                # Kiểm tra khoảng cách giữa các vị trí click
                if self.last_click_position:
                    distance = self._calculate_distance(current_position, self.last_click_position)
                    if distance < 0.05:  # Threshold cho khoảng cách double click
                        return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Lỗi khi phát hiện double click: {e}")
            return False
    
    def detect_hover(self, current_position: Tuple[float, float]) -> bool:
        """
        Phát hiện hover (giữ tay ở một vị trí trong thời gian dài)
        
        Args:
            current_position: Vị trí hiện tại
            
        Returns:
            bool: True nếu đang hover
        """
        try:
            current_time = time.time()
            
            if self.hover_position is None:
                self.hover_position = current_position
                self.hover_start_time = current_time
                return False
            
            # Tính khoảng cách di chuyển
            distance = self._calculate_distance(current_position, self.hover_position)
            
            if distance < 0.03:  # Threshold cho hover (ít di chuyển)
                if current_time - self.hover_start_time >= HOVER_TIME:
                    if not self.is_hovering:
                        self.is_hovering = True
                        self.logger.debug("Hover detected")
                    return True
            else:
                # Reset hover nếu di chuyển quá nhiều
                self.hover_position = current_position
                self.hover_start_time = current_time
                self.is_hovering = False
            
            return False
            
        except Exception as e:
            self.logger.error(f"Lỗi khi phát hiện hover: {e}")
            return False
