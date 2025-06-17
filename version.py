# AeroHand Version Information

__version__ = "1.0.0"
__author__ = "AeroHand Team"
__email__ = "aerohand@example.com"
__description__ = "Gesture Mouse Control Application using Computer Vision"
__url__ = "https://github.com/aerohand/aerohand"

# Build information
BUILD_DATE = "2025-06-17"
PYTHON_VERSION_REQUIRED = "3.8"

# Feature flags
FEATURES = {
    "gesture_mouse_control": True,
    "left_click_pinch": True,
    "right_click_fist": True,
    "real_time_preview": True,
    "fps_display": True,
    "gesture_smoothing": True,
    "click_cooldown": True
}

# Supported platforms
SUPPORTED_PLATFORMS = ["Windows", "macOS", "Linux"]

def get_version_info():
    """Trả về thông tin phiên bản dạng dictionary"""
    return {
        "version": __version__,
        "author": __author__,
        "description": __description__,
        "build_date": BUILD_DATE,
        "python_required": PYTHON_VERSION_REQUIRED,
        "features": FEATURES,
        "supported_platforms": SUPPORTED_PLATFORMS
    }
