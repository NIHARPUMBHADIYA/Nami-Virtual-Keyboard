# 🎨 UI Components

This folder contains all user interface components for the Nami Neural Gesture Keyboard system.

## 📁 Files in this folder:

### 1. `virtual_keyboard.py`
- **Purpose**: Standard virtual keyboard implementation
- **Description**: Basic virtual keyboard with modern design and animations
- **Key Features**:
  - QWERTY layout with centered design
  - Hover effects and visual feedback
  - Text area with blinking cursor
  - ENTER button integration
  - Transparent design with borders

### 2. `welcome_screen.py`
- **Purpose**: Application welcome screen
- **Description**: Introductory screen shown at application startup
- **Key Features**:
  - Animated welcome message
  - System information display
  - Smooth transitions
  - Auto-dismiss functionality

## 🔗 Interconnection Diagram:

```
┌─────────────────────────┐
│    welcome_screen.py    │ ◄─── App Startup
└───────────┬─────────────┘
            │
            │ (Shows welcome, then transitions)
            │
            ▼
┌─────────────────────────┐
│   virtual_keyboard.py   │ ◄─── Main UI Component
└───────────┬─────────────┘
            │
            │ ┌─── Draws keyboard layout
            │ │
            │ ├─── Handles hover effects
            │ │
            │ ├─── Manages text area
            │ │
            │ └─── Processes key clicks
            │
            ▼
┌─────────────────────────┐
│     ../core/            │ ◄─── Integration Point
│   gesture_app.py        │
└───────────┬─────────────┘
            │
            │ (Enhanced by AI keyboard)
            │
            ▼
┌─────────────────────────┐
│  ../ai_intelligence/    │ ◄─── AI Enhancement
│ ai_virtual_keyboard.py  │
└─────────────────────────┘
```

## 🎨 UI Design Philosophy:

### Visual Design
- **Modern Aesthetic**: Clean, minimalist design
- **High Contrast**: White borders on dark background
- **Responsive Feedback**: Visual changes on interaction
- **Neural Theming**: Purple/magenta colors for AI features

### User Experience
- **Intuitive Layout**: Standard QWERTY keyboard
- **Clear Feedback**: Hover effects and color changes
- **Smooth Animations**: Fluid transitions and effects
- **Accessibility**: High contrast and clear typography

### Performance
- **Efficient Rendering**: Optimized drawing routines
- **Smooth Interactions**: 60+ FPS rendering
- **Low Latency**: Immediate visual feedback
- **Memory Efficient**: Minimal resource usage

## 🖥️ UI Components Breakdown:

### Virtual Keyboard Layout:
```
┌─────────────────────────────────────────────┐
│  Q  W  E  R  T  Y  U  I  O  P              │
│   A  S  D  F  G  H  J  K  L                │
│    Z  X  C  V  B  N  M                     │
│     .  ?  !  ,  SPACE  BACKSPACE           │
└─────────────────────────────────────────────┘
```

### Text Area:
```
┌─────────────────────────────────┬─────────┐
│ Your typed text appears here... │  ENTER  │
└─────────────────────────────────┴─────────┘
```

### AI Enhancement (when available):
```
┌─────────────────────────────────────────────┐
│  [word1]  [word2]  [word3]  [word4]  [🧠]   │ ◄─── AI Suggestions
├─────────────────────────────────────────────┤
│ Your typed text appears here... │  ENTER  │ ◄─── Text Area
├─────────────────────────────────────────────┤
│  Q  W  E  R  T  Y  U  I  O  P              │ ◄─── Keyboard
│   A  S  D  F  G  H  J  K  L                │
│    Z  X  C  V  B  N  M                     │
│     .  ?  !  ,  SPACE  BACKSPACE           │
└─────────────────────────────────────────────┘
```

## 🎯 Key Features:

### Standard Keyboard
- **Centered Layout**: Automatically centers on screen
- **Adaptive Sizing**: Adjusts to different screen sizes
- **Hover Effects**: Cyan glow on key hover
- **Text Rendering**: High-contrast text with outlines

### AI-Enhanced Keyboard
- **Suggestion Area**: Smart word predictions above text
- **Neural Colors**: Purple/magenta theme for AI features
- **Real-time Stats**: Live WPM and accuracy display
- **Interactive Suggestions**: Clickable word completions

### Welcome Screen
- **Animated Intro**: Smooth fade-in effects
- **System Info**: Shows neural engine status
- **Auto-dismiss**: Automatically closes after timeout
- **User Control**: Can be closed manually

## 🔧 Dependencies:

- **External**: OpenCV (cv2), NumPy, Time
- **Internal**: 
  - `../core/gesture_app.py` (Main integration)
  - `../ai_intelligence/` (AI enhancements)
  - `../neural_engine/` (Neural processing)

## 📊 Performance Specifications:

- **Rendering Speed**: 60-120 FPS
- **Response Time**: <16ms for visual feedback
- **Memory Usage**: 20-50MB for UI components
- **Screen Resolution**: Supports 720p to 4K
- **Color Depth**: 24-bit RGB with alpha channel