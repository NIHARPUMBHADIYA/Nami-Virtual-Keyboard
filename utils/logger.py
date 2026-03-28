

from datetime import datetime
import os
from .cache_manager import get_cache_path, ensure_cache_dir

class SessionLogger:

    def __init__(self, log_file="gesture_keyboard_log.txt"):
        ensure_cache_dir()
        self.log_file = get_cache_path(log_file)
        self.init_log_file()

    def init_log_file(self):

        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write("\n" + "="*60 + "\n")
                f.write(f"Session started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("="*60 + "\n\n")
            print(f"✓ Logging to: {self.log_file}")
        except Exception as e:
            print(f"Warning: Could not create log file: {e}")

    def log_spoken_text(self, text):

        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                f.write(f"[{timestamp}] {text}\n")
        except Exception as e:
            print(f"Warning: Could not write to log: {e}")
