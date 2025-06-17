# Cấu hình ứng dụng AeroHand

# Cấu hình Camera
CAMERA_INDEX = 0  # Index của webcam (thường là 0 cho webcam chính)
CAMERA_WIDTH = 640   # Thu nhỏ từ 1280 xuống 640
CAMERA_HEIGHT = 480  # Thu nhỏ từ 720 xuống 480
FPS = 30

# Cấu hình MediaPipe Hand Detection
DETECTION_CONFIDENCE = 0.7  # Độ tin cậy tối thiểu để phát hiện tay (0.0 - 1.0)
TRACKING_CONFIDENCE = 0.5   # Độ tin cậy tối thiểu để theo dõi tay (0.0 - 1.0)
MAX_HANDS = 1              # Số lượng tay tối đa được phát hiện

# Cấu hình điều khiển chuột
SMOOTHING_FACTOR = 0.7     # Tăng để làm mượt hơn (0.0 - 1.0, càng cao càng mượt)
MOUSE_SPEED = 1.5          # Tốc độ di chuyển chuột
MOUSE_ACCELERATION = 1.0   # Không dùng gia tốc để tránh nháy
DEADZONE_SIZE = 0.05       # Tăng vùng chết để tránh rung lắc

# Cấu hình gesture recognition
CLICK_THRESHOLD = 0.06     # Giảm xuống để cần chạm gần hơn mới click
FIST_THRESHOLD = 0.8       # Tăng để khó kích hoạt right click hơn
DOUBLE_CLICK_TIME = 0.5    # Thời gian cho double click
PINCH_STABILITY_FRAMES = 3 # Tăng số frame ổn định để tránh false positive

# Cấu hình cooldown (tránh click liên tục)
CLICK_COOLDOWN = 0.1       # Giảm thời gian cooldown xuống rất thấp
HOVER_TIME = 1.0           # Thời gian hover để hiển thị thông tin cửa sổ

# Cấu hình UI
WINDOW_NAME = "AeroHand - Gesture Mouse Control"
FONT_SCALE = 1.0
FONT_THICKNESS = 2
TEXT_COLOR = (0, 255, 0)   # Màu xanh lá (BGR)
ERROR_COLOR = (0, 0, 255)  # Màu đỏ (BGR)
GESTURE_COLOR = (255, 0, 0)  # Màu xanh dương (BGR)

# Cấu hình vùng hoạt động (Screen bounds)
SCREEN_MARGIN = 50         # Margin từ mép màn hình
CURSOR_SMOOTHING_WINDOW = 8  # Tăng số frame để làm mượt hơn
PRECISION_MODE_THRESHOLD = 0.1  # Ngưỡng để bật chế độ chính xác
PRECISION_SPEED_FACTOR = 0.3    # Tốc độ trong chế độ chính xác
STABILIZATION_FRAMES = 3        # Số frame ổn định trước khi di chuyển chuột

# Cấu hình Network Camera
DEFAULT_CAMERA_PORT = 8080  # Port mặc định cho camera server
NETWORK_TIMEOUT = 5        # Timeout kết nối network camera (giây)
NETWORK_RETRY_COUNT = 3    # Số lần thử lại kết nối

# Cấu hình Error Handling
CAMERA_RETRY_DELAY = 1.0   # Thời gian chờ trước khi thử lại camera (giây)
MAX_CAMERA_RETRIES = 3     # Số lần thử lại tối đa khi camera lỗi
SHOW_ERROR_WINDOW = True   # Hiển thị cửa sổ lỗi khi có vấn đề

# Cấu hình Debug
DEBUG_MODE = True          # Bật debug mode để hiển thị thông tin chi tiết
SHOW_DEBUG_INFO = True     # Hiển thị debug info trên GUI
SHOW_LANDMARKS = True      # Hiển thị landmarks của bàn tay
SHOW_GESTURE_INFO = True   # Hiển thị thông tin gesture chi tiết
LOG_LEVEL = "DEBUG"        # Mức độ log: DEBUG, INFO, WARNING, ERROR
SAVE_DEBUG_FRAMES = False  # Lưu frame debug khi có lỗi
