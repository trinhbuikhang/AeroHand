"""
Mouse Control Module
Module điều khiển chuột máy tính với tính năng nâng cao
"""

import pyautogui
import numpy as np
import time
import logging
from typing import Tuple, Optional, List
from collections import deque
from config.settings import (
    SMOOTHING_FACTOR, MOUSE_SPEED, SCREEN_MARGIN, 
    MOUSE_ACCELERATION, DEADZONE_SIZE, CURSOR_SMOOTHING_WINDOW,
    PRECISION_MODE_THRESHOLD, PRECISION_SPEED_FACTOR
)

class MouseController:
    """Class điều khiển chuột máy tính với tính năng nâng cao"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Tắt fail-safe của pyautogui
        pyautogui.FAILSAFE = False
        pyautogui.PAUSE = 0  # Tắt delay mặc định
        
        # Lấy kích thước màn hình
        self.screen_width, self.screen_height = pyautogui.size()
        self.logger.info(f"Screen resolution: {self.screen_width}x{self.screen_height}")
        
        # Vị trí chuột trước đó
        self.prev_mouse_x = self.screen_width // 2
        self.prev_mouse_y = self.screen_height // 2
          # Buffer cho smoothing
        self.position_buffer = deque(maxlen=CURSOR_SMOOTHING_WINDOW)
        self.stable_position_buffer = deque(maxlen=3)  # Buffer nhỏ hơn cho ổn định
        
        # Vùng hoạt động hiệu dụng
        self.effective_width = self.screen_width - 2 * SCREEN_MARGIN
        self.effective_height = self.screen_height - 2 * SCREEN_MARGIN
        
        # Trạng thái precision mode
        self.precision_mode = False
        self.precision_start_time = 0
        
        # Trạng thái ổn định
        self.stable_frames = 0
        self.min_stable_frames = getattr(__import__('config.settings', fromlist=['STABILIZATION_FRAMES']), 'STABILIZATION_FRAMES', 3)        
        # Trạng thái click
        self.last_click_time = 0
        self.click_position = (0, 0)
    
    def move_cursor(self, hand_x: float, hand_y: float, frame_width: int, frame_height: int):
        """
        Di chuyển con trỏ chuột dựa trên vị trí tay với smoothing nâng cao
        
        Args:
            hand_x: Tọa độ x của tay trong frame
            hand_y: Tọa độ y của tay trong frame
            frame_width: Chiều rộng của frame webcam
            frame_height: Chiều cao của frame webcam
        """
        try:
            # Chuyển đổi tọa độ tay từ frame sang tọa độ màn hình
            screen_x = np.interp(hand_x, [0, frame_width], [SCREEN_MARGIN, self.screen_width - SCREEN_MARGIN])
            screen_y = np.interp(hand_y, [0, frame_height], [SCREEN_MARGIN, self.screen_height - SCREEN_MARGIN])
            
            # Thêm vào buffer ổn định
            self.stable_position_buffer.append((screen_x, screen_y))
            
            # Kiểm tra tính ổn định của tọa độ
            if len(self.stable_position_buffer) >= 2:
                current_pos = self.stable_position_buffer[-1]
                prev_pos = self.stable_position_buffer[-2]
                distance = np.sqrt((current_pos[0] - prev_pos[0])**2 + (current_pos[1] - prev_pos[1])**2)
                
                # Nếu di chuyển quá nhỏ, tăng counter ổn định
                if distance < DEADZONE_SIZE * self.screen_width:
                    self.stable_frames += 1
                else:
                    self.stable_frames = 0
                
                # Chỉ di chuyển chuột khi đã ổn định hoặc di chuyển đủ lớn
                if self.stable_frames < self.min_stable_frames and distance < DEADZONE_SIZE * self.screen_width:
                    return
            
            # Thêm vào buffer chính để làm mượt
            self.position_buffer.append((screen_x, screen_y))
            
            # Tính toán vị trí trung bình từ buffer với trọng số
            if len(self.position_buffer) > 1:
                # Sử dụng trọng số giảm dần cho các frame cũ
                weights = np.exp(-np.arange(len(self.position_buffer)) * 0.5)
                weights = weights / weights.sum()
                
                avg_x = sum(pos[0] * weight for pos, weight in zip(self.position_buffer, weights))
                avg_y = sum(pos[1] * weight for pos, weight in zip(self.position_buffer, weights))
            else:
                avg_x, avg_y = screen_x, screen_y
            
            # Áp dụng smoothing với SMOOTHING_FACTOR
            smooth_x = self.prev_mouse_x + (avg_x - self.prev_mouse_x) * (1 - SMOOTHING_FACTOR)
            smooth_y = self.prev_mouse_y + (avg_y - self.prev_mouse_y) * (1 - SMOOTHING_FACTOR)
            
            # Áp dụng tốc độ
            final_x = int(smooth_x)
            final_y = int(smooth_y)
            
            # Đảm bảo không vượt quá ranh giới màn hình
            final_x = max(0, min(final_x, self.screen_width - 1))
            final_y = max(0, min(final_y, self.screen_height - 1))
            
            # Di chuyển chuột
            pyautogui.moveTo(final_x, final_y, duration=0)
            
            # Cập nhật vị trí trước đó
            self.prev_mouse_x = final_x
            self.prev_mouse_y = final_y
            
        except Exception as e:
            self.logger.error(f"Lỗi khi di chuyển chuột: {e}")
    
    def left_click(self):
        """Thực hiện click chuột trái"""
        try:
            pyautogui.click()
            self.logger.debug("Left click performed")
        except Exception as e:
            self.logger.error(f"Lỗi khi click trái: {e}")
    
    def right_click(self):
        """Thực hiện click chuột phải"""
        try:
            pyautogui.rightClick()
            self.logger.debug("Right click performed")
        except Exception as e:
            self.logger.error(f"Lỗi khi click phải: {e}")
    
    def double_click(self):
        """Thực hiện double click"""
        try:
            pyautogui.doubleClick()
            self.logger.debug("Double click performed")
        except Exception as e:
            self.logger.error(f"Lỗi khi double click: {e}")
    
    def get_current_position(self) -> Tuple[int, int]:
        """
        Lấy vị trí hiện tại của con trỏ chuột
        
        Returns:
            Tuple[int, int]: (x, y) tọa độ hiện tại
        """
        try:
            return pyautogui.position()
        except Exception as e:
            self.logger.error(f"Lỗi khi lấy vị trí chuột: {e}")
            return (0, 0)
    
    def set_position(self, x: int, y: int):
        """
        Đặt vị trí chuột tức thì (không smooth)
        
        Args:
            x: Tọa độ x
            y: Tọa độ y
        """
        try:
            # Đảm bảo tọa độ hợp lệ
            x = max(0, min(x, self.screen_width - 1))
            y = max(0, min(y, self.screen_height - 1))
            
            pyautogui.moveTo(x, y)
            self.prev_mouse_x = x
            self.prev_mouse_y = y
            
        except Exception as e:
            self.logger.error(f"Lỗi khi đặt vị trí chuột: {e}")
    
    def get_screen_size(self) -> Tuple[int, int]:
        """
        Lấy kích thước màn hình
        
        Returns:
            Tuple[int, int]: (width, height)
        """
        return self.screen_width, self.screen_height
    
    def is_position_valid(self, x: int, y: int) -> bool:
        """
        Kiểm tra tọa độ có hợp lệ không
        
        Args:
            x: Tọa độ x
            y: Tọa độ y
            
        Returns:
            bool: True nếu tọa độ hợp lệ
        """
        return 0 <= x < self.screen_width and 0 <= y < self.screen_height
    
    def get_window_under_cursor(self):
        """Lấy thông tin cửa sổ dưới con trỏ chuột"""
        try:
            import win32gui
            import win32api
            
            # Lấy vị trí hiện tại của chuột
            x, y = win32api.GetCursorPos()
            
            # Lấy handle của cửa sổ tại vị trí đó
            hwnd = win32gui.WindowFromPoint((x, y))
            
            if hwnd:
                # Lấy tiêu đề cửa sổ
                window_title = win32gui.GetWindowText(hwnd)
                return window_title if window_title else "Unknown Window"
            return None
        except ImportError:
            # Nếu không có win32gui, trả về None
            return None
        except Exception as e:
            self.logger.debug(f"Cannot get window info: {e}")
            return None
    
    def show_cursor_info(self) -> dict:
        """Hiển thị thông tin về con trỏ hiện tại"""
        current_pos = self.get_current_position()
        window_info = self.get_window_under_cursor()
        
        return {
            "position": current_pos,
            "window": window_info,
            "precision_mode": self.precision_mode,
            "screen_size": (self.screen_width, self.screen_height)
        }
    
    def reset_smoothing(self):
        """Reset buffer smoothing"""
        self.position_buffer.clear()
        self.precision_mode = False
