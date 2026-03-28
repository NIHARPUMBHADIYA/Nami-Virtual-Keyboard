

import cv2
import numpy as np
from collections import deque
from typing import Optional, Tuple, Dict, Any
import time

try:
    import mediapipe as mp
    MEDIAPIPE_AVAILABLE = True
except ImportError:
    MEDIAPIPE_AVAILABLE = False

from .nami_neural_engine import get_neural_engine, NeuralProcessingMode

class NeuralHandTracker:

    def __init__(self, neural_mode: NeuralProcessingMode = NeuralProcessingMode.ADAPTIVE):
        if not MEDIAPIPE_AVAILABLE:
            raise ImportError("MediaPipe required for neural hand tracking!")

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

        self.neural_mode = neural_mode
        self.neural_engine = get_neural_engine()

        self.tracking_state = {
            'last_valid_position': None,
            'frames_without_detection': 0,
            'max_frames_without_detection': 20,
            'velocity': (0, 0),
            'acceleration': (0, 0),
            'confidence_history': deque(maxlen=10),
            'position_history': deque(maxlen=15),
            'face_detection_history': deque(maxlen=5)
        }

        self.prediction_system = {
            'enabled': True,
            'prediction_strength': 0.8,
            'stability_threshold': 0.7,
            'confidence_boost': 1.3
        }

        self.pinch_system = {
            'history': deque(maxlen=8),
            'adaptive_threshold': 60,
            'confidence_history': deque(maxlen=6),
            'neural_enhancement': True
        }

        print("🤖 Neural Hand Tracker initialized")
        print(f"   Neural Mode: {neural_mode.value}")
        print(f"   Neural Engine: {'CONNECTED' if self.neural_engine else 'STANDALONE'}")
        print(f"   Advanced Prediction: ENABLED")
        print(f"   Adaptive Thresholds: ENABLED")

    def find_hands(self, frame: np.ndarray) -> Optional[Tuple[Tuple[int, int], Tuple[int, int], bool]]:

        start_time = time.time()
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w = frame.shape[:2]

        face_region = self._detect_face_region(rgb_frame, w, h)

        results = self.hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]

            index_tip = hand_landmarks.landmark[8]
            thumb_tip = hand_landmarks.landmark[4]

            index_pos = (int(index_tip.x * w), int(index_tip.y * h))
            thumb_pos = (int(thumb_tip.x * w), int(thumb_tip.y * h))

            near_face = self._is_near_face(index_pos, face_region)

            base_confidence = self._calculate_base_confidence(hand_landmarks, near_face)

            if self.neural_engine:
                hand_data = (index_pos, thumb_pos, near_face)
                neural_result = self.neural_engine.process_gesture(hand_data, (h, w))

                if neural_result['neural_enhanced']:

                    enhanced_pos = neural_result['position']
                    enhanced_confidence = neural_result['confidence']

                    self._update_tracking_state(enhanced_pos, enhanced_confidence, near_face)

                    return (enhanced_pos, thumb_pos, near_face)

            self._update_tracking_state(index_pos, base_confidence, near_face)
            return (index_pos, thumb_pos, near_face)

        return self._handle_no_detection(w, h)

    def get_cursor_position(self, hand_data: Optional[Any], frame_shape: Tuple[int, int]) -> Tuple[int, int]:

        if not hand_data:

            if self.tracking_state['last_valid_position']:
                return self.tracking_state['last_valid_position'][0]
            return (frame_shape[1]//2, frame_shape[0]//2)

        (index_pos, thumb_pos, near_face) = hand_data

        if self.neural_engine and self.prediction_system['enabled']:

            insights = self.neural_engine.get_neural_insights()
            stability = float(insights['real_time_metrics']['gesture_stability'].rstrip('%')) / 100

            if stability > self.prediction_system['stability_threshold']:

                smoothing_factor = 0.9
            else:

                smoothing_factor = 0.9 if near_face else 0.95  # More responsive

            if hasattr(self, 'prev_cursor_pos') and self.prev_cursor_pos:
                smooth_x = int(smoothing_factor * index_pos[0] + (1 - smoothing_factor) * self.prev_cursor_pos[0])
                smooth_y = int(smoothing_factor * index_pos[1] + (1 - smoothing_factor) * self.prev_cursor_pos[1])
                cursor_pos = (smooth_x, smooth_y)
            else:
                cursor_pos = index_pos

            self.prev_cursor_pos = cursor_pos
            return cursor_pos

        return self._standard_cursor_smoothing(index_pos, near_face)

    def is_pinching(self, hand_data: Optional[Any], threshold: float = 80) -> bool:  # More sensitive threshold

        if not hand_data:
            return False

        (index_pos, thumb_pos, near_face) = hand_data

        if self.neural_engine and self.pinch_system['neural_enhancement']:
            pinch_result = self.neural_engine.enhance_pinch_detection(hand_data, threshold)

            if pinch_result['neural_enhanced']:

                is_pinching = pinch_result['is_pinching']
                confidence = pinch_result['confidence']

                self.pinch_system['history'].append(is_pinching)
                self.pinch_system['confidence_history'].append(confidence)

                recent_pinches = list(self.pinch_system['history'])[-3:]  # Shorter history
                confirmation_count = sum(recent_pinches)

                return confirmation_count >= 1 and confidence > 0.4  # More sensitive

        return self._standard_pinch_detection(index_pos, thumb_pos, threshold)

    def get_advanced_metrics(self) -> Dict[str, Any]:

        neural_insights = {}
        if self.neural_engine:
            neural_insights = self.neural_engine.get_neural_insights()

        return {
            'tracking_state': {
                'frames_without_detection': self.tracking_state['frames_without_detection'],
                'has_valid_position': self.tracking_state['last_valid_position'] is not None,
                'velocity': self.tracking_state['velocity'],
                'acceleration': self.tracking_state['acceleration']
            },
            'prediction_system': self.prediction_system,
            'pinch_system': {
                'adaptive_threshold': self.pinch_system['adaptive_threshold'],
                'recent_confidence': list(self.pinch_system['confidence_history'])[-3:] if self.pinch_system['confidence_history'] else []
            },
            'neural_insights': neural_insights
        }

    def _detect_face_region(self, rgb_frame: np.ndarray, w: int, h: int) -> Optional[Dict[str, int]]:

        face_results = self.face_detection.process(rgb_frame)

        if face_results.detections:
            detection = face_results.detections[0]
            bbox = detection.location_data.relative_bounding_box

            face_region = {
                'x': int(bbox.xmin * w),
                'y': int(bbox.ymin * h),
                'w': int(bbox.width * w),
                'h': int(bbox.height * h)
            }

            self.tracking_state['face_detection_history'].append(face_region)
            return face_region

        if self.tracking_state['face_detection_history']:
            return self.tracking_state['face_detection_history'][-1]

        return None

    def _is_near_face(self, position: Tuple[int, int], face_region: Optional[Dict[str, int]]) -> bool:

        if not face_region:
            return False

        x, y = position
        fx, fy, fw, fh = face_region['x'], face_region['y'], face_region['w'], face_region['h']

        margin = 0.3
        expanded_x = fx - int(fw * margin)
        expanded_y = fy - int(fh * margin)
        expanded_w = int(fw * (1 + margin * 2))
        expanded_h = int(fh * (1 + margin * 2))

        return (expanded_x < x < expanded_x + expanded_w and
                expanded_y < y < expanded_y + expanded_h)

    def _calculate_base_confidence(self, hand_landmarks: Any, near_face: bool) -> float:

        base_confidence = 0.8

        if near_face:
            base_confidence *= 0.75

        return base_confidence

    def _update_tracking_state(self, position: Tuple[int, int], confidence: float, near_face: bool):

        current_time = time.time()

        self.tracking_state['position_history'].append((position, current_time))
        self.tracking_state['confidence_history'].append(confidence)

        if len(self.tracking_state['position_history']) >= 2:
            recent_positions = list(self.tracking_state['position_history'])[-2:]
            pos1, time1 = recent_positions[0]
            pos2, time2 = recent_positions[1]

            dt = time2 - time1
            if dt > 0:
                vx = (pos2[0] - pos1[0]) / dt
                vy = (pos2[1] - pos1[1]) / dt
                self.tracking_state['velocity'] = (vx, vy)

        self.tracking_state['last_valid_position'] = (position, confidence, near_face)
        self.tracking_state['frames_without_detection'] = 0

    def _handle_no_detection(self, w: int, h: int) -> Optional[Tuple[Tuple[int, int], Tuple[int, int], bool]]:

        self.tracking_state['frames_without_detection'] += 1

        if (self.neural_engine and
            self.tracking_state['last_valid_position'] and
            self.tracking_state['frames_without_detection'] < self.tracking_state['max_frames_without_detection']):

            (last_pos, last_confidence, last_near_face) = self.tracking_state['last_valid_position']

            velocity = self.tracking_state['velocity']
            predicted_x = max(0, min(last_pos[0] + int(velocity[0] * 2), w - 1))
            predicted_y = max(0, min(last_pos[1] + int(velocity[1] * 2), h - 1))

            return ((predicted_x, predicted_y), last_pos, False)

        return None

    def _standard_cursor_smoothing(self, raw_position: Tuple[int, int], near_face: bool) -> Tuple[int, int]:

        smoothing_factor = 0.9 if near_face else 0.95  # More responsive

        if hasattr(self, 'prev_cursor_pos') and self.prev_cursor_pos:
            smooth_x = int(smoothing_factor * raw_position[0] + (1 - smoothing_factor) * self.prev_cursor_pos[0])
            smooth_y = int(smoothing_factor * raw_position[1] + (1 - smoothing_factor) * self.prev_cursor_pos[1])
            cursor_pos = (smooth_x, smooth_y)
        else:
            cursor_pos = raw_position

        self.prev_cursor_pos = cursor_pos
        return cursor_pos

    def _standard_pinch_detection(self, index_pos: Tuple[int, int], thumb_pos: Tuple[int, int], threshold: float) -> bool:

        distance = np.sqrt((index_pos[0] - thumb_pos[0])**2 + (index_pos[1] - thumb_pos[1])**2)

        is_pinching = distance < threshold
        self.pinch_system['history'].append(is_pinching)

        recent_pinches = list(self.pinch_system['history'])[-2:]  # Shorter history
        return sum(recent_pinches) >= 1  # More sensitive