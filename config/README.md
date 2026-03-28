# ⚙️ Configuration Files

This folder contains configuration files, settings, and system requirements for the Nami Neural Gesture Keyboard.

## 📁 Files in this folder:

### 1. `requirements.txt`
- **Purpose**: Python package dependencies
- **Description**: Lists all required Python packages and their versions
- **Contents**:
  - opencv-python>=4.10.0 (Computer vision)
  - numpy>=2.0.0 (Numerical computing)
  - pyttsx3>=2.98 (Text-to-speech)
  - mediapipe>=0.10.0 (Hand tracking)

### 2. `gesture_keyboard_log.txt` (Legacy)
- **Purpose**: Application log file (moved to cache/)
- **Description**: Runtime logs and session data now stored in cache/gesture_keyboard_log.txt
- **Contents**:
  - Application startup/shutdown events
  - Error messages and warnings
  - Performance metrics
  - User session summaries

## 🔗 Configuration Flow:

```
┌─────────────────────────┐
│   requirements.txt      │ ◄─── Package Dependencies
└───────────┬─────────────┘
            │
            │ (pip install -r requirements.txt)
            │
            ▼
┌─────────────────────────┐
│   System Installation   │ ◄─── Environment Setup
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│     ../core/main.py     │ ◄─── Application Launch
└───────────┬─────────────┘
            │
            │ (Runtime logging)
            │
            ▼
┌─────────────────────────┐
│gesture_keyboard_log.txt │ ◄─── Runtime Data
└─────────────────────────┘
```

## 📦 Package Dependencies:

### Core Dependencies
```
opencv-python>=4.10.0
├── Computer vision library
├── Camera capture and image processing
├── Frame manipulation and display
└── Window management

numpy>=2.0.0
├── Numerical computing foundation
├── Array operations and mathematics
├── Performance optimization
└── Data structure support

pyttsx3>=2.98
├── Text-to-speech synthesis
├── Cross-platform voice support
├── Voice customization
└── Background audio processing

mediapipe>=0.10.0
├── Hand tracking and detection
├── Face detection for anti-jitter
├── Real-time pose estimation
└── Machine learning models
```

### Installation Commands:
```bash
# Install all dependencies
pip install -r requirements.txt

# Or install individually
pip install opencv-python>=4.10.0
pip install numpy>=2.0.0
pip install pyttsx3>=2.98
pip install mediapipe>=0.10.0
```

## 📊 System Requirements:

### Minimum Requirements:
- **OS**: Windows 10, macOS 10.14, Ubuntu 18.04
- **Python**: 3.8 or higher (3.12 recommended)
- **RAM**: 4GB minimum, 8GB recommended
- **CPU**: Dual-core 2.0GHz minimum
- **Camera**: Any USB webcam or built-in camera
- **Storage**: 500MB free space

### Recommended Requirements:
- **OS**: Windows 11, macOS 12+, Ubuntu 20.04+
- **Python**: 3.12 (optimal MediaPipe compatibility)
- **RAM**: 16GB for best neural performance
- **CPU**: Quad-core 3.0GHz+ with AVX support
- **GPU**: Dedicated GPU for enhanced processing
- **Camera**: HD webcam with good low-light performance
- **Storage**: 2GB free space for AI data

## 🔧 Configuration Options:

### Neural Engine Configuration:
```json
{
  "neural_mode": "adaptive",
  "processing_fps": 120,
  "smoothing_factor": 0.85,
  "prediction_enabled": true,
  "learning_rate": 0.01
}
```

### AI Intelligence Configuration:
```json
{
  "vocabulary_size": 10000,
  "suggestion_count": 5,
  "learning_enabled": true,
  "privacy_mode": "local_only",
  "auto_save_interval": 10
}
```

### Performance Profiles:
- **Maximum Accuracy**: 98% accuracy, high CPU usage
- **Balanced Performance**: 95% accuracy, moderate CPU usage
- **Gaming Mode**: Ultra-responsive, optimized for speed
- **Power Efficient**: Extended battery life, reduced processing
- **Accessibility**: Enhanced stability, maximum smoothing

## 📝 Logging Configuration:

### Log Levels:
- **DEBUG**: Detailed diagnostic information
- **INFO**: General application events
- **WARNING**: Potential issues that don't stop operation
- **ERROR**: Serious problems that may affect functionality
- **CRITICAL**: Severe errors that may cause application failure

### Log Format:
```
[TIMESTAMP] [LEVEL] [COMPONENT] Message
Example: [2024-12-01 14:30:15] [INFO] [NEURAL_ENGINE] Neural processing started
```

### Log Rotation:
- **Max Size**: 10MB per log file
- **Backup Count**: Keep last 5 log files
- **Cleanup**: Automatic old log removal
- **Compression**: Compress archived logs

## 🔒 Privacy and Security:

### Data Privacy:
- **Local Processing**: All AI learning stays on device
- **No Network**: No data sent to external servers
- **User Control**: User can disable logging/learning
- **Data Encryption**: Sensitive data can be encrypted

### Security Features:
- **Safe Defaults**: Secure configuration out of the box
- **Input Validation**: All user inputs are validated
- **Error Isolation**: Errors don't compromise system security
- **Resource Limits**: Prevents resource exhaustion attacks

## 🚀 Performance Optimization:

### CPU Optimization:
- **Multi-threading**: Parallel processing where possible
- **Vectorization**: NumPy optimized operations
- **Memory Pooling**: Efficient memory management
- **Cache Optimization**: Smart caching strategies

### Memory Management:
- **Garbage Collection**: Automatic memory cleanup
- **Buffer Limits**: Prevents memory overflow
- **Lazy Loading**: Load resources only when needed
- **Memory Monitoring**: Track and optimize usage

## 📈 Monitoring and Metrics:

### Performance Metrics:
- **FPS**: Frames processed per second
- **Latency**: Response time measurements
- **Accuracy**: Gesture recognition accuracy
- **CPU/Memory**: Resource usage tracking

### Health Checks:
- **System Status**: Overall system health
- **Component Status**: Individual component health
- **Error Rates**: Track and analyze errors
- **Performance Trends**: Long-term performance analysis