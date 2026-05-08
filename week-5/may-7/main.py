"""Main entry point for the voice assistant application."""
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
    """Core workflow manager for the voice assistant."""

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

        self.logger.info(f"Recognized text: {text}")
        name = self.name_extractor.extract(text)
        if name:
            self.logger.info(f"Extracted name: {name}")

        intent = self.intent_classifier.detect(text)
        if not intent:
            self.logger.info("Attempting fuzzy fallback.")
            match = self.fuzzy_matcher.match(
                text, self.intent_classifier.get_all_patterns()
            )
            if match:
                intent = self.intent_classifier.intent_for_pattern(match)
                self.logger.info(f"Fuzzy fallback matched intent: {intent}")

        response = self._build_response(text, intent)
        self.logger.info(f"Assistant response: {response}")
        self.tts.speak(response)

    def run(self) -> None:
        self.logger.info("Voice assistant started.")
        print("Voice assistant is running. Press Ctrl+C to exit.")
        try:
            while True:
                self.process_audio()
        except KeyboardInterrupt:
            self.logger.info("Voice assistant stopped by user.")
            print("\nGoodbye!")
        except Exception as error:
            self.logger.exception("Unexpected error:")
            sys.exit(1)

def main() -> None:
    setup_logging("voice_assistant")
    assistant = VoiceAssistant()
    assistant.run()

if __name__ == "__main__":
    main()
