

import cv2
import numpy as np
from collections import deque
import time

try:
    import mediapipe as mp
    MEDIAPIPE_AVAILABLE = True
except ImportError:
    MEDIAPIPE_AVAILABLE = False

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from neural_engine.nami_neural_engine import initialize_neural_engine, NeuralProcessingMode, get_neural_engine
    NEURAL_ENGINE_AVAILABLE = True
except ImportError:
    NEURAL_ENGINE_AVAILABLE = False

class VRHandTracker:

    def __init__(self):
        if not MEDIAPIPE_AVAILABLE:
            raise ImportError("MediaPipe required!")

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            model_complexity=1,
            min_detection_confidence=0.7,  # Higher confidence for better accuracy
            min_tracking_confidence=0.8   # Higher tracking confidence
        )

        self.mp_face = mp.solutions.face_detection
        self.face_detection = self.mp_face.FaceDetection(min_detection_confidence=0.4)

        self.last_valid_position = None
        self.frames_without_detection = 0
        self.max_frames_without_detection = 20
        self.velocity = (0, 0)
        self.prev_pos = None
        self.pinch_history = deque(maxlen=8)

        self.neural_engine = None
        self.neural_enhanced = False
        self._initialize_neural_engine()

        self.neural_smoothing_factor = 0.85
        self.neural_confidence_boost = 1.2
        self.neural_prediction_enabled = True

        print(f"🧠 VR Hand Tracker initialized with Neural Engine: {'ACTIVE' if self.neural_enhanced else 'DISABLED'}")

    def _initialize_neural_engine(self):

        if NEURAL_ENGINE_AVAILABLE:
            try:

                self.neural_engine = get_neural_engine()

                if not self.neural_engine:

                    self.neural_engine = initialize_neural_engine(NeuralProcessingMode.ADAPTIVE)
                    self.neural_engine.start()

                self.neural_enhanced = True
                print("   🚀 Neural Engine integrated successfully")

            except Exception as e:
                print(f"   ⚠️ Neural Engine initialization failed: {e}")
                self.neural_enhanced = False
        else:
            print("   ℹ️ Neural Engine components not available - using standard tracking")

    def find_hands(self, frame):

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w = frame.shape[:2]

        face_results = self.face_detection.process(rgb_frame)
        face_region = None
        if face_results.detections:
            detection = face_results.detections[0]
            bbox = detection.location_data.relative_bounding_box
            face_region = {
                'x': int(bbox.xmin * w), 'y': int(bbox.ymin * h),
                'w': int(bbox.width * w), 'h': int(bbox.height * h)
            }

        results = self.hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]

            index_tip = hand_landmarks.landmark[8]
            x, y = int(index_tip.x * w), int(index_tip.y * h)

            near_face = self._is_near_face((x, y), face_region)

            thumb_tip = hand_landmarks.landmark[4]
            thumb_x, thumb_y = int(thumb_tip.x * w), int(thumb_tip.y * h)

            if self.last_valid_position:
                (last_x, last_y), _, _ = self.last_valid_position
                self.velocity = (x - last_x, y - last_y)

            self.frames_without_detection = 0
            raw_result = ((x, y), (thumb_x, thumb_y), near_face)

            if self.neural_enhanced and self.neural_engine:
                try:
                    neural_result = self.neural_engine.process_gesture(raw_result, (h, w))
                    if neural_result.get('neural_enhanced'):

                        enhanced_pos = neural_result['position']
                        enhanced_result = (enhanced_pos, (thumb_x, thumb_y), near_face)
                        self.last_valid_position = enhanced_result
                        return enhanced_result
                except Exception as e:

                    pass

            self.last_valid_position = raw_result
            return raw_result

        if self.last_valid_position:
            self.frames_without_detection += 1
            if self.frames_without_detection < self.max_frames_without_detection:
                (last_x, last_y), (thumb_x, thumb_y), _ = self.last_valid_position

                if self.neural_enhanced and self.neural_prediction_enabled:

                    prediction_strength = max(0.5, 1.0 - (self.frames_without_detection / self.max_frames_without_detection))
                    predicted_x = max(0, min(last_x + int(self.velocity[0] * prediction_strength), w - 1))
                    predicted_y = max(0, min(last_y + int(self.velocity[1] * prediction_strength), h - 1))
                else:

                    predicted_x = max(0, min(last_x + self.velocity[0], w - 1))
                    predicted_y = max(0, min(last_y + self.velocity[1], h - 1))

                return ((predicted_x, predicted_y), (thumb_x, thumb_y), False)

        return None

    def _is_near_face(self, position, face_region):

        if not face_region:
            return False

        x, y = position
        fx, fy, fw, fh = face_region['x'], face_region['y'], face_region['w'], face_region['h']

        margin = 0.3 if self.neural_enhanced else 0.2
        expanded_x = fx - int(fw * margin)
        expanded_y = fy - int(fh * margin)
        expanded_w = int(fw * (1 + margin * 2))
        expanded_h = int(fh * (1 + margin * 2))

        return (expanded_x < x < expanded_x + expanded_w and
                expanded_y < y < expanded_y + expanded_h)

    def get_cursor_position(self, hand_data, frame_shape):

        if not hand_data:
            return self.prev_pos if self.prev_pos else (frame_shape[1]//2, frame_shape[0]//2)

        (raw_x, raw_y), _, near_face = hand_data

        if self.neural_enhanced:

            base_alpha = 0.7 if near_face else 0.9
            neural_alpha = base_alpha * self.neural_smoothing_factor
        else:

            neural_alpha = 0.85 if near_face else 0.98

        if self.prev_pos:
            smooth_x = int(neural_alpha * raw_x + (1 - neural_alpha) * self.prev_pos[0])
            smooth_y = int(neural_alpha * raw_y + (1 - neural_alpha) * self.prev_pos[1])
        else:
            smooth_x, smooth_y = raw_x, raw_y

        self.prev_pos = (smooth_x, smooth_y)
        return (smooth_x, smooth_y)

    def is_pinching(self, hand_data, threshold=80):  # More sensitive threshold

        if not hand_data:
            return False

        (index_x, index_y), (thumb_x, thumb_y), _ = hand_data

        if self.neural_enhanced and self.neural_engine:
            try:
                pinch_result = self.neural_engine.enhance_pinch_detection(hand_data, threshold)
                if pinch_result.get('neural_enhanced'):
                    is_pinching = pinch_result['is_pinching']
                    confidence = pinch_result['confidence']

                    self.pinch_history.append(is_pinching and confidence > 0.4)  # More sensitive

                    recent_pinches = list(self.pinch_history)[-3:]  # Shorter history
                    return sum(recent_pinches) >= 1  # More responsive
            except Exception as e:

                pass

        distance = np.sqrt((index_x - thumb_x)**2 + (index_y - thumb_y)**2)

        if self.neural_enhanced:
            adaptive_threshold = threshold * (1.1 - 0.1 * self.neural_confidence_boost)
        else:
            adaptive_threshold = threshold

        self.pinch_history.append(distance < adaptive_threshold)
        return sum(self.pinch_history) >= 3

    def get_neural_status(self):

        return {
            'neural_enhanced': self.neural_enhanced,
            'neural_engine_active': self.neural_engine is not None,
            'smoothing_factor': self.neural_smoothing_factor,
            'confidence_boost': self.neural_confidence_boost,
            'prediction_enabled': self.neural_prediction_enabled
        }
