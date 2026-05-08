"""Fuzzy matcher module that falls back to similar commands."""
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


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    matcher = FuzzyMatcher(threshold=0.7)
    
    test_choices = [
        "hello",
        "world",
        "fuzzy",
        "matcher",
        "testing"
    ]
    
    test_cases = [
        "helo",
        "wrld",
        "fuzz",
        "match",
        "test"
    ]
    
    print("Testing FuzzyMatcher:")
    print("-" * 50)
    for test in test_cases:
        result = matcher.match(test, test_choices)
        print(f"Input: '{test}' -> Match: '{result}'")
