# 🚀 AeroHand - Gesture Mouse Control

**AeroHand** là một ứng dụng điều khiển chuột bằng cử chỉ tay sử dụng computer vision và machine learning. Ứng dụng cho phép bạn điều khiển con trỏ chuột và thực hiện các thao tác click chỉ bằng cách sử dụng cử chỉ tay trước webcam.

![AeroHand Demo](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)

## ✨ Tính năng chính

- 🖱️ **Điều khiển con trỏ chuột** bằng ngón trỏ
- 👆 **Left Click** bằng cử chỉ nhíp (ngón trỏ + ngón cái)
- ✊ **Right Click** bằng cử chỉ nắm tay
- 🎥 **Hỗ trợ camera local và network camera**
- 🔧 **Tùy chỉnh độ nhạy và kích thước hiển thị**
- 🐛 **Debug mode** để theo dõi việc nhận diện
- 📱 **GUI thân thiện** với thông tin real-time

## 🎮 Cách sử dụng

### Cử chỉ điều khiển:
- **Di chuyển chuột**: Giơ ngón trỏ và di chuyển tay
- **Left Click**: Chạm ngón trỏ với ngón cái (cử chỉ nhíp)
- **Right Click**: Nắm tay thành nắm đấm

### Phím tắt:
- `q` hoặc `ESC`: Thoát ứng dụng
- `r`: Reset ứng dụng
- `h`: Hiển thị trợ giúp

## 🛠️ Cài đặt

### Yêu cầu hệ thống:
- Python 3.8 trở lên
- Webcam hoặc camera USB
- Hỗ trợ Windows, Linux, macOS

### Cài đặt từ source:

```bash
# Clone repository
git clone https://github.com/yourusername/AeroHand.git
cd AeroHand

# Cài đặt dependencies
pip install -r requirements.txt

# Chạy ứng dụng
python main.py
```

### Cài đặt nhanh (Windows):
```bash
# Chạy script cài đặt
install.bat

# Hoặc chạy trực tiếp
run_aerohand.bat
```

## 🚀 Sử dụng

### Chạy cơ bản:
```bash
python main.py
```

### Tùy chọn nâng cao:
```bash
# Sử dụng network camera
python main.py --camera-ip 192.168.1.100

# Thu nhỏ cửa sổ hiển thị
python main.py --display-scale 0.5

# Chế độ demo
python main.py --demo

# Quét network để tìm camera
python main.py --scan-network
```

## ⚙️ Cấu hình

Tùy chỉnh các thông số trong `config/settings.py`:

```python
# Độ phân giải camera
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

# Độ nhạy gesture
CLICK_THRESHOLD = 0.08
SMOOTHING_FACTOR = 0.7

# Debug mode
DEBUG_MODE = True
SHOW_DEBUG_INFO = True
```

## 📁 Cấu trúc dự án

```
AeroHand/
├── main.py                 # File chính của ứng dụng
├── requirements.txt        # Dependencies Python
├── config/
│   └── settings.py        # Cấu hình ứng dụng
├── modules/
│   ├── camera_manager.py  # Quản lý camera
│   ├── hand_tracking.py   # Nhận diện bàn tay
│   └── network_camera.py  # Camera qua mạng
├── utils/
│   ├── gesture.py         # Nhận diện cử chỉ
│   ├── mouse_control.py   # Điều khiển chuột
│   └── system_check.py    # Kiểm tra hệ thống
├── demo.py                # Chế độ demo
├── launcher.py            # GUI launcher
└── docs/                  # Tài liệu
```

## 🔧 Các công cụ hỗ trợ

- `demo.py`: Chạy chế độ demo
- `setup.py`: Cài đặt và cấu hình
- `network_scanner.py`: Quét camera trên mạng
- `camera_troubleshoot.py`: Khắc phục sự cố camera
- `test_components.py`: Test các thành phần

## 🐛 Debug và Troubleshooting

### Bật debug mode:
```python
# Trong config/settings.py
DEBUG_MODE = True
SHOW_DEBUG_INFO = True
```

### Các vấn đề thường gặp:

1. **Camera không hoạt động**:
   ```bash
   python utils/system_check.py
   ```

2. **Chuột nháy nháy**:
   - Tăng SMOOTHING_FACTOR trong settings
   - Kiểm tra ánh sáng

3. **Không nhận diện gesture**:
   - Kiểm tra CLICK_THRESHOLD
   - Đảm bảo tay trong khung hình

## 🤝 Đóng góp

Chúng tôi hoan nghênh mọi đóng góp! Vui lòng:

1. Fork repository
2. Tạo feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push branch: `git push origin feature-name`
5. Tạo Pull Request

## 📄 License

Dự án này được cấp phép theo [MIT License](LICENSE).

## 🙏 Credits

- **MediaPipe** - Hand tracking
- **OpenCV** - Computer vision
- **PyAutoGUI** - Mouse control
- **NumPy** - Numerical computing

## 📞 Liên hệ

- **Author**: AeroHand Team
- **Email**: your.email@example.com
- **GitHub**: https://github.com/yourusername/AeroHand

## 🔄 Lịch sử phiên bản

### v1.0.0 (Current)
- ✅ Điều khiển chuột cơ bản
- ✅ Nhận diện gesture pinch và fist
- ✅ Hỗ trợ network camera
- ✅ Debug mode
- ✅ GUI thân thiện

### Roadmap
- [ ] Double click gesture
- [ ] Scroll gesture
- [ ] Multi-hand support
- [ ] Mobile app
- [ ] Voice commands integration

---

⭐ Nếu bạn thấy dự án hữu ích, hãy cho chúng tôi một star trên GitHub!
