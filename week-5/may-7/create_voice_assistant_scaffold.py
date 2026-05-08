from pathlib import Path
from textwrap import dedent

base = Path(r"d:\fire-house\week-5\may-7")
base.mkdir(parents=True, exist_ok=True)

dirs = ["audio", "speech", "tts", "llm", "intent", "utils", "config"]
for d in dirs:
    (base / d).mkdir(parents=True, exist_ok=True)

for d in ["speech", "tts", "llm", "intent", "utils", "config"]:
    (base / d / "__init__.py").write_text("", encoding="utf-8")

files = {
    "main.py": dedent(
        """\
        \"\"\"Main entry point for the voice assistant application.\"\"\"
        import logging
        import sys
        from typing import Optional

        from config.settings import Settings
        from intent.intent_classifier import IntentClassifier
        from intent.name_extractor import NameExtractor
        from intent.fuzzy_matcher import FuzzyMatcher
        from llm.ollama_client import OllamaClient
        from speech.speech_to_text import SpeechRecognizer
        from tts.text_to_speech import TextToSpeech
        from utils.helpers import setup_logging

        class VoiceAssistant:
            \"\"\"Core workflow manager for the voice assistant.\"\"\"

            def __init__(self, settings: Optional[Settings] = None) -> None:
                self.settings = settings or Settings()
                self.logger = setup_logging("voice_assistant", self.settings.LOG_LEVEL)
                self.speech_recognizer = SpeechRecognizer(timeout=self.settings.SPEECH_TIMEOUT)
                self.tts = TextToSpeech(
                    audio_folder=self.settings.AUDIO_FOLDER,
                    filename=self.settings.TEMP_AUDIO_NAME,
                    language=self.settings.LANGUAGE,
                )
                self.intent_classifier = IntentClassifier()
                self.name_extractor = NameExtractor()
                self.fuzzy_matcher = FuzzyMatcher(self.settings.FUZZY_THRESHOLD)
                self.ollama_client = OllamaClient(
                    url=self.settings.OLLAMA_URL,
                    model=self.settings.MODEL_NAME,
                    timeout=self.settings.RESPONSE_TIMEOUT,
                )

            def _build_response(self, text: str, intent: Optional[str]) -> str:
                if intent:
                    return self.intent_classifier.get_response(intent)
                self.logger.info("No intent detected, using Ollama fallback.")
                response = self.ollama_client.generate_response(text)
                return response or "I could not understand that. Please try again."

            def process_audio(self) -> None:
                self.logger.info("Listening for speech...")
                text = self.speech_recognizer.recognize()
                if not text:
                    self.logger.warning("No speech recognized.")
                    return

                self.logger.info(f\"Recognized text: {text}\")
                name = self.name_extractor.extract(text)
                if name:
                    self.logger.info(f\"Extracted name: {name}\")

                intent = self.intent_classifier.detect(text)
                if not intent:
                    self.logger.info("Attempting fuzzy fallback.")
                    match = self.fuzzy_matcher.match(
                        text, self.intent_classifier.get_all_patterns()
                    )
                    if match:
                        intent = self.intent_classifier.intent_for_pattern(match)
                        self.logger.info(f\"Fuzzy fallback matched intent: {intent}\")

                response = self._build_response(text, intent)
                self.logger.info(f\"Assistant response: {response}\")
                self.tts.speak(response)

            def run(self) -> None:
                self.logger.info("Voice assistant started.")
                print("Voice assistant is running. Press Ctrl+C to exit.")
                try:
                    while True:
                        self.process_audio()
                except KeyboardInterrupt:
                    self.logger.info("Voice assistant stopped by user.")
                    print("\\nGoodbye!")
                except Exception as error:
                    self.logger.exception("Unexpected error:")
                    sys.exit(1)

        def main() -> None:
            setup_logging("voice_assistant")
            assistant = VoiceAssistant()
            assistant.run()

        if __name__ == "__main__":
            main()
        """
    ),
    "requirements.txt": dedent(
        """\
        SpeechRecognition>=3.10.0
        gTTS>=2.3.2
        requests>=2.31.0
        rapidfuzz>=3.6.0
        python-dotenv>=1.0.0
        playsound>=1.3.0
        """
    ),
    "README.md": dedent(
        """\
        # Voice Assistant

        A clean, modular Python voice assistant scaffold with:
        - Speech-to-text using `SpeechRecognition`
        - Text-to-speech using `gTTS`
        - Ollama API integration with `gemma3:1b`
        - Intent detection and fuzzy fallback
        - Name extraction and configurable settings

        ## Setup

        1. Open a terminal in this folder:
           ```powershell
           cd d:\\fire-house\\week-5\\may-7
           ```

        2. Create and activate a virtual environment:
           ```powershell
           python -m venv venv
           .\\venv\\Scripts\\activate
           ```

        3. Install dependencies:
           ```powershell
           pip install -r requirements.txt
           ```

        4. Copy the environment example:
           ```powershell
           copy .env.example .env
           ```

        5. Edit `.env` if needed, then run:
           ```powershell
           python main.py
           ```

        ## Structure

        - `main.py` — main application workflow
        - `speech/` — speech recognition
        - `tts/` — text-to-speech
        - `llm/` — Ollama client
        - `intent/` — intent classifier, name extractor, fuzzy matcher
        - `utils/` — helper utilities
        - `config/` — settings and config
        - `audio/` — temporary audio output

        ## Notes

        - `audio/` stores generated MP3 files
        - `.env` is ignored by git
        - Use local Ollama API URL in `.env`
        """
    ),
    ".gitignore": dedent(
        """\
        __pycache__/
        *.py[cod]
        *.pyo
        *.pyd
        venv/
        ENV/
        env/
        .env
        audio/*.mp3
        .vscode/
        .idea/
        """
    ),
    ".env.example": dedent(
        """\
        OLLAMA_URL=http://localhost:11434
        MODEL_NAME=gemma3:1b
        FUZZY_THRESHOLD=0.7
        LANGUAGE=en
        AUDIO_FOLDER=audio
        TEMP_AUDIO_NAME=response.mp3
        SPEECH_TIMEOUT=5
        RESPONSE_TIMEOUT=30
        LOG_LEVEL=INFO
        """
    ),
    "config/settings.py": dedent(
        """\
        \"\"\"Configuration settings for the voice assistant.\"\"\"
        import os
        from dataclasses import dataclass
        from dotenv import load_dotenv

        load_dotenv()

        @dataclass
        class Settings:
            OLLAMA_URL: str = os.getenv("OLLAMA_URL", "http://localhost:11434")
            MODEL_NAME: str = os.getenv("MODEL_NAME", "gemma3:1b")
            FUZZY_THRESHOLD: float = float(os.getenv("FUZZY_THRESHOLD", "0.7"))
            LANGUAGE: str = os.getenv("LANGUAGE", "en")
            AUDIO_FOLDER: str = os.getenv("AUDIO_FOLDER", "audio")
            TEMP_AUDIO_NAME: str = os.getenv("TEMP_AUDIO_NAME", "response.mp3")
            SPEECH_TIMEOUT: int = int(os.getenv("SPEECH_TIMEOUT", "5"))
            RESPONSE_TIMEOUT: int = int(os.getenv("RESPONSE_TIMEOUT", "30"))
            LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
        """
    ),
    "utils/helpers.py": dedent(
        """\
        \"\"\"Helper utilities used across the voice assistant.\"\"\"
        import logging
        import sys
        from pathlib import Path
        from typing import Optional

        def setup_logging(name: str, level: str = "INFO") -> logging.Logger:
            logger = logging.getLogger(name)
            if not logger.handlers:
                handler = logging.StreamHandler(sys.stdout)
                formatter = logging.Formatter(
                    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                )
                handler.setFormatter(formatter)
                logger.addHandler(handler)
            logger.setLevel(level)
            return logger

        def ensure_folder_exists(path: str) -> Path:
            folder = Path(path)
            folder.mkdir(parents=True, exist_ok=True)
            return folder

        def normalize_text(text: Optional[str]) -> str:
            return text.strip() if text else ""
        """
    ),
    "speech/speech_to_text.py": dedent(
        """\
        \"\"\"Speech recognition module that captures audio from the microphone.\"\"\"
        import logging
        from typing import Optional

        import speech_recognition as sr

        logger = logging.getLogger(__name__)

        class SpeechRecognizer:
            def __init__(self, timeout: int = 5) -> None:
                self.recognizer = sr.Recognizer()
                self.timeout = timeout

            def recognize(self, audio_path: Optional[str] = None) -> Optional[str]:
                try:
                    if audio_path:
                        with sr.AudioFile(audio_path) as source:
                            audio_data = self.recognizer.record(source)
                    else:
                        with sr.Microphone() as source:
                            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                            audio_data = self.recognizer.listen(source, timeout=self.timeout)

                    text = self.recognizer.recognize_google(audio_data)
                    logger.info("Recognized speech: %s", text)
                    return text.strip()
                except sr.WaitTimeoutError:
                    logger.warning("Listening timed out.")
                except sr.UnknownValueError:
                    logger.warning("Speech was not understood.")
                except sr.RequestError as error:
                    logger.error("Speech recognition request error: %s", error)
                except OSError as error:
                    logger.error("Microphone error: %s", error)
                return None
        """
    ),
    "tts/text_to_speech.py": dedent(
        """\
        \"\"\"Text-to-speech module using gTTS.\"\"\"
        import logging
        from pathlib import Path
        from typing import Optional

        from gtts import gTTS
        from playsound import playsound

        from utils.helpers import ensure_folder_exists

        logger = logging.getLogger(__name__)

        class TextToSpeech:
            def __init__(self, audio_folder: str = "audio", filename: str = "response.mp3", language: str = "en") -> None:
                self.audio_folder = ensure_folder_exists(audio_folder)
                self.filename = filename
                self.language = language

            def speak(self, text: str) -> bool:
                if not text:
                    logger.warning("No text provided for TTS.")
                    return False

                try:
                    output_path = self.audio_folder / self.filename
                    tts = gTTS(text=text, lang=self.language, slow=False)
                    tts.save(str(output_path))
                    logger.info("Saved TTS file to %s", output_path)
                    playsound(str(output_path))
                    return True
                except Exception as error:
                    logger.error("TTS generation or playback failed: %s", error)
                    return False
        """
    ),
    "llm/ollama_client.py": dedent(
        """\
        \"\"\"Ollama client module for local LLM inference.\"\"\"
        import logging
        from typing import Optional

        import requests

        logger = logging.getLogger(__name__)

        class OllamaClient:
            def __init__(self, url: str, model: str, timeout: int = 30) -> None:
                self.url = url.rstrip("/")
                self.model = model
                self.timeout = timeout

            def generate_response(self, prompt: str) -> Optional[str]:
                payload = {"model": self.model, "prompt": prompt, "stream": False}
                try:
                    response = requests.post(
                        f"{self.url}/api/generate",
                        json=payload,
                        timeout=self.timeout,
                    )
                    response.raise_for_status()
                    data = response.json()
                    if isinstance(data, dict):
                        return data.get("response") or data.get("text") or ""
                    return ""
                except Exception as error:
                    logger.error("Ollama request failed: %s", error)
                    return None
        """
    ),
    "intent/intent_classifier.py": dedent(
        """\
        \"\"\"Intent classification module with predefined intents.\"\"\"
        import logging
        from typing import Dict, List, Optional

        logger = logging.getLogger(__name__)

        class IntentClassifier:
            INTENTS: Dict[str, List[str]] = {
                "greeting": ["hello", "hi", "hey", "good morning"],
                "farewell": ["goodbye", "bye", "see you later"],
                "help": ["help", "assist", "support", "how do i"],
                "time": ["time", "current time", "what time"],
                "status": ["how are you", "how is it going"],
            }

            RESPONSES: Dict[str, str] = {
                "greeting": "Hello! I am your voice assistant. How can I help?",
                "farewell": "Goodbye! Feel free to ask me again anytime.",
                "help": "I can help with simple requests or pass your question to the language model.",
                "time": "I am not connected to a real clock yet, but I can still help with general questions.",
                "status": "I am running normally and ready for your next command.",
            }

            def detect(self, text: str) -> Optional[str]:
                normalized = text.lower()
                for intent, keywords in self.INTENTS.items():
                    if any(keyword in normalized for keyword in keywords):
                        logger.info("Detected intent: %s", intent)
                        return intent
                return None

            def get_response(self, intent: str) -> str:
                return self.RESPONSES.get(intent, "I am not sure how to answer that yet.")

            def get_all_patterns(self) -> List[str]:
                patterns: List[str] = []
                for keywords in self.INTENTS.values():
                    patterns.extend(keywords)
                return patterns

            def intent_for_pattern(self, phrase: str) -> Optional[str]:
                phrase_lower = phrase.lower()
                for intent, keywords in self.INTENTS.items():
                    if phrase_lower in [keyword.lower() for keyword in keywords]:
                        return intent
                return None
        """
    ),
    "intent/name_extractor.py": dedent(
        """\
        \"\"\"Name extraction module using regular expressions.\"\"\"
        import logging
        import re
        from typing import Optional

        logger = logging.getLogger(__name__)

        class NameExtractor:
            PATTERNS = [
                r"\\b(?:my name is|i am|i'm|this is)\\s+([A-Za-z]+)\\b",
                r"\\bname\\s+is\\s+([A-Za-z]+)\\b",
            ]

            def extract(self, text: str) -> Optional[str]:
                for pattern in self.PATTERNS:
                    match = re.search(pattern, text, re.IGNORECASE)
                    if match:
                        name = match.group(1).strip()
                        logger.info("Extracted name: %s", name)
                        return name
                return None
        """
    ),
    "intent/fuzzy_matcher.py": dedent(
        """\
        \"\"\"Fuzzy matcher module that falls back to similar commands.\"\"\"
        import logging
        from typing import List, Optional

        logger = logging.getLogger(__name__)

        class FuzzyMatcher:
            def __init__(self, threshold: float = 0.7) -> None:
                self.threshold = threshold

            def match(self, text: str, choices: List[str]) -> Optional[str]:
                try:
                    from rapidfuzz import fuzz, process
                except ImportError as error:
                    logger.error("rapidfuzz is not installed: %s", error)
                    return None

                result = process.extractOne(
                    text,
                    choices,
                    scorer=fuzz.token_sort_ratio,
                )
                if result and len(result) >= 2:
                    choice, score, _ = result
                    similarity = score / 100.0
                    logger.info("Fuzzy matched %s with score %.2f", choice, similarity)
                    if similarity >= self.threshold:
                        return choice
                return None
        """
    ),
}

for relative_path, content in files.items():
    path = base / relative_path
    path.write_text(content, encoding="utf-8")

print("Created project scaffold in", base)