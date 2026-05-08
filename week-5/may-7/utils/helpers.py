"""Helper utilities used across the voice assistant."""
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
