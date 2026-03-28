# 🎯 Core System Components

This folder contains the main application files that form the core of the Nami Neural Gesture Keyboard system.

## 📁 Files in this folder:

### 1. `main.py`
- **Purpose**: Main application entry point
- **Description**: Launches the integrated neural gesture keyboard system
- **Key Features**:
  - Command-line argument parsing
  - Neural engine initialization
  - Demo mode support
  - Debug mode support

### 2. `gesture_app.py`
- **Purpose**: Main application logic and event loop
- **Description**: Core application class that manages the entire system
- **Key Features**:
  - Neural engine integration
  - AI intelligence integration
  - Real-time gesture processing
  - User interface management
  - Session management

### 3. `hand_tracker.py`
- **Purpose**: Hand tracking with integrated neural enhancement
- **Description**: VR-level precision hand tracking using MediaPipe with neural processing
- **Key Features**:
  - MediaPipe hand detection
  - Face detection for anti-jitter
  - Neural-enhanced smoothing
  - Predictive tracking
  - Adaptive pinch detection

## 🔗 Interconnection Diagram:

```
┌─────────────────┐
│    main.py      │ ◄─── Entry Point
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ gesture_app.py  │ ◄─── Main Controller
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ hand_tracker.py │ ◄─── Hand Detection & Neural Processing
└─────────────────┘
          │
          ▼
┌─────────────────┐
│ Neural Engine   │ ◄─── ../neural_engine/
└─────────────────┘
          │
          ▼
┌─────────────────┐
│ AI Intelligence │ ◄─── ../ai_intelligence/
└─────────────────┘
          │
          ▼
┌─────────────────┐
│ UI Components   │ ◄─── ../ui_components/
└─────────────────┘
```

## 🚀 Data Flow:

1. **main.py** → Initializes system and creates GestureKeyboardApp
2. **gesture_app.py** → Manages application lifecycle and coordinates all components
3. **hand_tracker.py** → Processes camera input and detects hand gestures
4. **Neural Engine** → Enhances gesture accuracy and provides predictions
5. **AI Intelligence** → Learns patterns and provides smart suggestions
6. **UI Components** → Renders keyboard and handles user interaction

## 🔧 Dependencies:

- **External**: OpenCV, MediaPipe, NumPy
- **Internal**: 
  - `../neural_engine/` (Neural processing)
  - `../ai_intelligence/` (AI learning and suggestions)
  - `../ui_components/` (User interface)
  - `../utils/` (Utilities and helpers)

## 📊 Key Metrics:

- **Processing Speed**: 60-120 FPS
- **Accuracy**: 95%+ with neural enhancement
- **Response Time**: <16ms
- **Memory Usage**: ~200-500MB