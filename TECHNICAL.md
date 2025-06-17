# AeroHand - Technical Documentation

## Architecture Overview

AeroHand is built with a modular architecture that separates concerns into distinct components:

```
AeroHand/
├── main.py                 # Main application entry point
├── config/                 # Configuration module
│   ├── __init__.py
│   └── settings.py         # Application settings and parameters
├── modules/                # Core modules
│   ├── __init__.py
│   ├── camera_manager.py   # Webcam management
│   └── hand_tracking.py    # Hand detection using MediaPipe
├── utils/                  # Utility modules
│   ├── __init__.py
│   ├── gesture.py          # Gesture recognition logic
│   └── mouse_control.py    # Mouse control interface
├── launcher.py             # GUI launcher
├── setup.py               # Setup and installation script
├── test_components.py     # Component testing
└── version.py             # Version information
```

## Core Components

### 1. CameraManager (`modules/camera_manager.py`)

Handles all webcam operations:
- **Initialization**: Configures camera with optimal settings
- **Frame Capture**: Provides thread-safe frame reading
- **Resource Management**: Proper cleanup of camera resources
- **Error Handling**: Robust error handling for camera failures

Key methods:
- `initialize_camera()`: Setup camera with specified resolution and FPS
- `read_frame()`: Capture and flip frame for mirror effect
- `check_camera_availability()`: Static method to test camera before use

### 2. HandTracker (`modules/hand_tracking.py`)

MediaPipe-based hand detection and tracking:
- **Hand Detection**: Uses MediaPipe Hands solution
- **Landmark Extraction**: 21-point hand landmarks
- **Coordinate Conversion**: Normalized to pixel coordinates
- **Multi-hand Support**: Configurable for multiple hands

Key methods:
- `detect_hands()`: Process frame and return landmarks
- `get_landmarks()`: Extract landmark coordinates
- `get_finger_tip_positions()`: Get fingertip positions
- `calculate_distance()`: Euclidean distance between points

### 3. GestureRecognizer (`utils/gesture.py`)

Intelligent gesture recognition system:
- **Pinch Detection**: Index finger + thumb proximity
- **Fist Detection**: All fingers closed state
- **Gesture Smoothing**: Buffer-based gesture stabilization
- **Cooldown System**: Prevents accidental multiple clicks

Recognition algorithms:
- **Pinch**: Distance between index tip and thumb tip < threshold
- **Fist**: Ratio analysis of fingertip-to-wrist vs MCP-to-wrist distances
- **Smoothing**: Moving average over gesture buffer

### 4. MouseController (`utils/mouse_control.py`)

System mouse control interface:
- **Coordinate Mapping**: Webcam frame to screen coordinates
- **Movement Smoothing**: Exponential smoothing for fluid motion
- **Click Operations**: Left click, right click, double click
- **Boundary Checking**: Screen edge protection

Coordinate transformation:
```python
screen_x = interp(hand_x, [0, frame_width], [margin, screen_width - margin])
smooth_x = prev_x + (screen_x - prev_x) * (1 - smoothing_factor)
```

## Configuration System

### Settings (`config/settings.py`)

All configurable parameters in one place:

```python
# Camera Configuration
CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 720
FPS = 30

# Detection Thresholds
DETECTION_CONFIDENCE = 0.7
TRACKING_CONFIDENCE = 0.5
CLICK_THRESHOLD = 0.05
FIST_THRESHOLD = 0.6

# Performance Tuning
SMOOTHING_FACTOR = 0.3
CLICK_COOLDOWN = 0.5
```

## Gesture Recognition Algorithms

### Pinch Detection

The pinch gesture is detected by measuring the Euclidean distance between the index fingertip and thumb tip:

```python
def detect_pinch_gesture(self, landmarks):
    index_tip = landmarks[8]  # INDEX_FINGER_TIP
    thumb_tip = landmarks[4]  # THUMB_TIP
    distance = sqrt((index_tip[0] - thumb_tip[0])² + (index_tip[1] - thumb_tip[1])²)
    return distance < CLICK_THRESHOLD
```

### Fist Detection

Fist detection uses a more complex algorithm that analyzes the relationship between fingertips and metacarpophalangeal (MCP) joints:

```python
def detect_fist_gesture(self, landmarks):
    closed_fingers = 0
    for finger_tip, finger_mcp in zip(finger_tips, finger_mcps):
        tip_to_wrist = distance(finger_tip, wrist)
        mcp_to_wrist = distance(finger_mcp, wrist)
        if tip_to_wrist < mcp_to_wrist * 0.9:
            closed_fingers += 1
    return closed_fingers >= 4
```

## Performance Optimizations

### 1. Frame Processing Pipeline
- **Efficient Color Conversion**: BGR ↔ RGB only when needed
- **Selective Processing**: Skip expensive operations when no hand detected
- **Memory Management**: Reuse frame buffers where possible

### 2. Gesture Smoothing
- **Buffer System**: Last N gestures stored for analysis
- **Majority Voting**: Most common gesture in buffer selected
- **Cooldown Protection**: Prevents rapid-fire clicking

### 3. Mouse Movement Smoothing
- **Exponential Smoothing**: Reduces jitter and provides fluid motion
- **Configurable Response**: Adjustable smoothing factor
- **Boundary Clamping**: Ensures cursor stays within screen bounds

## Error Handling Strategy

### 1. Graceful Degradation
- Camera failures → Show error message and exit gracefully
- MediaPipe errors → Continue with previous frame or skip frame
- Mouse control errors → Log error but continue operation

### 2. Resource Management
- **RAII Pattern**: Resources acquired in constructors, released in destructors
- **Exception Safety**: All exceptions caught and logged
- **Cleanup on Exit**: Proper resource cleanup on application termination

### 3. Logging System
- **Hierarchical Logging**: Different log levels for different components
- **File and Console**: Both file logging and console output
- **Structured Messages**: Consistent log message format

## Dependencies and Requirements

### Core Dependencies
- **OpenCV (cv2)**: Computer vision and camera operations
- **MediaPipe**: Hand detection and tracking ML models
- **PyAutoGUI**: System mouse and keyboard control
- **NumPy**: Numerical operations and array handling
- **Pillow**: Image processing support

### System Requirements
- **Python**: 3.8 or higher
- **Operating System**: Windows, macOS, or Linux
- **Webcam**: Any USB or built-in camera
- **RAM**: Minimum 4GB (8GB recommended)
- **CPU**: Modern multi-core processor for real-time processing

## Extension Points

### 1. Additional Gestures
The gesture recognition system can be extended with new gestures:

```python
def detect_custom_gesture(self, landmarks):
    # Implement custom gesture logic
    return gesture_detected

# Add to process_gesture method
if self.detect_custom_gesture(landmarks):
    return "custom_action"
```

### 2. Multiple Hands Support
Currently configured for single hand, but can support multiple hands:

```python
# In settings.py
MAX_HANDS = 2  # Enable dual-hand tracking

# In hand_tracking.py
for hand_idx in range(len(results.multi_hand_landmarks)):
    # Process each hand separately
```

### 3. Advanced Mouse Operations
Additional mouse operations can be added:

```python
def drag_operation(self, start_pos, end_pos):
    pyautogui.drag(end_pos[0] - start_pos[0], end_pos[1] - start_pos[1])

def scroll_operation(self, direction, amount):
    pyautogui.scroll(amount * direction)
```

## Troubleshooting Guide

### Common Issues

1. **Camera Not Found**
   - Check camera connection
   - Verify no other applications using camera
   - Try different CAMERA_INDEX values

2. **Poor Hand Detection**
   - Improve lighting conditions
   - Ensure hand is fully visible in frame
   - Adjust DETECTION_CONFIDENCE threshold

3. **Jittery Mouse Movement**
   - Increase SMOOTHING_FACTOR (0.0-1.0)
   - Reduce camera resolution if CPU limited
   - Check for system performance issues

4. **False Click Detection**
   - Increase CLICK_THRESHOLD for pinch
   - Adjust FIST_THRESHOLD for fist detection
   - Increase CLICK_COOLDOWN to prevent rapid clicks

### Performance Tuning

1. **High CPU Usage**
   - Reduce camera resolution
   - Lower FPS setting
   - Disable debug logging

2. **Latency Issues**
   - Minimize background applications
   - Use dedicated USB port for camera
   - Ensure adequate system RAM

3. **Detection Accuracy**
   - Calibrate thresholds for your hand size
   - Ensure consistent lighting
   - Position camera at appropriate distance

## Future Enhancements

### Planned Features
- [ ] Multi-gesture sequences
- [ ] Customizable gesture mapping
- [ ] Voice commands integration
- [ ] Gesture recording and playback
- [ ] Multiple camera support
- [ ] Remote control capabilities

### Technical Improvements
- [ ] GPU acceleration for MediaPipe
- [ ] Adaptive threshold adjustment
- [ ] Machine learning gesture customization
- [ ] Real-time performance monitoring
- [ ] Cross-platform native packaging

## Contributing

To contribute to AeroHand:

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Follow code style guidelines
4. Add tests for new functionality
5. Update documentation
6. Submit pull request

### Code Style
- Follow PEP 8 for Python code
- Use type hints where applicable
- Include docstrings for all public methods
- Keep functions focused and modular
- Handle exceptions appropriately

### Testing
- Run `python test_components.py` before submitting
- Test on multiple operating systems if possible
- Verify camera compatibility
- Test gesture recognition accuracy

---

For technical support, please refer to the main README.md or create an issue in the project repository.
