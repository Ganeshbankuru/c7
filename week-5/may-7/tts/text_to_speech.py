"""Text-to-speech module using gTTS."""
import logging
from pathlib import Path
from typing import Optional

from gtts import gTTS
import pygame

def play_audio(file_path: str) -> None:
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pass

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
            if output_path.exists():
                output_path.unlink()
                logger.info("Deleted existing TTS file %s", output_path)
            tts = gTTS(text=text, lang=self.language, slow=False)
            tts.save(str(output_path))
            logger.info("Saved TTS file to %s", output_path)
            play_audio(str(output_path))
            return True
        except Exception as error:
            logger.error("TTS generation or playback failed: %s", error)
            return False
if __name__ == "__main__":
    tts = TextToSpeech()
    tts.speak("Hi man, u look so ugly, u need to go to the gym")
