# AeroHand - Gesture Mouse Control

## Giới thiệu

AeroHand là một ứng dụng desktop nhẹ được viết bằng Python, cho phép điều khiển chuột máy tính bằng cử chỉ tay thông qua webcam. Ứng dụng sử dụng AI để nhận diện bàn tay và theo dõi chuyển động để thực hiện các thao tác chuột.

## Tính năng

- 🖱️ **Di chuyển chuột**: Sử dụng ngón trỏ để điều khiển con trỏ chuột
- 👆 **Click trái**: Chạm đầu ngón trỏ và ngón cái vào nhau
- ✊ **Click phải**: Nắm tay (co tất cả ngón tay)
- 📹 **Hiển thị trực tiếp**: Giao diện hiển thị webcam với overlay nhận diện tay
- 📊 **Trạng thái realtime**: Hiển thị trạng thái hiện tại (Moving/Left Click/Right Click)
- 🌐 **Network Camera**: Hỗ trợ sử dụng camera từ máy tính khác qua mạng

## Yêu cầu hệ thống

- Python 3.8 trở lên
- Webcam hoạt động
- Windows/macOS/Linux

## Cài đặt

1. **Clone hoặc tải project**:
   ```bash
   git clone <repository-url>
   cd AeroHand
   ```

2. **Tạo môi trường ảo (khuyến nghị)**:
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Cài đặt dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Chạy ứng dụng

### Sử dụng camera local (mặc định)
```bash
python main.py
```

### Sử dụng camera qua mạng
```bash
# Trên máy có camera (ví dụ: 192.168.14.123)
python camera_server.py

# Trên máy chạy AeroHand 
python main.py --camera-ip 192.168.14.123
```

### Các tùy chọn khác
```bash
# Scan mạng tìm camera servers
python network_scanner.py

# Chạy demo mode (không điều khiển chuột)
python main.py --demo

# Chạy GUI launcher
python launcher.py
```

## Cách sử dụng

1. **Khởi động ứng dụng**: Chạy `python main.py`
2. **Cho phép quyền truy cập webcam**: Khi được yêu cầu
3. **Đưa tay vào khung hình**: Ứng dụng sẽ tự động nhận diện
4. **Điều khiển chuột**:
   - Đưa ngón trỏ để di chuyển con trỏ
   - Chạm ngón trỏ và ngón cái để click trái
   - Nắm tay để click phải
5. **Thoát**: Nhấn 'q' hoặc đóng cửa sổ

## Sử dụng với Network Camera

### Tình huống: Máy không có camera muốn sử dụng camera từ máy khác

1. **Trên máy có camera (Server)**:
   ```bash
   # Tải AeroHand project
   git clone <repository-url>
   cd AeroHand
   
   # Cài đặt dependencies
   pip install opencv-python
   
   # Chạy camera server
   python camera_server.py
   
   # Ghi nhớ IP address được hiển thị (ví dụ: 192.168.14.123)
   ```

2. **Trên máy chạy AeroHand (Client)**:
   ```bash
   # Scan mạng tìm camera
   python network_scanner.py
   
   # Hoặc test IP cụ thể
   python network_scanner.py --ip 192.168.14.123
   
   # Chạy AeroHand với network camera
   python main.py --camera-ip 192.168.14.123
   ```

3. **Hoặc sử dụng GUI**:
   ```bash
   python launcher.py
   # → Chọn "Network Camera"
   # → Nhập IP: 192.168.14.123
   # → Click "Launch AeroHand"
   ```

### Hướng dẫn nhanh cho network setup:
```bash
# Chạy network setup guide
python network_setup.py
```

## Cấu trúc dự án

```
AeroHand/
├── main.py                 # File chính để chạy ứng dụng
├── modules/
│   ├── __init__.py
│   ├── hand_tracking.py    # Module nhận diện và theo dõi tay
│   └── camera_manager.py   # Quản lý webcam
├── utils/
│   ├── __init__.py
│   ├── gesture.py          # Xử lý các cử chỉ
│   └── mouse_control.py    # Điều khiển chuột
├── config/
│   ├── __init__.py
│   └── settings.py         # Cấu hình ứng dụng
├── requirements.txt        # Dependencies
└── README.md              # Tài liệu này
```

## Cấu hình

Có thể tùy chỉnh các thông số trong `config/settings.py`:

- `CAMERA_WIDTH`, `CAMERA_HEIGHT`: Độ phân giải webcam
- `DETECTION_CONFIDENCE`: Độ tin cậy nhận diện tay
- `TRACKING_CONFIDENCE`: Độ tin cậy theo dõi tay
- `SMOOTHING_FACTOR`: Độ mượt của chuyển động chuột
- `CLICK_THRESHOLD`: Ngưỡng khoảng cách để kích hoạt click

## Xử lý sự cố

### Webcam không hoạt động
- Kiểm tra webcam có được kết nối và hoạt động
- Đảm bảo không có ứng dụng khác đang sử dụng webcam
- Thử thay đổi `CAMERA_INDEX` trong settings

### Nhận diện tay không chính xác
- Đảm bảo ánh sáng đủ
- Giữ tay trong khung hình webcam
- Tăng `DETECTION_CONFIDENCE` nếu cần

### Chuột di chuyển giật lag
- Giảm `SMOOTHING_FACTOR`
- Kiểm tra hiệu năng CPU
- Giảm độ phân giải webcam nếu cần

## Đóng góp

Mọi đóng góp đều được chào đón! Hãy tạo issue hoặc pull request.

## Giấy phép

MIT License - Xem file LICENSE để biết thêm chi tiết.

## Tác giả

Created with ❤️ using Python, OpenCV, MediaPipe, and PyAutoGUI.
