import cv2
import numpy as np

class VirtualKeyboard:
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
        self.start_x = 50

        keyboard_height = 4 * (self.key_size + self.key_gap) + 60 + 30
        self.start_y = (self.frame_height - keyboard_height) // 2 + 100
        self.button_list = []
        self._create_buttons()

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

                y = self.start_y + row_idx * (self.key_size + self.key_gap)

                self.button_list.append({
                    'key': key,
                    'x': current_x,
                    'y': y,
                    'width': width,
                    'height': self.key_size
                })

                current_x += width + self.key_gap

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

                cv2.rectangle(frame, (x-2, y-2), (x + w+2, y + h+2), (0, 255, 255), 3)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 3)
            else:

                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 2)

            font = cv2.FONT_HERSHEY_DUPLEX
            font_scale = 0.5 if len(button['key']) > 1 else 0.8
            text_size = cv2.getTextSize(button['key'], font, font_scale, 2)[0]
            text_x = x + (w - text_size[0]) // 2
            text_y = y + (h + text_size[1]) // 2

            text_color = (0, 255, 255) if is_hover else (255, 255, 255)

            cv2.putText(frame, button['key'], (text_x, text_y),
                       font, font_scale, (0, 0, 0), 4)

            cv2.putText(frame, button['key'], (text_x, text_y),
                       font, font_scale, text_color, 2)

    def get_key_at_position(self, pos):

        x, y = pos
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

    def draw_text_area(self, frame, text, cursor_pos=None):

        keyboard_top = self.start_y - 30
        text_area_height = 60
        text_area_y = keyboard_top - text_area_height

        enter_button_width = 100
        enter_button_margin = 10

        if self.button_list:
            min_x = min(btn['x'] for btn in self.button_list)
            max_x = max(btn['x'] + btn['width'] for btn in self.button_list)
            total_width = max_x - min_x
            text_area_x = min_x
        else:
            total_width = 700
            text_area_x = (self.frame_width - total_width) // 2

        text_area_width = total_width - enter_button_width - enter_button_margin

        enter_button_x = text_area_x + text_area_width + enter_button_margin
        enter_button_y = text_area_y

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

        cv2.rectangle(frame, (text_area_x, text_area_y),
                     (text_area_x + text_area_width, text_area_y + text_area_height),
                     (255, 255, 255), 2)

        if enter_hover:

            cv2.rectangle(frame, (enter_button_x-2, enter_button_y-2),
                         (enter_button_x + enter_button_width+2, enter_button_y + text_area_height+2),
                         (0, 255, 255), 3)
            cv2.rectangle(frame, (enter_button_x, enter_button_y),
                         (enter_button_x + enter_button_width, enter_button_y + text_area_height),
                         (0, 255, 255), 3)
        else:

            cv2.rectangle(frame, (enter_button_x, enter_button_y),
                         (enter_button_x + enter_button_width, enter_button_y + text_area_height),
                         (255, 255, 255), 2)

        font = cv2.FONT_HERSHEY_DUPLEX
        enter_text = "ENTER"
        text_size = cv2.getTextSize(enter_text, font, 0.6, 2)[0]
        enter_text_x = enter_button_x + (enter_button_width - text_size[0]) // 2
        enter_text_y = enter_button_y + (text_area_height + text_size[1]) // 2
        text_color = (0, 255, 255) if enter_hover else (255, 255, 255)
        cv2.putText(frame, enter_text, (enter_text_x, enter_text_y),
                   font, 0.6, text_color, 2)

        font = cv2.FONT_HERSHEY_DUPLEX
        text_y = text_area_y + (text_area_height // 2) + 10
        cv2.putText(frame, text, (text_area_x + 10, text_y), font, 0.9, (255, 255, 255), 2)

        import time
        if int(time.time() * 2) % 2 == 0:
            text_width = cv2.getTextSize(text, font, 1.0, 2)[0][0]
            cursor_x = text_area_x + 10 + text_width + 5
            cursor_top = text_area_y + 15
            cursor_bottom = text_area_y + text_area_height - 15
            cv2.line(frame, (cursor_x, cursor_top), (cursor_x, cursor_bottom), (0, 255, 255), 3)

    def is_send_button_clicked(self, cursor_pos):

        if not hasattr(self, 'send_button') or not cursor_pos:
            return False

        x, y = cursor_pos
        btn = self.send_button
        return (btn['x'] < x < btn['x'] + btn['width'] and
                btn['y'] < y < btn['y'] + btn['height'])
