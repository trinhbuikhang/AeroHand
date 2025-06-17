# AeroHand Troubleshooting Guide
# Hướng dẫn khắc phục sự cố AeroHand

## 🚨 Common Issues / Các vấn đề thường gặp

### 1. Camera Issues / Vấn đề Camera

#### ❌ "Cannot open webcam" / "Không thể mở webcam"

**Nguyên nhân có thể:**
- Webcam không được kết nối
- Webcam đang được sử dụng bởi ứng dụng khác
- Driver webcam chưa được cài đặt
- Quyền truy cập camera bị từ chối

**Cách khắc phục:**
1. Kiểm tra kết nối webcam
2. Đóng tất cả ứng dụng khác đang sử dụng camera (Skype, Zoom, etc.)
3. Restart ứng dụng
4. Thử chạy với quyền Administrator
5. Sử dụng network camera thay thế:
   ```bash
   python main.py --camera-ip YOUR_PHONE_IP
   ```

#### ❌ Camera lag / jerky / Camera bị giật lag

**Cách khắc phục:**
- Giảm resolution trong `config/settings.py`:
  ```python
  CAMERA_WIDTH = 640
  CAMERA_HEIGHT = 480
  ```
- Giảm FPS:
  ```python
  FPS = 15
  ```

### 2. Hand Detection Issues / Vấn đề phát hiện tay

#### ❌ "No hands detected" / "Không phát hiện được tay"

**Cách khắc phục:**
1. Đảm bảo đủ ánh sáng
2. Giữ tay trong khung hình camera
3. Tránh background phức tạp
4. Điều chỉnh độ nhạy trong `config/settings.py`:
   ```python
   DETECTION_CONFIDENCE = 0.5  # Giảm để dễ phát hiện hơn
   ```

#### ❌ Hand detection inaccurate / Phát hiện tay không chính xác

**Cách khắc phục:**
1. Tăng độ nhạy tracking:
   ```python
   TRACKING_CONFIDENCE = 0.3
   ```
2. Đảm bảo tay không bị che khuất
3. Tránh di chuyển tay quá nhanh

### 3. Mouse Control Issues / Vấn đề điều khiển chuột

#### ❌ Mouse movement too sensitive / Chuột di chuyển quá nhạy

**Cách khắc phục:**
```python
# Trong config/settings.py
MOUSE_SPEED = 1.0  # Giảm tốc độ
SMOOTHING_FACTOR = 0.5  # Tăng độ mượt
```

#### ❌ Mouse movement too slow / Chuột di chuyển quá chậm

**Cách khắc phục:**
```python
# Trong config/settings.py
MOUSE_SPEED = 3.0  # Tăng tốc độ
SMOOTHING_FACTOR = 0.1  # Giảm độ mượt
```

#### ❌ Click detection not working / Không phát hiện được click

**Cách khắc phục:**
1. Điều chỉnh ngưỡng click:
   ```python
   CLICK_THRESHOLD = 0.08  # Tăng để dễ click hơn
   ```
2. Giảm cooldown time:
   ```python
   CLICK_COOLDOWN = 0.3
   ```

### 4. Network Camera Issues / Vấn đề Network Camera

#### ❌ Cannot connect to network camera / Không kết nối được camera mạng

**Cách khắc phục:**
1. Kiểm tra IP address:
   ```bash
   python main.py --scan-network
   ```
2. Đảm bảo camera server đang chạy trên thiết bị khác:
   ```bash
   python camera_server.py
   ```
3. Kiểm tra firewall và port 8080
4. Thử ping IP address:
   ```bash
   ping YOUR_CAMERA_IP
   ```

#### ❌ Network camera lag / Camera mạng bị lag

**Cách khắc phục:**
1. Đảm bảo WiFi stable
2. Giảm chất lượng video trên camera server
3. Sử dụng kết nối Ethernet thay WiFi

### 5. Performance Issues / Vấn đề hiệu năng

#### ❌ High CPU usage / CPU sử dụng cao

**Cách khắc phục:**
1. Giảm FPS và resolution
2. Tắt debug mode:
   ```python
   DEBUG_MODE = False
   ```
3. Đóng các ứng dụng không cần thiết

#### ❌ Memory leak / Rò rỉ bộ nhớ

**Cách khắc phục:**
1. Restart ứng dụng định kỳ
2. Đảm bảo đã cài đặt phiên bản OpenCV stable

### 6. Installation Issues / Vấn đề cài đặt

#### ❌ Package installation failed / Cài đặt package thất bại

**Cách khắc phục:**
1. Update pip:
   ```bash
   python -m pip install --upgrade pip
   ```
2. Cài đặt từng package riêng:
   ```bash
   pip install opencv-python
   pip install mediapipe
   pip install pyautogui
   ```
3. Sử dụng conda thay pip (nếu có Anaconda)

#### ❌ Import errors / Lỗi import

**Cách khắc phục:**
1. Kiểm tra Python version (cần Python 3.7+)
2. Activate virtual environment nếu có
3. Reinstall packages:
   ```bash
   pip uninstall opencv-python
   pip install opencv-python
   ```

## 🔧 Debug Tools / Công cụ debug

### System Check / Kiểm tra hệ thống
```bash
python utils/system_check.py
```

### Component Test / Test từng thành phần
```bash
python test_components.py
```

### Network Scanner / Quét mạng
```bash
python network_scanner.py
```

### Demo Mode / Chế độ demo
```bash
python demo.py
```

## 📞 Getting Help / Nhận trợ giúp

Nếu vẫn gặp vấn đề:

1. Chạy system check và gửi kết quả
2. Check log file: `aerohand.log`
3. Thử demo mode trước
4. Cung cấp thông tin:
   - OS version
   - Python version  
   - Camera model
   - Error messages

## 🎯 Performance Tuning / Tối ưu hiệu năng

### For Low-end Systems / Hệ thống cấu hình thấp:
```python
# config/settings.py
CAMERA_WIDTH = 480
CAMERA_HEIGHT = 360
FPS = 10
DETECTION_CONFIDENCE = 0.5
MAX_HANDS = 1
```

### For High-end Systems / Hệ thống cấu hình cao:
```python
# config/settings.py
CAMERA_WIDTH = 1920
CAMERA_HEIGHT = 1080
FPS = 60
DETECTION_CONFIDENCE = 0.8
MAX_HANDS = 2
```
