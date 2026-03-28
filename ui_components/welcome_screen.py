

import cv2
import numpy as np
import random
import time

class WelcomeScreen:

    MESSAGES = [
        '"Your voice matters. Let\'s make it heard."',
        '"Every gesture is a step towards expression."',
        '"Communication has no boundaries."',
        '"Your thoughts deserve to be shared."',
        '"Technology empowers your voice."',
        '"Express yourself freely and confidently."',
        '"Your words can change the world."',
        '"Silence speaks, but you can speak louder."',
        '"Breaking barriers, one word at a time."',
        '"Your voice is unique and powerful."',
        '"Communication is a right, not a privilege."',
        '"Let your hands do the talking."',
        '"Every message you send matters."',
        '"You are heard. You are valued."',
        '"Empowering voices through innovation."',
        '"Your voice can reshape the world."',
        '"Expression gives life to ideas."',
        '"Communication carries the power of change."',
        '"Your message deserves to travel far."',
        '"Speak with conviction and belief."',
        '"Every idea begins with a single spark."',
        '"Your voice is stronger than silence."',
        '"Expression builds bridges between minds."',
        '"Communication opens new possibilities."',
        '"Your message can move mountains."',
        '"Speak with courage, not fear."',
        '"Every word holds meaning beyond sound."',
        '"Your voice carries strength and identity."',
        '"Expression transforms thoughts into action."',
        '"Communication fuels human connection."',
        '"Your message matters more than you know."',
        '"Speak from the heart and inspire others."',
        '"Every gesture tells a deeper story."',
        '"Your voice breaks barriers gently."',
        '"Expression lifts the world higher."',
        '"Communication lights the path to unity."',
        '"Your message plants seeds of hope."',
        '"Speak boldly and be heard."',
        '"Every thought deserves expression."',
        '"Your voice brings clarity and truth."',
        '"Expression makes silence meaningful."',
        '"Communication turns strangers into allies."',
        '"Your message changes perspectives."',
        '"Speak like your words can change lives."',
        '"Every voice creates ripples of progress."',
        '"Your voice carries purpose and passion."',
        '"Expression unlocks endless possibility."',
        '"Communication shapes imagination."',
        '"Your message builds the future."',
        '"Speak your truth without hesitation."',
        '"Every sound has the power to impact."',
        '"Your voice is a gift for the world."',
        '"Expression brings dreams into light."',
        '"Communication strengthens understanding."',
        '"Your message shines through darkness."',
        '"Speak bravely and transform moments."',
        '"Every gesture holds powerful meaning."',
        '"Your voice adds value everywhere."',
        '"Expression ignites creativity."',
        '"Communication expands horizons."',
        '"Your message reaches hearts unseen."',
        '"Speak with fearless intention."',
        '"Every idea deserves attention."',
        '"Your voice inspires action."',
        '"Expression creates space for growth."',
        '"Communication leads to peace."',
        '"Your message sparks transformation."',
        '"Speak hope into existence."',
        '"Every movement shows meaning."',
        '"Your voice shapes tomorrow."',
        '"Expression nurtures connection."',
        '"Communication lifts the spirit."',
        '"Your message holds magic."',
        '"Speak proudly and confidently."',
        '"Every thought can change the world."',
        '"Your voice deserves the spotlight."',
        '"Expression fuels innovation."',
        '"Communication builds possibility."',
        '"Your message is powerful."',
        '"Speak what matters most."',
        '"Every sound carries energy."',
        '"Your voice lights the flame of change."',
        '"Expression is freedom in motion."',
        '"Communication reveals truth."',
        '"Your message inspires bravery."',
        '"Speak with intention and love."',
        '"Every moment invites expression."',
        '"Your voice opens doors."',
        '"Expression empowers the soul."',
        '"Communication holds extraordinary power."',
        '"Your message belongs to the future."',
        '"Speak like your words matter."',
        '"Every idea is worth sharing."',
        '"Your voice awakens progress."',
        '"Expression elevates minds."',
        '"Communication builds communities."',
        '"Your message can heal."',
        '"Speak the language of courage."',
        '"Every whisper generates movement."',
        '"Your voice holds unstoppable strength."',
        '"Expression teaches understanding."',
        '"Communication brings worlds together."',
        '"Your message paves new paths."',
        '"Speak into the silence."',
        '"Every gesture is a step forward."',
        '"Your voice writes history."',
        '"Expression turns dreams into reality."',
        '"Communication fuels hope."',
        '"Your message nurtures possibility."',
        '"Speak through every challenge."',
        '"Every idea carries potential."',
        '"Your voice motivates change."',
        '"Expression makes hearts visible."',
        '"Communication builds trust."',
        '"Your message can lift others up."',
        '"Speak clearly and fearlessly."',
        '"Every movement carries purpose."',
        '"Your voice leaves a legacy."',
        '"Expression reveals inner strength."',
        '"Communication creates unity."',
        '"Your message brings light."',
        '"Speak with unstoppable passion."',
        '"Every sound holds promise."',
        '"Your voice directs energy toward progress."',
        '"Expression breathes life into emotion."',
        '"Communication erases distance."',
        '"Your message travels beyond boundaries."',
        '"Speak your dreams into reality."',
        '"Every gesture inspires connection."',
        '"Your voice ignites inspiration."',
        '"Expression shapes identity."',
        '"Communication empowers growth."',
        '"Your message breaks limitations."',
        '"Speak without doubt."',
        '"Every idea sparks evolution."',
        '"Your voice builds tomorrow."',
        '"Expression activates potential."',
        '"Communication restores balance."',
        '"Your message can start revolutions."',
        '"Speak hope into every space."',
        '"Every signal matters."',
        '"Your voice can heal silence."',
        '"Expression touches souls."',
        '"Communication awakens understanding."',
        '"Your message bridges differences."',
        '"Speak boldly, even in uncertainty."',
        '"Every movement shifts direction."',
        '"Your voice amplifies possibility."',
        '"Expression turns thought into power."',
        '"Communication carries meaning forever."',
        '"Your message radiates strength."',
        '"Speak from your deepest truth."',
        '"Every gesture shares emotion."',
        '"Your voice opens minds."',
        '"Expression shapes experience."',
        '"Communication brings clarity."',
        '"Your message builds courage."',
        '"Speak with fearless honesty."',
        '"Every idea fuels progress."',
        '"Your voice brightens the future."',
        '"Expression strengthens belonging."',
        '"Communication unlocks solutions."',
        '"Your message stands strong."',
        '"Speak with purpose."',
        '"Every movement sparks awareness."',
        '"Your voice transforms silence."',
        '"Expression celebrates individuality."',
        '"Communication encourages growth."',
        '"Your message breathes inspiration."',
        '"Speak like you believe in miracles."',
        '"Every signal changes direction."',
        '"Your voice encourages bravery."',
        '"Expression sets ideas free."',
        '"Communication nurtures hope."',
        '"Your message holds timeless value."',
        '"Speak into possibility."',
        '"Every thought lights the sky."',
        '"Your voice energizes transformation."',
        '"Expression elevates perspective."',
        '"Communication builds empathy."',
        '"Your message connects souls."',
        '"Speak above the noise."',
        '"Every gesture builds strength."',
        '"Your voice nourishes courage."',
        '"Expression carries emotion across distance."',
        '"Communication shapes destiny."',
        '"Your message brings unity."',
        '"Speak with fearless clarity."',
        '"Every moment invites connection."',
        '"Your voice awakens inner power."',
        '"Expression gives vision wings."',
        '"Communication guides hearts forward."',
        '"Your message transcends boundaries."',
        '"Speak like change begins now."',
        '"Every idea can touch the world."',
        '"Your voice pushes possibility further."',
        '"Expression builds bridges of hope."',
        '"Communication inspires progress."',
        '"Your message reaches beyond limits."',
        '"Speak until the world listens."',
        '"Every sign tells a story."',
        '"Your voice turns silence into movement."',
        '"Expression is strength disguised as calm."',
        '"Communication keeps dreams alive."',
        '"Your message breathes life into hope."',
        '"Speak light into darkness."',
        '"Every gesture reveals intention."',
        '"Your voice carries endless potential."',
        '"Expression restores confidence."',
        '"Communication empowers every person."',
        '"Your message lives forever."',
        '"Speak like your soul is singing."',
        '"Every whisper becomes momentum."',
        '"Your voice carries unstoppable energy."',
        '"Expression turns barriers into opportunities."',
        '"Communication brings transformation."',
        '"Your message reaches where words cannot."',
        '"Speak truth with unwavering strength."',
        '"Every idea strengthens the world."',
        '"Your voice shifts reality."',
        '"Expression illuminates possibility."',
        '"Communication lifts humanity higher."',
        '"Your message continues beyond time."',
        '"Speak as if tomorrow depends on it."',
        '"Every movement builds the future."'
    ]

    def __init__(self):
        self.message = random.choice(self.MESSAGES)
        self.width = 1280
        self.height = 720

    def show(self, duration=3):

        window_name = "Gesture Keyboard - VR Precision"
        start_time = time.time()

        while time.time() - start_time < duration:
            frame = self._create_welcome_frame()

            cv2.imshow(window_name, frame)

            try:
                if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
                    return False
            except:
                return False

            if cv2.waitKey(30) & 0xFF != 255:
                break

        self._fade_out()
        return True

    def _create_welcome_frame(self):

        frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)

        for i in range(self.height):
            intensity = int(20 + (i / self.height) * 30)
            frame[i, :] = [intensity, intensity, intensity]

        title = "Gesture Keyboard"
        subtitle = "VR-Level Precision Hand Tracking"

        font = cv2.FONT_HERSHEY_DUPLEX
        title_size = cv2.getTextSize(title, font, 2.5, 4)[0]
        title_x = (self.width - title_size[0]) // 2
        title_y = 150

        cv2.putText(frame, title, (title_x, title_y), font, 2.5, (0, 200, 255), 8)
        cv2.putText(frame, title, (title_x, title_y), font, 2.5, (0, 255, 255), 4)

        subtitle_size = cv2.getTextSize(subtitle, font, 0.9, 2)[0]
        subtitle_x = (self.width - subtitle_size[0]) // 2
        subtitle_y = title_y + 60
        cv2.putText(frame, subtitle, (subtitle_x, subtitle_y), font, 0.9, (200, 200, 200), 2)

        msg_y = 280
        msg_box_height = 180
        msg_box_margin = 100

        cv2.rectangle(frame,
                     (msg_box_margin, msg_y),
                     (self.width - msg_box_margin, msg_y + msg_box_height),
                     (0, 255, 255), 3)

        cv2.rectangle(frame,
                     (msg_box_margin + 5, msg_y + 5),
                     (self.width - msg_box_margin - 5, msg_y + msg_box_height - 5),
                     (0, 200, 200), 1)

        self._draw_wrapped_text(frame, self.message,
                               msg_box_margin + 40, msg_y + 70,
                               self.width - 2 * msg_box_margin - 80,
                               font, 1.0, (255, 255, 255), 2, 40)

        features_y = msg_y + msg_box_height + 60
        features = [
            "✓ Hand Gesture Control",
            "✓ Pinch to Type",
            "✓ Text-to-Speech",
            "✓ Real-time Tracking"
        ]

        col_width = self.width // 2
        for i, feature in enumerate(features):
            x = (col_width // 2 if i < 2 else col_width + col_width // 2) - 100
            y = features_y + (i % 2) * 40
            cv2.putText(frame, feature, (x, y), font, 0.7, (0, 255, 255), 2)

        instruction = "Press any key to start or wait..."
        inst_size = cv2.getTextSize(instruction, font, 0.7, 2)[0]
        inst_x = (self.width - inst_size[0]) // 2
        inst_y = self.height - 50

        if int(time.time() * 2) % 2 == 0:
            cv2.putText(frame, instruction, (inst_x, inst_y), font, 0.7, (255, 255, 255), 2)

        return frame

    def _draw_wrapped_text(self, frame, text, x, y, max_width, font, font_scale, color, thickness, line_spacing):

        words = text.split(' ')
        lines = []
        current_line = []

        for word in words:
            test_line = ' '.join(current_line + [word])
            test_size = cv2.getTextSize(test_line, font, font_scale, thickness)[0]

            if test_size[0] <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]

        if current_line:
            lines.append(' '.join(current_line))

        for i, line in enumerate(lines):
            line_size = cv2.getTextSize(line, font, font_scale, thickness)[0]
            line_x = x + (max_width - line_size[0]) // 2
            line_y = y + i * line_spacing
            cv2.putText(frame, line, (line_x, line_y), font, font_scale, color, thickness)

    def _fade_out(self):

        window_name = "Gesture Keyboard - VR Precision"
        for alpha in range(10, 0, -1):

            try:
                if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
                    return
            except:
                return

            frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
            frame[:] = (int(50 * alpha / 10), int(50 * alpha / 10), int(50 * alpha / 10))

            cv2.imshow(window_name, frame)
            cv2.waitKey(30)
