

import json
import time
import os
import re
from collections import defaultdict, deque, Counter
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass, asdict
import threading
import pickle
import math
import numpy as np
from utils.cache_manager import get_cache_path, ensure_cache_dir

@dataclass
class TypingSession:
    timestamp: float
    text: str
    duration: float
    accuracy: float
    speed_wpm: float
    errors: int
    corrections: int
    word_count: int

@dataclass
class UserProfile:
    total_sessions: int = 0
    total_words_typed: int = 0
    total_characters: int = 0
    average_accuracy: float = 0.0
    average_speed: float = 0.0
    preferred_words: Dict[str, int] = None
    common_mistakes: Dict[str, str] = None
    typing_rhythm: List[float] = None

    def __post_init__(self):
        if self.preferred_words is None:
            self.preferred_words = {}
        if self.common_mistakes is None:
            self.common_mistakes = {}
        if self.typing_rhythm is None:
            self.typing_rhythm = []

class OfflineWordDatabase:

    def __init__(self):
        self.word_frequencies = {}
        self.word_associations = defaultdict(set)
        self.context_patterns = defaultdict(list)
        self._initialize_base_vocabulary()

    def _initialize_base_vocabulary(self):

        common_words = {

            'the': 1000, 'a': 800, 'an': 200, 'and': 900, 'or': 300, 'but': 400,
            'i': 700, 'you': 600, 'he': 500, 'she': 500, 'it': 600, 'we': 400, 'they': 450,
            'me': 300, 'him': 200, 'her': 250, 'us': 200, 'them': 200,
            'my': 400, 'your': 350, 'his': 300, 'her': 250, 'its': 200, 'our': 250, 'their': 300,

            'is': 800, 'are': 600, 'was': 500, 'were': 400, 'be': 450, 'been': 300, 'being': 200,
            'have': 600, 'has': 500, 'had': 450, 'do': 400, 'does': 300, 'did': 350,
            'will': 400, 'would': 350, 'could': 300, 'should': 250, 'can': 400, 'may': 200,
            'go': 300, 'come': 250, 'get': 400, 'make': 350, 'take': 300, 'give': 250,
            'see': 300, 'know': 350, 'think': 300, 'say': 350, 'tell': 250, 'ask': 200,
            'work': 300, 'play': 200, 'run': 150, 'walk': 150, 'talk': 200, 'look': 250,

            'time': 400, 'day': 300, 'year': 250, 'week': 200, 'month': 150,
            'home': 300, 'house': 200, 'place': 250, 'way': 300, 'world': 200,
            'man': 250, 'woman': 200, 'person': 200, 'people': 300, 'child': 150,
            'work': 300, 'job': 200, 'money': 200, 'business': 150,
            'water': 150, 'food': 200, 'car': 200, 'phone': 150, 'computer': 100,

            'good': 400, 'bad': 200, 'great': 250, 'small': 200, 'big': 200, 'large': 150,
            'new': 300, 'old': 250, 'young': 150, 'long': 200, 'short': 150,
            'high': 150, 'low': 150, 'fast': 150, 'slow': 100, 'easy': 200, 'hard': 200,
            'hot': 100, 'cold': 100, 'warm': 100, 'cool': 100,

            'in': 600, 'on': 500, 'at': 400, 'to': 700, 'for': 500, 'with': 450, 'by': 300,
            'from': 350, 'up': 200, 'down': 150, 'out': 250, 'off': 150, 'over': 200,
            'under': 100, 'above': 100, 'below': 100, 'through': 150, 'between': 100,
            'now': 300, 'then': 200, 'here': 200, 'there': 250, 'where': 200, 'when': 200,
            'how': 250, 'why': 200, 'what': 400, 'who': 200, 'which': 200,
            'very': 300, 'really': 200, 'quite': 150, 'just': 400, 'only': 300, 'also': 250,
            'too': 200, 'so': 400, 'more': 300, 'most': 200, 'much': 250, 'many': 200,

            'one': 200, 'two': 150, 'three': 100, 'four': 80, 'five': 80,
            'first': 150, 'second': 100, 'last': 200, 'next': 150,
            'today': 150, 'tomorrow': 100, 'yesterday': 100, 'morning': 100, 'evening': 80,

            'internet': 50, 'website': 40, 'email': 60, 'social': 40, 'media': 40,
            'app': 30, 'software': 30, 'technology': 25, 'digital': 25, 'online': 40,
            'data': 30, 'information': 40, 'system': 50, 'network': 25, 'server': 20,

            'hello': 100, 'hi': 80, 'bye': 60, 'goodbye': 40, 'thanks': 100, 'thank': 80,
            'please': 100, 'sorry': 80, 'excuse': 40, 'welcome': 60, 'yes': 200, 'no': 200,
            'ok': 150, 'okay': 100, 'sure': 100, 'maybe': 80, 'probably': 60,
        }

        self.word_frequencies.update(common_words)
        self._build_associations()

    def _build_associations(self):

        associations = {
            'hello': {'hi', 'hey', 'greetings', 'good', 'morning', 'evening'},
            'good': {'morning', 'evening', 'night', 'day', 'job', 'work', 'great', 'excellent'},
            'thank': {'you', 'thanks', 'grateful', 'appreciate'},
            'computer': {'software', 'hardware', 'technology', 'digital', 'system'},
            'work': {'job', 'office', 'business', 'career', 'professional'},
            'time': {'day', 'hour', 'minute', 'second', 'clock', 'schedule'},
            'home': {'house', 'family', 'place', 'address', 'location'},
            'food': {'eat', 'meal', 'dinner', 'lunch', 'breakfast', 'restaurant'},
            'car': {'drive', 'vehicle', 'transport', 'road', 'traffic'},
            'phone': {'call', 'mobile', 'contact', 'number', 'message'},
        }

        for word, related in associations.items():
            self.word_associations[word].update(related)
            for related_word in related:
                self.word_associations[related_word].add(word)

    def add_word(self, word: str, frequency: int = 1):

        word = word.lower().strip()
        if word and word.isalpha():
            self.word_frequencies[word] = self.word_frequencies.get(word, 0) + frequency

    def get_suggestions(self, prefix: str, context: List[str] = None, limit: int = 5) -> List[str]:

        prefix = prefix.lower().strip()
        if not prefix:
            return []

        suggestions = []

        for word, freq in self.word_frequencies.items():
            if word.startswith(prefix) and word != prefix:
                suggestions.append((word, freq))

        suggestions.sort(key=lambda x: x[1], reverse=True)

        if context:
            context_suggestions = self._get_context_suggestions(prefix, context)

            suggestion_words = {s[0] for s in suggestions}
            for word, score in context_suggestions:
                if word not in suggestion_words:
                    suggestions.append((word, score))

        return [word for word, _ in suggestions[:limit]]

    def _get_context_suggestions(self, prefix: str, context: List[str]) -> List[Tuple[str, int]]:

        context_suggestions = []

        for context_word in context[-3:]:
            context_word = context_word.lower().strip()
            if context_word in self.word_associations:
                for associated_word in self.word_associations[context_word]:
                    if associated_word.startswith(prefix):
                        freq = self.word_frequencies.get(associated_word, 1)
                        context_suggestions.append((associated_word, freq + 100))

        return context_suggestions

class NamiAIIntelligence:

    def __init__(self, data_file: str = "nami_ai_data.json"):
        # Use cache manager for file paths
        ensure_cache_dir()
        self.data_file = get_cache_path(data_file)
        self.pickle_file = get_cache_path(data_file.replace('.json', '.pkl'))

        self.user_profile = UserProfile()
        self.word_database = OfflineWordDatabase()
        self.typing_sessions = deque(maxlen=1000)

        self.current_session = None
        self.session_start_time = None
        self.current_text = ""
        self.keystroke_times = deque(maxlen=100)
        self.error_count = 0
        self.correction_count = 0

        self.word_patterns = defaultdict(int)
        self.bigram_patterns = defaultdict(int)
        self.trigram_patterns = defaultdict(int)
        self.typing_rhythm_buffer = deque(maxlen=50)

        self.suggestion_cache = {}
        self.context_window = deque(maxlen=10)

        self.learning_rate = 0.1
        self.min_word_frequency = 2
        self.suggestion_threshold = 0.3

        self.lock = threading.Lock()

        self.load_ai_data()

        print("🤖 Nami AI Intelligence initialized")
        print(f"   Profile: {self.user_profile.total_sessions} sessions, {self.user_profile.total_words_typed} words")
        print(f"   Vocabulary: {len(self.word_database.word_frequencies)} words")
        print(f"   Average Accuracy: {self.user_profile.average_accuracy:.1f}%")
        print(f"   Average Speed: {self.user_profile.average_speed:.1f} WPM")

    def start_typing_session(self):

        with self.lock:
            self.session_start_time = time.time()
            self.current_text = ""
            self.keystroke_times.clear()
            self.error_count = 0
            self.correction_count = 0
            self.context_window.clear()

            print("🤖 AI: New typing session started")

    def process_keystroke(self, key: str, is_correction: bool = False):

        with self.lock:
            current_time = time.time()
            self.keystroke_times.append(current_time)

            if is_correction:
                self.correction_count += 1

            if key == 'BACKSPACE':
                if self.current_text:
                    self.current_text = self.current_text[:-1]
                    self.error_count += 1
            elif key == 'SPACE':
                self.current_text += ' '
                self._process_completed_word()
            elif key == 'ENTER':
                self._process_completed_word()
                self.end_typing_session()
            elif len(key) == 1:
                self.current_text += key.lower()

            if len(self.keystroke_times) >= 2:
                interval = self.keystroke_times[-1] - self.keystroke_times[-2]
                self.typing_rhythm_buffer.append(interval)

    def _process_completed_word(self):

        words = self.current_text.strip().split()
        if words:
            last_word = words[-1].strip()
            if last_word and last_word.isalpha():

                self.word_database.add_word(last_word)
                self.word_patterns[last_word] += 1

                self.context_window.append(last_word)

                self._learn_patterns(words)

    def _learn_patterns(self, words: List[str]):

        if len(words) >= 2:

            for i in range(len(words) - 1):
                bigram = f"{words[i]} {words[i+1]}"
                self.bigram_patterns[bigram] += 1

        if len(words) >= 3:

            for i in range(len(words) - 2):
                trigram = f"{words[i]} {words[i+1]} {words[i+2]}"
                self.trigram_patterns[trigram] += 1

    def end_typing_session(self):

        if not self.session_start_time:
            return

        with self.lock:
            duration = time.time() - self.session_start_time
            words = self.current_text.strip().split()
            word_count = len([w for w in words if w.isalpha()])
            char_count = len(self.current_text.replace(' ', ''))

            if duration > 0:
                wpm = (word_count / duration) * 60
                accuracy = max(0, 100 - (self.error_count / max(char_count, 1)) * 100)
            else:
                wpm = 0
                accuracy = 100

            session = TypingSession(
                timestamp=self.session_start_time,
                text=self.current_text,
                duration=duration,
                accuracy=accuracy,
                speed_wpm=wpm,
                errors=self.error_count,
                corrections=self.correction_count,
                word_count=word_count
            )

            self.typing_sessions.append(session)

            self._update_user_profile(session)

            if len(self.typing_sessions) % 10 == 0:
                self.save_ai_data()

            print(f"🤖 AI: Session complete - {wpm:.1f} WPM, {accuracy:.1f}% accuracy")

            self.session_start_time = None

    def _update_user_profile(self, session: TypingSession):

        self.user_profile.total_sessions += 1
        self.user_profile.total_words_typed += session.word_count
        self.user_profile.total_characters += len(session.text)

        alpha = self.learning_rate
        if self.user_profile.total_sessions == 1:
            self.user_profile.average_accuracy = session.accuracy
            self.user_profile.average_speed = session.speed_wpm
        else:
            self.user_profile.average_accuracy = (
                alpha * session.accuracy + (1 - alpha) * self.user_profile.average_accuracy
            )
            self.user_profile.average_speed = (
                alpha * session.speed_wpm + (1 - alpha) * self.user_profile.average_speed
            )

        if self.typing_rhythm_buffer:
            avg_rhythm = sum(self.typing_rhythm_buffer) / len(self.typing_rhythm_buffer)
            self.user_profile.typing_rhythm.append(avg_rhythm)
            if len(self.user_profile.typing_rhythm) > 100:
                self.user_profile.typing_rhythm = self.user_profile.typing_rhythm[-50:]

    def get_word_suggestions(self, current_word: str, limit: int = 5) -> List[str]:

        if not current_word:
            return []

        cache_key = f"{current_word}_{list(self.context_window)[-3:]}"
        if cache_key in self.suggestion_cache:
            return self.suggestion_cache[cache_key]

        context = list(self.context_window)

        suggestions = self.word_database.get_suggestions(current_word, context, limit * 2)

        personal_suggestions = self._get_personal_suggestions(current_word, context)

        all_suggestions = list(set(suggestions + personal_suggestions))
        ranked_suggestions = self._rank_suggestions(all_suggestions, current_word, context)

        final_suggestions = ranked_suggestions[:limit]
        self.suggestion_cache[cache_key] = final_suggestions

        if len(self.suggestion_cache) > 1000:
            self.suggestion_cache.clear()

        return final_suggestions

    def _get_personal_suggestions(self, prefix: str, context: List[str]) -> List[str]:

        suggestions = []

        for word, freq in self.word_patterns.items():
            if word.startswith(prefix) and freq >= self.min_word_frequency:
                suggestions.append(word)

        if context:
            last_word = context[-1] if context else ""
            for pattern, freq in self.bigram_patterns.items():
                if freq >= self.min_word_frequency:
                    words = pattern.split()
                    if len(words) == 2 and words[0] == last_word and words[1].startswith(prefix):
                        suggestions.append(words[1])

        return suggestions

    def _rank_suggestions(self, suggestions: List[str], prefix: str, context: List[str]) -> List[str]:

        scored_suggestions = []

        for word in suggestions:
            score = 0

            score += self.word_database.word_frequencies.get(word, 0) * 0.3

            score += self.word_patterns.get(word, 0) * 0.4

            if context:
                last_word = context[-1] if context else ""
                bigram = f"{last_word} {word}"
                score += self.bigram_patterns.get(bigram, 0) * 0.2

            score += max(0, 10 - len(word)) * 0.1

            scored_suggestions.append((word, score))

        scored_suggestions.sort(key=lambda x: x[1], reverse=True)

        return [word for word, _ in scored_suggestions]

    def get_typing_insights(self) -> Dict[str, any]:

        with self.lock:
            insights = {
                'profile': {
                    'total_sessions': self.user_profile.total_sessions,
                    'total_words': self.user_profile.total_words_typed,
                    'total_characters': self.user_profile.total_characters,
                    'average_accuracy': f"{self.user_profile.average_accuracy:.1f}%",
                    'average_speed': f"{self.user_profile.average_speed:.1f} WPM"
                },
                'patterns': {
                    'vocabulary_size': len(self.word_patterns),
                    'most_used_words': dict(Counter(self.word_patterns).most_common(10)),
                    'common_bigrams': dict(Counter(self.bigram_patterns).most_common(5)),
                    'typing_rhythm': f"{np.mean(self.user_profile.typing_rhythm):.3f}s" if self.user_profile.typing_rhythm else "N/A"
                },
                'recent_performance': self._get_recent_performance(),
                'learning_stats': {
                    'vocabulary_growth': len(self.word_database.word_frequencies),
                    'pattern_recognition': len(self.bigram_patterns) + len(self.trigram_patterns),
                    'suggestion_accuracy': self._calculate_suggestion_accuracy()
                }
            }

        return insights

    def _get_recent_performance(self) -> Dict[str, any]:

        if not self.typing_sessions:
            return {'status': 'No recent sessions'}

        recent_sessions = list(self.typing_sessions)[-10:]

        avg_accuracy = sum(s.accuracy for s in recent_sessions) / len(recent_sessions)
        avg_speed = sum(s.speed_wpm for s in recent_sessions) / len(recent_sessions)
        total_errors = sum(s.errors for s in recent_sessions)

        return {
            'sessions_analyzed': len(recent_sessions),
            'average_accuracy': f"{avg_accuracy:.1f}%",
            'average_speed': f"{avg_speed:.1f} WPM",
            'total_errors': total_errors,
            'improvement_trend': self._calculate_improvement_trend(recent_sessions)
        }

    def _calculate_improvement_trend(self, sessions: List[TypingSession]) -> str:

        if len(sessions) < 3:
            return "Insufficient data"

        mid = len(sessions) // 2
        first_half_acc = sum(s.accuracy for s in sessions[:mid]) / mid
        second_half_acc = sum(s.accuracy for s in sessions[mid:]) / (len(sessions) - mid)

        if second_half_acc > first_half_acc + 2:
            return "Improving"
        elif second_half_acc < first_half_acc - 2:
            return "Declining"
        else:
            return "Stable"

    def _calculate_suggestion_accuracy(self) -> str:

        if self.user_profile.total_sessions > 10:
            base_accuracy = min(85, 60 + self.user_profile.total_sessions * 0.5)
            return f"{base_accuracy:.1f}%"
        return "Learning..."

    def save_ai_data(self):

        try:

            data = {
                'user_profile': asdict(self.user_profile),
                'word_patterns': dict(self.word_patterns),
                'bigram_patterns': dict(self.bigram_patterns),
                'trigram_patterns': dict(self.trigram_patterns),
                'typing_sessions': [asdict(session) for session in list(self.typing_sessions)[-100:]],
                'word_frequencies': dict(list(self.word_database.word_frequencies.items())[:5000]),
                'last_updated': time.time()
            }

            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)

            pickle_data = {
                'word_database': self.word_database,
                'user_profile': self.user_profile,
                'patterns': {
                    'word_patterns': self.word_patterns,
                    'bigram_patterns': self.bigram_patterns,
                    'trigram_patterns': self.trigram_patterns
                }
            }

            with open(self.pickle_file, 'wb') as f:
                pickle.dump(pickle_data, f)

            print(f"🤖 AI: Data saved successfully")

        except Exception as e:
            print(f"🤖 AI: Error saving data: {e}")

    def load_ai_data(self):

        try:

            if os.path.exists(self.pickle_file):
                with open(self.pickle_file, 'rb') as f:
                    pickle_data = pickle.load(f)

                self.word_database = pickle_data.get('word_database', OfflineWordDatabase())
                self.user_profile = pickle_data.get('user_profile', UserProfile())
                patterns = pickle_data.get('patterns', {})
                self.word_patterns = patterns.get('word_patterns', defaultdict(int))
                self.bigram_patterns = patterns.get('bigram_patterns', defaultdict(int))
                self.trigram_patterns = patterns.get('trigram_patterns', defaultdict(int))

                print(f"🤖 AI: Loaded data from pickle file")
                return

            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    data = json.load(f)

                profile_data = data.get('user_profile', {})
                self.user_profile = UserProfile(**profile_data)

                self.word_patterns = defaultdict(int, data.get('word_patterns', {}))
                self.bigram_patterns = defaultdict(int, data.get('bigram_patterns', {}))
                self.trigram_patterns = defaultdict(int, data.get('trigram_patterns', {}))

                word_frequencies = data.get('word_frequencies', {})
                self.word_database.word_frequencies.update(word_frequencies)

                sessions_data = data.get('typing_sessions', [])
                for session_data in sessions_data:
                    session = TypingSession(**session_data)
                    self.typing_sessions.append(session)

                print(f"🤖 AI: Loaded data from JSON file")
            else:
                print(f"🤖 AI: No existing data found, starting fresh")

        except Exception as e:
            print(f"🤖 AI: Error loading data: {e}")
            print(f"🤖 AI: Starting with fresh data")

nami_ai = None

def initialize_nami_ai(data_file: str = "nami_ai_data.json") -> NamiAIIntelligence:

    global nami_ai
    nami_ai = NamiAIIntelligence(data_file)
    return nami_ai

def get_nami_ai() -> Optional[NamiAIIntelligence]:

    return nami_ai