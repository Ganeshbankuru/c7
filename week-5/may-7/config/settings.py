"""Configuration settings for the voice assistant."""
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
