

import cv2
import time
import os
import numpy as np
from typing import Optional, Dict, Any

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

try:
    import mediapipe as mp
    MEDIAPIPE_AVAILABLE = True
except ImportError:
    MEDIAPIPE_AVAILABLE = False

from .neural_hand_tracker import NeuralHandTracker
from .nami_neural_engine import initialize_neural_engine, NeuralProcessingMode
from ..ui_components.virtual_keyboard import VirtualKeyboard
from ..utils.text_to_speech import TextToSpeech
from ..utils.logger import SessionLogger
# Welcome screen removed for direct startup
from ..utils.error_handler import error_handler

try:
    from ..ai_intelligence.nami_ai_intelligence import initialize_nami_ai, get_nami_ai
    from ..ai_intelligence.ai_virtual_keyboard import AIVirtualKeyboard
    AI_COMPONENTS_AVAILABLE = True
except ImportError:
    AI_COMPONENTS_AVAILABLE = False

class NeuralGestureKeyboardApp:

    def __init__(self, neural_mode: NeuralProcessingMode = NeuralProcessingMode.ADAPTIVE):
        if not MEDIAPIPE_AVAILABLE:
            print("ERROR: MediaPipe required!")
            print("Install with: pip install mediapipe")
            exit(1)

        print("🧠 Initializing Neural Gesture Keyboard...")

        self.neural_engine = initialize_neural_engine(neural_mode)
        self.neural_engine.start()

        error_handler.start_monitoring()

        self.hand_tracker = NeuralHandTracker(neural_mode)
        
        # Initialize AI first, then keyboard
        self._initialize_ai_intelligence()
        
        if AI_COMPONENTS_AVAILABLE and self.ai_intelligence:
            self.keyboard = AIVirtualKeyboard()
            self.ai_enhanced = True
        else:
            self.keyboard = VirtualKeyboard()
            self.ai_enhanced = False
            
        self.tts = TextToSpeech()
        self.logger = SessionLogger()

        self.text = ""
        self.last_pinch_time = 0
        self.pinch_cooldown = 0.1  # Faster response
        self.was_pinching = False
        self.fps_counter = []
        self.window_name = "Nami Neural Gesture Keyboard"
        self.window_closed = False

        self.neural_stats = {
            'total_neural_predictions': 0,
            'successful_neural_enhancements': 0,
            'accuracy_improvements': 0,
            'processing_time_savings': 0.0
        }

        self.show_neural_overlay = True
        self.show_performance_metrics = True
        self.neural_visualization = True

        print("✅ Neural Gesture Keyboard initialized")
        print(f"   Neural Engine: {neural_mode.value.upper()}")
        print(f"   Advanced Tracking: ENABLED")
        print(f"   Real-time Optimization: ACTIVE")

    def _initialize_ai_intelligence(self):
        """Initialize AI Intelligence system."""
        if AI_COMPONENTS_AVAILABLE:
            try:
                self.ai_intelligence = initialize_nami_ai()
                print("   🤖 AI Intelligence initialized successfully")
                print(f"      Vocabulary: {len(self.ai_intelligence.word_database.word_frequencies)} words")
                print(f"      User Profile: {self.ai_intelligence.user_profile.total_sessions} sessions")
            except Exception as e:
                print(f"   ⚠️ AI Intelligence initialization failed: {e}")
                self.ai_intelligence = None
        else:
            print("   ℹ️ AI Intelligence components not available")
            self.ai_intelligence = None

    def run(self):

        print("🙏 Neural Speaking: Jai Swaminarayan - Nami Neural Engine Active")
        self.tts.speak("Jai Swaminarayan. Nami Neural Engine is now active.")

        # Welcome screen removed - direct startup

        cap = error_handler.safe_camera_init(0)

        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL | cv2.WINDOW_GUI_EXPANDED)
        cv2.resizeWindow(self.window_name, 1280, 720)
        cv2.setWindowProperty(self.window_name, cv2.WND_PROP_ASPECT_RATIO, cv2.WINDOW_FREERATIO)

        self._print_neural_welcome_message()

        while True:
            loop_start_time = time.time()

            ret, frame = error_handler.safe_frame_read(cap)
            if not ret or frame is None:
                continue

            frame = cv2.flip(frame, 1)

            try:
                window_rect = cv2.getWindowImageRect(self.window_name)
                if window_rect[2] > 0 and window_rect[3] > 0:
                    frame = cv2.resize(frame, (window_rect[2], window_rect[3]))
            except:
                pass

            h, w = frame.shape[:2]

            hand_data = self._neural_hand_detection(frame)

            cursor_pos = None
            if hand_data:
                cursor_pos = self._process_neural_hand_data(frame, hand_data)
            else:
                self._draw_no_hand_indicator(frame)

            self._draw_neural_interface(frame, cursor_pos)

            if self.show_neural_overlay:
                self._draw_neural_overlay(frame, loop_start_time)

            error_handler.safe_imshow(self.window_name, frame)

            if self._handle_window_events():
                break

        self._neural_cleanup()

    def _neural_hand_detection(self, frame: np.ndarray) -> Optional[Any]:

        try:
            hand_data = self.hand_tracker.find_hands(frame)

            if hand_data:
                self.neural_stats['total_neural_predictions'] += 1

                if hasattr(self.hand_tracker, 'neural_engine') and self.hand_tracker.neural_engine:
                    self.neural_stats['successful_neural_enhancements'] += 1

            return hand_data

        except Exception as e:
            print(f"⚠️ Neural hand detection error: {e}")
            return None

    def _process_neural_hand_data(self, frame: np.ndarray, hand_data: Any) -> Optional[tuple]:

        cursor_pos = self.hand_tracker.get_cursor_position(hand_data, frame.shape)

        if cursor_pos is None:
            return None

        self._draw_neural_cursor(frame, cursor_pos, hand_data)

        is_pinching = self.hand_tracker.is_pinching(hand_data)

        if is_pinching:

            self._draw_neural_pinch_indicator(frame, cursor_pos)

            self._handle_neural_pinch_gesture(cursor_pos)

        self.was_pinching = is_pinching
        return cursor_pos

    def _draw_neural_cursor(self, frame: np.ndarray, cursor_pos: tuple, hand_data: Any):

        x, y = cursor_pos

        if self.neural_engine:
            insights = self.neural_engine.get_neural_insights()
            confidence = float(insights['real_time_metrics']['confidence'].rstrip('%')) / 100
            stability = float(insights['real_time_metrics']['gesture_stability'].rstrip('%')) / 100
        else:
            confidence = 0.8
            stability = 0.8

        base_size = 15  # Larger, more visible cursor
        confidence_size = int(base_size * (0.7 + confidence * 0.3))

        if stability > 0.8:
            color = (0, 255, 0)
        elif stability > 0.6:
            color = (0, 255, 255)
        else:
            color = (0, 165, 255)

        cv2.circle(frame, (x, y), confidence_size + 2, color, 2)
        cv2.circle(frame, (x, y), confidence_size, color, -1)
        cv2.circle(frame, (x, y), max(1, confidence_size - 3), (255, 255, 255), -1)

        # Removed text display

    def _draw_neural_pinch_indicator(self, frame: np.ndarray, cursor_pos: tuple):

        x, y = cursor_pos

        pulse_size = int(12 + 6 * np.sin(time.time() * 10))  # Larger pulse
        cv2.circle(frame, (x, y), pulse_size, (0, 255, 0), 2)

        # Removed text display

    def _draw_no_hand_indicator(self, frame: np.ndarray):

        cv2.putText(frame, "Show Hand - Neural Tracking Ready", (10, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 100, 0), 2)

        if self.neural_engine:
            cv2.putText(frame, "🧠 Neural Engine: ACTIVE", (10, 90),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 1)

    def _draw_neural_interface(self, frame: np.ndarray, cursor_pos: Optional[tuple]):

        if self.ai_enhanced:
            # Update AI with current word for suggestions
            self.keyboard.update_current_word(self.text)
            # Draw AI suggestions
            self.keyboard.draw_ai_suggestions(frame, cursor_pos)

        error_handler.safe_keyboard_draw(self.keyboard, frame, cursor_pos)
        error_handler.safe_text_area_draw(self.keyboard, frame, self.text, cursor_pos)

        if cursor_pos and self.neural_visualization:

            predicted_key = self.keyboard.get_key_at_position(cursor_pos)
            if predicted_key:

                pass

    def _draw_neural_overlay(self, frame: np.ndarray, loop_start_time: float):

        h, w = frame.shape[:2]

        fps = 1.0 / (time.time() - loop_start_time) if time.time() > loop_start_time else 0
        self.fps_counter.append(fps)
        if len(self.fps_counter) > 30:
            self.fps_counter.pop(0)
        avg_fps = sum(self.fps_counter) / len(self.fps_counter) if self.fps_counter else 0

        if self.neural_engine:
            insights = self.neural_engine.get_neural_insights()

            cv2.putText(frame, f"FPS: {int(avg_fps)}", (10, 30),
                       cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 255, 0), 2)

            y_offset = 60
            metrics = [
                f"Neural Accuracy: {insights['real_time_metrics']['accuracy']}",
                f"Confidence: {insights['real_time_metrics']['confidence']}",
                f"Stability: {insights['real_time_metrics']['gesture_stability']}",
                f"Processing: {insights['real_time_metrics']['processing_time']}",
                f"Gestures: {insights['performance_stats']['gestures_processed']}"
            ]

            for i, metric in enumerate(metrics):
                cv2.putText(frame, metric, (10, y_offset + i * 25),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

        cv2.putText(frame, "Nami Neural Engine", (10, h - 20),
                   cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 0, 255), 1)

        if self.neural_stats['total_neural_predictions'] > 0:
            enhancement_rate = (self.neural_stats['successful_neural_enhancements'] /
                              self.neural_stats['total_neural_predictions']) * 100
            cv2.putText(frame, f"Neural Enhancement: {enhancement_rate:.1f}%",
                       (w - 250, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 1)

    def _handle_neural_pinch_gesture(self, cursor_pos: tuple):

        current_time = time.time()

        if not self.was_pinching and current_time - self.last_pinch_time > self.pinch_cooldown:

            if self.ai_enhanced:
                if self.keyboard.is_enter_button_clicked(cursor_pos):
                    print(f"✓ NEURAL AI ENTER pressed!")
                    self.handle_key_press('ENTER')
                    self.last_pinch_time = current_time
                    return

                key = self.keyboard.get_key_at_position(cursor_pos)
                if key:
                    if key.startswith('SUGGESTION:'):
                        suggestion = key.replace('SUGGESTION:', '')
                        print(f"✓ NEURAL AI Suggestion '{suggestion}' selected!")
                        self._handle_suggestion_selection(suggestion)
                    else:
                        print(f"✓ NEURAL AI Key '{key}' pressed!")
                        self.handle_key_press(key)
                    self.last_pinch_time = current_time
                    self.neural_stats['accuracy_improvements'] += 1
            else:
                if error_handler.safe_enter_check(self.keyboard, cursor_pos):
                    print(f"✓ NEURAL ENTER pressed!")
                    self.handle_key_press('ENTER')
                    self.last_pinch_time = current_time
                    self.neural_stats['accuracy_improvements'] += 1
                else:
                    key = error_handler.safe_key_press(self.keyboard, cursor_pos)
                    if key:
                        print(f"✓ Neural Key '{key}' pressed!")
                        self.handle_key_press(key)
                        self.last_pinch_time = current_time
                    self.neural_stats['accuracy_improvements'] += 1

    def _handle_suggestion_selection(self, suggestion):
        """Handle AI suggestion selection."""
        if not self.ai_intelligence:
            return

        words = self.text.split()
        if words and not self.text.endswith(' '):
            # Replace the current incomplete word with the suggestion
            words[-1] = suggestion
            self.text = ' '.join(words) + ' '
        else:
            # Add new word if no incomplete word exists
            self.text += suggestion + ' '

        # Update the keyboard's current word to trigger new suggestions
        self.keyboard.update_current_word(self.text)

        self.neural_stats['neural_enhancements'] += 1
        self.ai_intelligence.process_keystroke(suggestion)

    def _handle_window_events(self) -> bool:

        key = cv2.waitKey(1) & 0xFF

        try:
            visible = cv2.getWindowProperty(self.window_name, cv2.WND_PROP_VISIBLE)
            if visible < 1:
                print("✓ Window closed by user")
                return True
        except:
            return True

        if key == ord('q'):
            print("✓ Exiting Neural Gesture Keyboard")
            return True
        elif key == ord('n'):

            self.show_neural_overlay = not self.show_neural_overlay
            print(f"✓ Neural overlay: {'ON' if self.show_neural_overlay else 'OFF'}")
        elif key == ord('v'):

            self.neural_visualization = not self.neural_visualization
            print(f"✓ Neural visualization: {'ON' if self.neural_visualization else 'OFF'}")
        elif key == ord('i'):

            self._print_neural_insights()

        return False

    def _print_neural_welcome_message(self):

        print("=" * 70)
        print("    🧠 NAMI NEURAL GESTURE KEYBOARD")
        print("=" * 70)
        print("✓ Neural Engine: ACTIVE")
        print("✓ Advanced Gesture Prediction")
        print("✓ Adaptive Learning System")
        print("✓ Real-time Optimization")
        print("✓ Enhanced Accuracy & Stability")
        print("=" * 70)
        print("\nNEURAL CONTROLS:")
        print("  • Move hand = Neural cursor tracking")
        print("  • Pinch fingers = Neural-enhanced key press")
        print("  • Press 'q' = Quit")
        print("  • Press 'n' = Toggle neural overlay")
        print("  • Press 'v' = Toggle neural visualization")
        print("  • Press 'i' = Show neural insights")
        print("=" * 70)

    def _print_neural_insights(self):

        if not self.neural_engine:
            print("Neural Engine not available")
            return

        insights = self.neural_engine.get_neural_insights()

        print("\n" + "="*50)
        print("🧠 NEURAL INSIGHTS")
        print("="*50)
        print(f"Engine Status: {insights['engine_status']}")
        print(f"Processing Mode: {insights['processing_mode']}")
        print("\nReal-time Metrics:")
        for key, value in insights['real_time_metrics'].items():
            print(f"  {key}: {value}")
        print("\nPerformance Stats:")
        for key, value in insights['performance_stats'].items():
            print(f"  {key}: {value}")
        print("="*50)

    def _neural_cleanup(self):

        if self.neural_engine:
            self.neural_engine.stop()

        error_handler.stop_monitoring()

        cv2.destroyAllWindows()

        self._print_final_neural_stats()

    def _print_final_neural_stats(self):

        print("\n" + "="*60)
        print("🧠 NAMI NEURAL ENGINE - FINAL STATISTICS")
        print("="*60)
        print(f"Total Neural Predictions: {self.neural_stats['total_neural_predictions']}")
        print(f"Successful Enhancements: {self.neural_stats['successful_neural_enhancements']}")
        print(f"Accuracy Improvements: {self.neural_stats['accuracy_improvements']}")

        if self.neural_stats['total_neural_predictions'] > 0:
            enhancement_rate = (self.neural_stats['successful_neural_enhancements'] /
                              self.neural_stats['total_neural_predictions']) * 100
            print(f"Neural Enhancement Rate: {enhancement_rate:.1f}%")

        print("="*60)
        print("Thank you for using Nami Neural Engine! 🚀")

    def handle_key_press(self, key: str):

        if key == 'SPACE':
            self.text += ' '
        elif key == 'BACKSPACE':
            self.text = self.text[:-1]
        elif key == 'ENTER':
            if self.text:
                print(f"Neural Speaking: {self.text}")
                error_handler.safe_tts_speak(self.tts, self.text)
                error_handler.safe_logger_log(self.logger, self.text)
            else:
                print("Neural Speaking: Empty")
                error_handler.safe_tts_speak(self.tts, "Empty")
        else:
            self.text += key

if __name__ == "__main__":

    app = NeuralGestureKeyboardApp(NeuralProcessingMode.ADAPTIVE)
    app.run()