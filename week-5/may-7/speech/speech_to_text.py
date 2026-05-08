"""Speech recognition module that captures audio from the microphone."""
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
                    self.recognizer.adjust_for_ambient_noise(source, duration=1)
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
    
if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    recognizer = SpeechRecognizer(timeout=5)

    print("Speech Recognition Test")
    print("-" * 40)
    print("Speak something into the microphone...")
    print("Listening...")

    result = recognizer.recognize()

    print("-" * 40)

    if result:
        print(f"Recognized Text: {result}")
    else:
        print("No speech recognized.")
