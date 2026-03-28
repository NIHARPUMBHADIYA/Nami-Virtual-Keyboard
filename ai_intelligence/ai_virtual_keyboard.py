

import cv2
import numpy as np
import time
from typing import List, Optional, Tuple
from .nami_ai_intelligence import get_nami_ai

class AIVirtualKeyboard:

    def __init__(self):

        self.keys = [
            ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
            ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
            ['Z', 'X', 'C', 'V', 'B', 'N', 'M'],
            ['.', '?', '!', ',', 'SPACE', 'BACKSPACE']
        ]

        self.key_size = 60
        self.key_gap = 10
        self.frame_width = 1280
        self.frame_height = 720

        self.suggestion_area_height = 50
        self.suggestion_gap = 10
        self.max_suggestions = 5

        self._calculate_layout()
        self._create_buttons()

        self.ai = get_nami_ai()
        self.current_word = ""
        self.suggestions = []
        self.suggestion_buttons = []
        self.selected_suggestion = -1

        self.suggestion_animation_time = {}
        # AI glow effects removed

        print("AI Virtual Keyboard initialized")
        print(f"   AI Integration: {'ACTIVE' if self.ai else 'DISABLED'}")
        
        # If AI is not available yet, try to get it again later
        if not self.ai:
            print("   AI not initialized yet - will retry during operation")

    def _calculate_layout(self):

        keyboard_height = 4 * (self.key_size + self.key_gap)
        text_area_height = 60
        suggestion_area_height = self.suggestion_area_height + self.suggestion_gap
        total_height = keyboard_height + text_area_height + suggestion_area_height + 60

        start_y = (self.frame_height - total_height) // 2 + 50

        self.suggestion_area_y = start_y
        self.text_area_y = self.suggestion_area_y + self.suggestion_area_height + self.suggestion_gap
        self.keyboard_start_y = self.text_area_y + text_area_height + 20

    def _create_buttons(self):

        self.button_list = []

        max_row_width = 0
        for row in self.keys:
            row_width = 0
            for key in row:
                if key == 'SPACE':
                    row_width += 180 + self.key_gap
                elif key in ['BACKSPACE', 'ENTER']:
                    row_width += 120 + self.key_gap
                elif key in ['.', '?', '!', ',']:
                    row_width += 50 + self.key_gap
                else:
                    row_width += self.key_size + self.key_gap
            max_row_width = max(max_row_width, row_width)

        keyboard_start_x = (self.frame_width - max_row_width) // 2

        for row_idx, row in enumerate(self.keys):

            row_width = 0
            for key in row:
                if key == 'SPACE':
                    row_width += 180 + self.key_gap
                elif key in ['BACKSPACE', 'ENTER']:
                    row_width += 120 + self.key_gap
                elif key in ['.', '?', '!', ',']:
                    row_width += 50 + self.key_gap
                else:
                    row_width += self.key_size + self.key_gap

            row_start_x = keyboard_start_x + (max_row_width - row_width) // 2

            current_x = row_start_x
            for col_idx, key in enumerate(row):
                if key == 'SPACE':
                    width = 180
                elif key == 'BACKSPACE':
                    width = 120
                elif key in ['.', '?', '!', ',']:
                    width = 50
                else:
                    width = self.key_size

                y = self.keyboard_start_y + row_idx * (self.key_size + self.key_gap)

                self.button_list.append({
                    'key': key,
                    'x': current_x,
                    'y': y,
                    'width': width,
                    'height': self.key_size
                })

                current_x += width + self.key_gap

        self.keyboard_left = keyboard_start_x
        self.keyboard_width = max_row_width

    def update_current_word(self, text: str):

        words = text.split()
        if words and not text.endswith(' '):

            self.current_word = words[-1].lower()
        else:

            self.current_word = ""

        self._update_suggestions()

    def _update_suggestions(self):

        # Try to get AI if not available
        if not self.ai:
            self.ai = get_nami_ai()

        if not self.ai or not self.current_word:
            self.suggestions = []
            self.suggestion_buttons = []
            return

        self.suggestions = self.ai.get_word_suggestions(self.current_word, limit=self.max_suggestions)

        self._create_suggestion_buttons()

        current_time = time.time()
        for suggestion in self.suggestions:
            if suggestion not in self.suggestion_animation_time:
                self.suggestion_animation_time[suggestion] = current_time

    def _create_suggestion_buttons(self):

        self.suggestion_buttons = []

        if not self.suggestions:
            return

        total_width = self.keyboard_width
        button_width = (total_width - (len(self.suggestions) - 1) * self.suggestion_gap) // len(self.suggestions)
        button_height = self.suggestion_area_height - 10

        start_x = self.keyboard_left
        for i, suggestion in enumerate(self.suggestions):
            x = start_x + i * (button_width + self.suggestion_gap)
            y = self.suggestion_area_y + 5

            self.suggestion_buttons.append({
                'text': suggestion,
                'x': x,
                'y': y,
                'width': button_width,
                'height': button_height,
                'index': i
            })

    def draw_ai_suggestions(self, frame, cursor_pos=None):

        if not self.suggestions:

            self._draw_empty_suggestion_area(frame)
            return

        # AI glow effects removed

        for i, button in enumerate(self.suggestion_buttons):
            self._draw_suggestion_button(frame, button, cursor_pos, i)

        # AI indicator removed

    def _draw_empty_suggestion_area(self, frame):

        cv2.rectangle(frame,
                     (self.keyboard_left, self.suggestion_area_y),
                     (self.keyboard_left + self.keyboard_width, self.suggestion_area_y + self.suggestion_area_height),
                     (30, 30, 30), -1)

        cv2.rectangle(frame,
                     (self.keyboard_left, self.suggestion_area_y),
                     (self.keyboard_left + self.keyboard_width, self.suggestion_area_y + self.suggestion_area_height),
                     (100, 100, 100), 2)

        status_text = "Start typing for suggestions"
        color = (200, 200, 200)

        font = cv2.FONT_HERSHEY_SIMPLEX
        text_size = cv2.getTextSize(status_text, font, 0.6, 2)[0]
        text_x = self.keyboard_left + (self.keyboard_width - text_size[0]) // 2
        text_y = self.suggestion_area_y + (self.suggestion_area_height + text_size[1]) // 2

        cv2.putText(frame, status_text, (text_x, text_y), font, 0.6, color, 2)

    def _draw_suggestion_button(self, frame, button, cursor_pos, index):

        x, y, w, h = button['x'], button['y'], button['width'], button['height']
        suggestion = button['text']

        is_hover = False
        if cursor_pos:
            cx, cy = cursor_pos
            if x < cx < x + w and y < cy < y + h:
                is_hover = True
                self.selected_suggestion = index

        current_time = time.time()
        animation_age = current_time - self.suggestion_animation_time.get(suggestion, current_time)
        animation_factor = min(1.0, animation_age / 0.5)

        if is_hover:

            bg_color = (50, 150, 255)
            border_color = (100, 200, 255)
            text_color = (255, 255, 255)
            border_thickness = 3
        else:
            # Clean suggestion button styling
            bg_color = (40, 40, 80)
            border_color = (120, 120, 200)
            text_color = (200, 200, 255)
            border_thickness = 2

        scale = 0.8 + 0.2 * animation_factor
        scaled_w = int(w * scale)
        scaled_h = int(h * scale)
        scaled_x = x + (w - scaled_w) // 2
        scaled_y = y + (h - scaled_h) // 2

        cv2.rectangle(frame, (scaled_x, scaled_y), (scaled_x + scaled_w, scaled_y + scaled_h), bg_color, -1)

        cv2.rectangle(frame, (scaled_x, scaled_y), (scaled_x + scaled_w, scaled_y + scaled_h), border_color, border_thickness)

        font = cv2.FONT_HERSHEY_DUPLEX
        font_scale = 0.7
        text_size = cv2.getTextSize(suggestion, font, font_scale, 2)[0]
        text_x = scaled_x + (scaled_w - text_size[0]) // 2
        text_y = scaled_y + (scaled_h + text_size[1]) // 2

        cv2.putText(frame, suggestion, (text_x, text_y), font, font_scale, (0, 0, 0), 4)
        cv2.putText(frame, suggestion, (text_x, text_y), font, font_scale, text_color, 2)

        confidence = min(1.0, len(suggestion) / 10.0)
        confidence_width = int(scaled_w * confidence * 0.8)
        confidence_x = scaled_x + (scaled_w - confidence_width) // 2
        confidence_y = scaled_y + scaled_h - 3

        confidence_color = (0, int(255 * confidence), int(255 * (1 - confidence)))
        cv2.rectangle(frame, (confidence_x, confidence_y), (confidence_x + confidence_width, confidence_y + 2), confidence_color, -1)

    # AI indicator removed - cleaner interface

    def draw_keyboard(self, frame, cursor_pos=None):

        for button in self.button_list:
            x, y = button['x'], button['y']
            w, h = button['width'], button['height']

            is_hover = False
            if cursor_pos:
                cx, cy = cursor_pos
                if x < cx < x + w and y < cy < y + h:
                    is_hover = True

            if is_hover:

                border_color = (255, 100, 255)
                glow_color = (255, 150, 255)
                cv2.rectangle(frame, (x-2, y-2), (x + w+2, y + h+2), glow_color, 3)
                cv2.rectangle(frame, (x, y), (x + w, y + h), border_color, 3)
            else:

                border_color = (255, 255, 255)
                cv2.rectangle(frame, (x, y), (x + w, y + h), border_color, 2)

            font = cv2.FONT_HERSHEY_DUPLEX
            font_scale = 0.5 if len(button['key']) > 1 else 0.8
            text_size = cv2.getTextSize(button['key'], font, font_scale, 2)[0]
            text_x = x + (w - text_size[0]) // 2
            text_y = y + (h + text_size[1]) // 2

            if is_hover:
                text_color = (255, 100, 255)
            else:
                text_color = (255, 255, 255)

            cv2.putText(frame, button['key'], (text_x, text_y), font, font_scale, (0, 0, 0), 4)
            cv2.putText(frame, button['key'], (text_x, text_y), font, font_scale, text_color, 2)

    def draw_text_area(self, frame, text, cursor_pos=None):

        text_area_height = 60
        enter_button_width = 100
        enter_button_margin = 10

        text_area_x = self.keyboard_left
        text_area_width = self.keyboard_width - enter_button_width - enter_button_margin

        enter_button_x = text_area_x + text_area_width + enter_button_margin
        enter_button_y = self.text_area_y

        enter_hover = False
        if cursor_pos:
            cx, cy = cursor_pos
            if (enter_button_x < cx < enter_button_x + enter_button_width and
                enter_button_y < cy < enter_button_y + text_area_height):
                enter_hover = True

        self.enter_button = {
            'x': enter_button_x,
            'y': enter_button_y,
            'width': enter_button_width,
            'height': text_area_height
        }

        bg_color = (20, 20, 20)
        border_color = (255, 255, 255)

        cv2.rectangle(frame, (text_area_x, self.text_area_y),
                     (text_area_x + text_area_width, self.text_area_y + text_area_height),
                     bg_color, -1)
        cv2.rectangle(frame, (text_area_x, self.text_area_y),
                     (text_area_x + text_area_width, self.text_area_y + text_area_height),
                     border_color, 2)

        if enter_hover:
            cv2.rectangle(frame, (enter_button_x-2, enter_button_y-2),
                         (enter_button_x + enter_button_width+2, enter_button_y + text_area_height+2),
                         (255, 100, 255), 3)
            cv2.rectangle(frame, (enter_button_x, enter_button_y),
                         (enter_button_x + enter_button_width, enter_button_y + text_area_height),
                         (255, 100, 255), 3)
            enter_text_color = (255, 100, 255)
        else:
            cv2.rectangle(frame, (enter_button_x, enter_button_y),
                         (enter_button_x + enter_button_width, enter_button_y + text_area_height),
                         border_color, 2)
            enter_text_color = border_color

        font = cv2.FONT_HERSHEY_DUPLEX
        enter_text = "ENTER"
        text_size = cv2.getTextSize(enter_text, font, 0.6, 2)[0]
        enter_text_x = enter_button_x + (enter_button_width - text_size[0]) // 2
        enter_text_y = enter_button_y + (text_area_height + text_size[1]) // 2
        cv2.putText(frame, enter_text, (enter_text_x, enter_text_y), font, 0.6, enter_text_color, 2)

        font = cv2.FONT_HERSHEY_DUPLEX
        text_y = self.text_area_y + (text_area_height // 2) + 10
        text_color = (255, 255, 255)
        cv2.putText(frame, text, (text_area_x + 10, text_y), font, 0.9, text_color, 2)

        if int(time.time() * 2) % 2 == 0:
            text_width = cv2.getTextSize(text, font, 0.9, 2)[0][0]
            cursor_x = text_area_x + 10 + text_width + 5
            cursor_top = self.text_area_y + 15
            cursor_bottom = self.text_area_y + text_area_height - 15

            cursor_color = (0, 255, 255) if not self.ai else (255, 100, 255)
            cv2.line(frame, (cursor_x, cursor_top), (cursor_x, cursor_bottom), cursor_color, 3)

        if self.ai:
            self._draw_typing_stats(frame, text_area_x, text_area_width)

    def _draw_typing_stats(self, frame, text_area_x, text_area_width):

        if not self.ai:
            return

        try:
            insights = self.ai.get_typing_insights()
            profile = insights.get('profile', {})

            stats_text = f"WPM: {profile.get('average_speed', 'N/A')} | Acc: {profile.get('average_accuracy', 'N/A')}"

            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.4
            text_size = cv2.getTextSize(stats_text, font, font_scale, 1)[0]

            stats_x = text_area_x + text_area_width - text_size[0] - 10
            stats_y = self.text_area_y + 55

            cv2.rectangle(frame, (stats_x - 5, stats_y - 12), (stats_x + text_size[0] + 5, stats_y + 5), (0, 0, 0), -1)

            cv2.putText(frame, stats_text, (stats_x, stats_y), font, font_scale, (100, 255, 100), 1)

        except Exception as e:
            pass

    def get_key_at_position(self, pos):

        x, y = pos

        for button in self.suggestion_buttons:
            bx, by = button['x'], button['y']
            bw, bh = button['width'], button['height']
            if bx < x < bx + bw and by < y < by + bh:
                return f"SUGGESTION:{button['text']}"

        for button in self.button_list:
            bx, by = button['x'], button['y']
            bw, bh = button['width'], button['height']
            if bx < x < bx + bw and by < y < by + bh:
                return button['key']

        return None

    def is_enter_button_clicked(self, cursor_pos):

        if not hasattr(self, 'enter_button') or not cursor_pos:
            return False

        x, y = cursor_pos
        btn = self.enter_button
        return (btn['x'] < x < btn['x'] + btn['width'] and
                btn['y'] < y < btn['y'] + btn['height'])

    def get_ai_status(self):

        return {
            'ai_active': self.ai is not None,
            'current_word': self.current_word,
            'suggestions_count': len(self.suggestions),
            'suggestions': self.suggestions
        }