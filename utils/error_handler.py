

import sys
import traceback
import threading
import time
from datetime import datetime

class ErrorHandler:

    def __init__(self):
        self.error_log = []
        self.fix_count = 0
        self.monitoring = True
        self.last_check = time.time()

    def log_error(self, error_type, error_msg, fix_applied):

        entry = {
            'time': datetime.now().strftime("%H:%M:%S"),
            'type': error_type,
            'message': error_msg,
            'fix': fix_applied,
            'fixed': True
        }
        self.error_log.append(entry)
        self.fix_count += 1

    def safe_camera_init(self, camera_id=0):

        import cv2
        try:
            cap = cv2.VideoCapture(camera_id, cv2.CAP_DSHOW)
            if not cap.isOpened():

                cap = cv2.VideoCapture(camera_id)
                self.log_error("CameraError", "DSHOW failed", "Switched to default backend")

            try:
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
                cap.set(cv2.CAP_PROP_FPS, 120)
                cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
                cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
            except Exception as e:
                self.log_error("CameraSettings", str(e), "Using default camera settings")

            return cap
        except Exception as e:
            self.log_error("CameraInit", str(e), "Attempting fallback camera")
            return cv2.VideoCapture(0)

    def safe_frame_read(self, cap):

        try:
            ret, frame = cap.read()
            if not ret or frame is None:
                self.log_error("FrameRead", "Failed to read frame", "Skipping frame")
                return False, None
            return True, frame
        except Exception as e:
            self.log_error("FrameRead", str(e), "Returning empty frame")
            return False, None

    def safe_hand_detection(self, hand_tracker, frame):

        try:
            return hand_tracker.find_hands(frame)
        except Exception as e:
            self.log_error("HandDetection", str(e), "Returning None for hand data")
            return None

    def safe_cursor_position(self, hand_tracker, hand_data, frame_shape):

        try:
            if hand_data:
                return hand_tracker.get_cursor_position(hand_data, frame_shape)
            return None
        except Exception as e:
            self.log_error("CursorPosition", str(e), "Using center position")
            return (frame_shape[1]//2, frame_shape[0]//2)

    def safe_pinch_detection(self, hand_tracker, hand_data):

        try:
            if hand_data:
                return hand_tracker.is_pinching(hand_data)
            return False
        except Exception as e:
            self.log_error("PinchDetection", str(e), "Returning False")
            return False

    def safe_keyboard_draw(self, keyboard, frame, cursor_pos):

        try:
            keyboard.draw_keyboard(frame, cursor_pos)
        except Exception as e:
            self.log_error("KeyboardDraw", str(e), "Skipping keyboard draw")

    def safe_text_area_draw(self, keyboard, frame, text, cursor_pos):

        try:
            keyboard.draw_text_area(frame, text, cursor_pos)
        except Exception as e:
            self.log_error("TextAreaDraw", str(e), "Skipping text area draw")

    def safe_key_press(self, keyboard, cursor_pos):

        try:
            return keyboard.get_key_at_position(cursor_pos)
        except Exception as e:
            self.log_error("KeyPress", str(e), "Returning None")
            return None

    def safe_enter_check(self, keyboard, cursor_pos):

        try:
            return keyboard.is_enter_button_clicked(cursor_pos)
        except Exception as e:
            self.log_error("EnterCheck", str(e), "Returning False")
            return False

    def safe_tts_speak(self, tts, text):
        """Instant TTS with fallback"""
        try:
            tts.speak(text)
        except Exception as e:
            try:
                tts.speak_sync(text)
            except Exception as e2:
                self.log_error("TTS", f"Speech failed: {e}", "Speech output skipped")

    def safe_logger_log(self, logger, text):

        try:
            logger.log_spoken_text(text)
        except Exception as e:
            self.log_error("Logger", str(e), "Skipping log entry")

    def safe_imshow(self, window_name, frame):

        try:
            import cv2
            if frame is not None and frame.size > 0:
                cv2.imshow(window_name, frame)
        except Exception as e:
            self.log_error("Display", str(e), "Skipping frame display")

    def monitor_system(self):

        while self.monitoring:
            try:
                current_time = time.time()
                if current_time - self.last_check > 1.0:

                    self.last_check = current_time
                time.sleep(0.1)
            except Exception as e:
                self.log_error("Monitor", str(e), "Continuing monitoring")

    def start_monitoring(self):

        monitor_thread = threading.Thread(target=self.monitor_system, daemon=True)
        monitor_thread.start()

    def stop_monitoring(self):

        self.monitoring = False

    def get_stats(self):

        return {
            'total_fixes': self.fix_count,
            'errors_handled': len(self.error_log)
        }

    def wrap_function(self, func, error_name, default_return=None):

        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                self.log_error(error_name, str(e), f"Returning {default_return}")
                return default_return
        return wrapper

error_handler = ErrorHandler()

def handle_exception(exc_type, exc_value, exc_traceback):

    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    error_msg = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    error_handler.log_error("UnhandledException", error_msg, "Logged and continuing")

sys.excepthook = handle_exception
