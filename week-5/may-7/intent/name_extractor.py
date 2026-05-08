"""Name extraction module using regular expressions."""
import logging
import re
from typing import List, Optional, Pattern

logger = logging.getLogger(__name__)

class NameExtractor:
    PATTERNS = [
        r"\b(?:my name is|i am|i'm|this is)\s+([A-Za-z]+)\b",
        r"\bname\s+is\s+([A-Za-z]+)\b",
    ]

    def __init__(self) -> None:
        self.compiled_patterns: List[Pattern[str]] = [re.compile(pattern, re.IGNORECASE) for pattern in self.PATTERNS]

    def extract(self, text: str) -> Optional[str]:
        for pattern in self.compiled_patterns:
            match = pattern.search(text)
            if match:
                name = match.group(1).strip()
                logger.info("Extracted name: %s", name)
                return name
        return None


if __name__ == "__main__":
    extractor = NameExtractor()
    samples = [
        "My name is Alice.",
        "Hello, I am Bob",
        "This is Carol",
        "name is Dave",
        "No name here",
    ]

    for sample in samples:
        result = extractor.extract(sample)
        print(f"Input: {sample!r} -> Extracted: {result}")
