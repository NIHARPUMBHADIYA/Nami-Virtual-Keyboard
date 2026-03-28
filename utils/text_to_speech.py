import pyttsx3
import threading
from .hinglish_dictionary import convert_to_hinglish_phonetic, is_hinglish_text
from .name_dictionary import convert_names_in_text, is_name

class TextToSpeech:

    def __init__(self):

        self.rate = 165
        self.volume = 1.0
        self.voice_id = None

        temp_engine = pyttsx3.init()
        voices = temp_engine.getProperty('voices')
        if len(voices) > 0:
            self.voice_id = voices[0].id
        temp_engine.stop()
        del temp_engine

    def speak(self, text):
        """Speak text instantly"""
        def _speak():
            engine = None
            try:
                engine = pyttsx3.init()
                
                if self.voice_id:
                    engine.setProperty('voice', self.voice_id)
                engine.setProperty('rate', self.rate)
                engine.setProperty('volume', self.volume)

                engine.say(text)
                engine.runAndWait()
                
            except Exception as e:
                print(f"TTS Error: {e}")
            finally:
                if engine:
                    try:
                        engine.stop()
                        del engine
                    except:
                        pass

        thread = threading.Thread(target=_speak)
        thread.daemon = False
        thread.start()
    
    def speak_sync(self, text):
        """Synchronous speak method as backup"""
        engine = None
        try:
            engine = pyttsx3.init()
            
            if self.voice_id:
                engine.setProperty('voice', self.voice_id)
            engine.setProperty('rate', self.rate)
            engine.setProperty('volume', self.volume)

            engine.say(text)
            engine.runAndWait()
            
        except Exception as e:
            print(f"TTS Error: {e}")
        finally:
            if engine:
                try:
                    engine.stop()
                    del engine
                except:
                    pass

    def speak_based_on_input(self, text):

        text = text.strip()

        if len(text) == 0:
            self.speak("Empty")
            return

        text = convert_names_in_text(text)

        is_hinglish = is_hinglish_text(text)

        if is_hinglish:
            text = convert_to_hinglish_phonetic(text)
            print(f"[Hinglish detected] Phonetic: {text}")

        has_question = '?' in text
        has_exclamation = '!' in text
        has_period = '.' in text

        if len(text) == 1:

            if text in ['.', '?', '!', ',']:
                punctuation_names = {
                    '.': 'Period',
                    '?': 'Question mark',
                    '!': 'Exclamation mark',
                    ',': 'Comma'
                }
                self.speak(punctuation_names.get(text, text))
            else:
                self.speak(f"Alphabet: {text}")
        elif ' ' not in text and not any(p in text for p in ['.', '?', '!', ',']):

            if is_hinglish:

                self._speak_with_emotion(text, False, False)
            else:
                self.speak(f"Word: {text}")
        else:

            self._speak_with_emotion(text, has_question, has_exclamation)

    def _speak_with_emotion(self, input_text, has_question, has_exclamation):

        def _speak_emotional():
            try:

                text = input_text

                engine = pyttsx3.init()

                voices = engine.getProperty('voices')

                if has_exclamation:

                    if len(voices) > 1:

                        engine.setProperty('voice', voices[1].id)
                    engine.setProperty('rate', 200)
                    engine.setProperty('volume', 1.0)

                    text = self._add_emphasis(text)

                elif has_question:

                    if len(voices) > 1:

                        engine.setProperty('voice', voices[1].id)
                    engine.setProperty('rate', 185)
                    engine.setProperty('volume', 0.95)

                    text = self._add_question_emphasis(text)

                else:

                    if self.voice_id:
                        engine.setProperty('voice', self.voice_id)
                    engine.setProperty('rate', 165)
                    engine.setProperty('volume', self.volume)

                processed_text = self._add_pauses(text)

                engine.say(processed_text)
                engine.runAndWait()

                engine.stop()
                del engine
            except Exception as e:
                print(f"TTS Error: {e}")

        import threading
        thread = threading.Thread(target=_speak_emotional)
        thread.daemon = True
        thread.start()

    def _add_emphasis(self, text):

        words = text.split()
        if len(words) > 0:

            if words[-1].endswith('!'):
                words[-1] = words[-1][:-1].upper() + '!'
            else:
                words[-1] = words[-1].upper()
        return ' '.join(words)

    def _add_question_emphasis(self, text):

        text = text.replace('?', ' ?')
        return text

    def _add_pauses(self, text):

        text = text.replace('. ', '.   ')

        text = text.replace('? ', '?   ')

        text = text.replace('! ', '!   ')

        text = text.replace(', ', ',  ')

        return text
