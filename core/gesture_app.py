

import cv2
import time
import os
import numpy as np

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

try:
    import mediapipe as mp
    MEDIAPIPE_AVAILABLE = True
except ImportError:
    MEDIAPIPE_AVAILABLE = False

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.hand_tracker import VRHandTracker
from ui_components.virtual_keyboard import VirtualKeyboard
from utils.text_to_speech import TextToSpeech
from utils.logger import SessionLogger
# Welcome screen removed for direct startup
from utils.error_handler import error_handler

try:
    from neural_engine.neural_config_manager import initialize_config_manager, ConfigurationProfile
    from neural_engine.neural_system_monitor import initialize_system_monitor
    NEURAL_COMPONENTS_AVAILABLE = True
except ImportError:
    NEURAL_COMPONENTS_AVAILABLE = False

try:
    from ai_intelligence.nami_ai_intelligence import initialize_nami_ai, get_nami_ai
    from ai_intelligence.ai_virtual_keyboard import AIVirtualKeyboard
    AI_COMPONENTS_AVAILABLE = True
except ImportError:
    AI_COMPONENTS_AVAILABLE = False

class GestureKeyboardApp:

    def __init__(self):
        if not MEDIAPIPE_AVAILABLE:
            print("ERROR: MediaPipe required!")
            print("Install with: pip install mediapipe")
            exit(1)

        print("🧠 Initializing VR Gesture Keyboard with Neural Engine...")

        error_handler.start_monitoring()

        self.hand_tracker = VRHandTracker()

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
        self.pinch_confirmed_frames = 0
        self.is_fullscreen = False
        self.window_name = "Nami Neural Gesture Keyboard"
        self.window_closed = False

        self.config_manager = None
        self.system_monitor = None
        self.neural_enhanced = False
        self._initialize_neural_components()

        self.ai_intelligence = None
        self.ai_session_active = False

        self.show_neural_overlay = True
        self.neural_visualization = True

        self.neural_stats = {
            'total_gestures': 0,
            'neural_enhancements': 0,
            'accuracy_improvements': 0
        }
        
        # Flag to prevent immediate suggestion updates after selection
        self.suggestion_just_selected = False
        self.suggestion_cooldown_time = 0

    def _initialize_neural_components(self):

        if NEURAL_COMPONENTS_AVAILABLE:
            try:

                self.config_manager = initialize_config_manager()

                self.system_monitor = initialize_system_monitor(1.0)
                self.system_monitor.start_monitoring()

                self.neural_enhanced = True
                print("   ✅ Neural components initialized successfully")

            except Exception as e:
                print(f"   ⚠️ Neural components initialization failed: {e}")
                self.neural_enhanced = False
        else:
            print("   ℹ️ Neural components not available - using standard mode")

    def _initialize_ai_intelligence(self):

        if AI_COMPONENTS_AVAILABLE:
            try:

                self.ai_intelligence = initialize_nami_ai()
                print(f"   🤖 AI Intelligence object created: {self.ai_intelligence}")

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

        print("🙏 Speaking: Jai Swaminarayan")
        self.tts.speak("Jai Swaminarayan")

        # Welcome screen removed - direct startup

        cap = error_handler.safe_camera_init(0)

        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL | cv2.WINDOW_GUI_EXPANDED)
        cv2.resizeWindow(self.window_name, 1280, 720)

        cv2.setWindowProperty(self.window_name, cv2.WND_PROP_ASPECT_RATIO, cv2.WINDOW_FREERATIO)

        def on_window_close():
            self.window_closed = True

        try:
            cv2.setWindowProperty(self.window_name, cv2.WND_PROP_AUTOSIZE, cv2.WINDOW_AUTOSIZE)
        except:
            pass

        self._print_welcome_message()
        print("  • Click Maximize (□) = Fill screen")
        print("  • Press 'q' = Quit application")
        print("=" * 60)
        print("\nTIP: Use the maximize button (□) for fullscreen experience")
        print("=" * 60)

        while True:
            start_time = time.time()

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

            hand_data = error_handler.safe_hand_detection(self.hand_tracker, frame)

            cursor_pos = None
            if hand_data:
                cursor_pos = self._process_hand_data(frame, hand_data)
            else:
                cv2.putText(frame, "Show Hand", (10, 60),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 100, 0), 2)

            if self.ai_enhanced:
                # Check if suggestion cooldown has expired
                current_time = time.time()
                if self.suggestion_just_selected and current_time < self.suggestion_cooldown_time:
                    # Skip updating current word during cooldown
                    pass
                else:
                    # Reset the flag and update current word normally
                    self.suggestion_just_selected = False
                    self.keyboard.update_current_word(self.text)

                self.keyboard.draw_ai_suggestions(frame, cursor_pos)

                self.keyboard.draw_keyboard(frame, cursor_pos)
                self.keyboard.draw_text_area(frame, self.text, cursor_pos)
            else:

                error_handler.safe_keyboard_draw(self.keyboard, frame, cursor_pos)
                error_handler.safe_text_area_draw(self.keyboard, frame, self.text, cursor_pos)

            self._draw_fps(frame, start_time)

            error_handler.safe_imshow(self.window_name, frame)

            key = cv2.waitKey(1) & 0xFF

            window_exists = True
            try:

                visible = cv2.getWindowProperty(self.window_name, cv2.WND_PROP_VISIBLE)
                if visible < 1:
                    window_exists = False
            except:
                window_exists = False

            if key == 255 and not window_exists:
                print("✓ Window closed by user")
                break

            if self.window_closed:
                print("✓ Window closed by user")
                break

            if key == ord('q'):
                print("✓ Exiting Neural Gesture Keyboard")
                break

            elif key == ord('f'):
                print(f"✓ 'f' key pressed (key code: {key})")
                self._toggle_fullscreen()

            elif key == ord('n') and self.neural_enhanced:
                self.show_neural_overlay = not self.show_neural_overlay
                print(f"✓ Neural overlay: {'ON' if self.show_neural_overlay else 'OFF'}")

            elif key == ord('i') and self.neural_enhanced:
                self._print_neural_insights()

            elif key == ord('a') and self.ai_intelligence:
                self._print_ai_insights()

        if self.system_monitor:
            self.system_monitor.stop_monitoring()

        error_handler.stop_monitoring()
        cap.release()
        cv2.destroyAllWindows()

        self._print_final_stats()

    def _toggle_fullscreen(self):

        self.is_fullscreen = not self.is_fullscreen

        if self.is_fullscreen:
            print("✓ Fullscreen mode - Use maximize button (□) or press 'f' again to restore")

        else:
            print("✓ Windowed mode - Window restored to normal size")

    def _print_welcome_message(self):

        neural_status = self.hand_tracker.get_neural_status()

        print("=" * 70)
        if neural_status['neural_enhanced']:
            print("    🧠 VR-LEVEL PRECISION + NAMI NEURAL ENGINE 🧠")
        else:
            print("    VR-LEVEL PRECISION GESTURE KEYBOARD")
        print("=" * 70)
        print("✓ MediaPipe Hand Tracking")
        print("✓ Face Detection (anti-jitter)")
        print("✓ Velocity Prediction")
        print("✓ Session Logging")

        if neural_status['neural_enhanced']:
            print("✓ 🧠 Neural Engine: ACTIVE")
            print("✓ 🚀 Adaptive Learning")
            print("✓ 📊 Real-time Optimization")
            print("✓ 🎯 Enhanced Accuracy")

        if self.ai_intelligence:
            print("✓ 🤖 AI Intelligence: ACTIVE")
            print("✓ 📝 Pattern Learning")
            print("✓ 💡 Smart Suggestions")
            print("✓ 📊 Typing Analytics")

        print("=" * 70)
        print("\nCONTROLS:")
        print("  • Move hand = Neural cursor tracking")
        print("  • Pinch fingers = Neural-enhanced key press")
        print("  • Press 'q' = Quit")

        if neural_status['neural_enhanced']:
            print("  • Press 'n' = Toggle neural overlay")
            print("  • Press 'i' = Neural insights")

        if self.ai_intelligence:
            print("  • Press 'a' = AI insights")
            print("  • AI suggestions appear above text area")

    def _process_hand_data(self, frame, hand_data):

        cursor_pos = error_handler.safe_cursor_position(self.hand_tracker, hand_data, frame.shape)

        if cursor_pos is None:
            return None

        self.neural_stats['total_gestures'] += 1

        self._draw_neural_cursor(frame, cursor_pos, hand_data)

        is_pinching = error_handler.safe_pinch_detection(self.hand_tracker, hand_data)

        if is_pinching:
            self.pinch_confirmed_frames += 1

            self._draw_neural_pinch_indicator(frame, cursor_pos)

            self._handle_pinch_gesture(cursor_pos)
        else:
            self.pinch_confirmed_frames = 0

        self.was_pinching = is_pinching

        return cursor_pos

    def _draw_neural_cursor(self, frame, cursor_pos, hand_data):

        neural_status = self.hand_tracker.get_neural_status()

        if neural_status['neural_enhanced']:

            confidence = neural_status.get('confidence_boost', 1.0)
            base_size = 15  # Larger, more visible cursor
            enhanced_size = int(base_size * min(1.2, confidence))

            color = (255, 0, 255)

            cv2.circle(frame, cursor_pos, enhanced_size + 2, color, 2)
            cv2.circle(frame, cursor_pos, enhanced_size, color, -1)
            cv2.circle(frame, cursor_pos, max(1, enhanced_size - 3), (255, 255, 255), -1)

            # Removed text display
        else:

            cv2.circle(frame, cursor_pos, 15, (0, 255, 255), 2)  # Larger cursor
            cv2.circle(frame, cursor_pos, 12, (0, 255, 255), -1)
            cv2.circle(frame, cursor_pos, 8, (255, 255, 255), -1)

    def _draw_neural_pinch_indicator(self, frame, cursor_pos):

        if self.neural_enhanced:

            pulse_size = int(12 + 6 * np.sin(time.time() * 8))  # Larger pulse
            cv2.circle(frame, cursor_pos, pulse_size, (255, 0, 255), 2)

            # Removed text display
        else:

            cv2.circle(frame, cursor_pos, 18, (0, 255, 0), 2)  # Larger pinch indicator
            cv2.circle(frame, cursor_pos, 15, (0, 255, 0), -1)
            cv2.circle(frame, cursor_pos, 10, (255, 255, 255), -1)

    def _handle_pinch_gesture(self, cursor_pos):

        current_time = time.time()
        if not self.was_pinching and current_time - self.last_pinch_time > self.pinch_cooldown:

            if self.ai_enhanced:
                if self.keyboard.is_enter_button_clicked(cursor_pos):
                    print(f"✓ AI ENTER pressed!")
                    self.handle_key_press('ENTER')
                    self.last_pinch_time = current_time
                    return

                key = self.keyboard.get_key_at_position(cursor_pos)
                if key:
                    if key.startswith('SUGGESTION:'):
                        suggestion = key.replace('SUGGESTION:', '')
                        self._handle_suggestion_selection(suggestion)
                    else:
                        print(f"✓ AI Key '{key}' pressed!")
                        self.handle_key_press(key)
                    self.last_pinch_time = current_time
            else:

                if error_handler.safe_enter_check(self.keyboard, cursor_pos):
                    print(f"✓ ENTER pressed!")
                    self.handle_key_press('ENTER')
                    self.last_pinch_time = current_time
                else:
                    key = error_handler.safe_key_press(self.keyboard, cursor_pos)
                    if key:
                        print(f"✓ Key '{key}' pressed!")
                        self.handle_key_press(key)
                        self.last_pinch_time = current_time

    def _handle_suggestion_selection(self, suggestion):
        try:
            print(f"✓ AI Suggestion '{suggestion}' selected - replacing text")
            
            # Split text into words
            words = self.text.split()
            
            if words and not self.text.endswith(' '):
                # Replace the current incomplete word with the suggestion
                words[-1] = suggestion
                self.text = ' '.join(words)
            else:
                # Add new word if no incomplete word exists
                if self.text and not self.text.endswith(' '):
                    self.text += ' '
                self.text += suggestion

            print(f"✓ Text updated to: '{self.text}'")

            # Clear current word and suggestions
            self.keyboard.current_word = ""
            self.keyboard.suggestions = []
            self.keyboard.suggestion_buttons = []
            
            # Set cooldown to prevent immediate suggestion updates
            self.suggestion_just_selected = True
            self.suggestion_cooldown_time = time.time() + 0.5  # 500ms cooldown

            self.neural_stats['neural_enhancements'] += 1
            
            # Only process with AI if available
            if self.ai_intelligence:
                self.ai_intelligence.process_keystroke(suggestion)
            
        except Exception as e:
            print(f"❌ Error in suggestion selection: {e}")

    def _draw_fps(self, frame, start_time):

        fps = 1.0 / (time.time() - start_time) if time.time() > start_time else 0
        self.fps_counter.append(fps)
        if len(self.fps_counter) > 30:
            self.fps_counter.pop(0)
        avg_fps = sum(self.fps_counter) / len(self.fps_counter) if self.fps_counter else 0

        cv2.putText(frame, f"FPS: {int(avg_fps)}", (10, 30),
                   cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 255, 0), 2)

        neural_status = self.hand_tracker.get_neural_status()
        if neural_status['neural_enhanced']:
            cv2.putText(frame, "🧠 Nami Neural Engine", (10, frame.shape[0] - 20),
                       cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 0, 255), 1)

            if self.show_neural_overlay:
                self._draw_neural_overlay(frame)
        else:
            cv2.putText(frame, "VR Precision Keyboard", (10, frame.shape[0] - 20),
                       cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)

    def _draw_neural_overlay(self, frame):

        if not self.neural_enhanced:
            return

        h, w = frame.shape[:2]

        if self.neural_stats['total_gestures'] > 0:
            enhancement_rate = (self.neural_stats['neural_enhancements'] /
                              self.neural_stats['total_gestures']) * 100

            overlay_text = [
                f"Neural: {enhancement_rate:.1f}%",
                f"Gestures: {self.neural_stats['total_gestures']}",
                f"Enhanced: {self.neural_stats['neural_enhancements']}"
            ]

            for i, text in enumerate(overlay_text):
                cv2.putText(frame, text, (w - 200, 30 + i * 25),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 1)

    def handle_key_press(self, key):

        if self.ai_intelligence and not self.ai_session_active:
            self.ai_intelligence.start_typing_session()
            self.ai_session_active = True

        # Reset suggestion cooldown when user types manually
        self.suggestion_just_selected = False

        is_correction = False

        if key == 'SPACE':
            self.text += ' '
        elif key == 'BACKSPACE':
            if self.text:
                self.text = self.text[:-1]
                is_correction = True
        elif key == 'ENTER':
            if self.text:
                print(f"AI Neural Speaking: {self.text}")
                error_handler.safe_tts_speak(self.tts, self.text)
                error_handler.safe_logger_log(self.logger, self.text)

                if self.ai_intelligence and self.ai_session_active:
                    self.ai_intelligence.end_typing_session()
                    self.ai_session_active = False
            else:
                print("AI Neural Speaking: Empty")
                error_handler.safe_tts_speak(self.tts, "Empty")
        else:
            self.text += key.lower()

        if self.ai_intelligence:
            self.ai_intelligence.process_keystroke(key, is_correction)

        if self.neural_enhanced:
            self.neural_stats['neural_enhancements'] += 1

    def _print_neural_insights(self):

        if not self.neural_enhanced:
            print("Neural insights not available")
            return

        neural_status = self.hand_tracker.get_neural_status()

        print("\n" + "="*50)
        print("🧠 NEURAL INSIGHTS")
        print("="*50)
        print(f"Neural Enhanced: {neural_status['neural_enhanced']}")
        print(f"Neural Engine Active: {neural_status['neural_engine_active']}")
        print(f"Smoothing Factor: {neural_status['smoothing_factor']:.2f}")
        print(f"Confidence Boost: {neural_status['confidence_boost']:.2f}")
        print(f"Total Gestures: {self.neural_stats['total_gestures']}")
        print(f"Neural Enhancements: {self.neural_stats['neural_enhancements']}")

        if self.neural_stats['total_gestures'] > 0:
            enhancement_rate = (self.neural_stats['neural_enhancements'] /
                              self.neural_stats['total_gestures']) * 100
            print(f"Enhancement Rate: {enhancement_rate:.1f}%")

        print("="*50)

    def _print_ai_insights(self):

        if not self.ai_intelligence:
            print("AI insights not available")
            return

        try:
            insights = self.ai_intelligence.get_typing_insights()

            print("\n" + "="*60)
            print("🤖 AI INTELLIGENCE INSIGHTS")
            print("="*60)

            profile = insights.get('profile', {})
            print(f"Total Sessions: {profile.get('total_sessions', 0)}")
            print(f"Total Words Typed: {profile.get('total_words', 0)}")
            print(f"Total Characters: {profile.get('total_characters', 0)}")
            print(f"Average Speed: {profile.get('average_speed', 'N/A')}")
            print(f"Average Accuracy: {profile.get('average_accuracy', 'N/A')}")

            patterns = insights.get('patterns', {})
            print(f"\nVocabulary Size: {patterns.get('vocabulary_size', 0)} words")

            most_used = patterns.get('most_used_words', {})
            if most_used:
                print("Most Used Words:")
                for word, count in list(most_used.items())[:5]:
                    print(f"  {word}: {count} times")

            recent = insights.get('recent_performance', {})
            if 'sessions_analyzed' in recent:
                print(f"\nRecent Performance ({recent['sessions_analyzed']} sessions):")
                print(f"  Average Speed: {recent.get('average_speed', 'N/A')}")
                print(f"  Average Accuracy: {recent.get('average_accuracy', 'N/A')}")
                print(f"  Improvement Trend: {recent.get('improvement_trend', 'N/A')}")

            learning = insights.get('learning_stats', {})
            print(f"\nAI Learning Statistics:")
            print(f"  Vocabulary Growth: {learning.get('vocabulary_growth', 0)} words")
            print(f"  Pattern Recognition: {learning.get('pattern_recognition', 0)} patterns")
            print(f"  Suggestion Accuracy: {learning.get('suggestion_accuracy', 'N/A')}")

            print("="*60)

        except Exception as e:
            print(f"Error getting AI insights: {e}")

    def _print_final_stats(self):

        stats = error_handler.get_stats()

        print("\n" + "="*60)
        if self.neural_enhanced:
            print("🧠 NAMI NEURAL GESTURE KEYBOARD - SESSION COMPLETE")
        else:
            print("VR GESTURE KEYBOARD - SESSION COMPLETE")
        print("="*60)

        if stats['total_fixes'] > 0:
            print(f"Auto-fixed errors: {stats['total_fixes']}")

        if self.neural_enhanced:
            print(f"Total gestures processed: {self.neural_stats['total_gestures']}")
            print(f"Neural enhancements applied: {self.neural_stats['neural_enhancements']}")

            if self.neural_stats['total_gestures'] > 0:
                enhancement_rate = (self.neural_stats['neural_enhancements'] /
                                  self.neural_stats['total_gestures']) * 100
                print(f"Neural enhancement rate: {enhancement_rate:.1f}%")

        if self.ai_intelligence:

            self.ai_intelligence.save_ai_data()

            if self.ai_session_active:
                self.ai_intelligence.end_typing_session()

            profile = self.ai_intelligence.user_profile
            print(f"AI Sessions: {profile.total_sessions}")
            print(f"Words learned: {len(self.ai_intelligence.word_patterns)}")
            print(f"Final typing speed: {profile.average_speed:.1f} WPM")
            print(f"Final accuracy: {profile.average_accuracy:.1f}%")

        print("="*60)
        if self.ai_intelligence:
            print("Thank you for using Nami AI Neural Engine! 🤖🧠🚀")
        else:
            print("Thank you for using Nami Neural Engine! 🚀")
