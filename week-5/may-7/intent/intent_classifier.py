"""Intent classification module with predefined intents."""
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

if __name__ == "__main__":
    classifier = IntentClassifier()
    # Example usage
    text = "at what time according to the ist the california get sunrise"
    intent = classifier.detect(text)
    if intent:
        response = classifier.get_response(intent)
        print(f"Intent: {intent}, Response: {response}")
    else:
        print("No intent detected.")
